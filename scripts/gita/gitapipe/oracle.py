"""The oracle seam (prakriya TRANSLATION_PIPELINE_SPEC §0.6): grammar `analyze`, `derive`,
`split` and meaning `page`, implemented by prakriya `scripts/gita_kit/` (Vidyut behind the
grammar calls, non-authoritative). Nothing here chooses a reading; it calls, normalises to
the SCHEMAS.md shapes and caches.

Resolution order for each module, detected at runtime:
  1. in process: `scripts/gita_kit/<module>.py` imported with its functions;
  2. the CLI `python3 -I scripts/gita_kit/gita_kit.py <module> <op> …` (or `<module>.py <op>`),
     JSON on stdout;
  3. absent → OracleUnavailable with the paths looked at and what to install.
A fixture oracle (`load(fixture=PATH)`) serves tests from a JSON file of canned answers.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from . import common as C

ANALYSIS_KEYS = ("id", "form", "kind", "stem", "dhatu", "lakara", "prayoga", "purusha", "vacana", "linga",
                 "vibhakti", "krt", "taddhita", "source")
KINDS = {"tinanta", "subanta", "krdanta", "taddhitanta", "avyaya", "samasa"}


class OracleUnavailable(RuntimeError):
    pass


def _jsonable(x: Any) -> Any:
    """Dataclasses, enums and other objects from an in-process oracle → plain JSON values."""
    return json.loads(json.dumps(x, ensure_ascii=False, default=lambda o: (
        o.__dict__ if hasattr(o, "__dict__") else getattr(o, "name", str(o)))))


def normalise_analysis(a: dict, form: str | None = None) -> dict:
    """The oracle's dict kept whole (derive needs its own fields back), every SCHEMAS key present."""
    if not isinstance(a, dict):
        raise ValueError(f"analysis is not an object: {a!r}")
    out = dict(a)
    for k in ANALYSIS_KEYS:
        out.setdefault(k, None)
    out["form"] = out["form"] or form
    if not out["id"]:
        body = {k: out[k] for k in ANALYSIS_KEYS if k not in ("id", "source")}
        out["id"] = "pipe-" + C.canon_hash(body)[:16]
        out["id_assigned_by"] = "pipeline (the oracle returned no id)"
    return out


def normalise_split(c: Any, k: int) -> dict:
    if isinstance(c, list):
        toks, src, extra = c, "oracle", {}
    elif isinstance(c, dict):
        toks = next((c[n] for n in ("tokens", "padas", "split", "words") if isinstance(c.get(n), list)), None)
        if toks is None:
            raise ValueError(f"split candidate without tokens: {str(c)[:200]}")
        src = c.get("source") or "oracle"
        extra = {n: v for n, v in c.items() if n not in ("tokens", "padas", "split", "words", "source")}
    else:
        raise ValueError(f"split candidate of unknown shape: {c!r}")
    tokens = []
    for t in toks:
        if isinstance(t, str):
            tokens.append(t)
        elif isinstance(t, dict):
            tokens.append(next(t[n] for n in ("form", "text", "pada", "iast", "surface") if isinstance(t.get(n), str)))
        else:
            raise ValueError(f"split token of unknown shape: {t!r}")
    return {"id": c.get("id") if isinstance(c, dict) and c.get("id") else f"s{k}", "tokens": tokens, "source": src, **extra}


class Oracle:
    """Base: subclasses implement _analyze, _derive, _split, _page."""

    def __init__(self) -> None:
        self._a: dict[str, list[dict]] = {}
        self._d: dict[str, dict] = {}
        self._p: dict[tuple, dict] = {}

    def analyze(self, form: str) -> list[dict]:
        key = C.nfc(form)
        if key not in self._a:
            raw = self._analyze(key) or []
            self._a[key] = [normalise_analysis(a, key) for a in raw]
        return self._a[key]

    def derive(self, analysis: dict) -> dict | None:
        aid = analysis.get("id")
        if aid not in self._d:
            d = self._derive(analysis)
            self._d[aid] = d if isinstance(d, dict) else None
        return self._d[aid]

    def split(self, locus: str) -> list[dict]:
        return [normalise_split(c, k) for k, c in enumerate(self._split(locus) or [])]

    def page(self, lemma: str, root: str | None = None) -> dict:
        key = (C.nfc(lemma), C.nfc(root or ""))
        if key not in self._p:
            self._p[key] = self._page(*key[:1], root or None)
        return self._p[key]

    def identity(self) -> dict:
        return {"oracle": type(self).__name__}


# ---------------------------------------------------------------- prakriya gita_kit
def _import_module(name: str):
    path = C.GITA_KIT / f"{name}.py"
    if not path.is_file():
        return None, f"{path} not found"
    for p in (str(C.GITA_KIT), str(C.LOOKUP_DIR)):
        if p not in sys.path:
            sys.path.append(p)
    try:
        spec = importlib.util.spec_from_file_location(f"gita_kit_{name}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, None
    except Exception as e:  # e.g. vidyut not importable in this interpreter
        return None, f"{path} failed to import in {sys.executable}: {type(e).__name__}: {e}"


class _VenvWorker:
    """The grammar module under the Vidyut venv, behind kit_worker.py (one process, engine loaded once)."""

    def __init__(self, python: Path) -> None:
        self.cmd = [str(python), "-I", str(Path(__file__).with_name("kit_worker.py")), str(C.GITA_KIT)]
        self.p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                  text=True, encoding="utf-8", cwd=str(C.PRAKRIYA))
        hello = self.p.stdout.readline()
        if not hello.strip().startswith('{"ready"'):
            raise OracleUnavailable(f"grammar worker did not start: {' '.join(self.cmd)}")

    def call(self, op: str, *args):
        self.p.stdin.write(json.dumps({"op": op, "args": list(args)}, ensure_ascii=False) + "\n")
        self.p.stdin.flush()
        line = self.p.stdout.readline()
        if not line:
            raise OracleUnavailable(f"grammar worker died during {op} {str(args)[:120]}")
        r = json.loads(line)
        if "error" in r:
            raise OracleError(f"grammar.{op}{tuple(str(a)[:60] for a in args)}: {r['error']}")
        return r["ok"]


class OracleError(RuntimeError):
    pass


class KitOracle(Oracle):
    def __init__(self, need_grammar: bool = True, need_meaning: bool = True, python: str | None = None) -> None:
        super().__init__()
        self.python = python or sys.executable
        self.notes: list[str] = []
        self.grammar = self.meaning = None
        self.grammar_cli = self.meaning_cli = None
        self.worker = None
        cli = C.GITA_KIT / "gita_kit.py"
        if need_grammar:
            mod, why = _import_module("grammar")
            if mod is not None and all(callable(getattr(mod, f, None)) for f in ("analyze", "derive", "split")):
                self.grammar = mod
            else:
                self.notes.append(why or f"{C.GITA_KIT}/grammar.py lacks analyze/derive/split")
                if (C.GITA_KIT / "grammar.py").is_file() and C.VIDYUT_PY.is_file():
                    try:
                        self.worker = _VenvWorker(C.VIDYUT_PY)
                    except OracleUnavailable as e:
                        self.notes.append(str(e))
                if self.worker is not None:
                    pass
                elif cli.is_file():
                    self.grammar_cli = [self.python, "-I", str(cli), "grammar"]
                elif (C.GITA_KIT / "grammar.py").is_file():
                    self.grammar_cli = [self.python, "-I", str(C.GITA_KIT / "grammar.py")]
            if self.grammar is None and self.worker is None and self.grammar_cli is None:
                raise OracleUnavailable(
                    "grammar oracle absent: neither prakriya/scripts/gita_kit/grammar.py (analyze, derive, split) "
                    f"nor gita_kit.py is usable ({'; '.join(self.notes)}). Stage A needs it for every analysis and "
                    "derivation; wait for the oracle or run with --without-grammar for a labelled partial build.")
        if need_meaning:
            mod, why = _import_module("meaning")
            if mod is not None and callable(getattr(mod, "page", None)):
                self.meaning = mod
            else:
                self.notes.append(why or f"{C.GITA_KIT}/meaning.py lacks page")
                if cli.is_file():
                    self.meaning_cli = [self.python, "-I", str(cli), "meaning"]
                elif (C.GITA_KIT / "meaning.py").is_file():
                    self.meaning_cli = [self.python, "-I", str(C.GITA_KIT / "meaning.py")]
            if self.meaning is None and self.meaning_cli is None:
                raise OracleUnavailable(
                    f"meaning oracle absent: prakriya/scripts/gita_kit/meaning.py (page) not usable ({'; '.join(self.notes)}).")

    # CLI calls: JSON on stdout; `--json` is retried when plain output is not JSON
    def _cli(self, base: list[str], args: list[str]) -> Any:
        for extra in ([], ["--json"]):
            r = subprocess.run(base + args + extra, capture_output=True, text=True, cwd=str(C.PRAKRIYA))
            if r.returncode == 0:
                try:
                    return json.loads(r.stdout)
                except json.JSONDecodeError:
                    continue
        raise OracleUnavailable(f"oracle CLI failed: {' '.join(base + args)}: {r.stderr.strip()[-400:]}")

    def _analyze(self, form):
        if self.worker:
            return self.worker.call("analyze", form)
        if self.grammar:
            return _jsonable(self.grammar.analyze(form))
        return self._cli(self.grammar_cli, ["analyze", form])

    def _derive(self, analysis):
        if self.worker:
            return self.worker.call("derive", analysis)
        if self.grammar:
            return _jsonable(self.grammar.derive(analysis))
        return self._cli(self.grammar_cli, ["derive", json.dumps(analysis, ensure_ascii=False)])

    def _split(self, locus):
        if self.worker:
            return self.worker.call("split", locus)
        if self.grammar:
            return _jsonable(self.grammar.split(locus))
        return self._cli(self.grammar_cli, ["split", locus])

    def _page(self, lemma, root):
        if self.meaning:
            return _jsonable(self.meaning.page(lemma, root) if root else self.meaning.page(lemma))
        return self._cli(self.meaning_cli, ["page", lemma] + (["--root", root] if root else []))

    def identity(self) -> dict:
        def ident(mod, cli, name):
            if name == "grammar" and self.worker is not None:
                p = C.GITA_KIT / "grammar.py"
                return {"mode": "venv-worker", "path": str(p), "sha256": C.sha256_file(p), "python": str(C.VIDYUT_PY)}
            if mod is not None:
                p = Path(mod.__file__)
                return {"mode": "in-process", "path": str(p), "sha256": C.sha256_file(p),
                        "version": getattr(mod, "VERSION", None) or getattr(mod, "ENGINE", None)}
            if cli is not None:
                return {"mode": "cli", "command": " ".join(cli)}
            return {"mode": "absent"}
        return {"oracle": "prakriya gita_kit", "grammar": ident(self.grammar, self.grammar_cli, "grammar"),
                "meaning": ident(self.meaning, self.meaning_cli, "meaning"), "notes": self.notes,
                "authority": "non-authoritative locating aids (vedanta standard §6.1)"}


class NoGrammar(KitOracle):
    """Meaning only; the grammar calls answer nothing. For a labelled partial stage A."""

    def __init__(self) -> None:
        KitOracle.__init__(self, need_grammar=False, need_meaning=True)

    def _analyze(self, form):
        return []

    def _derive(self, analysis):
        return None

    def _split(self, locus):
        return []

    def identity(self) -> dict:
        d = KitOracle.identity(self)
        d["grammar"] = {"mode": "absent", "note": "built with --without-grammar: no analyses, no derivations"}
        return d


class FixtureOracle(Oracle):
    """Canned answers: {"analyses": {form: [Analysis]}, "derivations": {id: Derivation},
    "splits": {locus: [SplitCandidate]}, "pages": {lemma: MeaningPage}}."""

    def __init__(self, path: Path | str) -> None:
        super().__init__()
        self.path = Path(path)
        self.data = C.read_json(self.path)

    def _analyze(self, form):
        a = self.data.get("analyses") or {}
        return a.get(form) or a.get(C.form_key(form)) or []

    def _derive(self, analysis):
        return (self.data.get("derivations") or {}).get(analysis.get("id"))

    def _split(self, locus):
        return (self.data.get("splits") or {}).get(locus) or []

    def _page(self, lemma, root):
        pages = self.data.get("pages") or {}
        return pages.get(lemma) or {"lemma": lemma, "root": root, "kosha": [], "dhatuvrtti": [], "nirukta": [],
                                    "dictionaries": {}, "concord": [], "site_renderings": []}

    def identity(self) -> dict:
        return {"oracle": "fixture", "path": str(self.path), "sha256": C.sha256_file(self.path)}


def load(fixture: str | None = None, without_grammar: bool = False) -> Oracle:
    if fixture:
        return FixtureOracle(fixture)
    if without_grammar:
        return NoGrammar()
    return KitOracle()

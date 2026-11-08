#!/usr/bin/env python3
"""Deterministic, idempotent migration of Gītā producer shards gita-producer-v1 → v2.

    python3 scripts/migrate_gita_producer_v2.py 12            # dry run: per-check counts before/after, per shard
    python3 scripts/migrate_gita_producer_v2.py 12 --write    # rewrite internal/sanskrit_reviews/gita/ch12/producer-*.json
    python3 scripts/migrate_gita_producer_v2.py --dir DIR     # any directory holding packet.json + producer-*.json

Only mechanical schema differences are migrated; content is never judged:
  - schema_version → gita-producer-v2; policy_sha256 → content hash of the current
    data/glossary/term_policy.json (the shard's `policy_version` label is kept);
  - word_class inferred from affix/morph/compound/root (name, copula, pronoun, particle, content);
  - evidence `kind` inferred from the locus path; `also` and `kashika` side-loci split into
    their own Kāśikā items (quote = the cited line, verbatim, at most 160 characters);
    `witness_note` appended to the claim; `locus_repaired` dropped;
  - `sutra` on Aṣṭādhyāyī items from the quote's number or the line's record, and on Kāśikā
    items from the paired sūtra item, the claim ("Kāśikā on 6.2.61") or the quote, in that
    order; never from the Kāśikā line itself (that would make B3 vacuous);
  - root_id from the Dhātupāṭha when exactly one record matches the card's root, gaṇa and
    pada, or, among several, the one record the card's own evidence cites; otherwise left
    unset and listed for a human.
Fallbacks are not migrated: whether one concerns a root, a pratyaya or a compound is a
judgement (audit B18), listed in the report.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_gita_chapter_reader as B  # noqa: E402

V2 = B.PRODUCER_SCHEMA
SUTRA_NUM = re.compile(r"(?<![\d.])([1-8])\.([1-4])\.(\d{1,3})(?![\d.])")
KASHIKA_CITE = re.compile(r"Kāśikā[^0-9\n]{0,12}([1-8]\.[1-4]\.\d{1,3})")
QUOTE_MAX = 160

KIND_BY_PATH = [
    ("ashtadhyayi", "sutra"), ("kashika", "kashika"), ("dhatupatha", "dhatupatha"), ("amarakosha", "kosha"),
    ("/kosha/", "kosha"), ("unadi", "unadi"), ("ganapatha", "ganapatha"), ("linganushasana", "linganushasana"),
    ("laghusiddhantakaumudi", "siddhantakaumudi"), ("siddhantakaumudi", "siddhantakaumudi"),
    ("bhagavadgita_mula", "mula"), ("_gita_bhasya", "commentary"), ("packet.json", "commentary"),
    ("data/glossary/", "glossary"), ("verses.js", "reader"),
]


def evidence_kind(locus: str) -> str:
    for needle, kind in KIND_BY_PATH:
        if needle in (locus or ""):
            return kind
    return "other"


def infer_word_class(w: dict) -> str:
    a = f"{w.get('affix', '')} {w.get('morph', '')}"
    if re.search(r"sambodhana|\bvoc\.|vocative|proper name|epithet", a, re.I):
        return "name"
    root = w.get("root") or ""
    if re.match(r"^√as\b", root) and "adādi" in root:
        return "copula"
    if w.get("compound"):
        return "content"
    if (w.get("stem") or "") in B_PRONOUN_STEMS or re.search(r"pronoun|sarvanāma", a, re.I):
        return "pronoun"
    if not root and re.search(r"avyaya|nipāta|indeclinable|particle", a, re.I):
        return "particle"
    return "content"


B_PRONOUN_STEMS = {"tad", "yad", "kim", "idam", "etad", "asmad", "yuṣmad", "adas", "mad", "tvad"}


class Tools:
    """What the migration reads: source lines, the Aṣṭādhyāyī line → sūtra table and the
    Dhātupāṭha. Tests pass doubles; the default reads the prakriya library."""

    def __init__(self, prakriya: Path = B.PRAKRIYA, root: Path = B.ROOT,
                 sutra_of_line: Callable[[int], str | None] | None = None,
                 dhatu_records: Callable[[str], list[dict]] | None = None,
                 attested: Callable[[str], bool | None] | None = None):
        self.sources = B.Sources(root, prakriya)
        self.prakriya = prakriya
        self._sutra_of_line = sutra_of_line
        self._dhatu_records = dhatu_records
        self._attested = attested
        self._attested_cache: dict[str, bool | None] = {}

    def attested(self, word: str) -> bool | None:
        """Does lookup.english_define find the word or phrase? None when it cannot answer."""
        if self._attested:
            return self._attested(word)
        if word not in self._attested_cache:
            try:
                d = self.prakriya / "scripts/lookup"
                if str(d) not in sys.path:
                    sys.path.insert(0, str(d))
                import lookup  # noqa: E402
                self._attested_cache[word] = B.define_result(lookup.english_define(word))["attested"]
            except BaseException:
                self._attested_cache[word] = None
        return self._attested_cache[word]

    def line(self, locus: str) -> str | None:
        pl = B.parse_locus(locus)
        if not pl or not pl["a"]:
            return None
        p = self.sources.resolve(pl["path"])
        if p is None:
            return None
        L = self.sources.lines(p)
        a = int(pl["a"])
        return L[a - 1] if 1 <= a <= len(L) else None

    def sutra_of_line(self, n: int) -> str | None:
        if self._sutra_of_line:
            return self._sutra_of_line(n)
        p = self.prakriya / "sources/raw/panini/sutrapatha/ashtadhyayi.json"
        if not p.is_file():
            return None
        data = self.sources.json(p)
        table = data.get("data", data) if isinstance(data, dict) else data
        if 1 <= n <= len(table):
            s = table[n - 1]
            return f"{s['a']}.{s['p']}.{s['n']}"
        return None

    def dhatu_records(self, root: str) -> list[dict]:
        """Dhātupāṭha records whose root (without anubandhas) is `root` (IAST, with or without √)."""
        if self._dhatu_records:
            return self._dhatu_records(root)
        p = self.prakriya / "sources/raw/panini/lexica/dhatupatha.json"
        tr = B._translit()
        if not p.is_file() or tr is None:
            return []
        bare = tr.transliterate(root.lstrip("√"), tr.IAST, tr.DEVANAGARI).rstrip("्")
        strip = lambda s: re.sub(r"[ँ-ॣ]", "", s or "").rstrip("्")  # noqa: E731
        out = []
        for d in self.sources.json(p)["data"]:
            if (d.get("dhatu") or "").rstrip("्") == bare or (d.get("aupadeshik") or "").rstrip("्") == bare or strip(d.get("aupadeshik")) == bare:
                out.append({"id": str(d["i"]), "gana": int(d["gana"]), "pada": d["pada"]})
        return out


def leading_sutra(text: str) -> str | None:
    m = re.match(r"\s*([1-8])\.([1-4])\.(\d{1,3})\b", text or "")
    return f"{m.group(1)}.{m.group(2)}.{int(m.group(3))}" if m else None


def quote_from_line(line: str | None) -> str:
    t = (line or "").strip()
    if len(t) <= QUOTE_MAX:
        return t
    cut = t[:QUOTE_MAX]
    sp = cut.rfind(" ")
    return cut[:sp] if sp > QUOTE_MAX // 2 else cut


def kashika_item(locus: str, sutra: str | None, quote: str | None, tools: Tools) -> dict:
    loc = re.sub(r"\s+\(.*\)$", "", locus.strip())
    item = {"claim": f"Kāśikā on {sutra}" if sutra else "Kāśikā", "locus": loc,
            "quote": quote or quote_from_line(tools.line(loc)), "kind": "kashika"}
    if sutra:
        item["sutra"] = sutra
    return item


def migrate_evidence(items: list, tools: Tools, todo: list[str], label: str) -> list:
    out: list = []
    prev_sutra: str | None = None
    for e in items:
        if not isinstance(e, dict):
            out.append(e)
            continue
        e = dict(e)
        e.pop("locus_repaired", None)
        note = e.pop("witness_note", None)
        if note:
            e["claim"] = f"{e.get('claim', '')} ({note})".strip()
        side = [(k, e.pop(k)) for k in ("also", "kashika") if k in e]
        side_quote = e.pop("kashika_quote", None)
        e.setdefault("kind", evidence_kind(e.get("locus", "")))
        if e["kind"] == "sutra" and not e.get("sutra"):
            pl = B.parse_locus(e.get("locus", ""))
            e["sutra"] = leading_sutra(e.get("quote", "")) or (tools.sutra_of_line(int(pl["a"])) if pl and pl["a"] else None)
            if not e["sutra"]:
                e.pop("sutra")
        if e["kind"] == "kashika" and not e.get("sutra"):
            m = KASHIKA_CITE.search(e.get("claim", "")) or KASHIKA_CITE.search(e.get("quote", ""))
            nums = {".".join(x) for x in SUTRA_NUM.findall(e.get("claim", ""))}
            sutra = (m.group(1) if m else None) or (next(iter(nums)) if len(nums) == 1 else None) or prev_sutra
            if sutra:
                e["sutra"] = sutra
            else:
                todo.append(f"{label}: Kāśikā item {e.get('locus')} — no sūtra in the claim, quote or a paired sūtra item")
        if e.get("sutra"):
            e["sutra"] = re.sub(r"\.0+(\d)", r".\1", e["sutra"])
        out.append({k: e[k] for k in ("claim", "locus", "quote", "sutra", "kind") if k in e} | {k: v for k, v in e.items() if k not in B.EVIDENCE_KEYS})
        if e["kind"] == "sutra":
            prev_sutra = e.get("sutra")
        elif e["kind"] != "kashika":
            prev_sutra = None
        for k, loc in side:
            if isinstance(loc, str) and B.parse_locus(re.sub(r"\s+\(.*\)$", "", loc.strip())):
                out.append(kashika_item(loc, e.get("sutra"), side_quote if k == "kashika" else None, tools))
            else:
                todo.append(f"{label}: `{k}` value is not a locus: {str(loc)[:80]}")
    return out


ROOT_RE = re.compile(r"^(?:[^\s;←]+\s*←\s*)?(√[^\s;]+)\s*(?:\([^),]*\)\s*)?\(([a-zā]+ādi),\s*(\d+)\s*([PAUĀ])\b")   # optional upadeśa form: √i (iṇ) (adādi, 2P)


def resolve_root_id(w: dict, tools: Tools) -> tuple[str | None, str]:
    m = ROOT_RE.match(w.get("root") or "")
    if (w.get("root") or "").count("√") > 1 and not (w.get("root") or "").startswith("√"):
        # the card's own root is written first ('√yuj (rudhādi, 7U); satata …'); a string that
        # opens with a member's derivation ('hita ← √dhā …; bhūta ← √bhū …') does not say which root is the card's
        return None, f"root string opens with a member's derivation and names several roots ({w.get('root')[:80]!r})"
    if not m:
        return None, f"root string {w.get('root')!r} not in the form '√x (gaṇa, NP …)' (one root per card)"
    root, gnum, pada = m.group(1), int(m.group(3)), m.group(4).replace("Ā", "A")
    recs = [r for r in tools.dhatu_records(root) if r["gana"] == gnum and r["pada"] == pada]
    if len(recs) == 1:
        return f"dhatupatha.json#{recs[0]['id']}", "unique gaṇa+pada match"
    cited = {re.search(r"#(\d+)$", e.get("locus", "")).group(1) for e in w.get("evidence") or []
             if isinstance(e, dict) and "dhatupatha.json#" in e.get("locus", "") and re.search(r"#(\d+)$", e.get("locus", ""))}
    pick = [r for r in recs if r["id"] in cited]
    if len(pick) == 1:
        return f"dhatupatha.json#{pick[0]['id']}", "card's own cited record among several gaṇa+pada matches"
    return None, f"{len(recs)} Dhātupāṭha records match {root} gaṇa {gnum} pada {pada}" + (f" ({[r['id'] for r in recs]})" if recs else "")


def migrate_shard(sh: dict, policy_sha: str, tools: Tools) -> tuple[dict, dict]:
    """Return (migrated shard, notes). Idempotent: a v2 shard comes back unchanged."""
    out = copy.deepcopy(sh)
    notes = {"root_id_set": [], "root_id_todo": [], "evidence_todo": [], "fallbacks_untyped": [], "composed": []}
    out["schema_version"] = V2
    out["policy_sha256"] = policy_sha
    for v in out.get("verses") or []:
        for i, w in enumerate(v.get("words") or []):
            label = f"{v.get('locus')}[{i}] {w.get('iast')}"
            if w.get("word_class") not in B.WORD_CLASSES:
                w["word_class"] = infer_word_class(w)
            w["evidence"] = migrate_evidence(w.get("evidence") or [], tools, notes["evidence_todo"], label)
            if w.get("root") and not w.get("root_id"):
                rid, why = resolve_root_id(w, tools)
                if rid:
                    w["root_id"] = rid
                    notes["root_id_set"].append(f"{label}: {rid} ({why})")
                else:
                    notes["root_id_todo"].append(f"{label}: {why}")
            for c in (w.get("wording") or {}).get("candidates") or []:
                word = (c.get("word") or "") if isinstance(c, dict) else ""
                toks = re.findall(r"[^\W\d_][\w'\-]*", re.sub(r"\([^)]*\)", " ", word))   # annotations like '(adj.)' are not words
                if (len(toks) > 1 and B.ENGLISH_SOURCE_RE.search(str(c.get("source", "")))
                        and tools.attested(word) is False):
                    # a multi-word candidate define does not resolve: a phrase composed of its words (lead, 2026-11-08)
                    c["cited_source"] = c["source"]
                    c["source"] = "composed"
                    c["parts"] = [t.lower() for t in toks]
                    notes["composed"].append(f"{label}: '{word}'")
            for k, f in enumerate(w.get("fallback") or []):
                if not isinstance(f, dict) or not f.get("kind"):
                    notes["fallbacks_untyped"].append(f"{label} fallback[{k}]")
    return out, notes


def check_counts(chapter: int, chapter_dir: Path, root: Path, prakriya: Path) -> dict[str, dict[str, int]]:
    ctx = B.Ctx(chapter=chapter, root=root, prakriya=prakriya, chapter_dir=chapter_dir, run_render_contract=False)
    B.run(ctx)
    return ctx.report.counts_by_scope()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", type=int, nargs="?")
    ap.add_argument("--dir", type=Path, help="chapter directory (default internal/sanskrit_reviews/gita/chN)")
    ap.add_argument("--root", type=Path, default=B.ROOT)
    ap.add_argument("--prakriya", type=Path, default=B.PRAKRIYA)
    ap.add_argument("--write", action="store_true", help="rewrite the shards in place (default: dry run)")
    ap.add_argument("--no-counts", action="store_true", help="skip the before/after builder run")
    a = ap.parse_args(argv)
    d = a.dir or a.root / f"internal/sanskrit_reviews/gita/ch{a.chapter}"
    ch = a.chapter or json.loads((d / "packet.json").read_text(encoding="utf-8"))["chapter"]
    policy_sha = B.load_policy(a.root / "data/glossary/term_policy.json").sha256
    tools = Tools(a.prakriya, a.root)
    shards = sorted(d.glob("producer-*.json"))
    migrated, report = {}, {"policy_sha256": policy_sha, "shards": {}}
    for sp in shards:
        raw = sp.read_text(encoding="utf-8")
        new, notes = migrate_shard(json.loads(raw), policy_sha, tools)
        text = json.dumps(new, ensure_ascii=False, indent=1) + "\n"
        migrated[sp.name] = (raw, text)
        report["shards"][sp.name] = {"changed": json.loads(raw) != new, "root_id_set": len(notes["root_id_set"]),
                                     "candidates_composed": len(notes["composed"]),
                                     "root_id_todo": notes["root_id_todo"], "evidence_todo": notes["evidence_todo"],
                                     "fallbacks_untyped": notes["fallbacks_untyped"]}
    if not a.no_counts:
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            for f in d.iterdir():
                if f.is_file() and f.suffix == ".json":
                    shutil.copyfile(f, t / f.name)
            report["before"] = check_counts(ch, t, a.root, a.prakriya)
            for name, (_, text) in migrated.items():
                (t / name).write_text(text, encoding="utf-8")
            report["after"] = check_counts(ch, t, a.root, a.prakriya)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    if a.write:
        for name, (raw, text) in migrated.items():
            if json.loads(raw) != json.loads(text):
                (d / name).write_text(text, encoding="utf-8")
                print(f"written {d / name}", file=sys.stderr)
    else:
        print("dry run: nothing written (pass --write)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

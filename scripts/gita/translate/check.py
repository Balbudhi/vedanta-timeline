"""Exact checks on job outputs. Each returns a list of error strings (empty = pass)."""
from __future__ import annotations

import json
import re
from pathlib import Path

FUNCTION_WORDS = set("""a an the as at by for from in into of off on onto out over to up upon with within
this that these those he she it they them his her its their him who whom whose which what when where why how
there here be is are was were been being am do does did done have has had having will shall would should may might
must can could let i me my mine we us our you your yours thou thee thy o whoever whatever whoso""".split())
# Not function words (they render Sanskrit: na, eva, api, ca, sarva, sama …): not no none nor all any every each
# both only even also same very more most less least own such than and but or if then so.
GRAMMATICAL_FORKS = {"split", "analysis", "compound_type", "relation", "referent"}
CLASSES = {"content", "particle", "pronoun", "name", "copula"}
FORBIDDEN_READ = re.compile(r"secondaries|sanskrit_reviews|gita/ch\d|verses\.js|translation\.json|term_policy|"
                            r"cwsa19|essays-on-the-gita|gita_briefs|internal/gita_pipeline/(?!packets|run)")


def words_of(s: str) -> list[str]:
    return [w.lower().strip("'’-") for w in re.findall(r"[A-Za-zĀ-ž'’-]+", s or "") if w.strip("'’-")]


def _loss_complete(lost: list) -> list[str]:
    errs = []
    for l in lost or []:
        for k in ("component", "existing_searched", "new_attempted", "preserved_fails"):
            if not str(l.get(k) or "").strip():
                errs.append(f"loss '{l.get('component')}' lacks {k} (a loss needs the full three-step showing)")
    return errs


def construe(out: dict, inp: dict) -> list[str]:
    errs = []
    cand = {w["i"]: {c["id"] for c in w["candidates"]} for w in inp["words"]}
    padas = {w["i"]: w.get("padas") or [] for w in inp["words"]}
    got = {w["i"]: w for w in out.get("words", [])}
    for i in cand:
        w = got.get(i)
        if not w:
            errs.append(f"word {i} ({inp['words'][i]['form']}) has no construal")
            continue
        if w.get("analysis_id") and w["analysis_id"] not in cand[i]:
            errs.append(f"word {i}: analysis_id {w['analysis_id']} is not a candidate")
        if not w.get("analysis_id") and not w.get("manual"):
            errs.append(f"word {i}: neither analysis_id nor manual")
        given = (w.get("manual") or {}).get("padas") or []
        if len(padas[i]) > 1 and not w.get("analysis_id") and len(given) != len(padas[i]):
            errs.append(f"word {i}: a token of {len(padas[i])} padas {padas[i]} needs manual.padas with one entry each")
        for pd in given:
            if isinstance(pd, dict) and pd.get("analysis_id") and pd["analysis_id"] not in cand[i]:
                errs.append(f"word {i}: pada analysis_id {pd['analysis_id']} is not a candidate")
        if w.get("word_class") not in CLASSES:
            errs.append(f"word {i}: word_class {w.get('word_class')!r} not in {sorted(CLASSES)}")
        if not w.get("stem"):
            errs.append(f"word {i}: no stem (for a verb give its root without √)")
        if w.get("root") and not re.fullmatch(r"√[^\s,;()+]+", w["root"]):
            errs.append(f"word {i}: root must be the bare root with √ (e.g. '√āp'), got {w['root']!r}")
    for f in out.get("forks", []):
        if f.get("kind") not in GRAMMATICAL_FORKS | {"doctrine"}:
            errs.append(f"fork {f.get('words')}: kind must be one of {sorted(GRAMMATICAL_FORKS | {'doctrine'})}")
    if not isinstance(out.get("continues_into_next"), bool):
        errs.append("continues_into_next must be true or false")
    return errs


def lexicon(out: dict, inp: dict, calls: list[dict]) -> list[str]:
    errs = []
    cmds = [c["cmd"] for c in calls]
    if "english" not in cmds:
        errs.append("no `english` (find-by-meaning) search was run (W1)")
    defined = {" ".join(c["args"]).lower() for c in calls if c["cmd"] == "define"}
    for r in out.get("rows", []):
        sid = r.get("sense_id")
        if not r.get("default"):
            errs.append(f"{sid}: no default")
            continue
        rs = r.get("rendering_set") or []
        if not all(isinstance(x, dict) and x.get("english") and isinstance(x.get("carries"), list) for x in rs):
            errs.append(f"{sid}: rendering_set entries must be {{english, carries[]}}")
        elif r["default"] not in [x["english"] for x in rs]:
            errs.append(f"{sid}: default not in rendering_set")
        else:
            sig = set(r.get("signification") or [])
            dflt = next(x for x in rs if x["english"] == r["default"])
            unknown = set(dflt["carries"]) - sig
            if unknown:
                errs.append(f"{sid}: carries names components not in signification: {sorted(unknown)}")
            missing = sig - set(dflt["carries"])
            listed = {l.get("component") for l in r.get("loss") or []}
            if missing - listed:
                errs.append(f"{sid}: default does not carry {sorted(missing - listed)} and no loss showing is given (L1)")
        if r.get("form") != "preserved":
            heads = [w for w in words_of(r["default"]) if w not in FUNCTION_WORDS]
            if heads and not any(any(h in d for d in defined) for h in heads):
                errs.append(f"{sid}: default '{r['default']}' was never checked with `define` (W1)")
        if not r.get("searches"):
            errs.append(f"{sid}: no searches recorded (W1)")
        errs += [f"{sid}: {e}" for e in _loss_complete(r.get("loss"))]
    return errs


def verse(out: dict, inp: dict, rows: dict) -> list[str]:
    errs = []
    lines = out.get("lines") or {}
    for v in inp["verses"]:
        if not (lines.get(v["locus"]) or "").strip():
            errs.append(f"no line for {v['locus']}")
    by = {(w.get("locus"), w.get("i")): w for w in out.get("words", [])}
    rendered: set[str] = set()
    for w in out.get("words", []):
        rendered |= set(words_of(w.get("english")))
    for v in inp["verses"]:
        for cw in v["construal"]["words"]:
            if cw.get("word_class") not in ("content", "name", "particle", "pronoun"):
                continue
            w = by.get((v["locus"], cw["i"]))
            if not w or not (w.get("english") or "").strip():
                errs.append(f"{v['locus']} word {cw['i']} ({cw['form']}) is not rendered (L1)")
                continue
            errs += [f"{v['locus']} {cw['form']}: {e}" for e in _loss_complete(w.get("lost"))]
            sid = w.get("sense_id")
            row = rows.get(sid)
            if row:
                rs = [x for x in row.get("rendering_set", []) if isinstance(x, dict)]
                chosen = next((x for x in rs if x["english"] == w.get("rendering")), None)
                if not w.get("deviation") and chosen is None:
                    errs.append(f"{v['locus']} {cw['form']}: rendering '{w.get('rendering')}' is not exactly one of row {sid}'s renderings and no deviation is given (W6)")
                carried = set(w.get("deviation_carries") or []) if w.get("deviation") else set((chosen or {}).get("carries", []))
                missing = set(row.get("signification") or []) - carried - {l.get("component") for l in w.get("lost") or []}
                if missing:
                    errs.append(f"{v['locus']} {cw['form']}: rendering '{w['english']}' does not carry {sorted(missing)} (row {sid}); carry it or show the loss (L1)")
            if row and not w.get("deviation"):
                allowed = " | ".join([*(x["english"] for x in row.get("rendering_set", []) if isinstance(x, dict)), *map(str, (row.get("forms") or {}).values())]).lower()
                heads = [x for x in words_of(w["english"]) if x not in FUNCTION_WORDS]
                if heads and not any(h[:5] in allowed for h in heads):
                    errs.append(f"{v['locus']} {cw['form']}: '{w['english']}' is not in row {sid}'s renderings and no deviation is given (W6)")
    from collections import Counter
    for loc, line in lines.items():
        have = Counter(x for w in out.get("words", []) if w.get("locus") == loc for x in words_of(w.get("english"))
                       if x not in FUNCTION_WORDS)
        need = Counter(x for x in words_of(line) if x not in FUNCTION_WORDS)
        extra = need - have
        if extra:
            errs.append(f"{loc}: line words not assigned to any Sanskrit word of this verse: {sorted(extra.elements())} (L0 — add nothing)")
    alt = out.get("alternative")
    if alt:
        kinds = {f.get("kind") for v in inp["verses"] for f in v["construal"].get("forks", [])}
        if not kinds & GRAMMATICAL_FORKS:
            errs.append("a second line is given but the construal records no grammatical fork (M3)")
    return errs


def forbidden_reads(events_path: Path, tool: str = "scripts/gita/translate/tool.py") -> list[str]:
    hits = []
    if not events_path.exists():
        return hits
    for line in events_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        s = json.dumps(e, ensure_ascii=False)
        item = e.get("item") or {}
        if e.get("type") == "item.started" and item.get("type") == "command_execution":
            cmd = item.get("command") or ""
            m = FORBIDDEN_READ.search(cmd)
            if m:
                hits.append(f"forbidden source touched: {m.group(0)}")
            elif tool not in cmd and re.search(r"(?<![\w.])/(?!bin/zsh)[A-Za-z]", cmd):
                hits.append(f"command outside the job folder and the tool: {cmd[:120]}")
    return sorted(set(hits))

#!/usr/bin/env python3
"""Side by side: the pipeline's lines against the reference (gold) lines, per sentence unit, with
the word-level differences (content words only). Writes <run>/COMPARE.md (private).

    python3 scripts/gita/translate/compare.py --run ch15-heldout --gold internal/gita_pipeline/gold/ch15.md
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pipeline as P


def gold_lines(path: Path) -> dict[str, dict]:
    """'### 12.3–4' headings with **Line:** / **Second line:** -> {first locus: {line, second}}."""
    out, cur = {}, None
    for l in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^###\s+(\d+\.\d+)", l)
        if m:
            cur = out.setdefault(m.group(1), {"line": None, "second": None, "head": l[4:].strip()})
            continue
        if cur is not None:
            m = re.match(r"^\*\*(Line|Second line)[^*]*\*\*:?\s*(.*)", l)
            if m:
                key = "line" if m.group(1) == "Line" else "second"
                cur["_in"] = key if not m.group(2).strip() else None
                cur[key] = cur[key] or m.group(2).strip() or None
                continue
            m = re.match(r"^\d+\.\d+\s*[—-]\s*(.+)", l)  # a multi-verse line written per verse
            if m and cur.get("_in"):
                cur[cur["_in"]] = ((cur[cur["_in"]] or "") + " " + m.group(1).strip()).strip()
            elif not l.strip():
                cur["_in"] = cur.get("_in") if cur.get(cur.get("_in") or "line") is None else None
    return out


def content(text: str) -> list[str]:
    return [P.en_stem(t) for t in P.tokens(text or "") if t not in P.EN_FUNCTION]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--gold", required=True)
    a = ap.parse_args()
    gold = gold_lines(Path(a.gold))
    rows, overlap = [], []
    recs = [json.loads(f.read_text()) for f in (P.RUNS / a.run / "translate").glob("*.json") if not f.name.startswith("_")]
    recs.sort(key=lambda r: [int(x) for x in r["unit"][0].split(".")])
    for r in recs:
        lines = (r.get("output") or {}).get("lines") or {}
        mine = " ".join(lines.get(l, "") for l in r["unit"])
        g = gold.get(r["unit"][0]) or {}
        gl = g.get("line") or ""
        a_, b_ = set(content(mine)), set(content(gl))
        j = len(a_ & b_) / max(1, len(a_ | b_))
        overlap.append(j)
        rows.append(f"### {'–'.join(r['unit'])}\n\n- **gold:** {gl}\n- **pipeline:** {mine}\n"
                    f"- only in gold: {', '.join(sorted(b_ - a_)) or '—'}\n- only in pipeline: {', '.join(sorted(a_ - b_)) or '—'}\n"
                    f"- code errors left: {len(r.get('code_errors') or [])}; S1/S2 findings left: {len(r.get('review') or [])}\n")
    head = (f"# {a.run} against {Path(a.gold).name}\n\nUnits: {len(recs)}. Mean content-word overlap with the gold "
            f"(Jaccard, stems): {sum(overlap) / max(1, len(overlap)):.2f}. Overlap is a pointer to where to read, not a score.\n\n")
    out = P.RUNS / a.run / "COMPARE.md"
    out.write_text(head + "\n".join(rows), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

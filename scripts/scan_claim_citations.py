#!/usr/bin/env python3
"""Scan thinker JSONs for uncited claims.

Surfaces every value in defendable-claim fields that lacks a citation marker.
Citation marker patterns:
  - cite://thinker/work/locus  (canonical)
  - [ref|...]                  (alt form)
  - [[short]](<cite://...>)    (alt form)
  - ^N superscript (Unicode)
  - "citation" sub-field with non-empty value

A claim is "uncited" if the field's prose contains a substantive claim
but no citation marker is present.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path("/orcd/home/002/eeshan/worktrees/ui-fixes/claim-citation-phase3-1778607240")
THINKERS = ROOT / "data" / "thinkers"

CITE_PATS = [
    re.compile(r"cite://"),
    re.compile(r"\[ref\|"),
    re.compile(r"\[\[[^\]]+\]\]\(<cite://"),
    re.compile(r"[¹²³⁰-⁹]+"),  # superscript digits
]

DEFENDABLE_TEXT_FIELDS = [
    "dates_notes",
    "core_thesis",
    "school_affiliation_basis",
    "notes",
]

def has_citation(text: str) -> bool:
    if not text:
        return True  # empty: nothing to defend
    for pat in CITE_PATS:
        if pat.search(text):
            return True
    return False


def is_substantive(text: str) -> bool:
    if not text:
        return False
    # Heuristic: > 60 chars and not a single tag
    return len(text.strip()) > 60


def scan_file(path: Path) -> dict:
    data = json.loads(path.read_text())
    issues = []

    for field in DEFENDABLE_TEXT_FIELDS:
        v = data.get(field)
        if isinstance(v, str) and is_substantive(v) and not has_citation(v):
            issues.append({"field": field, "snippet": v[:240]})

    # key_moves: a list of strings or objects
    for i, mv in enumerate(data.get("key_moves", []) or []):
        if isinstance(mv, dict):
            text = mv.get("claim") or mv.get("text") or mv.get("description") or ""
        else:
            text = str(mv)
        if is_substantive(text) and not has_citation(text):
            issues.append({"field": f"key_moves[{i}]", "snippet": text[:240]})

    # engaged_works[*].claim / .summary
    for i, w in enumerate(data.get("engaged_works", []) or []):
        if not isinstance(w, dict):
            continue
        for sub in ("claim", "summary", "ascription_notes"):
            text = w.get(sub) or ""
            if is_substantive(text) and not has_citation(text):
                issues.append({
                    "field": f"engaged_works[{i}].{sub}",
                    "work_id": w.get("work_id") or w.get("title"),
                    "snippet": text[:200],
                })

    return {
        "thinker_id": data.get("id"),
        "issue_count": len(issues),
        "issues": issues,
    }


def main():
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    results = []
    for f in sorted(THINKERS.glob("*.json")):
        if only and f.stem not in only:
            continue
        try:
            r = scan_file(f)
        except Exception as e:
            results.append({"thinker_id": f.stem, "error": str(e)})
            continue
        if r["issue_count"]:
            results.append(r)

    out = {
        "total_thinkers_with_issues": len(results),
        "total_issues": sum(r.get("issue_count", 0) for r in results),
        "by_thinker": results,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

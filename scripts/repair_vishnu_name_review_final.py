#!/usr/bin/env python3
"""Apply concrete defects found by the independent 1,000-name reviewer."""

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "internal/sanskrit_reviews/name-analysis-review-501-750.json"
ANALYSIS = ROOT / "gita/vishnu-sahasranama/analysis.json"


def main() -> None:
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    base = json.loads(ANALYSIS.read_text(encoding="utf-8"))["names"]
    vanamali = copy.deepcopy(base[560])
    vanamali["parts"] = [
        {"form_iast": "vana", "gloss": "forest; woodland", "kind": "member"},
        {"form_iast": "mālin", "gloss": "garlanded; wearing a garland", "kind": "member"},
        {"form_iast": "su", "gloss": "marks nominative singular", "kind": "ending"},
    ]
    review["rows"]["561"] = {
        "status": "replace",
        "analysis": vanamali,
        "evidence": {"review": "independent second pass"},
        "notes": "Replaced two truncated dictionary extracts with lexical member glosses.",
    }
    yadu = review["rows"]["705"]["analysis"]
    next(part for part in yadu["parts"] if part["form_iast"] == "śreṣṭha")["gloss"] = "best; most excellent"
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"repaired_names": [561, 705]}))


if __name__ == "__main__":
    main()

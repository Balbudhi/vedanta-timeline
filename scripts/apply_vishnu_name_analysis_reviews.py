#!/usr/bin/env python3
"""Apply the four closed-population name-popup review shards."""

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "gita/vishnu-sahasranama"
ANALYSIS = BASE / "analysis.json"
REVIEWS = tuple(sorted((ROOT / "internal/sanskrit_reviews").glob("name-analysis-review-*.json")))


def main() -> None:
    data = json.loads(ANALYSIS.read_text(encoding="utf-8"))
    by_number = {row["number"]: row for row in data["names"]}
    replacements = 0
    reviewed = set()
    for path in REVIEWS:
        review = json.loads(path.read_text(encoding="utf-8"))
        for number_text, record in review["rows"].items():
            number = int(number_text)
            if number in reviewed:
                raise ValueError(f"duplicate reviewed name {number}")
            reviewed.add(number)
            if record["status"] == "replace":
                by_number[number] = copy.deepcopy(record["analysis"])
                replacements += 1
    if reviewed != set(range(1, 1001)):
        raise ValueError(f"name review population differs: missing={sorted(set(range(1,1001))-reviewed)}")
    data["names"] = [by_number[number] for number in range(1, 1001)]
    data["review_status"] = "primary-grammar-reviewed-complete"
    data["review_population"] = {
        "names": 1000,
        "source_first_replacements": replacements,
        "verified_unchanged": 1000 - replacements,
        "review_skill": "/Users/eeshan/.codex/skills/sanskrit-source-derivation-review/SKILL.md",
        "interpreter_used": False,
    }
    sources = data.setdefault("sources", {})
    sources["grammar_source_library"] = {
        "path": "/Users/eeshan/Dev/prakriya/sources",
        "manifest": "manifest/clean_witnesses.json",
        "authority": "direct source-text derivation; unfinished interpreter not used",
    }
    for key in ("monier_williams", "vidyut"):
        if key in sources:
            sources[key]["status"] = "historical-candidate-input-only; not public-analysis authority"
    ANALYSIS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reviewed": 1000, "replacements": replacements}, indent=2))


if __name__ == "__main__":
    main()

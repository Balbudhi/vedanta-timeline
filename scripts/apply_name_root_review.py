#!/usr/bin/env python3
"""Apply internally source-checked roots to the four name-review shards."""

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "gita/vishnu-sahasranama"
ANALYSIS = {row["number"]: row for row in json.loads((BASE / "analysis.json").read_text(encoding="utf-8"))["names"]}
REVIEWS = tuple(sorted((ROOT / "internal/sanskrit_reviews").glob("name-analysis-review-*.json")))
CLAIMS = tuple(sorted((ROOT / "internal/sanskrit_reviews").glob("root-claim-review-*.json")))
SKIP = {273}  # The independently parsed compound head is vi-√viś, not the challenged śipi claim.
GANA = {
    "1": "bhvādi (1)", "2": "adādi (2)", "3": "juhotyādi (3)",
    "4": "divādi (4)", "5": "svādi (5)", "6": "tudādi (6)",
    "7": "rudhādi (7)", "8": "tanādi (8)", "9": "kryādi (9)",
    "10": "curādi (10)",
}
PADA = {"P": "parasmaipada", "A": "ātmanepada", "U": "ubhayapada"}


def normalize_root(value: dict) -> dict:
    root = copy.deepcopy(value)
    root["gana"] = GANA.get(str(root.get("gana")), root.get("gana"))
    root["pada"] = PADA.get(str(root.get("pada")), root.get("pada"))
    return root


def main() -> None:
    derived = {}
    for path in CLAIMS:
        for row in json.loads(path.read_text(encoding="utf-8"))["rows"]:
            if row.get("independently_derived_root") and row["name_number"] not in SKIP:
                derived[row["name_number"]] = normalize_root(row["independently_derived_root"])
    applied = set()
    for path in REVIEWS:
        data = json.loads(path.read_text(encoding="utf-8"))
        for key, record in data["rows"].items():
            number = int(key)
            if number not in derived:
                continue
            if record["status"] == "verified-unchanged":
                record["status"] = "replace"
                record["analysis"] = copy.deepcopy(ANALYSIS[number])
            record["analysis"]["root"] = derived[number]
            record["analysis"]["evidence"]["dhatupatha"] = derived[number]["dhatupatha"]
            applied.add(number)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if applied != set(derived):
        raise ValueError(f"name-root application differs: missing={sorted(set(derived)-applied)}")
    print(json.dumps({"applied": len(applied), "skipped_internal_challenge": sorted(SKIP)}, indent=2))


if __name__ == "__main__":
    main()

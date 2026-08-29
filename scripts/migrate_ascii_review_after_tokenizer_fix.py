#!/usr/bin/env python3
"""Rebuild ASCII candidates and replay reviews by immutable source coordinates."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "internal/sanskrit_reviews"
INVENTORY = INTERNAL / "ascii-sanskrit-candidate-inventory.json"
REVIEWS = (
    (1, 250, INTERNAL / "ascii-sanskrit-review-001-250.json"),
    (251, 500, INTERNAL / "ascii-sanskrit-review-251-500.json"),
    (501, 750, INTERNAL / "ascii-sanskrit-review-501-750.json"),
    (751, 1000, INTERNAL / "ascii-sanskrit-review-751-1000.json"),
)


def coordinate(row: dict) -> tuple:
    return (
        int(row["name_number"]), int(row["paragraph_index"]),
        int(row["source_start"]), int(row["source_end"]), row["text"],
    )


def main() -> None:
    old_inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    old_candidates = {row["id"]: row for row in old_inventory["candidates"]}
    reviewed_by_coordinate = {}
    for _, _, path in REVIEWS:
        data = json.loads(path.read_text(encoding="utf-8"))
        for occurrence_id, review in data["rows"].items():
            candidate = old_candidates[occurrence_id]
            key = coordinate(candidate)
            if key in reviewed_by_coordinate:
                raise ValueError(f"duplicate old review coordinate {key}")
            reviewed_by_coordinate[key] = review

    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts/build_chinmayananda_ascii_sanskrit_inventory.py")],
        cwd=ROOT,
    )
    new_inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    new_candidates = new_inventory["candidates"]
    missing = [row for row in new_candidates if coordinate(row) not in reviewed_by_coordinate]
    if missing:
        raise ValueError(f"new unreviewed ASCII candidates after tokenizer repair: {[row['id'] for row in missing[:30]]}")

    retained_coordinates = {coordinate(row) for row in new_candidates}
    removed = sorted(set(reviewed_by_coordinate) - retained_coordinates)
    for start, end, path in REVIEWS:
        candidates = [row for row in new_candidates if start <= int(row["name_number"]) <= end]
        data = json.loads(path.read_text(encoding="utf-8"))
        data["expected_ids"] = [row["id"] for row in candidates]
        data["rows"] = {
            row["id"]: reviewed_by_coordinate[coordinate(row)]
            for row in candidates
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "old_candidates": len(old_candidates),
        "new_candidates": len(new_candidates),
        "removed_tokenizer_fragments": len(removed),
    }, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Insert the reviewed 56-unit Dāma reader into the citation index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "gita/yogavasistha-dama/review.json"
INDEX = ROOT / "data/citation_index.json"
PREFIX = "gauda-abhinanda/laghu-yogavasistha/sthiti/2/"
LEGACY_PREFIX = "gauda-abhinanda/laghu-yogavasistha/sthiti/2."


def entries(review: dict) -> dict[str, dict]:
    result = {}
    for unit in review["units"]:
        verse = unit["verse"]
        key = f"{PREFIX}{verse}"
        result[key] = {
            "thinker_id": "gauda-abhinanda",
            "work_id": "laghu-yogavasistha",
            "locus": f"Laghu-Yoga-Vāsiṣṭha, Sthitiprakaraṇa 2.{verse}",
            "locus_short": f"LYV 2.{verse}",
            "sanskrit_devanagari": unit["devanagari"],
            "sanskrit_iast": unit["iast"],
            "english_close": unit["translation"],
            "source": f"gita/yogavasistha-dama/review.json#units[{verse - 31}]",
            "verified": True,
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", type=Path, default=REVIEW)
    parser.add_argument("--index", type=Path, default=INDEX)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    review = json.loads(args.review.read_text(encoding="utf-8"))
    index = json.loads(args.index.read_text(encoding="utf-8"))
    expected = entries(review)
    if len(expected) != 56:
        raise SystemExit(f"expected 56 citation entries, found {len(expected)}")
    if args.check:
        observed = {key: index["entries"].get(key) for key in expected}
        if observed != expected:
            raise SystemExit("Dāma citation entries are missing or stale")
        print("Dāma citations: 56/56 current")
        return
    for key in [key for key in index["entries"] if key.startswith(LEGACY_PREFIX)]:
        del index["entries"][key]
    index["entries"].update(expected)
    args.index.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote 56 Dāma citation entries")


if __name__ == "__main__":
    main()

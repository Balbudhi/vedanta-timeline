#!/usr/bin/env python3
"""Freeze every Chinmayananda name-derivation candidate for source review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "gita/vishnu-sahasranama/reader.json"
OUTPUT = ROOT / "internal/sanskrit_reviews/chinmayananda-derivation-candidate-inventory.json"


def build() -> dict:
    reader = json.loads(READER.read_text(encoding="utf-8"))
    names = [name for stanza in reader["stanzas"] for name in stanza["names"]]
    rows = []
    for name in names:
        claim = str(name.get("traditional_derivation") or "").strip()
        if not claim:
            continue
        analysis = name.get("word_analysis") or {}
        rows.append({
            "id": f"name-{int(name['number']):04d}-derivation-claim",
            "name_number": int(name["number"]),
            "citation_iast": analysis.get("citation_iast") or name.get("citation_iast"),
            "citation_devanagari": analysis.get("citation_devanagari") or name.get("deva"),
            "claim_text": claim,
            "full_commentary": name.get("chinmayananda", {}).get("commentary", ""),
            "scan_pages": name.get("chinmayananda", {}).get("scan_pages", []),
            "current_analysis": analysis,
        })
    return {
        "schema_version": 1,
        "population_status": "closed-pending-source-review",
        "source_reader": str(READER.relative_to(ROOT)),
        "expected_count": 269,
        "rows": rows,
    }


def validate(data: dict) -> None:
    expected = build()
    if data != expected:
        expected_ids = {row["id"] for row in expected["rows"]}
        observed_ids = {row.get("id") for row in data.get("rows", [])}
        raise ValueError(
            "derivation inventory differs from the reader: "
            f"expected={len(expected_ids)} observed={len(observed_ids)} "
            f"missing={sorted(expected_ids - observed_ids)[:10]} "
            f"extra={sorted(observed_ids - expected_ids)[:10]}"
        )
    ids = [row["id"] for row in data["rows"]]
    numbers = [row["name_number"] for row in data["rows"]]
    if data.get("expected_count") != 269 or len(ids) != 269:
        raise ValueError(f"derivation inventory must contain exactly 269 rows, found {len(ids)}")
    if len(ids) != len(set(ids)) or numbers != sorted(numbers):
        raise ValueError("derivation inventory IDs must be unique and source ordered")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.check:
        data = json.loads(args.output.read_text(encoding="utf-8"))
        validate(data)
    else:
        data = build()
        if len(data["rows"]) != data["expected_count"]:
            raise ValueError(
                f"expected {data['expected_count']} derivation candidates, found {len(data['rows'])}"
            )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": 269, "status": "ok"}, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Remove English components that an OCR-style hyphen joined to Sanskrit."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "internal/sanskrit_reviews"
INVENTORY_PATH = INTERNAL / "inline-sanskrit-inventory.json"
REMOVED = {
    "darkkṛṣṇa", "destinationmokṣa", "effectmāyā", "gloryanuttamaḥ",
    "sātvatapeople", "worldofmāyā",
}


def main() -> None:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    expected_by_shard = {
        index: sorted(key for key, unit in inventory["units"].items() if int(unit["shard"]) == index)
        for index in range(4)
    }
    shard_data = {}
    for index in range(4):
        path = INTERNAL / f"inline-analysis-shard-{index}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in REMOVED:
            data["rows"].pop(key, None)
        shard_data[index] = (path, data)

    anuttama = inventory["units"]["anuttamaḥ"]
    shard_data[int(anuttama["shard"])][1]["rows"]["anuttamaḥ"] = {
        "unit_key": "anuttamaḥ",
        "occurrence_classification": "lexical Sanskrit",
        "canonical_devanagari": "अनुत्तमः",
        "canonical_iast": "anuttamaḥ",
        "printed_devanagari_forms": [],
        "iast_forms": anuttama["iast_forms"],
        "occurrence_ids": anuttama["occurrence_ids"],
        "source_qualification": "The site analyzes only the printed Sanskrit component; the adjacent English word remains ordinary Chinmayananda prose.",
        "reference": {"type": "name-analysis", "number": 80},
    }

    for key in ("kṛṣṇa", "mokṣa", "māyā", "sātvata"):
        unit = inventory["units"][key]
        row = shard_data[int(unit["shard"])][1]["rows"][key]
        row["iast_forms"] = unit["iast_forms"]
        row["occurrence_ids"] = unit["occurrence_ids"]

    for index, (path, data) in shard_data.items():
        expected = expected_by_shard[index]
        if set(data["rows"]) != set(expected):
            missing = sorted(set(expected) - set(data["rows"]))
            extra = sorted(set(data["rows"]) - set(expected))
            raise ValueError(f"shard {index} differs after repair: missing={missing}, extra={extra}")
        data["expected_unit_keys"] = expected
        if "expected_unit_count" in data:
            data["expected_unit_count"] = len(expected)
        if "observed_unit_count" in data:
            data["observed_unit_count"] = len(expected)
        if "review_counts" in data:
            data["review_counts"] = {
                "exact_form_reference_count": sum("reference" in row for row in data["rows"].values()),
                "independent_popup_count": sum("popup" in row for row in data["rows"].values()),
            }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"unique_units": len(inventory["units"]), "removed_mixed_units": len(REMOVED)}, indent=2))


if __name__ == "__main__":
    main()

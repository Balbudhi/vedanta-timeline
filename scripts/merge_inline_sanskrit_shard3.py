#!/usr/bin/env python3
"""Merge the three reviewed shard-3 work packets into the runtime shard."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "internal/sanskrit_reviews"
INVENTORY = json.loads((INTERNAL / "inline-sanskrit-inventory.json").read_text(encoding="utf-8"))


def main() -> None:
    expected = sorted(key for key, unit in INVENTORY["units"].items() if unit["shard"] == 3)
    rows = {}
    for suffix in "abc":
        path = INTERNAL / f"inline-analysis-shard-3{suffix}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("review_status") != "complete":
            raise ValueError(f"{path.name} is incomplete")
        overlap = set(rows) & set(data["rows"])
        if overlap:
            raise ValueError(f"duplicate units: {sorted(overlap)}")
        rows.update(data["rows"])
    if set(rows) != set(expected):
        raise ValueError(
            f"shard 3 population differs: missing={sorted(set(expected)-set(rows))}, "
            f"extra={sorted(set(rows)-set(expected))}"
        )
    output = {
        "schema_version": 1,
        "shard": 3,
        "review_status": "complete",
        "expected_unit_keys": expected,
        "rows": {key: rows[key] for key in expected},
    }
    path = INTERNAL / "inline-analysis-shard-3.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "output": str(path.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()

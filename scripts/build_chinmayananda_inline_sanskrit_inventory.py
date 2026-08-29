#!/usr/bin/env python3
"""Build the closed inline-Sanskrit occurrence and unique-form inventory."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts/audit_chinmayananda_sanskrit_coverage.py"
OUTPUT = ROOT / "internal/sanskrit_reviews/inline-sanskrit-inventory.json"


def key(value: str) -> str:
    value = unicodedata.normalize("NFC", value).lower().replace("~", "ṃ")
    return re.sub(r"[^a-zāīūṛṝḷṅñṭḍṇśṣṃḥ]", "", value)


def main() -> None:
    audit = json.loads(subprocess.check_output([sys.executable, str(AUDIT)], cwd=ROOT))
    previous_shards = {}
    if OUTPUT.exists():
        previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
        previous_shards = {key: unit["shard"] for key, unit in previous.get("units", {}).items()}
    units: dict[str, dict] = {}
    occurrences = []
    for row in audit["spans"]:
        if row["status"] != "inline-non-gita-candidate":
            continue
        source_iast = transliterate(row["text"], sanscript.DEVANAGARI, sanscript.IAST).replace("~", "ṃ")
        unit_key = key(source_iast)
        occurrence = {
            "id": row["id"], "kind": "deva", "name_number": row["name_number"],
            "paragraph_index": row["paragraph_index"], "source_start": row["source_start"],
            "source_end": row["source_end"], "text": row["text"], "unit_key": unit_key,
        }
        occurrences.append(occurrence)
        unit = units.setdefault(unit_key, {
            "unit_key": unit_key, "printed_devanagari_forms": [], "iast_forms": [],
            "occurrence_ids": [], "review_status": "unreviewed",
        })
        if row["text"] not in unit["printed_devanagari_forms"]:
            unit["printed_devanagari_forms"].append(row["text"])
        if source_iast not in unit["iast_forms"]:
            unit["iast_forms"].append(source_iast)
        unit["occurrence_ids"].append(row["id"])
    for row in audit["iast_spans"]:
        unit_key = key(row["normalized_form"])
        occurrence = {
            "id": row["id"], "kind": "iast", "name_number": row["name_number"],
            "paragraph_index": row["paragraph_index"], "source_start": row["source_start"],
            "source_end": row["source_end"], "text": row["text"], "unit_key": unit_key,
        }
        occurrences.append(occurrence)
        unit = units.setdefault(unit_key, {
            "unit_key": unit_key, "printed_devanagari_forms": [], "iast_forms": [],
            "occurrence_ids": [], "review_status": "unreviewed",
        })
        if row["text"] not in unit["iast_forms"]:
            unit["iast_forms"].append(row["text"])
        unit["occurrence_ids"].append(row["id"])
    ordered = sorted(units)
    for index, unit_key in enumerate(ordered):
        units[unit_key]["shard"] = previous_shards.get(
            unit_key, min(3, index * 4 // len(ordered))
        )
    data = {
        "schema_version": 1,
        "review_status": "inventory-complete-analysis-pending",
        "counts": {
            "inline_devanagari_occurrences": 296,
            "iast_marked_occurrences": 2457,
            "total_occurrences": 2753,
            "unique_units": 750,
        },
        "units": {key: units[key] for key in ordered},
        "occurrences": occurrences,
    }
    actual = {
        "inline_devanagari_occurrences": sum(row["kind"] == "deva" for row in occurrences),
        "iast_marked_occurrences": sum(row["kind"] == "iast" for row in occurrences),
        "total_occurrences": len(occurrences),
        "unique_units": len(units),
    }
    if actual != data["counts"]:
        raise ValueError(f"inline Sanskrit population changed: {actual}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data["counts"], indent=2))


if __name__ == "__main__":
    main()

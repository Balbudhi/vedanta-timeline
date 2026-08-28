#!/usr/bin/env python3
"""Validate the reviewed non-Gītā Sanskrit commentary shards."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHARDS = (
    ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-001-250.json",
    ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-251-500.json",
    ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-501-750.json",
    ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-751-1000.json",
)
AUDIT = ROOT / "scripts/audit_chinmayananda_sanskrit_coverage.py"
SLOT_RE = re.compile(r"\{([\d,\s]+):([^}]*)\}")


def expected_ids() -> set[str]:
    output = subprocess.check_output([sys.executable, str(AUDIT)], cwd=ROOT)
    audit = json.loads(output)
    return {
        row["id"]
        for row in audit["spans"]
        if row["status"] == "standalone-non-gita-candidate"
    }


def plain(slotted: str) -> str:
    return SLOT_RE.sub(lambda match: match.group(2), slotted)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    expected = expected_ids()
    quotes: dict[str, dict] = {}
    withheld: dict[str, object] = {}
    errors = []
    statuses = {}

    for path in SHARDS:
        if not path.exists():
            if args.require_complete:
                errors.append(f"missing shard {path.relative_to(ROOT)}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        statuses[path.name] = data.get("review_status")
        for key, row in data.get("quotes", {}).items():
            if key in quotes or key in withheld:
                errors.append(f"duplicate row {key}")
            quotes[key] = row
        for key, reason in data.get("withheld", {}).items():
            if key in quotes or key in withheld:
                errors.append(f"duplicate row {key}")
            withheld[key] = reason

    observed = set(quotes) | set(withheld)
    if observed - expected:
        errors.append(f"unexpected IDs: {sorted(observed - expected)}")
    if args.require_complete and observed != expected:
        errors.append(f"unaccounted IDs: {sorted(expected - observed)}")
    if args.require_complete and withheld:
        errors.append(f"withheld rows remain: {sorted(withheld)}")
    if args.require_complete and any(value != "primary-grammar-reviewed-complete" for value in statuses.values()):
        errors.append(f"incomplete shard statuses: {statuses}")

    required_row = (
        "quote_id", "name_number", "printed_devanagari", "canonical_devanagari",
        "iast", "source_label", "canonical_locus", "textual_notes", "english",
        "english_source", "english_slots", "words",
    )
    required_word = (
        "i", "deva", "iast", "gloss", "parts", "stem", "affix", "morph", "evidence",
    )
    for quote_id, row in quotes.items():
        if row.get("quote_id") != quote_id:
            errors.append(f"{quote_id}: quote_id mismatch")
        for field in required_row:
            if row.get(field) in (None, "", []):
                errors.append(f"{quote_id}: missing {field}")
        if row.get("english_source") not in ("Swami Chinmayananda", "site-literal-translation"):
            errors.append(f"{quote_id}: invalid english_source")
        words = row.get("words", [])
        if [word.get("i") for word in words] != list(range(len(words))):
            errors.append(f"{quote_id}: non-contiguous word indices")
        for word in words:
            for field in required_word:
                if word.get(field) in (None, "", []):
                    errors.append(f"{quote_id} word {word.get('i')}: missing {field}")
            if "root" not in word:
                errors.append(f"{quote_id} word {word.get('i')}: missing root key")
        slots = row.get("english_slots", "")
        if plain(slots) != row.get("english"):
            errors.append(f"{quote_id}: English slot replay differs")
        indices = [
            int(value.strip())
            for match in SLOT_RE.finditer(slots)
            for value in match.group(1).split(",")
            if value.strip()
        ]
        if set(indices) != set(range(len(words))):
            errors.append(f"{quote_id}: Sanskrit slot coverage differs")
        residue = SLOT_RE.sub("", slots)
        if re.search(r"[A-Za-z]", residue):
            errors.append(f"{quote_id}: visible English remains unslotted")

    if errors:
        raise ValueError("\n".join(errors[:200]))
    print(json.dumps({
        "expected": len(expected),
        "reviewed": len(quotes),
        "withheld": len(withheld),
        "unaccounted": len(expected - observed),
        "statuses": statuses,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

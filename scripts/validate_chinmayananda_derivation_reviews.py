#!/usr/bin/env python3
"""Validate the closed source review of Chinmayananda derivation claims."""

from __future__ import annotations

import collections
import glob
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "internal/sanskrit_reviews/chinmayananda-derivation-candidate-inventory.json"
REVIEWS = ROOT / "internal/sanskrit_reviews/chinmayananda-derivation-review-*.json"
CLASSIFICATIONS = {
    "established-grammar",
    "source-backed-alternative",
    "attested-traditional-nirvacana",
    "interpretive-not-etymology",
    "unsupported-withheld",
}
PRIMARY_RELATIONS = {"agrees", "qualified", "different-question", "unsupported"}


def review_rows() -> tuple[dict[str, dict], collections.Counter, list[dict]]:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    expected = {row["id"]: row for row in inventory["rows"]}
    observed = {}
    counts = collections.Counter()
    public = []
    errors = []
    paths = sorted(glob.glob(str(REVIEWS)))
    if len(paths) != 4:
        errors.append(f"expected 4 derivation review shards, found {len(paths)}")
    for raw_path in paths:
        path = Path(raw_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or data.get("review_status") != "complete":
            errors.append(f"{path.name}: review header is incomplete")
        ids = data.get("expected_ids", [])
        rows = data.get("rows", {})
        if ids != [row["id"] for row in inventory["rows"] if data["range"][0] <= row["name_number"] <= data["range"][1]]:
            errors.append(f"{path.name}: expected_ids do not replay the closed inventory range")
        if set(rows) != set(ids):
            errors.append(f"{path.name}: row IDs differ from expected_ids")
        for row_id, row in rows.items():
            if row_id in observed:
                errors.append(f"duplicate derivation review row {row_id}")
            observed[row_id] = row
            if row.get("primary_relation") not in PRIMARY_RELATIONS:
                errors.append(f"{row_id}: invalid primary_relation")
            dispositions = row.get("dispositions", [])
            if not dispositions:
                errors.append(f"{row_id}: no claim disposition")
            for index, disposition in enumerate(dispositions):
                classification = disposition.get("classification")
                counts[classification] += 1
                if classification not in CLASSIFICATIONS:
                    errors.append(f"{row_id}[{index}]: invalid classification")
                if not disposition.get("claim_text") or not disposition.get("reason"):
                    errors.append(f"{row_id}[{index}]: missing claim text/reason")
                evidence = disposition.get("evidence", [])
                if not evidence or any(not all(item.get(field) for field in ("source", "locus", "detail")) for item in evidence):
                    errors.append(f"{row_id}[{index}]: incomplete evidence")
                derivation = disposition.get("public_derivation")
                if classification in {"unsupported-withheld", "interpretive-not-etymology"} and derivation is not None:
                    errors.append(f"{row_id}[{index}]: non-derivational claim was made public")
                if derivation is None:
                    continue
                public.append({"row_id": row_id, **derivation})
                for field in ("id", "label", "kind", "meaning", "parts", "formation", "morphology", "qualification", "evidence"):
                    if derivation.get(field) in (None, "", [], {}):
                        errors.append(f"{row_id}[{index}]: public derivation lacks {field}")
                if derivation.get("kind") not in {"grammatical", "traditional-nirvacana"}:
                    errors.append(f"{row_id}[{index}]: invalid public derivation kind")
                if any(not all(part.get(field) for field in ("form", "gloss")) for part in derivation.get("parts", [])):
                    errors.append(f"{row_id}[{index}]: incomplete public derivation parts")
                for root in derivation.get("roots", []):
                    if not all(root.get(field) for field in ("form", "gana", "pada", "gloss", "dhatupatha")):
                        errors.append(f"{row_id}[{index}]: incomplete public derivation root")
                    dhatu = root.get("dhatupatha", {})
                    if not all(dhatu.get(field) for field in ("locus", "aupadeshika_devanagari", "artha_sanskrit")):
                        errors.append(f"{row_id}[{index}]: incomplete Dhātupāṭha root evidence")
                if any(not all(item.get(field) for field in ("source", "locus", "detail")) for item in derivation.get("evidence", [])):
                    errors.append(f"{row_id}[{index}]: incomplete public evidence")
    if set(observed) != set(expected):
        errors.append(
            "review population differs: "
            f"missing={sorted(set(expected) - set(observed))[:10]} "
            f"extra={sorted(set(observed) - set(expected))[:10]}"
        )
    public_ids = [f"{row['row_id']}::{row['id']}" for row in public]
    if len(public_ids) != len(set(public_ids)):
        errors.append("public parallel derivation IDs are not unique")
    if errors:
        raise ValueError("\n".join(errors[:300]))
    return observed, counts, public


def alternatives_by_name() -> dict[int, list[dict]]:
    inventory = {
        row["id"]: row
        for row in json.loads(INVENTORY.read_text(encoding="utf-8"))["rows"]
    }
    _rows, _counts, public = review_rows()
    result: dict[int, list[dict]] = {}
    for derivation in public:
        row_id = derivation["row_id"]
        number = int(inventory[row_id]["name_number"])
        value = {key: item for key, item in derivation.items() if key != "row_id"}
        value["id"] = f"{row_id}-{value['id']}"
        result.setdefault(number, []).append(value)
    return result


def main() -> None:
    rows, counts, public = review_rows()
    print(json.dumps({
        "candidate_rows": len(rows),
        "dispositions": sum(counts.values()),
        "classifications": dict(sorted(counts.items())),
        "public_parallel_derivations": len(public),
        "names_with_parallel_derivations": len(alternatives_by_name()),
    }, indent=2))


if __name__ == "__main__":
    main()

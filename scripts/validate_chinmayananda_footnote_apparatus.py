#!/usr/bin/env python3
"""Validate and expose Chinmayananda's complete printed footnote apparatus."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "internal/sanskrit_reviews/chinmayananda-footnote-apparatus-review.json"
ANCHOR_REVIEWS = (
    ROOT / "internal/sanskrit_reviews/chinmayananda-footnote-anchor-review-a.json",
    ROOT / "internal/sanskrit_reviews/chinmayananda-footnote-anchor-review-b.json",
)
PAYLOAD_CORRECTIONS = (
    ROOT / "internal/sanskrit_reviews/chinmayananda-footnote-payload-corrections.json"
)
COMMENTARY = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
ANCHOR_OCCURRENCE_OVERRIDES = {
    "cm-vs-fn-p020-n01": 0,
    "cm-vs-fn-p116-n02": 2,
}


def comparison_key(value: object) -> str:
    folded = unicodedata.normalize("NFKD", str(value or ""))
    folded = "".join(char for char in folded if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "", folded.casefold())


def merged_footnotes() -> list[dict]:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    entries = [dict(row) for row in base.get("entries", [])]
    expected_unresolved = {
        row["id"] for row in entries if row.get("source_status") == "needs-page-image-reread"
    }
    reviewed = {}
    for path in ANCHOR_REVIEWS:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or data.get("review_status") != "complete":
            raise ValueError(f"{path.name}: footnote anchor review is incomplete")
        if set(data.get("rows", {})) != set(data.get("expected_ids", [])):
            raise ValueError(f"{path.name}: anchor row IDs differ from expected_ids")
        for row_id, row in data["rows"].items():
            if row_id in reviewed:
                raise ValueError(f"duplicate footnote anchor review {row_id}")
            reviewed[row_id] = row
    if set(reviewed) != expected_unresolved:
        raise ValueError(
            "footnote anchor review population differs: "
            f"missing={sorted(expected_unresolved - set(reviewed))[:10]} "
            f"extra={sorted(set(reviewed) - expected_unresolved)[:10]}"
        )
    corrections = {}
    if PAYLOAD_CORRECTIONS.exists():
        data = json.loads(PAYLOAD_CORRECTIONS.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or data.get("review_status") != "complete":
            raise ValueError(f"{PAYLOAD_CORRECTIONS.name}: payload review is incomplete")
        if set(data.get("rows", {})) != set(data.get("expected_ids", [])):
            raise ValueError(f"{PAYLOAD_CORRECTIONS.name}: payload row IDs differ from expected_ids")
        corrections = data["rows"]
    commentary = {
        int(row["number"]): row["commentary"]
        for row in json.loads(COMMENTARY.read_text(encoding="utf-8"))["names"]
    }
    block_ids = []
    errors = []
    for entry in entries:
        override = reviewed.get(entry["id"])
        if override:
            for field in (
                "anchor_text", "anchor_text_normalized", "marker_printed", "source_status",
                "owner_name_number", "additional_name_numbers", "note_text",
                "note_text_normalized",
                "anchor_scope", "root_call_name_number",
            ):
                if field in override:
                    entry[field] = override[field]
            if "containment_override" in override:
                entry["current_containment"] = override["containment_override"]
            entry["anchor_review_evidence"] = override["evidence"]
            entry["review_notes"] = list(entry.get("review_notes", [])) + list(override.get("review_notes", []))
        correction = corrections.get(entry["id"])
        if correction:
            for field in (
                "note_text", "note_text_normalized", "owner_name_number",
                "additional_name_numbers", "anchor_text", "anchor_text_normalized",
                "marker_printed",
                "anchor_scope", "root_call_name_number",
            ):
                if field in correction:
                    entry[field] = correction[field]
            containment = correction.get("containment_override") or correction.get("current_containment")
            if containment:
                entry["current_containment"] = containment
            entry["payload_review_evidence"] = correction.get("evidence", {})
            entry["review_notes"] = (
                list(entry.get("review_notes", []))
                + list(correction.get("review_notes", []))
                + list(correction.get("correction_notes", []))
            )
        if not entry.get("anchor_text_normalized") or not entry.get("note_text_normalized"):
            errors.append(f"{entry.get('id')}: missing anchor/note text")
        if entry.get("source_status") not in {"scan-backed-normalized-transcription", "scan-verified-anchor"}:
            errors.append(f"{entry.get('id')}: unresolved source status")
        if entry.get("printed_page") != entry.get("pdf_page") - 4:
            errors.append(f"{entry.get('id')}: printed/PDF page mismatch")
        key = comparison_key(entry.get("anchor_text_normalized"))
        owner = int(entry["owner_name_number"])
        count = comparison_key(commentary[owner]).count(key) if key else 0
        occurrence = ANCHOR_OCCURRENCE_OVERRIDES.get(entry["id"], 0)
        if entry.get("anchor_scope") != "root-text" and count <= occurrence:
            errors.append(
                f"{entry.get('id')}: anchor occurrence {occurrence} not found uniquely enough in name {owner}"
            )
        if entry.get("anchor_scope") == "root-text" and not entry.get("root_call_name_number"):
            errors.append(f"{entry.get('id')}: root-text call lacks a target name")
        entry["anchor_occurrence"] = occurrence
        containment = entry.get("current_containment", {})
        ids = containment.get("block_ids", [])
        if not ids:
            errors.append(f"{entry.get('id')}: expected at least one containment block")
        block_ids.extend(ids)
    ids = [entry.get("id") for entry in entries]
    if len(entries) != 328 or len(set(ids)) != 328:
        errors.append(f"footnote population must be exactly 328 unique rows, found {len(entries)}")
    if len(block_ids) != len(set(block_ids)):
        errors.append("footnote containment blocks must not be shared between notes")
    if len({entry["pdf_page"] for entry in entries}) != 170:
        errors.append("footnote apparatus must span exactly 170 physical pages")
    if errors:
        raise ValueError("\n".join(errors[:300]))
    return entries


def main() -> None:
    entries = merged_footnotes()
    print(json.dumps({
        "footnotes": len(entries),
        "pages": len({row["pdf_page"] for row in entries}),
        "anchors": sum(bool(row.get("anchor_text_normalized")) for row in entries),
        "containment_blocks": len({block_id for row in entries for block_id in row["current_containment"]["block_ids"]}),
    }, indent=2))


if __name__ == "__main__":
    main()

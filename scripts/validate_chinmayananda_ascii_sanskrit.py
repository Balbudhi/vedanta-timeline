#!/usr/bin/env python3
"""Validate the human-reviewed undiacritized Roman Sanskrit population."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "internal/sanskrit_reviews"
INVENTORY = INTERNAL / "ascii-sanskrit-candidate-inventory.json"
DHATUPATHA_WITNESS = INTERNAL / "dhatupatha-witness.json"
DHATUPATHA_RAW_SHA256 = "e8c0e929294c4ab68455b461ee81234e7a0febac1b72e6873ea832354a28b641"
DHATUPATHA_PROJECTION_SHA256 = "346eadffd84c6bd72cbce6a2c9fc54b38416c6507de7a8d50a837443b0b543b9"
DHATUPATHA_RECORD_COUNT = 2259
DHATUPATHA_FIELDS = ("baseindex", "dhatu", "aupadeshik", "artha")
REVIEWS = (
    INTERNAL / "ascii-sanskrit-review-001-250.json",
    INTERNAL / "ascii-sanskrit-review-251-500.json",
    INTERNAL / "ascii-sanskrit-review-501-750.json",
    INTERNAL / "ascii-sanskrit-review-751-1000.json",
)
SLOT_RE = re.compile(r"\{([\d,\s]+):([^}]*)\}")
PLACEHOLDER_RE = re.compile(
    r"surface/citation form as contextually printed|surface token preserved|"
    r"exact .* pending|generic (?:noun|verb|form)|see parts",
    re.I,
)
VERBAL_MARKERS = (
    "indicative", "imperative", "optative", "participle", "absolutive",
    "gerundive", "finite verb", "verbal form",
)


def load_dhatupatha_witness() -> dict[str, dict]:
    """Load the pinned raw-field projection used for exact locus replay."""
    snapshot = json.loads(DHATUPATHA_WITNESS.read_text(encoding="utf-8"))
    source = snapshot.get("source", {})
    projection = snapshot.get("projection", {})
    rows = snapshot.get("data")
    if snapshot.get("schema_version") != 1 or snapshot.get("kind") != "dhatupatha-validation-witness":
        raise ValueError("Dhātupāṭha witness schema is invalid")
    if source.get("sha256") != DHATUPATHA_RAW_SHA256:
        raise ValueError("Dhātupāṭha witness source checksum differs from the pinned raw transport")
    if (
        projection.get("record_count") != DHATUPATHA_RECORD_COUNT
        or projection.get("unique_baseindex_count") != DHATUPATHA_RECORD_COUNT
        or not isinstance(rows, list)
        or len(rows) != DHATUPATHA_RECORD_COUNT
    ):
        raise ValueError("Dhātupāṭha witness record count is invalid")
    if projection.get("fields") != list(DHATUPATHA_FIELDS):
        raise ValueError("Dhātupāṭha witness field projection is invalid")
    encoded_rows = json.dumps(
        rows,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    if (projection.get("data_sha256") != DHATUPATHA_PROJECTION_SHA256
            or hashlib.sha256(encoded_rows).hexdigest() != DHATUPATHA_PROJECTION_SHA256):
        raise ValueError("Dhātupāṭha witness data checksum differs")
    if any(set(row) != set(DHATUPATHA_FIELDS) for row in rows):
        raise ValueError("Dhātupāṭha witness rows must contain only the pinned raw fields")
    by_locus = {row["baseindex"]: row for row in rows}
    if len(by_locus) != DHATUPATHA_RECORD_COUNT:
        raise ValueError("Dhātupāṭha witness baseindex population is not unique and complete")
    return by_locus


DHATUPATHA = load_dhatupatha_witness()


def fold(value: object) -> str:
    value = unicodedata.normalize("NFD", str(value or "").lower())
    return re.sub(r"[^a-z]", "", "".join(char for char in value if unicodedata.category(char) != "Mn"))


def ascii_key(value: object) -> str:
    value = unicodedata.normalize("NFC", str(value or "").lower())
    for source, target in (
        ("ā", "a"), ("ī", "i"), ("ū", "u"), ("ṛ", "ri"), ("ṝ", "rri"),
        ("ḷ", "li"), ("ṅ", "n"), ("ñ", "n"), ("ṭ", "t"), ("ḍ", "d"),
        ("ṇ", "n"), ("ś", "sh"), ("ṣ", "sh"), ("ṃ", "m"), ("ṁ", "m"),
        ("ḥ", "h"),
    ):
        value = value.replace(source, target)
    value = re.sub(r"[^a-z]", "", value)
    return re.sub(r"([aeiou])\1+", r"\1", value)


def equivalent(left: object, right: object) -> bool:
    return fold(left) == fold(right) or ascii_key(left) == ascii_key(right)


def load_inline_units() -> dict[str, dict]:
    rows = {}
    for index in range(4):
        data = json.loads((INTERNAL / f"inline-analysis-shard-{index}.json").read_text(encoding="utf-8"))
        rows.update(data["rows"])
    return rows


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    expected = {row["id"]: row for row in inventory["candidates"]}
    inline_units = load_inline_units()
    observed = {}
    errors = []
    for path in REVIEWS:
        if not path.exists():
            errors.append(f"missing review shard {path.name}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("review_status") != "complete":
            errors.append(f"incomplete review shard {path.name}")
        if set(data.get("expected_ids", [])) != set(data.get("rows", {})):
            errors.append(f"{path.name}: expected_ids do not replay rows")
        for occurrence_id, row in data.get("rows", {}).items():
            if occurrence_id in observed:
                errors.append(f"duplicate review row {occurrence_id}")
            observed[occurrence_id] = row
    if set(observed) != set(expected):
        errors.append(
            f"review population differs: missing={len(set(expected) - set(observed))}, "
            f"extra={len(set(observed) - set(expected))}"
        )
    accepted = rejected = referenced = independent = 0
    for occurrence_id, row in observed.items():
        candidate = expected.get(occurrence_id)
        if not candidate:
            continue
        decision = row.get("decision")
        if decision == "reject":
            rejected += 1
            if not str(row.get("reason", "")).strip():
                errors.append(f"{occurrence_id}: rejection lacks reason")
            continue
        if decision != "accept":
            errors.append(f"{occurrence_id}: invalid decision {decision!r}")
            continue
        accepted += 1
        canonical = row.get("canonical_iast")
        candidate_forms = candidate.get("candidate_iast_forms", [])
        reference = row.get("reference_unit_key")
        popup = row.get("popup")
        canonical_is_located = canonical and any(equivalent(canonical, form) for form in candidate_forms)
        if not canonical or (not canonical_is_located and not (popup and str(row.get("canonical_note", "")).strip())):
            errors.append(f"{occurrence_id}: reviewed canonical correction lacks a canonical_note")
        if bool(reference) == bool(popup):
            errors.append(f"{occurrence_id}: accepted row must have exactly one reference_unit_key or popup")
            continue
        if reference:
            referenced += 1
            unit = inline_units.get(reference)
            if not unit:
                errors.append(f"{occurrence_id}: missing reference unit {reference}")
            elif not equivalent(unit.get("canonical_iast"), canonical):
                errors.append(f"{occurrence_id}: reference unit is a different grammatical form")
        else:
            independent += 1
            words = popup.get("words", [])
            if not words or [word.get("i") for word in words] != list(range(len(words))):
                errors.append(f"{occurrence_id}: popup lacks contiguous words")
            for word in words:
                for field in ("deva", "iast", "gloss", "parts", "stem", "affix", "morph", "evidence"):
                    if word.get(field) in (None, "", []):
                        errors.append(f"{occurrence_id} word {word.get('i')}: missing {field}")
                if "root" not in word:
                    errors.append(f"{occurrence_id} word {word.get('i')}: missing root key")
                if PLACEHOLDER_RE.search(" ".join((str(word.get("affix", "")), str(word.get("morph", ""))))):
                    errors.append(f"{occurrence_id} word {word.get('i')}: placeholder morphology remains")
                evidence = word.get("evidence", {})
                if not evidence.get("grammar_witnesses"):
                    errors.append(f"{occurrence_id} word {word.get('i')}: grammar_witnesses are empty")
                morph = str(word.get("morph", "")).lower()
                root = word.get("root")
                if any(marker in morph for marker in VERBAL_MARKERS) and not isinstance(root, dict):
                    errors.append(f"{occurrence_id} word {word.get('i')}: verbal form lacks structured root")
                if isinstance(root, dict):
                    for field in ("form", "gana", "pada", "gloss", "dhatupatha"):
                        if root.get(field) in (None, "", {}):
                            errors.append(f"{occurrence_id} word {word.get('i')}: root lacks {field}")
                    dhatu = root.get("dhatupatha", {})
                    for field in ("locus", "dhatu_devanagari", "aupadeshika_devanagari", "artha_sanskrit"):
                        if dhatu.get(field) in (None, ""):
                            errors.append(f"{occurrence_id} word {word.get('i')}: Dhātupāṭha record lacks {field}")
                    witness = DHATUPATHA.get(str(dhatu.get("locus", "")))
                    if not witness:
                        errors.append(f"{occurrence_id} word {word.get('i')}: Dhātupāṭha locus is absent from paired raw witness")
                    elif (
                        witness.get("dhatu") != dhatu.get("dhatu_devanagari")
                        or witness.get("aupadeshik") != dhatu.get("aupadeshika_devanagari")
                        or witness.get("artha") != dhatu.get("artha_sanskrit")
                    ):
                        errors.append(f"{occurrence_id} word {word.get('i')}: Dhātupāṭha fields do not replay paired raw witness")
            slots = popup.get("english_slots", "")
            replay = SLOT_RE.sub(lambda match: match.group(2), slots)
            if replay != popup.get("english"):
                errors.append(f"{occurrence_id}: English slots change the popup English")
            indices = {
                int(value)
                for match in SLOT_RE.finditer(slots)
                for value in match.group(1).split(",") if value.strip()
            }
            if indices != set(range(len(words))):
                errors.append(f"{occurrence_id}: English slots do not cover every word")
    if errors:
        raise ValueError("\n".join(errors[:200]))
    print(json.dumps({
        "candidates": len(expected),
        "accepted_sanskrit": accepted,
        "rejected_non_sanskrit": rejected,
        "exact_references": referenced,
        "independent_popups": independent,
    }, indent=2))


if __name__ == "__main__":
    main()

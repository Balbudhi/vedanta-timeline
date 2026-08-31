#!/usr/bin/env python3
"""Check producer transport/replay; never claim a semantic review from a pass."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLOT = re.compile(r"\{([\d,\s]+):([^{}]*)\}")
GENERIC = {"quoted lexical form", "lexical citation form", "inline Sanskrit token",
           "nominal citation/inflected form", "citation form"}


def validate(path: Path, packet_path: Path) -> list[str]:
    data = json.loads(path.read_text())
    packet_bytes = packet_path.read_bytes()
    packet = json.loads(packet_bytes)
    errors = []
    if data.get("schema_version") != "sanskrit-producer-review-v1":
        errors.append("schema_version must be sanskrit-producer-review-v1")
    if data.get("name_number") != packet["name_number"]:
        errors.append("name_number differs from the input packet")
    if data.get("source_packet_sha256") != hashlib.sha256(packet_bytes).hexdigest():
        errors.append("input packet hash does not replay")
    units = data.get("units", [])
    ids = [u.get("id") for u in units]
    expected_ids = data.get("scope", {}).get("closed_unit_ids", [])
    if not ids or len(set(ids)) != len(ids) or ids != expected_ids:
        errors.append("units must match the declared ordered closed_unit_ids exactly")
    for unit in units:
        label = str(unit.get("id", "?"))
        source_text = unit.get("source_text")
        if (not isinstance(source_text, str) or not source_text
                or source_text not in packet["source_name"]["commentary"]):
            errors.append(f"{label}: source_text does not replay the commentary")
        if unit.get("status") not in {"producer-reviewed", "unresolved"}:
            errors.append(f"{label}: invalid producer status")
        if not isinstance(unit.get("unresolved"), list):
            errors.append(f"{label}: unresolved must be a list")
        elif unit["unresolved"] and unit.get("status") != "unresolved":
            errors.append(f"{label}: unresolved findings cannot be marked producer-reviewed")
        witnesses = unit.get("source_witnesses", [])
        if not witnesses:
            errors.append(f"{label}: source witnesses missing")
        for witness in witnesses:
            witness_path = Path(witness.get("path", ""))
            if not witness_path.is_absolute():
                witness_path = ROOT / witness_path
            excerpt = witness.get("excerpt")
            if not witness_path.is_file() or not witness.get("locus") or not excerpt:
                errors.append(f"{label}: witness needs a real file, locus and exact excerpt")
            elif excerpt not in witness_path.read_text(encoding="utf-8"):
                errors.append(f"{label}: witness excerpt does not replay {witness['path']}")
        words = unit.get("words", [])
        indices = list(range(len(words)))
        if not words or [w.get("i") for w in words] != indices:
            errors.append(f"{label}: words must be contiguous and nonempty")
        for word in words:
            word_label = f"{label}/word/{word.get('i', '?')}"
            for field in ("deva", "iast", "gloss", "parts", "stem", "affix", "morph", "evidence"):
                if not word.get(field):
                    errors.append(f"{word_label}: missing {field}")
            if re.search(r"[A-Za-z]", word.get("deva", "")):
                errors.append(f"{word_label}: Latin text in Devanagari field")
            if word.get("morph", "").lower() in GENERIC or word.get("affix", "").lower() in GENERIC:
                errors.append(f"{word_label}: generic analysis placeholder")
            for part in word.get("parts", []):
                if not part.get("form") or not part.get("gloss"):
                    errors.append(f"{word_label}: every morpheme needs form and gloss")
            if "root" not in word:
                errors.append(f"{word_label}: root must be present (null is permitted)")
            elif word["root"] is not None:
                root = word["root"]
                if not isinstance(root, dict) or any(not root.get(k) for k in ("form", "gana", "pada", "gloss", "dhatupatha")):
                    errors.append(f"{word_label}: root lacks structured form/gana/pada/gloss/dhatupatha")
                elif any(not root["dhatupatha"].get(k) for k in ("locus", "aupadeshika_devanagari", "artha_sanskrit")):
                    errors.append(f"{word_label}: incomplete Dhātupāṭha witness")
        segments = unit.get("source_segments", [])
        if "".join(s.get("text", "") for s in segments) != unit.get("devanagari"):
            errors.append(f"{label}: source_segments do not replay displayed Devanagari")
        segment_indices = {i for s in segments for i in s.get("word_indices", [])}
        if segment_indices != set(indices):
            errors.append(f"{label}: source_segments do not cover exactly all words")
        english, slots = unit.get("english"), unit.get("english_slots")
        if not isinstance(english, str) or not isinstance(slots, str):
            errors.append(f"{label}: english must be plain text; english_slots must be a slotted string")
            continue
        if SLOT.sub(lambda m: m[2], slots) != english:
            errors.append(f"{label}: slots do not replay plain English")
        if "{" in english or "}" in english or "[" in english or "]" in english:
            errors.append(f"{label}: English contains markup or bracketed editorial additions")
        used = {int(i) for m in SLOT.finditer(slots) for i in m[1].split(",") if i.strip()}
        if used != set(indices):
            errors.append(f"{label}: English slots do not cover exactly all words")
        if re.search(r"[A-Za-z]", SLOT.sub("", slots)):
            errors.append(f"{label}: English words outside mapped slots")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--require-resolved", action="store_true",
                        help="Fail candidate integration while any producer unit remains unresolved")
    args = parser.parse_args()
    errors = validate(args.review, args.packet)
    if errors:
        raise SystemExit("\n".join(errors))
    units = json.loads(args.review.read_text())["units"]
    unresolved = [u["id"] for u in units if u.get("status") == "unresolved"]
    if args.require_resolved and unresolved:
        raise SystemExit("Producer units remain unresolved: " + ", ".join(unresolved))
    print(json.dumps({"transport_and_replay": "pass", "units": len(units),
                      "unresolved_unit_ids": unresolved,
                      "independent_linguistic_review": "required"}, indent=2))


if __name__ == "__main__":
    main()

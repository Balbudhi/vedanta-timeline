#!/usr/bin/env python3
"""Validate every inline Sanskrit occurrence and unique popup unit."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "internal/sanskrit_reviews"
INVENTORY = INTERNAL / "inline-sanskrit-inventory.json"
SHARDS = tuple(INTERNAL / f"inline-analysis-shard-{index}.json" for index in range(4))
SLOT_RE = re.compile(r"\{[\d,\s]+:([^}]*)\}")
VERBAL_MARKERS = (
    "indicative", "imperative", "optative", "participle", "absolutive",
    "gerundive", "finite verb", "verbal form",
)
PLACEHOLDER_RE = re.compile(
    r"contextual-name|name-analysis-context|contextually tied|"
    r"surface token preserved|see parts|exact .* pending|"
    r"citation form in inline|inline term normalization for popup identity",
    re.I,
)
GLOSS_PROSE_RE = re.compile(r"^(?:one who|the one|that which|the Lord)$|^(?:one who|the one|that which)\b", re.I)
NON_MORPHEME_FORM_RE = re.compile(
    r"(?i)\b(?:finite|present|perfect|past|future)\s+(?:verbal|form|ending|plural|singular)\b|"
    r"\b(?:enclitic\s+oblique|verbal\s+ending)\b"
)


def key(value: str) -> str:
    value = unicodedata.normalize("NFC", value).lower().replace("~", "ṃ")
    return re.sub(r"[^a-zāīūṛṝḷṅñṭḍṇśṣṃḥ]", "", value)


def effective_names() -> dict[int, dict]:
    base = {
        row["number"]: row
        for row in json.loads((ROOT / "gita/vishnu-sahasranama/analysis.json").read_text(encoding="utf-8"))["names"]
    }
    for path in sorted((ROOT / "internal/sanskrit_reviews").glob("name-analysis-review-*.json")):
        for number_text, record in json.loads(path.read_text(encoding="utf-8"))["rows"].items():
            if record.get("status") == "replace":
                base[int(number_text)] = record["analysis"]
    return base


def quote_words() -> dict[tuple[str, int], dict]:
    result = {}
    for path in sorted((ROOT / "gita/vishnu-sahasranama").glob("commentary-sanskrit-analysis-*.json")):
        for quote_id, row in json.loads(path.read_text(encoding="utf-8"))["quotes"].items():
            for word in row["words"]:
                result[(quote_id, int(word["i"]))] = word
    gita = json.loads((ROOT / "gita/vishnu-sahasranama/commentary-quote-analysis.json").read_text(encoding="utf-8"))
    for quote_id, row in gita["quotes"].items():
        for word in row["words"]:
            result[(quote_id, int(word["i"]))] = word
    return result


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    expected = inventory["units"]
    names = effective_names()
    qwords = quote_words()
    rows = {}
    errors = []
    for path in SHARDS:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("review_status") != "complete":
            errors.append(f"{path.name}: review_status is not complete")
        expected_keys = {key for key, unit in expected.items() if unit["shard"] == int(path.stem.rsplit("-", 1)[1])}
        shard_rows = data.get("rows", {})
        if set(shard_rows) != expected_keys:
            errors.append(f"{path.name}: population differs")
        for unit_key, row in shard_rows.items():
            if unit_key in rows:
                errors.append(f"duplicate unit {unit_key}")
            rows[unit_key] = row
    if set(rows) != set(expected):
        errors.append(f"inline unit population differs: missing={len(set(expected)-set(rows))}")

    reference_count = 0
    popup_count = 0
    for unit_key, row in rows.items():
        if set(row.get("occurrence_ids", [])) != set(expected[unit_key]["occurrence_ids"]):
            errors.append(f"{unit_key}: occurrence population differs")
        canonical_iast = row.get("canonical_iast", "")
        if not canonical_iast:
            errors.append(f"{unit_key}: lacks canonical_iast")
        serialized = json.dumps(row, ensure_ascii=False)
        if PLACEHOLDER_RE.search(serialized):
            errors.append(f"{unit_key}: context/placeholder reference remains")
        reference = row.get("reference")
        popup = row.get("popup")
        if bool(reference) == bool(popup):
            errors.append(f"{unit_key}: must have exactly one reference or popup")
            continue
        if reference:
            reference_count += 1
            ref_type = reference.get("type") or reference.get("kind")
            if ref_type in ("name-analysis", "name-analysis-review"):
                number = reference.get("number")
                if number is None:
                    values = reference.get("name_numbers", [])
                    number = values[0] if len(values) == 1 else None
                target = names.get(int(number)) if number is not None else None
                if not target or key(target["citation_iast"]) != key(canonical_iast):
                    errors.append(f"{unit_key}: name reference is not an exact lexical-form match")
            elif ref_type == "quote-word":
                target = qwords.get((reference.get("quote_id"), int(reference.get("word_i", -1))))
                if not target or key(target["iast"]) != key(canonical_iast):
                    errors.append(f"{unit_key}: quote-word reference is not exact")
            else:
                errors.append(f"{unit_key}: unsupported reference type {ref_type!r}")
            continue
        popup_count += 1
        if popup.get("english_source") not in ("site-literal-translation", "Swami Chinmayananda"):
            errors.append(f"{unit_key}: popup lacks English provenance")
        if SLOT_RE.sub(lambda match: match.group(1), popup.get("english_slots", "")) != popup.get("english"):
            errors.append(f"{unit_key}: popup English does not replay slots")
        words = popup.get("words", [])
        if not words or [word.get("i") for word in words] != list(range(len(words))):
            errors.append(f"{unit_key}: popup words are absent/non-contiguous")
            continue
        lexical_tokens = [token for token in re.split(r"\s+", canonical_iast.strip()) if key(token)]
        if len(lexical_tokens) > 1 and len(words) < 2:
            errors.append(f"{unit_key}: multiword unit collapsed to one popup word")
        indices = {
            int(value)
            for group in re.findall(r"\{([\d,\s]+):", popup.get("english_slots", ""))
            for value in group.split(",") if value.strip()
        }
        if indices != set(range(len(words))):
            errors.append(f"{unit_key}: popup slot coverage differs")
        for word in words:
            for field in ("deva", "iast", "gloss", "parts", "stem", "affix", "morph", "evidence"):
                if word.get(field) in (None, "", [], {}):
                    errors.append(f"{unit_key} word {word.get('i')}: lacks {field}")
            morph = str(word.get("morph", "")).lower()
            glosses = [str(word.get("gloss", ""))] + [str(part.get("gloss", "")) for part in word.get("parts", [])]
            if any(GLOSS_PROSE_RE.search(gloss) or len(gloss) > 140 for gloss in glosses):
                errors.append(f"{unit_key} word {word.get('i')}: prose/debris remains in lexical gloss")
            if any(NON_MORPHEME_FORM_RE.search(str(part.get("form", ""))) for part in word.get("parts", [])):
                errors.append(f"{unit_key} word {word.get('i')}: English grammar description appears in morpheme form")
            if any(marker in morph for marker in VERBAL_MARKERS):
                roots = [word["root"]] if isinstance(word.get("root"), dict) else word.get("roots", [])
                if not roots:
                    errors.append(f"{unit_key} word {word.get('i')}: verbal form lacks root")
                for root in roots:
                    dhatu = root.get("dhatupatha", {})
                    if not re.fullmatch(r"\d{2}\.\d{4}", str(dhatu.get("locus", ""))):
                        errors.append(f"{unit_key} word {word.get('i')}: invalid Dhātupāṭha locus")
    if errors:
        raise ValueError("\n".join(errors[:400]))
    print(json.dumps({
        "occurrences": inventory["counts"]["total_occurrences"],
        "unique_units": len(rows),
        "exact_references": reference_count,
        "independent_popups": popup_count,
    }, indent=2))


if __name__ == "__main__":
    main()

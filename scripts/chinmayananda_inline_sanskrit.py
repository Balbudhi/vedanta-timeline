"""Attach reviewed inline-Sanskrit popup data to commentary prose blocks."""

from __future__ import annotations

import copy
import json
import re
import unicodedata
from pathlib import Path

from add_sanskrit_source_segments import align
from chinmayananda_sanskrit_blocks import reader_word


ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "internal/sanskrit_reviews"
INVENTORY = json.loads((INTERNAL / "inline-sanskrit-inventory.json").read_text(encoding="utf-8"))
ANALYSES = tuple(INTERNAL / f"inline-analysis-shard-{index}.json" for index in range(4))
ASCII_INVENTORY = json.loads((INTERNAL / "ascii-sanskrit-candidate-inventory.json").read_text(encoding="utf-8"))
ASCII_REVIEWS = (
    INTERNAL / "ascii-sanskrit-review-001-250.json",
    INTERNAL / "ascii-sanskrit-review-251-500.json",
    INTERNAL / "ascii-sanskrit-review-501-750.json",
    INTERNAL / "ascii-sanskrit-review-751-1000.json",
)
DEVA_SPAN_RE = re.compile(r"[\u0900-\u097f][\u0900-\u097f\u200c\u200d\s।॥,;:…\-–—()]+")


def english_source_key(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", ascii_text)


def lexical_phrase_range(text: str, phrase: str) -> tuple[int, int] | None:
    target = english_source_key(phrase)
    if not target:
        return None
    normalized = []
    source_indices = []
    for index, char in enumerate(text):
        folded = unicodedata.normalize("NFKD", char).encode("ascii", "ignore").decode().lower()
        for item in folded:
            if item.isalnum():
                normalized.append(item)
                source_indices.append(index)
    joined = "".join(normalized)
    start = joined.find(target)
    if start < 0:
        return None
    source_start = source_indices[start]
    source_end = source_indices[start + len(target) - 1] + 1
    while source_start > 0 and text[source_start - 1] in "\"'“‘":
        source_start -= 1
    while source_end < len(text) and text[source_end] in "\"'”’":
        source_end += 1
    return source_start, source_end


def structured_source_ranges() -> dict[tuple[int, int], list[tuple[int, int]]]:
    commentary = {
        int(row["number"]): row["commentary"].split("\n\n")
        for row in json.loads((ROOT / "gita/vishnu-sahasranama/chinmayananda.json").read_text(encoding="utf-8"))["names"]
    }
    ranges: dict[tuple[int, int], list[tuple[int, int]]] = {}
    gita = json.loads((ROOT / "gita/vishnu-sahasranama/commentary-quotes.json").read_text(encoding="utf-8"))["quotes"]
    claimed: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for quote in sorted(gita, key=lambda row: row["id"]):
        number = int(quote["name_number"])
        translation = quote.get("chinmayananda_translation")
        if translation:
            for paragraph_index, paragraph in enumerate(commentary[number]):
                found = lexical_phrase_range(paragraph, translation)
                if not found:
                    continue
                key = (number, paragraph_index)
                if any(found[0] < end and found[1] > start for start, end in claimed.get(key, [])):
                    continue
                claimed.setdefault(key, []).append(found)
                ranges.setdefault(key, []).append(found)
                break
        paragraph_index = int(quote["paragraph_index"])
        paragraph = commentary[number][paragraph_index]
        start, end = int(quote["source_start"]), int(quote["source_end"])
        roman = re.match(r"\s*[\"'”’]*\s*\([^)]{2,600}\)", paragraph[end:])
        if roman:
            end += roman.end()
        ranges.setdefault((number, paragraph_index), []).append((start, end))

    for path in sorted((ROOT / "gita/vishnu-sahasranama").glob("commentary-sanskrit-analysis-[0-9]*.json")):
        for row in json.loads(path.read_text(encoding="utf-8"))["quotes"].values():
            number = int(row["name_number"])
            match = re.search(r"-paragraph-(\d+)-span-(\d+)$", row["quote_id"])
            if not match:
                raise ValueError(f"non-Gītā quote lacks paragraph identity: {row['quote_id']}")
            paragraph_index = int(match.group(1))
            span_index = int(match.group(2))
            paragraph = commentary[number][paragraph_index]
            spans = list(DEVA_SPAN_RE.finditer(paragraph))
            if span_index >= len(spans):
                raise ValueError(f"non-Gītā quote does not replay source paragraph: {row['quote_id']}")
            start, end = spans[span_index].span()
            unmatched_open = paragraph.rfind("(", start, end)
            if unmatched_open >= start:
                close = paragraph.find(")", end)
                if close >= end and close - unmatched_open <= 800:
                    end = close + 1
            roman = re.match(r"\s*[\"'”’]*\s*\([^)]{2,800}\)", paragraph[end:])
            if roman:
                end += roman.end()
            ranges.setdefault((number, paragraph_index), []).append((start, end))
    return ranges


STRUCTURED_RANGES = structured_source_ranges()


def represented_by_structured_block(occurrence: dict) -> bool:
    key = (int(occurrence["name_number"]), int(occurrence["paragraph_index"]))
    start, end = int(occurrence["source_start"]), int(occurrence["source_end"])
    return any(start < range_end and end > range_start for range_start, range_end in STRUCTURED_RANGES.get(key, []))


def load_units() -> dict[str, dict]:
    rows = {}
    for path in ANALYSES:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("review_status") != "complete":
            raise ValueError(f"inline Sanskrit review is incomplete: {path.name}")
        for key, row in data["rows"].items():
            if key in rows:
                raise ValueError(f"duplicate inline Sanskrit unit {key}")
            rows[key] = row
    if set(rows) != set(INVENTORY["units"]):
        raise ValueError(f"inline Sanskrit unit population differs: {len(rows)}")
    return rows


def load_quote_words() -> dict[tuple[str, int], dict]:
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


UNITS = load_units()


def load_ascii_occurrences() -> list[dict]:
    candidates = {row["id"]: row for row in ASCII_INVENTORY["candidates"]}
    reviews = {}
    for path in ASCII_REVIEWS:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("review_status") != "complete":
            raise ValueError(f"ASCII Sanskrit review is incomplete: {path.name}")
        for occurrence_id, row in data.get("rows", {}).items():
            if occurrence_id in reviews:
                raise ValueError(f"duplicate ASCII Sanskrit review {occurrence_id}")
            reviews[occurrence_id] = row
    if set(reviews) != set(candidates):
        raise ValueError(
            f"ASCII Sanskrit review population differs: missing={len(set(candidates) - set(reviews))}, "
            f"extra={len(set(reviews) - set(candidates))}"
        )
    accepted = []
    for occurrence_id, review in reviews.items():
        if review.get("decision") == "reject":
            continue
        if review.get("decision") != "accept":
            raise ValueError(f"invalid ASCII Sanskrit review decision for {occurrence_id}")
        occurrence = dict(candidates[occurrence_id])
        occurrence["kind"] = "ascii"
        reference = review.get("reference_unit_key")
        popup = review.get("popup")
        if bool(reference) == bool(popup):
            raise ValueError(f"ASCII Sanskrit review {occurrence_id} lacks a single analysis route")
        if reference:
            if reference not in UNITS:
                raise ValueError(f"ASCII Sanskrit review {occurrence_id} references missing unit {reference}")
            occurrence["unit_key"] = reference
        else:
            synthetic_key = f"ascii:{occurrence_id}"
            UNITS[synthetic_key] = {"popup": popup}
            occurrence["unit_key"] = synthetic_key
        accepted.append(occurrence)
    return accepted


ASCII_OCCURRENCES = load_ascii_occurrences()
ASCII_ACCEPTED_IDS = {row["id"] for row in ASCII_OCCURRENCES}
ASCII_STRUCTURED_IDS = {row["id"] for row in ASCII_OCCURRENCES if represented_by_structured_block(row)}
ASCII_ATTACHED_IDS: set[str] = set()
NAMES = {
    row["number"]: row
    for row in json.loads((ROOT / "gita/vishnu-sahasranama/analysis.json").read_text(encoding="utf-8"))["names"]
}
QUOTE_WORDS = load_quote_words()
OCCURRENCES_BY_NAME: dict[int, list[dict]] = {}
for occurrence in INVENTORY["occurrences"]:
    if not represented_by_structured_block(occurrence):
        OCCURRENCES_BY_NAME.setdefault(int(occurrence["name_number"]), []).append(occurrence)
for occurrence in ASCII_OCCURRENCES:
    if occurrence["id"] not in ASCII_STRUCTURED_IDS:
        OCCURRENCES_BY_NAME.setdefault(int(occurrence["name_number"]), []).append(occurrence)


def name_word(number: int) -> dict:
    row = NAMES[number]
    word = {
        "i": 0,
        "deva": row["citation_devanagari"],
        "iast": row["citation_iast"],
        "gloss": row["whole_gloss"],
        "parts": [
            {"form": part["form_iast"], "gloss": part["gloss"]}
            for part in row["parts"]
        ],
        "stem": row["stem"],
        "root": row.get("root"),
        "affix": row["affix"],
        "morph": row["morph"],
    }
    return reader_word(word)


def resolved_words(unit: dict) -> list[dict]:
    popup = unit.get("popup")
    if popup:
        return [reader_word(word) for word in popup["words"]]
    reference = unit["reference"]
    ref_type = reference.get("type") or reference.get("kind")
    if ref_type in ("name-analysis", "name-analysis-review"):
        number = reference.get("number")
        if number is None:
            number = reference["name_numbers"][0]
        return [name_word(int(number))]
    if ref_type == "quote-word":
        return [reader_word(copy.deepcopy(QUOTE_WORDS[(reference["quote_id"], int(reference["word_i"]))]))]
    raise ValueError(f"unsupported inline reference type {ref_type!r}")


def segments_for(text: str, language: str, words: list[dict]) -> list[dict]:
    if language == "sa-Deva":
        try:
            return align(text, words)[0]
        except ValueError:
            pass
    return [{"text": text, "word_indices": [word["i"] for word in words]}]


def popup_payload(unit_key: str, occurrence: dict, display_text: str | None = None) -> dict:
    unit = UNITS[unit_key]
    words = resolved_words(unit)
    language = "sa-Deva" if occurrence["kind"] == "deva" else "sa-Latn"
    text = display_text if display_text is not None else occurrence["text"]
    return {
        "id": occurrence["id"],
        "unit_key": unit_key,
        "text": text,
        "language": language,
        "words": words,
        "source_segments": segments_for(text, language, words),
    }


def promote_inline_blocks(name_number: int, blocks: list[dict]) -> list[dict]:
    occurrences = OCCURRENCES_BY_NAME.get(int(name_number), [])
    if not occurrences:
        return blocks
    by_text: dict[str, list[dict]] = {}
    for occurrence in occurrences:
        match_text = occurrence["text"].lstrip("-—–") or occurrence["text"]
        by_text.setdefault(match_text, []).append(occurrence)
    candidates = sorted(by_text, key=lambda text: (-len(text), text))
    used_ids = set()
    result = []
    for block in blocks:
        if block.get("type") != "prose":
            result.append(block)
            continue
        text = block.get("text", "")
        occupied: list[tuple[int, int]] = []
        annotations = []
        for candidate_text in candidates:
            available = [
                occurrence for occurrence in by_text[candidate_text]
                if occurrence["id"] not in used_ids
            ]
            if not available:
                continue
            start = 0
            positions = []
            while len(positions) < len(available):
                index = text.find(candidate_text, start)
                if index < 0:
                    break
                end = index + len(candidate_text)
                start = end
                if any(index < claimed_end and end > claimed_start for claimed_start, claimed_end in occupied):
                    continue
                positions.append((index, end))
            for occurrence, (index, end) in zip(available, positions):
                occupied.append((index, end))
                used_ids.add(occurrence["id"])
                if occurrence["id"] in ASCII_ACCEPTED_IDS:
                    ASCII_ATTACHED_IDS.add(occurrence["id"])
                annotation = popup_payload(occurrence["unit_key"], occurrence, candidate_text)
                annotation["start"] = index
                annotation["end"] = end
                annotations.append(annotation)
        if annotations:
            block = dict(block)
            block["inline_sanskrit"] = sorted(annotations, key=lambda row: row["start"])
        result.append(block)
    return result


def ascii_attachment_report() -> dict:
    return {
        "accepted": len(ASCII_ACCEPTED_IDS),
        "attached_to_prose": len(ASCII_ATTACHED_IDS),
        "represented_by_structured_blocks": len(ASCII_STRUCTURED_IDS),
        "unaccounted_ids": sorted(ASCII_ACCEPTED_IDS - ASCII_ATTACHED_IDS - ASCII_STRUCTURED_IDS),
    }

"""Attach reviewed inline-Sanskrit popup data to commentary prose blocks."""

from __future__ import annotations

import copy
import difflib
import json
import re
import unicodedata
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

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
DISPLAY_LETTER_RE = re.compile(r"[A-Za-zĀ-ỹÑñ\u0900-\u097f]")
DISPLAY_IAST_MARK_RE = re.compile(r"[āīūṛṝḷṅñṭḍṇśṣṃṁḥ]")
DISPLAY_SOURCE_KEYWORD_RE = re.compile(
    r"(?:[A-Za-zĀ-ỹÑñ]*opaniṣad|Upaniṣad|Up\.|Purāṇa|Parva|Veda|Smṛti|Mahābhārata|Bhāgavata|Gītā|"
    r"Kaṭha|Katha|Chāndogya|Taittirīya|Aitareya|Bṛhadāraṇyaka|Śvetāśvatara|"
    r"Muṇḍaka|Mundaka|Harivaṃśa|Kośa|śāstra|Vyāsa|Īśa|Ṛg)",
    re.I,
)
DISPLAY_ENGLISH_HINT_RE = re.compile(
    r"\b(?:a|an|and|are|as|by|for|from|full|he|her|him|his|in|is|it|its|"
    r"means|of|one|protector|enjoyer|read|says?|that|the|their|them|these|"
    r"this|to|when|whence|who|with)\b",
    re.I,
)


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


def parenthetical_is_romanization(value: str, quote: dict) -> bool:
    if len(re.findall(
        r"\b(?:the|a|an|is|am|are|among|which|where|all|beings|serpents?|sage|one|who|in|to|of)\b",
        value,
        flags=re.I,
    )) >= 2:
        return False
    return difflib.SequenceMatcher(
        a=english_source_key(value),
        b=english_source_key(quote.get("canonical_iast", "")),
        autojunk=False,
    ).ratio() >= 0.40


def structured_source_ranges() -> dict[tuple[int, int], list[tuple[int, int]]]:
    commentary = {
        int(row["number"]): row["commentary"].split("\n\n")
        for row in json.loads((ROOT / "gita/vishnu-sahasranama/chinmayananda.json").read_text(encoding="utf-8"))["names"]
    }
    ranges: dict[tuple[int, int], list[tuple[int, int]]] = {}
    gita = json.loads((ROOT / "gita/vishnu-sahasranama/commentary-quotes.json").read_text(encoding="utf-8"))["quotes"]
    gita_review = json.loads(
        (ROOT / "gita/vishnu-sahasranama/commentary-quote-analysis.json").read_text(encoding="utf-8")
    )["quotes"]
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
                if gita_review.get(quote["id"], {}).get("english_source") != "Swami Chinmayananda":
                    ranges.setdefault(key, []).append(found)
                break
        paragraph_index = int(quote["paragraph_index"])
        paragraph = commentary[number][paragraph_index]
        start, end = int(quote["source_start"]), int(quote["source_end"])
        if end > 0 and paragraph[end - 1] == "(":
            roman_end = paragraph.find(")", end)
            if roman_end >= 0 and parenthetical_is_romanization(paragraph[end:roman_end], quote):
                end = roman_end + 1
        else:
            roman = re.match(r"\s*[\"'”’]*\s*\(([^)]{2,800})(?:\)|$)", paragraph[end:])
            if roman and parenthetical_is_romanization(roman.group(1), quote):
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
            else:
                printed_roman = re.match(
                    r'^\s*["\'”’]*\s*([^"“]{3,800}(?:\)|\.))\s*(?=["“])',
                    paragraph[end:],
                )
                if printed_roman and parenthetical_is_romanization(
                    printed_roman.group(1),
                    {"canonical_iast": row.get("source_iast", "")},
                ):
                    end += printed_roman.end(1)
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


def standalone_display_candidate(text: str, annotations: list[dict]) -> bool:
    if not annotations:
        return False
    total_letters = [index for index, char in enumerate(text) if DISPLAY_LETTER_RE.match(char)]
    if not total_letters:
        return False
    covered = set()
    for annotation in annotations:
        for index in range(int(annotation["start"]), int(annotation["end"])):
            if index < len(text) and DISPLAY_LETTER_RE.match(text[index]):
                covered.add(index)
    trimmed = text.lstrip()
    without_opening = re.sub(r'^[“"‘\'\s(]+', "", trimmed)
    starts_quote = bool(re.match(r'^[“"‘\']', trimmed))
    starts_devanagari = bool(re.match(r'^[\u0900-\u097f]', without_opening))
    first_interactive = min(int(annotation["start"]) for annotation in annotations)
    return len(covered) / len(total_letters) >= 0.55 and (
        starts_devanagari or starts_quote or first_interactive <= 3
    )


def source_tail(text: str) -> tuple[str, str]:
    matches = list(DISPLAY_SOURCE_KEYWORD_RE.finditer(text))
    if not matches:
        return text.strip(), ""
    match = matches[-1]
    prefix = text[:match.start()]
    dash = max(prefix.rfind("—"), prefix.rfind("–"), prefix.rfind(" -"))
    explicit_dash = dash >= 0 and match.start() - dash <= 64
    if explicit_dash:
        start = dash + 1
    else:
        start = match.start()
        previous = re.search(r"([A-ZĀ-Ž][A-Za-zĀ-ỹÑñ'’.\-]+\s+)$", prefix)
        if previous and match.group(0).casefold() in {"upaniṣad", "up.", "purāṇa", "parva", "veda"}:
            start = previous.start()
    source = text[start:].strip(" \t\n—–-").rstrip(".")
    source = re.sub(r"\s*\([^)]*\)\s*$", "", source).rstrip(".")
    if not re.search(r"[IVXLC\d]", source) and not explicit_dash and not re.fullmatch(
        r"(?:Upaniṣad|Smṛti|Mahābhārata|Vyāsa|Kaṭhopaniṣad|Amara Kośa)",
        source,
        re.I,
    ):
        return text.strip(), ""
    body = text[:start].strip(" \t\n—–-")
    return body, source


def clean_display_english(value: str, allow_short_quote: bool = False) -> str:
    candidate = value.strip(" \t\n—–-()")
    candidate = re.sub(r'^[”’\'।.\s]+(?=[“\"])', "", candidate)
    if not candidate:
        return ""
    hints = DISPLAY_ENGLISH_HINT_RE.findall(candidate)
    quoted_word = allow_short_quote and bool(re.fullmatch(r'[“\"][A-Z][A-Za-z -]+[.!?]?[”\"]', candidate))
    if len(hints) < 2 and not re.search(r"\b(?:says?|read|means)\b", candidate, re.I) and not quoted_word:
        return ""
    candidate = re.sub(r"\s+", " ", candidate).strip()
    return candidate.rstrip(' “\"') if not allow_short_quote else candidate


def normalized_display_word(word: dict, index: int) -> dict:
    result = copy.deepcopy(word)
    result["i"] = index
    return result


def normalized_quote_display(text: str, annotations: list[dict]) -> dict | None:
    if not standalone_display_candidate(text, annotations):
        return None
    leading_source = DISPLAY_SOURCE_KEYWORD_RE.search(text)
    if (
        leading_source
        and leading_source.start() < 24
        and re.search(r"[IVXLC\d]", text)
        and not re.search(r"[\u0900-\u097f]", text)
    ):
        return None
    body, citation = source_tail(text)
    if not body:
        return None
    if (
        DISPLAY_SOURCE_KEYWORD_RE.search(body)
        and re.search(r"[IVXLC\d]", body)
        and not re.search(r"[\u0900-\u097f]", body)
    ):
        return None
    devanagari_ranges = [match.span() for match in DEVA_SPAN_RE.finditer(body)]
    if devanagari_ranges:
        selected = [
            annotation for annotation in annotations
            if any(
                int(annotation["start"]) < end and int(annotation["end"]) > start
                for start, end in devanagari_ranges
            )
        ]
    else:
        selected = [annotation for annotation in annotations if int(annotation["start"]) < len(body)]
    if not selected:
        return None
    selected.sort(key=lambda row: (int(row["start"]), int(row["end"]), row["id"]))
    words = []
    segments = []
    surfaces = []
    for annotation in selected:
        local_words = annotation.get("words", [])
        if not local_words:
            continue
        indices = []
        for word in local_words:
            indices.append(len(words))
            words.append(normalized_display_word(word, len(words)))
        raw_surface = str(annotation.get("text", "")).strip(' \t\n\"“”‘’')
        if annotation.get("language") == "sa-Deva":
            surface = raw_surface
        elif DISPLAY_IAST_MARK_RE.search(raw_surface):
            surface = transliterate(raw_surface, sanscript.IAST, sanscript.DEVANAGARI)
        else:
            forms = []
            for word in local_words:
                form = str(word.get("deva", ""))
                if not re.search(r"[\u0900-\u097f]", form):
                    form = transliterate(
                        str(word.get("iast", "")).removeprefix("√"),
                        sanscript.IAST,
                        sanscript.DEVANAGARI,
                    )
                forms.append(form)
            surface = " ".join(forms)
        surface = surface.strip(' \t\n\"“”‘’.,।॥')
        if not surface:
            continue
        if surfaces:
            segments.append({"text": " ", "word_indices": []})
        surfaces.append(surface)
        segments.append({"text": surface, "word_indices": indices})
    devanagari = " ".join(surfaces)
    if not devanagari or re.search(r"[A-Za-z]", devanagari):
        raise ValueError(f"normalized standalone quotation retains Latin text: {text!r}")
    start = min(int(annotation["start"]) for annotation in selected)
    end = max(int(annotation["end"]) for annotation in selected)
    before = clean_display_english(body[:start])
    after = clean_display_english(body[end:], allow_short_quote=True)
    return {
        "content_class": "partial_cited_fragment",
        "render_mode": "display_fragment",
        "source_authority": "site_normalized_fragment",
        "citation_completeness": "fragment",
        "promotion_eligible": False,
        "literal_translation_source": "none",
        "display_devanagari": devanagari,
        "display_words": words,
        "display_source_segments": segments,
        "display_before": before,
        "display_after": after,
        "display_citation": citation,
        "display_policy": "normalized-devanagari-from-reviewed-word-records",
    }


def promote_inline_blocks(name_number: int, blocks: list[dict]) -> list[dict]:
    occurrences = OCCURRENCES_BY_NAME.get(int(name_number), [])
    if not occurrences:
        return blocks
    by_text: dict[str, list[dict]] = {}
    for occurrence in occurrences:
        match_text = occurrence["text"].strip("-—–") or occurrence["text"]
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
            display = normalized_quote_display(text, block["inline_sanskrit"])
            if display:
                block.update(display)
        result.append(block)
    return result


def ascii_attachment_report() -> dict:
    return {
        "accepted": len(ASCII_ACCEPTED_IDS),
        "attached_to_prose": len(ASCII_ATTACHED_IDS),
        "represented_by_structured_blocks": len(ASCII_STRUCTURED_IDS),
        "unaccounted_ids": sorted(ASCII_ACCEPTED_IDS - ASCII_ATTACHED_IDS - ASCII_STRUCTURED_IDS),
    }

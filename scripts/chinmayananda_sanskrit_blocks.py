"""Promote reviewed non-Gītā Sanskrit prose into interactive reader blocks."""

from __future__ import annotations

import difflib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHARDS = tuple(sorted((ROOT / "gita/vishnu-sahasranama").glob("commentary-sanskrit-analysis-*.json")))


def load_rows() -> dict[int, list[dict]]:
    by_name: dict[int, list[dict]] = {}
    seen = set()
    for path in SHARDS:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("review_status") != "primary-grammar-reviewed-complete":
            raise ValueError(f"non-Gītā Sanskrit shard is not complete: {path.name}")
        if data.get("withheld"):
            raise ValueError(f"non-Gītā Sanskrit shard has withheld rows: {path.name}")
        for quote_id, row in data.get("quotes", {}).items():
            if quote_id in seen:
                raise ValueError(f"duplicate non-Gītā Sanskrit row {quote_id}")
            seen.add(quote_id)
            by_name.setdefault(int(row["name_number"]), []).append(row)
    if len(seen) != 54:
        raise ValueError(f"expected 54 reviewed non-Gītā Sanskrit rows, found {len(seen)}")
    return by_name


ROWS_BY_NAME = load_rows()


def reader_word(word: dict) -> dict:
    result = {
        "i": word["i"],
        "iast": word["iast"],
        "deva": word["deva"],
        "gloss": word["gloss"],
        "parts": word["parts"],
        "stem": word["stem"],
        "affix": word["affix"],
        "morph": word["morph"],
    }
    root = word.get("root")
    if isinstance(root, dict):
        result["root"] = root["form"]
        result["rootGloss"] = root["gloss"]
        dhatu = root.get("dhatupatha") or {}
        notes = [f"{root['gana']}; {root['pada']}"]
        if dhatu:
            notes.append(f"Dhātupāṭha {dhatu['locus']}: {dhatu['artha_sanskrit']}")
        result["note"] = " · ".join(notes)
    roots = word.get("roots")
    if roots:
        result["roots"] = roots
        root_notes = [
            f"{root['form']} · {root['gana']}; {root['pada']} · "
            f"Dhātupāṭha {root['dhatupatha']['locus']}: {root['dhatupatha']['artha_sanskrit']}"
            for root in roots
        ]
        result["note"] = " · ".join(root_notes)
    return result


def clean_tail(value: str, source_iast: str = "") -> str:
    tail = value.strip()
    tail = re.sub(r'^["\'”’]+\s*', "", tail)
    roman = re.match(r"^\([^)]{2,800}\)\s*", tail)
    if roman:
        tail = tail[roman.end():].strip()
    printed_roman = re.match(r'^([^"“]{3,800}(?:\)|\.))\s*(?=["“])', tail)
    if printed_roman and source_iast:
        similarity = difflib.SequenceMatcher(
            a=prose_key(printed_roman.group(1)),
            b=prose_key(source_iast),
            autojunk=False,
        ).ratio()
        if similarity >= 0.40:
            tail = tail[printed_roman.end():].strip()
    again = re.search(r"\bAgain\b", tail)
    if again:
        tail = tail[again.start():].strip()
    elif tail.startswith(("—", "–", "-")) and len(tail) < 180:
        return ""
    tail = re.sub(r"^[\s.;:—–-]+", "", tail).strip()
    return re.sub(r',(["”])$', r'.\1', tail)


def prose_key(value: str) -> str:
    folded = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", folded)


def quote_block(row: dict, source_paragraph_index: int | None = None) -> dict:
    block = {
        "type": "sanskrit-quote",
        "id": row["quote_id"],
        "content_class": "complete_quote",
        "render_mode": "footnote_quote",
        "source_authority": "chinmayananda_printed_quote",
        "citation_completeness": "complete",
        "promotion_eligible": True,
        "literal_translation_source": (
            "chinmayananda" if row.get("english_source") == "Swami Chinmayananda"
            else "site_literal" if row.get("english_source") == "site-literal-translation"
            else "none"
        ),
        "devanagari": row["canonical_devanagari"],
        "source_iast": row["source_iast"],
        "iast": row["iast"],
        "source_segments": row["source_segments"],
        "english": row["english"],
        "english_slots": row["english_slots"],
        "english_source": row["english_source"],
        "words": [reader_word(word) for word in row["words"]],
        "word_analysis_status": "primary-grammar-reviewed",
        "printed_loci": [row["source_label"]],
        "canonical_locus": row["canonical_locus"],
        "textual_notes": row["textual_notes"],
    }
    if source_paragraph_index is not None:
        block["source_paragraph_index"] = source_paragraph_index
    return block


def promote_non_gita_blocks(name_number: int, blocks: list[dict]) -> list[dict]:
    rows = ROWS_BY_NAME.get(int(name_number), [])
    if not rows:
        return blocks
    complete_prose_key = prose_key(" ".join(
        block.get("text", "") for block in blocks if block.get("type") == "prose"
    ))
    remaining = {row["quote_id"]: row for row in rows}
    result = []
    for block in blocks:
        if block.get("type") != "prose":
            result.append(block)
            continue
        text = block.get("text", "")
        matched = next(
            (row for row in remaining.values() if text.startswith(row["printed_devanagari"])),
            None,
        )
        if not matched:
            result.append(block)
            continue
        promoted = quote_block(matched, block.get("source_paragraph_index"))
        tail = clean_tail(text[len(matched["printed_devanagari"]):], matched.get("source_iast", ""))
        if matched.get("english_source") == "Swami Chinmayananda":
            author_english = str(matched.get("english", "")).strip()
            if author_english and prose_key(author_english) not in complete_prose_key:
                promoted["display_english"] = True
        if tail:
            result.append({
                "type": "prose",
                "text": tail,
                "source_paragraph_index": block.get("source_paragraph_index"),
            })
        result.append(promoted)
        del remaining[matched["quote_id"]]
    if remaining:
        raise ValueError(
            f"name {name_number} did not promote reviewed Sanskrit rows: {sorted(remaining)}"
        )
    return result

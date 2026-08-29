"""Promote reviewed non-Gītā Sanskrit prose into interactive reader blocks."""

from __future__ import annotations

import json
import re
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


def clean_tail(value: str) -> str:
    tail = value.strip()
    tail = re.sub(r'^["”’]+\s*', "", tail)
    roman = re.match(r"^\([^)]{2,800}\)\s*", tail)
    if roman:
        tail = tail[roman.end():].strip()
    again = re.search(r"\bAgain\b", tail)
    if again:
        tail = tail[again.start():].strip()
    elif tail.startswith(("—", "–", "-")) and len(tail) < 180:
        return ""
    return re.sub(r"^[\s.;:—–-]+", "", tail).strip()


def quote_block(row: dict) -> dict:
    return {
        "type": "sanskrit-quote",
        "id": row["quote_id"],
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


def promote_non_gita_blocks(name_number: int, blocks: list[dict]) -> list[dict]:
    rows = ROWS_BY_NAME.get(int(name_number), [])
    if not rows:
        return blocks
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
        result.append(quote_block(matched))
        tail = clean_tail(text[len(matched["printed_devanagari"]):])
        if tail:
            result.append({"type": "prose", "text": tail})
        del remaining[matched["quote_id"]]
    if remaining:
        raise ValueError(
            f"name {name_number} did not promote reviewed Sanskrit rows: {sorted(remaining)}"
        )
    return result

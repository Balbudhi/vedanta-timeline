#!/usr/bin/env python3
"""Map exact Devanāgarī source chunks to segmented analysis word indices."""

from __future__ import annotations

import difflib
import functools
import json
import re
import unicodedata
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
PATHS = tuple(sorted((ROOT / "gita/vishnu-sahasranama").glob("commentary-sanskrit-analysis-*.json")))
GITA_REGISTRY = ROOT / "gita/vishnu-sahasranama/commentary-quotes.json"
GITA_ANALYSIS = ROOT / "gita/vishnu-sahasranama/commentary-quote-analysis.json"


def key(value: str) -> str:
    value = unicodedata.normalize("NFC", value).lower().replace("~", "ṃ")
    return re.sub(r"[^a-zāīūṛṝḷṅñṭḍṇśṣṃḥ]", "", value)


def similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    ratio = difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()
    length = min(len(left), len(right)) / max(len(left), len(right))
    return ratio * length ** 0.35


def source_chunks(devanagari: str) -> list[str]:
    raw = re.findall(r"\S+\s*", devanagari)
    chunks = []
    pending = ""
    for token in raw:
        lexical = re.sub(r"[।॥\s]", "", token)
        if lexical:
            chunks.append(pending + token)
            pending = ""
        elif chunks:
            chunks[-1] += token
        else:
            pending += token
    if pending and chunks:
        chunks[-1] += pending
    return chunks


def align(devanagari: str, words: list[dict]) -> tuple[list[dict], float]:
    chunks = source_chunks(devanagari)
    source_keys = [
        key(transliterate(chunk, sanscript.DEVANAGARI, sanscript.IAST))
        for chunk in chunks
    ]
    word_keys = [key(word["iast"]) for word in words]
    m, n = len(source_keys), len(word_keys)
    if not m or m > n:
        raise ValueError(f"cannot partition {m} source chunks across {n} analysis words")

    @functools.lru_cache(None)
    def solve(source_index: int, word_index: int) -> tuple[float, tuple[tuple[int, int, float], ...]]:
        if source_index == m:
            return (0.0, ()) if word_index == n else (-10**9, ())
        remaining_chunks = m - source_index - 1
        best = (-10**9, ())
        for end in range(word_index + 1, n - remaining_chunks + 1):
            score = similarity(source_keys[source_index], "".join(word_keys[word_index:end]))
            tail_score, tail = solve(source_index + 1, end)
            candidate = (score + tail_score, ((word_index, end, score),) + tail)
            if candidate[0] > best[0]:
                best = candidate
        return best

    total, partition = solve(0, 0)
    average = total / m
    if average < 0.65:
        raise ValueError(f"weak source/word alignment: {average:.3f}")
    segments = [
        {"text": chunk, "word_indices": list(range(start, end))}
        for chunk, (start, end, _) in zip(chunks, partition)
    ]
    if "".join(segment["text"] for segment in segments) != devanagari:
        raise ValueError("source segments do not replay Devanāgarī")
    return segments, round(average, 4)


def main() -> None:
    rows = 0
    gita_rows = 0
    scores = []
    for path in PATHS:
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data.get("quotes", {}).values():
            segments, score = align(row["canonical_devanagari"], row["words"])
            row["source_segments"] = segments
            row["source_alignment_score"] = score
            rows += 1
            scores.append(score)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    registry = {
        row["id"]: row
        for row in json.loads(GITA_REGISTRY.read_text(encoding="utf-8"))["quotes"]
    }
    analysis = json.loads(GITA_ANALYSIS.read_text(encoding="utf-8"))
    for quote_id, row in analysis["quotes"].items():
        segments, score = align(registry[quote_id]["canonical_devanagari"], row["words"])
        row["source_segments"] = segments
        row["source_alignment_score"] = score
        gita_rows += 1
        scores.append(score)
    GITA_ANALYSIS.write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "non_gita_rows": rows,
        "gita_rows": gita_rows,
        "minimum_score": min(scores),
    }, indent=2))


if __name__ == "__main__":
    main()

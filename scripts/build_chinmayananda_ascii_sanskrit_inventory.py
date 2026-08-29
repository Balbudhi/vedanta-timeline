#!/usr/bin/env python3
"""Inventory undiacritized Roman Sanskrit left outside the reviewed inline map.

This is a locator, not Sanskrit authority.  It proposes tokens only when their
ASCII spelling folds to a Sanskrit form already present in a reviewed name,
quotation, inline popup, preface word, or glossary headword.  Human review must
still accept or reject each occurrence in context.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMENTARY = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
INLINE = ROOT / "internal/sanskrit_reviews/inline-sanskrit-inventory.json"
OUTPUT = ROOT / "internal/sanskrit_reviews/ascii-sanskrit-candidate-inventory.json"
TOKEN_RE = re.compile(r"(?<![A-Za-zĀ-ỹÑñ])[A-Za-z][A-Za-zĀ-ỹÑñ'’\-]*(?![A-Za-zĀ-ỹÑñ])")
ROMAN_NUMERAL_RE = re.compile(r"^[IVXLCDM]+$")
ENGLISH_STOP = {
    "a", "am", "an", "and", "are", "as", "at", "be", "because", "been",
    "being", "but", "by", "can", "could", "did", "do", "does", "for",
    "from", "go", "had", "has", "have", "he", "her", "here", "him", "his",
    "how", "i", "if", "in", "into", "is", "it", "its", "may", "me", "more",
    "most", "must", "my", "new", "no", "non", "not", "of", "on", "one",
    "only", "or", "our", "out", "over", "same", "should", "so", "such",
    "than", "that", "the", "their", "them", "then", "there", "these", "they",
    "this", "those", "through", "to", "under", "up", "was", "way", "we",
    "were", "what", "when", "where", "which", "who", "why", "will", "with",
    "would", "you", "your", "dark", "destination", "effect", "ending",
    "finite", "glory", "people", "perfect", "put", "ten",
}


def fold(value: str) -> str:
    value = unicodedata.normalize("NFD", str(value or "").lower().replace("√", ""))
    return re.sub(r"[^a-z]", "", "".join(char for char in value if unicodedata.category(char) != "Mn"))


def add_form(lookup: dict[str, set[str]], value: object) -> None:
    text = str(value or "").strip()
    for token in re.findall(r"[A-Za-zĀ-ỹ]+", text):
        key = fold(token)
        if len(key) > 1 and key not in ENGLISH_STOP:
            lookup[key].add(token)


def reviewed_lexicon() -> dict[str, set[str]]:
    lookup: dict[str, set[str]] = defaultdict(set)
    analysis = json.loads((ROOT / "gita/vishnu-sahasranama/analysis.json").read_text(encoding="utf-8"))
    for row in analysis["names"]:
        add_form(lookup, row.get("citation_iast"))
        add_form(lookup, row.get("stem"))
    for path in [
        ROOT / "gita/vishnu-sahasranama/commentary-quote-analysis.json",
        *(ROOT / "gita/vishnu-sahasranama").glob("commentary-sanskrit-analysis-[0-9]*.json"),
        ROOT / "gita/vishnu-sahasranama/preface-analysis.json",
    ]:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data.get("quotes", {}).values() if "quotes" in data else [
            unit for group in data.get("groups", []) for unit in group.get("units", [])
        ] + data.get("postlude", [])
        for row in rows:
            for word in row.get("words", []):
                add_form(lookup, word.get("iast"))
                add_form(lookup, word.get("stem"))
    for path in (ROOT / "internal/sanskrit_reviews").glob("inline-analysis-shard-[0-3].json"):
        for unit in json.loads(path.read_text(encoding="utf-8"))["rows"].values():
            popup = unit.get("popup")
            if popup:
                for word in popup.get("words", []):
                    add_form(lookup, word.get("iast"))
                    add_form(lookup, word.get("stem"))
    for path in (ROOT / "data/glossary").glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not data.get("term_devanagari"):
            continue
        head = data.get("term_iast")
        add_form(lookup, head)
        head_fold = fold(head)
        for alias in data.get("aliases", []):
            if fold(alias) == head_fold:
                add_form(lookup, alias)
    return lookup


def main() -> None:
    commentary = json.loads(COMMENTARY.read_text(encoding="utf-8"))["names"]
    inline = json.loads(INLINE.read_text(encoding="utf-8"))
    occupied: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for row in inline["occurrences"]:
        occupied[(int(row["name_number"]), int(row["paragraph_index"]))].append(
            (int(row["source_start"]), int(row["source_end"]))
        )
    lexicon = reviewed_lexicon()
    rows = []
    for name in commentary:
        number = int(name["number"])
        for paragraph_index, paragraph in enumerate(name["commentary"].split("\n\n")):
            token_index = 0
            for match in TOKEN_RE.finditer(paragraph):
                token = match.group().strip("-'’")
                token_fold = fold(token)
                if (
                    not token
                    or token_fold in ENGLISH_STOP
                    or ROMAN_NUMERAL_RE.fullmatch(token)
                    or token_fold not in lexicon
                    or any(match.start() < end and match.end() > start for start, end in occupied[(number, paragraph_index)])
                ):
                    continue
                rows.append({
                    "id": f"name-{number}-paragraph-{paragraph_index}-ascii-{token_index}",
                    "name_number": number,
                    "paragraph_index": paragraph_index,
                    "source_start": match.start(),
                    "source_end": match.end(),
                    "text": match.group(),
                    "folded": token_fold,
                    "candidate_iast_forms": sorted(lexicon[token_fold]),
                    "context": paragraph[max(0, match.start() - 90):match.end() + 90],
                    "review_status": "pending-context-review",
                })
                token_index += 1
    data = {
        "schema_version": 1,
        "purpose": "candidate locator only; not grammatical or textual authority",
        "candidate_occurrences": len(rows),
        "candidates": rows,
    }
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "candidate_occurrences": len(rows),
        "unique_ascii_forms": len({row["text"].lower() for row in rows}),
    }, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Account for every Devanāgarī span in Chinmayananda's commentary.

This is a population/shape audit only.  It does not infer a source, repair a
reading, translate Sanskrit, or promote OCR into a public witness.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMENTARY = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
GITA_QUOTES = ROOT / "gita/vishnu-sahasranama/commentary-quotes.json"

DEVA_RE = re.compile(r"[\u0900-\u097f][\u0900-\u097f\u200c\u200d\s।॥,;:…\-–—()]+")
IAST_TOKEN_RE = re.compile(r"(?<![A-Za-zĀ-ỹÑñ])(?:√)?[A-Za-zĀ-ỹÑñ'’\-]+")
IAST_MARK_RE = re.compile(r"[āīūṛṝḷṅñṭḍṇśṣṃṁḥ]|^√")
NON_SANSKRIT_HYPHEN_COMPONENTS = {
    "conch", "dark", "destination", "effect", "glory", "of", "people",
    "subjective", "world",
}

# These paragraphs begin with a short Devanāgarī label, not a freestanding
# Sanskrit passage.  They stay in the inline population.
INLINE_LEADING_LABELS = {
    "name-107-paragraph-1-span-0",  # rūpam, followed by English exposition
    "name-824-paragraph-1-span-0",  # śvaḥ, the first item in an inline equation
}

EXPECTED = {
    "deva_spans": 491,
    "existing_gita_source_spans": 141,
    "existing_gita_blocks": 142,
    "standalone_non_gita_spans": 54,
    "inline_non_gita_spans": 296,
    "iast_marked_instances": 2457,
    "iast_marked_unique_forms": 507,
}


def trim_mixed_iast_token(token: str) -> tuple[str, int, int]:
    """Exclude English sides of OCR-style English–Sanskrit hyphen strings."""
    pieces = list(re.finditer(r"[^-]+", token))
    first, last = 0, len(pieces)
    while first < last and pieces[first].group().strip("'’").lower() in NON_SANSKRIT_HYPHEN_COMPONENTS:
        first += 1
    while last > first and pieces[last - 1].group().strip("'’").lower() in NON_SANSKRIT_HYPHEN_COMPONENTS:
        last -= 1
    if first == last:
        return token, 0, len(token)
    start, end = pieces[first].start(), pieces[last - 1].end()
    return token[start:end], start, end


def clean_span(value: str) -> str:
    return " ".join(value.split()).strip(" -–—(),;:")


def gita_source_ids(data: dict) -> set[str]:
    return {
        re.sub(r"-piece-\d+$", "", row["id"])
        for row in data["quotes"]
    }


def build() -> dict:
    commentary = json.loads(COMMENTARY.read_text(encoding="utf-8"))
    gita = json.loads(GITA_QUOTES.read_text(encoding="utf-8"))
    represented = gita_source_ids(gita)
    rows = []
    iast_rows = []

    for name in commentary["names"]:
        paragraphs = name["commentary"].split("\n\n")
        for paragraph_index, paragraph in enumerate(paragraphs):
            leading_offset = len(paragraph) - len(paragraph.lstrip())
            for span_index, match in enumerate(DEVA_RE.finditer(paragraph)):
                text = clean_span(match.group())
                span_id = (
                    f"name-{name['number']}-paragraph-{paragraph_index}"
                    f"-span-{span_index}"
                )
                if span_id in represented:
                    status = "existing-gita-source-span"
                elif match.start() == leading_offset and span_id not in INLINE_LEADING_LABELS:
                    status = "standalone-non-gita-candidate"
                else:
                    status = "inline-non-gita-candidate"
                rows.append({
                    "id": span_id,
                    "name_number": name["number"],
                    "paragraph_index": paragraph_index,
                    "span_index": span_index,
                    "source_start": match.start(),
                    "source_end": match.end(),
                    "text": text,
                    "status": status,
                    "paragraph": paragraph,
                })
            for token_index, match in enumerate(IAST_TOKEN_RE.finditer(paragraph)):
                token, trim_start, trim_end = trim_mixed_iast_token(match.group())
                if not IAST_MARK_RE.search(token):
                    continue
                iast_rows.append({
                    "id": (
                        f"name-{name['number']}-paragraph-{paragraph_index}"
                        f"-iast-{token_index}"
                    ),
                    "name_number": name["number"],
                    "paragraph_index": paragraph_index,
                    "token_index": token_index,
                    "source_start": match.start() + trim_start,
                    "source_end": match.start() + trim_end,
                    "text": token,
                    "normalized_form": token.lower().strip("-'’"),
                    "status": "iast-marked-candidate",
                })

    counts = {
        "deva_spans": len(rows),
        "existing_gita_source_spans": sum(
            row["status"] == "existing-gita-source-span" for row in rows
        ),
        "existing_gita_blocks": len(gita["quotes"]),
        "standalone_non_gita_spans": sum(
            row["status"] == "standalone-non-gita-candidate" for row in rows
        ),
        "inline_non_gita_spans": sum(
            row["status"] == "inline-non-gita-candidate" for row in rows
        ),
        "iast_marked_instances": len(iast_rows),
        "iast_marked_unique_forms": len({row["normalized_form"] for row in iast_rows}),
    }
    return {
        "schema_version": 1,
        "purpose": "closed-population shape audit; not translation or textual authority",
        "counts": counts,
        "spans": rows,
        "iast_spans": iast_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check and data["counts"] != EXPECTED:
        raise ValueError(f"Sanskrit population changed: {data['counts']} != {EXPECTED}")
    print(json.dumps(data["counts"] if args.summary else data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

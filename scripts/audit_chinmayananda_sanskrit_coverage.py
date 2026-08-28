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

# These paragraphs begin with a short Devanāgarī label, not a freestanding
# Sanskrit passage.  They stay in the inline population.
INLINE_LEADING_LABELS = {
    "name-107-paragraph-1-span-0",  # rūpam, followed by English exposition
    "name-824-paragraph-1-span-0",  # śvaḥ, the first item in an inline equation
}

EXPECTED = {
    "deva_spans": 489,
    "existing_gita_source_spans": 141,
    "existing_gita_blocks": 142,
    "standalone_non_gita_spans": 54,
    "inline_non_gita_spans": 294,
}


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

    for name in commentary["names"]:
        paragraphs = name["commentary"].split("\n\n")
        for paragraph_index, paragraph in enumerate(paragraphs):
            leading_offset = len(paragraph) - len(paragraph.lstrip())
            for span_index, match in enumerate(DEVA_RE.finditer(paragraph)):
                text = clean_span(match.group())
                if len(re.sub(r"\s", "", text)) < 2:
                    continue
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
    }
    return {
        "schema_version": 1,
        "purpose": "closed-population shape audit; not translation or textual authority",
        "counts": counts,
        "spans": rows,
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

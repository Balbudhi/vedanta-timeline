#!/usr/bin/env python3
"""Validate canonical presentation classes in the public Sahasranama reader."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "gita/vishnu-sahasranama/reader.json"
RENDERER = ROOT / "assets/sahasranama.js"

CONTENT_CLASSES = {
    "prose_sanskrit_term",
    "formula_nirvacana",
    "complete_quote",
    "partial_cited_fragment",
    "printed_footnote_prose",
    "work_title",
}
RENDER_MODES = {"inline", "prose", "footnote_note", "footnote_quote", "display_fragment"}
AUTHORITIES = {
    "chinmayananda_prose",
    "chinmayananda_printed_quote",
    "independently_verified_primary",
    "site_normalized_fragment",
}
COMPLETENESS = {"complete", "fragment", "derivational", "title_only", "term_only"}
LITERAL_SOURCES = {"none", "chinmayananda", "site_literal"}


def walk(blocks: list[dict]):
    for block in blocks:
        yield block
        if block.get("type") == "footnote":
            yield from walk(block.get("blocks", []))


def main() -> None:
    reader = json.loads(READER.read_text(encoding="utf-8"))
    errors: list[str] = []
    renderer = RENDERER.read_text(encoding="utf-8")
    for forbidden in ("PILOT_", "INLINE_SANSKRIT_REPAIRS", "INLINE_WORD_OVERRIDES", "INLINE_ITEM_OVERRIDES"):
        if forbidden in renderer:
            errors.append(f"renderer retains forbidden runtime review table marker: {forbidden}")
    counts: dict[str, int] = {}
    for name in reader["stanzas"]:
        for item in name["names"]:
            for block in walk(item.get("chinmayananda", {}).get("blocks", [])):
                kind = block.get("type")
                if kind not in {"prose", "footnote", "gita-quote", "sanskrit-quote"}:
                    continue
                label = f"name {item['number']} {kind} {block.get('id', block.get('source_paragraph_index', '?'))}"
                content_class = block.get("content_class")
                render_mode = block.get("render_mode")
                authority = block.get("source_authority")
                completeness = block.get("citation_completeness")
                literal = block.get("literal_translation_source")
                if content_class not in CONTENT_CLASSES:
                    errors.append(f"{label}: invalid content_class {content_class!r}")
                if render_mode not in RENDER_MODES:
                    errors.append(f"{label}: invalid render_mode {render_mode!r}")
                if authority not in AUTHORITIES:
                    errors.append(f"{label}: invalid source_authority {authority!r}")
                if completeness not in COMPLETENESS:
                    errors.append(f"{label}: invalid citation_completeness {completeness!r}")
                if literal not in LITERAL_SOURCES:
                    errors.append(f"{label}: invalid literal_translation_source {literal!r}")
                if kind in {"gita-quote", "sanskrit-quote"}:
                    if content_class != "complete_quote" or completeness != "complete" or block.get("promotion_eligible") is not True:
                        errors.append(f"{label}: quote promotion contract violated")
                if block.get("display_devanagari"):
                    if content_class != "partial_cited_fragment" or render_mode != "display_fragment" or block.get("promotion_eligible") is not False:
                        errors.append(f"{label}: display fragment contract violated")
                counts[content_class] = counts.get(content_class, 0) + 1
    if errors:
        raise SystemExit("\n".join(errors[:100]))
    print(json.dumps({"reader": str(READER.relative_to(ROOT)), "classes": counts}, indent=2))


if __name__ == "__main__":
    main()

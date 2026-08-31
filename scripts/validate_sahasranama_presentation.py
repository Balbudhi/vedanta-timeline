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
    for forbidden in (
        "PILOT_", "INLINE_SANSKRIT_REPAIRS", "INLINE_WORD_OVERRIDES", "INLINE_ITEM_OVERRIDES",
        "cm-vs-fn-", "name-2-paragraph-1-span-0",
    ):
        if forbidden in renderer:
            errors.append(f"renderer retains forbidden runtime review table marker: {forbidden}")
    counts: dict[str, int] = {}
    inline_occurrences = 0
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
                if content_class == "complete_quote":
                    if completeness != "complete" or block.get("promotion_eligible") is not True:
                        errors.append(f"{label}: complete quote contract violated")
                    if authority not in {"chinmayananda_printed_quote", "independently_verified_primary"}:
                        errors.append(f"{label}: complete quote has invalid authority")
                    if kind == "prose":
                        annotations = block.get("inline_sanskrit", [])
                        if len(annotations) != 1 or not annotations[0].get("presentation_payload"):
                            errors.append(f"{label}: prose quotation lacks one reviewed presentation payload")
                        if not block.get("display_citation"):
                            errors.append(f"{label}: prose quotation lacks a displayed citation")
                if block.get("display_devanagari"):
                    if content_class != "partial_cited_fragment" or render_mode != "display_fragment" or block.get("promotion_eligible") is not False:
                        errors.append(f"{label}: display fragment contract violated")
                for annotation in block.get("inline_sanskrit", []):
                    inline_occurrences += 1
                    annotation_label = f"{label} inline {annotation.get('id', '?')}"
                    # Inline occurrences inherit their authority, completeness,
                    # and visual role from the validated containing block; this
                    # avoids serving five duplicated fields 3,665 times.
                    if not annotation.get("words") or not annotation.get("source_segments"):
                        errors.append(f"{annotation_label}: lacks reviewed inline payload")
                    payload = annotation.get("presentation_payload")
                    if not payload:
                        continue
                    payload_words = payload.get("words", [])
                    payload_indices = [word.get("i") for word in payload_words]
                    if payload_indices != list(range(len(payload_words))):
                        errors.append(f"{label}: presentation payload has non-contiguous word analysis")
                    payload_segments = payload.get("source_segments", [])
                    if "".join(segment.get("text", "") for segment in payload_segments) != annotation.get("text"):
                        errors.append(f"{label}: presentation payload changes its printed source text")
                    covered = {int(index) for segment in payload_segments for index in segment.get("word_indices", [])}
                    if covered != set(range(len(payload_words))):
                        errors.append(f"{label}: presentation payload does not map every word")
                    if not payload.get("devanagari") or any("A" <= char <= "z" for char in payload["devanagari"]):
                        errors.append(f"{label}: presentation payload lacks a Devanāgarī display witness")
                if content_class == "formula_nirvacana":
                    payload = block.get("formula_payload")
                    if not payload:
                        errors.append(f"{label}: derivational note lacks a reviewed formula payload")
                    else:
                        words = payload.get("words", [])
                        segments = payload.get("source_segments", [])
                        if [word.get("i") for word in words] != list(range(len(words))):
                            errors.append(f"{label}: derivational payload has non-contiguous words")
                        if {int(index) for segment in segments for index in segment.get("word_indices", [])} != set(range(len(words))):
                            errors.append(f"{label}: derivational payload does not map every word")
                        if "".join(segment.get("text", "") for segment in segments) != payload.get("devanagari"):
                            errors.append(f"{label}: derivational payload changes Devanāgarī")
                        if not payload.get("english_slots") or payload.get("literal_translation_source") != "site_literal":
                            errors.append(f"{label}: derivational payload lacks a marked literal translation")
                counts[content_class] = counts.get(content_class, 0) + 1
    if errors:
        raise SystemExit("\n".join(errors[:100]))
    print(json.dumps({"reader": str(READER.relative_to(ROOT)), "classes": counts, "inline_occurrences": inline_occurrences}, indent=2))


if __name__ == "__main__":
    main()

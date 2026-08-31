#!/usr/bin/env python3
"""Validate canonical presentation classes in the public Sahasranama reader."""

from __future__ import annotations

import json
import re
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
EVIDENCE_ROLES = {"inline_mention", "claim_evidence", "derivation_formula", "note_prose", "translation_shadow", "work_title"}
EVIDENCE_SHAPES = {"none", "fragment_quote", "complete_quote", "inline_list", "formula", "shadow"}
INTERACTION_MODES = {"inline_token", "inline_phrase", "evidence_block", "derivation_block", "prose_note"}
TRANSLATION_SURFACES = {"none", "inline_only", "visible_literal_line", "source_owned_only"}
ANALYSIS_MODES = {"rooted_derivation", "compound_analysis", "inflected_lexeme", "indeclinable", "title_or_work_reference", "root_not_asserted"}


def walk(blocks: list[dict]):
    for block in blocks:
        yield block
        if block.get("type") == "footnote":
            yield from walk(block.get("blocks", []))


def validate_analysis_modes(words: list[dict], label: str, errors: list[str]) -> None:
    for word in words:
        if word.get("analysis_mode") not in ANALYSIS_MODES:
            errors.append(f"{label}: word {word.get('i', '?')} lacks valid analysis_mode")


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
                evidence_role = block.get("evidence_role")
                evidence_shape = block.get("evidence_shape")
                interaction_mode = block.get("interaction_mode")
                translation_surface = block.get("translation_surface")
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
                if evidence_role not in EVIDENCE_ROLES:
                    errors.append(f"{label}: invalid evidence_role {evidence_role!r}")
                if evidence_shape not in EVIDENCE_SHAPES:
                    errors.append(f"{label}: invalid evidence_shape {evidence_shape!r}")
                if interaction_mode not in INTERACTION_MODES:
                    errors.append(f"{label}: invalid interaction_mode {interaction_mode!r}")
                if translation_surface not in TRANSLATION_SURFACES:
                    errors.append(f"{label}: invalid translation_surface {translation_surface!r}")
                allowed_surface = {
                    ("inline_mention", "none", "inline_token"),
                    ("inline_mention", "none", "inline_phrase"),
                    ("claim_evidence", "fragment_quote", "evidence_block"),
                    ("claim_evidence", "complete_quote", "evidence_block"),
                    ("derivation_formula", "formula", "derivation_block"),
                    ("note_prose", "none", "prose_note"),
                    ("note_prose", "none", "inline_token"),
                    ("note_prose", "none", "inline_phrase"),
                    ("note_prose", "inline_list", "inline_phrase"),
                    ("translation_shadow", "shadow", "prose_note"),
                }
                if (evidence_role, evidence_shape, interaction_mode) not in allowed_surface:
                    errors.append(f"{label}: illegal evidence surface {evidence_role}/{evidence_shape}/{interaction_mode}")
                if evidence_role == "inline_mention" and literal != "none":
                    errors.append(f"{label}: inline mention may not carry a site literal")
                if evidence_role in {"claim_evidence", "derivation_formula"} and translation_surface != "visible_literal_line":
                    errors.append(f"{label}: evidence surface must expose a literal English line")
                if evidence_role in {"note_prose", "translation_shadow"} and block.get("render_mode") == "display_fragment":
                    errors.append(f"{label}: note/shadow may not render as a standalone Sanskrit block")
                if kind == "footnote":
                    child_roles = {child.get("evidence_role") for child in block.get("blocks", [])}
                    if "claim_evidence" in child_roles and len(child_roles - {"claim_evidence"}) > 0:
                        if block.get("bundle_contract") != "typed_children":
                            errors.append(f"{label}: mixed evidence bundle lacks typed-child contract")
                        allowed_roles = {"claim_evidence", "translation_shadow", "note_prose", "derivation_formula"}
                        if not child_roles <= allowed_roles:
                            errors.append(f"{label}: mixed evidence bundle contains an unapproved child role")
                validate_analysis_modes(block.get("words", []), label, errors)
                validate_analysis_modes(block.get("display_words", []), label, errors)
                validate_analysis_modes(block.get("display_payload", {}).get("words", []), label, errors)
                validate_analysis_modes(block.get("formula_payload", {}).get("words", []), label, errors)
                site_literal = block.get("site_literal")
                if site_literal:
                    english_slots = site_literal.get("english_slots") or site_literal.get("englishSlots")
                    if english_slots and not site_literal.get("text"):
                        errors.append(f"{label}: site literal lacks a plain-English fallback")
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
                    if kind in {"gita-quote", "sanskrit-quote"} and not (block.get("english_slots") or block.get("site_literal", {}).get("english_slots")):
                        errors.append(f"{label}: complete quotation lacks a slotted English rendering")
                if block.get("display_devanagari"):
                    if content_class != "partial_cited_fragment" or render_mode != "display_fragment" or block.get("promotion_eligible") is not False:
                        errors.append(f"{label}: display fragment contract violated")
                    display_words = block.get("display_payload", {}).get("words") or block.get("display_words", [])
                    slots = block.get("site_literal", {}).get("english_slots", "")
                    slot_indices = {
                        int(index)
                        for group in re.findall(r"\{([\d,\s]+):", slots)
                        for index in group.split(",") if index.strip()
                    }
                    if slot_indices != set(range(len(display_words))):
                        errors.append(f"{label}: display fragment lacks a complete slotted English rendering")
                for annotation in block.get("inline_sanskrit", []):
                    inline_occurrences += 1
                    annotation_label = f"{label} inline {annotation.get('id', '?')}"
                    # Inline occurrences inherit their authority, completeness,
                    # and visual role from the validated containing block; this
                    # avoids serving five duplicated fields 3,665 times.
                    if not annotation.get("words") or not annotation.get("source_segments"):
                        errors.append(f"{annotation_label}: lacks reviewed inline payload")
                    validate_analysis_modes(annotation.get("words", []), annotation_label, errors)
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

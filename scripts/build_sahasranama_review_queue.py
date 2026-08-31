#!/usr/bin/env python3
"""Freeze review inputs and enumerate defects without certifying old analyses.

This is an audit producer, not a public-content generator. Every review unit
starts pending, including units for which the mechanical scan finds no issue.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "gita/vishnu-sahasranama/reader.json"
SOURCE = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
DEFAULT_OUTPUT = ROOT / "internal/sanskrit_reviews/reader-review-queue.json"
GENERIC_MORPH = {
    "quoted lexical form", "lexical citation form", "inline Sanskrit token",
    "nominal citation/inflected form", "inflected nominal form in inline phrase",
}


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def walk(blocks: list[dict], pointer: str):
    for index, block in enumerate(blocks):
        location = f"{pointer}/{index}"
        yield block, location
        if block.get("type") == "footnote":
            yield from walk(block.get("blocks", []), f"{location}/blocks")


def surfaces(blocks: list[dict], pointer: str):
    """Select renderer-consumed payloads; don't count hidden alternate copies."""
    for index, block in enumerate(blocks):
        location = f"{pointer}/{index}"
        if block.get("type") == "footnote":
            if block.get("formula_payload"):
                yield block["formula_payload"], f"{location}/formula_payload", block
            else:
                yield from surfaces(block.get("blocks", []), f"{location}/blocks")
        elif block.get("display_devanagari"):
            payload = block.get("display_payload")
            if payload:
                yield payload, f"{location}/display_payload", block
            else:
                yield {"words": block.get("display_words", [])}, f"{location}/display_words", block
        elif block.get("type") in {"gita-quote", "sanskrit-quote"}:
            yield block, location, block
        else:
            for annotation_index, annotation in enumerate(block.get("inline_sanskrit", [])):
                annotation_path = f"{location}/inline_sanskrit/{annotation_index}"
                if annotation.get("presentation_payload"):
                    yield annotation["presentation_payload"], f"{annotation_path}/presentation_payload", block
                else:
                    yield annotation, annotation_path, block


def build_report(source: dict, reader: dict) -> dict:
    source_names = source["names"]
    reader_names = [(si, ni, n) for si, stanza in enumerate(reader["stanzas"])
                    for ni, n in enumerate(stanza["names"])]
    if [n["number"] for n in source_names] != list(range(1, 1001)):
        raise ValueError("Source population is not exactly 1–1000")
    if [n["number"] for _, _, n in reader_names] != list(range(1, 1001)):
        raise ValueError("Reader population is not exactly 1–1000")
    issues, units, name_rows = [], [], []
    categories = Counter()

    def issue(number, pointer, code, detail):
        identity = digest(f"{number}:{pointer}:{code}".encode())[:20]
        issues.append({"id": f"issue-{identity}", "name_number": number,
                       "reader_pointer": pointer, "code": code, "detail": detail,
                       "status": "open"})

    for si, ni, name in reader_names:
        number = name["number"]
        original = source_names[number - 1]
        base = f"/stanzas/{si}/names/{ni}/chinmayananda/blocks"
        blocks = name.get("chinmayananda", {}).get("blocks", [])
        start_issue_count = len(issues)
        unit_ids = []
        for block, location in walk(blocks, base):
            category = "/".join(str(block.get(k, "none")) for k in
                                ("type", "evidence_role", "evidence_shape"))
            categories[category] += 1
            if block.get("site_literal", {}).get("note") == "Word-for-word rendering — site":
                issue(number, location, "GLOSS_JOIN_REQUIRES_TRANSLATION_REVIEW",
                      "Visible English was assembled from word glosses, not independently translated as a passage.")
            locus = str(block.get("canonical_locus", ""))
            if block.get("content_class") == "complete_quote" and re.search(r"formula|synonym list|nirvacana", locus, re.I):
                issue(number, location, "QUOTE_ROLE_CONFLICTS_WITH_SOURCE_DESCRIPTION", locus)
            if block.get("evidence_role") == "translation_shadow" and not block.get("shadow_of"):
                issue(number, location, "SHADOW_WITHOUT_TARGET", "No exact quotation target is recorded.")

        for index, block in enumerate(blocks[:-2]):
            if (block.get("type") == "prose" and re.search(r"\bsays:\s*$", block.get("text", ""))
                    and blocks[index + 1].get("type") == "footnote"
                    and blocks[index + 2].get("content_class") == "complete_quote"):
                issue(number, f"{base}/{index}", "QUOTE_INTRO_INTERRUPTED",
                      "A footnote separates the quotation introduction from the quotation.")

        for payload, location, block in surfaces(blocks, base):
            words = payload.get("words", [])
            if not words:
                issue(number, location, "EMPTY_PUBLIC_WORD_PAYLOAD", "Renderer-selected Sanskrit payload has no words.")
                continue
            unit_hash = digest(json.dumps({"payload": payload, "context": block.get("text", "")},
                                         ensure_ascii=False, sort_keys=True).encode())
            unit_id = f"unit-{number}-{digest(location.encode())[:12]}"
            unit_ids.append(unit_id)
            units.append({"id": unit_id, "name_number": number,
                          "reader_pointer": location, "content_sha256": unit_hash,
                          "word_count": len(words), "review_status": "pending",
                          "reviews": {"source": "pending", "linguistic": "pending", "rendered": "pending"}})
            for word in words:
                word_location = f"{location}/word/{word.get('i', '?')}"
                if word.get("morph", "") in GENERIC_MORPH:
                    issue(number, word_location, "GENERIC_MORPHOLOGY", word["morph"])
                deva = str(word.get("deva", ""))
                if re.search(r"[A-Za-z]", deva) and not re.search(r"[\u0900-\u097f]", deva):
                    issue(number, word_location, "LATIN_IN_DEVANAGARI_FIELD", deva)
                if not word.get("gloss") or not word.get("parts") or not word.get("morph"):
                    issue(number, word_location, "INCOMPLETE_WORD_ANALYSIS", str(word.get("iast", "")))

        name_rows.append({"number": number, "source_sha256": digest(original["commentary"].encode()),
                          "source_paragraph_count": len(original["commentary"].split("\n\n")),
                          "scan_pages": original.get("scan_pages", []),
                          "review_status": "pending", "unit_ids": unit_ids,
                          "mechanical_issue_count": len(issues) - start_issue_count})
    return {
        "schema_version": 1,
        "status": "audit-only-not-publication-approval",
        "scope": "All 1,000 source names and renderer-selected commentary Sanskrit payloads; candidate detection still requires source review.",
        "sources": [{"path": str(path.relative_to(ROOT)), "sha256": digest(path.read_bytes())}
                    for path in (SOURCE, READER)],
        "counts": {"names": len(name_rows), "review_units": len(units),
                   "word_records": sum(u["word_count"] for u in units),
                   "open_mechanical_issues": len(issues),
                   "issues_by_code": dict(sorted(Counter(i["code"] for i in issues).items()))},
        "categories": dict(sorted(categories.items())), "names": name_rows,
        "review_units": units, "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Compare the frozen queue without changing it")
    parser.add_argument("--packet-numbers", type=int, nargs="*", default=[])
    parser.add_argument("--packet-dir", type=Path,
                        default=ROOT / "internal/sanskrit_reviews/reader-packets")
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    reader = json.loads(READER.read_text())
    report = build_report(source, reader)
    if args.check:
        if not args.output.exists() or json.loads(args.output.read_text()) != report:
            raise SystemExit("Review queue is missing or stale against its source hashes")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if args.packet_numbers:
        if args.check:
            raise SystemExit("--check cannot write review packets")
        if any(number not in range(1, 1001) for number in args.packet_numbers):
            raise SystemExit("Packet numbers must be between 1 and 1000")
        reader_names = {n["number"]: n for s in reader["stanzas"] for n in s["names"]}
        args.packet_dir.mkdir(parents=True, exist_ok=True)
        for number in sorted(set(args.packet_numbers)):
            packet = {"schema_version": 1, "status": "unreviewed-input",
                      "name_number": number, "source_snapshots": report["sources"],
                      "source_name": source["names"][number - 1],
                      "current_reader_name": reader_names[number],
                      "review_units": [u for u in report["review_units"] if u["name_number"] == number],
                      "open_issues": [i for i in report["issues"] if i["name_number"] == number]}
            (args.packet_dir / f"name-{number:04d}.json").write_text(
                json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report["counts"], indent=2))


if __name__ == "__main__":
    main()

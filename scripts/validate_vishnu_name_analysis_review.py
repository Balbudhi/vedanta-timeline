#!/usr/bin/env python3
"""Gate the four source-first review shards for all 1,000 name popups."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "gita/vishnu-sahasranama/analysis.json"
COMMENTARY = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
REVIEWS = tuple(sorted((ROOT / "internal/sanskrit_reviews").glob("name-analysis-review-*.json")))
CLAIM_RE = re.compile(
    r"(?i)(?:comes? from|derived from|the)\s+(?:sanskrit\s+)?root\b|"
    r"\broot\s+[A-Za-zĀ-ỹ√]"
)
DEBRIS_RE = re.compile(
    r"\bMn\.|\bNir\.?$|\bacc\.?\b|\bmf\(|\bI older than\b|"
    r"\bTattvas?\b|\(in\s+comp|\(cf\b|\bMaitrUp\.|^\)|\bpl\.\s|"
    r"\bopposed to\b|\bsaid of\b|[,;:]\s*$",
    re.I,
)
PROSE_GLOSS_RE = re.compile(
    r"^(?:One who|The One|This is made up|The author|The Abode)\b",
    re.I,
)
PLACEHOLDER_RE = re.compile(
    r"surface token preserved|surface form preserved|see parts for analysis|"
    r"exact .* pending|context-free",
    re.I,
)


def check_analysis(number: int, row: dict, errors: list[str]) -> None:
    for field in (
        "number", "citation_iast", "citation_devanagari", "whole_gloss", "parts",
        "stem", "affix", "morph", "sandhi", "grammar", "source_basis", "status",
        "evidence",
    ):
        if row.get(field) in (None, "", [], {}):
            errors.append(f"name {number}: analysis lacks {field}")
    if row.get("number") != number:
        errors.append(f"name {number}: replacement number differs")
    for part in row.get("parts", []):
        for field in ("form_iast", "gloss", "kind"):
            if part.get(field) in (None, ""):
                errors.append(f"name {number}: part lacks {field}")
        if DEBRIS_RE.search(str(part.get("gloss", ""))):
            errors.append(f"name {number}: lexical debris remains in {part.get('form_iast')}")
        if PROSE_GLOSS_RE.search(str(part.get("gloss", ""))) or len(str(part.get("gloss", ""))) > 140:
            errors.append(f"name {number}: prose remains in lexical part {part.get('form_iast')}")
    text = json.dumps(row, ensure_ascii=False)
    if PLACEHOLDER_RE.search(text):
        errors.append(f"name {number}: placeholder analysis remains")
    root = row.get("root")
    if root:
        for field in ("form", "gana", "pada", "gloss", "dhatupatha"):
            if root.get(field) in (None, "", {}):
                errors.append(f"name {number}: root lacks {field}")
        dhatu = root.get("dhatupatha", {})
        for field in ("locus", "aupadeshika_devanagari", "artha_sanskrit"):
            if dhatu.get(field) in (None, ""):
                errors.append(f"name {number}: Dhātupāṭha record lacks {field}")


def main() -> None:
    base = {
        row["number"]: row
        for row in json.loads(ANALYSIS.read_text(encoding="utf-8"))["names"]
    }
    commentary = {
        row["number"]: row
        for row in json.loads(COMMENTARY.read_text(encoding="utf-8"))["names"]
    }
    errors = []
    reviews = {}
    for path in REVIEWS:
        data = json.loads(path.read_text(encoding="utf-8"))
        status = data.get("review_status")
        complete = status in ("complete", "primary-grammar-reviewed-complete") or (
            isinstance(status, dict)
            and status.get("expected_count") == 250
            and status.get("observed_count") == 250
        )
        if not complete:
            errors.append(f"{path.name}: review_status is not complete")
        expected = data.get("expected_numbers", [])
        rows = data.get("rows", {})
        if {int(key) for key in rows} != set(expected):
            errors.append(f"{path.name}: row keys differ from expected_numbers")
        for key, record in rows.items():
            number = int(key)
            if number in reviews:
                errors.append(f"duplicate name {number}")
            reviews[number] = record
    if set(reviews) != set(range(1, 1001)):
        errors.append(
            f"review population differs: missing={sorted(set(range(1,1001))-set(reviews))}"
        )

    replacements = 0
    for number, record in reviews.items():
        status = record.get("status")
        if status == "replace":
            replacements += 1
            row = record.get("analysis")
            if not isinstance(row, dict):
                errors.append(f"name {number}: replacement lacks analysis")
                continue
        elif status == "verified-unchanged":
            row = base[number]
        else:
            errors.append(f"name {number}: invalid review status {status!r}")
            continue
        check_analysis(number, row, errors)
        has_root_claim = bool(CLAIM_RE.search(commentary[number].get("commentary", "")))
        # A metaphorical English use of “root” may legitimately have no Sanskrit
        # root. Every other explicit claim must result in an evidenced popup root.
        metaphorical = number in {429}
        if has_root_claim and not metaphorical and not row.get("root"):
            errors.append(f"name {number}: commentary root claim lacks popup root")

    if errors:
        raise ValueError("\n".join(errors[:300]))
    print(json.dumps({
        "reviewed": len(reviews),
        "replacements": replacements,
        "verified_unchanged": len(reviews) - replacements,
        "lexical_debris": 0,
        "unresolved_nonmetaphorical_root_claims": 0,
    }, indent=2))


if __name__ == "__main__":
    main()

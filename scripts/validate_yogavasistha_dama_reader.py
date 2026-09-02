#!/usr/bin/env python3
"""Validate all generated Dāma GitaReader artifacts against their inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import build_yogavasistha_dama_reader as builder


ASSIGNMENT_RE = re.compile(
    r"^/\*.*?\*/\s*window\.(YV_DAMA_VERSES|YV_DAMA_APPARATUS)\s*=\s*(.*);\s*$",
    re.DOTALL,
)
REVIEW_PATHS = tuple(
    builder.ROOT / f"internal/sanskrit_reviews/yogavasistha-dama/independent-review-{start}-{end}.json"
    for start, end in builder.EXPECTED_RANGES
)
SEMANTIC_REVIEW_PATH = (
    builder.ROOT
    / "internal/sanskrit_reviews/yogavasistha-dama/independent-review-semantic-fields.json"
)


def validate_independent_reviews(producers: tuple[Path, ...]) -> None:
    if len(producers) != len(REVIEW_PATHS):
        raise builder.BuildError("independent-review gate requires all four producer ranges")
    for producer, review_path in zip(producers, REVIEW_PATHS, strict=True):
        review = json.loads(review_path.read_text(encoding="utf-8"))
        producer_hash = hashlib.sha256(producer.read_bytes()).hexdigest()
        recorded_hash = review.get("producer_sha256")
        if not recorded_hash:
            recorded_hash = next(
                (value for key, value in review.get("input_hashes", {}).items() if key.startswith("producer_")),
                None,
            )
        if recorded_hash != producer_hash:
            raise builder.BuildError(f"stale independent review for {producer.name}")
        passed = (
            review.get("verdict") == "pass"
            or review.get("status") == "pass"
            or review.get("result", {}).get("pass") is True
        )
        release = review.get("release_gate")
        if isinstance(release, dict):
            passed = passed and release.get("pass") is True
        if not passed or review.get("errors", []):
            raise builder.BuildError(f"independent review is not zero-error for {producer.name}")

    semantic_review = json.loads(SEMANTIC_REVIEW_PATH.read_text(encoding="utf-8"))
    semantic_hash = hashlib.sha256(builder.SEMANTIC_FIELDS_PATH.read_bytes()).hexdigest()
    if semantic_review.get("producer_sha256") != semantic_hash:
        raise builder.BuildError("stale independent review for semantic-fields.json")
    population = semantic_review.get("closed_population") or semantic_review.get("population", {})
    expected_fields = population.get("expected_fields", population.get("expected_entries"))
    reviewed_fields = population.get("reviewed_fields", population.get("reviewed_entries"))
    if expected_fields != len(builder.EXPECTED_SEMANTIC_KEYS):
        raise builder.BuildError("semantic-field review has the wrong expected population")
    if reviewed_fields != len(builder.EXPECTED_SEMANTIC_KEYS):
        raise builder.BuildError("semantic-field review is incomplete")
    semantic_passed = (
        semantic_review.get("result", {}).get("pass") is True
        or semantic_review.get("release_gate", {}).get("pass") is True
    )
    if not semantic_passed or semantic_review.get("errors", []):
        raise builder.BuildError("independent semantic-field review is not zero-error")


def parse_assignment(path: Path, expected_global: str) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise builder.BuildError(f"generated artifact is missing: {path}") from exc
    match = ASSIGNMENT_RE.fullmatch(text)
    if not match or match.group(1) != expected_global:
        raise builder.BuildError(f"{path} must assign exactly window.{expected_global}")
    try:
        return json.loads(match.group(2))
    except json.JSONDecodeError as exc:
        raise builder.BuildError(
            f"invalid JSON payload in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def validate_artifacts(output_dir: Path, expected: dict[str, Any]) -> None:
    artifacts = builder.generated_artifacts(expected)
    for name, rendered in artifacts.items():
        path = output_dir / name
        try:
            observed = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise builder.BuildError(f"generated artifact is missing: {path}") from exc
        if observed != rendered:
            raise builder.BuildError(f"generated artifact is stale or hand-edited: {path}")

    verses = parse_assignment(output_dir / "verses.js", "YV_DAMA_VERSES")
    if verses != expected["units"]:
        raise builder.BuildError("verses.js does not exactly replay the normalized unit population")
    require_semantic_coverage = expected.get("source", {}).get("packet") == str(
        builder.SOURCE_PATH.relative_to(builder.ROOT)
    )
    builder.validate_public_payload(
        {**expected, "units": verses},
        require_semantic_coverage=require_semantic_coverage,
    )

    apparatus = parse_assignment(output_dir / "apparatus.js", "YV_DAMA_APPARATUS")
    expected_apparatus = {
        "schema_version": "yogavasistha-dama-apparatus-v1",
        "textual_notes": expected["textual_notes"],
        "apparatus": expected["apparatus"],
        "semantic_fields": expected["semantic_fields"],
    }
    if apparatus != expected_apparatus:
        raise builder.BuildError("apparatus.js does not exactly replay the source-note populations")

    try:
        review = json.loads((output_dir / "review.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise builder.BuildError(f"review.json is invalid JSON: {exc}") from exc
    if review != expected:
        raise builder.BuildError("review.json does not exactly replay the merged review payload")

    index = (output_dir / "index.html").read_text(encoding="utf-8")
    if '<script>location.replace("../../#/article/yogavasistha-dama");</script>' not in index:
        raise builder.BuildError("index.html lacks the canonical in-app article redirect")
    forbidden = ("GitaReader", "word-card", "<style", "YV_DAMA_VERSES", "apparatus.js")
    present = [marker for marker in forbidden if marker in index]
    if present:
        raise builder.BuildError(f"index.html contains a bespoke reader path: {present}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=builder.SOURCE_PATH)
    parser.add_argument("--producer", type=Path, action="append", dest="producers")
    parser.add_argument("--output-dir", type=Path, default=builder.ROOT / "gita/yogavasistha-dama")
    args = parser.parse_args()
    producers = tuple(args.producers) if args.producers else builder.PRODUCER_PATHS
    try:
        validate_independent_reviews(producers)
        expected = builder.build_payload(args.source, producers)
        validate_artifacts(args.output_dir, expected)
        words = sum(len(unit["words"]) for unit in expected["units"])
        print(
            f"PASS: {len(expected['units'])} exact source units; {words} reviewed words; "
            f"{len(expected['semantic_fields']['fields'])} reviewed semantic fields; "
            "2.33 textual note preserved; apparatus attached after 46 and 64; "
            "embedded and registry evidence resolved"
        )
        return 0
    except (builder.BuildError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

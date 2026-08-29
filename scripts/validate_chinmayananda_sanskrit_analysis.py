#!/usr/bin/env python3
"""Validate the reviewed non-Gītā Sanskrit commentary shards."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
SHARDS = (
    ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-001-250.json",
    ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-251-500.json",
    ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-501-750.json",
    ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-751-1000.json",
)
AUDIT = ROOT / "scripts/audit_chinmayananda_sanskrit_coverage.py"
MANIFEST = ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis.manifest.json"
SLOT_RE = re.compile(r"\{([\d,\s]+):([^}]*)\}")
NON_MORPHEME_FORM_RE = re.compile(
    r"(?i)\b(?:finite|present|perfect|past|future)\s+(?:verbal|form|ending|plural|singular)\b|"
    r"\b(?:enclitic\s+oblique|verbal\s+ending)\b"
)


def expected_ids() -> set[str]:
    output = subprocess.check_output([sys.executable, str(AUDIT)], cwd=ROOT)
    audit = json.loads(output)
    return {
        row["id"]
        for row in audit["spans"]
        if row["status"] == "standalone-non-gita-candidate"
    }


def plain(slotted: str) -> str:
    return SLOT_RE.sub(lambda match: match.group(2), slotted)


def iast_key(value: str) -> str:
    # indic-transliteration currently emits ``~`` for anusvāra before some
    # sibilants; normalize that library spelling to the site's IAST ``ṃ``.
    value = unicodedata.normalize("NFC", value).lower().replace("~", "ṃ")
    return re.sub(r"[^a-zāīūṛṝḷṅñṭḍṇśṣṃḥ]", "", value)


def deva_key(value: str) -> str:
    return re.sub(r"[^\u0900-\u097f]", "", unicodedata.normalize("NFC", value))


def is_verbal_form(morph: str) -> bool:
    value = morph.lower()
    return any(marker in value for marker in (
        "indicative", "imperative", "optative", "participle", "absolutive",
        "gerundive", "finite verb", "verbal form",
    ))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    expected = expected_ids()
    quotes: dict[str, dict] = {}
    withheld: dict[str, object] = {}
    errors = []
    statuses = {}
    shard_counts = {}

    for path in SHARDS:
        if not path.exists():
            if args.require_complete:
                errors.append(f"missing shard {path.relative_to(ROOT)}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        statuses[path.name] = data.get("review_status")
        shard_counts[path.name] = len(data.get("quotes", {}))
        for key, row in data.get("quotes", {}).items():
            if key in quotes or key in withheld:
                errors.append(f"duplicate row {key}")
            quotes[key] = row
        for key, reason in data.get("withheld", {}).items():
            if key in quotes or key in withheld:
                errors.append(f"duplicate row {key}")
            withheld[key] = reason

    observed = set(quotes) | set(withheld)
    if observed - expected:
        errors.append(f"unexpected IDs: {sorted(observed - expected)}")
    if args.require_complete and observed != expected:
        errors.append(f"unaccounted IDs: {sorted(expected - observed)}")
    if args.require_complete and withheld:
        errors.append(f"withheld rows remain: {sorted(withheld)}")
    if args.require_complete and any(value != "primary-grammar-reviewed-complete" for value in statuses.values()):
        errors.append(f"incomplete shard statuses: {statuses}")
    if args.require_complete:
        if not MANIFEST.exists():
            errors.append("missing commentary Sanskrit analysis manifest")
        else:
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
            population = manifest.get("population", {})
            if population != {"expected": len(expected), "reviewed": len(quotes), "withheld": len(withheld)}:
                errors.append(f"manifest population is stale: {population}")
            listed = {row.get("path"): row for row in manifest.get("shards", [])}
            for path in SHARDS:
                row = listed.get(path.name)
                if not row:
                    errors.append(f"manifest omits {path.name}")
                    continue
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if row.get("sha256") != digest:
                    errors.append(f"manifest hash is stale for {path.name}")
                if row.get("quotes") != shard_counts.get(path.name):
                    errors.append(f"manifest quote count is stale for {path.name}")

    required_row = (
        "quote_id", "name_number", "printed_devanagari", "canonical_devanagari",
        "source_iast", "iast", "source_segments", "source_alignment_score",
        "source_label", "canonical_locus", "textual_notes", "english",
        "english_source", "english_slots", "words",
    )
    required_word = (
        "i", "deva", "iast", "gloss", "parts", "stem", "affix", "morph", "evidence",
    )
    for quote_id, row in quotes.items():
        if row.get("quote_id") != quote_id:
            errors.append(f"{quote_id}: quote_id mismatch")
        for field in required_row:
            if row.get(field) in (None, "", []):
                errors.append(f"{quote_id}: missing {field}")
        if row.get("english_source") not in ("Swami Chinmayananda", "site-literal-translation"):
            errors.append(f"{quote_id}: invalid english_source")
        words = row.get("words", [])
        if [word.get("i") for word in words] != list(range(len(words))):
            errors.append(f"{quote_id}: non-contiguous word indices")
        canonical_deva = row.get("canonical_devanagari", "")
        source_iast = row.get("source_iast", "")
        canonical_iast = row.get("iast", "")
        transliterated = transliterate(canonical_deva, sanscript.DEVANAGARI, sanscript.IAST)
        if iast_key(transliterated) != iast_key(source_iast):
            errors.append(f"{quote_id}: Devanāgarī/IAST replay differs")
        if iast_key(" ".join(str(word.get("iast", "")) for word in words)) != iast_key(canonical_iast):
            errors.append(f"{quote_id}: word IAST replay differs")
        source_segments = row.get("source_segments", [])
        if "".join(str(segment.get("text", "")) for segment in source_segments) != canonical_deva:
            errors.append(f"{quote_id}: source segments do not replay Devanāgarī")
        source_indices = {
            int(index)
            for segment in source_segments
            for index in segment.get("word_indices", [])
        }
        if source_indices != set(range(len(words))):
            errors.append(f"{quote_id}: source segment word coverage differs")
        if float(row.get("source_alignment_score", 0)) < 0.70:
            errors.append(f"{quote_id}: weak source segment alignment")
        for word in words:
            for field in required_word:
                if word.get(field) in (None, "", []):
                    errors.append(f"{quote_id} word {word.get('i')}: missing {field}")
            for part in word.get("parts", []):
                if NON_MORPHEME_FORM_RE.search(str(part.get("form", ""))):
                    errors.append(f"{quote_id} word {word.get('i')}: English grammar description appears in morpheme form")
            if "root" not in word:
                errors.append(f"{quote_id} word {word.get('i')}: missing root key")
            if is_verbal_form(str(word.get("morph", ""))):
                root = word.get("root")
                roots = word.get("roots")
                root_records = [root] if isinstance(root, dict) else roots if isinstance(roots, list) else []
                if not root_records:
                    errors.append(f"{quote_id} word {word.get('i')}: verbal form lacks structured root")
                for root in root_records:
                    for field in ("form", "gana", "pada", "gloss", "dhatupatha"):
                        if root.get(field) in (None, "", {}):
                            errors.append(f"{quote_id} word {word.get('i')}: root lacks {field}")
                    dhatu = root.get("dhatupatha", {})
                    for field in ("locus", "aupadeshika_devanagari", "artha_sanskrit"):
                        if dhatu.get(field) in (None, ""):
                            errors.append(f"{quote_id} word {word.get('i')}: Dhātupāṭha root lacks {field}")
            placeholder = " ".join((str(word.get("morph", "")), str(word.get("affix", "")))).lower()
            if "surface token preserved" in placeholder or "surface form preserved" in placeholder:
                errors.append(f"{quote_id} word {word.get('i')}: placeholder grammar is not review")
        slots = row.get("english_slots", "")
        if plain(slots) != row.get("english"):
            errors.append(f"{quote_id}: English slot replay differs")
        indices = [
            int(value.strip())
            for match in SLOT_RE.finditer(slots)
            for value in match.group(1).split(",")
            if value.strip()
        ]
        if set(indices) != set(range(len(words))):
            errors.append(f"{quote_id}: Sanskrit slot coverage differs")
        residue = SLOT_RE.sub("", slots)
        if re.search(r"[A-Za-z]", residue):
            errors.append(f"{quote_id}: visible English remains unslotted")

    if errors:
        raise ValueError("\n".join(errors[:200]))
    print(json.dumps({
        "expected": len(expected),
        "reviewed": len(quotes),
        "withheld": len(withheld),
        "unaccounted": len(expected - observed),
        "statuses": statuses,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

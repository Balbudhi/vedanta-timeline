#!/usr/bin/env python3
"""Build the closed-population Dāma reader from reviewed producer packets.

This builder is deliberately fail-closed.  It never repairs producer JSON,
fills a missing verse, transliterates a witness, or guesses an evidence
reference.  The public payload is embedded in the standalone HTML so the
reader has one generated artifact and one validation boundary.
"""

from __future__ import annotations

import argparse
import copy
import functools
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "data/sources/sanskrit/vedanta/laghuyogavasistha_dama_story.json"
SEMANTIC_FIELDS_PATH = (
    ROOT / "internal/sanskrit_reviews/yogavasistha-dama/semantic-fields.json"
)
PRODUCER_PATHS = tuple(
    ROOT / f"internal/sanskrit_reviews/yogavasistha-dama/producer-{start}-{end}.json"
    for start, end in ((31, 44), (45, 58), (59, 72), (73, 86))
)
SCHEMA = "yogavasistha-dama-reader-v1"
PRODUCER_SCHEMA = "yogavasistha-dama-producer-v1"
FIRST_VERSE = 31
LAST_VERSE = 86
EXPECTED_IDS = tuple(f"lyv-4-2-{verse}" for verse in range(FIRST_VERSE, LAST_VERSE + 1))
EXPECTED_RANGES = ((31, 44), (45, 58), (59, 72), (73, 86))
EXPECTED_SEMANTIC_KEYS = (
    "purusha",
    "shambara",
    "daitya",
    "danava",
    "amara",
    "deva",
    "sura",
    "tridasha",
    "asura",
    "dama",
    "vyala",
    "kata",
)
SLOT_RE = re.compile(r"\{([0-9]+(?:\s*,\s*[0-9]+)*):([^{}]+)\}")
SOURCE_TOKEN_RE = re.compile(r"[^\s|।॥]+")
DEVANAGARI_CHUNK_RE = re.compile(r"[^\s|।॥]+|\s+|[|।॥]+")


class BuildError(ValueError):
    """Raised when an input violates the closed reader contract."""


def _fail(message: str) -> None:
    raise BuildError(message)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _fail(f"missing required input: {path}")
    except json.JSONDecodeError as exc:
        _fail(f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}")
    if not isinstance(value, dict):
        _fail(f"top-level JSON value must be an object: {path}")
    return value


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(f"{label} must be a non-empty string")
    return value


def _require_keys(value: Mapping[str, Any], keys: Iterable[str], label: str) -> None:
    missing = [key for key in keys if key not in value]
    if missing:
        _fail(f"{label} is missing required keys: {', '.join(missing)}")


def _exact_ids(items: Sequence[Mapping[str, Any]], expected: Sequence[str], label: str) -> None:
    ids = [item.get("id") for item in items]
    duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
    if duplicates:
        _fail(f"{label} has duplicate IDs: {', '.join(map(str, duplicates))}")
    missing = [item_id for item_id in expected if item_id not in ids]
    unexpected = [str(item_id) for item_id in ids if item_id not in expected]
    if missing or unexpected:
        details = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if unexpected:
            details.append(f"unexpected {', '.join(unexpected)}")
        _fail(f"{label} ID population mismatch: {'; '.join(details)}")


def _registry(packet: Mapping[str, Any], *names: str) -> dict[str, Any]:
    found = [packet[name] for name in names if name in packet]
    if len(found) > 1 and any(value != found[0] for value in found[1:]):
        _fail(f"conflicting producer registries: {', '.join(names)}")
    value = found[0] if found else {}
    if not isinstance(value, dict):
        _fail(f"producer registry {names[0]} must be an object")
    for key, record in value.items():
        _nonempty_string(key, f"{names[0]} registry key")
        if not isinstance(record, dict):
            _fail(f"{names[0]} registry entry {key!r} must be an object")
    return value


def _explicit_refs(word: Mapping[str, Any], names: Sequence[str]) -> list[str]:
    refs: list[str] = []
    for name in names:
        if name not in word:
            continue
        value = word[name]
        values = value if isinstance(value, list) else [value]
        for ref in values:
            if ref is None:
                continue
            refs.append(_nonempty_string(ref, f"word {word.get('i')} {name}"))
    return refs


def _normalize_root_record(record: Mapping[str, Any], label: str) -> dict[str, Any]:
    root = copy.deepcopy(dict(record))
    dhatu = root.get("dhatupatha")
    if not isinstance(dhatu, dict):
        # Legacy producer packets keep the Dhātupāṭha fields beside the root.
        dhatu = {
            "locus": root.get("locus"),
            "aupadeshika_devanagari": root.get("aupadeshika_devanagari", root.get("aupadeshika")),
            "artha_sanskrit": root.get("artha_sanskrit", root.get("artha")),
        }
    else:
        dhatu = copy.deepcopy(dhatu)
        if "aupadeshika_devanagari" not in dhatu and "aupadeshika" in dhatu:
            dhatu["aupadeshika_devanagari"] = dhatu["aupadeshika"]
        if "artha_sanskrit" not in dhatu and "artha" in dhatu:
            dhatu["artha_sanskrit"] = dhatu["artha"]
    if "dhatu_devanagari" in root and "dhatu_devanagari" not in dhatu:
        dhatu["dhatu_devanagari"] = root["dhatu_devanagari"]
    root["dhatupatha"] = dhatu
    _require_keys(root, ("form", "gana", "pada", "gloss", "dhatupatha"), label)
    for key in ("form", "gana", "pada", "gloss"):
        _nonempty_string(root[key], f"{label}.{key}")
    _require_keys(dhatu, ("locus", "aupadeshika_devanagari", "artha_sanskrit"), f"{label}.dhatupatha")
    for key in ("locus", "aupadeshika_devanagari", "artha_sanskrit"):
        _nonempty_string(dhatu[key], f"{label}.dhatupatha.{key}")
    return root


def _resolve_root(
    word: Mapping[str, Any], root_registry: Mapping[str, Any], label: str
) -> dict[str, Any] | None:
    ref_names = (
        "rootEvidenceRef",
        "root_evidence_ref",
        "rootEvidenceRefs",
        "root_evidence_refs",
        "rootRef",
        "root_ref",
    )
    refs = _explicit_refs(word, ref_names)
    root_value = word.get("root")
    if isinstance(root_value, dict):
        embedded_ref = root_value.get("$ref", root_value.get("ref", root_value.get("root_evidence_ref")))
        if embedded_ref is not None:
            refs.append(_nonempty_string(embedded_ref, f"{label}.root ref"))
            if len(root_value) > 1:
                _fail(f"{label}.root may not mix a registry reference with embedded fields")
            root_value = None
    elif isinstance(root_value, str) and root_value in root_registry:
        refs.append(root_value)
        root_value = None
    if len(set(refs)) > 1:
        _fail(f"{label} refers to multiple root-evidence records: {', '.join(refs)}")
    if refs:
        ref = refs[0]
        if ref not in root_registry:
            _fail(f"{label} has dangling root-evidence reference {ref!r}")
        if root_value not in (None, "") or word.get("rootEvidence") is not None:
            _fail(f"{label} mixes registry root evidence with embedded root evidence")
        return _normalize_root_record(root_registry[ref], f"{label}.root[{ref}]")
    if root_value is None:
        if word.get("rootEvidence") not in (None, {}):
            _fail(f"{label} supplies rootEvidence while root is null")
        return None
    if isinstance(root_value, dict):
        record = dict(root_value)
    elif isinstance(root_value, str):
        evidence = word.get("rootEvidence")
        if not isinstance(evidence, dict):
            _fail(f"{label} root {root_value!r} lacks embedded or referenced evidence")
        record = {
            "form": root_value,
            "gana": evidence.get("gana"),
            "pada": evidence.get("pada"),
            "gloss": word.get("rootGloss"),
            "dhatupatha": {
                "locus": evidence.get("locus"),
                "aupadeshika_devanagari": evidence.get(
                    "aupadeshika_devanagari", evidence.get("aupadeshika")
                ),
                "artha_sanskrit": evidence.get("artha_sanskrit", evidence.get("artha")),
            },
        }
    else:
        _fail(f"{label}.root must be null, a root object, or an evidence reference")
    return _normalize_root_record(record, f"{label}.root")


def _resolve_grammar_refs(
    word: Mapping[str, Any], grammar_registry: Mapping[str, Any], label: str
) -> dict[str, Any]:
    refs = _explicit_refs(
        word,
        (
            "grammarEvidenceRef",
            "grammar_evidence_ref",
            "grammarEvidenceRefs",
            "grammar_evidence_refs",
            "grammarRef",
            "grammar_ref",
            "grammarRefs",
            "grammar_refs",
            "ruleRefs",
            "rule_refs",
        ),
    )
    resolved: dict[str, Any] = {}
    for ref in refs:
        if ref not in grammar_registry:
            _fail(f"{label} has dangling grammar-evidence reference {ref!r}")
        resolved[ref] = copy.deepcopy(grammar_registry[ref])
    return resolved


def _validate_slots(english: str, word_ids: Sequence[int], label: str) -> None:
    matches = list(SLOT_RE.finditer(english))
    if not matches:
        _fail(f"{label}.english has no slotted text")
    residue = SLOT_RE.sub("", english)
    if "{" in residue or "}" in residue:
        _fail(f"{label}.english contains malformed slot syntax")
    referenced: list[int] = []
    allowed = set(word_ids)
    for match in matches:
        indices = [int(value.strip()) for value in match.group(1).split(",")]
        if len(indices) != len(set(indices)):
            _fail(f"{label}.english repeats an index inside one slot")
        unknown = set(indices) - allowed
        if unknown:
            _fail(f"{label}.english references unknown word indices: {sorted(unknown)}")
        referenced.extend(indices)
    observed = set(referenced)
    if observed != allowed:
        _fail(f"{label}.english slot coverage mismatch: expected {sorted(allowed)}, observed {sorted(observed)}")
    duplicates = sorted(index for index in allowed if referenced.count(index) != 1)
    if duplicates:
        _fail(f"{label}.english must reference each word exactly once; bad indices: {duplicates}")


def _latin_key(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.lower())
    return "".join(
        char for char in decomposed if unicodedata.category(char)[0] in {"L", "N"}
    )


def _edit_distance(left: str, right: str) -> int:
    previous = list(range(len(right) + 1))
    for row, left_char in enumerate(left, 1):
        current = [row]
        for column, right_char in enumerate(right, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1] + (left_char != right_char),
                )
            )
        previous = current
    return previous[-1]


def _source_word_groups(
    source_iast: str, words: Sequence[Mapping[str, Any]], label: str
) -> list[list[int]]:
    """Map each exact saṃhitā token to consecutive reviewed pada indices.

    This is a deterministic UI alignment, not a Sanskrit parser. The producer
    review remains the authority for sandhi resolution; the alignment gate
    rejects missing, reordered, or implausibly distant pada populations.
    """

    source_tokens = SOURCE_TOKEN_RE.findall(source_iast)
    token_keys = [_latin_key(token) for token in source_tokens]
    word_keys = [_latin_key(_nonempty_string(word.get("iast"), f"{label}.word.iast")) for word in words]
    if not source_tokens or not words:
        _fail(f"{label} requires source tokens and reviewed words")

    @functools.lru_cache(maxsize=None)
    def align(token_index: int, word_index: int) -> tuple[int, tuple[int, ...], int]:
        if token_index == len(token_keys):
            return (0, (), 1) if word_index == len(word_keys) else (10**9, (), 0)
        remaining_tokens = len(token_keys) - token_index - 1
        maximum_group = min(7, len(word_keys) - word_index - remaining_tokens)
        best_cost = 10**9
        best_path: tuple[int, ...] = ()
        best_count = 0
        for group_size in range(1, maximum_group + 1):
            rest_cost, rest_path, rest_count = align(
                token_index + 1, word_index + group_size
            )
            if not rest_count:
                continue
            candidate_cost = _edit_distance(
                token_keys[token_index],
                "".join(word_keys[word_index : word_index + group_size]),
            ) + rest_cost
            if candidate_cost < best_cost:
                best_cost = candidate_cost
                best_path = (group_size, *rest_path)
                best_count = rest_count
            elif candidate_cost == best_cost:
                best_count = min(2, best_count + rest_count)
        return best_cost, best_path, best_count

    total_cost, path, path_count = align(0, 0)
    if path_count != 1 or len(path) != len(source_tokens):
        _fail(f"{label} has no unique source-token/pada alignment")
    if total_cost > 12:
        _fail(f"{label} source-token/pada alignment is too distant (cost {total_cost})")

    groups: list[list[int]] = []
    word_index = 0
    for token, token_key, group_size in zip(source_tokens, token_keys, path, strict=True):
        indices = list(range(word_index, word_index + group_size))
        candidate = "".join(word_keys[index] for index in indices)
        distance = _edit_distance(token_key, candidate)
        ratio = distance / max(1, len(token_key))
        if distance >= 3 and ratio > 0.45:
            _fail(
                f"{label} source token {token!r} does not plausibly replay "
                f"padas {indices} (distance {distance})"
            )
        groups.append(indices)
        word_index += group_size
    if word_index != len(words):
        _fail(f"{label} source-token alignment does not cover every reviewed word")
    return groups


def _source_segments(
    devanagari: str,
    source_iast: str,
    words: Sequence[Mapping[str, Any]],
    label: str,
) -> list[dict[str, Any]]:
    groups = _source_word_groups(source_iast, words, label)
    devanagari_tokens = SOURCE_TOKEN_RE.findall(devanagari)
    if len(devanagari_tokens) != len(groups):
        _fail(
            f"{label} paired Devanāgarī/IAST token counts differ: "
            f"{len(devanagari_tokens)} != {len(groups)}"
        )
    segments: list[dict[str, Any]] = []
    group_index = 0
    for chunk in DEVANAGARI_CHUNK_RE.findall(devanagari):
        if SOURCE_TOKEN_RE.fullmatch(chunk):
            segments.append({"text": chunk, "word_indices": groups[group_index]})
            group_index += 1
        else:
            segments.append({"text": chunk, "word_indices": []})
    if group_index != len(groups):
        _fail(f"{label} did not consume every source-token alignment group")
    if "".join(segment["text"] for segment in segments) != devanagari:
        _fail(f"{label} source segments do not reconstruct exact Devanāgarī")
    return segments


def _apparatus_alignment_iast(entry: Mapping[str, Any]) -> str | None:
    alignment = entry.get("alignment_iast")
    if isinstance(alignment, str) and alignment.strip():
        return alignment
    source_iast = entry.get("source_iast")
    if not isinstance(source_iast, str) or not source_iast.strip():
        return None
    source_iast = re.sub(r"\s*//\s*[A-Z][^\n]*$", " ||", source_iast)
    return source_iast.replace("/", "|")


def _validate_semantic_fields(path: Path = SEMANTIC_FIELDS_PATH) -> dict[str, Any]:
    bundle = _load_json(path)
    if bundle.get("schema_version") != "yogavasistha-dama-semantic-fields-v1":
        _fail(f"{path} has an unsupported semantic-field schema")
    methodology = bundle.get("methodology")
    if not isinstance(methodology, dict):
        _fail(f"{path}.methodology must be an object")
    _require_keys(methodology, ("title", "summary", "principles"), f"{path}.methodology")
    principles = methodology["principles"]
    if not isinstance(principles, list) or len(principles) < 4:
        _fail(f"{path}.methodology.principles must contain the complete method")
    principle_ids = []
    for index, principle in enumerate(principles):
        if not isinstance(principle, dict):
            _fail(f"{path}.methodology.principles[{index}] must be an object")
        _require_keys(principle, ("id", "title", "text"), f"methodology principle {index}")
        principle_ids.append(principle["id"])
    if len(principle_ids) != len(set(principle_ids)):
        _fail(f"{path}.methodology has duplicate principle IDs")

    history = bundle.get("witness_history")
    expected_history = ("laghu", "mokshopaya-critical", "yogavasistha-vulgate", "venkatesananda")
    if not isinstance(history, list) or tuple(item.get("id") for item in history) != expected_history:
        _fail(f"{path}.witness_history must contain {expected_history} in order")
    for item in history:
        _require_keys(item, ("id", "label", "relation", "description", "source_label"), f"witness {item.get('id')}")

    fields = bundle.get("fields")
    if not isinstance(fields, list) or tuple(field.get("key") for field in fields) != EXPECTED_SEMANTIC_KEYS:
        _fail(f"{path}.fields must contain the frozen semantic-field population")
    for field in fields:
        label = f"semantic field {field.get('key')}"
        _require_keys(
            field,
            ("key", "lemma_iast", "lemma_devanagari", "match_forms", "opening", "chronology_note", "readings"),
            label,
        )
        if not isinstance(field["match_forms"], list) or not field["match_forms"]:
            _fail(f"{label}.match_forms must be a non-empty list")
        if not isinstance(field["readings"], list) or len(field["readings"]) < 2:
            _fail(f"{label}.readings must preserve multiple layers")
        for index, reading in enumerate(field["readings"]):
            if not isinstance(reading, dict):
                _fail(f"{label}.readings[{index}] must be an object")
            _require_keys(reading, ("category", "meaning"), f"{label}.readings[{index}]")
            if reading.get("source_path") and not Path(reading["source_path"]).is_file():
                _fail(f"{label}.readings[{index}] source_path is missing")
    return bundle


def _semantic_candidates(word: Mapping[str, Any]) -> set[str]:
    values = [word.get("iast"), word.get("stem")]
    values.extend(part.get("form") for part in word.get("parts", []) if isinstance(part, dict))
    compound = word.get("compound")
    if isinstance(compound, dict):
        values.extend(compound.get("members", []))
    candidates: set[str] = set()
    for value in values:
        if not isinstance(value, str) or not value.strip():
            continue
        candidates.add(_latin_key(value))
        for piece in re.split(r"[-+ /→]+", value):
            if piece:
                candidates.add(_latin_key(piece))
    return candidates


def _semantic_keys(
    word: Mapping[str, Any], fields: Sequence[Mapping[str, Any]]
) -> list[str]:
    candidates = _semantic_candidates(word)
    return [
        field["key"]
        for field in fields
        if any(_latin_key(form) in candidates for form in field["match_forms"])
    ]


def _normalize_word(
    raw: Mapping[str, Any],
    expected_index: int,
    producer_evidence: Mapping[str, Any],
    root_registry: Mapping[str, Any],
    grammar_registry: Mapping[str, Any],
    unit_id: str,
) -> dict[str, Any]:
    label = f"{unit_id}.words[{expected_index}]"
    _require_keys(
        raw,
        ("i", "deva", "iast", "gloss", "parts", "stem", "affix", "morph", "karaka"),
        label,
    )
    if raw["i"] != expected_index:
        _fail(f"{label}.i must be {expected_index}, observed {raw['i']!r}")
    for key in ("deva", "iast", "gloss", "stem", "affix", "morph", "karaka"):
        _nonempty_string(raw[key], f"{label}.{key}")
    parts = raw["parts"]
    if not isinstance(parts, list) or not parts:
        _fail(f"{label}.parts must be a non-empty list")
    for part_index, part in enumerate(parts):
        if not isinstance(part, dict):
            _fail(f"{label}.parts[{part_index}] must be an object")
        _nonempty_string(part.get("form"), f"{label}.parts[{part_index}].form")
        _nonempty_string(part.get("gloss"), f"{label}.parts[{part_index}].gloss")

    normalized = copy.deepcopy(dict(raw))
    normalized["root"] = _resolve_root(raw, root_registry, label)
    if normalized["root"] is None and any(
        isinstance(part, dict) and str(part.get("form", "")).lstrip().startswith("√") for part in parts
    ):
        _fail(f"{label} contains an explicit verbal root part but publishes root=null")

    grammar_records = _resolve_grammar_refs(raw, grammar_registry, label)
    evidence = raw.get("evidence")
    if evidence is None:
        evidence = {
            "text_witness": producer_evidence.get(
                "text_witness", producer_evidence.get("controlling_text", producer_evidence.get("text_layer"))
            ),
            "grammar_witnesses": producer_evidence.get(
                "grammar_witnesses",
                [
                    *producer_evidence.get("grammar_primary", []),
                    *producer_evidence.get("grammar_raw", []),
                ],
            ),
            "review_method": producer_evidence.get("review_method", producer_evidence.get("method")),
        }
    elif not isinstance(evidence, dict):
        _fail(f"{label}.evidence must be an object")
    else:
        evidence = copy.deepcopy(evidence)
    evidence = {key: value for key, value in evidence.items() if value not in (None, "", [])}
    if grammar_records:
        evidence["grammar_records"] = grammar_records
    if not evidence:
        _fail(f"{label} has no source/grammar evidence")
    normalized["evidence"] = evidence

    derivation_sets = []
    for key in ("parallelDerivations", "derivations", "alternatives"):
        value = raw.get(key, [])
        if not isinstance(value, list):
            _fail(f"{label}.{key} must be a list")
        derivation_sets.extend(copy.deepcopy(value))
    resolved_derivations = []
    for derivation_index, derivation in enumerate(derivation_sets):
        if not isinstance(derivation, dict):
            _fail(f"{label}.parallelDerivations[{derivation_index}] must be an object")
        item = copy.deepcopy(derivation)
        refs = []
        for ref_key in ("root_ref", "root_refs", "rootRef", "rootRefs"):
            if ref_key not in item:
                continue
            values = item[ref_key] if isinstance(item[ref_key], list) else [item[ref_key]]
            refs.extend(_nonempty_string(value, f"{label}.parallelDerivations[{derivation_index}].{ref_key}") for value in values)
        roots = []
        for ref in refs:
            if ref not in root_registry:
                _fail(f"{label}.parallelDerivations[{derivation_index}] has dangling root reference {ref!r}")
            roots.append(_normalize_root_record(root_registry[ref], f"{label}.parallelDerivations[{derivation_index}].root[{ref}]"))
        embedded_roots = item.get("roots", [])
        if embedded_roots:
            if not isinstance(embedded_roots, list):
                _fail(f"{label}.parallelDerivations[{derivation_index}].roots must be a list")
            roots.extend(
                _normalize_root_record(root, f"{label}.parallelDerivations[{derivation_index}].roots[{index}]")
                for index, root in enumerate(embedded_roots)
            )
        item["roots"] = roots
        resolved_derivations.append(item)
    normalized["parallelDerivations"] = resolved_derivations
    return normalized


def _validate_source(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    _require_keys(
        source,
        (
            "schema_version",
            "population",
            "work",
            "section",
            "controlling_witness",
            "parallel_witnesses",
            "units",
            "textual_notes",
            "apparatus",
        ),
        "source packet",
    )
    population = source["population"]
    if not isinstance(population, dict):
        _fail("source packet population must be an object")
    expected_population = {
        "first_id": EXPECTED_IDS[0],
        "last_id": EXPECTED_IDS[-1],
        "expected_units": len(EXPECTED_IDS),
        "observed_units": len(EXPECTED_IDS),
    }
    for key, expected in expected_population.items():
        if population.get(key) != expected:
            _fail(f"source population.{key} must be {expected!r}, observed {population.get(key)!r}")
    units = source["units"]
    if not isinstance(units, list) or not all(isinstance(unit, dict) for unit in units):
        _fail("source packet units must be a list of objects")
    _exact_ids(units, EXPECTED_IDS, "source packet units")
    by_id = {unit["id"]: unit for unit in units}
    ordered = [copy.deepcopy(by_id[item_id]) for item_id in EXPECTED_IDS]
    for verse, unit in zip(range(FIRST_VERSE, LAST_VERSE + 1), ordered):
        if unit.get("verse") != verse:
            _fail(f"source {unit['id']}.verse must be {verse}")
        _nonempty_string(unit.get("deva"), f"source {unit['id']}.deva")
        _nonempty_string(unit.get("iast"), f"source {unit['id']}.iast")
    return ordered


def _validate_attached_evidence(source: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    notes = source["textual_notes"]
    if not isinstance(notes, list) or len(notes) != 1 or not isinstance(notes[0], dict):
        _fail("source packet must contain exactly the witnessed textual note for 2.33")
    if notes[0].get("unit_id") != "lyv-4-2-33":
        _fail("the textual note must attach to lyv-4-2-33")
    _require_keys(notes[0], ("printed_and_transcribed", "parallel_reading", "policy"), "2.33 textual note")

    apparatus = source["apparatus"]
    if not isinstance(apparatus, list) or not all(isinstance(item, dict) for item in apparatus):
        _fail("source packet apparatus must be a list of objects")
    _exact_ids(apparatus, ("construction-cluster", "robot-reading"), "source apparatus")
    expected_attach = {
        "construction-cluster": "lyv-4-2-46",
        "robot-reading": "lyv-4-2-64",
    }
    for item in apparatus:
        if item.get("attach_after") != expected_attach[item["id"]]:
            _fail(
                f"apparatus {item['id']} must attach after {expected_attach[item['id']]}, "
                f"observed {item.get('attach_after')!r}"
            )
    return copy.deepcopy(notes), copy.deepcopy(apparatus)


def _load_producers(paths: Sequence[Path]) -> list[dict[str, Any]]:
    if len(paths) != len(EXPECTED_RANGES):
        _fail(f"exactly {len(EXPECTED_RANGES)} producer packets are required")
    packets = []
    for path, (first, last) in zip(paths, EXPECTED_RANGES):
        packet = _load_json(path)
        if packet.get("schema_version") != PRODUCER_SCHEMA:
            _fail(f"{path} schema_version must be {PRODUCER_SCHEMA!r}")
        range_record = packet.get("range")
        if not isinstance(range_record, dict):
            _fail(f"{path} range must be an object")
        expected_ids = tuple(f"lyv-4-2-{verse}" for verse in range(first, last + 1))
        expected_range = {
            "first_id": expected_ids[0],
            "last_id": expected_ids[-1],
            "expected_units": len(expected_ids),
            "observed_units": len(expected_ids),
        }
        for key, expected in expected_range.items():
            if range_record.get(key) != expected:
                _fail(f"{path} range.{key} must be {expected!r}, observed {range_record.get(key)!r}")
        units = packet.get("units")
        if not isinstance(units, list) or not all(isinstance(unit, dict) for unit in units):
            _fail(f"{path} units must be a list of objects")
        _exact_ids(units, expected_ids, f"producer {path.name}")
        if len(units) != range_record["observed_units"]:
            _fail(
                f"{path} declares {range_record['observed_units']} observed units but contains {len(units)}"
            )
        evidence = packet.get("evidence")
        if not isinstance(evidence, dict) or not evidence:
            _fail(f"{path} evidence must be a non-empty object")
        packets.append(packet)
    return packets


def build_payload(
    source_path: Path = SOURCE_PATH, producer_paths: Sequence[Path] = PRODUCER_PATHS
) -> dict[str, Any]:
    source = _load_json(source_path)
    source_units = _validate_source(source)
    textual_notes, apparatus = _validate_attached_evidence(source)
    semantic_fields = _validate_semantic_fields()
    semantic_field_records = semantic_fields["fields"]
    packets = _load_producers(producer_paths)

    raw_units: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for packet in packets:
        for unit in packet["units"]:
            raw_units.append((unit, packet))
    _exact_ids([unit for unit, _ in raw_units], EXPECTED_IDS, "merged producer units")
    raw_by_id = {unit["id"]: (unit, packet) for unit, packet in raw_units}
    source_by_id = {unit["id"]: unit for unit in source_units}
    notes_by_id = {note["unit_id"]: [note] for note in textual_notes}
    apparatus_by_id: dict[str, list[dict[str, Any]]] = {}
    for item in apparatus:
        apparatus_by_id.setdefault(item["attach_after"], []).append(item)

    public_units: list[dict[str, Any]] = []
    for unit_id in EXPECTED_IDS:
        raw, packet = raw_by_id[unit_id]
        source_unit = source_by_id[unit_id]
        label = f"producer unit {unit_id}"
        _require_keys(
            raw,
            ("id", "source_id", "locus", "speaker", "devanagari", "iast", "english", "sense", "grammar", "words"),
            label,
        )
        if raw["source_id"] != unit_id:
            _fail(f"{label}.source_id must equal {unit_id!r}")
        if raw["devanagari"] != source_unit["deva"]:
            _fail(f"{unit_id} Devanāgarī does not exactly replay the controlling source packet")
        if raw["iast"] != source_unit["iast"]:
            _fail(f"{unit_id} IAST does not exactly replay the controlling source packet")
        for key in ("locus", "speaker", "english", "sense"):
            _nonempty_string(raw[key], f"{label}.{key}")
        grammar = raw["grammar"]
        if not isinstance(grammar, dict):
            _fail(f"{label}.grammar must be an object")
        for key in ("karakaSummary", "verbalModality"):
            _nonempty_string(grammar.get(key), f"{label}.grammar.{key}")
        words = raw["words"]
        if not isinstance(words, list) or not words or not all(isinstance(word, dict) for word in words):
            _fail(f"{label}.words must be a non-empty list of objects")
        root_registry = _registry(packet, "root_evidence", "rootEvidence")
        grammar_registry = _registry(packet, "grammar_evidence", "grammarEvidence")
        normalized_words = [
            _normalize_word(
                word,
                index,
                packet["evidence"],
                root_registry,
                grammar_registry,
                unit_id,
            )
            for index, word in enumerate(words)
        ]
        for word in normalized_words:
            word["semanticFieldKeys"] = _semantic_keys(word, semantic_field_records)
        _validate_slots(raw["english"], [word["i"] for word in normalized_words], label)

        normalized_apparatus = []
        for apparatus_index, apparatus_entry in enumerate(raw.get("apparatus", [])):
            if not isinstance(apparatus_entry, dict):
                _fail(f"{label}.apparatus[{apparatus_index}] must be an object")
            entry = copy.deepcopy(apparatus_entry)
            apparatus_words = entry.get("words", [])
            if apparatus_words:
                if not isinstance(apparatus_words, list) or not all(isinstance(word, dict) for word in apparatus_words):
                    _fail(f"{label}.apparatus[{apparatus_index}].words must be a list of objects")
                entry["words"] = [
                    _normalize_word(
                        word,
                        index,
                        packet["evidence"],
                        root_registry,
                        grammar_registry,
                        f"{unit_id}.apparatus[{apparatus_index}]",
                    )
                    for index, word in enumerate(apparatus_words)
                ]
                for word in entry["words"]:
                    word["semanticFieldKeys"] = _semantic_keys(word, semantic_field_records)
                _validate_slots(
                    _nonempty_string(entry.get("english"), f"{label}.apparatus[{apparatus_index}].english"),
                    [word["i"] for word in entry["words"]],
                    f"{label}.apparatus[{apparatus_index}]",
                )
                alignment_iast = _apparatus_alignment_iast(entry)
                if alignment_iast and isinstance(entry.get("devanagari"), str):
                    entry["sourceSegments"] = _source_segments(
                        entry["devanagari"],
                        alignment_iast,
                        entry["words"],
                        f"{unit_id}.apparatus[{apparatus_index}]",
                    )
            normalized_apparatus.append(entry)

        public = copy.deepcopy(raw)
        public["verse"] = source_unit["verse"]
        # The work and section are already fixed by the reader title and blurb.
        # Repeat only the verse number in each of the 56 cards.
        public["locus"] = f"2.{source_unit['verse']}"
        public["translation"] = raw["sense"]
        public["words"] = normalized_words
        public["sourceSegments"] = _source_segments(
            raw["devanagari"], raw["iast"], normalized_words, unit_id
        )
        public["apparatus"] = normalized_apparatus
        public["textualNotes"] = copy.deepcopy(notes_by_id.get(unit_id, []))
        public["apparatusAfter"] = copy.deepcopy(apparatus_by_id.get(unit_id, []))
        public_units.append(public)

    payload = {
        "schema_version": SCHEMA,
        "title": "The Story of Dāma, Vyāla, and Kaṭa",
        "work": source["work"],
        "section": source["section"],
        "population": copy.deepcopy(source["population"]),
        "source": {
            "packet": str(source_path.relative_to(ROOT)) if source_path.is_relative_to(ROOT) else str(source_path),
            "controlling_witness": copy.deepcopy(source["controlling_witness"]),
            "parallel_witnesses": copy.deepcopy(source["parallel_witnesses"]),
        },
        "textual_notes": textual_notes,
        "apparatus": apparatus,
        "semantic_fields": semantic_fields,
        "units": public_units,
    }
    require_semantic_coverage = (
        source_path.resolve() == SOURCE_PATH.resolve()
        and tuple(path.resolve() for path in producer_paths)
        == tuple(path.resolve() for path in PRODUCER_PATHS)
    )
    validate_public_payload(payload, require_semantic_coverage=require_semantic_coverage)
    return payload


def validate_public_payload(
    payload: Mapping[str, Any], *, require_semantic_coverage: bool = False
) -> None:
    if payload.get("schema_version") != SCHEMA:
        _fail(f"public payload schema_version must be {SCHEMA!r}")
    units = payload.get("units")
    if not isinstance(units, list) or not all(isinstance(unit, dict) for unit in units):
        _fail("public payload units must be a list of objects")
    _exact_ids(units, EXPECTED_IDS, "public payload units")
    ordered_ids = [unit["id"] for unit in units]
    if ordered_ids != list(EXPECTED_IDS):
        _fail("public payload units are not in exact source order")
    semantic_bundle = payload.get("semantic_fields")
    if not isinstance(semantic_bundle, dict):
        _fail("public payload lacks the reviewed semantic-field bundle")
    semantic_keys = {field["key"] for field in semantic_bundle.get("fields", [])}
    if semantic_keys != set(EXPECTED_SEMANTIC_KEYS):
        _fail("public payload semantic-field population is incomplete")
    observed_semantic_keys: set[str] = set()
    for unit in units:
        _nonempty_string(unit.get("translation"), f"{unit['id']}.translation")
        segments = unit.get("sourceSegments")
        if not isinstance(segments, list) or not segments:
            _fail(f"{unit['id']}.sourceSegments must be a non-empty list")
        for segment in segments:
            if not isinstance(segment, dict) or not isinstance(segment.get("text"), str) or segment["text"] == "":
                _fail(f"{unit['id']}.sourceSegments entries require non-empty text")
            if not isinstance(segment.get("word_indices"), list):
                _fail(f"{unit['id']}.sourceSegments.word_indices must be a list")
        reconstructed = "".join(segment["text"] for segment in segments)
        if reconstructed != unit.get("devanagari"):
            _fail(f"{unit['id']}.sourceSegments do not reconstruct exact Devanāgarī")
        observed_indices = [
            index
            for segment in segments
            for index in segment.get("word_indices", [])
        ]
        expected_indices = list(range(len(unit.get("words", []))))
        if observed_indices != expected_indices:
            _fail(
                f"{unit['id']}.sourceSegments must cover each word once in source order: "
                f"expected {expected_indices}, observed {observed_indices}"
            )
        for word in unit.get("words", []):
            keys = word.get("semanticFieldKeys")
            if not isinstance(keys, list) or any(key not in semantic_keys for key in keys):
                _fail(f"{unit['id']} has invalid semantic-field keys")
            observed_semantic_keys.update(keys)
        for entry in unit.get("apparatus", []):
            public_ready = entry.get("status") == "producer-complete" or entry.get("public_ready") is True
            if not public_ready or not entry.get("words"):
                continue
            apparatus_segments = entry.get("sourceSegments")
            if not isinstance(apparatus_segments, list) or not apparatus_segments:
                _fail(f"{unit['id']}.{entry.get('id')}.sourceSegments are required")
            if "".join(segment["text"] for segment in apparatus_segments) != entry.get("devanagari"):
                _fail(f"{unit['id']}.{entry.get('id')} source segments do not preserve Devanāgarī")
            apparatus_indices = [
                index
                for segment in apparatus_segments
                for index in segment.get("word_indices", [])
            ]
            if apparatus_indices != list(range(len(entry["words"]))):
                _fail(f"{unit['id']}.{entry.get('id')} source segments do not cover every word once")
            for word in entry["words"]:
                keys = word.get("semanticFieldKeys")
                if not isinstance(keys, list) or any(key not in semantic_keys for key in keys):
                    _fail(f"{unit['id']}.{entry.get('id')} has invalid semantic-field keys")
                observed_semantic_keys.update(keys)
    if require_semantic_coverage and observed_semantic_keys != semantic_keys:
        missing = sorted(semantic_keys - observed_semantic_keys)
        _fail(f"semantic fields are not attached to the closed word population: {missing}")
    notes = [note for unit in units for note in unit.get("textualNotes", [])]
    if notes != payload.get("textual_notes"):
        _fail("public textual-note attachment does not exactly replay the top-level note population")
    attached = [item for unit in units for item in unit.get("apparatusAfter", [])]
    if attached != payload.get("apparatus"):
        # Top-level source order is robot then construction; display order is source order by verse.
        if sorted(attached, key=lambda item: item["id"]) != sorted(
            payload.get("apparatus", []), key=lambda item: item["id"]
        ):
            _fail("public apparatus attachments do not exactly replay the top-level apparatus population")
    attachment_counts = {
        "lyv-4-2-46": len(next(unit for unit in units if unit["id"] == "lyv-4-2-46")["apparatusAfter"]),
        "lyv-4-2-64": len(next(unit for unit in units if unit["id"] == "lyv-4-2-64")["apparatusAfter"]),
    }
    if attachment_counts != {"lyv-4-2-46": 1, "lyv-4-2-64": 1}:
        _fail(f"public apparatus attachment counts are wrong: {attachment_counts}")


def render_verses_js(payload: Mapping[str, Any]) -> str:
    body = json.dumps(payload["units"], ensure_ascii=False, indent=2)
    return (
        "/* Generated by scripts/build_yogavasistha_dama_reader.py.\n"
        "   Closed population: Laghu-Yoga-Vāsiṣṭha, Sthiti-prakaraṇa 2.31–86. */\n\n"
        f"window.YV_DAMA_VERSES = {body};\n"
    )


def render_review_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_apparatus_js(payload: Mapping[str, Any]) -> str:
    apparatus = {
        "schema_version": "yogavasistha-dama-apparatus-v1",
        "textual_notes": payload["textual_notes"],
        "apparatus": payload["apparatus"],
        "semantic_fields": payload["semantic_fields"],
    }
    body = json.dumps(apparatus, ensure_ascii=False, indent=2)
    return (
        "/* Generated source notes for the Dāma reader. */\n\n"
        f"window.YV_DAMA_APPARATUS = {body};\n"
    )


def render_index_html() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <script>location.replace("../../#/article/yogavasistha-dama");</script>
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=2" />
  <meta name="robots" content="noindex,nofollow,noarchive,nosnippet,noimageindex" />
  <meta name="referrer" content="no-referrer" />
  <title>The Story of Dāma, Vyāla, and Kaṭa</title>
</head>
<body></body>
</html>
"""


def generated_artifacts(payload: Mapping[str, Any]) -> dict[str, str]:
    return {
        "verses.js": render_verses_js(payload),
        "review.json": render_review_json(payload),
        "apparatus.js": render_apparatus_js(payload),
        "index.html": render_index_html(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE_PATH)
    parser.add_argument("--producer", type=Path, action="append", dest="producers")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "gita/yogavasistha-dama")
    parser.add_argument("--check", action="store_true", help="validate inputs and compare all generated artifacts without writing")
    args = parser.parse_args()
    producer_paths = tuple(args.producers) if args.producers else PRODUCER_PATHS
    try:
        payload = build_payload(args.source, producer_paths)
        artifacts = generated_artifacts(payload)
        if args.check:
            for name, expected in artifacts.items():
                path = args.output_dir / name
                if not path.exists():
                    _fail(f"generated reader artifact is missing: {path}")
                if path.read_text(encoding="utf-8") != expected:
                    _fail(f"generated reader artifact is stale: {path}")
            print(f"PASS: {len(payload['units'])} units; all generated artifacts are current")
            return 0
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, rendered in artifacts.items():
            (args.output_dir / name).write_text(rendered, encoding="utf-8")
        print(f"WROTE {args.output_dir}: " + ", ".join(artifacts) + f" ({len(payload['units'])} units)")
        return 0
    except BuildError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

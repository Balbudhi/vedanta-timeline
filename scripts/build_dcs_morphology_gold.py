#!/usr/bin/env python3
"""Build the DCS morphology gold standard for prakriya cross-validation.

Reads the DCS CoNLL-U dump (one file per chapter) and emits a JSONL where
each line is one DCS token enriched with:

  * Surface forms in DCS-native IAST, plus SLP1 + Devanāgarī projections.
  * Parsed UD FEATS as a dict.
  * A `kind` discriminator: tinanta / krdanta / subanta / indeclinable /
    compound (where compound is the multiword-token range row).
  * The matching prakriya tuple for that kind, with vocabulary mapped from
    UD names to the names used by `prakriya.panini_prakriya` (Vidyut
    cross-validation tuples).

Tuple shapes (matching `cross_validate_vidyut.py` fixture rows):

  tinanta_tuple = [root_slp1, gana_or_null, lakara, purusha, vacana, pada]
  krdanta_tuple = [root_slp1, krt_or_null, linga, vibhakti, vacana]
  subanta_tuple = [stem_slp1, linga, vibhakti, vacana]

Gaṇa lookup uses the bundled prakriya dhātupāṭha (Python source + the
`dhatu_set_flags_baked.json` table). The lookup is by SLP1-clean lemma;
roots not in the inventory get gana=null, flagged for the prakriya chat.

Outputs:

  Primary (large, NOT inside the worktree):
    /nas/ucb/eeshan/dcs_morphology_gold/dcs_morphology_gold.jsonl

  Wire-up artifacts (small, committed under the worktree):
    data/dcs_morphology_gold/sample.jsonl
    data/dcs_morphology_gold/coverage_report.json

Re-run: `python3 scripts/build_dcs_morphology_gold.py`. No CLI args
required for the standard run; flags are exposed for incremental debugging.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

# Use indic_transliteration if available; otherwise fall back to a tiny
# IAST→SLP1 / IAST→Devanāgarī shim (not used in the standard run because
# the prakriya .venv is on the runtime path).
try:
    from indic_transliteration.sanscript import (
        DEVANAGARI,
        IAST,
        SLP1,
        transliterate,
    )

    def iast_to_slp1(text: str) -> str:
        if not text:
            return ""
        try:
            return transliterate(text, IAST, SLP1)
        except Exception:
            return ""

    def iast_to_devanagari(text: str) -> str:
        if not text:
            return ""
        try:
            return transliterate(text, IAST, DEVANAGARI)
        except Exception:
            return ""

except Exception:  # pragma: no cover - we expect the lib at runtime

    def iast_to_slp1(text: str) -> str:
        return text

    def iast_to_devanagari(text: str) -> str:
        return text


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DCS_CONLLU_ROOT = Path(
    "/nas/ucb/eeshan/corpus_worktrees/external-ingest/data/external/dcs/dump/"
    "dcs_repo/dcs/data/conllu/files"
)
PRAKRIYA_ROOT = Path("/nas/ucb/eeshan/prakriya")
DHATUPATHA_PY = PRAKRIYA_ROOT / "src/prakriya/panini_prakriya/dhatupatha.py"
DHATUPATHA_BAKED = (
    PRAKRIYA_ROOT
    / "src/prakriya/panini_prakriya/data/dhatu_set_flags_baked.json"
)

OUTPUT_DIR = Path("/nas/ucb/eeshan/dcs_morphology_gold")
OUTPUT_JSONL = OUTPUT_DIR / "dcs_morphology_gold.jsonl"

WORKTREE_DATA_DIR = (
    Path(__file__).resolve().parent.parent / "data" / "dcs_morphology_gold"
)
SAMPLE_JSONL = WORKTREE_DATA_DIR / "sample.jsonl"
COVERAGE_JSON = WORKTREE_DATA_DIR / "coverage_report.json"


# ---------------------------------------------------------------------------
# UD → prakriya vocabulary maps
# ---------------------------------------------------------------------------

# UD `Tense`/`Mood` → prakriya lakāra (internal SLP1-style key as used in
# `panini_prakriya.tin_pratyaya`: law/liw/luw/lfw/low/laN/liN/luN/lfN).
#
# Coverage notes:
#   * UD's `Mood=Imp` (imperative) → loṭ (low).
#   * UD's `Mood=Opt` (optative) / `Mood=Sub` (subjunctive) → liṅ (liN).
#   * UD's `Mood=Cnd` (conditional) → lṛṅ (lfN).
#   * UD's `Tense=Aor` → luṅ (luN); `Tense=Imp` → laṅ (laN); `Tense=Perf` →
#     liṭ (liw); `Tense=Fut` → lṛṭ (lfw); `Tense=Pqp` → lṛṅ (lfN, best
#     available approximation for DCS pluperfect tags which Pāṇini does
#     not have a separate lakāra for).
#   * UD `Tense=Pres,Mood=Ind` → laṭ (law).
#
# The mapping is intentionally Mood-first then Tense; entries below are
# matched in order of priority.

LAKARA_PRIORITY: tuple[tuple[tuple[str, str], str], ...] = (
    (("Mood", "Imp"), "low"),
    (("Mood", "Opt"), "liN"),
    (("Mood", "Sub"), "liN"),
    (("Mood", "Cnd"), "lfN"),
    (("Mood", "Jus"), "luN"),    # injunctive (Vedic) → luṅ (best fit)
    (("Mood", "Ben"), "liN"),    # benedictive → āśīr-liṅ
    (("Tense", "Pres"), "law"),
    (("Tense", "Past"), "laN"),
    (("Tense", "Imp"), "laN"),
    (("Tense", "Aor"), "luN"),
    (("Tense", "Perf"), "liw"),
    (("Tense", "Pqp"), "lfN"),
    (("Tense", "Fut"), "lfw"),
)

PADA_MAP = {
    "Act": "parasmaipada",
    "Mid": "atmanepada",
    "Pass": "atmanepada",  # karmaṇi takes ātmanepada endings
}

PURUSHA_MAP = {
    "1": "uttama",
    "2": "madhyama",
    "3": "prathama",
}

VACANA_MAP = {
    "Sing": "ekavacana",
    "Dual": "dvivacana",
    "Plur": "bahuvacana",
}

# UD `Case` → vibhakti number (1..7 + 8 for sambodhana). DCS uses the
# standard UD names; "Cpd" marks compound members and we keep the surface
# but don't emit a subanta tuple.
VIBHAKTI_MAP = {
    "Nom": 1,
    "Acc": 2,
    "Ins": 3,
    "Dat": 4,
    "Abl": 5,
    "Gen": 6,
    "Loc": 7,
    "Voc": 8,
}

LINGA_MAP = {
    "Masc": "pum",
    "Fem": "stri",
    "Neut": "napumsaka",
}


# ---------------------------------------------------------------------------
# Dhātupāṭha lookup: IAST/clean lemma → list of gaṇa numbers.
# ---------------------------------------------------------------------------

_DHATU_ENTRY_RE = re.compile(
    r'DhatuEntry\(\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*(\d+)\s*,'
)


def _load_dhatupatha_index() -> dict[str, list[int]]:
    """Return SLP1-clean root → sorted list of gaṇas (1..10).

    Combines (a) the inline `DhatuEntry(...)` literals in
    `panini_prakriya/dhatupatha.py` and (b) the baked
    `dhatu_set_flags_baked.json` table (which is the Vidyut-derived
    superset).
    """

    by_clean: dict[str, set[int]] = defaultdict(set)

    # (a) Python source.
    if DHATUPATHA_PY.exists():
        src = DHATUPATHA_PY.read_text(encoding="utf-8")
        for m in _DHATU_ENTRY_RE.finditer(src):
            _upadesha, clean, gana = m.group(1), m.group(2), int(m.group(3))
            if clean:
                by_clean[clean].add(gana)

    # (b) Baked JSON (Vidyut-derived rows).
    if DHATUPATHA_BAKED.exists():
        with DHATUPATHA_BAKED.open("r", encoding="utf-8") as fh:
            doc = json.load(fh)
        for row in doc.get("rows", []):
            clean = row.get("clean") or ""
            gana = row.get("gana")
            if clean and isinstance(gana, int):
                by_clean[clean].add(gana)

    return {k: sorted(v) for k, v in by_clean.items()}


DHATU_INDEX: dict[str, list[int]] = {}


# Common upasargas (preverbs) in SLP1, longest-first so multi-syllable prefixes
# match before their substrings (`sam` ⊂ `samanu`).
UPASARGAS_SLP1: tuple[str, ...] = (
    "samanu",
    "abhinis",
    "abhisam",
    "samupa",
    "samabhi",
    "anuvi",
    "pratyA",
    "praty",
    "uparis",
    "abhi",
    "anuv",
    "anu",
    "adhi",
    "ava",
    "apa",
    "api",
    "ati",
    "ut",
    "ud",
    "ni",
    "nis",
    "nir",
    "para",
    "pari",
    "pra",
    "prati",
    "vi",
    "sam",
    "su",
    "dur",
    "dus",
    "A",
    "upa",
)


def _strip_upasargas(root_slp1: str) -> str:
    """Strip leading upasarga(s) from a compound dhātu lemma.

    Greedy; iterates until no more prefix removal possible OR the residual
    is in the dhātupāṭha. Returns the (possibly unchanged) bare root.
    """
    cur = root_slp1
    for _ in range(4):  # at most 4 layers of preverbs
        if cur in DHATU_INDEX:
            return cur
        stripped = False
        for prefix in UPASARGAS_SLP1:
            if cur.startswith(prefix) and len(cur) > len(prefix) + 1:
                cand = cur[len(prefix) :]
                if cand in DHATU_INDEX:
                    return cand
                # Allow speculative descent even if not yet a direct hit, so
                # `samanuSI` → `anuSI` → `SI` resolves.
                cur = cand
                stripped = True
                break
        if not stripped:
            break
    return cur


@lru_cache(maxsize=200_000)
def _lookup_gana(root_slp1: str) -> int | None:
    """Return the unique gaṇa for ``root_slp1`` or None if ambiguous/missing.

    DCS does not tag gaṇa on the dhātu, so we resolve via the prakriya
    dhātupāṭha. When the SLP1-clean root maps to multiple gaṇas (e.g.
    homonymous roots like ``han`` in gaṇa 2 vs ``han~`` in gaṇa 10),
    we return None and leave gaṇa for the prakriya chat to resolve from
    semantics. When the root is not in the inventory at all, we strip
    leading upasargas (preverbs) and retry; on still-unresolved we return
    None (the coverage report flags the unresolved fraction).
    """

    if not root_slp1:
        return None
    options = DHATU_INDEX.get(root_slp1)
    if options is None:
        bare = _strip_upasargas(root_slp1)
        if bare != root_slp1:
            options = DHATU_INDEX.get(bare)
    if not options:
        return None
    if len(options) == 1:
        return options[0]
    return None  # ambiguous


# ---------------------------------------------------------------------------
# FEATS parsing
# ---------------------------------------------------------------------------


def parse_feats(feats_field: str) -> dict[str, str]:
    """Parse a CoNLL-U FEATS field (`Key=Val|Key=Val`) into a dict."""
    if not feats_field or feats_field == "_":
        return {}
    out: dict[str, str] = {}
    for chunk in feats_field.split("|"):
        if "=" in chunk:
            k, v = chunk.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def parse_misc(misc_field: str) -> dict[str, str]:
    if not misc_field or misc_field == "_":
        return {}
    out: dict[str, str] = {}
    for chunk in misc_field.split("|"):
        if "=" in chunk:
            k, v = chunk.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def feats_to_lakara(feats: dict[str, str]) -> str | None:
    for (key, val), lakara in LAKARA_PRIORITY:
        if feats.get(key) == val:
            return lakara
    return None


def feats_to_pada(feats: dict[str, str]) -> str | None:
    voice = feats.get("Voice")
    if not voice:
        return None
    return PADA_MAP.get(voice)


def classify_kind(upos: str, feats: dict[str, str]) -> str:
    """Return one of: tinanta, krdanta, subanta, indeclinable, other."""
    if upos == "VERB":
        # UD marks participles / infinitives / converbs with VerbForm; the
        # finite verb form has VerbForm=Fin or no VerbForm at all (with
        # Person/Tense/Mood set).
        vform = feats.get("VerbForm")
        if vform in {"Part", "Inf", "Conv", "Ger", "Gdv", "Vnoun"}:
            return "krdanta"
        if vform == "Fin" or "Person" in feats:
            return "tinanta"
        # Naked VERB without Person/VerbForm — treat as krdanta (DCS does
        # mark many adjectival past-participles this way).
        return "krdanta"
    if upos in {"NOUN", "PROPN", "ADJ", "PRON", "NUM", "DET"}:
        # If Case=Cpd, it is a compound member (not a free-standing subanta).
        if feats.get("Case") == "Cpd":
            return "compound_member"
        return "subanta"
    if upos in {"ADV", "PART", "INTJ", "CCONJ", "SCONJ", "CONJ", "ADP", "X"}:
        return "indeclinable"
    return "other"


# ---------------------------------------------------------------------------
# Tuple builders
# ---------------------------------------------------------------------------


def build_tinanta_tuple(
    lemma_slp1: str, feats: dict[str, str]
) -> list[Any] | None:
    lakara = feats_to_lakara(feats)
    if lakara is None:
        return None
    person = PURUSHA_MAP.get(feats.get("Person", ""))
    vacana = VACANA_MAP.get(feats.get("Number", ""))
    pada = feats_to_pada(feats)
    if not (person and vacana):
        return None
    gana = _lookup_gana(lemma_slp1)
    return [lemma_slp1, gana, lakara, person, vacana, pada]


def build_krdanta_tuple(
    lemma_slp1: str, feats: dict[str, str]
) -> list[Any] | None:
    # DCS doesn't tag the kṛt suffix directly; encode the linga/case/number
    # for the nominal half and leave krt=null for the prakriya chat to
    # back out from VerbForm + Voice + Tense. We still emit the row so the
    # tuple can be cross-validated when the kṛt is later resolved.
    linga = LINGA_MAP.get(feats.get("Gender", ""))
    vibhakti = VIBHAKTI_MAP.get(feats.get("Case", ""))
    vacana = VACANA_MAP.get(feats.get("Number", ""))
    if not (linga and vibhakti and vacana):
        return None
    # Heuristic kṛt inference from VerbForm + Tense + Voice:
    krt = _infer_krt(feats)
    return [lemma_slp1, krt, linga, vibhakti, vacana]


def _infer_krt(feats: dict[str, str]) -> str | None:
    vform = feats.get("VerbForm")
    tense = feats.get("Tense")
    voice = feats.get("Voice")
    if vform == "Part":
        if tense == "Past" and voice in {"Pass", None}:
            return "kta"
        if tense == "Past" and voice == "Act":
            return "ktavatu"
        if tense == "Pres" and voice == "Act":
            return "Satf"
        if tense == "Pres" and voice == "Mid":
            return "SAnac"
        if tense == "Fut" and voice == "Act":
            return "syatf"
        if tense == "Fut" and voice == "Mid":
            return "syamAna"
        if tense == "Perf":
            return "kvasu"
    if vform == "Inf":
        return "tumun"
    if vform == "Conv":
        return "ktvA"
    if vform == "Gdv":
        return "tavya"
    return None


def build_subanta_tuple(
    stem_slp1: str, feats: dict[str, str]
) -> list[Any] | None:
    linga = LINGA_MAP.get(feats.get("Gender", ""))
    vibhakti = VIBHAKTI_MAP.get(feats.get("Case", ""))
    vacana = VACANA_MAP.get(feats.get("Number", ""))
    if not (linga and vibhakti and vacana):
        return None
    return [stem_slp1, linga, vibhakti, vacana]


# ---------------------------------------------------------------------------
# CoNLL-U streaming parser
# ---------------------------------------------------------------------------

_NFC = lambda s: unicodedata.normalize("NFC", s) if s else s


def iter_conllu_files(root: Path) -> Iterator[Path]:
    for p in sorted(root.rglob("*.conllu")):
        yield p


def parse_file(path: Path) -> Iterator[dict[str, Any]]:
    """Yield per-token dicts, with file-level + sentence-level context."""

    text_id = None
    text_name = None
    chapter = None
    chapter_id = None

    sent_id = None
    sent_counter = None
    sent_subcounter = None
    sent_text = None

    # Track the most-recent multiword range so we can mark its members.
    range_start = None
    range_end = None
    range_form = None

    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n")

            if not line:
                # Sentence boundary — reset sentence context.
                sent_id = sent_counter = sent_subcounter = sent_text = None
                range_start = range_end = range_form = None
                continue

            if line.startswith("## "):
                # File-level header.
                key, _, val = line[3:].partition(":")
                key = key.strip()
                val = val.strip()
                if key == "text":
                    text_name = val
                elif key == "text_id":
                    text_id = val
                elif key == "chapter":
                    chapter = val
                elif key == "chapter_id":
                    chapter_id = val
                continue

            if line.startswith("# "):
                # Sentence-level header.
                body = line[2:]
                if body.startswith("text = "):
                    sent_text = body[len("text = ") :]
                elif body.startswith("sent_id = "):
                    sent_id = body[len("sent_id = ") :]
                elif body.startswith("sent_counter = "):
                    sent_counter = body[len("sent_counter = ") :]
                elif body.startswith("sent_subcounter = "):
                    sent_subcounter = body[len("sent_subcounter = ") :]
                continue

            cols = line.split("\t")
            if len(cols) < 10:
                continue

            tok_id, form, lemma, upos, _xpos, feats_s, _head, _dep, _deps, misc_s = (
                cols[0],
                cols[1],
                cols[2],
                cols[3],
                cols[4],
                cols[5],
                cols[6],
                cols[7],
                cols[8],
                cols[9],
            )

            if "-" in tok_id:
                # Multiword (compound) range row.
                try:
                    a, b = tok_id.split("-", 1)
                    range_start = int(a)
                    range_end = int(b)
                except ValueError:
                    range_start = range_end = None
                range_form = form
                yield {
                    "_kind": "compound_range",
                    "tok_id": tok_id,
                    "form": form,
                    "text_id": text_id,
                    "text_name": text_name,
                    "chapter": chapter,
                    "chapter_id": chapter_id,
                    "sent_id": sent_id,
                    "sent_counter": sent_counter,
                    "sent_subcounter": sent_subcounter,
                    "sent_text": sent_text,
                }
                continue

            # Regular token.
            try:
                tok_index = int(tok_id)
            except ValueError:
                tok_index = None

            in_compound = (
                range_start is not None
                and range_end is not None
                and tok_index is not None
                and range_start <= tok_index <= range_end
            )
            compound_role: str | None
            if in_compound:
                if tok_index == range_start:
                    compound_role = "purvapada"
                elif tok_index == range_end:
                    compound_role = "uttarapada"
                else:
                    compound_role = "madhyamapada"
            else:
                compound_role = None

            yield {
                "_kind": "token",
                "tok_id": tok_id,
                "tok_index": tok_index,
                "form": _NFC(form),
                "lemma": _NFC(lemma),
                "upos": upos,
                "feats_raw": feats_s,
                "misc_raw": misc_s,
                "text_id": text_id,
                "text_name": text_name,
                "chapter": chapter,
                "chapter_id": chapter_id,
                "sent_id": sent_id,
                "sent_counter": sent_counter,
                "sent_subcounter": sent_subcounter,
                "sent_text": sent_text,
                "compound_member": in_compound,
                "compound_role": compound_role,
                "compound_form": range_form if in_compound else None,
            }


# ---------------------------------------------------------------------------
# Per-token enrichment
# ---------------------------------------------------------------------------


def enrich_token(rec: dict[str, Any]) -> dict[str, Any] | None:
    """Turn a parsed CoNLL-U token row into the gold-output schema.

    Returns None for non-emittable rows (compound ranges, blank lemmas).
    """

    if rec["_kind"] != "token":
        return None
    if rec["upos"] in {"_", "", "PUNCT"}:
        return None

    feats = parse_feats(rec["feats_raw"])
    misc = parse_misc(rec["misc_raw"])

    lemma_iast = rec["lemma"] or ""
    surface_iast = rec["form"] or ""
    unsandhied = misc.get("Unsandhied") or surface_iast

    lemma_slp1 = iast_to_slp1(lemma_iast)
    surface_dev = iast_to_devanagari(surface_iast)

    kind = classify_kind(rec["upos"], feats)

    tinanta_tuple: list[Any] | None = None
    krdanta_tuple: list[Any] | None = None
    subanta_tuple: list[Any] | None = None

    if kind == "tinanta":
        tinanta_tuple = build_tinanta_tuple(lemma_slp1, feats)
    elif kind == "krdanta":
        krdanta_tuple = build_krdanta_tuple(lemma_slp1, feats)
    elif kind in {"subanta", "compound_member"}:
        subanta_tuple = build_subanta_tuple(lemma_slp1, feats)

    return {
        "dcs_occ_id": misc.get("OccId"),
        "dcs_lemma_id": misc.get("LemmaId"),
        "lemma_iast": lemma_iast,
        "lemma_slp1": lemma_slp1,
        "surface_devanagari": surface_dev,
        "surface_iast": surface_iast,
        "unsandhied": unsandhied,
        "upos": rec["upos"],
        "feats": feats,
        "kind": kind,
        "tinanta_tuple": tinanta_tuple,
        "subanta_tuple": subanta_tuple,
        "krdanta_tuple": krdanta_tuple,
        "text_id": rec["text_id"],
        "text_name": rec["text_name"],
        "chapter_id": rec["chapter_id"],
        "verse_id": rec["sent_id"],
        "sent_counter": rec["sent_counter"],
        "sent_subcounter": rec["sent_subcounter"],
        "compound_member": bool(rec["compound_member"]),
        "compound_role": rec["compound_role"],
        "compound_form": rec["compound_form"],
    }


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--limit-files",
        type=int,
        default=0,
        help="Cap on number of CoNLL-U files to process (0 = all). Debug only.",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_JSONL,
        help=f"Where to write the gold JSONL (default: {OUTPUT_JSONL}).",
    )
    ap.add_argument(
        "--sample-lines",
        type=int,
        default=50,
        help="Number of leading lines to also copy into sample.jsonl.",
    )
    args = ap.parse_args(argv)

    global DHATU_INDEX
    DHATU_INDEX = _load_dhatupatha_index()
    print(
        f"[init] dhātupāṭha index: {len(DHATU_INDEX)} unique SLP1-clean roots",
        file=sys.stderr,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    WORKTREE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Coverage accumulators.
    total_files = 0
    total_tokens = 0
    total_compound_ranges = 0
    kind_counts: Counter[str] = Counter()
    text_counts: dict[str, Counter[str]] = defaultdict(Counter)
    text_lemma_resolved: dict[str, dict[str, int]] = defaultdict(
        lambda: {"tinanta_tuples": 0, "krdanta_tuples": 0, "subanta_tuples": 0}
    )
    gana_resolved = 0
    tinanta_total = 0
    upos_counts: Counter[str] = Counter()

    start = time.time()
    sample_buf: list[str] = []

    with args.output.open("w", encoding="utf-8") as out_fh:
        for path in iter_conllu_files(DCS_CONLLU_ROOT):
            total_files += 1
            if args.limit_files and total_files > args.limit_files:
                break
            text_key = path.parent.name  # work name
            for raw_rec in parse_file(path):
                if raw_rec["_kind"] == "compound_range":
                    total_compound_ranges += 1
                    kind_counts["compound_range"] += 1
                    text_counts[text_key]["compound_range"] += 1
                    continue
                gold = enrich_token(raw_rec)
                if gold is None:
                    continue
                total_tokens += 1
                upos_counts[gold["upos"]] += 1
                kind_counts[gold["kind"]] += 1
                text_counts[text_key][gold["kind"]] += 1

                if gold["tinanta_tuple"] is not None:
                    tinanta_total += 1
                    if gold["tinanta_tuple"][1] is not None:
                        gana_resolved += 1
                    text_lemma_resolved[text_key]["tinanta_tuples"] += 1
                if gold["krdanta_tuple"] is not None:
                    text_lemma_resolved[text_key]["krdanta_tuples"] += 1
                if gold["subanta_tuple"] is not None:
                    text_lemma_resolved[text_key]["subanta_tuples"] += 1

                line = json.dumps(gold, ensure_ascii=False)
                out_fh.write(line)
                out_fh.write("\n")
                if len(sample_buf) < args.sample_lines:
                    sample_buf.append(line)

            if total_files % 500 == 0:
                elapsed = time.time() - start
                print(
                    f"[progress] files={total_files} tokens={total_tokens} "
                    f"elapsed={elapsed:.1f}s",
                    file=sys.stderr,
                )

    elapsed = time.time() - start

    # Write sample.
    with SAMPLE_JSONL.open("w", encoding="utf-8") as fh:
        for line in sample_buf:
            fh.write(line)
            fh.write("\n")

    # Compute sha256 + size of the big JSONL.
    sha = hashlib.sha256()
    size_bytes = 0
    with args.output.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            sha.update(chunk)
            size_bytes += len(chunk)

    # Build coverage report.
    coverage = {
        "generated_at_unix": int(time.time()),
        "wall_clock_seconds": round(elapsed, 2),
        "input_root": str(DCS_CONLLU_ROOT),
        "output_path": str(args.output),
        "output_sha256": sha.hexdigest(),
        "output_size_bytes": size_bytes,
        "total_files_processed": total_files,
        "total_tokens_emitted": total_tokens,
        "total_compound_ranges": total_compound_ranges,
        "kind_counts": dict(kind_counts),
        "upos_counts": dict(upos_counts),
        "tinanta_total": tinanta_total,
        "tinanta_gana_resolved": gana_resolved,
        "tinanta_gana_resolution_rate": (
            round(gana_resolved / tinanta_total, 4) if tinanta_total else None
        ),
        "dhatupatha_unique_cleans": len(DHATU_INDEX),
        "per_text": {
            name: {
                "kind_counts": dict(counts),
                "resolved_tuples": dict(text_lemma_resolved.get(name, {})),
            }
            for name, counts in sorted(text_counts.items())
        },
    }

    with COVERAGE_JSON.open("w", encoding="utf-8") as fh:
        json.dump(coverage, fh, ensure_ascii=False, indent=2)

    # Print high-level summary.
    print(
        f"[done] files={total_files} tokens={total_tokens} "
        f"compound_ranges={total_compound_ranges} elapsed={elapsed:.1f}s",
        file=sys.stderr,
    )
    for k, n in kind_counts.most_common():
        print(f"  kind={k:<20s} {n}", file=sys.stderr)
    print(
        f"  tinanta gaṇa resolution: {gana_resolved}/{tinanta_total} "
        f"({coverage['tinanta_gana_resolution_rate']})",
        file=sys.stderr,
    )
    print(f"  output: {args.output} ({size_bytes / 1e6:.1f} MB)", file=sys.stderr)
    print(f"  sha256: {sha.hexdigest()}", file=sys.stderr)
    print(f"  coverage report: {COVERAGE_JSON}", file=sys.stderr)
    print(f"  sample: {SAMPLE_JSONL}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    os.environ.setdefault("TMPDIR", "/nas/ucb/eeshan/tmp")
    raise SystemExit(main())

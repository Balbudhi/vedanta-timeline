#!/usr/bin/env python3
"""Build the in-repo primary-source mirror for the unified panel's Source tab.

The full primary-text corpus (`materials/primary_texts/`) is ~8 GB and lives
*outside* the site repo. GitHub Pages can only serve what is in the site repo,
so this script:

  1. Walks `materials/primary_texts/` (including the curated `_replaced/_pure_sanskrit/`
     subset; the noisy raw `_replaced/` djvu OCR is skipped except where named
     explicitly via `WORK_OVERRIDES`).
  2. Selects files referenced by `citation_index.json` and by `engaged_works[]`
     entries in `data/thinkers/*.json` whose `source_status` is `clean-on-disk`
     or `acceptable-on-disk`.
  3. Copies the selected files into `site/data/sources/<lang>/<category>/<file>`.
  4. Writes `site/data/primary_text_manifest.json` with metadata for ONLY the
     files actually shipped — so the Source tab's tree shows only what loads.

Selection has three strata:
  (a) `WORK_OVERRIDES`: explicit (thinker_id, work_id) → relative-path map for
      cases where transliteration differs (e.g. Madhva files use mixed-case
      GRETIL conventions). Authoritative.
  (b) Citation-index heuristic match (token-based, with romanization aliases).
  (c) Canonical comparator/foundational texts (`ALWAYS_INCLUDE`).

Wave-10 OCR fallback: if `tmp/wave10_ocr_out/<work_slug>/_FINAL/*.txt`
exists, it is mirrored under `sanskrit/_wave10/`. This lets the script pull
in freshly-OCR'd texts as the wave-10 jobs complete.

Public-tier policy: `enforce_public_tier_only()` aborts the build if any
selected file resolves under `materials/secondary_sources/` (modern academic
scholarship). The site mirror is a public GitHub Pages artifact.

Run from anywhere:
    python3 site/scripts/build_site_sources.py

Output is reproducible: the script is idempotent.
"""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]  # …/philosophy
SITE_ROOT = REPO_ROOT / "site"
MATERIALS = REPO_ROOT / "materials" / "primary_texts"
SECONDARY_TIER = REPO_ROOT / "materials" / "secondary_sources"
WAVE10_OCR = REPO_ROOT / "tmp" / "wave10_ocr_out"
OUT_DIR = SITE_ROOT / "data" / "sources"
MANIFEST_OUT = SITE_ROOT / "data" / "primary_text_manifest.json"
CITATION_INDEX = SITE_ROOT / "data" / "citation_index.json"
THINKERS_DIR = SITE_ROOT / "data" / "thinkers"

TEXT_EXTENSIONS = {".txt", ".md"}
SKIP_BASENAMES = {"PROVENANCE.md", "README.md", ".DS_Store", "_extract.py"}
# `_replaced` proper holds raw djvu OCR (very noisy); `_replaced/_pure_sanskrit`
# under it is curated and IS included by walking it directly below.
SKIP_DIR_PARTS = {"_replaced", "_acquired_wave10", "__pycache__", "_wave10_ocr_out"}

# Curated supplementary directory (under _replaced but worth shipping).
PURE_SKT_DIR = MATERIALS / "sanskrit" / "_replaced" / "_pure_sanskrit"

# Canonical comparator/foundational texts to always ship even when not directly
# referenced by a citation entry — these are useful for the Source tab as
# orientation reading.
ALWAYS_INCLUDE = [
    "sanskrit/comparator/badarayana_brahma_sutra.txt",
    "sanskrit/comparator/aksapada_nyaya_sutra.txt",
    "sanskrit/comparator/jaimini_mimamsa_sutra.txt",
    "sanskrit/comparator/kanada_vaisesika_sutra.txt",
    "sanskrit/comparator/patanjali_yoga_sutra.txt",
    "sanskrit/comparator/isvarakrsna_samkhya_karika.txt",
    "sanskrit/comparator/umasvati_tattvartha_sutra.txt",
    "sanskrit/comparator/shabara_mimamsa_sutra_bhasya.txt",
    "sanskrit/comparator/vatsyayana_nyaya_bhasya.txt",
    "sanskrit/comparator/vyasa_yoga_bhasya.txt",
]

# Authoritative (thinker_id, work_id) → primary-text path. Paths are relative
# to MATERIALS; if a path does not exist it is silently skipped. Includes
# pointers into `_replaced/_pure_sanskrit/` (curated) and the normally-skipped
# `_replaced/` (the raw djvu, where it is the only available witness).
WORK_OVERRIDES: Dict[Tuple[str, str], List[str]] = {
    # Sankara
    ("sankara", "brahma-sutra-bhasya"): ["sanskrit/vedanta/shankara_brahma_sutra_bhasya.txt"],
    ("sankara", "upadesa-sahasri"): ["sanskrit/vedanta/full_corpus/shankara_upadesa_sahasri_gretil.txt"],
    ("sankara", "vivekacudamani"): ["sanskrit/vedanta/full_corpus/shankara_vivekacudamani_gretil.txt"],
    ("sankara", "mandukya-bhasya"): ["sanskrit/vedanta/full_corpus/mandukya_upanisad_gaudapada_shankara_bhasya_existing.txt"],
    ("gaudapada", "mandukya-karika"): ["sanskrit/vedanta/full_corpus/gaudapada_mandukya_karika_gretil.txt"],
    # Madhva
    ("madhva", "brahma-sutra-bhasya"): ["sanskrit/_replaced/_pure_sanskrit/madhva_brahma_sutra_bhasya_3comm_vol1__pure-skt.txt"],
    ("madhva", "anuvyakhyana"): ["sanskrit/vedanta/full_corpus/madhva_anuvyakhyana_gretil.txt"],
    ("madhva", "anuvyakhyana-bhasya-passages"): ["sanskrit/vedanta/full_corpus/madhva_anuvyakhyana_gretil.txt"],
    ("madhva", "mahabharata-tatparya-nirnaya"): ["sanskrit/vedanta/madhva_mahabharata_tatparya.txt"],
    ("madhva", "bhagavata-tatparya-nirnaya"): ["sanskrit/_replaced/_pure_sanskrit/madhva_bhagavata_tatparya_nirnaya__pure-skt.txt"],
    ("madhva", "mayavada-khandana"): ["sanskrit/vedanta/madhva_mayavada_khandana_anandamakaranda.txt"],
    ("madhva", "krsnamrtamaharnava"): ["sanskrit/vedanta/madhva_krsnamrta.txt"],
    ("mandana", "vidhi-viveka"): ["sanskrit/_replaced/gretil_sa_maNDanamizra-vibhramaviveka.txt"],
    ("srinivasa", "vedanta-kaustubha"): ["sanskrit/_replaced/_pure_sanskrit/nimbarka_brahmasutra_3comm_vrindavan__pure-skt.txt"],
    # Ramanuja
    ("ramanuja", "shri-bhasya"): ["sanskrit/_replaced/_pure_sanskrit/ramanuja_sribhashya__pure-skt.txt"],
    ("ramanuja", "vedartha-samgraha"): ["sanskrit/vedanta/ramanuja_vedartha_sangraha.txt"],
    ("ramanuja", "vedartha-sangraha"): ["sanskrit/vedanta/ramanuja_vedartha_sangraha.txt"],
    ("ramanuja", "gita-bhasya"): ["sanskrit/vedanta/ramanuja_gita_bhasya.txt"],
    # Madhusudana
    ("madhusudana", "advaita-siddhi"): ["sanskrit/_replaced/_pure_sanskrit/madhusudana_advaita_siddhi_anantakrishna__pure-skt.txt"],
    ("madhusudana", "siddhanta-bindu"): ["sanskrit/vedanta/full_corpus/madhusudana_siddhanta_bindu_gretil.txt"],
    ("madhusudana", "bhakti-rasayana"): ["sanskrit/_replaced/_pure_sanskrit/madhusudana_bhakti_rasayana_pandey__pure-skt.txt"],
    # Vyasatirtha
    ("vyasatirtha", "tarka-tandava"): ["sanskrit/vedanta/full_corpus/vyasatirtha_tarka_tandava_gretil.txt"],
    # Yamuna
    ("yamuna", "atma-siddhi"): ["sanskrit/vedanta/full_corpus/yamuna_atma_siddhi_gretil.txt"],
    ("yamuna", "isvara-siddhi"): ["sanskrit/vedanta/full_corpus/yamuna_isvara_siddhi_gretil.txt"],
    ("yamuna", "samvit-siddhi"): ["sanskrit/vedanta/full_corpus/yamuna_samvit_siddhi_gretil.txt"],
    ("yamuna", "siddhi-trayam"): [
        "sanskrit/vedanta/full_corpus/yamuna_atma_siddhi_gretil.txt",
        "sanskrit/vedanta/full_corpus/yamuna_isvara_siddhi_gretil.txt",
        "sanskrit/vedanta/full_corpus/yamuna_samvit_siddhi_gretil.txt",
    ],
    ("yamuna", "stotra-ratna"): ["sanskrit/vedanta/full_corpus/yamuna_stotra_ratna_gretil.txt"],
    ("yamuna", "catuh-shloki"): ["sanskrit/vedanta/full_corpus/yamuna_catuhsloki_gretil.txt"],
    ("yamuna", "catuhshloki"): ["sanskrit/vedanta/full_corpus/yamuna_catuhsloki_gretil.txt"],
    ("yamuna", "agama-pramanya"): ["sanskrit/_replaced/_pure_sanskrit/yamuna_agama_pramanya_rama_mishra_1937__pure-skt.txt"],
    # Mandana
    ("mandana", "brahma-siddhi"): ["sanskrit/vedanta/full_corpus/mandana_misra_brahma_siddhi_gretil.txt"],
    # Padmapada / Prakasatman
    ("padmapada", "pancapadika"): ["sanskrit/_replaced/padmapada_pancapadika_dli_archive_djvu.txt"],
    ("prakasatman", "pancapadika-vivarana"): ["sanskrit/_replaced/prakasatman_pancapadika_vivarana_archive_djvu.txt"],
    ("prakasatman", "vivarana-prameya-sangraha"): ["sanskrit/_replaced/prakasatman_pancapadika_vivarana_archive_djvu.txt"],
    # Vijnanabhiksu
    ("vijnanabhiksu", "vijnanamrta-bhasya"): ["sanskrit/_replaced/_pure_sanskrit/vijnanabhiksu_vijnanamrta_bhasya_1979__pure-skt.txt"],
    ("vijnanabhiksu", "yoga-varttika"): ["sanskrit/_replaced/_pure_sanskrit/vijnanabhiksu_yoga_varttika_1884__pure-skt.txt"],
    # Vimuktatman
    ("vimuktatman", "ishta-siddhi"): ["sanskrit/_replaced/_pure_sanskrit/vimuktatman_ista_siddhi_hiriyanna_1933__pure-skt.txt"],
    ("vimuktatman", "ista-siddhi"): ["sanskrit/_replaced/_pure_sanskrit/vimuktatman_ista_siddhi_hiriyanna_1933__pure-skt.txt"],
    # Sarvajnatman
    ("sarvajnatman", "samkshepa-sariraka"): ["sanskrit/_replaced/sarvajnatman_sanksepa_sariraka_veezhinathan_1972_archive_djvu.txt"],
    ("sarvajnatman", "samksepa-sariraka"): ["sanskrit/_replaced/sarvajnatman_sanksepa_sariraka_veezhinathan_1972_archive_djvu.txt"],
    # Sureshvara
    ("sureshvara", "naishkarmya-siddhi"): ["sanskrit/_replaced/suresvara_naiskarmya_siddhi_alston_archive_djvu.txt"],
    ("sureshvara", "brhadaranyaka-varttika"): ["sanskrit/_replaced/sureshvara_brhadaranyaka_varttika_agashe_1892_vol1_archive_djvu.txt"],
    ("sureshvara", "taittiriya-varttika"): ["sanskrit/_replaced/sureshvara_taittiriya_varttika_anandashram_1889_archive_djvu.txt"],
    # Vidyaranya
    ("vidyaranya", "jivanmukti-viveka"): ["sanskrit/_replaced/vidyaranya_jivanmukti_viveka_archive_djvu.txt"],
    ("vidyaranya", "panchadashi"): ["sanskrit/_replaced/vidyaranya_panchadasi_archive_djvu.txt"],
    ("vidyaranya", "panchadasi"): ["sanskrit/_replaced/vidyaranya_panchadasi_archive_djvu.txt"],
    ("vidyaranya", "vivarana-prameya-sangraha"): ["sanskrit/_replaced/prakasatman_pancapadika_vivarana_archive_djvu.txt"],
    # Vallabha
    ("vallabha", "anubhasya"): ["sanskrit/_replaced/_pure_sanskrit/vallabha_anubhasya_text_1921_mumbai__pure-skt.txt"],
    ("vallabha", "anu-bhasya"): ["sanskrit/_replaced/_pure_sanskrit/vallabha_anubhasya_text_1921_mumbai__pure-skt.txt"],
    # Nimbarka
    ("nimbarka", "vedanta-parijata-saurabha"): ["sanskrit/_replaced/_pure_sanskrit/nimbarka_brahmasutra_3comm_vrindavan__pure-skt.txt"],
    # Vedanta-Desika
    ("vedanta-desika", "pancaratra-raksha"): ["sanskrit/_replaced/_pure_sanskrit/vedanta_desika_pancaratra_raksha_adyar__pure-skt.txt"],
    ("vedanta-desika", "tattva-mukta-kalapa"): ["sanskrit/_replaced/vedanta_desika_tattva_mukta_kalapa_archive_djvu.txt"],
    # Raghavendra
    ("raghavendra", "nyaya-sudha-parimala"): [
        "sanskrit/_replaced/_pure_sanskrit/raghavendra_nyaya_sudha_parimala_ad1_krishnacharya_1895__pure-skt.txt",
        "sanskrit/_replaced/_pure_sanskrit/raghavendra_nyaya_sudha_parimala_ad2_krishnacharya_1895__pure-skt.txt",
        "sanskrit/_replaced/_pure_sanskrit/raghavendra_nyaya_sudha_parimala_ad3_krishnacharya_1895__pure-skt.txt",
        "sanskrit/_replaced/_pure_sanskrit/raghavendra_nyaya_sudha_parimala_ad4_krishnacharya_1895__pure-skt.txt",
    ],
    ("raghavendra", "tantra-dipika"): ["sanskrit/_replaced/_pure_sanskrit/tantra_dipika_raghavendra__pure-skt.txt"],
    # Caitanya/Gaudiya
    ("jiva-gosvami", "sat-sandarbha"): ["sanskrit/caitanya_gaudiya/jiva_sat_sandarbha.txt"],
    ("jiva", "sat-sandarbha"): ["sanskrit/caitanya_gaudiya/jiva_sat_sandarbha.txt"],
    ("rupa-gosvami", "bhakti-rasamrta-sindhu"): ["sanskrit/caitanya_gaudiya/rupa_bhakti_rasamrta_sindhu.txt"],
    ("rupa", "bhakti-rasamrta-sindhu"): ["sanskrit/caitanya_gaudiya/rupa_bhakti_rasamrta_sindhu.txt"],
    # Jayatirtha
    ("jayatirtha", "nyaya-sudha"): ["sanskrit/vedanta/jayatirtha_nyaya_sudha.txt"],
    # Kesava-Kasmiri
    ("kesava-kasmiri", "krama-dipika"): ["sanskrit/vedanta/full_corpus/kesava_kasmiri_kramadipika_gretil.txt"],
    # Madhyamaka / Yogacara comparators
    ("nagarjuna", "mula-madhyamaka-karika"): ["sanskrit/buddhist/nagarjuna_mula_madhyamaka_karika.txt"],
    ("nagarjuna", "vigraha-vyavartani"): ["sanskrit/buddhist/nagarjuna_vigraha_vyavartani.txt"],
    ("candrakirti", "madhyamakavatara"): ["sanskrit/buddhist/candrakirti_madhyamakavatara.txt"],
    ("dharmakirti", "pramana-varttika"): ["sanskrit/buddhist/dharmakirti_pramana_varttika.txt"],
    ("vasubandhu", "trimsika"): ["sanskrit/buddhist/vasubandhu_trimsika.txt"],
    ("vasubandhu", "vimsatika"): ["sanskrit/buddhist/vasubandhu_vimsatika.txt"],
}

# Some thinker IDs in citation_index don't appear in their canonical Sanskrit
# romanization in filenames; map id → file-name fragments to broaden scoring.
THINKER_NAME_ALIASES: Dict[str, List[str]] = {
    "sankara": ["sankara", "shankara", "saṅkara"],
    "sureshvara": ["sureshvara", "suresvara", "sureśvara"],
    "vimuktatman": ["vimuktatman", "ista", "iṣṭa"],
    "kesava-kasmiri": ["kesava", "keśava", "kasmiri", "kāśmīri"],
    "madhva": ["madhva", "anandatirtha", "purnaprajna"],
    "vidyaranya": ["vidyaranya", "vidyāraṇya"],
    "ramanuja": ["ramanuja", "rāmānuja"],
    "padmapada": ["padmapada", "padmapāda"],
    "prakasatman": ["prakasatman", "prakāśātman"],
    "sarvajnatman": ["sarvajnatman", "sarvajñātman", "sanksepa", "saṅkṣepa"],
    "jiva-gosvami": ["jiva", "jīva", "gosvami", "gosvāmin"],
    "rupa-gosvami": ["rupa", "rūpa"],
    "vedanta-desika": ["vedanta_desika", "vedānta-deśika"],
}


MAX_FILE_BYTES = 12 * 1024 * 1024  # 12 MB cap per file
MAX_TOTAL_MB = 200                 # site mirror size budget


def humanize_filename(stem: str) -> str:
    s = stem.replace("_", " ").replace("-", " ").strip()
    s = re.sub(r"\s+gretil$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+pure[\s-]+skt$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+archive\s+djvu$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+cwsa$", "", s, flags=re.IGNORECASE)
    return s.title() if s else stem


def guess_edition(text_head: str, path: Path) -> Optional[str]:
    head_low = text_head.lower()
    name_low = path.name.lower()
    if "gretil" in head_low or "gretil" in name_low:
        return "GRETIL (Göttingen)"
    if "cwsa" in head_low or "cwsa" in name_low:
        return "CWSA (Sri Aurobindo)"
    if "gutenberg" in head_low:
        return "Project Gutenberg"
    if "internet archive" in head_low or "archive.org" in head_low or "archive_djvu" in name_low:
        return "Internet Archive (djvu OCR)"
    if "_pure-skt" in name_low or "pure_sanskrit" in str(path):
        return "Internet Archive (curated extract)"
    if "wikisource" in head_low:
        return "Wikisource"
    return None


def guess_format(text_head: str) -> str:
    if re.search(r"\|\s*\w+_\d", text_head):
        return "text-with-locus-marker"
    if text_head.lstrip().startswith("#"):
        return "markdown"
    return "plain-text"


# Lines that are only non-letter glyphs (digits, punctuation, banner runs)
# are not titles — reject them so we fall back to a humanized filename.
_TITLE_BAD = re.compile(r"^[\W\d_]+$")


def extract_title(text_head: str, path: Path) -> str:
    fallback = humanize_filename(path.stem)
    for raw in text_head.splitlines()[:30]:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# ") and len(line) <= 120:
            return line.lstrip("# ").strip()
        if line.startswith(("//", "##", "<", "%", "|")):
            continue
        if _TITLE_BAD.match(line):
            continue
        letters = sum(1 for c in line if c.isalpha())
        if 5 <= len(line) <= 120 and letters >= 5:
            return line
    return fallback


def candidate_files() -> List[Path]:
    """All in-corpus text files we would consider mirroring."""
    out: List[Path] = []
    seen: Set[Path] = set()
    for fp in sorted(MATERIALS.rglob("*")):
        if not fp.is_file():
            continue
        if fp.name in SKIP_BASENAMES:
            continue
        if any(part in SKIP_DIR_PARTS for part in fp.parts):
            continue
        if fp.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if fp.stat().st_size > MAX_FILE_BYTES:
            continue
        out.append(fp)
        seen.add(fp)
    if PURE_SKT_DIR.is_dir():
        for fp in sorted(PURE_SKT_DIR.glob("*.txt")):
            if fp in seen or fp.name in SKIP_BASENAMES:
                continue
            if fp.stat().st_size > MAX_FILE_BYTES:
                continue
            out.append(fp)
            seen.add(fp)
    return out


def thinker_work_keys() -> List[Tuple[str, str]]:
    keys: Set[Tuple[str, str]] = set()
    if CITATION_INDEX.is_file():
        d = json.loads(CITATION_INDEX.read_text(encoding="utf-8"))
        for e in (d.get("entries") or {}).values():
            tid = e.get("thinker_id") or ""
            wid = e.get("work_id") or ""
            if tid and wid:
                keys.add((tid, wid))
    if THINKERS_DIR.is_dir():
        for tf in THINKERS_DIR.glob("*.json"):
            try:
                td = json.loads(tf.read_text(encoding="utf-8"))
            except Exception:
                continue
            tid = td.get("id") or tf.stem
            for w in td.get("engaged_works") or []:
                wid = w.get("work_id") or ""
                st = w.get("source_status") or ""
                if wid and st in ("clean-on-disk", "acceptable-on-disk"):
                    keys.add((tid, wid))
    return sorted(keys)


def normalize_token(s: str) -> str:
    return s.lower().replace("-", "_")


def score_file(path: Path, tid: str, wid: str) -> int:
    p = str(path).lower()
    score = 0
    aliases = THINKER_NAME_ALIASES.get(tid, [tid])
    if any(a.lower() in p for a in aliases):
        score += 3
    wid_norm = normalize_token(wid)
    if wid_norm in p:
        score += 6
    tokens = [t for t in wid_norm.split("_") if len(t) >= 4]
    for tk in tokens:
        if tk in p:
            score += 1
    if "gretil" in p:
        score += 1
    if "_pure-skt" in p or "pure_sanskrit" in p:
        score += 1
    if "archive_djvu" in p:
        score -= 1
    return score


def select_files() -> List[Tuple[Path, str, List[Tuple[str, str]]]]:
    """Return list of (source_path, dest_relpath, owners) tuples.

    `owners` is the list of (thinker_id, work_id) keys that each picked this
    file (used for manifest annotation + Open-in-Source-tab disambiguation).
    """
    candidates = candidate_files()
    selected: Dict[Path, Tuple[str, List[Tuple[str, str]]]] = {}

    def add(fp: Path, rel_out: str, owner: Optional[Tuple[str, str]]) -> bool:
        if fp in selected:
            _cur_rel, owners = selected[fp]
            if owner is not None and owner not in owners:
                owners.append(owner)
            return False
        selected[fp] = (rel_out, [owner] if owner is not None else [])
        return True

    def normalize_dest(rel: str) -> str:
        if "_replaced/_pure_sanskrit/" in rel:
            return rel.replace("_replaced/_pure_sanskrit/", "_pure_sanskrit/")
        if "_replaced/" in rel:
            return rel.replace("_replaced/", "_djvu/")
        return rel

    for rel in ALWAYS_INCLUDE:
        fp = MATERIALS / rel
        if fp.is_file():
            add(fp, rel, None)

    keys = thinker_work_keys()
    print(f"  citation+thinker keys: {len(keys)}")

    n_override = 0
    for tid, wid in keys:
        ov = WORK_OVERRIDES.get((tid, wid))
        if not ov:
            continue
        for rel in ov:
            if not rel.endswith((".txt", ".md")):
                continue
            fp = MATERIALS / rel
            if not fp.is_file():
                continue
            rel_out = normalize_dest(str(Path(rel)))
            if add(fp, rel_out, (tid, wid)):
                n_override += 1
    print(f"  override matches: {n_override}")

    for rel in ALWAYS_INCLUDE:
        fp = MATERIALS / rel
        if not fp.is_file():
            continue
        for tid, wid in keys:
            if (tid, wid) in WORK_OVERRIDES:
                continue
            if score_file(fp, tid, wid) >= 6:
                add(fp, rel, (tid, wid))

    n_heuristic = 0
    for tid, wid in keys:
        if (tid, wid) in WORK_OVERRIDES:
            continue
        best: Optional[Path] = None
        best_score = 0
        for fp in candidates:
            s = score_file(fp, tid, wid)
            if s > best_score:
                best_score = s
                best = fp
        if best is not None and best_score >= 5:
            rel = normalize_dest(str(best.relative_to(MATERIALS)))
            if add(best, rel, (tid, wid)):
                n_heuristic += 1
    print(f"  heuristic matches: {n_heuristic}")

    n_wave10 = 0
    if WAVE10_OCR.is_dir():
        for tid, wid in keys:
            if (tid, wid) in WORK_OVERRIDES:
                continue
            wid_slug = normalize_token(wid)
            tid_slug = normalize_token(tid)
            for sub in WAVE10_OCR.iterdir():
                if not sub.is_dir():
                    continue
                name = sub.name.lower()
                if wid_slug in name or any(
                    t in name for t in wid_slug.split("_") if len(t) >= 5
                ):
                    final_dir = sub / "_FINAL"
                    cand = list(final_dir.glob("*.txt")) if final_dir.is_dir() else []
                    if cand:
                        rel_out = f"sanskrit/_wave10/{tid_slug}__{wid_slug}.txt"
                        if add(cand[0], rel_out, (tid, wid)):
                            n_wave10 += 1
                            break
    print(f"  wave-10 fallback matches: {n_wave10}")

    return sorted(
        ((fp, rel, owners) for fp, (rel, owners) in selected.items()),
        key=lambda x: x[1],
    )


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def enforce_public_tier_only(plan: Iterable[Tuple[Path, str, List[Tuple[str, str]]]]) -> None:
    """Abort if any selected source is from the private `secondary_sources/`
    tier or otherwise outside the public primary tree. The site mirror is a
    public artifact (GitHub Pages); modern academic scholarship must never
    leak in. See docs/CORPUS_TWO_TIER_SPLIT.md."""
    materials_resolved = MATERIALS.resolve()
    secondary_resolved = (
        SECONDARY_TIER.resolve() if SECONDARY_TIER.exists() else None
    )
    leaks: List[str] = []
    for fp, _rel, _owners in plan:
        try:
            src = fp.resolve()
        except OSError:
            leaks.append(f"unresolvable source: {fp}")
            continue
        if secondary_resolved is not None and _is_under(src, secondary_resolved):
            leaks.append(f"secondary-tier leak: {fp}")
            continue
        # Wave-10 OCR output also lives outside MATERIALS but is approved.
        if WAVE10_OCR.exists() and _is_under(src, WAVE10_OCR.resolve()):
            continue
        if not _is_under(src, materials_resolved):
            leaks.append(f"non-public-tier source: {fp}")
    if leaks:
        msg = "\n  ".join(leaks)
        raise SystemExit(
            "build aborted: secondary-tier or non-public sources in plan:\n  "
            + msg
        )


def build_entry(src_fp: Path, rel_in_repo: Path, owners: List[Tuple[str, str]]) -> Dict[str, Any]:
    data = src_fp.read_bytes()
    try:
        text = data.decode("utf-8", errors="replace")
    except Exception:
        text = ""
    head = "\n".join(text.splitlines()[:30])
    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    parts = rel_in_repo.parts
    language = parts[0] if len(parts) >= 1 else "unknown"
    category = parts[1] if len(parts) >= 3 else None
    entry: Dict[str, Any] = {
        "path": str(rel_in_repo).replace("\\", "/"),
        "language": language,
        "category": category,
        "title": extract_title(head, src_fp),
        "size_bytes": len(data),
        "line_count": line_count,
        "edition": guess_edition(head, src_fp),
        "format": guess_format(head),
    }
    if owners:
        entry["thinker_id"] = owners[0][0]
        entry["work_id"] = owners[0][1]
        if len(owners) > 1:
            entry["additional_owners"] = [
                {"thinker_id": t, "work_id": w} for t, w in owners[1:]
            ]
    return entry


def main() -> None:
    if not MATERIALS.is_dir():
        raise SystemExit(f"materials directory not found: {MATERIALS}")
    plan = select_files()
    print(f"selected {len(plan)} files for site mirror")
    enforce_public_tier_only(plan)
    print("public-tier policy: OK (no secondary leaks)")

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    files: List[Dict[str, Any]] = []
    total_bytes = 0
    budget = MAX_TOTAL_MB * 1024 * 1024
    for src_fp, rel, owners in plan:
        rel_path = Path(rel)
        size = src_fp.stat().st_size
        if total_bytes + size > budget:
            print(f"  budget exceeded ({total_bytes/1e6:.1f} MB), stopping at {rel}")
            break
        dest = OUT_DIR / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_fp, dest)
        total_bytes += size
        files.append(build_entry(src_fp, rel_path, owners))

    manifest = {
        "version": 3,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": "data/sources/",
        "file_count": len(files),
        "note": (
            "Site-mirrored subset of the primary-text corpus. The full corpus "
            "(~8 GB) lives outside the repo at materials/primary_texts/; this "
            "manifest lists only the files shipped to GitHub Pages, which the "
            "Source tab fetches from data/sources/."
        ),
        "files": files,
    }
    MANIFEST_OUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"wrote {MANIFEST_OUT}  ({len(files)} files, {total_bytes/1e6:.1f} MB)")


if __name__ == "__main__":
    main()

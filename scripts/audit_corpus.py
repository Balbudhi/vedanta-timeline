#!/usr/bin/env python3
"""Corpus audit — Lane 4, 2026-05-19.

Runs four audits over `data/thinkers/*.json`, `data/full_translations/*.md`,
`data/sources/sanskrit/**`, and `data/ingested/` and writes punch-list
markdowns under `docs/`.

Audits:
    1. Thinker engaged_works completeness.
    2. CORPUS_EXPANSION_v2 vs current `data/thinkers/`.
    3. full_translations layer audit.
    4. External-source cross-reference vs prakriya inventory.

This script writes only to `docs/audit_*_2026-05-19.md`. It does not modify
any thinker JSON, translation MD, or source file.
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

# -----------------------------------------------------------------------------
# Paths

ROOT = Path(__file__).resolve().parent.parent
THINKERS_DIR = ROOT / "data" / "thinkers"
TRANSLATIONS_DIR = ROOT / "data" / "full_translations"
SOURCES_SANSKRIT_DIR = ROOT / "data" / "sources" / "sanskrit"
INGESTED_DIR = ROOT / "data" / "ingested"
DOCS_DIR = ROOT / "docs"

DATE_TAG = "2026-05-19"


# -----------------------------------------------------------------------------
# Helpers

def strip_json(fn: str) -> str:
    return fn[:-5] if fn.endswith(".json") else fn


def slugify(s: str) -> str:
    """Strip diacritics, lowercase, alnum + underscore. For loose matching."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def load_thinkers() -> dict[str, dict[str, Any]]:
    out = {}
    for fn in sorted(os.listdir(THINKERS_DIR)):
        if not fn.endswith(".json"):
            continue
        with open(THINKERS_DIR / fn) as f:
            out[fn] = json.load(f)
    return out


def list_sanskrit_sources() -> list[str]:
    if not SOURCES_SANSKRIT_DIR.is_dir():
        return []
    out = []
    for dirpath, _dirnames, filenames in os.walk(SOURCES_SANSKRIT_DIR):
        for fn in filenames:
            out.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))
    return out


def list_translations() -> list[str]:
    return sorted(f for f in os.listdir(TRANSLATIONS_DIR) if f.endswith(".md"))


def list_ingested() -> list[str]:
    if not INGESTED_DIR.is_dir():
        return []
    return sorted(os.listdir(INGESTED_DIR))


# -----------------------------------------------------------------------------
# Audit 1: Thinker engaged_works completeness


REQUIRED_TOP_FIELDS = [
    "id", "name", "name_iast", "school",
    "dates_low", "dates_high", "dates_tier",
    "engaged_works", "key_passages",
]

# In this corpus, the per-work field that records primary-text linkage is
# `source_status`, not `primary_text_status`. The stub-equivalent statuses are
# "primary-text-not-in-corpus" and "degraded-on-disk".
STUB_STATUSES = {"primary-text-not-in-corpus", "degraded-on-disk"}
ONDISK_STATUSES = {"clean-on-disk", "acceptable-on-disk"}


def audit1_engaged_works(
    thinkers: dict[str, dict[str, Any]],
    sanskrit_files: list[str],
    translations: list[str],
    ingested: list[str],
) -> str:
    """Return markdown body for audit 1."""

    sanskrit_slugs = [slugify(f) for f in sanskrit_files]
    translation_slugs = [slugify(t) for t in translations]
    ingested_slugs = [slugify(i) for i in ingested]

    no_ew: list[tuple[str, str, str, str]] = []      # (file, name, school, suggested_first_work)
    schema_problems: list[tuple[str, str]] = []      # (file, reason)
    no_primary_linkage: list[tuple[str, str, str, str]] = []  # (thinker, work, status, pathway)
    stub_works: list[tuple[str, str, str]] = []      # (thinker, work, status)

    # Suggested first work for empty engaged_works[] — manual seeds for figures
    # the corpus already knows but who entered without works because they are
    # Western philosophers, modern thinkers, etc.
    seed_suggestions = {
        "anirban": "Pranab-darshan / Anirvanian recorded talks (start)",
        "bergson": "L'Évolution créatrice (1907)",
        "deleuze": "Différence et répétition (1968)",
        "derrida": "De la grammatologie (1967)",
        "foucault": "Les mots et les choses (1966)",
        "gebser": "Ursprung und Gegenwart / The Ever-Present Origin (1949–53)",
        "leibniz": "Monadologie (1714)",
        "levinas": "Totalité et Infini (1961)",
        "mcgilchrist": "The Master and His Emissary (2009)",
        "medhananda": "Integral Yoga essays (Aurobindonian)",
        "prigogine": "Order Out of Chaos (Prigogine & Stengers, 1984)",
    }

    for fn, d in thinkers.items():
        tid = d.get("id") or strip_json(fn)

        # Schema-adjacent checks
        for field in REQUIRED_TOP_FIELDS:
            if field not in d:
                schema_problems.append((fn, f"missing field `{field}`"))
        if "dates_low" in d and not isinstance(d.get("dates_low"), (int, float)):
            schema_problems.append((fn, f"dates_low not numeric: {d.get('dates_low')!r}"))
        if "dates_high" in d and not isinstance(d.get("dates_high"), (int, float)):
            schema_problems.append((fn, f"dates_high not numeric: {d.get('dates_high')!r}"))

        ew = d.get("engaged_works") or []
        if not ew:
            seed = seed_suggestions.get(tid, "(none recommended — manual review)")
            no_ew.append((fn, d.get("name", "?"), d.get("school", "?"), seed))
            continue

        for w in ew:
            # Required engaged-work fields
            if not w.get("title_iast"):
                schema_problems.append((fn, f"engaged_work missing title_iast: {w.get('work_id', '?')}"))
            if not w.get("ascription_tier"):
                schema_problems.append((fn, f"engaged_work missing ascription_tier: {w.get('work_id', '?')}"))
            if "source_status" not in w:
                schema_problems.append((fn, f"engaged_work missing source_status: {w.get('work_id', '?')}"))

            status = w.get("source_status", "")
            work_iast = w.get("title_iast", w.get("title", w.get("work_id", "?")))
            work_slug = slugify(work_iast)

            if status in STUB_STATUSES:
                stub_works.append((tid, work_iast, status))

                # Cross-reference: any sanskrit/translation/ingested file
                # whose slug contains the work slug?
                has_sanskrit = any(work_slug in s for s in sanskrit_slugs) if work_slug else False
                has_translation = any(work_slug in s for s in translation_slugs) if work_slug else False
                has_ingested = any(work_slug in s for s in ingested_slugs) if work_slug else False

                if not (has_sanskrit or has_translation or has_ingested):
                    pathway = suggest_pathway(tid, work_iast)
                    no_primary_linkage.append((tid, work_iast, status, pathway))

    # Build markdown
    lines: list[str] = []
    lines.append(f"# Audit — Thinker `engaged_works` completeness ({DATE_TAG})")
    lines.append("")
    lines.append("Generated by `scripts/audit_corpus.py`. This is a punch-list, not an edit.")
    lines.append("")
    lines.append(f"**Thinkers audited:** {len(thinkers)}")
    lines.append(f"**Thinkers without `engaged_works[]`:** {len(no_ew)}")
    lines.append(f"**Engaged works flagged stub (status in {sorted(STUB_STATUSES)}):** {len(stub_works)}")
    lines.append(f"**Stub works with no primary-text / translation / ingested linkage:** {len(no_primary_linkage)}")
    lines.append(f"**Schema problems:** {len(schema_problems)}")
    lines.append("")

    lines.append("## §1. Thinkers with no `engaged_works[]`")
    lines.append("")
    if not no_ew:
        lines.append("_None._")
    else:
        lines.append("| file | name | school | suggested first work to add |")
        lines.append("|---|---|---|---|")
        for fn, name, school, seed in no_ew:
            lines.append(f"| `{fn}` | {name} | {school} | {seed} |")
    lines.append("")

    lines.append("## §2. Engaged works with no primary-text linkage")
    lines.append("")
    lines.append("Stub engaged works (source_status = `primary-text-not-in-corpus` or `degraded-on-disk`) where loose slug-matching finds *no* file in `data/sources/sanskrit/`, `data/full_translations/`, or `data/ingested/`. Acquisition-pathway suggestion is drawn from `docs/ACQUISITION_PATHWAYS.md` (§A priority-12, §B categorial baskets).")
    lines.append("")
    if not no_primary_linkage:
        lines.append("_None._")
    else:
        lines.append("| thinker_id | work_iast | status | suggested acquisition pathway |")
        lines.append("|---|---|---|---|")
        for tid, work, status, pathway in sorted(no_primary_linkage):
            lines.append(f"| `{tid}` | {work} | `{status}` | {pathway} |")
    lines.append("")

    lines.append("## §3. Engaged works marked stub (full list)")
    lines.append("")
    lines.append("All entries with `source_status` in the stub set, regardless of whether linkage was found.")
    lines.append("")
    if not stub_works:
        lines.append("_None._")
    else:
        # Group by thinker for compactness
        by_thinker: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for tid, work, status in stub_works:
            by_thinker[tid].append((work, status))
        for tid in sorted(by_thinker):
            lines.append(f"### `{tid}` ({len(by_thinker[tid])})")
            lines.append("")
            for work, status in by_thinker[tid]:
                lines.append(f"- {work} — `{status}`")
            lines.append("")

    lines.append("## §4. Schema-adjacent problems")
    lines.append("")
    if not schema_problems:
        lines.append("_None._")
    else:
        by_file: dict[str, list[str]] = defaultdict(list)
        for fn, reason in schema_problems:
            by_file[fn].append(reason)
        for fn in sorted(by_file):
            lines.append(f"### `{fn}`")
            for r in by_file[fn]:
                lines.append(f"- {r}")
            lines.append("")

    return "\n".join(lines) + "\n"


def suggest_pathway(thinker_id: str, work_iast: str) -> str:
    """Rough mapping from thinker/work to ACQUISITION_PATHWAYS §A or §B basket."""
    w = work_iast.lower()
    t = thinker_id.lower()

    # §A priority-12
    if "govinda-bhāṣya" in w or "govinda-bhashya" in w:
        return "§A.1 archive.org `GovindaBhasya.KrsnadasBaba`"
    if t == "bhaskara" and "brahma" in w:
        return "§A.2 archive.org Chowkhamba 1903–1915 PDF"
    if t == "citsukha" or "tattva-pradīpikā" in w or "citsukhī" in w:
        return "§A.3 archive.org Nirṇayasāgara 1931"
    if t == "jayatirtha" and "prakāśik" in w:
        return "§A.4 archive.org `tattva-prakasika`"
    if t == "madhusudana" and ("gūḍhārtha" in w or "gudhartha" in w):
        return "§A.5 archive.org `tDyP_bhagavad-gita-with-gudharth-deepika-...`"
    if t == "madhva" and "gītā-bhāṣya" in w:
        return "§A.6 Madhwapracharavedike Sarvamūla index"
    if t == "madhva" and "tātparya-nirṇaya" in w:
        return "§A.7 archive.org `gitatatparya-nirnaya-...-d-prahladachar` (1987)"
    if t == "madhva" and "nyāya-vivaraṇa" in w:
        return "§A.8 Sarvamūla Sūtra-Prasthānam volume; archive.org via Madhwapracharavedike"
    if t == "sureshvara" and "bṛhadāraṇyaka" in w:
        return "§A.9 archive.org `BrihadaranyakaBhashyaVartikam2`"
    if t == "sureshvara" and "taittirīya" in w:
        return "§A.10 archive.org `gOtp_taitiriya-upanishad-bhashya-vartika-...`"
    if t == "vedanta-desika" and "śatadūṣaṇī" in w:
        return "§A.11 Chaukhamba Dwivedi ed. (print purchase)"
    if t == "vidyaranya" and "vivaraṇa-prameya" in w:
        return "§A.12 archive.org `fzFh_vivarana-prameya-sangraha-...-2005`"

    # §B baskets by school / lineage
    school_hint = ""
    if t in {"madhva", "jayatirtha", "vyasatirtha", "raghavendra", "narayana-panditacarya",
             "narahari-tirtha", "padmanabha-tirtha", "trivikrama-pandita", "vijayindra",
             "aksobhya-tirtha", "vallabha-balaka", "purusottama", "bannanje"}:
        return "§B.1 / §B.2 — Madhwapracharavedike Sarvamūla index; PPSM Bangalore"
    if t in {"manavala-mamunigal", "pillai-lokacarya", "periyavaccan-pillai", "vedanta-desika",
             "rangaramanuja-muni", "sudarsana", "nathamuni", "yamuna", "uttamur-viraraghavacharya"}:
        return "§B.3 EFEO Pondicherry / Sripedia / Adyar Library Series"
    if t in {"pancaratra-tradition"}:
        return "§B.4 Adyar Library Pāñcarātra editions on archive.org"
    if t in {"abhinavagupta", "ksemaraja", "utpaladeva", "somananda", "vasugupta", "jayaratha",
             "bhatta-kallata", "bhatta-ramakantha", "mahesvarananda", "malini-vijaya-tantra"}:
        return "§B.5 Muktabodha KSTS digital library / eGangotri KSTS listing"
    if t in {"sadyojyotis", "kaundinya", "lakulisha"}:
        return "§B.6 / §B.8 IFP-Pondichéry / Muktabodha Śaiva-Siddhānta bundle"
    if t in {"bhaskararaya", "lakshmidhara"}:
        return "§B.7 Adyar / Sampurnanand Śrīvidyā catalogue"
    if t in {"caitanya", "jiva-gosvami", "rupa-gosvami", "sanatana-gosvami", "kavi-karnapura",
             "kesava-kasmiri", "baladeva", "visvanatha", "vitthalanatha", "bhaktivinoda",
             "bhaktisiddhanta", "hariraya", "ramabhadracarya"}:
        return "§B.9 archive.org `vidyabhusanaproject` / BBT / VRI"
    if t in {"vimuktatman", "anandabodha", "sarvajnatman", "appayya", "dharmaraja",
             "brahmananda", "brahmananda-saraswati", "vidyaranya", "mandana", "prakasatman",
             "satchidanandendra", "anantakrishna-sastri", "karpatri",
             "candrasekhara-bharati", "totaka", "padmapada", "hastamalaka"}:
        return "§B.10 Ambuda + Sringeri publication catalogue"

    return "(no §A/§B match; manual evaluation needed)"


# -----------------------------------------------------------------------------
# Audit 2: CORPUS_EXPANSION_v2 punch-list


# Hand-extracted from docs/CORPUS_EXPANSION_v2.md Section A summary table.
# (proposed_id, name_iast, school, dates_low, dates_high, priority,
#  engaged_works_candidates)
V2_NEW_THINKERS: list[dict[str, Any]] = [
    {
        "proposed_id": "aurobindo",
        "name_iast": "Śrī Aravinda",
        "school": "Advaita (Pūrṇa-Advaita / Integral Vedānta)",
        "dates_low": 1872,
        "dates_high": 1950,
        "priority": "must-add",
        "engaged_works": [
            "The Life Divine", "Essays on the Gītā", "The Synthesis of Yoga",
            "The Secret of the Veda + Hymns to the Mystic Fire",
            "Īśopaniṣad commentary", "Kena Upaniṣad commentary",
            "Eight Upaniṣads", "Savitri",
        ],
    },
    {
        "proposed_id": "rambhadracharya",
        "name_iast": "Jagadguru Rāmabhadrācārya",
        "school": "Viśiṣṭādvaita (Rāmānanda-Sampradāya)",
        "dates_low": 1950, "dates_high": 0,
        "priority": "must-add (the blind ācārya)",
        "engaged_works": [
            "Śrīrāghavakṛpā-Bhāṣyam on Brahma-Sūtra",
            "Śrīrāghavakṛpā-Bhāṣyam on Bhagavad-Gītā",
            "Śrīrāghavakṛpā-Bhāṣyam on the Eleven Principal Upaniṣads",
            "Śrīrāghavakṛpā-Bhāṣyam on Nārada-Bhakti-Sūtra",
            "Aṣṭādhyāyī-Pradīpa",
        ],
    },
    {
        "proposed_id": "uttamur-viraraghavacharya",
        "name_iast": "Uttamūr Vīrarāghavācārya",
        "school": "Viśiṣṭādvaita (Vaḍakalai modern)",
        "dates_low": 1897, "dates_high": 1983,
        "priority": "must-add",
        "engaged_works": [
            "Paramārtha-Bhūṣaṇa", "Śrī-Bhāṣyārtha-Darpaṇa",
            "Sarvārtha-Siddhi-Vyākhyā", "Nyāya-Pariśuddhi-Vyākhyā",
            "Vaiśeṣika-Rasāyana", "Mīmāṃsā-Nyāya-Prakāśa-Vyākhyā",
            "Prabandha-Rakṣā",
        ],
    },
    {
        "proposed_id": "rangaramanuja",
        "name_iast": "Raṅgarāmānuja Muni",
        "school": "Viśiṣṭādvaita (Vaḍakalai Upaniṣad-bhāṣya)",
        "dates_low": 1550, "dates_high": 1650,
        "priority": "must-add",
        "engaged_works": [
            "Sanskrit bhāṣyas on twelve principal Upaniṣads",
            "Viṣaya-Vākya-Dīpikā", "Śruta-Prakāśikā-Bhāva-Prakāśikā",
            "Śārīraka-Śāstra-Dīpikā", "Siddhānta-Sāra",
        ],
    },
    {
        "proposed_id": "anantakrishna-sastri",
        "name_iast": "Anantakṛṣṇa Śāstrī",
        "school": "Advaita (Vivaraṇa modern editorial)",
        "dates_low": 1886, "dates_high": 1962,
        "priority": "must-add",
        "engaged_works": [
            "Śatabhūṣaṇī", "Advaita-Tattva-Sudhā", "Advaita-Dīpikā",
            "Vedānta-Rakṣā-Maṇi",
            "Crit. ed. of Advaita-Siddhi / Nyāyāmṛta",
            "Crit. ed. of Vedānta-Paribhāṣā",
        ],
    },
    {
        "proposed_id": "satchidanandendra",
        "name_iast": "Saccidānandendra Sarasvatī",
        "school": "Advaita (Śuddha-Śāṅkara-Prakriyā)",
        "dates_low": 1880, "dates_high": 1975,
        "priority": "must-add",
        "engaged_works": [
            "Mūlāvidyā-Nirāsa", "Vedānta-Prakriyā-Pratyabhijñā",
            "Śuddha-Śāṅkara-Prakriyā-Bhāskara",
            "Māṇḍūkya-Rahasya-Vivṛti",
            "Salient Features of Śaṅkara-Vedānta",
        ],
    },
    {
        "proposed_id": "bannanje-govindacharya",
        "name_iast": "Bannañje Govindācārya",
        "school": "Dvaita (Tattvavāda modern)",
        "dates_low": 1936, "dates_high": 2020,
        "priority": "must-add",
        "engaged_works": [
            "Critical edition of Madhva's Sarva-Mūla-Granthāḥ",
            "Mahābhārata-Tātparya-Nirṇaya vyākhyāna",
            "Bhāgavata vyākhyāna",
            "Upaniṣad-Bhāṣyas (Mādhva)",
            "Ācārya Madhva: Baḍuku-Bareha",
            "Stuti-Candrikā",
        ],
    },
    {
        "proposed_id": "bhaktisiddhanta",
        "name_iast": "Bhaktisiddhānta Sarasvatī",
        "school": "Acintya-Bhedābheda (Gauḍīya Maṭha)",
        "dates_low": 1874, "dates_high": 1937,
        "priority": "must-add",
        "engaged_works": [
            "Anubhāṣya on Caitanya-Caritāmṛta",
            "Bhāgavata commentary",
            "Brahma-Saṃhitā commentary",
            "Vaiṣṇava-Siddhānta-Mālā",
            "Editions of Gosvāmin corpus",
        ],
    },
    {
        "proposed_id": "karpatri",
        "name_iast": "Svāmī Karpātrī",
        "school": "Advaita (Daśanāmī-Sarasvatī revivalism)",
        "dates_low": 1907, "dates_high": 1982,
        "priority": "should-add",
        "engaged_works": [
            "Vedārtha-Pārijāta", "Vedānta-Mīmāṃsā (series)",
            "Saṅkīrtana-Mīmāṃsā", "Varṇāśrama-Maryādā",
            "Mārksavāda aur Rāmarājya",
        ],
    },
    {
        "proposed_id": "chandrashekhara-bharati",
        "name_iast": "Candraśekhara Bhāratī III",
        "school": "Advaita (Śṛṅgerī-paṭṭa)",
        "dates_low": 1892, "dates_high": 1954,
        "priority": "should-add",
        "engaged_works": [
            "Sanskrit commentary on Vivekacūḍāmaṇi",
            "Gururāja-Sūkti-Mālikā",
            "Recorded discourses",
        ],
    },
]


# Hand-extracted Section B augmentations: thinker_id → list of recommended
# additional work titles.
V2_SECTION_B: dict[str, list[str]] = {
    "caitanya": ["Rāmānanda-Saṃvāda", "Daśa-Mūla-Śikṣā"],
    "madhva": [
        "Ṛg-Bhāṣya",
        "Aitareya-Upaniṣad-Bhāṣya",
        "Chāndogya-Upaniṣad-Bhāṣya",
        "Daśa-Prakaraṇa bundle (Kathā-Lakṣaṇa, Pramāṇa-Lakṣaṇa, Karma-Nirṇaya, Tattva-Saṅkhyāna, Tattva-Viveka, Sad-Ācāra-Smṛti)",
    ],
    "nimbarka": ["Kṛṣṇa-Stava-Rāja", "Mantra-Rahasya-Ṣoḍaśī"],
    "vallabha": ["Ṣoḍaśa-Granthāḥ (16 sub-works) — bundle or split"],
    "vidyaranya": ["Anubhūti-Prakāśa"],
    "madhusudana": [
        "Vedānta-Kalpa-Latikā", "Prasthāna-Bheda",
        "Saṃkṣepa-Śārīraka-Sāra-Saṃgraha",
    ],
    "appayya": ["Naya-Mañjarī", "Catur-Mata-Sāra-Saṃgraha"],
    "vedanta-desika": ["Split Tattva-Muktā-Kalāpa / Sarvārtha-Siddhi into separate work-entries"],
    "vyasatirtha": ["Bhedojjīvana"],
    "manavala-mamunigal": [
        "Mumukṣuppaḍi-Vyākhyāna",
        "Tattva-Trayam-Vyākhyāna",
        "Śrī-Vacana-Bhūṣaṇa-Vyākhyāna",
    ],
}


def audit2_v2_punch_list(thinkers: dict[str, dict[str, Any]]) -> str:
    existing_ids = {d.get("id") or strip_json(fn) for fn, d in thinkers.items()}

    missing_thinkers = [v for v in V2_NEW_THINKERS if v["proposed_id"] not in existing_ids]
    existing_v2 = [v for v in V2_NEW_THINKERS if v["proposed_id"] in existing_ids]

    # Section B deltas — compute against existing engaged_works[]
    section_b_deltas: list[tuple[str, int, list[str]]] = []
    for tid, recommended in V2_SECTION_B.items():
        # find the thinker file for tid (some IDs use a different filename)
        candidates = [fn for fn, d in thinkers.items() if (d.get("id") == tid or strip_json(fn) == tid)]
        if not candidates:
            section_b_deltas.append((tid, -1, recommended))  # -1 = thinker missing
            continue
        d = thinkers[candidates[0]]
        ew = d.get("engaged_works") or []
        existing_titles = set()
        for w in ew:
            for k in ("title_iast", "title"):
                v = w.get(k)
                if v:
                    existing_titles.add(slugify(v))
            for at in w.get("alternate_titles") or []:
                existing_titles.add(slugify(at))
        missing_recs = []
        for rec in recommended:
            rec_slug = slugify(rec.split(" — ")[0].split(" (")[0])
            if not any(rec_slug and rec_slug in t for t in existing_titles):
                missing_recs.append(rec)
        if missing_recs:
            section_b_deltas.append((tid, len(ew), missing_recs))

    lines: list[str] = []
    lines.append(f"# Audit — CORPUS_EXPANSION_v2 punch-list ({DATE_TAG})")
    lines.append("")
    lines.append("Generated by `scripts/audit_corpus.py`. Source: `docs/CORPUS_EXPANSION_v2.md` Section A (new thinkers) and Section B (existing-thinker augmentations).")
    lines.append("")
    lines.append(f"**v2 new-thinker proposals:** {len(V2_NEW_THINKERS)}")
    lines.append(f"**…of which still missing from `data/thinkers/`:** {len(missing_thinkers)}")
    lines.append(f"**…of which already authored (delta vs v2 candidates below):** {len(existing_v2)}")
    lines.append(f"**Section B augmentation deltas open:** {len(section_b_deltas)}")
    lines.append("")

    lines.append("## §A. New thinkers named in v2 not yet present as `data/thinkers/<id>.json`")
    lines.append("")
    if not missing_thinkers:
        lines.append("_All v2 Section-A thinkers are present (by `proposed_id`)._")
    else:
        lines.append("This is the to-author list for a future authoring pass.")
        lines.append("")
        for v in missing_thinkers:
            lines.append(f"### `{v['proposed_id']}` — {v['name_iast']}")
            lines.append("")
            lines.append(f"- **school**: {v['school']}")
            lines.append(f"- **dates_low / dates_high**: {v['dates_low']} / {v['dates_high']}")
            lines.append(f"- **priority**: {v['priority']}")
            lines.append("- **engaged_works[] candidates:**")
            for w in v["engaged_works"]:
                lines.append(f"  - {w}")
            lines.append("")

    lines.append("## §A.bis. v2 Section-A candidates already authored")
    lines.append("")
    lines.append("Confirm later-pass review that the existing JSON's `engaged_works[]` matches the v2 list.")
    lines.append("")
    if not existing_v2:
        lines.append("_None._")
    else:
        for v in existing_v2:
            tid = v["proposed_id"]
            cand_files = [fn for fn, d in thinkers.items() if (d.get("id") == tid or strip_json(fn) == tid)]
            fn = cand_files[0] if cand_files else "?"
            d = thinkers.get(fn, {})
            ew_count = len(d.get("engaged_works") or [])
            lines.append(f"- `{tid}` — file `{fn}` — existing engaged_works: {ew_count} — v2 recommended: {len(v['engaged_works'])}")
    lines.append("")

    lines.append("## §B. Section-B deltas — existing thinkers missing v2-recommended works")
    lines.append("")
    if not section_b_deltas:
        lines.append("_None._")
    else:
        lines.append("| thinker_id | existing works | v2-recommended works missing |")
        lines.append("|---|---|---|")
        for tid, n, missing in section_b_deltas:
            n_str = str(n) if n >= 0 else "(thinker missing)"
            missing_str = "; ".join(missing)
            lines.append(f"| `{tid}` | {n_str} | {missing_str} |")
    lines.append("")

    return "\n".join(lines) + "\n"


# -----------------------------------------------------------------------------
# Audit 3: full_translations layer audit


# Devanāgarī range U+0900–U+097F; extended U+A8E0–U+A8FF
DEVANAGARI_RE = re.compile(r"[ऀ-ॿ꣠-ꣿ]")
IAST_DIACRITICS_RE = re.compile(r"[āīūṛṝḷḹṅñṭḍṇśṣḥṃĀĪŪṚṜḶḸṄÑṬḌṆŚṢḤṂ]")
# English: any ASCII paragraph of >=80 chars without devanāgarī
ENGLISH_PARA_RE = re.compile(r"(?m)^[A-Za-z][^\n]{80,}$")
COMMENTARY_RE = re.compile(
    r"(?i)("
    r"Śaṅkara comments|Bhāmatī|Vivaraṇa|"
    r"\[CITATION:|"
    r"commentary of|"
    r"gloss(?:es)? (?:of|on|by)|"
    r"sub-commentary|"
    r"Padmapāda|Vācaspati|Sureśvara|Madhusūdana|"
    r"Rāmānuja|Vedānta-Deśika|Sudarśana|"
    r"Madhva|Jayatīrtha|Vyāsatīrtha|Raghavendra|"
    r"Anandagiri|Govindānanda|Brahmānanda|"
    r"Prakāśātman|Maṇḍana|"
    r"Bhāskara|Nimbārka|Vallabha|Baladeva|"
    r"Tattvabodhinī|Subodhinī|Bhāva-Dīpa|Tātparya-Candrikā|"
    r"Jīva Gosvām|Viśvanātha|"
    r"Kṛṣṇadāsa Kavirāja"
    r")"
)
STUB_MARKER_RE = re.compile(r"(?i)\b(TODO|STUB|PLACEHOLDER|honest[- ]acknowledgment[- ]stub|acquisition queue|not currently in our corpus|placeholder)\b")


def audit3_translations(translations: list[str]) -> str:
    short_files: list[tuple[str, int]] = []
    stub_files: list[tuple[str, str]] = []
    missing_devanagari: list[str] = []
    missing_iast: list[str] = []
    missing_english: list[str] = []
    missing_commentary: list[str] = []
    ok_files: list[str] = []

    for fn in translations:
        path = TRANSLATIONS_DIR / fn
        text = path.read_text(encoding="utf-8", errors="replace")
        size = path.stat().st_size

        if size < 1024:
            short_files.append((fn, size))

        m = STUB_MARKER_RE.search(text)
        if m:
            # Capture a short snippet
            snippet = m.group(0)
            stub_files.append((fn, snippet))

        has_deva = bool(DEVANAGARI_RE.search(text))
        has_iast = bool(IAST_DIACRITICS_RE.search(text))
        has_en = bool(ENGLISH_PARA_RE.search(text))
        has_comm = bool(COMMENTARY_RE.search(text))

        if not has_deva:
            missing_devanagari.append(fn)
        if not has_iast:
            missing_iast.append(fn)
        if not has_en:
            missing_english.append(fn)
        if not has_comm:
            missing_commentary.append(fn)

        if has_deva and has_iast and has_en and has_comm and size >= 1024 and not m:
            ok_files.append(fn)

    lines: list[str] = []
    lines.append(f"# Audit — `data/full_translations/` layer completeness ({DATE_TAG})")
    lines.append("")
    lines.append("Generated by `scripts/audit_corpus.py`. Heuristic checks: ≥1 Devanāgarī block, ≥1 IAST block, ≥1 long English paragraph, ≥1 commentator citation, ≥1 KB.")
    lines.append("")
    lines.append(f"**Translations audited:** {len(translations)}")
    lines.append(f"**Files passing all checks:** {len(ok_files)}")
    lines.append(f"**Stub-marker hits:** {len(stub_files)}")
    lines.append(f"**Suspiciously short (<1 KB):** {len(short_files)}")
    lines.append(f"**Missing Devanāgarī layer:** {len(missing_devanagari)}")
    lines.append(f"**Missing IAST layer:** {len(missing_iast)}")
    lines.append(f"**Missing English paragraph:** {len(missing_english)}")
    lines.append(f"**Missing commentary reference:** {len(missing_commentary)}")
    lines.append("")

    def section(title: str, items: list[Any]) -> None:
        lines.append(f"## {title}")
        lines.append("")
        if not items:
            lines.append("_None._")
        else:
            for it in items:
                if isinstance(it, tuple):
                    a, b = it
                    lines.append(f"- `{a}` — {b}")
                else:
                    lines.append(f"- `{it}`")
        lines.append("")

    section("§1. Stub markers / honest-acknowledgment-stub files", stub_files)
    section("§2. Suspiciously short (<1 KB)", short_files)
    section("§3. Missing Devanāgarī layer", missing_devanagari)
    section("§4. Missing IAST layer", missing_iast)
    section("§5. Missing English paragraph", missing_english)
    section("§6. Missing commentary reference", missing_commentary)
    section("§7. Files passing all checks (clean)", ok_files)

    return "\n".join(lines) + "\n"


# -----------------------------------------------------------------------------
# Audit 4: External-source cross-reference


# Hand-curated map from texts named in CORPUS_PLAN.md / CORPUS_EXPANSION_v2.md
# but absent from data/sources/sanskrit/, to free-URL external sources known to
# host them (verified from ACQUISITION_PATHWAYS.md and prakriya inventory §3).
EXTERNAL_FOLLOWUP_CANDIDATES = [
    # (thinker_id, work_iast, external_source, url, format, lane2_action)
    ("baladeva", "Govinda-Bhāṣya", "archive_org",
     "https://archive.org/details/GovindaBhasya.KrsnadasBaba", "pdf", "fetch"),
    ("bhaskara", "Brahma-Sūtra-Bhāṣya", "archive_org",
     "https://archive.org/details/BrahmaSutraBhashyaOfBhaskarNos.70185209Year1915ChowkhambaSanskritSeries",
     "pdf", "fetch"),
    ("citsukha", "Tattva-Pradīpikā", "archive_org",
     "https://archive.org/details/SKEw_tattva-pradipika-chitsukhi-of-chitsukhacharya-with-commentary-nayana-prasadini-b",
     "pdf", "fetch"),
    ("jayatirtha", "Tattva-Prakāśikā", "archive_org",
     "https://archive.org/details/tattva-prakasika", "pdf", "fetch (verify edition)"),
    ("madhusudana", "Gūḍhārtha-Dīpikā", "archive_org",
     "https://archive.org/details/tDyP_bhagavad-gita-with-gudharth-deepika-by-madhusudan-sarasvati-translated-by-swami-",
     "pdf", "fetch"),
    ("madhva", "Gītā-Bhāṣya", "archive_org",
     "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books", "pdf", "fetch (Sarvamūla Prasthāna-trayī volume)"),
    ("madhva", "Gītā-Tātparya-Nirṇaya", "archive_org",
     "https://archive.org/details/anandatirthabhagavatpadacharyavirachitahgitatatparyanirnayaheditedbydprahladachar1987",
     "pdf", "fetch"),
    ("madhva", "Nyāya-Vivaraṇa", "archive_org",
     "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books", "pdf", "fetch (Sarvamūla Sūtra-Prasthānam volume)"),
    ("sureshvara", "Bṛhadāraṇyaka-Bhāṣya-Vārttika", "archive_org",
     "https://archive.org/details/BrihadaranyakaBhashyaVartikam2", "pdf", "fetch"),
    ("sureshvara", "Taittirīya-Bhāṣya-Vārttika", "archive_org",
     "https://archive.org/details/gOtp_taitiriya-upanishad-bhashya-vartika-by-sureshvara-acharya-1889-anand-ashram-press",
     "pdf", "fetch"),
    ("vidyaranya", "Vivaraṇa-Prameya-Saṅgraha", "archive_org",
     "https://archive.org/details/fzFh_vivarana-prameya-sangraha-by-vidyaranya-muni-edited-by-parasa-nath-dvivedi-2005-",
     "pdf", "fetch (replace existing 1893 degraded copy)"),

    # §B baskets — illustrative high-leverage entries.
    ("madhva", "Sarva-Mūla-Granthāḥ (full set)", "archive_org",
     "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books", "pdf",
     "manifest_only — batch download nine volumes"),
    ("abhinavagupta", "Tantrāloka (KSTS series)", "archive_org",
     "https://archive.org/details/in.ernet.dli.2015.281055", "pdf", "fetch"),
    ("ksemaraja", "Pratyabhijñā-Hṛdaya + Spanda-Nirṇaya (KSTS)", "muktabodha",
     "https://muktabodha.org/digital_library.htm", "etext+pdf",
     "manifest_only — Muktabodha registration"),
    ("kaundinya", "Pañcārtha-Bhāṣya", "archive_org",
     "https://archive.org/details/EHYo_pashupata-sutra-bhagavatpad-shri-kaundinya", "pdf", "fetch"),
    ("vedanta-desika", "Śatadūṣaṇī", "sanskritdocuments",
     "https://ibiblio.org/sripedia/ebooks/vdesikan/works.html", "pdf-or-itx",
     "manifest_only — hand-check Sripedia index"),
    ("appayya", "Catur-Mata-Sāra-Saṃgraha", "archive_org",
     "https://archive.org/", "pdf", "manifest_only — locate edition"),
    ("dharmaraja", "Vedānta-Paribhāṣā (Anantakṛṣṇa Śāstrī ed.)", "archive_org",
     "https://archive.org/details/dli.ernet.383732", "pdf", "fetch"),
    ("manavala-mamunigal", "Mumukṣuppaḍi-Vyākhyāna (et al.)", "sanskritdocuments",
     "https://ibiblio.org/sripedia/", "pdf-or-itx", "manifest_only"),
    ("pancaratra-tradition", "Ahirbudhnya-Saṃhitā", "archive_org",
     "https://archive.org/details/AhirbudhnyaSamhitaSanskritAdyar", "pdf", "fetch"),
    ("vidyaranya", "Anubhūti-Prakāśa", "gretil",
     "https://gretil.sub.uni-goettingen.de/gretil.html", "plain",
     "manifest_only — locate on GRETIL index"),
]


def audit4_external(thinkers: dict[str, dict[str, Any]], sanskrit_files: list[str]) -> str:
    sanskrit_slugs = [slugify(f) for f in sanskrit_files]

    relevant: list[tuple[str, str, str, str, str, str]] = []
    for tid, work, src, url, fmt, action in EXTERNAL_FOLLOWUP_CANDIDATES:
        work_slug = slugify(work)
        already_on_disk = any(work_slug and work_slug in s for s in sanskrit_slugs)
        if already_on_disk:
            continue
        relevant.append((tid, work, src, url, fmt, action))

    lines: list[str] = []
    lines.append(f"# Audit — External-source follow-up for Lane 2 ({DATE_TAG})")
    lines.append("")
    lines.append("Generated by `scripts/audit_corpus.py`. Texts referenced as primaries in `docs/CORPUS_PLAN.md` / `docs/CORPUS_EXPANSION_v2.md` that are *not* in `data/sources/sanskrit/` but are reachable from a free URL named in `docs/ACQUISITION_PATHWAYS.md` or in the prakriya inventory (§3 external sources).")
    lines.append("")
    lines.append(f"**Candidates:** {len(relevant)} (deduplicated against on-disk slug match)")
    lines.append("")
    lines.append("Feeds back into Lane 2's next pass.")
    lines.append("")

    for tid, work, src, url, fmt, action in relevant:
        lines.append(f"- `{tid}` / *{work}*")
        lines.append(f"  - external_source: {src}")
        lines.append(f"  - url: {url}")
        lines.append(f"  - format: {fmt}")
        lines.append(f"  - recommended_lane2_action: {action}")

    lines.append("")
    return "\n".join(lines) + "\n"


# -----------------------------------------------------------------------------
# Main


def main() -> None:
    thinkers = load_thinkers()
    sanskrit_files = list_sanskrit_sources()
    translations = list_translations()
    ingested = list_ingested()

    DOCS_DIR.mkdir(exist_ok=True)

    out1 = audit1_engaged_works(thinkers, sanskrit_files, translations, ingested)
    out2 = audit2_v2_punch_list(thinkers)
    out3 = audit3_translations(translations)
    out4 = audit4_external(thinkers, sanskrit_files)

    (DOCS_DIR / f"audit_thinker_engaged_works_{DATE_TAG}.md").write_text(out1)
    (DOCS_DIR / f"audit_corpus_expansion_v2_punch_list_{DATE_TAG}.md").write_text(out2)
    (DOCS_DIR / f"audit_full_translations_{DATE_TAG}.md").write_text(out3)
    (DOCS_DIR / f"audit_external_source_followup_{DATE_TAG}.md").write_text(out4)

    print(f"thinkers audited: {len(thinkers)}")
    print(f"sanskrit source files: {len(sanskrit_files)}")
    print(f"full_translations files: {len(translations)}")
    print(f"ingested entries: {len(ingested)}")
    print()
    print("Wrote:")
    for fn in (
        f"audit_thinker_engaged_works_{DATE_TAG}.md",
        f"audit_corpus_expansion_v2_punch_list_{DATE_TAG}.md",
        f"audit_full_translations_{DATE_TAG}.md",
        f"audit_external_source_followup_{DATE_TAG}.md",
    ):
        p = DOCS_DIR / fn
        print(f"  docs/{fn}  ({p.stat().st_size:>7} bytes)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Direct ingest pipeline for plain-text Sanskrit primaries.

Reads each *.txt under data/sources/sanskrit/, identifies the work via a
FILE_REGISTRY, validates UTF-8, detects script, segments into verses/sūtras,
normalizes to a Devanāgarī/IAST pair where possible, and emits one
data/ingested/<text_id>.json per work plus a _manifest.json summary.

Tokenizer: falls back to whitespace+danda since prakriya.ocr_api requires
Python 3.10+ slots semantics (rnn ships 3.8/3.9). Normalization uses
indic-transliteration installed to /nas/ucb/eeshan/tmp/pylocal.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable, Optional

# -- local indic-transliteration install --------------------------------------
PYLOCAL = "/nas/ucb/eeshan/tmp/pylocal/lib/python3.8/site-packages"
if PYLOCAL not in sys.path:
    sys.path.insert(0, PYLOCAL)

try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate

    HAS_TRANSLIT = True
except Exception:  # pragma: no cover
    HAS_TRANSLIT = False


# -- constants ----------------------------------------------------------------

WORKTREE = Path("/nas/ucb/eeshan/corpus_worktrees/direct-ingest")
SRC_ROOT = WORKTREE / "data" / "sources" / "sanskrit"
OUT_ROOT = WORKTREE / "data" / "ingested"
INGESTED_AT = "2026-05-19"
INGESTED_BY = "corpus-chat-lane1"

DEVANAGARI_RANGE = (0x0900, 0x097F)
DANDA = "।"
DOUBLE_DANDA = "॥"

# Filename -> (text_id, thinker_id, work_title_iast, work_title_devanagari, kind)
# kind drives the segmenter: 'verse_marker' (// Abbr_x.y //), 'numbered_prefix'
# (1.1.1: ...), 'comma_dotted' (bbs_1,1.1), 'parenthetical_marker'
# ((AnTs_N)), 'prose_paragraph', 'devanagari_danda', 'header_skip_paragraph'
FILE_REGISTRY: dict[str, dict] = {
    # comparator/
    "comparator/badarayana_brahma_sutra.txt": dict(
        text_id="badarayana-brahma-sutra",
        thinker_id="badarayana",
        work_title_iast="Brahma-Sūtra",
        work_title_devanagari="ब्रह्मसूत्र",
        kind="comma_dotted",
    ),
    "comparator/aksapada_nyaya_sutra.txt": dict(
        text_id="aksapada-nyaya-sutra",
        thinker_id="aksapada",
        work_title_iast="Nyāya-Sūtra",
        work_title_devanagari="न्यायसूत्र",
        kind="numbered_prefix",
    ),
    "comparator/isvarakrsna_samkhya_karika.txt": dict(
        text_id="isvarakrsna-samkhya-karika",
        thinker_id="isvarakrsna",
        work_title_iast="Sāṃkhya-Kārikā",
        work_title_devanagari="साङ्ख्यकारिका",
        kind="verse_marker",
    ),
    "comparator/jaimini_mimamsa_sutra.txt": dict(
        text_id="jaimini-mimamsa-sutra",
        thinker_id="jaimini",
        work_title_iast="Mīmāṃsā-Sūtra",
        work_title_devanagari="मीमांसासूत्र",
        kind="verse_marker",
    ),
    "comparator/kanada_vaisesika_sutra.txt": dict(
        text_id="kanada-vaisesika-sutra",
        thinker_id="kanada",
        work_title_iast="Vaiśeṣika-Sūtra",
        work_title_devanagari="वैशेषिकसूत्र",
        kind="verse_marker",
    ),
    "comparator/patanjali_yoga_sutra.txt": dict(
        text_id="patanjali-yoga-sutra",
        thinker_id="patanjali",
        work_title_iast="Yoga-Sūtra",
        work_title_devanagari="योगसूत्र",
        kind="verse_marker",
    ),
    "comparator/shabara_mimamsa_sutra_bhasya.txt": dict(
        text_id="shabara-mimamsa-sutra-bhasya",
        thinker_id="shabara",
        work_title_iast="Mīmāṃsā-Sūtra-Bhāṣya",
        work_title_devanagari="मीमांसासूत्रभाष्य",
        kind="verse_marker",
    ),
    "comparator/umasvati_tattvartha_sutra.txt": dict(
        text_id="umasvati-tattvartha-sutra",
        thinker_id="umasvati",
        work_title_iast="Tattvārtha-Sūtra",
        work_title_devanagari="तत्त्वार्थसूत्र",
        kind="verse_marker",
    ),
    "comparator/vatsyayana_nyaya_bhasya.txt": dict(
        text_id="vatsyayana-nyaya-bhasya",
        thinker_id="vatsyayana",
        work_title_iast="Nyāya-Bhāṣya",
        work_title_devanagari="न्यायभाष्य",
        kind="verse_marker",
    ),
    "comparator/vyasa_yoga_bhasya.txt": dict(
        text_id="vyasa-yoga-bhasya",
        thinker_id="vyasa-yoga",
        work_title_iast="Yoga-Bhāṣya",
        work_title_devanagari="योगभाष्य",
        kind="verse_marker",
    ),
    # buddhist/
    "buddhist/nagarjuna_mula_madhyamaka_karika.txt": dict(
        text_id="nagarjuna-mula-madhyamaka-karika",
        thinker_id="nagarjuna",
        work_title_iast="Mūla-Madhyamaka-Kārikā",
        work_title_devanagari="मूलमध्यमककारिका",
        kind="verse_marker",
    ),
    "buddhist/nagarjuna_vigraha_vyavartani.txt": dict(
        text_id="nagarjuna-vigraha-vyavartani",
        thinker_id="nagarjuna",
        work_title_iast="Vigraha-Vyāvartanī",
        work_title_devanagari="विग्रहव्यावर्तनी",
        kind="verse_marker",
    ),
    "buddhist/candrakirti_madhyamakavatara.txt": dict(
        text_id="candrakirti-madhyamakavatara",
        thinker_id="candrakirti",
        work_title_iast="Madhyamakāvatāra",
        work_title_devanagari="मध्यमकावतार",
        kind="verse_marker",
    ),
    "buddhist/dharmakirti_pramana_varttika.txt": dict(
        text_id="dharmakirti-pramana-varttika",
        thinker_id="dharmakirti",
        work_title_iast="Pramāṇa-Vārttika",
        work_title_devanagari="प्रमाणवार्त्तिक",
        kind="verse_marker",
    ),
    "buddhist/vasubandhu_trimsika.txt": dict(
        text_id="vasubandhu-trimsika",
        thinker_id="vasubandhu",
        work_title_iast="Triṃśikā",
        work_title_devanagari="त्रिंशिका",
        kind="verse_marker",
    ),
    "buddhist/vasubandhu_vimsatika.txt": dict(
        text_id="vasubandhu-vimsatika",
        thinker_id="vasubandhu",
        work_title_iast="Viṃśatikā",
        work_title_devanagari="विंशतिका",
        kind="verse_marker",
    ),
    # caitanya_gaudiya/
    "caitanya_gaudiya/jiva_sat_sandarbha.txt": dict(
        text_id="jiva-sat-sandarbha",
        thinker_id="jiva-gosvami",
        work_title_iast="Ṣaṭ-Sandarbha",
        work_title_devanagari="षट्सन्दर्भ",
        kind="prose_paragraph",
    ),
    "caitanya_gaudiya/rupa_bhakti_rasamrta_sindhu.txt": dict(
        text_id="rupa-bhakti-rasamrta-sindhu",
        thinker_id="rupa-gosvami",
        work_title_iast="Bhakti-Rasāmṛta-Sindhu",
        work_title_devanagari="भक्तिरसामृतसिन्धु",
        kind="verse_marker",
    ),
    # kala_cakra/
    "kala_cakra/abhinavagupta_tantraloka_chapter06_kalopaya_kalacakra.txt": dict(
        text_id="abhinavagupta-tantraloka-ch06-kalopaya-kalacakra",
        thinker_id="abhinavagupta",
        work_title_iast="Tantrāloka (Chapter 6: Kālopāya / Kālacakra)",
        work_title_devanagari="तन्त्रालोक (६: कालोपाय)",
        kind="verse_marker",
    ),
    # _kashmir_saivism/
    "_kashmir_saivism/AdvaitasiddhiVsNyayamrta.txt": dict(
        text_id="sharma-advaitasiddhi-vs-nyayamrta",
        thinker_id=None,  # secondary scholarship (B.N.K. Sharma), not a thinker text
        work_title_iast="Advaitasiddhi Vs Nyāyāmṛta — A Critical Re-Appraisal (B.N.K. Sharma)",
        work_title_devanagari="अद्वैतसिद्धिः vs न्यायामृतम् (शर्म)",
        kind="prose_paragraph",
        caveats=["Secondary scholarship by B.N.K. Sharma, not a primary Sanskrit text; OCR-quality English with embedded Sanskrit citations."],
    ),
    # kashmir_shaiva/
    "kashmir_shaiva/abhinavagupta_ipv.txt": dict(
        text_id="abhinavagupta-isvarapratyabhijna-vimarsini",
        thinker_id="abhinavagupta",
        work_title_iast="Īśvara-Pratyabhijñā-Vimarśinī",
        work_title_devanagari="ईश्वरप्रत्यभिज्ञाविमर्शिनी",
        kind="verse_marker",
    ),
    "kashmir_shaiva/abhinavagupta_paramartha_sara.txt": dict(
        text_id="abhinavagupta-paramartha-sara",
        thinker_id="abhinavagupta",
        work_title_iast="Paramārtha-Sāra",
        work_title_devanagari="परमार्थसार",
        kind="verse_marker",
    ),
    "kashmir_shaiva/abhinavagupta_tantrasara.txt": dict(
        text_id="abhinavagupta-tantrasara",
        thinker_id="abhinavagupta",
        work_title_iast="Tantrasāra",
        work_title_devanagari="तन्त्रसार",
        kind="prose_paragraph",
    ),
    "kashmir_shaiva/ksemaraja_pratyabhijna_hrdayam.txt": dict(
        text_id="ksemaraja-pratyabhijna-hrdayam",
        thinker_id="ksemaraja",
        work_title_iast="Pratyabhijñā-Hṛdayam",
        work_title_devanagari="प्रत्यभिज्ञाहृदयम्",
        kind="verse_marker",
    ),
    "kashmir_shaiva/spanda_karika.txt": dict(
        text_id="spanda-karika",
        thinker_id="bhatta-kallata",  # traditional ascription
        work_title_iast="Spanda-Kārikā",
        work_title_devanagari="स्पन्दकारिका",
        kind="verse_marker",
        caveats=["Authorship traditionally to Vasugupta or Bhaṭṭa Kallaṭa; ascription contested."],
    ),
    "kashmir_shaiva/utpaladeva_isvara_pratyabhijna_karika.txt": dict(
        text_id="utpaladeva-isvara-pratyabhijna-karika",
        thinker_id="utpaladeva",
        work_title_iast="Īśvara-Pratyabhijñā-Kārikā",
        work_title_devanagari="ईश्वरप्रत्यभिज्ञाकारिका",
        kind="verse_marker",
    ),
    # mimamsa/
    "mimamsa/kumarila_sloka_varttika_comm.txt": dict(
        text_id="kumarila-sloka-varttika-with-comm",
        thinker_id="kumarila",
        work_title_iast="Śloka-Vārttika (with commentary)",
        work_title_devanagari="श्लोकवार्त्तिक (सटीक)",
        kind="prose_paragraph",
    ),
    "mimamsa/madhava_jaimini_nyaya_mala.txt": dict(
        text_id="madhava-jaiminiya-nyaya-mala-vistara",
        thinker_id="madhava-vidyaranya",
        work_title_iast="Jaiminīya-Nyāya-Mālā-Vistara",
        work_title_devanagari="जैमिनीयन्यायमालाविस्तर",
        kind="verse_marker",
    ),
    "mimamsa/sucaritamisra_sloka_varttika.txt": dict(
        text_id="sucaritamisra-sloka-varttika-kasika",
        thinker_id="sucaritamisra",
        work_title_iast="Śloka-Vārttika-Kāśikā (Sucaritamiśra)",
        work_title_devanagari="श्लोकवार्त्तिककाशिका",
        kind="prose_paragraph",
    ),
    # nyaya/
    "nyaya/annambhatta_tarka_sangraha.txt": dict(
        text_id="annambhatta-tarka-sangraha",
        thinker_id="annambhatta",
        work_title_iast="Tarka-Saṃgraha",
        work_title_devanagari="तर्कसङ्ग्रह",
        kind="parenthetical_marker",
    ),
    "nyaya/annambhatta_tarka_sangraha_comm.txt": dict(
        text_id="annambhatta-tarka-sangraha-dipika",
        thinker_id="annambhatta",
        work_title_iast="Tarka-Saṃgraha-Dīpikā (auto-commentary + Bālapriyā)",
        work_title_devanagari="तर्कसङ्ग्रहदीपिका",
        kind="prose_paragraph",
        caveats=["File interleaves Tarka-Saṃgraha mūla, Dīpikā auto-commentary, and Bālapriyā subcommentary; structure not recovered by lane-1 (prose paragraphs only). Lane 4 should re-segment by `ants_NXY` markers."],
    ),
    "nyaya/dharmakirti_nyaya_bindu.txt": dict(
        text_id="dharmakirti-nyaya-bindu",
        thinker_id="dharmakirti",
        work_title_iast="Nyāya-Bindu",
        work_title_devanagari="न्यायबिन्दु",
        kind="verse_marker",
    ),
    "nyaya/nyaya_sutra_gautama.txt": dict(
        text_id="gautama-nyaya-sutra",
        thinker_id="aksapada",  # Akṣapāda Gautama
        work_title_iast="Nyāya-Sūtra (Gautama)",
        work_title_devanagari="न्यायसूत्र",
        kind="numbered_prefix",
        caveats=["Duplicate-class of comparator/aksapada_nyaya_sutra.txt; kept distinct as nyaya/ may carry different edition."],
    ),
    "nyaya/udayana_nyaya_kusumanjali.txt": dict(
        text_id="udayana-nyaya-kusumanjali",
        thinker_id="udayana",
        work_title_iast="Nyāya-Kusumāñjali",
        work_title_devanagari="न्यायकुसुमाञ्जलि",
        kind="verse_marker",
    ),
    # samkhya/
    "samkhya/samkhya_sutra_kapila.txt": dict(
        text_id="kapila-samkhya-sutra",
        thinker_id="kapila",
        work_title_iast="Sāṃkhya-Sūtra (with Tattvasamāsa)",
        work_title_devanagari="साङ्ख्यसूत्र",
        kind="verse_marker",
    ),
    # vedanta/full_corpus/
    "vedanta/full_corpus/gaudapada_mandukya_karika_gretil.txt": dict(
        text_id="gaudapada-mandukya-karika",
        thinker_id="gaudapada",
        work_title_iast="Māṇḍūkya-Kārikā (Āgama-Śāstra)",
        work_title_devanagari="माण्डूक्यकारिका",
        kind="verse_marker",
    ),
    "vedanta/full_corpus/madhusudana_siddhanta_bindu_gretil.txt": dict(
        text_id="madhusudana-siddhanta-bindu",
        thinker_id="madhusudana",
        work_title_iast="Siddhānta-Bindu",
        work_title_devanagari="सिद्धान्तबिन्दु",
        kind="verse_marker",
    ),
    "vedanta/full_corpus/madhva_anuvyakhyana_gretil.txt": dict(
        text_id="madhva-anuvyakhyana",
        thinker_id="madhva",
        work_title_iast="Anuvyākhyāna",
        work_title_devanagari="अनुव्याख्यान",
        kind="verse_marker",
    ),
    "vedanta/full_corpus/mandana_misra_brahma_siddhi_gretil.txt": dict(
        text_id="mandana-brahma-siddhi",
        thinker_id="mandana",
        work_title_iast="Brahma-Siddhi",
        work_title_devanagari="ब्रह्मसिद्धि",
        kind="verse_marker",
    ),
    "vedanta/full_corpus/shankara_upadesa_sahasri_gretil.txt": dict(
        text_id="shankara-upadesa-sahasri",
        thinker_id="sankara",
        work_title_iast="Upadeśa-Sāhasrī",
        work_title_devanagari="उपदेशसाहस्री",
        kind="verse_marker",
    ),
    "vedanta/full_corpus/shankara_vivekacudamani_gretil.txt": dict(
        text_id="shankara-vivekacudamani",
        thinker_id="sankara",
        work_title_iast="Vivekacūḍāmaṇi",
        work_title_devanagari="विवेकचूडामणि",
        kind="verse_marker",
        caveats=["Authorship `school-ascribed` per CORPUS_PLAN.md, not securely Śaṅkara."],
    ),
    "vedanta/full_corpus/vyasatirtha_tarka_tandava_gretil.txt": dict(
        text_id="vyasatirtha-tarka-tandava",
        thinker_id="vyasatirtha",
        work_title_iast="Tarka-Tāṇḍava",
        work_title_devanagari="तर्कताण्डव",
        kind="prose_paragraph",
    ),
    "vedanta/full_corpus/yamuna_atma_siddhi_gretil.txt": dict(
        text_id="yamuna-atma-siddhi",
        thinker_id="yamuna",
        work_title_iast="Ātma-Siddhi",
        work_title_devanagari="आत्मसिद्धि",
        kind="verse_marker",
    ),
    "vedanta/full_corpus/yamuna_isvara_siddhi_gretil.txt": dict(
        text_id="yamuna-isvara-siddhi",
        thinker_id="yamuna",
        work_title_iast="Īśvara-Siddhi",
        work_title_devanagari="ईश्वरसिद्धि",
        kind="verse_marker",
    ),
    "vedanta/full_corpus/yamuna_samvit_siddhi_gretil.txt": dict(
        text_id="yamuna-samvit-siddhi",
        thinker_id="yamuna",
        work_title_iast="Saṃvit-Siddhi",
        work_title_devanagari="संवित्सिद्धि",
        kind="verse_marker",
    ),
    "vedanta/full_corpus/yamuna_stotra_ratna_gretil.txt": dict(
        text_id="yamuna-stotra-ratna",
        thinker_id="yamuna",
        work_title_iast="Stotra-Ratna",
        work_title_devanagari="स्तोत्ररत्न",
        kind="verse_marker",
    ),
    # vedanta/ (top-level)
    "vedanta/jayatirtha_nyaya_sudha.txt": dict(
        text_id="jayatirtha-nyaya-sudha",
        thinker_id="jayatirtha",
        work_title_iast="Nyāya-Sudhā",
        work_title_devanagari="न्यायसुधा",
        kind="prose_paragraph",
    ),
    "vedanta/madhva_mahabharata_tatparya.txt": dict(
        text_id="madhva-mahabharata-tatparya-nirnaya",
        thinker_id="madhva",
        work_title_iast="Mahābhārata-Tātparya-Nirṇaya",
        work_title_devanagari="महाभारततात्पर्यनिर्णय",
        kind="pipe_inline",
    ),
    "vedanta/ramanuja_gita_bhasya.txt": dict(
        text_id="ramanuja-gita-bhasya",
        thinker_id="ramanuja",
        work_title_iast="Gītā-Bhāṣya",
        work_title_devanagari="गीताभाष्य",
        kind="prose_paragraph",
    ),
    "vedanta/ramanuja_vedartha_sangraha.txt": dict(
        text_id="ramanuja-vedartha-sangraha",
        thinker_id="ramanuja",
        work_title_iast="Vedārtha-Saṃgraha",
        work_title_devanagari="वेदार्थसङ्ग्रह",
        kind="prose_paragraph",
    ),
    "vedanta/shankara_brahma_sutra_bhasya.txt": dict(
        text_id="shankara-brahma-sutra-bhasya",
        thinker_id="sankara",
        work_title_iast="Brahma-Sūtra-Bhāṣya",
        work_title_devanagari="ब्रह्मसूत्रभाष्य",
        kind="prose_paragraph",
    ),
    "vedanta/vacaspati_bhamati.txt": dict(
        text_id="vacaspati-bhamati",
        thinker_id="vacaspati",
        work_title_iast="Bhāmatī",
        work_title_devanagari="भामती",
        kind="prose_paragraph",
    ),
}


# -- script detection ---------------------------------------------------------

def detect_script(sample: str) -> str:
    deva = iast = 0
    for ch in sample:
        if not ch.isalpha():
            continue
        cp = ord(ch)
        if DEVANAGARI_RANGE[0] <= cp <= DEVANAGARI_RANGE[1]:
            deva += 1
        elif ord(ch) < 0x80 or 0x80 <= cp <= 0x2AF:
            # ASCII Latin or IAST extended-Latin diacritics range
            iast += 1
    if deva == 0 and iast == 0:
        return "unknown"
    if deva > 5 * max(iast, 1):
        return "devanagari"
    if iast > 5 * max(deva, 1):
        return "iast"
    if deva == 0:
        return "iast"
    if iast == 0:
        return "devanagari"
    return "mixed"


# -- normalization ------------------------------------------------------------

def to_iast(text: str, src_script: str) -> str:
    if not HAS_TRANSLIT or not text:
        return ""
    if src_script == "iast":
        return text
    if src_script == "devanagari":
        try:
            return transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
        except Exception:
            return ""
    return ""


def to_devanagari(text: str, src_script: str) -> str:
    if not HAS_TRANSLIT or not text:
        return ""
    if src_script == "devanagari":
        return text
    if src_script == "iast":
        try:
            # strip any leftover ASCII tokens unsafe for sanscript — leave as-is
            return transliterate(text, sanscript.IAST, sanscript.DEVANAGARI)
        except Exception:
            return ""
    return ""


# -- tokenization (fallback) --------------------------------------------------

TOK_RE = re.compile(r"[^\s।॥|/\\]+", re.UNICODE)


def approx_token_count(text: str) -> int:
    return len(TOK_RE.findall(text))


# -- header stripping ---------------------------------------------------------

GRETIL_HEADER_END = re.compile(r"^\s*#\s*Text\s*$", re.MULTILINE)


def strip_gretil_header(text: str) -> tuple[str, int]:
    """Remove GRETIL header up through `# Text`. Returns (body, lines_skipped)."""
    m = GRETIL_HEADER_END.search(text)
    if m:
        idx = m.end()
        # advance to start of next non-empty line
        before = text[:idx]
        lines_skipped = before.count("\n") + 1
        body = text[idx:].lstrip("\n")
        return body, lines_skipped
    return text, 0


# -- segmenters ---------------------------------------------------------------

@dataclass
class Verse:
    verse_id: str
    adhyaya: Optional[int] = None
    pada: Optional[int] = None
    sutra_or_verse_num: Optional[str] = None
    sanskrit_devanagari: str = ""
    sanskrit_iast: str = ""
    source_line_start: int = 0
    source_line_end: int = 0


# pattern A: line(s) ending with one of:
#   // Abbr_X.Y //          (MMK_1.1, GpK_1.1, Pramāṇav_2.17, ys_1.1 if // delim)
#   || Abbr_X.Y ||          (some GRETIL with ||)
#   || N ||                 (numeric-only verse number; Spanda)
#   // Abbr_pref,X.Y //     (samupad_i,1.1 — letter-prefixed sub-section)
# trailing `//` or `||` optional. Anchored at line end.
VERSE_MARKER_RE = re.compile(
    r"(?://|\|\|)\s*(?:\d+\s+)?"
    r"(?:([A-Za-z][A-Za-z0-9]*)_([A-Za-z]+,)?([0-9]+(?:[.,][0-9]+){0,3})(?:[a-z]?)"
    r"|([0-9]+))"
    r"\s*(?://|\|\|)?\s*$"
)
# pattern A2: same but without slashes, just trailing `Abbr_X.Y` on its own line
VERSE_MARKER_TRAIL_RE = re.compile(
    r"\b([A-Za-z][A-Za-z0-9]*)_([0-9]+(?:[.,][0-9]+){0,3})(?:[a-z]?)\b\s*$"
)
# pattern B: `1.1.1:` prefix
NUMBERED_PREFIX_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+){1,3})\s*[:.]\s*(.*)$")
# pattern C: `bbs_1,1.1 |` comma-dotted (Brahma-Sūtra style)
COMMA_DOTTED_RE = re.compile(
    r"^\s*(.+?)\s*\|\s*([a-z]+_)?([0-9]+,[0-9]+(?:\.[0-9]+)?)\s*\|\s*$"
)
# pattern D: parenthetical `(AnTs_N)` or `//(AnTs_N)`
PAREN_MARKER_RE = re.compile(r"//?\s*\(\s*([A-Za-z][A-Za-z0-9]*)_([0-9]+(?:[.,][0-9]+){0,3})\s*\)\s*$")


def _extract_verse_num(m: re.Match) -> str:
    """Pull the verse-number string from VERSE_MARKER_RE match (handles all branches)."""
    abbr_num = m.group(3)
    bare_num = m.group(4)
    prefix = m.group(2) or ""
    if abbr_num:
        return f"{prefix}{abbr_num}".rstrip(",")
    return bare_num or ""


def segment_verse_marker(body: str) -> tuple[list[Verse], bool]:
    """Lines accumulate until a `// Abbr_X.Y //` or `|| N ||` marker closes a verse."""
    lines = body.splitlines()
    verses: list[Verse] = []
    buf: list[str] = []
    buf_start = 0
    found = False
    seq = 0
    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        if not buf:
            buf_start = i
        m = VERSE_MARKER_RE.search(line) or PAREN_MARKER_RE.search(line)
        if m:
            found = True
            if m.re is PAREN_MARKER_RE:
                num = m.group(2)
                cleaned = PAREN_MARKER_RE.sub("", line).rstrip()
            else:
                num = _extract_verse_num(m)
                cleaned = VERSE_MARKER_RE.sub("", line).rstrip()
            if cleaned:
                buf.append(cleaned)
            verse_text = "\n".join(b for b in buf if b.strip())
            if verse_text.strip():
                seq += 1
                if num:
                    vid = f"v_{num.replace(',', '_').replace('.', '_')}"
                    parts = re.split(r"[.,]", num)
                    adhyaya = int(parts[0]) if parts and parts[0].isdigit() else None
                    pada = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
                else:
                    vid = f"v_{seq:05d}"
                    adhyaya = None
                    pada = None
                verses.append(
                    Verse(
                        verse_id=vid,
                        adhyaya=adhyaya,
                        pada=pada,
                        sutra_or_verse_num=num or str(seq),
                        source_line_start=buf_start,
                        source_line_end=i,
                    )
                )
                verses[-1].sanskrit_iast = verse_text  # tentative; assigned per script below
            buf = []
            continue
        if line.strip():
            buf.append(line)
    return verses, found


def segment_numbered_prefix(body: str) -> tuple[list[Verse], bool]:
    """Lines like `1.1.1: <content>` (Nyāya-sūtra style)."""
    lines = body.splitlines()
    verses: list[Verse] = []
    current: Optional[Verse] = None
    buf: list[str] = []
    found = False
    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        m = NUMBERED_PREFIX_RE.match(line)
        if m:
            found = True
            # flush previous
            if current is not None:
                current.sanskrit_iast = "\n".join(b for b in buf if b.strip())
                current.source_line_end = i - 1
                verses.append(current)
            num = m.group(1)
            content = m.group(2).strip()
            parts = num.split(".")
            adhyaya = int(parts[0]) if parts and parts[0].isdigit() else None
            pada = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
            current = Verse(
                verse_id=f"v_{num.replace('.', '_')}",
                adhyaya=adhyaya,
                pada=pada,
                sutra_or_verse_num=num,
                source_line_start=i,
                source_line_end=i,
            )
            buf = [content] if content else []
        else:
            if current is not None and line.strip() and not line.lstrip().startswith("{"):
                buf.append(line)
    if current is not None:
        current.sanskrit_iast = "\n".join(b for b in buf if b.strip())
        current.source_line_end = len(lines)
        verses.append(current)
    return verses, found


def segment_comma_dotted(body: str) -> tuple[list[Verse], bool]:
    """Brahma-Sūtra style: `<text> | bbs_1,1.1 |`."""
    lines = body.splitlines()
    verses: list[Verse] = []
    found = False
    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        m = COMMA_DOTTED_RE.match(line)
        if m:
            found = True
            content = m.group(1).strip()
            num = m.group(3)
            # `1,1.1` -> adhyaya=1, pada=1, sutra=1
            head, rest = num.split(",", 1)
            adhyaya = int(head) if head.isdigit() else None
            rest_parts = rest.split(".")
            pada = int(rest_parts[0]) if rest_parts and rest_parts[0].isdigit() else None
            snum = rest_parts[1] if len(rest_parts) > 1 else None
            vid = f"v_{adhyaya}_{pada}_{snum}" if snum else f"v_{adhyaya}_{pada}"
            verses.append(
                Verse(
                    verse_id=vid,
                    adhyaya=adhyaya,
                    pada=pada,
                    sutra_or_verse_num=num.replace(",", "."),
                    sanskrit_iast=content,
                    source_line_start=i,
                    source_line_end=i,
                )
            )
    return verses, found


def segment_prose_paragraph(body: str) -> tuple[list[Verse], bool]:
    """Paragraph-level chunks; no structure recovered. Splits on blank lines."""
    paragraphs = re.split(r"\n\s*\n+", body)
    verses: list[Verse] = []
    line_cursor = 1
    for idx, para in enumerate(paragraphs, start=1):
        if not para.strip():
            line_cursor += para.count("\n") + 1
            continue
        n_lines = para.count("\n") + 1
        verses.append(
            Verse(
                verse_id=f"c_{idx:05d}",
                sanskrit_iast=para.strip(),
                source_line_start=line_cursor,
                source_line_end=line_cursor + n_lines - 1,
            )
        )
        line_cursor += n_lines + 1
    return verses, False


_PAREN_INLINE_RE = re.compile(r"//?\s*\(\s*([A-Za-z][A-Za-z0-9]*)_([0-9]+(?:[.,][0-9]+){0,3})\s*\)")


def segment_parenthetical_marker(body: str) -> tuple[list[Verse], bool]:
    """Tarka-Saṃgraha style: prose ending with `//(AnTs_N)`. Line-based, no DOTALL regex."""
    lines = body.splitlines()
    verses: list[Verse] = []
    buf: list[str] = []
    buf_start: Optional[int] = None
    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        if not line.strip():
            continue
        if buf_start is None:
            buf_start = i
        m = _PAREN_INLINE_RE.search(line)
        if m:
            num = m.group(2)
            cleaned = _PAREN_INLINE_RE.sub("", line).rstrip()
            if cleaned:
                buf.append(cleaned)
            verse_text = "\n".join(buf).strip()
            if verse_text:
                verses.append(
                    Verse(
                        verse_id=f"v_{num.replace('.', '_').replace(',', '_')}",
                        sutra_or_verse_num=num,
                        sanskrit_iast=verse_text,
                        source_line_start=buf_start or i,
                        source_line_end=i,
                    )
                )
            buf = []
            buf_start = None
        else:
            buf.append(line)
    return verses, bool(verses)


_PIPE_INLINE_RE = re.compile(r"\|\s*([0-9]+(?:\.[0-9]+){0,3})\s*\|")


def segment_pipe_inline(body: str) -> tuple[list[Verse], bool]:
    """Inline-delimited verses: `... text 1.1 | text 1.2 | ...` (Mahābhārata-Tātparya style)."""
    # find every marker; chunk between previous-end and this-start is the verse
    matches = list(_PIPE_INLINE_RE.finditer(body))
    if not matches:
        return [], False
    verses: list[Verse] = []
    prev_end = 0
    # build a running line-cursor by counting newlines in body[:offset]
    for m in matches:
        chunk = body[prev_end:m.start()].strip()
        num = m.group(1)
        if chunk:
            start_line = body.count("\n", 0, prev_end) + 1
            end_line = body.count("\n", 0, m.start()) + 1
            parts = num.split(".")
            adhyaya = int(parts[0]) if parts and parts[0].isdigit() else None
            pada = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
            verses.append(
                Verse(
                    verse_id=f"v_{num.replace('.', '_')}",
                    adhyaya=adhyaya,
                    pada=pada,
                    sutra_or_verse_num=num,
                    sanskrit_iast=chunk,
                    source_line_start=start_line,
                    source_line_end=end_line,
                )
            )
        prev_end = m.end()
    return verses, True


SEGMENTERS = {
    "verse_marker": segment_verse_marker,
    "numbered_prefix": segment_numbered_prefix,
    "comma_dotted": segment_comma_dotted,
    "prose_paragraph": segment_prose_paragraph,
    "parenthetical_marker": segment_parenthetical_marker,
    "pipe_inline": segment_pipe_inline,
}


# -- pipeline -----------------------------------------------------------------

def ingest_file(rel_path: str, meta: dict) -> dict:
    src = SRC_ROOT / rel_path
    raw_bytes = src.read_bytes()
    try:
        text = raw_bytes.decode("utf-8")
        encoding_ok = True
    except UnicodeDecodeError:
        text = raw_bytes.decode("utf-8", errors="replace")
        encoding_ok = False
    text = unicodedata.normalize("NFC", text)

    # strip GRETIL header if present
    body, header_lines = strip_gretil_header(text)

    script = detect_script(body[:5000])
    kind = meta.get("kind", "prose_paragraph")
    segmenter = SEGMENTERS.get(kind, segment_prose_paragraph)
    verses, structure_recovered = segmenter(body)

    # If verse_marker segmenter found nothing, fall back to prose_paragraph
    if not verses and kind == "verse_marker":
        verses, structure_recovered = segment_prose_paragraph(body)
        used_segmenter = "prose_paragraph(fallback)"
    else:
        used_segmenter = kind

    # Populate dual-script for each verse
    for v in verses:
        raw = v.sanskrit_iast  # tentative; what segmenter put there is raw content in source script
        if script == "iast":
            v.sanskrit_iast = raw
            v.sanskrit_devanagari = to_devanagari(raw, "iast")
        elif script == "devanagari":
            v.sanskrit_devanagari = raw
            v.sanskrit_iast = to_iast(raw, "devanagari")
        else:
            # mixed/unknown: keep raw under iast, leave devanagari blank
            v.sanskrit_iast = raw
            v.sanskrit_devanagari = ""

    caveats = list(meta.get("caveats", []))
    if not encoding_ok:
        caveats.append("UTF-8 decode errors encountered; some characters replaced.")
    if header_lines:
        caveats.append(f"Stripped GRETIL header ({header_lines} lines).")
    if used_segmenter != kind:
        caveats.append(f"Primary segmenter `{kind}` recovered no structure; fell back to `{used_segmenter}`.")
    if script == "mixed":
        caveats.append("Mixed script detected; dual-script normalization disabled per-verse.")
    if not HAS_TRANSLIT:
        caveats.append("indic-transliteration not available; dual-script generation skipped.")

    out = {
        "text_id": meta["text_id"],
        "thinker_id": meta.get("thinker_id"),
        "work_title_iast": meta["work_title_iast"],
        "work_title_devanagari": meta["work_title_devanagari"],
        "source_file": f"data/sources/sanskrit/{rel_path}",
        "source_script": script,
        "tokenizer": "fallback_whitespace",
        "normalizer": "indic_transliteration" if HAS_TRANSLIT else "none",
        "ingested_at": INGESTED_AT,
        "ingested_by": INGESTED_BY,
        "structure_recovered": bool(structure_recovered),
        "verse_count": len(verses),
        "token_count_approx": sum(approx_token_count(v.sanskrit_iast or v.sanskrit_devanagari) for v in verses),
        "verses": [
            {
                "verse_id": v.verse_id,
                "adhyaya": v.adhyaya,
                "pada": v.pada,
                "sutra_or_verse_num": v.sutra_or_verse_num,
                "sanskrit_devanagari": v.sanskrit_devanagari,
                "sanskrit_iast": v.sanskrit_iast,
                "source_line_start": v.source_line_start,
                "source_line_end": v.source_line_end,
            }
            for v in verses
        ],
        "caveats": caveats,
    }
    return out


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--only-missing", action="store_true",
                    help="Only ingest files whose output JSON is not yet present.")
    ap.add_argument("--files", nargs="*", help="Restrict to specific rel paths.")
    args = ap.parse_args()

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    skipped: list[dict] = []

    # discover all .txt files
    discovered = sorted(
        str(p.relative_to(SRC_ROOT))
        for p in SRC_ROOT.rglob("*.txt")
    )
    if args.files:
        discovered = [d for d in discovered if d in args.files]

    for rel in discovered:
        if args.only_missing and rel in FILE_REGISTRY:
            tid = FILE_REGISTRY[rel]["text_id"]
            if (OUT_ROOT / f"{tid}.json").exists():
                # still re-record manifest entry from existing file
                try:
                    with (OUT_ROOT / f"{tid}.json").open(encoding="utf-8") as fh:
                        doc = json.load(fh)
                    manifest.append(
                        dict(
                            text_id=doc["text_id"],
                            source_file=doc["source_file"],
                            verse_count=doc["verse_count"],
                            token_count_approx=doc["token_count_approx"],
                            structure_recovered=doc["structure_recovered"],
                            tokenizer=doc["tokenizer"],
                            caveats=doc.get("caveats", []),
                        )
                    )
                except Exception:
                    pass
                continue
        if rel not in FILE_REGISTRY:
            skipped.append(
                dict(
                    source_file=f"data/sources/sanskrit/{rel}",
                    reason="not in FILE_REGISTRY — unknown work, lane-1 will not ingest",
                )
            )
            continue
        meta = FILE_REGISTRY[rel]
        try:
            doc = ingest_file(rel, meta)
        except Exception as exc:  # pragma: no cover
            skipped.append(
                dict(
                    source_file=f"data/sources/sanskrit/{rel}",
                    reason=f"exception during ingest: {exc!r}",
                )
            )
            continue
        out_path = OUT_ROOT / f"{doc['text_id']}.json"
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=2)
        manifest.append(
            dict(
                text_id=doc["text_id"],
                source_file=doc["source_file"],
                verse_count=doc["verse_count"],
                token_count_approx=doc["token_count_approx"],
                structure_recovered=doc["structure_recovered"],
                tokenizer=doc["tokenizer"],
                caveats=doc["caveats"],
            )
        )
        print(f"OK  {doc['text_id']}: {doc['verse_count']} verses, {doc['token_count_approx']} tokens (structure_recovered={doc['structure_recovered']})", flush=True)

    # also include TODO entries
    todo = [
        dict(
            text_id="bhagavad-gita-chapters",
            reason="Per-chapter JSON lives at ~/Dev/Gita/ on a local machine, not on rnn; deferred until copied to NAS.",
        ),
    ]

    with (OUT_ROOT / "_manifest.json").open("w", encoding="utf-8") as fh:
        json.dump(
            dict(
                generated_at=INGESTED_AT,
                generated_by=INGESTED_BY,
                ingested=manifest,
                skipped=skipped,
                todo=todo,
            ),
            fh,
            ensure_ascii=False,
            indent=2,
        )

    if skipped:
        with (OUT_ROOT / "_skipped.json").open("w", encoding="utf-8") as fh:
            json.dump(skipped, fh, ensure_ascii=False, indent=2)

    print(f"\nWrote {len(manifest)} ingest files, {len(skipped)} skipped, {len(todo)} todo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

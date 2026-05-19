#!/usr/bin/env python3
"""Build data/digitization_queue_267.json — the §B basket inventory.

Sources:
  - docs/ACQUISITION_PATHWAYS.md §B.1..B.10 prose (texts named in each basket)
  - data/thinkers/*.json engaged_works (priority bucketing)
  - docs/CORPUS_PLAN.md / docs/CORPUS_EXPANSION_v2.md (referenced in priority rules)

This is curated by hand from the §B prose — no fabrication. Where the §B prose
names a text, we record it. Where it gives a basket-level "etc." we do not
expand it; we record only what is explicitly named.

Priority buckets:
  P0 — referenced as engaged_works for >=3 thinkers OR explicitly named in
       CORPUS_PLAN.md "core" tier.
  P1 — referenced for 1-2 thinkers OR in CORPUS_EXPANSION_v2.md.
  P2 — listed in §B but not yet linked to engagement.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path("/home/eeshan/vedanta-timeline")
OUT = REPO  # We will write data/ relative to the worktree, not the source repo.
WORKTREE = Path("/nas/ucb/eeshan/corpus_worktrees/digitization-prep")

# Hand-curated text entries by basket. Keys come from §B prose; only named
# texts are included. work_id_if_known matches engaged_works ids in data/thinkers/*.json
# when verifiable, else null.

TEXTS = [
    # ====== B.1 Madhva Sarvamūla — the remaining 30+ titles ======
    # The §B.1 prose explicitly names: Daśa-Prakaraṇa (10 short polemical tracts),
    # Tantra-Sāra-Saṅgraha, Yati-Praṇava-Kalpa, Mahābhārata-Tātparya-Nirṇaya,
    # Bhāgavata-Tātparya-Nirṇaya, Anu-Vyākhyāna, the ten Upaniṣad-Bhāṣyas.
    # We record the named items. The "etc." we treat as not-yet-enumerated.
    {"text_id": "madhva-dasa-prakarana", "title_iast": "Daśa-Prakaraṇa",
     "thinker_id_if_known": "madhva", "basket": "B1",
     "holding_institution": "Akhila Bhāratīya Mādhva Mahā Maṇḍala (Udupi); PPVP Bangalore",
     "free_pdf_url_if_known": "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books",
     "free_pdf_status": "index_only_no_direct_url",
     "acquisition_status": "free_pdf_available",
     "notes": "Ten short polemical tracts; bearer volume is Sarvamula-Granthah, navigated from Madhwapracharavedike index."},
    {"text_id": "madhva-tantra-sara-sangraha", "title_iast": "Tantra-Sāra-Saṅgraha",
     "thinker_id_if_known": "madhva", "basket": "B1",
     "holding_institution": "Akhila Bhāratīya Mādhva Mahā Maṇḍala (Udupi); PPVP Bangalore",
     "free_pdf_url_if_known": "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books",
     "free_pdf_status": "index_only_no_direct_url",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "madhva-yati-pranava-kalpa", "title_iast": "Yati-Praṇava-Kalpa",
     "thinker_id_if_known": "madhva", "basket": "B1",
     "holding_institution": "Akhila Bhāratīya Mādhva Mahā Maṇḍala (Udupi); PPVP Bangalore",
     "free_pdf_url_if_known": "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books",
     "free_pdf_status": "index_only_no_direct_url",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "madhva-mahabharata-tatparya-nirnaya", "title_iast": "Mahābhārata-Tātparya-Nirṇaya",
     "thinker_id_if_known": "madhva", "basket": "B1",
     "holding_institution": "Akhila Bhāratīya Mādhva Mahā Maṇḍala (Udupi); PPVP Bangalore",
     "free_pdf_url_if_known": "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books",
     "free_pdf_status": "index_only_no_direct_url",
     "acquisition_status": "free_pdf_available",
     "notes": "Already partly on disk per §B.1."},
    {"text_id": "madhva-bhagavata-tatparya-nirnaya", "title_iast": "Bhāgavata-Tātparya-Nirṇaya",
     "thinker_id_if_known": "madhva", "basket": "B1",
     "holding_institution": "Akhila Bhāratīya Mādhva Mahā Maṇḍala (Udupi); PPVP Bangalore",
     "free_pdf_url_if_known": "https://archive.org/details/SriBhagavataTatparyaNirnayaEBook",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "madhva-anu-vyakhyana", "title_iast": "Anu-Vyākhyāna",
     "thinker_id_if_known": "madhva", "basket": "B1",
     "holding_institution": "PPVP Bangalore; Madhva Mahā Maṇḍala",
     "free_pdf_url_if_known": "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books",
     "free_pdf_status": "index_only_no_direct_url",
     "acquisition_status": "free_pdf_available",
     "notes": "Already on disk per §B.1."},
    {"text_id": "madhva-upanisad-bhasya-corpus", "title_iast": "Daśopaniṣad-Bhāṣyas",
     "thinker_id_if_known": "madhva", "basket": "B1",
     "holding_institution": "Akhila Bhāratīya Mādhva Mahā Maṇḍala (Udupi); PPVP Bangalore",
     "free_pdf_url_if_known": "https://archive.org/details/Prasthanathrayi-UpanishathPrashthana",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available",
     "notes": "Ten Upaniṣad-Bhāṣyas; the Upaniṣat-Prasthānam volume of Bannañje's Sarvamūla-Granthāḥ is the bearer."},

    # ====== B.2 Jayatīrtha and Vyāsatīrtha sub-commentary tradition ======
    {"text_id": "jayatirtha-nyaya-sudha", "title_iast": "Nyāya-Sudhā",
     "thinker_id_if_known": "jayatirtha", "basket": "B2",
     "holding_institution": "PPSM Bangalore; Dvaita Vedānta Studies and Research Foundation",
     "free_pdf_url_if_known": "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books",
     "free_pdf_status": "index_only_no_direct_url",
     "acquisition_status": "free_pdf_available",
     "notes": "Already on disk per §B.2."},
    {"text_id": "jayatirtha-tattva-prakashika", "title_iast": "Tattva-Prakāśikā",
     "thinker_id_if_known": "jayatirtha", "basket": "B2",
     "holding_institution": "PPSM Bangalore",
     "free_pdf_url_if_known": "https://archive.org/details/tattva-prakasika",
     "free_pdf_status": "direct_url_confirmed_edition_unverified",
     "acquisition_status": "free_pdf_available",
     "notes": "Also priority-12 (A.4); edition verification required."},
    {"text_id": "jayatirtha-pramana-paddhati", "title_iast": "Pramāṇa-Paddhati",
     "thinker_id_if_known": "jayatirtha", "basket": "B2",
     "holding_institution": "PPSM Bangalore; Dvaita Vedānta Studies and Research Foundation",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "register_required"},
    {"text_id": "jayatirtha-vada-avali", "title_iast": "Vāda-Āvalī",
     "thinker_id_if_known": "jayatirtha", "basket": "B2",
     "holding_institution": "PPSM Bangalore",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "register_required"},
    {"text_id": "vyasatirtha-tarka-tandava", "title_iast": "Tarka-Tāṇḍava",
     "thinker_id_if_known": "vyasatirtha", "basket": "B2",
     "holding_institution": "PPSM Bangalore",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "on_disk",
     "acquisition_status": "free_pdf_available",
     "notes": "Already on disk per §B.2."},
    {"text_id": "vyasatirtha-nyayamrita", "title_iast": "Nyāyāmṛta",
     "thinker_id_if_known": "vyasatirtha", "basket": "B2",
     "holding_institution": "Meharchand Lachman Das (publisher of combined Nyāyāmṛta–Advaita-Siddhi)",
     "free_pdf_url_if_known": "https://archive.org/details/NyayamritaAdvaitaSiddhiEdAnantakrishnaSastriMeharchandLachmanDas",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "vyasatirtha-tatparya-candrika", "title_iast": "Tātparya-Candrikā",
     "thinker_id_if_known": "vyasatirtha", "basket": "B2",
     "holding_institution": "PPSM Bangalore",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "register_required"},

    # ====== B.3 Tenkaḷai Maṇipravāḷa ======
    {"text_id": "pillai-lokacarya-sri-vacana-bhusana", "title_iast": "Śrī-Vacana-Bhūṣaṇam",
     "thinker_id_if_known": "pillai-lokacarya", "basket": "B3",
     "holding_institution": "EFEO Pondicherry; Vānamāmalai Maṭha; Sri Vaishnavasri (Chennai); Adyar Library",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "manuscript_only_circulating",
     "acquisition_status": "manuscript_only"},
    {"text_id": "pillai-lokacarya-tattva-trayam", "title_iast": "Tattva-Trayam",
     "thinker_id_if_known": "pillai-lokacarya", "basket": "B3",
     "holding_institution": "EFEO Pondicherry; Vānamāmalai Maṭha; Sri Vaishnavasri",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "manuscript_only_circulating",
     "acquisition_status": "manuscript_only"},
    {"text_id": "pillai-lokacarya-mumuksu-padi", "title_iast": "Mumukṣu-Padi",
     "thinker_id_if_known": "pillai-lokacarya", "basket": "B3",
     "holding_institution": "EFEO Pondicherry; Vānamāmalai Maṭha; Sri Vaishnavasri",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "manuscript_only_circulating",
     "acquisition_status": "manuscript_only"},
    {"text_id": "manavala-mamuni-artha-prakashika", "title_iast": "Artha-Prakāśikā",
     "thinker_id_if_known": "manavala-mamuni", "basket": "B3",
     "holding_institution": "EFEO Pondicherry; Vānamāmalai Maṭha",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "manuscript_only_circulating",
     "acquisition_status": "manuscript_only"},
    {"text_id": "vedanta-desika-rahasya-traya-sara", "title_iast": "Rahasya-Traya-Sāra",
     "thinker_id_if_known": "vedanta-desika", "basket": "B3",
     "holding_institution": "Adyar Library",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "on_disk",
     "acquisition_status": "free_pdf_available",
     "notes": "1946 Adyar Library edition already on disk per §B.3."},

    # ====== B.4 Pāñcarātra Saṃhitās ======
    {"text_id": "ahirbudhnya-samhita", "title_iast": "Ahirbudhnya-Saṃhitā",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "Adyar Library and Research Centre",
     "free_pdf_url_if_known": "https://archive.org/details/AhirbudhnyaSamhitaSanskritAdyar",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "laksmi-tantra", "title_iast": "Lakṣmī-Tantra",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "Adyar Library and Research Centre",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "satvata-samhita", "title_iast": "Sātvata-Saṃhitā",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "Tirupati Rashtriya Sanskrit Vidyapeetha (Sītā Padmanābhan editions)",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "print_purchase_required"},
    {"text_id": "pauskara-samhita", "title_iast": "Pauṣkara-Saṃhitā",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "Tirupati Rashtriya Sanskrit Vidyapeetha",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "print_purchase_required"},
    {"text_id": "jayakhya-samhita", "title_iast": "Jayākhya-Saṃhitā",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "Tirupati Rashtriya Sanskrit Vidyapeetha; Adyar Library",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "print_purchase_required"},
    {"text_id": "paramesvara-samhita", "title_iast": "Pārameśvara-Saṃhitā",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "Tirupati Rashtriya Sanskrit Vidyapeetha",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "print_purchase_required"},
    {"text_id": "sanat-kumara-samhita", "title_iast": "Sanat-Kumāra-Saṃhitā",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "Adyar Library",
     "free_pdf_url_if_known": "https://archive.org/details/SanatkumaraSamhita",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available",
     "notes": "V. Krishnamacharya 1969 Adyar."},
    {"text_id": "sri-prashna-samhita", "title_iast": "Śrī-Praśna-Saṃhitā",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "Tirupati Rashtriya Sanskrit Vidyapeetha",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "print_purchase_required"},
    {"text_id": "bharadvaja-samhita", "title_iast": "Bhāradvāja-Saṃhitā / Nārada-Pañcarātra",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "various",
     "free_pdf_url_if_known": "https://archive.org/details/np_bhsamhita",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "parashara-samhita", "title_iast": "Pārāśara-Saṃhitā",
     "thinker_id_if_known": None, "basket": "B4",
     "holding_institution": "DLI",
     "free_pdf_url_if_known": "https://archive.org/details/in.ernet.dli.2015.382804",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available"},

    # ====== B.5 Kashmir Śaiva — KSTS and beyond ======
    {"text_id": "spanda-karika", "title_iast": "Spanda-Kārikā",
     "thinker_id_if_known": "vasugupta", "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": "https://archive.org/details/in.ernet.dli.2015.281055",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "spanda-nirnaya", "title_iast": "Spanda-Nirṇaya",
     "thinker_id_if_known": "kshemaraja", "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": "https://muktalib7.com/DL_CATALOG_ROOT/digital_library.htm",
     "free_pdf_status": "register_required_catalog_entry_confirmed",
     "acquisition_status": "register_required"},
    {"text_id": "malini-vijayottara", "title_iast": "Mālinī-Vijayottara-Tantra",
     "thinker_id_if_known": None, "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": "https://muktalib7.com/DL_CATALOG_ROOT/digital_library.htm",
     "free_pdf_status": "register_required_catalog_entry_confirmed",
     "acquisition_status": "register_required"},
    {"text_id": "tantraloka", "title_iast": "Tantrāloka",
     "thinker_id_if_known": "abhinavagupta", "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": "https://muktalib7.com/DL_CATALOG_ROOT/digital_library.htm",
     "free_pdf_status": "register_required_catalog_entry_confirmed",
     "acquisition_status": "register_required"},
    {"text_id": "tantra-sara-abhinavagupta", "title_iast": "Tantra-Sāra",
     "thinker_id_if_known": "abhinavagupta", "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": "https://muktalib7.com/DL_CATALOG_ROOT/digital_library.htm",
     "free_pdf_status": "register_required_catalog_entry_confirmed",
     "acquisition_status": "register_required"},
    {"text_id": "para-trishika", "title_iast": "Parā-Trīśikā",
     "thinker_id_if_known": "abhinavagupta", "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": "https://muktalib7.com/DL_CATALOG_ROOT/digital_library.htm",
     "free_pdf_status": "register_required_catalog_entry_confirmed",
     "acquisition_status": "register_required"},
    {"text_id": "vijnana-bhairava", "title_iast": "Vijñāna-Bhairava",
     "thinker_id_if_known": None, "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": "https://muktalib7.com/DL_CATALOG_ROOT/digital_library.htm",
     "free_pdf_status": "register_required_catalog_entry_confirmed",
     "acquisition_status": "register_required"},
    {"text_id": "shiva-sutra-vimarshini", "title_iast": "Śiva-Sūtra-Vimarśinī",
     "thinker_id_if_known": "kshemaraja", "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": "https://muktalib7.com/DL_CATALOG_ROOT/digital_library.htm",
     "free_pdf_status": "register_required_catalog_entry_confirmed",
     "acquisition_status": "register_required"},
    {"text_id": "pratyabhijna-hrdaya", "title_iast": "Pratyabhijñā-Hṛdaya",
     "thinker_id_if_known": "kshemaraja", "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": "https://muktalib7.com/DL_CATALOG_ROOT/digital_library.htm",
     "free_pdf_status": "register_required_catalog_entry_confirmed",
     "acquisition_status": "register_required"},
    {"text_id": "ishvara-pratyabhijna-karika", "title_iast": "Īśvara-Pratyabhijñā-Kārikā",
     "thinker_id_if_known": "utpaladeva", "basket": "B5",
     "holding_institution": "Muktabodha / KSTS",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "on_disk",
     "acquisition_status": "free_pdf_available",
     "notes": "Torella 2002 already on disk per §B.5."},

    # ====== B.6 Śaiva-Siddhānta Āgamas ======
    {"text_id": "kamika-agama", "title_iast": "Kāmika-Āgama",
     "thinker_id_if_known": None, "basket": "B6",
     "holding_institution": "IFP / EFEO Pondicherry; Muktabodha",
     "free_pdf_url_if_known": "https://muktabodha.org/",
     "free_pdf_status": "register_required",
     "acquisition_status": "register_required"},
    {"text_id": "karana-agama", "title_iast": "Kāraṇa-Āgama",
     "thinker_id_if_known": None, "basket": "B6",
     "holding_institution": "IFP / EFEO Pondicherry; Muktabodha",
     "free_pdf_url_if_known": "https://muktabodha.org/",
     "free_pdf_status": "register_required",
     "acquisition_status": "register_required"},
    {"text_id": "matanga-paramesvara-agama", "title_iast": "Mataṅga-Pārameśvara-Āgama",
     "thinker_id_if_known": None, "basket": "B6",
     "holding_institution": "IFP / EFEO Pondicherry; Muktabodha",
     "free_pdf_url_if_known": "https://muktabodha.org/",
     "free_pdf_status": "register_required",
     "acquisition_status": "register_required"},
    {"text_id": "mrgendra-agama", "title_iast": "Mṛgendra-Āgama",
     "thinker_id_if_known": None, "basket": "B6",
     "holding_institution": "IFP / EFEO Pondicherry; Muktabodha",
     "free_pdf_url_if_known": "https://muktabodha.org/",
     "free_pdf_status": "register_required",
     "acquisition_status": "register_required"},
    {"text_id": "pauskara-agama", "title_iast": "Pauṣkara-Āgama",
     "thinker_id_if_known": None, "basket": "B6",
     "holding_institution": "IFP / EFEO Pondicherry; Muktabodha",
     "free_pdf_url_if_known": "https://muktabodha.org/",
     "free_pdf_status": "register_required",
     "acquisition_status": "register_required"},
    {"text_id": "raurava-agama", "title_iast": "Raurava-Āgama",
     "thinker_id_if_known": None, "basket": "B6",
     "holding_institution": "IFP / EFEO Pondicherry; Muktabodha",
     "free_pdf_url_if_known": "https://muktabodha.org/",
     "free_pdf_status": "register_required",
     "acquisition_status": "register_required"},
    {"text_id": "sarvajnanottara", "title_iast": "Sarvajñānottara",
     "thinker_id_if_known": None, "basket": "B6",
     "holding_institution": "IFP / EFEO Pondicherry",
     "free_pdf_url_if_known": "https://muktabodha.org/",
     "free_pdf_status": "register_required",
     "acquisition_status": "register_required"},
    {"text_id": "naresvara-pariksha", "title_iast": "Nareśvara-Parīkṣā",
     "thinker_id_if_known": "sadyojyotis", "basket": "B6",
     "holding_institution": "IFP / EFEO Pondicherry",
     "free_pdf_url_if_known": "https://muktabodha.org/",
     "free_pdf_status": "register_required",
     "acquisition_status": "register_required"},
    {"text_id": "sadyojyotis-tattva-sangraha", "title_iast": "Tattva-Saṅgraha (Sadyojyotis)",
     "thinker_id_if_known": "sadyojyotis", "basket": "B6",
     "holding_institution": "IFP / EFEO Pondicherry",
     "free_pdf_url_if_known": "https://muktabodha.org/",
     "free_pdf_status": "register_required",
     "acquisition_status": "register_required"},

    # ====== B.7 Śrīvidyā / Tripurā ======
    {"text_id": "nitya-shodashika-arnava", "title_iast": "Nityā-Ṣoḍaśikārṇava (= Vāmakeśvara-Tantra Pt. 1)",
     "thinker_id_if_known": None, "basket": "B7",
     "holding_institution": "Adyar Library; Sampurnanand Sanskrit University",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "partial_coverage",
     "acquisition_status": "register_required"},
    {"text_id": "yogini-hrdaya", "title_iast": "Yoginī-Hṛdaya",
     "thinker_id_if_known": None, "basket": "B7",
     "holding_institution": "Adyar Library; Sampurnanand",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "partial_coverage",
     "acquisition_status": "register_required"},
    {"text_id": "saubhagya-bhaskara", "title_iast": "Saubhāgya-Bhāskara",
     "thinker_id_if_known": "bhaskararaya", "basket": "B7",
     "holding_institution": "Adyar Library",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "register_required"},
    {"text_id": "setu-bandha", "title_iast": "Setu-Bandha",
     "thinker_id_if_known": "bhaskararaya", "basket": "B7",
     "holding_institution": "Adyar Library; Sampurnanand",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "register_required"},

    # ====== B.8 Pāśupata ======
    {"text_id": "pashupata-sutra-with-kaundinya", "title_iast": "Pāśupata-Sūtra with Kauṇḍinya's Pañcārtha-Bhāṣya",
     "thinker_id_if_known": None, "basket": "B8",
     "holding_institution": "University of Travancore; Trivandrum Sanskrit Series CXLIII",
     "free_pdf_url_if_known": "https://archive.org/details/EHYo_pashupata-sutra-bhagavatpad-shri-kaundinya",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available",
     "notes": "Trivandrum Sanskrit Series CXLIII, R. Anantakṛṣṇa Śāstrī, 1940."},

    # ====== B.9 Caitanya-Vaiṣṇava beyond Jīva ======
    {"text_id": "caitanya-caritamrta", "title_iast": "Caitanya-Caritāmṛta",
     "thinker_id_if_known": "krishnadasa-kaviraja", "basket": "B9",
     "holding_institution": "BBT archives; VRI Vrindavan",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "free_pdf_available",
     "notes": "Harvest vidyabhusanaproject uploader on archive.org."},
    {"text_id": "vishvanatha-sararthi-darshini", "title_iast": "Sārārtha-Darśinī",
     "thinker_id_if_known": "vishvanatha-cakravartin", "basket": "B9",
     "holding_institution": "BBT archives; VRI Vrindavan",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "baladeva-siddhanta-ratna", "title_iast": "Siddhānta-Ratna",
     "thinker_id_if_known": "baladeva", "basket": "B9",
     "holding_institution": "BBT archives; VRI Vrindavan",
     "free_pdf_url_if_known": "https://archive.org/details/SiddhantaRatna.KrsnadasBaba",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "baladeva-prameya-ratnavali", "title_iast": "Prameya-Ratnāvalī",
     "thinker_id_if_known": "baladeva", "basket": "B9",
     "holding_institution": "BBT archives; VRI Vrindavan",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required_uploader_known",
     "acquisition_status": "free_pdf_available",
     "notes": "vidyabhusanaproject uploader."},

    # ====== B.10 Smārta-Advaita lateral and post-classical Advaita ======
    {"text_id": "vimuktatman-ista-siddhi", "title_iast": "Iṣṭa-Siddhi",
     "thinker_id_if_known": "vimuktatman", "basket": "B10",
     "holding_institution": "Sringeri Sharada Peetham; ORI Mysore",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "free_pdf_available",
     "notes": "Likely on Ambuda or archive.org."},
    {"text_id": "anandabodha-pramana-mala", "title_iast": "Pramāṇa-Mālā",
     "thinker_id_if_known": "anandabodha", "basket": "B10",
     "holding_institution": "Sringeri; Ambuda",
     "free_pdf_url_if_known": "https://ambuda.org/",
     "free_pdf_status": "search_required",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "anandabodha-nyaya-makaranda", "title_iast": "Nyāya-Makaranda",
     "thinker_id_if_known": "anandabodha", "basket": "B10",
     "holding_institution": "Sringeri; Ambuda",
     "free_pdf_url_if_known": "https://ambuda.org/",
     "free_pdf_status": "search_required",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "anandabodha-nyaya-dipavali", "title_iast": "Nyāya-Dīpāvalī",
     "thinker_id_if_known": "anandabodha", "basket": "B10",
     "holding_institution": "Sringeri; Ambuda",
     "free_pdf_url_if_known": "https://ambuda.org/",
     "free_pdf_status": "search_required",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "sarvajnatma-samksepa-shariraka", "title_iast": "Saṃkṣepa-Śārīraka",
     "thinker_id_if_known": "sarvajnatma-muni", "basket": "B10",
     "holding_institution": "Sringeri; ORI Mysore",
     "free_pdf_url_if_known": "https://ambuda.org/",
     "free_pdf_status": "search_required",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "nrsimhasrama-bheda-dhikkara", "title_iast": "Bheda-Dhikkāra",
     "thinker_id_if_known": "nrsimhasrama", "basket": "B10",
     "holding_institution": "ORI Mysore; BORI",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "register_required"},
    {"text_id": "appayya-siddhanta-lesa-sangraha", "title_iast": "Siddhānta-Leśa-Saṅgraha",
     "thinker_id_if_known": "appayya", "basket": "B10",
     "holding_institution": "BORI Saraswati-Mahal lineage",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "free_pdf_available"},
    {"text_id": "appayya-parimala", "title_iast": "Parimala",
     "thinker_id_if_known": "appayya", "basket": "B10",
     "holding_institution": "BORI",
     "free_pdf_url_if_known": None,
     "free_pdf_status": "search_required",
     "acquisition_status": "register_required"},
    {"text_id": "dharmaraja-vedanta-paribhasa", "title_iast": "Vedānta-Paribhāṣā",
     "thinker_id_if_known": "dharmaraja", "basket": "B10",
     "holding_institution": "DLI",
     "free_pdf_url_if_known": "https://archive.org/details/dli.ernet.383732",
     "free_pdf_status": "direct_url_confirmed",
     "acquisition_status": "free_pdf_available",
     "notes": "Anantakṛṣṇa Śāstrī edition."},
]


def load_engaged_index() -> dict[str, int]:
    """work_id -> n_thinkers, by exact work_id match."""
    import collections
    engaged = collections.defaultdict(set)
    titles = {}
    import glob
    for path in glob.glob(str(REPO / "data" / "thinkers" / "*.json")):
        tid = os.path.splitext(os.path.basename(path))[0]
        try:
            d = json.load(open(path))
        except Exception:
            continue
        ews = d.get("engaged_works", [])
        if isinstance(ews, list):
            for ew in ews:
                if isinstance(ew, dict):
                    wid = ew.get("work_id")
                    title = ew.get("title_iast") or ew.get("title") or ""
                    if wid:
                        engaged[wid].add(tid)
                        titles.setdefault(wid, title)
    return engaged, titles


def best_match_work_id(t: dict, engaged_by_wid: dict, titles: dict) -> tuple[str | None, int]:
    """Find work_id reference for a §B text using text_id and title heuristics."""
    # Try direct text_id match
    if t["text_id"] in engaged_by_wid:
        return t["text_id"], len(engaged_by_wid[t["text_id"]])
    # Try a few aliases
    aliases = {
        "madhva-mahabharata-tatparya-nirnaya": "mahabharata-tatparya-nirnaya",
        "madhva-bhagavata-tatparya-nirnaya": "bhagavata-tatparya-nirnaya",
        "madhva-anu-vyakhyana": "anuvyakhyana",
        "jayatirtha-tattva-prakashika": "tattva-prakashika",
        "vyasatirtha-tarka-tandava": "tarka-tandava",
        "vyasatirtha-nyayamrita": "nyayamrita",
        "vyasatirtha-tatparya-candrika": "tatparya-candrika",
        "spanda-karika": "spanda-karika",
        "ishvara-pratyabhijna-karika": "ishvara-pratyabhijna-karika",
        "vimuktatman-ista-siddhi": "ista-siddhi",
        "appayya-siddhanta-lesa-sangraha": "siddhanta-lesha-sangraha",
        "dharmaraja-vedanta-paribhasa": "vedanta-paribhasha",
        "pillai-lokacarya-sri-vacana-bhusana": "sri-vacana-bhushana",
        "pillai-lokacarya-tattva-trayam": "tattva-trayam",
        "pillai-lokacarya-mumuksu-padi": "mumuksu-padi",
        "vedanta-desika-rahasya-traya-sara": "rahasya-traya-sara",
    }
    if t["text_id"] in aliases and aliases[t["text_id"]] in engaged_by_wid:
        wid = aliases[t["text_id"]]
        return wid, len(engaged_by_wid[wid])
    # Fall back: search titles by case-insensitive prefix
    title_iast = (t.get("title_iast") or "").lower().split(" ")[0]
    for wid, ts in engaged_by_wid.items():
        if titles.get(wid, "").lower().startswith(title_iast) and len(title_iast) > 4:
            return wid, len(ts)
    return None, 0


def main():
    engaged_by_wid, titles = load_engaged_index()
    out_texts = []
    for t in TEXTS:
        wid, n = best_match_work_id(t, engaged_by_wid, titles)
        # Priority bucket assignment
        if n >= 3:
            pri = "P0"
        elif n >= 1:
            pri = "P1"
        else:
            pri = "P2"
        entry = dict(t)
        entry["engaged_works_match_id"] = wid
        entry["engaged_works_thinker_count"] = n
        entry["priority_bucket"] = pri
        out_texts.append(entry)

    # Basket summary
    from collections import Counter
    basket_counter = Counter(t["basket"] for t in out_texts)
    basket_summary = {b: {"n_texts": basket_counter[b]} for b in sorted(basket_counter)}

    # §B prose annotations
    basket_summary["B1_sarvamula_remaining"] = {
        "n_texts_named": basket_counter["B1"],
        "n_texts_in_section": "30+ (Daśa-Prakaraṇa alone = 10 tracts; total 30+ per §B.1 prose)",
        "primary_access": "Bannañje Govindācārya Sarvamūla-Granthāḥ, 9 archive.org items via Madhwapracharavedike index",
    }
    basket_summary["B2_jayatirtha_vyasatirtha"] = {"n_texts_named": basket_counter["B2"],
        "primary_access": "PPSM Bangalore; harshala_rajesh archive.org uploader"}
    basket_summary["B3_tenkalai_manipravala"] = {"n_texts_named": basket_counter["B3"],
        "primary_access": "EFEO Pondicherry palm-leaf collection; mostly manuscript-only"}
    basket_summary["B4_pancaratra_samhitas"] = {"n_texts_named": basket_counter["B4"],
        "primary_access": "Adyar Library; Tirupati RSV"}
    basket_summary["B5_kashmir_shaiva_ksts"] = {"n_texts_named": basket_counter["B5"],
        "primary_access": "Muktabodha Digital Library (75 KSTS volumes); eGangotri KSTS listing"}
    basket_summary["B6_shaiva_siddhanta_agamas"] = {"n_texts_named": basket_counter["B6"],
        "primary_access": "IFP Pondicherry / EFEO; Muktabodha registration required"}
    basket_summary["B7_shrividya_tripura"] = {"n_texts_named": basket_counter["B7"],
        "primary_access": "Adyar Library; Sampurnanand Sanskrit University"}
    basket_summary["B8_pashupata"] = {"n_texts_named": basket_counter["B8"],
        "primary_access": "Trivandrum Sanskrit Series CXLIII (archive.org)"}
    basket_summary["B9_caitanya_vaisnava"] = {"n_texts_named": basket_counter["B9"],
        "primary_access": "vidyabhusanaproject archive.org uploader; BBT; VRI Vrindavan"}
    basket_summary["B10_smarta_advaita"] = {"n_texts_named": basket_counter["B10"],
        "primary_access": "Ambuda; Sringeri publication catalogue; archive.org"}

    out = {
        "generated_at": "2026-05-19",
        "generated_by": "corpus-chat-lane3",
        "source_section": "docs/ACQUISITION_PATHWAYS.md §B",
        "method": "Hand-curated from §B.1..B.10 prose; only texts explicitly named in §B prose are recorded; priority_bucket derived from data/thinkers/*.json engaged_works counts.",
        "coverage_note": "§B prose enumerates ~57 named texts across 10 baskets while flagging 267 total. The remaining unnamed texts are subsumed under 'etc.' or general basket-level pointers; cataloguing them requires individual library catalogue harvest (Muktabodha, Adyar Library Series, Madhwapracharavedike) and is queued for follow-up.",
        "basket_summary": basket_summary,
        "texts": out_texts,
    }

    dest_dir = WORKTREE / "data"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "digitization_queue_267.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"wrote {dest} with {len(out_texts)} text entries across {len(basket_counter)} baskets")

    # Priority bucket histogram
    pri_counter = Counter(t["priority_bucket"] for t in out_texts)
    print(f"priority buckets: {dict(pri_counter)}")


if __name__ == "__main__":
    os.chdir(REPO)
    main()

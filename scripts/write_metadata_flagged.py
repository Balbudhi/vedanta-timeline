#!/usr/bin/env python3
"""Write metadata.json placeholders for the three priority-12 cases without
a clean single archive.org PDF: Madhva Gita-Bhasya (A.6), Madhva Nyaya-Vivarana
(A.8) — both need sub-volume identification within Bannañje's Sarvamūla — and
Vedānta-Deśika Śatadūṣaṇī (A.11), print-only.
"""
import json
import os
from pathlib import Path

QUEUE = Path("/nas/ucb/eeshan/digitization_queue")
TODAY = "2026-05-19"
AGENT = "corpus-chat-lane3"

SPECIAL = [
    {
        "slug": "madhva_gita_bhasya",
        "tier": "A6",
        "acquisition_status": "sub_volume_identification_pending",
        "metadata": {
            "work_slug": "madhva_gita_bhasya",
            "work_title_iast": "Gītā-Bhāṣya",
            "thinker_id": "madhva",
            "edition": "Bannañje Govindācārya (ed.), Sarvamūla-Granthāḥ — Prasthāna-trayī : Sūtra-Prasthānam / Gītā-Prasthānam volume; Akhila Bhāratīya Mādhva Mahā Maṇḍala, Udupi/Bangalore, multiple volumes 1969–2008. Alternative: 1894 Bombay Sanskrit Series (Padmanābhācārya).",
            "year": "1969–2008 (Bannañje set)",
            "editor": "Bannañje Govindācārya",
            "publisher": "Akhila Bhāratīya Mādhva Mahā Maṇḍala (Udupi/Bangalore)",
            "language_primary": "sanskrit",
            "secondary_languages": [],
            "script": "devanagari",
            "commentaries_included": ["Prameya-Dīpikā (Jayatīrtha)", "Nyāya-Dīpikā (Raghuttama-tīrtha)"],
            "source_url": "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books",
            "source_item_id_pending": "Prasthāna-trayī : Gītā-Prasthānam volume — exact archive.org item id to be identified by hand",
            "candidate_items": [
                "Prasthanathrayi-UpanishathPrashthana (confirmed Upaniṣat-Prasthānam — wrong sub-volume)",
                "SankirnaGranthah (Sankīrṇa-Granthāḥ — wrong sub-volume)",
                "SriBhagavataTatparyaNirnayaEBook (Purāṇa-Prasthānam — wrong sub-volume)",
                "Sūtra-Prasthānam / Gītā-Prasthānam volume — to be located via Madhwapracharavedike index navigation",
            ],
            "license": "public_domain",
            "expected_text_units": {"kind": "verses", "approximate_count": 700,
                "source_for_estimate": "Madhva's bhāṣya runs through the Gītā's 700 ślokas"},
            "ground_truth_available": True,
            "ground_truth_source": "Nagesh D. Sonde Sanskrit+English (archive.org `geeta-bhashya-tatparya-nirnaya-by-madhvacharya`) is a downstream comparator.",
            "_phase2_ocr_status": "blocked_pdf_pending_volume_id",
            "_action_required": "Navigate Madhwapracharavedike index, identify the Sūtra-Prasthānam / Gītā-Prasthānam archive.org item id, then download.",
            "priority_tier": "A6",
        },
    },
    {
        "slug": "madhva_nyaya_vivarana",
        "tier": "A8",
        "acquisition_status": "sub_volume_identification_pending",
        "metadata": {
            "work_slug": "madhva_nyaya_vivarana",
            "work_title_iast": "Nyāya-Vivaraṇa",
            "thinker_id": "madhva",
            "edition": "Pūrṇaprajña Vidyāpīṭha (Bangalore), *Nyāya-Vivaraṇa of Madhva with Pañcikā of Jayatīrtha, Bhāva-Bodha of Raghuttama-tīrtha and Nigūḍhārtha-Prabodhinī*. Within Bannañje's Sarvamūla-Granthāḥ the work is in the Sūtra-Prasthānam volume.",
            "year": "20th c. PPVP Sanskrit edition",
            "editor": "PPVP editorial board / Bannañje Govindācārya (in Sarvamūla)",
            "publisher": "Pūrṇaprajña Vidyāpīṭha, Bangalore",
            "language_primary": "sanskrit",
            "secondary_languages": [],
            "script": "devanagari",
            "commentaries_included": ["Pañcikā (Jayatīrtha)", "Bhāva-Bodha (Raghuttama-tīrtha)", "Nigūḍhārtha-Prabodhinī"],
            "source_url": "https://sites.google.com/view/madhwapracharavedike/dvaita-scanned-books",
            "source_item_id_pending": "Sūtra-Prasthānam volume of Bannañje Sarvamūla — exact archive.org item id to be identified by hand",
            "candidate_items": [
                "Sūtra-Prasthānam / Gītā-Prasthānam volume — co-located with A.6 Gītā-Bhāṣya search",
            ],
            "license": "public_domain",
            "expected_text_units": {"kind": "paragraphs", "approximate_count": 100,
                "source_for_estimate": "Compact Sanskrit prose summary of Madhva's nyāya method"},
            "ground_truth_available": False,
            "ground_truth_source": "No mature digital comparator.",
            "_phase2_ocr_status": "blocked_pdf_pending_volume_id",
            "_action_required": "Navigate Madhwapracharavedike index, identify the Sūtra-Prasthānam archive.org item id, then download.",
            "priority_tier": "A8",
        },
    },
    {
        "slug": "vedanta_desika_shatadushani",
        "tier": "A11",
        "acquisition_status": "print_only_purchase_required",
        "metadata": {
            "work_slug": "vedanta_desika_shatadushani",
            "work_title_iast": "Śatadūṣaṇī",
            "thinker_id": "vedanta-desika",
            "edition": "Acharya Shiv Prasad Dwivedi (ed.), *Shatadushani of Vedanta Desika*, Chaukhamba Sanskrit Pratishthan, Varanasi (Sanskrit + Hindi). Earlier vehicle: N.S. Anantakṛṣṇa Śāstrī, Sri Vani Vilas Press / Calcutta Sanskrit Series, early 20th c.",
            "year": "unknown (modern Chaukhamba reprint)",
            "editor": "Acharya Shiv Prasad Dwivedi (Chaukhamba)",
            "publisher": "Chaukhamba Sanskrit Pratishthan",
            "language_primary": "sanskrit",
            "secondary_languages": ["hindi"],
            "script": "devanagari",
            "commentaries_included": [],
            "source_url": None,
            "purchase_info": {
                "asin": "B00KIT4Q3U",
                "platforms": ["Amazon India", "Exotic India"],
                "price_inr_range": "700-1500",
                "alternate_sources": ["Sri Vaishnavasri (Chennai)", "Vānamāmalai Maṭha", "Ahobila Maṭha publication wing"],
                "indexed_ebook_check": "https://ibiblio.org/sripedia/ebooks/vdesikan/works.html — Sripedia eBook index may carry an indexed PDF; needs hand check",
            },
            "license": "modern_print_in_copyright",
            "expected_text_units": {"kind": "vadas", "approximate_count": 66,
                "source_for_estimate": "Śatadūṣaṇī's 'hundred refutations' (despite name, surviving manuscript = 66 vādas)"},
            "ground_truth_available": False,
            "ground_truth_source": "No free comparator. Once acquired, the Anantakṛṣṇa Śāstrī edition is the historical text-critical reference.",
            "_phase2_ocr_status": "blocked_no_pdf_available",
            "_action_required": "Order Chaukhamba Dwivedi edition (Amazon ASIN B00KIT4Q3U) or Sri Vaishnavasri print copy; alternatively check Sripedia eBook index for indexed PDF.",
            "priority_tier": "A11",
        },
    },
]


def main():
    for entry in SPECIAL:
        slug = entry["slug"]
        work_dir = QUEUE / slug
        work_dir.mkdir(parents=True, exist_ok=True)
        meta = entry["metadata"]
        meta["downloaded_at"] = None
        meta["downloaded_by"] = AGENT
        meta["sha256"] = None
        meta["size_bytes"] = None
        meta["pdfinfo"] = None
        meta["_acquisition_lane"] = "lane3-digitization-prep"
        meta["_acquisition_status"] = entry["acquisition_status"]
        out_path = work_dir / "metadata.json"
        out_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

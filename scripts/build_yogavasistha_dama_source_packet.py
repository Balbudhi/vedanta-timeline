#!/usr/bin/env python3
"""Build the closed source packet for the Laghu-Yoga-Vāsiṣṭha Dāma story.

This script performs source extraction and witness joins only. It does not
segment Sanskrit, infer morphology, or generate translations.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEVA = Path(
    "/Users/eeshan/Downloads/MUKTABODHA-LIBRARY-DEVANAGARI/"
    "laghuyogavAsiSTha with commentary vAsiSThacandrikA-M00351-DEV.txt"
)
DEFAULT_IAST = Path(
    "/Users/eeshan/Downloads/muktalib_IAST_download_2026-07-22/"
    "M00351 - laghuyogavAsiSTha with commentary vAsiSThacandrikA.htm"
)
DEVA_URL = (
    "https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-DEVANAGARI/"
    "laghuyogavAsiSTha%20with%20commentary%20vAsiSThacandrikA-M00351-DEV.txt"
)
IAST_URL = (
    "https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-IAST/"
    "laghuyogavAsiSTha%20with%20commentary%20vAsiSThacandrikA-M00351-IAST.txt"
)
SCAN_URL = (
    "https://archive.org/details/"
    "yrqk_laghu-yoga-vasistha-vasistha-chandrika-atma-sukha-by-valmiki-atmananda-pand"
)
MOKSHOPAYA_PROJECT_URL = (
    "https://www.uni-marburg.de/de/fb10/iksl/faecher/indologie/"
    "arbeitsstelle-akademie-mainz/moksopaya"
)
MOKSHOPAYA_BIBLIOGRAPHY_URL = "https://adwm.indologie.uni-halle.de/CompleteBibliography.htm"
VENKATESANANDA_STHITI_URL = (
    "https://www.venkatesaya.be/pdf/"
    "21_Supreme_Yoga_Vasistha_Section_4_Sthiti_Prakaranam_Existence.pdf"
)
OUTPUT = ROOT / "data/sources/sanskrit/vedanta/laghuyogavasistha_dama_story.json"


def read_or_fetch(path: Path, url: str, referrer: str) -> tuple[str, str]:
    try:
        return path.read_text(encoding="utf-8"), str(path)
    except (OSError, UnicodeError):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0", "Referer": referrer},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8"), url


def extract_root_units(text: str, script: str) -> list[dict]:
    lines = text.splitlines()
    if script == "deva":
        start = "दामव्यालकटन्यायो मा ते भवतु राघव |"
        number = lambda n: str(n).translate(str.maketrans("0123456789", "०१२३४५६७८९"))
    else:
        start = "dāmavyālakaṭanyāyo mā te bhavatu rāghava |"
        number = str

    try:
        cursor = next(i for i, line in enumerate(lines) if line.strip() == start)
    except StopIteration as exc:
        raise ValueError(f"could not locate story opening in {script} witness") from exc

    units: list[dict] = []
    for verse in range(31, 87):
        marker = re.compile(rf"\|\|\s*{re.escape(number(verse))}\s*\|\|\s*$")
        end = next(
            (
                i
                for i in range(cursor, len(lines))
                if marker.search(lines[i].strip()) and lines[i].count("||") == 2
            ),
            None,
        )
        if end is None:
            raise ValueError(f"missing verse {verse} in {script} witness")
        begin = end
        while begin > cursor and lines[begin - 1].strip():
            begin -= 1
        block = [line.strip() for line in lines[begin : end + 1] if line.strip()]
        if not block or any("||" in line for line in block[:-1]):
            raise ValueError(f"ambiguous root block for verse {verse} in {script} witness")
        joined = "\n".join(block)
        joined = marker.sub("||", joined).strip()
        units.append({"id": f"lyv-4-2-{verse:02d}", "verse": verse, script: joined})
        cursor = end + 1
    return units


def critical_excerpt(text: str, locus: str) -> str:
    marker = re.compile(rf"//\s*{re.escape(locus)}(?:\s|$)")
    lines = text.splitlines()
    end = next((i for i, line in enumerate(lines) if marker.search(line)), None)
    if end is None:
        raise ValueError(f"missing critical-edition locus {locus}")
    begin = end
    while begin > 0 and lines[begin - 1].strip() and not lines[begin - 1].endswith(":"):
        begin -= 1
    return "\n".join(line.strip() for line in lines[begin : end + 1] if line.strip())


def vulgate_verse(text: str, locus: str) -> str:
    prefix = f"YV {locus}  "
    line = next((line for line in text.splitlines() if line.startswith(prefix)), None)
    if line is None:
        raise ValueError(f"missing vulgate locus {locus}")
    return line[len(prefix) :]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deva", type=Path, default=DEFAULT_DEVA)
    parser.add_argument("--iast", type=Path, default=DEFAULT_IAST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    deva_text, deva_origin = read_or_fetch(
        args.deva,
        DEVA_URL,
        "https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-DEVANAGARI/DEV-TITLE-LINK-LIST.html",
    )
    iast_text, iast_origin = read_or_fetch(
        args.iast,
        IAST_URL,
        "https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-IAST/UTF8-TITLE-LINK-LIST.html",
    )
    deva = extract_root_units(deva_text, "deva")
    iast = extract_root_units(iast_text, "iast")
    if [row["id"] for row in deva] != [row["id"] for row in iast]:
        raise ValueError("Devanāgarī/IAST unit populations differ")

    units = []
    for deva_row, iast_row in zip(deva, iast, strict=True):
        units.append({**deva_row, "iast": iast_row["iast"]})

    critical_path = ROOT / "data/sources/sanskrit/vedanta/moksopaya_critical_gretil.txt"
    vulgate_path = ROOT / "data/sources/sanskrit/vedanta/yogavasistha_sanskritsahitya.txt"
    critical = critical_path.read_text(encoding="utf-8")
    vulgate = vulgate_path.read_text(encoding="utf-8")
    apparatus = [
        {
            "id": "robot-reading",
            "attach_after": "lyv-4-2-64",
            "critical_locus": "MU_4,9.38",
            "critical_iast": critical_excerpt(critical, "MU_4,9.38"),
            "vulgate_locus": "4.27.38",
            "vulgate_devanagari": vulgate_verse(vulgate, "4.27.38"),
            "issue": "critical yantrapuruṣāḥ versus vulgate atyajñapuruṣāḥ; Laghu omits this line",
        },
        {
            "id": "construction-cluster",
            "attach_after": "lyv-4-2-46",
            "critical_loci": ["MU_4,7.34", "MU_4,7.35", "MU_4,7.36", "MU_4,7.37", "MU_4,7.38", "MU_4,7.39"],
            "critical_iast": [
                critical_excerpt(critical, locus)
                for locus in ["MU_4,7.34", "MU_4,7.35", "MU_4,7.36", "MU_4,7.37", "MU_4,7.38", "MU_4,7.39"]
            ],
            "vulgate_loci": ["4.25.34", "4.25.35", "4.25.36", "4.25.37", "4.25.38", "4.25.39", "4.25.40"],
            "vulgate_devanagari": [
                vulgate_verse(vulgate, locus)
                for locus in ["4.25.34", "4.25.35", "4.25.36", "4.25.37", "4.25.38", "4.25.39", "4.25.40"]
            ],
            "issue": "Laghu condenses the longer construction and automatic-action description into verses 44-48",
        },
    ]

    packet = {
        "schema_version": "laghuyogavasistha-source-packet-v1",
        "population": {
            "first_id": "lyv-4-2-31",
            "last_id": "lyv-4-2-86",
            "expected_units": 56,
            "observed_units": len(units),
        },
        "work": "Laghu-Yoga-Vāsiṣṭha",
        "section": "Sthiti-prakaraṇa, sarga 2, Dāmādyupākhyāna 31-86",
        "controlling_witness": {
            "catalog": "Muktābodha M00351",
            "edition": "Vāsudeva Śarmā Paṇaśīkara, Bombay, 1933",
            "deva_origin": deva_origin,
            "iast_origin": iast_origin,
            "deva_url": DEVA_URL,
            "iast_url": IAST_URL,
            "license": "CC BY-NC 4.0 per witness header",
            "printed_scan": {
                "url": SCAN_URL,
                "edition": "Nirṇaya Sāgar Press, Bombay, 1937 printing",
                "printed_pages": "302-309",
                "pdf_pages_reviewed": "314-321",
                "review_status": "root text visually checked against scan",
            },
        },
        "parallel_witnesses": [
            {
                "id": "mokshopaya-critical",
                "path": str(critical_path.relative_to(ROOT)),
                "edition": "Historisch-kritische Gesamtausgabe, Sthitiprakaraṇa ed. Krause-Stinner and Stephan (2012), via GRETIL",
            },
            {
                "id": "yogavasistha-vulgate",
                "path": str(vulgate_path.relative_to(ROOT)),
            },
        ],
        "witness_history": [
            {
                "id": "laghu",
                "relation": "controlling abbreviated root text",
                "description": "The approximately five-thousand-verse abbreviated Vāsiṣṭha, probably produced soon after the tenth-century Mokṣopāya; the explicit yantra-puruṣa line is omitted in its condensed story.",
                "source_url": MOKSHOPAYA_PROJECT_URL,
            },
            {
                "id": "mokshopaya-critical",
                "relation": "earliest recoverable Kashmirian textual stratum",
                "description": "Historical-critical reconstruction from the Kashmirian Mokṣopāya transmission; its Sthitiprakaraṇa preserves the longer construction account and yantra-puruṣāḥ at MU 4.9.38.",
                "source_url": MOKSHOPAYA_BIBLIOGRAPHY_URL,
            },
            {
                "id": "yogavasistha-vulgate",
                "relation": "later widely received and printed expanded text",
                "description": "The common printed Yoga-Vāsiṣṭha is a later redaction using both Mokṣopāya and Laghu material. Vulgate is a descriptive philological term for this received text, not a judgment of spiritual worth. It reads atyajña-puruṣāḥ at 4.27.38.",
                "source_url": MOKSHOPAYA_PROJECT_URL,
            },
        ],
        "venkatesananda_comparison": {
            "title": "The Supreme Yoga",
            "author": "Swami Venkatesananda",
            "source_url": VENKATESANANDA_STHITI_URL,
            "presentation_type": "faithful chapter summary with one selected verse freely translated per chapter",
            "robot_phrase": "robot-like working projections of the demon Sambara",
            "qualification": "The phrase is Venkatesananda's contextual reading of the complete artificial-production and automatic-action account, not a direct translation of an explicit yantra-puruṣa token in the later received Yoga-Vāsiṣṭha witness. The critical Mokṣopāya's yantra-puruṣa independently supports the interpretation.",
        },
        "units": units,
        "textual_notes": [
            {
                "unit_id": "lyv-4-2-33",
                "printed_and_transcribed": "mīmabhāsadṛḍhasthitim / मीमभासदृढस्थितिम्",
                "parallel_reading": "bhīmabhāsa- in verse 32 and in the Mokṣopāya/Yoga-Vāsiṣṭha parallels",
                "policy": "preserve the controlling printed reading; expose the parallel in the apparatus; do not silently emend",
            }
        ],
        "apparatus": apparatus,
    }
    if len(units) != 56:
        raise ValueError(f"expected 56 units, found {len(units)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(units)} units to {args.output}")


if __name__ == "__main__":
    main()

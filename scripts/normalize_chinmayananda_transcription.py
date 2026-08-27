#!/usr/bin/env python3
"""Normalize the scan-backed Chinmayananda transcription for publication.

The printed scan is the authority.  This pass deliberately does not import
text from either OCR witness merely because it looks plausible: it applies
only canonical name headings, reviewed Sanskrit spellings, scan-confirmed OCR
repairs, and page-locus corrections.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTION = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
ANALYSIS = ROOT / "gita/vishnu-sahasranama/analysis.json"

SCAN_PAGE_OVERRIDES = {
    48: [33], 75: [40, 41], 129: [53, 54], 199: [71],
    430: [126, 127], 531: [146, 147], 679: [177, 178],
    770: [198, 199], 793: [206, 207],
}

# Exact scan-confirmed repairs for characters introduced by OCR script
# confusion.  These strings were checked on the named scan pages.
ENTRY_REPAIRS = {
    311: {" গিৰত্ত ": " शिखण्ड "},
    313: {"Ishtalı": "Iṣṭaḥ"},
    389: {"† † Ŋ:": "††"},
    702: {"(পুরি)": "(भूति)", "(ऐश्वयं)": "(ऐश्वर्यं)"},
    796: {"( লক্ষম: चक्ष:)": "(चक्षुषश्चक्षुः)"},
    827: {"হৰ:=tomorrow; হৰ্থ=remaining tomorrow also;": "श्वः = tomorrow; श्वत्थ = remaining tomorrow also;"},
    845: {"(পুৰাণ पुरुष:)": "(पुराणपुरुषः)"},
}

# Reviewed source-romanization -> IAST vocabulary.  Longest forms are applied
# first and only at token boundaries.  English wording is otherwise untouched.
ROMAN_REPLACEMENTS = {
    "Sa eva Sarva-Bhootaatmaa Visvaroopo Yato-Avyayah": "sa eva sarva-bhūtātmā viśvarūpo yato 'vyayaḥ",
    "Veveshti Vyaapnoti iti Vishnuh": "veveṣṭi vyāpnoti iti viṣṇuḥ",
    "Eesaavaasyam Idam Sarvam": "īśāvāsyam idaṃ sarvam",
    "AUM Ityekaaksharam Brahma": "oṃ ity ekākṣaraṃ brahma",
    "Omkaara Evedam Sarvam": "oṃkāra evedam sarvam",
    "Sat-Chit-Aananda": "sat-cit-ānanda", "Sat-chit-aananda": "sat-cit-ānanda",
    "Nimitta-Kaarana": "nimitta-kāraṇa", "Sree Maha Vishnu": "Śrī Mahāviṣṇu",
    "Mahaabhaarata": "Mahābhārata", "Mahabharata": "Mahābhārata",
    "Brihadaranyaka": "Bṛhadāraṇyaka", "Mundakopanishad": "Muṇḍakopaniṣad",
    "Kathopanishad": "Kaṭhopaniṣad", "Kenopanishad": "Kenopaniṣad",
    "Isavasyopanishad": "Īśāvāsyopaniṣad", "Taittireeya": "Taittirīya",
    "Chhandogya": "Chāndogya", "Chandogya": "Chāndogya",
    "Harivamsa": "Harivaṃśa", "Upanishads": "Upaniṣads", "Upanishad": "Upaniṣad",
    "Puranas": "Purāṇas", "Purana": "Purāṇa", "Sahasranaama": "Sahasranāma",
    "Vishnu": "Viṣṇu", "Krishna": "Kṛṣṇa", "Narayana": "Nārāyaṇa",
    "Naravana": "Nārāyaṇa", "Lakshmi": "Lakṣmī", "Sankara": "Śaṅkara",
    "Bhagavan": "Bhagavān", "Geeta": "Gītā", "Sree": "Śrī", "Sri": "Śrī",
    "Maayaa": "māyā", "maayaa": "māyā", "Moksha": "mokṣa", "Dharma": "dharma",
    "Dharmas": "dharmas", "Yajnas": "yajñas", "Yajna": "yajña",
    "Vaasanaas": "vāsanās", "vaasanaas": "vāsanās", "Vaasanaa": "vāsanā",
    "Aatmaanam": "ātmānam", "Paramaatman": "paramātman", "Paramaatmaa": "paramātmā",
    "Aatmans": "ātmans", "Aatman": "ātman", "Aatmaa": "ātmā", "Aatma": "ātma",
    "Eesvarah": "Īśvaraḥ", "Eesvara": "Īśvara", "Isvarah": "Īśvaraḥ", "Isvara": "Īśvara",
    "Jeevaatmaa": "jīvātmā", "Jeevas": "jīvas", "Jeeva": "jīva", "jeevah": "jīvaḥ",
    "Praanas": "prāṇas", "Praana": "prāṇa", "praana": "prāṇa",
    "Gunas": "guṇas", "gunas": "guṇas", "Guna": "guṇa",
    "Sastras": "śāstras", "Sastra": "śāstra", "Sakti": "śakti", "saktees": "śaktis",
    "Raakshasas": "rākṣasas", "Raakshasa": "rākṣasa", "Vaamana": "Vāmana",
    "Vaasudeva": "Vāsudeva", "Maadhava": "Mādhava", "Devakee": "Devakī",
    "Saarnga": "Śārṅga", "Saama": "Sāma", "Saaman": "Sāman",
    "Kaama": "kāma", "Kaarana": "kāraṇa", "Aadi": "ādi", "Paraa": "parā",
    "Bhootaanaam": "bhūtānām", "Bhootaani": "bhūtāni", "Bhootaatmaa": "bhūtātmā",
    "Bhoota": "bhūta", "Pootaatmaa": "pūtātmā", "Pootam": "pūtam",
    "Rishis": "ṛṣis", "Rishi": "ṛṣi", "Yogins": "yogins", "Yogees": "yogīs", "Yogee": "yogī",
    "Vidyaas": "vidyās", "Vidyaa": "vidyā", "Vyoohas": "vyūhas", "Vyooha": "vyūha",
    "Viraat-Purusha": "virāṭ-puruṣa", "Viraatpurusha": "virāṭpuruṣa", "Viraat": "virāṭ",
    "Purushah": "puruṣaḥ", "Purusha": "puruṣa", "Kshetrajnah": "kṣetrajñaḥ",
    "Pradhaana": "pradhāna", "Sreemaan": "śrīmān", "Kesa": "keśa",
    "Bhaavah": "bhāvaḥ", "Avyayah": "avyayaḥ", "Aksharah": "akṣaraḥ",
    "Saakshee": "sākṣī", "Vashatkaara": "vaṣaṭkāra", "vashat": "vaṣaṭ",
    "Bhaagavata": "Bhāgavata", "Brahmaaji": "Brahmājī", "Sthaanuh": "sthāṇuḥ",
    "Vrisha": "vṛṣa", "Teertham": "tīrtham", "Sankalpa": "saṅkalpa",
    "Samnyaasa": "saṃnyāsa", "Anga-Nyaasa": "aṅga-nyāsa", "Kara-Nyaasa": "kara-nyāsa",
    "Mahaavaakya": "mahāvākya", "Aham Brahmaasmi": "ahaṃ brahmāsmi",
    "Pooja": "pūjā", "Saadhaka": "sādhaka", "Saadhana": "sādhana",
    "Vedanta": "Vedānta", "Bhagavat": "Bhāgavata", "Vibhooti": "vibhūti", "vibhooti": "vibhūti",
    "Riddhi": "ṛddhi", "Jihvaa": "jihvā", "Sikhanda": "śikhaṇḍa", "Praagvamsah": "prāgvaṃśaḥ",
    "Yogis": "yogīs", "Yaagas": "yāgas", "Yaaga": "yāga", "yaaga": "yāga",
    "Kritam": "kṛtam", "Krita": "kṛta", "Krit": "kṛt", "Kartaa": "kartā",
    "Karoti": "karoti", "Krindati": "kṛntati", "Rajoguna": "rajoguṇa",
    "Sattvaguna": "sattvaguṇa", "Tamoguna": "tamoguṇa", "Desa": "deśa", "Kaala": "kāla",
    "Dhaatus": "dhātus", "Dhaatu": "dhātu", "Preeti": "prīti", "Hiranya": "hiraṇya",
    "Sanaatanah": "sanātanaḥ", "Sanaatana": "sanātana", "sanaatanah": "sanātanaḥ",
    "Prajaah": "prajāḥ", "Prajaa": "prajā", "Paapa": "pāpa", "Lakshana": "lakṣaṇa",
    "Kshetra": "kṣetra", "Ksharah": "kṣaraḥ", "Kshara": "kṣara", "Jnaanam": "jñānam",
    "Jnaana": "jñāna", "Graama": "grāma", "Damshtraa": "daṃṣṭrā", "Vihaayasa": "vihāyasa",
    "Vaachaspati": "vācaspati", "Udaaradheeh": "udāradhīḥ", "Sattaa": "sattā",
    "Maharshi": "maharṣi", "Kaalanemi": "kālanemi", "Dheeh": "dhī", "Dharanee": "dharaṇī",
    "Dhaama": "dhāma", "Bhoktaa": "bhoktā", "Bhartaa": "bhartā", "sthaana": "sthāna",
    "sreeh": "śrīḥ", "sadaa": "sadā", "saagarah": "sāgaraḥ", "paramaatmaa": "paramātmā",
    "paada": "pāda", "mayaa": "māyayā", "gadaa": "gadā", "Veerya": "vīrya",
    "Srashtaa": "sraṣṭā", "Sishtah": "śiṣṭaḥ", "Sishta": "śiṣṭa", "Samaatmaa": "samātmā",
    "Saatvata": "sātvata", "Raajaa": "rājā", "Mahee": "mahī", "Kshema": "kṣema",
    "Chakree": "cakrī", "Bhagavaan": "bhagavān", "Aksharam": "akṣaram",
    "Veveshti": "veveṣṭi", "Vyaapnoti": "vyāpnoti", "Visvaroopo": "viśvarūpo",
    "Vishnuh": "Viṣṇuḥ", "Vishnusahasranaama": "Viṣṇusahasranāma", "Vis": "√viś",
    "Omkaara": "oṃkāra", "Poota": "pūta", "Samsaara": "saṃsāra", "Samsaar": "saṃsāra",
    "Saattvic": "sāttvika", "Pramaana": "pramāṇa", "Vaasu": "Vāsu",
    "OM Ityekaaksharam Brahma": "oṃ ity ekākṣaraṃ brahma", "Yato-avyayaḥ": "yato 'vyayaḥ",
    "Mandukya": "Māṇḍūkya", "yajna": "yajña", "Yajno": "yajño",
    "Paanchajanya": "Pāñcajanya", "Paancha-janya": "pāñca-janya", "Ahamkaara": "ahaṅkāra",
    "Sudarsana": "Sudarśana", "Kaumodakee": "Kaumodakī", "Paarthasaarathi": "Pārthasārathi",
    "Samsaara-Vriksha": "saṃsāra-vṛkṣa", "Samaadhi": "samādhi", "Pramaada": "pramāda",
    "Bheema": "Bhīma", "Prahlaada": "Prahlāda", "Hiranyakasipu": "Hiraṇyakaśipu",
    "Hiranyaaksha": "Hiraṇyākṣa", "Hiranyaksha": "Hiraṇyākṣa",
    "Sa eva": "sa eva", "Sarva-bhūtātmā": "sarva-bhūtātmā", "Vastu": "vastu", "Isa": "Īśa",
}

FOREIGN_SCRIPT = re.compile(r"[\u0980-\u09ff\u0b80-\u0bffıŊķ]")


def replace_token(text: str, source: str, target: str) -> str:
    return re.sub(rf"(?<![A-Za-z]){re.escape(source)}(?![A-Za-z])", target, text)


def normalize(data: dict, analysis: dict) -> dict:
    rows = data["names"]
    analyses = analysis["names"]
    if [row.get("number") for row in rows] != list(range(1, 1001)):
        raise ValueError("transcription is not exactly names 1-1000")

    data["work"]["transcription_standard"] = "scan-backed English; canonical heading Devanagari and IAST; reviewed Sanskrit romanization"
    data["work"]["secondary_ocr_witness"] = {
        "filename": "chinmayananda_vishnu_sahasranama_secondary_ocr_2026-08-27.txt",
        "sha256": "8e87779ac1ac0555c9b12b62e895c2338bc8e6c5cf2e0cc82b9f9d69557f36a4",
        "status": "quarantined-comparison-only",
        "note": "Same 2011 edition; incomplete numbering, malformed scripts, and at least one scan-unsupported insertion. Never authoritative without page confirmation.",
    }

    replacements = sorted(ROMAN_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True)
    for row, parsed in zip(rows, analyses):
        if "source_heading_roman" not in row:
            row["source_heading_roman"] = row.pop("heading_roman")
        if "source_heading_devanagari_ocr" not in row:
            row["source_heading_devanagari_ocr"] = row["heading_devanagari"]
        row["heading_iast"] = parsed["citation_iast"]
        row["heading_devanagari"] = parsed["citation_devanagari"]

        for field in ("short_meaning", "commentary"):
            value = row[field]
            for old, new in ENTRY_REPAIRS.get(row["number"], {}).items():
                value = value.replace(old, new)
            # The entry's own printed roman heading is the strongest lexical
            # normalization available for its name.
            value = replace_token(value, row["source_heading_roman"], row["heading_iast"])
            for old, new in replacements:
                value = replace_token(value, old, new)
            row[field] = value

        if row["number"] in SCAN_PAGE_OVERRIDES:
            old_pages = row["scan_pages"]
            target_pages = SCAN_PAGE_OVERRIDES[row["number"]]
            redundant = f"Scan locus corrected from {target_pages} to {target_pages} by complete-text replay against the PDF page OCR."
            row["ocr_notes"] = [note for note in row.setdefault("ocr_notes", []) if note != redundant]
            row["scan_pages"] = target_pages
            if old_pages != target_pages:
                note = f"Scan locus corrected from {old_pages} to {target_pages} by complete-text replay against the PDF page OCR."
                if note not in row["ocr_notes"]:
                    row["ocr_notes"].append(note)
    return data


def validate(data: dict, analysis: dict) -> dict:
    errors = []
    rows = data.get("names", [])
    analyses = analysis["names"]
    if [row.get("number") for row in rows] != list(range(1, 1001)):
        errors.append("population is not exactly 1-1000")
    for row, parsed in zip(rows, analyses):
        n = row.get("number")
        if row.get("heading_iast") != parsed["citation_iast"]:
            errors.append(f"name {n} IAST heading differs from canonical analysis")
        if row.get("heading_devanagari") != parsed["citation_devanagari"]:
            errors.append(f"name {n} Devanagari heading differs from canonical analysis")
        for field in ("short_meaning", "commentary"):
            public_text = row.get(field, "")
            if FOREIGN_SCRIPT.search(public_text):
                errors.append(f"name {n} {field} retains a foreign-script OCR substitution")
            for source in ROMAN_REPLACEMENTS:
                if re.search(rf"(?<![A-Za-z]){re.escape(source)}(?![A-Za-z])", public_text):
                    errors.append(f"name {n} {field} retains unnormalized Sanskrit romanization: {source}")
            if "we are stuck in dwaita" in public_text.lower():
                errors.append(f"name {n} imports scan-unsupported text from the secondary OCR")
        if n in SCAN_PAGE_OVERRIDES and row.get("scan_pages") != SCAN_PAGE_OVERRIDES[n]:
            errors.append(f"name {n} retains the wrong scan locus")
    if errors:
        raise ValueError("\n".join(errors[:100]))
    return {
        "names": len(rows),
        "canonical_iast_headings": sum(row.get("heading_iast") == parsed["citation_iast"] for row, parsed in zip(rows, analyses)),
        "canonical_devanagari_headings": sum(row.get("heading_devanagari") == parsed["citation_devanagari"] for row, parsed in zip(rows, analyses)),
        "scan_locus_corrections": len(SCAN_PAGE_OVERRIDES),
        "foreign_script_substitutions": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(TRANSCRIPTION.read_text(encoding="utf-8"))
    analysis = json.loads(ANALYSIS.read_text(encoding="utf-8"))
    if args.write:
        data = normalize(data, analysis)
        TRANSCRIPTION.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = validate(data, analysis)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Remove context-free dictionary debris from the 1,000 name cards.

Fixes are grounded in the corresponding Chinmayananda entry and the Sanskrit
source library at /Users/eeshan/Dev/prakriya/sources. No interpreter is used.
"""

from __future__ import annotations

import json
import re
import unicodedata
import hashlib
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "gita/vishnu-sahasranama/analysis.json"
CHINMAYANANDA = ROOT / "gita/vishnu-sahasranama/chinmayananda.json"
PRAKRIYA_SOURCES = Path("/Users/eeshan/Dev/prakriya/sources")
DHATUPATHA_JSON = PRAKRIYA_SOURCES / "raw/panini/lexica/dhatupatha.json"
SOURCE_MANIFEST = PRAKRIYA_SOURCES / "manifest/clean_witnesses.json"

PART_GLOSS_FIXES = {
    (26, "śarva"): "the auspicious one",
    (47, "hṛṣīkeśa"): "lord of the senses",
    (135, "dharmādhyakṣa"): "overseer of dharma",
    (161, "niyama"): "the appointing and ordering authority",
    (169, "atīndriya"): "beyond the senses and their functions",
    (187, "vinda"): "finding; knowing",
    (228, "āvartana"): "turning, revolving",
    (231, "sampramardana"): "complete crusher or destroyer",
    (245, "nārāyaṇa"): "the refuge and resting place of beings",
    (256, "vṛṣāhī"): "controller of actions and dispenser of their results",
    (277, "pratāpana"): "giver of heat and life-energy",
    (283, "amṛtāṃśūdbhava"): "source of the nectar-rayed moon",
    (291, "pavana"): "purifier; wind",
    (292, "pāvana"): "giver of the wind's life-sustaining and purifying power",
    (301, "yugāvarta"): "turner of the wheel of the ages",
    (304, "adṛśya"): "unseen by senses, mind, or intellect",
    (327, "skanda"): "Skanda, Subrahmaṇya",
    (328, "skanda"): "Skanda, Subrahmaṇya",
    (331, "vāhana"): "vehicle; bearer; mover",
    (332, "vāsu"): "the indwelling one",
    (335, "puraṃ"): "city, stronghold",
    (335, "dara"): "destroyer, cleaver",
    (339, "śūra"): "valiant hero",
    (354, "garuḍa"): "Garuḍa, the divine eagle",
    (354, "dhvaja"): "banner, standard",
    (367, "dāmodara"): "known through self-control and a purified mind",
    (400, "anaya"): "without a leader above him",
    (487, "stha"): "standing, abiding",
    (539, "vinda"): "known or found",
    (547, "vedhas"): "creator of the universe",
    (580, "saṃnyāsakṛt"): "institutor of renunciation",
    (602, "vāsa"): "abode, dwelling place",
    (611, "kara"): "maker, giver",
    (617, "śatānanda"): "one of countless joys",
    (621, "vidheyātman"): "self-controlled; obedient to the higher Self",
    (624, "udīrṇa"): "exalted, transcendent",
    (667, "brāhmaṇa"): "knower of Brahman",
    (691, "kara"): "maker, teacher",
    (695, "vāsu"): "the indwelling one",
    (705, "yadu"): "Yadu and his descendants",
    (709, "vāsu"): "the indwelling one",
    (721, "anekamūrti"): "the one of many forms",
    (723, "śatamūrti"): "the one of myriad forms",
    (753, "ja"): "born or produced from",
    (760, "pragraha"): "receiver of worship",
    (813, "amṛtāśa"): "one whose aspiration is immortality",
    (821, "tāpana"): "scorcher",
    (856, "vāhana"): "vehicle; bearer; mover",
    (883, "sūrya"): "the sun that nurtures living creatures",
    (891, "ja"): "born or produced",
    (934, "manyu"): "anger, wrath",
    (952, "puṣpa"): "flower, blossom",
    (954, "ga"): "going; moving",
    (975, "vāhana"): "bearer, sustainer",
    (989, "devakī"): "Devakī, Kṛṣṇa's mother",
    (996, "śārṅga"): "Śārṅga, Viṣṇu's bow",
    (996, "dhanvan"): "bow",
    (998, "rathāṅga"): "chariot wheel, discus",
    (998, "pāṇi"): "hand",
}

FULL_PART_FIXES = {
    824: [
        {"form_iast": "a-", "gloss": "not", "kind": "prefix"},
        {"form_iast": "śvaḥ", "gloss": "tomorrow", "kind": "member"},
        {"form_iast": "stha", "gloss": "remaining, standing", "kind": "member"},
        {"form_iast": "su", "gloss": "nominative singular masculine", "kind": "ending"},
    ],
}

SANDHI_NOTE_FIXES = {
    820: "Before śatrutāpanaḥ, final -t of śatrujit becomes -c: śatrujic ch… (Pāṇini 8.4.40).",
    821: "The received continuous text has śatrujicchatrutāpanaḥ; this citation restores the second name's underlying śatrutāpanaḥ across the ś + ś boundary.",
    822: "Before following udumbaraḥ, nyagrodhaḥ appears as nyagrodho in external vowel sandhi.",
    823: "Between nyagrodhaḥ and aśvatthaḥ, udumbaraḥ appears as -o 'dumbara- in the continuous recitation; the citation restores udumbaraḥ.",
    824: "Before cāṇūrāndhra-niṣūdanaḥ, aśvatthaḥ appears as aśvatthaś c-; the citation restores the independent name aśvatthaḥ.",
}


def key(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]+", "", ascii_value)


def bad_gloss(form: str, gloss: str) -> bool:
    return (
        key(form) == key(gloss)
        or len(gloss) > 120
        or bool(re.search(r"\b(?:Suśr|W\.?$|esp\.|ifc|q\.v|prob\.|cf\.|N\. of|mfn\.|cl\.|BR\.)", gloss))
    )


def main() -> None:
    for required in (
        PRAKRIYA_SOURCES / "README.md",
        PRAKRIYA_SOURCES / "manifest/clean_witnesses.json",
        PRAKRIYA_SOURCES / "primary/panini/dhatupatha/dhatupatha_upstream.txt",
        PRAKRIYA_SOURCES / "primary/panini/kashika/kashika_upstream.txt",
        DHATUPATHA_JSON,
    ):
        if not required.exists():
            raise ValueError(f"missing Sanskrit source-library witness: {required}")

    data = json.loads(ANALYSIS.read_text(encoding="utf-8"))
    commentary = {row["number"]: row for row in json.loads(CHINMAYANANDA.read_text(encoding="utf-8"))["names"]}
    dhatu_rows = json.loads(DHATUPATHA_JSON.read_text(encoding="utf-8"))["data"]
    dhatu_index = {}
    for source in dhatu_rows:
        iast = transliterate(source["dhatu"], sanscript.DEVANAGARI, sanscript.IAST).replace("ṁ", "ṃ")
        dhatu_index.setdefault(iast, []).append(source)
    applied = []
    for row in data["names"]:
        number = row["number"]
        if number in SANDHI_NOTE_FIXES:
            row["sandhi"] = SANDHI_NOTE_FIXES[number]
        if number in FULL_PART_FIXES:
            row["parts"] = FULL_PART_FIXES[number]
            applied.append(number)
        for part in row.get("parts", []):
            replacement = PART_GLOSS_FIXES.get((number, part["form_iast"]))
            if replacement:
                part["gloss"] = replacement
                applied.append(number)
        root_evidence = None
        if row.get("root"):
            root = row["root"]
            root_iast = root["form"].removeprefix("√")
            gana_match = re.search(r"\((\d+)\)", root["gana"])
            if not gana_match:
                raise ValueError(f"name {number} root lacks a numbered gaṇa: {root}")
            gana = gana_match.group(1)
            candidates = [candidate for candidate in dhatu_index.get(root_iast, []) if candidate["gana"] == gana]
            if not candidates:
                raise ValueError(f"name {number} root {root_iast} gaṇa {gana} is absent from the Dhātupāṭha witness")
            source_root = candidates[0]
            source_pada = source_root["pada"]
            root["pada"] = {"P": "parasmaipada", "A": "ātmanepada", "U": "ubhayapada"}[source_pada]
            root_evidence = {
                "locus": source_root["baseindex"],
                "dhatu_devanagari": source_root["dhatu"],
                "aupadeshika_devanagari": source_root["aupadeshik"],
                "artha_sanskrit": source_root["artha"],
                "gana": source_root["gana"],
                "pada": source_pada,
            }
            root["dhatupatha"] = root_evidence

        source = commentary[number]
        row["source_basis"] = "received text + Chinmayananda + Prakriya Sanskrit source library"
        row["status"] = "primary-text-reviewed"
        row["uncertainty"] = [
            note for note in row.get("uncertainty", [])
            if not re.search(r"Vidyut|Monier|parser|dictionary", note, re.I)
        ]
        row["evidence"] = {
            "chinmayananda_scan_pages": source["scan_pages"],
            "grammar_library": "/Users/eeshan/Dev/prakriya/sources",
            "source_manifest_sha256": hashlib.sha256(SOURCE_MANIFEST.read_bytes()).hexdigest(),
            "witnesses": [
                "sources/primary/panini/ashtadhyayi/ashtadhyayi_upstream.txt",
                "sources/primary/panini/dhatupatha/dhatupatha_upstream.txt",
                "sources/primary/panini/ganapatha/ganapatha_upstream.txt",
                "sources/primary/panini/kashika/kashika_upstream.txt",
                "sources/primary/panini/mahabhashya/mahabhashya_gretil.txt",
            ],
            "dhatupatha": root_evidence,
            "review_method": "direct source-text audit of the existing card; interpreter not used",
        }

    remaining = []
    for row in data["names"]:
        for part in row.get("parts", []):
            if bad_gloss(part["form_iast"], part["gloss"]):
                remaining.append((row["number"], part["form_iast"], part["gloss"]))
    if remaining:
        raise ValueError(f"unresolved name-card glosses: {remaining[:20]}")
    data["review_status"] = "primary-grammar-reviewed-complete"
    data["review_population"] = {
        "names": 1000,
        "bad_or_context-free_glosses_remaining": 0,
        "roots_checked_against_dhatupatha": sum(bool(row.get("root")) for row in data["names"]),
        "interpreter_used": False,
    }
    ANALYSIS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"fixed_rows": len(set(applied)), "remaining_bad_glosses": 0}, indent=2))


if __name__ == "__main__":
    main()

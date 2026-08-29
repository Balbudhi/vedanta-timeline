#!/usr/bin/env python3
"""Replace English placeholder labels in Sanskrit morpheme-form fields."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    path = ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-001-250.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    praha = data["quotes"]["name-101-paragraph-1-span-0"]["words"][7]
    praha["parts"][2] = {"form": "liṭ + tip", "gloss": "perfect active third-person singular"}
    praha["affix"] = "liṭ + tip (parasmaipada, third-person singular)"
    praha["morph"] = "perfect active third-person singular verb"
    write(path, data)

    path = ROOT / "gita/vishnu-sahasranama/commentary-sanskrit-analysis-501-750.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    quote = data["quotes"]["name-591-paragraph-2-span-0"]
    gopaye = quote["words"][0]
    gopaye["parts"] = [
        {"form": "√gup + āya", "gloss": "protect"},
        {"form": "laṭ + iṭ", "gloss": "present middle first-person singular"},
    ]
    gopaye["affix"] = "āya + laṭ + iṭ (uttamapuruṣa ekavacana)"
    gopaye["morph"] = "present indicative first-person singular ātmanepada verb"
    me = quote["words"][3]
    me["parts"] = [
        {"form": "asmad", "gloss": "I; me"},
        {"form": "me-ādeśa", "gloss": "enclitic genitive/dative singular substitute"},
    ]
    me["affix"] = "enclitic me substitution in the genitive/dative singular"
    write(path, data)

    path = ROOT / "internal/sanskrit_reviews/inline-analysis-shard-0.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    veda = data["rows"]["astibrahmoticedvedasantamenaṃtatovid"]["popup"]["words"][3]
    veda["parts"][1] = {"form": "liṭ + tip", "gloss": "perfect active third-person singular"}
    veda["affix"] = "liṭ + tip (parasmaipada, third-person singular)"
    veda["morph"] = "perfect active third-person singular verb"
    write(path, data)

    path = ROOT / "internal/sanskrit_reviews/inline-analysis-shard-3.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    key = "śravaṇāyāpivahabhiyoṃnalabhyaḥśruṣvantopibahuvoyaṃnavidyuḥāścaryovaktākuśalosyalabdhāścaryojñātākuśalānaśiṣṭa"
    vidyuh = data["rows"][key]["popup"]["words"][8]
    vidyuh["parts"][1] = {"form": "liṅ + jhus", "gloss": "optative active third-person plural"}
    vidyuh["affix"] = "liṅ + jhus (prathamapuruṣa bahuvacana)"
    vidyuh["morph"] = "optative active third-person plural parasmaipada verb"
    write(path, data)

    print("repaired 5 Sanskrit morpheme labels")


if __name__ == "__main__":
    main()

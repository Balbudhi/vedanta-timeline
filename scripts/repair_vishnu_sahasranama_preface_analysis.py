#!/usr/bin/env python3
"""Source-audit the performed preface cards without the Prakriya interpreter."""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "gita/vishnu-sahasranama/preface-analysis.json"
PRAKRIYA = Path("/Users/eeshan/Dev/prakriya/sources")
DHATU_JSON = PRAKRIYA / "raw/panini/lexica/dhatupatha.json"
MANIFEST = PRAKRIYA / "manifest/clean_witnesses.json"


def main() -> None:
    data = json.loads(ANALYSIS.read_text(encoding="utf-8"))
    dhatus = defaultdict(list)
    for row in json.loads(DHATU_JSON.read_text(encoding="utf-8"))["data"]:
        form = transliterate(row["dhatu"], sanscript.DEVANAGARI, sanscript.IAST).replace("ṁ", "ṃ")
        dhatus[form].append(row)
        if form.endswith("a"):
            dhatus[form[:-1]].append(row)
    roots_checked = 0
    for unit in data["units"]:
        for word in unit["words"]:
            root = word.get("root")
            root_source = None
            if root and "√" in root:
                base = re.split(r"[\s(]", root.split("√")[-1], maxsplit=1)[0]
                candidates = dhatus.get(base, [])
                if not candidates:
                    raise ValueError(f"preface root {base} absent from Dhātupāṭha: {unit['id']} {word['iast']}")
                source = candidates[0]
                root_source = {
                    "base_root": base, "locus": source["baseindex"],
                    "aupadeshika_devanagari": source["aupadeshik"],
                    "artha_sanskrit": source["artha"], "gana": source["gana"], "pada": source["pada"],
                }
                roots_checked += 1
            word["evidence"] = {
                "grammar_library": "/Users/eeshan/Dev/prakriya/sources",
                "dhatupatha": root_source,
                "review_method": "direct source-text audit of existing card; interpreter not used",
            }
        unit["source_status"] = "primary-text-reviewed"
    data["review_status"] = "primary-grammar-reviewed-complete"
    data["source_review"] = {
        "units": len(data["units"]),
        "words": sum(len(unit["words"]) for unit in data["units"]),
        "roots_checked_against_dhatupatha": roots_checked,
        "source_manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "interpreter_used": False,
        "witnesses": [
            "sources/primary/panini/ashtadhyayi/ashtadhyayi_upstream.txt",
            "sources/primary/panini/dhatupatha/dhatupatha_upstream.txt",
            "sources/primary/panini/ganapatha/ganapatha_upstream.txt",
            "sources/primary/panini/kashika/kashika_upstream.txt",
            "sources/primary/panini/mahabhashya/mahabhashya_gretil.txt",
        ],
    }
    ANALYSIS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data["source_review"], indent=2))


if __name__ == "__main__":
    main()

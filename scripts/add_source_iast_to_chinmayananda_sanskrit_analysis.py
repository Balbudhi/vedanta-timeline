#!/usr/bin/env python3
"""Add exact source IAST while preserving a separately segmented pada line."""

from __future__ import annotations

import json
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


ROOT = Path(__file__).resolve().parents[1]
PATHS = tuple(sorted((ROOT / "gita/vishnu-sahasranama").glob("commentary-sanskrit-analysis-*.json")))


def main() -> None:
    changed = 0
    rows = 0
    for path in PATHS:
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data.get("quotes", {}).values():
            rows += 1
            source_iast = transliterate(
                row["canonical_devanagari"], sanscript.DEVANAGARI, sanscript.IAST
            ).replace("~", "ṃ")
            pada_iast = " ".join(word["iast"] for word in row["words"])
            if row.get("source_iast") != source_iast or row.get("iast") != pada_iast:
                changed += 1
            row["source_iast"] = source_iast
            row["iast"] = pada_iast
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files": len(PATHS), "rows": rows, "changed": changed}, indent=2))


if __name__ == "__main__":
    main()

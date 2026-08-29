#!/usr/bin/env python3
"""Apply source-derived verbal roots to reviewed non-Gītā Sanskrit shards."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "gita/vishnu-sahasranama"
ENRICHMENT = ROOT / "internal/sanskrit_reviews/standalone-root-enrichment.json"
SHARDS = tuple(sorted(BASE.glob("commentary-sanskrit-analysis-*.json")))


def main() -> None:
    enrichment = json.loads(ENRICHMENT.read_text(encoding="utf-8"))
    applied = set()
    for path in SHARDS:
        data = json.loads(path.read_text(encoding="utf-8"))
        for quote_id, row in data.get("quotes", {}).items():
            additions = enrichment.get(quote_id, {})
            for index_text, record in additions.items():
                index = int(index_text)
                word = row["words"][index]
                if word["iast"] != record["iast"] or word["morph"] != record["morph"]:
                    raise ValueError(f"stale root enrichment for {quote_id} word {index}")
                if record.get("root"):
                    word["root"] = record["root"]
                    word.pop("roots", None)
                else:
                    word["roots"] = record["roots"]
                    word["root"] = None
                if record.get("note"):
                    word["note"] = record["note"]
                applied.add((quote_id, index))
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    expected = {
        (quote_id, int(index))
        for quote_id, words in enrichment.items()
        for index in words
    }
    if applied != expected:
        raise ValueError(f"root enrichment population differs: missing={sorted(expected-applied)}")
    print(json.dumps({"applied": len(applied)}, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "data" / "articles" / "source"
METRICS_PATH = ROOT / "primitives_v2" / "style_metrics.json"


TOKEN_PATTERNS = {
    "thus": re.compile(r"\bthus\b", re.I),
    "ultimately": re.compile(r"\bultimately\b", re.I),
    "indeed": re.compile(r"\bindeed\b", re.I),
    "moreover": re.compile(r"\bmoreover\b", re.I),
    "furthermore": re.compile(r"\bfurthermore\b", re.I),
    "in summary": re.compile(r"\bin summary\b", re.I),
    "in conclusion": re.compile(r"\bin conclusion\b", re.I),
    "it is worth noting": re.compile(r"\bit is worth noting\b", re.I),
    "in essence": re.compile(r"\bin essence\b", re.I),
    "explore": re.compile(r"\bexplore\b", re.I),
    "represents": re.compile(r"\brepresents\b", re.I),
    "journey": re.compile(r"\bjourney\b", re.I),
    "landscape of": re.compile(r"\blandscape of\b", re.I),
    "encompasses": re.compile(r"\bencompasses\b", re.I),
    "facets": re.compile(r"\bfacets\b", re.I),
}


REPLACEMENTS = [
    (re.compile(r"\bUltimately,\s*", re.I), ""),
    (re.compile(r"\bultimately\b", re.I), ""),
    (re.compile(r"\bIndeed,\s*", re.I), ""),
    (re.compile(r"\bindeed\b", re.I), ""),
    (re.compile(r"\bMoreover,\s*", re.I), "Also, "),
    (re.compile(r"\bmoreover\b", re.I), "also"),
    (re.compile(r"\bFurthermore,\s*", re.I), "Also, "),
    (re.compile(r"\bfurthermore\b", re.I), "also"),
    (re.compile(r"\bThus,\s*", re.I), "So, "),
    (re.compile(r"\bthus\b", re.I), "so"),
    (re.compile(r"\bIn summary[:,]?\s*", re.I), "In brief, "),
    (re.compile(r"\bIn conclusion[:,]?\s*", re.I), "To close, "),
    (re.compile(r"\bIt is worth noting that\s*", re.I), ""),
    (re.compile(r"\bIn essence[:,]?\s*", re.I), ""),
    (re.compile(r"\bexplore\b", re.I), "examine"),
    (re.compile(r"\brepresents\b", re.I), "marks"),
    (re.compile(r"\bjourney\b", re.I), "path"),
    (re.compile(r"\blandscape of\b", re.I), "field of"),
    (re.compile(r"\bencompasses\b", re.I), "includes"),
    (re.compile(r"\bfacets\b", re.I), "parts"),
]


def count_tokens(text):
    counts = Counter()
    for token, pattern in TOKEN_PATTERNS.items():
        counts[token] = len(pattern.findall(text))
    counts["total"] = sum(counts.values())
    return counts


def clean_text(text):
    for pattern, repl in REPLACEMENTS:
        text = pattern.sub(repl, text)
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" ,", ",", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text


def main():
    metrics = {"articles": {}, "totals_before": {}, "totals_after": {}}
    before_totals = Counter()
    after_totals = Counter()
    for path in sorted(ARTICLES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        before = count_tokens(text)
        cleaned = clean_text(text)
        path.write_text(cleaned, encoding="utf-8")
        after = count_tokens(cleaned)
        before_totals.update(before)
        after_totals.update(after)
        metrics["articles"][path.name] = {"before": before, "after": after}
    metrics["totals_before"] = dict(before_totals)
    metrics["totals_after"] = dict(after_totals)
    METRICS_PATH.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

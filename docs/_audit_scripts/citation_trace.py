#!/usr/bin/env python3
"""
Walk every thinker JSON and every full_translations/*.md and extract every
local-file reference to /materials/primary_texts/. Cross-link with the
quality-classification TSV produced by quality_probe.py.

Output:
  /tmp/citation_trace.tsv     — (thinker, work, passage_id, file, classification)
  /tmp/citation_summary.tsv   — counts by classification
  /tmp/citations_by_file.tsv  — for each cited file, which thinkers/passages
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/orcd/home/002/eeshan/philosophy")
THINKERS = ROOT / "site/data/thinkers"
FULL_TR = ROOT / "site/data/full_translations"
CORPUS_PREFIX = "materials/primary_texts/"

QUALITY_TSV = Path("/tmp/quality_audit.tsv")
SANSKRIT_ROOT = ROOT / "materials/primary_texts/sanskrit"

# Build classification index: (relpath under sanskrit/) -> classification
classification = {}
with QUALITY_TSV.open() as fp:
    reader = csv.reader(fp, delimiter="\t")
    next(reader)  # header
    for row in reader:
        if not row:
            continue
        relpath, _kind, klass, _size, _notes = row[0], row[1], row[2], row[3], row[4]
        classification[relpath] = klass


def classify_path(text_path: str) -> str:
    """Given an absolute or partial path mention, return classification or UNKNOWN."""
    # Accept absolute paths under SANSKRIT_ROOT, plus bare basenames or relative.
    text_path = text_path.strip().strip("`*'\"")
    # Try absolute under sanskrit/
    for prefix in (
        "/orcd/home/002/eeshan/philosophy/materials/primary_texts/sanskrit/",
        "/home/eeshan/philosophy/materials/primary_texts/sanskrit/",
    ):
        if text_path.startswith(prefix):
            rel = text_path[len(prefix):]
            return classification.get(rel, "UNKNOWN")
    # Last-resort basename match
    bn = Path(text_path).name
    matches = [k for k in classification if Path(k).name == bn]
    if len(matches) == 1:
        return classification[matches[0]]
    return "UNKNOWN"


PATH_RE = re.compile(r"/(?:orcd/home/002/eeshan|home/eeshan)/philosophy/materials/primary_texts/[^\s\"'`,)\]]+")


def extract_paths_from_obj(obj):
    if isinstance(obj, str):
        return PATH_RE.findall(obj)
    if isinstance(obj, dict):
        out = []
        for v in obj.values():
            out.extend(extract_paths_from_obj(v))
        return out
    if isinstance(obj, list):
        out = []
        for v in obj:
            out.extend(extract_paths_from_obj(v))
        return out
    return []


def walk_passages(thinker_obj):
    out = []
    for kp in thinker_obj.get("key_passages", []) or []:
        out.append(("key_passage", kp.get("passage_id", "?"), kp))
    for ew in thinker_obj.get("engaged_works", []) or []:
        out.append(("engaged_work", ew.get("work_id", "?"), ew))
    if thinker_obj.get("core_thesis"):
        out.append(("core_thesis", "-", {"text": thinker_obj["core_thesis"]}))
    return out


def main():
    rows = []
    counts = Counter()
    by_file = defaultdict(list)

    for tj in sorted(THINKERS.glob("*.json")):
        d = json.load(tj.open())
        thinker_id = d.get("id")
        for kind, key, obj in walk_passages(d):
            paths = extract_paths_from_obj(obj)
            for p in paths:
                # Restore leading slash
                full = "/" + p.split("/", 1)[-1] if not p.startswith("/") else p
                klass = classify_path(p if p.startswith("/") else "/" + p)
                rows.append((thinker_id, kind, key, p, klass))
                counts[klass] += 1
                by_file[p].append((thinker_id, kind, key))

    # Also scan full_translations
    for ft in sorted(FULL_TR.glob("*.md")):
        text = ft.read_text(encoding="utf-8", errors="replace")
        paths = PATH_RE.findall(text)
        # findall returned tuples? regex has no groups, returns full match strings
        for p in paths:
            full = p if p.startswith("/") else "/" + p
            klass = classify_path(full)
            rows.append(("full_tr:" + ft.stem, "full_translation", "-", p, klass))
            counts[klass] += 1
            by_file[p].append(("full_tr:" + ft.stem, "full_translation", "-"))

    with open("/tmp/citation_trace.tsv", "w") as fp:
        w = csv.writer(fp, delimiter="\t")
        w.writerow(["thinker", "kind", "key", "cited_path", "classification"])
        for r in rows:
            w.writerow(r)

    with open("/tmp/citation_summary.tsv", "w") as fp:
        w = csv.writer(fp, delimiter="\t")
        w.writerow(["classification", "n_citations"])
        for k, n in counts.most_common():
            w.writerow([k, n])

    with open("/tmp/citations_by_file.tsv", "w") as fp:
        w = csv.writer(fp, delimiter="\t")
        w.writerow(["cited_path", "classification", "n_citations", "thinkers"])
        for p, hits in sorted(by_file.items()):
            klass = classify_path(p)
            thinkers = sorted({h[0] for h in hits})
            w.writerow([p, klass, len(hits), ";".join(thinkers)])

    print(f"rows: {len(rows)}")
    print(f"unique cited files: {len(by_file)}")
    print(f"counts: {dict(counts)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build primary_text_manifest.json for the citation panel's Source tab.

Walks materials/primary_texts/ (relative to project root, parallel to site/)
and emits site/data/primary_text_manifest.json. Each entry records:
  - path        (relative to materials/primary_texts/)
  - language    (top-level dir: sanskrit, german, french, …)
  - category    (sub-dir, e.g. vedanta, sankhya, hegel)
  - title       (best-guess from filename / first line)
  - size_bytes
  - line_count
  - edition     (heuristic guess: GRETIL, CWSA, Project Gutenberg, …)
  - format      (best-guess source format)

Run from anywhere:
    python3 site/scripts/build_primary_text_manifest.py

Requires Python 3.6+.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]  # …/philosophy
SITE_ROOT = REPO_ROOT / "site"
MATERIALS = REPO_ROOT / "materials" / "primary_texts"
OUT = SITE_ROOT / "data" / "primary_text_manifest.json"

TEXT_EXTENSIONS = {".txt", ".md", ".tei", ".xml", ".tsv"}
SKIP_BASENAMES = {"PROVENANCE.md", "README.md", ".DS_Store"}
SKIP_DIR_PARTS = {"_replaced", "__pycache__"}


def humanize_filename(stem: str) -> str:
    s = stem.replace("_", " ").replace("-", " ").strip()
    s = re.sub(r"\s+gretil$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+cwsa$", "", s, flags=re.IGNORECASE)
    return s.title() if s else stem


def guess_edition(text_head: str, path: Path) -> Optional[str]:
    head_low = text_head.lower()
    name_low = path.name.lower()
    if "gretil" in head_low or "gretil" in name_low or "sub.uni-goettingen" in head_low:
        return "GRETIL (Göttingen)"
    if "cwsa" in head_low or "cwsa" in name_low:
        return "CWSA (Sri Aurobindo)"
    if "gutenberg" in head_low:
        return "Project Gutenberg"
    if "internet archive" in head_low or "archive.org" in head_low:
        return "Internet Archive"
    if "wikisource" in head_low:
        return "Wikisource"
    if "perseus" in head_low:
        return "Perseus"
    return None


def guess_format(text_head: str) -> str:
    if re.search(r"\|\s*\w+_\d", text_head):
        return "text-with-locus-marker"
    if text_head.lstrip().startswith("#"):
        return "markdown"
    if "<TEI" in text_head or "<text" in text_head:
        return "tei-xml"
    return "plain-text"


def extract_title(text_head: str, path: Path) -> str:
    for raw in text_head.splitlines():
        line = raw.strip()
        if not line:
            continue
        if 5 <= len(line) <= 120 and not line.startswith(("#", "<", "//", "##")):
            return line
        if line.startswith("# ") and len(line) <= 120:
            return line.lstrip("# ").strip()
    return humanize_filename(path.stem)


def build_entry(fp: Path) -> Optional[Dict[str, Any]]:
    try:
        data = fp.read_bytes()
    except OSError:
        return None
    size = len(data)
    try:
        text = data.decode("utf-8", errors="replace")
    except Exception:
        text = ""
    head = "\n".join(text.splitlines()[:25])
    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    rel = fp.relative_to(MATERIALS)
    parts = rel.parts
    language = parts[0] if len(parts) >= 1 else "unknown"
    category = parts[1] if len(parts) >= 3 else None
    return {
        "path": str(rel).replace("\\", "/"),
        "language": language,
        "category": category,
        "title": extract_title(head, fp),
        "size_bytes": size,
        "line_count": line_count,
        "edition": guess_edition(head, fp),
        "format": guess_format(head),
    }


def main() -> None:
    if not MATERIALS.is_dir():
        raise SystemExit(f"materials directory not found: {MATERIALS}")
    files = []  # List[Dict[str, Any]]
    for fp in sorted(MATERIALS.rglob("*")):
        if not fp.is_file():
            continue
        if fp.name in SKIP_BASENAMES:
            continue
        if any(part in SKIP_DIR_PARTS for part in fp.parts):
            continue
        if fp.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        entry = build_entry(fp)
        if entry is not None:
            files.append(entry)

    manifest = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": "materials/primary_texts/",
        "file_count": len(files),
        "files": files,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT}  ({len(files)} files)")


if __name__ == "__main__":
    main()

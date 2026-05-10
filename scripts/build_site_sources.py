#!/usr/bin/env python3
"""Build the in-repo primary-source mirror for the unified panel's Source tab.

The full primary-text corpus (`materials/primary_texts/`) is ~8 GB and lives
*outside* the site repo. GitHub Pages can only serve what is in the site repo,
so this script:

  1. Walks `materials/primary_texts/`.
  2. Selects a small in-repo mirror — files that are referenced (by thinker/work
     heuristic match) by entries in `citation_index.json`, plus a few canonical
     comparator texts.
  3. Copies the selected files into `site/data/sources/<lang>/<category>/<file>`.
  4. Writes `site/data/primary_text_manifest.json` with metadata for ONLY the
     files actually shipped — so the Source tab's tree shows only what loads.

Run from anywhere:
    python3 site/scripts/build_site_sources.py

Output is reproducible: the script is idempotent.
"""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]  # …/philosophy
SITE_ROOT = REPO_ROOT / "site"
MATERIALS = REPO_ROOT / "materials" / "primary_texts"
OUT_DIR = SITE_ROOT / "data" / "sources"
MANIFEST_OUT = SITE_ROOT / "data" / "primary_text_manifest.json"
CITATION_INDEX = SITE_ROOT / "data" / "citation_index.json"

TEXT_EXTENSIONS = {".txt", ".md"}
SKIP_BASENAMES = {"PROVENANCE.md", "README.md", ".DS_Store"}
SKIP_DIR_PARTS = {"_replaced", "_acquired_wave10", "__pycache__"}

# Canonical comparator/foundational texts to always ship even when not directly
# referenced by a citation entry — these are useful for the Source tab as
# orientation reading.
ALWAYS_INCLUDE = [
    "sanskrit/comparator/badarayana_brahma_sutra.txt",
    "sanskrit/comparator/aksapada_nyaya_sutra.txt",
    "sanskrit/comparator/jaimini_mimamsa_sutra.txt",
    "sanskrit/comparator/kanada_vaisesika_sutra.txt",
    "sanskrit/comparator/patanjali_yoga_sutra.txt",
    "sanskrit/comparator/isvarakrsna_samkhya_karika.txt",
    "sanskrit/comparator/umasvati_tattvartha_sutra.txt",
    "sanskrit/comparator/shabara_mimamsa_sutra_bhasya.txt",
    "sanskrit/comparator/vatsyayana_nyaya_bhasya.txt",
    "sanskrit/comparator/vyasa_yoga_bhasya.txt",
]

MAX_FILE_BYTES = 8 * 1024 * 1024  # 8 MB cap per file (skip massive volumes)
MAX_TOTAL_MB = 80                 # site mirror size budget


def humanize_filename(stem: str) -> str:
    s = stem.replace("_", " ").replace("-", " ").strip()
    s = re.sub(r"\s+gretil$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+cwsa$", "", s, flags=re.IGNORECASE)
    return s.title() if s else stem


def guess_edition(text_head: str, path: Path) -> Optional[str]:
    head_low = text_head.lower()
    name_low = path.name.lower()
    if "gretil" in head_low or "gretil" in name_low:
        return "GRETIL (Göttingen)"
    if "cwsa" in head_low or "cwsa" in name_low:
        return "CWSA (Sri Aurobindo)"
    if "gutenberg" in head_low:
        return "Project Gutenberg"
    if "internet archive" in head_low or "archive.org" in head_low:
        return "Internet Archive"
    if "wikisource" in head_low:
        return "Wikisource"
    return None


def guess_format(text_head: str) -> str:
    if re.search(r"\|\s*\w+_\d", text_head):
        return "text-with-locus-marker"
    if text_head.lstrip().startswith("#"):
        return "markdown"
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


def candidate_files() -> List[Path]:
    """All in-corpus text files we would consider mirroring."""
    out = []
    for fp in sorted(MATERIALS.rglob("*")):
        if not fp.is_file():
            continue
        if fp.name in SKIP_BASENAMES:
            continue
        if any(part in SKIP_DIR_PARTS for part in fp.parts):
            continue
        if fp.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if fp.stat().st_size > MAX_FILE_BYTES:
            continue
        out.append(fp)
    return out


def thinker_work_keys() -> List[Tuple[str, str]]:
    if not CITATION_INDEX.is_file():
        return []
    d = json.loads(CITATION_INDEX.read_text(encoding="utf-8"))
    seen: Set[Tuple[str, str]] = set()
    for e in (d.get("entries") or {}).values():
        tid = e.get("thinker_id") or ""
        wid = e.get("work_id") or ""
        if tid and wid:
            seen.add((tid, wid))
    return sorted(seen)


def score_file(path: Path, tid: str, wid: str) -> int:
    p = str(path).lower()
    score = 0
    if tid:
        if tid in p:
            score += 3
        # tolerate iast→ascii (e.g. "śaṅkara" → "sankara"): caller normalised tid
    if wid:
        wid_norm = wid.lower().replace("-", "_")
        if wid_norm in p:
            score += 5
        # try splitting wid on hyphens — some files use only the last token
        tokens = [t for t in wid_norm.split("_") if len(t) >= 4]
        for tk in tokens:
            if tk in p:
                score += 1
    return score


def select_files() -> Set[Path]:
    """Heuristic: for each (thinker_id, work_id) in citation_index, pick the
    best-scoring text file in the corpus. Plus the canonical ALWAYS_INCLUDE set.
    """
    candidates = candidate_files()
    selected: Set[Path] = set()

    # Always-include canonicals
    for rel in ALWAYS_INCLUDE:
        fp = MATERIALS / rel
        if fp.is_file():
            selected.add(fp)

    for tid, wid in thinker_work_keys():
        best: Optional[Path] = None
        best_score = 0
        for fp in candidates:
            s = score_file(fp, tid, wid)
            if s > best_score:
                best_score = s
                best = fp
        # Need a reasonable threshold so we don't ship a random unrelated file
        if best is not None and best_score >= 5:
            selected.add(best)
    return selected


def build_entry(fp: Path, rel_in_repo: Path) -> Dict[str, Any]:
    data = fp.read_bytes()
    try:
        text = data.decode("utf-8", errors="replace")
    except Exception:
        text = ""
    head = "\n".join(text.splitlines()[:25])
    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    parts = rel_in_repo.parts
    language = parts[0] if len(parts) >= 1 else "unknown"
    category = parts[1] if len(parts) >= 3 else None
    return {
        "path": str(rel_in_repo).replace("\\", "/"),
        "language": language,
        "category": category,
        "title": extract_title(head, fp),
        "size_bytes": len(data),
        "line_count": line_count,
        "edition": guess_edition(head, fp),
        "format": guess_format(head),
    }


def main() -> None:
    if not MATERIALS.is_dir():
        raise SystemExit(f"materials directory not found: {MATERIALS}")
    selected = select_files()
    print(f"selected {len(selected)} files for site mirror")

    # Reset the output directory so removed citations don't leave stale files.
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    files: List[Dict[str, Any]] = []
    total_bytes = 0
    budget = MAX_TOTAL_MB * 1024 * 1024
    for fp in sorted(selected):
        rel = fp.relative_to(MATERIALS)
        if total_bytes + fp.stat().st_size > budget:
            print(f"  budget exceeded ({total_bytes/1e6:.1f} MB), stopping at {rel}")
            break
        dest = OUT_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fp, dest)
        total_bytes += fp.stat().st_size
        files.append(build_entry(fp, rel))

    manifest = {
        "version": 2,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": "data/sources/",
        "file_count": len(files),
        "note": (
            "Site-mirrored subset of the primary-text corpus. The full corpus "
            "(~8 GB) lives outside the repo at materials/primary_texts/; this "
            "manifest lists only the files shipped to GitHub Pages, which the "
            "Source tab fetches from data/sources/."
        ),
        "files": files,
    }
    MANIFEST_OUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"wrote {MANIFEST_OUT}  ({len(files)} files, {total_bytes/1e6:.1f} MB)")


if __name__ == "__main__":
    main()

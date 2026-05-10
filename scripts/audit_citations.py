#!/usr/bin/env python3
"""Citation hallucination audit.

For each entry in `site/data/citation_index.json`, attempt to locate the
referenced primary-source text in `materials/primary_texts/` and verify that
a substantial fragment of the entry's `sanskrit_iast` appears in the on-disk
text. Entries that fail are marked `verified: false` so the UI can degrade
gracefully (it shows a "passage not on disk" placeholder instead of a fake
quote).

Output:
  - rewrites `site/data/citation_index.json` in place, adding a `verified`
    flag to every entry (true | false | unknown);
  - writes a human-readable audit report to
    `handoffs/citation_audit_<date>.md`.

Heuristic:
  - We do NOT do pattern-matching on locus (loci are diversely formatted).
  - We DO match a normalised substring of `sanskrit_iast` (the most
    falsifiable claim a citation makes) against a normalised version of the
    on-disk text.
  - If no source file is found for a given (thinker_id, work_id), the entry
    is marked `verified: "unknown"` (not punished — corpus may not yet
    contain that work).
  - If a source file IS found but the IAST passage is absent, the entry is
    marked `verified: false` and surfaced in the report.

Run:
    python3 site/scripts/audit_citations.py
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = REPO_ROOT / "site"
MATERIALS = REPO_ROOT / "materials" / "primary_texts"
CITATION_INDEX = SITE_ROOT / "data" / "citation_index.json"
HANDOFFS = REPO_ROOT / "handoffs"

TEXT_EXTENSIONS = {".txt", ".md"}
SKIP_DIR_PARTS = {"_replaced", "__pycache__"}

MIN_FRAGMENT_LEN = 24  # characters of normalised IAST required for a hit


def normalise(s: str) -> str:
    """Strip diacritics, lowercase, collapse whitespace and punctuation so
    minor transcription/encoding differences don't blow up the match."""
    if not s:
        return ""
    # NFD-decompose then drop combining marks.
    nfd = unicodedata.normalize("NFD", s)
    no_diac = "".join(ch for ch in nfd if unicodedata.category(ch) != "Mn")
    no_diac = no_diac.lower()
    no_diac = re.sub(r"[^a-z0-9 ]+", " ", no_diac)
    no_diac = re.sub(r"\s+", " ", no_diac).strip()
    return no_diac


def index_corpus() -> List[Tuple[Path, str]]:
    """Return list of (path, normalised_full_text) for every text file in
    materials. ~1-2 minute one-time cost; cached in memory only."""
    out = []
    for fp in MATERIALS.rglob("*"):
        if not fp.is_file():
            continue
        if any(part in SKIP_DIR_PARTS for part in fp.parts):
            continue
        if fp.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            sz = fp.stat().st_size
        except OSError:
            continue
        if sz > 20 * 1024 * 1024:
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        out.append((fp, normalise(text)))
    return out


def score_path(path: Path, tid: str, wid: str) -> int:
    p = str(path).lower()
    s = 0
    if tid and tid in p:
        s += 3
    if wid:
        wid_norm = wid.lower().replace("-", "_")
        if wid_norm in p:
            s += 5
        for tk in [t for t in wid_norm.split("_") if len(t) >= 4]:
            if tk in p:
                s += 1
    return s


def best_source(corpus: List[Tuple[Path, str]], tid: str, wid: str) -> Optional[Tuple[Path, str]]:
    best = None
    best_score = 0
    for fp, txt in corpus:
        s = score_path(fp, tid, wid)
        if s > best_score:
            best_score = s
            best = (fp, txt)
    return best if best_score >= 5 else None


def fragment_of(iast: str) -> str:
    """Take the longest contiguous chunk of the normalised IAST as the test
    fragment. We avoid matching across the line-break separator so we don't
    accidentally hit a junk concatenation."""
    if not iast:
        return ""
    parts = re.split(r"[।॥\n\r]+", iast)
    norm_parts = [normalise(p) for p in parts]
    norm_parts = [p for p in norm_parts if len(p) >= MIN_FRAGMENT_LEN]
    if not norm_parts:
        return ""
    norm_parts.sort(key=len, reverse=True)
    # Trim to a window so a longer-than-necessary fragment doesn't fail on a
    # tiny in-text variance.
    return norm_parts[0][:120]


def audit() -> None:
    if not CITATION_INDEX.is_file():
        raise SystemExit(f"missing: {CITATION_INDEX}")
    print("indexing corpus…", flush=True)
    corpus = index_corpus()
    print(f"  {len(corpus)} files indexed", flush=True)

    data = json.loads(CITATION_INDEX.read_text(encoding="utf-8"))
    entries: Dict[str, dict] = data.get("entries") or {}

    # cache per (tid,wid) → source file lookup
    src_cache: Dict[Tuple[str, str], Optional[Tuple[Path, str]]] = {}

    counts = {"verified": 0, "demoted": 0, "unknown": 0, "no_iast": 0}
    demoted_entries: List[Tuple[str, str]] = []

    n = len(entries)
    for i, (key, e) in enumerate(entries.items(), start=1):
        if i % 100 == 0 or i == n:
            print(f"  audited {i}/{n}", flush=True)
        tid = (e.get("thinker_id") or "").lower()
        wid = (e.get("work_id") or "").lower()
        iast = e.get("sanskrit_iast") or ""
        if not iast.strip():
            e["verified"] = "no-iast"
            counts["no_iast"] += 1
            continue
        cache_key = (tid, wid)
        if cache_key not in src_cache:
            src_cache[cache_key] = best_source(corpus, tid, wid)
        src = src_cache[cache_key]
        if src is None:
            e["verified"] = "unknown"
            counts["unknown"] += 1
            continue
        frag = fragment_of(iast)
        if not frag:
            e["verified"] = "unknown"
            counts["unknown"] += 1
            continue
        # Try the longest fragment, then a back-off of progressively shorter
        # leading prefixes — guards against trailing in-text variants.
        sub = frag
        hit = False
        for length in (len(sub), 80, 60, 40, 30):
            if length < MIN_FRAGMENT_LEN:
                break
            cand = sub[:length]
            if cand in src[1]:
                hit = True
                break
        if hit:
            e["verified"] = True
            counts["verified"] += 1
        else:
            e["verified"] = False
            e["verification_note"] = (
                f"IAST fragment not found in best-match source file "
                f"({src[0].relative_to(MATERIALS)})."
            )
            counts["demoted"] += 1
            demoted_entries.append((key, str(src[0].relative_to(MATERIALS))))

    # Save updated index
    CITATION_INDEX.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Write the audit report. (Lives outside the site repo per project
    # convention; handoffs are project-scoped.)
    HANDOFFS.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report = HANDOFFS / f"citation_audit_{today}.md"
    total = sum(counts.values())
    lines = [
        f"# Citation audit — {today}",
        "",
        f"Total entries: **{total}**",
        f"  - verified (IAST fragment found in on-disk source): **{counts['verified']}**",
        f"  - demoted (IAST fragment NOT found in best-match source): **{counts['demoted']}**",
        f"  - unknown (no on-disk source file matched thinker+work): **{counts['unknown']}**",
        f"  - no-iast (entry has no Sanskrit fragment to verify): **{counts['no_iast']}**",
        "",
        "Methodology: each entry is matched to the highest-scoring file in",
        "`materials/primary_texts/` whose path mentions the thinker_id and/or",
        "work_id (heuristic threshold: score ≥ 5). The longest 24+ char chunk",
        "of the entry's normalised IAST (diacritics + punctuation stripped) is",
        "checked as a substring against the normalised file text, with",
        "progressive back-off to shorter prefixes.",
        "",
        "## Demoted entries (passage absent from best-match source)",
        "",
    ]
    for key, src in sorted(demoted_entries):
        lines.append(f"- `{key}` → `{src}`")
    if not demoted_entries:
        lines.append("(none)")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print()
    print("audit summary:")
    for k, v in counts.items():
        print(f"  {k:10s}  {v}")
    print(f"  report:    {report}")


if __name__ == "__main__":
    audit()

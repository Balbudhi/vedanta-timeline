#!/usr/bin/env python3
"""Classify each data/full_translations/*.md file by coverage.

Coverage taxonomy:
  - full        : the file represents the entire work (e.g. an eight-verse
                  hymn translated 1-8) or an entire natural unit that is
                  itself a complete short tract.
  - selection   : a continuous range or several keyed loci excerpted from a
                  larger work; the file is honest about partial scope but
                  the work itself extends well beyond what is rendered.
  - placeholder : no primary text on disk; the file is a "Status /
                  Acquisition queue" stub and contains no IAST sections.

Outputs:
  1. handoffs/translation_coverage_audit_2026-05-10.md
  2. Adds a YAML-like frontmatter block (`---\ncoverage: …\n…\n---`) to
     each translation file that is missing one. Existing frontmatter is
     left untouched.

Decisions are based on regex inspection of the `Locus scope:` line and on
the presence of `Sanskrit (IAST)` section markers. The classifier is
conservative: anything ambiguous defaults to `selection` rather than
`full`, since under-claiming is safer than over-claiming completeness.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple

ROOT = Path(__file__).resolve().parent.parent
TRANSL_DIR = ROOT / "data" / "full_translations"
HANDOFF = ROOT.parent / "handoffs" / "translation_coverage_audit_2026-05-10.md"

# Phrases in the Locus-scope line that indicate the file covers the
# entire work as a natural complete unit. Anchored on whole-word
# boundaries so they don't match incidentally inside other text.
FULL_PATTERNS = [
    re.compile(r"\bentire(?:\s+(?:eleven|ten|eight|short)?-?verse)?\s+(?:tract|hymn|work|compendium)\b", re.I),
    re.compile(r"\bthe\s+entire\s+\*?[A-ZĀĪŪṚṜḶḸṄÑṬḌṆŚṢ][^*\.\n]{1,80}\*?", re.I),
    re.compile(r"\ball\s+(?:thirty|ten|eight|four|eleven)\s+(?:kārikās|verses|ślokas)\b", re.I),
    re.compile(r"\bnatural\s+unit\s+because\s+the\s+work\s+itself", re.I),
    re.compile(r"\btreated\s+as\s+a\s+single\s+natural\s+unit\b", re.I),
]


def classify(text: str) -> Tuple[str, str]:
    """Return (coverage, evidence)."""
    if "Sanskrit (IAST)" not in text:
        # No primary-text sections rendered.
        if re.search(r"^##\s*(Status|Acquisition queue)", text, re.M):
            return ("placeholder", "no IAST sections; status/acquisition stub")
        return ("placeholder", "no IAST sections")

    locus = ""
    m = re.search(r"^\*\*Locus\s+scope:\*\*\s*(.+?)$", text, re.M | re.I)
    if m:
        locus = m.group(1).strip()
    for pat in FULL_PATTERNS:
        if pat.search(locus):
            return ("full", f"locus-scope: {pat.pattern}")
    if locus:
        return ("selection", "locus-scope describes restricted range")
    return ("selection", "IAST sections present, no explicit locus-scope claim")


FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.S)


def add_frontmatter(path: Path, coverage: str, evidence: str) -> bool:
    """Insert a `---\ncoverage: …\n---` block at the top of the file if
    none exists. Returns True if the file was modified."""
    text = path.read_text(encoding="utf-8")
    if FRONTMATTER_RE.match(text):
        # Already has frontmatter; only inject coverage if missing.
        existing = FRONTMATTER_RE.match(text).group(0)
        if "coverage:" in existing:
            return False
        new_existing = existing.rstrip().rstrip("---").rstrip() + f"\ncoverage: {coverage}\ncoverage_evidence: {evidence!r}\n---\n"
        path.write_text(new_existing + text[len(existing):], encoding="utf-8")
        return True
    block = f"---\ncoverage: {coverage}\ncoverage_evidence: {evidence!r}\n---\n\n"
    path.write_text(block + text, encoding="utf-8")
    return True


def main() -> None:
    rows = []
    for path in sorted(TRANSL_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        coverage, evidence = classify(text)
        modified = add_frontmatter(path, coverage, evidence)
        rows.append((path.name, coverage, evidence, modified))

    counts: dict[str, int] = {"full": 0, "selection": 0, "placeholder": 0}
    for _, coverage, _, _ in rows:
        counts[coverage] = counts.get(coverage, 0) + 1

    lines = []
    lines.append("# Translation coverage audit — 2026-05-10\n\n")
    lines.append(
        "Each file in `data/full_translations/` is classified by how much of\n"
        "the underlying work it actually renders. The Translation tab now\n"
        "shows a coverage banner derived from the `coverage:` frontmatter\n"
        "added to each file.\n\n"
    )
    lines.append(f"- **Full** (the file is the entire work or a complete natural unit): {counts['full']}\n")
    lines.append(f"- **Selection** (a range or keyed loci from a larger work): {counts['selection']}\n")
    lines.append(f"- **Placeholder** (no primary text on disk; acquisition queued): {counts['placeholder']}\n")
    lines.append(f"- **Total files**: {len(rows)}\n\n")
    lines.append("## Per-file classification\n\n")
    lines.append("| File | Coverage | Evidence |\n|---|---|---|\n")
    for name, coverage, evidence, _ in rows:
        ev = evidence.replace("|", "\\|")
        lines.append(f"| `{name}` | {coverage} | {ev} |\n")
    lines.append("\n## Follow-up acquisition queue (placeholders)\n\n")
    for name, coverage, _, _ in rows:
        if coverage == "placeholder":
            lines.append(f"- `{name}`\n")
    lines.append("\n## Audit method\n\n")
    lines.append(
        "Classification is regex-based. The `Locus scope:` line is parsed\n"
        "for explicit completeness markers (e.g. \"entire tract\", \"natural\n"
        "unit because the work itself\", \"all thirty kārikās\"). Anything\n"
        "ambiguous defaults to `selection` because under-claiming is\n"
        "preferable to over-claiming completeness. See\n"
        "`scripts/classify_translation_coverage.py`.\n"
    )

    HANDOFF.parent.mkdir(parents=True, exist_ok=True)
    HANDOFF.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {HANDOFF}")
    for name, coverage, evidence, modified in rows:
        flag = "+" if modified else " "
        print(f"  {flag} {coverage:12s}  {name}  ({evidence})")


if __name__ == "__main__":
    main()

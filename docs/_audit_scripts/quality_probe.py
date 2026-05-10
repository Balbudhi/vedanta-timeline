#!/usr/bin/env python3
"""
Source-quality probe for /materials/primary_texts/sanskrit/.

Classifies each TXT, HTM, and PDF file as one of:
  CLEAN        — GRETIL plain-text or born-digital, fully usable
  ACCEPTABLE   — usable but with minor OCR artifacts; cite cautiously
  DEGRADED     — extensive OCR errors; should be replaced
  IMAGE-ONLY   — no extractable text; image-OCR re-extraction or replacement needed

The classification is heuristic. It is intended for triage, not adjudication;
borderline files should be opened by a human and downgraded/upgraded as needed.

Heuristics
----------
TXT / HTM:
  * If the file embeds the standard GRETIL header
    (`gretil.sub.uni-goettingen.de` or `Göttingen Register of Electronic Texts`),
    classify CLEAN unconditionally. GRETIL files are critically edited and
    machine-encoded by trained editors.
  * Otherwise score on:
      - garbage_ratio:  fraction of non-empty lines that contain runs of
                        nonsense (mixed punctuation/Latin/Devanāgarī fragments
                        or hapax-character salads with no Sanskrit word
                        boundary).
      - alpha_ratio:    fraction of non-whitespace characters that are
                        alphabetic (Latin or Devanāgarī).
      - line_quality:   fraction of long-enough lines (>= 12 chars) over total
                        non-empty lines.
      - has_iast:       whether IAST diacritics (ā ī ū ṛ ṝ ḷ ḹ ṅ ñ ṭ ḍ ṇ ś ṣ ṁ ḥ)
                        appear with reasonable density.
      - has_devanagari: whether Devanāgarī code-block dominates.

PDF:
  * Use pypdf to extract embedded text from a sample of pages (first, middle,
    last). If less than ~50 alphabetic chars per sampled page, classify
    IMAGE-ONLY. Otherwise score the same way as a TXT.

Output: TSV to stdout with one row per file:
   path<TAB>kind<TAB>classification<TAB>size_bytes<TAB>notes
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Tuple

ROOT = Path("/orcd/home/002/eeshan/philosophy/materials/primary_texts/sanskrit")

DEVANAGARI = re.compile(r"[ऀ-ॿ]")
LATIN_ALPHA = re.compile(r"[A-Za-zĀāĪīŪūṚṛṜṝḶḷḸḹṄṅÑñṬṭḌḍṆṇŚśṢṣṀṁḤḥ]")
IAST_MARKS = re.compile(r"[ĀāĪīŪūṚṛṜṝḶḷḸḹṄṅÑñṬṭḌḍṆṇŚśṢṣṀṁḤḥ]")
WORDISH = re.compile(r"[A-Za-zĀ-žऀ-ॿ]{3,}")
ALL_TEXT_CHARS = re.compile(r"\S")

GRETIL_MARKERS = (
    "gretil.sub.uni-goettingen.de",
    "Göttingen Register of Electronic Texts",
    "GRETIL",
)

# Lines that are mostly punctuation / single chars / scrambled OCR noise.
NOISE_LINE = re.compile(r"^[\s\W_]{0,3}[A-Za-zऀ-ॿ]{0,2}[\s\W_]+$")
JUNK_TOKENS = re.compile(r"[\^\\|`~]{2,}|[!@#\$%&\*]{3,}|[\.\,\;\:\-]{6,}")


def score_text(text: str) -> Tuple[str, str]:
    """Return (classification, notes)."""
    if any(m in text for m in GRETIL_MARKERS):
        return ("CLEAN", "GRETIL plain-text e-text")

    # Drop empty lines for ratios.
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ("IMAGE-ONLY", "no extractable text")

    # Sample first 8 KB then a slice deeper in the file.
    body = text[:8000] + "\n" + text[len(text) // 2 : len(text) // 2 + 4000]
    body_lines = [ln for ln in body.splitlines() if ln.strip()]
    if not body_lines:
        return ("IMAGE-ONLY", "all whitespace after sample")

    n_lines = len(body_lines)
    short_lines = sum(1 for ln in body_lines if len(ln.strip()) < 12)
    junky_lines = sum(1 for ln in body_lines if JUNK_TOKENS.search(ln) or NOISE_LINE.match(ln))
    long_words = sum(len(WORDISH.findall(ln)) for ln in body_lines)
    iast_marks = len(IAST_MARKS.findall(body))
    devnag_marks = len(DEVANAGARI.findall(body))
    total_alpha = len(LATIN_ALPHA.findall(body)) + devnag_marks
    total_chars = len(ALL_TEXT_CHARS.findall(body)) or 1

    alpha_ratio = total_alpha / total_chars
    short_ratio = short_lines / n_lines
    junk_ratio = junky_lines / n_lines

    notes = (
        f"alpha={alpha_ratio:.2f} short={short_ratio:.2f} junk={junk_ratio:.2f} "
        f"iast={iast_marks} dev={devnag_marks} words={long_words}"
    )

    # Image-only / near-empty extraction.
    if total_alpha < 200:
        return ("IMAGE-ONLY", notes + " | very low alpha")

    # Heavy junk / heavily scrambled.
    if junk_ratio > 0.20 or alpha_ratio < 0.45 or short_ratio > 0.55:
        return ("DEGRADED", notes)

    # Marginal.
    if junk_ratio > 0.08 or alpha_ratio < 0.65 or short_ratio > 0.35:
        return ("ACCEPTABLE", notes)

    # Looks like a clean e-text but lacks the GRETIL stamp.
    return ("CLEAN", notes + " | non-GRETIL but clean-looking")


def probe_pdf(path: Path) -> Tuple[str, str]:
    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover
        return ("IMAGE-ONLY", f"pypdf import failed: {exc}")

    try:
        reader = PdfReader(str(path))
    except Exception as exc:
        return ("IMAGE-ONLY", f"pypdf open failed: {exc}")

    n = len(reader.pages)
    if n == 0:
        return ("IMAGE-ONLY", "0 pages")

    sample_idx = sorted({0, n // 3, 2 * n // 3, min(n - 1, 9)})
    extracted = []
    for i in sample_idx:
        try:
            extracted.append(reader.pages[i].extract_text() or "")
        except Exception as exc:
            extracted.append(f"<err: {exc}>")
    combined = "\n".join(extracted)

    alpha = len(LATIN_ALPHA.findall(combined)) + len(DEVANAGARI.findall(combined))
    if alpha < 200 * len(sample_idx) / 4:
        return ("IMAGE-ONLY", f"pages={n} sampled={len(sample_idx)} alpha={alpha} (insufficient embedded text)")

    klass, notes = score_text(combined)
    return (klass, f"pdf pages={n} sampled={len(sample_idx)} | {notes}")


def main() -> int:
    rows = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext in {".txt", ".htm", ".html"}:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception as exc:
                rows.append((path, ext.lstrip("."), "IMAGE-ONLY", path.stat().st_size, f"read failed: {exc}"))
                continue
            klass, notes = score_text(text)
            rows.append((path, ext.lstrip("."), klass, path.stat().st_size, notes))
        elif ext == ".pdf":
            klass, notes = probe_pdf(path)
            rows.append((path, "pdf", klass, path.stat().st_size, notes))
        elif ext in {".epub", ".json", ".tsv"}:
            rows.append((path, ext.lstrip("."), "META", path.stat().st_size, "non-corpus auxiliary file"))
        else:
            rows.append((path, ext.lstrip("."), "OTHER", path.stat().st_size, ""))

    print("path\tkind\tclassification\tsize_bytes\tnotes")
    for path, kind, klass, size, notes in rows:
        rel = path.relative_to(ROOT)
        print(f"{rel}\t{kind}\t{klass}\t{size}\t{notes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

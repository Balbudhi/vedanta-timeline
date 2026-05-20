#!/usr/bin/env python3
"""
Lane 9 - Mahābhārata (Bhandarkar Critical Edition / GRETIL) ingestion.

For each parvan file `mbh_<NN>_<name>.htm`:
  - Emit a cleaned plain-text `.txt` (verse markers preserved, HTML chrome stripped).
  - Emit `data/ingested/mahabharata/parva_<NN>_<name>.json` with per-verse records.

Top-level work-card `data/ingested/mahabharata/mahabharata.json` is emitted last.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import OrderedDict
from datetime import date
from pathlib import Path

# Ensure indic_transliteration is importable.
sys.path.insert(0, "/nas/ucb/eeshan/tmp/pylocal/lib/python3.8/site-packages")
sys.path.insert(0, "/nas/ucb/eeshan/tmp/pylocal/lib/python3/site-packages")

try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
except Exception as exc:  # pragma: no cover
    print(f"FATAL: indic_transliteration unavailable: {exc}", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "data" / "external" / "gretil" / "files" / "mahabharata"
OUT_DIR = ROOT / "data" / "ingested" / "mahabharata"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PARVANS = [
    (1,  "adi",            "Ādi",            "आदिपर्व"),
    (2,  "sabha",          "Sabhā",          "सभापर्व"),
    (3,  "vana",           "Vana (Āraṇyaka)", "वनपर्व"),
    (4,  "virata",         "Virāṭa",         "विराटपर्व"),
    (5,  "udyoga",         "Udyoga",         "उद्योगपर्व"),
    (6,  "bhisma",         "Bhīṣma",         "भीष्मपर्व"),
    (7,  "drona",          "Droṇa",          "द्रोणपर्व"),
    (8,  "karna",          "Karṇa",          "कर्णपर्व"),
    (9,  "shalya",         "Śalya",          "शल्यपर्व"),
    (10, "sauptika",       "Sauptika",       "सौप्तिकपर्व"),
    (11, "stri",           "Strī",           "स्त्रीपर्व"),
    (12, "shanti",         "Śānti",          "शान्तिपर्व"),
    (13, "anushasana",     "Anuśāsana",      "अनुशासनपर्व"),
    (14, "ashvamedhika",   "Aśvamedhika",    "अश्वमेधिकपर्व"),
    (15, "ashramavasika",  "Āśramavāsika",   "आश्रमवासिकपर्व"),
    (16, "mausala",        "Mausala",        "मौसलपर्व"),
    (17, "mahaprasthanika","Mahāprasthānika","महाप्रस्थानिकपर्व"),
    (18, "svargarohana",   "Svargārohaṇa",   "स्वर्गारोहणपर्व"),
]

# --- HTML/text cleaning -----------------------------------------------------

# Match the canonical verse-line marker at line start. Three families:
#   PP,AAA.VVVa / PP,AAA.VVVc  -- base critical text padas (lowercase letter pada-code)
#   PP,AAA.VVV*NNNN_LL          -- starred passages (appendix-like apparatus inserts)
#   PP,AAA.VVVx@NNN_LLLL        -- @-marked apparatus variants
# All share the leading PP,AAA.VVV which is the verse-id base.
VERSE_LINE_RE = re.compile(
    r"^(?P<parva>\d{1,2}),(?P<adhyaya>\d{3})\.(?P<verse>\d{3})"
    r"(?P<suffix>[A-Za-z]?(?:\*\d+_\d+)?(?:@\d+_\d+)?[A-Za-z]?)"
    # Separator between the verse-id and the verse-text varies between parvans:
    # most use a tab, parva-10 uses the literal sequence "<>".
    r"(?:\s+|<>)"
    r"(?P<text>.*?)$"
)

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t]+")


def strip_html_chrome(raw: str) -> list[str]:
    """Return body lines after the trailing <hr> chrome and before </body>.

    The GRETIL parvan files have a long header (encoding table + license), then
    a <hr> separator, then plain Sanskrit verse lines each terminated by <BR>.
    We split on <hr> and take the final segment; that yields the verse-only body.
    """
    parts = re.split(r"<hr\s*/?>", raw, flags=re.IGNORECASE)
    body = parts[-1] if parts else raw
    # Drop </body> tail
    body = re.sub(r"</body\s*>.*$", "", body, flags=re.IGNORECASE | re.DOTALL)
    # Normalize line breaks: <BR> -> \n
    body = re.sub(r"<br\s*/?>", "\n", body, flags=re.IGNORECASE)
    # Strip remaining tags
    body = TAG_RE.sub("", body)
    # Collapse runs of spaces/tabs
    lines = [WS_RE.sub(" ", ln).strip() for ln in body.splitlines()]
    return [ln for ln in lines if ln]


def iast_to_devanagari(text: str) -> str:
    """Convert IAST text to Devanagari (verse-marker fragments are preserved verbatim
    elsewhere; this is called only on the Sanskrit half).

    GRETIL uses non-standard '; ' caesura inside metrical lines. indic_transliteration
    tolerates this. Apostrophes (') -> avagraha are handled by sanscript.
    """
    if not text:
        return ""
    try:
        return transliterate(text, sanscript.IAST, sanscript.DEVANAGARI)
    except Exception:
        return ""


# --- Per-parvan pipeline ---------------------------------------------------


def parse_parvan(htm_path: Path) -> tuple[list[str], "OrderedDict[tuple[int,int,int], dict]"]:
    """Return (clean_text_lines, verses_dict).

    verses_dict is keyed by (parva, adhyaya, verse_num) and accumulates pādas
    (a/b/c/d) into a single record. Starred passages (*NNNN_LL) and @-variants
    are folded onto the closest base verse-id; they extend the verse text.
    """
    raw = htm_path.read_text(encoding="utf-8", errors="replace")
    lines = strip_html_chrome(raw)

    verses: "OrderedDict[tuple[int,int,int], dict]" = OrderedDict()
    clean_lines: list[str] = []
    for ln_idx, ln in enumerate(lines, start=1):
        m = VERSE_LINE_RE.match(ln)
        if not m:
            # Stray non-verse line. Drop (e.g. blank lines, stray HTML residue).
            continue
        parva = int(m.group("parva"))
        adhyaya = int(m.group("adhyaya"))
        verse_num = int(m.group("verse"))
        text = m.group("text").strip()
        suffix = m.group("suffix") or ""
        # Preserve the canonical line in the clean txt
        clean_lines.append(f"{parva:02d},{adhyaya:03d}.{verse_num:03d}{suffix}\t{text}")
        key = (parva, adhyaya, verse_num)
        rec = verses.get(key)
        if rec is None:
            rec = {
                "parva": parva,
                "adhyaya": adhyaya,
                "verse_num": verse_num,
                "padas": [],  # list of (suffix, text)
                "source_line_start": ln_idx,
                "source_line_end": ln_idx,
            }
            verses[key] = rec
        rec["padas"].append((suffix, text))
        rec["source_line_end"] = ln_idx
    return clean_lines, verses


def build_verse_records(verses: "OrderedDict[tuple[int,int,int], dict]") -> list[dict]:
    out = []
    for (parva, adhyaya, verse_num), rec in verses.items():
        # Reconstruct verse: concatenate pādas by suffix in source order.
        joined = " / ".join(t for _, t in rec["padas"])
        # Devanagari conversion of the IAST text body only.
        dev = iast_to_devanagari(joined)
        verse_id = f"v_{parva:02d}_{adhyaya:03d}_{verse_num:03d}"
        out.append({
            "verse_id": verse_id,
            "parva": parva,
            "adhyaya": adhyaya,
            "verse_num": verse_num,
            "sanskrit_iast": joined,
            "sanskrit_devanagari": dev,
            "pada_count": len(rec["padas"]),
            "source_line_start": rec["source_line_start"],
            "source_line_end": rec["source_line_end"],
        })
    return out


def approx_token_count(verses: list[dict]) -> int:
    n = 0
    for v in verses:
        n += len(v["sanskrit_iast"].replace("/", " ").split())
    return n


def main() -> int:
    summary = {"parvans": [], "verse_total": 0, "token_total": 0}
    for parva_num, slug, iast_name, dev_name in PARVANS:
        htm = SRC_DIR / f"mbh_{parva_num:02d}_{slug}.htm"
        if not htm.exists():
            print(f"MISSING: {htm}", file=sys.stderr)
            continue
        clean_lines, verses = parse_parvan(htm)

        # Write the cleaned .txt next to the .htm
        txt_path = SRC_DIR / f"mbh_{parva_num:02d}_{slug}.txt"
        header = [
            f"# Mahābhārata, parvan {parva_num}: {iast_name} ({dev_name})",
            "# Source: GRETIL, Bhandarkar Critical Edition (Pune, 1933-1966).",
            "# Encoded by Muneo Tokunaga et al., revised John Smith (Cambridge). (C) BORI 1999.",
            "# Format: PP,AAA.VVV<suffix>\\t<IAST verse-line>",
            "#   PP = parvan, AAA = adhyāya, VVV = verse, suffix-codes:",
            "#     a/c (etc) = pāda label; *NNNN_LL = apparatus passage; @NNN_LL = variant.",
            "",
        ]
        txt_path.write_text("\n".join(header) + "\n".join(clean_lines) + "\n", encoding="utf-8")

        recs = build_verse_records(verses)
        tok = approx_token_count(recs)

        parva_json = {
            "text_id": "mahabharata",
            "parva_num": parva_num,
            "parva_name_iast": iast_name,
            "parva_name_devanagari": dev_name,
            "source_file": f"data/external/gretil/files/mahabharata/mbh_{parva_num:02d}_{slug}.txt",
            "source_html": f"data/external/gretil/files/mahabharata/mbh_{parva_num:02d}_{slug}.htm",
            "source_script": "iast",
            "tokenizer": "fallback_whitespace",
            "normalizer": "indic_transliteration",
            "ingested_at": str(date.today()),
            "ingested_by": "corpus-chat-lane9",
            "structure_recovered": True,
            "verse_count": len(recs),
            "token_count_approx": tok,
            "verses": recs,
        }
        out_path = OUT_DIR / f"parva_{parva_num:02d}_{slug}.json"
        out_path.write_text(json.dumps(parva_json, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"parva {parva_num:02d} {slug:<18} verses={len(recs):>5}  tokens~{tok:>7}  -> {out_path.name}")

        summary["parvans"].append({
            "parva_num": parva_num,
            "parva_name_iast": iast_name,
            "parva_name_devanagari": dev_name,
            "verse_count": len(recs),
            "token_count_approx": tok,
            "file": f"parva_{parva_num:02d}_{slug}.json",
        })
        summary["verse_total"] += len(recs)
        summary["token_total"] += tok

    # Top-level work-card.
    work_card = {
        "text_id": "mahabharata",
        "thinker_id": "vyasa",
        "work_title_iast": "Mahābhārata (Bhandarkar critical edition)",
        "work_title_devanagari": "महाभारतम्",
        "source": "GRETIL / Bhandarkar Critical Edition (Pune, 1933-1966)",
        "source_url_base": "https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/2_epic/mbh/",
        "editor": "V.S. Sukthankar, S.K. Belvalkar, P.L. Vaidya, et al.",
        "encoder_chain": "Muneo Tokunaga et al. -> John Smith (Cambridge) -> GRETIL (BORI © 1999)",
        "license": "GRETIL: usage permitted with attribution; retain per-text headers",
        "source_script": "iast",
        "tokenizer": "fallback_whitespace",
        "normalizer": "indic_transliteration",
        "ingested_at": str(date.today()),
        "ingested_by": "corpus-chat-lane9",
        "structure_recovered": True,
        "ascription_tier": "traditional-multi-author",
        "verse_count": summary["verse_total"],
        "token_count_approx": summary["token_total"],
        "parva_count": len(summary["parvans"]),
        "parvans": summary["parvans"],
    }
    (OUT_DIR / "mahabharata.json").write_text(
        json.dumps(work_card, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nTOTAL verses={summary['verse_total']}  tokens~{summary['token_total']}")
    print(f"work-card: {OUT_DIR / 'mahabharata.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

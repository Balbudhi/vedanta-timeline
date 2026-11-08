#!/usr/bin/env python3
"""Full commentary passages per verse, for the verse agent's reading of what the verse
leaves unsaid (anvaya, adhyāhāra, referents, sentences across verses, purport).

The verse packet carries, per word, the clause in which each commentator glosses that
word. That misses everything a commentator says about the verse as a whole: the
construal order, the words he supplies, whom a pronoun or "evam" points to, how a
sentence continues into the next verse, the purpose of the verse in the argument. This
writes, per verse, every Sanskrit commentary passage the library holds (Śaṅkara,
Rāmānuja, Madhva on disk; the gita/gita index's Sanskrit commentators), with loci, and
the neighbouring verses' text so cross-verse construal is visible. No published
translation is included.

    python3 scripts/gita/build_commentary_packets.py            # all 700 verses
    python3 scripts/gita/build_commentary_packets.py --chapter 12
Output: internal/gita_pipeline/packets/commentary/<CH.V>.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.parent / "prakriya/scripts/lookup"))
import lookup  # noqa: E402

CHAPTER_LENGTHS = lookup.CHAPTER_LENGTHS
OUT = ROOT / "internal/gita_pipeline/packets/commentary"


def verse_text(ch: int, v: int) -> str | None:
    if not (1 <= ch <= 18 and 1 <= v <= CHAPTER_LENGTHS[ch - 1]):
        return None
    r = lookup.gita_lookup(f"{ch}.{v}")
    return " / ".join(l.split("  Bhg_")[0] for l in r["bori"]["lines"])


def build(ch: int, v: int) -> dict:
    r = lookup.gita_lookup(f"{ch}.{v}")
    passages = []
    for who, key in (("Śaṅkara", "shankara"), ("Rāmānuja", "ramanuja"), ("Madhva", "madhva")):
        b = r.get(key)
        if b:
            passages.append({"who": who, "locus": b["locus"], "text": "\n".join(l for _, l in b["lines"])})
    gg = r.get("gita_gita") or {}
    for c in gg.get("sanskrit_commentaries", []):
        passages.append({"who": c["author"], "locus": f"{gg.get('source', 'gita_gita')}#verse={gg.get('verse_id')}&author={c['author_id']}",
                         "text": c["text"]})
    return {
        "schema": "gita-commentary-packet-v1", "locus": f"{ch}.{v}",
        "verse": verse_text(ch, v), "previous_verse": verse_text(ch, v - 1), "next_verse": verse_text(ch, v + 1),
        "reading_guide": ("Read every passage for: (1) anvaya — the order in which the commentator construes the words; "
                          "(2) adhyāhāra — words he supplies (an elided verb, subject or object; 'iti śeṣaḥ', 'ity arthaḥ'); "
                          "(3) referents — whom ye/te/tat/evam/yathoktam point to; (4) sentences running across verses "
                          "(a relative here, its correlative in the next verse); (5) tātparya — what the verse does in the argument. "
                          "Record in the verse output: construals that differ → forks; supplied words stay out of the line "
                          "(standard §7.3, §7.14) and go into the sense paragraph or a note, attributed."),
        "passages": passages,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    chapters = [a.chapter] if a.chapter else range(1, 19)
    n = 0
    for ch in chapters:
        for v in range(1, CHAPTER_LENGTHS[ch - 1] + 1):
            (OUT / f"{ch}.{v}.json").write_text(json.dumps(build(ch, v), ensure_ascii=False, indent=1), encoding="utf-8")
            n += 1
    print(json.dumps({"written": n, "out": str(OUT.relative_to(ROOT))}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

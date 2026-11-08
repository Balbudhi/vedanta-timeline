#!/usr/bin/env python3
"""Build the ChapterPacket for one Bhagavad-Gītā chapter (GITA_FULL_TRANSLATION_PLAN.md §7, L0–L2).

Deterministic extraction and witness joins only: no segmentation, no morphology,
no translation. For every verse the packet holds

  - the BORI mūla (IAST, with file:line loci) and the speaker line;
  - a labelled lossless Devanāgarī transliteration of the BORI IAST, collated
    against two Devanāgarī witnesses (Madhva bhāṣya mūla lines; gita/gita index),
    with every difference recorded (plan L3);
  - Śaṅkara, Rāmānuja and Madhva on the verse, with loci (evidence only, L1);
  - the gita/gita index: further Sanskrit commentaries and the English
    secondaries (quotation only; never republished);
  - the Besant–Das 1905 word-by-word discourse text and the Roy/Aurobindo chapter
    text (private store), as inspiration for form, never as authority.

    python3 scripts/build_gita_chapter_packet.py 12
      -> internal/sanskrit_reviews/gita/ch12/packet.json (+ collation report)
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRAKRIYA = ROOT.parent / "prakriya"
sys.path.insert(0, str(PRAKRIYA / "scripts/lookup"))
import lookup  # noqa: E402  (prakriya/scripts/lookup/lookup.py)

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11,
         "XII": 12, "XIII": 13, "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18}
ORDINAL = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth",
           "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth", "Sixteenth", "Seventeenth", "Eighteenth"]


def fold_deva(s: str) -> str:
    """Fold free orthographic variation before collating two Devanāgarī strings."""
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"[\s­​‌‍]", "", s)
    s = s.replace("।", "").replace("॥", "").replace("|", "").replace("ऽ", "")
    s = re.sub(r"[0-9०-९.]", "", s)
    # anusvāra vs class nasal before a stop: fold both to anusvāra
    s = re.sub(r"ङ्(?=[कखगघ])|ञ्(?=[चछजझ])|ण्(?=[टठडढ])|न्(?=[तथदधन])|म्(?=[पफबभम])", "ं", s)
    # a word-final consonant (virama) followed by an independent vowel: the printed
    # saṃhitā joins them (क् + अ → क, क् + आ → का ...). GRETIL spaces the words.
    vowel_to_matra = {"अ": "", "आ": "ा", "इ": "ि", "ई": "ी", "उ": "ु", "ऊ": "ू", "ऋ": "ृ", "ए": "े", "ऐ": "ै", "ओ": "ो", "औ": "ौ"}
    s = re.sub(r"्([अआइईउऊऋएऐओऔ])", lambda m: vowel_to_matra[m.group(1)], s)
    # a stray combining-form glitch in the index witness (भक्ित for भक्ति)
    s = s.replace("्ि", "ि")
    return s


def bori_chapter(ch: int) -> list[dict]:
    L = lookup.lines(lookup.BORI)
    verses: dict[int, dict] = {}
    speaker = None
    for i, l in enumerate(L, 1):
        m = re.search(rf"\s+Bhg_{ch}\.(\d{{3}})([ac])?\s+\[=MBh_06,(\d{{3}})\.(\d{{3}})([ac])?\]", l)
        if not m:
            continue
        v = int(m.group(1))
        text = l[: m.start()].strip()
        if m.group(2) is None:  # speaker line
            speaker = text
            verses.setdefault(v, {"locus": f"{ch}.{v}", "lines": [], "loci": [], "speaker_line": None})
            verses[v]["speaker_line"] = {"text": text, "locus": f"{lookup.rel(lookup.BORI)}:{i}"}
            continue
        rec = verses.setdefault(v, {"locus": f"{ch}.{v}", "lines": [], "loci": [], "speaker_line": None})
        rec["lines"].append(text)
        rec["loci"].append(f"{lookup.rel(lookup.BORI)}:{i}")
        rec["mbh"] = f"MBh 6.{int(m.group(3))}.{int(m.group(4))}"
    out = []
    current_speaker = None
    for v in sorted(verses):
        rec = verses[v]
        if rec["speaker_line"]:
            current_speaker = rec["speaker_line"]["text"]
        rec["speaker"] = ("arjuna" if current_speaker and "arjuna" in current_speaker else
                          "krishna" if current_speaker and "bhagav" in current_speaker else
                          "samjaya" if current_speaker and "saṃjaya" in current_speaker else
                          "dhrtarashtra" if current_speaker and "dhṛtarāṣṭra" in current_speaker else None)
        rec["iast"] = " |\n".join(rec["lines"]) + " ||"
        out.append(rec)
    return out


def devanagari_from_iast(iast: str) -> str:
    deva = lookup.to_deva(iast.replace(" |", " ").replace(" ||", " ").replace("|", ""))
    lines = [l.strip() for l in deva.split("\n")]
    return " ।\n".join(lines[:-1] + [lines[-1] + " ॥"]) if len(lines) > 1 else lines[0] + " ॥"


def madhva_mula_lines(ch: int, v: int) -> list[str]:
    blk = lookup.madhva_block(ch, v)
    if not blk:
        return []
    tag = f"॥{v:02d}॥"
    lines = [l.strip() for _, l in blk["lines"]]
    # the mūla is the two lines ending at the first occurrence of the tag inside the block
    idx = next((k for k, l in enumerate(lines) if l.endswith(tag)), None)
    if idx is None:
        return []
    cand = lines[max(0, idx - 1): idx + 1]
    # the previous line must look like a verse line (ends with daṇḍa), else keep only the tagged line
    if len(cand) == 2 and not cand[0].endswith("।"):
        cand = cand[1:]
    return cand


def gita_gita_deva(rec: dict) -> str | None:
    gg = rec.get("gita_gita") or {}
    return gg.get("devanagari_witness")


def besant_das_discourse(ch: int) -> dict | None:
    p = lookup.SECONDARIES / "besant_das_1905_wg1100.txt"
    if not p.exists():
        return None
    L = p.read_text(encoding="utf-8", errors="replace").split("\n")
    start = next((i for i, l in enumerate(L) if re.match(rf"^\s*{ORDINAL[ch - 1]} Discourse", l)), None)
    end = next((i for i, l in enumerate(L) if i > (start or 0) and re.match(rf"^\s*{ORDINAL[ch]} Discourse", l)), len(L)) if ch < 18 and start is not None else len(L)
    if start is None:
        return None
    return {"source": f"{lookup.rel(p)}:{start + 1}-{end}", "edition": "Annie Besant & Bhagavan Das, The Bhagavad-Gita, 1905 (PD; archive.org wg1100 OCR; Devanāgarī is garbled in the OCR, English word-glosses survive)", "text": "\n".join(L[start:end])}


def roy_chapter(ch: int) -> dict | None:
    p = lookup.SECONDARIES / "roy_bhagavad_gita_auro_ebooks.txt"
    if not p.exists():
        return None
    L = p.read_text(encoding="utf-8", errors="replace").split("\n")
    roman = [k for k, n in ROMAN.items() if n == ch][0]
    nxt = [k for k, n in ROMAN.items() if n == ch + 1]
    heads = [i for i, l in enumerate(L) if re.match(rf"^\s*CHAPTER {roman}\b", l)]
    if len(heads) < 2:
        return None
    start = heads[-1]
    end = next((i for i, l in enumerate(L) if i > start and nxt and re.match(rf"^\s*CHAPTER {nxt[0]}\b", l)), len(L))
    return {"source": f"{lookup.rel(p)}:{start + 1}-{end}", "edition": "The Bhagavad Gita, in the words of Sri Aurobindo, compiled by Anilbaran Roy (1938); Sri Aurobindo Ashram e-book (auro-ebooks). Aurobindo's exegesis, not a translation he endorsed; quotation only.", "text": "\n".join(L[start:end])}


def build(ch: int) -> dict:
    verses = bori_chapter(ch)
    packet_verses = []
    collation = []
    for rec in verses:
        v = int(rec["locus"].split(".")[1])
        g = lookup.gita_lookup(rec["locus"])
        deva = devanagari_from_iast(rec["iast"])
        witnesses = {}
        m_lines = madhva_mula_lines(ch, v)
        if m_lines:
            witnesses["madhva_bhasya_mula"] = {"text": "\n".join(m_lines), "locus": (g["madhva"] or {}).get("locus")}
        gd = gita_gita_deva(g)
        if gd:
            witnesses["gita_gita_index"] = {"text": gd, "locus": f"{lookup.rel(lookup.GITA_GITA)}/verse.json#id={g['gita_gita']['verse_id']}"}
        folded = fold_deva(deva)
        diffs = {}
        for name, w in witnesses.items():
            wf = fold_deva(w["text"])
            # strip the speaker line that the gita/gita witness prepends
            wf = re.sub(r"^(अर्जुनउवाच|श्रीभगवानुवाच|सञ्जयउवाच|संजयउवाच|धृतराष्ट्रउवाच)", "", wf)
            diffs[name] = "identical" if wf == folded else {"ours": folded, "witness": wf}
        collation.append({"locus": rec["locus"], "result": diffs})
        packet_verses.append({
            "locus": rec["locus"], "mbh": rec.get("mbh"), "speaker": rec["speaker"],
            "speaker_line": rec["speaker_line"],
            "iast": rec["iast"], "bori_loci": rec["loci"],
            "devanagari": deva,
            "devanagari_status": "deterministic transliteration of the BORI IAST (indic_transliteration IAST→DEVANAGARI); collated against the witnesses listed; see collation",
            "devanagari_witnesses": witnesses,
            "collation": diffs,
            "commentaries": {
                "shankara": g["shankara"], "ramanuja": g["ramanuja"], "madhva": g["madhva"],
                "gita_gita_sanskrit": (g.get("gita_gita") or {}).get("sanskrit_commentaries", []),
            },
            "secondaries_english": (g.get("gita_gita") or {}).get("english_translations", []),
        })
    packet = {
        "schema_version": "gita-chapter-packet-v1",
        "chapter": ch,
        "verse_count": len(packet_verses),
        "mula_witness": {"path": lookup.rel(lookup.BORI), "edition": "BORI critical edition of the Mahābhārata (Tokunaga et al., rev. John Smith; GRETIL)", "script": "IAST"},
        "commentary_witnesses": {k: lookup.rel(p) for k, p in (("shankara", lookup.SHANKARA), ("ramanuja", lookup.RAMANUJA), ("madhva", lookup.MADHVA))},
        "index_witness": {"path": lookup.rel(lookup.GITA_GITA), "licence_note": "gita/gita repository (MIT for code; texts by permission of their holders) — used as a private evidence index; nothing from it is republished."},
        "secondaries_chapter_texts": {"besant_das_1905": besant_das_discourse(ch), "roy_aurobindo_1938": roy_chapter(ch)},
        "lookup_tools": "prakriya/scripts/lookup/lookup.py (sutra, dhatu, kosha, amara, unadi, linga, gita, cheda, english)",
        "verses": packet_verses,
    }
    return packet, collation


def main():
    ch = int(sys.argv[1])
    out_dir = ROOT / f"internal/sanskrit_reviews/gita/ch{ch}"
    out_dir.mkdir(parents=True, exist_ok=True)
    packet, collation = build(ch)
    (out_dir / "packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "devanagari-collation.json").write_text(json.dumps(collation, ensure_ascii=False, indent=1), encoding="utf-8")
    n_ident = sum(1 for c in collation for r in c["result"].values() if r == "identical")
    n_tot = sum(len(c["result"]) for c in collation)
    print(json.dumps({"chapter": ch, "verses": packet["verse_count"], "out": str(out_dir.relative_to(ROOT)),
                      "collation_identical": n_ident, "collation_pairs": n_tot,
                      "shankara_found": sum(1 for v in packet["verses"] if v["commentaries"]["shankara"]),
                      "ramanuja_found": sum(1 for v in packet["verses"] if v["commentaries"]["ramanuja"]),
                      "madhva_found": sum(1 for v in packet["verses"] if v["commentaries"]["madhva"]),
                      "english_secondaries_per_verse": sorted({len(v["secondaries_english"]) for v in packet["verses"]})}))


if __name__ == "__main__":
    main()

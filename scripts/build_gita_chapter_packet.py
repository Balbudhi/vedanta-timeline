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

Packet v2 (audit §5.6, the deterministic part) adds:

  - per verse `padas[]`: the BORI tokens split at spaces, each with the Vidyut cheda hint
    (labelled non-authoritative; only when the vidyut environment is installed), the
    commentators' clauses that contain the pada (`gloss`, when lookup.py provides
    gloss_lookup) and the policy rows whose detector matches the token or its cheda lemma;
  - `lemma_inventory[]`: lemma, occurrences, policy status, dossier path or `needed`, and the
    renderings the published readers already give the lemma — from the producer cards when
    shards exist, else from the Vidyut split (non-authoritative); a concord summary (BORI
    occurrence count) when lookup.py provides concord_lookup;
  - `shard_plan[]`: consecutive sentence units (Rāmānuja's grouped tags such as
    (BhGR_12.3-5), and a producer line that does not end a sentence) packed into shards
    of about 60 cards with the smallest largest shard;
  - `policy_sha256`, the content hash producers record on their shards.

The packet is written even when a lemma occurring three or more times in the chapter
has neither a policy row nor a `translate_by_wording` mark (the inventory is what the
rows are decided from), but the run then exits 1: the chapter is not ready for production.

    python3 scripts/build_gita_chapter_packet.py 12 [--out DIR]
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
sys.path.insert(0, str(ROOT / "scripts"))
import build_gita_chapter_reader as builder  # noqa: E402  (policy, reader discovery)

CARDS_PER_SHARD = 60
FUNCTION_WORDS = {"ca", "na", "eva", "api", "hi", "tu", "iti", "vā", "yad", "tad", "idam", "etad", "kim", "asmad", "yuṣmad",
                  "adas", "sma", "ha", "u", "atha", "tathā", "yathā", "iva", "evam"}

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
        m = re.search(rf"\s+Bhg_{ch:02d}\.(\d{{3}})([ac])?\s+\[=MBh_06,(\d{{3}})\.(\d{{3}})([ac])?\]", l)
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


# ---------------------------------------------------------------- packet v2 (audit §5.6)
def feature(*names: str):
    """The first lookup.py function of these names, or None (the packet builds without it)."""
    return next((getattr(lookup, n) for n in names if callable(getattr(lookup, n, None))), None)


def bori_tokens(iast: str) -> list[str]:
    return [t for t in re.split(r"\s+", iast.replace("|", " ")) if t]


def cheda_hint(iast: str) -> list[dict] | None:
    venv = PRAKRIYA / "tmp/vidyut-venv/bin/python"
    if not venv.exists():
        return None
    try:
        return lookup.cheda(iast.replace("|", " ").replace("\n", " "))
    except BaseException:
        return None


def policy_rows_for_text(policy: "builder.Policy", texts: list[str]) -> list[str]:
    return [k for k, r in policy.rows.items() if r.match and any(r.match.search(t) for t in texts if t)]


def verse_padas(rec: dict, policy, gloss_fn) -> list[dict]:
    toks = bori_tokens(rec["iast"])
    cheda = cheda_hint(rec["iast"])
    gloss = None
    if gloss_fn:
        try:
            gloss = gloss_fn(rec["locus"])
        except BaseException as e:
            gloss = {"error": str(e)[:200]}
    gl_padas = (gloss or {}).get("padas") or []
    out = []
    for k, tok in enumerate(toks):
        pd = {"i": k, "token": tok, "policy_rows": policy_rows_for_text(policy, [tok])}
        if gloss is not None:
            g = gl_padas[k] if k < len(gl_padas) and gl_padas[k].get("pada") == tok else next((x for x in gl_padas if x.get("pada") == tok), None)
            pd["gloss"] = {"glosses": g.get("glosses", []), "clause_counts": g.get("clause_counts", {}),
                           "authors_without_match": g.get("authors_without_match", [])} if g else None
        out.append(pd)
    block = {"tokens": out}
    if cheda is not None:
        block["cheda_hint"] = {"status": "Vidyut cheda split: a hint, not an analysis (non-authoritative)", "split": cheda}
        for pd in out:
            pd["policy_rows"] = sorted(set(pd["policy_rows"]) | set(policy_rows_for_text(policy, [c.get("lemma") for c in cheda])
                                                                      if any(latin(c.get("text", "")) in latin(pd["token"]) for c in cheda) else set()))
    if gloss is not None and "error" in gloss:
        block["gloss_error"] = gloss["error"]
    return block


def latin(s: str) -> str:
    return builder.latin_key(s)


def ramanuja_units(ch: int, n: int) -> list[list[int]]:
    """Sentence units from Rāmānuja's grouped tags (BhGR_12.3-5): consecutive verse numbers."""
    groups = {}
    p = lookup.RAMANUJA
    if p.exists():
        for m in re.finditer(rf"\(BhGR_{ch}\.(\d+)-(\d+)\)", p.read_text(encoding="utf-8", errors="replace")):
            a, b = int(m.group(1)), int(m.group(2))
            if 1 <= a < b <= n:
                groups[a] = max(groups.get(a, a), b)
    return merge_units(n, [(a, b) for a, b in groups.items()])


def merge_units(n: int, spans: list[tuple[int, int]]) -> list[list[int]]:
    link = [False] * (n + 2)                  # link[v]: verse v continues into v+1
    for a, b in spans:
        for v in range(a, b):
            link[v] = True
    units, cur = [], []
    for v in range(1, n + 1):
        cur.append(v)
        if not link[v]:
            units.append(cur)
            cur = []
    if cur:
        units.append(cur)
    return units


def balanced_partition(sizes: list[int], target: int = CARDS_PER_SHARD) -> list[list[int]]:
    """Split consecutive items into k = round(total/target) groups minimising the largest group."""
    n = len(sizes)
    if n == 0:
        return []
    k = max(1, min(n, round(sum(sizes) / target)))
    pre = [0]
    for x in sizes:
        pre.append(pre[-1] + x)
    INF = float("inf")
    best = [[INF] * (n + 1) for _ in range(k + 1)]
    cut = [[0] * (n + 1) for _ in range(k + 1)]
    best[0][0] = 0
    for j in range(1, k + 1):
        for i in range(1, n + 1):
            for c in range(j - 1, i):
                cost = max(best[j - 1][c], pre[i] - pre[c])
                if cost < best[j][i]:
                    best[j][i], cut[j][i] = cost, c
    groups, i = [], n
    for j in range(k, 0, -1):
        c = cut[j][i]
        groups.append(list(range(c, i)))
        i = c
    return groups[::-1]


def shard_plan(ch: int, n: int, cards_per_verse: dict[int, int], producer_lines: dict[int, str], source: str) -> list[dict]:
    spans = []
    for v, line in producer_lines.items():
        if v < n and not re.search(r"[.?!][\"'’”)]*\s*$", line.strip()):
            spans.append((v, v + 1))          # the English line does not end the sentence
    units = merge_units(n, [(u[0], u[-1]) for u in ramanuja_units(ch, n) if len(u) > 1] + spans)
    sizes = [sum(cards_per_verse.get(v, 0) for v in u) for u in units]
    plan = []
    for g in balanced_partition(sizes):
        verses = [v for k in g for v in units[k]]
        plan.append({"verses": f"{ch}.{verses[0]}-{ch}.{verses[-1]}", "units": [f"{ch}.{units[k][0]}" + (f"-{units[k][-1]}" if len(units[k]) > 1 else "") for k in g],
                     "cards": sum(sizes[k] for k in g), "card_count_source": source})
    return plan


def prior_renderings(root: Path, ch: int, policy) -> dict[str, list[dict]]:
    """lemma → renderings in the other published readers: by declared term, else by a policy
    row's detector on a legacy card, else by stem."""
    out: dict[str, list[dict]] = {}
    for p in builder.discover_readers(root):
        if p.parent.name == f"ch{ch}":
            continue
        try:
            verses = builder.load_reader(p)
        except builder.BuildError:
            continue
        for v in verses:
            smap = builder.slot_map(v.get("english") or "")
            for w in v.get("words") or []:
                rend = smap.get(w.get("i"), [])
                if not rend:
                    continue
                keys = [t["lemma"] for t in [w.get("term")] + list(w.get("terms") or []) if isinstance(t, dict) and t.get("lemma")]
                keys = keys or policy.regex_rows(w) or ([w["stem"]] if w.get("stem") else [])
                for key in keys:
                    out.setdefault(key, []).append({"reader": p.parent.name, "at": f"{v.get('locus')}[{w.get('i')}]",
                                                    "iast": w.get("iast"), "rendering": " … ".join(rend)})
    return out


def lemma_inventory(ch: int, packet_verses: list[dict], shards: list[dict], policy, prior: dict, concord_fn) -> tuple[list[dict], list[str]]:
    occ: dict[str, dict] = {}
    if shards:
        for sh in shards:
            for v in sh.get("verses") or []:
                for i, w in enumerate(v.get("words") or []):
                    key = (w.get("term") or {}).get("lemma") or w.get("stem") or w.get("iast")
                    e = occ.setdefault(key, {"lemma": key, "occurrences": [], "content": False, "source": "producer cards"})
                    e["occurrences"].append(f"{v.get('locus')}[{i}]")
                    wc = w.get("word_class")
                    e["content"] |= (wc == "content") if wc else not (w.get("stem") in FUNCTION_WORDS or
                                                                     re.search(r"avyaya|nipāta|pronoun|sarvanāma", f"{w.get('affix', '')} {w.get('morph', '')}"))
    else:
        for v in packet_verses:
            split = ((v.get("padas") or {}).get("cheda_hint") or {}).get("split") or []
            for k, c in enumerate(split):
                key = c.get("lemma") or c.get("text")
                e = occ.setdefault(key, {"lemma": key, "occurrences": [], "content": True, "source": "Vidyut split (non-authoritative)"})
                e["occurrences"].append(f"{v['locus']}[{k}]")
                if key in FUNCTION_WORDS or re.search(r"avyaya|sarvanAma|pronoun", c.get("analysis", ""), re.I):
                    e["content"] = False
    missing = []
    out = []
    for key, e in sorted(occ.items(), key=lambda kv: (-len(kv[1]["occurrences"]), kv[0] or "")):
        row = policy.rows.get(key)
        if row is None and e["source"] != "producer cards":
            rows = policy_rows_for_text(policy, [key])
            row = policy.rows[rows[0]] if len(rows) == 1 else None
        status = None
        if row:
            sts = sorted({s.status or "unrecorded" for s in row.senses.values()})
            status = sts[0] if len(sts) == 1 else sts
        dossier = row.dossier if row and row.dossier and (ROOT / row.dossier).exists() else ("needed" if row or (e["content"] and len(e["occurrences"]) >= 3) else None)
        rec = {"lemma": key, "row": row.lemma if row else None, "occurrences": e["occurrences"], "content": e["content"],
               "policy_status": status or ("translate-by-wording" if key in policy.translate_by_wording else "no row"),
               "dossier": dossier, "prior_renderings": prior.get(row.lemma if row else key, []), "source": e["source"]}
        if concord_fn and row:
            try:
                try:   # the row's own detector, when it has one, is the occurrence pattern
                    c = concord_fn(row.lemma_iast or key, regex=row.match.pattern) if row.match else concord_fn(row.lemma_iast or key)
                except TypeError:
                    c = concord_fn(row.lemma_iast or key)
                rec["concord"] = {"bori_occurrences": len(c.get("bori_occurrences") or []), "reader_cards": len(c.get("reader_cards") or [])}
            except BaseException as ex:
                rec["concord"] = {"error": str(ex)[:120]}
        if e["content"] and len(e["occurrences"]) >= 3 and not row and key not in policy.translate_by_wording:
            missing.append(f"{key} ({len(e['occurrences'])}×)")
        out.append(rec)
    return out, missing


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
    policy = builder.load_policy(ROOT / "data/glossary/term_policy.json")
    gloss_fn = feature("gloss_lookup", "gloss")
    concord_fn = feature("concord_lookup", "concord")
    for pv in packet_verses:
        pv["padas"] = verse_padas(pv, policy, gloss_fn)
    shard_dir = ROOT / f"internal/sanskrit_reviews/gita/ch{ch}"
    shards = []
    for sp in sorted(shard_dir.glob("producer-*.json")):
        try:
            shards.append(json.loads(sp.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            pass
    inventory, missing_rows = lemma_inventory(ch, packet_verses, shards, policy, prior_renderings(ROOT, ch, policy), concord_fn)
    cards = {int(v["locus"].split(".")[1]): len(v.get("words") or []) for sh in shards for v in sh.get("verses") or []}
    lines_ = {int(v["locus"].split(".")[1]): v.get("english") or "" for sh in shards for v in sh.get("verses") or []}
    if cards:
        src = "producer cards"
    else:
        src = "BORI tokens"
        cards = {int(pv["locus"].split(".")[1]): len(pv["padas"]["tokens"]) for pv in packet_verses}
    packet = {
        "schema_version": "gita-chapter-packet-v2",
        "policy_sha256": policy.sha256,
        "lookup_features": {"gloss": bool(gloss_fn), "concord": bool(concord_fn), "cheda": (PRAKRIYA / "tmp/vidyut-venv/bin/python").exists()},
        "chapter": ch,
        "verse_count": len(packet_verses),
        "mula_witness": {"path": lookup.rel(lookup.BORI), "edition": "BORI critical edition of the Mahābhārata (Tokunaga et al., rev. John Smith; GRETIL)", "script": "IAST"},
        "commentary_witnesses": {k: lookup.rel(p) for k, p in (("shankara", lookup.SHANKARA), ("ramanuja", lookup.RAMANUJA), ("madhva", lookup.MADHVA))},
        "index_witness": {"path": lookup.rel(lookup.GITA_GITA), "licence_note": "gita/gita repository (MIT for code; texts by permission of their holders) — used as a private evidence index; nothing from it is republished."},
        "secondaries_chapter_texts": {"besant_das_1905": besant_das_discourse(ch), "roy_aurobindo_1938": roy_chapter(ch)},
        "lookup_tools": "prakriya/scripts/lookup/lookup.py (sutra, dhatu, kosha, amara, unadi, linga, gita, cheda, english)",
        "verses": packet_verses,
        "lemma_inventory": inventory,
        "lemmas_needing_rows": missing_rows,
        "shard_plan": shard_plan(ch, len(packet_verses), cards, lines_, src),
    }
    return packet, collation


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", type=int)
    ap.add_argument("--out", type=Path, help="output directory (default internal/sanskrit_reviews/gita/chN)")
    a = ap.parse_args()
    ch = a.chapter
    out_dir = a.out or ROOT / f"internal/sanskrit_reviews/gita/ch{ch}"
    out_dir.mkdir(parents=True, exist_ok=True)
    packet, collation = build(ch)
    if a.out is None:
        builder.write_policy_snapshot(ROOT, ROOT / "data/glossary/term_policy.json")
    (out_dir / "packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "devanagari-collation.json").write_text(json.dumps(collation, ensure_ascii=False, indent=1), encoding="utf-8")
    n_ident = sum(1 for c in collation for r in c["result"].values() if r == "identical")
    n_tot = sum(len(c["result"]) for c in collation)
    print(json.dumps({"chapter": ch, "verses": packet["verse_count"], "out": str(out_dir),
                      "collation_identical": n_ident, "collation_pairs": n_tot,
                      "shankara_found": sum(1 for v in packet["verses"] if v["commentaries"]["shankara"]),
                      "ramanuja_found": sum(1 for v in packet["verses"] if v["commentaries"]["ramanuja"]),
                      "madhva_found": sum(1 for v in packet["verses"] if v["commentaries"]["madhva"]),
                      "english_secondaries_per_verse": sorted({len(v["secondaries_english"]) for v in packet["verses"]}),
                      "policy_sha256": packet["policy_sha256"], "lookup_features": packet["lookup_features"],
                      "lemmas": len(packet["lemma_inventory"]), "shard_plan": [s["verses"] + f" ({s['cards']})" for s in packet["shard_plan"]],
                      "lemmas_needing_rows": packet["lemmas_needing_rows"]}, ensure_ascii=False))
    if packet["lemmas_needing_rows"]:
        print(f"NOT READY FOR PRODUCTION: {len(packet['lemmas_needing_rows'])} lemma(s) occur three or more times without a policy row "
              "or a translate_by_wording mark (audit §5.6)")
        sys.exit(1)


if __name__ == "__main__":
    main()

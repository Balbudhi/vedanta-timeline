#!/usr/bin/env python3
"""Code-built job inputs. Everything exact is done here; agents only judge.

Inputs are Sanskrit (the library) plus the lexicon's decided rows; no English translation
of the Gītā (published, gita/gita, or this site's) is ever included.

    construe_input(locus)        -> one verse: candidate analyses per word + every commentary
    families(construals)         -> word families (by root, else stem) from CHOSEN analyses
    family_input(family, ...)    -> lexicon job: occurrences, glosses, dhātu + meaning pages
    units(construals)            -> sentence units from the construe stage's continuation flags
    unit_input(unit, ...)        -> verse job: mūla, construal, rows, every commentary
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKETS = ROOT / "internal/gita_pipeline/packets"
TOOL = Path(__file__).with_name("tool.py")
ANALYSIS_KEYS = ("id", "kind", "stem", "root", "gram", "krt", "taddhita", "members")  # no commentary signal: the grammar is read first


def verse_packet(locus: str) -> dict:
    return json.loads((PACKETS / "verses" / f"{locus}.json").read_text(encoding="utf-8"))


def commentary(locus: str) -> dict:
    return json.loads((PACKETS / "commentary" / f"{locus}.json").read_text(encoding="utf-8"))


def _derivation(aid: str) -> list[str]:
    import sanskrit_card as S
    _, d = S._row(aid)
    return S._derivation(d)


FURTHER_CAP = 40
FINITE_LIKE = ("śatṛ", "śānac", "kta", "ktavatu", "ktvā", "lyap", "tumun", "kvasu", "cānaś")


def _further(fa: dict, shown: set, pada: str | None) -> list[dict]:
    """Analyses past the packet's top 8 (`all_ids`), compact and without derivation: one per distinct
    (kind, stem, root, grammar, affix), finite verbs first, then participles, absolutives and infinitives,
    indeclinables, plain nominals, then the rest; at most FURTHER_CAP. The top-8 cut had hidden the right
    analysis of 21 of 41 hand-analysed words in chapter 15 (finite veda, utkrāmantam …)."""
    import sanskrit_card as S
    seen, out = set(), []
    for aid in fa.get("all_ids") or []:
        if aid in shown:
            continue
        a, _ = S._row(aid)
        if not a:
            continue
        krt = (a.get("krt") or {}).get("name")
        gram = " ".join(x for x in (a.get("lakara"), a.get("prayoga"), a.get("pada"), a.get("purusha"), a.get("vibhakti"),
                                    a.get("vacana"), a.get("linga")) if x)
        root = (a.get("dhatu") or {}).get("root")
        key = (a.get("kind"), a.get("stem"), root, gram, krt, (a.get("taddhita") or {}).get("name"))
        if key in seen:
            continue
        seen.add(key)
        rank = 0 if a.get("kind") == "tinanta" else 1 if krt in FINITE_LIKE else 2 if a.get("avyaya") or a.get("kind") == "avyaya" \
            else 3 if a.get("kind") == "subanta" else 4
        x = {"id": aid, "kind": a.get("kind"), "stem": a.get("stem"), "root": root, "gram": gram, "krt": krt,
             "taddhita": (a.get("taddhita") or {}).get("name"), "further": True}
        if pada:
            x["pada"] = pada
        out.append((rank, {k: v for k, v in x.items() if v not in (None, "")}))
    out.sort(key=lambda r: r[0])
    return [x for _, x in out[:FURTHER_CAP]]


def construe_input(locus: str) -> dict:
    """The parse card, grammar first (plan §3.1 M1): every token with the grammar engine's candidate
    analyses of each of its padas (a sandhi-joined token has several) and each candidate's derivation
    (prakṛti + pratyaya with sūtras); the neighbouring verses; and LAST the commentaries, as witnesses.
    Token -> pada forms through the packet's occurrences (bori_token), never by the sandhi surface."""
    p, c = verse_packet(locus), commentary(locus)
    padas: dict[int, list[str]] = {}
    for o in p["occurrences"]:
        padas.setdefault(o["bori_token"], []).append(o["form"])
    words = []
    for t in p["tokens"]:
        fs = padas.get(t["i"]) or [t["token"]]
        cands = []
        for f in fs:
            fa = p["forms"].get(f) or p["forms"].get(f.replace("-", "")) or {}
            for a in fa.get("analyses", []):
                x = {k: a.get(k) for k in ANALYSIS_KEYS if a.get(k) not in (None, [], "")}
                if len(fs) > 1:
                    x["pada"] = f
                dv = _derivation(a["id"])
                if dv:
                    x["derivation"] = dv
                cands.append(x)
        further = []
        for f in fs:
            fa = p["forms"].get(f) or p["forms"].get(f.replace("-", "")) or {}
            further += _further(fa, {c["id"] for c in cands}, f if len(fs) > 1 else None)
        w = {"i": t["i"], "form": t["token"], "candidates": cands + further}
        if len(fs) > 1:
            w["padas"] = fs
        words.append(w)
    return {"locus": locus, "speaker": p.get("speaker"), "iast": p["iast"],
            "split_tokens": [t["token"] for t in p["tokens"]], "words": words,
            "previous_verse": c["previous_verse"], "next_verse": c["next_verse"],
            "commentaries_last": [{"who": x["who"], "text": x["text"]} for x in c["passages"]]}


def units(construals: list[dict]) -> list[list[str]]:
    """Merge verses whose construal says the sentence continues into the next verse."""
    out, cur = [], []
    for c in sorted(construals, key=lambda c: tuple(int(x) for x in c["locus"].split("."))):
        cur.append(c["locus"])
        if not c.get("continues_into_next"):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def _family_key(w: dict) -> str | None:
    if w.get("word_class") != "content":
        return None
    import re
    m = re.search(r"√\s*([^\s,;()+]+)", w.get("root") or "")
    r = m.group(1) if m else ((w.get("root") or "").split() or [""])[0]
    return ("√" + r) if r else w.get("stem")


def families(construals: list[dict]) -> dict[str, dict]:
    """Families from the chosen analyses; compounds contribute each member."""
    fam: dict[str, dict] = {}
    for c in construals:
        for w in c["words"]:
            parts = w.get("members") or [w]
            for m in parts:
                m = {**m, "word_class": m.get("word_class", w.get("word_class"))}
                k = _family_key(m)
                if not k:
                    continue
                f = fam.setdefault(k, {"family": k, "root": k[1:] if k.startswith("√") else None, "lemmas": {}})
                f["lemmas"].setdefault(m["stem"], []).append({"locus": c["locus"], "i": w["i"], "form": w["form"]})
    return fam


def _tool(*args: str) -> str:
    r = subprocess.run([sys.executable, "-I", str(TOOL), *args], capture_output=True, text=True)
    return r.stdout


def family_input(f: dict) -> dict:
    occ = []
    for stem, places in f["lemmas"].items():
        for pl in places:
            p = verse_packet(pl["locus"])
            tok = next((t for t in p["tokens"] if t["i"] == pl["i"]), {"glosses": []})
            seen, glosses = set(), []
            for g in tok["glosses"]:
                if g["text"] not in seen:
                    seen.add(g["text"])
                    glosses.append({"who": g["who"], "text": g["text"]})
            occ.append({"stem": stem, "locus": pl["locus"], "form": pl["form"], "verse": p["iast"], "glosses": glosses})
    pages = {stem: _tool("meaning", stem) for stem in f["lemmas"]}
    elsewhere = {}
    for stem in f["lemmas"]:
        try:
            con = json.loads(_tool("concord", stem) or "{}")
        except json.JSONDecodeError:
            con = {}
        here = {pl["locus"] for pl in f["lemmas"][stem]}
        elsewhere[stem] = [{"verse": o["verse"], "form": o["form"], "line": o["line"]}
                           for o in con.get("bori_occurrences", []) if o["verse"] not in here]
    return {"family": f["family"], "root_entry": _tool("dhatu", f["root"]) if f.get("root") else None,
            "occurrences_in_scope": occ, "meaning_pages": pages,
            "elsewhere_in_gita": elsewhere}


def unit_input(unit: list[str], construals: dict[str, dict], rows: dict[str, dict]) -> dict:
    verses = []
    for loc in unit:
        p, c = verse_packet(loc), commentary(loc)
        verses.append({"locus": loc, "iast": p["iast"], "construal": construals[loc],
                       "commentaries": [{"who": x["who"], "text": x["text"]} for x in c["passages"]]})
    stems = {m["stem"] for loc in unit for w in construals[loc]["words"] for m in (w.get("members") or [w])
             if m.get("stem")}
    used = {k: r for k, r in rows.items() if any(l in stems for l in r.get("lemmas", []))}
    return {"unit": unit, "previous_verse": commentary(unit[0])["previous_verse"],
            "next_verse": commentary(unit[-1])["next_verse"], "verses": verses, "lexicon_rows": used}

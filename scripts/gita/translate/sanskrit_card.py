#!/usr/bin/env python3
"""The Sanskrit card for one word at one place, in the owner's order for meaning
(docs/GITA_FULL_TRANSLATION_PLAN.md §3.1, M1–M5). Code finds and cites; the model only judges.

    word_card(entry, locus, word)  -> {"M1_decode", "M2_morphemes", "M3_lexical_texts", "M4_usage",
                                       "M5_commentaries_last", "sources"}
    member_card(entry)             -> M2 and M3 only (a compound member; its commentary is the compound's)
    audit(entry, card)             -> [error], every source with an entry for the lemma is on the card

    python3 -I sanskrit_card.py RUN LOCUS I     print one card (RUN holds construe/<locus>/output.json)

Specification
-------------
Input. `entry` is one value of evidence.lemmas_from_construals (stem, root, upasargas, kinds, places,
verbal); `word` is the accepted construal's word (form, analysis_id or manual gram, compound).

M1 decode. The analysis the construal chose (analyses.sqlite by analysis_id; for a manual analysis, the
verse packet's analysis of the same form whose gram equals the manual gram): its grammar, its prakṛti
(root with gaṇa, Dhātupāṭha number and artha, or the nominal stem) and affixes, and the derivation
steps of the pratyaya chapters (Aṣṭādhyāyī 3.1.1–5.4.160) with their sūtras: the prakṛti + pratyaya
sequence. A compound adds its type and vigraha from the construal.

M2 morpheme meanings. The root's Dhātupāṭha entries; Dhātuvṛtti windows, 2 per work from the
Mādhavīya, Kṣīrataraṅgiṇī and Dhātupradīpa, and Daiva/Puruṣakāra when it treats the root; and for every
affix, lakāra, prayoga, sanādi suffix and case the sūtras that state its meaning
(affix_meanings.json), with the sūtra text read from the clean Aṣṭādhyāyī.

M3 lexical texts. Every kośa (Amarakośa, Amaraviveka, Halāyudha, Vaijayantī, Yādavakośa,
Ākhyātacandrikā), the Nirukta and Nighaṇṭu, and the Śabdakalpadruma and Vācaspatya: entries in which
the lemma is a whole word (or begins a sandhi-joined token with a case ending), ≤ 2 per work, ≤ 320
characters around the word. A verb's Ākhyātacandrikā group comes through its root. Hits where the
lemma is only part of another word (a compound member, a derivative) are not entries; their number is
recorded per work.

M4 usage. Number of places in the Gītā (this verse included) and up to six other lines, standalone uses
first; the rest by locus. In the Mahābhārata (BORI critical text): the number of verse-lines using the
word in any generated inflected form, by parvan, with three examples (mbh_usage.py).

M5 commentaries, last. Every commentator's clause on this word in this verse, one per commentator,
identical clauses merged. Witnesses: they choose among senses M1–M4 allow and may supply a fork.

sources. Every source of the inventory with its status: "shown N", "no entry", "not applicable" (no
root, a verb in a nominal kośa), "partial matches only (N)", "not in the library". Nothing is left
out unrecorded. audit() recomputes the kit's exact kośa and Nirukta hits independently and reports
any work with an entry that the card does not show.

The card is Sanskrit only: no English translation, no Sanskrit–English dictionary (Monier-Williams,
Apte, PW are never read here), no reader renderings. Tests: tests/test_sanskrit_card.py.
"""
from __future__ import annotations

import functools
import json
import re
import sqlite3
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import evidence as E  # noqa: E402  (also puts prakriya's lookup and gita_kit on the path)
import compile as C  # noqa: E402

M, L = E.M, E.L
ANALYSES = E.PACKETS / "analyses.sqlite"
AFFIXES = json.loads((HERE / "affix_meanings.json").read_text(encoding="utf-8"))
KOSHAS = {"amarakosha": "Amarakośa", "amaraviveka": "Amaraviveka", "halayudha": "Halāyudha",
          "vaijayanti": "Vaijayantī", "yaadavakosha": "Yādavakośa", "akhyata_chandrika": "Ākhyātacandrikā"}
NIRUKTA = {"nirukta": "Nirukta", "nighantu": "Nighaṇṭu"}
DICTS = {"skd": "Śabdakalpadruma", "vcp": "Vācaspatya"}
DHATUVRTTIS = {"Mādhavīya": "Mādhavīya Dhātuvṛtti", "Kṣīrataraṅgiṇī": "Kṣīrataraṅgiṇī",
               "Dhātupradīpa": "Dhātupradīpa", "Daiva": "Daiva with Puruṣakāra"}
SOURCES = (["Dhātupāṭha", *DHATUVRTTIS.values(), "Aṣṭādhyāyī meaning sūtras", *KOSHAS.values(), *NIRUKTA.values(),
            *DICTS.values(), "Gītā usage", "Mahābhārata usage", "Commentaries"])
CAP = {"per_work": 2, "text": 320, "vrtti": 6, "usage_lines": 6}
VIBHAKTI = ("prathamā", "dvitīyā", "tṛtīyā", "caturthī", "pañcamī", "ṣaṣṭhī", "saptamī", "sambodhana")
PRATYAYA_CHAPTERS = re.compile(r"^(3|4|5)\.")


# ------------------------------------------------------------------ M1 decode
@functools.lru_cache(maxsize=1)
def _db() -> sqlite3.Connection:
    return sqlite3.connect(f"file:{ANALYSES}?mode=ro", uri=True, check_same_thread=False)


def _blob(b):
    if b is None:
        return None
    try:
        return json.loads(b)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return json.loads(zlib.decompress(b))


def _row(aid: str | None) -> tuple[dict | None, dict | None]:
    if not aid:
        return None, None
    r = _db().execute("SELECT analysis, derivation FROM analyses WHERE id = ?", (aid,)).fetchone()
    return (_blob(r[0]), _blob(r[1])) if r else (None, None)


def _pausal(form: str) -> str:
    return re.sub(r"ṃ$", "m", re.sub(r"r$", "ḥ", form.rstrip(";").strip()))


def resolve(locus: str, word: dict) -> tuple[dict | None, dict | None, str | None]:
    """(analysis, derivation, gram) of the construal's chosen analysis. A manual analysis is matched to
    the packet's analysis of the same form with the same gram, when there is exactly one."""
    a, d = _row(word.get("analysis_id"))
    manual = word.get("manual") or {}
    gram = manual.get("gram")
    if a is None and gram:
        forms = C.verse_packet(locus)["forms"]
        f = forms.get(word["form"]) or forms.get(_pausal(word["form"])) or {}
        same = [x for x in f.get("analyses", []) if x.get("gram") == gram.split(";")[0].strip()
                and (not word.get("stem") or x.get("stem") == word.get("stem"))]
        if len(same) == 1:
            a, d = _row(same[0]["id"])
    if a is not None and not gram:
        gram = next((x.get("gram") for x in C.verse_packet(locus)["forms"].get(word["form"], {}).get("analyses", [])
                     if x.get("id") == word.get("analysis_id")), None)
    return a, d, gram


def _derivation(d: dict | None) -> list[str]:
    """The pratyaya steps (Aṣṭādhyāyī chapters 3–5) with their sūtras, then the derived form."""
    if not d or not d.get("matches"):
        return []
    out, last = [], None
    for s in d.get("steps") or []:
        if PRATYAYA_CHAPTERS.match(s["sutra"]) and s["result"] != last:
            out.append(f"{s['sutra']}: {s['result']}")
            last = s["result"]
    return out + [f"→ {d.get('form_derived')}"] if out else []


def decode(locus: str, word: dict, analysis: dict | None, derivation: dict | None, gram: str | None) -> dict:
    out = {"form": word["form"], "grammar": gram}
    if analysis:
        dh = analysis.get("dhatu") or {}
        if dh:
            out["prakrti"] = (f"√{dh.get('root')} ({E.iast(dh.get('aupadeshika') or '')}, {dh.get('gana_name')} "
                              f"{dh.get('code')}, {E.iast(dh.get('artha') or '')})")
            if dh.get("upasargas"):
                out["upasargas"] = dh["upasargas"]
            if dh.get("sanadi"):
                out["sanadi"] = dh["sanadi"]
        elif analysis.get("stem"):
            out["prakrti"] = analysis["stem"]
        for k in ("krt", "taddhita"):
            if analysis.get(k):
                out[k] = analysis[k]["name"] + (f" (base {analysis[k]['base']})" if analysis[k].get("base") else "")
        steps = _derivation(derivation)
        if steps:
            out["derivation"] = steps
        if derivation and derivation.get("scope"):
            out["derivation_scope"] = derivation["scope"]
    else:
        out["prakrti"] = word.get("stem") or None
        if word.get("root"):
            out["root"] = word["root"]
        if word.get("upasargas"):
            out["upasargas"] = word["upasargas"]
        out["derivation"] = "none: the analysis was supplied by the parse, not derived by the grammar engine"
    comp = word.get("compound")
    if comp:
        out["compound"] = {k: v for k, v in (("type", comp.get("type")), ("vigraha", comp.get("vigraha"))) if v}
    return {k: v for k, v in out.items() if v not in (None, "", [])}


# ------------------------------------------------------------------ M2 morpheme meanings
@functools.lru_cache(maxsize=512)
def sutra_text(code: str) -> str | None:
    try:
        return E.iast(L.sutra_lookup(code)["ashtadhyayi_text"].strip())
    except (SystemExit, ValueError, KeyError):
        return None


def _meanings(table: str, name: str | None) -> list[dict]:
    rows = AFFIXES[table].get(name or "") or []
    return [{"sutra": r["sutra"], "text": sutra_text(r["sutra"]), "artha": r["artha"]} for r in rows]


def affix_meanings(analysis: dict | None, gram: str | None) -> list[dict]:
    """Every affix of the word with the sūtras that state its meaning; unknown affixes are named with
    `sutras: []` so the gap is visible."""
    out = []

    def add(kind: str, table: str, name: str | None):
        if name:
            out.append({"affix": name, "kind": kind, "sutras": _meanings(table, name)})
    a = analysis or {}
    g = (gram or "").split(";")[0]
    for s in ((a.get("dhatu") or {}).get("sanadi") or []):
        add("sanādi", "sanadi", s)
    if a.get("krt"):
        add("kṛt", "krt", a["krt"].get("substitute", {}).get("name") or a["krt"]["name"])
    if a.get("taddhita"):
        add("taddhita", "taddhita", a["taddhita"]["name"])
    lak = a.get("lakara") or next((x for x in AFFIXES["lakara"] if re.search(rf"(^|\s){x}(\s|$)", g)), None)
    add("lakāra", "lakara", lak)
    pra = a.get("prayoga") or ("karmaṇi" if "karmaṇi" in g else None)
    if lak or pra:
        add("prayoga", "prayoga", pra or "kartari")
    vib = a.get("vibhakti") or next((x for x in VIBHAKTI if x in g), None)
    add("vibhakti", "vibhakti", vib)
    return out


def morphemes(entry: dict, analysis: dict | None, gram: str | None) -> tuple[dict, dict]:
    """(M2 section, source statuses)."""
    st: dict = {}
    sec: dict = {}
    if entry.get("root"):
        dh = E.dhatu_section(entry, limit=CAP["vrtti"])
        if dh["entries"]:
            sec["root"] = [f"{x['aupadesika']} ({x['gana']}, DP {x['dp']}): {x['artha']}" for x in dh["entries"]]
        st["Dhātupāṭha"] = f"shown {len(dh['entries'])}" if dh["entries"] else "no entry"
        vr = [{"work": v["work"], "text": v["text"]} for v in dh["vrtti"]]
        vr += _missing_vrtti(entry, {v["work"].split(" ")[0] for v in vr})
        daiva = [x for x in _kit_dhatuvrtti(entry["root"].lstrip("√")) if x["work"] == "daiva_purushakara"][:1]
        vr += [{"work": "Daiva with Puruṣakāra", "text": _strip_label(x["text"])} for x in daiva]
        if vr:
            sec["dhatuvrtti"] = vr
        for short, name in DHATUVRTTIS.items():
            n = sum(1 for v in vr if v["work"].startswith(short) or v["work"] == name)
            st[name] = f"shown {n}" if n else "no entry"
    else:
        for name in ["Dhātupāṭha", *DHATUVRTTIS.values()]:
            st[name] = "not applicable (no root)"
    aff = affix_meanings(analysis, gram)
    if aff:
        sec["affixes"] = aff
    n = sum(len(x["sutras"]) for x in aff)
    st["Aṣṭādhyāyī meaning sūtras"] = f"shown {n}" if n else "no affix analysed"
    return sec, st


def _missing_vrtti(entry: dict, shown: set[str]) -> list[dict]:
    """The opening of a Dhātuvṛtti's entry for the root when dhatu_section chose no window from that
    work: every work that treats the root is heard."""
    out = []
    for d in M.root_dp_entries(entry["root"].lstrip("√")):
        for r in E._vrtti_rows(d):
            name = E.DV_WORKS[r["work"]]
            if name in shown:
                continue
            text = E._cut(E.iast(E._clean_vrtti(E._strip_head(r["text"], d))), CAP["text"] // 2)
            if len(text) >= 12:
                own = re.search(r"own no\. (\d+)", r["label"])
                out.append({"work": name + (f" {own.group(1)}" if own else ""), "text": text})
                shown.add(name)
    return out


@functools.lru_cache(maxsize=2048)
def _kit_dhatuvrtti(root: str) -> list[dict]:
    dv, _ = M.dhatuvrtti_entries(root)
    return dv


@functools.lru_cache(maxsize=2048)
def _kit_akhyata(root: str) -> tuple:
    _, ak = M.dhatuvrtti_entries(root)
    return tuple(ak)


def _strip_label(text: str) -> str:
    return E._cut(E.iast(re.sub(r"^\[[^\]]*\]\s*", "", text)), CAP["text"])


# ------------------------------------------------------------------ M3 lexical texts
def _work_hits(stem: str, section: str) -> dict[str, tuple[list, int]]:
    """work -> (exact hits, number of partial hits) for the lemma in a kit section."""
    works = (KOSHAS if section == "kosha" else NIRUKTA)
    out: dict = {}
    ids = set()
    for work in works:  # per work: one work's whole-token hit must not hide another work's sandhi-joined entry
        exact = E._exact_hits(stem, section, work)
        ids |= {h[2]["uid"] for h in exact}
        if exact:
            out[work] = (exact, 0)
    for h in M._hits(M.to_slp(stem), section):
        if h[2]["uid"] not in ids:
            ex, n = out.get(h[2]["work"], ([], 0))
            out[h[2]["work"]] = (ex, n + 1)
    return out


def _label(r) -> str:
    return re.sub(r" = sanskrit_kosha.*$", "", r["label"])


@functools.lru_cache(maxsize=4096)
def _lexical(stem: str, root: str | None, verbal: bool) -> tuple[dict, dict]:
    sec: dict = {}
    st: dict = {}
    kosha = {} if verbal else _work_hits(stem, "kosha")
    for work, name in KOSHAS.items():
        ex, partial = kosha.get(work, ([], 0))
        items = [{"work": name, "where": _label(r), "text": E._cut(E.iast(M._window(r["text"], needle, CAP["text"])), CAP["text"])}
                 for _, _, r, needle in ex[:CAP["per_work"]]]
        if work == "akhyata_chandrika" and root and verbal:
            items += [{"work": name, "where": "via the root", "text": _strip_label(x["text"])}
                      for x in _kit_akhyata(root)[:CAP["per_work"]]]
        sec.setdefault("koshas", []).extend(items)
        if items:
            st[name] = f"shown {len(items)}" + (f" of {len(ex)}" if len(ex) > len(items) else "")
        elif verbal and work != "akhyata_chandrika":
            st[name] = "not applicable (a verb; its synonyms are in the Ākhyātacandrikā)"
        else:
            st[name] = f"partial matches only ({partial}; compound members or derivatives, not entries)" if partial else "no entry"
    nir = {} if verbal else _work_hits(stem, "nirukta")
    for work, name in NIRUKTA.items():
        ex, partial = nir.get(work, ([], 0))
        ex = sorted(ex, key=lambda h: " kasmA" not in " " + h[2]["slp"].split(M.to_slp(stem), 1)[-1][:12])
        items = [{"work": name, "where": h[2]["label"], "text": E._cut(E.iast(M._window(h[2]["text"], h[3], CAP["text"])), CAP["text"])}
                 for h in ex[:CAP["per_work"]]]
        sec.setdefault("nirukta_nighantu", []).extend(items)
        st[name] = (f"shown {len(items)}" + (f" of {len(ex)}" if len(ex) > len(items) else "")) if items else \
            (f"partial matches only ({partial})" if partial else ("not applicable (a verb)" if verbal else "no entry"))
    ks = E.kosha_section({"stem": stem, "root": f"√{root}" if root else None, "upasargas": [], "verbal": verbal}, CAP["text"] * 2)
    for d, name in DICTS.items():
        items = [{"work": name, "headword": k["headword"], "text": k["text"]} for k in ks if k["dict"] == d][:CAP["per_work"]]
        sec.setdefault("dictionaries", []).extend(items)
        st[name] = f"shown {len(items)}" if items else "no entry"
    return {k: v for k, v in sec.items() if v}, st


def lexical(entry: dict) -> tuple[dict, dict]:
    root = (entry.get("root") or "").lstrip("√") or None
    if entry.get("verbal"):
        sec, st = _lexical(entry["stem"], root, True)
        # a verbal lemma's SKD/VCP entry is its root's paragraph for these upasargas
        ks = E.kosha_section(entry, CAP["text"] * 2)
        sec = {**sec, "dictionaries": [{"work": DICTS[k["dict"]], "headword": k["headword"], "text": k["text"]} for k in ks]}
        st = {**st, **{name: (f"shown {sum(1 for k in ks if k['dict'] == d)}" if any(k["dict"] == d for k in ks) else "no entry")
                       for d, name in DICTS.items()}}
        return {k: v for k, v in sec.items() if v}, st
    return _lexical(entry["stem"], root, False)


# ------------------------------------------------------------------ M4 usage, M5 commentaries
def usage(entry: dict) -> tuple[dict, dict]:
    shown, more = E.elsewhere_section(entry, CAP["usage_lines"])
    here = sorted({p["locus"] for p in entry["places"]}, key=E._locus_key)
    sec = {"gita_places": len(here) + len(shown) + len(more), "in_this_run": here,
           "other_lines": [f"{x['locus']}: {x['line']}" for x in shown]}
    if more:
        sec["more_loci"] = more
    import mbh_usage
    mbh = mbh_usage.usage(entry["stem"])
    if mbh is not None:
        sec["mahabharata"] = mbh
        st = f"shown: {mbh['lines']} lines" if mbh["lines"] else "no whole-word use outside the Gītā"
    elif not mbh_usage.MBH.exists():
        sec["mahabharata"], st = "not in the library", "not in the library"
    else:
        sec["mahabharata"], st = "paradigm not generated (mbh_usage.py forms)", "paradigm not generated"
    return sec, {"Gītā usage": f"shown {len(shown)} of {len(shown) + len(more)} other lines", "Mahābhārata usage": st}


def commentaries(entry: dict, locus: str) -> tuple[list[str], dict]:
    occ = [o for o in E.occurrences_section(entry) if o["locus"] == locus]
    out = [f"{', '.join(g['who'])}: {g['clause']}" for o in occ for g in o.get("glosses", [])
           if g.get("clause") and not g.get("same_as")]
    return out, {"Commentaries": f"shown {len(out)}" if out else "no clause on this word in this verse"}


# ------------------------------------------------------------------ the card
_LOCK = None


def word_card(entry: dict, locus: str, word: dict) -> dict:
    """The M1–M5 card for one word at one place (see the module docstring)."""
    analysis, derivation, gram = resolve(locus, word)
    m1 = decode(locus, word, analysis, derivation, gram)
    m2, st = morphemes(entry, analysis, gram)
    m3, st3 = lexical(entry)
    m4, st4 = usage(entry)
    m5, st5 = commentaries(entry, locus)
    status = {**st, **st3, **st4, **st5}
    return {"lemma": entry["stem"], "M1_decode": m1, "M2_morphemes": m2, "M3_lexical_texts": m3, "M4_usage": m4,
            "M5_commentaries_last": m5, "sources": {s: status.get(s, "not consulted") for s in SOURCES}}


def member_card(entry: dict) -> dict:
    """A compound member: its morpheme and lexical evidence (M2, M3) and the number of Gītā places."""
    m2, st = morphemes(entry, None, None)
    m3, st3 = lexical(entry)
    return {"lemma": entry["stem"], "M2_morphemes": m2, "M3_lexical_texts": m3,
            "sources": {s: v for s, v in {**st, **st3}.items()}}


def audit(entry: dict, card: dict) -> list[str]:
    """Independent coverage check: every inventory source has a status, and every kośa / Nirukta work in
    which the kit's index finds the lemma as a word (a whole token, or the start of a sandhi-joined
    token followed by a case ending) is shown on the card."""
    errs = [f"{entry['stem']}: source {s} has no status" for s in SOURCES if s not in card.get("sources", {})]
    if entry.get("verbal"):
        return errs
    shown = {x["work"] for sec in ("koshas", "nirukta_nighantu") for x in card.get("M3_lexical_texts", {}).get(sec, [])}
    names = {**KOSHAS, **NIRUKTA}
    errs += [f"{entry['stem']}: the kit has {names[w]} entries for it but the card shows none"
             for w in sorted(_entry_works(entry["stem"])) if names.get(w) and names[w] not in shown]
    return errs


@functools.lru_cache(maxsize=4096)
def _entry_works(stem: str) -> frozenset:
    works = set()
    for sp in E.spellings(stem):
        slp = M.to_slp(sp)
        keys = [k for k in M.lemma_keys(slp) if len(k) >= 3]
        for section in ("kosha", "nirukta"):
            for rank, how, r, needle in M._hits(slp, section):
                if rank == 0 or any(t.startswith(k) and M._inflected_residue(k, t[len(k):len(k) + 2])
                                    for t in r["slp"].split() for k in keys):
                    works.add(r["work"])
    return frozenset(works)


def main(argv: list[str]) -> None:
    run, locus, i = argv[0], argv[1], int(argv[2])
    import pipeline as P
    cons = [json.loads(p.read_text()) for p in sorted((P.RUNS / run / "construe").glob("*/output.json"))]
    pos, ents = P.lemma_map(cons)
    word = next(w for c in cons if c["locus"] == locus for w in c["words"] if w["i"] == i)
    lemma = pos[(locus, i)]["word"] or word.get("stem")
    card = word_card(ents[lemma], locus, word)
    print(json.dumps(card, ensure_ascii=False, indent=1))
    print("audit:", audit(ents[lemma], card) or "ok", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])

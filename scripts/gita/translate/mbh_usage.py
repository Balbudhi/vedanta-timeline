#!/usr/bin/env python3
"""Usage of a Gītā word across the Mahābhārata (plan §3.1 M4): how many verse-lines of the epic use the
word, by parvan, with example lines. Code counts; the model reads the counts and examples.

    python3 mbh_usage.py lemmas RUN [RUN …]                       list the runs' lemmas (pipeline environment)
    tmp/vidyut-venv/bin/python mbh_usage.py forms                 generate their paradigms (Vidyut environment)
    python3 mbh_usage.py show LEMMA                              print one lemma's usage

Method. The grammar engine (Vidyut, the same engine as the parse) generates every inflected form of the
lemma: a nominal stem in the three genders, eight cases, three numbers; a verbal lemma (root with its
upasargas) in the finite forms of laṭ, laṅ, liṭ, luṅ, lṛṭ, loṭ and vidhiliṅ, active and passive, both
padas, and its ktvā/lyap and tumun. The Mahābhārata text (BORI critical edition, GRETIL; prakriya
corpus/acquisition-20261109) is tokenised on spaces; a token and a generated form match when they are
equal after removing word-final sandhi (kit `meaning.fold`: final visarga, anusvāra/m, s/ṣ/ś/r, -o→-a)
and restoring an avagraha's a. So whole words are counted; a word inside a compound, or fused with the
next word by vowel sandhi (caiva), is not. Lines of the Gītā itself (6.23–6.40) are counted apart.
Paradigms are cached in internal/gita_pipeline/packets/usage/forms.json (private working state); the
epic's token index in internal/gita_pipeline/packets/usage/mbh_tokens.json.
"""
from __future__ import annotations

import functools
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRAKRIYA = ROOT.parent / "prakriya"
MBH = PRAKRIYA / "corpus/acquisition-20261109/itihasa/mahabharata_bori_gretil/mahabharata_bori_constituted_iast.txt"
USAGE = ROOT / "internal/gita_pipeline/packets/usage"
FORMS = USAGE / "forms.json"
TOKENS = USAGE / "mbh_tokens.json"
GITA = re.compile(r"^6\.(2[3-9]|3\d|40)\.")
EXAMPLES = 3


def _kit():
    sys.path.insert(0, str(PRAKRIYA / "scripts/gita_kit"))
    sys.path.insert(0, str(PRAKRIYA / "scripts/lookup"))
    import meaning as M
    return M


def norm(token_iast: str) -> str:
    M = _kit()
    t = token_iast.strip(".,;:|!?()[]\"“”")
    if t.startswith("'"):
        t = "a" + t[1:]
    t = t.replace("'", "")
    return M.fold(M.to_slp(t)) if t else ""


# ------------------------------------------------------------------ the epic's token index
def build_tokens() -> dict:
    idx: dict[str, list[str]] = defaultdict(list)
    for line in MBH.read_text(encoding="utf-8").splitlines():
        locus, _, text = line.partition("\t")
        for tok in set(text.split()):
            k = norm(tok)
            if k:
                idx[k].append(locus)
    USAGE.mkdir(parents=True, exist_ok=True)
    TOKENS.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    return idx


@functools.lru_cache(maxsize=1)
def tokens() -> dict:
    if not MBH.exists():
        return {}
    if TOKENS.exists() and TOKENS.stat().st_mtime >= MBH.stat().st_mtime:
        return json.loads(TOKENS.read_text(encoding="utf-8"))
    return build_tokens()


@functools.lru_cache(maxsize=1)
def lines() -> dict:
    return dict(l.split("\t", 1) for l in MBH.read_text(encoding="utf-8").splitlines() if "\t" in l)


@functools.lru_cache(maxsize=1)
def forms() -> dict:
    return json.loads(FORMS.read_text(encoding="utf-8")) if FORMS.exists() else {}


# ------------------------------------------------------------------ usage
def usage(lemma: str) -> dict | None:
    """{lines, gita_lines, by_parvan, examples} for a lemma whose paradigm was generated; None when the
    text or the paradigm is missing (the card then says so)."""
    rec = forms().get(lemma)
    idx = tokens()
    if not rec or not idx or not rec.get("forms"):  # no paradigm: the card says so, never "no use"
        return None
    fs = rec["forms"]
    hits = set()
    for f in {_kit().fold(x) for x in fs}:
        hits.update(idx.get(f, []))
    epic = sorted((l for l in hits if not GITA.match(l)), key=_key)
    by = Counter(l.split(".")[0] for l in epic)
    step = max(1, len(epic) // EXAMPLES)
    ex = [f"{l}: {lines()[l]}" for l in epic[::step][:EXAMPLES]]
    return {"lines": len(epic), "gita_lines": len(hits) - len(epic),
            "by_parvan": {p: by[p] for p in sorted(by, key=int)}, "examples": ex,
            "ambiguous_forms_excluded": len(rec.get("ambiguous") or []),
            "method": "whole words in any inflected form the grammar generates, less forms the grammar's lexicon also reads as "
                      "another word; compound members and vowel-fused words not counted"}


def _key(locus: str) -> tuple:
    return tuple(int(x) if x.isdigit() else 0 for x in re.split(r"[.]", re.sub(r"[a-zA-Z]+$", "", locus)))


# ------------------------------------------------------------------ paradigms (Vidyut)
def generate(lemmas: dict) -> dict:
    """lemma -> [SLP1 forms]. `lemmas` maps lemma -> {"verbal", "root" (aupadeśika), "gana", "upasargas"}."""
    from vidyut.prakriya import (Dhatu, Gana, Lakara, Linga, Pada, Pratipadika, Prayoga, Purusha, Vacana, Vibhakti,
                                 Krt, DhatuPada, Vyakarana)
    from vidyut.kosha import Kosha
    eng = Vyakarana()
    kosha = Kosha(str(PRAKRIYA / "tmp/vidyut-data/kosha"))
    out = {}
    for lemma, e in lemmas.items():
        fs: set[str] = set()
        try:
            for aup, gn in (e.get("roots") or []) if e.get("verbal") else []:
                d = Dhatu.mula(aup, getattr(Gana, G_GANA[int(gn)]), prefixes=list(e.get("upasargas") or []))
                for lak in ("Lat", "Lan", "Lit", "Lun", "Lrt", "Lot", "VidhiLin"):
                    for pra in ("Kartari", "Karmani"):
                        for pur in ("Prathama", "Madhyama", "Uttama"):
                            for vac in ("Eka", "Dvi", "Bahu"):
                                for dp in (DhatuPada.Parasmaipada, DhatuPada.Atmanepada):
                                    try:
                                        p = Pada.Tinanta(d, getattr(Prayoga, pra), getattr(Lakara, lak),
                                                         getattr(Purusha, pur), getattr(Vacana, vac), dhatu_pada=dp)
                                        fs.update(x.text for x in eng.derive(p))
                                    except BaseException:  # Vidyut raises Rust panics, not Exception
                                        pass
                for k in ("ktvA", "tumun"):
                    try:
                        fs.update(x.text for x in eng.derive(Pratipadika.krdanta(d, getattr(Krt, k))))
                    except BaseException:
                        pass
            if not e.get("verbal"):
                stem = e["slp"]
                if not re.fullmatch(r"[a-zA-Z~]+", stem or ""):
                    out[lemma] = {"error": f"stem {stem!r} is not plain SLP1"}
                    continue
                prati = Pratipadika.basic(stem)
                for lin in ("Pum", "Stri", "Napumsaka"):
                    for vib in ("Prathama", "Dvitiya", "Trtiya", "Caturthi", "Panchami", "Sasthi", "Saptami", "Sambodhana"):
                        for vac in ("Eka", "Dvi", "Bahu"):
                            try:
                                fs.update(x.text for x in eng.derive(Pada.Subanta(prati, getattr(Linga, lin),
                                                                                  getattr(Vibhakti, vib), getattr(Vacana, vac))))
                            except BaseException:
                                pass
        except BaseException as ex:  # recorded, never silent (Vidyut raises Rust panics)
            out[lemma] = {"error": repr(ex)[:200]}
            continue
        amb = sorted(f for f in fs if _other_reading(kosha, eng, f, e))
        out[lemma] = {"forms": sorted(set(fs) - set(amb)), "ambiguous": amb}
    return out


_NASAL = re.compile(r"[MNYRnm](?=[kKgGcCjJwWqQtTdDpPbB])")


def _same_stem(a: str, b: str) -> bool:
    a, b = _NASAL.sub("M", a), _NASAL.sub("M", b)
    return a == b or (a.endswith("a") and b == a[:-1] + "A")


def _other_reading(kosha, eng, form: str, e: dict) -> bool:
    """The grammar's lexicon (Vidyut kosha) also reads `form` as another word: for a nominal lemma, a finite
    verb or a plain stem other than this one (a kṛdanta entry derives this stem from its root: bhakta from
    bhaj); for a verbal lemma, a plain nominal stem (cakra beside kṛ's perfect cakra)."""
    for key in {form, re.sub(r"H$", "s", form)}:
        for ent in kosha.get(key):
            kind = type(ent).__name__
            pe = getattr(ent, "pratipadika_entry", None)
            basic = pe is not None and type(pe).__name__.endswith("Basic")
            if e.get("verbal"):
                if "Subanta" in kind and basic:
                    return True
            elif "Tinanta" in kind or (basic and not _same_stem(pe.lemma or "", e["slp"])):
                return True
    return False


G_GANA = {1: "Bhvadi", 2: "Adadi", 3: "Juhotyadi", 4: "Divadi", 5: "Svadi", 6: "Tudadi", 7: "Rudhadi", 8: "Tanadi",
          9: "Kryadi", 10: "Curadi"}


def lemmas_of_runs(runs: list[str]) -> dict:
    """The lemmas of the runs' accepted construals with what the paradigm needs (root's Dhātupāṭha
    aupadeśika and gaṇa from the kit for a verbal lemma)."""
    sys.path.insert(0, str(HERE))
    import evidence as E
    import pipeline as P
    out = {}
    for run in runs:
        cons, _ = P.accepted_construals(run)
        for stem, e in E.lemmas_from_construals(cons).items():
            if stem in out:
                continue
            item = {"verbal": bool(e.get("verbal")), "upasargas": e.get("upasargas") or [], "slp": E.M.to_slp(stem)}
            if e.get("verbal") and e.get("root"):
                dps = E.M.root_dp_entries(e["root"].lstrip("√"))
                ganas = (e.get("hints") or {}).get("ganas") or []
                sel = [d for d in dps if d["gana"] in ganas] or dps  # the parse's gaṇa, else every root of that form
                item["roots"] = [[d["aup_slp"], d["gana"]] for d in sel]
            out[stem] = item
    return out


def main(argv: list[str]) -> int:
    if argv[:1] == ["lemmas"]:
        want = lemmas_of_runs(argv[1:])
        USAGE.mkdir(parents=True, exist_ok=True)
        old = json.loads((USAGE / "lemmas.json").read_text()) if (USAGE / "lemmas.json").exists() else {}
        (USAGE / "lemmas.json").write_text(json.dumps({**old, **want}, ensure_ascii=False), encoding="utf-8")
        tokens()  # build the epic's token index in this environment
        print(json.dumps({"lemmas": len({**old, **want})}))
        return 0
    if argv[:1] == ["forms"]:
        want = json.loads((USAGE / "lemmas.json").read_text(encoding="utf-8"))
        have = {k: v for k, v in forms().items() if isinstance(v, dict) and "forms" in v and "--redo" not in argv}
        todo = {k: v for k, v in want.items() if k not in have}
        new = generate(todo)
        FORMS.parent.mkdir(parents=True, exist_ok=True)
        FORMS.write_text(json.dumps({**have, **new}, ensure_ascii=False), encoding="utf-8")
        errs = sum(1 for v in new.values() if "error" in v)
        print(json.dumps({"lemmas": len(want), "generated": len(new), "errors": errs,
                          "empty": sum(1 for v in new.values() if not v.get("forms"))}))
        return 0
    if argv[:1] == ["show"]:
        print(json.dumps(usage(argv[1]), ensure_ascii=False, indent=1))
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

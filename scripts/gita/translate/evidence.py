#!/usr/bin/env python3
"""Stage 2a of the retired lexicon-first design (docs/history/gita/WORKFLOW_lexicon_first.md), used today by pipeline.evidence_at: the Sanskrit card for one lemma (code finds; the model only chooses).

    lemmas_from_construals(construals) -> {stem: {stem, root, upasargas, kinds, places, hints, members}}
    sanskrit_card(lemma_entry)         -> card dict (≤ ~6 KB as compact JSON), every item with an id
    card_bytes(card)                   -> size of the card as the model receives it

    python3 -I evidence.py card RUN_DIR LEMMA      one card (RUN_DIR holds construe/<CH.V>/output.json)
    python3 -I evidence.py stats RUN_DIR [--show L,L]   every lemma of the run: sizes, time, empty sections

Specification (this module's amendment to stage 2a of docs/history/gita/WORKFLOW_lexicon_first.md; 2026-11-09)
-----------------------------------------------------------------------------
Lemmas. Content words and names of the accepted construals; particles, pronouns and the copula are
skipped. A compound yields its own lemma (kind ``samāsa``) and one per content member (kind
``member``); a sandhi-joined word (``para + upeta``) yields each pada, and the place records the
pada. Roots are normalised to a bare ``√X``; what the construal adds to a root (``abhi-√as
(kṣepaṇe)``, ``vi-√vṛj (curādi)``, ``ā-√viś + ṇic``, an analysis's ``√ās adādi 2 … + pari-upa``)
becomes upasargas, ``hints`` (gaṇa, artha) and kinds. A finite verb, and a non-finite form (tumun,
ktvā, lyap, śatṛ, śānac) whose stem is upasargas + the root, is one VERBAL lemma keyed by the
upasargas joined to the root in sandhi (``pari-upa-ās``, ``paryupās`` and ``ās`` + pari-upa are one
lemma ``paryupās``; ``kurvat``, ``kartum`` and ``kuru`` are ``kṛ``). Kta participles, kṛt nouns and
compound members stay nominal (``bhakta``, ``abhyāsa``, the ``vid`` of yogavittama).

Card sections (all Sanskrit, in IAST; nothing from an English translation, a reader's renderings, a
Sanskrit–English dictionary or the Dhātupāṭha's ``artha_english``):

* ``dhatu.entries`` D1…: Dhātupāṭha entries of the root (aupadeśika, gaṇa, artha), restricted by the
  hints when they select something; entries whose vṛtti names this lemma come first.
  ``dhatu.vrtti`` D1.v1…: at most three windows (≤ 160 characters) from the Mādhavīya Dhātuvṛtti,
  Kṣīrataraṅgiṇī and Dhātupradīpa entries of those roots (paradigm lists and sūtra numbers removed):
  a window glossing the artha (संज्ञानं चैतन्यम्) or naming the lemma (भक्तः, not भक्तिः; उद्विजते for
  udvega) first, then derivative lists; a bare opening (grammar talk) only when nothing else exists.
* ``amara`` A1…: Amarakośa ślokas in which the lemma, in either nasal spelling, is a whole token
  (``=``); failing that a token that begins with it plus a case ending (भक्तमन्धो); at most two.
* ``kosha`` K1…: Śabdakalpadruma and Vācaspatya entries whose headword is exactly the lemma (stem,
  citation form, nasal spelling), at most three per dictionary, ≤ 600 characters, reduced to their
  glosses (quotations, inline references and citation-only segments dropped). A verbal lemma's
  headword is its root (also the Dhātupāṭha aupadeśika without anubandhas: काक्षिँ -> काक्ष); the text
  is the root entry's paragraph for these upasargas (VCP ``pari--upa--``, SKD ``(upa)``) up to the
  next paragraph, else the root entries' heads.
* ``nirukta`` N1…: Nirukta / Nighaṇṭu units with the lemma as a whole token (same rule as Amara),
  nirvacana (``… kasmāt``) first, ≤ 3, ≤ 180 characters.
* ``occurrences`` O1…: every place of the lemma in scope with the verse and, per commentator, one
  clause containing the word as a word (a joined token must continue with the word's own ending and
  not start with a negation or upasarga: priyaviyoge is not priyaḥ), cut to ≤ 160 characters: one
  word before, then to a pause after 30 or a word boundary after GLOSS_FIRM characters. When the
  word occurs twice in the verse, the clause nearest the neighbouring words is chosen. A clause that
  only repeats the verse or a pratīka (``yo madbhaktaḥ sa me priyaḥ``, ``kūṭasthamiti``) is not a
  gloss and is dropped. Identical clauses (compared sandhi-neutrally) are one item with every
  ``who``; one already given at an earlier place is ``same_as`` that item. Where the packet has no
  glosses for a token (sandhi-joined pada, reading variant), the verse's commentaries are searched,
  accepting a one-letter variant reading (mānāpamānayoḥ for BORI mānāvamānayoḥ) per commentator.
* ``elsewhere`` E1…: every other BORI line whose word is this lemma (the packet inventory's
  analyses; for a verb, its ``U-√root`` key and its tumun/ktvā/lyap forms) or a compound of which it
  is a member. Membership: the rest of the compound must read as members of the SKD/VCP headword
  list on both sides; a member right after an upasarga-final piece (avibhakta) and taddhita affixes
  (bhaktimat) do not count. Standalone uses are shown first; lines past the shown number are listed
  by locus in ``elsewhere_more``.

Budget. A card over BUDGET (6 KB of compact JSON) is rebuilt with the next of STAGES (fewer full
elsewhere lines, then shorter clause windows, then shorter kośa texts); ``stage`` records it. Nothing
is dropped unidentified. Precision rules: kośa and Amara are keyed by exact headword, Dhātuvṛtti by
the root's Dhātupāṭha entries, Nirukta by whole tokens; no substring hits. Tests:
tests/test_evidence.py.
"""
from __future__ import annotations

import argparse
import functools
import itertools
import json
import re
import statistics
import sys
import time
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKETS = ROOT / "internal/gita_pipeline/packets"
PRAKRIYA = ROOT.parent / "prakriya"
sys.path.insert(0, str(PRAKRIYA / "scripts/lookup"))
sys.path.insert(0, str(PRAKRIYA / "scripts/gita_kit"))
import lookup as L  # noqa: E402  (prakriya scripts/lookup/lookup.py)
import meaning as M  # noqa: E402  (prakriya scripts/gita_kit/meaning.py)

SKIP_CLASSES = {"particle", "pronoun", "copula"}
NONFINITE = {"tumun", "ktvā", "lyap", "śatṛ", "śānac"}
UPASARGAS = ("pra", "parā", "apa", "sam", "anu", "ava", "nis", "dus", "vi", "ā", "ni", "adhi", "api",
             "ati", "su", "ud", "abhi", "prati", "pari", "upa")
UPASARGA_ALIASES = {"āṅ": "ā", "nir": "nis", "dur": "dus", "ut": "ud", "saṃ": "sam"}
GANA_BY_NAME = {v: k for k, v in L.GANA_NAMES.items()}
DV_WORKS = {"madhaviya_dhatuvrtti": "Mādhavīya", "kshiratarangini": "Kṣīrataraṅgiṇī",
            "dhatupradipa": "Dhātupradīpa"}
WHO = {"Shankaracharya": "Śaṅkara", "Ramanujacharya": "Rāmānuja", "Madhavacharya": "Madhva",
       "Anandgiri": "Ānandagiri", "Dhanpati": "Dhanapati", "Neelkanth": "Nīlakaṇṭha",
       "Madhusudan Saraswati": "Madhusūdana", "Purushottamji": "Puruṣottama",
       "Vallabhacharya": "Vallabha", "Sridhara Swami": "Śrīdhara", "Jayatritha": "Jayatīrtha",
       "Abhinavgupta": "Abhinavagupta", "Vedantadeshikacharya Venkatanatha": "Vedāntadeśika"}
CAPS = {"vrtti": 3, "vrtti_text": 160, "amara": 2, "kosha_per_dict": 3, "kosha_text": 600,
        "nirukta": 3, "nirukta_text": 180, "clause": 160}
ELSEWHERE_LINES = 16
VOWELS = "aāiīuūṛṝḷeo"


# ------------------------------------------------------------------ sandhi of upasargas + root
def _join2(a: str, b: str) -> str:
    """Join two IAST pieces with the external sandhi an upasarga takes before what follows."""
    if not a:
        return b
    if not b:
        return a
    x, y = a[-1], b[0]
    if a == "nis" or a == "dus":
        if y in VOWELS or y in "gjḍdbnmyrlvhṅñṇ":
            return a[:-1] + "r" + b
        return a[:-1] + {"k": "ṣ", "p": "ṣ", "c": "ś", "t": "s"}.get(y, "ḥ") + b
    if a == "ud":
        if y in "kcṭtpśṣs":
            return "ut" + b
        if y in "nm":
            return "un" + b
        return "ud" + b
    if x == "m":
        return a + b if y in VOWELS else a[:-1] + "ṃ" + b
    if x in "aā" and y in VOWELS:
        fused = {"a": "ā", "ā": "ā", "i": "e", "ī": "e", "u": "o", "ū": "o", "ṛ": "ar", "e": "ai",
                 "o": "au"}.get(y)
        if b[:2] == "ai":
            fused, b = "ai", b[1:]
        elif b[:2] == "au":
            fused, b = "au", b[1:]
        return a[:-1] + fused + b[1:]
    if x in "iī" and y in VOWELS:
        return a[:-1] + ("ī" + b[1:] if y in "iī" else "y" + b)
    if x in "uū" and y in VOWELS:
        return a[:-1] + ("ū" + b[1:] if y in "uū" else "v" + b)
    return a + b


def join_upasargas(upasargas: list[str], root: str) -> str:
    """paryupās = join_upasargas(['pari', 'upa'], 'ās')."""
    out = ""
    for p in [*upasargas, root]:
        out = _join2(out, p) if out else p
    return out


_GRADES = {"a": "aā", "ā": "āa", "i": "iīeai", "ī": "īie", "u": "uūoau", "ū": "ūuo", "ṛ": "ṛar"}


def _root_heads(root: str) -> list[str]:
    """How the root can begin inside a derived stem: a consonant-initial root by its consonant (vij ->
    veg-); a vowel-initial root by a grade of its vowel plus the next consonant unless that is a nasal
    (as -> as-/ās-, añj -> a-/ā-, i -> i/e/ai/ī)."""
    if not root:
        return []
    first = root[0]
    if first not in _GRADES:
        return [first]
    nxt = root[1:2] if root[1:2] and root[1:2] not in "ṅñṇnmṃ" else ""
    grades = re.findall(r"ai|au|ar|.", _GRADES[first])
    return sorted({g + nxt for g in grades}, key=len, reverse=True)


@functools.lru_cache(maxsize=4096)
def split_upasargas(stem: str, root: str) -> tuple[str, ...] | None:
    """The fewest upasargas U such that stem = join(U, root…) at the boundary (vowel grades of the root
    allowed): udvega/vij -> ('ud',); abhyāsa/as -> ('abhi',); upeta/i -> ('upa',); kurvat/kṛ -> ();
    śraddadhāna/dhā -> None."""
    s = _norm(stem)
    for n in range(0, 4):
        for U in itertools.product(UPASARGAS, repeat=n):
            for head in _root_heads(root):
                j = join_upasargas(list(U), head)
                if s.startswith(_norm(j)) and len(s) > len(_norm(j)) - len(head):
                    return tuple(U)
    return None


def _norm(s: str) -> str:
    return L.norm_sa(s) if s else ""


# ------------------------------------------------------------------ roots
_ROOT_RE = re.compile(r"√\s*([^\s,;()+]+)")


def parse_root(raw: str | None) -> dict:
    """'abhi-√as (kṣepaṇe)' -> {root 'as', upasargas ['abhi'], ganas [], arthas ['kṣepaṇe'], kinds []};
    '√ās adādi 2 ātmanepada + pari-upa' -> gaṇa 2, upasargas ['pari', 'upa']; '+ ṇic' -> kind ṇic."""
    out = {"root": None, "upasargas": [], "ganas": [], "arthas": [], "kinds": []}
    if not raw:
        return out
    raw = unicodedata.normalize("NFC", raw)
    m = _ROOT_RE.search(raw)
    if not m:
        return out
    out["root"] = m.group(1)
    pre = raw[:m.start()].strip().rstrip("-")
    if pre:
        out["upasargas"] += [_upa(p) for p in pre.split("-") if p.strip()]
    rest = raw[m.end():]
    for name, num in GANA_BY_NAME.items():
        if re.search(rf"\b{name}\b", rest):
            out["ganas"].append(num)
    for g in re.findall(r"\(([^)]*)\)", rest):
        g = g.strip()
        if g in GANA_BY_NAME:
            out["ganas"].append(GANA_BY_NAME[g])
        elif g:
            out["arthas"].append(g)
    for part in rest.split("+")[1:]:
        part = part.strip()
        if part in ("ṇic", "san", "yaṅ", "yaṅluk"):
            out["kinds"].append(part)
        elif part:
            out["upasargas"] += [_upa(p) for p in part.split("-") if p.strip()]
    out["upasargas"] = [u for u in out["upasargas"] if u in UPASARGAS]
    out["ganas"] = sorted(set(out["ganas"]))
    return out


def _upa(p: str) -> str:
    p = unicodedata.normalize("NFC", p.strip())
    return UPASARGA_ALIASES.get(p, p)


# ------------------------------------------------------------------ lemmas
@functools.lru_cache(maxsize=1024)
def verse_packet(locus: str) -> dict:
    return json.loads((PACKETS / "verses" / f"{locus}.json").read_text(encoding="utf-8"))


@functools.lru_cache(maxsize=1024)
def _analyses(locus: str) -> dict:
    return {a["id"]: a for f in verse_packet(locus)["forms"].values() for a in f["analyses"]}


def _krt_name(src: dict) -> str | None:
    k = src.get("krt")
    return k.get("name") if isinstance(k, dict) else (k if isinstance(k, str) else None)


def _taddhita_name(src: dict) -> str | None:
    t = src.get("taddhita")
    return t.get("name") if isinstance(t, dict) else None


def _kind_tags(src: dict) -> list[str]:
    tags = []
    kind = (src.get("kind") or "").replace("samāsa", "samasa").replace("taddhitānta", "taddhitanta")
    for k in ("tinanta", "krdanta", "samasa", "taddhitanta", "subanta", "avyaya"):
        if k in kind:
            tags.append({"tinanta": "tiṅanta", "krdanta": "kṛdanta", "samasa": "samāsa",
                         "taddhitanta": "taddhitānta"}.get(k, k))
    for n in (_krt_name(src), _taddhita_name(src)):
        if n and " " not in n.strip():
            tags.append(n.strip())
    return tags


def _units(locus: str, w: dict):
    """(stem, root string, upasargas, kinds, word_class, members, analysis root, pada) for each lexical
    unit of a word; `pada` is the unit's own form when a sandhi-joined word is split, else None."""
    manual = w.get("manual") or {}
    analysis = _analyses(locus).get(w.get("analysis_id") or "", {}) if w.get("analysis_id") else {}
    src = manual or analysis
    if manual.get("padas"):
        for p in manual["padas"]:
            yield (p.get("stem"), p.get("root"), [], _kind_tags(p), p.get("word_class", "content"), None, None,
                   p.get("form") or p.get("stem"))
        return
    if " + " in (w.get("stem") or ""):
        for s in w["stem"].split(" + "):
            yield (s.strip(), None, [], [], w.get("word_class"), None, None, s.strip())
        return
    kinds = _kind_tags(src)
    root = w.get("root") or (src.get("root") if manual else None)
    yield (w.get("stem"), root, list(w.get("upasargas") or []), kinds, w.get("word_class"), w.get("members"),
           analysis.get("root"), None)


def _lexeme(stem: str, root_raw: str | None, ups: list[str], kinds: list[str], analysis_root: str | None,
            compound: bool, member: bool = False) -> tuple[str, dict]:
    """(key, partial entry) for one unit, applying the verbal folding rule of the docstring."""
    pr, pa = parse_root(root_raw), parse_root(analysis_root)
    root = pr["root"] or pa["root"]
    kinds = list(dict.fromkeys(kinds + pr["kinds"] + pa["kinds"]))
    stem = re.sub(r"[√\s]", "", unicodedata.normalize("NFC", stem or ""))
    given_u = [_upa(u) for u in ups if _upa(u) in UPASARGAS] or pr["upasargas"] or pa["upasargas"]
    hints = {"ganas": sorted(set(pr["ganas"] + pa["ganas"])), "arthas": pr["arthas"] + pa["arthas"]}
    if "-" in stem and root:                                      # 'pari-upa-ās'
        parts = stem.split("-")
        if all(_upa(p) in UPASARGAS for p in parts[:-1]):
            given_u = given_u or [_upa(p) for p in parts[:-1]]
            stem = join_upasargas([_upa(p) for p in parts[:-1]], parts[-1])
    verbal = False
    if root and not compound and not member:
        finite = "tiṅanta" in kinds
        nonfinite = any(k in NONFINITE for k in kinds) or (stem.endswith("tum") and "kṛdanta" in kinds)
        parsed = split_upasargas(stem, root)
        if finite or _norm(stem) == _norm(root) or _norm(stem) == _norm(join_upasargas(given_u, root)):
            verbal = True
            ups_v = given_u or list(parsed or ())
        elif nonfinite and parsed is not None and (not given_u or list(parsed) == given_u or not parsed):
            verbal = True
            ups_v = given_u or list(parsed)
        if verbal:
            return join_upasargas(ups_v, root), {"root": root, "upasargas": ups_v, "kinds": kinds,
                                                 "hints": hints, "verbal": True}
    upasargas = given_u if root else []
    if root and not upasargas and not compound:
        parsed = split_upasargas(stem, root)
        upasargas = list(parsed or ())
    return stem, {"root": root, "upasargas": upasargas, "kinds": kinds, "hints": hints, "verbal": False}


def _merge(out: dict, key: str, part: dict, place: dict, members=None) -> None:
    e = out.setdefault(key, {"stem": key, "root": None, "upasargas": [], "kinds": [], "places": [],
                             "hints": {"ganas": [], "arthas": []}, "verbal": False})
    if part.get("root") and not e["root"]:
        e["root"] = "√" + part["root"]
    if part.get("upasargas") and not e["upasargas"]:
        e["upasargas"] = part["upasargas"]
    e["verbal"] = e["verbal"] or part.get("verbal", False)
    e["kinds"] = list(dict.fromkeys(e["kinds"] + part.get("kinds", [])))
    for k in ("ganas", "arthas"):
        e["hints"][k] = list(dict.fromkeys(e["hints"][k] + part.get("hints", {}).get(k, [])))
    if members:
        e["members"] = members
    if place not in e["places"]:
        e["places"].append(place)


def lemmas_from_construals(construals: list[dict]) -> dict[str, dict]:
    """Lemma entries {stem, root, upasargas, kinds, places:[{locus, i, form}], hints, verbal[, members]}
    from accepted construals (stage-1 outputs); see the module docstring for the rules."""
    out: dict[str, dict] = {}
    for c in sorted(construals, key=lambda c: _locus_key(c["locus"])):
        for w in c["words"]:
            for stem, root, ups, kinds, wc, members, aroot, pada in _units(c["locus"], w):
                if not stem or wc in SKIP_CLASSES:
                    continue
                place = {"locus": c["locus"], "i": w["i"], "form": w["form"], **({"pada": pada} if pada else {})}
                content_members = [m for m in (members or []) if m.get("word_class") not in SKIP_CLASSES
                                   and m.get("stem") and m["stem"] != "nañ"]
                compound = bool(members)
                key, part = _lexeme(stem, root, ups, kinds + (["samāsa"] if compound else []), aroot, compound)
                _merge(out, key, part, place, [m["stem"] for m in members] if compound else None)
                for m in content_members:                       # a member is never a verb form
                    mkey, mpart = _lexeme(m["stem"], m.get("root"), [], ["member"], None, False, member=True)
                    mpart["kinds"] = ["member"]
                    _merge(out, mkey, mpart, place)
    return out


def _locus_key(locus: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", locus))


# ------------------------------------------------------------------ text helpers
_APPARATUS = re.compile(r"\([^()]*[A-Za-z][^()]*\)|//\s*\(BhGR_[^)]*\)|\(BhGR_[^)]*\)|(?i:bhgr)_[\w.\-–]+|//\s*\d+\s*//|//|[\[\]]")


def iast(text: str) -> str:
    return re.sub(r"\s+", " ", L.to_iast(unicodedata.normalize("NFC", text))).strip()


def _cut(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit]
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > limit * 0.6 else cut).rstrip(" ,;|") + " …"


def _deva(s: str) -> str:
    return L.to_deva(s)


def _sig(word: str) -> str:
    return L.pada_core(word)


_HOMORGANIC = {**dict.fromkeys("kgṅ", "ṅ"), **{"kh": "ṅ", "gh": "ṅ"}, **dict.fromkeys("cjñ", "ñ"),
               **dict.fromkeys("ṭḍṇ", "ṇ"), **dict.fromkeys("tdn", "n"), **dict.fromkeys("pbm", "m")}


def spellings(stem: str) -> list[str]:
    """The stem with anusvāra before a stop and with the homorganic nasal (ahaṃkāra / ahaṅkāra):
    the kośas and the Amarakośa copies follow either convention."""
    homo = re.sub(r"ṃ(?=([kgcjṭḍtdpb]))", lambda m: _HOMORGANIC[m.group(1)], stem)
    anus = re.sub(r"[ṅñṇnm](?=[kgcjṭḍtdpb])", "ṃ", stem)
    return list(dict.fromkeys([stem, homo, anus]))


def _citation_root(aupadesika: str) -> str:
    """Dhātupāṭha aupadeśika -> the SKD/VCP root headword: काक्षिँ -> काक्ष, विजिँर् -> विज,
    ओँविजीँ -> विज, प्रीङ् -> प्री."""
    s = re.sub(r"^(?:ञि|टु|डु|ओँ)", "", aupadesika)
    s = re.sub(r"[िीुूृॄ]ँ(?:र्)?$", "", s)
    s = re.sub(r"[ङञ]्$", "", s)
    return s.replace("ँ", "").rstrip("्")


# ------------------------------------------------------------------ dhātu
def _vrtti_rows(dp: dict) -> list[dict]:
    con = M._db()
    rows = con.execute("SELECT u.*, r.match AS how FROM roots r JOIN units u ON u.uid = r.uid "
                       "WHERE r.baseindex = ?", (dp["baseindex"],)).fetchall()
    return [dict(r) for r in rows if r["work"] in DV_WORKS and "own no." in r["label"]]


def _strip_head(text: str, dp: dict) -> str:
    """Drop the entry's head (aupadeśika + artha) from a vṛtti text."""
    key = M.nk(dp["key"])
    acc = ""
    for pos, ch in enumerate(text[:80]):
        acc += M.nk(ch)
        if acc.endswith(key[-max(3, len(key) // 2):]) and len(acc) >= len(key) - 2:
            return text[pos + 1:]
    return text


def _clean_vrtti(text: str) -> str:
    t = text
    for _ in range(3):
        t = re.sub(r"\([^()]*\)|\[[^\[\]]*\]", " ", t)
    t = re.sub(r"[\"'’‘“”]+", "", t)
    t = re.sub(r"[०-९]+", "", t)
    t = re.sub(r"\s*-\s*", " ", t)
    return re.sub(r"\s+", " ", t).strip(" ।,-")


def _mention_pos(text: str, entry: dict, citation: set[str] = frozenset()) -> tuple[int, int] | None:
    """(position, strength) of the first token of a Devanāgarī vṛtti text that names this lemma:
    a nominal lemma's inflected form (folded token equals a lemma key: भक्तः, not भक्तिः; the root's
    own citation token such as मन is not the noun manas) -> 4; a token beginning with all the lemma's
    upasargas + root (उद्विजते for udvij / udvega) -> 4; with only the last upasarga (उपासितः for
    paryupās) -> 3."""
    keys = set(M.lemma_keys(M.to_slp(entry["stem"]))) if not entry.get("verbal") else set()
    prefixes = []
    ups, root = entry.get("upasargas") or [], (entry.get("root") or "").lstrip("√")
    if ups and root:
        prefixes = [(M.to_slp(join_upasargas(ups[i:], root)), 4 if i == 0 else 3) for i in range(len(ups))]
    best = None
    for m in re.finditer(r"[ऀ-ॿ]+", text):
        tok = M.deva_to_slp(m.group(0))
        if keys and tok not in citation and M.fold(tok) in keys:
            return m.start(), 4
        for pre, strength in prefixes:
            if len(pre) >= 3 and tok.startswith(pre):
                if strength == 4:
                    return m.start(), 4
                best = best or (m.start(), strength)
    return best


def _windows(text: str, entry: dict, limit: int, citation: set[str]) -> list[tuple[int, str]]:
    """(score, window) candidates from a cleaned vṛtti text: the opening, and the lemma's mention."""
    out = [(0, text[: limit * 2])]
    hit = _mention_pos(text, entry, citation)
    if hit is not None:
        a = max(0, hit[0] - 40)
        out.append((hit[1], ("…" if a else "") + text[a: a + limit * 2]))
    return out


def dhatu_section(entry: dict, limit: int = CAPS["vrtti"]) -> dict:
    """Dhātupāṭha entries of the root and up to `limit` Dhātuvṛtti windows (2 per work)."""
    root = (entry.get("root") or "").lstrip("√")
    if not root:
        return {"entries": [], "vrtti": []}
    dps = M.root_dp_entries(root)
    hints = entry.get("hints") or {}
    sel = [d for d in dps if d["gana"] in hints.get("ganas", [])] if hints.get("ganas") else dps
    if hints.get("arthas"):
        by_artha = [d for d in sel if any(_norm(iast(d["artha_raw"])).startswith(_norm(a)[:4])
                                          for a in hints["arthas"])]
        sel = by_artha or sel
    sel = sel or dps
    scored = []
    for d in sel:
        rows = _vrtti_rows(d)
        texts = [(r, _clean_vrtti(_strip_head(r["text"], d))) for r in rows]
        citation = {d["aup_slp"].replace("~", ""), d["dhatu_slp"]}
        named = any(_mention_pos(t, entry, citation) is not None for _, t in texts)
        scored.append((not named, d["gana"], d["baseindex"], d, texts, citation))
    scored.sort(key=lambda x: x[:3])
    entries, cands = [], []
    for n, (_, _, _, d, texts, citation) in enumerate(scored, 1):
        did = f"D{n}"
        entries.append({"id": did, "dp": d["baseindex"], "aupadesika": iast(d["aupadeshik"]),
                        "gana": f"{d['gana']} {L.GANA_NAMES.get(d['gana'])}", "artha": iast(d["artha_raw"])})
        artha_core = M.nk(d["artha"])[:3]
        for r, t in texts:
            if not t:
                continue
            for score, win in _windows(t, entry, CAPS["vrtti_text"], citation):
                if score == 0 and M.nk(t[:12]).startswith(artha_core):
                    score = 5                                   # the opening glosses the artha
                if score == 0 and r["work"] in ("dhatupradipa", "kshiratarangini"):
                    score = 1                                   # derivatives and short glosses
                order = list(DV_WORKS).index(r["work"])
                cands.append((-score, n, order, did, r, win))
    cands.sort(key=lambda x: x[:3])
    vrtti, seen, per_work = [], set(), {}
    if any(c[0] < 0 for c in cands):                  # a bare opening (grammar talk) only when nothing better
        cands = [c for c in cands if c[0] < 0]
    for neg, n, order, did, r, win in cands:
        text = _cut(iast(win), CAPS["vrtti_text"])
        key = _norm(text)[:60]
        if key in seen or per_work.get(r["work"], 0) >= 2 or len(text) < 12:
            continue
        seen.add(key)
        per_work[r["work"]] = per_work.get(r["work"], 0) + 1
        own = re.search(r"own no\. (\d+)", r["label"])
        vrtti.append({"id": f"{did}.v{sum(1 for v in vrtti if v['id'].startswith(did + '.')) + 1}",
                      "work": DV_WORKS[r["work"]] + (f" {own.group(1)}" if own else ""), "text": text})
        if len(vrtti) >= limit:
            break
    vrtti.sort(key=lambda v: v["id"])
    return {"entries": entries, "vrtti": vrtti}


# ------------------------------------------------------------------ Amara, Nirukta
_AMARA_LABEL = re.compile(r"Amara (\d+)\.(\d+)\.[\d–]+.*?v\.(\d+)")


def _exact_hits(lemma: str, section: str, work: str | None = None):
    """Whole-token hits ('='); failing those, 'joined' hits whose token BEGINS with the lemma followed by
    a case ending in sandhi (भक्तमन्धो), never a lemma inside another word (vibhaktastutim). Every
    nasal spelling of the lemma is tried."""
    seen, out = set(), []
    for sp in spellings(lemma):
        for h in _exact_hits_one(sp, section, work):
            if h[2]["uid"] not in seen:
                seen.add(h[2]["uid"])
                out.append(h)
    eq = [h for h in out if h[0] == 0]
    return eq or out


def _exact_hits_one(lemma: str, section: str, work: str | None):
    slp = M.to_slp(lemma)
    keys = [k for k in M.lemma_keys(slp) if len(k) >= 3]
    hits = [h for h in M._hits(slp, section) if work is None or h[2]["work"] == work]
    eq = [h for h in hits if h[0] == 0]
    if eq:
        return eq

    def starts(r) -> bool:
        return any(t.startswith(k) and M._inflected_residue(k, t[len(k):len(k) + 2])
                   for t in r["slp"].split() for k in keys)
    return [h for h in hits if h[0] == 1 and starts(h[2])]


def amara_section(entry: dict) -> list[dict]:
    if entry.get("verbal"):
        return []
    out = []
    for rank, how, r, needle in _exact_hits(entry["stem"], "kosha", "amarakosha")[: CAPS["amara"]]:
        m = _AMARA_LABEL.search(r["label"])
        locus = f"Amara {m.group(1)}.{m.group(2)}.{m.group(3)}" if m else r["label"].split(" = ")[0]
        out.append({"id": f"A{len(out) + 1}", "locus": locus, "text": iast(r["text"])})
    return out


def nirukta_section(entry: dict) -> list[dict]:
    if entry.get("verbal"):
        return []
    slp = M.to_slp(entry["stem"])
    keys = M.lemma_keys(slp)

    def nirvacana(r) -> bool:
        toks = r["slp"].split()
        return any(M.fold(a) in keys and b.startswith("kasmA") for a, b in zip(toks, toks[1:]))

    hits = sorted(_exact_hits(entry["stem"], "nirukta"), key=lambda h: (not nirvacana(h[2]), h[2]["uid"]))
    out = []
    for rank, how, r, needle in hits[: CAPS["nirukta"]]:
        text = M._window(r["text"], needle, CAPS["nirukta_text"] * 2 // 3)
        out.append({"id": f"N{len(out) + 1}", "locus": r["label"], "text": _cut(iast(text), CAPS["nirukta_text"])})
    return out


# ------------------------------------------------------------------ kośa (SKD, VCP)
_VERB_ENTRY = re.compile(r"(?:स|अ)क\s?[०ं]|कविकल्पद्रुम")
_DEVA_UPA = {"ud": ["उद्", "उत्"], "nis": ["निर्", "निस्"], "dus": ["दुर्", "दुस्"], "sam": ["सम्"], "ā": ["आङ्", "आ"]}


def headwords(entry: dict) -> list[str]:
    """Devanāgarī headword spellings: the stem, its citation forms, SKD's r-doubling."""
    out = []
    for sp in spellings(entry["stem"]):
        out += [v for v in M.headword_variants(sp) if v not in out]
    stem = entry["stem"]
    s = M.to_slp(stem)
    extra = []
    if s.endswith("as") or s.endswith("is") or s.endswith("us"):
        extra.append(s[:-1] + "H")
    if s.endswith("at"):
        extra.append(s[:-2] + "An")
    if s.endswith("in"):
        extra.append(s[:-2] + "I")
    if s.endswith("f"):
        extra.append(s[:-1] + "A")
    for x in extra:
        d = M.slp_to_deva(x)
        if d not in out:
            out.append(d)
    return out


_CITATION = re.compile(r"yathā\s*(?:,|--|$)|^yathā\b|adhyāy|khaṇḍe|purāṇe|tatraiva|māhātmy|ślokaḥ|paricchedaḥ"
                       r"|^atha\b|^iti śrī|^api ca$|^ca$|^\W*$|^[\d\s.,;:*()-]+$|^\S+\s+[\d\s,]+$|^[^\s]+0$")
_INLINE_REF = re.compile(r"(?:[^\s|()]+0\s+)+(?:\d+\s*[,.]?\s*)+(?:a0)?")


def kosha_text(text: str, limit: int) -> str:
    """A Cologne SKD/VCP record reduced to its glosses: quotations and inline references (bhā0 sa0 1 a0)
    dropped, then every '|'-segment that is only a citation (yathā, …, chapter, purāṇa and khaṇḍa
    references) dropped; ≤ limit characters."""
    t = re.sub(r"“[^”]*”|\"[^\"]*\"|[“”]", " ", text)
    t = _INLINE_REF.sub(" ", iast(t))
    segs = [x.strip(" ,-()") for x in re.split(r"\s*\|+\s*", t)]
    keep = [x for x in segs if x and not _CITATION.search(x)]
    return _cut(re.sub(r"\s+", " ", " | ".join(keep)).strip(), limit)


_UPA_DEVA = "|".join(sorted({re.escape(d) for u in UPASARGAS for d in
                              ([L.to_deva(u)] + ([L.to_deva(u) + "्"] if u[-1] not in "aāiīuū" else []))}
                             | {"उद्", "उत्", "निर्", "दुर्", "आङ्"}, key=len, reverse=True))
_NEXT_PARA = re.compile(rf"(?:^|[।॥|\s])(?:(?:{_UPA_DEVA})\s*--\s*)+|\(\s*(?:{_UPA_DEVA})(?:\s*\+\s*(?:{_UPA_DEVA}))*\s*\)")


def _upa_markers(ups: list[str]) -> list[re.Pattern]:
    forms = [_DEVA_UPA.get(u, [_deva(u) + "्" if u[-1] not in VOWELS else _deva(u)]) for u in ups]
    pats = []
    for combo in itertools.product(*forms):
        bare = [c.rstrip("्") if c.endswith("्") else c for c in combo]
        pats.append(re.compile(r"(?<!-)" + r"\s*--\s*".join(map(re.escape, combo)) + r"\s*--"))  # VCP
        pats.append(re.compile(r"\(\s*" + r"\s*\+\s*".join(map(re.escape, combo)) + r"\s*\)"))      # SKD
        if bare != list(combo):
            pats.append(re.compile(r"\(\s*" + r"\s*\+\s*".join(map(re.escape, bare)) + r"\s*\)"))
    return pats


def kosha_section(entry: dict, lim: int = CAPS["kosha_text"]) -> list[dict]:
    out = []
    if entry.get("verbal"):
        root = entry["root"].lstrip("√")
        variants = list(dict.fromkeys([_deva(root).rstrip("्"), _deva(root)] +
                                      [_citation_root(d["aupadeshik"]) for d in M.root_dp_entries(root)]))
        ups = entry.get("upasargas") or []
        for name in ("skd", "vcp"):
            recs = []
            for v in variants:
                recs = [e for e in L.kosha_lookup(v, [name]) if _VERB_ENTRY.search(e["text"][:160])]
                if recs:
                    break
            picked = []
            for e in recs:
                text = e["text"]
                if ups:
                    found = [m for p in _upa_markers(ups) for m in [p.search(text)] if m]
                    if not found:
                        continue
                    m0 = min(found, key=lambda m: m.start())
                    nxt = _NEXT_PARA.search(text, m0.end())
                    text = text[m0.start(): nxt.start() if nxt else None]
                picked.append((e, text))
            if ups and not picked:                       # no paragraph for these upasargas: root heads
                picked = [(e, e["text"][:200]) for e in recs]
            for e, text in picked[: CAPS["kosha_per_dict"]]:
                out.append({"id": f"K{len(out) + 1}", "dict": name, "headword": iast(e["headword"]),
                            "locus": f"{name}#{e['locus'].rsplit('#', 1)[1]}",
                            "text": kosha_text(text, lim)})
        return out
    variants = headwords(entry)
    for name in ("skd", "vcp"):
        rows, seen = [], set()
        for v in variants:
            for e in L.kosha_lookup(v, [name]):
                if e["locus"] not in seen and e["headword"] == v:
                    seen.add(e["locus"])
                    rows.append(e)
        for e in rows[: CAPS["kosha_per_dict"]]:
            out.append({"id": f"K{len(out) + 1}", "dict": name, "headword": iast(e["headword"]),
                        "locus": f"{name}#{e['locus'].rsplit('#', 1)[1]}",
                        "text": kosha_text(e["text"], lim)})
    return out


# ------------------------------------------------------------------ occurrences and glosses
def _who(raw: str) -> str:
    name = re.sub(r"\s*\(gita/gita\)$", "", raw).strip()
    name = re.sub(r"^Sri\s+", "", name)
    return WHO.get(name, name)


def _clean_clause(text: str) -> str:
    t = _APPARATUS.sub(" ", unicodedata.normalize("NFC", text))
    t = re.sub(r"[A-Za-z]*\d+[A-Za-z_.\d]*", " ", t) if not re.search(r"[a-zāīūṛṣṇṭḍśṅñṃḥ]{3}", t) else t
    t = t.replace("?", ",").replace("--", ",")
    t = iast(t)
    t = re.sub(r"\s*,\s*(,\s*)*", ", ", t)
    return re.sub(r"\s+", " ", t).strip(" ,")


def _residue_ok(base: str, residue: str) -> bool:
    """Does what follows a word's base inside a joined token begin like its own ending in sandhi
    (कूटस्थमिति, प्रियो, भक्ताः) rather than another word (प्रियवियोगे, प्रियलाभे)?"""
    if not residue:
        return True
    ok = "ḥṃmsśṣrnoeā"
    if base[-1:] in "iī":
        ok += "y"
    if base[-1:] in "uū":
        ok += "v"
    return residue[0] in ok


_NOT_A_WORD_BEFORE = {"a", "an", "na", *UPASARGAS, "nir", "dur", "ut", "saṃ"}


def _prefix_ok(prefix: str) -> bool:
    """What precedes the word inside a joined token must be a word (मामुपासते), not a negation or an
    upasarga that makes another word (apriyam, vibhaktam)."""
    return not prefix or (len(prefix) >= 2 and prefix not in _NOT_A_WORD_BEFORE)


def _one_off(a: str, b: str) -> bool:
    return len(a) == len(b) and sum(x != y for x, y in zip(a, b)) <= 1


def _word_hits(tokens: list[str], pada: str, variant: bool = False) -> list[int]:
    """Indices of clause tokens that are this pada: the same word in any sandhi form, or a joined token
    (Devanāgarī commentaries write मामुपासते) that contains it with its own ending. `variant` also
    accepts a reading differing in one letter at the start of a token (mānāpamānayoḥ for BORI
    mānāvamānayoḥ), for bases of eight or more letters."""
    sig = L.sa_sig(pada)
    base = sig[0]
    hits = []
    for k, t in enumerate(tokens):
        n = L.norm_sa(t)
        if not n:
            continue
        if variant:
            if len(base) >= 8 and _one_off(n[:len(base)], base) and _residue_ok(base, n[len(base):]):
                hits.append(k)
            continue
        if L._sig_equal(sig, L.sa_sig(t)):
            hits.append(k)
        elif len(base) >= 4 and L.sa_sig(t)[0] != base:    # same stem, other case: another word here
            pos = n.find(base)
            while pos >= 0:
                if _residue_ok(base, n[pos + len(base):]) and _prefix_ok(n[:pos]):
                    hits.append(k)
                    break
                pos = n.find(base, pos + 1)
    return hits


def _context_score(tokens: list[str], k: int, neighbours: list[str]) -> int:
    near = " ".join(L.norm_sa(t) for t in tokens[max(0, k - 4): k + 5])
    return sum(1 for nb in neighbours if len(_sig(nb)) >= 3 and _sig(nb) in near)


def clause_window(clause: str, pada: str, limit: int = CAPS["clause"], neighbours: list[str] = (),
                  variant: bool = False, firm: int | None = None) -> str:
    """The clause cut to ≤ limit characters around the glossed word: one word before it, then onward
    to the first pause after ≥ GLOSS_SOFT characters or to GLOSS_FIRM characters at a word boundary.
    When the word occurs twice, the hit nearest the verse's neighbouring words is used. '' when the
    clause does not contain the word as a word."""
    tokens = _clean_clause(clause).split()
    hits = _word_hits(tokens, pada, variant) if tokens else []
    if not hits:
        return ""
    k = max(hits, key=lambda h: (_context_score(tokens, h, list(neighbours)), -h))
    start = max(0, k - 1)
    out, n = [], 0
    for j, t in enumerate(tokens[start:], start):
        if n + len(t) + 1 > limit - 2 and out:
            break
        out.append(t)
        n += len(t) + 1
        past_word = j > k
        if past_word and ((n >= GLOSS_SOFT and t[-1:] in ",;|") or n >= (firm or GLOSS_FIRM)):
            break
    text = " ".join(out).rstrip(" ,;|")
    if start + len(out) < len(tokens):
        text += " …"
    return ("… " if start else "") + text


GLOSS_SOFT, GLOSS_FIRM = 30, 64
FILLER = {"iti", "ca", "tu", "hi", "eva", "api", "vā", "atha", "ataḥ", "tathā", "yathā", "arthaḥ", "ityarthaḥ",
          "āha", "ityāha", "tadāha", "ucyate", "uktam", "ityuktam", "pūrvavat", "ityādi", "hīti", "ceti", "yadvā"}
_ITI_TAIL = ("ityarthaḥ", "ityāha", "apīti", "pīti", "iti", "īti", "eti", "ity")


def _verse_sigs(p: dict) -> set[str]:
    words = p["iast"].replace("|", " ").split()
    for c in p.get("split_candidates") or []:
        words += c.get("tokens") or []
    return {_sig(w) for w in words if _sig(w)}


def _verse_word(tok: str, verse_sigs: set[str]) -> bool:
    n = L.norm_sa(tok)
    if n in FILLER or _sig(tok) in verse_sigs:
        return True
    for tail in _ITI_TAIL:                                # pratīka + iti: kūṭasthamiti, abhyāse 'pīti
        if n.endswith(tail) and len(n) > len(tail) + 2:
            head = n[: -len(tail)]
            if any(_sig(h) in verse_sigs for h in (head, head + "ḥ", head.rstrip("m") + "ṃ", head + "a")):
                return True
    return False


def quotes_verse(text: str, verse_sigs: set[str]) -> bool:
    """True when every word of a clause window is a word of the verse, a filler, or a pratīka with iti:
    the commentator repeats or announces the mūla here and glosses nothing."""
    toks = [t for t in re.findall(r"[^\s,;|…']+", text)]
    content = [t for t in toks if L.norm_sa(t) not in FILLER]
    return all(_verse_word(t, verse_sigs) for t in content)


def _clause_key(text: str) -> str:
    return " ".join(_sig(t) for t in re.findall(r"[^\s,;|…]+", text) if _sig(t))


@functools.lru_cache(maxsize=1024)
def commentary(locus: str) -> dict:
    return json.loads((PACKETS / "commentary" / f"{locus}.json").read_text(encoding="utf-8"))


def _searched_glosses(locus: str, needle: str) -> list[dict]:
    """[{who, text, variant}] — per commentator, the first clause of the verse's commentary that
    contains the needle as a word (failing that, as a one-letter reading variant): used when the
    packet has no glosses for a token (sandhi-joined padas, variant readings)."""
    out = []
    for psg in commentary(locus)["passages"]:
        spans = [psg["text"][a:b] for a, b in L.clauses_of(psg["text"])]
        for variant in (False, True):
            clause = next((c for c in spans if _word_hits(_clean_clause(c).split(), needle, variant)), None)
            if clause:
                out.append({"who": psg["who"], "text": clause, "variant": variant})
                break
    return out


def occurrences_section(entry: dict, firm: int | None = None) -> list[dict]:
    out, seen = [], {}
    for n, pl in enumerate(sorted(entry["places"], key=lambda p: (_locus_key(p["locus"]), p["i"])), 1):
        oid = f"O{n}"
        p = verse_packet(pl["locus"])
        tok = next((t for t in p["tokens"] if t["i"] == pl["i"]), {"token": pl["form"], "glosses": []})
        needle = pl.get("pada") or tok["token"]
        raw = tok["glosses"] if tok["glosses"] and not pl.get("pada") else _searched_glosses(pl["locus"], needle)
        items, vsig = [], _verse_sigs(p)
        nbrs = [t["token"] for t in p["tokens"] if t["i"] in (pl["i"] - 1, pl["i"] + 1)]
        repeated = sum(1 for t in p["tokens"] if _sig(t["token"]) == _sig(tok["token"])) > 1
        by_person: dict[str, tuple[int, int, str]] = {}   # who -> (context score, order, window)
        for order, g in enumerate(raw):
            who = _who(g["who"])
            text = clause_window(g["text"], needle, neighbours=nbrs, variant=g.get("variant", False), firm=firm)
            if not text or quotes_verse(text, vsig):
                continue
            score = _context_score(text.split(), len(text.split()) // 2, nbrs) if repeated else 0
            if who not in by_person or score > by_person[who][0]:
                by_person[who] = (score, by_person.get(who, (0, order))[1], text)
        for who, (_, _, text) in sorted(by_person.items(), key=lambda kv: kv[1][1]):
            key = _clause_key(text)
            same = next((it for it in items if key and it["_k"] == key), None)   # identical words only
            if same:
                same["who"].append(who)
                continue
            items.append({"who": [who], "clause": text, "_k": key})
        glosses = []
        for j, it in enumerate(items, 1):
            gid = f"{oid}.g{j}"
            if it["_k"] in seen:
                glosses.append({"id": gid, "who": it["who"], "same_as": seen[it["_k"]]})
            else:
                seen[it["_k"]] = gid
                glosses.append({"id": gid, "who": it["who"], "clause": it["clause"]})
        out.append({"id": oid, "locus": pl["locus"], "form": pl["form"], "verse": p["iast"].replace("\n", " "),
                    "glosses": glosses})
    return out


# ------------------------------------------------------------------ elsewhere in the Gītā
@functools.lru_cache(maxsize=1)
def inventory() -> list[dict]:
    return json.loads((PACKETS / "inventory.json").read_text(encoding="utf-8"))["lemmas"]


_STOP_RE = re.compile(r"[NYRnm](?=[kKgGcCjJwWqQtTdDpPbB])")
_SLP_UPASARGAS = {"pra", "parA", "apa", "sam", "anu", "ava", "nis", "nir", "dus", "dur", "vi", "A", "ni", "aDi",
                  "api", "ati", "su", "ud", "ut", "aBi", "prati", "pari", "upa", "saM"}
_SLP_AFFIXES = {"mat", "vat", "maya", "tama", "tara", "tva", "tA", "ka", "in", "ya", "ika", "vin", "tas", "tra",
                "DA", "Sas", "vant", "mant", "ta", "na", "ana", "tf", "ti"}
_SLP_NON_FINAL = {"mad", "mat", "tvad", "tvat", "a", "an"}
_SLP_SHORT_MEMBERS = {"a", "an", "mad", "mat", "tvad", "tvat", "ga", "ja", "da", "pa", "sTa", "ha", "BU", "Df", "jYa"}
_FUSE_SLP = {"A": ("a", "A"), "e": ("i", "I"), "o": ("u", "U"), "E": ("e",), "O": ("o",)}
_SLP_VOWELS = set("aAiIuUfFxXeEoO")


def _key(slp: str) -> str:
    """SLP1 comparison key: a nasal before a stop written as anusvāra (ahaNkAra = ahaMkAra)."""
    return _STOP_RE.sub("M", slp)


def _slp_spellings(stem_slp: str) -> set[str]:
    """A member's spellings inside a compound: manas -> mano/manaH, Atman -> Atma, mat -> mad."""
    s = stem_slp[:-1] + "s" if stem_slp.endswith("H") else stem_slp
    out = {s}
    if s.endswith("as"):
        out |= {s[:-2] + "o", s[:-1] + "H"}
    if s.endswith(("is", "us")):
        out |= {s[:-1] + "r", s[:-1] + "H"}
    if s.endswith(("an", "in")):
        out.add(s[:-1])
    if s.endswith("at"):
        out.add(s[:-1] + "d")
    return {_key(x) for x in out}


@functools.lru_cache(maxsize=1)
def _vocabulary() -> frozenset[str]:
    """Compound-member spellings: every SKD and Vācaspatya headword (a Sanskrit word list) and every
    inventory lemma; upasargas and taddhita affixes are never members; members under three letters
    only from _SLP_SHORT_MEMBERS."""
    heads = {M.deva_to_slp(w) for name in ("skd", "vcp") for w in L.kosha(name)["words"]}
    heads |= {M.deva_to_slp(L.to_deva(x["lemma"])) for x in inventory() if "√" not in x["key"]}
    heads = {h for h in heads if len(h) >= 3} - _SLP_UPASARGAS - _SLP_AFFIXES
    forms = set()
    for h in heads | _SLP_SHORT_MEMBERS:
        forms |= _slp_spellings(h)
    return frozenset(forms)


@functools.lru_cache(maxsize=65536)
def _segmentable(s: str, compound_end: bool) -> bool:
    """Can `s` (SLP key) be read as a sequence of members? An a-final member may fuse with the next
    member's initial vowel (harzAmarza = harza + amarza)."""
    if not s:
        return True
    voc = _vocabulary()
    for n in range(1, min(len(s), 24) + 1):
        piece, rest = s[:n], s[n:]
        if piece in voc and not (not rest and compound_end and piece in _SLP_NON_FINAL):
            if _segmentable(rest, compound_end):
                return True
        if rest and n >= 2 and piece[-1] in _FUSE_SLP:
            for head in (piece[:-1] + "a", piece[:-1] + "A"):
                if head in voc:
                    if any(_segmentable(ini + rest, compound_end) for ini in _FUSE_SLP[piece[-1]]):
                        return True
    return False


@functools.lru_cache(maxsize=16384)
def _slp(iast_word: str) -> str:
    return M.deva_to_slp(L.to_deva(iast_word))


def contains_member(compound: str, stem: str) -> bool:
    """Is `stem` a member of `compound` (IAST stems)? The rest of the compound must read as members on
    both sides; a member right after an upasarga-final piece does not count (avibhakta), and taddhita
    affixes are not members. madbhakta/bhakta, harṣāmarṣabhayodvega/udvega, arpitamanobuddhi/manas
    -> True; vibhakta/bhakta, avibhakta/bhakta, bhaktimat/bhakti -> False."""
    probe = _norm(stem[1:] if stem[:1] in VOWELS else stem)
    if probe[:max(2, len(probe) - 2)] not in _norm(compound):   # cheap filter: the stem's core is there
        return False
    word, target = _key(_slp(compound)), _slp(stem)
    if word == _key(target):
        return False
    forms = set()
    for f in _slp_spellings(target):
        forms.add((f, ""))
        if f[0] in _SLP_VOWELS:                       # fused with a preceding a-final member
            for fused, initials in _FUSE_SLP.items():
                if f[0] in initials:
                    forms.add((fused + f[1:], "a"))
        if f.endswith("a"):                           # fused with a following vowel-initial member
            for fused in _FUSE_SLP:
                forms.add((f[:-1] + fused, "+" + fused))
    for f, how in forms:
        p = word.find(f)
        while p >= 0:
            left, right = word[:p], word[p + len(f):]
            if how == "a":
                left += "a"
            elif how.startswith("+"):
                right_opts = [ini + right for ini in _FUSE_SLP[how[1:]]]
            ok_left = not left or (_segmentable(left, False)
                                   and not any(left.endswith(u) for u in _SLP_UPASARGAS if len(u) >= 2))
            if how.startswith("+"):
                ok_right = any(_segmentable(r, True) for r in right_opts)
            else:
                ok_right = not right or _segmentable(right, True)
            if ok_left and ok_right and (left or right):
                return True
            p = word.find(f, p + 1)
    return False


def _verb_key(key: str) -> tuple[tuple[str, ...], str] | None:
    if "√" not in key:
        return None
    parts = key.split("-")
    root = parts[-1].lstrip("√")
    return tuple(_upa(p) for p in parts[:-1]), root


@functools.lru_cache(maxsize=4096)
def _occurrence_line(at: str) -> dict | None:
    """'2.47[3]' (inventory split index) -> {locus 'CH.Vh', ch, v, bori_token, line, pada}."""
    m = re.match(r"^(\d+)\.(\d+)\[(\d+)\]$", at)
    if not m:
        return None
    ch, v, k = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        occ = verse_packet(f"{ch}.{v}")["occurrences"]
    except FileNotFoundError:
        return None
    if k >= len(occ):
        return None
    bt = occ[k]["bori_token"]
    padas = L.verse_padas(ch, v)
    if bt >= len(padas):
        return None
    half = padas[bt]["half"]
    line = next((r["text"] for r in L.bori_lines() if r["ch"] == ch and r["v"] == v and r["half"] == half), "")
    return {"locus": f"{ch}.{v}{half}", "verse": f"{ch}.{v}", "bori_token": bt, "line": line,
            "pada": padas[bt]["pada"]}


def elsewhere_section(entry: dict, n_lines: int = ELSEWHERE_LINES) -> tuple[list[dict], list[str]]:
    here = {(p["locus"], p["i"]) for p in entry["places"]}
    stem = entry["stem"]
    root = (entry.get("root") or "").lstrip("√")
    want_u = tuple(entry.get("upasargas") or ())
    hits, standalone = [], set()
    for x in inventory():
        vk = _verb_key(x["key"])
        if entry.get("verbal"):
            ok = vk is not None and vk[1] == root and vk[0] == want_u
            if not ok and vk is None and root in (x.get("roots") or []):
                k = x["lemma"]
                ok = k == stem or ((k.endswith(("tum", "tvā")) or (want_u and k.endswith("ya")))
                                   and split_upasargas(k, root) == want_u)
        else:
            ok = vk is None and (x["lemma"] == stem or (len(x["lemma"]) > len(stem) and contains_member(x["lemma"], stem)))
        if ok:
            hits += [o["at"] for o in x["occurrences"]]
            if x["lemma"] == stem or entry.get("verbal"):
                standalone |= {o["at"] for o in x["occurrences"]}
    lines: dict[str, dict] = {}
    for at in hits:
        o = _occurrence_line(at)
        if not o or (o["verse"], o["bori_token"]) in here:
            continue
        e = lines.setdefault(o["locus"], {"locus": o["locus"], "forms": [], "line": o["line"], "compound": True})
        if o["pada"] not in e["forms"]:
            e["forms"].append(o["pada"])
        if at in standalone:
            e["compound"] = False
    shown_first = sorted(lines.values(), key=lambda e: (e["compound"], _locus_key(e["locus"]), e["locus"]))
    ordered = sorted(shown_first[:n_lines], key=lambda e: _locus_key(e["locus"])) + \
        sorted(shown_first[n_lines:], key=lambda e: _locus_key(e["locus"]))
    shown = [{"id": f"E{n}", "locus": e["locus"], "form": " ".join(e["forms"]), "line": e["line"]}
             for n, e in enumerate(ordered[:n_lines], 1)]
    return shown, [e["locus"] for e in ordered[n_lines:]]


# ------------------------------------------------------------------ the card
BUDGET = 6144
# Reductions applied in turn while a card is over BUDGET; nothing is dropped unidentified (elsewhere
# lines become loci in elsewhere_more; clauses and kośa texts are cut, not removed).
STAGES = ({"n_lines": ELSEWHERE_LINES, "firm": None, "kosha": CAPS["kosha_text"]},
          {"n_lines": 8, "firm": None, "kosha": CAPS["kosha_text"]},
          {"n_lines": 8, "firm": 44, "kosha": CAPS["kosha_text"]},
          {"n_lines": 4, "firm": 44, "kosha": 360})


def sanskrit_card(lemma_entry: dict, budget: int = BUDGET) -> dict:
    """The Sanskrit card of stage 2a (docs/history/gita/WORKFLOW_lexicon_first.md) for one entry of lemmas_from_construals. A card over
    `budget` bytes is rebuilt with the next of STAGES; `card["stage"]` records which one was used."""
    e = lemma_entry
    head = {"lemma": e["stem"], "root": e.get("root"), "upasargas": e.get("upasargas") or [],
            "kinds": e.get("kinds") or [], "verbal": bool(e.get("verbal"))}
    if e.get("members"):
        head["members"] = e["members"]
    fixed = {"dhatu": dhatu_section(e), "amara": amara_section(e), "nirukta": nirukta_section(e)}
    for n, st in enumerate(STAGES):
        shown, more = elsewhere_section(e, st["n_lines"])
        card = {**head, "dhatu": fixed["dhatu"], "amara": fixed["amara"], "kosha": kosha_section(e, st["kosha"]),
                "nirukta": fixed["nirukta"], "occurrences": occurrences_section(e, st["firm"]), "elsewhere": shown}
        if more:
            card["elsewhere_more"] = more
        if n:
            card["stage"] = n
        if card_bytes(card) <= budget:
            break
    return card


def card_json(card: dict) -> str:
    return json.dumps(card, ensure_ascii=False, separators=(",", ":"))


def card_bytes(card: dict) -> int:
    return len(card_json(card).encode("utf-8"))


def load_construals(run_dir: Path) -> list[dict]:
    run_dir = Path(run_dir)
    base = run_dir / "construe" if (run_dir / "construe").is_dir() else run_dir
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(base.glob("*/output.json"))]


def stats(run_dir: Path) -> dict:
    lemmas = lemmas_from_construals(load_construals(run_dir))
    sizes, empty, slow = {}, {"dhatu": [], "amara": [], "kosha": [], "gloss": []}, []
    t0 = time.time()
    for k, e in lemmas.items():
        t = time.time()
        c = sanskrit_card(e)
        slow.append((time.time() - t, k))
        sizes[k] = card_bytes(c)
        if e.get("root") and not c["dhatu"]["entries"]:
            empty["dhatu"].append(k)
        if not c["amara"]:
            empty["amara"].append(k)
        if not c["kosha"]:
            empty["kosha"].append(k)
        if not any(o["glosses"] for o in c["occurrences"]):
            empty["gloss"].append(k)
    total = time.time() - t0
    v = sorted(sizes.values())
    return {"lemmas": len(lemmas), "with_root": sum(1 for e in lemmas.values() if e.get("root")),
            "bytes_median": statistics.median(v), "bytes_max": max(v),
            "over_6kb": sorted((k for k, s in sizes.items() if s > 6144), key=lambda k: -sizes[k]),
            "build_s_total": round(total, 2), "build_s_slowest": [(round(s, 2), k) for s, k in sorted(slow)[-3:]],
            "empty": {k: (len(x), sorted(x)) for k, x in empty.items()}, "sizes": sizes}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("card")
    a.add_argument("run")
    a.add_argument("lemma")
    b = sub.add_parser("stats")
    b.add_argument("run")
    args = ap.parse_args(argv)
    if args.cmd == "card":
        lemmas = lemmas_from_construals(load_construals(Path(args.run)))
        if args.lemma not in lemmas:
            raise SystemExit(f"no lemma {args.lemma!r}; have: {', '.join(sorted(lemmas))}")
        print(json.dumps(sanskrit_card(lemmas[args.lemma]), ensure_ascii=False, indent=1))
    else:
        print(json.dumps(stats(Path(args.run)), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

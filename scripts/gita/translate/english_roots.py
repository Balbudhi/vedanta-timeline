#!/usr/bin/env python3
"""Stage 2c companion (README.md, English evidence): ENGLISH WORDS BY ETYMOLOGY — by shared root or by root image.

    build(out=DB) -> dict                       one pass over the English Wiktionary dump into SQLite
    by_sanskrit(root_or_lemma, limit=15, loans=False) -> Result   cognates and shared-PIE-root words
    by_image(image, limit=15) -> Result         words whose etymon gloss carries the picture
    by_pie(root, limit=15) -> Result            words descending from one PIE root

`english.py` finds English words by DEFINITION; this module finds them by DESCENT, so stage 2d can
mark whether an English word carries the Sanskrit root's image (√yuj ~ yoke, upa-√ās ~ assiduous)
or record that no English word shares the root. Code only; no model.

Data: kaikki.org's extraction of English Wiktionary (one JSON object per headword + part of speech
+ etymology section; every object is lang_code "en"). Per entry the build keeps:
  - the etymology text with the generated "Etymology tree"/"PIE word" header removed;
  - PIE roots (`root` templates, Proto-Indo-European terms ending in "-" in derivation templates,
    the etymology-tree lines and the prose), with Wiktionary's homograph id where one is given;
  - Sanskrit terms (templates in sa/vsn/cls and Devanāgarī words the prose attributes to Sanskrit),
    in IAST without accents; `kind` is "cognate" (cited alongside) or "loan" (the English word comes
    from it);
  - the etyma of the English word's own chain — the prose up to "Cognate…/Compare…/Related…" —
    as (language, term, gloss) in chain order, glosses being the quoted “…” text; a chain term
    cited without a gloss takes the commonest gloss the same language's term has in other entries'
    chains (`inferred`; Latin pervādō is unglossed under pervade, “spread through” under pervasive);
  - the first sense, the number of senses, whether every sense is a form-of/alt-of, and whether the
    word is native (inherited through Old English).
An FTS5 index (porter) covers the etymon glosses.

Rows: {word, pos, modern (first sense ≤100), etym (≤160, the passage that shows the link),
link ("cognate" | "pie" | "etymon-gloss"; "loan" only with loans=True), via, score}.
A Result is a list of rows with `.searched` (what was looked for and in what) and `.record()`,
which states `none: True` when nothing was found so the pipeline can record "no English word shares
this root" with its evidence.

Sanskrit matching (by_sanskrit): the query (√, hyphens, Devanāgarī, accents normalised) is expanded
into stem forms by general Sanskrit alternations: final-consonant alternants (j → k/g; 0.9), and at
0.85 vowel grades of the root vowel, the nasal present (yuj → yunak/yuñj), reduplication
(sthā → tiṣṭh, dhā → dadh) and a Cñ onset losing its nasal (jñā → jānā). A cited Sanskrit term
matches when, after up to two upasargas (×0.9 each), it is the bare root (1.0), a stem form plus a
known ending (≤0.9), or — for forms of ≥3 sounds — a stem form plus anything (0.5). Each matched term
votes, with its strength divided by the number of roots its entry names, for the PIE roots of the
entries citing it (choose_roots: the strongest tier, ≥0.8). Every English word descending from a
chosen root is a "pie" row. A citing word whose etymology names a different PIE root is dropped
as a coincidence (yūkā "louse" for √yuj); one naming none needs strength ≥0.9.
Loans (English words that descend from Sanskrit or another Indic language: Devanāgarī in their own
chain or tree) are "loan" rows, hidden unless loans=True; they still vote.
"""
from __future__ import annotations

import functools
import gzip
import json
import math
import os
import re
import sqlite3
import sys
import threading
import time
import unicodedata
from bisect import bisect_right
from collections import Counter, defaultdict
from pathlib import Path

PRAKRIYA = Path(__file__).resolve().parents[4] / "prakriya"
sys.path.insert(0, str(PRAKRIYA / "scripts/lookup"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lookup  # noqa: E402  (Devanāgarī → IAST; lookup.py is not modified)
from english import porter, us_spelling  # noqa: E402  (the stemmer FTS5's porter tokenizer uses)

DUMP = PRAKRIYA / "sources/raw/upstream_data/english/kaikki-english/kaikki.org-dictionary-English.jsonl.gz"
DB = PRAKRIYA / "tmp/english/etym.db"
SCHEMA_VERSION = "1"

SANSKRIT_CODES = {"sa", "vsn", "cls"}
SKIP_POS = {"name", "prefix", "suffix", "infix", "interfix", "circumfix", "affix", "symbol", "character",
            "abbrev", "punct", "romanization", "contraction", "phrase", "proverb"}
LINKS = ("cognate", "pie", "etymon-gloss", "loan")

# ---------------------------------------------------------------- etymology text: header, chain, etyma
_TREE_HEADS = ("Etymology tree", "PIE word")


def split_header(text: str) -> tuple[list[str], str]:
    """(tree lines, prose). Wiktionary's generated "Etymology tree" / "PIE word" header is a run of
    short "<Language> <term>" lines before the first prose line (≥5 words)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() not in _TREE_HEADS:
        return [], text.strip()
    i = 1
    while i < len(lines) and len(lines[i].split()) < 5:
        i += 1
    return [ln.strip() for ln in lines[1:i]], "\n".join(lines[i:]).strip()


# Where the word's own descent ends and comparison begins.
_CHAIN_END = re.compile(
    r"(?:^|\n|(?<=[.;:] ))(?:\*? ?(?:Cognates?\b|Cognate\b|Further cognates|Other cognates|Compare\b|Related to\b|"
    r"Doublet of\b|Doublets?\b|Akin to\b|See also\b|More at\b|cognates, etc|Displaced native|Equivalent to\b|"
    r"By surface analysis\b|Ultimately cognate\b|Also related\b|Germanic cognates|Indo-European cognates))", re.I)
_CHAIN_END_MID = re.compile(r"(?<=[,;–—] )(?:cognate (?:with|to)|akin to|compare|related to|cf\.)\b", re.I)
_ASIDE = re.compile(r"\((?:compare|cf\.|cognate|see|whence|related|also|as in|doublet)[^()]*(?:\([^()]*\)[^()]*)*\)",
                    re.I)


def chain_of(prose: str) -> str:
    """The part of the prose that traces the word's own ancestry, asides removed."""
    ends = [m.start() for m in (_CHAIN_END.search(prose), _CHAIN_END_MID.search(prose)) if m]
    chain = prose[: min(ends)] if ends else prose
    prev = None
    while prev != chain:  # nested asides
        prev, chain = chain, _ASIDE.sub("", chain)
    return chain


_LANG = re.compile(
    r"\b(?:Proto-[A-Z][a-z]+(?:[- ][A-Z][a-z]+)?|Anglo-Norman|Anglo-Latin|Old Northern French|Old Central French|"
    r"(?:(?:Old|Middle|Late|Early|Medieval|New|Vulgar|Ancient|Classical|Ecclesiastical|Koine|Byzantine|Modern|"
    r"Biblical|Vedic|Renaissance|Contemporary|Hellenistic|Epic|Attic|Ionic|Doric|Aeolic) )?"
    r"(?:Latin|Greek|English|French|Norse|High German|Low German|German|Dutch|Frisian|Saxon|Irish|Welsh|"
    r"Italian|Spanish|Portuguese|Occitan|Provençal|Sanskrit|Persian|Arabic|Hebrew|Aramaic|Hindi|Prakrit|Pali|"
    r"Gothic|Scots|Danish|Swedish|Icelandic|Catalan|Breton|Cornish|Gaulish|Hindustani|Urdu|Marathi|Nepali|"
    r"Bengali|Gujarati|Punjabi|Tamil|Malay|Turkish|Russian|Polish|Czech|Lithuanian|Avestan|Tocharian [AB]|"
    r"Armenian|Albanian|Hittite|Etruscan|Celtic|Brittonic|Norman|Picard|Walloon|Romance))\b")
_GLOSSED = re.compile(r"(?P<term>[^\s(),;:“”+=]+) \((?:(?P<tr>[^()“”]*?), )?“(?P<gloss>[^”]{1,200})”\)")
_LANG_TERM = re.compile(_LANG.pattern + r" (?P<term>[^\s(),;:“”+=.]+)(?=[.,;:]?(?:\s|$))(?! \()")


def _family(lang: str) -> str:
    for fam in ("Latin", "Greek", "Old English", "French", "Sanskrit"):
        if fam in lang:
            return fam
    return lang


def etyma(chain: str) -> tuple[list[tuple[int, str, str, str]], list[tuple[int, str, str]]]:
    """([(offset, language, term, gloss)] glossed; [(offset, language, term)] cited without a gloss).
    Offsets are positions in the chain, so the two lists merge into chain order.
    A term's language is the nearest language name before it ("from dictiō (“a speaking”)" after
    "Latin dictiōnārius" is Latin)."""
    langs = [(m.start(), m.group(0)) for m in _LANG.finditer(chain)]
    starts = [p for p, _ in langs]

    def lang_at(pos: int) -> str:
        i = bisect_right(starts, pos) - 1
        return langs[i][1] if i >= 0 else ""

    glossed = []
    for m in _GLOSSED.finditer(chain):
        term = m.group("term").strip("[]*'\"")
        if term.startswith("-") or not term:  # suffix glosses ("-ārium (“room, place”)") carry no picture
            continue
        if _LANG.fullmatch(term) or term in ("from", "of"):
            continue
        glossed.append((m.start(), lang_at(m.start()), term, m.group("gloss").strip()))
    seen = {t for _, _, t, _ in glossed}
    bare = []
    for m in _LANG_TERM.finditer(chain):
        term = m.group("term").strip("[]*'\"")
        if term and term not in seen and not term.startswith("-") and not term[0].isupper():
            bare.append((m.start("term"), m.group(0)[: m.start("term") - m.start()].strip(), term))
    return glossed, bare


# ---------------------------------------------------------------- Sanskrit normalisation
_DEVA = re.compile(r"[ऀ-ॿ᳐-᳿꣠-ꣿ]")
_VEDIC_MARKS = re.compile(r"[॑-॔᳐-᳿꣠-꣱]")
_ACCENTS = {"̀", "́", "̂"}


def _strip_vowel_accents(s: str) -> str:
    """Remove pitch accents (á à â) from vowels only: in NFD ś is s + U+0301 and must survive."""
    out = []
    base = ""
    marks: list[str] = []

    def flush():
        if base:
            vowel = base.lower() in "aeiou" or (base.lower() in "rl" and "̣" in marks)
            out.append(base + "".join(c for c in marks if not (vowel and c in _ACCENTS)))

    for ch in unicodedata.normalize("NFD", s):
        if unicodedata.combining(ch):
            marks.append(ch)
        else:
            flush()
            base, marks = ch, []
    flush()
    return unicodedata.normalize("NFC", "".join(out))


def norm_sa(s: str) -> str:
    """Comparison form of a Sanskrit term: IAST, lower case, no accents/√/hyphens/punctuation,
    nasal before a consonant written ṃ, final visarga written s."""
    s = unicodedata.normalize("NFC", s.strip())
    if _DEVA.search(s):
        s = lookup.to_iast(_VEDIC_MARKS.sub("", s))
    s = _strip_vowel_accents(s).lower().replace("ṁ", "ṃ").replace("ṝ", "ṝ")
    s = re.sub(r"[√\-‐'’ʼ`*\[\]()?.,·\s‌‍­]", "", s)
    s = re.sub(r"[ṅñṇnm](?=[kgcjṭḍtdpbśṣsh])", "ṃ", s)
    s = re.sub(r"ḥ$", "s", s)
    return s


# ---------------------------------------------------------------- Sanskrit root → stem variants
_VOWELS = ("ai", "au", "ā", "ī", "ū", "ṝ", "ṛ", "ḷ", "a", "i", "u", "e", "o")
_LONG = str.maketrans("iu", "īū")
_GRADES = {"a": ["a", "ā"], "ā": ["ā", "a", "i", "ī"], "i": ["i", "ī", "e", "ai", "ay", "āy"],
           "ī": ["ī", "i", "e", "ai", "ay", "āy"], "u": ["u", "ū", "o", "au", "av", "āv", "uv"],
           "ū": ["ū", "u", "o", "au", "av", "āv", "uv"], "ṛ": ["ṛ", "ar", "ār"],
           "ṝ": ["ṝ", "ṛ", "ar", "ār", "ir", "īr", "ur", "ūr"], "e": ["e", "i", "ay"], "o": ["o", "u", "av"],
           "ai": ["ai", "āy", "e"], "au": ["au", "āv", "o"], "ḷ": ["ḷ", "al"]}
_CODA = {"j": ["j", "k", "g", "ṃj", "ṃk", "ṃg"], "c": ["c", "k", "g", "ṃc", "ṃk"], "ś": ["ś", "k", "ṣ", "ṭ"],
         "ṣ": ["ṣ", "ṭ", "k", "ḍ"], "h": ["h", "g", "gh", "ḍh", "dh", "ṭ"], "dh": ["dh", "d", "t", "ddh", "ṃdh"],
         "bh": ["bh", "b", "p", "ṃbh"], "d": ["d", "t", "ṃd"], "t": ["t", "d"], "g": ["g", "k", "ṃg"],
         "gh": ["gh", "g", "k"], "p": ["p", "b"], "b": ["b", "p"]}
_DEASP = {"kh": "k", "gh": "g", "ch": "c", "jh": "j", "ṭh": "ṭ", "ḍh": "ḍ", "th": "t", "dh": "d", "ph": "p", "bh": "b"}
_PALATAL = {"k": "c", "g": "j", "h": "j"}
_RETRO = {"t": "ṭ", "th": "ṭh", "n": "ṇ"}
# Endings a short stem may carry and still count as a form of the root (nominal and verbal
# suffixes of the commonest derivatives; tested on whole terms, so "as" + "ura" does not qualify).
ENDINGS = sorted(set("""a ā i ī u ū as is us an in at ant vat vant mat mant ti tī ati āti anti te ate ante ete
ta tā ita īta tvā tum tu thu na nā ana anā nāti noti tṛ tar tāra itṛ tra tram man mān ma mi ya yā yati yate aya
ayati ka aka ikā ika iṣṭha īyas ra ri van vas ā u""".split()), key=len, reverse=True)
UPASARGAS = sorted("""pra parā apa saṃ sam sa anu ava nis nir niḥ niṣ dus dur duḥ duṣ vi ā ni adhi api ati su ut
ud uc uj ul abhi prati pari upa""".split(), key=len, reverse=True)


def _sounds(s: str) -> int:
    """Number of phonemes (aspirates and diphthongs count once)."""
    return len(re.findall(r"(?:[kgcjṭḍtdpb]h|ai|au|.)", s))


def _split_root(r: str) -> tuple[str, str, str]:
    """(onset, last vowel, coda)."""
    best = None
    for v in _VOWELS:
        i = r.rfind(v)
        if i >= 0 and (best is None or i > best[0] or (i == best[0] and len(v) > len(best[1]))):
            best = (i, v)
    if best is None:
        return r, "", ""
    i, v = best
    return r[:i], v, r[i + len(v):]


def variants(root: str) -> dict[str, float]:
    """Stem forms of a root (or of a lemma, taken as its own stem) → strength: the root itself 1.0,
    a final-consonant alternant 0.9, a changed vowel grade, the nasal present, reduplication or the
    class-9 stem 0.85 (a grade change can land on another root: as/ās)."""
    r = norm_sa(root)
    out: dict[str, float] = {}
    if not r:
        return out

    def add(form: str, s: float):
        form = norm_sa(form)
        for f in {form, re.sub(r"[nmñṇṅ]$", "ṃ", form)}:   # a final nasal is ṃ before a suffix's stop
            if f and out.get(f, 0) < s:
                out[f] = s

    add(r, 1.0)
    onset, v, coda = _split_root(r)
    if not v:
        return out
    codas = _CODA.get(coda, [coda, "ṃ" + coda] if coda and coda not in "nmñṇṅ" else [coda])
    grades = [g for g in _GRADES.get(v, [v])
              if not (coda and (g[-1] in "yv" or (len(v) == 1 and v in "iu" and g == v.translate(_LONG))))]
    m = re.match(r"^([kgcjṭḍtdpbh]h?)([ñnṇ])$", onset)
    if m and v == "ā" and not coda:          # jñā → jānā-ti, jānī-te (class 9, the nasal lost)
        add(m.group(1) + "ānā", 0.85)
        add(m.group(1) + "ānī", 0.85)
    for g in grades:                          # ay/av/āy/āv/uv and lengthened i/u stand only before a vowel
        for c in codas:
            add(onset + g + c, 0.9 if g == v and not c.startswith("ṃ") else 0.85)
            if onset and c and not c.startswith("ṃ") and g in ("a", "i", "u", "ṛ"):
                add(onset + g + "na" + c, 0.85)      # nasal present: yunak-, bhinad-
    # reduplication: first consonant deaspirated, velar → palatal; s+stop onsets reduplicate the stop
    rv = {"u": "u", "ū": "u", "i": "i", "ī": "i", "ṛ": "i", "ṝ": "i"}.get(v, "a")
    m = re.match(r"^(s)([kt]h?|p)(.*)$", onset)
    if m:
        stop = m.group(2)
        red = _DEASP.get(stop, stop)
        rest = "ṣ" + _RETRO.get(stop, stop) + m.group(3) if stop.startswith("t") else "ṣ" + stop + m.group(3)
        for vv in {"i", "a"}:
            for g in grades[:2]:
                add(red + vv + rest + g + coda, 0.85)
            add(red + vv + rest + coda, 0.85)       # tiṣṭh-
    else:
        m = re.match(r"^([kgcjṭḍtdpbh]h?|[mnyrlvśṣs])(.*)$", onset)
        if m:
            first = m.group(1)
            red = _PALATAL.get(_DEASP.get(first, first), _DEASP.get(first, first))
            for vv in {rv, "a"}:
                for g in grades[:3]:
                    add(red + vv + onset + g + coda, 0.85)
                if v == "ā":
                    add(red + vv + onset + coda, 0.85)    # dadh-
    return out


def match_strength(term: str, forms: dict[str, float]) -> float:
    """How strongly a normalised Sanskrit term is a form of the root whose stem forms are given."""
    best = 0.0
    cands = [(term, 1.0)]
    for _ in range(2):                                # strip up to two upasargas
        nxt = []
        for t, f in cands:
            for u in UPASARGAS:
                if t.startswith(u) and len(t) - len(u) >= 2:
                    nxt.append((t[len(u):], f * 0.9))
        cands += nxt
    for t, f in cands:
        for form, s in forms.items():
            if not t.startswith(form):
                continue
            rest = t[len(form):]
            if rest == "":
                best = max(best, s * f)
            elif rest in ENDINGS:
                best = max(best, min(s, 0.9) * f)
            elif _sounds(form) >= 3:
                best = max(best, 0.5 * f)
    return best


# ---------------------------------------------------------------- templates
_MENTION = {"cog", "cognate", "noncog", "ncog", "nc", "m", "mention", "l", "link", "m+", "l-lite", "m-lite",
            "cog-lite", "noncognate", "lang"}
_DERIV = {"der", "inh", "bor", "lbor", "uder", "bor+", "der+", "inh+", "lbor+", "slbor", "ubor", "calque",
          "cal", "psm", "sl", "obor", "der-lite", "inh-lite", "bor-lite", "learned borrowing", "borrowed",
          "derived", "inherited", "clq", "translit", "tl"}
_PARTS = {"af", "affix", "compound", "com", "prefix", "pre", "suffix", "suf", "confix", "con", "blend", "com+"}
_MOD = re.compile(r"<(\w+):([^<>]*)>")


def _split_terms(value: str) -> list[tuple[str, dict]]:
    """'manus<t:human>,manu<t:…>' → [('manus', {'t': 'human'}), ('manu', {...})]."""
    parts, depth, cur = [], 0, ""
    for ch in value:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    out = []
    for p in parts:
        mods = dict(_MOD.findall(p))
        term = _MOD.sub("", p).strip().replace("[[", "").replace("]]", "")
        if term and term != "-":
            out.append((term, mods))
    return out


def template_terms(templates: list[dict]):
    """Yield (kind, lang, term, gloss, tr, rid) for every term a template names.
    kind: 'cognate' (mentioned alongside), 'source' (an ancestor/donor), 'part' (a morpheme of one),
    'root' (a `root` template's root)."""
    for t in templates or []:
        name, a = t.get("name") or "", t.get("args") or {}
        if name == "root":
            lang = a.get("2", "")
            n = 0
            for k in sorted((k for k in a if k.isdigit() and int(k) >= 3), key=int):
                n += 1
                rid = a.get("id" if n == 1 else f"id{n}", "")
                for term, _ in _split_terms(a[k]):
                    yield "root", lang, term, "", "", rid
        elif name in _MENTION:
            lang, val = a.get("1", ""), a.get("2", "")
            for term, mods in _split_terms(val):
                for lg in lang.split(","):
                    yield ("cognate", lg, term, mods.get("t") or a.get("t") or a.get("gloss") or a.get("4", ""),
                           mods.get("tr") or a.get("tr", ""), a.get("id", ""))
        elif name in _DERIV:
            lang, val = a.get("2", ""), a.get("3", "")
            for term, mods in _split_terms(val):
                for lg in lang.split(","):
                    yield ("source", lg, term, mods.get("t") or a.get("t") or a.get("gloss") or a.get("5", ""),
                           mods.get("tr") or a.get("tr", ""), a.get("id", ""))
        elif name in ("ety", "etymon"):
            for k in sorted((k for k in a if k.isdigit()), key=int):
                m = re.match(r"^([a-z]{2,3}(?:-[a-z]{2,5})*):(.+)$", a[k])
                if m:
                    for term, mods in _split_terms(m.group(2)):
                        yield "source", m.group(1), term, mods.get("t", ""), mods.get("tr", ""), mods.get("id", "")
        elif name in _PARTS:
            lang = a.get("1", "")
            for k in sorted((k for k in a if k.isdigit() and int(k) >= 2), key=int):
                i = int(k) - 1
                for term, mods in _split_terms(a[k]):
                    yield ("part", a.get(f"lang{i}", lang), term, mods.get("t") or a.get(f"t{i}", ""),
                           mods.get("tr") or a.get(f"tr{i}", ""), a.get(f"id{i}", ""))


_TREE_MARK = re.compile(r"(?<=\S)(?:lbor|slbor|ubor|bor|der|inh|nom|calq|psm|sl|af|lbor\?|der\?|bor\?)\.$")


def _pie_key(term: str) -> str | None:
    """A PIE ROOT in comparison form ('*yewg-' → 'yewg-'), or None for a word or a suffix."""
    t = unicodedata.normalize("NFC", term.strip())
    t = _TREE_MARK.sub("", t).rstrip("?.,;:").strip().lstrip("*").strip()
    if not t.endswith("-") or t.startswith("-") or len(t) < 3 or " " in t:
        return None
    return t


_PIE_PROSE = re.compile(r"Proto-Indo-European (\*[^\s,;()“”]+)")
_DEVA_WORD = re.compile(r"((?:[ऀ-ॿ᳐-᳿꣠-ꣿ]+)(?: [ऀ-ॿ᳐-᳿꣠-ꣿ]+)?)"
                        r"(?: \((?P<inner>[^()]*)\))?")
_INDIC_LANG = re.compile(r"\b(?:Vedic Sanskrit|Classical Sanskrit|Sanskrit|Hindi|Marathi|Nepali|Hindustani|Prakrit|"
                         r"Bengali|Gujarati|Punjabi|Konkani|Maithili|Bhojpuri|Awadhi|Pali|Urdu|Braj|Rajasthani|"
                         r"Sindhi|Assamese|Odia|Oriya|Dogri|Kashmiri|Magahi|Newar|Sinhalese|Tamil|Telugu)\b")


def sanskrit_in_prose(prose: str) -> list[tuple[str, str, str, str]]:
    """[(shown, tr, gloss, kind)] for Devanāgarī words the prose attributes to Sanskrit."""
    langs = [(m.start(), m.group(0)) for m in _INDIC_LANG.finditer(prose)]
    starts = [p for p, _ in langs]
    out = []
    for m in _DEVA_WORD.finditer(prose):
        i = bisect_right(starts, m.start()) - 1
        if i < 0 or "Sanskrit" not in langs[i][1]:
            continue
        inner = m.group("inner") or ""
        g = re.search(r"“([^”]*)”", inner)
        tr = inner.split(",")[0].strip() if inner and not inner.startswith("“") else ""
        before = prose[max(0, langs[i][0] - 30): langs[i][0]].lower()
        kind = "loan" if re.search(r"\b(?:from|borrowed|borrowing|via)\s*$", before) else "cognate"
        out.append((m.group(1), tr, g.group(1) if g else "", kind))
    return out


# ---------------------------------------------------------------- build
def _first_sense(senses: list[dict]) -> str:
    for s in senses or []:
        gl = s.get("glosses") or s.get("raw_glosses")
        if gl:
            g = gl[0]
            if re.match(r"^Senses? relat", g) and len(gl) > 1:
                g = gl[-1]
            return g
    return ""


def _form_of(senses: list[dict]) -> bool:
    return bool(senses) and all(s.get("form_of") or s.get("alt_of") or
                                {"form-of", "alt-of"} & set(s.get("tags") or []) for s in senses)


SCHEMA = """
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE etym(id INTEGER PRIMARY KEY, text TEXT NOT NULL);
CREATE TABLE entry(id INTEGER PRIMARY KEY, word TEXT NOT NULL, pos TEXT, etym_no TEXT, gloss TEXT,
                   n_senses INTEGER, form_of INTEGER, native INTEGER, etym_id INTEGER);
CREATE TABLE pie(entry_id INTEGER, root TEXT, rid TEXT, src TEXT);
CREATE TABLE sa(entry_id INTEGER, term TEXT, shown TEXT, kind TEXT, gloss TEXT);
CREATE TABLE etymon(id INTEGER PRIMARY KEY, entry_id INTEGER, ord INTEGER, lang TEXT, term TEXT, gloss TEXT,
                    inferred TEXT);
"""
INDEXES = """
CREATE INDEX entry_word ON entry(word);
CREATE INDEX pie_root ON pie(root);
CREATE INDEX pie_entry ON pie(entry_id);
CREATE INDEX sa_term ON sa(term);
CREATE INDEX etymon_entry ON etymon(entry_id);
CREATE VIRTUAL TABLE etymon_fts USING fts5(gloss, content='etymon', content_rowid='id',
                                           tokenize='porter unicode61 remove_diacritics 2');
INSERT INTO etymon_fts(etymon_fts) VALUES('rebuild');
"""


def _named_in(shown: str, chain: str) -> bool:
    form, _, rest = _VEDIC_MARKS.sub("", shown).partition(" (")
    tr = rest.rstrip(")")
    chain = _VEDIC_MARKS.sub("", chain)
    return bool(form and form in chain) or bool(tr and tr in chain)


def parse_entry(e: dict) -> dict | None:
    """One dump object → the rows build() stores, or None when it has no etymology."""
    text = e.get("etymology_text") or ""
    templates = e.get("etymology_templates") or []
    if not text.strip() and not templates:
        return None
    tree, prose = split_header(text)
    chain = chain_of(prose)
    pies: dict[tuple[str, str], str] = {}
    sas: dict[str, tuple[str, str, str]] = {}
    native = False
    for kind, lang, term, gloss, tr, rid in template_terms(templates):
        if lang == "ine-pro" and kind in ("root", "source"):
            k = _pie_key(term)
            if k:
                pies.setdefault((k, rid or ""), "template")
        if lang in SANSKRIT_CODES and not term.startswith("-"):
            shown = term + (f" ({tr})" if tr else "")
            key = norm_sa(term if _DEVA.search(term) or not tr else tr)
            if key:
                sas[key] = (shown, "loan" if kind in ("source", "part") else "cognate", gloss)
        if kind == "source" and lang in ("ang", "gem-pro", "gmw-pro"):
            native = True
    for ln in tree:
        if ln.startswith("Proto-Indo-European "):
            k = _pie_key(ln.split(" ", 1)[1])
            if k:
                pies.setdefault((k, ""), "tree")
        if ln.startswith("Old English "):
            native = True
    for m in _PIE_PROSE.finditer(chain):
        k = _pie_key(m.group(1))
        if k:
            pies.setdefault((k, ""), "prose")
    for shown, tr, gloss, kind in sanskrit_in_prose(prose):
        key = norm_sa(shown)
        if key and key not in sas:
            sas[key] = (shown + (f" ({tr})" if tr else ""), kind, gloss)
    # A Sanskrit form named in the word's own chain is its source ("loan"); one named only among the
    # comparisons is a cognate. If the word comes from Sanskrit or another Indic language (its chain
    # holds Devanāgarī), every Sanskrit form it cites is its ancestry.
    sas = {k: (sh, "loan" if _named_in(sh, chain) else "cognate", g) for k, (sh, _, g) in sas.items()}
    if _DEVA.search(chain) or any(_DEVA.search(t) for t in tree) or any(k == "loan" for _, k, _ in sas.values()):
        sas = {k: (sh, "loan", g) for k, (sh, _, g) in sas.items()}
    if re.search(r"\bfrom Old English\b", chain, re.I):
        native = True
    # a root given both with and without a homograph id keeps the id only
    ided = {k for (k, rid) in pies if rid}
    pies = {(k, rid): s for (k, rid), s in pies.items() if rid or k not in ided}
    glossed, bare = etyma(chain)
    senses = e.get("senses") or []
    return {"word": e.get("word") or "", "pos": e.get("pos") or "", "etym_no": e.get("etymology_number") or "",
            "gloss": _first_sense(senses), "n_senses": len(senses), "form_of": int(_form_of(senses)),
            "native": int(native), "text": prose or text.strip(), "pie": pies, "sa": sas,
            "glossed": glossed, "bare": bare}


def build(out: Path | str = DB, dump: Path | str = DUMP, limit: int | None = None) -> dict:
    """One pass over the dump into a fresh SQLite file (written beside `out`, then renamed over it).
    Returns the build statistics also stored in table meta."""
    out, dump = Path(out), Path(dump)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".building")
    if tmp.exists():
        tmp.unlink()
    t0 = time.time()
    con = sqlite3.connect(tmp)
    con.executescript("PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF;" + SCHEMA)
    texts: dict[str, int] = {}
    stats = Counter()
    entries, pies, sas, ety = [], [], [], []
    bare_terms: list[tuple[int, int, str, str]] = []          # (entry, ord, lang, term) awaiting a gloss
    gloss_by_term: dict[tuple[str, str], Counter] = defaultdict(Counter)
    eid = 0
    etymon_id = 0

    def flush():
        con.executemany("INSERT INTO entry VALUES(?,?,?,?,?,?,?,?,?)", entries)
        con.executemany("INSERT INTO pie VALUES(?,?,?,?)", pies)
        con.executemany("INSERT INTO sa VALUES(?,?,?,?,?)", sas)
        con.executemany("INSERT INTO etymon VALUES(?,?,?,?,?,?,?)", ety)
        entries.clear(), pies.clear(), sas.clear(), ety.clear()

    with gzip.open(dump, "rt", encoding="utf-8") as fh:
        for line in fh:
            stats["objects"] += 1
            if limit and stats["objects"] > limit:
                break
            e = json.loads(line)
            if e.get("lang_code") != "en":
                continue
            stats["english"] += 1
            p = parse_entry(e)
            if p is None:
                continue
            eid += 1
            stats["with_etymology"] += 1
            tid = texts.get(p["text"])
            if tid is None:
                tid = texts[p["text"]] = len(texts) + 1
                con.execute("INSERT INTO etym VALUES(?,?)", (tid, p["text"]))
            entries.append((eid, p["word"], p["pos"], p["etym_no"], p["gloss"], p["n_senses"], p["form_of"],
                            p["native"], tid))
            pies.extend((eid, k, rid, src) for (k, rid), src in p["pie"].items())
            sas.extend((eid, k, shown, kind, gloss) for k, (shown, kind, gloss) in p["sa"].items())
            chain_items = sorted([(o, lang, term, gloss) for o, lang, term, gloss in p["glossed"]] +
                                 [(o, lang, term, None) for o, lang, term in p["bare"]])
            for ord_, (_, lang, term, gloss) in enumerate(chain_items):
                if gloss is None:
                    bare_terms.append((eid, ord_, lang, term))
                    continue
                etymon_id += 1
                ety.append((etymon_id, eid, ord_, lang, term, gloss, None))
                if p["word"] != term:
                    gloss_by_term[(_family(lang), term)][gloss] += 1
            if len(entries) >= 20000:
                flush()
    flush()
    # unglossed chain terms take the commonest gloss the same language's term has elsewhere
    inferred = 0
    for eid_, ord_, lang, term in bare_terms:
        c = gloss_by_term.get((_family(lang), term))
        if c:
            gloss, _ = c.most_common(1)[0]
            etymon_id += 1
            inferred += 1
            ety.append((etymon_id, eid_, ord_, lang, term, gloss, "elsewhere"))
    flush()
    con.executescript(INDEXES)
    stats.update(texts=len(texts), etyma=etymon_id, inferred_glosses=inferred,
                 pie_rows=con.execute("SELECT count(*) FROM pie").fetchone()[0],
                 sanskrit_rows=con.execute("SELECT count(*) FROM sa").fetchone()[0])
    stats["build_seconds"] = round(time.time() - t0, 1)
    meta = {"schema": SCHEMA_VERSION, "dump": str(dump), "dump_bytes": dump.stat().st_size,
            "dump_mtime": int(dump.stat().st_mtime), "built": time.strftime("%Y-%m-%dT%H:%M:%S"), **stats}
    con.executemany("INSERT INTO meta VALUES(?,?)", [(k, str(v)) for k, v in meta.items()])
    con.commit()
    con.execute("VACUUM")
    con.close()
    os.replace(tmp, out)
    meta["db_bytes"] = out.stat().st_size
    con = sqlite3.connect(out)
    con.execute("INSERT OR REPLACE INTO meta VALUES('db_bytes', ?)", (str(meta["db_bytes"]),))
    con.commit()
    con.close()
    return meta


# ---------------------------------------------------------------- queries
_local = threading.local()


def _con(db: Path = DB) -> sqlite3.Connection:
    cons = getattr(_local, "cons", None)
    if cons is None:
        cons = _local.cons = {}
    if db not in cons:
        if not Path(db).exists():
            raise FileNotFoundError(f"{db} not built; run: python3 {Path(__file__).name} build")
        cons[db] = sqlite3.connect(f"file:{db}?mode=ro", uri=True, check_same_thread=False)
    return cons[db]


class Result(list):
    """Rows, plus what was searched. `record()` is the JSON the pipeline stores."""

    def __init__(self, query: str, rows: list[dict], searched: dict):
        super().__init__(rows)
        self.query, self.searched = query, searched

    def record(self) -> dict:
        out = {"query": self.query, "rows": list(self), "none": not self, "searched": self.searched}
        if not self:
            out["note"] = self.searched.get("none_means", "")
        return out


def snippet(text: str, needle: str, n: int = 160) -> str:
    """≤n characters of `text` around the first occurrence of `needle` (the start when absent)."""
    text = re.sub(r"\s+", " ", text).strip()
    i = text.find(needle) if needle else -1
    if i < 0 or len(text) <= n:
        return text[: n - 1] + "…" if len(text) > n else text
    start = max(0, min(i - 50, len(text) - n + 1))
    if start > 0:
        sp = text.find(" ", start)
        start = sp + 1 if 0 <= sp < i else start
    s = ("…" if start else "") + text[start:]
    return s[: n - 1] + "…" if len(s) > n else s


def _clip(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


@functools.lru_cache(maxsize=4)
def _sa_terms(db: Path = DB) -> list[str]:
    return [r[0] for r in _con(db).execute("SELECT DISTINCT term FROM sa")]


def _entries(con, ids) -> dict[int, tuple]:
    ids = list(ids)
    out = {}
    for i in range(0, len(ids), 900):
        chunk = ids[i:i + 900]
        q = ("SELECT e.id, e.word, e.pos, e.gloss, e.n_senses, e.form_of, e.native, t.text FROM entry e "
             f"JOIN etym t ON t.id = e.etym_id WHERE e.id IN ({','.join('?' * len(chunk))})")
        for r in con.execute(q, chunk):
            out[r[0]] = r[1:]
    return out


def _usable(word: str, pos: str) -> bool:
    return pos not in SKIP_POS and not word.startswith("-") and not word.endswith("-")


ENGLISH_DB = lookup.ENGLISH_DB


def _known(words: list[str]) -> dict[str, tuple[int, bool]]:
    """word → (number of dictionaries in prakriya's English index that define it, in OEWN 2025).
    Empty when that index is absent; ranking then falls back to the number of Wiktionary senses."""
    if not ENGLISH_DB.exists() or not words:
        return {}
    cons = getattr(_local, "cons", None) or {}
    _local.cons = cons
    if ENGLISH_DB not in cons:
        cons[ENGLISH_DB] = sqlite3.connect(f"file:{ENGLISH_DB}?mode=ro", uri=True, check_same_thread=False)
    out = {}
    ws = sorted({w.lower() for w in words})
    for i in range(0, len(ws), 900):
        chunk = ws[i:i + 900]
        q = (f"SELECT hw, count(DISTINCT source), max(source = 'oewn2025') FROM defs WHERE hw IN "
             f"({','.join('?' * len(chunk))}) GROUP BY hw")
        for hw, n, oewn in cons[ENGLISH_DB].execute(q, chunk):
            out[hw] = (n, bool(oewn))
    return out


def _commonness(n_senses: int, native: int, word: str, known: dict | None = None) -> float:
    """0..1 preference among same-strength rows: defined by many dictionaries and by a modern one
    (else many Wiktionary senses), native, a single plain word."""
    if known:
        n, oewn = known.get(word.lower(), (0, False))
        s = 0.6 * min(1.0, n / 6) + 0.2 * oewn
    else:
        s = 0.8 * min(1.0, math.log1p(n_senses) / math.log(25))
    s += 0.1 * native + 0.1 * (" " not in word and "-" not in word and word.islower())
    return s


def _collect(rows: list[dict], limit: int) -> list[dict]:
    """Best row per word (parts of speech joined), ranked by score."""
    by_word: dict[str, dict] = {}
    for r in sorted(rows, key=lambda r: -r["score"]):
        w = by_word.get(r["word"])
        if w is None:
            by_word[r["word"]] = dict(r)
        elif r["pos"] not in w["pos"].split("/"):
            w["pos"] += "/" + r["pos"]
    return sorted(by_word.values(), key=lambda r: -r["score"])[:limit]


def _pie_rows(con, roots: list[tuple[str, str, str]], skip: set[int], limit: int) -> list[dict]:
    """English words descending from the given (root, rid, why) PIE roots. A root with a homograph id
    takes only entries carrying that id. Ranked: the root named by a `root` template (the editors'
    own classification) over one met only in a tree or the prose; entries naming few roots (not
    compounds that inherit every member's roots); native, many-sensed, plain words."""
    rows = []
    for root, rid, why in roots:
        q = ("SELECT p.entry_id, p.src, (SELECT count(DISTINCT q.root) FROM pie q WHERE q.entry_id = p.entry_id) "
             "FROM pie p WHERE p.root = ? AND p.rid = ?")
        hits = [h for h in con.execute(q, (root, rid)) if h[0] not in skip]
        ents = _entries(con, [h[0] for h in hits])
        known = _known([w[0] for w in ents.values()])
        for e, src, n_roots in hits:
            word, pos, gloss, n_senses, form_of, native, text = ents[e]
            if form_of or not _usable(word, pos):
                continue
            needle = "*" + root
            score = (0.5 + 0.3 * _commonness(n_senses, native, word, known) + 0.1 * (src == "template")
                     + 0.05 * (needle in text) - 0.05 * min(3, n_roots - 1) * (src != "template"))
            rows.append({"word": word, "pos": pos, "modern": _clip(gloss, 100), "etym": snippet(text, needle),
                         "link": "pie", "via": f"PIE *{root}" + (f" ({rid})" if rid else "") + why,
                         "score": round(score, 4)})
    return _collect(rows, max(limit * 4, 60))


def choose_roots(totals: dict, support: dict) -> list:
    """The PIE roots a Sanskrit root reaches. support = the strongest matching term behind a root,
    totals = the sum over distinct matching terms. Kept: roots whose support is within 0.04 of the
    strongest (so √as's asti outranks āsa, a grade change that lands on √ās) and ≥ 0.8 (a chance
    prefix never selects), with at least half the top total among them. A root given both with and
    without Wiktionary's homograph id keeps the id'd one."""
    if not support:
        return []
    top_s = max(support.values())
    if top_s < 0.8:
        return []
    tier = [k for k in support if support[k] >= top_s - 0.04]
    top_t = max(totals[k] for k in tier)
    keep = [k for k in tier if totals[k] >= top_t / 2]
    ided = {r for r, rid in keep if rid}
    keep = [(r, rid) for r, rid in keep if rid or r not in ided]
    return sorted(keep, key=lambda k: (-totals[k], k))


def by_sanskrit(root_or_lemma: str, limit: int = 15, loans: bool = False, db: Path = DB) -> Result:
    """English words whose etymology cites this Sanskrit root or lemma (link 'cognate'; 'loan' for
    words borrowed from it, only with loans=True), then words sharing the PIE root(s) those
    etymologies give (link 'pie'). Accepts √, hyphenated upasargas, IAST or Devanāgarī."""
    con = _con(db)
    q = root_or_lemma.strip()
    parts = [p for p in re.split(r"[-\s]+", q.replace("√", "-√")) if p]
    core = parts[-1].lstrip("√") if parts else q
    forms = variants(core)
    whole = norm_sa(q)
    if whole and whole != norm_sa(core):
        forms[whole] = 1.0
    matched: dict[str, float] = {}
    for term in _sa_terms(db):
        s = match_strength(term, forms)
        if s > 0:
            matched[term] = s
    # which entries cite them, and their PIE roots
    cites = defaultdict(list)     # entry -> [(term, strength, shown, kind)]
    for term, s in matched.items():
        for e, shown, kind in con.execute("SELECT entry_id, shown, kind FROM sa WHERE term = ?", (term,)):
            cites[e].append((term, s, shown, kind))
    ents = _entries(con, cites)
    # each matched Sanskrit term votes once, with its strength, for the PIE roots of entries citing it
    vote: dict[tuple[str, str], dict[str, float]] = defaultdict(dict)   # (root, rid) -> term -> strength
    words_of: dict[tuple[str, str], set] = defaultdict(set)
    e_roots: dict[int, set] = defaultdict(set)
    for e in cites:
        roots = con.execute("SELECT root, rid FROM pie WHERE entry_id = ?", (e,)).fetchall()
        share = 1 / max(1, len({r for r, _ in roots}))   # an entry naming three roots is unsure of each
        for root, rid in roots:
            e_roots[e].add(root)
            for term, s, _, _ in cites[e]:
                vote[(root, rid)][term] = max(vote[(root, rid)].get(term, 0), s * share)
            words_of[(root, rid)].add(ents[e][0])
    totals = {k: sum(v.values()) for k, v in vote.items()}
    support = {k: max(v.values()) for k, v in vote.items()}
    chosen = choose_roots(totals, support)
    chosen_roots = {k[0] for k in chosen}
    rows = []
    cited_ids = set()
    known = _known([w[0] for w in ents.values()])
    for e, cs in cites.items():
        word, pos, gloss, n_senses, form_of, native, text = ents[e]
        term, s, shown, kind = max(cs, key=lambda c: c[1])
        if not (s >= 1.0 or e_roots[e] & chosen_roots or (not e_roots[e] and s >= 0.9)):
            continue           # its etymology names a different PIE root: the match is a coincidence
        cited_ids.add(e)
        if not _usable(word, pos) or (kind == "loan" and not loans):
            continue
        needle = shown.split(" (")[0]
        rows.append({"word": word, "pos": pos, "modern": _clip(gloss, 100), "etym": snippet(text, needle),
                     "link": "loan" if kind == "loan" else "cognate",
                     "via": f"Sanskrit {shown.split(' (')[0]} ({term}) cited as {kind}; match {s:.2f}",
                     "score": round(1.0 + s + 0.3 * _commonness(n_senses, native, word, known), 4)})
    cog = _collect(rows, limit * 4)
    why = {k: f" — the root of {', '.join(sorted(words_of[k])[:3])}" for k in chosen}
    pie = _pie_rows(con, [(r, rid, why[(r, rid)]) for r, rid in chosen], cited_ids, limit)
    seen = {r["word"] for r in cog}
    out = (cog + [r for r in pie if r["word"] not in seen])[:limit]
    searched = {
        "normalised": norm_sa(core), "stem_forms": sorted(forms)[:40], "n_stem_forms": len(forms),
        "sanskrit_terms_matched": sorted(((t, round(s, 2)) for t, s in matched.items()), key=lambda x: -x[1])[:25],
        "entries_citing": len(cites),
        "pie_roots": [{"root": "*" + r, "rid": rid, "vote": round(totals[(r, rid)], 2),
                       "terms": sorted(vote[(r, rid)])[:6], "words": sorted(words_of[(r, rid)])[:6]}
                      for r, rid in chosen],
        "pie_roots_rejected": [{"root": "*" + r, "rid": rid, "vote": round(t, 2),
                                "support": round(support[(r, rid)], 2)} for (r, rid), t in
                               sorted(totals.items(), key=lambda kv: -kv[1]) if (r, rid) not in chosen][:8],
        "sanskrit_terms_in_db": len(_sa_terms(db)), "db": str(db),
        "none_means": (f"no English Wiktionary etymology cites a Sanskrit form of {q!r} and no PIE root was "
                       f"reached, so no English word in this data shares the root"),
    }
    return Result(q, out, searched)


def by_pie(root: str, limit: int = 15, db: Path = DB) -> Result:
    """English words whose etymology gives this PIE root ('*h₁ed-', 'h₁ed-')."""
    con = _con(db)
    k = _pie_key(root if root.rstrip("?").endswith("-") else root + "-") or root
    rows = _pie_rows(con, [(k, "", "")], set(), limit)[:limit]
    return Result(root, rows, {"pie_root": "*" + k, "db": str(db),
                               "none_means": f"no English Wiktionary etymology gives *{k}"})


# ---------------------------------------------------------------- image search
# Spatial words are kept unstemmed and matched with their near-equivalents (a closed class: the
# image's particle — "sit NEAR", "carry UP" — is what Latin ad-/ex-/per- and English up/out carry).
_KEEP = {"up", "out", "down", "off", "away", "forth", "back", "over", "under", "through", "across", "near",
         "by", "beside", "around", "about", "apart", "together", "into", "upon", "within", "before", "behind",
         "at", "toward", "towards", "everywhere", "throughout", "below", "beneath", "above", "aloft", "upward",
         "round", "asunder", "next", "nigh", "close", "to"}
_IMG_STOP = set("""a an the of be is are one oneself someone something thing it its as or and that which
for with very""".split())
_SYN = {"near": ["by", "beside", "close", "nigh", "next", "at", "to", "toward", "towards"],
        "through": ["across", "throughout"], "everywhere": ["throughout"],
        "up": ["upward", "aloft", "above"], "out": ["forth", "away", "off"], "down": ["below", "beneath", "under"],
        "around": ["about", "round"], "apart": ["asunder", "away"], "together": ["with"]}


def _gstems(text: str) -> list[str]:
    """Content stems of one gloss segment. "to" is dropped as the infinitive marker and kept as a
    preposition (the segment's last word: ad- “to”, assidēre “to sit down to”)."""
    toks = [us_spelling(w) for w in re.findall(r"[a-z]+", text.lower())]
    out = []
    for i, w in enumerate(toks):
        if w in _IMG_STOP or (w == "to" and i < len(toks) - 1):
            continue
        out.append(w if w in _KEEP else porter(w))
    return out


def _segments(gloss: str) -> list[list[str]]:
    return [st for seg in re.split(r"[,;:/]| or ", gloss) if (st := _gstems(seg))]


def image_alternatives(image: str) -> list[list[str]]:
    """'carry up/out' → [['carri','up'], ['carri','out']]; ' / ', ',' and ';' separate alternatives."""
    alts = []
    for part in re.split(r"\s+/\s+|[,;|]", image):
        toks = part.strip().split()
        if not toks:
            continue
        combos = [[]]
        for t in toks:
            combos = [c + [o] for c in combos for o in t.split("/") if o]
        for c in combos:
            st = _gstems(" ".join(c))
            if st and st not in alts:
                alts.append(st)
    return alts


def _cover(alt: list[str], stems: set[str]) -> tuple[float, float, set[str]]:
    """(weighted coverage of the image's terms by `stems`, the action's match, stems used). The first
    term, the action, weighs double; a spatial near-equivalent counts 0.6."""
    weights = [2.0] + [1.0] * (len(alt) - 1)
    got, head, used = 0.0, 0.0, set()
    for i, (t, w) in enumerate(zip(alt, weights)):
        m = 0.0
        if t in stems:
            m = 1.0
            used.add(t)
        else:
            hit = [x for x in _SYN.get(t, []) if x in stems]
            if hit:
                m = 0.6
                used.update(hit)
        got += w * m
        if i == 0:
            head = m
    return got / sum(weights), head, used


def gloss_score(alt: list[str], gloss: str, extra: set[str] = frozenset()) -> float:
    """How fully a gloss carries one image alternative: coverage of the image's terms × (0.6 + 0.4 ×
    how much of the gloss the image accounts for — mostly of its best ;/,-segment, so a list of
    synonyms is not penalised much, partly of the whole gloss). `extra` adds stems from the word's other etyma (ad “to” + sedeō “sit” = "sit to").
    0 unless this gloss itself carries the action."""
    segs = _segments(gloss)
    own = set().union(*segs) if segs else set()
    if not own:
        return 0.0
    _, head, _ = _cover(alt, own)
    if head == 0:
        return 0.0
    coverage, _, used = _cover(alt, own | set(extra))
    best_seg = max((len(used & set(sg)) / len(sg) for sg in segs if used & set(sg)), default=0.0)
    whole = len(used & own) / len(own)          # a long many-sense gloss carries the picture less
    return coverage * (0.6 + 0.4 * (0.7 * best_seg + 0.3 * whole))


def by_image(image: str, limit: int = 15, db: Path = DB) -> Result:
    """English words whose own etymon (Latin, Greek, Old English, French, PIE …) is glossed with this
    picture ("sit near", "to yoke, join", "carry up/out"). An etymon's gloss is read together with the
    glosses of the word's other first etyma (its prefix, its base), closer etyma rank higher, and a
    gloss inferred from another entry counts 0.9."""
    con = _con(db)
    alts = image_alternatives(image)
    scored = 0
    hits: dict[int, list[tuple]] = defaultdict(list)          # entry -> FTS rows carrying an action
    for alt in alts:
        words_ = [alt[0], *_SYN.get(alt[0], [])]
        expr = " OR ".join(f'"{w}"' if w in _KEEP or len(w) < 3 else f'"{w}"*' for w in words_)
        q = ("SELECT x.id, x.entry_id, x.ord, x.lang, x.term, x.gloss, x.inferred FROM etymon_fts f "
             "JOIN etymon x ON x.id = f.rowid WHERE etymon_fts MATCH ? ORDER BY bm25(etymon_fts) LIMIT 8000")
        for r in con.execute(q, (expr,)):
            scored += 1
            hits[r[1]].append(r)
    # the word's first etyma (ord ≤ 5), whose glosses compose the picture
    near: dict[int, set[str]] = defaultdict(set)
    ords: dict[int, list[int]] = defaultdict(list)
    ids = list(hits)
    for i in range(0, len(ids), 900):
        chunk = ids[i:i + 900]
        q = f"SELECT entry_id, ord, gloss FROM etymon WHERE entry_id IN ({','.join('?' * len(chunk))}) ORDER BY ord"
        for e, o, g in con.execute(q, chunk):
            ords[e].append(o)
            if len(ords[e]) <= 4:
                for sg in _segments(g):
                    near[e].update(sg)
    best: dict[int, tuple[float, tuple]] = {}
    for e, rs in hits.items():
        for r in rs:
            for alt in alts:
                s = max(gloss_score(alt, r[5]), 0.97 * gloss_score(alt, r[5], near[e]))
                s *= 0.93 ** ords[e].index(r[2]) * (0.9 if r[6] else 1.0)   # k-th glossed etymon
                if s > best.get(e, (0.0, None))[0]:
                    best[e] = (s, r)
    top = sorted(best.items(), key=lambda kv: -kv[1][0])[: limit * 20]
    ents = _entries(con, [e for e, _ in top])
    known = _known([w[0] for w in ents.values()])
    rows = []
    for e, (s, r) in top:
        word, pos, gloss, n_senses, form_of, native, text = ents[e]
        if form_of or not _usable(word, pos):
            continue
        _, _, ord_, lang, term, egloss, inferred = r
        via = f"{lang or 'etymon'} {term} “{egloss}”" + (" (gloss from another entry's etymology)" if inferred else "")
        rows.append({"word": word, "pos": pos, "modern": _clip(gloss, 100), "etym": snippet(text, term),
                     "link": "etymon-gloss", "via": _clip(via, 160),
                     "score": round(s * (0.7 + 0.3 * _commonness(n_senses, native, word, known)), 4)})
    out = _collect(rows, limit)
    searched = {"alternatives": [" ".join(a) for a in alts], "glosses_scored": scored,
                "glosses_in_db": con.execute("SELECT count(*) FROM etymon").fetchone()[0], "db": str(db),
                "none_means": f"no English word's etymon is glossed with {image!r}"}
    return Result(image, out, searched)


# ---------------------------------------------------------------- benchmark and CLI
BENCH_SANSKRIT = [("yuj", ["yoke"]), ("sthā", ["stand"]), ("jñā", ["know"]), ("man", ["mind"]),
                  ("vid", ["wit", "wise"]), ("bhṛ", ["bear"]), ("dhā", ["do"]), ("ad", ["eat"]),
                  ("as", ["is"]), ("bhū", ["be"]), ("muc", []), ("bhaj", []), ("tyaj", []), ("dviṣ", ["two"])]
BENCH_IMAGE = [("sit near", ["assiduous", "assess"]), ("carry up/out", []),
               ("go everywhere / pervade", ["pervade"]), ("anvil", []), ("tremble, shake", ["quake", "tremble"])]


def bench(limit: int = 15) -> list[dict]:
    out = []
    for kind, cases, fn in (("sanskrit", BENCH_SANSKRIT, by_sanskrit), ("image", BENCH_IMAGE, by_image)):
        for q, want in cases:
            t = time.time()
            res = fn(q, limit=limit)
            dt = time.time() - t
            ws = [r["word"] for r in res]
            out.append({"kind": kind, "query": q, "want": want,
                        "hits": {w: (ws.index(w) + 1 if w in ws else None) for w in want},
                        "top": ws[:8], "n": len(res), "seconds": round(dt, 3),
                        "pie_roots": [p["root"] for p in res.searched.get("pie_roots", [])]})
    return out


def main(argv: list[str]) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--out", default=str(DB))
    b.add_argument("--limit", type=int)
    for name in ("sanskrit", "image", "pie"):
        p = sub.add_parser(name)
        p.add_argument("query")
        p.add_argument("--limit", type=int, default=15)
        p.add_argument("--json", action="store_true")
        if name == "sanskrit":
            p.add_argument("--loans", action="store_true")
    sub.add_parser("bench")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        print(json.dumps(build(a.out, limit=a.limit), ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "bench":
        for r in bench():
            print(json.dumps(r, ensure_ascii=False))
        return 0
    if a.cmd == "sanskrit":
        res = by_sanskrit(a.query, a.limit, loans=a.loans)
    elif a.cmd == "image":
        res = by_image(a.query, a.limit)
    else:
        res = by_pie(a.query, a.limit)
    if a.json:
        print(json.dumps(res.record(), ensure_ascii=False, indent=1))
    else:
        for r in res:
            print(f"{r['word']:<16} {r['pos']:<10} {r['link']:<12} {r['via'][:70]}\n    {r['modern']}\n    {r['etym']}")
        if not res:
            print("(none)", json.dumps(res.searched, ensure_ascii=False)[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

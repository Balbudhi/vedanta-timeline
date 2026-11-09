#!/usr/bin/env python3
"""Stage 2c (README.md, English evidence): the ENGLISH TABLE for one sense — English words found BY MEANING.

    english_table(sense, image=None, pos=None, limit=25) -> [{word, pos, defs, tags, modern, fit, via}]

Code only; no model. Reads the English index built by prakriya's lookup.py (tmp/english/english.db:
Webster 1913, GCIDE, Wiktionary, OEWN 2025, Roget 1911, Moby, WordNet 3.1) read-only.

Method, per call:
  1. Split the sense (and the image) into short clauses at , ; : and read each clause's frame:
     "one who X" (agent noun), "to X" (verb), "not/without/free of X" (negated adjective),
     a single -ed word (participle), a single -ly word (adverb).
  2. Reverse dictionary: full-text search of definitions for each clause (all terms, then any term),
     each hit scored by idf-weighted coverage of the clause and by how much of the definition (or of
     one of its ;-segments) the clause accounts for. Roget groups that match a clause make their
     members candidates; a Moby list that matches makes its headword one.
     A short verb clause is also searched in its verbs' synonyms ('lifts up' ~ 'raise aloft'),
     a synonym counting 0.6 of the word itself.
  3. Thesaurus expansion: the clause's own words and phrases and the best hits are seeds; their
     OEWN/WordNet synset members, Wiktionary synonyms and Roget co-members become candidates,
     and so do words whose definition lists a best hit as a gloss ('Forbearing: … long-suffering').
  4. Attested derived forms: for verb candidates, the agent noun (-er) under an agent frame, the
     participle under a participle/adjective frame, and un-/-less forms of a negated word —
     each kept only if a source attests it (as a headword or a recorded inflection).
  5. Every candidate is defined: all its senses are scored against every clause (a definition that
     glosses it by one of the best hits inherits part of that hit's match); fit combines the
     definition match, thesaurus support from distinct seeds, the sense naming the word itself,
     part-of-speech agreement with the frame and how many sources know the word. A derived form
     inherits its verb's evidence. Inflections and spelling variants of a ranked word in the same
     role are dropped. Rows carry ≤2 short definitions from different sources, register tags of
     the matching senses, and the first modern (OEWN, else Wiktionary) sense.
"""
from __future__ import annotations

import functools
import math
import re
import sqlite3
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path

PRAKRIYA = Path(__file__).resolve().parents[4] / "prakriya"
sys.path.insert(0, str(PRAKRIYA / "scripts/lookup"))
import lookup  # noqa: E402  (constants and the index location; lookup.py is not modified)

DB = lookup.ENGLISH_DB
SENSE_SOURCES = ("webster1913", "gcide", "wiktionary", "oewn2025", "wordnet3.1")
MODERN_SOURCES = ("oewn2025", "wiktionary")
REGISTER = set(lookup.REGISTER_TAGS) | {"colloquial", "informal", "slang", "dialectal", "provincial",
                                        "nonstandard", "scottish"}
JUNK_POS = {"name", "prefix", "suffix", "symbol", "character", "abbrev", "punct", "infix", "interfix",
            "affix", "circumfix", "num", "romanization", "prop. n.", "prop. a.", "contraction", "det", "pron",
            "conj", "prep", "article", "particle"}
STOP = set("""a an the of to in on at by for with from into onto upon as or and nor but if than then so
such be is are was were been being am do does did done have has had having it its this that these those
who whom whose which what one ones someone something somebody person people thing things he she they
we you i me my your his her their our us them him there here very more most much many any some all no
each every own same other another also just only even being way manner state quality act kind sort
can could may might must shall should will would under about through within across toward towards
among during while""".split())
PARTICLES = {"up", "out", "forth", "down", "over", "off", "back", "away", "under", "fore"}
NEG_WORDS = {"not", "without", "free", "lacking", "devoid", "void", "un", "no", "never", "none"}
NEG_DEF = re.compile(r"\b(?:not|without|no|free (?:of|from)|lacking|devoid of|void of|destitute of|absence of|"
                     r"un[a-z]{3,}|[a-z]{3,}less)\b")
AGENT = re.compile(r"^(?:one|someone|somebody|a person|the person|he|she|the one|any one|anyone|a man|those)"
                   r"\s+(?:who|that|which)\s+(.*)$")

# British spellings the definitions also use; both sides of every comparison are normalized.
_OUR = ("labour", "colour", "honour", "favour", "behaviour", "harbour", "neighbour", "rumour", "vapour",
        "valour", "vigour", "rigour", "splendour", "endeavour", "ardour", "fervour", "clamour", "humour",
        "odour", "savour", "parlour", "armour", "candour", "saviour", "flavour", "demeanour", "succour")
_SPELL = {"offence": "offense", "defence": "defense", "pretence": "pretense", "licence": "license",
          "skilful": "skillful", "wilful": "willful", "fulfil": "fulfill", "instil": "instill",
          "grey": "gray", "plough": "plow", "sceptic": "skeptic"}


def us_spelling(w: str) -> str:
    if w in _SPELL:
        return _SPELL[w]
    for b in _OUR:
        if w.startswith(b):
            return b[:-2] + "r" + w[len(b):]
    return w


# ---------------------------------------------------------------- Porter stemmer (the algorithm FTS5's
# `porter` tokenizer implements, so stems here index its vocabulary for document frequencies)
def _cons(w: str, i: int) -> bool:
    c = w[i]
    if c in "aeiou":
        return False
    if c == "y":
        return i == 0 or not _cons(w, i - 1)
    return True


def _measure(s: str) -> int:
    n, i, L = 0, 0, len(s)
    while i < L and _cons(s, i):
        i += 1
    while i < L:
        while i < L and not _cons(s, i):
            i += 1
        if i >= L:
            break
        while i < L and _cons(s, i):
            i += 1
        n += 1
    return n


def _has_vowel(s: str) -> bool:
    return any(not _cons(s, i) for i in range(len(s)))


def _doublec(s: str) -> bool:
    return len(s) >= 2 and s[-1] == s[-2] and _cons(s, len(s) - 1)


def _cvc(s: str) -> bool:
    return (len(s) >= 3 and _cons(s, len(s) - 3) and not _cons(s, len(s) - 2) and _cons(s, len(s) - 1)
            and s[-1] not in "wxy")


_STEP2 = sorted({"ational": "ate", "tional": "tion", "enci": "ence", "anci": "ance", "izer": "ize", "bli": "ble",
                 "alli": "al", "entli": "ent", "eli": "e", "ousli": "ous", "ization": "ize", "ation": "ate",
                 "ator": "ate", "alism": "al", "iveness": "ive", "fulness": "ful", "ousness": "ous",
                 "aliti": "al", "iviti": "ive", "biliti": "ble", "logi": "log"}.items(), key=lambda kv: -len(kv[0]))
_STEP3 = sorted({"icate": "ic", "ative": "", "alize": "al", "iciti": "ic", "ical": "ic", "ful": "",
                 "ness": ""}.items(), key=lambda kv: -len(kv[0]))
_STEP4 = sorted(["al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement", "ment", "ent", "ion", "ou",
                 "ism", "ate", "iti", "ous", "ive", "ize"], key=len, reverse=True)


def _rule(w: str, rules, min_m: int) -> str:
    for suf, rep in rules:
        if w.endswith(suf):
            stem = w[: -len(suf)]
            return stem + rep if _measure(stem) > min_m else w
    return w


def porter(w: str) -> str:
    if len(w) <= 2:
        return w
    if w.endswith("sses"):
        w = w[:-2]
    elif w.endswith("ies"):
        w = w[:-2]
    elif w.endswith("s") and not w.endswith("ss"):
        w = w[:-1]
    if w.endswith("eed"):
        if _measure(w[:-3]) > 0:
            w = w[:-1]
    else:
        for suf in ("ed", "ing"):
            if w.endswith(suf) and _has_vowel(w[: -len(suf)]):
                w = w[: -len(suf)]
                if w.endswith(("at", "bl", "iz")):
                    w += "e"
                elif _doublec(w) and w[-1] not in "lsz":
                    w = w[:-1]
                elif _measure(w) == 1 and _cvc(w):
                    w += "e"
                break
    if w.endswith("y") and _has_vowel(w[:-1]):
        w = w[:-1] + "i"
    w = _rule(w, _STEP2, 0)
    w = _rule(w, _STEP3, 0)
    for suf in _STEP4:
        if w.endswith(suf):
            stem = w[: -len(suf)]
            if _measure(stem) > 1 and (suf != "ion" or stem.endswith(("s", "t"))):
                w = stem
            break
    if w.endswith("e"):
        stem = w[:-1]
        if _measure(stem) > 1 or (_measure(stem) == 1 and not _cvc(stem)):
            w = stem
    if _measure(w) > 1 and _doublec(w) and w.endswith("l"):
        w = w[:-1]
    return w


def words(text: str) -> list[str]:
    return [us_spelling(w) for w in re.findall(r"[a-z]+", text.lower())]


@functools.lru_cache(maxsize=200_000)
def _stem(w: str) -> str | None:
    """Stem of one raw lowercase word, None for a stopword."""
    w = us_spelling(w)
    return None if w in STOP else porter(w)


def stems(text: str) -> list[str]:
    return [s for w in re.findall(r"[a-z]+", text.lower()) if (s := _stem(w))]


# ---------------------------------------------------------------- the index connection (one per thread)
_local = threading.local()


def _con() -> sqlite3.Connection:
    con = getattr(_local, "con", None)
    if con is None:
        if not DB.exists():
            raise SystemExit(f"English index {DB} is missing; run prakriya's `lookup.py english-build`")
        con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        present = {s for (s,) in con.execute("select source from meta")}
        missing = [s for s in lookup.EXPECTED_SOURCES if s not in present]
        if missing:
            raise SystemExit(f"English index lacks sources {missing}; rerun prakriya's `lookup.py english-build`")
        con.execute("create virtual table temp.vocab using fts5vocab(main, 'defs_fts', 'row')")
        _local.con, _local.idf = con, {}
        _local.n_docs = con.execute("select count(*) from defs").fetchone()[0]
    return con


def idf(stem: str) -> float:
    con = _con()
    cache = _local.idf
    if stem not in cache:
        r = con.execute("select doc from temp.vocab where term=?", (stem,)).fetchone()
        cache[stem] = math.log(_local.n_docs / (1 + (r[0] if r else 0)))
    return cache[stem]


# ---------------------------------------------------------------- the sense, read as clauses
NEG_LEAD = r"^(?:not|without|free (?:of|from)|lacking|devoid of|void of|never|no)\s+"


@dataclass
class Clause:
    text: str
    stems: list[str]            # one key stem per content word, query order, unique
    weights: dict[str, float]   # key stem -> idf
    match: dict[str, tuple]     # definition stem -> (key stem, credit): the word itself or its lemma 1.0
                                # (freed ~ free), a synonym of it 0.6 (lifts ~ raise)
    frame: str | None           # 'agent' | 'verb' | 'neg' | 'participle' | 'adv' | 'noun' | None
    weight: float = 1.0         # image and simile clauses count less; the whole-sense clause 0.9
    content: list[str] = field(default_factory=list)  # content words (US spelling)
    heads: list[str] = field(default_factory=list)    # the words the clause is built on
    negated: list[str] = field(default_factory=list)  # the word under not / without / free of
    whole: bool = False         # the whole sense read as one clause
    expand: dict[str, list] = field(default_factory=dict)   # content word -> its synonyms (search)


def _frame(text: str) -> tuple[str | None, str]:
    """(frame, body): the clause's construction and the words that carry its meaning."""
    t = " ".join(text.strip().lower().split())
    m = AGENT.match(t)
    if m:
        return "agent", m.group(1)
    if t.startswith("to "):
        return "verb", t[3:]
    if re.match(NEG_LEAD, t):
        return "neg", t
    ws = [w for w in re.findall(r"[a-z]+", t) if w not in STOP]
    if len(ws) == 1 and ws[0].endswith("ly"):
        return "adv", t
    if len(ws) == 1 and re.search(r"(?:ed|en)$", ws[0]):
        return "participle", t
    if re.match(r"^(?:the|a|an)\s", t):
        return "noun", t
    return None, t


def _lemma(con, w: str) -> str:
    """The base form the sources record for an inflected word (lifts → lift, carries → carry)."""
    if con.execute("select 1 from defs where hw=? and source in ('oewn2025','webster1913') limit 1", (w,)).fetchone():
        if not re.search(r"(?:s|ed|ing)$", w):
            return w
    r = con.execute("select lower(lemma) from inflections where form=? and source='wiktionary' "
                    "and tags not like '%alt-of%' limit 1", (w,)).fetchone()
    return r[0] if r and _ok_word(r[0]) else w


def _heads(con, frame: str | None, body: str) -> list[str]:
    """The words a clause is built on, as headwords (a form no source has as a headword, like
    'highest', gives way to its lemma)."""
    return [w if con.execute("select 1 from defs where hw=? limit 1", (w,)).fetchone() else _lemma(con, w)
            for w in _head_words(con, frame, body)]


def _head_words(con, frame: str | None, body: str) -> list[str]:
    ws = [w for w in words(body)]
    content = [w for w in ws if w not in STOP and w not in NEG_WORDS]
    if len(content) <= 2 and frame not in ("verb", "agent"):   # 'homeless', 'patient under injury'
        return content
    if frame in ("verb", "agent"):   # the verbs of 'to sit near and attend on', 'one who lifts up and carries out'
        out = [ws[0]] + [ws[i + 1] for i, w in enumerate(ws[:-1]) if w in ("and", "or")]
        return [_lemma(con, w) if frame == "agent" else w for w in out if w not in STOP]
    return []


def parse(sense: str, image: str | None = None) -> list[Clause]:
    con = _con()
    out = []
    pieces = [(p, 1.0) for p in re.split(r"[,;:()]|\s+—\s+|\s+-\s+", sense)]
    if image:
        pieces += [(p, 0.6) for p in re.split(r"[,;:()]", image)]
    split = []
    for raw, w in pieces:      # coordinated verbs: 'one who lifts up and carries out' -> each verb too
        raw = " ".join(raw.split())
        m = re.match(r"^(.+?)\s+((?:like|as if|as though)\s.+)$", raw, re.I)
        if m:                  # 'standing firm like an anvil': the simile is an image clause
            raw = m.group(1)
            split.append((m.group(2), min(w, 0.6)))
        split.append((raw, w))
        f, body = _frame(raw)
        if f in ("agent", "verb") and re.search(r"\s(?:and|or)\s", body):
            lead = raw[: len(raw) - len(body)]
            split += [(lead + part, w * 0.9) for part in re.split(r"\s+(?:and|or)\s+", body) if part.strip()]
    for raw, w in split:
        if not raw:
            continue
        if re.match(r"^(?:like|as)\s", raw.lower()):     # a simile inside the sense is an image
            w = min(w, 0.6)
        frame, body = _frame(raw)
        content = [x for x in words(body) if x not in STOP and x not in NEG_WORDS and len(x) > 1]
        if not content:
            continue
        keys = list(dict.fromkeys(porter(x) for x in content))
        match: dict[str, tuple] = {}
        expand: dict[str, list] = {}
        for x in content:
            k = porter(x)
            for a in {k, porter(_lemma(con, x))}:
                match[a] = (k, 1.0)
        if frame in ("verb", "agent") and len(content) <= 3:   # a short verb clause, in its verbs' synonyms
            for x in content:
                syn = _synonyms(con, _lemma(con, x), "v")
                expand[x] = syn
                for y in syn:
                    match.setdefault(porter(y), (porter(x), 0.6))
        neg = []
        if frame == "neg":
            neg = [x for x in words(re.sub(NEG_LEAD, "", body.lower())) if x not in STOP][:1]
        out.append(Clause(raw, keys, {s: idf(s) for s in keys}, match, frame, w, content,
                          [] if frame == "neg" else _heads(con, frame, body), neg, expand=expand))
    parts = [c for c in out if c.weight == 1.0]
    if len(parts) > 1:   # the whole sense as one clause too, for definitions that cover several parts
        keys = list(dict.fromkeys(k for c in parts for k in c.stems))
        match = {}
        for c in parts:
            for a, (k, cr) in c.match.items():
                if cr > match.get(a, ("", 0))[1]:
                    match[a] = (k, cr)
        frame = "neg" if all(c.frame == "neg" for c in parts) else None
        out.append(Clause(sense, keys, {s: idf(s) for s in keys}, match, frame, 0.9,
                          [x for c in parts for x in c.content], whole=True))
    return out


def _synonyms(con, w: str, pos: str | None, n: int = 5) -> list[str]:
    """Single-word synonyms from the first senses of a word: up to `n` from OEWN, `n` from Wiktionary."""
    out: list[str] = []
    for src in ("oewn2025", "wiktionary"):
        mine: list[str] = []
        rows = [r for r in con.execute("select pos, synonyms from defs where hw=? and source=? and synonyms!='' "
                                       "order by id limit 12", (w, src)) if pos is None or _npos(r[0]) == pos][:3]
        for _p, syn in rows:
            mine += [y.strip().lower() for y in syn.split(",")
                     if re.fullmatch(r"[a-z]{3,}", y.strip().lower()) and y.strip().lower() not in STOP]
        out += [y for y in dict.fromkeys(mine) if y != w and y not in out][:n]
    return out


FRAME_POS = {"agent": {"n"}, "noun": {"n"}, "verb": {"v"}, "neg": {"adj"}, "participle": {"adj", "v"},
             "adv": {"adv"}}


def sense_pos(clauses: list[Clause], pos: str | None) -> set[str] | None:
    """The parts of speech that can render the sense: the caller's, else the first framed clause's."""
    if pos:
        return {_npos(pos)}
    return next((FRAME_POS[c.frame] for c in clauses if c.frame in FRAME_POS), None)


def _npos(p: str) -> str:
    p = (p or "").lower().strip()
    if p.startswith("v"):
        return "v"
    if p.startswith(("a.", "adj")) or p in ("a", "s"):
        return "adj"
    if p.startswith(("adv", "r")):
        return "adv"
    if p.startswith("n"):
        return "n"
    return p


# ---------------------------------------------------------------- scoring a definition against a clause
_CITE = re.compile(r"\s+\(e\.g\.|\s\[under:|\s--\s|;\s*\"|\.\s+(?=[A-Z\"“'])")
_NOT_NEG = {"under", "until", "unless", "unto", "unit", "unity", "union", "unique", "universal", "universe",
            "unite", "united", "bless"}


def short_def(d: str, n: int = 90) -> str:
    d = _CITE.split(d or "", 1)[0]
    d = re.sub(r"\[[^\]]{0,40}\]", "", d)
    d = " ".join(d.split()).strip(" .;,")
    if len(d) > n:
        d = d[:n].rsplit(" ", 1)[0].rstrip(" ,;") + "…"
    return d


_NEG_STEMS = {"not", "without", "free", "no", "lack", "devoid", "void", "destitut"}


def _negative(text: str) -> bool:
    return any(m.group(0) not in _NOT_NEG for m in NEG_DEF.finditer(text))


@functools.lru_cache(maxsize=50_000)
def _segments(defn: str) -> tuple:
    """The definition's first sentence and each of its ;-segments: (stems, has a negation)."""
    text = short_def(defn, 220).lower()
    segs = [text] + ([x for x in text.split(";") if x.strip()] if ";" in text else [])
    return tuple((tuple(stems(x)), _negative(x)) for x in segs)


def def_score(defn: str, c: Clause) -> float:
    """1.0 when the clause and the definition (or one ;-segment of it) say the same thing: idf-
    weighted coverage of the clause (raised to 1.5, so half a clause is worth about a third),
    damped by how much of the definition the clause leaves out. Under a negated clause a
    definition without a negation counts 0.3 (it names the opposite)."""
    total = sum(c.weights.values()) or 1.0
    best = 0.0
    for i, (ds, negative) in enumerate(_segments(defn)):
        if not ds:
            continue
        credit: dict[str, float] = {}
        for x in ds:
            m = c.match.get(x)
            if m and m[1] > credit.get(m[0], 0):
                credit[m[0]] = m[1]
        if not credit:
            continue
        cov = sum(c.weights[k] * v for k, v in credit.items()) / total
        extra = len([x for x in ds if x not in c.match and x not in _NEG_STEMS])
        prec = len(credit) / (len(credit) + extra)
        sc = cov ** 1.5 * (0.6 + 0.4 * prec)
        if c.frame == "neg" and not negative:
            sc *= 0.3
        if i:          # one ;-segment matched alone: a little less than the whole definition
            sc *= 0.95
        best = max(best, sc)
    return best


def _ok_word(w: str) -> bool:
    return bool(re.fullmatch(r"[a-z][a-z'\- ]*[a-z]", w)) and len(w.split()) <= 3


# ---------------------------------------------------------------- candidate evidence
@dataclass
class Cand:
    word: str
    hit: float = 0.0       # best reverse-dictionary score found by search
    links: dict = field(default_factory=dict)   # thesaurus support: link key -> strongest link
    own: float = 0.0       # the sense itself is built on this word
    base: str | None = None   # derived form: the verb or word it is derived from
    kind: str | None = None   # 'agent' | 'participle' | 'adj' | 'neg'
    via: list[str] = field(default_factory=list)

    def note(self, why: str) -> None:
        if len(self.via) < 3 and why not in self.via:
            self.via.append(why)

    @property
    def syn(self) -> float:
        """Links from different seeds combine as independent evidence; several sources linking
        the same seed count once (its strongest link), so one seed's synonyms stay as weak as it."""
        p = 1.0
        for v in self.links.values():
            p *= 1 - v
        return 1 - p

    def prelim(self) -> float:
        return self.hit + 0.6 * self.syn + 0.6 * self.own


class Pool(dict):
    def get_(self, w: str) -> Cand | None:
        w = w.strip().lower()
        if not _ok_word(w):
            return None
        if w not in self:
            self[w] = Cand(w)
        return self[w]

    def add_hit(self, w: str, sc: float, why: str) -> None:
        c = self.get_(w)
        if c and sc > 0:
            c.hit = max(c.hit, sc)
            c.note(why)

    def add_syn(self, w: str, sc: float, why: str, key: str, create: bool = True) -> None:
        w = w.strip().lower()
        if not create and w not in self:
            return
        c = self.get_(w)
        if c and sc > 0 and key != w:
            c.links[key] = max(c.links.get(key, 0.0), min(sc, 0.9))
            c.note(why)


def _fts_terms(c: Clause) -> list[str]:
    out = []
    for w in c.content:
        alts = {w}
        for b in _OUR:          # also search the British spelling a source may use
            br = b[:-2] + "r"
            if w.startswith(br):
                alts.add(b + w[len(br):])
        alts |= {k for k, v in _SPELL.items() if v == w}
        alts = sorted(a for a in alts if re.fullmatch(r"[a-z]+", a))
        if alts:
            out.append("(" + " OR ".join(f'"{a}"' for a in alts) + ")")
    return list(dict.fromkeys(out))


def _search(con, c: Clause, pool: Pool, roget_groups: dict) -> None:
    """Reverse dictionary for one clause: definitions with all its terms, then with any."""
    terms = _fts_terms(c)
    if not terms:
        return
    queries = [("definition:(" + " AND ".join(terms) + ")", 150)] if len(terms) > 1 else []
    queries.append(("definition:(" + " OR ".join(terms) + ")", 250))
    if any(c.expand.values()):   # the same clause in its words' synonyms: 'lifts up' ~ 'raise aloft'
        ex = ["(" + " OR ".join(f'"{y}"' for y in [x] + c.expand.get(x, [])) + ")" for x in c.content]
        queries.append(("definition:(" + " AND ".join(ex) + ")", 150))
    seen = set()
    for q, lim in queries:
        rows = con.execute(
            "select d.id, d.headword, d.pos, d.source, d.definition, d.synonyms, d.locus from defs_fts "
            "join defs d on d.id = defs_fts.rowid where defs_fts match ? order by bm25(defs_fts) limit ?",
            (q, lim)).fetchall()
        for rid, hw, pos, src, defn, syn, locus in rows:
            if rid in seen or (pos or "").lower() in JUNK_POS:
                continue
            seen.add(rid)
            if src == "roget1911":
                sc = def_score(defn.split("synonyms:", 1)[-1], c) * c.weight
                if sc > roget_groups.get(locus, (0, ""))[0]:
                    roget_groups[locus] = (sc, defn)
                continue
            if src == "moby":
                ds = set(stems(defn[:1500]))
                cov = sum(c.weights[s] for s in c.stems if s in ds) / (sum(c.weights.values()) or 1)
                pool.add_syn(hw, 0.45 * cov * c.weight, f"Moby list of '{hw.lower()}'", "moby-self")
                continue
            sc = def_score(defn, c) * c.weight
            if sc < 0.15:
                continue
            pool.add_hit(hw, sc, f"{src}: \"{short_def(defn, 60)}\"")
            if syn and sc >= 0.35:
                for s in syn.split(",")[:12]:
                    pool.add_syn(s, 0.6 * sc, f"synonym of '{hw.lower()}' ({src})", hw.lower())


def _rows_for(con, words_: list[str]) -> dict[str, list[tuple]]:
    """Every row of each headword: (pos, source, tags, definition, synonyms); Moby's long
    synonym lists are cut and its definition column (the same list) dropped."""
    out: dict[str, list[tuple]] = {}
    words_ = list(dict.fromkeys(words_))
    for k in range(0, len(words_), 400):
        chunk = words_[k:k + 400]
        q = ",".join("?" * len(chunk))
        for hw, pos, src, tags, defn, syn in con.execute(
                f"select hw, pos, source, tags, case when source='moby' then '' else definition end, "
                f"case when source='moby' then substr(synonyms, 1, 6000) else synonyms end "
                f"from defs where hw in ({q}) order by id", chunk):
            out.setdefault(hw, []).append((pos or "", src, tags or "", defn or "", syn or ""))
    return out


def _defined_as(con, pool: Pool, hits: list[Cand]) -> None:
    """Dictionary synonymy of the best hits: words whose definition lists the hit as a gloss
    ('Forbearing: … patient; long-suffering', 'Immovable: … Steadfast; fixed')."""
    for h in hits:
        q = 'definition:"' + h.word.replace('"', "") + '"'
        for hw, defn in con.execute(
                "select d.headword, d.definition from defs_fts join defs d on d.id = defs_fts.rowid "
                "where defs_fts match ? and d.kind = 'sense' order by bm25(defs_fts) limit 120", (q,)):
            segs = {x.strip(" .").lower() for x in re.split(r"[;,]", short_def(defn, 160))}
            if h.word in segs:
                pool.add_syn(hw, 0.6 * h.hit, f"defined as '{h.word}'", "def:" + h.word)


def _gather(con, clauses: list[Clause], sense: str) -> Pool:
    """Steps 1–3: reverse dictionary, matching Roget groups, the sense's own words, thesaurus expansion."""
    pool = Pool()
    roget_groups: dict[str, tuple[float, str]] = {}
    for c in clauses:
        _search(con, c, pool, roget_groups)
    for sc, defn in sorted(roget_groups.values(), key=lambda x: -x[0])[:12]:
        if sc < 0.2:
            continue
        head = defn.split("]", 1)[0].strip("[")
        for m in defn.split("synonyms:", 1)[-1].split(","):
            pool.add_syn(m, 0.55 * sc, f"{head} group", head)
    # seeds: the words and phrases the sense is built on, then the best hits
    seeds: dict[str, float] = {}
    for c in clauses:
        if c.weight < 0.9 or c.whole:
            continue
        for h in c.heads:
            seeds[h] = max(seeds.get(h, 0), 0.9 / len(c.heads))
            d = pool.get_(h)
            if d:
                d.own = max(d.own, 0.9 / len(c.heads))
                d.note("a word of the sense")
        ws = words(_frame(c.text)[1])
        for a, b in zip(ws, ws[1:]):        # phrases of the sense: 'draw back', 'set loose', 'attend on'
            if (a not in STOP or b not in STOP) and a not in NEG_WORDS:
                seeds.setdefault(f"{a} {b}", 0.45)
    for t in sorted(pool.values(), key=lambda x: -x.prelim())[:10]:
        seeds[t.word] = max(seeds.get(t.word, 0), min(1.0, t.prelim()))
    _defined_as(con, pool, [t for t in sorted(pool.values(), key=lambda x: -x.hit)[:5] if t.hit >= 0.5])
    seed_rows = _rows_for(con, list(seeds))
    for s, sw in seeds.items():
        rows = seed_rows.get(s, [])
        if " " in s and rows:                # an attested phrase of the sense is itself a candidate
            d = pool.get_(s)
            if d:
                d.own = max(d.own, sw)
                d.note("a phrase of the sense")
        for _p, src, _t, _d, syn in rows:
            if not syn:
                continue
            if src == "moby":                # Moby confirms; its lists are too long to add from
                for m in syn.split(","):
                    pool.add_syn(m, 0.25 * sw, f"Moby: '{s}'", s, create=False)
                continue
            w = {"oewn2025": 0.7, "wordnet3.1": 0.6, "wiktionary": 0.55, "roget1911": 0.45}.get(src, 0.4)
            for m in syn.split(",")[:30]:
                pool.add_syn(m, w * sw, f"synonym of '{s}' ({src})", s)
    return pool


# ---------------------------------------------------------------- derived forms (step 4)
def _verb_forms(v: str, kind: str) -> list[str]:
    if " " in v or len(v) < 3:
        return []
    dbl = v + v[-1] if re.search(r"[^aeiou][aeiou][bdgklmnprt]$", v) else None
    if kind == "agent":
        out = [v + "r"] if v.endswith("e") else [v + "er"] + ([dbl + "er"] if dbl else [])
        return out + ([v[:-1] + "ier"] if v.endswith("y") else [])
    if kind == "participle":
        out = [v + "d"] if v.endswith("e") else [v + "ed"] + ([dbl + "ed"] if dbl else [])
        return out + ([v[:-1] + "ied"] if v.endswith("y") else []) + [v + "n", v + "en"]
    if kind == "adj":   # present participles used as adjectives (forbearing, unchanging)
        if v.endswith("e") and not v.endswith("ee"):
            return [v[:-1] + "ing"]
        return [v + "ing"] + ([dbl + "ing"] if dbl else [])
    return []


def _neg_forms(w: str, lemma: str) -> list[str]:
    out = ["un" + w, "in" + w, "im" + w, "non" + w, w + "less", lemma + "less", "un" + lemma]
    return list(dict.fromkeys(out))


def _derive(con, clauses: list[Clause], want: set[str] | None, pool: Pool, verbs: list[str]) -> list[str]:
    """Attested agent nouns / participles / -ing adjectives of the candidate verbs the frames ask
    for, and un-/-less forms of a negated word. A form counts only if a source has it as a headword
    or records it as an inflection of that verb."""
    frames = {c.frame for c in clauses}
    # -ing adjectives only for an adjectival sense that is neither negated (the verbs found there name
    # what is negated) nor a past participle; and only lexicalized ones (with adjective senses) count
    kinds = (["agent"] if "agent" in frames else []) + (["participle"] if "participle" in frames else []) \
        + (["adj"] if (want is None or want == {"adj"}) and not frames & {"neg", "participle"} else [])
    gen: dict[str, tuple[str, str]] = {}
    for v in verbs:
        for kind in kinds:
            for f in _verb_forms(v, kind):
                if f != v and f not in gen:
                    gen[f] = (v, kind)
    for c in clauses:
        for w in c.negated:
            for f in _neg_forms(w, _lemma(con, w)):
                gen.setdefault(f, (w, "neg"))
    if not gen:
        return []
    forms = list(gen)
    attested = set()
    for k in range(0, len(forms), 400):
        chunk = forms[k:k + 400]
        q = ",".join("?" * len(chunk))
        attested |= {hw for (hw,) in con.execute(
            f"select distinct hw from defs where hw in ({q}) and source in "
            f"('webster1913','gcide','wiktionary','oewn2025')", chunk)}
        attested |= {f for f, lem in con.execute(
            f"select form, lower(lemma) from inflections where form in ({q})", chunk) if gen[f][0] == lem}
    out = []
    for f in forms:
        if f in attested:
            base, kind = gen[f]
            d = pool.get_(f)
            if d and not d.base:
                d.base, d.kind = base, kind
                d.note(f"{kind} form of '{base}'" if kind != "neg" else f"negation of '{base}'")
                out.append(f)
    return out


# ---------------------------------------------------------------- scoring each candidate (step 5)
@dataclass
class Scored:
    fit: float                   # core plus part-of-speech agreement with the sense
    core: float                  # meaning evidence alone (what a derived form inherits)
    cand: Cand
    pos: str
    rows: list[tuple]            # sense rows (pos, source, tags, definition, synonyms)
    best: list[tuple]            # (score, row) of the best row per clause, best first


AGENTIVE = re.compile(r"\b(?:one|person|someone|he|those|who|whoever)\b", re.I)
FORM_OF = re.compile(r"^\s*(?:(?:strong|obs\.|archaic)\s+)?(?:imp\.|p\.\s*p\.|pres\.\s*p\.|pl\.|3d pers|"
                     r"superl\.|compar\.|plural of|past (?:tense|participle) of|present participle of)", re.I)


@functools.lru_cache(maxsize=50_000)
def _glosses(defn: str) -> frozenset:
    """The one- or two-word glosses a definition lists, with suffix-rule lemmas of single words:
    'One who upbears or upholds' -> {upbears, upbear, upholds, uphold}."""
    out = set()
    for seg in re.split(r"[;,]", short_def(defn, 160).lower()):
        seg = re.sub(r"^\s*(?:to|one who|one that|that which|who|a|an|the|also|hence|so)\s+", "", seg.strip(" ."))
        for part in re.split(r"\s+or\s+", seg):
            part = part.strip(" .")
            if 0 < len(part.split()) <= 2:
                out.add(part)
                if " " not in part:
                    out.update(lookup.lemma_candidates(part))
    return frozenset(out)


def _score(c: Cand, rows: list[tuple], clauses: list[Clause], want: set[str] | None,
           strong: dict[str, float]) -> Scored | None:
    particles = {w for cl in clauses for w in words(cl.text) if w in PARTICLES}
    srows = [r for r in rows if r[1] in SENSE_SOURCES and r[3] and r[0].lower() not in JUNK_POS
             and not FORM_OF.match(r[3])]
    if not srows:
        return None
    per, best = [], []
    for cl in clauses:
        m, mr = 0.0, None
        for r in srows:
            s = def_score(r[3], cl)
            if s > m:
                m, mr = s, r
        m *= cl.weight
        if c.word in cl.content or c.word in cl.heads:   # the sense names the word: it glosses itself
            self_ = def_score(c.word, cl) * cl.weight * 0.8
            m = max(m, self_)
        per.append(m)
        if mr:
            best.append((m, mr))
    dfit = 0.6 * max(per) + 0.4 * (sum(per) / len(per))
    best.sort(key=lambda x: -x[0])
    # definitional substitution: a definition that glosses the word by a strong hit means what that
    # hit means ('Forbearing: … patient; long-suffering', 'Upbearer: One who upbears or upholds')
    sub, via = 0.0, None
    for r in srows:
        for g in _glosses(r[3]):
            if g != c.word and g in strong and strong[g] > sub:
                sub, via = strong[g], g
    # thesaurus support, without the links that restate the substituted gloss (same evidence)
    p = 1.0
    for k, v in c.links.items():
        if not via or k not in (via, "def:" + via):
            p *= 1 - v
    syn = 1 - p
    if via:   # a substitution alone (one sense of 'daft' glossed 'meek') counts about half as much
        dfit = max(dfit, sub * (0.6 if dfit >= 0.15 or syn >= 0.15 else 0.35))
    nsrc = len({r[1] for r in srows})
    prior = math.log(1 + nsrc) / math.log(6)
    top = best[0][0] if best else 0
    match_pos = [_npos(r[0]) for s, r in best if s >= 0.6 * top] or [_npos(r[0]) for r in srows]
    if c.own:   # the sense itself uses the word, in whatever role its frame gives it
        match_pos += [_npos(r[0]) for r in srows]
    if c.kind == "agent":
        match_pos = ["n"]
    elif c.kind in ("participle", "adj", "neg"):
        match_pos = ["adj"]
    ok = [p for p in match_pos if want is None or p in want]
    meaning = 1 - (1 - dfit) * (1 - 0.5 * syn)   # definitions first; thesaurus support adds to them
    core = 0.75 * meaning + 0.12 * c.own + 0.08 * prior - (0.05 if " " in c.word else 0)
    if any(c.word.startswith(p) and len(c.word) > len(p) + 2 for p in particles):
        core += 0.05      # the sense's particle as a prefix: 'lifts up' -> uplift, upbear
    return Scored(core + (0.04 if ok else -0.1), core, c, (ok or match_pos or [""])[0], srows, best)


def english_table(sense: str, image: str | None = None, pos: str | None = None, limit: int = 25) -> list[dict]:
    """≤ `limit` English candidates for a sense (and its image), ranked by `fit` (0–1).
    Each row: word, pos (n|v|adj|adv), defs (≤2 short, different sources, 'source: text'),
    tags (register labels on the senses that matched), modern (first OEWN, else Wiktionary,
    sense), fit, via (how the word was found)."""
    con = _con()
    clauses = parse(sense, image)
    if not clauses:
        return []
    want = sense_pos(clauses, pos)
    pool = _gather(con, clauses, sense)
    ordered = sorted(pool.values(), key=lambda x: -x.prelim())
    cands = ordered[:260]
    # step 4 needs only attestation, so it runs over the wider pool; bases of attested forms are scored
    derived = _derive(con, clauses, want, pool, [c.word for c in ordered[:600] if " " not in c.word])
    need = list(dict.fromkeys([c.word for c in cands] + derived + [pool[f].base for f in derived if pool[f].base in pool]))
    rows = _rows_for(con, need)
    strong = {c.word: c.hit for c in sorted(cands, key=lambda x: -x.hit)[:5] if c.hit >= 0.5}
    scored = {w: s for w in need if (s := _score(pool[w], rows.get(w, []), clauses, want, strong))}
    for f in derived:
        c, s = pool[f], scored.get(f)
        if c.kind == "neg":       # the regular negation of the sense's own negated word
            core, pos = (s.core if s else 0.2) + 0.12, "adj"
        elif c.kind == "adj" and not (s and any(_npos(r[0]) == "adj" for r in s.rows)):
            continue
        else:                     # the agent noun / participle of a candidate verb: as good as the verb
            b = scored.get(c.base)
            if not b or not any(_npos(r[0]) == "v" for r in b.rows):
                continue
            # the form the frame asks for ranks just above its verb; an agent noun none of whose
            # definitions names the verb (runer: 'a bard') is another word, so it inherits less
            names_base = not s or any(porter(c.base) in stems(r[3]) and (c.kind != "agent" or AGENTIVE.search(r[3]))
                                      for r in s.rows)
            core = b.core * (1.0 if names_base else 0.8) + (0.02 if c.kind in ("agent", "participle") else -0.03)
            pos = "n" if c.kind == "agent" else "adj"
        fit = core + (0.04 if want is None or pos in want else -0.1)
        if s is None:
            scored[f] = Scored(fit, core, c, pos, [], [])
        elif fit > s.fit:
            s.fit, s.core, s.pos = fit, core, pos
    ranked = _collapse(con, sorted(scored.values(), key=lambda s: -s.fit))[:limit]
    return [_row(s, scored) for s in ranked]


def _collapse(con, ranked: list[Scored]) -> list[Scored]:
    """One row per word in one role: an inflection or spelling variant of a ranked word, in the same
    part of speech (drilling ~ drill, practise ~ practice), gives way to the better-ranked of the two.
    Forms a frame asked for (the participle, the agent noun, the negation) stand on their own."""
    names = [s.cand.word for s in ranked]
    present = set(names)
    lemma: dict[str, str] = {}
    for k in range(0, len(names), 400):
        chunk = names[k:k + 400]
        for f, lem in con.execute(f"select form, lower(lemma) from inflections where form in "
                                  f"({','.join('?' * len(chunk))})", chunk):
            if lem in present and lem != f:
                lemma.setdefault(f, lem)
    out, seen = [], set()
    for s in ranked:
        w = s.cand.word
        key = (w if s.cand.kind in ("agent", "participle", "neg") else lemma.get(w, w), s.pos)
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def _row(s: Scored, scored: dict) -> dict:
    defs, used = [], set()
    c = s.cand
    pref = [r for _, r in s.best] + [r for r in s.rows if _npos(r[0]) == s.pos] + s.rows
    if c.base and c.kind in ("agent", "participle"):   # the sense the derivation is about first
        pref = [r for r in s.rows if porter(c.base) in stems(r[3])] + pref
    for r in pref:
        if r[1] in used or len(defs) >= 2:
            continue
        t = short_def(r[3])
        if t and all(t.lower() != d.split(": ", 1)[1].lower() for d in defs):
            defs.append(f"{r[1]}: {t}")
            used.add(r[1])
    if c.base and not defs:
        b = scored.get(c.base)
        bdef = short_def(b.best[0][1][3] if b and b.best else (b.rows[0][3] if b and b.rows else ""), 70)
        defs = [f"{c.kind} of '{c.base}'" + (f": {bdef}" if bdef else "")]
    top = s.best[0][0] if s.best else 0
    tags = sorted({t for sc, r in s.best if sc >= 0.6 * top for t in r[2].split(",") if t in REGISTER})
    # the first modern sense in the row's part of speech (labor, v: not 'a political party')
    modern = next((short_def(r[3]) for same in (True, False) for src in MODERN_SOURCES for r in s.rows
                   if r[1] == src and (not same or _npos(r[0]) == s.pos)), None)
    return {"word": c.word, "pos": s.pos or None, "defs": defs, "tags": tags, "modern": modern,
            "fit": round(max(0.0, min(1.0, s.fit)), 3), "via": c.via[:2]}


if __name__ == "__main__":
    import json
    import time
    t = time.time()
    out = english_table(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"{time.time() - t:.2f}s", file=sys.stderr)

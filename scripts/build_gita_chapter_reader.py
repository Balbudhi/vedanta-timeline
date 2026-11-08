#!/usr/bin/env python3
"""Fail-closed builder: producer shards + independent reviews → gita/chN/ reader.

    python3 scripts/build_gita_chapter_reader.py 12 [--check-only] [--allow-unreviewed] [--json-report PATH]
    python3 scripts/build_gita_chapter_reader.py 12 --register-only --root DIR
    python3 scripts/build_gita_chapter_reader.py --policy-hash
    python3 scripts/build_gita_chapter_reader.py --snapshot-policy

Inputs (internal/sanskrit_reviews/gita/chN/):
  packet.json                       the ChapterPacket (build_gita_chapter_packet.py)
  producer-AA-BB.json               producer shards (schema gita-producer-v2), covering 1..N once
  independent-review-AA-BB.json     one per shard, complete:true, producer_sha256 matching the shard
Outputs (only when every check passes):
  gita/chN/verses.js                window.CH<N>_VERSES — public cards and verse fields only
  gita/chN/index.html               standalone page (forwards into the app)
  internal/sanskrit_reviews/gita/chN/apparatus.json   evidence, fallbacks, wording, fork evidence
      (published under gita/chN/ only if the reader registration loads it; audit B13)
  internal/sanskrit_reviews/gita/chN/deviations.json  deviation defences (they quote secondaries)
  internal/sanskrit_reviews/gita/chN/owner-review-queue.json   built from occurrences (B14)
  registration in assets/app.js GITA_READINGS and data/articles/manifest.json (idempotent)

Contract: docs/GITA_CH12_PIPELINE_AUDIT.md §5.7 (checks B1–B18) and
docs/GITA_CARD_MEANING_SCHEMA.md (meaning, fork words/display, public-text rule).
Every violation is reported with its check id; nothing is written while any
error stands. The builder never repairs producer JSON.

The policy version is a content hash: sha256 of the canonical JSON of
data/glossary/term_policy.json without its `changelog` (history about the
content, not content). Producers record it as `policy_sha256` on the shard.
Both policy structures are read: v1 (`terms` → `senses` with `english`) and
v2 (`lemmas` → `senses` with `forms` per grammatical category, `reserved_english`,
`status`), audit §5.4.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRAKRIYA = ROOT.parent / "prakriya"

FUNCTION_WORDS = set("""a an the all any some no not none nor or and but if then so as at by for from in into of
off on onto out over to up upon with without within this that these those he she it they them his her its their
him who whom whose which what when where why how one ones each every both either neither more most less least
very too also even just only own same such than there here be is are was were been being am do does did done
have has had having will shall would should may might must can could let""".split())

PRODUCER_SCHEMA = "gita-producer-v2"
WORD_CLASSES = {"content", "particle", "pronoun", "name", "copula"}
EVIDENCE_KEYS = {"claim", "locus", "quote", "sutra", "kind"}
MEANING_CATS = ["formation", "lexical", "nirvacana", "commentator", "usage", "reception", "synthesis"]
MEANING_ATTRIBUTED = {"lexical", "nirvacana", "commentator", "reception"}
MEANING_MAX_LINES = 8
RECEPTION_QUOTE_MAX_WORDS = 8          # "at most a few words of quotation" (card meaning schema)
BLOCKING_FALLBACK_KINDS = {"root", "pratyaya", "compound"}   # plan §13.4.2
ENGLISH_STACK = ["webster1913", "gcide", "wiktionary", "oewn", "century", "roget", "moby"]   # plan §3.2
ENGLISH_SOURCE_RE = re.compile(r"webster|gcide|wordnet|oewn|wiktionary|kaikki|century|roget|moby", re.I)
DICTIONARY_SOURCES = re.compile(r"webster|gcide|wordnet|oewn|wiktionary|century|roget|moby|\bmw\b|ap90|apte|monier|skd|vcp|amara|cologne|kosha|define", re.I)

# Plan §13.3 fairness test set. Verse-level entries need a fork in the verse; word-level
# entries (latin-key prefix of the card iast) need a fork whose `words` names that card.
REQUIRED_FORK_VERSES = {12: {"12.3", "12.4", "12.5", "12.6", "12.10", "12.11", "12.12", "12.13", "12.16", "12.19", "12.20"},
                        2: {"2.12", "2.16", "2.39", "2.47", "2.48", "2.49", "2.50", "2.72"}}
FAIRNESS_WORDS = {12: [("12.3", "aksaram"), ("12.3", "avyaktam"), ("12.5", "avyaktasaktacetasam"), ("12.12", "jnan"),
                       ("12.12", "dhyan"), ("12.12", "karmaphalatyag"), ("12.20", "dharmyamrtam")],
                  2: [("2.16", "asat"), ("2.39", "sankhy"), ("2.47", "karman"), ("2.48", "samatv"), ("2.49", "buddhiyog"),
                      ("2.50", "kausal"), ("2.72", "brahmanirvan")]}
INTERROGATIVE_STEMS = {"kim", "ka", "kva", "katham", "kutas", "kutaḥ", "kadā", "kati", "kaccit", "kuha", "kiyat", "katara", "katama"}
INTERROGATIVE_FORMS = {"kim", "kaḥ", "ke", "kā", "kam", "kena", "kasya", "kasmāt", "kasmai", "kasmin", "keṣām", "kāni", "kau",
                       "kva", "katham", "kutaḥ", "kadā", "kati", "kaccit", "kuha"}
TRAILING_PARTICLES = {"on", "to", "upon", "in", "at", "of", "with", "from", "by", "for", "up", "down", "out", "off", "away", "into", "onto", "over"}
ING_EXCEPTIONS = {"thing", "nothing", "something", "everything", "anything", "king", "being", "spring", "string", "sing",
                  "bring", "wing", "ring", "evening", "morning"}
TRANSLATORS = ["Adidevananda", "Gambhirananda", "Gambirananda", "Sivananda", "Purohit", "Tapasyananda", "Chinmayananda",
               "Prabhupada", "Radhakrishnan", "Edgerton", "Zaehner", "Sargeant", "Telang", "Besant", "Arnold", "Mascaro",
               "Easwaran", "Sampatkumaran", "Warrier", "Ramsukhdas", "Swarupananda", "Aurobindo", "Anilbaran", "Prabhavananda",
               "Isherwood", "Feuerstein", "Minor", "van Buitenen", "Johnson", "Miller", "Mitchell", "Sri Aurobindo"]

# Public-text rule (card meaning schema; audit B9). Ordinary English words that are
# also pipeline words (lead, owner, gate, policy) are matched only in pipeline use.
PIPELINE_PATTERNS = [
    ("policy row/table", re.compile(r"\bpolicy (?:rows?|notes?|table|decisions?|detectors?)\b|\bper (?:the )?(?:term )?policy\b|\bterm[_ ]policy\b|\bunder (?:the )?policy\b", re.I)),
    ("lead", re.compile(r"\blead(?:'s)? (?:decision|ruling|note|choice|edit)s?\b|\(lead\b|\bthe lead (?:decided|chose|ruled|asked)\b", re.I)),
    ("owner", re.compile(r"\bowner(?:'s)? (?:gate|decision|review|queue|choice|aesthetic|decided|may|prefers)\b|\(owner\b|\bthe owner (?:decided|chose|asked|prefers)\b", re.I)),
    ("gate", re.compile(r"\bgate\s*(?:\d|O\d)|\b(?:aesthetic|meaning|review|owner'?s?) gate\b", re.I)),
    ("shard", re.compile(r"\bshards?\b", re.I)),
    ("producer/reviewer", re.compile(r"\bproducers?\b|\breviewers?\b", re.I)),
    ("fallback", re.compile(r"\bfallbacks?\b", re.I)),
    ("F-number", re.compile(r"\bF\d{1,2}\b")),
    ("internal § reference", re.compile(r"§\s*\d")),
    ("pilot", re.compile(r"\breview:\s*pilot\b|\bpilot rows?\b", re.I)),
    ("fork structure", re.compile(r"\bforks?\b|\bterms\[\]", re.I)),
    ("code term", re.compile(r"`[^`]+`|\b(?:glossaryKey|lemma_id|iast_forms|word_class|policy_sha256|rootGloss|form_note)\b")),
    ("policy wording", re.compile(r"\bpreserved (?:term|per)\b|\bkept in iast\b", re.I)),
    ("pipeline artefact", re.compile(r"\b(?:packet|dossier|joycean|wording records?|deviation defen[cs]es?|self-review)\b", re.I)),
]
SANSKRIT_ONLY_FIELDS = {"iast", "deva", "devanagari", "locus", "speaker", "meter", "stem", "i", "words"}


# Sense statuses production may use (lead, 2026-11-08): owner-decided; lexicon-reviewed (published
# provisional, the owner reads after publication); pilot. `proposed` is refused.
ADMITTED_STATUSES = ("owner-decided", "lexicon-reviewed", "pilot")


class BuildError(ValueError):
    pass


# ---------------------------------------------------------------- report
@dataclass
class Report:
    """Violations as (check id, message, scope); scope is the producer shard being
    checked, or "chapter" for chapter-level checks."""
    errors: list[tuple[str, str, str]] = field(default_factory=list)
    warnings: list[tuple[str, str, str]] = field(default_factory=list)
    scope: str = "chapter"

    def err(self, check: str, msg: str) -> None:
        self.errors.append((check, msg, self.scope))

    def warn(self, check: str, msg: str) -> None:
        self.warnings.append((check, msg, self.scope))

    def counts(self) -> dict[str, int]:
        return dict(sorted(Counter(c for c, _, _ in self.errors).items(), key=lambda kv: _check_order(kv[0])))

    def counts_by_scope(self) -> dict[str, dict[str, int]]:
        out: dict[str, Counter] = {}
        for c, _, sc in self.errors:
            out.setdefault(sc, Counter())[c] += 1
        return {sc: dict(sorted(cn.items(), key=lambda kv: _check_order(kv[0]))) for sc, cn in sorted(out.items())}

    def checks_failed(self) -> set[str]:
        return {c for c, _, _ in self.errors}


def _check_order(c: str) -> tuple:
    m = re.match(r"B(\d+)$", c)
    return (0, int(m.group(1)), "") if m else (1, 0, c)


# ---------------------------------------------------------------- text helpers
def latin_key(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "").lower()
    s = re.sub(r"[̀-ͯ]", "", s)
    return re.sub(r"[^a-z]", "", s)


def edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


SLOT_RE = re.compile(r"\{([\d,\s]+):([^{}]*)\}")


def slot_map(english: str) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    for m in SLOT_RE.finditer(english or ""):
        for i in m.group(1).split(","):
            i = i.strip()
            if i:
                out.setdefault(int(i), []).append(m.group(2))
    return out


QUOTED_RE = re.compile(r"“[^”]*”|‘[^’]*’|\"[^\"]*\"|(?<![A-Za-z])'[^']*'(?![A-Za-z])")


def strip_quotations(s: str) -> str:
    return QUOTED_RE.sub(" ", s or "")


def word_re(w: str) -> re.Pattern:
    return re.compile(rf"(?<![A-Za-z]){re.escape(w.lower())}(?![A-Za-z])")


def iter_strings(node: Any, path: str = ""):
    """Yield (path, string) for every string in a JSON value."""
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from iter_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from iter_strings(v, f"{path}[{i}]")


# ---------------------------------------------------------------- policy (v1 and v2)
PROSE_KEYS = {"changelog", "note", "notes", "detectors_note", "rule", "description"}


def _decisions_only(node):
    if isinstance(node, dict):
        return {k: _decisions_only(v) for k, v in node.items() if k not in PROSE_KEYS}
    if isinstance(node, list):
        return [_decisions_only(v) for v in node]
    return node


def policy_content_hash(data: dict) -> str:
    """sha256 of the canonical JSON of the policy's DECISIONS: prose (`changelog`, `note`,
    `rule`, …) is excluded, so explaining a row better does not invalidate the shards
    produced under it; changing a match, rendering, forbidden word, status or form does."""
    body = _decisions_only(data)
    canon = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


@dataclass
class Sense:
    policy: str
    iast: str | None
    iast_forms: list[str]
    english: list[str]                 # every admitted English form (v2: union of `forms`)
    forms: dict[str, list[str]] | None  # v2 only: grammatical category → forms
    forbidden: list[str]
    glossary_key: str | None
    status: str | None                 # v2 status; v1: "pilot" when review == pilot, else None
    applies_to: list[str]
    decided: dict | None
    raw: dict


@dataclass
class Row:
    lemma: str
    lemma_iast: str | None
    match: re.Pattern | None
    root_ids: list[str]
    upasargas: list[list[str]]
    senses: dict[str, Sense]
    dossier: str | None
    raw: dict


class Policy:
    def __init__(self, data: dict):
        if not isinstance(data, dict):
            raise BuildError("term policy is not a JSON object")
        self.raw = data
        self.sha256 = policy_content_hash(data)
        self.label = data.get("version")
        if "lemmas" in data:
            self.structure = "v2"
            rows = data["lemmas"]
        elif "terms" in data:
            self.structure = "v1"
            rows = data["terms"]
        else:
            raise BuildError("term policy has neither `terms` (v1) nor `lemmas` (v2)")
        self.translate_by_wording = set(data.get("translate_by_wording") or [])
        self.rows: dict[str, Row] = {}
        for lemma, r in rows.items():
            senses = {}
            for sname, s in (r.get("senses") or {}).items():
                forms = s.get("forms") if self.structure == "v2" else None
                if forms is not None and not isinstance(forms, dict):
                    raise BuildError(f"policy {lemma}/{sname}: `forms` must map a grammatical category to a list")
                english = [e for fl in (forms or {}).values() for e in fl] if forms is not None else list(s.get("english") or [])
                status = s.get("status") if self.structure == "v2" else ("pilot" if s.get("review") == "pilot" else None)
                iast = s.get("iast") or (r.get("lemma_iast") if s.get("policy") == "preserve" else None)
                senses[sname] = Sense(policy=s.get("policy", ""), iast=iast, iast_forms=list(s.get("iast_forms") or ([iast] if iast else [])),
                                      english=list(dict.fromkeys(english)), forms=forms, forbidden=list(s.get("forbidden_english") or []),
                                      glossary_key=s.get("glossaryKey"), status=status, applies_to=list(s.get("applies_to") or []),
                                      decided=s.get("decided"), raw=s)
            det = r.get("detect") or {}
            pat = r.get("match") or det.get("match")
            self.rows[lemma] = Row(lemma=lemma, lemma_iast=r.get("lemma_iast"), match=re.compile(pat) if pat else None,
                                   root_ids=list(det.get("root_ids") or ([r["root_id"]] if r.get("root_id") else [])),
                                   upasargas=[list(u) for u in det.get("upasargas") or []], senses=senses,
                                   dossier=r.get("dossier"), raw=r)
        self.reserved: dict[str, str] = {}
        for word, owner in (data.get("reserved_english") or {}).items():
            # Function words are never reserved (standard §7.15): a row may render
            # sarva "all", but "with anything at all" must stay writable elsewhere.
            if all(t in FUNCTION_WORDS for t in re.findall(r"[a-z']+", word.lower())):
                continue
            self.reserved[word] = self._row_key(owner) or owner

    def _row_key(self, owner: str) -> str | None:
        if owner in self.rows:
            return owner
        for k, r in self.rows.items():
            if owner in (r.lemma_iast, *(s.iast for s in r.senses.values())):
                return k
        return None

    def sense(self, lemma: str | None, sense: str | None) -> Sense | None:
        r = self.rows.get(lemma or "")
        return r.senses.get(sense or "") if r else None

    def regex_rows(self, w: dict) -> list[str]:
        hay = [x for x in [w.get("stem"), w.get("iast"), *[p.get("form", "") for p in w.get("parts") or []],
                           *((w.get("compound") or {}).get("members") or [])] if x]
        return [k for k, r in self.rows.items() if r.match and any(r.match.search(h) for h in hay)]

    def root_rows(self, w: dict) -> list[str]:
        rid = w.get("root_id")
        if not rid:
            return []
        ups = card_upasargas(w)
        out = []
        for k, r in self.rows.items():
            if rid in r.root_ids and (not r.upasargas or ups in r.upasargas):
                out.append(k)
        return out


def card_upasargas(w: dict) -> list[str]:
    out = []
    for p in w.get("parts") or []:
        f = (p.get("form") or "").strip()
        if f.startswith("√"):
            break
        if f.endswith("-") and not f.startswith("-"):
            out.append(f.rstrip("-"))
    return out


def load_policy(path: Path) -> Policy:
    return Policy(json.loads(path.read_text(encoding="utf-8")))


# ---------------------------------------------------------------- grammatical category of a card
def form_category(w: dict) -> str:
    if w.get("form_category"):
        return w["form_category"]
    a = f"{w.get('affix', '')} {w.get('morph', '')}"
    if re.search(r"\blyap\b|\bktvā\b|absolutive|\bgerund\b", a, re.I):
        return "absolutive"
    if re.search(r"\bktavatu\b", a):
        return "participle_past_active"
    if re.search(r"\bkta\b|past passive participle", a, re.I):
        return "participle_past"
    if re.search(r"\bśatṛ\b|\bśānac\b|present participle", a, re.I):
        return "participle_present"
    if re.search(r"\btumun\b|infinitive", a, re.I):
        return "infinitive"
    if re.search(r"\b(?:tṛc|tṛn|ṇvul|ṇini|ghinuṇ)\b|\bagent noun\b", a, re.I):
        return "agent"
    if re.search(r"indicative|imperative|optative|aorist|perfect|future|\bla[ṭṅ]\b|\blo[ṭ]\b|\bli[ṅṭ]\b|\blṛ[ṭṅ]\b|\blu[ṅṭ]\b", a, re.I):
        return "finite"
    return "noun"


# ---------------------------------------------------------------- source resolution (B2, B3, B17)
class Sources:
    """Resolves evidence loci against the files on disk. Paths are tried relative to
    the prakriya library, the Dev workspace and this repository, in that order."""

    def __init__(self, root: Path, prakriya: Path):
        self.root, self.prakriya = root, prakriya
        self.bases = [prakriya, root.parent, root]
        self._lines: dict[Path, list[str]] = {}
        self._json: dict[Path, Any] = {}

    def resolve(self, rel: str) -> Path | None:
        # Loci written as "vedanta-timeline/…" name THIS repository wherever it is checked
        # out (a deploy worktree is not at ../vedanta-timeline).
        if rel.startswith("vedanta-timeline/"):
            p = ROOT / rel[len("vedanta-timeline/"):]
            if p.is_file():
                return p
        for b in self.bases:
            p = b / rel
            if p.is_file():
                return p
        return None

    def lines(self, p: Path) -> list[str]:
        if p not in self._lines:
            self._lines[p] = p.read_text(encoding="utf-8", errors="replace").split("\n")
        return self._lines[p]

    def json(self, p: Path) -> Any:
        if p not in self._json:
            self._json[p] = json.loads(p.read_text(encoding="utf-8"))
        return self._json[p]

    def json_id_text(self, p: Path, ident: str) -> str | None:
        data = self.json(p)
        if p.name == "packet.json" or ident.startswith("verses["):
            return packet_selector_text(data, ident)
        body = data.get("data", data) if isinstance(data, dict) else data
        if isinstance(body, dict) and isinstance(body.get("text"), dict):          # Cologne kośa: data.text[id]
            rec = body["text"].get(ident)
            if rec is None:
                return None
            return " ".join(str(x) for x in rec) if isinstance(rec, list) else str(rec)
        if isinstance(body, list):                                                 # Dhātupāṭha and other id lists
            for e in body:
                if isinstance(e, dict) and str(e.get("i", e.get("id"))) == ident:
                    if "aupadeshik" in e:
                        from_lookup = f"{e.get('aupadeshik')} {e.get('gana')} {gana_name(e.get('gana'))} {e.get('pada')} {e.get('artha')}"
                        return from_lookup + " || " + " ".join(str(v) for v in e.values() if isinstance(v, str))
                    return " ".join(s for _, s in iter_strings(e))
            return None
        if isinstance(body, dict) and ident in body:
            return " ".join(s for _, s in iter_strings(body[ident]))
        return None

    def dhatu(self, root_id: str) -> dict | None:
        m = re.match(r"(?:.*dhatupatha\.json#)?(\d+)$", root_id or "")
        if not m:
            return None
        p = self.prakriya / "sources/raw/panini/lexica/dhatupatha.json"
        if not p.is_file():
            return None
        data = self.json(p)
        for e in data.get("data", data):
            if str(e.get("i")) == m.group(1):
                return e
        return None


GANA_NAMES = {1: "bhvādi", 2: "adādi", 3: "juhotyādi", 4: "divādi", 5: "svādi", 6: "tudādi", 7: "rudhādi", 8: "tanādi", 9: "kryādi", 10: "curādi"}


def gana_name(g: Any) -> str:
    try:
        return GANA_NAMES.get(int(g), "")
    except (TypeError, ValueError):
        return ""


def _find_key(node: Any, name: str) -> Any:
    """Breadth-first search for the first dict holding `name`."""
    queue = [node]
    while queue:
        cur = queue.pop(0)
        if isinstance(cur, dict):
            if name in cur:
                return cur[name]
            queue += list(cur.values())
        elif isinstance(cur, list):
            queue += cur
    return None


def _select(node: Any, sel: str) -> Any:
    if not isinstance(node, list):
        return None
    if "=" in sel:
        k, vs = sel.split("=", 1)
        hits = [e for e in node if isinstance(e, dict) and str(e.get(k)) in vs.split(",")]
        return hits[0] if len(hits) == 1 else (hits or None)
    if re.fullmatch(r"\d+\.\d+", sel):
        return next((e for e in node if isinstance(e, dict) and e.get("locus") == sel), None)
    if sel.isdigit():
        return node[int(sel)] if int(sel) < len(node) else None
    return next((e for e in node if isinstance(e, dict) and sel in [v for v in e.values() if isinstance(v, str)]), None)


def packet_selector_text(data: Any, ident: str) -> str | None:
    """Resolve a packet locus to its text. Two spellings are in use:
    `verses[12.1].commentaries.gita_gita_sanskrit[author=Sri Dhanpati]` (a list selector
    is `locus`, `key=value`, a bare value of some field, or a 0-based index) and
    `12.1/gita_gita_sanskrit/author_id=5` (a verse locus, then keys found by search)."""
    node = data
    if "/" in ident and "[" not in ident:
        for seg in ident.split("/"):
            if re.fullmatch(r"\d+\.\d+", seg):
                node = _select(node.get("verses") if isinstance(node, dict) else node, seg)
            elif "=" in seg:
                node = _select(node, seg)
            else:
                node = _find_key(node, seg)
            if node is None:
                return None
        return " ".join(s for _, s in iter_strings(node))
    for name, sel in re.findall(r"([A-Za-z_][\w]*)(?:\[([^\]]*)\])?", ident):
        if not isinstance(node, dict) or name not in node:
            return None
        node = node[name]
        if sel:
            node = _select(node, sel)
            if node is None:
                return None
    return " ".join(s for _, s in iter_strings(node))


@lru_cache(maxsize=None)
def _translit():
    try:
        from indic_transliteration import sanscript
        return sanscript
    except ImportError:
        return None


DEVA_RE = re.compile(r"[ऀ-ॿ]")


def quote_key(s: str) -> str:
    """Normalised comparison key: Devanāgarī → IAST, NFC, no accents, avagraha,
    punctuation or spaces; m and n folded (anusvāra versus class nasal)."""
    s = unicodedata.normalize("NFC", s or "")
    if DEVA_RE.search(s):
        tr = _translit()
        if tr is None:
            raise BuildError("indic_transliteration is required to compare Devanāgarī quotes (B2)")
        s = tr.transliterate(s, tr.DEVANAGARI, tr.IAST)
    return latin_key(s).replace("m", "n")


LOCUS_RE = re.compile(r"^(?P<path>[^\s:#()]+?\.(?:txt|json|js|md|tsv|csv|xml))(?:(?::(?P<a>\d+)(?:-(?P<b>\d+))?)|(?:#(?P<id>.+)))?(?:\s+\(.*\))?$")


def parse_locus(locus: str) -> dict | None:
    m = LOCUS_RE.match((locus or "").strip())
    return m.groupdict() if m else None


def approx_end(pat: str, text: str, k: int) -> int | None:
    """End index of the leftmost substring of `text` within edit distance k of `pat`
    (Sellers' algorithm), or None."""
    prev = [0] * (len(text) + 1)
    for i, pc in enumerate(pat, 1):
        cur = [i] + [0] * len(text)
        for j, tc in enumerate(text, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (pc != tc))
        prev = cur
    for j, d in enumerate(prev):
        if d <= k:
            return j
    return None


def quote_match(quote: str, text: str) -> str | None:
    """'exact' when every ellipsis-separated segment of the quote occurs, in order, in the
    text after folding (script, accents, spaces, hyphens, daṇḍas, avagraha, m/n);
    'sandhi' when a segment occurs only as a sandhi-resolved spelling (at most one edit per
    word junction plus two, and at most a quarter of the segment); else None."""
    hay = quote_key(text)
    pos, how = 0, "exact"
    for seg in re.split(r"…|\.\.\.|\[…\]", quote or ""):
        k = quote_key(seg)
        if not k:
            continue
        i = hay.find(k, pos)
        if i >= 0:
            pos = i + len(k)
            continue
        tol = min(len(re.findall(r"[\s\-]+", seg.strip())) + 2, max(2, len(k) // 4))
        e = approx_end(k, hay[pos:], tol)
        if e is None:
            return None
        pos, how = pos + e, "sandhi"
    return how


def quote_in(quote: str, text: str) -> bool:
    return quote_match(quote, text) is not None


# ---------------------------------------------------------------- the build
@dataclass
class Ctx:
    chapter: int
    root: Path = ROOT
    prakriya: Path = PRAKRIYA
    chapter_dir: Path | None = None
    policy_path: Path | None = None
    complete: bool = True                 # False with --allow-unreviewed (never for publication)
    lookup: Any = None                    # prakriya lookup module (or a test double); None → import it
    run_render_contract: bool = True
    report: Report = field(default_factory=Report)

    def __post_init__(self):
        self.chapter_dir = self.chapter_dir or self.root / f"internal/sanskrit_reviews/gita/ch{self.chapter}"
        self.policy_path = self.policy_path or self.root / "data/glossary/term_policy.json"
        self.policy = load_policy(self.policy_path)
        self.sources = Sources(self.root, self.prakriya)
        self.snapshot_dir = self.root / "internal/sanskrit_reviews/gita/policy-snapshots"

    def tools(self):
        if self.lookup is None:
            d = self.prakriya / "scripts/lookup"
            if (d / "lookup.py").is_file():
                sys.path.insert(0, str(d))
                try:
                    import lookup  # noqa: E402
                    self.lookup = lookup
                except Exception as e:  # pragma: no cover - environment
                    self.lookup = False
                    self.report.warn("TOOLS", f"prakriya lookup.py failed to import: {e}")
            else:
                self.lookup = False
        return self.lookup or None


# ---- policy checks on one card (presence; v1 rendering; B8 forms)
def check_term(ctx: Ctx, label: str, w: dict, phrases: str) -> Sense | None:
    rep, pol = ctx.report, ctx.policy
    term = w.get("term")
    for t in w.get("terms") or []:
        if not pol.sense((t or {}).get("lemma"), (t or {}).get("sense")):
            rep.err("POLICY", f"{label}: terms[] entry {t} is not a policy (lemma, sense)")
    if pol.structure == "v1":
        rows = pol.regex_rows(w)
        if rows and not term:
            rep.err("POLICY", f"{label}: matches policy row(s) {rows} but carries no term{{lemma,sense}}")
            return None
    else:
        rows = pol.root_rows(w)
        if rows and not term:
            rep.err("POLICY", f"{label}: root_id/upasargas match policy row(s) {rows} but the card carries no term")
            return None
        lint = [r for r in pol.regex_rows(w) if not term or r != term.get("lemma")]
        if lint and not term:
            rep.warn("POLICY", f"{label}: possible unmarked occurrence of {lint}")
    if not term:
        return None
    if not isinstance(term, dict):
        rep.err("POLICY", f"{label}: term must be {{lemma, sense}}")
        return None
    lemma, sname = term.get("lemma"), term.get("sense")
    row = pol.rows.get(lemma)
    if row is None:
        rep.err("POLICY", f"{label}: term.lemma {lemma!r} has no policy row")
        return None
    s = row.senses.get(sname)
    if s is None:
        rep.err("POLICY", f"{label}: term.sense {sname!r} not in policy senses {list(row.senses)} for {lemma}")
        return None
    if pol.structure == "v2" and s.status not in ADMITTED_STATUSES:
        rep.err("POLICY", f"{label}: {lemma}/{sname} has status {s.status!r}; production may use only {'/'.join(ADMITTED_STATUSES)} rows")
    if phrases:
        low = phrases.lower()
        if s.policy == "preserve":
            if not any(f in phrases for f in s.iast_forms or [s.iast or lemma]):
                rep.err("B8", f"{label}: preserved {lemma}/{sname} must print '{s.iast}' in its slot — got \"{phrases}\"")
        else:
            admitted = s.english
            if s.forms is not None:
                cat = form_category(w)
                admitted = s.forms.get(cat) or s.forms.get("any")
                if admitted is None:
                    rep.err("B8", f"{label}: {lemma}/{sname} has no form decided for grammatical category '{cat}' (forms: {sorted(s.forms)})")
                    admitted = []
            if admitted and not any(word_re(e).search(low) for e in admitted):
                rep.err("B8", f"{label}: translated {lemma}/{sname} must use one of {admitted} — got \"{phrases}\"")
        gk = s.glossary_key
        if gk and w.get("glossaryKey") not in (gk, None):
            rep.warn("POLICY", f"{label}: glossaryKey {w.get('glossaryKey')!r} differs from policy's {gk!r}")
    return s


def own_lemmas(w: dict) -> set[str]:
    out = {(w.get("term") or {}).get("lemma")} | {(t or {}).get("lemma") for t in w.get("terms") or []}
    return {x for x in out if x}


def card_forbidden(ctx: Ctx, w: dict) -> list[tuple[str, str]]:
    """(forbidden word, lemma/sense) for every policy sense the card declares."""
    out = []
    for t in [w.get("term")] + list(w.get("terms") or []):
        s = ctx.policy.sense((t or {}).get("lemma"), (t or {}).get("sense"))
        if s:
            out += [(b, f"{t['lemma']}/{t['sense']}") for b in s.forbidden]
    return list(dict.fromkeys(out))


# ---- B9 public text and B13 secondaries in public strings
OPEN_QUOTE = r"(?:[“‘\"]|(?<![A-Za-z])')"     # an opening quotation mark, not a possessive apostrophe


def check_public_text(ctx: Ctx, label: str, node: Any, translators: list[str], reception_paths: set[str] = frozenset()) -> None:
    """B9 pipeline vocabulary in any public string; B13 a translator named and then quoted,
    except in `reception` meaning lines, whose quotation length check_meaning caps."""
    rep = ctx.report
    for path, s in iter_strings(node):
        top = re.split(r"[.\[]", path)[-1] if path else ""
        if top in SANSKRIT_ONLY_FIELDS:
            continue
        for name, pat in PIPELINE_PATTERNS:
            m = pat.search(s)
            if m:
                rep.err("B9", f"{label} {path}: pipeline vocabulary ({name}) '{m.group(0)}' in public text — \"{s[:120]}\"")
                break
        if path in reception_paths:
            continue
        for t in translators:
            m = re.search(rf"\b{re.escape(t)}\b[^\"“‘\n]{{0,40}}?{OPEN_QUOTE}", s)
            if m:
                rep.err("B13", f"{label} {path}: translator '{t}' followed by a quotation in public text — \"{s[:120]}\"")
                break


def check_meaning(ctx: Ctx, label: str, w: dict, phrases: str, required: bool, line: str = "") -> None:
    rep = ctx.report
    m = w.get("meaning")
    if m is None:
        if required:
            rep.err("MEANING", f"{label}: `meaning` required (card has a root, a compound or a preserved term)")
        return
    if not isinstance(m, dict):
        rep.err("MEANING", f"{label}: `meaning` must be an object")
        return
    lines = m.get("lines")
    if not isinstance(lines, list) or not (1 <= len(lines) <= MEANING_MAX_LINES):
        rep.err("MEANING", f"{label}: meaning.lines must hold 1–{MEANING_MAX_LINES} lines")
        lines = lines if isinstance(lines, list) else []
    last = -1
    for k, ln in enumerate(lines):
        if not isinstance(ln, dict):
            rep.err("MEANING", f"{label}: meaning.lines[{k}] is not an object")
            continue
        cat = ln.get("cat")
        if cat not in MEANING_CATS:
            rep.err("MEANING", f"{label}: meaning.lines[{k}].cat {cat!r} not in {MEANING_CATS}")
            continue
        if not (ln.get("text") or "").strip():
            rep.err("MEANING", f"{label}: meaning.lines[{k}] ({cat}) has no text")
        if cat in MEANING_ATTRIBUTED and not (ln.get("who") or "").strip():
            rep.err("MEANING", f"{label}: meaning.lines[{k}] ({cat}) names no source (`who`)")
        if MEANING_CATS.index(cat) < last:
            rep.err("MEANING", f"{label}: meaning.lines out of display order at [{k}] ({cat})")
        last = max(last, MEANING_CATS.index(cat))
        if cat == "reception":
            quoted = " ".join(QUOTED_RE.findall(ln.get("text") or ""))
            if len(re.findall(r"[A-Za-z]+", quoted)) > RECEPTION_QUOTE_MAX_WORDS:
                rep.err("B13", f"{label}: meaning.lines[{k}] reception quotes more than {RECEPTION_QUOTE_MAX_WORDS} words")
        if ln.get("locus"):
            check_locus_exists(ctx, f"{label} meaning.lines[{k}]", ln["locus"])
    rendering = m.get("rendering")
    if rendering is not None:
        if not isinstance(rendering, str) or not rendering.strip():
            rep.err("MEANING", f"{label}: meaning.rendering must be a non-empty string")
        elif phrases:
            # the rendering may span neighbouring slots ('I become' where 'I' is aham's slot):
            # it must read in order in the line and share a word with this card's slot
            toks = lambda x: re.findall(r"[a-zA-Zāīūṛṝḷṃḥṅñṭḍṇśṣ'-]+", x.lower())
            want, slot = toks(rendering), set(toks(phrases))
            it = iter(toks(SLOT_RE.sub(lambda m: m.group(2), line)))
            if not (set(want) & slot and all(any(x == y for y in it) for x in want)):
                rep.err("MEANING", f"{label}: meaning.rendering '{rendering}' is not what the line prints for this word (\"{phrases}\")")
    alts = m.get("alternatives")
    if alts is not None and not (isinstance(alts, list) and all(isinstance(a, str) for a in alts)):
        rep.err("MEANING", f"{label}: meaning.alternatives must be a list of strings")


def check_locus_exists(ctx: Ctx, label: str, locus: str) -> dict | None:
    pl = parse_locus(locus)
    if not pl:
        return None
    p = ctx.sources.resolve(pl["path"])
    if p is None:
        ctx.report.err("B2", f"{label}: locus file not found: {locus}")
        return None
    if pl["a"]:
        a, b = int(pl["a"]), int(pl["b"] or pl["a"])
        if not (1 <= a <= b <= len(ctx.sources.lines(p))):
            ctx.report.err("B2", f"{label}: line range out of file: {locus}")
            return None
    return {**pl, "file": p}


def check_evidence(ctx: Ctx, label: str, ev: list, b12: bool = True) -> None:
    rep, src = ctx.report, ctx.sources
    tools = None
    for k, e in enumerate(ev):
        el = f"{label} evidence[{k}]"
        if not isinstance(e, dict):
            rep.err("B12", f"{el}: evidence item is not an object")
            continue
        if b12:
            for key in ("claim", "locus", "quote", "kind"):
                if not (isinstance(e.get(key), str) and e[key].strip()):
                    rep.err("B12", f"{el}: evidence lacks {key}")
            extra = set(e) - EVIDENCE_KEYS
            if extra:
                rep.err("B12", f"{el}: evidence keys outside {{claim, locus, quote, sutra?, kind}}: {sorted(extra)}")
        locus = e.get("locus") or ""
        pl = check_locus_exists(ctx, el, locus)
        if pl is None:
            if not parse_locus(locus):
                rep.err("B2", f"{el}: locus is not file:line[-line] or file#id: {locus!r}")
            continue
        p = pl["file"]
        if pl["a"]:
            a, b = int(pl["a"]), int(pl["b"] or pl["a"])
            text = "\n".join(src.lines(p)[a - 1:b])
        elif pl["id"]:
            text = src.json_id_text(p, pl["id"])
            if text is None:
                rep.err("B2", f"{el}: {pl['path']}#{pl['id']} does not exist")
                continue
        else:
            text = p.read_text(encoding="utf-8", errors="replace")
        record = bool(pl["id"]) and p.name == "dhatupatha.json"     # a record of fields, not prose: every quoted token in it
        found = (all(quote_key(t) in quote_key(text) for t in re.split(r"[\s()\[\],;]+", e["quote"]) if quote_key(t))
                 if record else quote_match(e["quote"], text)) if e.get("quote") else True
        if found == "sandhi":
            rep.warn("B2", f"{el}: quote matches {locus} only as a sandhi-resolved spelling")
        if not found:
            rep.err("B2", f"{el}: quote not found in {locus} — \"{e['quote'][:70]}\"")
        if "kashika" in pl["path"]:
            if not e.get("sutra"):
                rep.err("B3", f"{el}: Kāśikā locus without `sutra`")
                continue
            tools = tools or ctx.tools()
            span_fn = getattr(tools, "kashika_span", None) if tools else None
            if span_fn is None:
                rep.err("B3", f"{el}: Kāśikā span cannot be verified (lookup.kashika_span, audit L-3, unavailable)")
                continue
            sm0 = re.fullmatch(r"(\d)\.(\d)\.(\d+)", str(e["sutra"]).strip())
            span = span_fn(f"{sm0.group(1)}{sm0.group(2)}{int(sm0.group(3)):03d}" if sm0 else str(e["sutra"]))
            if not span:
                rep.err("B3", f"{el}: no Kāśikā vṛtti span for sūtra {e['sutra']}")
                continue
            key = "kashika_upstream" if "upstream" in pl["path"] else "kashika"
            sm = re.search(r":(\d+)(?:-(\d+))?$", span.get(key) or "")
            if not sm or not pl["a"]:
                rep.err("B3", f"{el}: Kāśikā locus {locus} has no line range comparable with the span {span}")
                continue
            s0, s1 = int(sm.group(1)), int(sm.group(2) or sm.group(1))
            if not (s0 <= int(pl["a"]) and int(pl["b"] or pl["a"]) <= s1):
                rep.err("B3", f"{el}: Kāśikā locus {locus} lies outside the vṛtti of {e['sutra']} ({span.get(key)})")


def english_stack_sources(ctx: Ctx) -> set[str] | None:
    db = ctx.prakriya / "tmp/english/english.db"
    if not db.is_file():
        return None
    import sqlite3
    con = sqlite3.connect(str(db))
    try:
        return {r[0] for r in con.execute("select distinct source from defs")}
    finally:
        con.close()


def define_result(raw: Any) -> dict:
    """Normalise lookup.english_define output: a list of entries (older lookup) or
    {attested, groups[{entries, phrase_entries}], not_indexed} (audit L-1/L-2)."""
    if isinstance(raw, list):
        return {"attested": bool(raw), "loci": {e.get("locus") for e in raw if isinstance(e, dict)}, "not_indexed": None}
    if isinstance(raw, dict):
        loci = {e.get("locus") for g in raw.get("groups") or [] for e in (g.get("entries") or []) + (g.get("phrase_entries") or [])
                if isinstance(e, dict)}
        return {"attested": bool(raw.get("attested")), "loci": loci, "not_indexed": raw.get("not_indexed") or {}}
    return {"attested": False, "loci": set(), "not_indexed": None}


def locus_in_define(cited: str, loci: set) -> str | None:
    """'entry' when the cited locus is one define returns for the word (allowing the index's
    longer path prefix and, for line loci, the entry's first lines rather than its headword
    line); 'file' when the citation names only the source file (GCIDE letter files) and
    define finds the word's headword in that file; else None."""
    cited = re.sub(r"\s+\([^)]*\)$", "", cited.strip())
    cm = re.fullmatch(r"(.+?):(\d+)", cited)
    file_level = not cm and "#" not in cited and not re.search(r":\d", cited)
    for l in loci:
        l = l or ""
        if l == cited or l.endswith("/" + cited):
            return "entry"
        lm = re.fullmatch(r"(.+?):(\d+)", l)
        if cm and lm and (lm.group(1) == cm.group(1) or lm.group(1).endswith("/" + cm.group(1))) \
                and 0 <= int(cm.group(2)) - int(lm.group(2)) <= 2:
            return "entry"
    if file_level and any(re.search(rf"(?:^|/){re.escape(cited)}(?:#|:)", l or "") for l in loci):
        return "file"
    return None


def check_wording(ctx: Ctx, label: str, wd: dict, define_cache: dict) -> None:
    rep = ctx.report
    for k in ("sense_description", "candidates", "chosen"):
        if not wd.get(k):
            rep.err("CARD", f"{label}: wording lacks {k}")
    tools = ctx.tools()
    define = getattr(tools, "english_define", None) if tools else None

    def lookup_def(word: str) -> dict | str:
        """define_result(...) or a string saying why define could not answer."""
        if define is None:
            return "lookup.english_define unavailable"
        if word not in define_cache:
            try:
                try:
                    raw = define(word, limit=500)       # every entry, not the first few (homographs)
                except TypeError:
                    raw = define(word)
                define_cache[word] = define_result(raw)
            except BaseException as e:  # english_define raises SystemExit when the index is missing or incomplete
                define_cache[word] = f"define refused: {str(e)[:120]}"
        return define_cache[word]

    for c in wd.get("candidates") or []:
        if not isinstance(c, dict):
            continue
        word = c.get("word") or ""
        if c.get("source") == "composed":
            # a phrase composed of attested words (lead decision 2026-11-08): every part must resolve
            parts = c.get("parts")
            if not (isinstance(parts, list) and parts and all(isinstance(x, str) and x.strip() for x in parts)):
                rep.err("B4", f"{label}: composed candidate '{word}' must list its headwords in `parts`")
                continue
            for part in parts:
                got = lookup_def(part)
                if isinstance(got, str) or not got["attested"]:
                    rep.err("B4", f"{label}: composed candidate '{word}': part '{part}' does not resolve via define"
                                  + (f" ({got})" if isinstance(got, str) else ""))
            continue
        if not ENGLISH_SOURCE_RE.search(str(c.get("source", ""))):
            continue
        got = lookup_def(word)
        if isinstance(got, str):
            rep.err("B4", f"{label}: candidate '{word}' cannot be verified ({got})")
        elif not got["attested"]:
            hint = "; a phrase of attested words may be source: composed with parts" if len(word.split()) > 1 else ""
            rep.err("B4", f"{label}: candidate '{word}' ({c.get('source')}) has no headword in the English stack{hint}")
        else:
            how = locus_in_define(str(c.get("locus")), got["loci"])
            if how is None:
                rep.err("B4", f"{label}: candidate '{word}' cites {c.get('locus')!r}, not one of define's loci for it")
            elif how == "file":
                rep.warn("B4", f"{label}: candidate '{word}' cites only the file {c.get('locus')!r}; define finds the headword there")
    if wd.get("joycean"):
        for k in ("formation", "parts", "relation", "paraphrase", "why_no_attested_word"):
            if not wd["joycean"].get(k):
                rep.err("CARD", f"{label}: joycean record lacks {k}")
        chosen = wd.get("chosen")
        chosen = chosen.get("word") if isinstance(chosen, dict) else chosen
        got = lookup_def(chosen or "")
        if isinstance(got, str):
            rep.err("B4", f"{label}: Joycean record for '{chosen}' cannot be certified ({got})")
            return
        if got["attested"]:
            rep.err("B4", f"{label}: Joycean record for '{chosen}', but define attests it ({len(got['loci'])} loci)")
        report_fn = getattr(tools, "english_define_report", None)
        if got["not_indexed"] is None and report_fn is not None:
            try:
                got = dict(got, not_indexed=(report_fn(chosen or "") or {}).get("not_indexed") or {})
            except BaseException as e:
                rep.err("B4", f"{label}: Joycean record for '{chosen}' cannot be certified (define report failed: {str(e)[:100]})")
                return
        if got["not_indexed"] is None:                      # older lookup: read the index's sources directly
            have = english_stack_sources(ctx) or set()
            missing = [s for s in ENGLISH_STACK if not any(h.startswith(s) for h in have)]
            if missing:
                rep.err("B4", f"{label}: Joycean record cannot be certified: the English stack lacks {missing}")
        elif got["not_indexed"]:
            # sources the lookup declares unobtainable, with its reason: reported, not fatal
            rep.warn("B4", f"{label}: Joycean record certified without {sorted(got['not_indexed'])} (declared not indexable by lookup.py)")


def check_root(ctx: Ctx, label: str, w: dict) -> None:
    rep = ctx.report
    root = w.get("root")
    if not root:
        return
    if not w.get("rootGloss"):
        rep.err("CARD", f"{label}: root given without rootGloss")
    m = re.search(r"\(([a-zā]+ādi),\s*(\d+)\s*([PAUĀ])\b", root)
    if not m:
        rep.err("B17", f"{label}: root {root!r} lacks '(gaṇa, NP)' e.g. '√yuj (rudhādi, 7U)'")
        return
    rid = w.get("root_id")
    if not rid:
        rep.err("B17", f"{label}: root {root!r} without root_id (dhatupatha.json record)")
        return
    rec = ctx.sources.dhatu(rid)
    if rec is None:
        rep.err("B17", f"{label}: root_id {rid!r} does not resolve in dhatupatha.json")
        return
    gname, gnum, pada = m.group(1), int(m.group(2)), m.group(3).replace("Ā", "A")
    if int(rec["gana"]) != gnum or gana_name(rec["gana"]) != gname or rec["pada"] != pada:
        rep.err("B17", f"{label}: root string says {gname} {gnum}{pada}; record {rid} is {gana_name(rec['gana'])} {rec['gana']}{rec['pada']}")


def check_card(ctx: Ctx, label: str, w: dict, idx: int, phrases: str, define_cache: dict, line: str = "") -> dict:
    rep = ctx.report
    for k in ("iast", "deva", "gloss", "parts", "affix", "morph"):
        if k not in w or w[k] in (None, "", []):
            rep.err("CARD", f"{label}: card field {k!r} missing/empty")
    if w.get("i") != idx:
        rep.err("CARD", f"{label}: i={w.get('i')} but position is {idx}")
    for p in w.get("parts") or []:
        if not p.get("form") or not p.get("gloss"):
            rep.err("CARD", f"{label}: parts[] piece lacks form/gloss: {p}")
    wc = w.get("word_class")
    if wc not in WORD_CLASSES:
        rep.err("B12", f"{label}: word_class {wc!r} not in {sorted(WORD_CLASSES)}")
    check_root(ctx, label, w)
    gk = w.get("glossaryKey")
    if gk and not (ctx.root / "data/glossary" / f"{gk}.json").exists():
        rep.err("CARD", f"{label}: glossaryKey {gk!r} has no file data/glossary/{gk}.json")
    comp = w.get("compound")
    if comp:
        for k in ("type", "vigraha", "members"):
            if not comp.get(k):
                rep.err("CARD", f"{label}: compound lacks {k}")
    ev, fb = w.get("evidence") or [], w.get("fallback") or []
    if (w.get("root") or comp or (w.get("affix") and "avyaya" not in w["affix"] and "nipāta" not in w["affix"])) and not ev and not fb:
        rep.err("CARD", f"{label}: no evidence[] and no fallback[] for a grammatical claim")
    check_evidence(ctx, label, ev)
    for k, f in enumerate(fb):
        if not isinstance(f, dict) or not (f.get("kind") or "").strip() or not (f.get("text") or f.get("claim") or "").strip():
            rep.err("B18", f"{label}: fallback[{k}] must be {{kind, text}} — got {str(f)[:80]}")
        elif f["kind"] in BLOCKING_FALLBACK_KINDS and ctx.complete:
            rep.err("B18", f"{label}: fallback on a {f['kind']} blocks a complete chapter (plan §13.4.2)")
    sense = check_term(ctx, label, w, phrases)
    preserved = bool(sense and sense.policy == "preserve")
    if wc == "content" and not preserved and not w.get("wording"):
        rep.err("CARD", f"{label}: content word without wording{{}} record")
    if w.get("wording"):
        check_wording(ctx, label, w["wording"], define_cache)
    # B5 form agreement
    cat = form_category(w)
    for ph in ([phrases] if phrases and not comp else []):     # a member's kta/lyap is not the card's own form
        if cat == "absolutive" and not re.match(r"^\W*having\b", ph, re.I) and not w.get("form_note"):
            rep.err("B5", f"{label}: lyap/ktvā printed \"{ph}\" (not 'having …') without form_note")
        if cat == "participle_past" and not w.get("form_note"):
            toks = [t.lower() for t in re.findall(r"[A-Za-z]+", ph)]
            while toks and toks[-1] in TRAILING_PARTICLES:
                toks.pop()
            if toks and toks[-1].endswith("ing") and len(toks[-1]) > 4 and toks[-1] not in ING_EXCEPTIONS:
                rep.err("B5", f"{label}: kta printed as an -ing form ('{toks[-1]}') in \"{ph}\" without form_note")
    # B6 forbidden words: the rendered slot (check_forbidden_in_line) and meaning.rendering.
    # gloss, parts[].gloss and meaning.lines list dictionary senses and are not scanned (lead, 2026-11-08).
    m = w.get("meaning") if isinstance(w.get("meaning"), dict) else {}
    val = m.get("rendering")
    if isinstance(val, str):
        bare = strip_quotations(val).lower()
        for bad, row in card_forbidden(ctx, w):
            if word_re(bad).search(bare):
                rep.err("B6", f"{label} meaning.rendering: forbidden '{bad}' ({row}) — \"{val[:100]}\"")
    # meaning (card meaning schema)
    required = bool(w.get("root") or comp or preserved) and wc not in ("particle", "pronoun", "name")
    check_meaning(ctx, label, w, phrases, required, line)
    public = {k: w[k] for k in ("i", "deva", "iast", "gloss", "stem", "root", "rootGloss", "affix", "morph", "karaka",
                                 "glossaryKey", "translatable", "parts", "compound", "sandhi", "note", "term", "meaning")
              if k in w and w[k] is not None}
    return public


def public_fork(f: dict) -> dict:
    out = {k: f[k] for k in ("at", "words", "display", "open", "followed", "reason_class") if k in f}
    out["construals"] = [{k: c[k] for k in ("reading", "traditions") if k in c} for c in f.get("construals") or [] if isinstance(c, dict)]
    return out


def check_forks(ctx: Ctx, label: str, v: dict, n_words: int) -> None:
    rep, ch = ctx.report, ctx.chapter
    forks = v.get("forks") or []
    for f in forks:
        fl = f"{label} fork at {f.get('at')!r}"
        cons = f.get("construals") or []
        if len(cons) < 2:
            rep.err("B7", f"{fl}: fewer than two construals")
        for k, c in enumerate(cons):
            if not isinstance(c, dict) or not ((c.get("basis") or c.get("grammar_basis") or "").strip()):
                rep.err("B7", f"{fl}: construal {k} lacks basis")
            for e in (c.get("evidence") or []) if isinstance(c, dict) else []:
                if isinstance(e, str) and parse_locus(e):
                    check_locus_exists(ctx, f"{fl} construal {k}", e)
        if not isinstance(f.get("followed"), int) or not (0 <= f["followed"] < len(cons)):
            rep.err("B7", f"{fl}: 'followed' index invalid")
        if f.get("reason_class") not in (1, 2, 3, 4, 5):
            rep.err("B7", f"{fl}: reason_class must be 1–5 (plan §13.2)")
        if (f.get("open") is True) != (f.get("reason_class") == 5):
            rep.err("B7", f"{fl}: open must be true exactly when reason_class is 5 (open={f.get('open')!r}, class={f.get('reason_class')!r})")
        if re.search(r"\b(because|since)\b[^.;]{0,60}\b(Śaṅkara|Rāmānuja|Madhva|Abhinavagupta|the school|the tradition|the commentators?)\b[^.;]{0,40}\b(reads?|says?|takes?|holds?|glosses)\b", f.get("reason", ""), re.I):
            rep.err("B7", f"{fl}: resolved by a school's authority — not an admissible reason")
        words = f.get("words")
        if not (isinstance(words, list) and words and all(isinstance(i, int) and 0 <= i < n_words for i in words)):
            rep.err("B7", f"{fl}: `words` must list the card indices the fork concerns (0–{n_words - 1})")
        if f.get("open") is True and not (f.get("display") or "").strip():
            rep.err("B7", f"{fl}: open fork without reader-facing `display`")
        if "display" in f and not (isinstance(f["display"], str) and f["display"].strip()):
            rep.err("B7", f"{fl}: `display` must be a non-empty string")
    loc = v.get("locus")
    if loc in REQUIRED_FORK_VERSES.get(ch, set()) and not forks:
        rep.err("B7", f"{label}: fairness locus without a fork record (plan §13.3)")
    for floc, key in FAIRNESS_WORDS.get(ch, []):
        if floc != loc:
            continue
        idx = {i for i, w in enumerate(v.get("words") or []) if latin_key(w.get("iast", "")).startswith(key)}
        if not idx:
            rep.err("B7", f"{label}: fairness word '{key}' not found among the cards")
        elif not any(set(f.get("words") or []) & idx for f in forks):
            rep.err("B7", f"{label}: fairness locus '{key}' (cards {sorted(idx)}) has no fork naming it in `words`")


# ---- B11 pada-pāṭha versus saṃhitā by token alignment
def samhita_tokens(iast: str) -> list[tuple[str, bool]]:
    out = []
    for t in re.split(r"\s+", (iast or "").replace("|", " ")):
        if not t:
            continue
        elided = t[0] in "'’ऽ"
        k = latin_key(t)
        if k:
            out.append((k, elided))
    return out


def group_matches(padas: list[str], tok: str, elided: bool) -> bool:
    J = "".join(padas)
    if not J:
        return False
    if elided:
        if J[0] != "a":
            return False
        J = J[1:]
    n_j = len(padas) - 1
    if J[:1] == "s" and tok[:2] == "ch":           # ś → ch after a stop (8.4.63)
        J = "ch" + J[1:]
    if not (J[:1] == tok[:1] or (J[:1] == "s" and tok[:2] == "ch") or (J[:1] == "h" and tok[1:2] == "h")):
        return False
    if len(tok) - len(J) > 1 + n_j or len(J) - len(tok) > 1 + n_j:
        return False
    return edit_distance(J, tok) <= 2 * n_j + 2


def align_padas(samhita: list[tuple[str, bool]], padas: list[str], max_group: int = 4) -> int | None:
    """Monotone alignment of pada groups to saṃhitā tokens. Returns None when every
    token is covered exactly once, else the index of the first token that cannot be."""
    m, n = len(samhita), len(padas)
    reach = [[False] * (n + 1) for _ in range(m + 1)]
    reach[0][0] = True
    best = 0
    for i in range(m):
        for j in range(n + 1):
            if not reach[i][j]:
                continue
            for g in range(1, max_group + 1):
                if j + g <= n and group_matches(padas[j:j + g], *samhita[i]):
                    reach[i + 1][j + g] = True
                    best = max(best, i + 1)
    return None if reach[m][n] else best


def check_pada_patha(ctx: Ctx, label: str, pv: dict, words: list[dict]) -> None:
    sam = samhita_tokens(pv["iast"])
    padas = [latin_key(w.get("iast", "")) for w in words]
    bad = align_padas(sam, padas)
    if bad is not None:
        near = " ".join(t for t, _ in sam[max(0, bad - 1): bad + 2])
        ctx.report.err("B11", f"{label}: pada-pāṭha does not reproduce the BORI saṃhitā token by token (first unmatched near '{near}'); nothing may be dropped or invented")


# ---- verse
def check_verse(ctx: Ctx, v: dict, pv: dict, translators: list[str], define_cache: dict) -> tuple[dict, dict, int]:
    rep = ctx.report
    loc = v.get("locus")
    label = f"{loc}"
    if v.get("iast") != pv["iast"]:
        rep.err("VERSE", f"{label}: iast differs from packet (must be verbatim)")
    if v.get("devanagari") != pv["devanagari"]:
        rep.err("VERSE", f"{label}: devanagari differs from packet (must be verbatim)")
    if v.get("speaker") != pv["speaker"]:
        rep.err("VERSE", f"{label}: speaker {v.get('speaker')!r} ≠ packet {pv['speaker']!r}")
    for k in ("sense", "english", "words", "grammar"):
        if not v.get(k):
            rep.err("VERSE", f"{label}: missing {k}")
    english = v.get("english") or ""
    if "[" in english or "]" in english:
        rep.err("VERSE", f"{label}: bracket insert in english line")
    rest = SLOT_RE.sub("", english)
    if "{" in rest or "}" in rest:
        rep.err("B12", f"{label}: malformed slot syntax in english line")
    for m in SLOT_RE.finditer(english):
        if not m.group(2).strip():
            rep.err("B12", f"{label}: empty slot {m.group(0)}")
    words = v.get("words") or []
    smap = slot_map(english)
    n = len(words)
    for i in smap:
        if i >= n or i < 0:
            rep.err("VERSE", f"{label}: slot {{{i}:…}} has no word")
    unslotted = [w.get("iast") for w in words if w.get("i") not in smap]
    if unslotted:
        rep.warn("VERSE", f"{label}: unslotted words {unslotted}")
    check_pada_patha(ctx, label, pv, words)
    # B5 mood: a question mark needs an interrogative word
    if "?" in english and not any((w.get("stem") or "") in INTERROGATIVE_STEMS or (w.get("iast") or "") in INTERROGATIVE_FORMS
                                  or re.search(r"interrogative", f"{w.get('morph', '')} {w.get('affix', '')} {w.get('karaka', '')}", re.I)
                                  for w in words):
        rep.err("B5", f"{label}: '?' in the line but no word is interrogative (kim, kva, katham …)")
    public_words, apparatus_words, fallbacks = [], [], 0
    for idx, w in enumerate(words):
        wl = f"{label}[{idx}] {w.get('iast')}"
        phrases = " ".join(smap.get(idx, []))
        public_words.append(check_card(ctx, wl, w, idx, phrases, define_cache, english))
        fallbacks += len(w.get("fallback") or [])
        apparatus_words.append({"i": idx, "iast": w.get("iast"), "evidence": w.get("evidence") or [], "fallback": w.get("fallback") or [],
                                "wording": w.get("wording"), "term": w.get("term"), "form_note": w.get("form_note")})
    check_forbidden_in_line(ctx, label, v, words, smap)
    check_forks(ctx, label, v, n)
    if "deviations" not in v:
        rep.err("VERSE", f"{label}: deviations[] missing (may be empty)")
    if len(v.get("secondaries_consulted") or []) < 5:
        rep.err("VERSE", f"{label}: fewer than five secondaries consulted")
    public = {"locus": loc, "speaker": v.get("speaker"), "meter": v.get("meter") or "anuṣṭubh", "devanagari": v.get("devanagari"),
              "iast": v.get("iast"), "sense": v.get("sense"), "english": english, "words": public_words, "grammar": v.get("grammar"),
              "forks": [public_fork(f) for f in v.get("forks") or []]}
    reception = {f"words[{i}].meaning.lines[{k}].text" for i, w in enumerate(public_words)
                 for k, ln in enumerate((w.get("meaning") or {}).get("lines") or [] if isinstance(w.get("meaning"), dict) else [])
                 if isinstance(ln, dict) and ln.get("cat") == "reception"}
    check_public_text(ctx, label, {k: public[k] for k in ("sense", "english", "grammar", "forks", "words")}, translators, reception)
    apparatus = {"locus": loc, "words": apparatus_words, "forks": v.get("forks") or [],
                 "secondaries_consulted": v.get("secondaries_consulted"), "fallback_count": fallbacks,
                 "_private_deviations": v.get("deviations")}
    return public, apparatus, fallbacks


def slot_groups(english: str) -> dict[int, list[tuple[str, list[int]]]]:
    """index → [(slot text, every index that slot carries)]."""
    out: dict[int, list[tuple[str, list[int]]]] = {}
    for m in SLOT_RE.finditer(english or ""):
        idx = [int(i) for i in m.group(1).split(",") if i.strip()]
        for i in idx:
            out.setdefault(i, []).append((m.group(2), idx))
    return out


def member_rows(pol: "Policy", w: dict) -> list[list[str]]:
    """For each compound member, the table rows whose detector matches it (the term detector's rule)."""
    return [pol.regex_rows({"stem": m, "iast": m}) for m in (w.get("compound") or {}).get("members") or [] if isinstance(m, str)]


def check_forbidden_in_line(ctx: Ctx, label: str, v: dict, words: list[dict], smap: dict[int, list[str]]) -> None:
    """B6 on each rendered slot against the card's own policy senses, and B8 reserved
    English; quotations exempt. Reserved English is the card's own when it owns the row, when
    another index of the same {i,j} slot owns it (na + verb: the verb owns 'shrink'), or when a
    member of the card's compound matches the row (lead, 2026-11-08). A compound member that
    two rows match needs its sense named (`terms` entry with `member`)."""
    rep, pol = ctx.report, ctx.policy
    groups = slot_groups(v.get("english") or "")
    for i, w in enumerate(words):
        mrows = member_rows(pol, w)
        named = {t.get("member") for t in w.get("terms") or [] if isinstance(t, dict)}
        for k, rows in enumerate(mrows):
            if len(rows) > 1 and k not in named:
                rep.err("B8", f"{label}[{i}] {w.get('iast')}: compound member {w['compound']['members'][k]!r} matches rows {rows}; "
                              "name its sense (compound.members[].sense)")
        for ph, idx in groups.get(i, []) or [(p, [i]) for p in smap.get(i, [])]:
            bare = strip_quotations(ph).lower()
            for bad, row in card_forbidden(ctx, w):
                if word_re(bad).search(bare):
                    rep.err("B6", f"{label}[{i}] {w.get('iast')}: slot uses forbidden '{bad}' ({row}) — \"{ph}\"")
            owners = set(own_lemmas(w)) | {r for rows in mrows for r in rows}
            for j in idx:
                if j != i and 0 <= j < len(words):
                    owners |= own_lemmas(words[j])
            for rw, owner in pol.reserved.items():
                if word_re(rw).search(bare) and owner not in owners:
                    rep.err("B8", f"{label}[{i}] {w.get('iast')}: reserved English '{rw}' (for {owner}) printed for another lemma — \"{ph}\"")


# ---- reviews (B15) and shards (B1, B12)
def check_review(ctx: Ctx, sp: Path, rev: Path) -> None:
    rep = ctx.report
    r = json.loads(rev.read_text(encoding="utf-8"))
    current = sha256_file(sp)
    if r.get("producer_sha256") != current:
        rep.err("REVIEW", f"{rev.name}: producer_sha256 does not match the current {sp.name} (review is stale)")
    if r.get("complete") is not True:
        rep.err("REVIEW", f"{rev.name}: review not complete")
    open_sev1 = [f for f in r.get("findings", []) if f.get("severity") == 1 and f.get("status", "open") != "resolved"]
    if open_sev1:
        rep.err("REVIEW", f"{rev.name}: {len(open_sev1)} open severity-1 findings")
    rr = r.get("rereview")
    rr_date = (rr or {}).get("date") if isinstance(rr, dict) else None
    if isinstance(rr, dict):
        if rr.get("producer_sha256") != r.get("producer_sha256") or not rr_date:
            rep.err("B15", f"{rev.name}: rereview must record the producer_sha256 it re-reviewed and its date; "
                           f"the stamped hash is not the re-reviewed one")
    for e in r.get("lead_edits_after_acceptance") or []:
        if e.get("new_sha256") == r.get("producer_sha256") and not (rr_date and rr_date >= str(e.get("date", "")) and
                                                                   isinstance(rr, dict) and rr.get("producer_sha256") == e.get("new_sha256")):
            rep.err("B15", f"{rev.name}: producer_sha256 re-stamped after an edit ({e.get('date')}) without re-review")
    sh = json.loads(sp.read_text(encoding="utf-8"))
    changed = sh.get("last_changed")
    reviewed = rr_date or r.get("date")
    if changed and (not reviewed or str(reviewed) < str(changed)):
        rep.err("B15", f"{rev.name}: review date {reviewed!r} precedes the shard's last change {changed!r}")


def policy_snapshot(ctx: Ctx, sha: str) -> Policy | None:
    p = ctx.snapshot_dir / f"{sha}.json"
    return load_policy(p) if p.is_file() else None


def write_policy_snapshot(root: Path, policy_path: Path) -> Path:
    pol = load_policy(policy_path)
    d = root / "internal/sanskrit_reviews/gita/policy-snapshots"
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"{pol.sha256}.json"
    if not out.exists():
        shutil.copyfile(policy_path, out)
    return out


def changed_rows(old: Policy, new: Policy) -> list[str]:
    keys = set(old.rows) | set(new.rows)
    out = sorted(k for k in keys if (old.rows.get(k).raw if k in old.rows else None) != (new.rows.get(k).raw if k in new.rows else None))
    if old.reserved != new.reserved:
        out.append("(reserved_english)")
    return out


def check_shard_policy(ctx: Ctx, sp: Path, sh: dict) -> None:
    rep, pol = ctx.report, ctx.policy
    got = sh.get("policy_sha256")
    if got == pol.sha256:
        return
    if not got:
        rep.err("B1", f"{sp.name}: no policy_sha256 (the shard must record the content hash of the policy it was produced under; current {pol.sha256[:12]})")
        return
    old = policy_snapshot(ctx, got)
    if old is None:
        rep.err("B1", f"{sp.name}: produced under policy {got[:12]}, current is {pol.sha256[:12]}; no snapshot of {got[:12]} to list the changed rows")
        return
    rows = changed_rows(old, pol)
    occ = [f"{v.get('locus')}[{i}]" for v in sh.get("verses") or [] for i, w in enumerate(v.get("words") or []) if own_lemmas(w) & set(rows)]
    rep.err("B1", f"{sp.name}: policy changed since production ({got[:12]} → {pol.sha256[:12]}); rows changed: {rows}; affected occurrences: {occ or 'none'}")


def translator_names(packet: dict, shards: list[dict]) -> list[str]:
    names = set(TRANSLATORS)
    for v in packet.get("verses") or []:
        for s in v.get("secondaries_english") or []:
            a = re.sub(r"^(?:Swami|Sri|Śrī|Shri|Dr\.?|Prof\.?)\s+", "", (s.get("author") or "").strip())
            if a:
                names.add(a.split()[-1])
    for sh in shards:
        for v in sh.get("verses") or []:
            for s in v.get("secondaries_consulted") or []:
                if isinstance(s, str) and re.fullmatch(r"[A-Z][A-Za-z\-]{3,}", s):
                    names.add(s)
    return sorted(names)


# ---- B8 across published readers (B16 discovery)
def discover_readers(root: Path) -> list[Path]:
    return sorted(root.glob("gita/*/verses.js"))


def load_reader(path: Path) -> list[dict]:
    """Evaluate a verses.js with node and return its *_VERSES array."""
    code = ("const fs=require('fs');const w={};new Function('window',fs.readFileSync(process.argv[1],'utf8'))(w);"
            "const k=Object.keys(w).find(k=>/_VERSES$/.test(k));process.stdout.write(JSON.stringify(k?w[k]:[]));")
    r = subprocess.run(["node", "-e", code, str(path)], capture_output=True, text=True)
    if r.returncode != 0:
        raise BuildError(f"cannot load {path}: {r.stderr[-300:]}")
    return json.loads(r.stdout or "[]")


def check_other_readers(ctx: Ctx) -> None:
    pol = ctx.policy
    if not pol.reserved:
        return
    legacy_hits = 0
    for p in discover_readers(ctx.root):
        if p.parent.name == f"ch{ctx.chapter}":
            continue
        try:
            verses = load_reader(p)
        except BuildError as e:
            ctx.report.warn("B16", str(e))
            continue
        policy_built = any(w.get("term") for v in verses for w in v.get("words") or [])
        for v in verses:
            smap = slot_map(v.get("english") or "")
            for w in v.get("words") or []:
                for ph in smap.get(w.get("i"), []):
                    for rw, owner in pol.reserved.items():
                        if word_re(rw).search(strip_quotations(ph).lower()) and owner not in own_lemmas(w):
                            if policy_built:
                                ctx.report.err("B8", f"{p.parent.name} {v.get('locus')}[{w.get('i')}]: reserved '{rw}' (for {owner}) printed for another lemma — \"{ph}\"")
                            else:
                                legacy_hits += 1
    if legacy_hits:
        ctx.report.warn("B8", f"{legacy_hits} reserved-English uses in legacy (pre-policy) readers; they are checked when migrated")


# ---- B10 render contract
RENDER_CONTRACT_JS = r"""
const fs = require("fs"), vm = require("vm"), path = require("path");
const input = JSON.parse(fs.readFileSync(0, "utf8"));
const stub = () => ({style:{}, setAttribute(){}, addEventListener(){}, getClientRects(){return [];}, matches(){return false;},
  contains(){return false;}, querySelectorAll(){return [];}, getBoundingClientRect(){return {width:300,height:300};}});
const context = {window:{scrollX:0, scrollY:0, innerHeight:844}, document:{addEventListener(){}, documentElement:{clientWidth:390},
  body:{appendChild(){}}, querySelectorAll(){return [];}, getElementById(){return null;}, createElement: stub}};
const src = fs.readFileSync(input.gita_js, "utf8");
// Works with both reader generations: one exposes wordCardHtml(w); the other builds the
// card inside showCard(span, w) into the shared card element.
vm.runInNewContext(src.replace("window.GitaReader = {",
  "window.__contract = {renderVerse, wordCardHtml: (typeof wordCardHtml === 'function' ? wordCardHtml : null), " +
  "showCard: (typeof showCard === 'function' ? showCard : null), card: () => (typeof cardEl !== 'undefined' ? cardEl : null), " +
  "panel: (typeof meaningPanelHtml === 'function' ? meaningPanelHtml : null)}; " +
  "window.GitaReader = {"), context);
const c = context.window.__contract;
const span = Object.assign(stub(), {textContent: "", dataset: {}, closest(){return null;}, parentElement: null});
const out = {verse: "", cards: {}};
try { out.verse = c.renderVerse(input.verse, {}); } catch (e) { out.verse_error = String(e); }
for (const w of input.cards) {
  try {
    if (c.wordCardHtml) out.cards[w.i] = c.wordCardHtml(w);
    else { c.showCard(span, w); const el = c.card(); out.cards[w.i] = el ? (el.innerHTML || "") : ""; }
    // the card shows the first meaning lines and opens the rest in the reader's panel
    if (c.panel) out.cards[w.i] += " " + (c.panel(w) || "");
  } catch (e) { out.cards[w.i] = ""; out.card_error = String(e); }
}
process.stdout.write(JSON.stringify(out));
"""


def html_text(html: str) -> str:
    import html as H
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", html or ""))).strip()


def check_render_contract(ctx: Ctx, public: list[dict]) -> None:
    rep = ctx.report
    fork_verse = next((v for v in public for f in v.get("forks") or [] if f.get("open")), None)
    meaning_verse = next((v for v in public for w in v["words"] if w.get("meaning")), None)
    if not fork_verse and not meaning_verse and not any(v.get("forks") for v in public):
        return
    gita_js = ctx.root / "assets/gita.js"
    probes = []
    if fork_verse:
        f = next(f for f in fork_verse["forks"] if f.get("open"))
        probes.append((fork_verse, [w for w in fork_verse["words"] if w["i"] in (f.get("words") or [])], ("fork", f)))
    elif any(v.get("forks") for v in public):
        v = next(v for v in public if v.get("forks"))
        f = v["forks"][0]
        probes.append((v, [w for w in v["words"] if w["i"] in (f.get("words") or [])], ("fork", f)))
    if meaning_verse:
        w = next(w for w in meaning_verse["words"] if w.get("meaning"))
        probes.append((meaning_verse, [w], ("meaning", w)))
    for verse, cards, (kind, obj) in probes:
        r = subprocess.run(["node", "-e", RENDER_CONTRACT_JS], input=json.dumps({"gita_js": str(gita_js), "verse": verse, "cards": cards}),
                           capture_output=True, text=True)
        if r.returncode != 0:
            rep.err("B10", f"render contract could not run on assets/gita.js: {r.stderr.strip()[-200:]}")
            return
        out = json.loads(r.stdout)
        # the reader's API for attaching forks to cards is the UI owner's; the contract is
        # only that what the reader must show appears somewhere in the rendered verse or cards
        shown = " ".join([html_text(out.get("verse", ""))] + [html_text(v) for v in out.get("cards", {}).values()])
        if kind == "fork":
            disp = obj.get("display") or ""
            need = [disp] if disp else [c.get("reading", "") for c in obj.get("construals") or []]
            if not all(n and html_text(n) in shown for n in need):
                rep.err("B10", f"reader cannot show forks: {verse['locus']} fork '{obj.get('at')}' does not appear in the rendered verse or its cards")
        else:
            texts = [ln.get("text", "") for ln in obj["meaning"].get("lines") or [] if isinstance(ln, dict)]
            if not texts or not all(t and html_text(t) in shown for t in texts):
                rep.err("B10", f"reader cannot show meaning: {verse['locus']}[{obj['i']}] meaning lines do not appear in the rendered card")


# ---- the run
def load_shards(ctx: Ctx) -> list[tuple[Path, dict]]:
    out = []
    for sp in sorted(ctx.chapter_dir.glob("producer-*.json")):
        try:
            out.append((sp, json.loads(sp.read_text(encoding="utf-8"))))
        except json.JSONDecodeError as e:
            ctx.report.err("SHARD", f"{sp.name}: invalid JSON ({e})")
    return out


def run(ctx: Ctx) -> dict:
    """Run every check. Returns the build result; ctx.report holds the violations."""
    rep, ch = ctx.report, ctx.chapter
    packet = json.loads((ctx.chapter_dir / "packet.json").read_text(encoding="utf-8"))
    by_locus = {v["locus"]: v for v in packet["verses"]}
    n = packet["verse_count"]
    shards = load_shards(ctx)
    if not shards:
        raise BuildError("no producer shards")
    covered: dict[str, str] = {}
    verses_in: list[dict] = []
    shard_of: dict[str, str] = {}
    for sp, sh in shards:
        rep.scope = sp.name
        if sh.get("schema_version") != PRODUCER_SCHEMA:
            rep.err("B12", f"{sp.name}: schema_version must be {PRODUCER_SCHEMA} (got {sh.get('schema_version')!r})")
        check_shard_policy(ctx, sp, sh)
        rev = ctx.chapter_dir / sp.name.replace("producer-", "independent-review-")
        if rev.exists():
            check_review(ctx, sp, rev)
        elif ctx.complete:
            rep.err("REVIEW", f"{sp.name}: no independent review file {rev.name}")
        for v in sh.get("verses", []):
            loc = v.get("locus")
            if loc in covered:
                rep.err("SHARD", f"{loc} produced twice ({covered[loc]}, {sp.name})")
            covered[loc] = sp.name
            shard_of[loc] = sp.name
            if loc not in by_locus:
                rep.err("SHARD", f"{sp.name}: unknown locus {loc}")
                continue
            verses_in.append(v)
    rep.scope = "chapter"
    missing = [f"{ch}.{i}" for i in range(1, n + 1) if f"{ch}.{i}" not in covered]
    if missing:
        rep.err("SHARD", f"verses not produced: {missing}")
    verses_in.sort(key=lambda v: int(v["locus"].split(".")[1]))
    translators = translator_names(packet, [sh for _, sh in shards])
    public, apparatus, total_fb, define_cache = [], [], 0, {}
    for v in verses_in:
        rep.scope = shard_of.get(v["locus"], "chapter")
        pub, app_, fb = check_verse(ctx, v, by_locus[v["locus"]], translators, define_cache)
        public.append(pub)
        apparatus.append(app_)
        total_fb += fb
    rep.scope = "chapter"
    check_other_readers(ctx)
    if ctx.run_render_contract:
        check_render_contract(ctx, public)
    return {"packet": packet, "public": public, "apparatus": apparatus, "fallbacks": total_fb, "verse_count": n}


# ---------------------------------------------------------------- outputs
def render_verses_js(ch: int, verses: list[dict], policy: Policy) -> str:
    head = f"""/* =============================================================
   Bhagavad-Gītā {ch} — the adhyāya entire, verses 1–{len(verses)}.
   window.CH{ch}_VERSES — one object per verse. GENERATED by
   scripts/build_gita_chapter_reader.py from the reviewed producer shards
   — do not edit by hand.
   Schema: docs/SANSKRIT_TRANSLATION_STANDARD.md and docs/GITA_CARD_MEANING_SCHEMA.md;
   term policy data/glossary/term_policy.json (content sha256 {policy.sha256[:12]}).
   Mūla: data/sources/sanskrit/vedanta/bhagavadgita_mula_bori.txt (BORI critical
   edition); Devanāgarī is a labelled deterministic transliteration of that IAST,
   collated against two Devanāgarī witnesses.
   Root text only — no commentary layer.
   ============================================================= */

window.CH{ch}_VERSES = """
    return head + json.dumps(verses, ensure_ascii=False, indent=2) + ";\n"


def render_index_html(root: Path, ch: int, n: int, has_audio: bool) -> str:
    tmpl = (root / "gita/ch5/index.html").read_text(encoding="utf-8")
    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"][ch - 1]
    out = tmpl.replace("gita-ch5", f"gita-ch{ch}").replace("CH5_VERSES", f"CH{ch}_VERSES")
    out = out.replace("Bhagavad-Gītā 5", f"Bhagavad-Gītā {ch}").replace("adhyāya V", f"adhyāya {roman}")
    out = out.replace("verses 1–29", f"verses 1–{n}")
    if has_audio:
        out = out.replace('<script src="verses.js"></script>', '<script src="verses.js"></script>\n  <script src="audio.js"></script>')
        out = out.replace("audio: null,", f"audio: window.CH{ch}_AUDIO,")
    return out


def reader_files(root: Path, ch: int) -> list[str]:
    s = (root / "assets/app.js").read_text(encoding="utf-8")
    m = re.search(rf'  "gita-ch{ch}": \{{.*?files:\s*\[([^\]]*)\]', s, re.S)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []


def register(root: Path, ch: int, n: int, has_audio: bool) -> None:
    app = root / "assets/app.js"
    s = app.read_text(encoding="utf-8")
    key = f'"gita-ch{ch}": {{'
    files = '["verses.js", "audio.js"]' if has_audio else '["verses.js"]'
    block = f'''  "gita-ch{ch}": {{
    base: "gita/ch{ch}/",
    files: {files},
    title: "Bhagavad-Gītā {ch}",
    blurb: "The adhyāya entire — the root text, word by word{', with recitation' if has_audio else ''}.",
    data: () => ({{
      verses: window.CH{ch}_VERSES, commentary: null,
      aurobindo: null, parallels: null, audio: {f'window.CH{ch}_AUDIO || null' if has_audio else 'null'},
    }}),
  }},
'''
    if key in s:
        s = re.sub(rf'  "gita-ch{ch}": \{{.*?\n  \}},\n', lambda _: block, s, count=1, flags=re.S)
    else:
        anchor = '  "yogavasistha-dama": {'
        if anchor not in s:
            raise BuildError("app.js GITA_READINGS anchor not found")
        s = s.replace(anchor, block + anchor, 1)
    app.write_text(s, encoding="utf-8")
    man_p = root / "data/articles/manifest.json"
    man = json.loads(man_p.read_text(encoding="utf-8"))
    arts = man["articles"] if isinstance(man, dict) and "articles" in man else man
    entry = {"slug": f"gita-ch{ch}", "title": f"Bhagavad-Gītā {ch}",
             "subtitle": f"The whole adhyāya, all {n} verses: the BORI root text word by word, with full Pāṇinian grammar cited to its sources, a literal rendering under one sense-constant term policy, and the places where more than one construal is admissible shown as such. Every Sanskrit word tappable{'; verse-synced recitation' if has_audio else ''}. Root text only — no commentary layer.",
             "kind": "reading", "interactive": f"gita-ch{ch}", "date": "2026-11-08", "status": "provisional"}
    idx = next((i for i, a in enumerate(arts) if a.get("slug") == f"gita-ch{ch}"), None)
    if idx is None:
        pos = next((i for i, a in enumerate(arts) if a.get("slug") == "gita-ch5"), len(arts) - 1) + 1
        arts.insert(pos, entry)
    else:
        entry["status"] = arts[idx].get("status", "provisional")
        arts[idx] = entry
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def public_apparatus(apparatus: list[dict]) -> list[dict]:
    """Apparatus fit for publication: no deviation defences, no candidate offered by
    a secondary translation, fork evidence only where it is a file locus (B13)."""
    out = []
    for a in apparatus:
        a = {k: v for k, v in a.items() if k != "_private_deviations"}
        words = []
        for w in a["words"]:
            w = dict(w)
            wd = w.get("wording")
            if wd:
                wd = dict(wd)
                wd["candidates"] = [c for c in wd.get("candidates") or []
                                    if DICTIONARY_SOURCES.search(f"{c.get('source', '')} {c.get('locus', '')}")]
                w["wording"] = wd
            words.append(w)
        a["words"] = words
        forks = []
        for f in a.get("forks") or []:
            f = json.loads(json.dumps(f))
            for c in f.get("construals") or []:
                c["evidence"] = [e for e in c.get("evidence") or [] if isinstance(e, str) and parse_locus(e)]
            forks.append(f)
        a["forks"] = forks
        a.pop("secondaries_consulted", None)
        out.append(a)
    return out


def owner_queue(ctx: Ctx, public: list[dict]) -> dict:
    """B14: every policy sense used in the chapter, with its rendering per occurrence;
    senses not owner-decided first; senses changed since their decision flagged."""
    pol = ctx.policy
    uses: dict[tuple[str, str], list[dict]] = {}
    for v in public:
        smap = slot_map(v["english"])
        for w in v["words"]:
            for t in [w.get("term")] + list(w.get("terms") or []):
                if t and pol.sense(t.get("lemma"), t.get("sense")):
                    uses.setdefault((t["lemma"], t["sense"]), []).append(
                        {"at": f"{v['locus']}[{w['i']}]", "iast": w.get("iast"), "rendering": " … ".join(smap.get(w["i"], [])) or None})
    rows = []
    for (lemma, sname), occ in uses.items():
        s = pol.sense(lemma, sname)
        flag = None
        d = s.decided or {}
        if d.get("row_sha256"):
            cur = hashlib.sha256(json.dumps(pol.rows[lemma].raw, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
            flag = "changed since decision" if cur != d["row_sha256"] else None
        elif d.get("policy_sha256") and d["policy_sha256"] != pol.sha256:
            old = policy_snapshot(ctx, d["policy_sha256"])
            if old is None:
                flag = "decision snapshot missing; cannot tell whether the row changed"
            elif lemma in changed_rows(old, pol):
                flag = "changed since decision"
        rows.append({"lemma": lemma, "sense": sname, "policy": s.policy, "status": s.status or "unrecorded", "changed_flag": flag,
                     "fixed": s.iast if s.policy == "preserve" else (s.forms or s.english), "occurrences": occ})
    rank = {"proposed": 0, "unrecorded": 1, "pilot": 2, "lexicon-reviewed": 2, "owner-decided": 3}
    rows.sort(key=lambda r: (rank.get(r["status"], 0), r["changed_flag"] is None, r["lemma"], r["sense"]))
    return {"chapter": ctx.chapter, "policy_sha256": pol.sha256,
            "instructions": "Read each verse's English line; tap any word on the site for its card. Decide the rows listed first (not owner-decided, or changed since the decision), each shown with its rendering at every occurrence.",
            "rows": rows,
            "verses": [{"locus": v["locus"], "english": v["english"], "sense": v["sense"],
                        "forks_open": [f["at"] for f in v["forks"] if f.get("open")]} for v in public]}


def write_outputs(ctx: Ctx, result: dict) -> list[str]:
    ch, root = ctx.chapter, ctx.root
    public, apparatus, n = result["public"], result["apparatus"], result["verse_count"]
    out = root / f"gita/ch{ch}"
    out.mkdir(parents=True, exist_ok=True)
    audio_js = out / "audio.js"
    has_audio = audio_js.exists()
    if has_audio:
        s = audio_js.read_text(encoding="utf-8")
        if f"window.CH{ch}_AUDIO" not in s:
            audio_js.write_text(re.sub(r"window\.\w+_AUDIO\s*=", f"window.CH{ch}_AUDIO =", s, count=1), encoding="utf-8")
    written = []
    (out / "verses.js").write_text(render_verses_js(ch, public, ctx.policy), encoding="utf-8")
    written.append(f"gita/ch{ch}/verses.js")
    deviations = {a["locus"]: a.get("_private_deviations") for a in apparatus}
    (ctx.chapter_dir / "deviations.json").write_text(json.dumps({"chapter": ch, "verses": deviations}, ensure_ascii=False, indent=1), encoding="utf-8")
    private_app = {"chapter": ch, "policy_sha256": ctx.policy.sha256, "verses": [{k: v for k, v in a.items() if k != "_private_deviations"} for a in apparatus]}
    (ctx.chapter_dir / "apparatus.json").write_text(json.dumps(private_app, ensure_ascii=False, indent=1), encoding="utf-8")
    pub_app = out / "apparatus.json"
    if "apparatus.json" in reader_files(root, ch):
        pub_app.write_text(json.dumps({"chapter": ch, "policy_sha256": ctx.policy.sha256, "verses": public_apparatus(apparatus)},
                                      ensure_ascii=False, indent=1), encoding="utf-8")
        written.append(f"gita/ch{ch}/apparatus.json")
    elif pub_app.exists():
        pub_app.unlink()                     # B13: the reader does not load it, so it is not published
        written.append(f"(removed unpublished gita/ch{ch}/apparatus.json)")
    (out / "index.html").write_text(render_index_html(root, ch, n, has_audio), encoding="utf-8")
    written.append(f"gita/ch{ch}/index.html")
    register(root, ch, n, has_audio)
    (ctx.chapter_dir / "owner-review-queue.json").write_text(json.dumps(owner_queue(ctx, public), ensure_ascii=False, indent=1), encoding="utf-8")
    write_policy_snapshot(root, ctx.policy_path)
    return written


def print_report(ctx: Ctx, result: dict | None) -> None:
    rep = ctx.report
    summary = {"chapter": ctx.chapter, "policy_sha256": ctx.policy.sha256, "policy_structure": ctx.policy.structure,
               "errors": len(rep.errors), "warnings": len(rep.warnings), "errors_by_check": rep.counts(),
               "errors_by_shard": rep.counts_by_scope()}
    if result:
        summary.update({"verses": len(result["public"]), "cards": sum(len(v["words"]) for v in result["public"]),
                        "fallbacks": result["fallbacks"], "forks": sum(len(v["forks"]) for v in result["public"])})
    print(json.dumps(summary, ensure_ascii=False))
    for c, w, _ in rep.warnings:
        print("WARN", c, w)
    for c, e, _ in rep.errors:
        print("ERROR", c, e)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", type=int, nargs="?")
    ap.add_argument("--allow-unreviewed", action="store_true", help="build without complete independent reviews (never for publication)")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--json-report", type=Path, help="write {errors_by_check, errors, warnings} as JSON")
    ap.add_argument("--register-only", action="store_true", help="apply the app.js + manifest registration under --root and write nothing else")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--policy-hash", action="store_true", help="print the content hash producers record as policy_sha256")
    ap.add_argument("--snapshot-policy", action="store_true", help="store the current policy under its hash so B1 can list changed rows later")
    a = ap.parse_args(argv)
    policy_path = a.root / "data/glossary/term_policy.json"
    if a.policy_hash:
        print(load_policy(policy_path).sha256)
        return 0
    if a.snapshot_policy:
        print(write_policy_snapshot(a.root, policy_path))
        return 0
    if a.chapter is None:
        ap.error("chapter required")
    ch = a.chapter
    if a.register_only:
        out = a.root / f"gita/ch{ch}"
        vjs = out / "verses.js"
        if not vjs.is_file():
            raise BuildError(f"{vjs} missing; copy the chapter files before registering")
        n = len(load_reader(vjs))
        register(a.root, ch, n, (out / "audio.js").exists())
        print(f"registered gita-ch{ch} ({n} verses) under {a.root}")
        return 0
    ctx = Ctx(chapter=ch, root=a.root, complete=not a.allow_unreviewed)
    result = None
    try:
        result = run(ctx)
    finally:
        print_report(ctx, result)
        if a.json_report:
            a.json_report.write_text(json.dumps({"errors_by_check": ctx.report.counts(), "errors_by_shard": ctx.report.counts_by_scope(),
                                                 "errors": ctx.report.errors,
                                                 "warnings": ctx.report.warnings}, ensure_ascii=False, indent=1), encoding="utf-8")
    if ctx.report.errors:
        print(f"REFUSED: {len(ctx.report.errors)} contract violations; nothing written.")
        return 1
    if a.check_only:
        return 0
    for w in write_outputs(ctx, result):
        print("written", w)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as e:
        print("ERROR", e)
        sys.exit(1)

#!/usr/bin/env python3
"""The owner's translation pipeline (scripts/gita/translate/README.md; design: docs/GITA_FULL_TRANSLATION_PLAN.md §3): the parse is given; one model call per
sentence decides the words in context and writes the line; code checks every mechanical rule; one
review; a chapter consistency pass.

    python3 scripts/gita/translate/pipeline.py translate   --run ch12-qual [--only 12.13] [--jobs 24]
    python3 scripts/gita/translate/pipeline.py consistency --run ch12-qual [ch15-heldout …]   (several runs: the book)
    python3 scripts/gita/translate/pipeline.py sheet       --run ch12-qual
"""
from __future__ import annotations

import argparse
import functools
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check  # noqa: E402
import compile as C  # noqa: E402

sys.path.insert(0, str(Path.home() / "Dev/prakriya/scripts/lookup"))

ROOT = HERE.parents[2]
PROMPTS = HERE / "prompts3"
RUNS = ROOT / "internal/gita_pipeline/run"
MAX_REVISIONS = 2
_LOOKUP = threading.Lock()  # the prakriya lookup layer (sqlite) is not thread-safe
_CALLS = threading.BoundedSemaphore(int(os.environ.get("GITA_MAX_CALLS", "32")))
TERM_POLICY = json.loads((ROOT / "data/glossary/term_policy.json").read_text(encoding="utf-8"))["terms"]
SEED_TERMS = json.loads((HERE / "seed_terms.json").read_text(encoding="utf-8"))["terms"]  # plan §6.1 seed defaults


# ---------------------------------------------------------------- prompts
CRAFT = ROOT / "docs/gita_briefs/ENGLISH_CRAFT.md"
STANDARD = ROOT / "docs/SANSKRIT_TRANSLATION_STANDARD.md"


def _between(text: str, start: str, end: str) -> str:
    a = text.index(start)
    return text[a:text.index(end, a)].strip()


def prompt(task: str) -> str:
    """A prompt file with the owner's documents inserted verbatim (never paraphrased)."""
    t = (PROMPTS / f"{task}.md").read_text(encoding="utf-8")
    if "{{" in t:
        craft, std = CRAFT.read_text(encoding="utf-8"), STANDARD.read_text(encoding="utf-8")
        t = (t.replace("{{CRAFT_PRINCIPLES}}", _between(craft, "**The five principles that matter most:**", "**The ten revised lines**"))
              .replace("{{CRAFT_STEPS}}", _between(craft, "### Step 3. Choose the kind of expression", "## 3. Calibration").rstrip("-").strip())
              .replace("{{STANDARD_7}}", _between(std, "### 7.1 Do not collapse meaning", "## 8. Preserve or translate"))
              .replace("{{STANDARD_8}}", _between(std, "### 8.1 The rule: three tests", "### 8.2 Disputed referents")
                       + "\n\n" + _between(std, "### 8.5 The decision procedure", "## 9. Other translations")))
    return t


SLOT = re.compile(r"\{[\d,\s]+:([^{}]*)\}")


def strip_slots(d):
    """The craft brief writes slots as {i:text}; lines are plain English (the slot map is `words`)."""
    if isinstance(d, dict):
        return {k: (v if k == "slotted" else strip_slots(v)) for k, v in d.items()}
    if isinstance(d, list):
        return [strip_slots(x) for x in d]
    if isinstance(d, str):
        return SLOT.sub(r"\1", d)
    return d


# ---------------------------------------------------------------- model call
def call(task: str, card: dict, extra: str = "") -> tuple[dict | None, dict]:
    """One tool-free model call through runner.py (Codex or Claude): prompt + card inline -> (parsed JSON
    or None, stats). One retry when the answer is not JSON."""
    import runner
    text = prompt(task) + extra + "\n\nCARD:\n" + json.dumps(card, ensure_ascii=False, indent=1)
    for attempt in (1, 2):
        with _CALLS:
            r = runner.run(text, RUNS, sandbox="read-only")
        stats = {"task": task, "s": r.seconds, "attempt": attempt, "runner": runner.RUNNER, "model": runner.model_name(),
                 "effort": runner.EFFORT, "card_bytes": len(json.dumps(card, ensure_ascii=False).encode()),
                 "commands": r.commands, "output_tokens": r.usage.get("output_tokens", 0),
                 "input_tokens": r.usage.get("input_tokens", 0)}
        if r.usage.get("error"):
            stats["error"] = r.usage["error"]
        m = re.search(r"\{.*\}", r.raw, re.S)
        try:
            if m:
                return strip_slots(json.loads(m.group(0))), stats
        except json.JSONDecodeError:
            pass
    return None, stats


# ---------------------------------------------------------------- term decisions
def fold(s: str) -> str:
    """Lowercase without diacritics: kūṭastha -> kutastha."""
    return "".join(c for c in unicodedata.normalize("NFD", (s or "").lower()) if unicodedata.category(c) != "Mn")


def term_rows(lemma: str) -> list[dict]:
    """The owner's standing decisions for a lemma (term_policy.json); where the owner's table has none,
    the plan's seed decisions (§4), marked seed: binding unless the translator records a challenge."""
    return _rows(lemma, TERM_POLICY) or [dict(r, seed=True) for r in _rows(lemma, SEED_TERMS)]


def _rows(lemma: str, table: dict) -> list[dict]:
    """Rows whose iast_forms name the lemma or whose pattern matches it. A preserve row applies only to
    the forms it names (or their inflections)."""
    out = []
    for key, row in table.items():
        senses = row.get("senses") or {}
        named = any(lemma in (s.get("iast_forms") or []) for s in senses.values())
        if not (named or re.search(row.get("match") or "^$", lemma)):
            continue
        for sid, s in senses.items():
            forms = s.get("iast_forms") or ([s["iast"]] if s.get("iast") else [])
            if s.get("policy") == "preserve" and forms and lemma not in forms and not any(lemma.startswith(f[:-1]) for f in forms):
                continue
            out.append({"term": f"{key}.{sid}", "policy": s.get("policy"), "english": list(s.get("english") or []),
                        "keep": (lemma if lemma in forms else s.get("iast")) if s.get("policy") == "preserve" else None,
                        "forbidden": list(s.get("forbidden_english") or []), "note": (s.get("note") or "")[:300]})
    return out


# ---------------------------------------------------------------- English forms
_SUFFIX = re.compile(r"(ments?|ings?|ers?|ions?|ness|edly|ed|es|s|ly)$")
EN_FUNCTION = set(check.FUNCTION_WORDS) | {"the", "a", "an", "of", "to", "in", "on", "by", "with", "from", "who", "which",
                                           "that", "for", "it", "he", "its", "their", "there",
                                           # auxiliaries: grammar, not content
                                           "am", "is", "are", "was", "were", "be", "been", "being", "do", "does", "did",
                                           "have", "has", "had", "will", "would", "shall", "should", "may", "might",
                                           "can", "could", "must"}


@functools.lru_cache(maxsize=65536)
def en_stem(w: str) -> str:
    """The English word's lemma (irregular forms included: gone/went -> go, men -> man), then its
    derivational stem (relinquishment ~ relinquish)."""
    w = w.lower().strip("’'‘“”\"")
    try:
        from lemminflect import getAllLemmas
        ls = getAllLemmas(w)
        if ls:
            w = sorted({x for v in ls.values() for x in v}, key=len)[0]
    except ImportError:
        pass
    r = _SUFFIX.sub("", w)
    return r if len(r) >= 3 else w


def tokens(text: str) -> list[str]:
    """Lower-cased word tokens; a possessive ending (Veda's, Vedas’) is not part of the word."""
    out = []
    for t in re.findall(r"[\wāīūṛṝḷṅñṭḍṇśṣḥṃ’'-]+", (text or "").lower()):
        t = re.sub(r"[’']s?$", "", t)
        if t:
            out.append(t)
    return out


def renders(text: str, option: str) -> bool:
    """`text` contains `option` in some English form of the same words (relinquish ~ relinquishment)."""
    toks = {en_stem(x) for t in tokens(text) for x in [t, *t.split("-")]}
    need = [en_stem(t) for t in tokens(option) if t not in EN_FUNCTION]
    if not need:
        return bool(option) and option.lower() in (text or "").lower()

    def hit(n):
        return any(t == n or (min(len(t), len(n)) >= 5 and (t.startswith(n) or n.startswith(t))) for t in toks)
    return all(hit(n) for n in need)


def keeps(text: str, iast: str) -> bool:
    """The Sanskrit term is kept in the English (inflected the English way: bhaktas, yogins)."""
    k = fold(iast)
    return any(fold(t).startswith(k[:-1] if len(k) > 3 else k) for t in tokens(text))


# ---------------------------------------------------------------- card
def lemma_map(cons: list[dict]) -> tuple[dict, dict]:
    """(locus, i) -> {word: lemma, members: [lemma]}; lemma -> evidence entry. Same normalisation as
    the evidence layer (pari-upa-ās -> paryupās)."""
    import evidence
    ents = evidence.lemmas_from_construals(cons)
    pos: dict = {}
    for stem, e in ents.items():
        member = "member" in (e.get("kinds") or [])
        for p in e["places"]:
            d = pos.setdefault((p["locus"], p["i"]), {"word": None, "members": []})
            (d["members"].append(stem) if member else d.__setitem__("word", stem))
    return pos, ents


_ROOTS_CACHE: dict = {}


def root_words(root: str | None) -> list[dict]:
    """English words sharing the Sanskrit root through PIE, or whose etymon pictures it (≤6)."""
    if not root:
        return []
    if root not in _ROOTS_CACHE:
        import english_roots as er
        with _LOOKUP:
            rows = list(er.by_sanskrit(root, limit=6))
        _ROOTS_CACHE[root] = [{"word": r["word"], "modern": (r.get("modern") or "")[:80], "link": (r.get("link") or "")[:60]}
                              for r in rows]
    return _ROOTS_CACHE[root]


def sanskrit_at(entry: dict | None, locus: str, word: dict) -> dict:
    """The M1–M5 Sanskrit card for one word at one place (sanskrit_card.py), with its coverage audit."""
    if not entry:
        return {}
    import sanskrit_card as S
    with _LOOKUP:
        card = S.word_card(entry, locus, word)
        errs = S.audit(entry, card)
    if errs:
        card["coverage_errors"] = errs
    return card


def member_at(entry: dict | None) -> dict:
    if not entry:
        return {}
    import sanskrit_card as S
    with _LOOKUP:
        return S.member_card(entry)


_DEF: dict = {}
MODERN_FIRST = {"oewn2025": 0, "wiktionary": 1, "webster1913": 2, "gcide": 3}


def define(word: str) -> dict:
    """The word's own entries in the English dictionaries (modern sources first), compact."""
    w = word.strip().lower()
    if w not in _DEF:
        import lookup
        with _LOOKUP:
            r = lookup.english_define_report(w, limit=10)
        ents = [e for g in r.get("groups", []) for e in g.get("entries", [])]
        ents.sort(key=lambda e: MODERN_FIRST.get(e.get("source"), 9))
        _DEF[w] = {"attested": bool(r.get("attested")),
                   "entries": [f"{e.get('source')} {e.get('pos') or ''}{' [' + e['tags'] + ']' if e.get('tags') else ''}: "
                               f"{re.sub(chr(10), ' ', e.get('definition') or '')[:120]}" for e in ents[:4]],
                   "loci": [e["locus"] for e in ents[:4] if e.get("locus")]}
    return _DEF[w]


def attested(text: str) -> bool:
    """Every content word of an English rendering is a real English word (or a form of one)."""
    toks = [t for t in tokens(text) if t not in EN_FUNCTION and not re.search(r"[āīūṛṝḷṅñṭḍṇśṣḥṃ]", t)]
    return all(define(x)["attested"] for t in toks for x in t.split("-") if x)


def candidates(sense: dict, root: str | None, limit: int = 12) -> list[dict]:
    """ENGLISH_CRAFT step 2: words found in the English dictionaries by the sense description and the
    root image first (semantic search, then keyword search), then words the translator remembered (≤4,
    checked the same way), then English words sharing the root (≤2); each defined. A failing tool raises:
    a run never silently translates without its English evidence (preflight() checks the tools)."""
    import english
    import english_bench as B
    q = sense.get("search") or ""  # the core meaning only: grammar words in a description pollute the search
    retrieved: list[tuple[str, str]] = []
    matched = {}
    for r in (B.find(q, k=6) if q else []):
        retrieved.append((r["word"], "found by meaning"))
        matched[r["word"].lower()] = r["definition"]
    if sense.get("image"):
        for r in B.find(sense["image"], k=3):
            retrieved.append((r["word"], "found by image"))
            matched.setdefault(r["word"].lower(), r["definition"])
    if q:
        with _LOOKUP:
            retrieved += [(r["word"], "retrieved: sense") for r in english.english_table(q, sense.get("image"), limit=4)]
    remembered = [(w, "remembered") for w in (sense.get("remembered") or [])[:4]]
    roots = [(r["word"], "root") for r in root_words(root)[:2]]  # last: PIE homonyms are noisy
    out, seen = [], set()
    quota = {"retrieved": limit - len(remembered) - len(roots), "remembered": 4, "root": 2}
    for group, items in (("retrieved", retrieved), ("remembered", remembered), ("root", roots)):
        n = 0
        for w, how in items:
            if w.lower() in seen or n >= quota[group]:
                continue
            d = define(w)
            if not d["attested"] and how != "remembered":
                continue
            seen.add(w.lower())
            n += 1
            item = {"word": w, "found_by": how, "attested": d["attested"] or attested(w),
                    "modern_first_sense": (d["entries"][:1] or [None])[0], "loci": d["loci"][:2]}
            if matched.get(w.lower()):
                item["matching_sense"] = matched[w.lower()][:140]
            elif len(d["entries"]) > 1:
                item["other_sense"] = d["entries"][1]
            pr = B.profile(w)
            item.update({k: pr[k] for k in ("zipf", "stress", "origin") if pr.get(k) not in (None, [], "")})
            out.append(item)
    multi = [c["word"] for c in out if " " in c["word"]]
    if multi:
        pf = B.phrase_freq(multi)
        for c in out:
            if c["word"] in pf and pf[c["word"]] is not None:
                c["books_per_billion"] = round(pf[c["word"]] * 1e9, 1)
    return out


def preflight(allow_partial: bool = False) -> dict:
    """Every English tool the run depends on, checked before the first model call: the semantic index
    (and how complete it is), the embedding server, LanguageTool, lemminflect. Missing tools abort the
    run unless `allow_partial`, and the state is recorded in the run summary."""
    state: dict = {}
    try:
        import english_bench as B
        state["index"] = B.index_state()
        B.embed_query("test")
        state["embedding_server"] = "ok"
    except Exception as e:
        state["embedding_server"] = f"FAILED: {e!r}"[:200]
    try:
        grammar("This is a test line.")
        state["languagetool"] = "ok"
    except Exception as e:
        state["languagetool"] = f"FAILED: {e!r}"[:200]
    try:
        import lemminflect  # noqa: F401
        state["lemminflect"] = "ok"
    except ImportError as e:
        state["lemminflect"] = f"FAILED: {e!r}"
    bad = [k for k, v in state.items() if isinstance(v, str) and v.startswith("FAILED")]
    if not (state.get("index") or {}).get("complete"):
        bad.append(f"index {state.get('index')}")
    state["missing"] = bad
    if bad and not allow_partial:
        raise SystemExit(f"preflight: English tools missing or incomplete: {bad} (run with --allow-partial-tools to "
                         "proceed and record it)")
    return state


SANSKRIT_ONLY = ("sanskrit", "member_sanskrit")
ENGLISH_KEYS = ("standing", "english_case")  # owner decisions and case hints in English: not on the Sanskrit-only card


def meaning_view(card: dict) -> dict:
    """The card for step 1 (the meaning call): Sanskrit only, so the owner's English decisions and case
    hints are removed; every word keeps its grammar and its M1–M5 Sanskrit card."""
    return {**card, "verses": [{**v, "words": [{k: x for k, x in w.items() if k not in ENGLISH_KEYS} for w in v["words"]]}
                               for v in card["verses"]]}


def translate_card(card: dict, senses: dict) -> dict:
    """The card for steps 3–6: grammar, the step-1 sense, the step-2 English candidates with their
    definitions, standing decisions. The Sanskrit evidence has done its work in step 1."""
    verses = []
    for v in card["verses"]:
        words = []
        for w in v["words"]:
            d = {k: x for k, x in w.items() if k not in SANSKRIT_ONLY}
            sn = senses.get((v["locus"], w["i"])) or {}
            for k in ("literal", "image", "readings"):
                if sn.get(k):
                    d[k] = sn[k]
            owner_rows = [r for r in w.get("standing") or [] if not r.get("seed")]
            if w.get("class") not in CLOSED and not owner_rows and sn:  # a seed row may be challenged: give candidates
                d["candidates"] = candidates(sn, (w.get("root") or "").split(" ")[0] or None)
            words.append(d)
        verses.append({**v, "words": words})
    return {**card, "verses": verses}


def sanskrit_summary(card: dict) -> dict:
    """For the reviewer: the root's Dhātupāṭha meaning, the affix meanings and the first entry of each
    lexical text (the evidence a rendering must answer to)."""
    m2, m3 = card.get("M2_morphemes") or {}, card.get("M3_lexical_texts") or {}
    out = {"root": m2.get("root"), "affixes": [f"{a['affix']}: " + "; ".join(f"{x['sutra']} {x['text']}" for x in a["sutras"])
                                              for a in m2.get("affixes") or [] if a["kind"] in ("kṛt", "taddhita", "sanādi")],
           "lexical": [f"{x['work']}: {x['text'][:160]}" for sec in ("koshas", "dictionaries") for x in (m3.get(sec) or [])[:2]]}
    return {k: v for k, v in out.items() if v}


TEXT_GROUNDS = re.compile(r"\b(DP|Dhātupāṭha|Mādhavīya|Kṣīrataraṅgiṇī|Dhātupradīpa|Daiva|Dhātuvṛtti|Amara\w*|Halāyudha|"
                          r"Vaijayantī|Yādava\w*|Ākhyātacandrikā|Nirukta|Nighaṇṭu|Śabdakalpadruma|Vācaspatya|SKD|VCP|"
                          r"Gītā|grammar|Aṣṭādhyāyī)\b|\b\d\.\d{1,2}\.\d{1,3}\b|\b\d{1,2}\.\d{1,2}[a-f]?\b", re.I)


def meaning_errors(m: dict | None, card: dict) -> list[str]:
    """Step 1 checked by code: every content word has a literal meaning and grounds; a literal grounded only
    in commentaries is an error when the texts (M2, M3) have an entry for the word."""
    if not m:
        return ["no answer"]
    got = {(w.get("locus"), w.get("i")): w for w in m.get("words") or []}
    errs = []
    for v in card["verses"]:
        for w in v["words"]:
            if w.get("class") not in ("content", "name") and not w.get("compound"):
                continue
            tag = f"{v['locus']} word {w['i']} ({w['form']})"
            a = got.get((v["locus"], w["i"]))
            if not a or not (a.get("literal") or "").strip():
                errs.append(f"{tag}: no literal meaning")
                continue
            if a["literal"].strip().lower() == "unresolved":
                continue
            grounds = a.get("grounds") or []
            texts = w.get("sanskrit") or {}
            has_text = any(x for x in (texts.get("M2_morphemes") or {}).values()) or any(
                x for x in (texts.get("M3_lexical_texts") or {}).values())
            if not grounds:
                errs.append(f"{tag}: no grounds for the literal meaning")
            elif has_text and not any(TEXT_GROUNDS.search(g) for g in grounds):
                errs.append(f"{tag}: the literal meaning is grounded only in commentaries ({grounds}), but the texts "
                            "(M2 morphemes, M3 lexical texts) have entries for this word: build it from them")
    return errs


def gram_of(locus: str, w: dict) -> str | None:
    if w.get("manual"):
        return (w["manual"] or {}).get("gram")
    for a in C.verse_packet(locus)["forms"].get(w["form"], {}).get("analyses", []):
        if a.get("id") == w.get("analysis_id"):
            return a.get("gram")
    return None


RELEASE = ("mukta", "vimukta", "vinirmukta", "rahita", "hīna", "vihīna", "varjita", "vivarjita", "viyukta", "apeta", "vigata", "śūnya")
COMPARE = ("śreyas", "viśiṣ", "adhika", "garīyas", "jyāyas", "tara")
THINK_KTA = ("mata", "iṣṭa", "jñāta", "vidita", "pūjita", "sammata", "abhimata")
ABLE = ("samartha", "śakta", "kuśala", "kṣama")
CASES = ("prathamā", "dvitīyā", "tṛtīyā", "caturthī", "pañcamī", "ṣaṣṭhī", "saptamī")


def case_rule(grammar: str | None, head: str | None) -> str | None:
    """Pāṇinian case uses whose English preposition differs from the default, decided by the head word:
    instrumental/ablative with words of release ('freed from'), ablative of comparison ('than'),
    genitive agent of a past participle of thinking ('deemed by'), locative of an ability ('capable of')."""
    g, h = (grammar or "").split(";")[0], head or ""
    case = next((c for c in CASES if c in g), None)
    if case in ("tṛtīyā", "pañcamī") and any(h.endswith(r) for r in RELEASE):
        return "'from' (separation with a word of release or lack: 'freed from', 'devoid of')"
    if case == "pañcamī" and any(r in h for r in COMPARE):
        return "'than' / 'above' (comparison)"
    if case == "ṣaṣṭhī" and any(h.endswith(x) for x in THINK_KTA):
        return "'by' (agent of a past participle of thinking: 'deemed by me')"
    if case == "saptamī" and any(h.endswith(x) for x in ABLE):
        return "'of' / 'at' (sphere of an ability: 'capable of')"
    if case == "ṣaṣṭhī" and h.startswith("priy"):
        return "'to' ('dear to me')"
    return None


def unit_card(unit: list[str], cons: dict, pos: dict, ents: dict, fixed: dict | None = None) -> dict:
    fixed = fixed or {}
    verses = []
    for loc in unit:
        c = cons[loc]
        forms = {x["i"]: x["form"] for x in c["words"]}
        words = []
        for w in c["words"]:
            p = pos.get((loc, w["i"]), {"word": None, "members": []})
            lemma = p["word"] or w.get("stem")
            rel = w.get("relation") or {}
            head_lemma = (pos.get((loc, rel.get("head")), {}).get("word") or next((x.get("stem") for x in c["words"] if x["i"] == rel.get("head")), None)) \
                if isinstance(rel.get("head"), int) else None
            d = {"i": w["i"], "form": w["form"], "lemma": lemma, "class": w.get("word_class"), "analysis_id": w.get("analysis_id"),
                 "root": w.get("root"), "upasargas": w.get("upasargas") or None, "grammar": gram_of(loc, w),
                 "depends_on": forms.get(rel.get("head")) if isinstance(rel.get("head"), int) else rel.get("head"),
                 "relation": rel.get("role")}
            rule = case_rule(d["grammar"], head_lemma)
            if rule:
                d["english_case"] = rule
            sandhi = (w.get("manual") or {}).get("padas") or (w.get("manual") or {}).get("parts")
            if w.get("compound") or sandhi:
                comp = w.get("compound") or {}
                parts = sandhi or w.get("members") or []
                d["compound"] = {"type": comp.get("type") or "two words joined by sandhi", "analysis": comp.get("vigraha"),
                                 "members": [{"stem": m.get("stem"), "class": m.get("word_class"), "grammar": m.get("gram"),
                                              "morphemes": max(1, len(m.get("members") or [])) + len(m.get("upasargas") or [])}
                                             for m in parts]}
            if w.get("word_class") in ("content", "name") or d.get("compound"):
                ev = sanskrit_at(ents.get(lemma), loc, w)
                if ev:
                    d["sanskrit"] = ev
                if d.get("compound"):
                    d["member_sanskrit"] = {m: member_at(ents.get(m)) for m in p["members"]}
            rows = term_rows(lemma or "") + [dict(r, member=m) for m in p["members"] for r in term_rows(m)]
            if rows:
                d["standing"] = rows
            if fixed.get((lemma, loc)):
                d["FIXED"] = fixed[(lemma, loc)]
            for m in (d.get("compound") or {}).get("members") or []:
                f = fixed.get(((m.get("stem") or "").strip("-"), loc))
                if f:
                    m["FIXED"] = f
            words.append(d)
        verses.append({"locus": loc, "iast": C.verse_packet(loc)["iast"], "words": words,
                       "referents": c.get("referents", []),
                       "forks": [f for f in c.get("forks", []) if f.get("kind") in check.GRAMMATICAL_FORKS]})
    return {"unit": unit, "verses": verses}


def admits(row: dict, text: str) -> bool:
    return (row["policy"] == "preserve" and keeps(text, row.get("keep") or "")) or \
           (row["policy"] == "translate" and any(renders(text, e) for e in row.get("english") or []))


def term_errors(tag: str, text: str, parts: list[dict], rows: list[dict], challenge: str | None = None) -> list[str]:
    """A lemma's rows are its senses: the rendering must be admitted by one of them (the translator
    picks the sense); a forbidden word is an error only when no row admits the rendering."""
    errs = []
    groups: dict = {}
    for r in rows:
        groups.setdefault(r.get("member"), []).append(r)
    for member, rs in groups.items():
        if member:
            part = next((m for m in parts if m.get("stem") == member), None)
            sub = (part or {}).get("english")
            if sub is None:
                continue  # a missing part is reported by the compound check
        else:
            sub = text
        if any(admits(r, sub) for r in rs):
            continue
        if all(r.get("seed") for r in rs) and challenge:
            continue  # a plan seed may be challenged with a reason; the challenge goes to the owner's sheet
        bad = sorted({f for r in rs for f in r.get("forbidden") or [] if renders(sub, f)})
        want = "; ".join(f"{r['term']}: " + (f"keep {r['keep']}" if r["policy"] == "preserve" else " / ".join(r["english"])) for r in rs)
        errs.append(f"{tag}: '{sub}'{' (member ' + member + ')' if member else ''} follows none of the owner's decisions "
                    f"[{want}]" + (f"; forbidden: {', '.join(bad)}" if bad else ""))
    return errs


# ---------------------------------------------------------------- checks
def check_unit(out: dict, card: dict) -> list[str]:
    """Every mechanical rule of the owner's standard (README.md, "Code checks")."""
    if not out:
        return ["no answer"]
    inp = {"verses": [{"locus": v["locus"], "construal": {"forks": v["forks"], "words": [
        {"i": w["i"], "form": w["form"], "word_class": w["class"]} for w in v["words"]]}} for v in card["verses"]]}
    errs = [e for e in check.verse({**out, "words": [{**w, "sense_id": None, "lost": None} for w in out.get("words", [])]}, inp, {})
            if "W6" not in e and "L0" not in e]
    used = {t for w in out.get("words", []) for t in check.words_of(w.get("english"))}
    for loc, line in (out.get("lines") or {}).items():
        extra = sorted({t for t in check.words_of(line) if t not in check.FUNCTION_WORDS and t not in used})
        if extra:  # repetition of a word's own rendering (English ellipsis) is allowed; a new word is not
            errs.append(f"{loc}: line words not assigned to any Sanskrit word: {extra} (add nothing)")
    cw = {(v["locus"], w["i"]): w for v in card["verses"] for w in v["words"]}
    for w in out.get("words", []):
        c = cw.get((w.get("locus"), w.get("i")))
        if not c:
            continue
        text, tag = w.get("english") or "", f"{w.get('locus')} word {w.get('i')} ({c['form']})"
        morphemes = (sum(m.get("morphemes") or 1 for m in (c.get("compound") or {}).get("members") or []) or 1) \
            + len(c.get("upasargas") or [])
        content = [t for t in tokens(text) if t not in EN_FUNCTION]
        if len(content) > morphemes + 2:
            errs.append(f"{tag}: '{text}' has {len(content)} content words for {morphemes} Sanskrit morpheme(s) — "
                        "an explanation, not a rendering (add nothing)")
        if c.get("compound"):
            parts = w.get("parts") or []
            stems = {(m.get("stem") or "") for m in parts}
            for m in c["compound"]["members"]:
                if m.get("class") in ("particle",) or not m.get("stem"):
                    continue
                if m["stem"] not in stems:
                    errs.append(f"{tag}: compound member {m['stem']} has no entry in parts")
            for m in parts:
                if m.get("english") and not renders(text, m["english"]) and not keeps(text, m["english"]):
                    errs.append(f"{tag}: member {m.get('stem')} is given as '{m['english']}' but that is not in '{text}'")
            for m in c["compound"]["members"]:
                part = next((x for x in parts if x.get("stem") == m.get("stem")), None)
                if m.get("FIXED") and part and not (same(part.get("english") or "", m["FIXED"]) or renders(part.get("english") or "", m["FIXED"])):
                    errs.append(f"{tag}: member {m['stem']}'s fixed rendering in this chapter is '{m['FIXED']}'")
        errs += term_errors(tag, text, w.get("parts") or [], c.get("standing") or [], (w.get("challenge") or "").strip() or None)
        errs += trace_errors(tag, text, c, w)
        kind = w.get("kind")
        if kind == "e" and not keeps(text, c.get("lemma") or c["form"]):
            errs.append(f"{tag}: kind e keeps the Sanskrit, but '{text}' is not the word {c.get('lemma')}")
        if kind != "e" and not c.get("standing") and not attested(text):
            errs.append(f"{tag}: '{text}' contains a word the English dictionaries do not have (step 3: real English words only)")
        if kind == "d" and len(w.get("models") or []) < 2:
            errs.append(f"{tag}: formation '{text}' needs two attested models of its pattern (step 3d.2)")
        if c.get("FIXED") and not (renders(text, c["FIXED"]) or keeps(text, c["FIXED"])):
            errs.append(f"{tag}: the chapter's fixed rendering is '{c['FIXED']}'")
        if w.get("carried") is False and kind in ("a", "b", "c") and not (w.get("why") or "").strip():
            errs.append(f"{tag}: '{text}' loses {w.get('lost')!r}; by the owner's order use a formation (kind d) or keep "
                        "the Sanskrit (kind e), or say in 'why' why neither serves")
        if w.get("carried") is False and not (w.get("lost") or "").strip():
            errs.append(f"{tag}: carried is false but 'lost' does not say what is not carried")
        if w.get("found_by") == "remembered" and c.get("class") not in CLOSED:
            found = [x["word"] for x in c.get("candidates") or [] if not x["found_by"].startswith(("remembered", "root"))]
            if found and not any(re.search(rf"\b{re.escape(x.lower())}\b", (w.get("why") or "").lower()) for x in found):
                errs.append(f"{tag}: '{text}' is a remembered word; 'why' must name the retrieved candidate it beats "
                            f"(one of {found[:6]}) and say why (step 2: English is found by meaning)")
    errs += line_errors(out, card)
    errs += slot_errors(out, card)
    for loc, line in (out.get("lines") or {}).items():
        if "\n" in line.strip():
            errs.append(f"{loc}: one line per verse; a second reading is one `alternative`, never extra lines")
    for w in out.get("words", []):
        if "\n" in (w.get("english") or "").strip():
            errs.append(f"{w.get('locus')} word {w.get('i')}: one English rendering per word and line, not several")
    alt = out.get("alternative")
    if alt and "lines" in out:  # the second line is checked by every rule the first is (§6.5)
        over = {(w.get("locus"), w.get("i")): w for w in alt.get("words") or []}
        alt_out = {"lines": alt.get("lines") or {}, "slotted": alt.get("slotted") or {},
                   "words": [over.get((w.get("locus"), w.get("i")), w) for w in out.get("words", [])]}
        errs += [f"second line: {e}" for e in check_unit(alt_out, card)]
    return errs


_LT = None
LT_IGNORE = {"UPPERCASE_SENTENCE_START", "MORFOLOGIK_RULE_EN_US", "EN_QUOTES", "DASH_RULE", "WHITESPACE_RULE",
             "COMMA_PARENTHESIS_WHITESPACE", "EN_UNPAIRED_QUOTES", "EN_UNPAIRED_BRACKETS", "PUNCTUATION_PARAGRAPH_END"}


def grammar(line: str) -> list[str]:
    """LanguageTool (local) grammar findings for an English line; spelling (Sanskrit words) ignored."""
    global _LT
    import language_tool_python  # a missing grammar checker raises (preflight() reports it before the run)
    with _LOOKUP:
        if _LT is None:
            os.environ.setdefault("JAVA_HOME", "/opt/homebrew/opt/openjdk@21")
            _LT = language_tool_python.LanguageTool("en-US")
        ms = _LT.check(line)
    return [f"{m.rule_id}: {m.message} — '{line[m.offset:m.offset + m.error_length]}'" for m in ms if m.rule_id not in LT_IGNORE]


def measured(out: dict) -> dict:
    """The line pass, measured by code, for the reviewer (ENGLISH_CRAFT L1–L9)."""
    import english_bench as B
    res = {}
    for loc, line in (out.get("lines") or {}).items():
        m = B.line_metrics(line)
        m["grammar"] = grammar(line)
        res[loc] = m
    return res


INTERROGATIVE = re.compile(r"\b(kim|ke|kā|kaḥ|ko|kau|kva|katham|kasmāt|kena|kasya|kutaḥ|kutas|kadā|kiyat)\b")


TRACE_FREE = {"and", "or", "nor", "as", "than", "above", "beyond", "then", "so", "too", "also", "not", "no", "one", "ones", "whose", "whom", "his",
              "her", "them", "they", "him", "this", "these", "those", "what", "being", "having", "made", "been"}


def trace_errors(tag: str, text: str, c: dict, w: dict) -> list[str]:
    """Every content word of a word's English must be traceable: one of its English candidates (found in
    the dictionaries or remembered and defined), a word of its literal meaning, a standing decision,
    a fixed rendering, or the Sanskrit kept. A word from none of these is a commentator's reading or an
    invention put into the line (§7.2–§7.3)."""
    if c.get("class") in CLOSED or w.get("kind") == "e":
        return []
    sources = [x["word"] for x in c.get("candidates") or []] + [c.get("literal") or "", c.get("FIXED") or ""]
    sources += [e for r in c.get("standing") or [] for e in (r.get("english") or []) + [r.get("keep") or ""]]
    sources += [m.get("english") or "" for m in w.get("parts") or []]
    if not (c.get("candidates") or c.get("literal") or c.get("standing")):
        return []
    pool = " ".join(sources)
    bad = [t for t in tokens(text) if t not in EN_FUNCTION and t not in TRACE_FREE
           and not re.search(r"[āīūṛṝḷṅñṭḍṇśṣḥṃ]", t) and not renders(pool, t)]
    return [f"{tag}: {bad} in '{text}' come from neither its English candidates nor its literal meaning — "
            "a commentator's reading or an addition (§7.2–§7.3)"] if bad else []


SLOT_IN = re.compile(r"\{([\d,\s]+):([^{}]*)\}")


def slot_errors(out: dict, card: dict) -> list[str]:
    """The slotted line places each word's English: with the slots removed it is the line; every word with
    an English rendering has a slot holding exactly that rendering (its position in the line)."""
    slotted = out.get("slotted")
    if slotted is None:
        return ["no slotted lines: write each word's English in the line as {i:english} (its position)"]
    errs = []
    for loc, line in (out.get("lines") or {}).items():
        sl = slotted.get(loc)
        if sl is None:
            errs.append(f"{loc}: no slotted line")
            continue
        if re.sub(r"\s+", " ", SLOT_IN.sub(r"\2", sl)).strip() != re.sub(r"\s+", " ", line).strip():
            errs.append(f"{loc}: the slotted line without its slots is not the line")
        held: dict = {}
        for ids, text in SLOT_IN.findall(sl):
            for i in re.findall(r"\d+", ids):
                held.setdefault(int(i), []).append(text.strip())
        for w in out.get("words", []):
            if w.get("locus") != loc or not (w.get("english") or "").strip():
                continue
            got = held.get(w.get("i"))
            if not got:
                errs.append(f"{loc} word {w.get('i')}: '{w['english']}' has no slot in the slotted line")
            elif w["english"].strip() not in got and " ".join(got) != w["english"].strip():
                errs.append(f"{loc} word {w.get('i')}: its slot holds {got}, not its English '{w['english']}'")
    return errs


def line_errors(out: dict, card: dict) -> list[str]:
    """Mechanical rules of the standard and the line pass: §7.8 no question without an interrogative;
    L7 one dash; L3 no 'of'-chain; L5-limit one formation per line; §7.16 hybrid compounds, bare
    'whatsoever'."""
    errs = []
    iast = {v["locus"]: v.get("iast") or "" for v in card["verses"]}
    for loc, line in (out.get("lines") or {}).items():
        if "?" in line and not INTERROGATIVE.search(iast.get(loc, "")):
            errs.append(f"{loc}: a question mark needs an interrogative in the Sanskrit (§7.8)")
        if line.rstrip().rstrip("—").count("—") > 1:
            errs.append(f"{loc}: more than one dash (line pass L7)")
        if re.search(r"\bof\b(\W+\w+){1,3}\W+of\b(\W+\w+){1,3}\W+of\b", line):
            errs.append(f"{loc}: an 'of'-chain of three (line pass L3)")
        if re.search(r"(?<!any)(?<!anything )\bwhatsoever\b", line) and not re.search(r"\b(any\w*|no\w*|what\w*)\s+whatsoever", line):
            errs.append(f"{loc}: bare 'whatsoever' (§7.16)")
        for t in re.findall(r"\b[\w’']+(?:-[\w’']+)+\b", line):
            parts = t.split("-")
            if any(re.search(r"[āīūṛṝḷṅñṭḍṇśṣḥṃ]", x) for x in parts) and not all(re.search(r"[āīūṛṝḷṅñṭḍṇśṣḥṃ]", x) for x in parts):
                errs.append(f"{loc}: Sanskrit–English hybrid compound '{t}' (§7.16)")
        n = sum(1 for w in out.get("words", []) if w.get("locus") == loc and w.get("kind") == "d")
        if n > 1:
            errs.append(f"{loc}: {n} formations in one line; at most one (step 3d.8)")
        errs += [f"{loc}: grammar — {g}" for g in grammar(line)]
    return errs


# ---------------------------------------------------------------- stage 2
def translate_unit(unit: list[str], cons: dict, pos: dict, ents: dict, outdir: Path, fixed: dict | None = None) -> dict:
    try:
        return _translate_unit(unit, cons, pos, ents, outdir, fixed)
    except Exception as e:  # one unit's failure is recorded; the run continues
        import traceback
        rec = {"unit": unit, "calls": [], "rounds": [], "output": None, "card": {"verses": []},
               "code_errors": [f"pipeline failure: {e!r}"], "review": [], "trace": traceback.format_exc()}
        (outdir / f"{'-'.join(unit)}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        return rec


def _translate_unit(unit: list[str], cons: dict, pos: dict, ents: dict, outdir: Path, fixed: dict | None = None) -> dict:
    scard = unit_card(unit, cons, pos, ents, fixed)
    rec = {"unit": unit, "calls": [], "rounds": []}
    prev = outdir / f"{'-'.join(unit)}.json"
    m = json.loads(prev.read_text()).get("meaning") if (fixed and prev.exists()) else None
    if m is None:
        m, st = call("meaning", meaning_view(scard))  # step 1: Sanskrit sources only, in the owner's order
        rec["calls"].append(st)
        merrs = meaning_errors(m, scard)
        if merrs:  # one correction round: every content word meant, and meant from the texts
            m2, st = call("meaning", meaning_view(scard), "\n\nCORRECTION. Code found these errors in your answer "
                          "PREVIOUS; fix each and return the full JSON again.\nPREVIOUS: " + json.dumps(m, ensure_ascii=False)
                          + "\nERRORS: " + json.dumps(merrs, ensure_ascii=False))
            rec["calls"].append(st)
            m = m2 or m
        rec["meaning_errors"] = meaning_errors(m, scard)
    senses = {(w.get("locus"), w.get("i")): w for w in (m or {}).get("words", [])}
    card = translate_card(scard, senses)  # step 2: English found and defined by code
    here = {f"{k[0]}:{k[1]}": v.get("here") for k, v in senses.items() if v.get("here")}
    roots = {f"{v['locus']}:{w['i']}": sanskrit_summary(w["sanskrit"]) for v in scard["verses"] for w in v["words"]
             if sanskrit_summary(w.get("sanskrit") or {})}
    rec["coverage_errors"] = [e for v in scard["verses"] for w in v["words"] for e in (w.get("sanskrit") or {}).get("coverage_errors", [])]
    rec["meaning"] = m
    rec["meaning_card"] = meaning_view(scard)  # exactly what the meaning call was given
    out, st = call("translate", card)  # steps 3–6 and the line pass
    rec["calls"].append(st)
    prior = None
    for rnd in range(MAX_REVISIONS + 1):
        errs = check_unit(out, card)
        extra = "" if prior is None else ("\n\nRE-REVIEW. The answer was revised after these findings: "
                                          + json.dumps(prior["review"], ensure_ascii=False)
                                          + "\nReport any that are not fixed, and any new error.")
        rv, st = call("review", {**card, "SANSKRIT_MEANING": roots, "COMMENTATORS_HERE": here, "ANSWER": out,
                                 "MEASURED": measured(out or {})}, extra)
        rec["calls"].append(st)
        allf = [f for f in (rv or {}).get("findings", []) if f.get("kind")]
        findings = [f for f in allf if f.get("severity") in ("S1", "S2")]  # S3 is taste: recorded, not forced
        rec["rounds"].append({"answer": out, "code_errors": errs, "review": findings, "taste": [f for f in allf if f not in findings]})
        if (not errs and not findings) or rnd == MAX_REVISIONS:
            break
        prior = {"code": errs, "review": findings}
        extra = ("\n\nREVISION. Your previous answer is PREVIOUS. Code found the ERRORS (each must be fixed) and a "
                 "reviewer the FINDINGS (adopt each unless it breaks the standard; list declined ones with a reason in "
                 "\"declined\"). Return the full JSON again.\nPREVIOUS: " + json.dumps(out, ensure_ascii=False)
                 + "\nERRORS: " + json.dumps(errs, ensure_ascii=False) + "\nFINDINGS: " + json.dumps(findings, ensure_ascii=False))
        out2, st = call("translate", card, extra)
        rec["calls"].append(st)
        out = out2 or out
    last = rec["rounds"][-1]
    rec.update({"card": card, "output": last["answer"], "code_errors": last["code_errors"], "review": last["review"]})
    (outdir / f"{'-'.join(unit)}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


# ---------------------------------------------------------------- stage 3
CLOSED = {"pronoun", "particle"}
NEGATIVE = {"a", "an", "na", "nañ", "nis", "nir", "niḥ", "vi", "dus", "dur"}


def renderings(recs: list[dict]) -> dict:
    """lemma -> [(locus, english, means, line)] over content words and compound members."""
    by: dict = {}
    for r in recs:
        lines = (r.get("output") or {}).get("lines") or {}
        cw = {(v["locus"], w["i"]): w for v in r["card"]["verses"] for w in v["words"]}
        lit = {(x.get("locus"), x.get("i")): x for x in ((r.get("meaning") or {}).get("words") or [])}
        for w in (r.get("output") or {}).get("words", []):
            c = cw.get((w.get("locus"), w.get("i")))
            if not c or c.get("class") in CLOSED or not w.get("english"):
                continue
            if not [t for t in tokens(w["english"]) if t not in EN_FUNCTION]:
                continue  # a copula or auxiliary rendering ('am', 'is') is grammar, not a term
            item = {"lemma": c["lemma"], "root": (c.get("root") or "").split(" ")[0] or None, "locus": w["locus"],
                    "english": w["english"], "literal": (lit.get((w["locus"], w["i"])) or {}).get("literal"),
                    "line": lines.get(w["locus"])}
            sandhi = (c.get("compound") or {}).get("type") == "two words joined by sandhi"
            if not sandhi:  # a sandhi-joined token is checked through its two words
                by.setdefault(c["lemma"], []).append({**item, "whole_compound": bool(c.get("compound"))})
            if w.get("kind") == "e":
                continue  # a word kept in Sanskrit is one term; its members are not rendered
            mems = (c.get("compound") or {}).get("members") or []
            negative = bool(mems) and (mems[0].get("stem") or "").strip("-") in NEGATIVE
            content_members = set() if negative else {m.get("stem") for m in mems  # a nañ compound is one unit
                                                      if m.get("class") not in CLOSED and m.get("stem") not in NEGATIVE}
            for m in w.get("parts") or []:  # content members of compounds are checked too (duḥkha in sukhaduḥkha)
                if m.get("stem") in content_members and m.get("english") and [t for t in tokens(m["english"]) if t not in EN_FUNCTION]:
                    by.setdefault(m["stem"], []).append({**item, "lemma": m["stem"], "english": m["english"],
                                                         "in_compound": w["english"], "of": c["lemma"]})
    return by


CASE_WORDS = {"than", "above", "comparison", "through", "in", "to", "of", "by", "from", "for", "with"}


def term_key(text: str) -> str:
    """The rendering as a term: content-word stems, without case prepositions and grammatical words."""
    return " ".join(sorted({en_stem(t) for t in tokens(text) if t not in EN_FUNCTION and t not in CASE_WORDS
                            and t not in TRACE_FREE}))


def same(a: str, b: str) -> bool:
    ka, kb = term_key(a), term_key(b)
    return bool(ka) and (ka == kb or (renders(a, b) and renders(b, a)))


def conflicts(by: dict) -> dict:
    """Groups to decide: a lemma rendered two ways (by English stem), and two lemmas rendered by the same
    English (§7.6), merged into connected groups keyed by their lemmas."""
    groups: list[set] = []

    def join(lemmas: set):
        hit = [g for g in groups if g & lemmas]
        for g in hit:
            groups.remove(g)
            lemmas |= g
        groups.append(lemmas)
    for lemma, items in by.items():
        forms: list[str] = []
        for it in items:
            if not any(same(f, it["english"]) for f in forms):
                forms.append(it["english"])
        if len(forms) > 1:
            join({lemma})
    owner: dict = {}
    for lemma, items in by.items():
        for it in items:
            if it.get("whole_compound"):
                continue  # a compound shares its members' English by design; members are checked themselves
            key = term_key(it["english"])
            if key:
                owner.setdefault(key, {})[lemma] = it.get("root")
    for key, lr in owner.items():
        lemmas = set(lr)
        roots = {r for r in lr.values() if r}
        if len(lemmas) > 1 and len(roots) == 1 and all(lr.values()):
            continue  # one root: words of a family share English by design (the root echo)
        if len(lemmas) > 1 and not any(term_rows(l) and term_rows(m) and {r["term"].split(".")[0] for r in term_rows(l)} & {r["term"].split(".")[0] for r in term_rows(m)}
                                       for l in lemmas for m in lemmas if l != m):
            join(set(lemmas))
    changed = True
    while changed:  # a member's group and its compound's group are decided together (veda with vedavid)
        changed = False
        for g in list(groups):
            parents = {it.get("of") for l in g for it in by[l] if it.get("of")}
            other = next((h for h in groups if h is not g and (h & parents or any(it.get("of") in g for l in h for it in by[l]))), None)
            if other is not None:
                groups.remove(g)
                groups.remove(other)
                groups.append(g | other)
                changed = True
                break
    return {" + ".join(sorted(g)): [it for l in sorted(g) for it in by[l]] for g in groups}


def compliance(recs: list[dict], decisions: dict) -> dict:
    """How many decided placements now use the decided English, and which do not."""
    fixed = {(r.get("lemma") or k, loc): r["english"] for k, rs in decisions.items() for r in rs for loc in r.get("loci") or []}
    total, bad = 0, []
    for lemma, items in renderings(recs).items():
        for it in items:
            f = fixed.get((lemma, it["locus"]))
            if f is None:
                continue
            total += 1
            if not (renders(it["english"], f) or keeps(it["english"], f) or same(it["english"], f)):
                bad.append(f"{lemma} {it['locus']}: '{it['english']}' (decided '{f}')")
    return {"decided_placements": total, "compliant": total - len(bad), "not_compliant": bad}


# ---------------------------------------------------------------- owner sheet
SHEET_KINDS = {"d": "formation", "e": "Sanskrit kept"}


def sheet_rows(recs: list[dict], decisions: dict | None = None) -> list[dict]:
    """What the owner rules on: formations (kind d), Sanskrit kept (kind e), losses (carried false), seed
    decisions challenged, second lines, and the consistency decisions."""
    rows = []
    for r in recs:
        lit = {(x.get("locus"), x.get("i")): x for x in ((r.get("meaning") or {}).get("words") or [])}
        out = r.get("output") or {}
        for w in out.get("words", []):
            why = []
            if w.get("kind") in SHEET_KINDS:
                why.append(SHEET_KINDS[w["kind"]] + (f" (models: {', '.join(w.get('models') or [])})" if w["kind"] == "d" else ""))
            if w.get("carried") is False:
                why.append(f"loses: {w.get('lost')}")
            if (w.get("challenge") or "").strip():
                why.append(f"challenges the seed decision: {w['challenge']}")
            if why:
                rows.append({"locus": w.get("locus"), "i": w.get("i"), "english": w.get("english"),
                             "literal": (lit.get((w.get("locus"), w.get("i"))) or {}).get("literal") or "",
                             "issue": "; ".join(why), "why": w.get("why") or ""})
        alt = out.get("alternative")
        if alt:
            for loc, line in (alt.get("lines") or {}).items():
                rows.append({"locus": loc, "i": None, "english": line, "literal": "", "issue": f"second line ({alt.get('fork')})",
                             "why": ""})
    for lemma, d in (decisions or {}).items():
        rows.append({"locus": ", ".join(x["loci"][0] for x in d if x.get("loci")), "i": lemma,
                     "english": " / ".join(x["english"] for x in d), "literal": "", "issue": "consistency decision",
                     "why": "; ".join(x.get("why") or "" for x in d)})
    return rows


def sheet(run: str) -> Path:
    d = RUNS / run / "translate"
    recs = [json.loads(f.read_text()) for f in sorted(d.glob("*.json")) if not f.name.startswith("_")]
    cons = d / "_consistency.json"
    rows = sheet_rows(recs, json.loads(cons.read_text()) if cons.exists() else None)
    cell = lambda x: str(x if x is not None else "").replace("|", "\\|").replace("\n", " ")  # noqa: E731
    out = RUNS / run / "DECISIONS.md"
    out.write_text("# Owner decision sheet\n\nFormations, Sanskrit kept, losses, challenged seed decisions, second lines and "
                   "consistency decisions. Rule on each row: keep, or give the word.\n\n"
                   "| locus | word | English | literal meaning | issue | why |\n|---|---|---|---|---|---|\n"
                   + "\n".join(f"| {cell(r['locus'])} | {cell(r['i'])} | **{cell(r['english'])}** | {cell(r['literal'])} | "
                                f"{cell(r['issue'])} | {cell(r['why'])} |" for r in rows) + "\n", encoding="utf-8")
    return out


# ---------------------------------------------------------------- CLI
def accepted_construals(run: str) -> tuple[list[dict], list[str]]:
    """The construals whose parse was accepted (construe/<locus>/record.json "accepted": true), and the
    loci left out (rejected, unreviewed or missing a record). A rejected parse is never translated."""
    cons, left = [], []
    for out in sorted((RUNS / run / "construe").glob("*/output.json")):
        rec = out.parent / "record.json"
        if rec.exists() and json.loads(rec.read_text(encoding="utf-8")).get("accepted"):
            cons.append(json.loads(out.read_text(encoding="utf-8")))
        else:
            left.append(out.parent.name)
    return cons, left


def load(run: str) -> tuple[dict, dict, dict, list[list[str]]]:
    cons, left = accepted_construals(run)
    if left:
        print(f"not translated (parse not accepted): {', '.join(left)}", file=sys.stderr)
    pos, ents = lemma_map(cons)
    return {c["locus"]: c for c in cons}, pos, ents, C.units(cons)


def summary(recs: list[dict], t: float) -> dict:
    calls = [c for r in recs for c in r["calls"]]
    return {"units": len(recs), "wall_s": round(time.time() - t), "calls": len(calls),
            "output_tokens": sum(c["output_tokens"] for c in calls), "commands_run": sum(c["commands"] for c in calls),
            "rounds": {"-".join(r["unit"]): len(r["rounds"]) for r in recs},
            "code_errors_left": {"-".join(r["unit"]): r["code_errors"] for r in recs if r["code_errors"]},
            "review_left": {"-".join(r["unit"]): r["review"] for r in recs if r["review"]}}


def consistency(runs: list[str], jobs: int) -> dict:
    """The consistency pass over one chapter's run or, given several runs, the whole book: conflicting
    groups across every run are decided once, and the units that break a decision are re-translated in
    their own run with the decision fixed."""
    loaded = {run: load(run) for run in runs}
    recs = []
    for run in runs:
        for f in sorted((RUNS / run / "translate").glob("*.json")):
            if not f.name.startswith("_"):
                recs.append({**json.loads(f.read_text()), "_run": run})
    conf = conflicts(renderings(recs))
    ents_all: dict = {}
    for run in runs:
        ents_all.update(loaded[run][2])

    def decide(item):
        key, places = item
        lemmas = key.split(" + ")
        card = {"words": [{"lemma": l, "sanskrit": sanskrit_summary(member_at(ents_all.get(l))),
                           "standing": term_rows(l)} for l in lemmas], "places": places}
        d, st = call("consistency", card)
        return key, (d or {}).get("renderings") or [], st
    with ThreadPoolExecutor(jobs) as ex:
        got = list(ex.map(decide, conf.items()))
    fixed, decisions = {}, {}
    for key, rs, _ in got:
        decisions[key] = rs
        for r in rs:
            for loc in r.get("loci") or []:
                fixed[(r.get("lemma") or key, loc)] = r["english"]
    for run in runs:
        (RUNS / run / "translate" / "_consistency.json").write_text(json.dumps(decisions, ensure_ascii=False, indent=1),
                                                                    encoding="utf-8")
    redo = []
    for r in recs:
        by = renderings([r])
        if any(not renders(it["english"], fixed[(lm, it["locus"])]) for lm, items in by.items() for it in items
               if (lm, it["locus"]) in fixed):
            redo.append((r["_run"], r["unit"]))
    t = time.time()

    def again(job):
        run, unit = job
        cons, pos, ents, _ = loaded[run]
        return translate_unit(unit, cons, pos, ents, RUNS / run / "translate", fixed)
    with ThreadPoolExecutor(jobs) as ex:
        recs2 = list(ex.map(again, redo))
    after = [json.loads(f.read_text()) for run in runs for f in (RUNS / run / "translate").glob("*.json")
             if not f.name.startswith("_")]
    return {"runs": runs, "lemmas_in_conflict": len(conf), "units_redone": len(redo), **summary(recs2, t),
            "decision_calls": len(got), **compliance(after, decisions)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["translate", "consistency", "sheet"])
    ap.add_argument("--run", required=True, nargs="+", help="one run; consistency and sheet take several (the book)")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--jobs", type=int, default=24)
    ap.add_argument("--allow-partial-tools", action="store_true",
                    help="proceed when an English tool is missing or the index incomplete (recorded in the summary)")
    a = ap.parse_args()
    if a.stage == "sheet":
        for run in a.run:
            print(sheet(run))
        return 0
    if a.stage == "translate" and len(a.run) != 1:
        raise SystemExit("translate takes one run")
    t = time.time()
    tools = preflight(a.allow_partial_tools)
    if a.stage == "translate":
        cons, pos, ents, units = load(a.run[0])
        outdir = RUNS / a.run[0] / "translate"
        outdir.mkdir(parents=True, exist_ok=True)
        todo = [u for u in units if not a.only or set(u) & set(a.only)]
        with ThreadPoolExecutor(a.jobs) as ex:
            recs = list(ex.map(lambda u: translate_unit(u, cons, pos, ents, outdir), todo))
        s = summary(recs, t)
    else:
        s = consistency(a.run, a.jobs)
        recs = []
    import english_bench as B
    s = {**s, "tools": tools, "ngram_failures": len(B.NGRAM_FAILURES),
         "coverage_errors": {"-".join(r["unit"]): r.get("coverage_errors") for r in recs if r.get("coverage_errors")},
         "meaning_errors_left": {"-".join(r["unit"]): r.get("meaning_errors") for r in recs if r.get("meaning_errors")}}
    for run in a.run:
        (RUNS / run / "translate" / f"_summary_{a.stage}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1),
                                                                         encoding="utf-8")
    print(json.dumps(s, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

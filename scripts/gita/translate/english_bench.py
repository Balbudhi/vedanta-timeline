#!/usr/bin/env python3
"""The English workbench: everything code can know about an English word or line, indexed for fast
queries, so the model judges from evidence (ENGLISH_CRAFT §2 steps 2–4 and the line pass).

Data (local, under prakriya/tmp/english/bench/; built once):
- senses   the seven-source definition table (english.db `defs`), modern sources first;
- vectors  semantic index of definitions (qwen3-embedding via Ollama), for finding words by meaning;
- profile  per headword: current frequency (wordfreq Zipf), stress pattern and syllables (CMUdict,
           else Wiktionary IPA), register tags (archaic, literary, poetic, dated, rare …), origin
           (Germanic / Latin / Greek / French … from the etymology table);
- ngrams   phrase frequency in English books (Google Books Ngram JSON), cached.

Queries: find(sense, k) -> words by meaning; profile(word); phrase_freq(phrases);
line_metrics(line) -> syllables, stresses, end-weight, sibilants, collisions, of-chains, register mix.

    benchenv/bin/python english_bench.py build-index      # resumable; ~1–2 h on an M4 Max
    benchenv/bin/python english_bench.py build-profiles
    benchenv/bin/python english_bench.py find "lift up and carry out of danger"
"""
from __future__ import annotations

import argparse
import functools
import gzip
import json
import re
import sqlite3
import sys
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

ENG = Path.home() / "Dev/prakriya/tmp/english"
DB = ENG / "english.db"
ETYM = ENG / "etym.db"
BENCH = ENG / "bench"
KAIKKI = Path.home() / "Dev/prakriya/sources/raw/upstream_data/english/kaikki-english/kaikki.org-dictionary-English.jsonl.gz"
MODEL = "qwen3-embedding:0.6b"
DIM = 1024
SHARD = 20000
DEF_SOURCES = ("oewn2025", "webster1913", "wiktionary")  # GCIDE is built on Webster 1913
FORM_OF = re.compile(r"^(plural of|alternative form of|obsolete form of|archaic form of|misspelling of|"
                     r"comparative form of|superlative form of|third-person singular|.*(past tense|participle) of|"
                     r".*spelling of)", re.I)
REGISTER_TAGS = ("archaic", "obsolete", "rare", "literary", "poetic", "dated", "formal", "dialectal", "slang",
                 "informal", "colloquial", "nonstandard", "historical", "biblical", "technical")
_lock = threading.Lock()


def con(path: Path = DB) -> sqlite3.Connection:
    c = sqlite3.connect(str(path), check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c


# ---------------------------------------------------------------- semantic index
def index_rows() -> list[tuple[int, str, str]]:
    """(def id, headword, text) worth finding: current words (Zipf ≥ 1) and every register-tagged sense
    (the rare exact words), definitions only (no inflection stubs, no thesaurus lists)."""
    from wordfreq import zipf_frequency
    rows, seen = [], set()
    q = (f"select id, hw, pos, tags, definition, source from defs where source in ({','.join('?' * len(DEF_SOURCES))}) "
         "order by case source when 'oewn2025' then 0 when 'webster1913' then 1 else 2 end, id")
    for r in con().execute(q, DEF_SOURCES):
        d = (r["definition"] or "").strip()
        if len(d) < 12 or FORM_OF.match(d) or not re.fullmatch(r"[a-z][a-z' -]*", r["hw"] or ""):
            continue
        tagged = any(t in (r["tags"] or "") for t in REGISTER_TAGS)
        if not tagged and zipf_frequency(r["hw"], "en") < 1.0:
            continue
        key = (r["hw"], d.lower()[:200])
        if key in seen:
            continue
        seen.add(key)
        rows.append((r["id"], r["hw"], f"{r['hw']} ({r['pos'] or ''}): {d[:300]}"))
    import random
    random.Random(20261109).shuffle(rows)  # every shard is a uniform sample: a partial index is usable
    return rows


def build_index() -> None:
    import numpy as np
    import ollama
    BENCH.mkdir(parents=True, exist_ok=True)
    meta = BENCH / "index_rows.json"
    if not meta.exists():
        rows = index_rows()
        meta.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    rows = json.loads(meta.read_text(encoding="utf-8"))
    client = ollama.Client()
    n = (len(rows) + SHARD - 1) // SHARD
    print(json.dumps({"rows": len(rows), "shards": n}), flush=True)
    for k in range(n):
        out = BENCH / f"vec_{k:04d}.npy"
        if out.exists():
            continue
        t = time.time()
        part = rows[k * SHARD:(k + 1) * SHARD]
        vecs = []
        for i in range(0, len(part), 256):
            for attempt in range(6):  # the local server occasionally drops a connection: retry with backoff
                try:
                    r = client.embed(model=MODEL, input=[x[2] for x in part[i:i + 256]])
                    break
                except Exception as e:
                    print(json.dumps({"retry": attempt + 1, "error": str(e)[:120]}), flush=True)
                    time.sleep(5 * (attempt + 1))
            else:
                raise SystemExit("embedding failed six times")
            vecs += r["embeddings"]
        v = np.asarray(vecs, dtype=np.float32)
        v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-9
        np.save(out, v.astype(np.float16))
        print(json.dumps({"shard": k, "of": n, "s": round(time.time() - t)}), flush=True)


@functools.lru_cache(maxsize=1)
def _index():
    """(rows, matrix) of the shards built so far; index_state() says how complete it is."""
    import numpy as np
    rows = json.loads((BENCH / "index_rows.json").read_text(encoding="utf-8"))
    shards = sorted(BENCH.glob("vec_*.npy"))
    mat = np.concatenate([np.load(s).astype(np.float32) for s in shards]) if shards else np.zeros((0, DIM), np.float32)
    return rows[:len(mat)], mat


def index_state() -> dict:
    rows = json.loads((BENCH / "index_rows.json").read_text(encoding="utf-8")) if (BENCH / "index_rows.json").exists() else []
    want = (len(rows) + SHARD - 1) // SHARD
    have = len(list(BENCH.glob("vec_*.npy")))
    return {"shards": have, "of": want, "complete": bool(want) and have == want}


def embed_query(text: str):
    import numpy as np
    import ollama
    q = "Instruct: Given a description of a meaning, retrieve dictionary definitions that express it\nQuery: " + text
    v = np.asarray(ollama.Client().embed(model=MODEL, input=[q])["embeddings"][0], dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-9)


def find(sense: str, k: int = 15) -> list[dict]:
    """Words whose definitions express `sense` (best definition per headword), by cosine similarity."""
    import numpy as np
    rows, mat = _index()
    if not len(mat):
        return []
    s = mat @ embed_query(sense)
    top = np.argsort(-s)[: k * 6]
    out, seen = [], set()
    for i in top:
        hw = rows[i][1]
        if hw in seen:
            continue
        seen.add(hw)
        out.append({"word": hw, "score": round(float(s[i]), 3), "definition": rows[i][2].split(": ", 1)[-1][:160]})
        if len(out) >= k:
            break
    return out


# ---------------------------------------------------------------- word profile
@functools.lru_cache(maxsize=1)
def _kaikki_ipa() -> dict[str, str]:
    path = BENCH / "ipa.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    with gzip.open(KAIKKI, "rt", encoding="utf-8") as f:
        for line in f:
            if '"ipa"' not in line:
                continue
            e = json.loads(line)
            w = (e.get("word") or "").lower()
            if w in out or not re.fullmatch(r"[a-z][a-z'-]*", w):
                continue
            for s in e.get("sounds") or []:
                if s.get("ipa") and "ˈ" in s["ipa"]:
                    out[w] = s["ipa"]
                    break
    BENCH.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


_IPA_V = re.compile(r"(?:aɪ|aʊ|ɔɪ|eɪ|oʊ|əʊ|ɪə|eə|ʊə|[aeiouæɑɒɔəɛɜɪʊʌyøɐɘɵɤ]ː?|[nlmr]̩)")


def ipa_stress(ipa: str) -> str | None:
    """IPA -> stress digits per syllable (1 primary, 2 secondary, 0 none)."""
    s = re.sub(r"[/\[\]()]", "", ipa.split(",")[0]).strip()
    out, pending = [], "0"
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "ˈ":
            pending = "1"
        elif ch == "ˌ":
            pending = "2"
        m = _IPA_V.match(s, i)
        if m:
            out.append(pending)
            pending = "0"
            i = m.end()
            continue
        i += 1
    return "".join(out) or None


def stress(word: str) -> str | None:
    import pronouncing
    w = word.lower()
    p = pronouncing.phones_for_word(w)
    if p:
        return pronouncing.stresses(p[0])
    ipa = _kaikki_ipa().get(w)
    if ipa:
        return ipa_stress(ipa)
    for k in range(len(w) - 2, 1, -1):  # a closed compound of two known words: straight+way, up+bearer
        a, b = w[:k], w[k:]
        pa, pb = pronouncing.phones_for_word(a), pronouncing.phones_for_word(b)
        if pa and pb and len(a) >= 2 and len(b) >= 3:
            sa, sb = pronouncing.stresses(pa[0]), pronouncing.stresses(pb[0])
            return (sa.replace("1", "1") + sb.replace("1", "2")) if len(sa) == 1 else sa + sb.replace("1", "2")
    return None


@functools.lru_cache(maxsize=1)
def _etym() -> sqlite3.Connection | None:
    return con(ETYM) if ETYM.exists() else None


def origin(word: str) -> str | None:
    """'native' (inherited from Old English) or the language of the nearest etymon (Latin, French …)."""
    c = _etym()
    if not c:
        return None
    r = c.execute("select e.native, (select lang from etymon where entry_id=e.id order by ord limit 1) as lang "
                  "from entry e where word=? and form_of=0 order by n_senses desc limit 1", (word.lower(),)).fetchone()
    if not r:
        return None
    return "native" if r["native"] else r["lang"]


def profile(word: str) -> dict:
    """What code knows about an English word: frequency now, stress, register tags, origin."""
    from wordfreq import zipf_frequency
    w = word.lower().strip()
    toks = re.findall(r"[a-z']+", w)
    with _lock:
        c = con()
        senses = [r[0] or "" for r in c.execute("select tags from defs where hw=? and source='wiktionary' order by id", (w,))]
    tags = set()
    if senses:
        tags |= {t for t in REGISTER_TAGS if t in senses[0]}                      # the main (first) sense
        tags |= {t for t in REGISTER_TAGS if sum(t in x for x in senses) * 2 >= len(senses)}  # most senses
    st = [stress(t) for t in toks]
    return {"word": word, "zipf": round(zipf_frequency(w, "en"), 2),
            "stress": "-".join(x or "?" for x in st), "syllables": sum(len(x) for x in st if x) or None,
            "register": sorted(tags), "origin": origin(w) if len(toks) == 1 else None}


# ---------------------------------------------------------------- phrase frequency (Google Books)
NGRAM_CACHE = BENCH / "ngram_cache.sqlite"
_last = [0.0]


NGRAM_FAILURES: list[str] = []


def phrase_freq(phrases: list[str], year_start: int = 1900) -> dict[str, float | None]:
    """Mean relative frequency of each phrase in English books since `year_start` (cached; ≤1 req/s)."""
    BENCH.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(NGRAM_CACHE))
    c.execute("create table if not exists f(p text primary key, v real)")
    out, todo = {}, []
    for p in phrases:
        r = c.execute("select v from f where p=?", (p.lower(),)).fetchone()
        (out.__setitem__(p, r[0]) if r else todo.append(p))
    for i in range(0, len(todo), 10):
        chunk = todo[i:i + 10]
        with _lock:
            wait = 1.0 - (time.time() - _last[0])
            if wait > 0:
                time.sleep(wait)
            _last[0] = time.time()
        url = ("https://books.google.com/ngrams/json?" + urllib.parse.urlencode(
            {"content": ",".join(chunk), "year_start": year_start, "year_end": 2022, "corpus": "en", "smoothing": 0}))
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                data = json.loads(r.read().decode())
        except Exception as e:  # recorded: the phrase's frequency stays unknown (None), never 0
            NGRAM_FAILURES.append(f"{chunk[0]}…: {e!r}"[:160])
            data = []
        got = {d["ngram"].lower(): sum(d["timeseries"]) / max(1, len(d["timeseries"])) for d in data}
        for p in chunk:
            v = got.get(p.lower(), 0.0 if data else None)
            out[p] = v
            if v is not None:
                c.execute("insert or replace into f values(?,?)", (p.lower(), v))
        c.commit()
    return out


# ---------------------------------------------------------------- line metrics (the line pass, measured)
FUNCTION = {"the", "a", "an", "of", "to", "in", "on", "by", "with", "from", "for", "and", "or", "but", "is", "are",
            "was", "be", "who", "which", "that", "it", "he", "his", "their", "its", "as", "at", "not", "no"}


def line_metrics(line: str) -> dict:
    """Measured facts for the line pass (ENGLISH_CRAFT L1–L9): per clause the final word and whether it
    is a stressed content word (L2), 'of' runs (L3), sibilant density and consonant collisions at word
    boundaries (L5), dashes (L7), register-tagged words (L8), syllable count."""
    clauses = [c.strip() for c in re.split(r"[;:—,]|--", line) if c.strip()]
    ends = []
    for c in clauses:
        ws = re.findall(r"[A-Za-zāīūṛṭḍṇśṣḥṃ']+", c)
        if ws:
            w = ws[-1].lower()
            st = stress(w) or ""
            ends.append({"clause": c[-40:], "last": w, "content": w not in FUNCTION, "final_syllable_stressed": st.endswith("1")})
    words = re.findall(r"[A-Za-z']+", line.lower())
    sib = sum(len(re.findall(r"s|z|sh|ch|x", w)) for w in words)
    collisions = [f"{a} {b}" for a, b in zip(words, words[1:]) if a and b and a[-1] == b[0] and a[-1] in "bdgkptszfv"]
    of_runs = max((len(re.findall(r"\bof\b", c)) for c in clauses), default=0)
    reg = {w: profile(w)["register"] for w in set(words) if w not in FUNCTION and len(w) > 3}
    syl = sum(len(stress(w) or "0") for w in words)
    return {"syllables": syl, "clause_ends": ends, "weak_ends": [e["last"] for e in ends if not e["content"]],
            "sibilants_per_word": round(sib / max(1, len(words)), 2), "collisions": collisions,
            "max_of_chain": of_runs, "dashes": line.count("—"),
            "register_words": {w: r for w, r in reg.items() if r}}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build-index", "build-profiles", "find", "profile", "line", "ngram"])
    ap.add_argument("arg", nargs="*")
    a = ap.parse_args()
    if a.cmd == "build-index":
        build_index()
    elif a.cmd == "build-profiles":
        print(len(_kaikki_ipa()), "IPA entries")
    elif a.cmd == "find":
        print(json.dumps(find(" ".join(a.arg)), ensure_ascii=False, indent=1))
    elif a.cmd == "profile":
        print(json.dumps([profile(w) for w in a.arg], ensure_ascii=False))
    elif a.cmd == "line":
        print(json.dumps(line_metrics(" ".join(a.arg)), ensure_ascii=False, indent=1))
    else:
        print(json.dumps(phrase_freq(a.arg), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

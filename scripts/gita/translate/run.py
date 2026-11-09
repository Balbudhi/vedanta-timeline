#!/usr/bin/env python3
"""RETIRED lexicon-first stages (docs/history/gita/WORKFLOW_lexicon_first.md): code builds small cards; the model makes one choice per call,
with no tools and no files; code checks; a reviewer sees the same card; one revision.

    python3 scripts/gita/translate/run.py lexicon --run ch12-qual [--only bhakta manas]
    python3 scripts/gita/translate/run.py verse   --run ch12-qual [--only 12.13]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check  # noqa: E402
import compile as C  # noqa: E402

ROOT = HERE.parents[2]
P2 = HERE / "prompts2"
RUNS = ROOT / "internal/gita_pipeline/run"
MODEL = os.environ.get("GITA_MODEL", "gpt-6-astra")
EFFORT = os.environ.get("GITA_EFFORT", "high")
CODEX_HOME = os.environ.get("GITA_CODEX_HOME", str(Path.home() / ".codex-gita"))
WORD_MAX = 3
import threading  # noqa: E402
_ENGLISH_LOCK = threading.Lock()  # the shared prakriya lookup layer under english.py is not thread-safe
_CALLS = threading.BoundedSemaphore(int(os.environ.get("GITA_MAX_CALLS", "32")))  # concurrent model calls


def roots_rows(root: str | None, upasargas: list | None, image: str | None) -> tuple[list[dict], dict]:
    """English words sharing the Sanskrit root (PIE cognates) or whose etymon pictures the image."""
    import english_roots as er
    rows, searched = [], {}
    with _ENGLISH_LOCK:
        if root:
            q = ("-".join(list(upasargas or []) + [root])) if upasargas else root
            r = er.by_sanskrit(q, limit=8)
            rows += list(r)
            searched["root"] = r.record() if hasattr(r, "record") else {"query": q}
        if image:
            r = er.by_image(image, limit=8)
            rows += list(r)
            searched["image"] = r.record() if hasattr(r, "record") else {"query": image}
    out, seen = [], set()
    for x in rows:
        if x["word"] in seen:
            continue
        seen.add(x["word"])
        out.append({"word": x["word"], "pos": x.get("pos"), "modern": x.get("modern"), "etym": x.get("etym"),
                    "link": x.get("link")})
    none = {k: bool((v or {}).get("none")) for k, v in searched.items()}
    return out, none


def etable(sense: str, image: str | None, limit: int) -> list[dict]:
    import english
    with _ENGLISH_LOCK:
        return english.english_table(sense, image, limit=limit)


def call(task: str, card: dict, extra: str = "") -> tuple[dict | None, dict]:
    """One model call: instructions + card inline; returns (json, stats). No tools expected."""
    text = (P2 / f"{task}.md").read_text(encoding="utf-8") + extra + "\n\nCARD:\n" + json.dumps(card, ensure_ascii=False, indent=1)
    for attempt in range(2):  # one retry when the answer is not parseable JSON (a failed or cut-off call)
        _CALLS.acquire()
        t = time.time()
        try:
            r, raw = _exec(text)
        finally:
            _CALLS.release()
        out, stats = _parse(r, raw, task, card, t)
        if out is not None:
            break
    stats["attempts"] = attempt + 1
    return out, stats


def _exec(text: str):
    with tempfile.TemporaryDirectory(dir=RUNS) as d:
        out = Path(d) / "out.txt"
        r = subprocess.run(["codex", "exec", "--skip-git-repo-check", "-s", "read-only", "-C", d, "-m", MODEL,
                            "-c", f"model_reasoning_effort={EFFORT}", "-c", "project_doc_max_bytes=0", "--json",
                            "-o", str(out), text], stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           env={**os.environ, "CODEX_HOME": CODEX_HOME})
        raw = out.read_text(encoding="utf-8") if out.exists() else ""
    return r, raw


def _parse(r, raw: str, task: str, card: dict, t: float) -> tuple[dict | None, dict]:
    cmds = tok = 0
    for l in r.stdout.splitlines():
        if '"command_execution"' in l and '"item.started"' in l:
            cmds += 1
        if '"turn.completed"' in l:
            u = json.loads(l).get("usage") or {}
            tok += u.get("input_tokens", 0) + u.get("output_tokens", 0)
    stats = {"task": task, "s": round(time.time() - t, 1), "card_bytes": len(json.dumps(card, ensure_ascii=False).encode()),
             "commands": cmds, "tokens": tok}
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        return (json.loads(m.group(0)) if m else None), stats
    except json.JSONDecodeError:
        return None, stats


# ---------------------------------------------------------------- lexicon
def check_choice(ch: dict, table: list[dict]) -> list[str]:
    errs = []
    d = (ch or {}).get("default") or ""
    if not d:
        return ["no default"]
    words = d.replace("-", " ").split()
    if ch.get("form") != "new" and len(words) > WORD_MAX:
        errs.append(f"'{d}' has {len(words)} words; a rendering is a word, a compound or ≤{WORD_MAX} words")
    if re.search(r"\b(and|who|which|that|whose)\b", d):
        errs.append(f"'{d}' is a pair or a clause, not a rendering")
    names = {r["word"].lower() for r in table}
    head = d.lower()
    if ch.get("form") == "existing" and head not in names and not any(n in head.split() for n in names):
        errs.append(f"'{d}' is marked existing but is not in the dictionary table; choose from it or mark it new with parts")
    if ch.get("form") == "new" and not ((ch.get("new") or {}).get("parts") and len((ch.get("new") or {}).get("models") or []) >= 2):
        errs.append("a new word needs its parts and two attested models")
    if not set(ch.get("carries") or []) <= {"sense", "image", "double"}:
        errs.append("carries must be a subset of sense, image, double")
    return errs


def _parts_attested(m: dict) -> bool:
    import english
    parts = m.get("parts") or re.findall(r"[A-Za-z]+", m["word"])
    with _ENGLISH_LOCK:
        con = english._con()
        found = english._rows_for(con, [p.lower() for p in parts])
    return all(found.get(p.lower()) for p in parts)


def pick(marks: list[dict], active: bool, family_root: str | None, stand: list[dict] | None = None,
         standing_sense: str | None = None, standing_english: str | None = None, lemma: str | None = None,
         pair_base: str | None = None, min_support: int = 1) -> dict:
    """The owner's order, applied by code to the model's marks: an existing word (or construction of
    real words) carrying sense and image; then a new word carrying both; then a word carrying the sense
    with the image recorded as lost; else the Sanskrit word is kept (preserved). An owner-reviewed
    standing row wins over all of these; a better-tier candidate is reported as a challenger.
    `min_support` is the number of independent marking calls that must have marked a candidate good."""
    stand = stand or []
    forbidden = {f.lower() for s in stand for f in s.get("forbidden", [])}
    standing_words = {e.lower() for s in stand if s.get("policy") == "translate" for e in s.get("english", [])}

    def good(m):
        w = m["word"].lower()
        return (m.get("sense") == 2 and not m.get("misleads") and m.get("register") == "ok" and m.get("idiomatic") is not False
                and m.get("pos_fits") is not False and m.get("attested", True)
                and not any(renders(w, f) for f in forbidden)
                and not re.search(r"\b(and|or)\b", w)
                and len(w.replace("-", " ").split()) <= WORD_MAX)

    def order(ms):
        return sorted(ms, key=lambda m: (m["word"].lower() not in standing_words,
                                         not (pair_base and renders(m["word"], pair_base)),
                                         not (family_root and family_root.lower() in m["word"].lower()),
                                         -(m.get("support") or 1), m.get("rank") or 99))

    def tiers_of(pool):
        ok = [m for m in pool if good(m) and (m.get("kind") != "new" or len(m.get("models") or []) >= 2)]
        old = [m for m in ok if m.get("kind") != "new"]
        new = [m for m in ok if m.get("kind") == "new"]
        return ([("existing, carries sense and image", [m for m in old if m.get("image") == 1], []),
                 ("new word, carries sense and image", [m for m in new if m.get("image") == 1], []),
                 ("existing, carries sense; image lost", old, ["image"])] if active else
                [("existing, carries sense", old, []), ("new word, carries sense", new, [])])

    def best(pool):
        for n, (tier, ms, loss) in enumerate(tiers_of(pool)):
            if ms:
                ms = order(ms)
                return n, tier, ms, loss
        return None

    stable = [m for m in marks if (m.get("support") or 1) >= min_support]
    b = best(stable) or best(marks)
    loose = best(marks)
    challenger = None
    if loose and b and loose[0] < b[0]:  # a single call found a better-tier candidate: the owner sees it
        challenger = {"word": loose[2][0]["word"], "tier": loose[1], "support": loose[2][0].get("support")}

    chosen_row = next((s for s in stand if s["term"] == standing_sense), None)
    if chosen_row is None and len(stand) == 1 and stand[0].get("policy") == "preserve":
        chosen_row = stand[0]
    if chosen_row is not None:
        top = {"word": b[2][0]["word"], "tier": b[1]} if b else None
        if chosen_row.get("policy") == "preserve":
            return {"default": chosen_row.get("iast"), "tier": f"standing {chosen_row['term']}: preserved (owner decision)",
                    "loss": [], "alternates": [], "form": "preserved", "challenger": top}
        eng = list(chosen_row.get("english") or [])
        if eng:
            if standing_english and standing_english.lower() in {e.lower() for e in eng}:
                eng.remove(next(e for e in eng if e.lower() == standing_english.lower()))
                eng.insert(0, standing_english)
            return {"default": eng[0], "tier": f"standing {chosen_row['term']} (owner decision)", "loss": [],
                    "alternates": [e for e in eng[1:4] if " and " not in e], "form": "existing",
                    "challenger": top if top and top["word"].lower() not in {e.lower() for e in eng} else None}
    if b:
        n, tier, ms, loss = b
        return {"default": ms[0]["word"], "tier": tier, "loss": loss, "alternates": [m["word"] for m in ms[1:4]],
                "form": "new" if ms[0].get("kind") == "new" else "existing", "challenger": challenger,
                "support": ms[0].get("support")}
    part = order([m for m in marks if m.get("sense") == 1 and not m.get("misleads")])
    return {"default": lemma, "tier": "preserved: no English word carries the sense (owner's order, step 3)",
            "loss": [], "alternates": [], "form": "preserved", "near": [m["word"] for m in part[:3]]}


MARK_FIELDS = ("sense", "image", "misleads", "register", "idiomatic", "pos_fits")


def merge_marks(anns: list[dict]) -> dict:
    """Majority of independent marking calls. Per candidate, each field takes the value most calls gave
    (a tie takes the stricter value); `support` counts the calls that marked the candidate good."""
    from collections import Counter
    fam_roots = Counter(a.get("family_root") for a in anns if a.get("family_root"))
    out = {"family_root": fam_roots.most_common(1)[0][0] if fam_roots else None, "lemmas": [], "calls": len(anns)}
    by: dict = {}
    for a in anns:
        for l in a.get("lemmas", []):
            for s in l.get("senses", []):
                k = (l.get("lemma"), s.get("sense_id"))
                d = by.setdefault(k, {"standing_sense": [], "standing_english": [], "cands": {}})
                d["standing_sense"].append(s.get("standing_sense"))
                d["standing_english"].append(s.get("standing_english"))
                for m in s.get("marks", []) + s.get("new", []):
                    if m.get("word"):
                        d["cands"].setdefault(m["word"].strip().lower(), []).append(m)
    strict = {"sense": min, "image": min, "misleads": max, "idiomatic": min, "pos_fits": min}
    lemmas: dict = {}
    for (lem, sid), d in by.items():
        marks = []
        for w, ms in d["cands"].items():
            m = {"word": ms[0]["word"], "kind": Counter(x.get("kind") for x in ms).most_common(1)[0][0],
                 "parts": ms[0].get("parts"), "models": ms[0].get("models")}
            for f in MARK_FIELDS:
                c = Counter(json.dumps(x.get(f)) for x in ms).most_common()
                top = [json.loads(v) for v, n in c if n == c[0][1]]
                m[f] = top[0] if len(top) == 1 else (strict[f]([t for t in top if t is not None], default=None)
                                                     if f in strict else top[0])
            ranks = sorted(x["rank"] for x in ms if isinstance(x.get("rank"), (int, float)))
            m["rank"] = ranks[(len(ranks) - 1) // 2] if ranks else None
            m["support"] = sum(1 for x in ms if x.get("sense") == 2 and not x.get("misleads"))
            m["marked_by"] = len(ms)
            marks.append(m)
        ss = Counter(x for x in d["standing_sense"] if x).most_common(1)
        se = Counter(x for x in d["standing_english"] if x).most_common(1)
        lemmas.setdefault(lem, []).append({"sense_id": sid, "standing_sense": ss[0][0] if ss else None,
                                           "standing_english": se[0][0] if se else None, "marks": marks})
    out["lemmas"] = [{"lemma": k, "senses": v} for k, v in lemmas.items()]
    return out


def attest(marks_doc: dict, card: dict) -> None:
    """Every candidate the model added (a word, a construction, a new compound) must be made of real
    English words; a table word must be in its table. Unattested candidates are marked and cannot win."""
    tables = {(L["lemma"], s["sense_id"]): {r["word"].lower() for r in s["table"]} for L in card["lemmas"] for s in L["senses"]}
    for l in marks_doc.get("lemmas", []):
        for s in l.get("senses", []):
            t = tables.get((l["lemma"], s["sense_id"]), set())
            for m in s.get("marks", []):
                if m.get("kind") == "table" and m["word"].lower() in t:
                    continue
                if m.get("kind") == "table":
                    m["kind"] = "word"
                m["attested"] = _parts_attested(m)


def apply_corrections(ann: dict, corrections: list[dict]) -> None:
    for c in corrections or []:
        for l in ann.get("lemmas", []):
            if l.get("lemma") != c.get("lemma"):
                continue
            for s in l.get("senses", []):
                if s.get("sense_id") != c.get("sense_id"):
                    continue
                for m in s.get("marks", []):
                    if m.get("word", "").lower() == (c.get("word") or "").lower() and c.get("field"):
                        m[c["field"]] = c.get("value")


TERM_POLICY = json.loads((ROOT / "data/glossary/term_policy.json").read_text(encoding="utf-8"))["terms"]


def standing(stem: str) -> list[dict]:
    """The owner-reviewed term decisions whose pattern matches this lemma."""
    out = []
    for key, row in TERM_POLICY.items():
        named = any(stem in (s.get("iast_forms") or []) for s in (row.get("senses") or {}).values())
        if named or re.search(row.get("match") or "^$", stem):
            for sid, s in (row.get("senses") or {}).items():
                forms = s.get("iast_forms") or ([s["iast"]] if s.get("iast") else [])
                if s.get("policy") == "preserve" and forms and stem not in forms and not any(stem.startswith(f[:-1]) for f in forms):
                    continue
                out.append({"term": f"{key}.{sid}", "policy": s.get("policy"), "english": (s.get("english") or [])[:4],
                            "iast": stem if stem in (s.get("iast_forms") or []) else s.get("iast"), "forbidden": s.get("forbidden_english") or [],
                            "note": (s.get("note") or "")[:500]})
    return out


def standing_exact(stem: str) -> bool:
    """A standing row names this exact word (kūṭastha), not only one of its members."""
    for row in TERM_POLICY.values():
        for s in (row.get("senses") or {}).values():
            if stem in (s.get("iast_forms") or []) or stem == s.get("iast"):
                return True
    return False


NEG_PREFIXES = ("a", "an", "apa", "ava", "nir", "niḥ", "dur", "duḥ")
ANNOTATE_CALLS = int(os.environ.get("GITA_ANNOTATE_CALLS", "3"))


def pair_of(stem: str, family: list[str]) -> str | None:
    """apamāna -> māna, aśubha -> śubha: the opposite of another lemma of the family keeps its English base."""
    for p in NEG_PREFIXES:
        if stem.startswith(p) and stem[len(p):] in family:
            return stem[len(p):]
    return None


def english_opposite(word: str) -> str | None:
    """The English negative of a word, if the dictionaries have it (honour -> dishonour)."""
    import english
    if " " in word:
        return None
    with _ENGLISH_LOCK:
        con = english._con()
        for pre in ("dis", "un", "in", "im", "ir", "il"):
            cand = pre + word.lower()
            if english._rows_for(con, [cand]).get(cand):
                return cand
    return None


def senses_of(stem: str, entry: dict) -> tuple[list[dict], dict]:
    """One call: the senses of one lemma from its Sanskrit card. A sense must be used at a place of the
    Gītā (the root's picture is never a sense by itself); each place belongs to one sense."""
    import evidence
    with _ENGLISH_LOCK:
        scard = evidence.sanskrit_card(entry)
    s, st = call("senses", scard)
    senses = [x for x in (s or {}).get("senses", []) if x.get("sense")]
    if len(senses) > 1:
        senses = [x for x in senses if x.get("occurrences")] or senses[:1]
    seen: set = set()
    for x in senses:
        x["occurrences"] = [o for o in x.get("occurrences") or [] if not (o in seen or seen.add(o))]
    return senses, st


def table_for(sense: dict, entry: dict) -> tuple[list[dict], dict]:
    """English candidates found by code: reverse dictionary on the core sense, its range and the image;
    words sharing the Sanskrit root through PIE; words whose etymon pictures the image."""
    rows = etable(sense["sense"], sense.get("image"), 22)
    have = {r["word"] for r in rows}
    for q, n in ((sense.get("range"), 12), (sense.get("image"), 8)):
        if q:
            rows += [r for r in etable(q, None, n) if r["word"] not in have]
            have = {r["word"] for r in rows}
    table = [{k: v for k, v in r.items() if k not in ("via", "fit")} for r in rows]
    roots, none = roots_rows(entry.get("root"), entry.get("upasargas"), sense.get("image"))
    table += [r for r in roots if r["word"] not in have]
    return table, none


def lexicon_family(fam: str, members: dict, outdir: Path) -> dict:
    rec = {"family": fam, "calls": [], "lemmas": {}}
    with ThreadPoolExecutor(len(members)) as ex:
        got = list(ex.map(lambda kv: (kv[0], senses_of(kv[0], kv[1])), members.items()))
    for stem, (senses, st) in got:
        rec["calls"].append(st)
        rec["lemmas"][stem] = {"senses": senses}
    card = {"family": fam, "lemmas": []}
    for stem, L in rec["lemmas"].items():
        senses = []
        for sense in L["senses"]:
            table, none = table_for(sense, members[stem])
            senses.append({"sense_id": sense["sense_id"], "sense": sense["sense"], "range": sense.get("range"),
                           "root_search_empty": none, "image": sense.get("image"),
                           "image_active": bool(sense.get("image")) and not sense.get("image_dead"), "table": table})
        card["lemmas"].append({"lemma": stem, "word_class": members[stem].get("kinds"), "standing": standing(stem),
                               "opposite_of": pair_of(stem, list(members)), "senses": senses})
    # Two independent marking calls; a third only when the two lead code to different choices
    # (throughput, not parallelism, bounds wall time: calls are the cost).
    with ThreadPoolExecutor(2) as ex:
        got2 = list(ex.map(lambda _: call("annotate", card), range(2)))
    anns = [a for a, _ in got2 if a]
    rec["calls"] += [st for _, st in got2]

    def outcome(doc):
        attest(doc, card)
        return {(l["lemma"], s["sense_id"]): pick(s.get("marks", []), True, doc.get("family_root"),
                                                  next((L.get("standing") for L in card["lemmas"] if L["lemma"] == l["lemma"]), []),
                                                  s.get("standing_sense"), s.get("standing_english"), l["lemma"]).get("default")
                for l in doc.get("lemmas", []) for s in l.get("senses", [])}
    if len(anns) < 2 or outcome(merge_marks(anns[:1])) != outcome(merge_marks(anns[1:2])):
        a3, st = call("annotate", card)
        rec["calls"].append(st)
        anns += [a3] if a3 else []
    ann = merge_marks(anns)
    attest(ann, card)
    need = 2 if len(anns) >= 2 else 1

    def decide():
        out = {}
        family = list(members)
        stand_first = {L["lemma"] for L in card["lemmas"] if L.get("standing")}
        order_ = sorted(ann.get("lemmas", []), key=lambda l: (pair_of(l["lemma"], family) is not None,
                                                              l["lemma"] not in stand_first))
        for l in order_:
            L = next((x for x in card["lemmas"] if x["lemma"] == l.get("lemma")), None)
            if not L:
                continue
            base = pair_of(l["lemma"], family)
            base_en = next((v["default"] for k, v in out.items() if k[0] == base and v.get("form") == "existing"), None)
            fam_en = next((v["default"] for k, v in out.items() if k[0] != l["lemma"] and v.get("form") == "existing"
                           and (v.get("tier") or "").startswith("standing")), None)
            for s in l.get("senses", []):
                src = next((x for x in L["senses"] if x["sense_id"] == s.get("sense_id")), None)
                if src:
                    ch = pick(s.get("marks", []), src["image_active"], ann.get("family_root"),
                              L.get("standing"), s.get("standing_sense"),
                              s.get("standing_english"), l["lemma"], base_en or fam_en, need)
                    if base_en and not (ch.get("tier") or "").startswith("standing") and not renders(ch.get("default") or "", base_en):
                        opp = english_opposite(base_en)
                        if opp:
                            ch = {**ch, "alternates": [ch["default"], *ch.get("alternates", [])][:4], "default": opp,
                                  "tier": f"opposite of {base} '{base_en}' (English pair)", "form": "existing"}
                    out[(l["lemma"], s["sense_id"])] = ch
        return out

    picks = decide()
    rv, st = call("review_marks", {**card, "marks": ann, "chosen": {f"{k[0]} / {k[1]}": v for k, v in picks.items()}})
    rec["calls"].append(st)
    corrections = (rv or {}).get("corrections", [])
    if corrections:
        apply_corrections(ann, corrections)
        picks = decide()
    rec.update({"card": card, "marks": ann, "corrections": corrections,
                "choices": [{"lemma": k[0], "sense_id": k[1], **v,
                             "sense": next(x for L in card["lemmas"] if L["lemma"] == k[0] for x in L["senses"] if x["sense_id"] == k[1]),
                             "occurrences": next((x.get("occurrences", []) for x in rec["lemmas"][k[0]]["senses"] if x["sense_id"] == k[1]), [])}
                            for k, v in picks.items()]})
    safe = fam.replace("/", "_").replace("√", "root-")
    (outdir / f"{safe}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


def resolve_collisions(recs: list[dict]) -> list[str]:
    """One English default may not render two different lemmas: the worse-ranked takes its next alternate."""
    notes, owner, term_of = [], {}, {}
    for r in recs:
        for c in r.get("choices", []):
            d = (c.get("default") or "").lower()
            if not d:
                continue
            term = (c.get("tier") or "").split()[1] if (c.get("tier") or "").startswith("standing") else None
            if d in owner and term and term_of.get(d) == term:
                continue  # forms of one owner-decided term (paryupās / upās) share it by design
            term_of.setdefault(d, term)
            if d in owner and owner[d] != c["lemma"]:
                if c.get("alternates"):
                    new = c["alternates"].pop(0)
                    notes.append(f"'{d}' already renders {owner[d]}; {c['lemma']} takes '{new}'")
                    c["default"] = new
                    owner[new.lower()] = c["lemma"]
                else:
                    notes.append(f"'{d}' renders both {owner[d]} and {c['lemma']}; no alternate — review")
            else:
                owner[d] = c["lemma"]
    return notes


def consistency(recs: list[dict]) -> list[str]:
    seen: dict[str, str] = {}
    out = []
    for r in recs:
        for c in r.get("choices", []):
            d = ((c.get("choice") or {}).get("default") or "").lower()
            if d and d in seen and seen[d] != r["lemma"]:
                out.append(f"'{d}' renders both {seen[d]} and {r['lemma']}")
            seen.setdefault(d, r["lemma"])
    return out


# ---------------------------------------------------------------- verse
def lexicon_index(run: str) -> dict:
    """(stem, locus) -> {default, alternates, sense}; stem -> first sense as fallback."""
    idx = {}
    for f in (RUNS / run / "lexicon2").glob("*.json"):
        if f.name == "summary.json":
            continue
        r = json.loads(f.read_text())
        for c in r.get("choices", []):
            if not c.get("default"):
                continue
            v = {"default": c["default"], "alternates": c.get("alternates", []), "sense": c["sense"]["sense"]}
            idx.setdefault(c["lemma"], v)
            for loc in c.get("occurrences", []):
                idx[(c["lemma"], loc)] = v
    return idx


def gram_of(locus: str, w: dict) -> str | None:
    if w.get("manual"):
        return (w["manual"] or {}).get("gram")
    p = C.verse_packet(locus)
    for a in p["forms"].get(w["form"], {}).get("analyses", []):
        if a.get("id") == w.get("analysis_id"):
            return a.get("gram")
    return None


def whole_word_stems(cons: dict) -> set[str]:
    """Compounds decided as one word: negative (nañ) compounds and those a standing row names."""
    pos = positions(cons)
    out = set()
    for c in cons.values():
        for w in c["words"]:
            first = ((w.get("members") or [{}])[0].get("stem") or "").strip("-")
            stem = pos.get((c["locus"], w["i"]), {}).get("word") or w.get("stem")
            ctype = ((w.get("compound") or {}).get("type") or "").lower()
            upasarga = (w.get("members") or [{}])[0].get("word_class") == "particle" and re.match(r"(gati|prādi)", ctype)
            if stem and (first in ("a", "an", "nañ", "na") or upasarga):
                out.add(stem)
    return out


def positions(cons: dict) -> dict:
    """(locus, i) -> the lexicon's lemma for the whole word and for its members (same normalisation
    the lexicon used: pari-upa-ās -> paryupās)."""
    import evidence
    pos: dict = {}
    for stem, e in evidence.lemmas_from_construals(list(cons.values())).items():
        member = "member" in (e.get("kinds") or [])
        for p in e["places"]:
            d = pos.setdefault((p["locus"], p["i"]), {"word": None, "members": []})
            if member:
                d["members"].append(stem)
            else:
                d["word"] = stem
    return pos


def forbidden_for(stem: str, english: str | None) -> list[str]:
    """Forbidden renderings of the standing sense actually used (the row whose English or kept term is
    this English); when no row's English is used, all rows' forbidden words apply."""
    rows = standing(stem)

    def own(s):
        return {e.lower() for e in s.get("english", [])} | ({s["iast"].lower()} if s.get("iast") else set())
    used = [s for s in rows if english and english.lower() in own(s)]
    rows = used or rows
    mine = set().union(*[own(s) for s in rows]) if rows else set()
    return sorted({f for s in rows for f in s.get("forbidden", []) if f.lower() not in mine})


CASES = ("prathamā", "dvitīyā", "tṛtīyā", "caturthī", "pañcamī", "ṣaṣṭhī", "saptamī", "sambodhana")
RELEASE = ("mukta", "vimukta", "vinirmukta", "rahita", "hīna", "vihīna", "varjita", "vivarjita", "viyukta", "apeta",
           "vigata", "vihīna", "śūnya")
THINK_KTA = ("mata", "iṣṭa", "jñāta", "vidita", "pūjita", "sammata", "abhimata")
ABLE = ("samartha", "śakta", "kuśala", "kṣama")
COMPARE = ("śreyas", "viśiṣ", "adhika", "garīyas", "jyāyas", "tara", "anya", "ṛte")
CASE_EN = {"prathamā": "subject or predicate (no preposition)",
           "dvitīyā": "object of the verb or agent noun (no preposition; 'X-er of' with an agent noun)",
           "tṛtīyā": "'by' (agent of a passive) or 'with/by' (instrument, accompaniment)",
           "caturthī": "'for' or 'to' (purpose, recipient)",
           "pañcamī": "'from' (source, separation, cause of fear)",
           "ṣaṣṭhī": "'of' or the possessive; 'to' with words of dearness and relation ('dear to me')",
           "saptamī": "'in', 'on' or 'into' (with verbs of placing: 'set in me', 'fixed on me'); 'among'",
           "sambodhana": "address ('O ...' or a plain vocative set off by commas)"}


def case_hint(grammar: str | None, head_stem: str | None) -> str | None:
    """How English marks this word's case relation, decided by code from the case and its head."""
    g = (grammar or "").split(";")[0]
    case = next((c for c in CASES if c in g), None)
    if not case:
        return None
    h = head_stem or ""
    if case in ("tṛtīyā", "pañcamī") and any(h.endswith(r) for r in RELEASE):
        return "'from': the head is a word of release or lack ('freed from', 'devoid of' for -varjita)"
    if case == "pañcamī" and any(r in h for r in COMPARE):
        return "'than' or 'above': the head is a comparative ('better than')"
    if case == "ṣaṣṭhī" and h.startswith("priy"):
        return "'to': 'dear to me'"
    if case == "ṣaṣṭhī" and any(h.endswith(x) for x in THINK_KTA):
        return "'by': the agent of a past participle of thinking or knowing ('deemed by me')"
    if case == "saptamī" and any(h.endswith(x) for x in ABLE):
        return "'of' or 'at': the sphere of an ability ('capable of')"
    return CASE_EN[case]


def compound_pattern(ctype: str | None, last: str | None = None) -> str | None:
    """The English shape of a compound built from its members' decided English, by compound type
    (and by its last member where that decides the preposition)."""
    t = (ctype or "").lower()
    outer = re.split(r"[;—,(]", t)[0]
    if not t:
        return None
    if "nañ" in outer and "bahuvrīhi" not in outer:
        return "negative: the established English negative of the member ('inconceivable', not 'unconceivable'), or 'not'/'without'"
    if "dvandva" in outer and "bahuvrīhi" not in outer:
        return "coordination: the members joined by 'and' ('X and Y'; 'X, Y and Z')"
    if "bahuvrīhi" in outer:
        return ("possessive: describes one who HAS it — an English -ed compound where English has one "
                "('self-restrained', 'firm-minded'), else 'with X Y' or 'whose X is Y'; never a bare noun phrase 'X Y'")
    if last and any(last.endswith(r) for r in RELEASE):
        return "release or lack: 'free from X', 'devoid of X', 'X gone' — never 'by'"
    if "upapada" in outer:
        return ("agent with its object or place, as the word's class needs: an agent noun 'Y-er of X' ('knower of "
                "the field'), or an adjective 'Y-ing X' / 'X-Y-ing'")
    for case, en in (("ṣaṣṭh", "'the Y of X' or 'X's Y' (the last member is the head)"), ("saptam", "'Y in X'"),
                     ("tṛtīy", "'Y by X' or 'Y with X'"), ("caturth", "'Y for X'"), ("pañcam", "'Y from X'"),
                     ("dvitīy", "'Y X' with X as object ('gone beyond X')")):
        if case in outer:
            return en
    if "karmadhāraya" in outer:
        return ("the first member describes the second: an adjective first gives 'X Y' ('the highest goal'); a NOUN "
                "first gives 'the Y of X' or 'the Y that is X' — never a noun pile like 'knowledge sacrifice'")
    return "the members in English order, last member the head; never a bare noun pile"


CLOSED_EN = {"asmad": "my", "mad": "my", "mat": "my", "yuṣmad": "your", "tvad": "your", "tvat": "your", "sarva": "all",
             "tad": "that", "etad": "this", "idam": "this", "sva": "own", "eka": "one", "ud": None}


def member_english(w: dict, lex_members: list[str], idx: dict, loc: str) -> list[dict]:
    """The members of a compound (or the padas of a sandhi-joined token) with their decided English.
    The construal's member list is the authority; the lexicon gives content members' English, a code
    table gives closed-class members' (sarva 'all', asmad 'my'); upasargas are part of their word."""
    padas = (w.get("manual") or {}).get("padas")
    src = padas or w.get("members") or []
    out = []
    for m in src:
        stem = (m.get("stem") or "").strip("-")
        if m.get("word_class") == "particle" and stem not in CLOSED_EN:
            continue
        lemma = next((x for x in lex_members if x == stem), None) or next((x for x in lex_members if stem and (x.endswith(stem) or stem.endswith(x))), stem)
        row = idx.get((lemma, loc)) or idx.get(lemma) or {}
        en = row.get("default") or CLOSED_EN.get(stem)
        d = {"stem": stem, "english": en, "alternates": row.get("alternates") or []}
        if padas:
            d["grammar"] = m.get("gram")
        out.append(d)
    return out


def unit_card(unit: list[str], cons: dict, idx: dict, pos: dict | None = None) -> dict:
    pos = pos if pos is not None else positions(cons)
    whole = whole_word_stems(cons)
    verses = []
    for loc in unit:
        c = cons[loc]
        words = []
        for w in c["words"]:
            p = pos.get((loc, w["i"]), {"word": None, "members": []})
            stem = p["word"] or w.get("stem")
            own = idx.get((stem, loc)) or idx.get(stem)
            lex = own if (not w.get("members") or standing_exact(stem or "") or stem in whole) else None
            members = [] if lex else member_english(w, p["members"], idx, loc)
            head = (w.get("relation") or {}).get("head")
            head_stem = (pos.get((loc, head), {}).get("word") or next((x.get("stem") for x in c["words"] if x["i"] == head), None)) \
                if isinstance(head, int) else None
            grammar = gram_of(loc, w)
            words.append({"i": w["i"], "form": w["form"], "class": w.get("word_class"), "grammar": grammar,
                          "english_case": case_hint(grammar, head_stem),
                          "compound_pattern": (compound_pattern(("bahuvrīhi (-vat/-mat: having)" if re.search(r"(vat|mat)$", stem or "") else
                                                                 (w.get("compound") or {}).get("type")), (members[-1]["stem"] if members else None))
                                               if not lex and members and not (w.get("manual") or {}).get("padas") else
                                               "two words joined by sandhi: render each by its own grammar" if members else None),
                          "light_verb": stem == "kṛ" or None,
                          "depends_on": (w.get("relation") or {}).get("head"), "relation": (w.get("relation") or {}).get("role"),
                          "compound": (w.get("compound") or {}).get("type"),
                          "english": lex and {"default": lex["default"], "alternates": lex["alternates"]},
                          "forbidden": sorted(set(forbidden_for(stem or "", lex and lex["default"]))
                                              | {f for m in members for f in forbidden_for(m["stem"], m["english"])}),
                          "members": members or None})
        verses.append({"locus": loc, "iast": C.verse_packet(loc)["iast"], "words": words,
                       "referents": c.get("referents", []),
                       "forks": [f for f in c.get("forks", []) if f.get("kind") in check.GRAMMATICAL_FORKS]})
    return {"unit": unit, "verses": verses}


EN_FUNCTION = {"the", "a", "an", "of", "to", "in", "on", "by", "with", "from", "is", "are", "be", "who", "which", "that", "for"}
_SUFFIX = re.compile(r"(ments?|ings?|ers?|ions?|ness|edly|ed|es|s|ly)$")


def _en_stem(w: str) -> str:
    w = w.lower().strip("’'")
    r = _SUFFIX.sub("", w)
    return r if len(r) >= 3 else w


def renders(text: str, option: str) -> bool:
    """`text` renders `option` when every content word of the option appears in it in some English form
    of the same word (relinquishment / relinquish / relinquisher; shrink / shrinks)."""
    toks = [_en_stem(t) for t in re.findall(r"[\w’'-]+", (text or "").lower())]
    toks += [_en_stem(x) for t in re.findall(r"[\w’'-]+", (text or "").lower()) for x in t.split("-")]
    need = [_en_stem(t) for t in re.findall(r"[\w’'-]+", (option or "").lower()) if t not in EN_FUNCTION]
    def hit(n):
        return any(t == n or (min(len(t), len(n)) >= 5 and (t.startswith(n) or n.startswith(t))) for t in toks)
    if not need:
        return bool(option) and option.lower() in (text or "").lower()
    return all(hit(n) for n in need)


def check_line(out: dict, card: dict) -> list[str]:
    inp = {"verses": [{"locus": v["locus"], "construal": {"forks": v["forks"], "words": [
        {"i": w["i"], "form": w["form"], "word_class": w["class"]} for w in v["words"]]}} for v in card["verses"]]}
    errs = check.verse({**out, "words": [{**w, "sense_id": None} for w in out.get("words", [])]}, inp, {})
    errs = [e for e in errs if "W6" not in e]
    cardw = {(v["locus"], w["i"]): w for v in card["verses"] for w in v["words"]}
    for w in out.get("words", []):
        cw = cardw.get((w.get("locus"), w.get("i")))
        if not cw:
            continue
        text = w.get("english") or ""
        if cw.get("english"):
            opts = [cw["english"]["default"], *cw["english"].get("alternates", [])]
            shared = cw.get("light_verb") and any(x is not w and (x.get("english") or "").lower() == text.lower()
                                                  for x in out.get("words", []))
            if not shared and not any(o and renders(text, o) for o in opts):
                errs.append(f"{w['locus']} word {w['i']} ({cw['form']}): '{text}' is not the decided English {opts} "
                            "in any form (W6)")
        for m in cw.get("members") or []:
            if m.get("english") and not any(renders(text, o) for o in [m["english"], *m.get("alternates", [])]):
                errs.append(f"{w['locus']} word {w['i']} ({cw['form']}): member {m['stem']} is decided as "
                            f"'{m['english']}' and is missing from '{text}' (W6)")
        for f in cw.get("forbidden") or []:
            if re.search(rf"\b{re.escape(f.lower())}\b", text.lower()):
                errs.append(f"{w['locus']} word {w['i']}: '{f}' is forbidden for this word by the owner's term policy")
    return errs


REVISIONS = 2


def verse_one(unit: list[str], cons: dict, idx: dict, outdir: Path, pos: dict | None = None) -> dict:
    """Line, code check, independent review; up to REVISIONS rounds of revision, each re-checked by code
    and re-reviewed (the re-review verifies the earlier findings and reports only real new errors)."""
    card = unit_card(unit, cons, idx, pos)
    rec = {"unit": unit, "calls": [], "rounds": []}
    out, st = call("line", card)
    rec["calls"].append(st)
    prior = None
    for rnd in range(REVISIONS + 1):
        errs = check_line(out or {}, card)
        extra = "" if prior is None else ("\n\nRE-REVIEW. The line was revised after these findings: "
                                          + json.dumps(prior, ensure_ascii=False)
                                          + "\nFor each, say whether it is fixed. Report a NEW finding only if it is an "
                                          "adds, drops or grammar error, or a stumble a reader would trip on.")
        rv, st = call("review_line", {**card, "line": out}, extra)
        rec["calls"].append(st)
        findings = [f for f in (rv or {}).get("findings", []) if f.get("kind")]
        rec["rounds"].append({"line": out, "code_errors": errs, "review": findings})
        if (not errs and not findings) or rnd == REVISIONS:
            break
        extra = ("\n\nREVISION. Your previous answer is under PREVIOUS; code errors and a reviewer's findings are under "
                 "FINDINGS. Fix every code error; adopt each finding's fix unless it breaks a rule above (say which in "
                 "\"declined\"). Return the same JSON.\nPREVIOUS: "
                 + json.dumps(out, ensure_ascii=False) + "\nFINDINGS: " + json.dumps({"code": errs, "review": findings}, ensure_ascii=False))
        out2, st = call("line", card, extra)
        rec["calls"].append(st)
        out = out2 or out
        prior = {"code": errs, "review": findings}
    rec.update({"card": card, "output": out, "code_errors": rec["rounds"][-1]["code_errors"],
                "review": rec["rounds"][-1]["review"]})
    (outdir / f"{'-'.join(unit)}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


def sheet(run: str) -> Path:
    """The owner's decision sheet: every rendering code chose with a recorded loss, a coinage, a kept
    Sanskrit word because no English carried the sense, or a challenger to a standing decision."""
    rows = []
    for f in sorted((RUNS / run / "lexicon2").glob("*.json")):
        if f.name == "summary.json":
            continue
        for c in json.loads(f.read_text()).get("choices", []):
            why = []
            if c.get("challenger"):
                why.append(f"challenger: {c['challenger']['word']} ({c['challenger']['tier']})")
            if "image" in (c.get("loss") or []):
                why.append(f"image lost: {c['sense'].get('image')}")
            if (c.get("tier") or "").startswith("preserved"):
                why.append("kept in Sanskrit: no English word carries the sense" + (f" (nearest: {', '.join(c['near'])})" if c.get("near") else ""))
            if c.get("form") == "new":
                why.append("new English word")
            if why:
                loci = [o for o in c.get("occurrences", []) if o.startswith(run.split("-")[0].replace("ch", "") + ".")] or c.get("occurrences", [])[:3]
                rows.append(f"| {c['lemma']} | {c['sense']['sense']} | **{c['default']}** | {', '.join(c.get('alternates') or [])} | "
                            f"{'; '.join(why)} | {', '.join(loci[:4])} |")
    out = RUNS / run / "DECISIONS.md"
    out.write_text("# Owner decision sheet\n\nEach row: code's choice by the owner's order, and why it needs a look. "
                   "Answer by row: keep, take an alternate, or give a word.\n\n| lemma | sense | chosen | alternates | why | where |\n"
                   "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["lexicon", "verse", "sheet"])
    ap.add_argument("--run", default="ch12-qual")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--jobs", type=int, default=40)
    a = ap.parse_args()
    if a.stage == "sheet":
        print(sheet(a.run))
        return 0
    import evidence
    cons = [json.loads(p.read_text()) for p in (RUNS / a.run / "construe").glob("*/output.json")]
    if a.stage == "lexicon":
        lem = evidence.lemmas_from_construals(cons)
        whole = whole_word_stems({c["locus"]: c for c in cons})
        todo = {k: v for k, v in lem.items() if (not a.only or k in a.only)
                and (standing_exact(k) or k in whole or not any("samāsa" in str(x) for x in (v.get("kinds") or [])))}
        fams: dict[str, dict] = {}
        for k, v in todo.items():
            fams.setdefault(v.get("root") or k, {})[k] = v
        outdir = RUNS / a.run / "lexicon2"
        outdir.mkdir(parents=True, exist_ok=True)
        t = time.time()
        with ThreadPoolExecutor(a.jobs) as ex:
            recs = list(ex.map(lambda kv: lexicon_family(kv[0], kv[1], outdir), fams.items()))
        notes = resolve_collisions(recs)
        for r in recs:
            safe = r["family"].replace("/", "_").replace("√", "root-")
            (outdir / f"{safe}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        calls = [c for r in recs for c in r["calls"]]
        summ = {"lemmas": len(recs), "wall_s": round(time.time() - t), "calls": len(calls),
                "call_s_median": sorted(c["s"] for c in calls)[len(calls) // 2] if calls else None,
                "commands_run": sum(c["commands"] for c in calls), "tokens": sum(c["tokens"] for c in calls),
                "unresolved": [f"{c['lemma']}/{c['sense_id']}" for r in recs for c in r["choices"] if not c.get("default")],
                "image_lost": [f"{c['lemma']}/{c['sense_id']}" for r in recs for c in r["choices"] if "image" in c.get("loss", [])],
                "collisions": notes}
        (outdir / "summary.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1))
        print(json.dumps(summ, ensure_ascii=False))
    else:
        bylocus = {c["locus"]: c for c in cons}
        idx = lexicon_index(a.run)
        units = [u for u in C.units(cons) if not a.only or set(u) & set(a.only)]
        outdir = RUNS / a.run / "verse2"
        outdir.mkdir(parents=True, exist_ok=True)
        t = time.time()
        pos = positions(bylocus)
        with ThreadPoolExecutor(a.jobs) as ex:
            recs = list(ex.map(lambda u: verse_one(u, bylocus, idx, outdir, pos), units))
        calls = [c for r in recs for c in r["calls"]]
        summ = {"units": len(recs), "wall_s": round(time.time() - t), "calls": len(calls),
                "commands_run": sum(c["commands"] for c in calls), "tokens": sum(c["tokens"] for c in calls),
                "code_errors_left": {"-".join(r["unit"]): r["code_errors"] for r in recs if r["code_errors"]},
                "review_left": {"-".join(r["unit"]): r["review"] for r in recs if r["review"]},
                "rounds": {"-".join(r["unit"]): len(r["rounds"]) for r in recs}}
        (outdir / "summary.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1))
        print(json.dumps(summ, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

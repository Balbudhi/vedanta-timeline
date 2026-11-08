"""Stage A: verse packets, the Gītā-wide lemma inventory, concordance, meaning pages, shard
plan and the private translations files (plan §7.3; SCHEMAS.md amendments).

Packets hold no published translation: the BORI text, the oracle's split candidates,
analyses and derivations, and the Sanskrit commentators' glosses (lookup.py `gloss`). The
translations go only to `secondaries/CH.json`, read by review jobs.
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import defaultdict
from functools import lru_cache

from . import common as C
from . import names as N
from . import oracle as O
from . import store as S

_W: dict = {}          # per-process worker state


def _packet_builder():
    """scripts/build_gita_chapter_packet.py (BORI, Devanāgarī, sentence units, partition)."""
    import sys
    p = str(C.ROOT / "scripts")
    if p not in sys.path:
        sys.path.append(p)
    import build_gita_chapter_packet as P  # noqa: E402
    return P


def _lookup_cached():
    lk = C.import_lookup()
    if not getattr(lk.gita_gita_tables, "_gp_cached", False):
        f = lru_cache(maxsize=1)(lk.gita_gita_tables)
        f._gp_cached = True
        lk.gita_gita_tables = f
    return lk


def worker_init(fixture: str | None, without_grammar: bool) -> None:
    if without_grammar:
        _W["oracle"] = _GrammarOff()
    else:
        _W["oracle"] = O.FixtureOracle(fixture) if fixture else O.KitOracle(need_grammar=True, need_meaning=False)
    _W["lookup"] = _lookup_cached()
    _W["builder"] = C.import_builder()


class _GrammarOff(O.Oracle):
    def _analyze(self, form):
        return []

    def _derive(self, a):
        return None

    def _split(self, locus):
        return []


# ---------------------------------------------------------------- exact helpers
SYL = re.compile(r"ai|au|[aāiīuūṛṝḷeo]")


def meter_of(iast: str) -> dict:
    lines = [l for l in iast.replace("||", "|").split("|") if l.strip()]
    counts = [len(SYL.findall(l)) for l in lines]
    total = sum(counts)
    name = {32: "anuṣṭubh", 44: "triṣṭubh", 48: "jagatī"}.get(total, f"mixed ({total} syllables)")
    return {"name": name, "syllables_per_line": counts}


def align_groups(builder, samhita_iast: str, padas: list[str], max_group: int = 4) -> list[int] | None:
    """For each pada, the index of the BORI saṃhitā token it falls in (the builder's alignment),
    or None when the padas do not recompose to the saṃhitā."""
    sam = builder.samhita_tokens(samhita_iast)
    keys = [C.latin_key(p) for p in padas]
    m, n = len(sam), len(keys)
    back: dict[tuple[int, int], tuple[int, int]] = {}
    reach = {(0, 0)}
    for i in range(m):
        for j in range(n + 1):
            if (i, j) not in reach:
                continue
            for g in range(1, max_group + 1):
                if j + g <= n and builder.group_matches(keys[j:j + g], *sam[i]) and (i + 1, j + g) not in reach:
                    reach.add((i + 1, j + g))
                    back[(i + 1, j + g)] = (i, j)
    if (m, n) not in reach:
        return None
    out = [0] * n
    cur = (m, n)
    while cur != (0, 0):
        prev = back[cur]
        for j in range(prev[1], cur[1]):
            out[j] = prev[0]
        cur = prev
    return out


def lemma_records(an: dict) -> dict | None:
    """The lemma an analysis names: {key, lemma, root, page_lemma, content}."""
    d = an.get("dhatu") or {}
    root = d.get("root")
    kind = an.get("kind")
    if kind == "tinanta" and root:
        ups = [u for u in (d.get("upasargas") or []) if isinstance(u, str)]
        lemma = "-".join(ups + [f"√{root}"])
        page_lemma = root
    else:
        lemma = an.get("stem") or an.get("form")
        page_lemma = lemma
    if not lemma:
        return None
    wc = N.word_class(an)
    return {"key": f"{C.nfc(lemma)}|{C.nfc(root or '')}", "lemma": C.nfc(lemma), "root": C.nfc(root) if root else None,
            "page_lemma": C.nfc(page_lemma), "content": wc in ("content", "copula") and wc != "copula"}


# ---------------------------------------------------------------- one verse (worker)
def verse_packet(rec: dict) -> dict:
    t0 = time.perf_counter()
    orc, lk, builder = _W["oracle"], _W["lookup"], _W["builder"]
    P = _packet_builder()
    locus = rec["locus"]
    iast = rec["iast"]
    toks = P.bori_tokens(iast)
    try:
        gl = lk.gloss_lookup(locus)
        gl_padas = gl.get("padas") or []
        gloss_error = None
    except BaseException as e:  # noqa: BLE001 - lookup raises SystemExit on a missing verse
        gl_padas, gloss_error = [], f"{type(e).__name__}: {e}"
    tokens = []
    for k, tok in enumerate(toks):
        g = gl_padas[k] if k < len(gl_padas) and gl_padas[k].get("pada") == tok else next((x for x in gl_padas if x.get("pada") == tok), None)
        tokens.append({"i": k, "token": tok,
                       "glosses": [{"who": h.get("author"), "locus": h.get("locus"), "text": h.get("clause"), "match": h.get("match")}
                                   for h in (g or {}).get("glosses", [])],
                       "authors_without_match": (g or {}).get("authors_without_match", [])})
    cands = []
    for c in orc.split(locus):
        groups = align_groups(builder, iast, c["tokens"])
        cands.append({**c, "recomposes_bori": groups is not None, "bori_token_of_pada": groups})
    forms: dict[str, dict] = {}
    new_rows: list = []

    def add_form(form: str, role: str):
        fk = C.form_key(form)
        if not fk or fk in forms:
            if fk in forms and role not in forms[fk]["roles"]:
                forms[fk]["roles"].append(role)
            return
        ans, err = [], None
        try:
            got = orc.analyze(form.replace("-", ""))
        except O.OracleError as e:
            got, err = [], str(e)
        for a in got:
            try:
                d = orc.derive(a)
            except O.OracleError as e:
                d = {"analysis_id": a.get("id"), "matches": False, "steps": [], "error": str(e)}
            ans.append({**a, "derivation": d})
        forms[fk] = {"form": form, "roles": [role], "analyses": ans, **({"error": err} if err else {})}
        if ans:
            new_rows.extend((a["id"], fk, {k: v for k, v in a.items() if k != "derivation"}, S.compact_derivation(a["derivation"]))
                            for a in ans)

    for c in cands:
        for t in c["tokens"]:
            add_form(t, "pada")
            if "-" in t:
                for mem in t.split("-"):
                    add_form(mem, "member")
    for f in list(forms.values()):          # compound members the oracle names
        for a in f["analyses"]:
            for m in a.get("members") or []:
                mf = m if isinstance(m, str) else (m.get("form") or m.get("stem") or m.get("pausal")) if isinstance(m, dict) else None
                if mf:
                    add_form(mf, "member")
    primary = next((c for c in cands if c["recomposes_bori"]), None)
    occ = []
    if primary:
        for i, t in enumerate(primary["tokens"]):
            recs = {}
            for a in forms[C.form_key(t)]["analyses"]:
                r = lemma_records(a)
                if r:
                    recs.setdefault(r["key"], {**r, "analysis_ids": []})["analysis_ids"].append(a["id"])
            fa = forms[C.form_key(t)]["analyses"]
            has_function = any(N.word_class(a) in ("pronoun", "particle", "copula") for a in fa)
            occ.append({"i": i, "form": t, "bori_token": primary["bori_token_of_pada"][i], "lemmas": list(recs.values()),
                        "function_reading": has_function})
    deva = P.devanagari_from_iast(iast)
    gloss_key = frozenset(C.latin_key(x) for t in tokens for g in t["glosses"]
                          for x in re.split(r"[\s\-—–,;:.|।॥()]+", lk.to_iast(g["text"] or "")) if C.latin_key(x))
    return {
        "schema": C.SCHEMA_PACKET, "locus": locus, "chapter": int(locus.split(".")[0]), "verse": int(locus.split(".")[1]),
        "speaker": rec.get("speaker"), "speaker_line": rec.get("speaker_line"), "mbh": rec.get("mbh"),
        "iast": iast, "devanagari": deva, "bori_loci": rec.get("loci"), "meter": meter_of(iast),
        "tokens": tokens, "gloss_error": gloss_error,
        "split_candidates": cands, "primary_split": primary["id"] if primary else None,
        "forms": {fk: ranked_form(f, gloss_key) for fk, f in forms.items()},
        "occurrences": occ,
        "analysis_store": "internal/gita_pipeline/packets/analyses.sqlite (full Analysis and Derivation by id)",
        "oracle": orc.identity().get("oracle"), "seconds": round(time.perf_counter() - t0, 3),
    }, new_rows


SHOWN = 8
ROOT_NOUN_KRT = {"kvip", "vic", "kvin", "ṇvi", "viṭ", "kvasu"}


def ranked_form(f: dict, gloss_key: frozenset) -> dict:
    """SCHEMAS amendment (grammar oracle): readings agreeing with a commentator's gloss first;
    root-noun (kvip/vic) readings only when nothing else fits; at most 8 shown, every id kept."""
    summ = [S.summary(a) for a in f["analyses"]]
    def root_noun(x):
        return N.affix_name(x.get("krt")) in ROOT_NOUN_KRT
    others = [x for x in summ if not root_noun(x)]
    pool = others or summ
    def agrees(x):
        st = C.latin_key(x.get("stem") or "")
        return len(st) >= 3 and any(w == st or (len(st) >= 4 and w.startswith(st)) for w in gloss_key)

    def key(x):
        return (not agrees(x), C.nfc(x.get("stem") or "") not in N.PRONOUNS, x.get("derives") is not True,
                "sambodhana" in (x.get("gram") or ""), x.get("source") != "vidyut-kosha", x.get("kind") == "samasa")
    pool = sorted(pool, key=key)
    for x in pool:
        x["agrees_with_gloss"] = agrees(x)
    shown = pool[:SHOWN]
    shown_ids = {x["id"] for x in shown}
    out = {k: v for k, v in f.items() if k != "analyses"}
    out.update({"analyses": shown, "more": len(summ) - len(shown), "all_ids": [x["id"] for x in summ],
                "more_note": ("further readings by id in all_ids; `python3 scripts/gita/show_analysis.py FORM` lists them "
                              "(root-noun kvip/vic readings are listed only there when another reading fits)") if len(summ) > len(shown) else None})
    return out


def _run_verse(rec: dict) -> tuple[str, float, list]:
    pk, rows = verse_packet(rec)
    C.write_json(C.packet_path(rec["locus"]), pk, indent=None)
    return rec["locus"], pk["seconds"], rows


# ---------------------------------------------------------------- whole run (main process)
def bori_records(chapters: list[int]) -> list[dict]:
    """BORI verses via lookup.bori_lines() (tags Bhg_CC.VVV[a|c]); speaker from the last speaker line.
    (build_gita_chapter_packet.bori_chapter matches `Bhg_{ch}` unpadded and finds nothing for 1–9.)"""
    lk = C.import_lookup()
    rel_bori = lk.rel(lk.BORI)
    by: dict[tuple[int, int], dict] = {}
    speaker = None
    for r in lk.bori_lines():
        if r["ch"] not in chapters:
            continue
        rec = by.setdefault((r["ch"], r["v"]), {"locus": f"{r['ch']}.{r['v']}", "lines": [], "loci": [], "speaker_line": None})
        if not r["half"]:
            speaker = r["text"]
            rec["speaker_line"] = {"text": r["text"], "locus": f"{rel_bori}:{r['line']}"}
            continue
        rec["lines"].append(r["text"])
        rec["loci"].append(f"{rel_bori}:{r['line']}")
        rec["_speaker"] = speaker
    out = []
    for ch in chapters:
        recs = [by[k] for k in sorted(by) if k[0] == ch]
        if len(recs) != C.VERSE_COUNTS[ch]:
            raise SystemExit(f"BORI chapter {ch}: {len(recs)} verses, expected {C.VERSE_COUNTS[ch]}")
        cur = None
        for rec in recs:
            if rec["speaker_line"]:
                cur = rec["speaker_line"]["text"]
            cur = cur or rec.pop("_speaker", None)
            rec.pop("_speaker", None)
            rec["speaker"] = ("arjuna" if cur and "arjuna" in cur else "krishna" if cur and "bhagav" in cur else
                              "samjaya" if cur and "saṃjaya" in cur else "dhrtarashtra" if cur and "dhṛtarāṣṭra" in cur else None)
            rec["iast"] = " |\n".join(rec["lines"]) + " ||"
            out.append(rec)
    return out


def build(chapters: list[int], workers: int = 0, fixture: str | None = None, without_grammar: bool = False,
          skip_meaning: bool = False, log=print) -> dict:
    timings: dict[str, float] = {}
    t = time.perf_counter()
    # fail before any work if the oracles are absent
    probe = O.load(fixture=fixture, without_grammar=without_grammar)
    identity = probe.identity()
    recs = bori_records(chapters)
    timings["bori"] = time.perf_counter() - t
    log(f"stage A: {len(recs)} verses in chapters {chapters}; oracle {identity.get('oracle')}")

    t = time.perf_counter()
    workers = workers or min(8, os.cpu_count() or 2)
    per_verse = {}
    st = S.Store(write=True)
    if workers <= 1:
        worker_init(fixture, without_grammar)
        for r in recs:
            loc, s, rows = _run_verse(r)
            per_verse[loc] = s
            st.put_many(rows)
    else:
        import multiprocessing as mp
        from concurrent.futures import ProcessPoolExecutor
        ctx = mp.get_context("spawn")
        with ProcessPoolExecutor(max_workers=workers, mp_context=ctx, initializer=worker_init,
                                 initargs=(fixture, without_grammar)) as ex:
            for loc, s, rows in ex.map(_run_verse, recs, chunksize=2):
                per_verse[loc] = s
                st.put_many(rows)
    timings["verse_packets"] = time.perf_counter() - t
    log(f"  verse packets: {timings['verse_packets']:.1f}s wall ({workers} workers), "
        f"{sum(per_verse.values()):.1f}s summed per-verse")

    t = time.perf_counter()
    packets = {r["locus"]: C.read_json(C.packet_path(r["locus"])) for r in recs}
    inv = inventory(packets)
    C.write_json(C.PIPE / "packets/inventory.json", inv)
    C.write_json(C.PIPE / "packets/concordance.json", concordance(packets, inv), indent=None)
    plan = shard_plan(chapters, packets)
    C.write_json(C.PIPE / "packets/shard_plan.json", plan)
    timings["inventory_plan"] = time.perf_counter() - t

    t = time.perf_counter()
    n_pages = 0
    if not skip_meaning and inv["lemmas"]:
        morc = probe if fixture else O.KitOracle(need_grammar=False, need_meaning=True)
        for e in inv["lemmas"]:
            if not e["content"] or e["weight"] <= 0:
                continue
            pg = dict(morc.page(e["page_lemma"], e["root"]))
            if not pg.get("glosses"):
                pg["glosses"] = occurrence_glosses(packets, e)
                pg["glosses_from"] = "lookup.py gloss, per occurrence (filled by stage A)"
            C.write_json(C.meaning_path(e["file_key"]), pg, indent=None)
            n_pages += 1
    timings["meaning_pages"] = time.perf_counter() - t

    t = time.perf_counter()
    for ch in chapters:
        C.write_json(C.PIPE / "secondaries" / f"{ch}.json", secondaries(ch))
    timings["secondaries"] = time.perf_counter() - t

    leaks = secondary_leaks(packets)
    manifest = {"chapters": chapters, "verses": len(recs), "oracle": identity, "workers": workers,
                "analyses_stored": st.count(),
                "analyses": sum(len(f["analyses"]) for p in packets.values() for f in p["forms"].values()),
                "forms": sum(len(p["forms"]) for p in packets.values()),
                "verses_without_recomposing_split": sorted((l for l, p in packets.items() if not p["primary_split"]), key=C.locus_sort_key),
                "gloss_errors": {l: p["gloss_error"] for l, p in packets.items() if p.get("gloss_error")},
                "lemmas": len(inv["lemmas"]), "content_lemmas": sum(1 for e in inv["lemmas"] if e["content"]),
                "lexicon_scope": sum(1 for e in inv["lemmas"] if e["in_lexicon_scope"]),
                "meaning_pages": n_pages, "shards": sum(len(v) for v in plan["chapters"].values()),
                "timings_s": {k: round(v, 2) for k, v in timings.items()},
                "slowest_verses": sorted(per_verse.items(), key=lambda kv: -kv[1])[:5],
                "secondary_leaks_in_packets": leaks}
    C.write_json(C.PIPE / "packets/manifest.json", manifest)
    if leaks:
        raise SystemExit(f"packets contain secondary-translation fields: {leaks[:5]}")
    return manifest


def secondary_leaks(packets: dict) -> list[str]:
    bad = []
    for loc, p in packets.items():
        s = json.dumps(p, ensure_ascii=False)
        for k in ("english_translations", "secondaries_english", "besant", "roy_aurobindo", "cwsa19"):
            if k in s:
                bad.append(f"{loc}:{k}")
    return bad


def inventory(packets: dict) -> dict:
    builder = C.import_builder()
    P = _packet_builder()
    pol = builder.load_policy(C.current_policy_path())
    prior = P.prior_renderings(C.ROOT, 0, pol)
    lem: dict[str, dict] = {}
    for loc in sorted(packets, key=C.locus_sort_key):
        p = packets[loc]
        for o in p["occurrences"]:
            by_lemma: dict[str, list] = {}
            for r in o["lemmas"]:
                by_lemma.setdefault(r["lemma"], []).append(r)
            content = [k for k, rs in by_lemma.items() if any(r["content"] for r in rs)]
            for lemma, rs in by_lemma.items():
                is_content = any(r["content"] for r in rs)
                # weight: an occurrence that also admits a pronoun/particle reading, or several
                # content lemmas, counts fractionally (a priority signal, not a decision)
                w = 0.0 if (o.get("function_reading") and is_content) else (1.0 / max(1, len(content)) if is_content else 1.0)
                roots = sorted({r["root"] for r in rs if r["root"]})
                e = lem.setdefault(lemma, {"key": lemma, "lemma": lemma, "roots": set(), "page_lemma": rs[0]["page_lemma"],
                                           "content": False, "occurrences": [], "forms": set(), "weight": 0.0})
                e["roots"].update(roots)
                e["content"] = e["content"] or is_content
                e["weight"] += w
                e["occurrences"].append({"at": f"{loc}[{o['i']}]", "form": o["form"], "ambiguous": len(by_lemma) > 1, "weight": round(w, 3),
                                         "analysis_ids": [i for r in rs for i in r["analysis_ids"]]})
                e["forms"].add(o["form"])
    out = []
    for e in lem.values():
        forms = sorted(e.pop("forms"))
        e["roots"] = sorted(e["roots"])
        e["root"] = e["roots"][0] if e["roots"] else None
        e["weight"] = round(e["weight"], 3)
        rows = sorted({rk for f in forms for rk in pol.regex_rows({"stem": e["lemma"], "iast": f})})
        gkey = C.latin_key(e["lemma"].split("√")[-1])
        glossary = gkey if (C.GLOSSARY / f"{gkey}.json").is_file() else None
        pr = [x for k in (rows or [e["lemma"]]) for x in prior.get(k, [])]
        freq = len(e["occurrences"])
        unamb = sum(1 for o in e["occurrences"] if not o["ambiguous"])
        system = bool(rows or glossary)
        e.update({"forms": forms, "frequency": freq, "unambiguous": unamb, "verses": sorted({o["at"].split("[")[0] for o in e["occurrences"]}, key=C.locus_sort_key),
                  "rows": rows, "glossary_key": glossary, "system": system, "prior_renderings": pr[:20],
                  "file_key": C.lemma_file_key(e["page_lemma"], e["root"]),
                  # scope (lead, 2026-11-08): ≥ 3 occurrences, or a table row / glossary (system) term; every
                  # other content lemma is decided inline by the verse job and recorded after its review
                  "in_lexicon_scope": bool(e["content"] and (e["weight"] >= 3 or ((rows or system) and e["weight"] >= 1)))})
        e["meaning_page"] = C.rel(C.meaning_path(e["file_key"]))
        out.append(e)
    out.sort(key=lambda e: (not e["system"], -e["weight"], -e["frequency"], e["lemma"]))
    return {"policy": C.rel(C.current_policy_path()), "policy_sha256": pol.sha256, "lemmas": out,
            "note": "Candidates from every analysis of each pada of the first recomposing split. `weight` counts an "
                    "occurrence fully only when one content lemma is possible and no pronoun/particle reading exists; "
                    "lexicon scope = content lemmas of weight >= 3, or with a table row or glossary entry and weight >= 1; "
                    "the rest are decided inline in the verse jobs. "
                    "Code proposes; the lexicon decides; verse producers request what the scope misses."}


def occurrence_glosses(packets: dict, e: dict) -> list[dict]:
    out = []
    for o in e["occurrences"]:
        loc = o["at"].split("[")[0]
        p = packets[loc]
        i = int(o["at"].split("[")[1].rstrip("]"))
        occ = p["occurrences"][i]
        tok = p["tokens"][occ["bori_token"]] if occ.get("bori_token") is not None else None
        line = next((l for l in p["iast"].split("\n") if tok and tok["token"] in l), p["iast"])
        for g in (tok or {}).get("glosses", []):
            out.append({"at": o["at"], "locus": g["locus"], "who": g["who"], "text": g["text"], "line": line.strip(" |")})
    return out


def concordance(packets: dict, inv: dict) -> dict:
    out = {}
    for e in inv["lemmas"]:
        if not e["content"]:
            continue
        rows = []
        for o in e["occurrences"]:
            loc = o["at"].split("[")[0]
            rows.append({"at": o["at"], "form": o["form"], "iast": packets[loc]["iast"]})
        out[e["key"]] = rows
    return out


def shard_plan(chapters: list[int], packets: dict, target: int = 60) -> dict:
    P = _packet_builder()
    plan = {"target_cards": target, "chapters": {}}
    for ch in chapters:
        n = C.VERSE_COUNTS[ch]
        units = P.ramanuja_units(ch, n)
        def cards(v):
            p = packets[f"{ch}.{v}"]
            prim = next((c for c in p["split_candidates"] if c["id"] == p["primary_split"]), None)
            return len(prim["tokens"]) if prim else len(p["tokens"])
        sizes = [sum(cards(v) for v in u) for u in units]
        shards = []
        for k, g in enumerate(P.balanced_partition(sizes, target), 1):
            vs = [v for i in g for v in units[i]]
            shards.append({"id": f"{ch:02d}-{k:02d}", "verses": [f"{ch}.{v}" for v in vs], "range": f"{vs[0]:02d}-{vs[-1]:02d}",
                           "cards_estimate": sum(sizes[i] for i in g),
                           "units": [f"{ch}.{units[i][0]}" + (f"-{units[i][-1]}" if len(units[i]) > 1 else "") for i in g]})
        plan["chapters"][str(ch)] = shards
    return plan


def secondaries(ch: int) -> dict:
    """Private: the published translations of chapter CH for the review jobs' blind check only."""
    lk = _lookup_cached()
    P = _packet_builder()
    verses, trans, comm = lk.gita_gita_tables()
    by_vid = defaultdict(list)
    for r in trans:
        if r.get("lang") == "english":
            by_vid[str(r["verse_id"])].append({"author": r["authorName"], "text": r["description"]})
    out = {"chapter": ch, "private": "published translations — review jobs only; never committed, never read by lexicon or verse jobs",
           "verses": {f"{ch}.{v}": by_vid.get(str(lk.gita_verse_id(ch, v)), []) for v in range(1, C.VERSE_COUNTS[ch] + 1)},
           "besant_das_1905": P.besant_das_discourse(ch), "roy_aurobindo_1938": P.roy_chapter(ch)}
    cw = lk.SECONDARIES / "cwsa19_essays_on_the_gita.txt"
    if cw.is_file():
        out["cwsa19"] = {"path": lk.rel(cw), "sha256": C.sha256_file(cw),
                         "note": "Sri Aurobindo, Essays on the Gita (CWSA 19): not divided by verse; search it for the chapter's words."}
    return out

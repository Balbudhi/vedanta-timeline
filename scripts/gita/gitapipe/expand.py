"""Expansion (stage C): a verse-job output (gita-verse-v1) + the verse packets and analysis store
+ the lexicon → the producer-v2 shard the fail-closed builder reads. Every card field and
citation is built here from ids; the producer's judgement fields (choice of analysis, sense,
English, kāraka, compound type and vigraha, note, line, sense paragraph, forks, commentator
lines) are carried verbatim. `card_overrides` (optional, per word) replace generated display
fields verbatim; a producer normally omits them.
"""
from __future__ import annotations

import re
from functools import lru_cache

from . import common as C
from . import names as N
from .lexicon import sense_index
from .store import Store

MEANING_CATS = ["formation", "lexical", "nirvacana", "commentator", "usage", "reception", "synthesis"]
CARD_SHOWS_COMMENTATORS = 3
SAMASA_SUTRA = {  # compound type named by the producer → the general sūtra that forms it (cited, not chosen)
    "dvitiya-tatpurusa": "2.1.24", "dvitiya": "2.1.24", "trtiya-tatpurusa": "2.1.30", "trtiya": "2.1.30",
    "caturthi-tatpurusa": "2.1.36", "caturthi": "2.1.36", "pancami-tatpurusa": "2.1.37", "pancami": "2.1.37",
    "sasthi-tatpurusa": "2.2.8", "sasthi": "2.2.8", "saptami-tatpurusa": "2.1.40", "saptami": "2.1.40",
    "karmadharaya": "2.1.57", "bahuvrihi": "2.2.24", "dvandva": "2.2.29", "itaretara-dvandva": "2.2.29",
    "samahara-dvandva": "2.2.29", "avyayibhava": "2.1.6", "nan-tatpurusa": "2.2.6", "nan": "2.2.6",
    "upapada-tatpurusa": "2.2.19", "upapada": "2.2.19", "dvigu": "2.1.52", "pradi-tatpurusa": "2.2.18",
    "nan-bahuvrihi": "2.2.24",
}
EN_SOURCES = [("webster", "webster1913"), ("gcide", "gcide"), ("kaikki", "wiktionary"), ("wiktionary", "wiktionary"),
              ("oewn", "oewn2025"), ("wordnet", "wordnet3.1"), ("roget", "roget1911"), ("moby", "moby")]


SAMASA_ORDER = ["nan-bahuvrihi", "bahuvrihi", "itaretara-dvandva", "samahara-dvandva", "dvandva", "avyayibhava", "dvigu",
                "karmadharaya", "upapada", "pradi-tatpurusa", "nan-tatpurusa", "dvitiya", "trtiya", "caturthi", "pancami",
                "sasthi", "saptami"]


def samasa_sutra(ctype: str | None) -> str | None:
    """The forming sūtra of the compound type the producer named: a 2.1/2.2 sūtra the type text
    itself cites, else the general sūtra of the first type word it contains."""
    if not ctype:
        return None
    m = re.search(r"\b(2\.[12]\.\d{1,2})\b", ctype)
    if m:
        return m.group(1)
    keys = [C.latin_key(t) for t in re.split(r"[\s(),;:/\[\]]+", ctype) if t]
    joined = [C.latin_key(t) for t in re.split(r"[\s(),;:/\[\]]+", ctype.replace("-", "")) if t]
    for name in SAMASA_ORDER:
        k = C.latin_key(name)
        if k in keys or k in joined or any(x.startswith(k) for x in keys):
            return SAMASA_SUTRA.get(name) or SAMASA_SUTRA.get(name + "-tatpurusa")
    return None


@lru_cache(maxsize=None)
def sutra(s: str) -> dict | None:
    try:
        return C.import_lookup().sutra_lookup(s)
    except BaseException:  # noqa: BLE001 - lookup exits on an unknown sūtra
        return None


@lru_cache(maxsize=1)
def dhatupatha() -> dict[str, dict]:
    d = C.read_json(C.DHATUPATHA)
    return {str(e.get("i")): e for e in (d.get("data", d) if isinstance(d, dict) else d)}


def sutra_evidence(s: str, claim: str) -> dict | None:
    r = sutra(s)
    if not r or not r.get("ashtadhyayi"):
        return None
    return {"claim": claim, "locus": r["ashtadhyayi"], "quote": f"{s} {r.get('ashtadhyayi_text') or r.get('text')}", "sutra": s, "kind": "sutra"}


def dp_evidence(i: str) -> tuple[dict, dict] | None:
    e = dhatupatha().get(i)
    if not e:
        return None
    g = int(e["gana"])
    q = f"{e['aupadeshik']} {e['gana']} {N.GANA_NAMES.get(g, '')} {e['pada']} {e['artha']}"
    return e, {"claim": f"√{e['dhatu']} {N.GANA_NAMES.get(g, '')} {g}{e['pada']} '{e['artha']}'",
               "locus": f"sources/raw/panini/lexica/dhatupatha.json#{i}", "quote": q, "kind": "dhatupatha"}


def infer_member_term(policy, form: str) -> dict | None:
    """A compound member's term by the term detector's rule (lead, 2026-11-08): exactly one row
    matches the member and that row has one sense; otherwise the producer names it."""
    rows = policy.regex_rows({"stem": form, "iast": form})
    if len(rows) == 1 and len(policy.rows[rows[0]].senses) == 1:
        return {"lemma": rows[0], "sense": next(iter(policy.rows[rows[0]].senses))}
    return None


def en_source(locus: str | None) -> str:
    l = (locus or "").lower()
    return next((name for k, name in EN_SOURCES if k in l), "unknown")


class Expander:
    def __init__(self, policy_path=None, extra_entries: list[dict] | None = None, store: Store | None = None,
                 include_outputs: bool = True) -> None:
        self.builder = C.import_builder()
        self.policy_path = policy_path or C.current_policy_path()
        self.policy_raw = C.read_json(self.policy_path)
        self.policy = self.builder.Policy(self.policy_raw)
        self.extra = list(extra_entries or [])
        self.index = sense_index(self.policy_raw, include_outputs=include_outputs, extra_entries=self.extra)
        self.store = store
        self.lookup = C.import_lookup()
        self._packets: dict[str, dict] = {}

    def packet(self, locus: str) -> dict:
        if locus not in self._packets:
            self._packets[locus] = C.read_json(C.packet_path(locus))
        return self._packets[locus]

    def iast(self, s):
        return self.lookup.to_iast(s) if s and re.search(r"[\u0900-\u097f]", s) else s

    # ---------------------------------------------------------- analyses
    def resolve(self, ref) -> tuple[dict | None, dict | None, bool, str | None]:
        """(analysis, derivation, manual, error)."""
        if isinstance(ref, str):
            if self.store is None:
                self.store = Store()
            got = self.store.get(ref)
            if got is None:
                return None, None, False, f"analysis id {ref!r} not in the analysis store"
            return got[0], got[1], False, None
        if isinstance(ref, dict) and isinstance(ref.get("manual"), dict):
            return ref["manual"], None, True, None
        return None, None, False, f"analysis must be an id or {{manual: Analysis}} — got {str(ref)[:80]}"

    # ---------------------------------------------------------- one word
    def card(self, w: dict, v: dict, pk: dict, sandhi_of: dict[int, dict], review_rwm: dict) -> tuple[dict, list[str]]:
        errs: list[str] = []
        i = w.get("i")
        pada = v["padas"][i] if isinstance(i, int) and 0 <= i < len(v.get("padas") or []) else ""
        an, der, manual, err = self.resolve(w.get("analysis"))
        if err:
            errs.append(f"{v['locus']}[{i}]: {err}")
            an = {"kind": None, "stem": pada}
        comp = w.get("compound")
        members = []
        member_derivs = []
        for m in (comp or {}).get("members") or []:
            ma, md, mman, merr = self.resolve(m.get("analysis")) if m.get("analysis") is not None else (None, None, True, None)
            if merr:
                errs.append(f"{v['locus']}[{i}] member {m.get('form')}: {merr}")
            members.append((m, ma or {}, md))
            if md:
                member_derivs.append(md)
        d = an.get("dhatu") or {}
        if not d and members:
            d = (members[-1][1].get("dhatu") or {})
        sid = w.get("sense")
        ent = self.index.get(sid) if sid else None
        if sid and not ent:
            errs.append(f"{v['locus']}[{i}]: sense {sid!r} not in the lexicon")
        lex = (ent or {}).get("lexicon") or {}
        tsense = self.policy.sense(ent["row"], ent["sense"]) if ent else None
        preserve = bool(lex.get("preserve") or lex.get("chosen") == "preserve" or (tsense and tsense.policy == "preserve"))
        wc = w.get("word_class") or (N.word_class(an) if an.get("kind") else "content")
        dpi = N.dp_id(d)
        dp = dp_evidence(dpi) if dpi else None
        root_gloss = (dp[0].get("artha_english") if dp else None) or (d.get("artha") if d else None)
        morph, affix = N.morph_text(an), N.affix_text(an)
        english = w.get("english") or ""
        card = {"i": i, "iast": pada, "deva": self.lookup.to_deva(pada.replace("-", "")), "word_class": wc,
                "gloss": english, "parts": self.parts(an, d, root_gloss, morph, english, members, lex),
                "stem": "-".join(x[0].get("form") or "" for x in members) if (comp and not an.get("stem")) else (an.get("stem") or N.verb_stem(an) or an.get("form") or pada),
                "root": N.root_string({**d, "pada": N.pada(d.get("pada")), "artha": self.iast(d.get("artha"))} if d else {}),
                "rootGloss": root_gloss if d.get("root") else None,
                "affix": affix, "morph": morph, "karaka": w.get("karaka"),
                "compound": ({"type": comp.get("type"), "vigraha": comp.get("vigraha"), "members": [m[0].get("form") for m in members]}
                             if comp else None),
                "sandhi": sandhi_of.get(i, {}).get("text"),
                "glossaryKey": None, "translatable": not preserve, "note": w.get("note")}
        if w.get("form_note"):
            card["form_note"] = w["form_note"]
        if dpi and d.get("root"):
            card["root_id"] = f"dhatupatha.json#{dpi}"
        if ent:
            card["term"] = {"lemma": ent["row"], "sense": ent["sense"]} if self.policy.sense(ent["row"], ent["sense"]) else None
            gk = lex.get("glossaryKey") or (tsense.glossary_key if tsense else None)
            card["glossaryKey"] = gk if gk and (C.GLOSSARY / f"{gk}.json").is_file() else None
        member_terms = []
        for k, (m, _, _) in enumerate(members):
            me = self.index.get(m.get("sense")) if m.get("sense") else None
            if me and self.policy.sense(me["row"], me["sense"]):
                member_terms.append({"lemma": me["row"], "sense": me["sense"], "member": k})
            elif not m.get("sense") and m.get("form"):
                t = infer_member_term(self.policy, m["form"])
                if t:
                    member_terms.append({**t, "member": k, "inferred": True})
        if member_terms:
            card["terms"] = ([card["term"]] if card.get("term") else []) + member_terms
        # evidence and fallback
        ev, fb = [], []
        if dp and d.get("root"):
            ev.append(dp[1])
        for dd in [der] + member_derivs:
            for st in (dd or {}).get("steps") or []:
                if st.get("sutra") and st.get("ashtadhyayi") and (st.get("source") in (None, "aṣṭādhyāyī")):
                    e = sutra_evidence(st["sutra"], f"{st['sutra']} → {st.get('result')}")
                    if e:
                        ev.append(e)
        if comp:
            s = comp.get("sutra") or samasa_sutra(comp.get("type"))
            e = sutra_evidence(s, f"{comp.get('type')} by {s}") if s else None
            if e:
                ev.append(e)
                # SCHEMAS amendment: Vidyut derives no samāsa, so the compound is the analyst's claim, flagged for review
                fb.append({"kind": "other", "text": f"compound: the type ({comp.get('type')}) and its sūtra {s} are the analyst's claim; "
                                                    "the members were derived, the compounding was not"})
            else:
                fb.append({"kind": "compound", "text": f"the compound type '{comp.get('type')}' was not mapped to its forming sūtra"})
            if not member_derivs and not der:
                fb.append({"kind": "compound", "text": "no member of the compound was derived"})
        for s in (w.get("analysis") or {}).get("sutras", []) if isinstance(w.get("analysis"), dict) else []:
            e = sutra_evidence(s, f"cited by the analyst: {s}")
            if e:
                ev.append(e)
        for b in (sandhi_of.get(i) or {}).get("evidence", []):
            ev.append(b)
        affixed = an.get("krt") or an.get("taddhita") or an.get("kind") in ("tinanta", "subanta", "krdanta", "taddhitanta")
        if manual and affixed and not any(e.get("kind") == "sutra" for e in ev) and wc not in ("particle",):
            fb.append({"kind": "pratyaya", "text": "the formation is the analyst's; no derivation was generated for it"})
        if der and der.get("matches") is False and not comp:
            fb.append({"kind": "pratyaya", "text": f"the generated derivation yields {der.get('form_derived')!r}, not {der.get('form_expected')!r}"})
        if an.get("kind") == "avyaya" or wc in ("particle",):
            card["affix"] = card["affix"] if "avyaya" in card["affix"] else card["affix"] + " (avyaya)"
        seen = set()
        card["evidence"] = [e for e in ev if not ((e["locus"], e["quote"]) in seen or seen.add((e["locus"], e["quote"])))]
        card["fallback"] = fb
        card["derivation"] = ({k: der.get(k) for k in ("analysis_id", "form_expected", "form_derived", "matches", "engine", "scope")}
                              | {"steps": der.get("steps") or []}) if der else None
        # meaning and wording
        lex_m = lex
        if not lex and w.get("meaning_lines"):    # decided inline in the verse job (SCHEMAS "Inline sense fields")
            lex_m = {k: w.get(k) for k in ("image", "meaning_lines", "why", "plain", "rich", "chosen", "joycean")}
            lex_m["gloss"] = w.get("why")
        elif not lex and dp and d.get("root"):      # a root-bearing word without a sense (copula): the root's own record
            rec = dp[0]
            lex_m = {"image": f"√{d['root']} '{self.iast(rec.get('artha'))}'",
                     "meaning_lines": [{"cat": "lexical", "text": rec.get("artha_english") or self.iast(rec.get("artha")),
                                        "who": "Dhātupāṭha", "locus": dp[1]["locus"]}]}
        card["meaning"] = self.meaning(w, lex_m, english, review_rwm.get(i) or [])
        if wc == "content" and not preserve and (lex_m.get("plain") or lex_m.get("candidates")):
            card["wording"] = self.wording(lex_m)
        for k, val in (w.get("card_overrides") or {}).items():
            card[k] = val
        if not card.get("meaning"):
            card.pop("meaning", None)
        if card.get("term") is None:
            card.pop("term", None)
        return card, errs

    def parts(self, an, d, root_gloss, morph, english, members, lex) -> list[dict]:
        if members:
            return [{"form": m.get("form") or ma.get("stem") or "?", "gloss": m.get("english") or self._sense_gloss(m.get("sense"))
                     or (ma.get("stem") or m.get("form") or "member")} for m, ma, _ in members]
        out = []
        for u in d.get("upasargas") or []:
            if isinstance(u, str):
                out.append({"form": f"{u}-", "gloss": N.UPASARGA_GLOSS.get(u, "prefix")})
        if d.get("root"):
            out.append({"form": f"√{d['root']}", "gloss": root_gloss or lex.get("image") or "root"})
        else:
            out.append({"form": an.get("stem") or an.get("form") or "?", "gloss": lex.get("gloss") or english or "stem"})
        krt, tad = N.affix_name(an.get("krt")), N.affix_name(an.get("taddhita"))
        if krt:
            out.append({"form": f"-{krt}", "gloss": N.KRT_GLOSS.get(krt, "kṛt affix")})
        if tad:
            out.append({"form": f"-{tad}", "gloss": "taddhita affix"})
        end = (an.get("ending") or {}).get("name")
        if end and an.get("kind") != "avyaya":
            out.append({"form": f"-{end}", "gloss": morph})
        return out

    def _sense_gloss(self, sid):
        e = self.index.get(sid) if sid else None
        return ((e or {}).get("lexicon") or {}).get("gloss")

    def meaning(self, w: dict, lex: dict, english: str, rwm: list[dict]) -> dict | None:
        comm = [{"cat": "commentator", "text": c.get("text"), "who": c.get("who"), "locus": c.get("locus")}
                for c in w.get("commentator_lines") or [] if isinstance(c, dict)]
        rec = [{"cat": "reception", "text": f"“{r.get('word')}”", "who": r.get("who")}
               for r in rwm if isinstance(r, dict) and r.get("word") and r.get("who")]
        lexl = [dict(x) for x in lex.get("meaning_lines") or [] if isinstance(x, dict) and x.get("cat") in MEANING_CATS]
        shown_c = comm[:CARD_SHOWS_COMMENTATORS]
        room = max(0, 8 - len(shown_c) - min(len(rec), 2))
        lines = lexl[:room] + shown_c + rec[:max(0, 8 - len(lexl[:room]) - len(shown_c))]
        lines.sort(key=lambda x: MEANING_CATS.index(x["cat"]))
        image = lex.get("image")
        if not (lines or image):
            return None
        m = {"image": image, "lines": lines, "rendering": english, "why": lex.get("why"),
             "alternatives": list(dict.fromkeys(r.get("word") for r in rwm if r.get("word") and r.get("word") != english))}
        if len(comm) > len(shown_c):
            m["commentators_all"] = comm
        return {k: val for k, val in m.items() if val not in (None, "")}

    def wording(self, lex: dict) -> dict:
        def cand(c):
            if not isinstance(c, dict) or not c.get("word"):
                return None
            return {**c, "source": c.get("source") or en_source(c.get("locus"))}
        plain, rich = cand(lex.get("plain")), cand(lex.get("rich"))
        chosen_kind = lex.get("chosen")
        jc = lex.get("joycean")
        chosen = {"plain": (plain or {}).get("word"), "rich": (rich or {}).get("word"),
                  "joycean": (jc or {}).get("expression")}.get(chosen_kind) or (plain or {}).get("word")
        # the lexicon's own candidate list when it gives one (each checked by the builder against
        # `define`), else its plain and rich words
        cands = [c for c in ([cand(x) for x in lex["candidates"]] if lex.get("candidates") else [plain, rich]) if c]
        uniq = {(c["word"], c.get("locus")): c for c in cands}
        out = {"sense_description": lex.get("gloss"), "plain": plain, "rich": rich, "chosen": chosen, "chosen_kind": chosen_kind,
               "why": lex.get("why"), "candidates": list(uniq.values()), "joycean": None}
        if isinstance(jc, dict):
            out["joycean"] = {"formation": jc.get("expression") or jc.get("formation"), "parts": jc.get("parts"),
                              "relation": jc.get("relation"), "paraphrase": jc.get("paraphrase"),
                              "why_no_attested_word": jc.get("why_no_attested_word")}
        return out

    # ---------------------------------------------------------- sandhi from the oracle's split
    def sandhi_map(self, v: dict, pk: dict) -> dict[int, dict]:
        keys = [C.form_key(p) for p in v.get("padas") or []]
        for c in pk.get("split_candidates") or []:
            if [C.form_key(t) for t in c["tokens"]] != keys:
                continue
            out, k = {}, 0
            for h in c.get("hemistichs") or []:
                bs = h.get("boundaries") or []
                for j, b in enumerate(bs):
                    idx = k + j
                    if b.get("engine_rule") and b.get("sutras"):
                        ev = [e for s in b["sutras"] if (e := sutra_evidence(s, f"sandhi {b.get('left')} + {b.get('right')} → {b.get('surface')}: {s}"))]
                        out[idx] = {"text": f"{b.get('left')} + {b.get('right')} → {b.get('surface')} ({', '.join(b['sutras'])})", "evidence": ev}
                k += len(h.get("tokens") or [])
            return out
        return {}

    # ---------------------------------------------------------- the shard
    def shard(self, vo: dict, source_path: str | None = None, source_sha: str | None = None, review: dict | None = None,
              secondaries: list[str] | None = None) -> tuple[dict, list[str]]:
        errs: list[str] = []
        rwm: dict[tuple[str, int], list[dict]] = {}
        for r in (review or {}).get("readers_will_meet") or []:
            for x in r.get("renderings") or []:
                rwm.setdefault((r.get("locus"), r.get("word_i")), []).append(x)
        verses = []
        rows_used: dict[str, str] = {}
        for v in vo.get("verses") or []:
            loc = v.get("locus")
            try:
                pk = self.packet(loc)
            except FileNotFoundError:
                errs.append(f"{loc}: no verse packet")
                continue
            smap = self.sandhi_map(v, pk)
            per = {i: rwm.get((loc, i), []) for i in range(len(v.get("words") or []))}
            words = []
            for w in v.get("words") or []:
                c, e = self.card(w, v, pk, smap, per)
                errs += e
                words.append(c)
                for t in [c.get("term")] + list(c.get("terms") or []):
                    if t and t["lemma"] in self.policy.rows:
                        rows_used[t["lemma"]] = C.canon_hash(self.policy.rows[t["lemma"]].raw)
            verse = {"locus": loc, "speaker": pk.get("speaker"), "meter": (pk.get("meter") or {}).get("name") or "anuṣṭubh",
                     "iast": pk["iast"], "devanagari": pk["devanagari"], "sense": v.get("sense"), "english": v.get("line"),
                     "words": words, "grammar": v.get("grammar") or self.grammar(words), "forks": v.get("forks") or [],
                     "deviations": [], "secondaries_consulted": list(secondaries or [])}
            verses.append(verse)
        loci = [v["locus"] for v in verses]
        ch = int(loci[0].split(".")[0]) if loci else None
        rng = f"{int(loci[0].split('.')[1]):02d}-{int(loci[-1].split('.')[1]):02d}" if loci else ""
        shard = {"schema_version": C.SCHEMA_PRODUCER, "chapter": ch, "range": rng, "job": vo.get("job"), "mode": "analysis",
                 "policy_sha256": self.policy.sha256, "policy_path": C.rel(self.policy_path),
                 "source": {"verse_output": source_path, "sha256": source_sha, "review": (review or {}).get("job")},
                 "rows_used": rows_used, "generated_by": "scripts/gita/expand_cards.py",
                 "secondaries_consulted_by": "the review's blind check (private translations file), not the producer",
                 "verses": verses, "lexicon_requests": vo.get("lexicon_requests") or [],
                 "fallback_count": sum(len(w.get("fallback") or []) for v in verses for w in v["words"])}
        return shard, errs

    @staticmethod
    def grammar(words: list[dict]) -> dict:
        kar = "; ".join(f"{w['iast']}: {w['karaka']}" for w in words if w.get("karaka"))
        verbs = "; ".join(f"{w['iast']}: {w['morph']}" for w in words
                          if re.search(r"indicative|imperative|optative|future|perfect|aorist|imperfect|absolutive|infinitive|participle|conditional|benedictive",
                                       w.get("morph") or ""))
        return {"karakaSummary": kar or "no kāraka recorded", "verbalModality": verbs or "no verbal form"}

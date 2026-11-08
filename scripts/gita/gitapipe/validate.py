"""Validators per job type (SCHEMAS.md and its amendments). Each returns (errors, warnings);
a job is done only when errors is empty. Referential checks read the packets, the analysis
store, the lexicon and the builder; a verse output is also expanded and run through the
builder's own verse and card checks (check mode, unreviewed)."""
from __future__ import annotations

import json
import re
import subprocess
from functools import lru_cache
from pathlib import Path

from . import common as C
from . import lexicon as L
from . import names as N
from .oracle import ANALYSIS_KEYS, KINDS

SENSE_ID = re.compile(r"^[a-z0-9][a-z0-9_-]*\.[a-z0-9][a-z0-9_-]*$")
MEANING_CATS = ["formation", "lexical", "nirvacana", "commentator", "usage", "reception", "synthesis"]
REVIEW_CHECKS = {"grammar", "form", "meaning", "readability", "policy", "forks", "public"}
LEXREVIEW_CHECKS = {"occurrences", "evidence", "image", "tests", "candidates", "readability", "distinctness", "public"}
NGRAM = 6
QUOTE_WORDS = 8          # this many words in sequence from a translation = a quotation


class Result:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, m: str) -> None:
        self.errors.append(m)

    def warn(self, m: str) -> None:
        self.warnings.append(m)


# ---------------------------------------------------------------- shared
@lru_cache(maxsize=1)
def builder():
    return C.import_builder()


def public_text(res: Result, label: str, node) -> None:
    for path, s in builder().iter_strings(node):
        for name, pat in builder().PIPELINE_PATTERNS:
            m = pat.search(s)
            if m:
                res.err(f"{label} {path}: pipeline vocabulary ({name}) '{m.group(0)}' in reader-facing text")
                break


@lru_cache(maxsize=1)
def translator_names() -> tuple[str, ...]:
    names = set(builder().TRANSLATORS) | {"Besant", "Bhagavan Das", "Anilbaran", "Sankaranarayan"}
    return tuple(sorted(names))


@lru_cache(maxsize=32)
def _secondary_ngrams(ch: int) -> frozenset:
    p = C.PIPE / "secondaries" / f"{ch}.json"
    if not p.is_file():
        return frozenset()
    d = C.read_json(p)
    out = set()
    for items in (d.get("verses") or {}).values():
        for it in items:
            toks = re.findall(r"[a-z]+", (it.get("text") or "").lower())
            out.update(tuple(toks[k:k + NGRAM]) for k in range(len(toks) - NGRAM + 1))
    return frozenset(out)


def no_secondaries(res: Result, label: str, node, chapters: set[int]) -> None:
    grams = set()
    for ch in chapters:
        grams |= _secondary_ngrams(ch)
    for path, s in builder().iter_strings(node):
        for t in translator_names():
            if re.search(rf"(?<![A-Za-z]){re.escape(t)}(?![A-Za-z])", s):
                res.err(f"{label} {path}: names a published translator ({t}); translations enter only the review's blind check")
                break
        toks = re.findall(r"[a-z]+", s.lower())
        k, best, at = 0, 0, None
        while k <= len(toks) - NGRAM:           # longest run of overlapping 6-grams = longest shared word sequence
            n = 0
            while k + n <= len(toks) - NGRAM and tuple(toks[k + n:k + n + NGRAM]) in grams:
                n += 1
            if n and n + NGRAM - 1 > best:
                best, at = n + NGRAM - 1, k
            k += max(n, 1)
        if best >= QUOTE_WORDS:
            res.err(f"{label} {path}: {best} words identical to a published translation ('{' '.join(toks[at:at + best])}')")
        elif best:
            res.warn(f"{label} {path}: {best} words identical to a published translation ('{' '.join(toks[at:at + best])}'); "
                     "literal convergence or copying — the reviewer decides")


def locus_exists(res: Result, label: str, locus: str) -> None:
    for one in [x.strip() for x in str(locus or "").split(";") if x.strip()]:
        base = re.sub(r"\s+\(.*\)$", "", one)
        path = re.split(r"[#:]", base, maxsplit=1)[0] if not base.endswith((".gz",)) else base
        path = re.sub(r"(\.gz):.*$", r"\1", base) if ".gz:" in base else path
        cands = [C.PRAKRIYA / path, C.ROOT.parent / path, C.ROOT / path]
        if not any(p.is_file() for p in cands):
            res.err(f"{label}: locus file not found: {one}")
            continue
        m = re.search(r":(\d+)(?:-(\d+))?$", base)
        if m and not base.endswith(".gz") and ".gz:" not in base and "#" not in base:
            p = next(p for p in cands if p.is_file())
            with open(p, encoding="utf-8", errors="replace") as fh:
                n = sum(1 for _ in fh)
            a, b = int(m.group(1)), int(m.group(2) or m.group(1))
            if not (1 <= a <= b <= n):
                res.err(f"{label}: line range outside the file: {one}")


def job_record(job_id: str) -> dict | None:
    for st in ("running", "pending", "done", "failed"):
        p = C.PIPE / "queue" / st / f"{job_id}.json"
        if p.is_file():
            return C.read_json(p)
    return None


def job_input(job_id: str, kind: str) -> dict | None:
    p = C.ns() / "jobs" / kind / f"{job_id}.input.json"
    return C.read_json(p) if p.is_file() else None


def _schema(d: dict) -> str | None:
    return d.get("schema") or d.get("schema_version")


# ---------------------------------------------------------------- lexicon
def check_entry(res: Result, label: str, e: dict, pol: dict, inv_forms: list[str] | None, others: dict[str, str]) -> list[str]:
    """One gita-lexicon-v1 entry; returns its sense ids."""
    ids = []
    if e.get("skip"):
        if e.get("senses"):
            res.err(f"{label}: an entry with `skip` has no senses")
        if not isinstance(e["skip"], str) or len(e["skip"]) < 10:
            res.err(f"{label}: `skip` must give the reason (e.g. the inventory lemma comes only from a wrong analysis)")
        return ids
    if not (isinstance(e.get("lemma"), str) and e["lemma"].strip()):
        res.err(f"{label}: lemma missing")
    try:
        rx = re.compile(e.get("match") or "")
        if not e.get("match"):
            res.err(f"{label}: `match` (the term checker's regex) missing")
        elif inv_forms and not any(rx.search(f) or rx.search(C.nfc(f)) for f in inv_forms + [e.get("lemma") or ""]):
            res.err(f"{label}: match {e['match']!r} matches none of the lemma's Gītā forms {inv_forms[:6]}")
    except re.error as x:
        res.err(f"{label}: match is not a regular expression ({x})")
    senses = e.get("senses")
    if not isinstance(senses, list) or not senses:
        res.err(f"{label}: senses must be a non-empty list")
        return ids
    rows = set()
    reserved = pol.get("reserved_english") or {}
    for k, s in enumerate(senses):
        sl = f"{label} senses[{k}]"
        sid = s.get("id") or ""
        if not SENSE_ID.match(sid):
            res.err(f"{sl}: id {sid!r} must be 'row.sense' in lower-case ASCII")
            continue
        ids.append(sid)
        row = sid.split(".")[0]
        rows.add(row)
        if sid in others:
            res.err(f"{sl}: sense id {sid} already defined by {others[sid]}")
        for f in ("gloss", "image", "why"):
            if not (isinstance(s.get(f), str) and s[f].strip()):
                res.err(f"{sl}: `{f}` missing")
        chosen = s.get("chosen")
        if chosen not in L.CHOSEN:
            res.err(f"{sl}: chosen {chosen!r} not in {sorted(L.CHOSEN)}")
        preserve = bool(s.get("preserve")) or chosen == "preserve"
        if preserve and not s.get("iast"):
            res.err(f"{sl}: a preserved sense needs `iast` (SCHEMAS amendment)")
        if s.get("preserve") is True and chosen not in ("preserve", None):
            res.warn(f"{sl}: preserve true but chosen {chosen!r}")
        forms = s.get("forms")
        if not isinstance(forms, dict) or not forms:
            res.err(f"{sl}: forms must map a grammatical category to English")
        else:
            for fk, fv in forms.items():
                if not (isinstance(fv, str) and fv.strip() or isinstance(fv, list) and fv and all(isinstance(x, str) and x.strip() for x in fv)):
                    res.err(f"{sl}: forms[{fk!r}] must be a string or a list of strings")
                if L.cat_of(fk) is None:
                    res.err(f"{sl}: forms key {fk!r} names no grammatical category the builder knows "
                            f"({sorted(L.CAT_ALIASES)}, optionally '+upasarga')")
        for which in ("plain", "rich"):
            c = s.get(which)
            if c is None and which == "rich":
                continue
            if not (isinstance(c, dict) and c.get("word") and c.get("locus")):
                res.err(f"{sl}: `{which}` must be {{word, locus}}")
            else:
                locus_exists(res, f"{sl} {which}", c["locus"])
        if chosen == "rich" and not isinstance(s.get("rich"), dict):
            res.err(f"{sl}: chosen rich without a rich candidate")
        jc = s.get("joycean")
        if chosen == "joycean" and not isinstance(jc, dict):
            res.err(f"{sl}: chosen joycean without a joycean record")
        if isinstance(jc, dict):
            for f in ("expression", "parts", "relation", "paraphrase"):
                if not jc.get(f):
                    res.err(f"{sl}: joycean.{f} missing")
        fb = s.get("forbidden", [])
        if not isinstance(fb, list) or not all(isinstance(x, str) for x in fb):
            res.err(f"{sl}: forbidden must be a list of strings")
        eng = [x.lower() for x in L.base_english(forms or {})]
        for x in fb if isinstance(fb, list) else []:
            if x.lower() in eng:
                res.err(f"{sl}: '{x}' is both a form and forbidden")
        if not preserve:
            for w in eng:
                owner = reserved.get(w)
                if owner and owner != row:
                    res.err(f"{sl}: English '{w}' is reserved for the row {owner} (standard §7.6: two Sanskrit words never share one English word)")
        ml = s.get("meaning_lines")
        if not isinstance(ml, list) or not ml:
            res.err(f"{sl}: meaning_lines must be a non-empty list")
        else:
            for j, ln in enumerate(ml):
                if not isinstance(ln, dict) or ln.get("cat") not in MEANING_CATS:
                    res.err(f"{sl} meaning_lines[{j}]: cat must be one of {MEANING_CATS}")
                    continue
                if ln["cat"] in ("reception", "synthesis"):
                    res.err(f"{sl} meaning_lines[{j}]: no {ln['cat']} lines in the lexicon (they come from the blind check / the owner)")
                if not (ln.get("text") or "").strip():
                    res.err(f"{sl} meaning_lines[{j}]: text missing")
                if ln["cat"] in ("lexical", "nirvacana", "commentator") and not (ln.get("who") or "").strip():
                    res.err(f"{sl} meaning_lines[{j}]: `who` missing")
                if ln.get("locus"):
                    locus_exists(res, f"{sl} meaning_lines[{j}]", ln["locus"])
        occ = s.get("occurrences")
        if not isinstance(occ, list) or not occ:
            res.err(f"{sl}: occurrences must list the verses this sense covers")
        else:
            for o in occ:
                if not C.parse_occurrence(str(o)):
                    res.err(f"{sl}: occurrence {o!r} is not a Gītā locus")
        public_text(res, sl, {k: s.get(k) for k in ("gloss", "image", "why", "forms")} |
                    {"meaning_lines": [x.get("text") for x in ml or [] if isinstance(x, dict)]})
    if len(rows) > 1:
        res.err(f"{label}: senses of one entry must share one row prefix (got {sorted(rows)})")
    return ids


def validate_lexicon(path: Path) -> Result:
    res = Result()
    d = C.read_json(path)
    if _schema(d) != C.SCHEMA_LEXICON:
        res.err(f"schema must be {C.SCHEMA_LEXICON}")
    job = d.get("job")
    inp = job_input(job, "lexicon") if job else None
    if inp is None:
        res.warn(f"no job input found for {job!r}; lemma coverage not checked")
    pol = L.load_policy()
    # a sense of the current table restated under the same id is an amendment (merge records the diff);
    # an id another lexicon output already defines is a collision
    others = {sid: x["origin"] for sid, x in L.sense_index(pol).items() if x["origin"] not in (f"lexicon {job}", "table")}
    entries = d.get("entries")
    if not isinstance(entries, list) or not entries:
        res.err("entries must be a non-empty list")
        return res
    want = {C.nfc(l["lemma"]): l for l in (inp or {}).get("lemmas", [])}
    got = set()
    english_rows: dict[str, set] = {}
    chapters = set()
    for k, e in enumerate(entries):
        lab = f"entries[{k}] {e.get('lemma')}"
        key = C.nfc(e.get("inventory") or e.get("lemma") or "")
        il = want.get(key) or next((x for n, x in want.items() if C.latin_key(n) == C.latin_key(key)), None)
        if il:
            got.add(C.nfc(il["lemma"]))
        elif inp is not None:
            res.err(f"{lab}: not a lemma of this job (give `inventory` with the job's lemma it covers)")
        ids = check_entry(res, lab, e, pol, (il or {}).get("forms"), others)
        for sid in ids:
            others.setdefault(sid, f"this output {lab}")
        for s in e.get("senses") or []:
            if not (s.get("preserve") or s.get("chosen") == "preserve"):
                for w in L.base_english(s.get("forms") or {}):
                    english_rows.setdefault(w.lower(), set()).add((s.get("id") or ".").split(".")[0])
            for o in s.get("occurrences") or []:
                po = C.parse_occurrence(str(o))
                if po:
                    chapters.add(int(po[0].split(".")[0]))
                    if il and po[0] not in il.get("verses", []):
                        res.warn(f"{lab}: occurrence {o} is not among the inventory's verses for this lemma")
    for w, rs in english_rows.items():
        if len(rs) > 1:
            res.err(f"English '{w}' given to two rows in this batch: {sorted(rs)}")
    for k, rq in enumerate(d.get("lexicon_requests") or []):
        if not (isinstance(rq, dict) and rq.get("lemma") and (rq.get("why") or rq.get("reason"))):
            res.err(f"lexicon_requests[{k}]: needs lemma and why (a lemma this batch needs decided in its own job)")
    missing = sorted(set(want) - got)
    if missing:
        res.err(f"lemmas of the job without an entry: {missing}")
    no_secondaries(res, "lexicon", entries, chapters or set(C.VERSE_COUNTS))
    return res


def validate_lexicon_review(path: Path) -> Result:
    res = Result()
    d = C.read_json(path)
    if _schema(d) != C.SCHEMA_LEXICON_REVIEW:
        res.err(f"schema must be {C.SCHEMA_LEXICON_REVIEW}")
    lj = d.get("lexicon_job")
    lp = C.ns() / "out/lexicon" / f"{lj}.json"
    if not lj or not lp.is_file():
        res.err(f"lexicon_job {lj!r} names no lexicon output ({C.rel(lp)})")
        return res
    if d.get("lexicon_sha256") != C.sha256_file(lp):
        res.err("lexicon_sha256 is not the sha256 of the lexicon output as it stands (reviewed a different version?)")
    lx = C.read_json(lp)
    lemmas = {C.nfc(e.get("lemma") or "") for e in lx.get("entries") or []}
    sids = {s.get("id") for e in lx.get("entries") or [] for s in e.get("senses") or []}
    rows = {x.split(".")[0] for x in sids if x}
    findings = d.get("findings")
    if not isinstance(findings, list):
        res.err("findings must be a list")
        findings = []
    for k, f in enumerate(findings):
        fl = f"findings[{k}]"
        if C.nfc(f.get("lemma") or "") not in lemmas and f.get("lemma") not in rows:
            res.err(f"{fl}: lemma {f.get('lemma')!r} is not in the batch")
        s = f.get("sense")
        if s and s not in sids and not any(x.endswith("." + str(s)) for x in sids):
            res.err(f"{fl}: sense {s!r} is not in the batch")
        if f.get("severity") not in (1, 2, 3):
            res.err(f"{fl}: severity must be 1, 2 or 3")
        if f.get("check") not in LEXREVIEW_CHECKS:
            res.err(f"{fl}: check must be one of {sorted(LEXREVIEW_CHECKS)}")
        for x in ("says", "should_be"):
            if not (f.get(x) or "").strip():
                res.err(f"{fl}: `{x}` missing")
        if not isinstance(f.get("evidence"), list):
            res.err(f"{fl}: evidence must be a list of loci and quotes")
    if d.get("verdict") not in ("accept", "revise"):
        res.err("verdict must be accept or revise")
    open_s1 = [f for f in findings if f.get("severity") == 1 and f.get("status", "open") != "resolved"]
    if d.get("verdict") == "accept" and open_s1:
        res.err(f"verdict accept with {len(open_s1)} open S1 finding(s)")
    return res


# ---------------------------------------------------------------- verse
def _packet(locus: str) -> dict | None:
    p = C.packet_path(locus)
    return C.read_json(p) if p.is_file() else None


def check_manual(res: Result, label: str, a: dict) -> None:
    missing = [k for k in ANALYSIS_KEYS if k not in ("id",) and k not in a]
    if missing:
        res.err(f"{label}: manual analysis lacks {missing} (every Analysis field, null where it does not apply)")
    if a.get("source") != "manual":
        res.err(f"{label}: manual analysis must have source 'manual'")
    if a.get("kind") not in KINDS:
        res.err(f"{label}: kind {a.get('kind')!r} not in {sorted(KINDS)}")
    d = a.get("dhatu")
    if d:
        if not (d.get("root") and N.gana(d.get("gana")) and N.pada(d.get("pada"))):
            res.err(f"{label}: manual dhatu needs root, gana (1–10) and pada")
        i = N.dp_id(d)
        from .expand import dhatupatha
        rec = dhatupatha().get(i) if i else None
        if not rec:
            res.err(f"{label}: manual dhatu's dp_locus/dp_record does not resolve in dhatupatha.json")
        elif int(rec["gana"]) != N.gana(d.get("gana")) or rec["pada"] != N.pada(d.get("pada")):
            res.err(f"{label}: manual dhatu says gaṇa {d.get('gana')} {d.get('pada')}; the record is {rec['gana']}{rec['pada']}")


INLINE_CATS = ("formation", "lexical", "nirvacana", "usage")


def check_inline(res: Result, wl: str, w: dict) -> None:
    """SCHEMAS 'Inline sense fields': a content word without a lexicon sense carries english, image,
    plain {word, locus}, rich {word, locus, tags} | null, chosen ∈ plain|rich|joycean, joycean when
    chosen, why, and 1–4 meaning_lines (formation|lexical|nirvacana|usage, {cat, text, who, locus})."""
    lab = f"{wl}: a content word without a lexicon sense is decided inline —"
    for f in ("why", "image"):
        if not (isinstance(w.get(f), str) and w[f].strip()):
            res.err(f"{lab} `{f}` missing")
    ml = w.get("meaning_lines")
    if not (isinstance(ml, list) and 1 <= len(ml) <= 4):
        res.err(f"{lab} `meaning_lines` must hold 1–4 lines chosen from the packet's meaning page")
    else:
        for j, ln in enumerate(ml):
            if not (isinstance(ln, dict) and ln.get("cat") in INLINE_CATS and (ln.get("text") or "").strip()):
                res.err(f"{wl} meaning_lines[{j}]: needs cat (one of {list(INLINE_CATS)}) and text")
            elif ln["cat"] in ("lexical", "nirvacana") and not ((ln.get("who") or "").strip() and ln.get("locus")):
                res.err(f"{wl} meaning_lines[{j}]: `who` and `locus` required")
            elif ln.get("locus"):
                locus_exists(res, f"{wl} meaning_lines[{j}]", ln["locus"])
    for which in ("plain", "rich"):
        c = w.get(which)
        if c is None and which == "rich":
            continue
        if not (isinstance(c, dict) and c.get("word") and c.get("locus")):
            res.err(f"{lab} `{which}` must be {{word, locus}} (the headword's own define entry)")
        else:
            locus_exists(res, f"{wl} {which}", c["locus"])
    ch = w.get("chosen")
    if ch not in ("plain", "rich", "joycean"):
        res.err(f"{lab} `chosen` must be plain, rich or joycean (inline senses are always translated)")
    elif ch == "rich" and not isinstance(w.get("rich"), dict):
        res.err(f"{lab} chosen rich without `rich`")
    elif ch == "joycean":
        jc = w.get("joycean")
        if not isinstance(jc, dict) or any(not jc.get(f) for f in ("expression", "parts", "relation", "paraphrase")):
            res.err(f"{lab} chosen joycean needs `joycean` {{expression, parts, relation, paraphrase}}")


def validate_verse(path: Path, run_builder: bool = True) -> Result:
    from .expand import Expander
    from .store import Store
    res = Result()
    d = C.read_json(path)
    if _schema(d) != C.SCHEMA_VERSE:
        res.err(f"schema must be {C.SCHEMA_VERSE}")
    job = d.get("job")
    inp = job_input(job, "verse") if job else None
    verses = d.get("verses") or []
    got = [v.get("locus") for v in verses]
    if inp and got != inp.get("verses"):
        res.err(f"verses must be exactly {inp['verses']} in order (got {got})")
    reqs = d.get("lexicon_requests") or []
    req_entries = []
    req_targets = set()
    for k, r in enumerate(reqs):
        rl = f"lexicon_requests[{k}]"
        if not r.get("lemma"):
            res.err(f"{rl}: lemma missing")
        if not (r.get("why") or r.get("reason")):
            res.err(f"{rl}: `why` missing")
        for o in ([r["locus"]] if r.get("locus") else []) + list(r.get("occurrences") or []):
            po = C.parse_occurrence(str(o))
            if not po:
                res.err(f"{rl}: locus {o!r} is not 'C.V:i'")
            else:
                req_targets.add(po)
        e = L.request_entry(r)
        if e is not None:                 # a proposed entry: its sense may be used now, reviewed with the shard
            req_entries.append(e)
            check_entry(res, rl, e, L.load_policy(), None, {})
        else:                             # no proposal: the lemma goes to a lexicon job; the word is decided inline meanwhile
            req_targets.difference_update({po for o in ([r.get("locus")] + list(r.get("occurrences") or [])) if o
                                           and (po := C.parse_occurrence(str(o)))})
    try:
        store = Store()
    except FileNotFoundError as e:
        res.err(str(e))
        return res
    ex = Expander(extra_entries=req_entries, store=store)
    b = builder()
    chapters = set()
    for v in verses:
        loc = v.get("locus")
        lab = f"{loc}"
        pk = _packet(loc) if C.parse_verse_locus(loc or "") else None
        if pk is None:
            res.err(f"{lab}: no verse packet for this locus")
            continue
        chapters.add(pk["chapter"])
        padas = v.get("padas") or []
        if not padas or not all(isinstance(p, str) and p.strip() for p in padas):
            res.err(f"{lab}: padas must be a non-empty list of strings")
            continue
        bad = b.align_padas(b.samhita_tokens(pk["iast"]), [C.latin_key(p) for p in padas])
        if bad is not None:
            res.err(f"{lab}: padas do not recompose to the saṃhitā (first unmatched BORI token #{bad})")
        words = v.get("words") or []
        if [w.get("i") for w in words] != list(range(len(padas))):
            res.err(f"{lab}: words must be i = 0..{len(padas) - 1}, one per pada")
        smap = b.slot_map(v.get("line") or "")
        rest = b.SLOT_RE.sub("", v.get("line") or "")
        if "{" in rest or "}" in rest:
            res.err(f"{lab}: malformed slot in line")
        for i in smap:
            if not 0 <= i < len(padas):
                res.err(f"{lab}: slot {{{i}:…}} names no word")
        gloss_loci = {g.get("locus") for t in pk.get("tokens") or [] for g in t.get("glosses") or []}
        for w in words:
            i = w.get("i")
            wl = f"{lab}[{i}] {padas[i] if isinstance(i, int) and i < len(padas) else '?'}"
            if not isinstance(i, int) or not 0 <= i < len(padas):
                continue
            ref = w.get("analysis")
            form = C.form_key(padas[i])
            fe = pk["forms"].get(form) or {}
            ids_here = {a["id"] for a in fe.get("analyses", [])} | set(fe.get("all_ids") or [])
            an = None
            if isinstance(ref, str):
                if ref not in ids_here:
                    got_ = store.get(ref)
                    res.err(f"{wl}: analysis {ref} is not among the packet's analyses of '{padas[i]}'"
                            + (f" (it analyses '{got_[0].get('form')}')" if got_ else " (unknown id)")
                            + ("; the packet has none for this form — use {manual: …}" if not ids_here else ""))
                else:
                    an = store.get(ref)[0]
            elif isinstance(ref, dict) and isinstance(ref.get("manual"), dict):
                an = ref["manual"]
                check_manual(res, wl, an)
            else:
                res.err(f"{wl}: analysis must be a packet id or {{manual: Analysis}}")
            comp = w.get("compound")
            if comp is not None:
                if not (isinstance(comp, dict) and comp.get("type") and comp.get("vigraha") and isinstance(comp.get("members"), list) and comp["members"]):
                    res.err(f"{wl}: compound must be {{type, vigraha, members[]}}")
                else:
                    for m in comp["members"]:
                        mr = m.get("analysis")
                        if isinstance(mr, str) and store.get(mr) is None:
                            res.err(f"{wl}: member {m.get('form')}: unknown analysis id {mr}")
                        elif isinstance(mr, dict) and isinstance(mr.get("manual"), dict):
                            check_manual(res, f"{wl} member {m.get('form')}", mr["manual"])
                        elif mr is not None and not isinstance(mr, (str, dict)):
                            res.err(f"{wl}: member {m.get('form')}: analysis must be an id or {{manual: …}}")
            sid = w.get("sense")
            wc = w.get("word_class") or (N.word_class(an) if an else None)
            if sid is not None and sid not in ex.index:
                res.err(f"{wl}: sense {sid!r} is not in the lexicon or this output's lexicon_requests")
            if sid is None and wc == "content" and (loc, i) not in req_targets:
                check_inline(res, wl, w)
            eng = w.get("english")
            if not (isinstance(eng, str) and eng.strip()):
                res.err(f"{wl}: english missing")
            elif i not in smap:
                res.err(f"{wl}: the word is not slotted in the line")
            elif eng not in smap[i]:
                res.err(f"{wl}: english '{eng}' is not the text of its slot ({smap[i]})")
            cl = w.get("commentator_lines") or []
            if not isinstance(cl, list):
                res.err(f"{wl}: commentator_lines must be a list")
                cl = []
            for j, c in enumerate(cl):
                if not (isinstance(c, dict) and c.get("who") and c.get("locus") and c.get("text")):
                    res.err(f"{wl} commentator_lines[{j}]: needs who, locus, text")
                elif c["locus"] not in gloss_loci:
                    res.warn(f"{wl} commentator_lines[{j}]: locus {c['locus']} is not one of the packet's gloss hits for this verse")
        public_text(res, lab, {"line": v.get("line"), "sense": v.get("sense"),
                               "words": [{k: w.get(k) for k in ("english", "note", "why", "image")} | {"c": [c.get("text") for c in w.get("commentator_lines") or [] if isinstance(c, dict)],
                                                                                    "m": [x.get("text") for x in w.get("meaning_lines") or [] if isinstance(x, dict)]}
                                         for w in words],
                               "forks": [f.get("display") for f in v.get("forks") or [] if isinstance(f, dict)]})
    no_secondaries(res, "verse output", {"verses": verses, "requests": reqs}, chapters)
    if run_builder and not res.errors:
        builder_check(res, ex, d, path)
    return res


def builder_check(res: Result, ex, vo: dict, path: Path) -> dict | None:
    """Expand in memory and run the builder's own verse/card checks (unreviewed check mode)."""
    b = builder()
    sec = secondaries_names(vo)
    shard, errs = ex.shard(vo, C.rel(path), C.sha256_file(path), secondaries=sec)
    for e in errs:
        res.err(f"expansion: {e}")
    if not shard["verses"]:
        return shard
    ch = shard["chapter"]
    ctx = b.Ctx(chapter=ch, policy_path=ex.policy_path, complete=False, run_render_contract=False)
    define_cache: dict = {}
    for v in shard["verses"]:
        pv = {"iast": v["iast"], "devanagari": v["devanagari"], "speaker": v["speaker"]}
        b.check_verse(ctx, v, pv, translator_names(), define_cache)
    for check, msg, _ in ctx.report.errors:
        if "production may use only" in msg:
            res.warn(f"builder {check}: {msg} (a stage-E gate, not this job's)")
        else:
            res.err(f"builder {check}: {msg}")
    for check, msg, _ in ctx.report.warnings:
        res.warn(f"builder {check}: {msg}")
    return shard


def secondaries_names(vo: dict) -> list[str]:
    chs = {int(v["locus"].split(".")[0]) for v in vo.get("verses") or [] if C.parse_verse_locus(v.get("locus") or "")}
    names: list[str] = []
    for ch in sorted(chs):
        p = C.PIPE / "secondaries" / f"{ch}.json"
        if p.is_file():
            d = C.read_json(p)
            for items in (d.get("verses") or {}).values():
                for it in items:
                    if it.get("author") and it["author"] not in names:
                        names.append(it["author"])
            for k, label in (("besant_das_1905", "Besant–Das 1905"), ("roy_aurobindo_1938", "Roy/Aurobindo 1938"), ("cwsa19", "Sri Aurobindo, Essays on the Gita")):
                if d.get(k) and label not in names:
                    names.append(label)
    return names


# ---------------------------------------------------------------- review
def git_ignored(path: Path) -> bool:
    r = subprocess.run(["git", "check-ignore", "-q", str(path)], cwd=str(C.ROOT), capture_output=True)
    return r.returncode == 0


def validate_review(path: Path) -> Result:
    res = Result()
    d = C.read_json(path)
    if _schema(d) != C.SCHEMA_REVIEW:
        res.err(f"schema must be {C.SCHEMA_REVIEW}")
    if not git_ignored(path):
        res.err(f"{C.rel(path)} is not git-ignored; a review quotes published translations and must stay private")
    job = d.get("job")
    inp = job_input(job, "review") if job else None
    vpath = C.ROOT / inp["verse_output"] if inp else None
    if vpath is None or not vpath.is_file():
        res.err(f"cannot find the verse output this review covers (job input for {job!r})")
        return res
    if d.get("shard_sha256") != C.sha256_file(vpath):
        res.err("shard_sha256 is not the sha256 of the verse output as it stands (it changed during review?)")
    vo = C.read_json(vpath)
    nwords = {v["locus"]: len(v.get("words") or []) for v in vo.get("verses") or []}
    for k, f in enumerate(d.get("findings") or []):
        fl = f"findings[{k}]"
        if f.get("locus") not in nwords:
            res.err(f"{fl}: locus {f.get('locus')!r} is not in the shard")
        elif f.get("word_i") is not None and not (isinstance(f["word_i"], int) and 0 <= f["word_i"] < nwords[f["locus"]]):
            res.err(f"{fl}: word_i {f.get('word_i')!r} out of range")
        if f.get("severity") not in (1, 2, 3):
            res.err(f"{fl}: severity must be 1, 2 or 3")
        if f.get("check") not in REVIEW_CHECKS:
            res.err(f"{fl}: check must be one of {sorted(REVIEW_CHECKS)}")
        for x in ("says", "should_be"):
            if not (f.get(x) or "").strip():
                res.err(f"{fl}: `{x}` missing")
        if not isinstance(f.get("evidence"), list):
            res.err(f"{fl}: evidence must be a list")
    if not isinstance(d.get("findings"), list):
        res.err("findings must be a list")
    bsc = d.get("blind_secondary_check")
    seen = {x.get("locus") for x in bsc or [] if isinstance(x, dict)}
    if not isinstance(bsc, list) or seen != set(nwords):
        res.err(f"blind_secondary_check must have one entry per verse {sorted(nwords, key=C.locus_sort_key)} (got {sorted(x for x in seen if x)})")
    for k, r in enumerate(d.get("readers_will_meet") or []):
        rl = f"readers_will_meet[{k}]"
        if r.get("locus") not in nwords or not (isinstance(r.get("word_i"), int) and 0 <= r["word_i"] < nwords.get(r.get("locus"), 0)):
            res.err(f"{rl}: locus/word_i do not name a word of the shard")
        for x in r.get("renderings") or []:
            if not (x.get("who") and x.get("word")):
                res.err(f"{rl}: each rendering needs who and word")
            elif len(re.findall(r"[A-Za-z']+", x["word"])) > 8:
                res.err(f"{rl}: rendering longer than eight words")
    if d.get("verdict") not in ("accept", "revise"):
        res.err("verdict must be accept or revise")
    s1 = [f for f in d.get("findings") or [] if f.get("severity") == 1 and f.get("status", "open") != "resolved"]
    if d.get("verdict") == "accept" and s1:
        res.err(f"verdict accept with {len(s1)} open S1 finding(s)")
    return res


VALIDATORS = {"lexicon": validate_lexicon, "lexicon-fix": validate_lexicon, "lexicon-review": validate_lexicon_review,
              "lexicon-rereview": validate_lexicon_review, "verse": validate_verse, "fix": validate_verse,
              "review": validate_review, "rereview": validate_review}

"""The Gītā lexicon: accepted lexicon outputs (and accepted verse-job lexicon requests) merged into
the term policy v3 = the v2 structure (`lemmas` → `senses` with `forms` per grammatical
category, `reserved_english`, `status`), a superset of the current table. Legacy v1 rows are
migrated with `scripts/migrate_term_policy_v2.py`'s own `migrate()`; new senses get status
`lexicon-reviewed`; conflicts (two rows claiming one English word, a sense id defined twice,
a legacy decision changed) are reported, and a conflict involving a new row refuses install.
"""
from __future__ import annotations

import fcntl
import json
import re
import sys
from pathlib import Path

from . import common as C

# lexicon `forms` keys → the builder's grammatical categories (build_gita_chapter_reader.form_category)
BUILDER_CATS = {"finite", "noun", "participle_past", "participle_past_active", "participle_present", "absolutive",
                "infinitive", "agent", "any"}
CAT_ALIASES = {"verb": "finite", "finite": "finite", "noun": "noun", "plural": "noun", "predicate": "noun",
               "adjective": "noun", "adverb": "noun", "gerundive": "noun", "name": "noun", "vocative": "noun",
               "participle": "participle_past", "past_participle": "participle_past", "participle_past": "participle_past",
               "participle_past_active": "participle_past_active", "present_participle": "participle_present",
               "participle_present": "participle_present", "absolutive": "absolutive", "having": "absolutive",
               "infinitive": "infinitive", "agent": "agent", "agent_noun": "agent", "any": "any"}
CHOSEN = {"plain", "rich", "joycean", "preserve"}


def cat_of(key: str) -> str | None:
    base = re.split(r"[+:]", key.strip().lower().replace(" ", "_"))[0]
    return CAT_ALIASES.get(base)


def _inflect(phrase: str) -> list[str]:
    """Regular English inflections of a verb phrase's first word (admitted, never chosen)."""
    w, _, rest = phrase.partition(" ")
    tail = f" {rest}" if rest else ""
    if not w.isalpha():
        return [phrase]
    if re.search(r"(s|sh|ch|x|z)$", w):
        s3 = w + "es"
    elif re.search(r"[^aeiou]y$", w):
        s3 = w[:-1] + "ies"
    else:
        s3 = w + "s"
    if w.endswith("e"):
        ed, ing = w + "d", w[:-1] + "ing"
    elif re.search(r"[^aeiou]y$", w):
        ed, ing = w[:-1] + "ied", w + "ing"
    else:
        ed, ing = w + "ed", w + "ing"
    return list(dict.fromkeys([phrase, s3 + tail, ed + tail, ing + tail]))


def builder_forms(forms: dict) -> tuple[dict[str, list[str]], list[str]]:
    """Lexicon forms → {builder category: [admitted English]} and the keys that map to none."""
    out: dict[str, list[str]] = {}
    unmapped = []
    for k, v in (forms or {}).items():
        vals = [v] if isinstance(v, str) else [x for x in (v or []) if isinstance(x, str)]
        cat = cat_of(k)
        if cat is None:
            unmapped.append(k)
            continue
        if cat == "finite":
            vals = [x for val in vals for x in _inflect(val)]
        out.setdefault(cat, [])
        out[cat] += [x for x in vals if x not in out[cat]]
    return out, unmapped


def base_english(forms: dict) -> list[str]:
    out = []
    for v in (forms or {}).values():
        for x in ([v] if isinstance(v, str) else v or []):
            if isinstance(x, str) and x not in out:
                out.append(x)
    return out


# ---------------------------------------------------------------- reading the outputs
def out_dir(kind: str) -> Path:
    return C.ns() / "out" / kind


def review_dir(kind: str) -> Path:
    return C.ns() / ("private/out" if kind in ("review", "rereview") else "out") / kind


def accepted_lexicon_outputs() -> list[tuple[Path, dict, dict]]:
    """(path, lexicon output, accepting review) for every lexicon output whose most recent review
    at the output's current sha256 says accept."""
    reviews: dict[str, list[tuple[float, dict]]] = {}
    for kind in ("lexicon-review", "lexicon-rereview"):
        for p in sorted(review_dir(kind).glob("*.json")):
            try:
                r = C.read_json(p)
            except (OSError, json.JSONDecodeError):
                continue
            if r.get("schema") == C.SCHEMA_LEXICON_REVIEW and r.get("lexicon_job"):
                reviews.setdefault(r["lexicon_job"], []).append((p.stat().st_mtime, r))
    out = []
    for p in sorted(out_dir("lexicon").glob("*.json")):
        try:
            lx = C.read_json(p)
        except (OSError, json.JSONDecodeError):
            continue
        sha = C.sha256_file(p)
        rs = sorted((x for x in reviews.get(lx.get("job"), []) if x[1].get("lexicon_sha256") == sha), key=lambda x: x[0])
        if rs and rs[-1][1].get("verdict") == "accept":
            out.append((p, lx, rs[-1][1]))
    return out


def accepted_requests() -> list[tuple[str, dict]]:
    """Lexicon requests from verse outputs whose latest review at the output's sha256 accepts."""
    reviews: dict[str, list[tuple[float, dict]]] = {}
    for kind in ("review", "rereview"):
        for p in sorted(review_dir(kind).glob("*.json")):
            try:
                r = C.read_json(p)
            except (OSError, json.JSONDecodeError):
                continue
            if r.get("schema") == C.SCHEMA_REVIEW:
                reviews.setdefault(r.get("verse_job") or r.get("job", "").replace("rereview-", "verse-").replace("review-", "verse-").split("-r")[0],
                                   []).append((p.stat().st_mtime, r))
    out = []
    for p in sorted(out_dir("verse").glob("*.json")):
        try:
            vo = C.read_json(p)
        except (OSError, json.JSONDecodeError):
            continue
        sha = C.sha256_file(p)
        rs = sorted((x for x in reviews.get(vo.get("job"), []) if x[1].get("shard_sha256") == sha), key=lambda x: x[0])
        if rs and rs[-1][1].get("verdict") == "accept":
            for req in vo.get("lexicon_requests") or []:
                out.append((vo.get("job"), req))
    return out


def accepted_verse_outputs() -> list[tuple[str, dict]]:
    """(verse job, output) for every verse output whose latest review at its current sha256 accepts."""
    reviews: dict[str, list[tuple[float, dict]]] = {}
    for kind in ("review", "rereview"):
        for p in sorted(review_dir(kind).glob("*.json")):
            try:
                r = C.read_json(p)
            except (OSError, json.JSONDecodeError):
                continue
            inp = C.ns() / "jobs/review" / f"{r.get('job')}.input.json"
            vj = C.read_json(inp).get("verse_job") if inp.is_file() else None
            if r.get("schema") == C.SCHEMA_REVIEW and vj:
                reviews.setdefault(vj, []).append((p.stat().st_mtime, r))
    out = []
    for p in sorted(out_dir("verse").glob("*.json")):
        try:
            vo = C.read_json(p)
        except (OSError, json.JSONDecodeError):
            continue
        rs = sorted((x for x in reviews.get(vo.get("job"), []) if x[1].get("shard_sha256") == C.sha256_file(p)), key=lambda x: x[0])
        if rs and rs[-1][1].get("verdict") == "accept":
            out.append((vo.get("job"), vo))
    return out


def inline_entries(outputs: list[tuple[str, dict]]) -> list[dict]:
    """Content words decided inline (sense null, english + why + meaning_lines) in accepted verse
    outputs → gita-lexicon-v1 entries: row = the lemma's ASCII key, sense = the English, so a later
    chapter reuses the decision by id; the same English for the same lemma merges its occurrences."""
    from . import names as N
    from .store import Store
    try:
        st = Store()
    except FileNotFoundError:
        st = None
    rows: dict[str, dict] = {}
    for job, vo in outputs:
        for v in vo.get("verses") or []:
            for w in v.get("words") or []:
                if w.get("sense") is not None or not w.get("meaning_lines") or not (w.get("english") or "").strip():
                    continue
                ref = w.get("analysis")
                an = (st.get(ref)[0] if st and isinstance(ref, str) and st.get(ref) else
                      ref.get("manual") if isinstance(ref, dict) else None) or {}
                if (w.get("word_class") or N.word_class(an)) != "content":
                    continue
                lemma = an.get("stem") or N.verb_stem(an) or (v.get("padas") or [""])[w.get("i", 0)]
                row = C.latin_key(lemma)
                sname = re.sub(r"[^a-z0-9]+", "-", C.latin_key(w["english"]) or w["english"].lower()).strip("-")[:40] or "s"
                cat = N.form_category(an)
                e = rows.setdefault(row, {"lemma": lemma, "match": "(^|-)" + re.escape(lemma), "senses": {}, "inline_from": set()})
                s = e["senses"].setdefault(sname, {"id": f"{row}.{sname}", "gloss": w["why"], "image": w.get("image") or w["why"],
                                                   "preserve": False, "forms": {}, "plain": w.get("plain"), "rich": w.get("rich"),
                                                   "chosen": w.get("chosen"), "why": w["why"], "joycean": w.get("joycean"),
                                                   "forbidden": [], "meaning_lines": w["meaning_lines"], "occurrences": []})
                s["forms"].setdefault("finite" if cat == "finite" else cat, w["english"])
                s["occurrences"].append(f"{v['locus']}:{w.get('i')}")
                e["inline_from"].add(job)
    out = []
    for row, e in rows.items():
        ss = list(e["senses"].values())
        for s in ss:
            if s.get("chosen") not in ("plain", "rich", "joycean"):
                s["chosen"] = "plain"
        out.append({**e, "senses": ss, "inline_from": sorted(e["inline_from"]),
                    # one lemma decided inline with different English: not merged; it goes to a lexicon job
                    "divergent": len(ss) > 1})
    return out


def request_entry(req: dict) -> dict | None:
    """The gita-lexicon-v1 entry a verse-job lexicon request proposes (`proposal` or `entry`)."""
    e = req.get("proposal") if isinstance(req.get("proposal"), dict) else req.get("entry")
    return e if isinstance(e, dict) and isinstance(e.get("senses"), list) else None


# ---------------------------------------------------------------- the policy as a sense index
def load_policy(path: Path | None = None) -> dict:
    return C.read_json(path or C.current_policy_path())


def policy_rows(pol: dict) -> dict:
    return pol.get("lemmas") or pol.get("terms") or {}


def sense_index(pol: dict | None = None, include_outputs: bool = True, extra_entries: list[dict] | None = None) -> dict[str, dict]:
    """sense id ('row.sense') → {row, sense, data, origin} over the table, accepted lexicon
    outputs (not yet merged) and any extra entries (a verse output's own requests)."""
    pol = pol if pol is not None else load_policy()
    idx: dict[str, dict] = {}
    for row, r in policy_rows(pol).items():
        for sname, s in (r.get("senses") or {}).items():
            idx[f"{row}.{sname}"] = {"row": row, "sense": sname, "data": s, "row_data": r, "origin": "table"}
    entries: list[tuple[str, dict]] = []
    if include_outputs:
        entries += [(f"lexicon {lx.get('job')}", e) for _, lx, _ in accepted_lexicon_outputs() for e in lx.get("entries") or []]
    entries += [("this output", e) for e in extra_entries or []]
    for origin, e in entries:
        for s in e.get("senses") or []:
            sid = s.get("id") or ""
            if "." not in sid:
                continue
            row, sname = sid.split(".", 1)
            if sid in idx and idx[sid]["origin"] == "table" and origin != "this output":
                idx[sid] = {**idx[sid], "lexicon": s, "entry": e}
                continue
            idx[sid] = {"row": row, "sense": sname, "data": s, "entry": e, "lexicon": s, "origin": origin}
    return idx


# ---------------------------------------------------------------- merge
def _migrate_legacy(pol: dict, legacy_status: str) -> tuple[dict, dict]:
    if "lemmas" in pol:
        return json.loads(json.dumps(pol)), {"already": pol.get("version")}
    sys.path.append(str(C.ROOT / "scripts"))
    import migrate_term_policy_v2 as M  # noqa: E402
    shards = sorted(C.ROOT.glob("internal/sanskrit_reviews/gita/ch*/producer-*.json"))
    return M.migrate(pol, M.collect_uses(shards), legacy_status)


def sense_record(s: dict, entry: dict, origin: dict) -> tuple[dict, list[str]]:
    preserve = bool(s.get("preserve")) or s.get("chosen") == "preserve"
    rec = {"policy": "preserve" if preserve else "translate"}
    unmapped: list[str] = []
    if preserve:
        rec["iast"] = s.get("iast") or entry.get("lemma")
        forms_iast = [v for v in base_english(s.get("forms") or {}) if rec["iast"] and rec["iast"].lower() in v.lower()]
        if forms_iast:
            rec["iast_forms"] = [rec["iast"]]
    else:
        rec["forms"], unmapped = builder_forms(s.get("forms") or {})
    rec["forbidden_english"] = list(s.get("forbidden") or [])
    gk = s.get("glossaryKey") or s.get("glossary_key")
    if gk:
        rec["glossaryKey"] = gk
    rec["status"] = "lexicon-reviewed"
    rec["applies_to"] = list(s.get("occurrences") or [])
    rec["decided"] = None
    for k in ("gloss", "image", "plain", "rich", "chosen", "why", "joycean", "meaning_lines", "candidates"):
        if s.get(k) is not None:
            rec[k] = s[k]
    rec["lexicon_forms"] = s.get("forms") or {}
    rec["lexicon"] = origin
    return rec, unmapped


def merge(pol: dict, outputs: list[tuple[str, dict, dict]], legacy_status: str = "lexicon-reviewed") -> tuple[dict, dict]:
    """outputs: (origin label, entry, origin record). Returns (v3 policy, report)."""
    v3, mig = _migrate_legacy(pol, legacy_status)
    rows = v3["lemmas"]
    legacy_keys = set(rows) if "lemmas" not in pol else {k for k, r in rows.items() if not any((s.get("lexicon") for s in r["senses"].values()))}
    report = {"migration": {k: v for k, v in mig.items() if k != "status"} if isinstance(mig, dict) else mig,
              "added_senses": [], "enriched_legacy": [], "changed_legacy": [], "conflicts": [], "warnings": [], "unmapped_forms": {}}
    seen: dict[str, str] = {}
    row_from: dict[str, str] = {}
    for label, e, origin in outputs:
        for s in e.get("senses") or []:
            sid = s.get("id") or ""
            row, _, sname = sid.partition(".")
            if not row or not sname:
                report["conflicts"].append({"kind": "malformed sense id", "id": sid, "from": label})
                continue
            if sid in seen and seen[sid] != label:
                prev = rows.get(row, {}).get("senses", {}).get(sname)
                new_forms = sense_record(s, e, origin)[0].get("forms")
                if prev is not None and not label.startswith("lexicon ") and not seen[sid].startswith("lexicon ") \
                        and prev.get("forms") == new_forms:
                    # the same request or inline decision from two shards: one sense, both occurrences
                    prev["applies_to"] = sorted(set(prev.get("applies_to") or []) | set(s.get("occurrences") or []))
                    continue
                report["conflicts"].append({"kind": "sense id defined twice", "id": sid, "rows": [row], "from": {row: label}, "labels": [seen[sid], label]})
                continue
            seen[sid] = label
            rec, unmapped = sense_record(s, e, origin)
            if unmapped:
                report["unmapped_forms"][sid] = unmapped
            r = rows.setdefault(row, {"lemma_iast": e.get("lemma"), "detect": {"match": e.get("match"), "root_ids": [], "upasargas": []},
                                      "occurrences": [], "dossier": None, "senses": {}})
            if e.get("match") and not (r.get("detect") or {}).get("match"):
                r.setdefault("detect", {})["match"] = e["match"]
            old = r["senses"].get(sname)
            if old is not None and row in legacy_keys:
                same = (old.get("policy") == rec["policy"] and (rec["policy"] == "preserve" or
                        set(base_english(old.get("forms") or {})) <= set(base_english(rec["forms"])) |
                        set(x for v in rec["forms"].values() for x in v)))
                if same:
                    rec["status"] = old.get("status") or rec["status"]
                    report["enriched_legacy"].append(sid)
                else:
                    report["changed_legacy"].append({"id": sid, "old": old.get("forms") or old.get("iast"),
                                                     "new": rec.get("forms") or rec.get("iast"), "from": label})
                for k in ("glossaryKey", "note"):
                    if k in old and k not in rec:
                        rec[k] = old[k]
                if old.get("iast_forms"):          # a preserved term's admitted spellings (yoga, yogī …) survive
                    rec["iast_forms"] = list(dict.fromkeys(list(old["iast_forms"]) + list(rec.get("iast_forms") or [])))
            else:
                report["added_senses"].append(sid)
            r["senses"][sname] = rec
            row_from[row] = label
            r["occurrences"] = sorted(set(r.get("occurrences") or []) | set(rec["applies_to"]))
    # English distinctness across rows (standard §7.6)
    owners: dict[str, set[str]] = {}
    for row, r in rows.items():
        for sname, s in r["senses"].items():
            if s.get("policy") != "translate":
                continue
            words = base_english(s.get("lexicon_forms") or {}) or base_english(s.get("forms") or {})
            for w in words:
                owners.setdefault(w.lower(), set()).add(row)
    reserved = {}
    for w, rs in sorted(owners.items()):
        if len(rs) == 1:
            reserved[w] = next(iter(rs))
        else:
            new = [x for x in rs if x not in legacy_keys]
            item = {"kind": "English claimed by two rows", "english": w, "rows": sorted(rs),
                    "from": {x: row_from.get(x, "table") for x in sorted(rs)}}
            (report["conflicts"] if new else report["warnings"]).append(item)
    v3["reserved_english"] = reserved
    v3["version"] = "3"
    v3["schema"] = "gita-term-policy-v3"
    v3.setdefault("changelog", []).append({"version": "3", "by": "scripts/gita/merge_lexicon.py",
                                           "changes": f"{len(report['added_senses'])} senses added, {len(report['enriched_legacy'])} enriched, "
                                                      f"{len(report['changed_legacy'])} legacy decisions changed"})
    builder = C.import_builder()
    report["policy_sha256"] = builder.policy_content_hash(v3)
    report["senses_not_admitted_by_builder"] = sorted(
        f"{row}.{sn}" for row, r in rows.items() for sn, s in r["senses"].items() if s.get("status") not in ("owner-decided", "lexicon-reviewed", "pilot"))
    return v3, report


class Lock:
    def __init__(self, path: Path) -> None:
        self.path = path

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.f = open(self.path, "w")
        fcntl.flock(self.f, fcntl.LOCK_EX)
        return self

    def __exit__(self, *a):
        fcntl.flock(self.f, fcntl.LOCK_UN)
        self.f.close()

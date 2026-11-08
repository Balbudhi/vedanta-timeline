#!/usr/bin/env python3
"""The chapter-12 round trip (acceptance test of expand_cards.py).

    python3 scripts/gita/convert_ch12.py [--out DIR] [--json]

1. Convert: each reviewed producer-v2 shard (internal/sanskrit_reviews/gita/ch12/producer-*.json)
   is re-expressed as a lean verse-job output (gita-verse-v1): padas, the packet analysis id that
   matches the card (root record, stem, case/number/gender or lakāra/person/number) or a manual
   analysis when none does, the compound with its members, kāraka, sense id from the card's term,
   the slot text, note, the card's commentator lines, the line, sense and forks. Nothing else of
   the card is carried: no display override, no evidence, no wording. Each term's sense becomes a
   gita-lexicon-v1 entry (gloss, image, plain/rich/chosen, why, meaning lines other than
   commentator/reception lines, from the cards of that sense); a content word without a term
   becomes a lexicon request of its verse output, as VERSE_BRIEF prescribes.
2. Expand every converted output against the current table (data/glossary/term_policy.json).
3. Run the fail-closed builder (library call, unreviewed mode, render contract on) on the
   expanded shards and, as the baseline, on the original shards, each in its own temporary
   chapter directory with the chapter's builder packet. Report: lines identical, error classes,
   and card-by-card equality of the identity fields.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from gitapipe import common as C  # noqa: E402

C.fix_sys_path()

CH12 = C.ROOT / "internal/sanskrit_reviews/gita/ch12"
IDENTITY = ("iast", "deva", "stem", "root_id", "word_class", "term", "glossaryKey", "compound.type", "compound.members",
            "meaning.rendering", "meaning.image", "morph", "root")
MORPH_CASE = {"nom": 1, "acc": 2, "instr": 3, "ins": 3, "dat": 4, "abl": 5, "gen": 6, "loc": 7, "voc": 8}


def parse_morph(m: str) -> dict:
    m = (m or "").lower()
    out = {}
    cs = [MORPH_CASE[x] for x in re.findall(r"\b(nom|acc|instr|ins|dat|abl|gen|loc|voc)\.", m)]
    if len(cs) == 1:
        out["vibhakti"] = cs[0]
    for k, pat in (("sg", r"\bsg\b|\bsingular|\b1 ?sg|\b2 ?sg|\b3(rd)? ?sg"), ("du", r"\bdu\b|\bdual"), ("pl", r"\bpl\b|\bplural")):
        if re.search(pat, m):
            out["vacana"] = k
    for k, pat in (("masc", r"\bmasc"), ("fem", r"\bfem"), ("neut", r"\bneut")):
        if re.search(pat, m):
            out["linga"] = k
    for k, pat in ((3, r"\b3(rd)?\b"), (2, r"\b2(nd)?\b"), (1, r"\b1(st)?\b")):
        if re.search(pat, m) and re.search(r"present|future|imperative|optative|perfect|aorist|imperfect|indic|sg\.|pl\.", m):
            out["purusha"] = k
            break
    if "indeclinable" in m or "adverb" in m and "acc." not in m:
        out["avyaya"] = True
    return out


def score(card: dict, a: dict) -> int:
    from gitapipe import names as N
    s = 0
    want = card.get("root_id")
    got = N.dp_id(a.get("dhatu"))
    if want and got:
        s += 4 if want.endswith("#" + got) else -3
    elif got:
        s -= 1
    if C.latin_key(card.get("stem") or "").replace("v", "") == C.latin_key(a.get("stem") or "").replace("v", ""):
        s += 2
    pm = parse_morph(card.get("morph"))
    if "vibhakti" in pm:
        s += 1 if N.vibhakti(a.get("vibhakti")) == pm["vibhakti"] else -2
    if "vacana" in pm:
        s += 1 if N.vacana(a.get("vacana")) == pm["vacana"] else -2
    if "linga" in pm and a.get("linga"):
        s += 1 if N.linga(a.get("linga")) == pm["linga"] else -1
    if "purusha" in pm and a.get("kind") == "tinanta":
        s += 1 if N.purusha(a.get("purusha")) == pm["purusha"] else -2
    if pm.get("avyaya"):
        s += 2 if a.get("kind") == "avyaya" or a.get("avyaya") else -1
    lk = re.search(r"\b(laṭ|loṭ|lṛṭ|liṭ|laṅ|luṅ|vidhiliṅ|āśīrliṅ)\b", f"{card.get('affix')} {card.get('morph')}")
    if lk and a.get("kind") == "tinanta":
        s += 1 if N.lakara(a.get("lakara")) == lk.group(1) else -2
    krt = re.search(r"\b(kta|ktavatu|śatṛ|śānac|ktvā|lyap|tumun)\b", card.get("affix") or "")
    if krt:
        s += 1 if N.affix_name(a.get("krt")) == krt.group(1) else -1
    return s


def manual_from(card: dict) -> dict:
    from gitapipe import names as N
    from gitapipe.expand import dhatupatha
    pm = parse_morph(card.get("morph"))
    dhatu = None
    if card.get("root_id"):
        i = card["root_id"].split("#")[-1]
        rec = dhatupatha().get(i)
        if rec:
            ups = [p["form"].rstrip("-") for p in card.get("parts") or [] if (p.get("form") or "").endswith("-") and not p["form"].startswith("-")]
            dhatu = {"aupadeshika": rec["aupadeshik"], "root": re.sub(r"\s*\(.*", "", (card.get("root") or "").lstrip("√")).split()[0] if card.get("root") else rec["dhatu"],
                     "gana": int(rec["gana"]), "gana_name": N.GANA_NAMES.get(int(rec["gana"])), "pada": rec["pada"], "artha": rec["artha"],
                     "upasargas": ups, "dp_record": f"sources/raw/panini/lexica/dhatupatha.json#{i}"}
    kind = ("samasa" if card.get("compound") else "avyaya" if pm.get("avyaya") else
            "tinanta" if "purusha" in pm else "krdanta" if dhatu else "subanta")
    krt = re.search(r"\b(kta|ktavatu|śatṛ|śānac|ktvā|lyap|tumun|ac|ghañ|lyuṭ|ktin|kvip|ṇini|tṛc)\b", card.get("affix") or "")
    return {"form": card.get("iast"), "kind": kind, "stem": card.get("stem"), "dhatu": dhatu,
            "lakara": (re.search(r"\b(laṭ|loṭ|lṛṭ|liṭ|laṅ|luṅ|vidhiliṅ)\b", f"{card.get('affix')} {card.get('morph')}") or [None, None])[1],
            "prayoga": None, "purusha": pm.get("purusha"), "vacana": pm.get("vacana"), "linga": pm.get("linga"),
            "vibhakti": pm.get("vibhakti"), "krt": krt.group(1) if krt else None, "taddhita": None, "source": "manual"}


def convert(shards: list[Path]) -> tuple[list[dict], dict, dict]:
    from gitapipe.store import Store
    from gitapipe import lexicon as L
    from gitapipe import names as N
    st = Store()
    b = C.import_builder()
    pol = L.load_policy(C.POLICY)
    rows = L.policy_rows(pol)
    stats = collections.Counter()
    by_sense: dict[str, list[tuple[str, dict]]] = collections.defaultdict(list)
    outputs = []
    for sp in shards:
        sh = C.read_json(sp)
        verses = []
        for v in sh["verses"]:
            pk = C.read_json(C.packet_path(v["locus"]))
            smap = b.slot_map(v["english"])
            words, reqs = [], []
            for w in v["words"]:
                fe = pk["forms"].get(C.form_key(w["iast"])) or {}
                fa = [{"id": i} for i in (fe.get("all_ids") or [x["id"] for x in fe.get("analyses", [])])]
                best = max(((score(w, st.get(x["id"])[0]), x["id"]) for x in fa), default=(None, None))
                if best[0] is not None and best[0] >= 3:
                    ref = best[1]
                    stats["analysis: packet id"] += 1
                else:
                    ref = {"manual": manual_from(w)}
                    stats["analysis: manual" + (" (no packet analysis of the form)" if not fa else "")] += 1
                comp = None
                if w.get("compound"):
                    mem = []
                    for m in w["compound"].get("members") or []:
                        # any analysis in this verse's packet whose stem is the member, deriving ones first
                        cands = [x for fe in pk["forms"].values() for x in fe.get("analyses", [])
                                 if C.latin_key(x.get("stem") or "") == C.latin_key(m)]
                        want = (w.get("root_id") or "").split("#")[-1]
                        cands.sort(key=lambda x: (not (want and want in (x.get("root") or "") and False), x.get("root") is None,
                                                  x.get("derives") is not True))
                        if want:
                            hit = [x for x in cands if N.dp_id((st.get(x["id"])[0].get("dhatu"))) == want]
                            cands = hit + [x for x in cands if x not in hit]
                        mem.append({"form": m, "analysis": cands[0]["id"] if cands else None})
                    for t in w.get("terms") or []:          # member senses (the card's terms with `member`)
                        if isinstance(t, dict) and isinstance(t.get("member"), int) and t["member"] < len(mem) and t.get("lemma") in rows:
                            mem[t["member"]]["sense"] = f"{t['lemma']}.{t['sense']}"
                    comp = {"type": w["compound"].get("type"), "vigraha": w["compound"].get("vigraha"), "members": mem}
                t = w.get("term")
                sid = f"{t['lemma']}.{t['sense']}" if t and t.get("lemma") in rows else None
                if sid:
                    by_sense[sid].append((v["locus"], w))
                elif w.get("word_class") in ("content", "name"):
                    key = C.latin_key(w.get("stem") or w["iast"]) or "x"
                    sid = f"c12{key}.{key}"
                    reqs.append({"lemma": w.get("stem") or w["iast"], "sense": sid, "locus": f"{v['locus']}:{w['i']}",
                                 "proposal": {"lemma": w.get("stem") or w["iast"], "match": re.escape(w["iast"]),
                                              "senses": [sense_entry(sid, [(v["locus"], w)], None)]},
                                 "why": "converted from the reviewed chapter-12 card (no table row)"})
                    stats["sense: lexicon request"] += 1
                an_wc = N.word_class(st.get(ref)[0]) if isinstance(ref, str) else None
                extra = {"word_class": w["word_class"]} if w.get("word_class") != an_wc else {}
                if w.get("form_note"):
                    extra["form_note"] = w["form_note"]
                words.append({"i": w["i"], "analysis": ref, "compound": comp, "karaka": w.get("karaka"), "sense": sid, **extra,
                              "english": (smap.get(w["i"]) or [""])[0], "note": w.get("note"),
                              "commentator_lines": [{"who": l.get("who"), "locus": l.get("locus"), "text": l.get("text")}
                                                    for l in (w.get("meaning") or {}).get("lines") or [] if l.get("cat") == "commentator"]})
            verses.append({"locus": v["locus"], "padas": [w["iast"] for w in v["words"]], "words": words, "line": v["english"],
                           "sense": v["sense"], "forks": v.get("forks") or []})
            if reqs:
                verses[-1]["_requests"] = reqs
        reqs_all = [r for vv in verses for r in vv.pop("_requests", [])]
        outputs.append({"schema": C.SCHEMA_VERSE, "job": f"verse-12-{sh['range']}", "verses": verses, "lexicon_requests": reqs_all,
                        "_from": C.rel(sp)})
    entries = {}
    for sid, occ in by_sense.items():
        row, sname = sid.split(".", 1)
        s = (rows[row].get("senses") or {}).get(sname) or {}
        e = entries.setdefault(row, {"lemma": row, "match": rows[row].get("match") or row, "senses": []})
        e["senses"].append(sense_entry(sid, occ, s))
    lexicon = {"schema": C.SCHEMA_LEXICON, "job": "lexicon-ch12-roundtrip", "entries": list(entries.values())}
    return outputs, lexicon, dict(stats)


def sense_entry(sid: str, occ: list[tuple[str, dict]], pol_sense: dict | None) -> dict:
    w0 = occ[0][1]
    wd = w0.get("wording") or {}
    mg = w0.get("meaning") or {}
    lines, seen = [], set()
    for _, w in occ:
        for l in (w.get("meaning") or {}).get("lines") or []:
            k = (l.get("cat"), l.get("text"))
            if l.get("cat") not in ("commentator", "reception") and k not in seen:
                seen.add(k)
                lines.append({x: l[x] for x in ("cat", "text", "who", "locus") if l.get(x)})
    preserve = bool(pol_sense and pol_sense.get("policy") == "preserve")
    plain = wd.get("plain") if isinstance(wd.get("plain"), dict) else None
    rich = wd.get("rich") if isinstance(wd.get("rich"), dict) else None
    chosen_word = wd.get("chosen") if isinstance(wd.get("chosen"), str) else (wd.get("chosen") or {}).get("word")
    chosen = "preserve" if preserve else ("rich" if rich and chosen_word == rich.get("word") else "plain")
    return {"id": sid, "gloss": w0.get("gloss"), "image": mg.get("image"), "preserve": preserve,
            **({"iast": pol_sense.get("iast")} if preserve and pol_sense else {}),
            "forms": {"any": (pol_sense or {}).get("english") or [mg.get("rendering") or w0.get("gloss")]},
            "plain": plain, "rich": rich, "chosen": chosen, "why": mg.get("why") or wd.get("why"),
            "joycean": None, "forbidden": (pol_sense or {}).get("forbidden_english") or [],
            "candidates": [c for c in wd.get("candidates") or [] if isinstance(c, dict)],
            "meaning_lines": lines[:6], "occurrences": sorted({l for l, _ in occ}, key=C.locus_sort_key)}


def get(d: dict, path: str):
    for k in path.split("."):
        d = d.get(k) if isinstance(d, dict) else None
    return d


def run_builder(chapter_dir: Path) -> tuple[dict, list]:
    b = C.import_builder()
    ctx = b.Ctx(chapter=12, chapter_dir=chapter_dir, complete=False)
    result = b.run(ctx)
    return result, ctx.report


def roundtrip(out: Path) -> dict:
    from gitapipe.expand import Expander
    from gitapipe import validate as V
    shards = sorted(CH12.glob("producer-*.json"))
    outputs, lexicon, stats = convert(shards)
    out.mkdir(parents=True, exist_ok=True)
    C.write_json(out / "lexicon-ch12.json", lexicon)
    tmp_rt, tmp_base = out / "roundtrip-shards", out / "baseline-shards"
    for d in (tmp_rt, tmp_base):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        shutil.copy(CH12 / "packet.json", d / "packet.json")
    for sp in shards:
        shutil.copy(sp, tmp_base / sp.name)
    expansion_errors = []
    for vo, sp in zip(outputs, shards):
        vp = out / f"{vo['job']}.json"
        C.write_json(vp, {k: v for k, v in vo.items() if k != "_from"})
        ex = Expander(policy_path=C.POLICY, extra_entries=lexicon["entries"] + [r["proposal"] for r in vo["lexicon_requests"]],
                      include_outputs=False)
        shard, errs = ex.shard(vo, C.rel(vp), C.sha256_file(vp), secondaries=V.secondaries_names(vo))
        expansion_errors += errs
        C.write_json(tmp_rt / sp.name, shard)
    res_rt, rep_rt = run_builder(tmp_rt)
    res_b, rep_b = run_builder(tmp_base)
    orig = {v["locus"]: v for sp in shards for v in C.read_json(sp)["verses"]}
    rt = {v["locus"]: v for sp in sorted(tmp_rt.glob("producer-*.json")) for v in C.read_json(sp)["verses"]}
    lines_same = sum(1 for l in orig if rt.get(l, {}).get("english") == orig[l]["english"])
    eq = collections.Counter()
    diffs = collections.defaultdict(list)
    n = 0
    for l, v in orig.items():
        for w, x in zip(v["words"], rt[l]["words"]):
            n += 1
            for f in IDENTITY:
                a, c = get(w, f), get(x, f)
                if f == "term" and a is None and c is None:
                    a = c = None
                if a == c:
                    eq[f] += 1
                elif len(diffs[f]) < 6:
                    diffs[f].append(f"{l}[{w['i']}] {w['iast']}: {a!r} → {c!r}")
    classes = lambda rep: dict(collections.Counter(c for c, _, _ in rep.errors))  # noqa: E731
    new_classes = {k: v for k, v in classes(rep_rt).items() if k not in classes(rep_b)}
    report = {"conversion": stats, "verse_outputs": len(outputs), "verses": len(orig), "cards": n,
              "lines_identical": f"{lines_same}/{len(orig)}", "expansion_errors": expansion_errors,
              "builder_baseline_errors": classes(rep_b), "builder_roundtrip_errors": classes(rep_rt),
              "error_classes_not_in_baseline": new_classes,
              "roundtrip_error_messages": [f"{c} {m}" for c, m, _ in rep_rt.errors][:60],
              "identity_fields_equal": {f: f"{eq[f]}/{n}" for f in IDENTITY}, "identity_diff_examples": dict(diffs),
              "fallbacks": {"baseline": res_b["fallbacks"], "roundtrip": res_rt["fallbacks"]},
              "accepted": lines_same == len(orig) and not new_classes and not expansion_errors}
    C.write_json(out / "roundtrip_report.json", report)
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=C.PIPE / "roundtrip-ch12")
    a = ap.parse_args(argv)
    rep = roundtrip(a.out)
    print(json.dumps({k: rep[k] for k in rep if k not in ("roundtrip_error_messages", "identity_diff_examples")}, ensure_ascii=False, indent=1))
    return 0 if rep["accepted"] else 1


if __name__ == "__main__":
    sys.exit(main())

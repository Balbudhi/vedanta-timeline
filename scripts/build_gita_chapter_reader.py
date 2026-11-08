#!/usr/bin/env python3
"""Fail-closed builder: producer shards + independent reviews → gita/chN/ reader.

    python3 scripts/build_gita_chapter_reader.py 12 [--allow-unreviewed] [--check-only]

Inputs (internal/sanskrit_reviews/gita/chN/):
  packet.json                       the ChapterPacket (build_gita_chapter_packet.py)
  producer-AA-BB.json               producer shards (schema gita-producer-v1), covering 1..N once
  independent-review-AA-BB.json     one per shard, complete:true, producer_sha256 matching the shard
Outputs:
  gita/chN/verses.js                window.CH<N>_VERSES — public cards (standard §3 + term, sandhi, note, forks)
  gita/chN/apparatus.json           evidence loci, fallbacks, wording records, deviations per word/verse
  gita/chN/index.html               standalone page (forwards into the app)
  internal/sanskrit_reviews/gita/chN/owner-review-queue.json   what the owner is asked to read
  registration in assets/app.js GITA_READINGS and data/articles/manifest.json (idempotent)

The builder never repairs producer JSON. Any violation of the contract below
raises BuildError and nothing is written (--check-only reports all violations).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "data/glossary"
POLICY = json.loads((GLOSSARY / "term_policy.json").read_text(encoding="utf-8"))

REQUIRED_FORK_VERSES = {12: {"12.3", "12.4", "12.5", "12.6", "12.10", "12.11", "12.12", "12.13", "12.16", "12.19", "12.20"}}
GANA_RE = re.compile(r"\b(?:bhv|ad|juhoty|div|sv|tud|rudh|tan|kry|cur)ādi\b[^;]*?\b\d+\s*[PAUĀ]\b")
SLOT_RE = re.compile(r"\{([\d,\s]+):([^}]*)\}")
PRONOUN_STEMS = {"tad", "yad", "kim", "idam", "etad", "asmad", "yuṣmad", "adas", "sa", "saḥ", "te", "ye", "yaḥ", "mad", "tvad", "ka"}


class BuildError(ValueError):
    pass


ERRORS: list[str] = []
WARNINGS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def latin_key(s: str) -> str:
    s = unicodedata.normalize("NFD", s).lower()
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


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def slot_map(english: str) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    for m in SLOT_RE.finditer(english or ""):
        for i in m.group(1).split(","):
            i = i.strip()
            if i:
                out.setdefault(int(i), []).append(m.group(2))
    return out


def policy_rows_for(word: dict) -> list[tuple[str, dict]]:
    hay = [x for x in [word.get("stem"), word.get("iast"), *[p.get("form", "") for p in word.get("parts") or []],
                       *((word.get("compound") or {}).get("members") or [])] if x]
    rows = []
    for lemma, row in POLICY["terms"].items():
        if any(re.search(row["match"], h) for h in hay):
            rows.append((lemma, row))
    return rows


def check_policy(label: str, w: dict, phrases: str) -> None:
    rows = policy_rows_for(w)
    term = w.get("term")
    if not rows:
        if term:
            warn(f"{label}: term {term} declared but no policy row matches the word")
        return
    if not term or not isinstance(term, dict):
        err(f"{label}: matches policy row(s) {[l for l, _ in rows]} but carries no term{{lemma,sense}}")
        return
    lemma, sense = term.get("lemma"), term.get("sense")
    row = dict(rows).get(lemma)
    if row is None:
        err(f"{label}: term.lemma {lemma!r} is not among the matching rows {[l for l, _ in rows]}")
        return
    srow = row["senses"].get(sense)
    if srow is None:
        err(f"{label}: term.sense {sense!r} not in policy senses {list(row['senses'])} for {lemma}")
        return
    if not phrases:
        return  # unslotted word (particle) — nothing rendered to check
    low = phrases.lower()
    if srow["policy"] == "preserve":
        if not any(f in phrases for f in srow.get("iast_forms", [srow["iast"]])):
            err(f"{label}: preserved {lemma}/{sense} must print '{srow['iast']}' in its slot — got \"{phrases}\"")
        for bad in srow.get("forbidden_english", []):
            if re.search(rf"\b{re.escape(bad.lower())}\b", low):
                err(f"{label}: preserved {lemma}/{sense} rendered with forbidden '{bad}' — \"{phrases}\"")
    else:
        if not any(re.search(rf"\b{re.escape(e.lower())}\b", low) for e in srow["english"]):
            err(f"{label}: translated {lemma}/{sense} must use one of {srow['english']} — got \"{phrases}\"")
        for bad in srow.get("forbidden_english", []):
            if re.search(rf"(?<![‘'\"“])\b{re.escape(bad.lower())}\b", low):
                err(f"{label}: translated {lemma}/{sense} uses forbidden '{bad}' — \"{phrases}\"")
    gk = srow.get("glossaryKey")
    if gk and w.get("glossaryKey") not in (gk, None):
        warn(f"{label}: glossaryKey {w.get('glossaryKey')!r} differs from policy's {gk!r}")


def check_card(label: str, w: dict, idx: int, phrases: str) -> dict:
    """Return the public card; record errors."""
    for k in ("iast", "deva", "gloss", "parts", "affix", "morph"):
        if k not in w or w[k] in (None, "", []):
            err(f"{label}: card field {k!r} missing/empty")
    if w.get("i") != idx:
        err(f"{label}: i={w.get('i')} but position is {idx}")
    for p in w.get("parts") or []:
        if not p.get("form") or not p.get("gloss"):
            err(f"{label}: parts[] piece lacks form/gloss: {p}")
    root = w.get("root")
    if root:
        if not GANA_RE.search(root):
            err(f"{label}: root {root!r} lacks gaṇa and pada (e.g. '√yuj (rudhādi, 7U)')")
        if not w.get("rootGloss"):
            err(f"{label}: root given without rootGloss")
    gk = w.get("glossaryKey")
    if gk and not (GLOSSARY / f"{gk}.json").exists():
        err(f"{label}: glossaryKey {gk!r} has no file data/glossary/{gk}.json")
    comp = w.get("compound")
    if comp:
        for k in ("type", "vigraha", "members"):
            if not comp.get(k):
                err(f"{label}: compound lacks {k}")
    ev, fb = w.get("evidence") or [], w.get("fallback") or []
    if (root or comp or (w.get("affix") and "avyaya" not in w["affix"] and "nipāta" not in w["affix"])) and not ev and not fb:
        err(f"{label}: no evidence[] and no fallback[] for a grammatical claim")
    for e in ev:
        if not e.get("locus") or not e.get("claim"):
            err(f"{label}: evidence item lacks locus/claim: {e}")
    preserved = any(r["senses"].get((w.get("term") or {}).get("sense"), {}).get("policy") == "preserve"
                    for l, r in policy_rows_for(w) if l == (w.get("term") or {}).get("lemma"))
    is_name = bool(re.search(r"sambodhana|voc\.|vocative|proper name|epithet", f"{w.get('affix','')} {w.get('morph','')} {w.get('gloss','')} {w.get('note','')}"))
    is_copula = bool(re.match(r"^(is|are|am|was|were|be|being|you are|there is)\b", (w.get("gloss") or "").strip(), re.I))
    content = (bool(root or comp) or (w.get("translatable", True) and (w.get("stem") or "") not in PRONOUN_STEMS
                                       and not re.search(r"avyaya|nipāta|indeclinable|pronoun|sarvanāma", f"{w.get('affix','')} {w.get('morph','')}")))
    content = content and not preserved and not is_name and not is_copula and w.get("translatable", True) is not False
    wd = w.get("wording")
    if content and not wd:
        err(f"{label}: content word without wording{{}} record")
    if wd:
        for k in ("sense_description", "candidates", "chosen"):
            if not wd.get(k):
                err(f"{label}: wording lacks {k}")
        if wd.get("joycean"):
            for k in ("formation", "parts", "relation", "paraphrase", "why_no_attested_word"):
                if not wd["joycean"].get(k):
                    err(f"{label}: joycean record lacks {k}")
    check_policy(label, w, phrases)
    public = {k: w[k] for k in ("i", "deva", "iast", "gloss", "stem", "root", "rootGloss", "affix", "morph", "karaka",
                                 "glossaryKey", "translatable", "parts", "compound", "sandhi", "note", "term") if k in w and w[k] is not None}
    return public


DICTIONARY_SOURCES = re.compile(r"webster|gcide|wordnet|oewn|wiktionary|century|roget|moby|\bmw\b|ap90|apte|monier|skd|vcp|amara|cologne|kosha|define", re.I)


def public_wording(wd: dict | None) -> dict | None:
    """The public apparatus keeps dictionary evidence verbatim but never another
    translator's wording: a candidate offered by a secondary keeps only the word
    and the translator's name (plan §12: secondaries are quotation-only, private)."""
    if not wd:
        return wd
    out = dict(wd)
    cands = []
    for c in wd.get("candidates") or []:
        c = dict(c)
        src = f"{c.get('source','')} {c.get('locus','')}"
        if not DICTIONARY_SOURCES.search(src):
            for k in ("definition", "quote", "rejected_because", "context"):
                c.pop(k, None)
            c["source_note"] = "offered by a secondary translation (private; quotation not republished)"
        cands.append(c)
    out["candidates"] = cands
    return out


def check_verse(v: dict, pv: dict, ch: int) -> tuple[dict, dict, int]:
    loc = v.get("locus")
    label = f"{loc}"
    if v.get("iast") != pv["iast"]:
        err(f"{label}: iast differs from packet (must be verbatim)")
    if v.get("devanagari") != pv["devanagari"]:
        err(f"{label}: devanagari differs from packet (must be verbatim)")
    if v.get("speaker") != pv["speaker"]:
        err(f"{label}: speaker {v.get('speaker')!r} ≠ packet {pv['speaker']!r}")
    for k in ("sense", "english", "words", "grammar"):
        if not v.get(k):
            err(f"{label}: missing {k}")
    english = v.get("english") or ""
    if "[" in english or "]" in english:
        err(f"{label}: bracket insert in english line")
    words = v.get("words") or []
    smap = slot_map(english)
    n = len(words)
    for i in smap:
        if i >= n or i < 0:
            err(f"{label}: slot {{{i}:…}} has no word")
    unslotted = [w.get("iast") for w in words if w.get("i") not in smap]
    if unslotted:
        warn(f"{label}: unslotted words {unslotted}")
    # the pada-pāṭha must reproduce the saṃhitā (sandhi only)
    samhita = latin_key(pv["iast"])
    padas = latin_key(" ".join(w.get("iast", "") for w in words))
    d = edit_distance(samhita, padas)
    ratio = d / max(1, len(samhita))
    if ratio > 0.16:
        err(f"{label}: pada-pāṭha does not reproduce the BORI saṃhitā (edit ratio {ratio:.2f}); nothing may be dropped or invented")
    elif ratio > 0.10:
        warn(f"{label}: pada/saṃhitā edit ratio {ratio:.2f} — check the split")
    public_words, apparatus_words, fallbacks = [], [], 0
    for idx, w in enumerate(words):
        wl = f"{label}[{idx}] {w.get('iast')}"
        phrases = " ".join(smap.get(idx, []))
        public_words.append(check_card(wl, w, idx, phrases))
        fallbacks += len(w.get("fallback") or [])
        apparatus_words.append({"i": idx, "iast": w.get("iast"), "evidence": w.get("evidence") or [], "fallback": w.get("fallback") or [],
                                "wording": public_wording(w.get("wording")), "term": w.get("term")})
    forks = v.get("forks") or []
    for f in forks:
        if len(f.get("construals") or []) < 2:
            err(f"{label}: fork at {f.get('at')!r} has fewer than two construals")
        if not isinstance(f.get("followed"), int) or not (0 <= f["followed"] < len(f.get("construals") or [])):
            err(f"{label}: fork at {f.get('at')!r} 'followed' index invalid")
        if f.get("reason_class") not in (1, 2, 3, 4, 5):
            err(f"{label}: fork at {f.get('at')!r} reason_class must be 1–5 (plan §13.2)")
        if re.search(r"\b(because|since)\b[^.;]{0,60}\b(Śaṅkara|Rāmānuja|Madhva|Abhinavagupta|the school|the tradition|the commentators?)\b[^.;]{0,40}\b(reads?|says?|takes?|holds?|glosses)\b", f.get("reason", ""), re.I):
            err(f"{label}: fork at {f.get('at')!r} resolved by a school's authority — not an admissible reason")
        if f.get("reason_class") == 5 and f.get("open") is not True:
            err(f"{label}: fork at {f.get('at')!r} class 5 (English forced a choice) must be open:true")
    if loc in REQUIRED_FORK_VERSES.get(ch, set()) and not forks:
        err(f"{label}: fairness locus without a fork record (plan §13.3)")
    if "deviations" not in v:
        err(f"{label}: deviations[] missing (may be empty)")
    if len(v.get("secondaries_consulted") or []) < 5:
        err(f"{label}: fewer than five secondaries consulted")
    public = {"locus": loc, "speaker": v.get("speaker"), "meter": v.get("meter") or "anuṣṭubh", "devanagari": v["devanagari"],
              "iast": v["iast"], "sense": v.get("sense"), "english": english, "words": public_words, "grammar": v.get("grammar"), "forks": forks}
    apparatus = {"locus": loc, "words": apparatus_words, "secondaries_consulted": v.get("secondaries_consulted"),
                 "fallback_count": fallbacks, "_private_deviations": v.get("deviations")}
    return public, apparatus, fallbacks


def render_verses_js(ch: int, verses: list[dict]) -> str:
    head = f"""/* =============================================================
   Bhagavad-Gītā {ch} — the adhyāya entire, verses 1–{len(verses)}.
   window.CH{ch}_VERSES — one object per verse. GENERATED by
   scripts/build_gita_chapter_reader.py from the reviewed producer shards in
   internal/sanskrit_reviews/gita/ch{ch}/ — do not edit by hand.
   Schema + policy: docs/SANSKRIT_TRANSLATION_STANDARD.md; term policy:
   data/glossary/term_policy.json (sense-constant, see GITA_FULL_TRANSLATION_PLAN.md §4);
   forks[] per verse record grammatically admissible construals (plan §13).
   Mūla: data/sources/sanskrit/vedanta/bhagavadgita_mula_bori.txt (BORI critical
   edition); Devanāgarī is a labelled deterministic transliteration of that IAST,
   collated against two Devanāgarī witnesses (internal/.../devanagari-collation.json).
   Evidence loci, wording records and deviation defences: gita/ch{ch}/apparatus.json.
   Root text only — no commentary layer.
   ============================================================= */

window.CH{ch}_VERSES = """
    return head + json.dumps(verses, ensure_ascii=False, indent=2) + ";\n"


def render_index_html(ch: int, n: int, has_audio: bool) -> str:
    tmpl = (ROOT / "gita/ch5/index.html").read_text(encoding="utf-8")
    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"][ch - 1]
    out = tmpl.replace("gita-ch5", f"gita-ch{ch}").replace("CH5_VERSES", f"CH{ch}_VERSES")
    out = out.replace("Bhagavad-Gītā 5", f"Bhagavad-Gītā {ch}").replace("adhyāya V", f"adhyāya {roman}")
    out = out.replace("verses 1–29", f"verses 1–{n}")
    if has_audio:
        out = out.replace('<script src="verses.js"></script>', f'<script src="verses.js"></script>\n  <script src="audio.js"></script>')
        out = out.replace("audio: null,", f"audio: window.CH{ch}_AUDIO,")
    return out


def register(ch: int, n: int, has_audio: bool) -> None:
    app = ROOT / "assets/app.js"
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
        s = re.sub(rf'  "gita-ch{ch}": \{{.*?\n  \}},\n', block, s, count=1, flags=re.S)
    else:
        anchor = '  "yogavasistha-dama": {'
        if anchor not in s:
            raise BuildError("app.js GITA_READINGS anchor not found")
        s = s.replace(anchor, block + anchor, 1)
    app.write_text(s, encoding="utf-8")
    man_p = ROOT / "data/articles/manifest.json"
    man = json.loads(man_p.read_text(encoding="utf-8"))
    arts = man["articles"] if isinstance(man, dict) and "articles" in man else man
    entry = {"slug": f"gita-ch{ch}", "title": f"Bhagavad-Gītā {ch}",
             "subtitle": f"The whole adhyāya, all {n} verses: the BORI root text word by word, with full Pāṇinian grammar cited to its sources, a literal rendering under one sense-constant term policy, and the places where more than one construal is admissible shown as such. Every Sanskrit word tappable{'; verse-synced recitation' if has_audio else ''}. Root text only — no commentary layer.",
             "kind": "reading", "interactive": f"gita-ch{ch}", "date": "2026-11-08"}
    idx = next((i for i, a in enumerate(arts) if a.get("slug") == f"gita-ch{ch}"), None)
    if idx is None:
        pos = next((i for i, a in enumerate(arts) if a.get("slug") == "gita-ch5"), len(arts) - 1) + 1
        arts.insert(pos, entry)
    else:
        arts[idx] = entry
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", type=int)
    ap.add_argument("--allow-unreviewed", action="store_true", help="build without complete independent reviews (never for publication)")
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    ch = a.chapter
    d = ROOT / f"internal/sanskrit_reviews/gita/ch{ch}"
    packet = json.loads((d / "packet.json").read_text(encoding="utf-8"))
    by_locus = {v["locus"]: v for v in packet["verses"]}
    n = packet["verse_count"]
    shards = sorted(d.glob("producer-*.json"))
    if not shards:
        raise BuildError("no producer shards")
    covered: dict[str, str] = {}
    verses_in: list[tuple[dict, str]] = []
    for sp in shards:
        try:
            sh = json.loads(sp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"{sp.name}: invalid JSON ({e})")
            continue
        if sh.get("schema_version") != "gita-producer-v1":
            err(f"{sp.name}: schema_version must be gita-producer-v1")
        if sh.get("policy_version") != POLICY["version"]:
            err(f"{sp.name}: policy_version {sh.get('policy_version')!r} ≠ {POLICY['version']!r}")
        rev = d / sp.name.replace("producer-", "independent-review-")
        if rev.exists():
            r = json.loads(rev.read_text(encoding="utf-8"))
            if r.get("producer_sha256") != sha256(sp):
                err(f"{rev.name}: producer_sha256 does not match the current {sp.name} (review is stale)")
            if r.get("complete") is not True:
                err(f"{rev.name}: review not complete")
            open_sev1 = [f for f in r.get("findings", []) if f.get("severity") == 1 and f.get("status", "open") != "resolved"]
            if open_sev1:
                err(f"{rev.name}: {len(open_sev1)} open severity-1 findings")
        elif not a.allow_unreviewed:
            err(f"{sp.name}: no independent review file {rev.name}")
        for v in sh.get("verses", []):
            loc = v.get("locus")
            if loc in covered:
                err(f"{loc} produced twice ({covered[loc]}, {sp.name})")
            covered[loc] = sp.name
            if loc not in by_locus:
                err(f"{sp.name}: unknown locus {loc}")
                continue
            verses_in.append((v, sp.name))
    missing = [f"{ch}.{i}" for i in range(1, n + 1) if f"{ch}.{i}" not in covered]
    if missing:
        err(f"verses not produced: {missing}")
    verses_in.sort(key=lambda t: int(t[0]["locus"].split(".")[1]))
    public, apparatus, total_fb = [], [], 0
    for v, _ in verses_in:
        pub, app_, fb = check_verse(v, by_locus[v["locus"]], ch)
        public.append(pub); apparatus.append(app_); total_fb += fb
    print(json.dumps({"chapter": ch, "verses": len(public), "cards": sum(len(v["words"]) for v in public), "fallbacks": total_fb,
                      "forks": sum(len(v["forks"]) for v in public), "errors": len(ERRORS), "warnings": len(WARNINGS)}, ensure_ascii=False))
    for w in WARNINGS:
        print("WARN", w)
    for e in ERRORS:
        print("ERROR", e)
    if ERRORS:
        print(f"REFUSED: {len(ERRORS)} contract violations; nothing written.")
        return 1
    if a.check_only:
        return 0
    out = ROOT / f"gita/ch{ch}"
    out.mkdir(parents=True, exist_ok=True)
    audio_js = out / "audio.js"
    has_audio = audio_js.exists()
    if has_audio:
        s = audio_js.read_text(encoding="utf-8")
        if f"window.CH{ch}_AUDIO" not in s:
            s = re.sub(r"window\.\w+_AUDIO\s*=", f"window.CH{ch}_AUDIO =", s, count=1)
            audio_js.write_text(s, encoding="utf-8")
    (out / "verses.js").write_text(render_verses_js(ch, public), encoding="utf-8")
    # Deviation defences quote the secondaries' full renderings: private store only (plan §12).
    deviations = {a_["locus"]: a_.pop("_private_deviations") for a_ in apparatus}
    (d / "deviations.json").write_text(json.dumps({"chapter": ch, "verses": deviations}, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "apparatus.json").write_text(json.dumps({"chapter": ch, "policy_version": POLICY["version"],
        "note": "Evidence loci, fallbacks and wording records per word. Deviation defences against other translations are kept privately (they quote copyrighted renderings).",
        "verses": apparatus}, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "index.html").write_text(render_index_html(ch, n, has_audio), encoding="utf-8")
    register(ch, n, has_audio)
    queue = {"chapter": ch, "instructions": "Read each verse's english and sense; tap any word on the site for its card. Decide the rows marked review:pilot in data/glossary/term_policy.json. Listen to the audio disagreements listed in gita/ch%d/audio.js if present." % ch,
             "pilot_policy_rows": {l: {s: r.get("note") for s, r in row["senses"].items() if r.get("review") == "pilot"} for l, row in POLICY["terms"].items() if any(r.get("review") == "pilot" for r in row["senses"].values())},
             "verses": [{"locus": v["locus"], "english": v["english"], "sense": v["sense"], "forks_open": [f["at"] for f in v["forks"] if f.get("open")],
                         "fallbacks": ap_["fallback_count"]} for v, ap_ in zip(public, apparatus)]}
    (d / "owner-review-queue.json").write_text(json.dumps(queue, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"written gita/ch{ch}/verses.js, apparatus.json, index.html; registered gita-ch{ch}; audio={'yes' if has_audio else 'no'}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as e:
        print("ERROR", e)
        sys.exit(1)

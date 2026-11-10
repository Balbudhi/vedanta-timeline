#!/usr/bin/env python3
"""Publication bridge: a pipeline run → the chapter builder's input (plan §5 gap 8, roadmap step 5).

    python3 scripts/gita/translate/publish.py --run RUN --chapter N --out DIR [--allow-unfinished] [--check]

Reads `internal/gita_pipeline/run/RUN/translate/*.json` (one record per sentence unit, written by
`pipeline._translate_unit`) and the verse packets `internal/gita_pipeline/packets/verses/N.V.json`
(the BORI text, its Devanāgarī, speaker and metre). Writes what `scripts/build_gita_chapter_reader.py`
reads from its chapter directory:

    DIR/packet.json                  {chapter, verse_count, verses[{locus, speaker, meter, iast, devanagari}]}
    DIR/producer-01-NN.json          one shard, schema gita-producer-v2, every verse of the chapter
    DIR/independent-review-01-NN.json  the pipeline's review findings, with the shard's sha256

Nothing is invented, and nothing is taken from a published translation or a Sanskrit–English
dictionary: every field is copied from the run record or the verse packet, or computed from them
(Devanāgarī of a pada by transliteration; slot positions by locating the word's English in the line;
grammar from the analysis store). A field the run does not hold stays absent.

Mapping (run record → builder card, standard §3.1–§3.2):
  verse    iast, devanagari, speaker, meter        ← verse packet
           english (slotted `{i:…}`)               ← output.slotted[locus] (new runs), checked against the
                                                     line; else output.words[].english located in the line
           forks                                   ← output.alternative: one open fork (reason class 5,
                                                     standard §6.5: a second full line exists only for a
                                                     construal fork English cannot keep open); construal 0
                                                     is the line, construal 1 the second line, display = the
                                                     second line, words = alternative.words (or the card's
                                                     grammatical forks at this verse)
           deviations = []                         (the pipeline compares with no secondary translation)
  card     iast ← card.form; deva ← transliterated form; gloss ← output english; stem ← lemma;
           root ← card.root; morph ← card.grammar; karaka ← relation → depends_on; word_class ← class;
           compound {type, vigraha, members} ← card.compound; parts ← output.parts (members with English);
           from the grammar engine's analysis (card.analysis_id, else the accepted parse's word at the same
             place, resolved by sanskrit_card.resolve in analyses.sqlite) — grammar_fields():
             root "√r (gaṇa, NP, 'artha')", root_id (Dhātupāṭha record), rootGloss (its artha, Sanskrit),
             affix, parts (morpheme pieces) when the translation gave none, morph when the card has none,
             evidence: the Dhātupāṭha record and each samāsa/vibhakti/pratyaya sūtra (Aṣṭādhyāyī 2–5) of a
             derivation that reproduces the form, quoted from its line once the line is checked to be that
             sūtra. A manual analysis has no engine record: its fields stay absent;
           term/terms ← the card's standing term-policy rows (never seed rows);
           wording {sense_description, candidates, chosen, why} (content words) ← meaning literal,
             card candidates (locus = the first of define()'s `loci` in new runs, source = the dictionary
             it names), output english, output why;
           meaning {image, lines, rendering, why} ← meaning.here and readings (commentator lines),
             meaning.literal (+ grounds as `who`) as the synthesis line, output english, output why.
  Private audit data the builder ignores: card `pipeline` {kind, found_by, carried, lost, challenge},
  verse `pipeline` {unit, record_sha256, forks, taste}, shard `pipeline` {run, units}.

Fail closed. Nothing is written (exit 1) when
  - a verse of the chapter is in no unit record, or in two;
  - a unit has no output, code_errors, S1/S2 review findings or meaning_errors left;
  - a field the builder requires is absent or cannot be placed (`builder_gaps`), including an
    English rendering whose place in the line is ambiguous between two different words.
With --allow-unfinished the files are written anyway (exit 2): every reason is listed under
`unfinished` on the shard and on each verse, and the shard's schema_version is
`gita-producer-v2+unfinished`, which the builder refuses (B12) — it has no way to publish a verse
marked unfinished, so the marker keeps such a shard from ever being built.
--check runs the builder's own checks on DIR read-only (build_gita_chapter_reader.run with
chapter_dir=DIR; nothing is written) and exits 1 if it reports errors.

Beyond the builder, a claim needs its own evidence: a root its Dhātupāṭha record, a compound a
samāsa sūtra (2.1–2.2); otherwise it is listed as unfinished.

The review file holds what the run has: each unit's review findings (S1/S2 left, S3 taste; severity
1–3), the review model, and the shard's sha256. `complete` and `date` have no source in the run and
are not written (listed in `not_in_the_run`), so the builder reports the review as not complete. The
term-policy hash is not recorded by the run either; B1 stands.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUNS = ROOT / "internal/gita_pipeline/run"
PACKETS = ROOT / "internal/gita_pipeline/packets/verses"
SCHEMA = "gita-producer-v2"                      # build_gita_chapter_reader.PRODUCER_SCHEMA
SCHEMA_UNFINISHED = SCHEMA + "+unfinished"
WORD_CLASSES = {"content", "particle", "pronoun", "name", "copula"}   # builder WORD_CLASSES
MIN_SECONDARIES = 5                               # builder check_verse: "fewer than five secondaries consulted"
BLOCKING_SEVERITIES = ("S1", "S2")                # pipeline: S3 is taste, stored, never forced
SEARCH_LIMIT = 200_000                            # slot-placement search nodes before giving up as ambiguous


class PublishError(ValueError):
    pass


# ---------------------------------------------------------------- inputs
def load_records(run_dir: Path) -> dict[str, dict]:
    """Unit records by file name, skipping the `_summary` and `_consistency` files."""
    d = run_dir / "translate"
    if not d.is_dir():
        raise PublishError(f"no translate records: {d}")
    return {p.name: json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.json")) if not p.name.startswith("_")}


def chapter_packets(chapter: int, packets: Path) -> list[dict]:
    """The chapter's verse packets in verse order: the authority for which verses exist."""
    out = []
    for p in packets.glob(f"{chapter}.*.json"):
        m = re.fullmatch(rf"{chapter}\.(\d+)\.json", p.name)
        if m:
            out.append((int(m.group(1)), json.loads(p.read_text(encoding="utf-8"))))
    if not out:
        raise PublishError(f"no verse packets for chapter {chapter} in {packets}")
    return [v for _, v in sorted(out, key=lambda x: x[0])]


def unit_problems(rec: dict) -> list[str]:
    """What the pipeline itself left unfinished in one unit."""
    out = []
    if not rec.get("output"):
        out.append("no translation output")
    out += [f"code error left: {e}" for e in rec.get("code_errors") or []]
    for f in rec.get("review") or []:
        if f.get("severity") in BLOCKING_SEVERITIES:
            out.append(f"{f.get('severity')} review finding left ({f.get('kind')}, {f.get('locus')}): {f.get('says')}")
    out += [f"meaning error left: {e}" for e in rec.get("meaning_errors") or []]
    return out


# ---------------------------------------------------------------- grammar from the analysis store
PRAKRIYA = ROOT.parent / "prakriya"
DHATUPATHA = PRAKRIYA / "sources/raw/panini/lexica/dhatupatha.json"
PADA = {"parasmaipada": "P", "ātmanepada": "A", "ubhayapada": "U"}
CITED_CHAPTERS = re.compile(r"^[2-5]\.\d+\.\d+$")   # samāsa and vibhakti (2), pratyaya (3–5)
SAMASA_SUTRA = re.compile(r"^2\.[12]\.")


def parse_words(run_dir: Path) -> dict[tuple[str, int], dict]:
    """(locus, i) → the accepted parse's word (construe/<locus>/output.json with record.json accepted),
    which holds the analysis_id the translate card does not carry."""
    out = {}
    for p in sorted((run_dir / "construe").glob("*/output.json")):
        rec = p.parent / "record.json"
        if not (rec.exists() and json.loads(rec.read_text(encoding="utf-8")).get("accepted")):
            continue
        o = json.loads(p.read_text(encoding="utf-8"))
        for w in o.get("words") or []:
            out[(o["locus"], w["i"])] = w
    return out


_STORE: list = []


def store():
    """sanskrit_card (its resolve over analyses.sqlite), or None when it cannot be loaded."""
    if not _STORE:
        try:
            sys.path.insert(0, str(HERE))
            import sanskrit_card
            _STORE.append(sanskrit_card)
        except Exception as e:  # noqa: BLE001 - recorded as a reason, never silent
            _STORE.append(None)
            _STORE.append(f"{type(e).__name__}: {e}")
    return _STORE[0]


def analysis_for(locus: str, cw: dict, pw: dict | None) -> tuple[dict | None, dict | None, str | None, str | None]:
    """(analysis, derivation, gram, why none). The card's own analysis_id when it has one, else the
    accepted parse's word at the same (locus, i) with the same form."""
    if cw.get("analysis_id"):
        word = {"form": cw.get("form"), "analysis_id": cw["analysis_id"], "manual": cw.get("manual"), "stem": cw.get("lemma")}
    elif pw is None:
        return None, None, None, "no accepted parse of this word in the run"
    elif pw.get("form") != cw.get("form"):
        return None, None, None, f"the parse's form {pw.get('form')!r} differs from the card's"
    else:
        word = pw
    S = store()
    if S is None:
        return None, None, None, f"analysis store unavailable ({_STORE[1]})"
    a, d, gram = S.resolve(locus, word)
    if a is None:
        return None, None, gram, "manual analysis: no grammar-engine record"
    return a, d, gram, None


def _iast(deva: str) -> str:
    from indic_transliteration import sanscript
    return sanscript.transliterate(deva or "", sanscript.DEVANAGARI, sanscript.IAST)


def _letters(s: str) -> str:
    s = _iast(s) if re.search(r"[ऀ-ॿ]", s or "") else (s or "")
    return re.sub(r"[^a-z]", "", _plain(s))


_DP: dict = {}


def dp_record(locus: str) -> dict | None:
    m = re.search(r"dhatupatha\.json#(\d+)$", locus or "")
    if not m:
        return None
    if not _DP and DHATUPATHA.is_file():
        data = json.loads(DHATUPATHA.read_text(encoding="utf-8"))
        _DP.update({str(e.get("i")): e for e in data.get("data", data)})
    return _DP.get(m.group(1))


_LINES: dict = {}


def source_line(locus: str) -> str | None:
    m = re.fullmatch(r"(.+):(\d+)", locus or "")
    if not m:
        return None
    p = PRAKRIYA / m.group(1)
    if p not in _LINES:
        _LINES[p] = p.read_text(encoding="utf-8").split("\n") if p.is_file() else []
    n = int(m.group(2))
    return _LINES[p][n - 1].strip() if 1 <= n <= len(_LINES[p]) else None


def grammar_fields(a: dict, d: dict | None, gram: str | None, card_root: str | None) -> tuple[dict, list[str]]:
    """Builder card fields from one grammar-engine analysis, by code: root (with gaṇa and pada),
    root_id, rootGloss (the Dhātupāṭha artha, in Sanskrit), affix, parts (morpheme pieces, glossed by
    the Dhātupāṭha artha, the affix's meaning sūtra in affix_meanings.json, or its grammatical
    category) and evidence (the Dhātupāṭha record; each samāsa, vibhakti and pratyaya step of a
    derivation that reproduces the form, quoted from its Aṣṭādhyāyī line after checking the line is
    that sūtra). Returns (fields, notes on what could not be filled)."""
    S = store()
    out: dict = {}
    notes: list[str] = []
    ev: list[dict] = []
    pieces: list[dict] = []
    meaning = {}
    for x in (S.affix_meanings(a, gram) if S else []):
        arthas = [s["artha"] for s in x["sutras"] if s.get("artha")]
        if arthas:
            meaning[x["affix"]] = arthas[0]
    dh = a.get("dhatu") or {}
    if dh:
        root = dh.get("root")
        rec = dp_record(dh.get("dp_record"))
        pada = PADA.get(dh.get("pada"))
        if card_root and card_root.split(" ")[0].lstrip("√") != root:
            notes.append(f"the engine's root √{root} differs from the card's {card_root}")
        elif rec is None or pada is None or str(rec.get("gana")) != str(dh.get("gana")) or rec.get("pada") != pada:
            notes.append(f"√{root}: the Dhātupāṭha record {dh.get('dp_record')} is missing or disagrees with the analysis")
        else:
            artha = _iast(rec["artha"])
            out.update({"root": f"√{root} ({dh['gana_name']}, {dh['gana']}{pada}, '{artha}')",
                        "root_id": dh["dp_record"], "rootGloss": artha})
            ev.append({"claim": f"√{root}: Dhātupāṭha {rec.get('baseindex')} {_iast(rec['aupadeshik'])}, "
                                f"{dh['gana_name']} {rec['gana']}{rec['pada']}, '{artha}'",
                       "locus": dh["dp_record"], "quote": f"{rec['aupadeshik']} {rec['pada']} {rec['artha']}", "kind": "dhatupatha"})
        pieces += [{"form": f"{u}-", "gloss": "upasarga"} for u in dh.get("upasargas") or []]
        pieces.append({"form": f"√{root}", "gloss": out.get("rootGloss") or "dhātu"})
    elif (a.get("taddhita") or {}).get("base"):
        pieces.append({"form": a["taddhita"]["base"], "gloss": "prātipadika"})
    elif a.get("stem"):
        pieces.append({"form": a["stem"], "gloss": "avyaya" if a.get("avyaya") else "prātipadika"})
    names = ["avyaya"] if a.get("avyaya") else []
    for s in dh.get("sanadi") or []:
        names.append(f"{s} (sanādi)")
        pieces.append({"form": s, "gloss": meaning.get(s) or "sanādi"})
    for kind, label in (("krt", "kṛt"), ("taddhita", "taddhita")):
        if a.get(kind):
            nm = a[kind]["name"]
            names.append(f"{nm} ({label})")
            pieces.append({"form": nm, "gloss": meaning.get(nm) or label})
    if a.get("lakara"):
        names.append(f"{a['lakara']} ({a['prayoga']})" if a.get("prayoga") else a["lakara"])
    e = a.get("ending") or {}
    if e.get("name"):
        names.append(f"{e['name']} ({e.get('type')} {e.get('sutra')}" + (f", elided by {e['luk']}" if e.get("luk") else "") + ")")
        if not e.get("luk"):
            cat = [a.get(k) for k in ("lakara", "prayoga", "purusha", "vacana", "pada")] if e.get("type") == "tiṅ" \
                else [a.get(k) for k in ("vibhakti", "vacana", "linga")]
            pieces.append({"form": f"-{e['name']}", "gloss": " ".join(x for x in cat if x) or e.get("type")})
    if names:
        out["affix"] = "; ".join(names)
    if len(pieces) > 1 or (pieces and dh):
        out["parts"] = pieces
    if gram:
        out["morph"] = gram
    if d and d.get("matches"):
        seen = set()
        for s in d.get("steps") or []:
            su, loc = s.get("sutra") or "", s.get("ashtadhyayi")
            if not CITED_CHAPTERS.match(su) or not loc or su in seen:
                continue
            seen.add(su)
            line, want = source_line(loc), (S.sutra_text(su) if S else None)
            if not line or not want or _letters(line) != _letters(want):
                notes.append(f"sūtra {su}: the line at {loc} is not that sūtra's text; not cited")
                continue
            ev.append({"claim": f"{su}: {s.get('result')}", "locus": loc, "quote": line, "sutra": su, "kind": "sutra"})
    elif d is not None:
        notes.append("the engine's derivation does not reproduce the form; no sūtra cited")
    if ev:
        out["evidence"] = ev
    return out, notes


# ---------------------------------------------------------------- slot placement
_QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'})
_PIECES = re.compile(r"\s*(?:…|\.\.\.)\s*")


def _fold(s: str) -> str:
    """Case and quote-mark folding, character by character, so offsets stay valid in the original
    (a character whose lower case is longer, such as İ, is kept as it is)."""
    return "".join(c.lower() if len(c.lower()) == 1 else c for c in s.translate(_QUOTES))


def _occurrences(piece: str, line: str) -> list[tuple[int, int]]:
    pat = re.compile(r"(?<!\w)" + re.escape(_fold(piece)) + r"(?!\w)")
    return [(m.start(), m.end()) for m in pat.finditer(_fold(line))]


PLACEMENT_CAP = 64


def placements(english: str, line: str, cap: int = PLACEMENT_CAP) -> list[tuple[tuple[int, int], ...]]:
    """Every way to find `english` in `line` as whole words: one span, or for a discontinuous
    rendering written with '…' one span per piece, in order and not overlapping (at most `cap`)."""
    pieces = [p for p in _PIECES.split(english.strip()) if p]
    if not pieces:
        return []
    occ = [_occurrences(p, line) for p in pieces]
    out = []
    for combo in itertools.product(*occ):
        if all(combo[k][1] <= combo[k + 1][0] for k in range(len(combo) - 1)):
            out.append(tuple(combo))
            if len(out) >= cap:
                break
    return out


@dataclass
class Item:
    i: int
    english: str
    identity: tuple            # words with equal identity and equal English are interchangeable
    options: list = field(default_factory=list)


@dataclass
class SlotResult:
    english: str               # the line with `{i:…}` / `{i,j:…}` slots
    placed: dict               # i → spans
    unplaced: list             # i whose English is not in the line
    ambiguous: list            # i whose place differs between equally good assignments
    by_order: list             # i placed among interchangeable twins by Sanskrit order
    problems: list = field(default_factory=list)   # a slotted line that does not match the record


def _compatible(a: Item, pa, b: Item, pb) -> bool:
    if pa == pb:                               # one slot carrying several words: same English only
        return _fold(a.english.strip()) == _fold(b.english.strip())
    return all(x[1] <= y[0] or y[1] <= x[0] for x in pa for y in pb)


def place_slots(line: str, words: list[tuple[int, str, tuple]]) -> SlotResult:
    """Assign each word (i, english, identity) a place in the line. Constraints: two words take
    the same place only when their English is identical (a joint slot `{i,j:…}`); otherwise their
    spans do not overlap (slots cannot nest). Objective: most words placed, then most distinct
    slots. Interchangeable words (same English, same identity) take their places in Sanskrit
    order; any other difference between optimal assignments is reported as ambiguous and those
    words are left unplaced."""
    items = [Item(i, e, ident, placements(e, line)) for i, e, ident in words if (e or "").strip()]
    unplaced = sorted(it.i for it in items if not it.options)
    crowded = sorted(it.i for it in items if len(it.options) >= PLACEMENT_CAP)   # alternatives not all seen
    live = sorted((it for it in items if it.options and it.i not in crowded), key=lambda it: (len(it.options), it.i))
    twins: dict[int, Item] = {}                # i → the previous interchangeable word (lower i)
    groups = defaultdict(list)
    for it in sorted(live, key=lambda it: it.i):
        groups[(_fold(it.english.strip()), it.identity)].append(it)
    for g in groups.values():
        for a, b in zip(g, g[1:]):
            twins[b.i] = a
    by_i = {it.i: it for it in live}
    best: list = [(-1, -1), []]
    nodes = 0
    chosen: dict[int, tuple] = {}

    def score(ch):
        ps = [p for p in ch.values() if p is not None]
        return (len(ps), len(set(ps)))

    def dfs(k: int, placed: int):
        nonlocal nodes
        nodes += 1
        if nodes > SEARCH_LIMIT:
            raise OverflowError
        if placed + (len(live) - k) < best[0][0]:
            return
        if k == len(live):
            s = score(chosen)
            if s > best[0]:
                best[0], best[1] = s, [dict(chosen)]
            elif s == best[0]:
                best[1].append(dict(chosen))
            return
        it = live[k]
        for p in it.options + [None]:
            if p is not None:
                # symmetry: twins take their places in Sanskrit order. Twins have the same English,
                # hence the same options, so the lower index is always visited first.
                tw = twins.get(it.i)
                if tw is not None and chosen.get(tw.i) is not None and chosen[tw.i][0] > p[0]:
                    continue
                if any(q is not None and not _compatible(it, p, by_i[j], q) for j, q in chosen.items()):
                    continue
            chosen[it.i] = p
            dfs(k + 1, placed + (p is not None))
            del chosen[it.i]

    try:
        dfs(0, 0)
        sols = best[1]
    except OverflowError:
        sols = []
    if not sols:
        return SlotResult(line, {}, unplaced, sorted(crowded + [it.i for it in live]), [])
    ambiguous = sorted(crowded + [it.i for it in live if len({s.get(it.i) for s in sols}) > 1])
    sol = {i: p for i, p in sols[0].items() if p is not None and i not in ambiguous}
    unplaced = sorted(unplaced + [i for i, p in sols[0].items() if p is None and i not in ambiguous])
    by_order = sorted(i for i in sol if i in twins or any(t.i == i for t in twins.values()))
    return SlotResult(render_slots(line, sol), sol, unplaced, ambiguous, by_order)


SLOT = re.compile(r"\{([\d,\s]+):([^{}]*)\}")          # build_gita_chapter_reader.SLOT_RE


def strip_slots(slotted: str | None) -> str | None:
    return SLOT.sub(lambda m: m.group(2), slotted) if slotted else None


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def from_slotted(slotted: str, line: str, cards: list[dict], ow: dict[int, dict]) -> SlotResult:
    """Placement written by the translation itself (`output.slotted`, new runs): used as the builder's
    `english` when, without its slots, it is the line and every slot names a card of the verse."""
    known = {w["i"] for w in cards}
    held: dict[int, list] = defaultdict(list)
    problems = []
    for m in SLOT.finditer(slotted):
        for x in m.group(1).split(","):
            if x.strip():
                held[int(x)].append(m.span())
    if _ws(strip_slots(slotted)) != _ws(line):
        problems.append("the slotted line without its slots is not the line")
    bad = sorted(set(held) - known)
    if bad:
        problems.append(f"the slotted line names words {bad} the card does not have")
    if problems:
        return SlotResult(line, {}, sorted(known), [], [], problems)
    unplaced = sorted(i for i in known if i not in held and (ow.get(i, {}).get("english") or "").strip())
    return SlotResult(slotted, dict(held), unplaced, [], [], [])


def render_slots(line: str, placed: dict[int, tuple]) -> str:
    """Insert `{i:text}` (or `{i,j:text}` for a joint slot) at the placed spans."""
    spans: dict[tuple[int, int], list[int]] = defaultdict(list)
    for i, p in placed.items():
        for sp in p:
            spans[sp].append(i)
    out, last = [], 0
    for (a, b), idx in sorted(spans.items()):
        out.append(line[last:a])
        out.append("{" + ",".join(str(i) for i in sorted(idx)) + ":" + line[a:b] + "}")
        last = b
    out.append(line[last:])
    return "".join(out)


# ---------------------------------------------------------------- cards
def devanagari(iast: str) -> str:
    try:
        from indic_transliteration import sanscript
    except ImportError as e:  # the builder needs the same package (quote_key)
        raise PublishError("indic_transliteration is required to write `deva`") from e
    return sanscript.transliterate(iast, sanscript.IAST, sanscript.DEVANAGARI)


def _plain(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if not unicodedata.combining(c)).lower()


def _admits(row: dict, text: str) -> bool:
    """The builder's B8 rule on the row as the card recorded it: a translated sense prints one of its
    English forms as whole words; a preserved sense keeps the Sanskrit (inflected the English way)."""
    if row.get("policy") == "preserve":
        k = _plain(row.get("keep") or "")
        k = k[:-1] if len(k) > 3 else k
        return bool(k) and any(t.startswith(k) for t in re.findall(r"[\w'-]+", _plain(text)))
    return any(re.search(r"(?<![A-Za-z])" + re.escape(e.lower()) + r"(?![A-Za-z])", _fold(text)) for e in row.get("english") or [])


def term_fields(cw: dict, ow: dict) -> tuple[dict | None, list[dict]]:
    """`term` and `terms` from the card's standing term-policy rows (never seed rows: plan defaults the
    builder cannot resolve). The run does not record which sense of a several-sense row the rendering
    follows; a sense is named only when it is the one sense of its row that admits the rendering (for a
    compound member, the member's English in `parts`), or, among preserved senses that all admit it,
    the one whose forms name the card's lemma. `term`, the one object the builder reads: the whole-word
    sense, else the sense of the last named member (compound order; the chapter-12 shards' convention
    of one sense in `term` and every sense in `terms`)."""
    rows = [r for r in cw.get("standing") or [] if not r.get("seed") and "." in (r.get("term") or "")]
    members = [m.get("stem") for m in (cw.get("compound") or {}).get("members") or []]
    part_en = {p.get("stem"): p.get("english") for p in ow.get("parts") or [] if isinstance(p, dict)}
    groups: dict[tuple, dict[str, dict]] = defaultdict(dict)
    for r in rows:
        lemma, sense = r["term"].split(".", 1)
        groups[(r.get("member"), lemma)].setdefault(sense, r)
    terms = []
    for (member, lemma), senses in groups.items():
        text = part_en.get(member) if member else ow.get("english")
        hits = [sn for sn, r in senses.items() if text and _admits(r, text)]
        if len(hits) > 1:
            own = [sn for sn in hits if senses[sn].get("policy") == "preserve"
                   and _plain(senses[sn].get("keep") or "") == _plain(member or cw.get("lemma") or "")]
            hits = own if len(own) == 1 else hits
        if len(hits) == 1:
            t = {"lemma": lemma, "sense": hits[0]}
            if member:
                t["member"] = members.index(member) if member in members else None
            terms.append(t)
    whole = [t for t in terms if "member" not in t]
    named = sorted((t for t in terms if t.get("member") is not None), key=lambda t: t["member"])
    pick = whole if whole else named[-1:]
    term = {"lemma": pick[0]["lemma"], "sense": pick[0]["sense"]} if len(pick) == 1 else None
    return term, terms


def meaning_block(mw: dict | None, ow: dict, locus: str) -> dict | None:
    """meaning{} from the step-1 record: commentator lines (here, readings), then the literal
    meaning as the synthesis line with its grounds as `who` (standard §3.1 category order)."""
    if not mw:
        return None
    literal = (mw.get("literal") or mw.get("sense") or "").strip()
    lines = []
    if (mw.get("here") or "").strip():
        lines.append({"cat": "commentator", "text": mw["here"].strip(), "who": f"commentators on {locus}"})
    for r in mw.get("readings") or []:
        if isinstance(r, dict) and (r.get("sense") or "").strip():
            lines.append({"cat": "commentator", "text": r["sense"].strip(), "who": (r.get("who") or "").strip()})
    if literal and literal.lower() != "unresolved":
        line = {"cat": "synthesis", "text": literal}
        if mw.get("grounds"):
            line["who"] = "; ".join(str(g) for g in mw["grounds"])
        lines.append(line)
    if not lines:
        return None
    out = {"lines": lines}
    if mw.get("image"):
        out["image"] = mw["image"]
    if (ow.get("english") or "").strip():
        out["rendering"] = ow["english"].strip()
    if (ow.get("why") or "").strip():
        out["why"] = ow["why"].strip()
    return out


DICTIONARY_IN_LOCUS = re.compile(r"webster|gcide|wordnet|oewn|wiktionary|kaikki|century|roget|moby", re.I)


def candidate(c) -> dict:
    """A card candidate as a wording candidate. New records carry define()'s `loci`: the first is the
    candidate's locus and the dictionary it names its source, so the builder (B4) verifies it against
    define. Older records carry no locus: the dictionary of the first entry is named, no locus is
    given, and B4 says so."""
    if isinstance(c, str):
        return {"word": c}
    out = {"word": c.get("word")}
    loci = [x for x in c.get("loci") or [] if x]
    entries = c.get("entries") or []
    if loci:
        out["locus"] = loci[0]
        m = DICTIONARY_IN_LOCUS.search(loci[0])
        if m:
            out["source"] = m.group(0).lower()
    elif entries:
        out["source"] = entries[0].split(" ", 1)[0]
    definition = c.get("matching_sense") or c.get("modern_first_sense") or (entries[0] if entries else None)
    if definition:
        out["definition"] = definition.split(":", 1)[-1].strip() if not c.get("matching_sense") else definition
    if c.get("found_by"):
        out["found_by"] = c["found_by"]
    return out


def card(cw: dict, ow: dict | None, mw: dict | None, locus: str, gram: dict | None = None) -> dict:
    """One builder card. `gram` holds the fields grammar_fields() filled from the analysis store; the
    translation's own `parts` (a compound's members with their English) take precedence."""
    ow, gram = ow or {}, gram or {}
    w: dict = {"i": cw["i"], "iast": cw.get("form"), "deva": devanagari(cw.get("form") or ""),
               "gloss": (ow.get("english") or "").strip() or None, "stem": cw.get("lemma"),
               "root": cw.get("root"), "morph": cw.get("grammar"), "word_class": cw.get("class")}
    rel, head = cw.get("relation"), cw.get("depends_on")
    if rel:
        w["karaka"] = f"{rel} → {head}" if head else rel
    for k in ("root", "root_id", "rootGloss", "affix", "evidence"):
        if gram.get(k):
            w[k] = gram[k]
    if not w.get("morph") and gram.get("morph"):
        w["morph"] = gram["morph"]
    if ow.get("parts"):
        w["parts"] = [{"form": p.get("stem"), "gloss": p.get("english")} for p in ow["parts"] if isinstance(p, dict)]
    elif gram.get("parts"):
        w["parts"] = gram["parts"]
    comp = cw.get("compound")
    if comp:
        w["compound"] = {"type": comp.get("type"), "vigraha": comp.get("analysis"),
                         "members": [m.get("stem") for m in comp.get("members") or []]}
    term, terms = term_fields(cw, ow)
    if term:
        w["term"] = term
    if terms:
        w["terms"] = terms
    preserved = any(r.get("policy") == "preserve" for r in cw.get("standing") or [] if not r.get("seed") and not r.get("member"))
    if cw.get("class") == "content" and not preserved:
        w["wording"] = {"sense_description": ((mw or {}).get("literal") or (mw or {}).get("sense") or "").strip() or None,
                        "candidates": [candidate(c) for c in cw.get("candidates") or []],
                        "chosen": w["gloss"], "why": (ow.get("why") or "").strip() or None}
    m = meaning_block(mw, ow, locus)
    if m:
        w["meaning"] = m
    w["pipeline"] = {k: ow.get(k) for k in ("kind", "found_by", "carried", "lost", "challenge") if k in ow}
    return {k: v for k, v in w.items() if v is not None}


# ---------------------------------------------------------------- what the builder requires
def builder_gaps(v: dict) -> list[str]:
    """Fields build_gita_chapter_reader requires that are absent: check_verse (sense, english,
    words, grammar, deviations, ≥5 secondaries_consulted) and check_card (iast, deva, gloss, parts,
    affix, morph, word_class; a root's rootGloss, gaṇa and pada, root_id; a compound's type,
    vigraha and members; evidence or fallback for a grammatical claim; wording on a content word;
    meaning on a card with a root, a compound or a preserved term)."""
    out = []
    for k in ("sense", "english", "words", "grammar"):
        if not v.get(k):
            out.append(f"verse {k} absent")
    if len(v.get("secondaries_consulted") or []) < MIN_SECONDARIES:
        out.append(f"fewer than {MIN_SECONDARIES} secondaries_consulted (the pipeline consults none)")
    for f in v.get("forks") or []:
        if not f.get("words"):
            out.append("second line: no card index the fork concerns")
    for w in v.get("words") or []:
        tag = f"[{w.get('i')}] {w.get('iast')}"
        for k in ("iast", "deva", "gloss", "parts", "affix", "morph"):
            if not w.get(k):
                out.append(f"{tag}: card {k} absent")
        if any(not p.get("form") or not p.get("gloss") for p in w.get("parts") or []):
            out.append(f"{tag}: a parts[] piece lacks form or gloss")
        if w.get("word_class") not in WORD_CLASSES:
            out.append(f"{tag}: word_class {w.get('word_class')!r} not one the builder admits")
        if w.get("root"):
            if not w.get("rootGloss"):
                out.append(f"{tag}: rootGloss absent")
            if not re.search(r"\(([a-zā]+ādi),\s*(\d+)\s*([PAUĀ])\b", w["root"]):
                out.append(f"{tag}: root without gaṇa and pada")
            if not w.get("root_id"):
                out.append(f"{tag}: root_id absent")
        comp = w.get("compound")
        if comp:
            for k in ("type", "vigraha", "members"):
                if not comp.get(k):
                    out.append(f"{tag}: compound {k} absent")
        affix = w.get("affix") or ""
        if (w.get("root") or comp or (affix and "avyaya" not in affix and "nipāta" not in affix)) \
                and not w.get("evidence") and not w.get("fallback"):
            out.append(f"{tag}: no evidence for the grammatical claim")
        for k in ("sense_description", "candidates", "chosen"):     # card() writes wording on every content
            if "wording" in w and not w["wording"].get(k):           # word that is not a preserved term
                out.append(f"{tag}: wording {k} absent")
        for c in (w.get("wording") or {}).get("candidates") or []:
            if c.get("locus") and not c.get("source"):
                out.append(f"{tag}: candidate '{c.get('word')}' cites a locus that names no dictionary")
        # stricter than the builder, which accepts any evidence: each claim needs its own
        kinds = {e.get("kind") for e in w.get("evidence") or []}
        sutras = [e.get("sutra") or "" for e in w.get("evidence") or []]
        if w.get("root") and w.get("evidence") and "dhatupatha" not in kinds:
            out.append(f"{tag}: the root has no Dhātupāṭha evidence")
        if comp and w.get("evidence") and not any(SAMASA_SUTRA.match(x) for x in sutras):
            out.append(f"{tag}: the compound type has no samāsa sūtra in the evidence")
        if (w.get("root") or comp) and w.get("word_class") not in ("particle", "pronoun", "name") and not w.get("meaning"):
            out.append(f"{tag}: meaning absent")
    return out


# ---------------------------------------------------------------- conversion
@dataclass
class Conversion:
    packet: dict
    shard: dict
    unfinished: dict[str, list[str]]           # scope (verse locus, unit file or "chapter") → reasons
    review: dict = field(default_factory=dict)  # the review record, without its producer_sha256

    @property
    def finished(self) -> bool:
        return not any(self.unfinished.values())


def _sha(rec_path: Path) -> str:
    return hashlib.sha256(rec_path.read_bytes()).hexdigest()


def convert(run: str, chapter: int, runs: Path = RUNS, packets: Path = PACKETS) -> Conversion:
    run_dir = runs / run
    records = load_records(run_dir)
    parsed = parse_words(run_dir)
    verses = chapter_packets(chapter, packets)
    loci = [v["locus"] for v in verses]
    unfinished: dict[str, list[str]] = defaultdict(list)
    owner: dict[str, str] = {}
    for name, rec in records.items():
        for loc in rec.get("unit") or []:
            if loc in owner:
                unfinished[loc].append(f"in two unit records ({owner[loc]}, {name})")
            owner.setdefault(loc, name)
        probs = unit_problems(rec)
        if probs:
            unfinished[name] += probs
    stray = sorted(set(owner) - set(loci))
    if stray:
        unfinished["chapter"].append(f"unit records for verses outside chapter {chapter}: {stray}")
    for loc in loci:
        if loc not in owner:
            unfinished[loc].append("no unit record translates this verse")
    unfinished["chapter"] += [
        "no term-policy hash: the run does not record the policy it was translated under (builder B1)",
        "the review record has no `complete`: the pipeline's review read each unit's English lines and word "
        "choices, not the shard's grammar fields, evidence or meaning lines; no source states the shard was "
        "reviewed in full (builder REVIEW)"]

    out_verses = []
    for pv in verses:
        loc = pv["locus"]
        name = owner.get(loc)
        rec = records.get(name) if name else None
        if not rec or not rec.get("output"):
            continue
        out = rec["output"]
        cverse = next((cv for cv in (rec.get("card") or {}).get("verses") or [] if cv.get("locus") == loc), None)
        if cverse is None:
            unfinished[loc].append("the unit record has no card for this verse")
            continue
        ow = {w["i"]: w for w in out.get("words") or [] if w.get("locus") == loc}
        mw = {w["i"]: w for w in ((rec.get("meaning") or {}).get("words") or []) if w.get("locus") == loc}
        cards = sorted(cverse.get("words") or [], key=lambda w: w["i"])
        form = {w["i"]: w.get("form") for w in cards}
        if [w["i"] for w in cards] != list(range(len(cards))):
            unfinished[loc].append("card indices are not contiguous from 0")
        line = (out.get("lines") or {}).get(loc)
        if not line:
            unfinished[loc].append("no English line for this verse")
            line = ""
        missing_en = [w["i"] for w in cards if not (ow.get(w["i"], {}).get("english") or "").strip()]
        if missing_en:
            unfinished[loc].append(f"no English for words {missing_en}")
        slotted = (out.get("slotted") or {}).get(loc)
        if slotted:
            slots = from_slotted(slotted, line, cards, ow)
            unfinished[loc] += slots.problems
        else:
            slots = place_slots(line, [(w["i"], ow.get(w["i"], {}).get("english") or "", (w.get("lemma"), w.get("grammar")))
                                       for w in cards])
        for i in slots.ambiguous:
            unfinished[loc].append(f"[{i}] {form[i]}: its English '{ow[i]['english']}' occurs more than once in the "
                                   "line and the record does not say which occurrence is this word's")
        words, grammar_notes = [], {}
        for cw in cards:
            a, d, gram, why = analysis_for(loc, cw, parsed.get((loc, cw["i"])))
            fields, notes = grammar_fields(a, d, gram, cw.get("root")) if a else ({"morph": gram} if gram else {}, [why])
            if notes:
                grammar_notes[cw["i"]] = notes
            words.append(card(cw, ow.get(cw["i"]), mw.get(cw["i"]), loc, fields))
        forks = []
        alt = out.get("alternative") or {}
        alt_line = (alt.get("lines") or {}).get(loc) or strip_slots((alt.get("slotted") or {}).get(loc))
        if alt_line:
            fork_words = sorted({w["i"] for w in alt.get("words") or [] if w.get("locus") == loc}) or \
                         sorted({i for f in cverse.get("forks") or [] for i in f.get("words") or []})
            basis = (alt.get("fork") or "").strip() or None
            forks.append({"at": " … ".join(form[i] for i in fork_words if i in form) or loc,
                          "words": fork_words,
                          "construals": [{"reading": line, "grammar_basis": basis}, {"reading": alt_line, "grammar_basis": basis}],
                          "followed": 0, "reason_class": 5, "reason": basis, "open": True, "display": alt_line})
        v = {"locus": loc, "speaker": pv.get("speaker"), "meter": (pv.get("meter") or {}).get("name") if isinstance(pv.get("meter"), dict) else pv.get("meter"),
             "iast": pv["iast"], "devanagari": pv["devanagari"], "english": slots.english, "words": words,
             "forks": forks, "deviations": [],
             "pipeline": {"unit": name, "record_sha256": _sha(run_dir / "translate" / name),
                          "slots_from": "slotted line" if slotted else "located by publish.py",
                          "unplaced_words": slots.unplaced, "placed_by_sanskrit_order": slots.by_order,
                          "grammar_not_filled": grammar_notes,
                          "card_forks": cverse.get("forks") or [], "taste": (rec.get("rounds") or [{}])[-1].get("taste") or []}}
        unfinished[loc] += builder_gaps(v)
        out_verses.append(v)

    unfinished = {k: r for k, r in unfinished.items() if r}
    n = len(verses)
    for v in out_verses:
        if unfinished.get(v["locus"]):
            v["unfinished"] = unfinished[v["locus"]]
    shard = {"schema_version": SCHEMA if not unfinished else SCHEMA_UNFINISHED, "chapter": chapter, "range": f"1-{n}",
             "packet_path": "packet.json",
             "pipeline": {"run": run, "units": {name: _sha(run_dir / "translate" / name) for name in records},
                          "declined": {name: (r.get("output") or {}).get("declined") or [] for name, r in records.items()}},
             "verses": out_verses}
    if unfinished:
        shard["unfinished"] = unfinished
    packet = {"chapter": chapter, "verse_count": n, "derived_from": "internal/gita_pipeline/packets/verses",
              "verses": [{"locus": v["locus"], "speaker": v.get("speaker"),
                          "meter": (v.get("meter") or {}).get("name") if isinstance(v.get("meter"), dict) else v.get("meter"),
                          "iast": v["iast"], "devanagari": v["devanagari"]} for v in verses]}
    return Conversion(packet, shard, unfinished, review_record(records, run_dir))


# ---------------------------------------------------------------- the review record
SEVERITY = {"S1": 1, "S2": 2, "S3": 3}      # pipeline S1 (must be fixed) ↔ builder severity 1 (blocks)


def review_record(records: dict[str, dict], run_dir: Path) -> dict:
    """The builder's review file, written from what the run holds: the pipeline's review call of each
    unit's last round (findings left: S1/S2 in rec["review"], S3 in the round's "taste"), its model,
    and (added at write time) the sha256 of the shard. Elements with no source in the run are not
    written and are listed in `not_in_the_run`: `complete` (no source states the shard was reviewed in
    full) and `date`."""
    findings, models, units = [], set(), {}
    for name, rec in sorted(records.items()):
        last = (rec.get("rounds") or [{}])[-1]
        for f in list(rec.get("review") or []) + list(last.get("taste") or []):
            findings.append({"unit": name, "locus": f.get("locus"), "severity": SEVERITY.get(f.get("severity")),
                             "pipeline_severity": f.get("severity"), "status": "open",
                             **{k: f.get(k) for k in ("kind", "quote", "says", "fix") if f.get(k)}})
        for c in rec.get("calls") or []:
            if c.get("task") == "review":
                models.add(f"{c.get('model')} ({c.get('effort')})" if c.get("effort") else str(c.get("model")))
        units[name] = {"rounds": len(rec.get("rounds") or []), "record_sha256": _sha(run_dir / "translate" / name)}
    return {"schema_version": "pipeline-review-v1", "written_by": "publish.py",
            "source": "pipeline.py translate stage, review step: one model call per unit and round, on the "
                      "unit's English lines and word choices",
            "reviewer_models": sorted(models), "units": units, "findings": findings,
            "not_in_the_run": ["complete", "date"]}


# ---------------------------------------------------------------- output
def shard_name(n: int) -> str:
    return f"producer-01-{n:02d}.json"


def review_name(n: int) -> str:
    return f"independent-review-01-{n:02d}.json"      # the builder's name for the shard's review


def guard_out(out: Path, conv: Conversion) -> None:
    """Never overwrite or sit beside files publish.py did not write: hand-made producer shards
    (chapter 12's) or a chapter packet from build_gita_chapter_packet.py."""
    for p in out.glob("producer-*.json"):
        if "pipeline" not in json.loads(p.read_text(encoding="utf-8")):
            raise PublishError(f"{p} was not written by publish.py; the builder would read both. Use another --out.")
    for p in out.glob("independent-review-*.json"):
        if json.loads(p.read_text(encoding="utf-8")).get("written_by") != "publish.py":
            raise PublishError(f"{p} was not written by publish.py; refusing to overwrite it. Use another --out.")
    pk = out / "packet.json"
    if pk.exists() and "derived_from" not in json.loads(pk.read_text(encoding="utf-8")):
        raise PublishError(f"{pk} was not written by publish.py; refusing to overwrite it. Use another --out.")


def write(out: Path, conv: Conversion) -> list[Path]:
    guard_out(out, conv)
    out.mkdir(parents=True, exist_ok=True)
    for p in [*out.glob("producer-*.json"), *out.glob("independent-review-*.json")]:
        p.unlink()                              # earlier publish.py files (guard_out checked they are)
    n = conv.packet["verse_count"]
    paths = [out / "packet.json", out / shard_name(n), out / review_name(n)]
    paths[0].write_text(json.dumps(conv.packet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    paths[1].write_text(json.dumps(conv.shard, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    review = {**conv.review, "shard": paths[1].name, "producer_sha256": _sha(paths[1])}
    paths[2].write_text(json.dumps(review, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return paths


def summarize(unfinished: dict[str, list[str]], limit: int = 6) -> list[str]:
    """Reasons grouped by kind (locus and word stripped), with where each occurs."""
    groups: dict[str, list[str]] = defaultdict(list)
    for scope, reasons in unfinished.items():
        for r in reasons:
            m = re.match(r"(\[\d+\] \S+): (.*)", r)
            kind = re.sub(r"'[^']*'", "'…'", m.group(2)) if m else r
            groups[kind].append(f"{scope}{m.group(1).split(' ')[0] if m else ''}")
    return [f"{len(at):4d} × {kind}  [{', '.join(at[:limit])}{', …' if len(at) > limit else ''}]"
            for kind, at in sorted(groups.items(), key=lambda kv: -len(kv[1]))]


def builder_check(chapter: int, out: Path) -> int:
    """The builder's own checks on DIR, read-only: run(ctx) without write_outputs."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_gita_chapter_reader as B
    ctx = B.Ctx(chapter=chapter, root=ROOT, chapter_dir=out)
    result = None
    try:
        result = B.run(ctx)
    except B.BuildError as e:
        ctx.report.err("BUILD", str(e))
    B.print_report(ctx, result)
    return len(ctx.report.errors)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", required=True)
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True, help="the builder's chapter directory to write")
    ap.add_argument("--allow-unfinished", action="store_true",
                    help="write even when unfinished; reasons recorded, schema marked so the builder refuses it")
    ap.add_argument("--check", action="store_true", help="then run the builder's checks on --out (read-only)")
    ap.add_argument("--runs", type=Path, default=RUNS, help=argparse.SUPPRESS)
    ap.add_argument("--packets", type=Path, default=PACKETS, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    try:
        conv = convert(a.run, a.chapter, a.runs, a.packets)
        if not conv.finished:
            print(f"UNFINISHED: run {a.run}, chapter {a.chapter}: "
                  f"{sum(len(r) for r in conv.unfinished.values())} reasons", file=sys.stderr)
            for s in summarize(conv.unfinished):
                print(s, file=sys.stderr)
            if not a.allow_unfinished:
                print("REFUSED: nothing written (--allow-unfinished writes a shard the builder refuses).", file=sys.stderr)
                return 1
        for p in write(a.out, conv):
            print("written", p)
    except PublishError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1
    status = 0 if conv.finished else 2
    if a.check:
        errors = builder_check(a.chapter, a.out)
        status = status or (1 if errors else 0)
    return status


if __name__ == "__main__":
    sys.exit(main())

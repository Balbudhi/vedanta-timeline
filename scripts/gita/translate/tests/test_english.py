import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import english  # noqa: E402

if not english.DB.exists():
    pytest.skip(f"English index {english.DB} not built", allow_module_level=True)

# Gold set (lead, 2026-11-09): sense -> words the table must contain within 25 rows.
GOLD = [
    ("toil that hurts, painful labour", ["travail"]),
    ("immediately, with no interval", ["straightway", "instantly"]),
    ("one who lifts up and carries out", ["upbearer"]),
    ("patient under injury, enduring offence", ["forbearing"]),
    ("one who has a share in, participates", ["partaker", "participant", "sharer"]),
    ("to sit near and attend on", ["attend"]),
    ("without a dwelling, homeless", ["houseless"]),
    ("skilful, quick and clever with the hands", ["deft"]),
    ("to recoil, draw back in fear", ["shrink", "recoil"]),
    ("freed, set loose", ["loosed", "loose"]),
    ("unchanging, standing firm like an anvil", ["steadfast", "immovable"]),
    ("not hating, free of hatred", ["unhating"]),
    ("the faculty of thinking and willing", ["mind"]),
    ("repeated exercise to acquire skill", ["practice", "exercise"]),
    ("to dislike, have aversion to", ["mislike"]),
]
KNOWN_MISS = {"upbearer"}   # rank ~46: found only through Roget co-membership with the strong hits


def words_of(rows):
    return [r["word"] for r in rows]


@pytest.fixture(scope="module")
def tables():
    return {sense: english.english_table(sense) for sense, _ in GOLD}


@pytest.mark.parametrize("sense,word", [
    pytest.param(s, w, marks=pytest.mark.xfail(strict=True, reason="known miss")) if w in KNOWN_MISS else (s, w)
    for s, ws in GOLD for w in ws])
def test_gold_word_within_25(tables, sense, word):
    assert word in words_of(tables[sense])


def test_gold_recall_floor(tables):
    hits25 = sum(w in words_of(tables[s]) for s, ws in GOLD for w in ws)
    hits10 = sum(w in words_of(tables[s])[:10] for s, ws in GOLD for w in ws)
    assert (hits25, hits10) >= (21, 18), (hits25, hits10)


# ---------------------------------------------------------------- the row contract (what stage 2d reads)
def test_row_shape(tables):
    for sense, rows in tables.items():
        assert 0 < len(rows) <= 25, sense
        fits = [r["fit"] for r in rows]
        assert fits == sorted(fits, reverse=True) and all(0 <= f <= 1 for f in fits), sense
        assert len(set(words_of(rows))) == len(rows), sense
        for r in rows:
            assert set(r) == {"word", "pos", "defs", "tags", "modern", "fit", "via"}
            assert r["pos"] in ("n", "v", "adj", "adv", None)
            assert 1 <= len(r["defs"]) <= 2 and all(len(d) <= 140 for d in r["defs"])
            sources = [d.split(": ", 1)[0] for d in r["defs"] if ": " in d]
            assert len(sources) == len(set(sources)), r
            assert set(r["tags"]) <= english.REGISTER
            assert r["modern"] is None or isinstance(r["modern"], str)


def test_limit_and_empty():
    assert len(english.english_table("joy, delight", limit=5)) == 5
    assert english.english_table("") == []
    assert english.english_table("the of and") == []


def test_register_tags_come_from_the_matching_sense():
    rows = {r["word"]: r for r in english.english_table("to dislike, have aversion to")}
    assert "mislike" in rows
    assert all(t in english.REGISTER for t in rows["mislike"]["tags"])


# ---------------------------------------------------------------- reading the sense
def test_frames():
    f = english._frame
    assert f("one who lifts up")[0] == "agent"
    assert f("to recoil")[0] == "verb"
    assert f("not hating")[0] == "neg" and f("free of hatred")[0] == "neg" and f("without a dwelling")[0] == "neg"
    assert f("freed")[0] == "participle"
    assert f("immediately")[0] == "adv"
    assert f("the faculty of thinking")[0] == "noun"
    assert f("painful labour")[0] is None


def test_parse_splits_coordination_and_similes():
    cl = english.parse("one who lifts up and carries out")
    texts = {c.text: c for c in cl}
    assert {"one who lifts up", "one who carries out"} <= set(texts)
    assert texts["one who lifts up and carries out"].heads == ["lift", "carry"]
    cl = english.parse("unchanging, standing firm like an anvil")
    simile = [c for c in cl if c.text.startswith("like")]
    assert simile and simile[0].weight == 0.6
    assert [c for c in cl if c.whole]                       # several parts -> one whole-sense clause too
    assert not [c for c in english.parse("homeless") if c.whole]


def test_image_clauses_count_less():
    cl = english.parse("steadfast", "an anvil")
    assert {c.text: c.weight for c in cl}["an anvil"] == 0.6
    assert english.english_table("steadfast", "an anvil")


def test_pos_argument_overrides_frames():
    cl = english.parse("one who knows")
    assert english.sense_pos(cl, None) == {"n"}
    assert english.sense_pos(cl, "verb") == {"v"}
    assert english.sense_pos(english.parse("freed"), None) == {"adj", "v"}


def test_spelling_normalization():
    assert english.us_spelling("labour") == "labor" and english.us_spelling("labours") == "labors"
    assert english.us_spelling("offence") == "offense" and english.us_spelling("skilful") == "skillful"
    assert english.us_spelling("four") == "four" and english.us_spelling("hour") == "hour"


def test_porter_matches_the_index_tokenizer():
    """idf lookups read FTS5's porter vocabulary, so stems must be the tokenizer's own."""
    sample = ("travail painful labours hurts carries lifts participates participation dwelling homeless "
              "skillful quickly cleverness hands recoiling shrinking freed loosed unchanging standing firmly "
              "hatred hating thinking willing repeated exercises acquire dislike aversion generalization "
              "relational conditional sensibility happiness hopeful formality adjustment controlling")
    con = sqlite3.connect(":memory:")
    con.execute("create virtual table t using fts5(x, tokenize='porter unicode61')")
    con.execute("create virtual table v using fts5vocab(t, 'instance')")
    for w in sample.split():
        con.execute("insert into t(x) values(?)", (w,))
    theirs = [term for (term,) in con.execute("select term from v order by doc")]
    assert [english.porter(w) for w in sample.split()] == theirs


# ---------------------------------------------------------------- scoring
def test_def_score_partitions():
    c = english.parse("to recoil")[0]
    assert english.def_score("To recoil", c) == pytest.approx(1.0)
    assert english.def_score("To draw back; to recoil", c) == pytest.approx(0.95)   # exactly one segment
    assert english.def_score("To draw back; to recoil, as in fear", c) == pytest.approx(0.76)  # + 'fear'
    assert english.def_score("A kind of fish", c) == 0.0
    two = english.parse("painful labour")[0]
    full = english.def_score("Painful labor", two)
    half = english.def_score("Painful", two)
    assert full == pytest.approx(1.0) and 0 < half < 0.5 * full    # half a clause is worth about a third
    neg = english.parse("not hating")[0]
    assert english.def_score("Not hating", neg) > 3 * english.def_score("Hating", neg)


def test_negation_ranks_the_negated_not_the_opposite(tables):
    rows = tables["not hating, free of hatred"]
    top = words_of(rows)[:5]
    assert not {"hate", "hating", "hateful", "hatred", "spite"} & set(top), top
    assert any(w.startswith("un") or w.endswith("less") for w in top)


def test_agent_frame_yields_agent_nouns(tables):
    rows = tables["one who has a share in, participates"][:10]
    assert sum(r["pos"] == "n" for r in rows) >= 8


def test_derived_forms_are_attested(tables):
    con = english._con()
    derived = [r for rows in tables.values() for r in rows
               if any(" form of " in v or v.startswith("negation of") for v in r["via"])]
    assert {"loosed", "unhating"} <= set(words_of(derived))
    for r in derived:
        w = r["word"]
        assert (con.execute("select 1 from defs where hw=? limit 1", (w,)).fetchone()
                or con.execute("select 1 from inflections where form=? limit 1", (w,)).fetchone()), w


def test_participle_frame_offers_the_participle_above_its_verb(tables):
    ws = words_of(tables["freed, set loose"])
    assert ws.index("loosed") < ws.index("loose")


def test_no_inflection_duplicates_in_one_role(tables):
    con = english._con()
    for sense, rows in tables.items():
        role = {(r["word"], r["pos"]) for r in rows}
        for r in rows:
            if any(" form of " in v for v in r["via"]):
                continue
            for (lemma,) in con.execute("select distinct lower(lemma) from inflections where form=?", (r["word"],)):
                assert lemma == r["word"] or (lemma, r["pos"]) not in role, (sense, r["word"], lemma)


# ---------------------------------------------------------------- operation
def test_threads_give_the_same_tables(tables):
    senses = [s for s, _ in GOLD[:6]]
    with ThreadPoolExecutor(4) as ex:
        got = list(ex.map(english.english_table, senses))
    assert [words_of(g) for g in got] == [words_of(tables[s]) for s in senses]


def test_time_per_call():
    for sense, _ in GOLD:
        t = time.time()
        english.english_table(sense)
        assert time.time() - t < 1.5, sense

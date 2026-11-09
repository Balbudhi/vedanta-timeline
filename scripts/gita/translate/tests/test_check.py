import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check  # noqa: E402

ROW = {"sense_id": "bhakta.partaker", "signification": ["sense", "image:sharing"],
       "rendering_set": [{"english": "partaker", "carries": ["sense", "image:sharing"]},
                         {"english": "devotee", "carries": ["sense"]}]}
INP = {"verses": [{"locus": "12.14", "construal": {"forks": [], "words": [
    {"i": 0, "form": "madbhaktaḥ", "word_class": "content"},
    {"i": 1, "form": "na", "word_class": "particle"}]}}]}


def out(line, words, alt=None):
    return {"lines": {"12.14": line}, "words": words, "alternative": alt}


def w(i, english, rendering=None, sid="bhakta.partaker", lost=None, deviation=None):
    return {"locus": "12.14", "i": i, "english": english, "rendering": rendering, "sense_id": sid,
            "lost": lost or [], "deviation": deviation}


ROWS = {"bhakta.partaker": ROW}


def test_clean_line_passes():
    o = out("not my partaker", [w(0, "my partaker", "partaker"), w(1, "not", sid=None)])
    assert check.verse(o, INP, ROWS) == []


def test_addition_is_caught():
    o = out("not my true partaker", [w(0, "my partaker", "partaker"), w(1, "not", sid=None)])
    assert any("L0" in e and "true" in e for e in check.verse(o, INP, ROWS))


def test_repeated_word_counts():  # multiset: a word used twice must be rendered twice
    o = out("not my partaker, partaker", [w(0, "my partaker", "partaker"), w(1, "not", sid=None)])
    assert any("L0" in e for e in check.verse(o, INP, ROWS))


def test_dropped_particle_is_caught():
    o = out("my partaker", [w(0, "my partaker", "partaker")])
    assert any("na" in e and "not rendered" in e for e in check.verse(o, INP, ROWS))


def test_flatter_rendering_must_show_loss():
    o = out("not my devotee", [w(0, "my devotee", "devotee"), w(1, "not", sid=None)])
    assert any("image:sharing" in e for e in check.verse(o, INP, ROWS))


def test_shown_loss_needs_all_three_steps():
    lost = [{"component": "image:sharing", "existing_searched": "english 'one who shares'", "new_attempted": ""}]
    o = out("not my devotee", [w(0, "my devotee", "devotee", lost=lost), w(1, "not", sid=None)])
    assert any("new_attempted" in e for e in check.verse(o, INP, ROWS))


def test_rendering_outside_row_needs_deviation():
    o = out("not my worshipper", [w(0, "my worshipper", "worshipper"), w(1, "not", sid=None)])
    assert any("W6" in e for e in check.verse(o, INP, ROWS))


def test_second_line_needs_grammatical_fork():
    o = out("not my partaker", [w(0, "my partaker", "partaker"), w(1, "not", sid=None)],
            alt={"fork": "doctrine", "lines": {"12.14": "x"}})
    assert any("M3" in e for e in check.verse(o, INP, ROWS))


def test_lexicon_default_must_carry_or_show():
    row = {**ROW, "default": "devotee", "searches": [{"query": "q"}], "loss": []}
    errs = check.lexicon({"rows": [row]}, {}, [{"cmd": "english", "args": ["q"]}, {"cmd": "define", "args": ["devotee"]}])
    assert any("image:sharing" in e for e in errs)


def test_lexicon_requires_search_and_define():
    row = {**ROW, "default": "partaker", "searches": [{"query": "q"}], "loss": []}
    errs = check.lexicon({"rows": [row]}, {}, [])
    assert any("english" in e for e in errs) and any("define" in e for e in errs)

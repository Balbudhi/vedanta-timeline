import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import english_roots as R  # noqa: E402

needs_db = pytest.mark.skipif(not R.DB.exists(), reason=f"{R.DB} not built (english_roots.py build)")


# ---------------------------------------------------------------- parsing (no index needed)
def test_norm_sa_scripts_marks_and_accents():
    assert R.norm_sa("√युज्") == "yuj"
    assert R.norm_sa("yunákti") == "yunakti"
    assert R.norm_sa("ṛ́śya") == "ṛśya"          # accent on a vocalic r removed
    assert R.norm_sa("śraddhā") == "śraddhā"      # ś is s + U+0301 in NFD and must survive
    assert R.norm_sa("मु॒ञ्चति॑") == "muṃcati"     # Vedic accent marks dropped, nasal before stop → ṃ
    assert R.norm_sa("manaḥ") == "manas"


def test_split_header_removes_generated_tree():
    text = ("Etymology tree\nProto-Indo-European *steh₂-der.\nProto-Germanic *standaną\nEnglish stand\n"
            "From Middle English stonden, from Old English standan (“to stand, occupy a place”).")
    tree, prose = R.split_header(text)
    assert tree == ["Proto-Indo-European *steh₂-der.", "Proto-Germanic *standaną", "English stand"]
    assert prose.startswith("From Middle English stonden")
    assert R._pie_key(tree[0].split(" ", 1)[1]) == "steh₂-"   # the tree's "der." marker is not part of it


def test_pie_key_keeps_roots_only():
    assert R._pie_key("*yewg-") == "yewg-"
    assert R._pie_key("*steh₂-.") == "steh₂-"
    assert R._pie_key("*h₁ésti") is None       # a word, not a root
    assert R._pie_key("*-eti") is None         # a suffix


def test_chain_stops_at_comparisons():
    prose = ("From Old English cnāwan (“to know, perceive”), from Proto-Indo-European *ǵneh₃- (“to know”).\n"
             "Cognates\n* from Indo-European: Latin gnoscō, Hindi जानना (jānnā, “to know”).")
    chain = R.chain_of(prose)
    assert "cnāwan" in chain and "gnoscō" not in chain
    mid = "from Gaulish *tannos (“green oak”). Per this hypothesis, related to Sanskrit धनु (dhánu)."
    assert "धनु" not in R.chain_of(mid)


def test_etyma_in_chain_order_with_languages():
    chain = ("A learned borrowing from Latin assiduus, from assidere (“to sit down to”), "
             "from ad- (“to”) + sedere (“to sit”).")
    glossed, bare = R.etyma(chain)
    assert [(lang, t, g) for _, lang, t, g in glossed] == [("Latin", "assidere", "to sit down to"),
                                                     ("Latin", "ad-", "to"), ("Latin", "sedere", "to sit")]
    assert [(lang, t) for _, lang, t in bare] == [("Latin", "assiduus")]
    _, bare = R.etyma("Learned borrowing from Latin pervādō.")
    assert [(lang, t) for _, lang, t in bare] == [("Latin", "pervādō")]


def test_sanskrit_in_prose_attributes_by_nearest_language():
    prose = ("Cognate with Latin stō (“to stand”), Hindi जानना (jānnā, “to know”), "
             "Sanskrit स्था (sthā, “to stand”).")
    assert R.sanskrit_in_prose(prose) == [("स्था", "sthā", "to stand", "cognate")]
    assert R.sanskrit_in_prose("Borrowed from Sanskrit द्वंद्व (dvaṃdvá).")[0][3] == "loan"


def test_template_terms_roots_ids_and_inline_modifiers():
    tps = [{"name": "root", "args": {"1": "en", "2": "ine-pro", "3": "*bʰerH-", "id": "brown", "4": "*ǵʰwer-"}},
           {"name": "cog", "args": {"1": "sa", "2": "युग", "t": "yoke"}},
           {"name": "m", "args": {"1": "sa", "2": "manus<t:human>,manu<t:human; thought>"}},
           {"name": "der", "args": {"1": "en", "2": "ine-pro", "3": "*h₁ed-", "t": "to eat"}}]
    got = list(R.template_terms(tps))
    assert ("root", "ine-pro", "*bʰerH-", "", "", "brown") in got
    assert ("root", "ine-pro", "*ǵʰwer-", "", "", "") in got
    assert ("cognate", "sa", "युग", "yoke", "", "") in got
    assert ("cognate", "sa", "manus", "human", "", "") in got and ("cognate", "sa", "manu", "human; thought", "", "") in got
    assert ("source", "ine-pro", "*h₁ed-", "to eat", "", "") in got


def test_parse_entry_loan_versus_cognate():
    cog = R.parse_entry({"word": "stand", "pos": "verb", "senses": [{"glosses": ["To be upright."]}],
                         "etymology_text": "From Old English standan (“to stand”).\nCognates\nCognate with "
                                           "Sanskrit स्था (sthā, “to stand”).",
                         "etymology_templates": [{"name": "root", "args": {"1": "en", "2": "ine-pro", "3": "*steh₂-"}},
                                                 {"name": "cog", "args": {"1": "sa", "2": "स्था", "t": "to stand"}}]})
    assert cog["sa"]["sthā"][1] == "cognate" and ("steh₂-", "") in cog["pie"] and cog["native"]
    loan = R.parse_entry({"word": "mukt", "pos": "adj", "senses": [{"glosses": ["Liberated."]}],
                          "etymology_text": "Borrowed from Hindi मुक्त (mukt). Compare Sanskrit मुक्ति.",
                          "etymology_templates": [{"name": "cog", "args": {"1": "sa", "2": "मुक्ति"}}]})
    assert loan["sa"]["mukti"][1] == "loan"      # an Indic loan: its Sanskrit forms are its ancestry


# ---------------------------------------------------------------- Sanskrit stem forms
@pytest.mark.parametrize("term,root", [("yuga", "yuj"), ("yunakti", "yuj"), ("tiṣṭhati", "sthā"),
                                       ("prajñā", "jñā"), ("jānāti", "jñā"), ("dadhāti", "dhā"),
                                       ("bharati", "bhṛ"), ("asti", "as"), ("bhavati", "bhū"), ("vedas", "vid"),
                                       ("maṃtra", "man"), ("muṃcati", "muc")])
def test_forms_of_the_root_match(term, root):
    assert R.match_strength(term, R.variants(root)) >= 0.8


@pytest.mark.parametrize("term,root", [("asura", "as"), ("asthi", "as"), ("jana", "jñā"), ("jānu", "jñā"),
                                       ("dhanu", "dhā"), ("bhurvan", "bhṛ")])
def test_unrelated_lookalikes_do_not_match_strongly(term, root):
    assert R.match_strength(term, R.variants(root)) < 0.8


def test_choose_roots_prefers_the_closer_form_and_needs_strength():
    # √as: asti (same vowel, 0.9) beats āsa (grade change landing on √ās, 0.85)
    assert R.choose_roots({("h₁es-", ""): 0.9, ("h₂eHs-", ""): 0.85},
                          {("h₁es-", ""): 0.9, ("h₂eHs-", ""): 0.85}) == [("h₁es-", "")]
    assert R.choose_roots({("x-", ""): 0.5}, {("x-", ""): 0.5}) == []          # a chance prefix alone
    assert R.choose_roots({("men-", "think"): 1.8, ("men-", ""): 0.9},
                          {("men-", "think"): 0.9, ("men-", ""): 0.9}) == [("men-", "think")]


# ---------------------------------------------------------------- image terms
def test_image_alternatives():
    assert R.image_alternatives("carry up/out") == [["carri", "up"], ["carri", "out"]]
    assert R.image_alternatives("go everywhere / pervade") == [["go", "everywhere"], ["pervad"]]
    assert R.image_alternatives("tremble, shake") == [["trembl"], ["shake"]]


def test_gloss_score_action_required_and_parts_compose():
    sit_near = ["sit", "near"]
    assert R.gloss_score(sit_near, "near, close") == 0                       # no action, no match
    alone = R.gloss_score(sit_near, "to sit")
    composed = R.gloss_score(sit_near, "to sit", extra={"to", "toward", "at"})   # ad “to, toward, at”
    assert 0 < alone < composed
    assert R.gloss_score(["shake"], "quiver, shake") > R.gloss_score(["shake"], "to move, shake, swing, agitate, totter")


# ---------------------------------------------------------------- the built index
SANSKRIT_GOLD = [("yuj", "yoke"), ("sthā", "stand"), ("jñā", "know"), ("man", "mind"), ("vid", "wit"),
                 ("vid", "wise"), ("bhṛ", "bear"), ("dhā", "do"), ("as", "is"), ("muc", "meek")]
# Data gaps (measured 2026-11-08): no English Wiktionary etymology cites a Sanskrit form of √ad or a
# cognate (non-loan) form of √bhū, so the root cannot be reached from the Sanskrit side.
SANSKRIT_GAPS = [("ad", "eat"), ("bhū", "be")]
IMAGE_GOLD = [("sit near", "assiduous"), ("sit near", "assess"), ("go everywhere / pervade", "pervade"),
              ("tremble, shake", "quake"), ("tremble, shake", "tremble"), ("anvil", "anvil")]


def words(rows):
    return [r["word"] for r in rows]


@needs_db
@pytest.mark.parametrize("root,word", SANSKRIT_GOLD)
def test_sanskrit_gold_within_15(root, word):
    assert word in words(R.by_sanskrit(root))


@needs_db
@pytest.mark.parametrize("root,word", [pytest.param(r, w, marks=pytest.mark.xfail(strict=True, reason="data gap"))
                                       for r, w in SANSKRIT_GAPS])
def test_sanskrit_gaps(root, word):
    assert word in words(R.by_sanskrit(root))


@needs_db
@pytest.mark.parametrize("pie,word", [("*h₁ed-", "eat"), ("*bʰuH-", "build"), ("h₁es-", "be")])
def test_by_pie_reaches_the_gap_words(pie, word):
    """When the pipeline knows the PIE root (by_pie lists lemmas; inflections such as "is" are skipped)."""
    assert word in words(R.by_pie(pie, limit=30))


@needs_db
def test_direct_cognate_ranks_first():
    for root, word in [("yuj", "yoke"), ("sthā", "stand"), ("vid", "wit"), ("bhṛ", "bear"), ("dhā", "do"), ("as", "is")]:
        rows = R.by_sanskrit(root)
        assert rows[0]["word"] == word and rows[0]["link"] == "cognate", (root, rows[0])


@needs_db
@pytest.mark.parametrize("root,wrong", [("yuj", "louse"), ("as", "ash"), ("vid", "widow"), ("bhaj", "bhang"),
                                        ("dhā", "tan")])
def test_coincidences_are_not_rows(root, wrong):
    """yūkā 'louse', āsa 'ashes', vidhavā 'widow', bhañj 'break', dhanu: forms that look like the root
    but whose etymologies name other roots (or none)."""
    assert wrong not in words(R.by_sanskrit(root, limit=500))


@needs_db
def test_loans_hidden_unless_asked():
    assert "yoga" not in words(R.by_sanskrit("yuj", limit=100))
    rows = {r["word"]: r for r in R.by_sanskrit("yuj", limit=100, loans=True)}
    assert rows["yoga"]["link"] == "loan" and rows["yoke"]["link"] == "cognate"


@needs_db
def test_input_forms_agree():
    base = words(R.by_sanskrit("yuj"))
    assert words(R.by_sanskrit("√yuj")) == base and words(R.by_sanskrit("युज्")) == base


@needs_db
@pytest.mark.parametrize("root", ["tyaj", "dviṣ"])
def test_no_cognate_is_an_explicit_record(root):
    res = R.by_sanskrit(root)
    rec = res.record()
    assert rec["rows"] == [] and rec["none"] is True and rec["note"]
    assert rec["searched"]["normalised"] == R.norm_sa(root)
    assert rec["searched"]["n_stem_forms"] > 1 and rec["searched"]["sanskrit_terms_in_db"] > 1000
    assert rec["searched"]["pie_roots"] == []


@needs_db
@pytest.mark.parametrize("image,word", IMAGE_GOLD)
def test_image_gold_within_15(image, word):
    assert word in words(R.by_image(image))


@needs_db
def test_image_inferred_gloss_is_marked():
    row = next(r for r in R.by_image("go everywhere / pervade") if r["word"] == "pervade")
    assert "pervādō" in row["via"] and "another entry" in row["via"]


@needs_db
def test_row_contract():
    for res in (R.by_sanskrit("yuj"), R.by_sanskrit("vid"), R.by_image("sit near"), R.by_pie("*steh₂-")):
        assert 0 < len(res) <= 15
        assert len(set(words(res))) == len(res)                      # one row per word
        assert [r["score"] for r in res] == sorted((r["score"] for r in res), reverse=True)
        for r in res:
            assert set(r) == {"word", "pos", "modern", "etym", "link", "via", "score"}
            assert r["link"] in ("cognate", "pie", "etymon-gloss")
            assert len(r["modern"]) <= 100 and 0 < len(r["etym"]) <= 160 and r["via"]


@needs_db
def test_queries_are_fast():
    R.by_sanskrit("yuj"), R.by_image("sit near")                     # open the connections
    worst = 0.0
    for q, fn in [(q, R.by_sanskrit) for q, _ in R.BENCH_SANSKRIT] + [(q, R.by_image) for q, _ in R.BENCH_IMAGE]:
        t = time.time()
        fn(q)
        worst = max(worst, time.time() - t)
    assert worst < 0.5, worst

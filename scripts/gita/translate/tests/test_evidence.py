"""Tests for evidence.py (stage 2a; docs/history/gita/WORKFLOW_lexicon_first.md). Expected values were read by hand from the sources:
Dhātupāṭha (prakriya sources/raw/panini/lexica/dhatupatha.json), Śabdakalpadruma / Vācaspatya
(sources/raw/upstream_data/kosha/{skd,vcp}.json), Amarakośa (gretil clean text), BORI mūla."""
import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import evidence as E  # noqa: E402

RUN = E.ROOT / "internal/gita_pipeline/run/ch12-qual"
needs_run = pytest.mark.skipif(not (RUN / "construe").is_dir(), reason="ch12 construals not present")


@pytest.fixture(scope="module")
def lemmas():
    return E.lemmas_from_construals(E.load_construals(RUN))


@pytest.fixture(scope="module")
def cards(lemmas):
    keep = ("bhakta", "paryupās", "upās", "kūṭastha", "manas", "cetas", "abhyāsa", "udvega", "udvij", "priya")
    return {k: E.sanskrit_card(lemmas[k]) for k in keep}


def ids(card):
    out = [d["id"] for d in card["dhatu"]["entries"] + card["dhatu"]["vrtti"]]
    out += [x["id"] for s in ("amara", "kosha", "nirukta", "elsewhere") for x in card[s]]
    for o in card["occurrences"]:
        out += [o["id"]] + [g["id"] for g in o["glosses"]]
    return out


# ------------------------------------------------------------------ sandhi, roots, upasargas
@pytest.mark.parametrize("ups,root,joined", [
    (["pari", "upa"], "ās", "paryupās"), (["upa"], "ās", "upās"), (["sam", "ni"], "as", "saṃnyas"),
    (["ud"], "vij", "udvij"), (["ava"], "āp", "avāp"), (["pra"], "āp", "prāp"), (["nis"], "diś", "nirdiś"),
    (["sam", "ā"], "dhā", "samādhā"), ([], "kṛ", "kṛ")])
def test_join_upasargas(ups, root, joined):
    assert E.join_upasargas(ups, root) == joined


@pytest.mark.parametrize("stem,root,ups", [
    ("udvega", "vij", ("ud",)), ("abhyāsa", "as", ("abhi",)), ("upeta", "i", ("upa",)),
    ("kurvat", "kṛ", ()), ("samādhātum", "dhā", ("sam", "ā")), ("śraddadhāna", "dhā", None)])
def test_split_upasargas(stem, root, ups):
    assert E.split_upasargas(stem, root) == ups


def test_parse_root_hints():
    r = E.parse_root("abhi-√as (kṣepaṇe)")
    assert (r["root"], r["upasargas"], r["arthas"]) == ("as", ["abhi"], ["kṣepaṇe"])
    r = E.parse_root("√ās adādi 2 ātmanepada + pari-upa")
    assert (r["root"], r["upasargas"], r["ganas"]) == ("ās", ["pari", "upa"], [2])
    assert E.parse_root("vi-√vṛj (curādi)")["ganas"] == [10]
    assert E.parse_root("ā-√viś + ṇic")["kinds"] == ["ṇic"]
    assert E.parse_root("√viś tudādi 6 parasmaipada + āṅ + ṇic")["upasargas"] == ["ā"]


# ------------------------------------------------------------------ lemmas from construals
def _w(i, form, stem, root=None, wc="content", **kw):
    return {"i": i, "form": form, "stem": stem, "root": root, "word_class": wc, "analysis_id": None,
            "manual": kw.pop("manual", None), "members": kw.pop("members", None), **kw}


SYNTH = [
    {"locus": "12.1", "words": [
        _w(0, "evaṃ", "evam", wc="particle"),
        _w(1, "ye", "yad", wc="pronoun"),
        _w(2, "bhaktās", "bhakta", "√bhaj", manual={"kind": "krdanta", "krt": {"name": "kta"}}),
        _w(3, "paryupāsate", "pari-upa-ās", "√ās", manual={"kind": "tinanta"}),
        _w(4, "avyaktaṃ", "avyakta", manual={"kind": "samasa"},
           members=[{"stem": "nañ", "root": None, "word_class": "particle"},
                    {"stem": "vyakta", "root": "vi-√añj", "word_class": "content"}])]},
    {"locus": "12.3", "words": [
        _w(5, "paryupāsate", "ās", "√ās", upasargas=["pari", "upa"], manual={"kind": "tinanta"}),
        _w(6, "kurvan", "kurvat", "√kṛ", manual={"kind": "krdanta", "krt": {"name": "śatṛ"}}),
        _w(7, "kuru", "kṛ", "√kṛ", manual={"kind": "tinanta"}),
        _w(8, "parayopetās", "para + upeta", "√i", manual={"kind": "sandhi", "padas": [
            {"form": "parayā", "stem": "para", "root": None, "kind": "subanta", "word_class": "content"},
            {"form": "upetāḥ", "stem": "upeta", "root": "√i", "kind": "krdanta", "krt": {"name": "kta"},
             "word_class": "content"}]}),
        _w(9, "abhyāse", "abhyāsa", "abhi-√as (kṣepaṇe)", manual={"kind": "krdanta", "krt": {"name": "ghañ"}})]},
]


def test_lemmas_skip_function_words_and_fold_verbs():
    lem = E.lemmas_from_construals(SYNTH)
    assert "evam" not in lem and "yad" not in lem and "nañ" not in lem
    # one verbal lemma for 'pari-upa-ās' and for 'ās' + [pari, upa]
    assert lem["paryupās"]["places"] == [{"locus": "12.1", "i": 3, "form": "paryupāsate"},
                                         {"locus": "12.3", "i": 5, "form": "paryupāsate"}]
    assert lem["paryupās"]["root"] == "√ās" and lem["paryupās"]["upasargas"] == ["pari", "upa"]
    # śatṛ and tiṅanta forms of √kṛ are the lemma kṛ; kta stays nominal
    assert [p["i"] for p in lem["kṛ"]["places"]] == [6, 7] and lem["kṛ"]["verbal"]
    assert lem["bhakta"]["root"] == "√bhaj" and not lem["bhakta"]["verbal"]
    # a compound is a lemma and so is each content member, at the compound's place
    assert "samāsa" in lem["avyakta"]["kinds"] and lem["vyakta"]["places"][0]["i"] == 4
    assert lem["vyakta"]["root"] == "√añj" and lem["vyakta"]["upasargas"] == ["vi"]
    # a sandhi-joined word yields each pada, with the pada recorded on the place
    assert lem["upeta"]["places"] == [{"locus": "12.3", "i": 8, "form": "parayopetās", "pada": "upetāḥ"}]
    assert lem["upeta"]["upasargas"] == ["upa"]
    # the root's artha hint is kept for the dhātu section
    assert lem["abhyāsa"]["root"] == "√as" and lem["abhyāsa"]["hints"]["arthas"] == ["kṣepaṇe"]


# ------------------------------------------------------------------ dhātu (hand-checked Dhātupāṭha facts)
def test_dhatu_bhaj_seva():
    d = E.dhatu_section({"stem": "bhaj", "root": "√bhaj", "upasargas": [], "verbal": True, "hints": {}})
    first = {(x["dp"], x["artha"]) for x in d["entries"]}
    assert ("01.1153", "sevāyām") in first          # भजँ सेवायाम्, bhvādi
    assert ("10.0259", "viśrāṇane") in first        # भजँ विश्राणने, curādi
    assert len(d["vrtti"]) <= 3 and all(len(v["text"]) <= 160 + 2 for v in d["vrtti"])


def test_dhatu_dvis_apritau_and_no_english():
    d = E.dhatu_section({"stem": "dviṣ", "root": "√dviṣ", "upasargas": [], "verbal": True, "hints": {}})
    assert [(x["dp"], x["artha"], x["gana"]) for x in d["entries"]] == [("02.0003", "aprītau", "2 adādi")]
    english = E.L.dhatu_lookup("dviṣ")["upstream"][0]["artha_english"]
    assert english and english not in json.dumps(d, ensure_ascii=False)
    assert "artha_english" not in json.dumps(d)


def test_dhatu_hint_selects_ganas():
    # abhyāsa is √as 'kṣepaṇe' (asu, divādi), not as 'bhuvi'
    d = E.dhatu_section({"stem": "abhyāsa", "root": "√as", "upasargas": ["abhi"], "verbal": False,
                         "hints": {"ganas": [], "arthas": ["kṣepaṇe"]}})
    assert [x["dp"] for x in d["entries"]] == ["04.0106"]


def test_dhatu_entry_naming_the_lemma_ranks_first():
    # udvega: the Mādhavīya entry of ओँविजीँ भयचलनयोः says प्रायेणायमुत्पूर्वः उद्विजते
    d = E.dhatu_section({"stem": "udvega", "root": "√vij", "upasargas": ["ud"], "verbal": False, "hints": {}})
    assert d["entries"][0]["dp"] in ("06.0009", "07.0023") and d["entries"][-1]["dp"] == "03.0013"
    assert any("utpūrvaḥ" in v["text"] for v in d["vrtti"])


# ------------------------------------------------------------------ precision of the library sections
def test_compound_membership():
    assert E.contains_member("madbhakta", "bhakta")
    assert E.contains_member("harṣāmarṣabhayodvega", "udvega")       # bhaya + udvega fused
    assert E.contains_member("arpitamanobuddhi", "manas")             # mano-
    assert not E.contains_member("vibhakta", "bhakta")                # vi- makes another word
    assert not E.contains_member("avibhakta", "bhakta")
    assert not E.contains_member("bhaktimat", "bhakti")               # -mat is an affix
    assert not E.contains_member("priyatama", "priya")
    assert not E.contains_member("prabhūta", "bhūta")


def test_kosha_text_keeps_glosses_drops_citations():
    vcp = next(e for e in E.L.kosha_lookup("कूटस्थ", ["vcp"]))["text"]
    t = E.kosha_text(vcp, 600)
    assert "kūṭo'yodhanavat niścalaṃ yathā tathā vā tiṣṭhati" in t    # 'yathā' inside a definition stays
    assert "ekarūpatayā sarvakālasthāyini" in t and "“" not in t


def test_clause_word_matching():
    toks = "priyaviyoge na śocati".split()
    assert E._word_hits(toks, "priyaḥ") == []                         # another word containing priya
    assert E._word_hits("āha kūṭasthamiti".split(), "kūṭastham") == [1]
    assert E._word_hits("parameśvaramupāsate cintayanti".split(), "upāsate") == [0]
    assert E._word_hits(["apriyam"], "priyaḥ") == []


def test_verse_quotation_is_not_a_gloss():
    vs = {E._sig(w) for w in "saṃtuṣṭaḥ satataṃ yogī yatātmā dṛḍhaniścayaḥ mayy arpitamanobuddhir yo "
                             "madbhaktaḥ sa me priyaḥ".split()}
    assert E.quotes_verse("… yo madbhaktaḥ sa me priyaḥ", vs)
    assert E.quotes_verse("āha, madbhakta iti", vs)
    assert not E.quotes_verse("madbhakto madbhajanaparo jñānavāniti yāvat", vs)


def test_clause_window_length_and_cut():
    clause = ("mayi viśva-rūpe parameśvara āveśya samādhāya mano ye bhaktāḥ santaḥ, māṃ sarva-yoge varāṇām "
              "adhīśvaraṃ sarvajñaṃ vimukta-rāgādi-kleśa-timira-dṛṣṭim, nitya-yuktā atītānantarādhyāyānta")
    w = E.clause_window(clause, "upāsate")
    assert w == ""                                                    # the word is not in this clause
    w = E.clause_window(clause, "mano")
    assert w.startswith("… samādhāya mano") and len(w) <= 160


# ------------------------------------------------------------------ the real chapter-12 cards
@needs_run
def test_bhakta_card(cards):
    c = cards["bhakta"]
    assert ("01.1153", "sevāyām") in {(d["dp"], d["artha"]) for d in c["dhatu"]["entries"]}
    assert [a["locus"] for a in c["amara"]] == ["Amara 2.8.48"]       # the only exact-headword group
    assert {"skd#24569", "vcp#36010"} <= {k["locus"] for k in c["kosha"]}
    assert not any("vibhakt" in n["text"] for n in c["nirukta"])      # the old page's substring hit
    loci = [e["locus"] for e in c["elsewhere"]] + c.get("elsewhere_more", [])
    assert {"4.3c", "9.34a", "18.65a"} <= set(loci)                   # bhakto, madbhakto
    assert not {"13.16a", "18.20c"} & set(loci)                       # vibhakta, avibhakta
    assert [o["locus"] for o in c["occurrences"]] == ["12.1", "12.14", "12.16", "12.20"]


@needs_run
def test_paryupas_card(cards, lemmas):
    c = cards["paryupās"]
    assert [p["locus"] for p in lemmas["paryupās"]["places"]] == ["12.1", "12.3", "12.20"]
    assert [d["dp"] for d in c["dhatu"]["entries"]] == ["02.0011"]     # आसँ उपवेशने, adādi
    assert any("pari--upa--upāsanasya prakarṣārthe" in k["text"] for k in c["kosha"])
    assert [e["locus"] for e in c["elsewhere"]] == ["4.25a", "9.22a"]
    assert any("samantād upāsate" in (g.get("clause") or "") for g in c["occurrences"][1]["glosses"])


@needs_run
def test_kutastha_manas_cetas(cards):
    assert [a["locus"] for a in cards["kūṭastha"]["amara"]] == ["Amara 3.1.73"]
    assert "vcp#14555" in {k["locus"] for k in cards["kūṭastha"]["kosha"]}
    assert [e["locus"] for e in cards["kūṭastha"]["elsewhere"]] == ["6.8a", "15.16c"]
    # citta, cetas, manas are one Amara group (1.4.31); each card shows it
    assert "Amara 1.4.31" in {a["locus"] for a in cards["manas"]["amara"]}
    assert "Amara 1.4.31" in {a["locus"] for a in cards["cetas"]["amara"]}
    manas_loci = [e["locus"] for e in cards["manas"]["elsewhere"]] + cards["manas"].get("elsewhere_more", [])
    assert "8.7c" in manas_loci                                       # mayy arpitamanobuddhir
    assert "Nighaṇṭu 3.9" in {n["locus"] for n in cards["cetas"]["nirukta"]}


@needs_run
def test_udvega_udvij(cards):
    assert [e["locus"] for e in cards["udvega"]["elsewhere"]] == ["17.15a"]   # anudvegakaraṃ
    assert [e["locus"] for e in cards["udvij"]["elsewhere"]] == ["5.20a"]     # nodvijet
    o1, o2 = cards["udvij"]["occurrences"]                                   # nodvijate twice in 12.15
    assert not all("same_as" in g for g in o2["glosses"])
    assert any("lokān" in (g.get("clause") or "") for g in o2["glosses"])


@needs_run
def test_card_shape_ids_lengths_and_no_english(cards):
    stop = {"the", "and", "of", "to", "is", "in", "for", "with", "omits", "adds", "worship", "serve"}
    for name, c in cards.items():
        all_ids = ids(c)
        assert len(all_ids) == len(set(all_ids)), name
        for x in all_ids:
            assert re.fullmatch(r"(D\d+(\.v\d+)?|A\d+|K\d+|N\d+|E\d+|O\d+(\.g\d+)?)", x), x
        for o in c["occurrences"]:
            for g in o["glosses"]:
                assert ("clause" in g) != ("same_as" in g)
                assert len(g.get("clause", "")) <= 160 + 2
        assert all(len(k["text"]) <= 600 + 2 for k in c["kosha"])
        words = re.findall(r"[A-Za-zāīūṛṝḷḹṅñṭḍṇśṣṃḥ]+", " ".join(
            x.get("text", "") for s in ("amara", "kosha", "nirukta") for x in c[s]) + " ".join(
            g.get("clause", "") for o in c["occurrences"] for g in o["glosses"]))
        assert not stop & {w.lower() for w in words if w.isascii()}, name


@needs_run
def test_chapter_sizes(lemmas):
    sizes = sorted(E.card_bytes(E.sanskrit_card(e)) for e in lemmas.values())
    assert sizes[len(sizes) // 2] <= E.BUDGET

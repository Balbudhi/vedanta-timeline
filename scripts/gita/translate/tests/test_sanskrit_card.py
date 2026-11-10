"""The M1–M5 Sanskrit card (sanskrit_card.py), the affix-meaning table, the grammar-first parse input
(compile.construe_input) and the step-1 checks (pipeline.meaning_errors, accepted_construals).
Facts are read from the sources, not from the code under test."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import compile as C  # noqa: E402
import evidence as E  # noqa: E402
import pipeline as P  # noqa: E402
import sanskrit_card as S  # noqa: E402

PACKETS = E.PACKETS
HAVE_DATA = (PACKETS / "analyses.sqlite").exists()
ASHTADHYAYI = E.PRAKRIYA / "sources/primary/panini/ashtadhyayi/ashtadhyayi_collated_clean.txt"


class AffixTable(unittest.TestCase):
    def test_every_citation_is_the_cited_sutra(self):
        """Each row's `check` token occurs in the clean text of the sūtra it cites."""
        t = json.loads((HERE / "affix_meanings.json").read_text(encoding="utf-8"))
        for sec, rows in t.items():
            if sec == "about":
                continue
            for name, cits in rows.items():
                self.assertTrue(cits, f"{sec}.{name} has no citation")
                for c in cits:
                    text = E.L.sutra_lookup(c["sutra"])["ashtadhyayi_text"]
                    self.assertIn(c["check"], text, f"{sec}.{name}: {c['sutra']} is {text!r}")

    def test_known_meanings(self):
        """kta is past (3.2.102 niṣṭhā); laṭ present (3.2.123); dvitīyā karman (2.3.2)."""
        a = {"krt": {"name": "kta"}, "lakara": None, "vibhakti": "prathamā"}
        got = {x["affix"]: [s["sutra"] for s in x["sutras"]] for x in S.affix_meanings(a, None)}
        self.assertIn("3.2.102", got["kta"])
        self.assertIn("2.3.46", got["prathamā"])
        got = {x["affix"]: [s["sutra"] for s in x["sutras"]] for x in S.affix_meanings(None, "laṭ prathama bahuvacana parasmaipada")}
        self.assertEqual(got["laṭ"], ["3.2.123"])
        self.assertIn("kartari", got)
        got = {x["affix"] for x in S.affix_meanings(None, "dvitīyā ekavacana napuṃsakaliṅga")}
        self.assertEqual(got, {"dvitīyā"})

    def test_unknown_affix_is_visible(self):
        got = S.affix_meanings({"krt": {"name": "nosuch"}}, None)
        self.assertEqual(got, [{"affix": "nosuch", "kind": "kṛt", "sutras": []}])


class Derivation(unittest.TestCase):
    def test_pratyaya_steps_only(self):
        d = {"matches": True, "form_derived": "bhaktaḥ", "steps": [
            {"sutra": "1.3.1", "result": "bhajam̐"}, {"sutra": "3.2.102", "result": "bhaj + kta"},
            {"sutra": "1.3.8", "result": "bhaj + ta"}, {"sutra": "4.1.2", "result": "bhaj + ta + su"},
            {"sutra": "4.1.2", "result": "bhaj + ta + su"}]}
        self.assertEqual(S._derivation(d), ["3.2.102: bhaj + kta", "4.1.2: bhaj + ta + su", "→ bhaktaḥ"])

    def test_failed_derivation_is_not_shown(self):
        self.assertEqual(S._derivation({"matches": False, "steps": [{"sutra": "3.2.102", "result": "x"}]}), [])


@unittest.skipUnless(HAVE_DATA, "pipeline packets not present")
class ParseInput(unittest.TestCase):
    def test_every_token_has_candidates(self):
        """Candidates are found through the pada forms (bori_token), not the sandhi surface:
        12.2 'parayopetās' is parayā + upetāḥ, 'mano' is manaḥ."""
        inp = C.construe_input("12.2")
        by = {w["form"]: w for w in inp["words"]}
        self.assertEqual(by["parayopetās"]["padas"], ["parayā", "upetāḥ"])
        self.assertTrue({c["pada"] for c in by["parayopetās"]["candidates"]} == {"parayā", "upetāḥ"})
        self.assertTrue(by["mano"]["candidates"])
        self.assertTrue(all(w["candidates"] for w in inp["words"]))

    def test_grammar_first_commentaries_last(self):
        inp = C.construe_input("15.1")
        self.assertEqual(list(inp)[-1], "commentaries_last")
        self.assertNotIn("commentaries", inp)
        for w in inp["words"]:
            for c in w["candidates"]:
                self.assertNotIn("agrees_with_gloss", c)
        self.assertTrue(any(c.get("derivation") for w in inp["words"] for c in w["candidates"]))


@unittest.skipUnless(HAVE_DATA and (P.RUNS / "ch15-heldout/construe").is_dir(), "ch15 run not present")
class Card(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cons, _ = P.accepted_construals("ch15-heldout")
        cls.pos, cls.ents = P.lemma_map(cons)
        cls.words = {(c["locus"], w["i"]): w for c in cons for w in c["words"]}

    def card(self, locus, i):
        lemma = self.pos[(locus, i)]["word"] or self.words[(locus, i)]["stem"]
        return self.ents[lemma], S.word_card(self.ents[lemma], locus, self.words[(locus, i)])

    def test_order_and_sources(self):
        e, c = self.card("15.1", 2)  # aśvatthaṃ
        self.assertEqual([k for k in c if k.startswith("M")],
                         ["M1_decode", "M2_morphemes", "M3_lexical_texts", "M4_usage", "M5_commentaries_last"])
        self.assertEqual(set(c["sources"]), set(S.SOURCES))
        self.assertTrue(c["sources"]["Mahābhārata usage"].startswith(("shown", "no whole-word", "not in the library",
                                                                     "paradigm not generated")))
        self.assertEqual(S.audit(e, c), [])

    def test_every_dhatuvrtti_that_treats_the_root_is_heard(self):
        """√sthā is in the Mādhavīya, Kṣīrataraṅgiṇī and Dhātupradīpa."""
        _, c = self.card("15.1", 2)
        works = {v["work"].split(" ")[0] for v in c["M2_morphemes"]["dhatuvrtti"]}
        self.assertTrue({"Mādhavīya", "Kṣīrataraṅgiṇī", "Dhātupradīpa"} <= works, works)

    def test_lexical_texts_and_no_english_dictionary(self):
        _, c = self.card("15.1", 2)
        works = {x["work"] for sec in c["M3_lexical_texts"].values() for x in sec}
        self.assertTrue({"Śabdakalpadruma", "Vācaspatya"} <= works)
        text = json.dumps(c, ensure_ascii=False)
        for forbidden in ("mw.json", "ap90", "pw.json", "site_renderings", "english"):
            self.assertNotIn(forbidden, text)

    def test_commentaries_are_this_verse_only(self):
        _, c = self.card("15.1", 2)
        self.assertTrue(c["M5_commentaries_last"])
        self.assertTrue(all("aśvattha" in x for x in c["M5_commentaries_last"]))

    def test_manual_analysis_resolved_to_packet_derivation(self):
        _, c = self.card("15.1", 2)
        self.assertIn("4.1.2: aśvattha + am", c["M1_decode"]["derivation"])

    def test_audit_catches_a_dropped_kosha(self):
        e, c = self.card("15.1", 2)
        c = json.loads(json.dumps(c))
        c["M3_lexical_texts"]["koshas"] = []
        self.assertTrue(any("Vaijayantī" in x for x in S.audit(e, c)))


class MeaningChecks(unittest.TestCase):
    CARD = {"verses": [{"locus": "1.1", "words": [
        {"i": 0, "form": "x", "class": "content", "sanskrit": {"M2_morphemes": {"root": ["ṣṭhā: gatinivṛttau"]},
                                                              "M3_lexical_texts": {}}},
        {"i": 1, "form": "ca", "class": "particle"}]}]}

    def test_missing_literal(self):
        self.assertEqual(P.meaning_errors({"words": []}, self.CARD), ["1.1 word 0 (x): no literal meaning"])

    def test_commentary_only_grounds(self):
        m = {"words": [{"locus": "1.1", "i": 0, "literal": "standing", "grounds": ["Śaṅkara"]}]}
        self.assertTrue(P.meaning_errors(m, self.CARD))
        m["words"][0]["grounds"] = ["DP 01.1077 gatinivṛttau", "Śaṅkara"]
        self.assertEqual(P.meaning_errors(m, self.CARD), [])

    def test_unresolved_is_allowed(self):
        m = {"words": [{"locus": "1.1", "i": 0, "literal": "unresolved"}]}
        self.assertEqual(P.meaning_errors(m, self.CARD), [])

    def test_meaning_view_is_sanskrit_only(self):
        card = {"verses": [{"locus": "1.1", "words": [{"i": 0, "standing": [{"english": ["x"]}], "english_case": "'from'",
                                                       "grammar": "g"}]}]}
        self.assertEqual(P.meaning_view(card)["verses"][0]["words"][0], {"i": 0, "grammar": "g"})


if __name__ == "__main__":
    unittest.main()

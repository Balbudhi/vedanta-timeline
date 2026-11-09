"""Rules of pipeline.check_unit and helpers (README.md, "Code checks"), on synthetic fixtures."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pipeline as P  # noqa: E402


def card(words, forks=()):
    return {"unit": ["9.99"], "verses": [{"locus": "9.99", "iast": "", "forks": list(forks), "referents": [], "words": words}]}


def W(i, form, cls="content", **kw):
    return {"i": i, "form": form, "lemma": form, "class": cls, **kw}


def out(line, words, alt=None):
    return {"lines": {"9.99": line}, "alternative": alt,
            "words": [{"locus": "9.99", "i": i, "english": e, **kw} for i, e, kw in words]}


class Helpers(unittest.TestCase):
    def test_renders_forms_of_same_word(self):
        self.assertTrue(P.renders("relinquish the fruit", "relinquishment"))
        self.assertTrue(P.renders("acts' fruit", "act"))
        self.assertFalse(P.renders("freed", "loosed"))
        self.assertFalse(P.renders("rest", "restless"))

    def test_keeps_inflected_sanskrit(self):
        self.assertTrue(P.keeps("the bhaktas", "bhakta"))
        self.assertTrue(P.keeps("is kutastha", "kūṭastha"))
        self.assertFalse(P.keeps("the devotees", "bhakta"))

    def test_term_rows(self):
        self.assertEqual([r["keep"] for r in P.term_rows("yogin")], ["yogin"])      # named by iast_forms
        self.assertTrue(any("foul" in r["english"] for r in P.term_rows("aśubha")))
        self.assertEqual(len(P.term_rows("karman")), 2)                              # both senses offered
        self.assertEqual(P.term_rows("zzzz"), [])


class CheckUnit(unittest.TestCase):
    base = [W(0, "priyaḥ"), W(1, "ca", "particle")]

    def test_clean(self):
        self.assertEqual(P.check_unit(out("and dear", [(0, "dear", {}), (1, "and", {})]), card(self.base)), [])

    def test_addition(self):
        e = P.check_unit(out("and dear in worship", [(0, "dear", {}), (1, "and", {})]), card(self.base))
        self.assertTrue(any("not assigned" in x for x in e), e)

    def test_drop(self):
        e = P.check_unit(out("dear", [(0, "dear", {})]), card(self.base))
        self.assertTrue(any("not rendered" in x for x in e), e)

    def test_explanation_too_long(self):
        e = P.check_unit(out("sit wholly intent in worship near you and",
                             [(0, "sit wholly intent in worship near you", {}), (1, "and", {})]), card(self.base))
        self.assertTrue(any("explanation" in x for x in e), e)

    def test_standing_translate_and_forbidden(self):
        rows = [{"term": "t.a", "policy": "translate", "english": ["attend upon"], "keep": None, "forbidden": ["worship"]}]
        c = card([W(0, "upāsate", standing=rows)])
        self.assertEqual(P.check_unit(out("attend upon", [(0, "attend upon", {})]), c), [])
        e = P.check_unit(out("worship", [(0, "worship", {})]), c)
        self.assertTrue(any("forbidden: worship" in x and "follows none" in x for x in e), e)

    def test_standing_preserve(self):
        rows = [{"term": "y.s", "policy": "preserve", "english": [], "keep": "yogin", "forbidden": ["discipline"]}]
        c = card([W(0, "yogī", standing=rows)])
        self.assertEqual(P.check_unit(out("a yogin", [(0, "a yogin", {})]), c), [])
        e = P.check_unit(out("a disciplined person", [(0, "a disciplined person", {})]), c)
        self.assertTrue(any("forbidden" in x for x in e), e)

    def test_rows_are_alternative_senses(self):
        rows = [{"term": "d.sorrow", "policy": "translate", "english": ["sorrow"], "keep": None, "forbidden": ["pain"], "member": "duḥkha"},
                {"term": "d.pain", "policy": "translate", "english": ["pain"], "keep": None, "forbidden": ["sorrow"], "member": "duḥkha"}]
        comp = {"type": "dvandva", "members": [{"stem": "sukha", "class": "content"}, {"stem": "duḥkha", "class": "content"}]}
        c = card([W(0, "sukhaduḥkhe", compound=comp, standing=rows)])
        good = out("pleasure and pain", [(0, "pleasure and pain", {"parts": [{"stem": "sukha", "english": "pleasure"}, {"stem": "duḥkha", "english": "pain"}]})])
        self.assertEqual(P.check_unit(good, c), [])
        bad = out("pleasure and misery", [(0, "pleasure and misery", {"parts": [{"stem": "sukha", "english": "pleasure"}, {"stem": "duḥkha", "english": "misery"}]})])
        self.assertTrue(any("follows none" in x for x in P.check_unit(bad, c)))

    def test_ellipsis_repeat_is_not_addition(self):
        c = card([W(0, "upāsate"), W(1, "ca", "particle")])
        o = out("those who attend upon you and those who attend upon it", [(0, "attend upon", {}), (1, "and", {})])
        self.assertEqual(P.check_unit(o, c), [])

    def test_case_rule(self):
        self.assertIn("from", P.case_rule("tṛtīyā bahuvacana", "mukta"))
        self.assertIn("than", P.case_rule("pañcamī ekavacana", "śreyas"))
        self.assertIn("by", P.case_rule("ṣaṣṭhī ekavacana", "mata"))
        self.assertIsNone(P.case_rule("tṛtīyā ekavacana", "yukta"))

    def test_fixed(self):
        c = card([W(0, "śatruḥ", FIXED="foe")])
        self.assertEqual(P.check_unit(out("foes", [(0, "foes", {})]), c), [])
        self.assertTrue(P.check_unit(out("enemy", [(0, "enemy", {})]), c))

    def test_loss_needs_reason(self):
        c = card([W(0, "śuciḥ")])
        e = P.check_unit(out("pure", [(0, "pure", {"carried": False, "lost": "glow", "step": "existing"})]), c)
        self.assertTrue(any("owner's order" in x for x in e), e)
        e = P.check_unit(out("pure", [(0, "pure", {"carried": False, "lost": "glow", "step": "existing", "why": "x"})]), c)
        self.assertEqual(e, [])

    def test_compound_members(self):
        comp = {"type": "ṣaṣṭhī-tatpuruṣa", "analysis": "", "members": [{"stem": "asmad", "class": "pronoun"},
                                                                          {"stem": "bhakta", "class": "content"}]}
        c = card([W(0, "madbhaktaḥ", compound=comp)])
        ok = out("my bhakta", [(0, "my bhakta", {"parts": [{"stem": "asmad", "english": "my"}, {"stem": "bhakta", "english": "bhakta"}]})])
        self.assertEqual(P.check_unit(ok, c), [])
        bad = out("a bhakta", [(0, "a bhakta", {"parts": [{"stem": "bhakta", "english": "bhakta"}]})])
        self.assertTrue(any("asmad" in x for x in P.check_unit(bad, c)))

    def test_member_fixed_rendering(self):
        comp = {"type": "dvandva", "members": [{"stem": "sukha", "class": "content"}, {"stem": "duḥkha", "class": "content", "FIXED": "pain"}]}
        c = card([W(0, "sukhaduḥkhe", compound=comp)])
        ok = out("pleasure and pain", [(0, "pleasure and pain", {"parts": [{"stem": "sukha", "english": "pleasure"}, {"stem": "duḥkha", "english": "pain"}]})])
        self.assertEqual(P.check_unit(ok, c), [])
        bad = out("pleasure and sorrow", [(0, "pleasure and sorrow", {"parts": [{"stem": "sukha", "english": "pleasure"}, {"stem": "duḥkha", "english": "sorrow"}]})])
        self.assertTrue(any("fixed rendering" in x for x in P.check_unit(bad, c)))

    def test_second_line_needs_fork(self):
        alt = {"fork": "x", "lines": {"9.99": "dear and"}}
        e = P.check_unit(out("and dear", [(0, "dear", {}), (1, "and", {})], alt), card(self.base))
        self.assertTrue(any("fork" in x for x in e), e)


class Trace(unittest.TestCase):
    def test_commentary_word_is_untraceable(self):
        c = card([W(0, "oṣadhīḥ", literal="plants, herbs", candidates=[{"word": "plants"}, {"word": "herbs"}])])
        self.assertEqual(P.check_unit(out("plants", [(0, "plants", {})]), c), [])
        e = P.check_unit(out("monocarpic plants", [(0, "monocarpic plants", {})]), c)
        self.assertTrue(any("monocarpic" in x for x in e), e)

    def test_seed_can_be_challenged(self):
        rows = [{"term": "seed-puruṣa.seed", "policy": "preserve", "english": [], "keep": "puruṣa", "forbidden": [], "seed": True}]
        c = card([W(0, "puruṣaḥ", standing=rows, literal="person, the one dwelling in the body")])
        self.assertTrue(P.check_unit(out("person", [(0, "person", {})]), c))
        self.assertEqual(P.check_unit(out("person", [(0, "person", {"challenge": "15.18 pun needs English"})]), c), [])


class LineRules(unittest.TestCase):
    def errs(self, line, iast=""):
        c = card([W(0, "x")]); c["verses"][0]["iast"] = iast
        return P.line_errors({"lines": {"9.99": line}, "words": []}, c)

    def test_question_needs_interrogative(self):
        self.assertTrue(self.errs("you are not able?", "na śaknoṣi"))
        self.assertEqual(self.errs("which of them are best?", "teṣāṃ ke yogavittamāḥ"), [])

    def test_one_dash(self):
        self.assertTrue(self.errs("a — b — c"))
        self.assertEqual(self.errs("a — b, c —"), [])

    def test_of_chain(self):
        self.assertTrue(self.errs("the relinquishment of the fruit of all acts of men"))
        self.assertEqual(self.errs("the relinquishment of action's fruit"), [])

    def test_hybrid_and_whatsoever(self):
        self.assertTrue(self.errs("the ocean of death-saṃsāra"))
        self.assertTrue(self.errs("content with whatsoever"))
        self.assertEqual(self.errs("content with anything whatsoever"), [])

    def test_real_words(self):
        self.assertTrue(P.attested("upbearer"))
        self.assertFalse(P.attested("blorfishness"))


class Consistency(unittest.TestCase):
    def test_conflicts_by_stem(self):
        by = {"bhakta": [{"english": "bhakta"}, {"english": "bhaktas"}], "śatru": [{"english": "foe"}, {"english": "enemy"}]}
        self.assertEqual(list(P.conflicts(by)), ["śatru"])

    def test_case_prepositions_are_not_a_different_rendering(self):
        self.assertTrue(P.same("than practice", "practice"))
        self.assertFalse(P.same("peepul", "peepal tree"))

    def test_same_root_may_share_english(self):
        by = {"śak": [{"english": "able", "root": "√śak"}], "śakta": [{"english": "able", "root": "√śak"}]}
        self.assertEqual(P.conflicts(by), {})

    def test_compound_member_is_checked(self):
        rec = {"unit": ["9.99"], "output": {"lines": {"9.99": "x"}, "words": [
            {"locus": "9.99", "i": 0, "english": "pleasure and misery", "parts": [{"stem": "sukha", "english": "pleasure"}, {"stem": "duḥkha", "english": "misery"}]},
            {"locus": "9.99", "i": 1, "english": "pain"}]},
            "card": card([W(0, "sukhaduḥkha", compound={"type": "dvandva", "members": [{"stem": "sukha", "class": "content"}, {"stem": "duḥkha", "class": "content"}]}),
                          W(1, "duḥkha")])}
        self.assertIn("duḥkha", P.conflicts(P.renderings([rec])))

    def test_member_and_compound_decided_together(self):
        by = {"veda": [{"english": "the Veda", "locus": "1"}, {"english": "Vedic scripture", "locus": "2", "of": "vedavid"}],
              "vedavid": [{"english": "knower of the Veda", "locus": "2"}, {"english": "Veda-knower", "locus": "3"}]}
        self.assertEqual(list(P.conflicts(by)), ["veda + vedavid"])

    def test_two_words_one_english(self):
        by = {"loka": [{"english": "world"}], "jagat": [{"english": "the world"}], "śatru": [{"english": "foe"}]}
        self.assertEqual(list(P.conflicts(by)), ["jagat + loka"])


if __name__ == "__main__":
    unittest.main()

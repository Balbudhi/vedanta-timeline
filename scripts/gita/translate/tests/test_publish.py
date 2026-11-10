"""publish.py: a pipeline run → the chapter builder's input, on synthetic run records.

Expected values are written from the builder's contract (build_gita_chapter_reader.py check_verse,
check_card, check_forks, check_meaning; standard §3.1–§3.2, §6.5), not from publish.py's output."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import publish as P  # noqa: E402

sys.path.insert(0, str(P.ROOT / "scripts"))
import build_gita_chapter_reader as B  # noqa: E402

CH = 99


def verse_packet(v, iast, deva):
    return {"locus": f"{CH}.{v}", "speaker": "krishna", "meter": {"name": "anuṣṭubh", "syllables_per_line": [16]},
            "iast": iast, "devanagari": deva}


PACKETS = [verse_packet(1, "yogī na śocati |", "योगी न शोचति ।"),
           verse_packet(2, "sa hṛṣyati na dveṣṭi na ||", "स हृष्यति न द्वेष्टि न ॥"),
           verse_packet(3, "tat ||", "तत् ॥")]

YOGA_ROWS = [{"term": "yoga.system", "policy": "preserve", "english": [], "keep": "yogin", "forbidden": ["union"]},
             {"term": "yoga.method", "policy": "preserve", "english": [], "keep": "yoga", "forbidden": []},
             {"term": "yoga.seed", "policy": "translate", "english": ["yogin"], "seed": True}]


def unit_1_2(**over):
    """Unit 99.1–99.2: a discontinuous rendering, a term row with two senses, twin particles,
    a second line, meaning records with here/readings/grounds."""
    card = {"unit": [f"{CH}.1", f"{CH}.2"], "verses": [
        {"locus": f"{CH}.1", "iast": PACKETS[0]["iast"], "referents": [],
         "forks": [{"kind": "relation", "words": [1, 2], "readings": [], "basis": "scope of na"}],
         "words": [
             {"i": 0, "form": "yogī", "lemma": "yogin", "class": "content", "root": "√yuj", "upasargas": None,
              "grammar": "prathamā ekavacana puṃliṅga", "depends_on": "śocati", "relation": "kartṛ", "standing": YOGA_ROWS},
             {"i": 1, "form": "na", "lemma": "na", "class": "particle", "root": None, "upasargas": None,
              "grammar": "niṣedha", "depends_on": "śocati", "relation": "pratiṣedha"},
             {"i": 2, "form": "śocati", "lemma": "śuc", "class": "content", "root": "√śuc", "upasargas": None,
              "grammar": "laṭ kartari prathamapuruṣa ekavacana", "depends_on": None, "relation": "mukhyakriyā",
              "candidates": [{"word": "grieve", "found_by": "retrieved", "attested": True,
                              "entries": ["oewn2025 v: feel grief; be sad"]}, "mourn"]}]},
        {"locus": f"{CH}.2", "iast": PACKETS[1]["iast"], "referents": [], "forks": [],
         "words": [
             {"i": 0, "form": "sa", "lemma": "tad", "class": "pronoun", "root": None, "grammar": "prathamā", "depends_on": None, "relation": "kartṛ"},
             {"i": 1, "form": "hṛṣyati", "lemma": "hṛṣ", "class": "content", "root": "√hṛṣ", "grammar": "laṭ", "depends_on": None, "relation": "kriyā",
              "candidates": []},
             {"i": 2, "form": "na", "lemma": "na", "class": "particle", "root": None, "grammar": "niṣedha", "depends_on": None, "relation": "pratiṣedha"},
             {"i": 3, "form": "dveṣṭi", "lemma": "dviṣ", "class": "content", "root": "√dviṣ", "grammar": "laṭ", "depends_on": None, "relation": "kriyā",
              "candidates": []},
             {"i": 4, "form": "na", "lemma": "na", "class": "particle", "root": None, "grammar": "niṣedha", "depends_on": None, "relation": "pratiṣedha"}]}]}
    meaning = {"words": [
        {"locus": f"{CH}.1", "i": 0, "literal": "One who has yoga.", "grounds": ["Aṣṭādhyāyī 5.2.115"], "here": None,
         "image": "yoked", "readings": None},
        {"locus": f"{CH}.1", "i": 2, "literal": "Grieves; laments.", "grounds": [], "here": "Śaṅkara: he does not lament.",
         "image": None, "readings": [{"sense": "does not grieve at loss", "who": "Rāmānuja"}]}]}
    output = {"lines": {f"{CH}.1": "The yogin does not grieve.", f"{CH}.2": "He rejoices not and hates not."},
              "alternative": {"fork": "na negates the whole clause or only the verb.",
                              "lines": {f"{CH}.1": "The yogin grieves not."},
                              "words": [{"locus": f"{CH}.1", "i": 2, "english": "grieves"}]},
              "words": [
                  {"locus": f"{CH}.1", "i": 0, "english": "The yogin", "parts": None, "kind": "e", "found_by": "standing",
                   "carried": True, "lost": None, "why": "Kept in Sanskrit."},
                  {"locus": f"{CH}.1", "i": 1, "english": "not", "parts": None, "kind": "a", "found_by": "grammar",
                   "carried": True, "lost": None, "why": ""},
                  {"locus": f"{CH}.1", "i": 2, "english": "does … grieve", "parts": None, "kind": "a", "found_by": "retrieved",
                   "carried": True, "lost": None, "why": "'Grieve' is the plain word; 'mourn' adds a rite."},
                  {"locus": f"{CH}.2", "i": 0, "english": "He", "kind": "a", "found_by": "grammar"},
                  {"locus": f"{CH}.2", "i": 1, "english": "rejoices", "kind": "a", "found_by": "remembered"},
                  {"locus": f"{CH}.2", "i": 2, "english": "not", "kind": "a", "found_by": "grammar"},
                  {"locus": f"{CH}.2", "i": 3, "english": "hates", "kind": "a", "found_by": "remembered"},
                  {"locus": f"{CH}.2", "i": 4, "english": "not", "kind": "a", "found_by": "grammar"}]}
    rec = {"unit": [f"{CH}.1", f"{CH}.2"], "calls": [], "rounds": [{"taste": [{"severity": "S3", "says": "flat"}]}],
           "meaning": meaning, "card": card, "output": output, "code_errors": [], "review": []}
    rec.update(over)
    return rec


def unit_3(**over):
    rec = {"unit": [f"{CH}.3"], "calls": [], "rounds": [{}], "meaning": {"words": []},
           "card": {"unit": [f"{CH}.3"], "verses": [{"locus": f"{CH}.3", "iast": "tat ||", "referents": [], "forks": [], "words": [
               {"i": 0, "form": "tat", "lemma": "tad", "class": "pronoun", "root": None, "grammar": "prathamā", "depends_on": None,
                "relation": "kartṛ"}]}]},
           "output": {"lines": {f"{CH}.3": "That."}, "alternative": None,
                      "words": [{"locus": f"{CH}.3", "i": 0, "english": "That", "kind": "a", "found_by": "grammar"}]},
           "code_errors": [], "review": []}
    rec.update(over)
    return rec


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.runs, self.packets = self.base / "runs", self.base / "packets"
        (self.runs / "R/translate").mkdir(parents=True)
        self.packets.mkdir()
        for p in PACKETS:
            (self.packets / f"{p['locus']}.json").write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
        self.put("99.1-99.2.json", unit_1_2())
        self.put("99.3.json", unit_3())
        (self.runs / "R/translate/_summary_translate.json").write_text("{}", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, name, rec):
        (self.runs / "R/translate" / name).write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")

    def main(self, *extra):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = P.main(["--run", "R", "--chapter", str(CH), "--out", str(self.base / "out"),
                           "--runs", str(self.runs), "--packets", str(self.packets), *extra])
        return code, err.getvalue()

    def verse(self, conv, loc):
        return next(v for v in conv.shard["verses"] if v["locus"] == loc)


class Conversion(Fixture):
    def test_verse_maps_to_builder_fields(self):
        conv = P.convert("R", CH, self.runs, self.packets)
        v = self.verse(conv, "99.1")
        self.assertEqual(v["english"], "{0:The yogin} {2:does} {1:not} {2:grieve}.")
        self.assertEqual((v["iast"], v["devanagari"], v["speaker"], v["meter"]),
                         ("yogī na śocati |", "योगी न शोचति ।", "krishna", "anuṣṭubh"))
        self.assertEqual(v["deviations"], [])
        self.assertNotIn("sense", v)          # the run has none: never written
        self.assertNotIn("grammar", v)
        w0, w2 = v["words"][0], v["words"][2]
        self.assertEqual({k: w0[k] for k in ("i", "iast", "deva", "gloss", "stem", "root", "morph", "karaka", "word_class", "term")},
                         {"i": 0, "iast": "yogī", "deva": "योगी", "gloss": "The yogin", "stem": "yogin", "root": "√yuj",
                          "morph": "prathamā ekavacana puṃliṅga", "karaka": "kartṛ → śocati", "word_class": "content",
                          "term": {"lemma": "yoga", "sense": "system"}})
        self.assertEqual(w0["terms"], [{"lemma": "yoga", "sense": "system"}])   # seed row and the non-admitting sense dropped
        self.assertNotIn("wording", w0)       # a preserved term needs none
        self.assertEqual(w0["meaning"], {"lines": [{"cat": "synthesis", "text": "One who has yoga.", "who": "Aṣṭādhyāyī 5.2.115"}],
                                         "image": "yoked", "rendering": "The yogin", "why": "Kept in Sanskrit."})
        self.assertEqual(w2["meaning"]["lines"], [
            {"cat": "commentator", "text": "Śaṅkara: he does not lament.", "who": "commentators on 99.1"},
            {"cat": "commentator", "text": "does not grieve at loss", "who": "Rāmānuja"},
            {"cat": "synthesis", "text": "Grieves; laments."}])
        self.assertEqual(w2["wording"], {"sense_description": "Grieves; laments.",
                                         "candidates": [{"word": "grieve", "source": "oewn2025", "definition": "feel grief; be sad",
                                                         "found_by": "retrieved"},
                                                        {"word": "mourn"}],
                                         "chosen": "does … grieve", "why": "'Grieve' is the plain word; 'mourn' adds a rite."})
        self.assertEqual(w2["pipeline"]["found_by"], "retrieved")
        for w in v["words"]:
            for k in ("affix", "parts", "evidence", "rootGloss", "root_id"):
                self.assertNotIn(k, w)        # absent from the run: never filled

    def test_second_line_is_an_open_fork(self):
        v = self.verse(P.convert("R", CH, self.runs, self.packets), "99.1")
        self.assertEqual(v["forks"], [{
            "at": "śocati", "words": [2],
            "construals": [{"reading": "The yogin does not grieve.", "grammar_basis": "na negates the whole clause or only the verb."},
                           {"reading": "The yogin grieves not.", "grammar_basis": "na negates the whole clause or only the verb."}],
            "followed": 0, "reason_class": 5, "reason": "na negates the whole clause or only the verb.", "open": True,
            "display": "The yogin grieves not."}])
        self.assertEqual(self.verse(P.convert("R", CH, self.runs, self.packets), "99.2")["forks"], [])

    def test_old_records_without_alternative_words_use_card_forks(self):
        rec = unit_1_2()
        del rec["output"]["alternative"]["words"]
        self.put("99.1-99.2.json", rec)
        v = self.verse(P.convert("R", CH, self.runs, self.packets), "99.1")
        self.assertEqual(v["forks"][0]["words"], [1, 2])

    def test_twins_take_places_in_sanskrit_order(self):
        v = self.verse(P.convert("R", CH, self.runs, self.packets), "99.2")
        self.assertEqual(v["english"], "{0:He} {1:rejoices} {2:not} and {3:hates} {4:not}.")
        self.assertEqual(v["pipeline"]["placed_by_sanskrit_order"], [2, 4])

    def test_builder_accepts_the_structures(self):
        """The builder's own checks on what publish.py writes: slots, fork, meaning lines."""
        conv = P.convert("R", CH, self.runs, self.packets)
        ctx = B.Ctx(chapter=CH, root=P.ROOT, chapter_dir=self.base)
        for v in conv.shard["verses"]:
            n = len(v["words"])
            self.assertTrue(all(0 <= i < n for i in B.slot_map(v["english"])))
            self.assertNotIn("{", B.SLOT_RE.sub("", v["english"]))
            B.check_forks(ctx, v["locus"], v, n)
            smap = B.slot_map(v["english"])
            for w in v["words"]:
                B.check_meaning(ctx, w["iast"], w, " ".join(smap.get(w["i"], [])), False, v["english"])
        self.assertEqual(ctx.report.errors, [])

    def test_packet(self):
        conv = P.convert("R", CH, self.runs, self.packets)
        self.assertEqual(conv.packet["verse_count"], 3)
        self.assertEqual(conv.packet["verses"][0], {"locus": "99.1", "speaker": "krishna", "meter": "anuṣṭubh",
                                                    "iast": "yogī na śocati |", "devanagari": "योगी न शोचति ।"})

    def test_missing_builder_fields_are_listed(self):
        conv = P.convert("R", CH, self.runs, self.packets)
        r = conv.unfinished["99.1"]
        for want in ("verse sense absent", "verse grammar absent", "fewer than 5 secondaries_consulted (the pipeline consults none)",
                     "[0] yogī: card affix absent", "[2] śocati: root without gaṇa and pada", "[2] śocati: no evidence for the grammatical claim"):
            self.assertIn(want, r)
        self.assertIn("[1] hṛṣyati: wording candidates absent", conv.unfinished["99.2"])
        self.assertTrue(any("term-policy hash" in x for x in conv.unfinished["chapter"]))
        self.assertTrue(any("review record has no `complete`" in x for x in conv.unfinished["chapter"]))

    def test_builder_gaps_empty_for_a_complete_verse(self):
        w = {"i": 0, "iast": "na", "deva": "न", "gloss": "not", "parts": [{"form": "na", "gloss": "not"}],
             "affix": "avyaya", "morph": "indeclinable", "word_class": "particle"}
        v = {"sense": "s", "english": "{0:not}", "words": [w], "grammar": {"karakaSummary": "k"}, "forks": [],
             "deviations": [], "secondaries_consulted": list("abcde")}
        self.assertEqual(P.builder_gaps(v), [])
        self.assertEqual(P.builder_gaps({**v, "words": [{**w, "parts": [{"form": "na", "gloss": ""}]}]}),
                         ["[0] na: a parts[] piece lacks form or gloss"])


class Slots(unittest.TestCase):
    def test_joint_slot_for_one_shared_rendering(self):
        r = P.place_slots("with anything at all", [(3, "with anything", ("kim", "x")), (4, "with anything", ("yad", "y"))])
        self.assertEqual(r.english, "{3,4:with anything} at all")

    def test_different_words_same_english_twice_is_ambiguous(self):
        r = P.place_slots("this and this", [(0, "this", ("idam", "x")), (1, "this", ("etad", "x"))])
        self.assertEqual((r.english, r.ambiguous), ("this and this", [0, 1]))

    def test_slots_do_not_nest(self):
        r = P.place_slots("into me, by me, me", [(0, "into me", ("a",)), (1, "by me", ("b",)), (2, "me", ("c",))])
        self.assertEqual((r.english, r.ambiguous), ("{0:into me}, {1:by me}, {2:me}", []))

    def test_not_found_is_unplaced(self):
        r = P.place_slots("The yogin grieves.", [(0, "The yogin", ("y",)), (1, "laments", ("l",))])
        self.assertEqual((r.english, r.unplaced), ("{0:The yogin} grieves.", [1]))

    def test_case_and_quote_marks_folded(self):
        r = P.place_slots("Those who know the Vedas’ end", [(0, "those who", ("y",)), (1, "Vedas' end", ("v",))])
        self.assertEqual(r.english, "{0:Those who} know the {1:Vedas’ end}")


class NewRecordFields(Fixture):
    """Fields of records written by the current pipeline: slotted lines and candidate loci."""

    def new_unit(self):
        rec = unit_1_2()
        rec["output"]["slotted"] = {"99.1": "{0:The yogin} {2:does} {1:not} {2:grieve}.",
                                    "99.2": "{0:He} {1:rejoices} {4:not} and {3:hates} {2:not}."}
        rec["output"]["alternative"]["slotted"] = {"99.1": "{0:The yogin} {2:grieves} {1:not}."}
        del rec["output"]["alternative"]["lines"]
        rec["card"]["verses"][0]["words"][2]["candidates"] = [
            {"word": "grieve", "found_by": "found by meaning", "modern_first_sense": "oewn2025 v: feel grief",
             "loci": ["sources/raw/upstream_data/english/webster1913_pg29765.txt:374695", "gcide-0.53/CIDE.G#1516712"]},
            {"word": "bewail", "found_by": "remembered", "loci": ["somewhere:1"]}]
        return rec

    def test_slotted_line_is_the_builder_english(self):
        self.put("99.1-99.2.json", self.new_unit())
        conv = P.convert("R", CH, self.runs, self.packets)
        v2 = self.verse(conv, "99.2")
        self.assertEqual(v2["english"], "{0:He} {1:rejoices} {4:not} and {3:hates} {2:not}.")   # the record's order, not ours
        self.assertEqual(v2["pipeline"]["slots_from"], "slotted line")
        self.assertEqual(self.verse(conv, "99.1")["forks"][0]["display"], "The yogin grieves not.")

    def test_slotted_line_that_is_not_the_line(self):
        rec = self.new_unit()
        rec["output"]["slotted"]["99.2"] = "{0:He} {1:rejoices} {9:never}."
        self.put("99.1-99.2.json", rec)
        r = P.convert("R", CH, self.runs, self.packets).unfinished["99.2"]
        self.assertIn("the slotted line without its slots is not the line", r)
        self.assertIn("the slotted line names words [9] the card does not have", r)

    def test_candidate_loci(self):
        self.put("99.1-99.2.json", self.new_unit())
        v = self.verse(P.convert("R", CH, self.runs, self.packets), "99.1")
        self.assertEqual(v["words"][2]["wording"]["candidates"], [
            {"word": "grieve", "locus": "sources/raw/upstream_data/english/webster1913_pg29765.txt:374695",
             "source": "webster", "definition": "feel grief", "found_by": "found by meaning"},
            {"word": "bewail", "locus": "somewhere:1", "found_by": "remembered"}])
        self.assertIn("[2] śocati: candidate 'bewail' cites a locus that names no dictionary",
                      P.convert("R", CH, self.runs, self.packets).unfinished["99.1"])

    def test_review_record(self):
        rec = unit_3(review=[{"severity": "S1", "kind": "adds", "locus": "99.3", "says": "adds", "fix": "drop it"}],
                     calls=[{"task": "review", "model": "m", "effort": "high"}])
        self.put("99.3.json", rec)
        code, _ = self.main("--allow-unfinished")
        self.assertEqual(code, 2)
        out = self.base / "out"
        r = json.loads((out / "independent-review-01-03.json").read_text(encoding="utf-8"))
        self.assertEqual(r["producer_sha256"], P._sha(out / "producer-01-03.json"))
        self.assertNotIn("complete", r)                       # no source states it
        self.assertEqual(r["not_in_the_run"], ["complete", "date"])
        self.assertEqual(r["reviewer_models"], ["m (high)"])
        self.assertEqual([(f["unit"], f["severity"], f["pipeline_severity"], f["status"]) for f in r["findings"]],
                         [("99.1-99.2.json", 3, "S3", "open"), ("99.3.json", 1, "S1", "open")])
        # the builder reads it as stated: not complete, one open severity-1 finding
        ctx = B.Ctx(chapter=CH, root=P.ROOT, chapter_dir=out)
        B.check_review(ctx, out / "producer-01-03.json", out / "independent-review-01-03.json")
        self.assertEqual(sorted(e[1] for e in ctx.report.errors),
                         ["independent-review-01-03.json: 1 open severity-1 findings",
                          "independent-review-01-03.json: review not complete"])


DP_RECORD = "sources/raw/panini/lexica/dhatupatha.json#1070003"
SUTRA_3_4_21 = "sources/primary/panini/ashtadhyayi/ashtadhyayi_collated_clean.txt:1154"
CHITTVA = {"kind": "krdanta", "stem": "chittvā", "avyaya": True, "vibhakti": None, "vacana": None, "linga": None,
           "dhatu": {"root": "chid", "gana": 7, "gana_name": "rudhādi", "pada": "ubhayapada", "upasargas": [], "sanadi": [],
                     "dp_record": DP_RECORD},
           "krt": {"name": "ktvā"}, "taddhita": None, "lakara": None, "prayoga": None,
           "ending": {"type": "sup", "name": "su", "sutra": "4.1.2", "luk": "2.4.82"}}
DERIV = {"matches": True, "steps": [{"sutra": "1.3.9", "result": "chid", "ashtadhyayi": "x:1"},
                                    {"sutra": "3.4.21", "result": "chid + ktvā", "ashtadhyayi": SUTRA_3_4_21},
                                    {"sutra": "3.4.21", "result": "again", "ashtadhyayi": SUTRA_3_4_21},
                                    {"sutra": "1.3.3.1", "result": "vārttika", "ashtadhyayi": None}]}


@unittest.skipUnless((P.PRAKRIYA / SUTRA_3_4_21.split(":")[0]).is_file() and P.DHATUPATHA.is_file(), "prakriya library absent")
class Grammar(unittest.TestCase):
    """grammar_fields on an engine analysis of chittvā (15.3), against the real Dhātupāṭha and Aṣṭādhyāyī."""

    def test_fields_from_the_analysis(self):
        f, notes = P.grammar_fields(CHITTVA, DERIV, None, "√chid")
        self.assertEqual(notes, [])
        self.assertEqual((f["root"], f["root_id"], f["rootGloss"]),
                         ("√chid (rudhādi, 7U, 'dvaidhīkaraṇe')", DP_RECORD, "dvaidhīkaraṇe"))
        self.assertEqual(f["affix"], "avyaya; ktvā (kṛt); su (sup 4.1.2, elided by 2.4.82)")
        self.assertEqual(f["parts"], [{"form": "√chid", "gloss": "dvaidhīkaraṇe"},
                                      {"form": "ktvā", "gloss": "samānakartṛkayoḥ pūrvakāle"}])   # the elided su is no piece
        self.assertEqual([(e["kind"], e.get("sutra"), e["locus"]) for e in f["evidence"]],
                         [("dhatupatha", None, DP_RECORD), ("sutra", "3.4.21", SUTRA_3_4_21)])   # chapters 2–5, once each
        self.assertEqual(f["evidence"][1]["quote"], P.source_line(SUTRA_3_4_21))

    def test_builder_verifies_the_evidence(self):
        f, _ = P.grammar_fields(CHITTVA, DERIV, None, "√chid")
        ctx = B.Ctx(chapter=CH, root=P.ROOT)
        B.check_evidence(ctx, "chittvā", f["evidence"])
        B.check_root(ctx, "chittvā", f)
        self.assertEqual(ctx.report.errors, [])

    def test_a_line_that_is_not_the_sutra_is_not_cited(self):
        wrong = {"matches": True, "steps": [{"sutra": "3.4.21", "result": "chid + ktvā",
                                             "ashtadhyayi": SUTRA_3_4_21.replace(":1154", ":1155")}]}
        f, notes = P.grammar_fields(CHITTVA, wrong, None, "√chid")
        self.assertEqual([e["kind"] for e in f["evidence"]], ["dhatupatha"])
        self.assertTrue(any("is not that sūtra's text" in n for n in notes))

    def test_a_derivation_that_misses_the_form_cites_nothing(self):
        f, notes = P.grammar_fields(CHITTVA, {**DERIV, "matches": False}, None, "√chid")
        self.assertEqual([e["kind"] for e in f["evidence"]], ["dhatupatha"])
        self.assertIn("the engine's derivation does not reproduce the form; no sūtra cited", notes)

    def test_root_differing_from_the_card_is_not_filled(self):
        f, notes = P.grammar_fields(CHITTVA, DERIV, None, "√bhid")
        self.assertNotIn("root", f)
        self.assertNotIn("root_id", f)
        self.assertIn("the engine's root √chid differs from the card's √bhid", notes)


class Refusals(Fixture):
    def test_unit_problems(self):
        self.assertEqual(P.unit_problems(unit_3()), [])
        self.assertEqual(P.unit_problems(unit_3(review=[{"severity": "S3", "says": "taste"}])), [])
        self.assertEqual(P.unit_problems(unit_3(output=None)), ["no translation output"])
        self.assertEqual(P.unit_problems(unit_3(code_errors=["x"])), ["code error left: x"])
        self.assertEqual(P.unit_problems(unit_3(review=[{"severity": "S1", "kind": "adds", "locus": "99.3", "says": "adds"}])),
                         ["S1 review finding left (adds, 99.3): adds"])

    def test_default_refuses_and_writes_nothing(self):
        code, err = self.main()
        self.assertEqual(code, 1)
        self.assertIn("REFUSED", err)
        self.assertIn("card affix absent", err)
        self.assertFalse((self.base / "out").exists())

    def test_missing_verse(self):
        (self.runs / "R/translate/99.3.json").unlink()
        conv = P.convert("R", CH, self.runs, self.packets)
        self.assertEqual(conv.unfinished["99.3"], ["no unit record translates this verse"])
        code, err = self.main()
        self.assertEqual(code, 1)
        self.assertIn("no unit record translates this verse", err)
        self.assertFalse((self.base / "out").exists())

    def test_code_errors_left(self):
        self.put("99.3.json", unit_3(code_errors=["99.3 word 0 (tat): no English"]))
        conv = P.convert("R", CH, self.runs, self.packets)
        self.assertEqual(conv.unfinished["99.3.json"], ["code error left: 99.3 word 0 (tat): no English"])
        code, err = self.main()
        self.assertEqual(code, 1)
        self.assertIn("code error left", err)

    def test_review_finding_left(self):
        self.put("99.3.json", unit_3(review=[{"severity": "S2", "kind": "line", "locus": "99.3", "says": "weak ending"}]))
        self.assertIn("S2 review finding left (line, 99.3): weak ending",
                      P.convert("R", CH, self.runs, self.packets).unfinished["99.3.json"])

    def test_verse_in_two_records(self):
        self.put("99.3-dup.json", unit_3())
        conv = P.convert("R", CH, self.runs, self.packets)
        self.assertIn("in two unit records (99.3-dup.json, 99.3.json)", conv.unfinished["99.3"])

    def test_allow_unfinished_writes_a_shard_the_builder_refuses(self):
        code, _ = self.main("--allow-unfinished")
        self.assertEqual(code, 2)
        out = self.base / "out"
        shard = json.loads((out / "producer-01-03.json").read_text(encoding="utf-8"))
        self.assertEqual(shard["schema_version"], "gita-producer-v2+unfinished")
        self.assertNotEqual(shard["schema_version"], B.PRODUCER_SCHEMA)
        self.assertIn("verse sense absent", shard["verses"][0]["unfinished"])
        self.assertEqual(json.loads((out / "packet.json").read_text(encoding="utf-8"))["verse_count"], 3)

    def test_never_writes_beside_hand_made_shards(self):
        out = self.base / "out"
        out.mkdir()
        (out / "producer-01-05.json").write_text(json.dumps({"schema_version": "gita-producer-v2", "verses": []}), encoding="utf-8")
        code, err = self.main("--allow-unfinished")
        self.assertEqual(code, 1)
        self.assertIn("was not written by publish.py", err)
        self.assertFalse((out / "packet.json").exists())


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Fixture tests for the Gītā chapter build: builder checks B1–B18 and the card meaning
contract, the producer-shard and term-policy migrations, packet v2 planning, the term
checker's policy/legacy split, and the deploy script.

    python3 scripts/test_build_gita_chapter_reader.py [-v]

Every check has a passing fixture (the base chapter builds with no error) and a failing
mutation. Fixtures live in temporary directories; nothing in the repository is read
except the scripts under test.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_gita_chapter_reader as B  # noqa: E402
import migrate_gita_producer_v2 as MS  # noqa: E402
import migrate_term_policy_v2 as MP  # noqa: E402

CH = 18                       # a real adhyāya number (index.html names it in Roman numerals)
IAST = "ye cāpy āsate ||"
DEVA = "ये चाप्य् आसते ॥"
ASH = "sources/primary/panini/ashtadhyayi/ashtadhyayi_collated_clean.txt"
KAS = "sources/primary/panini/kashika/kashika_collated_clean.txt"
DHP = "sources/raw/panini/lexica/dhatupatha.json"

POLICY_V1 = {
    "version": "test-1", "rule": "fixture", "detectors_note": "fixture",
    "terms": {"asana": {"match": "āsate|√ās", "senses": {"sit": {"policy": "translate", "english": ["sit"],
                                                                     "forbidden_english": ["squat"], "review": "pilot"}}},
              "yoga": {"match": "^yog", "senses": {"system": {"policy": "preserve", "iast": "yoga", "forbidden_english": ["union"]}}}},
    "changelog": [{"version": "test-1", "changes": "fixture"}],
}

GITA_JS_OK = r"""
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function renderVerse(v){return `<article>${(v.forks||[]).filter(f=>f.open).map(f=>`<p>${esc(f.display)}</p>`).join("")}</article>`;}
function wordCardHtml(w){const m=w.meaning||{};return `<div>${esc(w.gloss)}${(m.lines||[]).map(l=>`<p>${esc(l.text)}</p>`).join("")}</div>`;}
window.GitaReader = { renderVerse };
"""
GITA_JS_BLIND = GITA_JS_OK.replace("(v.forks||[]).filter(f=>f.open).map(f=>`<p>${esc(f.display)}</p>`).join(\"\")", "\"\"")


def card(i, iast, **kw):
    base = {"i": i, "iast": iast, "deva": iast, "gloss": kw.pop("gloss", iast), "parts": [{"form": iast, "gloss": "x"}],
            "affix": "none (avyaya)", "morph": "indeclinable particle", "stem": iast, "evidence": [], "fallback": []}
    base.update(kw)
    return base


def base_verse():
    return {
        "locus": f"{CH}.1", "speaker": "krishna", "meter": "anuṣṭubh", "iast": IAST, "devanagari": DEVA,
        "sense": "Those also sit.", "english": "{0:those} {1:and} {2:also} {3:sit}.",
        "grammar": {"karakaSummary": "ye (kartṛ) āsate"},
        "words": [
            card(0, "ye", stem="yad", word_class="pronoun", affix="jas → śī", morph="nom. pl. masc. pronoun",
                 evidence=[{"claim": "sūtra 1.1.1", "locus": f"{ASH}:1", "quote": "1.1.1 वृद्धिरादैच्", "kind": "sutra", "sutra": "1.1.1"}]),
            card(1, "ca", word_class="particle"),
            card(2, "api", word_class="particle"),
            card(3, "āsate", stem="√ās", word_class="content", gloss="they sit", root="√ās (adādi, 2A, 'upaveśane')",
                 root_id="dhatupatha.json#1020011", rootGloss="to sit", affix="laṭ jha → ate (3.4.79)", morph="3rd pl. present indicative",
                 parts=[{"form": "√ās", "gloss": "to sit"}, {"form": "-ate", "gloss": "3rd pl."}],
                 term={"lemma": "asana", "sense": "sit"},
                 wording={"sense_description": "to be seated", "chosen": "sit",
                          "candidates": [{"word": "sit", "source": "webster1913", "locus": "webster.txt:10"}]},
                 meaning={"image": "√ās 'to sit'", "lines": [{"cat": "lexical", "text": "to sit, be seated", "who": "Monier-Williams"},
                                                            {"cat": "synthesis", "text": "seated presence"}], "rendering": "sit"},
                 evidence=[{"claim": "√ās adādi 2A", "locus": f"{DHP}#1020011", "quote": "आसँ 2 adādi A उपवेशने", "kind": "dhatupatha"},
                           {"claim": "sūtra 3.4.79", "locus": f"{ASH}:2", "quote": "3.4.79 टित आत्मनेपदानां टेरे", "kind": "sutra", "sutra": "3.4.79"},
                           {"claim": "Kāśikā on 3.4.79", "locus": f"{KAS}:2", "quote": "टितो लकारस्य स्थाने", "kind": "kashika", "sutra": "3.4.79"}]),
        ],
        "forks": [{"at": "āsate (sense)", "words": [3], "display": "The verb can also mean to dwell.", "open": True, "reason_class": 5,
                   "followed": 0, "reason": "English forces a choice",
                   "construals": [{"reading": "sit", "basis": "√ās upaveśane", "traditions": ["Śaṅkara"]},
                                  {"reading": "dwell", "basis": "√ās in the sense of staying", "traditions": ["Rāmānuja"],
                                   "evidence": ["Adidevananda 99.1 'they abide'"]}]}],
        "deviations": [{"secondary": "Adidevananda", "their_rendering": "SECRET-DEVIATION-TEXT"}],
        "secondaries_consulted": ["Adidevananda", "Gambhirananda", "Sivananda", "Purohit", "Tapasyananda"],
    }


def fake_lookup(extra_defs=None):
    defs = {"sit": [{"locus": "sources/raw/upstream_data/english/webster.txt:10"}], "quietly": [{"locus": "webster.txt:20"}],
            "dwell": [{"locus": "webster.txt:30"}], "in": [{"locus": "webster.txt:40"}]}
    defs.update(extra_defs or {})
    return SimpleNamespace(english_define=lambda w, **kw: defs.get(w, []),
                           kashika_span=lambda rid: {"kashika": f"{KAS}:2-3"} if rid == "34079" else None)


class Fixture:
    """A repository root, a prakriya library and one chapter of one verse."""

    def __init__(self, gita_js: str = GITA_JS_OK, policy: dict | None = None):
        self.tmp = Path(tempfile.mkdtemp(prefix="gita-build-test-"))
        self.root, self.prakriya = self.tmp / "vedanta", self.tmp / "prakriya"
        self.policy = copy.deepcopy(policy or POLICY_V1)
        w = self.write
        w(self.root / "data/glossary/term_policy.json", self.policy)
        w(self.root / "assets/gita.js", gita_js)
        w(self.root / "assets/app.js", 'const GITA_READINGS = {\n  "yogavasistha-dama": {\n  },\n};\n')
        w(self.root / "data/articles/manifest.json", {"articles": [{"slug": "gita-ch5"}]})
        w(self.root / "gita/ch5/index.html", '<script src="verses.js"></script> gita-ch5 CH5_VERSES Bhagavad-Gītā 5 adhyāya V verses 1–29 audio: null,')
        w(self.prakriya / ASH, "1.1.1 वृद्धिरादैच्\n3.4.79 टित आत्मनेपदानां टेरे\n")
        w(self.prakriya / KAS, "प्रथमा\nटितो लकारस्य स्थाने यान्यात्मनेपदानि\nतेषां टेरेकारादेशो भवति।\nअन्यत्\n")
        w(self.prakriya / DHP, {"name": "dp", "data": [{"i": "1020011", "dhatu": "आस्", "aupadeshik": "आसँ", "gana": "2", "pada": "A", "artha": "उपवेशने"},
                                                        {"i": "1010001", "dhatu": "भू", "aupadeshik": "भू", "gana": "1", "pada": "P", "artha": "सत्तायाम्"}]})
        self.chdir = self.root / f"internal/sanskrit_reviews/gita/ch{CH}"
        w(self.chdir / "packet.json", {"chapter": CH, "verse_count": 1,
                                        "verses": [{"locus": f"{CH}.1", "iast": IAST, "devanagari": DEVA, "speaker": "krishna",
                                                    "secondaries_english": [{"author": "Swami Adidevananda", "text": "x"}]}]})
        self.verse = base_verse()
        self.shard_extra: dict = {}
        self.review_extra: dict = {}

    @staticmethod
    def write(p: Path, data) -> None:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    def shard(self) -> dict:
        sh = {"schema_version": B.PRODUCER_SCHEMA, "chapter": CH, "policy_sha256": B.policy_content_hash(self.policy), "verses": [self.verse]}
        sh.update(self.shard_extra)
        return sh

    def ctx(self, complete=True, render=True, lookup=None) -> B.Ctx:
        self.write(self.root / "data/glossary/term_policy.json", self.policy)
        sp = self.chdir / "producer-01-01.json"
        self.write(sp, self.shard())
        rev = {"producer_sha256": hashlib.sha256(sp.read_bytes()).hexdigest(), "complete": True, "findings": []}
        rev.update(self.review_extra)
        self.write(self.chdir / "independent-review-01-01.json", rev)
        return B.Ctx(chapter=CH, root=self.root, prakriya=self.prakriya, complete=complete,
                     lookup=lookup or fake_lookup(), run_render_contract=render)

    def run(self, **kw) -> B.Ctx:
        ctx = self.ctx(**kw)
        ctx.result = B.run(ctx)
        return ctx

    def word(self, i: int) -> dict:
        return self.verse["words"][i]

    def close(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class Base(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()

    def tearDown(self):
        self.fx.close()

    def errors(self, ctx, check=None):
        return [m for c, m, _ in ctx.report.errors if check is None or c == check]

    def assertPasses(self, **kw):
        ctx = self.fx.run(**kw)
        self.assertEqual(ctx.report.errors, [], "base fixture must build cleanly")
        return ctx

    def assertFails(self, check, needle=None, **kw):
        ctx = self.fx.run(**kw)
        errs = self.errors(ctx, check)
        self.assertTrue(errs, f"expected a {check} error; got {ctx.report.errors}")
        if needle:
            self.assertTrue(any(needle in e for e in errs), f"no {check} error mentions {needle!r}: {errs}")
        return ctx


class TestBaseFixture(Base):
    def test_base_builds_cleanly(self):
        self.assertPasses()


class TestB1PolicyHash(Base):
    def test_hash_is_content_not_changelog(self):
        a = copy.deepcopy(POLICY_V1)
        b = copy.deepcopy(POLICY_V1)
        b["changelog"].append({"changes": "note"})
        self.assertEqual(B.policy_content_hash(a), B.policy_content_hash(b))
        b["terms"]["asana"]["senses"]["sit"]["english"] = ["be seated"]
        self.assertNotEqual(B.policy_content_hash(a), B.policy_content_hash(b))

    def test_missing_hash(self):
        self.fx.shard_extra = {"policy_sha256": None}
        self.assertFails("B1", "no policy_sha256")

    def test_policy_edited_after_production_lists_rows(self):
        old_sha = B.policy_content_hash(self.fx.policy)
        snap = self.fx.root / "internal/sanskrit_reviews/gita/policy-snapshots" / f"{old_sha}.json"
        self.fx.write(snap, self.fx.policy)
        self.fx.shard_extra = {"policy_sha256": old_sha}
        self.fx.policy["terms"]["yoga"]["senses"]["system"]["forbidden_english"] = ["union", "discipline"]
        ctx = self.assertFails("B1", "rows changed: ['yoga']")
        self.assertIn("affected occurrences: none", self.errors(ctx, "B1")[0])


class TestB2Citations(Base):
    def test_quote_not_on_line(self):
        self.fx.word(0)["evidence"][0]["quote"] = "1.1.2 अदेङ्गुणः"
        self.assertFails("B2", "quote not found")

    def test_line_out_of_range(self):
        self.fx.word(0)["evidence"][0]["locus"] = f"{ASH}:99"
        self.assertFails("B2", "out of file")

    def test_ellipsis_spacing_and_hyphens_tolerated(self):
        self.fx.word(3)["evidence"][2]["quote"] = "टितो … स्थाने"
        self.fx.word(0)["evidence"][0]["quote"] = "1.1.1 वृद्धि-रादैच्।"
        self.assertPasses()

    def test_sandhi_resolved_quote_is_a_warning(self):
        self.assertEqual(B.quote_match("ye tu akṣaram", "ye tv akṣaram anirdeśyam"), "sandhi")
        self.assertEqual(B.quote_match("ye tv akṣaram", "ye tv akṣaram anirdeśyam"), "exact")
        self.assertIsNone(B.quote_match("sarvam idam jagat", "ye tv akṣaram anirdeśyam"))

    def test_packet_selectors(self):
        data = {"verses": [{"locus": "12.1", "commentaries": {"gita_gita_sanskrit": [{"author": "Sri X", "author_id": 5, "text": "abc"}]}}]}
        for sel in ("verses[12.1].commentaries.gita_gita_sanskrit[author=Sri X]", "verses[locus=12.1].commentaries.gita_gita_sanskrit[Sri X]",
                    "12.1/gita_gita_sanskrit/author_id=5", "verses[0].commentaries.gita_gita_sanskrit[author=Sri X]"):
            self.assertIn("abc", B.packet_selector_text(data, sel) or "", sel)
        self.assertIsNone(B.packet_selector_text(data, "verses[12.2].commentaries"))


class TestB3Kashika(Base):
    def test_sutra_required(self):
        del self.fx.word(3)["evidence"][2]["sutra"]
        self.assertFails("B3", "without `sutra`")

    def test_outside_span(self):
        ev = self.fx.word(3)["evidence"][2]
        ev["locus"], ev["quote"] = f"{KAS}:4", "अन्यत्"
        self.assertFails("B3", "outside the vṛtti")

    def test_unavailable_span_fails_closed(self):
        self.assertFails("B3", "cannot be verified", lookup=SimpleNamespace(english_define=fake_lookup().english_define))


class TestB4Wording(Base):
    def test_locus_not_from_define(self):
        self.fx.word(3)["wording"]["candidates"][0]["locus"] = "webster.txt:900"
        self.assertFails("B4", "not one of define's loci")

    def test_entry_line_after_headword_line_passes(self):
        self.fx.word(3)["wording"]["candidates"][0]["locus"] = "webster.txt:12"
        self.assertPasses()

    def test_unattested_word(self):
        self.fx.word(3)["wording"]["candidates"].append({"word": "sedentate", "source": "gcide", "locus": "gcide-0.53/CIDE.S"})
        self.assertFails("B4", "no headword")

    def test_composed_candidate(self):
        cands = self.fx.word(3)["wording"]["candidates"]
        cands.append({"word": "dwell in", "source": "composed", "parts": ["dwell", "in"]})
        self.assertPasses()
        cands[-1]["parts"] = ["dwell", "dveṣa"]
        self.assertFails("B4", "part 'dveṣa' does not resolve")

    def test_joycean_needs_unattested_word(self):
        self.fx.word(3)["wording"]["joycean"] = {"formation": "x", "parts": "x", "relation": "x", "paraphrase": "x", "why_no_attested_word": "x"}
        self.assertFails("B4", "but define attests it")


class TestB5Form(Base):
    def test_lyap_needs_having(self):
        self.fx.word(3)["affix"] = "lyap (7.1.37)"
        self.assertFails("B5", "lyap/ktvā")
        self.fx.verse["english"] = "{0:those} {1:and} {2:also} {3:having sat}."
        self.fx.word(3)["meaning"]["rendering"] = "having sat"
        self.fx.policy["terms"]["asana"]["senses"]["sit"]["english"] = ["sit", "sat"]
        self.assertPasses()

    def test_kta_not_ing(self):
        self.fx.word(3)["affix"] = "kta (3.2.102)"
        self.fx.verse["english"] = "{0:those} {1:and} {2:also} {3:sitting on}."
        self.fx.word(3)["meaning"]["rendering"] = "sitting"
        self.fx.policy["terms"]["asana"]["senses"]["sit"]["english"] = ["sitting"]
        self.assertFails("B5", "'sitting'")
        self.fx.word(3)["form_note"] = "the kta is adjectival here"
        self.assertPasses()

    def test_question_without_interrogative(self):
        self.fx.verse["english"] = "{0:those} {1:and} {2:also} {3:sit}?"
        self.assertFails("B5", "no word is interrogative")
        self.fx.word(0)["morph"] = "nom. pl. interrogative pronoun"
        self.assertPasses()


class TestB6Forbidden(Base):
    def test_slot(self):
        self.fx.verse["english"] = "{0:those} {1:and} {2:also} {3:sit and squat}."
        self.assertFails("B6", "slot uses forbidden 'squat'")

    def test_meaning_rendering(self):
        self.fx.word(3)["meaning"]["rendering"] = "squat"
        self.assertFails("B6", "meaning.rendering")

    def test_gloss_and_lines_may_list_senses(self):
        self.fx.word(3)["gloss"] = "they sit, squat"
        self.fx.word(3)["meaning"]["lines"][0]["text"] = "to sit, squat"
        self.assertPasses()

    def test_quotation_exempt(self):
        self.fx.verse["english"] = "{0:those} {1:and} {2:also} {3:sit (not ‘squat’)}."
        self.assertPasses()


class TestB7Forks(Base):
    def test_open_iff_class_5(self):
        self.fx.verse["forks"][0]["reason_class"] = 4
        self.assertFails("B7", "open must be true exactly when")

    def test_open_needs_display(self):
        del self.fx.verse["forks"][0]["display"]
        self.assertFails("B7", "without reader-facing `display`")

    def test_words_required(self):
        del self.fx.verse["forks"][0]["words"]
        self.assertFails("B7", "`words`")

    def test_basis_required(self):
        del self.fx.verse["forks"][0]["construals"][1]["basis"]
        self.assertFails("B7", "lacks basis")

    def test_fairness_word_level(self):
        self.fx.verse["locus"] = "12.12"
        self.fx.verse["words"][3]["iast"] = "jñānam"
        old = dict(B.FAIRNESS_WORDS)
        try:
            B.FAIRNESS_WORDS[CH] = [(f"{CH}.1", "asat")]
            self.fx.verse["locus"] = f"{CH}.1"
            self.fx.verse["words"][3]["iast"] = "āsate"
            self.fx.verse["forks"][0]["words"] = [0]
            self.assertFails("B7", "fairness locus 'asat'")
        finally:
            B.FAIRNESS_WORDS.clear()
            B.FAIRNESS_WORDS.update(old)


class TestB8Policy(Base):
    def test_rendering_outside_fixed_forms(self):
        self.fx.verse["english"] = "{0:those} {1:and} {2:also} {3:are seated}."
        self.fx.word(3)["meaning"]["rendering"] = "seated"
        self.assertFails("B8", "must use one of ['sit']")

    def test_missing_term(self):
        del self.fx.word(3)["term"]
        self.assertFails("POLICY", "carries no term")

    def test_v2_reserved_and_categories(self):
        v2, _ = MP.migrate(self.fx.policy, {}, default_status="owner-decided")
        v2["lemmas"]["asana"]["senses"]["sit"]["forms"] = {"finite": ["sit"]}
        v2["reserved_english"] = {"moreover": "yoga"}
        self.fx.policy = v2
        self.fx.verse["english"] = self.fx.verse["english"].replace("{2:also}", "{2:moreover}")
        ctx = self.assertFails("B8", "reserved English 'moreover'")
        self.assertFalse([e for e in self.errors(ctx, "B8") if "category" in e])
        v2["reserved_english"] = {}
        v2["lemmas"]["asana"]["senses"]["sit"]["forms"] = {"participle_present": ["sitting"]}
        self.assertFails("B8", "no form decided for grammatical category 'finite'")

    def test_reserved_in_shared_slot_owned_by_the_other_index(self):
        v2, _ = MP.migrate(self.fx.policy, {}, default_status="owner-decided")
        v2["lemmas"]["asana"]["senses"]["sit"]["forms"] = {"any": ["also sit", "sit"]}
        v2["reserved_english"] = {"also sit": "asana"}
        self.fx.policy = v2
        self.fx.verse["english"] = "{0:those} {1:and} {2:also sit} {3:sit}."
        self.assertTrue(any("for asana" in e for e in self.errors(self.fx.run(), "B8")))   # api's own slot prints it: refused
        self.fx.word(3)["meaning"]["rendering"] = "also sit"
        self.fx.verse["english"] = "{0:those} {1:and} {2,3:also sit}."
        self.assertFalse([e for e in self.errors(self.fx.run(), "B8") if "reserved" in e])  # shared with āsate, which owns it

    def test_function_words_are_never_reserved(self):
        v2, _ = MP.migrate(self.fx.policy, {}, default_status="owner-decided")
        v2["reserved_english"] = {"also": "yoga", "with all": "yoga"}
        self.fx.policy = v2
        self.assertFalse([e for e in self.errors(self.fx.run(), "B8") if "reserved English" in e])

    def test_compound_member_owns_reserved_english(self):
        v2, _ = MP.migrate(self.fx.policy, {}, default_status="owner-decided")
        v2["reserved_english"] = {"moreover": "yoga"}
        self.fx.policy = v2
        self.fx.verse["english"] = self.fx.verse["english"].replace("{2:also}", "{2:moreover}")
        self.assertFails("B8", "reserved English 'moreover'")
        self.fx.word(2)["compound"] = {"type": "karmadhāraya", "vigraha": "x", "members": ["yoga", "api"]}
        self.assertFalse([e for e in self.errors(self.fx.run(), "B8") if "reserved English 'moreover'" in e])
        v2["lemmas"]["yoga2"] = json.loads(json.dumps(v2["lemmas"]["yoga"]))       # two rows match the member: ambiguous
        self.assertFails("B8", "matches rows")
        self.fx.word(2)["terms"] = [{"lemma": "yoga", "sense": "system", "member": 0}]
        self.assertFalse([e for e in self.errors(self.fx.run(), "B8") if "matches rows" in e])

    def test_v2_proposed_status_refused(self):
        del self.fx.policy["terms"]["asana"]["senses"]["sit"]["review"]
        v2, _ = MP.migrate(self.fx.policy, {}, default_status="proposed")   # `proposed` is still refused (lead, 2026-11-08)
        self.fx.policy = v2
        self.assertFails("POLICY", "status 'proposed'")

    def test_v2_lexicon_reviewed_status_admitted(self):
        del self.fx.policy["terms"]["asana"]["senses"]["sit"]["review"]
        v2, _ = MP.migrate(self.fx.policy, {})                            # default: lexicon-reviewed
        self.fx.policy = v2
        ctx = self.fx.run()
        self.assertFalse([e for e in self.errors(ctx, "POLICY") if "status" in e])


class TestB9PublicText(Base):
    def test_pipeline_vocabulary(self):
        for text, needle in [("policy row asana", "policy"), ("see F12", "F-number"), ("as standard §7.6 says", "§"),
                             ("the owner's aesthetic gate", "owner"), ("lead decision", "lead"), ("fallback", "fallback"),
                             ("see fork", "fork")]:
            self.fx.word(3)["note"] = text
            self.assertFails("B9", needle)
        self.fx.word(3)["note"] = "the owner of the body sits at the gate of the city"
        self.assertPasses()

    def test_fork_display_and_meaning_are_public(self):
        self.fx.verse["forks"][0]["display"] = "Per the shard, also dwell."
        self.assertFails("B9", "shard")


class TestB10Render(Base):
    def test_reader_that_cannot_show_forks(self):
        self.fx.close()
        self.fx = Fixture(gita_js=GITA_JS_BLIND)
        self.assertFails("B10", "reader cannot show forks")


class TestB11PadaPatha(Base):
    def test_dropped_particles(self):
        for drop in (1, 2):
            fx = Fixture()
            try:
                words = [w for k, w in enumerate(fx.verse["words"]) if k != drop]
                for k, w in enumerate(words):
                    w["i"] = k
                fx.verse["words"] = words
                fx.verse["english"] = " ".join(f"{{{k}:{w['iast']}}}" for k, w in enumerate(words))
                fx.verse["forks"][0]["words"] = [len(words) - 1]
                ctx = fx.run()
                self.assertTrue(self.errors(ctx, "B11"), f"dropping {drop} must fail B11")
            finally:
                fx.close()

    def test_alignment_unit(self):
        sam = B.samhita_tokens("evaṃ satatayuktā ye bhaktās tvāṃ paryupāsate | ye cāpy akṣaram avyaktaṃ ||")
        good = ["evam", "satatayuktāḥ", "ye", "bhaktāḥ", "tvām", "paryupāsate", "ye", "ca", "api", "akṣaram", "avyaktam"]
        key = [B.latin_key(x) for x in good]
        self.assertIsNone(B.align_padas(sam, key))
        for particle in ("ca", "api"):
            self.assertIsNotNone(B.align_padas(sam, [k for k in key if k != particle]), particle)
        self.assertIsNotNone(B.align_padas(sam, key[:8] + ["eva"] + key[8:]), "an invented eva")
        sam2 = B.samhita_tokens("tyāgāc chāntir anantaram || te 'pi na hi tv eva ||")
        self.assertIsNone(B.align_padas(sam2, [B.latin_key(x) for x in ["tyāgāt", "śāntiḥ", "anantaram", "te", "api", "na", "hi", "tu", "eva"]]))
        for p in ("na", "hi", "tu", "eva"):
            self.assertIsNotNone(B.align_padas(sam2, [B.latin_key(x) for x in ["tyāgāt", "śāntiḥ", "anantaram", "te", "api", "na", "hi", "tu", "eva"] if x != p]), p)


class TestB12Schema(Base):
    def test_schema_version(self):
        self.fx.shard_extra = {"schema_version": "gita-producer-v1"}
        self.assertFails("B12", "schema_version")

    def test_word_class(self):
        del self.fx.word(1)["word_class"]
        self.assertFails("B12", "word_class")

    def test_evidence_shape(self):
        self.fx.word(0)["evidence"][0]["also"] = "x"
        self.assertFails("B12", "evidence keys outside")
        del self.fx.word(0)["evidence"][0]["also"]
        del self.fx.word(0)["evidence"][0]["kind"]
        self.assertFails("B12", "lacks kind")

    def test_slot_syntax(self):
        self.fx.verse["english"] = "{0:those} {1:and} {2:also} {3:sit"
        self.assertFails("B12", "malformed slot")


class TestB13Secondaries(Base):
    def test_translator_quoted_in_public_text(self):
        self.fx.word(3)["note"] = "Adidevananda 'they abide'"
        self.assertFails("B13", "Adidevananda")
        self.fx.word(3)["note"] = "Adidevananda's reading is different"
        self.assertPasses()

    def test_reception_quotation_length(self):
        self.fx.word(3)["meaning"]["lines"].insert(1, {"cat": "reception", "text": "\"sit\"", "who": "Sri Aurobindo"})
        self.assertPasses()
        self.fx.word(3)["meaning"]["lines"][1]["text"] = "\"they sit down there in the very same place all day long\""
        self.assertFails("B13", "reception quotes more than")

    def test_public_files_never_carry_deviations_or_secondary_wordings(self):
        self.fx.word(3)["wording"]["candidates"].append({"word": "abide", "source": "Adidevananda", "locus": "Adidevananda 99.1 'they abide'",
                                                         "definition": "SECRET-SECONDARY-TEXT"})
        ctx = self.fx.ctx()
        result = B.run(ctx)
        self.assertEqual(self.errors(ctx), [])
        (self.fx.root / f"gita/ch{CH}").mkdir(parents=True, exist_ok=True)
        (self.fx.root / f"gita/ch{CH}/apparatus.json").write_text("{}")       # a stale public apparatus
        B.write_outputs(ctx, result)
        pub = self.fx.root / f"gita/ch{CH}"
        self.assertFalse((pub / "apparatus.json").exists(), "the reader does not load apparatus.json, so it is not published")
        public_text = "".join(p.read_text(encoding="utf-8") for p in pub.iterdir())
        for secret in ("SECRET-DEVIATION-TEXT", "SECRET-SECONDARY-TEXT", "they abide", "Adidevananda"):
            self.assertNotIn(secret, public_text)
        self.assertIn("SECRET-DEVIATION-TEXT", (self.fx.chdir / "deviations.json").read_text(encoding="utf-8"))
        self.assertIn(f'"gita-ch{CH}"', (self.fx.root / "assets/app.js").read_text(encoding="utf-8"))
        # a reader that does load the apparatus gets one stripped of secondary candidates
        app = B.public_apparatus(result["apparatus"])
        self.assertNotIn("SECRET", json.dumps(app))
        self.assertNotIn("Adidevananda", json.dumps(app))


class TestB14OwnerQueue(Base):
    def test_queue_from_occurrences(self):
        ctx = self.fx.ctx()
        result = B.run(ctx)
        q = B.owner_queue(ctx, result["public"])
        row = q["rows"][0]
        self.assertEqual((row["lemma"], row["sense"], row["status"]), ("asana", "sit", "pilot"))
        self.assertEqual(row["occurrences"], [{"at": f"{CH}.1[3]", "iast": "āsate", "rendering": "sit"}])

    def test_changed_since_decision_flagged(self):
        v2, _ = MP.migrate(self.fx.policy, {}, default_status="owner-decided")
        v2["lemmas"]["asana"]["senses"]["sit"]["decided"] = {"by": "owner", "row_sha256": "0" * 64}
        self.fx.policy = v2
        ctx = self.fx.ctx()
        q = B.owner_queue(ctx, B.run(ctx)["public"])
        self.assertEqual(q["rows"][0]["changed_flag"], "changed since decision")


class TestB15Review(Base):
    def test_restamp_without_rereview(self):
        self.fx.review_extra = {"lead_edits_after_acceptance": [{"date": "2026-11-08", "new_sha256": None}]}
        ctx = self.fx.ctx()
        sp = self.fx.chdir / "producer-01-01.json"
        rev_p = self.fx.chdir / "independent-review-01-01.json"
        rev = json.loads(rev_p.read_text())
        rev["lead_edits_after_acceptance"][0]["new_sha256"] = rev["producer_sha256"]
        rev_p.write_text(json.dumps(rev))
        B.run(ctx)
        self.assertTrue(any("re-stamped" in e for e in self.errors(ctx, "B15")))
        rev["rereview"] = {"date": "2026-11-09", "producer_sha256": rev["producer_sha256"]}
        rev_p.write_text(json.dumps(rev))
        ctx2 = B.Ctx(chapter=CH, root=self.fx.root, prakriya=self.fx.prakriya, lookup=fake_lookup())
        B.run(ctx2)
        self.assertEqual(self.errors(ctx2, "B15"), [], sp)

    def test_stale_review(self):
        ctx = self.fx.ctx()
        (self.fx.chdir / "producer-01-01.json").write_text(json.dumps(self.fx.shard(), ensure_ascii=False))
        B.run(ctx)
        self.assertTrue(self.errors(ctx, "REVIEW"))


class TestB16Discovery(Base):
    def test_readers_discovered(self):
        for d in ("ch5", "ch77"):
            self.fx.write(self.fx.root / f"gita/{d}/verses.js", f"window.X{d}_VERSES = [];")
        self.assertEqual([p.parent.name for p in B.discover_readers(self.fx.root)], ["ch5", "ch77"])


class TestB17Root(Base):
    def test_root_id_required_and_resolved(self):
        del self.fx.word(3)["root_id"]
        self.assertFails("B17", "without root_id")
        self.fx.word(3)["root_id"] = "dhatupatha.json#1010001"
        self.assertFails("B17", "record dhatupatha.json#1010001 is bhvādi 1P")
        self.fx.word(3)["root_id"] = "dhatupatha.json#9999999"
        self.assertFails("B17", "does not resolve")


class TestB18Fallback(Base):
    def test_kinds(self):
        self.fx.word(0)["fallback"] = ["an untyped note"]
        self.assertFails("B18", "must be {kind, text}")
        self.fx.word(0)["fallback"] = [{"kind": "pratyaya", "text": "affix not located"}]
        self.assertFails("B18", "blocks a complete chapter")
        ctx = self.fx.run(complete=False)
        self.assertEqual(self.errors(ctx, "B18"), [])


class TestMeaning(Base):
    def test_required_on_root_card(self):
        del self.fx.word(3)["meaning"]
        self.assertFails("MEANING", "`meaning` required")

    def test_optional_on_particles(self):
        self.assertNotIn("meaning", self.fx.word(1))
        self.assertPasses()

    def test_closed_categories_order_and_sources(self):
        lines = self.fx.word(3)["meaning"]["lines"]
        lines[0]["cat"] = "folk"
        self.assertFails("MEANING", "not in")
        lines[0]["cat"] = "lexical"
        lines.reverse()
        self.assertFails("MEANING", "out of display order")
        lines.reverse()
        del lines[0]["who"]
        self.assertFails("MEANING", "names no source")

    def test_rendering_matches_line(self):
        self.fx.word(3)["meaning"]["rendering"] = "remain seated"
        self.assertFails("MEANING", "is not what the line prints")


class TestShardMigration(unittest.TestCase):
    def tools(self, fx):
        recs = {"√ās": [{"id": "1020011", "gana": 2, "pada": "A"}],
                "√kṣam": [{"id": "1040103", "gana": 4, "pada": "P"}, {"id": "1040128", "gana": 4, "pada": "P"}]}
        return MS.Tools(fx.prakriya, fx.root, sutra_of_line=lambda n: {1: "1.1.1", 2: "3.4.79"}.get(n),
                        dhatu_records=lambda r: recs.get(r, []), attested=lambda w: w in ("sit", "dwell", "in"))

    def v1_shard(self):
        v = base_verse()
        for w in v["words"]:
            w.pop("word_class", None)
            w.pop("root_id", None)
            for e in w["evidence"]:
                e.pop("kind", None)
                e.pop("sutra", None)
        w3 = v["words"][3]
        w3["evidence"][1]["also"] = f"{KAS}:2 (Kāśikā)"
        w3["evidence"][1]["locus_repaired"] = "2026-11-08"
        del w3["evidence"][2]
        w3["wording"]["candidates"].append({"word": "dwell in", "source": "gcide", "locus": "gcide-0.53/CIDE.D"})
        v["words"].append(card(4, "kṣamī", root="√kṣam (divādi, 4P, 'sahane')", affix="ghinuṇ", morph="nom. sg.",
                               evidence=[{"claim": "√kṣam", "locus": f"{DHP}#1040103", "quote": "x"}]))
        return {"schema_version": "gita-producer-v1", "policy_version": "test-1", "verses": [v]}

    def test_migration_fields_and_idempotence(self):
        fx = Fixture()
        try:
            tools = self.tools(fx)
            new, notes = MS.migrate_shard(self.v1_shard(), "abc", tools)
            self.assertEqual((new["schema_version"], new["policy_sha256"]), (B.PRODUCER_SCHEMA, "abc"))
            words = new["verses"][0]["words"]
            self.assertEqual([w["word_class"] for w in words], ["pronoun", "particle", "particle", "content", "content"])
            ev = words[3]["evidence"]
            self.assertEqual([e["kind"] for e in ev], ["dhatupatha", "sutra", "kashika"])
            self.assertEqual(ev[1]["sutra"], "3.4.79")
            self.assertEqual(ev[2], {"claim": "Kāśikā on 3.4.79", "locus": f"{KAS}:2", "quote": "टितो लकारस्य स्थाने यान्यात्मनेपदानि",
                                     "sutra": "3.4.79", "kind": "kashika"})
            self.assertNotIn("locus_repaired", ev[1])
            self.assertNotIn("also", ev[1])
            self.assertEqual(words[0]["evidence"][0]["sutra"], "1.1.1")
            self.assertEqual(words[3]["root_id"], "dhatupatha.json#1020011")
            self.assertEqual(words[4]["root_id"], "dhatupatha.json#1040103", "the card's own cited record breaks the tie")
            comp = words[3]["wording"]["candidates"][-1]
            self.assertEqual((comp["source"], comp["parts"], comp["cited_source"]), ("composed", ["dwell", "in"], "gcide"))
            again, _ = MS.migrate_shard(new, "abc", tools)
            self.assertEqual(again, new, "migration must be idempotent")
            words[4]["evidence"] = []
            words[4].pop("root_id")
            _, notes = MS.migrate_shard(new, "abc", tools)
            self.assertTrue(any("2 Dhātupāṭha records" in t for t in notes["root_id_todo"]))
        finally:
            fx.close()

    def test_migrated_fixture_builds(self):
        fx = Fixture()
        try:
            new, _ = MS.migrate_shard(self.v1_shard(), B.policy_content_hash(fx.policy), self.tools(fx))
            v = new["verses"][0]
            v["words"] = v["words"][:4]                       # the kṣamī card is not in this verse's text
            fx.verse = v
            ctx = fx.run()
            self.assertEqual([c for c, _, _ in ctx.report.errors], [])
        finally:
            fx.close()

    def test_kashika_sutra_from_claim_or_paired_item(self):
        todo = []
        out = MS.migrate_evidence([{"claim": "Kāśikā on 6.2.61 kte nityārthe", "locus": f"{KAS}:2", "quote": "x"},
                                   {"claim": "sūtra", "locus": f"{ASH}:2", "quote": "3.4.79 टित"},
                                   {"claim": "vṛtti", "locus": f"{KAS}:3", "quote": "y"},
                                   {"claim": "vṛtti", "locus": f"{KAS}:4", "quote": "z"}], self.tools(Fixture()), todo, "t")
        self.assertEqual([e.get("sutra") for e in out], ["6.2.61", "3.4.79", "3.4.79", "3.4.79"])
        out = MS.migrate_evidence([{"claim": "vṛtti", "locus": f"{KAS}:3", "quote": "y"}], self.tools(Fixture()), todo, "t")
        self.assertNotIn("sutra", out[0])
        self.assertTrue(todo)


class TestPolicyMigration(unittest.TestCase):
    def test_v1_to_v2(self):
        uses = {"asana": {"occurrences": ["99.1[3]"], "senses": {"sit": ["99.1[3]"]}, "root_ids": ["dhatupatha.json#1020011"], "upasargas": []}}
        v2, notes = MP.migrate(POLICY_V1, uses)
        pol = B.Policy(v2)
        self.assertEqual(pol.structure, "v2")
        s = pol.sense("asana", "sit")
        self.assertEqual((s.forms, s.status, s.applies_to), ({"any": ["sit"]}, "pilot", ["99.1[3]"]))
        self.assertEqual(pol.sense("yoga", "system").status, "lexicon-reviewed")   # default since the lead's decision of 2026-11-08
        self.assertEqual(pol.reserved, {"sit": "asana"})
        self.assertEqual(pol.rows["asana"].root_ids, ["dhatupatha.json#1020011"])
        self.assertEqual(v2["changelog"][:1], POLICY_V1["changelog"])
        self.assertEqual(MP.migrate(v2, uses)[1], {"already_v2": True})
        self.assertEqual(MP.migrate(POLICY_V1, uses)[0], v2, "deterministic")

    def test_shared_rendering_not_reserved(self):
        p = copy.deepcopy(POLICY_V1)
        p["terms"]["sad"] = {"match": "sad", "senses": {"sit": {"policy": "translate", "english": ["sit"]}}}
        v2, notes = MP.migrate(p, {})
        self.assertNotIn("sit", v2["reserved_english"])
        self.assertEqual(notes["shared_renderings"], {"sit": ["asana", "sad"]})

    def test_builder_and_checker_accept_v1_with_changelog(self):
        self.assertEqual(B.Policy(POLICY_V1).structure, "v1")


class TestPacketPlan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import build_gita_chapter_packet as P
            cls.P = P
        except Exception as e:  # the packet builder imports prakriya's lookup.py
            raise unittest.SkipTest(f"packet builder not importable: {e}")

    def test_balanced_partition(self):
        self.assertEqual(self.P.balanced_partition([12] * 20), [list(range(k, k + 5)) for k in (0, 5, 10, 15)])
        self.assertEqual(self.P.balanced_partition([30, 30, 30]), [[0], [1, 2]])
        groups = self.P.balanced_partition([50, 10, 10, 50])
        self.assertEqual(sorted(i for g in groups for i in g), [0, 1, 2, 3])
        self.assertLessEqual(max(sum([50, 10, 10, 50][i] for i in g) for g in groups), 60)

    def test_sentence_units_never_split(self):
        units = self.P.merge_units(6, [(2, 3), (5, 6)])
        self.assertEqual(units, [[1], [2, 3], [4], [5, 6]])
        plan = self.P.shard_plan(99, 6, {v: 30 for v in range(1, 7)}, {1: "A line —", 2: "ends.", 3: "ends."}, "test")
        for s in plan:
            self.assertFalse(any(u.startswith("99.2") and "99.1" in s["verses"] and not s["verses"].endswith("99.1") for u in s["units"]))
        flat = [u for s in plan for u in s["units"]]
        self.assertIn("99.1-2", flat, "a line without sentence-final punctuation joins the next verse")
        self.assertIn("99.3", flat)


class TestTermChecker(unittest.TestCase):
    """check_gita_terms.js: policy-built readers are governed by the policy alone; the legacy
    tables apply to the three pre-policy readers only."""

    def run_checker(self, readers: dict[str, list], policy=None):
        tmp = Path(tempfile.mkdtemp(prefix="gita-terms-test-"))
        try:
            (tmp / "scripts").mkdir()
            shutil.copy(HERE / "check_gita_terms.js", tmp / "scripts/check_gita_terms.js")
            Fixture.write(tmp / "data/glossary/manifest.json", {"terms": []})
            Fixture.write(tmp / "data/glossary/term_policy.json", policy or POLICY_V1)
            for d, verses in readers.items():
                Fixture.write(tmp / f"gita/{d}/verses.js", f"window.R{d.upper().replace('-', '')}_VERSES = {json.dumps(verses, ensure_ascii=False)};")
            r = subprocess.run(["node", str(tmp / "scripts/check_gita_terms.js")], capture_output=True, text=True)
            return r.returncode, r.stdout + r.stderr
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def verse(self, english, words):
        return [{"locus": "1.1", "english": english, "words": words}]

    def test_legacy_reader_keeps_tables_policy_reader_does_not(self):
        krodha = {"i": 0, "iast": "krodhaḥ", "stem": "krodha", "gloss": "anger"}
        code, out = self.run_checker({"ch5": self.verse("{0:krodha}", [krodha])})
        self.assertEqual(code, 0, out)
        code, out = self.run_checker({"ch5": self.verse("{0:anger}", [krodha])})
        self.assertNotEqual(code, 0, out)
        self.assertIn("D ch5", out)
        # a policy-built reader: the legacy krodha row does not apply
        sit = {"i": 1, "iast": "āsate", "stem": "√ās", "gloss": "they sit", "term": {"lemma": "asana", "sense": "sit"}}
        code, out = self.run_checker({"ch99": self.verse("{0:anger} {1:sit}", [krodha, sit])})
        self.assertEqual(code, 0, out)
        code, out = self.run_checker({"ch99": self.verse("{0:anger} {1:squat}", [krodha, sit])})
        self.assertIn("P ch99", out)
        self.assertNotEqual(code, 0)

    def test_v2_policy_and_reserved_english(self):
        v2, _ = MP.migrate(POLICY_V1, {}, default_status="owner-decided")
        sit = {"i": 0, "iast": "āsate", "stem": "√ās", "gloss": "they sit", "term": {"lemma": "asana", "sense": "sit"}}
        other = {"i": 1, "iast": "tiṣṭhati", "stem": "√sthā", "gloss": "stands"}
        code, out = self.run_checker({"ch99": self.verse("{0:sit} {1:stands}", [sit, other])}, v2)
        self.assertEqual(code, 0, out)
        code, out = self.run_checker({"ch99": self.verse("{0:sit} {1:sit up}", [sit, other])}, v2)
        self.assertIn("R ch99", out)


@unittest.skipUnless(shutil.which("git") and shutil.which("node"), "git and node required")
class TestDeploy(unittest.TestCase):
    def sh(self, *args, cwd, env=None, check=True):
        r = subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, env=env)
        if check and r.returncode != 0:
            raise AssertionError(f"{args} failed: {r.stdout}{r.stderr}")
        return r

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="gita-deploy-test-"))
        self.origin, self.work = self.tmp / "origin.git", self.tmp / "work"
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        self.env = env
        seed = self.tmp / "seed"
        Fixture.write(seed / "assets/app.js", 'const GITA_READINGS = {\n  "yogavasistha-dama": {\n  },\n};\n')
        Fixture.write(seed / "data/articles/manifest.json", {"articles": [{"slug": "gita-ch5"}]})
        Fixture.write(seed / "scripts/run_checks.sh", "exit 0\n")
        Fixture.write(seed / "README", "x\n")
        self.sh("git", "init", "-q", "-b", "main", cwd=seed)
        self.sh("git", "add", ".", cwd=seed)
        self.sh("git", "commit", "-q", "-m", "seed", cwd=seed, env=env)
        self.sh("git", "clone", "-q", "--bare", str(seed), str(self.origin), cwd=self.tmp)
        self.sh("git", "clone", "-q", str(self.origin), str(self.work), cwd=self.tmp)
        for f in ("deploy_gita_chapter.sh", "build_gita_chapter_reader.py"):
            shutil.copy(HERE / f, self.work / "scripts" / f)
        Fixture.write(self.work / "gita/ch99/verses.js", "window.CH99_VERSES = [{\"locus\": \"99.1\"}];")
        Fixture.write(self.work / "gita/ch99/index.html", "<html></html>")
        Fixture.write(self.work / "gita/ch99/apparatus.json", "{}")
        Fixture.write(self.work / "data/glossary/term_policy.json", POLICY_V1)
        Fixture.write(self.work / "README", "another agent's uncommitted edit\n")
        self.origin_head = self.sh("git", "rev-parse", "main", cwd=self.origin).stdout.strip()

    def tearDown(self):
        wt = self.sh("git", "worktree", "list", "--porcelain", cwd=self.work, check=False).stdout
        for line in wt.splitlines():
            if line.startswith("worktree ") and Path(line[9:]) != self.work:
                self.sh("git", "worktree", "remove", "--force", line[9:], cwd=self.work, check=False)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def deploy(self, checks="exit 0"):
        env = dict(self.env, DEPLOY_REMOTE_URL=str(self.origin), DEPLOY_SKIP_BUILD="1", DEPLOY_CHECKS=checks)
        return self.sh("sh", "scripts/deploy_gita_chapter.sh", "99", "Gītā 99: test reader", cwd=self.work, env=env, check=False)

    def test_commits_chapter_scope_and_does_not_push(self):
        r = self.deploy()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Not pushed", r.stdout)
        self.assertIn("push", r.stdout)
        wt = Path(next(l.split("'")[1] for l in r.stdout.splitlines() if "push" in l and "-C" in l))
        files = self.sh("git", "show", "--name-only", "--format=", "HEAD", cwd=wt).stdout.split()
        self.assertEqual(sorted(files), ["assets/app.js", "data/articles/manifest.json", "data/glossary/term_policy.json",
                                         "gita/ch99/index.html", "gita/ch99/verses.js"])
        self.assertIn('"gita-ch99"', (wt / "assets/app.js").read_text())
        man = json.loads((wt / "data/articles/manifest.json").read_text())
        self.assertEqual([a.get("status") for a in man["articles"] if a["slug"] == "gita-ch99"], ["provisional"])
        self.assertEqual(self.sh("git", "log", "-1", "--format=%s", cwd=wt).stdout.strip(), "Gītā 99: test reader")
        self.assertEqual(self.sh("git", "rev-parse", "main", cwd=self.origin).stdout.strip(), self.origin_head, "nothing pushed")
        self.assertEqual((self.work / "README").read_text(), "another agent's uncommitted edit\n", "working tree untouched")

    def test_failing_checks_refuse(self):
        r = self.deploy(checks="exit 3")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("checks failed", r.stderr)

    def test_unexpected_change_refused(self):
        r = self.deploy(checks="echo changed > README")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("other changes", r.stderr)


if __name__ == "__main__":
    unittest.main()

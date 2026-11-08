"""Tests for scripts/gita (run: python3 -m unittest discover -s scripts/gita/tests -v).

Fixture tests run in a temporary pipeline directory inside internal/gita_pipeline/ (git-ignored).
Tests marked "stage A" need the real stage-A products of chapter 12
(python3 scripts/gita/build_all_packets.py --chapters 12) and are skipped without them."""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent))
from gitapipe import common as C  # noqa: E402

C.fix_sys_path()
from gitapipe import lexicon as L, names as N, oracle as O, validate as V  # noqa: E402

REAL_PIPE = C.PIPE
HAVE_CH12 = (REAL_PIPE / "packets/verses/12.1.json").is_file() and (REAL_PIPE / "packets/analyses.sqlite").is_file()
UPASATE = {"id": "g-ebbbaba651a9aec1", "form": "upāsate", "pausal": "upāsate", "kind": "tinanta", "stem": None,
           "dhatu": {"aupadeshika": "आसँ॒", "root": "ās", "gana": 2, "gana_name": "adādi", "pada": "ātmanepada", "artha": "उपवेशने",
                     "upasargas": ["upa"], "sanadi": [], "dp_record": "sources/raw/panini/lexica/dhatupatha.json#1020011"},
           "lakara": "laṭ", "prayoga": "kartari", "purusha": "prathama", "vacana": "bahuvacana", "linga": None, "vibhakti": None,
           "pada": "ātmanepada", "krt": None, "taddhita": None, "ending": {"type": "tiṅ", "name": "jha", "sutra": "3.4.78"},
           "source": "vidyut-kosha"}


class TempPipe(unittest.TestCase):
    def setUp(self):
        base = REAL_PIPE / "test-tmp"
        base.mkdir(parents=True, exist_ok=True)
        self.pipe = Path(tempfile.mkdtemp(dir=base))
        C.PIPE = self.pipe
        V._secondary_ngrams.cache_clear()

    def tearDown(self):
        C.PIPE = REAL_PIPE
        shutil.rmtree(self.pipe, ignore_errors=True)


# ---------------------------------------------------------------- 1. the oracle seam
class OracleTests(unittest.TestCase):
    def test_absent_kit_fails_clearly(self):
        saved = C.GITA_KIT
        C.GITA_KIT = Path(tempfile.mkdtemp())
        try:
            with self.assertRaises(O.OracleUnavailable) as cm:
                O.KitOracle()
            self.assertIn("grammar oracle absent", str(cm.exception))
        finally:
            shutil.rmtree(C.GITA_KIT)
            C.GITA_KIT = saved

    def test_fixture_normalises(self):
        d = Path(tempfile.mkdtemp())
        f = d / "o.json"
        f.write_text(json.dumps({"analyses": {"ca": [{"form": "ca", "kind": "avyaya", "stem": "ca"}]},
                                 "splits": {"12.1": [{"tokens": [{"form": "evam"}, "satatayuktāḥ"], "source": "x"}]}}))
        o = O.FixtureOracle(f)
        a = o.analyze("ca")[0]
        self.assertTrue(a["id"].startswith("pipe-"))                      # id assigned when the oracle gives none
        self.assertEqual(a["id"], O.FixtureOracle(f).analyze("ca")[0]["id"])   # stable
        self.assertEqual(o.split("12.1")[0]["tokens"], ["evam", "satatayuktāḥ"])
        shutil.rmtree(d)


# ---------------------------------------------------------------- 2. names
class MemberTermTests(unittest.TestCase):
    def test_infer_member_term(self):
        from gitapipe.expand import infer_member_term
        b = C.import_builder()
        pol = b.Policy({"terms": {"yoga": {"match": "^yog", "senses": {"system": {"policy": "preserve", "iast": "yoga"}}},
                                  "two": {"match": "^dvi", "senses": {"a": {"policy": "translate", "english": ["x"]},
                                                                      "b": {"policy": "translate", "english": ["y"]}}},
                                  "dvi2": {"match": "^dvi", "senses": {"c": {"policy": "translate", "english": ["z"]}}}}})
        self.assertEqual(infer_member_term(pol, "yoga"), {"lemma": "yoga", "sense": "system"})
        self.assertIsNone(infer_member_term(pol, "dvija"))          # two rows match: the producer names it
        self.assertIsNone(infer_member_term(pol, "sama"))           # no row


class NamesTests(unittest.TestCase):
    def test_tinanta(self):
        self.assertEqual(N.morph_text(UPASATE), "present indicative, 3rd pl., ātmanepada")
        self.assertIn("jha", N.affix_text(UPASATE))
        self.assertEqual(N.verb_stem(UPASATE), "upa-√ās")
        self.assertEqual(N.dp_id(UPASATE["dhatu"]), "1020011")
        self.assertEqual(N.root_string({**UPASATE["dhatu"], "pada": "A", "artha": "upaveśane"}), "√ās (adādi, 2A, 'upaveśane')")

    def test_subanta_and_pronoun(self):
        a = {"kind": "subanta", "stem": "yuṣmad", "vibhakti": "dvitīyā", "vacana": "ekavacana", "linga": "strīliṅga"}
        self.assertEqual(N.morph_text(a), "acc. sg.")            # personal pronouns carry no gender
        self.assertEqual(N.word_class(a), "pronoun")
        self.assertIn("am (dvitīyā ekavacana)", N.affix_text(a))
        b = {"kind": "krdanta", "stem": "yukta", "krt": "kta", "vibhakti": "Prathama", "vacana": "Bahu", "linga": "Pum"}
        self.assertEqual(N.morph_text(b), "nom. pl. masc. (past participle (niṣṭhā))")
        self.assertEqual(N.form_category(b), "participle_past")


# ---------------------------------------------------------------- 3. stage A on a fixture
class StageATests(TempPipe):
    """Runs stage A for chapter 12 with canned oracle answers (the real gloss lookup, no meaning pages)."""
    def test_fixture_chapter(self):
        from gitapipe import stage_a
        fx = self.pipe / "oracle.json"
        fx.write_text(json.dumps({
            "splits": {"12.1": [{"tokens": ["evam", "satatayuktāḥ", "ye", "bhaktāḥ", "tvām", "paryupāsate", "ye", "ca", "api",
                                            "akṣaram", "avyaktam", "teṣām", "ke", "yogavittamāḥ"]},
                                {"tokens": ["evam", "satatayuktāḥ"]}]},
            "analyses": {"paryupāsate": [{**UPASATE, "id": "a-1", "form": "paryupāsate", "dhatu": {**UPASATE["dhatu"], "upasargas": ["pari", "upa"]}}],
                         "bhaktāḥ": [{"id": "a-2", "form": "bhaktāḥ", "kind": "krdanta", "stem": "bhakta", "krt": "kta", "vibhakti": "prathamā",
                                      "vacana": "bahuvacana", "linga": "puṃliṅga", "source": "vidyut-kosha"}],
                         "ye": [{"id": "a-3", "form": "ye", "kind": "subanta", "stem": "yad", "source": "vidyut-kosha"}]},
            "derivations": {"a-1": {"analysis_id": "a-1", "matches": True, "steps": [{"sutra": "3.4.78", "result": "x"}]}}}))
        m = stage_a.build([12], workers=1, fixture=str(fx), skip_meaning=True, log=lambda *a: None)
        self.assertEqual(m["verses"], 20)
        self.assertEqual(m["secondary_leaks_in_packets"], [])
        p = C.read_json(C.packet_path("12.1"))
        self.assertTrue(p["split_candidates"][0]["recomposes_bori"])
        self.assertFalse(p["split_candidates"][1]["recomposes_bori"])     # a split that drops words does not recompose
        self.assertEqual(p["primary_split"], p["split_candidates"][0]["id"])
        self.assertEqual(p["forms"]["paryupāsate"]["analyses"][0]["id"], "a-1")
        self.assertTrue(any(t["glosses"] for t in p["tokens"]))            # Sanskrit commentators' glosses are in
        self.assertNotIn("english_translations", json.dumps(p))
        sec = C.read_json(self.pipe / "secondaries/12.json")
        self.assertEqual(len(sec["verses"]["12.1"]), 5)                    # the translations go only here
        inv = C.read_json(self.pipe / "packets/inventory.json")
        bh = next(e for e in inv["lemmas"] if e["lemma"] == "bhakta")
        self.assertEqual(bh["occurrences"][0]["at"], "12.1[3]")
        ye = next(e for e in inv["lemmas"] if e["lemma"] == "yad")
        self.assertFalse(ye["content"])
        from gitapipe.store import Store
        self.assertEqual(Store().get("a-1")[1]["steps"][0]["sutra"], "3.4.78")


# ---------------------------------------------------------------- 4. lexicon validator, merge, jobs
def entry(row="testrow", sense="s", english="attend upon", lemma="upāsanā"):
    return {"lemma": lemma, "match": "(^|-)(upās|paryupās)", "senses": [{
        "id": f"{row}.{sense}", "gloss": "to come near and stay at hand", "image": "√ās 'sit' with upa 'near'",
        "preserve": False, "forms": {"verb": english, "noun": "attendance upon"},
        "plain": {"word": english, "locus": "sources/raw/upstream_data/english/webster1913_pg29765.txt:57966"},
        "rich": None, "chosen": "plain", "why": "It keeps nearness and service.", "joycean": None,
        "forbidden": ["worship"], "meaning_lines": [{"cat": "lexical", "text": "to sit near", "who": "Monier-Williams",
                                                     "locus": "sources/raw/upstream_data/kosha/mw.json#42231"}],
        "occurrences": ["12.2", "12.6"]}]}


class LexiconTests(TempPipe):
    def write_lexicon(self, job, entries):
        p = self.pipe / "out/lexicon" / f"{job}.json"
        C.write_json(p, {"schema": C.SCHEMA_LEXICON, "job": job, "entries": entries})
        return p

    def review(self, job, lp, verdict="accept", findings=()):
        p = self.pipe / "out/lexicon-review" / f"lexicon-review-{job}.json"
        C.write_json(p, {"schema": C.SCHEMA_LEXICON_REVIEW, "job": f"lexicon-review-{job}", "lexicon_job": job,
                         "lexicon_sha256": C.sha256_file(lp), "findings": list(findings), "verdict": verdict})
        return p

    def test_lexicon_validator(self):
        good = self.write_lexicon("lexicon-0001", [entry()])
        r = V.validate_lexicon(good)
        self.assertEqual(r.errors, [])
        bad_entries = [
            (lambda e: e["senses"][0].update(id="Bad Id"), "lower-case ASCII"),
            (lambda e: e["senses"][0].update(forms={"verb": "worship"}), "both a form and forbidden"),
            (lambda e: e["senses"][0].update(why="per the policy row"), "pipeline vocabulary"),
            (lambda e: e["senses"][0]["meaning_lines"].append({"cat": "reception", "text": "x", "who": "y"}), "no reception"),
            (lambda e: e["senses"][0].update(gloss="as Gambhirananda has it"), "published translator"),
            (lambda e: e["senses"][0].update(forms={"gerundish": "x"}), "names no grammatical category"),
            (lambda e: e["senses"][0].update(chosen="preserve"), "needs `iast`"),
            (lambda e: e.update(match="zzz"), None),
        ]
        for mutate, msg in bad_entries:
            e = copy.deepcopy(entry())
            mutate(e)
            r = V.validate_lexicon(self.write_lexicon("lexicon-0002", [e]))
            if msg:
                self.assertTrue(any(msg in x for x in r.errors), (msg, r.errors))

    def test_reserved_collision(self):
        pol = L.load_policy(C.POLICY)
        reserved = next(iter((pol.get("reserved_english") or {"wait upon": "other"}).items()), None)
        e = entry(english="yoked")   # 'yoked' is the yukta row's rendering in the current table
        v3, rep = L.merge(pol, [("lexicon A", e, {"job": "A"})])
        self.assertTrue(any(c["english"] == "yoked" for c in rep["conflicts"]), rep["conflicts"])

    def test_merge(self):
        lp = self.write_lexicon("lexicon-0001", [entry()])
        self.review("lexicon-0001", lp)
        lp2 = self.write_lexicon("lexicon-0002", [entry(row="other", english="sit by")])
        self.review("lexicon-0002", lp2, verdict="revise")
        acc = L.accepted_lexicon_outputs()
        self.assertEqual([lx["job"] for _, lx, _ in acc], ["lexicon-0001"])          # the revised batch is not merged
        lp.write_text(lp.read_text() + " ")                                          # edited after review → stale
        self.assertEqual(L.accepted_lexicon_outputs(), [])
        pol = L.load_policy(C.POLICY)
        v3, rep = L.merge(pol, [("lexicon A", entry(), {"job": "A"})])
        self.assertEqual(v3["version"], "3")
        self.assertIn("testrow.s", rep["added_senses"])
        s = v3["lemmas"]["testrow"]["senses"]["s"]
        self.assertEqual(s["status"], "lexicon-reviewed")
        self.assertIn("attends upon", s["forms"]["finite"])                           # inflections admitted
        legacy = pol.get("terms") or pol.get("lemmas")
        for row in legacy:                                                           # every legacy row kept
            self.assertIn(row, v3["lemmas"])
        sts = {x["status"] for r in v3["lemmas"].values() for x in r["senses"].values()}
        self.assertNotIn("proposed", sts)
        self.assertEqual(rep["senses_not_admitted_by_builder"], [])
        b = C.import_builder()
        self.assertEqual(rep["policy_sha256"], b.policy_content_hash(v3))
        legacy_forms = {(r, n): x["iast_forms"] for r, row in legacy.items() for n, x in row["senses"].items() if x.get("iast_forms")}
        restated = [(f"lexicon {r}", {"lemma": r, "match": "x", "senses": [{**entry()["senses"][0], "id": f"{r}.{n}", "preserve": True,
                     "chosen": "preserve", "iast": legacy[r]["senses"][n].get("iast"), "forms": {"noun": "x"}}]}, {"job": r})
                    for (r, n) in legacy_forms]
        v3b, _ = L.merge(pol, restated)
        for (r, n), forms in legacy_forms.items():               # enriching a preserved legacy sense keeps its spellings
            self.assertTrue(set(forms) <= set(v3b["lemmas"][r]["senses"][n].get("iast_forms") or []), (r, n))

    def test_lexicon_review_validator(self):
        lp = self.write_lexicon("lexicon-0001", [entry()])
        rp = self.review("lexicon-0001", lp, verdict="accept",
                         findings=[{"lemma": "upāsanā", "sense": "s", "severity": 1, "check": "tests", "says": "a", "should_be": "b", "evidence": []}])
        r = V.validate_lexicon_review(rp)
        self.assertTrue(any("open S1" in e for e in r.errors))
        lp.write_text(lp.read_text() + " ")
        self.assertTrue(any("lexicon_sha256" in e for e in V.validate_lexicon_review(rp).errors))

    def test_lexicon_jobs(self):
        import build_jobs as BJ
        inv = {"policy_sha256": "x", "lemmas": [
            {"key": f"l{k}", "lemma": f"l{k}", "roots": [], "forms": [f"l{k}"], "verses": ["2.1"], "occurrences": [{"at": "2.1[0]"}],
             "frequency": 3, "weight": 3 - k / 100, "rows": ["yoga"] if k < 3 else [], "glossary_key": None, "prior_renderings": [],
             "meaning_page": "x", "system": k < 3, "in_lexicon_scope": k != 5} for k in range(20)]}
        C.write_json(self.pipe / "packets/inventory.json", inv)
        jobs = BJ.lexicon_jobs(8)
        lex = [j for j in jobs if j["type"] == "lexicon"]
        self.assertEqual(len(lex), 3)                                     # 19 lemmas in scope, ≤ 8 per batch
        first = C.read_json(C.ROOT / lex[0]["inputs"][0])
        self.assertEqual([x["lemma"] for x in first["lemmas"]][:3], ["l0", "l1", "l2"])   # one row's lemmas together, first
        rv = [j for j in jobs if j["type"] == "lexicon-review"]
        self.assertEqual(rv[0]["depends_on"], ["lexicon-0001"])
        self.assertEqual(rv[0]["validate"], f"python3 scripts/gita/validate_job.py lexicon-review {C.rel(self.pipe / 'out/lexicon-review/lexicon-review-0001.json')}")

    def test_acceptance_namespace(self):
        import build_jobs as BJ
        inv = {"policy_sha256": "x", "lemmas": [
            {"key": l, "lemma": l, "roots": [], "forms": [l], "verses": [v], "occurrences": [{"at": v + "[0]"}], "frequency": 3,
             "weight": 3, "rows": [], "glossary_key": None, "prior_renderings": [], "meaning_page": "x", "system": False,
             "in_lexicon_scope": True} for l, v in (("a", "12.1"), ("b", "2.1"), ("c", "12.4"))]}
        C.write_json(self.pipe / "packets/inventory.json", inv)
        C.set_namespace("ch12")
        try:
            jobs = BJ.lexicon_jobs(12, chapter=12)
            lex = [j for j in jobs if j["type"] == "lexicon"]
            self.assertEqual([j["id"] for j in lex], ["acc12-lexicon-0001"])
            lemmas = [x["lemma"] for x in C.read_json(C.ROOT / lex[0]["inputs"][0])["lemmas"]]
            self.assertEqual(lemmas, ["a", "c"])                                   # only chapter 12's lemmas
            self.assertIn("acceptance/ch12/out/lexicon/", lex[0]["output"])
            self.assertTrue(C.in_namespace("acc12-verse-12-01") and not C.in_namespace("verse-02-01"))
            self.assertEqual(C.chapter_of_job("acc12-review-12-03-r1"), 12)
        finally:
            C.set_namespace(None)
        self.assertFalse(C.in_namespace("acc12-verse-12-01"))

    def test_inline(self):
        ok = {"i": 0, "sense": None, "english": "deft", "why": "the commentators gloss it as skilful",
              "image": "√daks 'be able'", "plain": {"word": "deft", "locus": "sources/raw/upstream_data/english/webster1913_pg29765.txt:1"},
              "rich": None, "chosen": "plain",
              "meaning_lines": [{"cat": "lexical", "text": "able, skilful", "who": "Monier-Williams", "locus": "sources/raw/upstream_data/kosha/mw.json#1"}]}
        r = V.Result()
        V.check_inline(r, "w", ok)
        self.assertEqual(r.errors, [])
        for k, val, msg in (("image", None, "`image`"), ("plain", None, "`plain`"), ("chosen", "preserve", "always translated"),
                            ("meaning_lines", [], "1–4 lines")):
            r = V.Result()
            V.check_inline(r, "w", {**ok, k: val})
            self.assertTrue(any(msg in e for e in r.errors), (k, r.errors))
        man = {"manual": {"form": "dakṣaḥ", "kind": "subanta", "stem": "dakṣa", "dhatu": None, "source": "manual"}}
        vo = lambda job, loc, eng: (job, {"job": job, "verses": [{"locus": loc, "padas": ["dakṣaḥ"],  # noqa: E731
                                                                  "words": [{**ok, "english": eng, "analysis": man}]}]})
        same = L.inline_entries([vo("verse-12-03", "12.16", "deft"), vo("verse-02-01", "2.50", "deft")])
        self.assertEqual(len(same), 1)
        self.assertFalse(same[0]["divergent"])
        self.assertEqual(sorted(same[0]["senses"][0]["occurrences"]), ["12.16:0", "2.50:0"])
        self.assertEqual(same[0]["senses"][0]["id"], "daksa.deft")
        div = L.inline_entries([vo("verse-12-03", "12.16", "deft"), vo("verse-02-01", "2.50", "skilful")])
        self.assertTrue(div[0]["divergent"])                                       # → a lexicon job, not a pick


# ---------------------------------------------------------------- 5. verse and review validators, round trip (stage A)
@unittest.skipUnless(HAVE_CH12, "stage A products for chapter 12 absent")
class Chapter12Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import convert_ch12
        cls.rt_dir = REAL_PIPE / "roundtrip-ch12"
        cls.report = convert_ch12.roundtrip(cls.rt_dir)

    def test_roundtrip_accepted(self):
        r = self.report
        self.assertEqual(r["lines_identical"], "20/20")
        self.assertEqual(r["error_classes_not_in_baseline"], {})
        self.assertEqual(r["expansion_errors"], [])
        for f in ("iast", "deva", "term", "word_class", "compound.type", "compound.members"):
            self.assertEqual(r["identity_fields_equal"][f], "244/244", f)
        self.assertTrue(r["accepted"])

    def mutated(self, fn):
        vo = C.read_json(self.rt_dir / "verse-12-1-5.json")
        fn(vo)
        p = self.rt_dir / "mutated.json"
        C.write_json(p, vo)
        return V.validate_verse(p, run_builder=False).errors

    def test_verse_rejections(self):
        def drop(vo):
            vo["verses"][0]["padas"][1] = "satata"          # a whole member dropped
        self.assertTrue(any("recompose" in e for e in self.mutated(drop)))

        def unknown(vo):
            vo["verses"][0]["words"][3]["analysis"] = "g-0000000000000000"
        self.assertTrue(any("not among the packet's analyses" in e for e in self.mutated(unknown)))

        def sense(vo):
            vo["verses"][0]["words"][3]["sense"] = "nosuch.sense"
        self.assertTrue(any("not in the lexicon" in e for e in self.mutated(sense)))

        def slot(vo):
            vo["verses"][0]["line"] = vo["verses"][0]["line"].replace("{3:bhaktas}", "bhaktas")
        self.assertTrue(any("not slotted" in e for e in self.mutated(slot)))

        def jargon(vo):
            vo["verses"][0]["sense"] = "The policy row decides this."
        self.assertTrue(any("pipeline vocabulary" in e for e in self.mutated(jargon)))

    def test_review_validator(self):
        vp = self.rt_dir / "verse-12-1-5.json"
        if not vp.is_file():
            self.skipTest("converted output absent")
        saved = C.PIPE
        tmp = Path(tempfile.mkdtemp(dir=REAL_PIPE / "private" if (REAL_PIPE / "private").is_dir() else REAL_PIPE))
        try:
            C.PIPE = tmp
            C.write_json(tmp / "jobs/review/review-12-01.input.json", {"verse_output": C.rel(vp)})
            vo = C.read_json(vp)
            good = {"schema": C.SCHEMA_REVIEW, "job": "review-12-01", "shard_sha256": C.sha256_file(vp),
                    "findings": [{"locus": "12.1", "word_i": 3, "severity": 2, "check": "meaning", "says": "a", "should_be": "b", "evidence": []}],
                    "blind_secondary_check": [{"locus": v["locus"], "construal_missed": None} for v in vo["verses"]],
                    "readers_will_meet": [{"locus": "12.1", "word_i": 3, "renderings": [{"who": "X", "word": "devotees"}]}],
                    "verdict": "accept"}
            rp = tmp / "review.json"
            C.write_json(rp, good)
            self.assertEqual(V.validate_review(rp).errors, [])
            for mutate, msg in ((lambda d: d["findings"][0].update(severity=1), "open S1"),
                                (lambda d: d.update(shard_sha256="0" * 64), "shard_sha256"),
                                (lambda d: d["blind_secondary_check"].pop(), "one entry per verse"),
                                (lambda d: d["findings"][0].update(check="taste"), "check must be")):
                d = copy.deepcopy(good)
                mutate(d)
                C.write_json(rp, d)
                self.assertTrue(any(msg in e for e in V.validate_review(rp).errors), msg)
        finally:
            C.PIPE = saved
            shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- 6. deploy: a batch of chapters + the whole-Gītā article
@unittest.skipUnless(shutil.which("git") and shutil.which("node"), "git and node required")
class DeployBatchTests(unittest.TestCase):
    def run_(self, *a, cwd, env=None, check=True):
        r = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True, env=env)
        if check and r.returncode != 0:
            raise AssertionError(f"{a}: {r.stdout}{r.stderr}")
        return r

    def test_batch_and_whole_gita_in_one_commit(self):
        import os
        tmp = Path(tempfile.mkdtemp(prefix="gita-deploy-batch-"))
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        try:
            seed, origin, work = tmp / "seed", tmp / "origin.git", tmp / "work"
            (seed / "assets").mkdir(parents=True)
            (seed / "assets/app.js").write_text('const GITA_READINGS = {\n  "yogavasistha-dama": {\n  },\n};\n')
            (seed / "data/articles").mkdir(parents=True)
            (seed / "data/articles/manifest.json").write_text(json.dumps({"articles": [{"slug": "gita-ch5"}]}))
            (seed / "scripts").mkdir()
            (seed / "scripts/run_checks.sh").write_text("exit 0\n")
            self.run_("git", "init", "-q", "-b", "main", cwd=seed)
            self.run_("git", "add", ".", cwd=seed)
            self.run_("git", "commit", "-q", "-m", "seed", cwd=seed, env=env)
            self.run_("git", "clone", "-q", "--bare", str(seed), str(origin), cwd=tmp)
            self.run_("git", "clone", "-q", str(origin), str(work), cwd=tmp)
            for f in ("deploy_gita_chapter.sh", "build_gita_chapter_reader.py"):
                shutil.copy(C.ROOT / "scripts" / f, work / "scripts" / f)
            shutil.copytree(C.GITA_SCRIPTS, work / "scripts/gita", ignore=shutil.ignore_patterns("__pycache__", "tests"))
            for n in (98, 99):
                (work / f"gita/ch{n}").mkdir(parents=True)
                (work / f"gita/ch{n}/verses.js").write_text(f"/* GENERATED by\n   scripts/build_gita_chapter_reader.py */\nwindow.CH{n}_VERSES = [{{\"locus\": \"{n}.1\"}}];\n")
                (work / f"gita/ch{n}/index.html").write_text("<html></html>")
            (work / "data/glossary").mkdir(parents=True)
            shutil.copy(C.POLICY, work / "data/glossary/term_policy.json")
            e = dict(env, DEPLOY_REMOTE_URL=str(origin), DEPLOY_SKIP_BUILD="1", DEPLOY_CHECKS="exit 0")
            r = self.run_("sh", "scripts/deploy_gita_chapter.sh", "98,99", "Gītā 98, 99: test", "--whole-gita", cwd=work, env=e, check=False)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            wt = Path(next(l.split("'")[1] for l in r.stdout.splitlines() if "push" in l and "-C" in l))
            files = sorted(self.run_("git", "show", "--name-only", "--format=", "HEAD", cwd=wt).stdout.split())
            self.assertEqual(files, ["assets/app.js", "data/articles/manifest.json", "data/glossary/term_policy.json",
                                     "gita/bhagavad-gita/chapters.js", "gita/bhagavad-gita/index.html", "gita/bhagavad-gita/reader.js",
                                     "gita/ch98/index.html", "gita/ch98/verses.js", "gita/ch99/index.html", "gita/ch99/verses.js"])
            app = (wt / "assets/app.js").read_text()
            for k in ('"gita-ch98"', '"gita-ch99"', '"bhagavad-gita"'):
                self.assertIn(k, app)
            self.assertEqual(self.run_("git", "rev-list", "--count", "HEAD", cwd=wt).stdout.strip(), "2")   # one commit on the seed
            self.assertEqual(self.run_("git", "rev-parse", "main", cwd=origin).stdout.strip(),
                             self.run_("git", "rev-parse", "HEAD~1", cwd=wt).stdout.strip(), "nothing pushed")
        finally:
            for line in self.run_("git", "worktree", "list", "--porcelain", cwd=tmp / "work", check=False).stdout.splitlines():
                if line.startswith("worktree ") and Path(line[9:]) != tmp / "work":
                    self.run_("git", "worktree", "remove", "--force", line[9:], cwd=tmp / "work", check=False)
            shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- 7. whole-Gītā article
class WholeGitaTests(unittest.TestCase):
    def test_index_and_registration(self):
        import build_whole_gita as W
        root = Path(tempfile.mkdtemp())
        try:
            (root / "gita/ch12").mkdir(parents=True)
            (root / "gita/ch5").mkdir(parents=True)
            (root / "gita/ch12/verses.js").write_text("/* GENERATED by\n   scripts/build_gita_chapter_reader.py */\nwindow.CH12_VERSES = [];\n")
            (root / "gita/ch12/audio.js").write_text("window.CH12_AUDIO = null;\n")
            (root / "gita/ch5/verses.js").write_text("/* hand-made */ window.CH5_VERSES = [];\n")
            (root / "assets").mkdir()
            app = subprocess.run(["git", "show", "HEAD:assets/app.js"], cwd=C.ROOT, capture_output=True, text=True).stdout
            (root / "assets/app.js").write_text(app)
            (root / "data/articles").mkdir(parents=True)
            (root / "data/articles/manifest.json").write_text(json.dumps({"articles": [{"slug": "gita-ch12"}]}))
            for _ in range(2):
                chs = W.write(root, False)
                W.register(root, chs)
            self.assertEqual([c["n"] for c in chs if c["available"]], [12])
            self.assertEqual(next(c for c in chs if c["n"] == 12)["files"], ["verses.js", "audio.js"])
            s = (root / "assets/app.js").read_text()
            self.assertEqual(s.count('"bhagavad-gita": {'), 1)
            man = json.loads((root / "data/articles/manifest.json").read_text())
            self.assertEqual([a["slug"] for a in man["articles"]].count("bhagavad-gita"), 1)
            self.assertEqual(next(a for a in man["articles"] if a["slug"] == "bhagavad-gita")["status"], "provisional")
            for f in ("gita/bhagavad-gita/reader.js", "gita/bhagavad-gita/chapters.js", "assets/app.js"):
                r = subprocess.run(["node", "--check", str(root / f)], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(sum(c["verses"] for c in chs), 700)
        finally:
            shutil.rmtree(root)


if __name__ == "__main__":
    unittest.main()

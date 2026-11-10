"""runner.py (Codex / Claude backends) and book.py (the whole-book driver), without model calls."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import book  # noqa: E402
import runner  # noqa: E402


class Runner(unittest.TestCase):
    def test_claude_is_tool_free_and_inlines_files(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "input.json"
            f.write_text('{"w": 1}')
            done = subprocess.CompletedProcess([], 0, json.dumps({"result": '{"ok": 1}', "usage": {"output_tokens": 3}}), "")
            with mock.patch.object(runner.subprocess, "run", return_value=done) as m:
                r = runner._claude("PROMPT", {"input.json": f}, None)
            args, kw = m.call_args
            cmd = args[0]
            self.assertEqual(cmd[cmd.index("--tools") + 1], "")
            self.assertIn("--strict-mcp-config", cmd)
            self.assertIn('==== FILE input.json ====\n{"w": 1}', kw["input"])
            self.assertEqual(r.raw, '{"ok": 1}')

    def test_backend_error_is_not_an_answer(self):
        done = subprocess.CompletedProcess([], 2, "", "Account Control: not starting")
        with mock.patch.object(runner.subprocess, "run", return_value=done):
            r = runner._claude("P", {}, None)
        self.assertEqual(r.raw, "")
        self.assertIn("Account Control", r.usage["error"])

    def test_unknown_backend(self):
        with mock.patch.object(runner, "RUNNER", "other"):
            with self.assertRaises(SystemExit):
                runner.run("x", Path("."))


class Book(unittest.TestCase):
    def test_chapters(self):
        self.assertEqual(book.chapters("1-3,12,15"), [1, 2, 3, 12, 15])
        self.assertEqual(book.chapters("18"), [18])
        with self.assertRaises(SystemExit):
            book.chapters("0-2")
        with self.assertRaises(SystemExit):
            book.chapters("19")

    def test_construe_done_needs_every_verse_accepted(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(book, "RUNS", Path(d)):
            for v in range(1, 21):
                p = Path(d) / "r" / "construe" / f"15.{v}"
                p.mkdir(parents=True)
                (p / "record.json").write_text(json.dumps({"accepted": v != 7}))
            self.assertFalse(book.done("r", "construe", 15))
            (Path(d) / "r/construe/15.7/record.json").write_text('{"accepted": true}')
            self.assertTrue(book.done("r", "construe", 15))


if __name__ == "__main__":
    unittest.main()


import mbh_usage as U  # noqa: E402


class MbhUsage(unittest.TestCase):
    def test_norm_removes_final_sandhi_and_restores_avagraha(self):
        M = U._kit()
        self.assertEqual(U.norm("bhaktāś"), M.fold("BaktAH"))
        self.assertEqual(U.norm("bhaktāḥ"), U.norm("bhaktāś"))
        self.assertEqual(U.norm("'bhavat"), U.norm("abhavat"))

    def test_usage_counts_whole_words_outside_the_gita(self):
        idx = {U.norm("bhaktāḥ"): ["3.1.1a", "6.30.14c"], U.norm("bhaktam"): ["12.2.3c", "3.1.1a"]}
        U.forms.cache_clear(); U.tokens.cache_clear(); U.lines.cache_clear()
        with mock.patch.object(U, "forms", lambda: {"bhakta": {"forms": ["BaktAH", "Baktam"], "ambiguous": []}}), \
                mock.patch.object(U, "tokens", lambda: idx), \
                mock.patch.object(U, "lines", lambda: {"3.1.1a": "x", "12.2.3c": "y"}):
            u = U.usage("bhakta")
        self.assertEqual(u["lines"], 2)
        self.assertEqual(u["gita_lines"], 1)
        self.assertEqual(u["by_parvan"], {"3": 1, "12": 1})
        with mock.patch.object(U, "forms", lambda: {}), mock.patch.object(U, "tokens", lambda: idx):
            self.assertIsNone(U.usage("bhakta"))

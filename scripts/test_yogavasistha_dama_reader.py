#!/usr/bin/env python3
"""Dāma reader merge and fail-closed contract tests."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_yogavasistha_dama_reader as builder
import validate_yogavasistha_dama_reader as validator


def word() -> dict:
    return {
        "i": 0,
        "deva": "पदम्",
        "iast": "padam",
        "gloss": "word",
        "parts": [{"form": "pada", "gloss": "word"}, {"form": "am", "gloss": "accusative singular"}],
        "stem": "pada",
        "root": None,
        "affix": "am (dvitīyā ekavacana)",
        "morph": "accusative singular neuter",
        "karaka": "karman",
        "compound": None,
        "glossaryKey": None,
        "translatable": True,
    }


def source_packet() -> dict:
    units = [
        {
            "id": item_id,
            "verse": verse,
            "deva": "पदम् ||",
            "iast": "padam ||",
        }
        for verse, item_id in zip(range(builder.FIRST_VERSE, builder.LAST_VERSE + 1), builder.EXPECTED_IDS)
    ]
    return {
        "schema_version": "laghuyogavasistha-source-packet-v1",
        "population": {
            "first_id": builder.EXPECTED_IDS[0],
            "last_id": builder.EXPECTED_IDS[-1],
            "expected_units": 56,
            "observed_units": 56,
        },
        "work": "Laghu-Yoga-Vāsiṣṭha",
        "section": "test",
        "controlling_witness": {"edition": "test witness"},
        "parallel_witnesses": [],
        "units": units,
        "textual_notes": [
            {
                "unit_id": "lyv-4-2-33",
                "printed_and_transcribed": "mīmabhāsa-",
                "parallel_reading": "bhīmabhāsa-",
                "policy": "preserve the controlling reading",
            }
        ],
        "apparatus": [
            {
                "id": "robot-reading",
                "attach_after": "lyv-4-2-64",
                "critical_locus": "MU test",
                "issue": "test variant",
            },
            {
                "id": "construction-cluster",
                "attach_after": "lyv-4-2-46",
                "critical_loci": ["MU test"],
                "issue": "test omission",
            },
        ],
    }


def producer_packet(first: int, last: int, source: dict) -> dict:
    source_by_id = {unit["id"]: unit for unit in source["units"]}
    units = []
    for verse in range(first, last + 1):
        item_id = f"lyv-4-2-{verse}"
        source_unit = source_by_id[item_id]
        units.append(
            {
                "id": item_id,
                "source_id": item_id,
                "locus": f"test {verse}",
                "speaker": "Vasiṣṭha",
                "devanagari": source_unit["deva"],
                "iast": source_unit["iast"],
                "english": "{0:word}",
                "sense": "word",
                "grammar": {"karakaSummary": "test syntax", "verbalModality": "nominal"},
                "words": [word()],
                "apparatus": [],
            }
        )
    return {
        "schema_version": builder.PRODUCER_SCHEMA,
        "range": {
            "first_id": f"lyv-4-2-{first}",
            "last_id": f"lyv-4-2-{last}",
            "expected_units": last - first + 1,
            "observed_units": last - first + 1,
        },
        "evidence": {
            "text_witness": "synthetic test witness",
            "grammar_witnesses": ["synthetic grammar witness"],
            "review_method": "direct test fixture",
        },
        "units": units,
    }


class DamaReaderContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = source_packet()
        self.source_path = self.root / "source.json"
        self.producers = [
            producer_packet(first, last, self.source) for first, last in builder.EXPECTED_RANGES
        ]
        self.producer_paths = [self.root / f"producer-{first}-{last}.json" for first, last in builder.EXPECTED_RANGES]

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self) -> None:
        self.source_path.write_text(json.dumps(self.source, ensure_ascii=False), encoding="utf-8")
        for path, packet in zip(self.producer_paths, self.producers):
            path.write_text(json.dumps(packet, ensure_ascii=False), encoding="utf-8")

    @staticmethod
    def root_record() -> dict:
        return {
            "form": "√bhū",
            "gana": "bhvādi (1)",
            "pada": "parasmaipada",
            "gloss": "to be, become",
            "dhatupatha": {
                "locus": "01.0001",
                "aupadeshika_devanagari": "भू",
                "artha_sanskrit": "सत्तायाम्",
            },
        }

    def test_complete_merge_resolves_registries_and_attaches_evidence(self) -> None:
        packet = self.producers[0]
        packet["root_evidence"] = {"bhu-01.0001": self.root_record()}
        packet["grammar_evidence"] = {
            "sup": {"locus": "Aṣṭādhyāyī 4.1.2", "claim": "sup endings"}
        }
        first_word = packet["units"][0]["words"][0]
        first_word.pop("root")
        first_word["root_ref"] = "bhu-01.0001"
        first_word["rule_refs"] = ["sup"]
        self.write()

        payload = builder.build_payload(self.source_path, self.producer_paths)
        self.assertEqual([unit["id"] for unit in payload["units"]], list(builder.EXPECTED_IDS))
        self.assertEqual(payload["units"][0]["words"][0]["root"]["form"], "√bhū")
        self.assertIn("sup", payload["units"][0]["words"][0]["evidence"]["grammar_records"])
        self.assertEqual(payload["units"][2]["textualNotes"][0]["unit_id"], "lyv-4-2-33")
        self.assertEqual(payload["units"][15]["apparatusAfter"][0]["id"], "construction-cluster")
        self.assertEqual(payload["units"][33]["apparatusAfter"][0]["id"], "robot-reading")
        self.assertEqual(payload["units"][0]["sourceSegments"][0], {"text": "पदम्", "word_indices": [0]})
        self.assertEqual(
            "".join(segment["text"] for segment in payload["units"][0]["sourceSegments"]),
            payload["units"][0]["devanagari"],
        )

    def test_legacy_embedded_root_evidence_is_normalized(self) -> None:
        first_word = self.producers[0]["units"][0]["words"][0]
        first_word.update(
            {
                "root": "√bhū",
                "rootGloss": "to be, become",
                "rootEvidence": {
                    "locus": "01.0001",
                    "aupadeshika": "भू",
                    "artha": "सत्तायाम्",
                    "gana": "bhvādi (1)",
                    "pada": "parasmaipada",
                },
            }
        )
        self.write()
        payload = builder.build_payload(self.source_path, self.producer_paths)
        root = payload["units"][0]["words"][0]["root"]
        self.assertEqual(root["dhatupatha"]["aupadeshika_devanagari"], "भू")

    def test_dangling_root_reference_fails(self) -> None:
        self.producers[0]["units"][0]["words"][0]["root_ref"] = "missing-root"
        self.write()
        with self.assertRaisesRegex(builder.BuildError, "dangling root-evidence reference"):
            builder.build_payload(self.source_path, self.producer_paths)

    def test_dangling_grammar_reference_fails(self) -> None:
        self.producers[0]["units"][0]["words"][0]["grammar_ref"] = "missing-rule"
        self.write()
        with self.assertRaisesRegex(builder.BuildError, "dangling grammar-evidence reference"):
            builder.build_payload(self.source_path, self.producer_paths)

    def test_missing_producer_unit_fails(self) -> None:
        self.producers[2]["units"].pop()
        self.write()
        with self.assertRaisesRegex(builder.BuildError, "ID population mismatch"):
            builder.build_payload(self.source_path, self.producer_paths)

    def test_source_replay_difference_fails(self) -> None:
        self.producers[1]["units"][0]["iast"] = "silently changed"
        self.write()
        with self.assertRaisesRegex(builder.BuildError, "exactly replay"):
            builder.build_payload(self.source_path, self.producer_paths)

    def test_source_word_omission_fails_alignment(self) -> None:
        self.producers[0]["units"][0]["words"] = []
        self.write()
        with self.assertRaisesRegex(builder.BuildError, "non-empty list"):
            builder.build_payload(self.source_path, self.producer_paths)

    def test_duplicate_english_word_slot_fails(self) -> None:
        self.producers[0]["units"][0]["english"] = "{0:word} {0:again}"
        self.write()
        with self.assertRaisesRegex(builder.BuildError, "exactly once"):
            builder.build_payload(self.source_path, self.producer_paths)

    def test_generated_artifacts_round_trip_and_stale_edit_fails(self) -> None:
        self.write()
        payload = builder.build_payload(self.source_path, self.producer_paths)
        output_dir = self.root / "reader"
        output_dir.mkdir()
        for name, rendered in builder.generated_artifacts(payload).items():
            (output_dir / name).write_text(rendered, encoding="utf-8")
        validator.validate_artifacts(output_dir, payload)
        verses_path = output_dir / "verses.js"
        verses_path.write_text(
            verses_path.read_text(encoding="utf-8").replace("window.YV_DAMA_VERSES", "window.WRONG"),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(builder.BuildError, "stale"):
            validator.validate_artifacts(output_dir, payload)

    def test_index_is_redirect_only_not_a_bespoke_reader(self) -> None:
        index = builder.render_index_html()
        self.assertIn('../../#/article/yogavasistha-dama', index)
        self.assertNotIn("<style", index)
        self.assertNotIn("GitaReader", index)
        self.assertNotIn("YV_DAMA_VERSES", index)


if __name__ == "__main__":
    unittest.main()

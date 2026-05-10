"""Mocked-engine consensus tests — no GPU needed."""

from __future__ import annotations

import sys
from pathlib import Path


# Make the package importable when running pytest from repo root.
_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


from philosophy_ocr.consensus import consensus_for_page, render_agreement_table  # noqa: E402
from philosophy_ocr.qwen_vl_runner import VLMPageResult  # noqa: E402
from philosophy_ocr.surya_runner import SuryaLine  # noqa: E402


def _surya(text: str, conf: float, idx: int) -> SuryaLine:
    return SuryaLine(text=text, bbox=(0.0, idx * 10.0, 100.0, (idx + 1) * 10.0), confidence=conf)


def _vlm(devanagari: str) -> VLMPageResult:
    return VLMPageResult(devanagari=devanagari, iast="")


def test_three_way_pass_all_agree() -> None:
    surya = [_surya("धर्मक्षेत्रे", 0.95, 0)]
    qwen = _vlm("धर्मक्षेत्रे")
    intern = _vlm("धर्मक्षेत्रे")
    out = consensus_for_page(surya, qwen, intern)
    assert len(out) == 1
    assert out[0].verdict == "PASS"


def test_split_one_disagrees() -> None:
    surya = [_surya("धर्मक्षेत्रे", 0.95, 0)]
    qwen = _vlm("धर्मक्षेत्रे")
    intern = _vlm("कुरुक्षेत्रे")  # very different
    out = consensus_for_page(surya, qwen, intern)
    assert out[0].verdict == "SPLIT"


def test_disagree_when_both_vlms_diverge() -> None:
    surya = [_surya("धर्मक्षेत्रे", 0.95, 0)]
    qwen = _vlm("कुरुक्षेत्रे")
    intern = _vlm("पाण्डवाश्चैव")
    out = consensus_for_page(surya, qwen, intern)
    assert out[0].verdict == "DISAGREE"


def test_low_conf_flag() -> None:
    surya = [_surya("धर्मक्षेत्रे", 0.30, 0)]  # below floor
    qwen = _vlm("धर्मक्षेत्रे")
    intern = _vlm("धर्मक्षेत्रे")
    out = consensus_for_page(surya, qwen, intern)
    assert out[0].verdict == "LOW_CONF"


def test_render_table_shape() -> None:
    surya = [_surya("a", 0.9, 0), _surya("b", 0.9, 1)]
    qwen = _vlm("a\nb")
    intern = _vlm("a\nb")
    table = render_agreement_table(consensus_for_page(surya, qwen, intern))
    assert table.startswith("| line |")
    assert table.count("\n") >= 3  # header + sep + 2 rows

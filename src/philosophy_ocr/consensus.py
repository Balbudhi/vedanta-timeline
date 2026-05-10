"""Three-engine line-level consensus.

For each Surya line, find the best-matching span in each VLM transcript by
Devanāgarī Levenshtein (rapidfuzz). Per-line agreement is reported against
both VLMs and a three-way vote yields ``PASS / SPLIT / DISAGREE`` per line.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .config import CONSENSUS_AGREEMENT_THRESHOLD, SURYA_CONFIDENCE_FLOOR
from .qwen_vl_runner import VLMPageResult
from .surya_runner import SuryaLine


ConsensusVerdict = Literal["PASS", "SPLIT", "DISAGREE", "LOW_CONF"]


@dataclass(frozen=True)
class LineConsensus:
    line_id: int
    surya_text: str
    surya_confidence: float
    qwen_match: str
    qwen_score: float
    internvl_match: str
    internvl_score: float
    verdict: ConsensusVerdict


def _split_lines(devanagari: str) -> list[str]:
    return [line.strip() for line in devanagari.splitlines() if line.strip()]


def _best_match(needle: str, haystack: list[str]) -> tuple[str, float]:
    """Return (best line, score in [0,1]) using rapidfuzz ratio."""

    if not haystack:
        return "", 0.0
    try:
        from rapidfuzz import fuzz, process
    except ImportError:  # pragma: no cover
        # Pure-Python fallback (slow but correct enough for tests).
        best, best_score = "", 0.0
        for cand in haystack:
            common = sum(1 for a, b in zip(needle, cand) if a == b)
            denom = max(len(needle), len(cand), 1)
            score = common / denom
            if score > best_score:
                best, best_score = cand, score
        return best, best_score
    match = process.extractOne(needle, haystack, scorer=fuzz.ratio)
    if not match:
        return "", 0.0
    text, score, _ = match
    return text, float(score) / 100.0


def consensus_for_page(
    surya_lines: list[SuryaLine],
    qwen: VLMPageResult,
    internvl: VLMPageResult,
    *,
    threshold: float = CONSENSUS_AGREEMENT_THRESHOLD,
    surya_floor: float = SURYA_CONFIDENCE_FLOOR,
) -> list[LineConsensus]:
    qwen_lines = _split_lines(qwen.devanagari)
    intern_lines = _split_lines(internvl.devanagari)

    out: list[LineConsensus] = []
    for idx, surya in enumerate(surya_lines):
        qm, qs = _best_match(surya.text, qwen_lines)
        im, is_ = _best_match(surya.text, intern_lines)
        if surya.confidence < surya_floor:
            verdict: ConsensusVerdict = "LOW_CONF"
        elif qs >= threshold and is_ >= threshold:
            verdict = "PASS"
        elif qs >= threshold or is_ >= threshold:
            verdict = "SPLIT"
        else:
            verdict = "DISAGREE"
        out.append(
            LineConsensus(
                line_id=idx,
                surya_text=surya.text,
                surya_confidence=surya.confidence,
                qwen_match=qm,
                qwen_score=qs,
                internvl_match=im,
                internvl_score=is_,
                verdict=verdict,
            )
        )
    return out


def render_agreement_table(consensus: list[LineConsensus]) -> str:
    """Human-readable Markdown table for the smoke report."""

    rows = [
        "| line | verdict | surya conf | qwen | internvl | surya_text |",
        "|---:|:---|---:|---:|---:|:---|",
    ]
    for c in consensus:
        rows.append(
            f"| {c.line_id} | {c.verdict} | {c.surya_confidence:.2f} "
            f"| {c.qwen_score:.2f} | {c.internvl_score:.2f} "
            f"| {c.surya_text[:60]} |"
        )
    return "\n".join(rows)

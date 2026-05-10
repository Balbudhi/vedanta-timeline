"""Layer-3 dispatch to Codex 5.4 reasoning=high for OCR disagreements.

Stub for v0.1: builds the prompt and invokes ``codex exec`` via subprocess so
the smoke test can show the wiring without making real API calls. Wire to the
real call site in a follow-up commit once smoke results justify it.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


JudgeVerdict = Literal["CONFIRM-OCR", "CORRECT-TO", "UNREADABLE", "NEEDS-HUMAN"]


@dataclass(frozen=True)
class JudgeRequest:
    page_image: Path
    surya_text: str
    qwen_text: str
    internvl_text: str
    flagged_token: str


@dataclass(frozen=True)
class JudgeResponse:
    verdict: JudgeVerdict
    correction: str | None
    rationale: str


def build_prompt(req: JudgeRequest) -> str:
    return (
        "You are judging an OCR three-engine disagreement on a Sanskrit page. "
        f"Engines disagree on the token `{req.flagged_token}`. "
        f"Surya proposed: `{req.surya_text}`. "
        f"Qwen2.5-VL proposed: `{req.qwen_text}`. "
        f"InternVL-2.5 proposed: `{req.internvl_text}`. "
        "Look at the page image (attached) and return JSON "
        "{verdict: 'CONFIRM-OCR'|'CORRECT-TO'|'UNREADABLE'|'NEEDS-HUMAN', "
        "correction: string|null, rationale: string}."
    )


def invoke_judge(req: JudgeRequest, *, dry_run: bool = True) -> JudgeResponse:
    if dry_run:
        return JudgeResponse(
            verdict="NEEDS-HUMAN",
            correction=None,
            rationale="dry-run: judge not invoked.",
        )
    prompt = build_prompt(req)
    proc = subprocess.run(
        [
            "codex", "exec",
            "--skip-git-repo-check", "--json",
            "-c", 'model="gpt-5.4"',
            "-c", 'model_reasoning_effort="high"',
            "-c", 'service_tier="fast"',
            prompt,
        ],
        capture_output=True,
        text=True,
        timeout=600,
    )
    # TODO: parse codex JSON envelope; for now treat any nonzero exit as NEEDS-HUMAN.
    if proc.returncode != 0:
        return JudgeResponse(
            verdict="NEEDS-HUMAN", correction=None, rationale=proc.stderr[:500]
        )
    return JudgeResponse(
        verdict="CONFIRM-OCR",
        correction=None,
        rationale=proc.stdout[:500],
    )

"""Three-engine Sanskrit OCR + verifier pipeline.

Scaffolded 2026-05-10 for the Phase-C smoke test. The package wraps Surya
line-OCR, Qwen2.5-VL-72B-AWQ, and InternVL2.5-78B-AWQ (Lipikar substitute) into
a three-way consensus, then runs Pāṇinian lexical verification via
``prakriya.ocr_api`` and a Codex-5.4 judge for residual disagreements.
"""

from __future__ import annotations

__version__ = "0.1.0"

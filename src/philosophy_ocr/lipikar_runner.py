"""Lipikar runner — stub that activates if ``LIPIKAR_HOME`` env var is set.

Lipikar is the IIT Delhi closed-source Sanskrit OCR. Until a binary bundle is
obtained, this module is a stub: ``available()`` returns False and ``run_lipikar``
raises. The pipeline uses :mod:`philosophy_ocr.internvl_runner` as a substitute.
"""

from __future__ import annotations

import os
from pathlib import Path

from .qwen_vl_runner import VLMPageResult


def available() -> bool:
    home = os.environ.get("LIPIKAR_HOME")
    return bool(home and Path(home).exists())


def run_lipikar(image_path: Path) -> VLMPageResult:  # pragma: no cover
    if not available():
        raise RuntimeError(
            "Lipikar binary not available; set LIPIKAR_HOME to a valid install."
        )
    raise NotImplementedError(
        "Lipikar wrapper unimplemented. Wire up once IIT Delhi bundle arrives."
    )

"""InternVL-2.5-78B-AWQ runner via vLLM (Lipikar substitute)."""

from __future__ import annotations

from pathlib import Path

from .config import INTERNVL_MODEL, INTERNVL_PORT
from .qwen_vl_runner import VLMPageResult, run_qwen_vl


def run_internvl(
    image_path: Path,
    *,
    port: int = INTERNVL_PORT,
    model: str = INTERNVL_MODEL,
    timeout: float = 240.0,
) -> VLMPageResult:
    """Same API as ``run_qwen_vl`` — different port and model."""

    return run_qwen_vl(image_path, port=port, model=model, timeout=timeout)

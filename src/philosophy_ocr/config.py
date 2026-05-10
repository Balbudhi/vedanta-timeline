"""Paths, model IDs, and partition presets for philosophy_ocr.

All path constants are absolute, matching the layout verified in
``docs/ORCD_INFRASTRUCTURE_INVESTIGATION.md`` and locked in
``docs/SANSKRIT_OCR_FINAL_PLAN.md``.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final


# --- storage ---------------------------------------------------------------

HF_HOME: Final[Path] = Path(
    os.environ.get("HF_HOME", "/orcd/scratch/orcd/009/eeshan/hf_cache")
)
VLLM_CACHE_ROOT: Final[Path] = Path(
    os.environ.get("VLLM_CACHE_ROOT", "/orcd/scratch/orcd/009/eeshan/cache/vllm")
)
TORCH_HOME: Final[Path] = Path(
    os.environ.get("TORCH_HOME", "/orcd/scratch/orcd/009/eeshan/cache/torch")
)
VENV_ROOT: Final[Path] = Path("/orcd/scratch/orcd/009/eeshan/venvs/ocr")
BULK_OUTPUT_ROOT: Final[Path] = Path("/orcd/pool/008/eeshan/philosophy_ocr")
SMOKE_OUTPUT_ROOT: Final[Path] = Path(
    "/orcd/home/002/eeshan/philosophy/tmp/ocr_smoke"
)
LOG_ROOT: Final[Path] = Path(
    "/orcd/home/002/eeshan/philosophy/handoffs/ocr_logs"
)


# --- models ----------------------------------------------------------------

QWEN_VL_MODEL: Final[str] = "Qwen/Qwen2.5-VL-72B-Instruct-AWQ"
INTERNVL_MODEL: Final[str] = "OpenGVLab/InternVL2_5-78B-AWQ"
SURYA_MODEL: Final[str] = "datalab-to/surya"


# --- vLLM serving ports ----------------------------------------------------

QWEN_VL_PORT: Final[int] = 8000
INTERNVL_PORT: Final[int] = 8001


# --- consensus thresholds (per plan §3.1) ----------------------------------

CONSENSUS_AGREEMENT_THRESHOLD: Final[float] = 0.92
SURYA_CONFIDENCE_FLOOR: Final[float] = 0.5
PAGE_PROMOTION_THRESHOLD: Final[float] = 0.95


# --- partitions ------------------------------------------------------------

DEFAULT_PARTITION: Final[str] = "sched_mit_sloan_gpu_r8"
DEFAULT_GPU_GRES: Final[str] = "gpu:a100:4"
DEFAULT_WALLTIME: Final[str] = "23:50:00"

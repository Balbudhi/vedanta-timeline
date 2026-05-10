"""Qwen2.5-VL-72B-AWQ runner via vLLM HTTP server.

Assumes a vLLM server has already been launched on ``QWEN_VL_PORT``. The CLI
``ocr-book`` / ``ocr-page`` entry point in :mod:`philosophy_ocr.cli` is
responsible for starting the server.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import QWEN_VL_MODEL, QWEN_VL_PORT


@dataclass(frozen=True)
class VLMPageResult:
    devanagari: str
    iast: str
    structure_tags: dict[str, str] = field(default_factory=dict)
    raw_response: dict[str, Any] = field(default_factory=dict)


_PROMPT_TEMPLATE = (
    "You are reading a degraded scan of a Sanskrit philosophical work. "
    "Transcribe the page in reading order. Output JSON with keys "
    "`devanagari` (Devanāgarī text, line-by-line, daṇḍas preserved), "
    "`iast` (IAST transliteration), and `structure_tags` "
    "(per-line region label: one of `mūla`, `bhāṣya`, `ṭīkā`, `footnote`, "
    "`marginalia`). Do not invent text. If a region is illegible, use "
    "`[…]` of matching length. Return only the JSON object."
)


def _encode_image(image_path: Path) -> str:
    return base64.b64encode(image_path.read_bytes()).decode("ascii")


def run_qwen_vl(
    image_path: Path,
    *,
    port: int = QWEN_VL_PORT,
    model: str = QWEN_VL_MODEL,
    timeout: float = 240.0,
) -> VLMPageResult:
    """POST the page image to the local vLLM Qwen2.5-VL server.

    Returns a structured ``VLMPageResult``. Raises on transport error or on
    a server response that cannot be parsed as the expected JSON.
    """

    try:
        import httpx
    except ImportError as exc:  # pragma: no cover
        raise ImportError("httpx not installed; pip install httpx.") from exc

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{_encode_image(image_path)}"
                        },
                    },
                    {"type": "text", "text": _PROMPT_TEMPLATE},
                ],
            }
        ],
        "temperature": 0.0,
        "max_tokens": 4096,
        "response_format": {"type": "json_object"},
    }
    url = f"http://127.0.0.1:{port}/v1/chat/completions"
    response = httpx.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    raw_text = data["choices"][0]["message"]["content"]
    import json as _json

    parsed = _json.loads(raw_text)
    return VLMPageResult(
        devanagari=parsed.get("devanagari", ""),
        iast=parsed.get("iast", ""),
        structure_tags=parsed.get("structure_tags", {}) or {},
        raw_response=data,
    )

"""Emit per-text artifacts in the schema the jyotish ingest pipeline expects."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


def _serialize(obj: Any) -> Any:
    if is_dataclass(obj):
        return {k: _serialize(v) for k, v in asdict(obj).items()}
    if isinstance(obj, list):
        return [_serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, Path):
        return str(obj)
    return obj


def write_results(results: dict, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "results.json"
    out.write_text(json.dumps(_serialize(results), ensure_ascii=False, indent=2))
    return out


def write_page_text(page_index: int, text: str, out_dir: Path) -> Path:
    text_dir = out_dir / "text"
    text_dir.mkdir(parents=True, exist_ok=True)
    out = text_dir / f"page_{page_index:04d}.txt"
    out.write_text(text)
    return out

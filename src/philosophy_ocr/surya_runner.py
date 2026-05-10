"""Surya line-OCR runner.

Wraps ``surya-ocr``'s detection + recognition predictors into a function that
takes a PNG path and returns ordered ``(text, bbox, confidence)`` lines.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SuryaLine:
    text: str
    bbox: tuple[float, float, float, float]
    confidence: float


def run_surya(image_path: Path, language: str = "sa") -> list[SuryaLine]:
    """Run Surya on ``image_path``. Returns ordered lines."""

    try:
        from PIL import Image
        from surya.recognition import RecognitionPredictor  # type: ignore
        from surya.detection import DetectionPredictor  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "surya-ocr not installed; pip install surya-ocr."
        ) from exc

    image = Image.open(str(image_path)).convert("RGB")
    det = DetectionPredictor()
    rec = RecognitionPredictor()
    predictions: list[Any] = rec([image], [[language]], det)
    if not predictions:
        return []
    page = predictions[0]
    lines: list[SuryaLine] = []
    for line in page.text_lines:
        bbox = tuple(line.bbox) if line.bbox else (0.0, 0.0, 0.0, 0.0)
        lines.append(
            SuryaLine(
                text=line.text or "",
                bbox=bbox,  # type: ignore[arg-type]
                confidence=float(getattr(line, "confidence", 0.0) or 0.0),
            )
        )
    return lines

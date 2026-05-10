"""Sanskrit lexical / sandhi verification via prakriya.ocr_api."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TokenVerdict:
    surface: str
    resolvable: bool
    method: str
    confidence: float


def verify_lines(lines: Iterable[str]) -> list[TokenVerdict]:
    from prakriya.ocr_api import lexically_resolvable, tokenize_for_ocr

    text = "\n".join(lines)
    tokens = tokenize_for_ocr(text)
    verdicts: list[TokenVerdict] = []
    for tok in tokens:
        result = lexically_resolvable(tok)
        verdicts.append(
            TokenVerdict(
                surface=tok.surface,
                resolvable=result.resolvable,
                method=result.method,
                confidence=result.confidence,
            )
        )
    return verdicts


def lexical_flag_rate(verdicts: list[TokenVerdict]) -> float:
    """Fraction of tokens that are unresolvable (== flag rate, in 0..1)."""

    if not verdicts:
        return 0.0
    return sum(1 for v in verdicts if not v.resolvable) / len(verdicts)

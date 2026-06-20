"""Confidence helpers shared by GhostEye inference modules."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Iterable


@dataclass(frozen=True)
class ConfidenceScore:
    """Bounded confidence value with a short explanation."""

    value: float
    reason: str


class ConfidenceCalibrator:
    """Combines evidence quality signals into a bounded confidence score."""

    def score(
        self,
        evidence: Iterable[float],
        coverage: float = 1.0,
        stability: float = 1.0,
        reason: str = "combined evidence",
    ) -> ConfidenceScore:
        evidence_values = [self._clamp(value) for value in evidence]
        evidence_mean = fmean(evidence_values) if evidence_values else 0.0
        value = evidence_mean * self._clamp(coverage) * self._clamp(stability)
        return ConfidenceScore(value=self._clamp(value), reason=reason)

    def from_delta(
        self,
        delta: float,
        threshold: float,
        stability: float = 1.0,
        reason: str = "signal delta",
    ) -> ConfidenceScore:
        if threshold <= 0:
            raise ValueError("threshold must be positive")
        return self.score([abs(delta) / threshold], stability=stability, reason=reason)

    @staticmethod
    def _clamp(value: float) -> float:
        return min(max(value, 0.0), 1.0)

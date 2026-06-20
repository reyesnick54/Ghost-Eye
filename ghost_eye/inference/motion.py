"""Motion inference from WiFi-only signal deltas."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Mapping

from .confidence import ConfidenceCalibrator, ConfidenceScore


@dataclass(frozen=True)
class MotionEstimate:
    """Coarse motion estimate derived from RSSI instability."""

    motion_score: float
    active: bool
    confidence: ConfidenceScore


class MotionDetector:
    """Detects motion from baseline-relative RSSI residuals."""

    def __init__(self, threshold_db: float = 4.0) -> None:
        if threshold_db <= 0:
            raise ValueError("threshold_db must be positive")
        self.threshold_db = threshold_db
        self._confidence = ConfidenceCalibrator()

    def estimate(self, residuals_db: Mapping[str, float]) -> MotionEstimate:
        magnitudes = [abs(value) for value in residuals_db.values()]
        mean_delta = fmean(magnitudes) if magnitudes else 0.0
        motion_score = min(mean_delta / self.threshold_db, 1.0)
        confidence = self._confidence.from_delta(
            mean_delta,
            threshold=self.threshold_db,
            reason="mean RSSI residual",
        )
        return MotionEstimate(
            motion_score=motion_score,
            active=motion_score >= 0.6,
            confidence=confidence,
        )

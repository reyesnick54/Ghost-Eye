"""Presence inference built on WiFi-only motion and disturbance signals."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .confidence import ConfidenceCalibrator, ConfidenceScore
from .disturbance_field import DisturbanceField
from .motion import MotionEstimate


PresenceState = Literal["clear", "possible_presence", "presence_detected"]


@dataclass(frozen=True)
class PresenceEstimate:
    """Presence state and confidence for a sensing interval."""

    state: PresenceState
    confidence: ConfidenceScore


class PresenceDetector:
    """Combines motion and disturbance indicators into a presence state."""

    def __init__(self) -> None:
        self._confidence = ConfidenceCalibrator()

    def estimate(
        self,
        motion: MotionEstimate,
        disturbance: DisturbanceField,
    ) -> PresenceEstimate:
        disturbance_score = min(disturbance.magnitude / 8.0, 1.0)
        combined = (motion.motion_score * 0.65) + (disturbance_score * 0.35)

        if combined >= 0.7 and disturbance.affected_access_points >= 2:
            state: PresenceState = "presence_detected"
        elif combined >= 0.35:
            state = "possible_presence"
        else:
            state = "clear"

        confidence = self._confidence.score(
            [combined, motion.confidence.value],
            reason="motion and disturbance agreement",
        )
        return PresenceEstimate(state=state, confidence=confidence)

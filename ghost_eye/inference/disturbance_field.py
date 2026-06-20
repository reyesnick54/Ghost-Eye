"""Translate RSSI residuals into coarse disturbance field estimates."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Mapping


@dataclass(frozen=True)
class DisturbanceField:
    """Aggregate signal disturbance estimate for a sensing session."""

    magnitude: float
    affected_access_points: int
    residuals_db: Mapping[str, float]


class DisturbanceFieldEstimator:
    """Estimates environmental disturbance from baseline-relative RSSI deltas."""

    def estimate(
        self,
        residuals_db: Mapping[str, float],
        minimum_delta_db: float = 2.5,
    ) -> DisturbanceField:
        affected = {
            bssid.lower(): residual
            for bssid, residual in residuals_db.items()
            if abs(residual) >= minimum_delta_db
        }
        magnitude = fmean(abs(value) for value in affected.values()) if affected else 0.0
        return DisturbanceField(
            magnitude=magnitude,
            affected_access_points=len(affected),
            residuals_db=dict(affected),
        )

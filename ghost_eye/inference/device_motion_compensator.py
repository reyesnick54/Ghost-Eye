"""Compensate for sensing-device movement in RSSI observations."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Mapping


@dataclass(frozen=True)
class DeviceMotionCompensation:
    """Signals corrected for estimated device movement."""

    corrected_signals: Mapping[str, float]
    offset_db: float
    moved: bool


class DeviceMotionCompensator:
    """Removes common-mode RSSI shifts that likely came from device motion."""

    def __init__(self, movement_threshold_db: float = 6.0) -> None:
        if movement_threshold_db <= 0:
            raise ValueError("movement_threshold_db must be positive")
        self.movement_threshold_db = movement_threshold_db

    def compensate(
        self,
        signals: Mapping[str, float],
        baseline: Mapping[str, float],
    ) -> DeviceMotionCompensation:
        shared_keys = {bssid.lower() for bssid in signals} & {
            bssid.lower() for bssid in baseline
        }
        if not shared_keys:
            return DeviceMotionCompensation(
                corrected_signals=dict(signals),
                offset_db=0.0,
                moved=False,
            )

        current = {bssid.lower(): value for bssid, value in signals.items()}
        expected = {bssid.lower(): value for bssid, value in baseline.items()}
        offsets = [current[key] - expected[key] for key in shared_keys]
        offset_db = float(median(offsets))
        moved = abs(offset_db) >= self.movement_threshold_db
        corrected = {
            bssid.lower(): rssi_dbm - offset_db
            for bssid, rssi_dbm in signals.items()
        }
        return DeviceMotionCompensation(
            corrected_signals=corrected,
            offset_db=offset_db,
            moved=moved,
        )

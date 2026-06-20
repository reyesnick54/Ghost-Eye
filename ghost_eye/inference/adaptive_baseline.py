"""Adaptive RSSI baselines for WiFi-only sensing."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Mapping


@dataclass(frozen=True)
class BaselineSnapshot:
    """Current expected RSSI values for known access points."""

    values: Mapping[str, float]
    observations: Mapping[str, int]
    timestamp: float = field(default_factory=time)


class AdaptiveBaseline:
    """Maintains an exponential moving average baseline per BSSID."""

    def __init__(self, alpha: float = 0.15) -> None:
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be within (0.0, 1.0]")
        self.alpha = alpha
        self._values: dict[str, float] = {}
        self._observations: dict[str, int] = {}

    def update(self, signals: Mapping[str, float]) -> BaselineSnapshot:
        """Update the baseline with observed RSSI values."""

        for bssid, rssi_dbm in signals.items():
            key = bssid.lower()
            if key in self._values:
                self._values[key] = (self.alpha * rssi_dbm) + (
                    (1.0 - self.alpha) * self._values[key]
                )
            else:
                self._values[key] = rssi_dbm
            self._observations[key] = self._observations.get(key, 0) + 1
        return self.snapshot()

    def residuals(self, signals: Mapping[str, float]) -> dict[str, float]:
        """Return current RSSI deltas from the learned baseline."""

        return {
            bssid.lower(): rssi_dbm - self._values.get(bssid.lower(), rssi_dbm)
            for bssid, rssi_dbm in signals.items()
        }

    def snapshot(self) -> BaselineSnapshot:
        return BaselineSnapshot(
            values=dict(self._values),
            observations=dict(self._observations),
        )

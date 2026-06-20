"""Normalize WiFi RSSI observations into stable inference features."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean, pstdev
from typing import Iterable, Mapping


@dataclass(frozen=True)
class NormalizedSignal:
    """Normalized signal state for one access point."""

    bssid: str
    rssi_dbm: float
    strength: float
    delta_db: float = 0.0
    z_score: float = 0.0


class SignalNormalizer:
    """Converts RSSI dBm values into bounded and baseline-relative features."""

    def __init__(self, floor_dbm: float = -95.0, ceiling_dbm: float = -35.0) -> None:
        if floor_dbm >= ceiling_dbm:
            raise ValueError("floor_dbm must be lower than ceiling_dbm")
        self.floor_dbm = floor_dbm
        self.ceiling_dbm = ceiling_dbm

    def strength(self, rssi_dbm: float) -> float:
        """Scale an RSSI value into the ``0.0`` to ``1.0`` range."""

        bounded = min(max(rssi_dbm, self.floor_dbm), self.ceiling_dbm)
        return (bounded - self.floor_dbm) / (self.ceiling_dbm - self.floor_dbm)

    def normalize(
        self,
        signals: Mapping[str, float],
        baseline: Mapping[str, float] | None = None,
    ) -> dict[str, NormalizedSignal]:
        """Normalize current RSSI values against an optional baseline."""

        baseline = baseline or {}
        values = list(signals.values())
        spread = pstdev(values) if len(values) > 1 else 0.0
        center = fmean(values) if values else 0.0

        normalized: dict[str, NormalizedSignal] = {}
        for bssid, rssi_dbm in signals.items():
            delta_db = rssi_dbm - baseline.get(bssid, rssi_dbm)
            normalized[bssid.lower()] = NormalizedSignal(
                bssid=bssid.lower(),
                rssi_dbm=rssi_dbm,
                strength=self.strength(rssi_dbm),
                delta_db=delta_db,
                z_score=((rssi_dbm - center) / spread) if spread else 0.0,
            )
        return normalized

    def mean_rssi(self, samples: Iterable[float]) -> float | None:
        values = list(samples)
        return fmean(values) if values else None

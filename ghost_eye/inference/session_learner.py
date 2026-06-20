"""Session-level learning for baselines and room fingerprints."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Iterable, Mapping

from .adaptive_baseline import AdaptiveBaseline, BaselineSnapshot
from .room_fingerprint_mapper import RoomFingerprint
from ghost_eye.wifi.wifi_scan import WifiScan


@dataclass(frozen=True)
class LearnedSessionState:
    """Learned signal state accumulated during a sensing session."""

    baseline: BaselineSnapshot
    fingerprints: tuple[RoomFingerprint, ...]
    updated_at: float = field(default_factory=time)


class SessionLearner:
    """Learns baselines and optional labeled room fingerprints from scans."""

    def __init__(self, baseline: AdaptiveBaseline | None = None) -> None:
        self._baseline = baseline or AdaptiveBaseline()
        self._fingerprints: list[RoomFingerprint] = []

    def observe(self, scan: WifiScan) -> BaselineSnapshot:
        return self._baseline.update(
            {network.bssid.lower(): network.rssi_dbm for network in scan.networks}
        )

    def learn_fingerprint(
        self,
        label: str,
        scans: Iterable[WifiScan],
    ) -> RoomFingerprint:
        totals: dict[str, float] = {}
        counts: dict[str, int] = {}
        for scan in scans:
            for network in scan.networks:
                key = network.bssid.lower()
                totals[key] = totals.get(key, 0.0) + network.rssi_dbm
                counts[key] = counts.get(key, 0) + 1

        fingerprint = RoomFingerprint(
            label=label,
            signals={key: totals[key] / counts[key] for key in totals},
        )
        self._fingerprints.append(fingerprint)
        return fingerprint

    def state(self) -> LearnedSessionState:
        return LearnedSessionState(
            baseline=self._baseline.snapshot(),
            fingerprints=tuple(self._fingerprints),
        )

    def load_fingerprints(self, fingerprints: Iterable[RoomFingerprint]) -> None:
        self._fingerprints = list(fingerprints)

    def load_baseline(self, values: Mapping[str, float]) -> None:
        self._baseline = AdaptiveBaseline()
        self._baseline.update(values)

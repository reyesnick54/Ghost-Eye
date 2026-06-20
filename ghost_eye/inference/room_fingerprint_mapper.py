"""Room fingerprint matching for WiFi RSSI vectors."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Mapping


@dataclass(frozen=True)
class RoomFingerprint:
    """A named RSSI fingerprint for a room or calibrated zone."""

    label: str
    signals: Mapping[str, float]


@dataclass(frozen=True)
class FingerprintMatch:
    """Best-match result for an observed RSSI vector."""

    label: str
    distance: float
    confidence: float


class RoomFingerprintMapper:
    """Matches current RSSI observations against stored room fingerprints."""

    def __init__(self, fingerprints: Iterable[RoomFingerprint] = ()) -> None:
        self._fingerprints = list(fingerprints)

    def add(self, fingerprint: RoomFingerprint) -> None:
        self._fingerprints.append(fingerprint)

    def match(self, signals: Mapping[str, float]) -> FingerprintMatch | None:
        if not self._fingerprints:
            return None

        normalized = {bssid.lower(): rssi for bssid, rssi in signals.items()}
        best_label = "unknown"
        best_distance = float("inf")

        for fingerprint in self._fingerprints:
            distance = self._distance(normalized, fingerprint.signals)
            if distance < best_distance:
                best_label = fingerprint.label
                best_distance = distance

        confidence = max(0.0, min(1.0, 1.0 - (best_distance / 60.0)))
        return FingerprintMatch(
            label=best_label,
            distance=best_distance,
            confidence=confidence,
        )

    @staticmethod
    def _distance(current: Mapping[str, float], fingerprint: Mapping[str, float]) -> float:
        normalized_fingerprint = {
            bssid.lower(): rssi for bssid, rssi in fingerprint.items()
        }
        keys = set(current) | set(normalized_fingerprint)
        if not keys:
            return float("inf")

        squared = 0.0
        for key in keys:
            current_rssi = current.get(key, -100.0)
            baseline_rssi = normalized_fingerprint.get(key, -100.0)
            squared += (current_rssi - baseline_rssi) ** 2
        return sqrt(squared / len(keys))

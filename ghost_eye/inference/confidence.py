"""Confidence helpers for WiFi-only non-CSI GhostEye telemetry."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

from ghost_eye.api.schemas import MODE_WIFI_ONLY_NON_CSI


@dataclass(frozen=True)
class ConfidenceCeilingResult:
    """Confidence after contextual ceiling limits are applied."""

    raw_confidence: float
    confidence_ceiling: float
    final_confidence: float
    reason: str

    def to_dict(self) -> dict[str, float | str]:
        return asdict(self)


@dataclass(frozen=True)
class ConfidenceScore:
    """Bounded confidence value with a short explanation."""

    value: float
    reason: str


class ConfidenceCalibrator:
    """Combine simple evidence scores into a bounded value."""

    def score(
        self,
        evidence: Iterable[float],
        coverage: float = 1.0,
        stability: float = 1.0,
        reason: str = "combined evidence",
    ) -> ConfidenceScore:
        values = [_clamp(value) for value in evidence]
        mean = sum(values) / len(values) if values else 0.0
        return ConfidenceScore(value=_clamp(mean * _clamp(coverage) * _clamp(stability)), reason=reason)

    def from_delta(self, delta: float, threshold: float, reason: str = "signal delta") -> ConfidenceScore:
        """Score confidence from a baseline-relative delta and threshold."""

        if threshold <= 0.0:
            raise ValueError("threshold must be positive")
        return ConfidenceScore(value=_clamp(abs(float(delta)) / float(threshold)), reason=reason)


class ConfidenceCeilingEngine:
    """Keep RSSI-only output confidence below the v0.2 non-CSI ceiling."""

    DEFAULT_MODE_CEILINGS: Mapping[str, float] = {
        MODE_WIFI_ONLY_NON_CSI: 0.65,
        "wifi_only_rssi_latency": 0.65,
        "simulated": 0.65,
        "rssi": 0.55,
        "unknown": 0.50,
    }

    def __init__(self, mode_ceilings: Mapping[str, float] | None = None) -> None:
        self._mode_ceilings = dict(self.DEFAULT_MODE_CEILINGS)
        if mode_ceilings:
            self._mode_ceilings.update({str(key): _clamp(float(value)) for key, value in mode_ceilings.items()})

    def evaluate(
        self,
        raw_confidence: float,
        signal_mode: str | None = None,
        signal_quality: float | str | None = None,
        device_motion_status: bool | str | None = None,
        map_ambiguity: float | bool | str | None = None,
        *,
        mode: str | None = None,
    ) -> dict[str, float | str]:
        effective_mode = mode or signal_mode or MODE_WIFI_ONLY_NON_CSI
        raw = _clamp(float(raw_confidence))
        ceiling = self._mode_ceilings.get(str(effective_mode), self._mode_ceilings["unknown"])
        ceiling = min(ceiling, _quality_ceiling(signal_quality), _motion_ceiling(device_motion_status), _ambiguity_ceiling(map_ambiguity))
        ceiling = round(ceiling, 2)
        final = round(min(raw, ceiling), 2)
        reason = f"wifi-only non-CSI confidence capped at {ceiling:.2f}"
        return ConfidenceCeilingResult(
            raw_confidence=round(raw, 2),
            confidence_ceiling=ceiling,
            final_confidence=final,
            reason=reason,
        ).to_dict()

    def apply(self, *args: Any, **kwargs: Any) -> dict[str, float | str]:
        return self.evaluate(*args, **kwargs)

    def compute(self, *args: Any, **kwargs: Any) -> dict[str, float | str]:
        return self.evaluate(*args, **kwargs)

    __call__ = evaluate


def _quality_ceiling(value: float | str | None) -> float:
    if value is None:
        return 1.0
    if isinstance(value, str):
        return {"excellent": 0.95, "good": 0.85, "fair": 0.70, "low": 0.55, "poor": 0.45}.get(value.lower(), 0.80)
    quality = _clamp(float(value))
    if quality >= 0.75:
        return 0.90
    if quality >= 0.50:
        return 0.75
    if quality >= 0.25:
        return 0.58
    return 0.42


def _motion_ceiling(value: bool | str | None) -> float:
    if value is None:
        return 1.0
    if isinstance(value, bool):
        return 0.70 if value else 1.0
    state = value.lower()
    if state in {"moving", "unstable"}:
        return 0.50
    if state == "unknown":
        return 0.58
    return 1.0


def _ambiguity_ceiling(value: float | bool | str | None) -> float:
    if value is None:
        return 1.0
    if isinstance(value, bool):
        return 0.60 if value else 1.0
    if isinstance(value, str):
        return {"high": 0.55, "medium": 0.72, "low": 0.90}.get(value.lower(), 0.75)
    ambiguity = _clamp(float(value))
    return max(0.45, 1.0 - (ambiguity * 0.45))


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))

"""Confidence ceiling logic for Ghost-Eye inference outputs.

The ceiling engine keeps reported confidence bounded by the sensing context.
Raw model confidence is useful, but some operating modes and environmental
conditions cannot support high certainty even when the model score is high.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True)
class ConfidenceCeilingResult:
    """Result returned after applying a confidence ceiling."""

    raw_confidence: float
    confidence_ceiling: float
    final_confidence: float
    reason: str

    def to_dict(self) -> dict[str, float | str]:
        """Return the result as a plain dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class _CeilingDecision:
    ceiling: float
    reason: str


class ConfidenceCeilingEngine:
    """Apply contextual ceilings to raw inference confidence.

    Parameters are intentionally small and serializable so the engine can sit
    between model inference and API responses.

    Inputs:
    - raw_confidence: model confidence before contextual capping.
    - signal_mode: sensing mode, such as ``csi``, ``rssi``, ``simulated``, or
      ``fallback``.
    - signal_quality: numeric 0..1, percentage 0..100, or a quality label.
    - device_motion_status: boolean or label describing whether the sensing
      device itself is moving/unstable.
    - map_ambiguity: numeric 0..1, boolean, or ambiguity label.
    """

    DEFAULT_MODE_CEILINGS: Mapping[str, float] = MappingProxyType(
        {
            "calibrated_csi": 0.96,
            "calibrated": 0.96,
            "high_fidelity": 0.95,
            "wifi_csi": 0.93,
            "csi": 0.93,
            "hybrid": 0.90,
            "standard": 0.85,
            "rssi": 0.78,
            "simulated": 0.65,
            "simulation": 0.65,
            "demo": 0.65,
            "degraded": 0.65,
            "fallback": 0.55,
            "lost": 0.35,
            "unknown": 0.60,
        }
    )
    UNKNOWN_MODE_CEILING = 0.60

    _QUALITY_LABEL_CEILINGS: Mapping[str, float] = MappingProxyType(
        {
            "excellent": 0.98,
            "high": 0.98,
            "good": 0.90,
            "medium": 0.80,
            "fair": 0.75,
            "low": 0.60,
            "poor": 0.55,
            "bad": 0.40,
            "none": 0.35,
            "no_signal": 0.35,
            "unknown": 0.80,
        }
    )
    _MOTION_LABEL_CEILINGS: Mapping[str, float] = MappingProxyType(
        {
            "stationary": 1.00,
            "stable": 1.00,
            "still": 1.00,
            "idle": 1.00,
            "not_moving": 1.00,
            "moving": 0.70,
            "in_motion": 0.70,
            "walking": 0.70,
            "vehicle": 0.65,
            "unstable": 0.60,
            "shaking": 0.60,
            "unknown": 0.85,
        }
    )
    _AMBIGUITY_LABEL_CEILINGS: Mapping[str, float] = MappingProxyType(
        {
            "none": 0.98,
            "clear": 0.98,
            "low": 0.90,
            "medium": 0.75,
            "moderate": 0.75,
            "high": 0.55,
            "severe": 0.45,
            "extreme": 0.40,
            "unknown": 0.75,
        }
    )

    def __init__(self, mode_ceilings: Mapping[str, float] | None = None) -> None:
        """Create an engine with optional per-mode ceiling overrides."""

        ceilings = dict(self.DEFAULT_MODE_CEILINGS)
        if mode_ceilings:
            for mode, ceiling in mode_ceilings.items():
                ceilings[self._normalize_label(mode)] = self._normalize_score(
                    ceiling,
                    allow_percentage=True,
                )
        self._mode_ceilings = MappingProxyType(ceilings)

    @property
    def mode_ceilings(self) -> Mapping[str, float]:
        """Configured ceilings keyed by normalized signal mode."""

        return self._mode_ceilings

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
        """Return confidence values after applying the strictest ceiling.

        ``mode`` is accepted as a keyword alias for ``signal_mode``.
        """

        effective_mode = signal_mode if signal_mode is not None else mode
        raw = self._normalize_score(raw_confidence)
        decisions = [
            self._mode_decision(effective_mode),
            self._quality_decision(signal_quality),
            self._motion_decision(device_motion_status),
            self._ambiguity_decision(map_ambiguity),
        ]
        strictest = min(decisions, key=lambda decision: decision.ceiling)
        confidence_ceiling = self._round_score(strictest.ceiling)
        final_confidence = self._round_score(min(raw, confidence_ceiling))

        if raw > confidence_ceiling:
            reason = (
                f"raw confidence capped by {strictest.reason} "
                f"at {confidence_ceiling:.2f}"
            )
        else:
            reason = (
                f"raw confidence within ceiling; strictest limit is "
                f"{strictest.reason} at {confidence_ceiling:.2f}"
            )

        return ConfidenceCeilingResult(
            raw_confidence=self._round_score(raw),
            confidence_ceiling=confidence_ceiling,
            final_confidence=final_confidence,
            reason=reason,
        ).to_dict()

    def apply(
        self,
        raw_confidence: float,
        signal_mode: str | None = None,
        signal_quality: float | str | None = None,
        device_motion_status: bool | str | None = None,
        map_ambiguity: float | bool | str | None = None,
        *,
        mode: str | None = None,
    ) -> dict[str, float | str]:
        """Alias for :meth:`evaluate`."""

        return self.evaluate(
            raw_confidence=raw_confidence,
            signal_mode=signal_mode,
            signal_quality=signal_quality,
            device_motion_status=device_motion_status,
            map_ambiguity=map_ambiguity,
            mode=mode,
        )

    def compute(
        self,
        raw_confidence: float,
        signal_mode: str | None = None,
        signal_quality: float | str | None = None,
        device_motion_status: bool | str | None = None,
        map_ambiguity: float | bool | str | None = None,
        *,
        mode: str | None = None,
    ) -> dict[str, float | str]:
        """Alias for :meth:`evaluate`."""

        return self.evaluate(
            raw_confidence=raw_confidence,
            signal_mode=signal_mode,
            signal_quality=signal_quality,
            device_motion_status=device_motion_status,
            map_ambiguity=map_ambiguity,
            mode=mode,
        )

    __call__ = evaluate

    def _mode_decision(self, signal_mode: str | None) -> _CeilingDecision:
        label = self._normalize_label(signal_mode or "unknown")
        ceiling = self._mode_ceilings.get(label, self.UNKNOWN_MODE_CEILING)
        reason = f"signal mode '{label}'"
        if label not in self._mode_ceilings:
            reason = f"unknown signal mode '{label}'"
        return _CeilingDecision(ceiling=ceiling, reason=reason)

    def _quality_decision(self, signal_quality: float | str | None) -> _CeilingDecision:
        if signal_quality is None:
            return _CeilingDecision(ceiling=1.0, reason="signal quality not provided")

        if isinstance(signal_quality, str):
            label = self._normalize_label(signal_quality)
            ceiling = self._QUALITY_LABEL_CEILINGS.get(label, 0.80)
            return _CeilingDecision(
                ceiling=ceiling,
                reason=f"signal quality '{label}'",
            )

        quality = self._normalize_score(signal_quality, allow_percentage=True)
        if quality >= 0.80:
            ceiling = 0.98
        elif quality >= 0.60:
            ceiling = 0.85
        elif quality >= 0.40:
            ceiling = 0.70
        elif quality >= 0.20:
            ceiling = 0.55
        else:
            ceiling = 0.40

        return _CeilingDecision(
            ceiling=ceiling,
            reason=f"signal quality {quality:.2f}",
        )

    def _motion_decision(
        self,
        device_motion_status: bool | str | None,
    ) -> _CeilingDecision:
        if device_motion_status is None:
            return _CeilingDecision(ceiling=1.0, reason="device motion not provided")

        if isinstance(device_motion_status, bool):
            ceiling = 0.70 if device_motion_status else 1.0
            label = "moving" if device_motion_status else "stable"
            return _CeilingDecision(
                ceiling=ceiling,
                reason=f"device motion status '{label}'",
            )

        label = self._normalize_label(device_motion_status)
        ceiling = self._MOTION_LABEL_CEILINGS.get(label, 0.85)
        return _CeilingDecision(
            ceiling=ceiling,
            reason=f"device motion status '{label}'",
        )

    def _ambiguity_decision(
        self,
        map_ambiguity: float | bool | str | None,
    ) -> _CeilingDecision:
        if map_ambiguity is None:
            return _CeilingDecision(ceiling=1.0, reason="map ambiguity not provided")

        if isinstance(map_ambiguity, bool):
            ceiling = 0.60 if map_ambiguity else 0.98
            label = "ambiguous" if map_ambiguity else "clear"
            return _CeilingDecision(ceiling=ceiling, reason=f"map ambiguity '{label}'")

        if isinstance(map_ambiguity, str):
            label = self._normalize_label(map_ambiguity)
            ceiling = self._AMBIGUITY_LABEL_CEILINGS.get(label, 0.75)
            return _CeilingDecision(ceiling=ceiling, reason=f"map ambiguity '{label}'")

        ambiguity = self._normalize_score(map_ambiguity, allow_percentage=True)
        if ambiguity <= 0.10:
            ceiling = 0.98
        elif ambiguity <= 0.25:
            ceiling = 0.90
        elif ambiguity <= 0.50:
            ceiling = 0.75
        elif ambiguity <= 0.75:
            ceiling = 0.60
        else:
            ceiling = 0.45

        return _CeilingDecision(
            ceiling=ceiling,
            reason=f"map ambiguity {ambiguity:.2f}",
        )

    @staticmethod
    def _normalize_label(value: Any) -> str:
        return str(value).strip().lower().replace("-", "_").replace(" ", "_")

    @classmethod
    def _normalize_score(cls, value: Any, *, allow_percentage: bool = False) -> float:
        try:
            score = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Expected a numeric confidence score, got {value!r}") from exc

        if allow_percentage and score > 1.0:
            score = score / 100.0
        return min(1.0, max(0.0, score))

    @staticmethod
    def _round_score(value: float) -> float:
        return round(value, 6)

"""Device motion compensation for Ghost-Eye inference decisions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, Union


DeviceMotionState = Literal["stable", "moving", "unknown"]
ScanValidity = Union[bool, Literal["degraded"]]


@dataclass(frozen=True)
class DeviceMotionCompensation:
    """Result of applying device-motion policy to one scan."""

    device_stability: DeviceMotionState
    confidence_multiplier: float
    scan_valid: ScanValidity
    reason: str


class DeviceMotionCompensator:
    """Apply v0.1 device-motion policy to inference confidence and scan validity."""

    STABLE: DeviceMotionState = "stable"
    MOVING: DeviceMotionState = "moving"
    UNKNOWN: DeviceMotionState = "unknown"

    def __init__(self, moving_confidence_multiplier: float = 0.5) -> None:
        if not 0.0 <= moving_confidence_multiplier <= 1.0:
            raise ValueError("moving_confidence_multiplier must be between 0.0 and 1.0")

        self._moving_confidence_multiplier = moving_confidence_multiplier

    def compensate(
        self,
        device_motion_state: Optional[str] = None,
    ) -> DeviceMotionCompensation:
        """Return the v0.1 compensation decision for an optional motion state."""
        state = self._normalize_state(device_motion_state)

        if state == self.MOVING:
            return DeviceMotionCompensation(
                device_stability=self.MOVING,
                confidence_multiplier=self._moving_confidence_multiplier,
                scan_valid=False,
                reason="device_moving_confidence_reduced_baseline_update_blocked",
            )

        if state == self.STABLE:
            return DeviceMotionCompensation(
                device_stability=self.STABLE,
                confidence_multiplier=1.0,
                scan_valid=True,
                reason="device_stable",
            )

        return DeviceMotionCompensation(
            device_stability=self.UNKNOWN,
            confidence_multiplier=1.0,
            scan_valid=True,
            reason="device_motion_unknown_no_compensation_applied",
        )

    def baseline_update_allowed(
        self,
        device_motion_state: Optional[str] = None,
    ) -> bool:
        """Return whether baseline updates are allowed for the motion state."""
        return self.compensate(device_motion_state).device_stability != self.MOVING

    @staticmethod
    def _normalize_state(device_motion_state: Optional[str]) -> DeviceMotionState:
        if device_motion_state is None:
            return "unknown"

        state = device_motion_state.strip().lower()
        if state in {"stable", "moving", "unknown"}:
            return state  # type: ignore[return-value]

        return "unknown"

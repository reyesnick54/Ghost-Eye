"""WiFi-only non-CSI cloud pipeline for mobile-submitted observations."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from math import exp
from statistics import pstdev
from typing import Any

from app.schemas.calibration import ZoneFingerprint
from app.schemas.telemetry import (
    LIMITATIONS,
    MobileWifiObservation,
    ObservationBatch,
    RoomMap,
    SelectedNetwork,
    SignalQuality,
    TelemetryScan,
)
from app.storage.calibration_store import CalibrationStore
from app.storage.session_store import SessionStore


class CloudInferencePipeline:
    """Convert allowed mobile WiFi/network observations into coarse telemetry."""

    mode = "wifi_only_non_csi"
    confidence_cap = 0.65

    def __init__(self, session_store: SessionStore, calibration_store: CalibrationStore) -> None:
        self._session_store = session_store
        self._calibration_store = calibration_store

    def process_observation(self, observation: MobileWifiObservation) -> TelemetryScan:
        recent = self._session_store.get_session_scans(observation.session_id)[-12:]
        baseline = self._calibration_store.get_baseline(observation.team_id, observation.room_id)
        fingerprints = self._calibration_store.list_fingerprints(observation.team_id, observation.room_id)
        signal_quality = self._signal_quality(observation, recent)
        motion_score = self._motion_score(observation, baseline, recent)
        zone_map = self._zone_map(observation, fingerprints, motion_score)
        zone = max(zone_map, key=zone_map.get) if zone_map else "unknown"
        presence = self._presence(motion_score, signal_quality)
        confidence_ceiling = self._confidence_ceiling(signal_quality, observation, zone_map)
        raw_confidence = 0.18 + (signal_quality.quality_score * 0.30) + (motion_score * 0.25)
        if baseline:
            raw_confidence += 0.08
        if fingerprints:
            raw_confidence += 0.05
        confidence = round(min(confidence_ceiling, max(0.0, min(1.0, raw_confidence))), 2)

        scan = TelemetryScan(
            scan_id=f"scan_{uuid.uuid4().hex[:12]}",
            device_id=observation.device_id,
            team_id=observation.team_id,
            session_id=observation.session_id,
            timestamp=datetime.now(timezone.utc),
            selected_network=SelectedNetwork(
                ssid=observation.ssid,
                bssid_masked=observation.bssid_masked,
                vendor_hint=observation.vendor_hint,
            ),
            signal_quality=signal_quality,
            presence=presence,
            motion_score=motion_score,
            zone=zone,
            confidence=confidence,
            confidence_ceiling=confidence_ceiling,
            confidence_explanation=(
                f"Confidence is capped at {confidence_ceiling:.2f} because hosted GhostEye Cloud "
                "only analyzes mobile-submitted WiFi RSSI/latency observations and has no direct RF sensor."
            ),
            room_map=RoomMap(
                room_id=observation.room_id,
                room_name=observation.metadata.get("room_name") if isinstance(observation.metadata, dict) else None,
                zones=zone_map,
            ),
            map=zone_map,
            limitations=LIMITATIONS,
            metadata={
                "capability_mode": observation.capability_mode,
                "device_motion_state": observation.device_motion_state,
                "calibration_phase": observation.calibration_phase,
                "baseline_available": bool(baseline),
                "zone_fingerprint_count": len(fingerprints),
                "analysis_boundary": "mobile_observations_only_no_direct_cloud_rf",
            },
        )
        self._session_store.add_scan(observation, scan)
        return scan

    def process_batch(self, batch: ObservationBatch) -> TelemetryScan:
        latest: TelemetryScan | None = None
        for observation in batch.observations:
            latest = self.process_observation(observation)
        if latest is None:
            raise ValueError("ObservationBatch requires at least one observation")
        return latest

    def _signal_quality(self, observation: MobileWifiObservation, recent: list[TelemetryScan]) -> SignalQuality:
        visible = observation.visible_access_points
        if visible is None:
            visible = 1 if observation.rssi_dbm is not None or observation.ssid else 0

        rssi_values = [
            scan.signal_quality.rssi_dbm for scan in recent if scan.signal_quality.rssi_dbm is not None
        ]
        if observation.rssi_dbm is not None:
            rssi_values.append(observation.rssi_dbm)
        if len(rssi_values) >= 2:
            rssi_stability = max(0.0, min(1.0, 1.0 - (pstdev(rssi_values) / 12.0)))
        elif observation.rssi_dbm is not None:
            rssi_stability = 0.62
        else:
            rssi_stability = 0.30

        quality_score = _quality_score(
            visible_access_points=visible,
            latency=observation.gateway_latency_ms,
            jitter=observation.jitter_ms,
            packet_loss=observation.packet_loss,
            rssi_stability=rssi_stability,
        )
        return SignalQuality(
            visible_access_points=visible,
            gateway_latency_ms=_round_optional(observation.gateway_latency_ms),
            jitter_ms=_round_optional(observation.jitter_ms),
            packet_loss=_round_optional(observation.packet_loss, digits=4),
            rssi_dbm=_round_optional(observation.rssi_dbm),
            rssi_stability=round(rssi_stability, 3),
            quality_score=round(quality_score, 3),
        )

    def _motion_score(
        self,
        observation: MobileWifiObservation,
        baseline: dict[str, Any] | None,
        recent: list[TelemetryScan],
    ) -> float:
        evidence: list[float] = []
        if baseline and observation.rssi_dbm is not None and baseline.get("rssi_dbm_mean") is not None:
            evidence.append(min(1.0, abs(observation.rssi_dbm - float(baseline["rssi_dbm_mean"])) / 14.0))
        elif observation.rssi_dbm is not None and recent:
            previous = [scan.signal_quality.rssi_dbm for scan in recent[-5:] if scan.signal_quality.rssi_dbm is not None]
            if previous:
                evidence.append(min(1.0, abs(observation.rssi_dbm - (sum(previous) / len(previous))) / 16.0))

        if observation.gateway_latency_ms is not None:
            reference = float(baseline.get("gateway_latency_ms_mean", 35.0)) if baseline else 35.0
            evidence.append(min(1.0, abs(observation.gateway_latency_ms - reference) / 180.0))
        if observation.jitter_ms is not None:
            reference = float(baseline.get("jitter_ms_mean", 8.0)) if baseline else 8.0
            evidence.append(min(1.0, abs(observation.jitter_ms - reference) / 80.0))
        if observation.packet_loss is not None:
            evidence.append(min(1.0, observation.packet_loss * 3.5))

        score = sum(evidence) / len(evidence) if evidence else 0.08
        if str(observation.device_motion_state).lower() in {"walking", "moving", "vehicle", "unstable"}:
            score = min(1.0, score + 0.18)
        return round(max(0.0, min(1.0, score)), 3)

    def _zone_map(
        self,
        observation: MobileWifiObservation,
        fingerprints: list[ZoneFingerprint],
        motion_score: float,
    ) -> dict[str, float]:
        if observation.zone_label:
            return {observation.zone_label: round(max(0.25, min(0.75, 0.35 + motion_score * 0.35)), 2)}
        if not fingerprints:
            return {"unknown": round(max(0.05, min(0.45, motion_score * 0.45)), 2)}

        scores: dict[str, float] = {}
        for fingerprint in fingerprints:
            distance = 0.0
            weights = 0
            if observation.rssi_dbm is not None and fingerprint.rssi_dbm_mean is not None:
                distance += abs(observation.rssi_dbm - fingerprint.rssi_dbm_mean) / 18.0
                weights += 1
            if observation.gateway_latency_ms is not None and fingerprint.gateway_latency_ms_mean is not None:
                distance += abs(observation.gateway_latency_ms - fingerprint.gateway_latency_ms_mean) / 160.0
                weights += 1
            if observation.jitter_ms is not None and fingerprint.jitter_ms_mean is not None:
                distance += abs(observation.jitter_ms - fingerprint.jitter_ms_mean) / 80.0
                weights += 1
            if weights == 0:
                score = 0.20
            else:
                score = 1.0 / (1.0 + exp((distance / weights) * 2.5))
            scores[fingerprint.zone_label] = max(scores.get(fingerprint.zone_label, 0.0), round(score, 3))

        return {zone: round(min(0.80, value), 2) for zone, value in scores.items()} or {"unknown": 0.1}

    def _presence(self, motion_score: float, signal_quality: SignalQuality) -> str:
        if signal_quality.quality_score < 0.22 or (signal_quality.packet_loss is not None and signal_quality.packet_loss > 0.70):
            return "unstable_scan"
        if motion_score >= 0.62:
            return "possible_presence"
        if motion_score >= 0.30:
            return "possible_motion"
        return "clear"

    def _confidence_ceiling(
        self,
        signal_quality: SignalQuality,
        observation: MobileWifiObservation,
        zone_map: dict[str, float],
    ) -> float:
        ceiling = self.confidence_cap
        if signal_quality.quality_score < 0.50:
            ceiling = min(ceiling, 0.52)
        if signal_quality.quality_score < 0.30:
            ceiling = min(ceiling, 0.42)
        if str(observation.device_motion_state).lower() in {"walking", "moving", "vehicle", "unstable"}:
            ceiling = min(ceiling, 0.48)
        if "unknown" in zone_map:
            ceiling = min(ceiling, 0.50)
        return round(ceiling, 2)


def _quality_score(
    visible_access_points: int,
    latency: float | None,
    jitter: float | None,
    packet_loss: float | None,
    rssi_stability: float,
) -> float:
    ap_score = min(1.0, visible_access_points / 3.0)
    latency_score = 0.75 if latency is None else max(0.0, 1.0 - (latency / 400.0))
    jitter_score = 0.70 if jitter is None else max(0.0, 1.0 - (jitter / 140.0))
    loss_score = 0.65 if packet_loss is None else max(0.0, 1.0 - (packet_loss * 4.0))
    return (
        ap_score * 0.22
        + latency_score * 0.18
        + jitter_score * 0.14
        + loss_score * 0.18
        + rssi_stability * 0.28
    )


def _round_optional(value: float | None, digits: int = 3) -> float | None:
    if value is None:
        return None
    return round(float(value), digits)

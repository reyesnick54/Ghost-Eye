"""Deterministic analyzer for S3M service deployments without S3M-Core."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.schemas.ai import AIAnalysis


class FallbackAIAnalyzer:
    provider = "s3m_service_fallback"

    def analyze_scan(self, scan: dict[str, Any], metadata: dict[str, Any] | None = None) -> AIAnalysis:
        confidence = _confidence(scan)
        risks = _risks(scan)
        calibration = _calibration(scan)
        return AIAnalysis(
            summary=_summary(scan),
            confidence_explanation=(
                f"Analysis uses GhostEye scan confidence {confidence:.2f}; it does not raise confidence "
                "above the mobile WiFi-only non-CSI telemetry ceiling."
            ),
            false_positive_risks=risks,
            calibration_recommendations=calibration,
            operator_notes=[
                "Analysis is advisory and bounded to mobile-submitted network observations.",
                "No exact object identity, person identity, or precise through-wall location is inferred.",
            ],
            recommended_next_action=_next_action(scan, risks, calibration),
            provider=self.provider,
            confidence=confidence,
            created_at=datetime.now(timezone.utc),
            metadata={"s3m_core_available": False, **(metadata or {})},
        )

    def analyze_session(self, session: dict[str, Any], metadata: dict[str, Any] | None = None) -> AIAnalysis:
        latest_scan = session.get("latest_scan") if isinstance(session.get("latest_scan"), dict) else {}
        analysis = self.analyze_scan(latest_scan, metadata=metadata)
        scan_count = int(session.get("scan_count") or 0)
        session_id = str(session.get("session_id") or "unknown")
        return analysis.model_copy(
            update={
                "summary": f"Session {session_id} includes {scan_count} scans. {analysis.summary}",
                "metadata": {**analysis.metadata, "session_id": session_id, "scan_count": scan_count},
            }
        )

    def recommend_calibration(self, payload: dict[str, Any]) -> AIAnalysis:
        latest_scan = payload.get("latest_scan") if isinstance(payload.get("latest_scan"), dict) else {}
        baseline = payload.get("existing_baseline")
        fingerprints = payload.get("zone_fingerprints") if isinstance(payload.get("zone_fingerprints"), list) else []
        recommendations: list[str] = []
        if not baseline:
            recommendations.append("Run empty-room calibration before interpreting live scans.")
        if not fingerprints:
            recommendations.append("Collect zone fingerprints for each coarse zone in the room.")
        if latest_scan and _quality_score(latest_scan) < 0.45:
            recommendations.append("Improve mobile WiFi observation quality before collecting more calibration samples.")
        if not recommendations:
            recommendations.append("Refresh calibration after material changes, router movement, or room layout changes.")

        return AIAnalysis(
            summary="Calibration review completed for GhostEye mobile WiFi-only telemetry.",
            confidence_explanation="Calibration guidance is rules-based and does not alter scan confidence.",
            false_positive_risks=_risks(latest_scan),
            calibration_recommendations=recommendations,
            operator_notes=["Use calibration only in authorized, consent-based controlled rooms."],
            recommended_next_action=recommendations[0],
            provider=self.provider,
            confidence=_confidence(latest_scan),
            created_at=datetime.now(timezone.utc),
            metadata={"s3m_core_available": False, "team_id": payload.get("team_id"), "room_id": payload.get("room_id")},
        )


def _summary(scan: dict[str, Any]) -> str:
    presence = str(scan.get("presence") or "unknown")
    zone = str(scan.get("zone") or "unknown")
    motion = float(scan.get("motion_score") or 0.0)
    if presence == "clear":
        return f"Telemetry is consistent with clear conditions in coarse zone {zone}."
    if presence == "unstable_scan":
        return "Telemetry is unstable; network quality should be improved before interpretation."
    return f"Telemetry reports {presence.replace('_', ' ')} with motion score {motion:.2f} in coarse zone {zone}."


def _risks(scan: dict[str, Any]) -> list[str]:
    signal_quality = scan.get("signal_quality") if isinstance(scan.get("signal_quality"), dict) else {}
    metadata = scan.get("metadata") if isinstance(scan.get("metadata"), dict) else {}
    risks: list[str] = []
    if not metadata.get("baseline_available"):
        risks.append("missing_empty_room_baseline")
    if int(metadata.get("zone_fingerprint_count") or 0) <= 0:
        risks.append("missing_zone_fingerprints")
    if float(signal_quality.get("packet_loss") or 0.0) > 0.10:
        risks.append("packet_loss")
    if float(signal_quality.get("jitter_ms") or 0.0) > 35.0:
        risks.append("high_jitter")
    if float(signal_quality.get("rssi_stability") or 0.0) < 0.45:
        risks.append("unstable_rssi")
    return risks


def _calibration(scan: dict[str, Any]) -> list[str]:
    metadata = scan.get("metadata") if isinstance(scan.get("metadata"), dict) else {}
    recommendations: list[str] = []
    if not metadata.get("baseline_available"):
        recommendations.append("Run empty-room calibration.")
    if int(metadata.get("zone_fingerprint_count") or 0) <= 0:
        recommendations.append("Run zone calibration for coarse room zones.")
    return recommendations or ["Keep calibration current when the room or router placement changes."]


def _next_action(scan: dict[str, Any], risks: list[str], calibration: list[str]) -> str:
    if str(scan.get("presence")) == "unstable_scan":
        return "Improve observation quality and send another mobile WiFi scan."
    if risks:
        return calibration[0]
    return "Continue analysis-only monitoring with calibrated mobile observations."


def _confidence(scan: dict[str, Any]) -> float:
    try:
        return max(0.0, min(1.0, float(scan.get("confidence") or 0.0)))
    except (TypeError, ValueError):
        return 0.0


def _quality_score(scan: dict[str, Any]) -> float:
    quality = scan.get("signal_quality") if isinstance(scan.get("signal_quality"), dict) else {}
    try:
        return max(0.0, min(1.0, float(quality.get("quality_score") or 0.0)))
    except (TypeError, ValueError):
        return 0.0

"""Deterministic analysis fallback for hosted GhostEye telemetry."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.schemas.ai import AIAnalysis
from app.schemas.sessions import SessionSummary
from app.schemas.telemetry import TelemetryScan


class FallbackAIAnalyzer:
    """Rules-based advisory analyzer used when S3M service is unavailable."""

    provider = "ghosteye_cloud_fallback"

    def analyze_scan(self, scan: TelemetryScan, metadata: dict[str, Any] | None = None) -> AIAnalysis:
        risks = self._risks(scan)
        recommendations = self._calibration_recommendations(scan)
        return AIAnalysis(
            summary=self._summary(scan),
            confidence_explanation=(
                f"Analysis confidence is capped to scan confidence {scan.confidence:.2f} and "
                f"non-CSI ceiling {scan.confidence_ceiling:.2f}. The cloud service has no direct "
                "RF view and only analyzes mobile-submitted network observations."
            ),
            false_positive_risks=risks,
            calibration_recommendations=recommendations,
            operator_notes=[
                "Treat output as probabilistic telemetry for controlled environments.",
                "Do not interpret WiFi-only non-CSI results as exact person, object, or through-wall localization.",
            ],
            recommended_next_action=self._next_action(scan, risks, recommendations),
            provider=self.provider,
            confidence=scan.confidence,
            created_at=datetime.now(timezone.utc),
            metadata={
                "fallback_reason": "s3m_ai_service_unavailable_or_not_configured",
                "scan_id": scan.scan_id,
                **(metadata or {}),
            },
        )

    def analyze_session(self, session: SessionSummary, metadata: dict[str, Any] | None = None) -> AIAnalysis:
        latest = session.latest_scan
        if latest is None:
            return AIAnalysis(
                summary="No scans are available for this session yet.",
                confidence_explanation="No scan confidence exists because the session has no telemetry.",
                false_positive_risks=["no_session_telemetry"],
                calibration_recommendations=["Send mobile WiFi observations before requesting session analysis."],
                operator_notes=["Session analysis is analysis-only and requires mobile-provided observations."],
                recommended_next_action="Send a mobile observation batch and retry analysis.",
                provider=self.provider,
                confidence=0.0,
                created_at=datetime.now(timezone.utc),
                metadata={"session_id": session.session_id, **(metadata or {})},
            )

        analysis = self.analyze_scan(latest, metadata=metadata)
        return analysis.model_copy(
            update={
                "summary": f"Session {session.session_id} has {session.scan_count} scans. {analysis.summary}",
                "metadata": {**analysis.metadata, "session_id": session.session_id, "scan_count": session.scan_count},
            }
        )

    @staticmethod
    def _summary(scan: TelemetryScan) -> str:
        if scan.presence == "clear":
            return f"Latest telemetry is consistent with a clear environment in coarse zone {scan.zone}."
        if scan.presence == "unstable_scan":
            return "Latest telemetry is unstable; improve network observation quality before interpreting motion."
        return (
            f"Latest telemetry indicates {scan.presence.replace('_', ' ')} with motion score "
            f"{scan.motion_score:.2f} in coarse zone {scan.zone}."
        )

    @staticmethod
    def _risks(scan: TelemetryScan) -> list[str]:
        risks: list[str] = []
        if not scan.metadata.get("baseline_available"):
            risks.append("missing_empty_room_baseline")
        if int(scan.metadata.get("zone_fingerprint_count") or 0) <= 0:
            risks.append("missing_zone_fingerprints")
        if scan.signal_quality.packet_loss is not None and scan.signal_quality.packet_loss > 0.10:
            risks.append("packet_loss_degrades_inference")
        if scan.signal_quality.jitter_ms is not None and scan.signal_quality.jitter_ms > 35:
            risks.append("high_gateway_jitter")
        if scan.signal_quality.rssi_stability < 0.45:
            risks.append("unstable_rssi")
        if scan.metadata.get("device_motion_state") in {"moving", "walking", "vehicle", "unstable"}:
            risks.append("mobile_device_motion")
        return risks

    @staticmethod
    def _calibration_recommendations(scan: TelemetryScan) -> list[str]:
        recommendations: list[str] = []
        if not scan.metadata.get("baseline_available"):
            recommendations.append("Run empty-room calibration for this room and team.")
        if int(scan.metadata.get("zone_fingerprint_count") or 0) <= 0:
            recommendations.append("Run zone calibration samples for each coarse room zone.")
        if not recommendations:
            recommendations.append("Refresh calibration if furniture, router placement, or phone position changes.")
        return recommendations

    @staticmethod
    def _next_action(scan: TelemetryScan, risks: list[str], recommendations: list[str]) -> str:
        if scan.presence == "unstable_scan":
            return "Improve mobile WiFi observation quality, keep the phone stationary, and send another scan."
        if risks:
            return recommendations[0]
        return "Continue monitoring the calibrated session and compare changes against baseline."

"""Zone-level inference from fingerprints and tomographic projections."""

from __future__ import annotations

from dataclasses import dataclass

from .confidence import ConfidenceScore
from .room_fingerprint_mapper import FingerprintMatch
from .rss_tomography import TomographyCell


@dataclass(frozen=True)
class ZoneEstimate:
    """Best-effort zone estimate for a sensing interval."""

    zone_id: str
    confidence: ConfidenceScore
    source: str


class ZoneClassifier:
    """Chooses a zone from room fingerprints or RSS tomography cells."""

    def classify(
        self,
        fingerprint: FingerprintMatch | None = None,
        tomography_cell: TomographyCell | None = None,
    ) -> ZoneEstimate:
        if fingerprint is not None and fingerprint.confidence >= 0.45:
            return ZoneEstimate(
                zone_id=fingerprint.label,
                confidence=ConfidenceScore(
                    value=fingerprint.confidence,
                    reason="room fingerprint match",
                ),
                source="fingerprint",
            )

        if tomography_cell is not None:
            value = min(tomography_cell.weight / 10.0, 1.0)
            return ZoneEstimate(
                zone_id=tomography_cell.cell_id,
                confidence=ConfidenceScore(value=value, reason="RSS tomography cell"),
                source="tomography",
            )

        return ZoneEstimate(
            zone_id="unknown",
            confidence=ConfidenceScore(value=0.0, reason="no zone evidence"),
            source="none",
        )

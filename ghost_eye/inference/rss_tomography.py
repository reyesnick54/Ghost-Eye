"""Coarse RSS tomographic projection for WiFi-only sensing."""
"""Opportunistic RSSI fingerprint disturbance localization.

This module deliberately does not implement true RF imaging or computed
tomography. It uses changes in received signal strength (RSSI) relative to a
baseline and compares those changes to saved zone fingerprints. The resulting
heatmap is probabilistic evidence for disturbance localization, not an image of
objects, bodies, or RF propagation through space.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class TomographyCell:
    """One coarse tomographic grid cell."""

    cell_id: str
    weight: float


class RssTomography:
    """Projects RSSI residuals onto preconfigured link-to-cell weights."""

    def __init__(self, link_weights: Mapping[str, Mapping[str, float]] | None = None) -> None:
        self.link_weights = {
            link.lower(): dict(weights)
            for link, weights in (link_weights or {}).items()
        }

    def project(self, residuals_db: Mapping[str, float]) -> tuple[TomographyCell, ...]:
        cell_scores: dict[str, float] = {}
        for link, residual in residuals_db.items():
            weights = self.link_weights.get(link.lower(), {})
            for cell_id, weight in weights.items():
                cell_scores[cell_id] = cell_scores.get(cell_id, 0.0) + abs(residual) * weight

        return tuple(
            TomographyCell(cell_id=cell_id, weight=score)
            for cell_id, score in sorted(
                cell_scores.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

    def strongest_cell(
        self,
        residuals_db: Mapping[str, float],
    ) -> TomographyCell | None:
        cells = self.project(residuals_db)
        return cells[0] if cells else None


def average_cells(cells: Iterable[TomographyCell]) -> float:
    cell_tuple = tuple(cells)
    if not cell_tuple:
        return 0.0
    return sum(cell.weight for cell in cell_tuple) / len(cell_tuple)
from math import exp, sqrt
from numbers import Real
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple


Observation = Any
RSSIVector = Dict[str, float]
ZoneFingerprints = Mapping[str, Observation]


@dataclass(frozen=True)
class RSSITomographyResult:
    """Result returned by :class:`OpportunisticRSSITomography`.

    Attributes:
        most_likely_zone: Zone with the highest heatmap score, or ``None`` when
            there is not enough usable RSSI evidence.
        heatmap: Per-zone likelihood-style scores in the range ``0.0`` to
            ``1.0``. Scores are comparable but are not guaranteed to sum to 1.
        confidence_hint: Human-readable confidence bucket derived from evidence
            coverage and top-zone separation.
    """

    most_likely_zone: Optional[str]
    heatmap: Dict[str, float]
    confidence_hint: str

    def as_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""

        return {
            "most_likely_zone": self.most_likely_zone,
            "heatmap": self.heatmap,
            "confidence_hint": self.confidence_hint,
        }


class OpportunisticRSSITomography:
    """Localize RSSI disturbances by comparing observations to fingerprints.

    Despite the name, this is not true RF imaging. It does not reconstruct a
    spatial attenuation field or produce body/shape imagery. It is a pragmatic,
    probabilistic RSSI/fingerprint disturbance localizer: current RSSI readings
    are differenced against a baseline observation, then matched against saved
    per-zone disturbance fingerprints.

    Accepted observations are intentionally lightweight:

    * ``{"ap_a": -61, "ap_b": -70}``
    * ``{"rssi": {"ap_a": -61, "ap_b": -70}}``
    * ``[{"bssid": "ap_a", "rssi": -61}, {"bssid": "ap_b", "rssi": -70}]``

    Zone fingerprints may be direct RSSI-delta vectors, lists of sample vectors,
    or mappings containing one of ``disturbance``, ``delta``, ``rssi_delta``,
    ``fingerprint``, ``centroid``, ``mean``, or ``samples``.
    """

    _VECTOR_KEYS = (
        "disturbance",
        "delta",
        "rssi_delta",
        "fingerprint",
        "centroid",
        "mean",
        "rssi",
        "rssis",
        "signals",
        "readings",
    )
    _SAMPLE_KEYS = ("samples", "fingerprints", "observations")
    _ID_KEYS = ("bssid", "mac", "ap", "ap_id", "id", "ssid", "sensor", "source")
    _RSSI_KEYS = ("rssi", "rss", "signal", "signal_dbm", "dbm", "value")

    def __init__(
        self,
        *,
        distance_scale_db: float = 10.0,
        min_common_signals: int = 1,
        score_precision: int = 2,
    ) -> None:
        """Create a localizer.

        Args:
            distance_scale_db: RMS RSSI-delta mismatch that should reduce a
                zone score by roughly ``e^-1`` before coverage weighting.
            min_common_signals: Minimum shared signal IDs needed before a match
                can receive a medium/high confidence hint.
            score_precision: Decimal places used in returned heatmap scores.
        """

        if distance_scale_db <= 0:
            raise ValueError("distance_scale_db must be positive")
        if min_common_signals < 1:
            raise ValueError("min_common_signals must be at least 1")
        if score_precision < 0:
            raise ValueError("score_precision must not be negative")

        self.distance_scale_db = float(distance_scale_db)
        self.min_common_signals = int(min_common_signals)
        self.score_precision = int(score_precision)

    def infer(
        self,
        current_observation: Observation,
        baseline_observation: Observation,
        saved_zone_fingerprints: ZoneFingerprints,
    ) -> RSSITomographyResult:
        """Infer the most likely disturbed zone.

        Args:
            current_observation: Current RSSI readings.
            baseline_observation: Baseline RSSI readings captured with no
                expected disturbance.
            saved_zone_fingerprints: Mapping of zone ID to saved disturbance
                fingerprint(s).

        Returns:
            ``RSSITomographyResult`` containing ``most_likely_zone``,
            ``heatmap``, and ``confidence_hint``.
        """

        if not isinstance(saved_zone_fingerprints, Mapping):
            raise TypeError("saved_zone_fingerprints must be a mapping of zone ID to fingerprint")

        disturbance = self._build_disturbance_vector(current_observation, baseline_observation)
        if not saved_zone_fingerprints:
            return RSSITomographyResult(None, {}, "insufficient_data")

        if not disturbance:
            empty_heatmap = {
                str(zone): 0.0
                for zone in saved_zone_fingerprints
            }
            return RSSITomographyResult(None, empty_heatmap, "insufficient_data")

        heatmap: Dict[str, float] = {}
        best_zone: Optional[str] = None
        best_score = -1.0
        best_common_count = 0

        for zone, fingerprint in saved_zone_fingerprints.items():
            zone_id = str(zone)
            fingerprint_vector = self._fingerprint_to_vector(fingerprint)
            score, common_count = self._score_zone(disturbance, fingerprint_vector)
            rounded_score = round(score, self.score_precision)
            heatmap[zone_id] = rounded_score

            if score > best_score:
                best_zone = zone_id
                best_score = score
                best_common_count = common_count

        if best_score <= 0:
            return RSSITomographyResult(None, heatmap, "insufficient_data")

        return RSSITomographyResult(
            most_likely_zone=best_zone,
            heatmap=heatmap,
            confidence_hint=self._confidence_hint(
                scores=heatmap,
                best_zone=best_zone,
                best_common_count=best_common_count,
            ),
        )

    def infer_dict(
        self,
        current_observation: Observation,
        baseline_observation: Observation,
        saved_zone_fingerprints: ZoneFingerprints,
    ) -> Dict[str, Any]:
        """Infer zones and return the result as a plain dictionary."""

        return self.infer(
            current_observation=current_observation,
            baseline_observation=baseline_observation,
            saved_zone_fingerprints=saved_zone_fingerprints,
        ).as_dict()

    __call__ = infer

    def _build_disturbance_vector(
        self,
        current_observation: Observation,
        baseline_observation: Observation,
    ) -> RSSIVector:
        current = self._observation_to_vector(current_observation)
        baseline = self._observation_to_vector(baseline_observation)

        shared_keys = current.keys() & baseline.keys()
        return {
            key: current[key] - baseline[key]
            for key in shared_keys
        }

    def _fingerprint_to_vector(self, fingerprint: Observation) -> RSSIVector:
        if isinstance(fingerprint, Mapping):
            for sample_key in self._SAMPLE_KEYS:
                samples = fingerprint.get(sample_key)
                if isinstance(samples, Iterable) and not isinstance(samples, (str, bytes, Mapping)):
                    return self._average_vectors(
                        self._fingerprint_to_vector(sample)
                        for sample in samples
                    )

            for vector_key in self._VECTOR_KEYS:
                if vector_key in fingerprint:
                    return self._observation_to_vector(fingerprint[vector_key])

        if isinstance(fingerprint, Iterable) and not isinstance(fingerprint, (str, bytes, Mapping)):
            return self._average_vectors(
                self._observation_to_vector(sample)
                for sample in fingerprint
            )

        return self._observation_to_vector(fingerprint)

    def _observation_to_vector(self, observation: Observation) -> RSSIVector:
        if observation is None:
            return {}

        if isinstance(observation, Mapping):
            nested_vector = self._extract_nested_vector(observation)
            if nested_vector is not None:
                return nested_vector

            reading = self._extract_reading(observation)
            if reading is not None:
                signal_id, rssi = reading
                return {signal_id: rssi}

            return {
                str(signal_id): float(rssi)
                for signal_id, rssi in observation.items()
                if self._is_number(rssi)
            }

        if isinstance(observation, Iterable) and not isinstance(observation, (str, bytes)):
            return self._average_vectors(
                self._observation_to_vector(reading)
                for reading in observation
            )

        return {}

    def _extract_nested_vector(self, observation: Mapping[str, Any]) -> Optional[RSSIVector]:
        for vector_key in self._VECTOR_KEYS:
            nested = observation.get(vector_key)
            if nested is None:
                continue

            nested_vector = self._observation_to_vector(nested)
            if nested_vector:
                return nested_vector

        return None

    def _extract_reading(self, reading: Mapping[str, Any]) -> Optional[Tuple[str, float]]:
        signal_id = None
        for id_key in self._ID_KEYS:
            value = reading.get(id_key)
            if value is not None:
                signal_id = str(value)
                break

        if signal_id is None:
            return None

        for rssi_key in self._RSSI_KEYS:
            value = reading.get(rssi_key)
            if self._is_number(value):
                return signal_id, float(value)

        return None

    def _score_zone(self, disturbance: RSSIVector, fingerprint: RSSIVector) -> Tuple[float, int]:
        if not disturbance or not fingerprint:
            return 0.0, 0

        common_keys = disturbance.keys() & fingerprint.keys()
        common_count = len(common_keys)
        if common_count == 0:
            return 0.0, 0

        squared_error = sum(
            (disturbance[key] - fingerprint[key]) ** 2
            for key in common_keys
        )
        rms_error = sqrt(squared_error / common_count)

        coverage = common_count / max(len(disturbance), len(fingerprint))
        score = exp(-rms_error / self.distance_scale_db) * sqrt(coverage)
        return min(1.0, max(0.0, score)), common_count

    def _confidence_hint(
        self,
        *,
        scores: Mapping[str, float],
        best_zone: Optional[str],
        best_common_count: int,
    ) -> str:
        if not best_zone or best_zone not in scores or best_common_count < self.min_common_signals:
            return "low"

        sorted_scores = sorted(scores.values(), reverse=True)
        best_score = sorted_scores[0] if sorted_scores else 0.0
        second_score = sorted_scores[1] if len(sorted_scores) > 1 else 0.0

        if best_score <= 0:
            return "insufficient_data"

        separation = (best_score - second_score) / best_score

        if best_score >= 0.65 and separation >= 0.35:
            return "high"
        if best_score >= 0.35 and separation >= 0.15:
            return "medium"
        return "low"

    @staticmethod
    def _average_vectors(vectors: Iterable[RSSIVector]) -> RSSIVector:
        sums: Dict[str, float] = {}
        counts: Dict[str, int] = {}

        for vector in vectors:
            for signal_id, rssi in vector.items():
                sums[signal_id] = sums.get(signal_id, 0.0) + rssi
                counts[signal_id] = counts.get(signal_id, 0) + 1

        return {
            signal_id: sums[signal_id] / counts[signal_id]
            for signal_id in sums
        }

    @staticmethod
    def _is_number(value: Any) -> bool:
        return isinstance(value, Real) and not isinstance(value, bool)

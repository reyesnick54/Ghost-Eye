"""Map WiFi observations to saved room fingerprints.

The mapper intentionally keeps fingerprints as small JSON documents so demos can
capture and reuse room signatures without introducing a database dependency.
"""

from __future__ import annotations

import json
import math
import re
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Tuple


NumberMap = Dict[str, float]


class ZoneComparison(dict):
    """Dictionary result that can also be treated as its numeric score."""

    def __float__(self) -> float:
        return float(self.get("score", 0.0))

    def __lt__(self, other: object) -> bool:
        return float(self) < _coerce_score(other)

    def __le__(self, other: object) -> bool:
        return float(self) <= _coerce_score(other)

    def __gt__(self, other: object) -> bool:
        return float(self) > _coerce_score(other)

    def __ge__(self, other: object) -> bool:
        return float(self) >= _coerce_score(other)


def _coerce_score(value: object) -> float:
    if isinstance(value, Mapping):
        return float(value.get("score", 0.0))
    return float(value)  # type: ignore[arg-type]


class RoomFingerprintMapper:
    """Create, compare, and estimate room fingerprints from WiFi observations."""

    DEFAULT_FINGERPRINT_DIR = (
        Path(__file__).resolve().parents[1] / "sessions" / "fingerprints"
    )

    DEFAULT_WEIGHTS = {
        "cosine_rssi": 0.30,
        "euclidean_rssi": 0.25,
        "weighted_rssi": 0.25,
        "latency": 0.10,
        "jitter": 0.10,
    }

    def __init__(
        self,
        fingerprint_dir: Optional[Path | str] = None,
        weights: Optional[Mapping[str, float]] = None,
    ) -> None:
        self.fingerprint_dir = Path(fingerprint_dir or self.DEFAULT_FINGERPRINT_DIR)
        merged_weights = dict(self.DEFAULT_WEIGHTS)
        if weights:
            merged_weights.update({key: float(value) for key, value in weights.items()})
        self.weights = self._normalize_weights(merged_weights)

    def create_fingerprint(
        self, zone_name: str, observation: Mapping[str, Any]
    ) -> Dict[str, Any]:
        """Create and persist a JSON fingerprint for ``zone_name``.

        The returned fingerprint is a plain dictionary suitable for storing,
        transmitting, or passing directly to :meth:`compare_to_zone`.
        """

        zone = str(zone_name).strip()
        if not zone:
            raise ValueError("zone_name must not be empty")

        features = self._extract_features(observation)
        fingerprint = {
            "zone": zone,
            "created_at": time.time(),
            "samples": 1,
            "rssi": features["rssi"],
            "rssi_weights": self._rssi_weights(features["rssi"], features["rssi_weights"]),
            "latency_ms": features["latency_ms"],
            "jitter_ms": features["jitter_ms"],
        }

        self._write_fingerprint(fingerprint)
        return fingerprint

    def compare_to_zone(
        self, observation: Mapping[str, Any], zone_fingerprint: Mapping[str, Any]
    ) -> ZoneComparison:
        """Compare an observation to one saved zone fingerprint.

        Returns a dictionary containing the zone, combined score, individual
        metric scores, and a confidence hint. The object can also be compared as
        a float for callers that only need the combined score.
        """

        observed = self._extract_features(observation)
        fingerprint = self._extract_features(zone_fingerprint)

        cosine_rssi = self._cosine_similarity(
            self._rssi_quality_vector(observed["rssi"]),
            self._rssi_quality_vector(fingerprint["rssi"]),
        )
        euclidean_rssi = self._euclidean_similarity(
            self._rssi_quality_vector(observed["rssi"]),
            self._rssi_quality_vector(fingerprint["rssi"]),
        )
        weighted_rssi = self._weighted_rssi_similarity(
            observed["rssi"],
            fingerprint["rssi"],
            fingerprint["rssi_weights"] or observed["rssi_weights"],
        )
        latency = self._timing_similarity(
            observed["latency_ms"],
            fingerprint["latency_ms"],
            scale_ms=100.0,
        )
        jitter = self._timing_similarity(
            observed["jitter_ms"],
            fingerprint["jitter_ms"],
            scale_ms=50.0,
        )

        metrics = {
            "cosine_rssi": cosine_rssi,
            "euclidean_rssi": euclidean_rssi,
            "weighted_rssi": weighted_rssi,
            "gateway_latency": latency,
            "jitter": jitter,
        }
        weighted_metrics = {
            "cosine_rssi": cosine_rssi,
            "euclidean_rssi": euclidean_rssi,
            "weighted_rssi": weighted_rssi,
            "latency": latency,
            "jitter": jitter,
        }
        score = self._weighted_average(weighted_metrics)

        return ZoneComparison(
            {
                "zone": str(zone_fingerprint.get("zone", "unknown")),
                "score": round(score, 6),
                "metrics": {key: round(value, 6) for key, value in metrics.items()},
                "confidence_hint": self._confidence_hint(score, None),
            }
        )

    def estimate_zone(
        self,
        observation: Mapping[str, Any],
        saved_fingerprints: Optional[
            Mapping[str, Mapping[str, Any]] | Iterable[Mapping[str, Any]] | str | Path
        ] = None,
    ) -> Dict[str, Any]:
        """Estimate the best zone for an observation.

        ``saved_fingerprints`` may be a zone-to-fingerprint mapping, an iterable
        of fingerprint dictionaries, a JSON file, a directory of JSON files, or
        ``None`` to load from the mapper's fingerprint directory.
        """

        fingerprints = self._load_fingerprints(saved_fingerprints)
        if not fingerprints:
            return {
                "zone": "unknown",
                "zone_scores": {},
                "confidence_hint": "low",
            }

        comparisons = [self.compare_to_zone(observation, item) for item in fingerprints]
        comparisons.sort(key=lambda item: float(item), reverse=True)

        zone_scores = {
            str(item["zone"]): round(float(item), 6) for item in comparisons
        }
        best = comparisons[0]
        runner_up = float(comparisons[1]) if len(comparisons) > 1 else None

        return {
            "zone": best["zone"],
            "zone_scores": zone_scores,
            "confidence_hint": self._confidence_hint(float(best), runner_up),
        }

    def _write_fingerprint(self, fingerprint: Mapping[str, Any]) -> Path:
        self.fingerprint_dir.mkdir(parents=True, exist_ok=True)
        path = self.fingerprint_dir / f"{self._slug(str(fingerprint['zone']))}.json"
        path.write_text(json.dumps(fingerprint, indent=2, sort_keys=True) + "\n")
        return path

    def _load_fingerprints(
        self,
        saved_fingerprints: Optional[
            Mapping[str, Mapping[str, Any]] | Iterable[Mapping[str, Any]] | str | Path
        ],
    ) -> List[Mapping[str, Any]]:
        source = saved_fingerprints
        if source is None:
            source = self.fingerprint_dir

        if isinstance(source, (str, Path)):
            path = Path(source)
            if path.is_dir():
                return [
                    self._read_json(item)
                    for item in sorted(path.glob("*.json"))
                    if item.is_file()
                ]
            if path.is_file():
                data = self._read_json(path)
                if isinstance(data, list):
                    return [item for item in data if isinstance(item, Mapping)]
                if isinstance(data, Mapping):
                    return self._fingerprints_from_mapping(data)
            return []

        if isinstance(source, Mapping):
            return self._fingerprints_from_mapping(source)

        return [item for item in source if isinstance(item, Mapping)]

    def _fingerprints_from_mapping(
        self, value: Mapping[str, Any]
    ) -> List[Mapping[str, Any]]:
        if "zone" in value:
            return [value]

        fingerprints: List[Mapping[str, Any]] = []
        for zone, fingerprint in value.items():
            if not isinstance(fingerprint, Mapping):
                continue
            if "zone" in fingerprint:
                fingerprints.append(fingerprint)
            else:
                copy = dict(fingerprint)
                copy["zone"] = str(zone)
                fingerprints.append(copy)
        return fingerprints

    def _read_json(self, path: Path) -> Any:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _extract_features(self, observation: Mapping[str, Any]) -> Dict[str, NumberMap]:
        rssi: NumberMap = {}
        rssi_weights: NumberMap = {}
        latency_ms: NumberMap = {}
        jitter_ms: NumberMap = {}

        self._merge_number_map(rssi, observation.get("rssi"))
        self._merge_number_map(rssi, observation.get("rssis"))
        self._merge_number_map(rssi, observation.get("rssi_by_gateway"))
        self._merge_number_map(rssi, observation.get("gateway_rssi"))
        self._merge_number_map(rssi_weights, observation.get("rssi_weights"))
        self._merge_number_map(rssi_weights, observation.get("weights"))
        self._merge_number_map(rssi_weights, observation.get("gateway_weights"))
        self._merge_number_map(latency_ms, observation.get("latency_ms"))
        self._merge_number_map(latency_ms, observation.get("latencies"))
        self._merge_number_map(latency_ms, observation.get("gateway_latency_ms"))
        self._merge_number_map(latency_ms, observation.get("gateway_latency"))
        self._merge_number_map(jitter_ms, observation.get("jitter_ms"))
        self._merge_number_map(jitter_ms, observation.get("jitters"))
        self._merge_number_map(jitter_ms, observation.get("gateway_jitter_ms"))
        self._merge_number_map(jitter_ms, observation.get("gateway_jitter"))

        for container_key in ("gateways", "access_points", "aps", "readings", "scan"):
            self._merge_gateway_container(
                observation.get(container_key), rssi, rssi_weights, latency_ms, jitter_ms
            )

        return {
            "rssi": rssi,
            "rssi_weights": rssi_weights,
            "latency_ms": latency_ms,
            "jitter_ms": jitter_ms,
        }

    def _merge_gateway_container(
        self,
        container: Any,
        rssi: MutableMapping[str, float],
        rssi_weights: MutableMapping[str, float],
        latency_ms: MutableMapping[str, float],
        jitter_ms: MutableMapping[str, float],
    ) -> None:
        if isinstance(container, Mapping):
            iterable = container.items()
        elif isinstance(container, Iterable) and not isinstance(container, (str, bytes)):
            iterable = ((None, item) for item in container)
        else:
            return

        for fallback_key, reading in iterable:
            if not isinstance(reading, Mapping):
                continue
            gateway = self._gateway_id(reading, fallback_key)
            if not gateway:
                continue
            self._assign_number(rssi, gateway, self._first_value(reading, ("rssi", "rss")))
            self._assign_number(
                rssi_weights,
                gateway,
                self._first_value(reading, ("weight", "rssi_weight", "confidence")),
            )
            self._assign_number(
                latency_ms,
                gateway,
                self._first_value(reading, ("latency_ms", "latency", "gateway_latency")),
            )
            self._assign_number(
                jitter_ms,
                gateway,
                self._first_value(reading, ("jitter_ms", "jitter", "gateway_jitter")),
            )

    def _gateway_id(self, reading: Mapping[str, Any], fallback_key: Any) -> str:
        for key in ("gateway", "gateway_id", "id", "mac", "bssid", "name"):
            value = reading.get(key)
            if value is not None:
                return str(value)
        return "" if fallback_key is None else str(fallback_key)

    def _first_value(self, reading: Mapping[str, Any], keys: Tuple[str, ...]) -> Any:
        for key in keys:
            if key in reading:
                return reading[key]
        return None

    def _merge_number_map(self, target: MutableMapping[str, float], value: Any) -> None:
        if isinstance(value, Mapping):
            for key, item in value.items():
                self._assign_number(target, str(key), item)
        else:
            self._assign_number(target, "default", value)

    def _assign_number(
        self, target: MutableMapping[str, float], key: str, value: Any
    ) -> None:
        number = self._as_float(value)
        if number is not None:
            target[key] = number

    def _as_float(self, value: Any) -> Optional[float]:
        if value is None or isinstance(value, bool):
            return None
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        if math.isnan(number) or math.isinf(number):
            return None
        return number

    def _rssi_weights(
        self, rssi: Mapping[str, float], supplied_weights: Mapping[str, float]
    ) -> NumberMap:
        if supplied_weights:
            return {
                gateway: max(0.0, weight)
                for gateway, weight in supplied_weights.items()
                if gateway in rssi and weight > 0.0
            }

        quality = self._rssi_quality_vector(rssi)
        return {gateway: max(value, 0.05) for gateway, value in quality.items()}

    def _rssi_quality_vector(self, rssi: Mapping[str, float]) -> NumberMap:
        return {
            gateway: self._rssi_to_quality(value) for gateway, value in rssi.items()
        }

    def _rssi_to_quality(self, rssi_value: float) -> float:
        return self._clamp((rssi_value + 100.0) / 70.0)

    def _cosine_similarity(self, left: Mapping[str, float], right: Mapping[str, float]) -> float:
        keys = set(left) | set(right)
        if not keys:
            return 0.5

        dot = sum(left.get(key, 0.0) * right.get(key, 0.0) for key in keys)
        left_norm = math.sqrt(sum(left.get(key, 0.0) ** 2 for key in keys))
        right_norm = math.sqrt(sum(right.get(key, 0.0) ** 2 for key in keys))
        if left_norm == 0.0 and right_norm == 0.0:
            return 1.0
        if left_norm == 0.0 or right_norm == 0.0:
            return 0.0
        return self._clamp(dot / (left_norm * right_norm))

    def _euclidean_similarity(
        self, left: Mapping[str, float], right: Mapping[str, float]
    ) -> float:
        keys = set(left) | set(right)
        if not keys:
            return 0.5
        mean_squared_distance = sum(
            (left.get(key, 0.0) - right.get(key, 0.0)) ** 2 for key in keys
        ) / len(keys)
        return self._clamp(1.0 - math.sqrt(mean_squared_distance))

    def _weighted_rssi_similarity(
        self,
        observed_rssi: Mapping[str, float],
        fingerprint_rssi: Mapping[str, float],
        weights: Mapping[str, float],
    ) -> float:
        keys = set(observed_rssi) | set(fingerprint_rssi)
        if not keys:
            return 0.5

        observed = self._rssi_quality_vector(observed_rssi)
        fingerprint = self._rssi_quality_vector(fingerprint_rssi)
        fallback_weight = 1.0 / len(keys)

        total_weight = 0.0
        weighted_distance = 0.0
        for key in keys:
            weight = max(float(weights.get(key, fallback_weight)), 0.0)
            total_weight += weight
            weighted_distance += weight * abs(observed.get(key, 0.0) - fingerprint.get(key, 0.0))

        if total_weight == 0.0:
            return self._euclidean_similarity(observed, fingerprint)
        return self._clamp(1.0 - (weighted_distance / total_weight))

    def _timing_similarity(
        self,
        observed: Mapping[str, float],
        fingerprint: Mapping[str, float],
        scale_ms: float,
    ) -> float:
        keys = set(observed) | set(fingerprint)
        if not keys:
            return 0.5

        total_distance = 0.0
        for key in keys:
            if key in observed and key in fingerprint:
                total_distance += abs(observed[key] - fingerprint[key])
            else:
                total_distance += scale_ms

        mean_distance = total_distance / len(keys)
        return self._clamp(1.0 / (1.0 + (mean_distance / scale_ms)))

    def _weighted_average(self, metrics: Mapping[str, float]) -> float:
        weighted_total = 0.0
        weight_total = 0.0
        for key, value in metrics.items():
            weight = max(self.weights.get(key, 0.0), 0.0)
            weighted_total += value * weight
            weight_total += weight
        if weight_total == 0.0:
            return 0.0
        return self._clamp(weighted_total / weight_total)

    def _confidence_hint(self, best_score: float, runner_up_score: Optional[float]) -> str:
        margin = best_score if runner_up_score is None else best_score - runner_up_score
        if best_score >= 0.82 and margin >= 0.10:
            return "high"
        if best_score >= 0.62 and margin >= 0.04:
            return "medium"
        return "low"

    def _normalize_weights(self, weights: Mapping[str, float]) -> Dict[str, float]:
        cleaned = {key: max(float(value), 0.0) for key, value in weights.items()}
        total = sum(cleaned.values())
        if total == 0.0:
            return dict(self.DEFAULT_WEIGHTS)
        return {key: value / total for key, value in cleaned.items()}

    def _slug(self, zone_name: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9_.-]+", "_", zone_name.strip()).strip("._-")
        return slug or "unknown"

    def _clamp(self, value: float, lower: float = 0.0, upper: float = 1.0) -> float:
        return max(lower, min(upper, value))


_DEFAULT_MAPPER = RoomFingerprintMapper()


def create_fingerprint(zone_name: str, observation: Mapping[str, Any]) -> Dict[str, Any]:
    """Create and store a fingerprint using the default mapper."""

    return _DEFAULT_MAPPER.create_fingerprint(zone_name, observation)


def compare_to_zone(
    observation: Mapping[str, Any], zone_fingerprint: Mapping[str, Any]
) -> ZoneComparison:
    """Compare an observation to a zone fingerprint using the default mapper."""

    return _DEFAULT_MAPPER.compare_to_zone(observation, zone_fingerprint)


def estimate_zone(
    observation: Mapping[str, Any],
    saved_fingerprints: Optional[
        Mapping[str, Mapping[str, Any]] | Iterable[Mapping[str, Any]] | str | Path
    ] = None,
) -> Dict[str, Any]:
    """Estimate the best matching zone using the default mapper."""

    return _DEFAULT_MAPPER.estimate_zone(observation, saved_fingerprints)

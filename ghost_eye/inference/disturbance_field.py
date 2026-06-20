"""Disturbance-field based presence inference.

The detector compares a live WiFi/network observation against an empty-room
baseline and turns changes in radio and scan-quality features into a smoothed
motion score.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from numbers import Real
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional, Sequence, Set, Tuple


PresenceState = str

NO_PRESENCE_DETECTED = "no_presence_detected"
POSSIBLE_MOTION = "possible_motion"
POSSIBLE_PRESENCE = "possible_presence"
UNSTABLE_SCAN = "unstable_scan"


_DEFAULT_WEIGHTS = {
    "rssi_delta_score": 0.35,
    "jitter_delta_score": 0.20,
    "latency_delta_score": 0.15,
    "packet_loss_delta_score": 0.15,
    "ap_visibility_delta_score": 0.15,
}


@dataclass(frozen=True)
class DisturbanceFieldResult:
    """Result returned by :class:`DisturbanceFieldDetector`."""

    motion_score: float
    presence_state: PresenceState
    explanation_features: Dict[str, Any]

    def as_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation."""

        return {
            "motion_score": self.motion_score,
            "presence_state": self.presence_state,
            "explanation_features": dict(self.explanation_features),
        }


@dataclass(frozen=True)
class _SignalSummary:
    rssi_values: Tuple[float, ...] = ()
    rssi_by_ap: Mapping[str, float] = field(default_factory=dict)
    jitter_values: Tuple[float, ...] = ()
    latency_values: Tuple[float, ...] = ()
    packet_loss_values: Tuple[float, ...] = ()
    visible_aps: Set[str] = field(default_factory=set)
    visible_ap_count: Optional[int] = None

    def average(self, metric_name: str) -> Optional[float]:
        values = getattr(self, f"{metric_name}_values")
        if not values:
            return None
        return sum(values) / len(values)

    @property
    def has_data(self) -> bool:
        return bool(
            self.rssi_values
            or self.jitter_values
            or self.latency_values
            or self.packet_loss_values
            or self.visible_aps
            or self.visible_ap_count is not None
        )

    @property
    def ap_count(self) -> Optional[int]:
        if self.visible_ap_count is not None:
            return self.visible_ap_count
        if self.visible_aps:
            return len(self.visible_aps)
        if self.rssi_by_ap:
            return len(self.rssi_by_ap)
        return None


@dataclass
class DisturbanceFieldDetector:
    """Detect likely presence from changes in WiFi disturbance features.

    Parameters:
        alpha: Smoothing factor for ``motion_score_t``. A higher value gives
            the current observation more influence; a lower value makes output
            steadier.
        weights: Optional weights for the five component delta scores.
        no_presence_threshold: Scores below this threshold are labeled
            ``no_presence_detected``.
        possible_presence_threshold: Scores at or above this threshold are
            labeled ``possible_presence`` unless scan quality is unstable.
    """

    alpha: float = 0.35
    weights: Optional[Mapping[str, float]] = None
    no_presence_threshold: float = 0.20
    possible_presence_threshold: float = 0.50
    unstable_packet_loss_threshold: float = 0.85
    unstable_network_threshold: float = 0.75
    previous_motion_score: Optional[float] = field(default=None, init=False)

    def __post_init__(self) -> None:
        if not 0.0 <= self.alpha <= 1.0:
            raise ValueError("alpha must be between 0 and 1")
        if not 0.0 <= self.no_presence_threshold <= 1.0:
            raise ValueError("no_presence_threshold must be between 0 and 1")
        if not 0.0 <= self.possible_presence_threshold <= 1.0:
            raise ValueError("possible_presence_threshold must be between 0 and 1")
        if self.no_presence_threshold > self.possible_presence_threshold:
            raise ValueError("no_presence_threshold cannot exceed possible_presence_threshold")

    def reset(self, motion_score: Optional[float] = None) -> None:
        """Reset the smoothing state.

        Args:
            motion_score: Optional seed value for the next smoothed output.
        """

        if motion_score is not None and not 0.0 <= motion_score <= 1.0:
            raise ValueError("motion_score must be between 0 and 1")
        self.previous_motion_score = motion_score

    def detect(
        self,
        current_observation: Any,
        empty_room_baseline: Any,
        adaptive_baseline: Any = None,
    ) -> DisturbanceFieldResult:
        """Compare an observation with baselines and infer presence state.

        The method accepts mappings, simple objects, or lists of per-AP mapping
        entries. Known metric aliases include ``rssi``, ``jitter_ms``,
        ``latency_ms``, ``packet_loss_rate``, ``access_points``, and
        ``visible_aps``.
        """

        current = _summarize_signal(current_observation)
        empty_reference = _summarize_signal(empty_room_baseline)
        adaptive_reference = _summarize_signal(adaptive_baseline) if adaptive_baseline is not None else None
        reference = _merge_reference(adaptive_reference, empty_reference)
        reference_name = "adaptive_baseline" if adaptive_reference is not None else "empty_room_baseline"

        rssi_delta_score = _rssi_delta_score(current, reference)
        jitter_delta_score = _metric_delta_score(
            current.average("jitter"),
            reference.average("jitter"),
            absolute_scale=30.0,
            relative_floor=5.0,
        )
        latency_delta_score = _metric_delta_score(
            current.average("latency"),
            reference.average("latency"),
            absolute_scale=150.0,
            relative_floor=20.0,
        )
        packet_loss_delta_score = _metric_delta_score(
            current.average("packet_loss"),
            reference.average("packet_loss"),
            absolute_scale=0.25,
            relative_floor=0.02,
        )
        ap_visibility_delta_score = _ap_visibility_delta_score(current, reference)

        component_scores = {
            "rssi_delta_score": rssi_delta_score,
            "jitter_delta_score": jitter_delta_score,
            "latency_delta_score": latency_delta_score,
            "packet_loss_delta_score": packet_loss_delta_score,
            "ap_visibility_delta_score": ap_visibility_delta_score,
        }
        current_score = _weighted_score(component_scores, self.weights)
        previous_score = self.previous_motion_score
        motion_score = _clamp(
            self.alpha * current_score + (1.0 - self.alpha) * previous_score
            if previous_score is not None
            else current_score
        )
        self.previous_motion_score = motion_score

        scan_unstable = self._is_unstable_scan(current, reference, component_scores)
        presence_state = self._presence_state(motion_score, scan_unstable)

        explanation_features: Dict[str, Any] = {
            **{key: round(value, 6) for key, value in component_scores.items()},
            "current_score": round(current_score, 6),
            "motion_score_unsmoothed": round(current_score, 6),
            "previous_motion_score": None if previous_score is None else round(previous_score, 6),
            "smoothing_alpha": self.alpha,
            "baseline_source": reference_name,
            "scan_unstable": scan_unstable,
            "current_rssi_avg": _round_optional(current.average("rssi")),
            "baseline_rssi_avg": _round_optional(reference.average("rssi")),
            "current_jitter_avg": _round_optional(current.average("jitter")),
            "baseline_jitter_avg": _round_optional(reference.average("jitter")),
            "current_latency_avg": _round_optional(current.average("latency")),
            "baseline_latency_avg": _round_optional(reference.average("latency")),
            "current_packet_loss_avg": _round_optional(current.average("packet_loss")),
            "baseline_packet_loss_avg": _round_optional(reference.average("packet_loss")),
            "current_visible_ap_count": current.ap_count,
            "baseline_visible_ap_count": reference.ap_count,
        }

        return DisturbanceFieldResult(
            motion_score=round(motion_score, 6),
            presence_state=presence_state,
            explanation_features=explanation_features,
        )

    __call__ = detect

    def _is_unstable_scan(
        self,
        current: _SignalSummary,
        reference: _SignalSummary,
        component_scores: Mapping[str, float],
    ) -> bool:
        if not current.has_data:
            return True

        current_count = current.ap_count
        reference_count = reference.ap_count
        if reference_count and current_count == 0:
            return True

        packet_loss_unstable = (
            component_scores["packet_loss_delta_score"] >= self.unstable_packet_loss_threshold
        )
        network_unstable = (
            component_scores["latency_delta_score"] >= self.unstable_network_threshold
            or component_scores["jitter_delta_score"] >= self.unstable_network_threshold
        )
        return packet_loss_unstable and network_unstable

    def _presence_state(self, motion_score: float, scan_unstable: bool) -> PresenceState:
        if scan_unstable:
            return UNSTABLE_SCAN
        if motion_score < self.no_presence_threshold:
            return NO_PRESENCE_DETECTED
        if motion_score < self.possible_presence_threshold:
            return POSSIBLE_MOTION
        return POSSIBLE_PRESENCE


def _merge_reference(
    adaptive_reference: Optional[_SignalSummary],
    empty_reference: _SignalSummary,
) -> _SignalSummary:
    if adaptive_reference is None:
        return empty_reference

    return _SignalSummary(
        rssi_values=adaptive_reference.rssi_values or empty_reference.rssi_values,
        rssi_by_ap=adaptive_reference.rssi_by_ap or empty_reference.rssi_by_ap,
        jitter_values=adaptive_reference.jitter_values or empty_reference.jitter_values,
        latency_values=adaptive_reference.latency_values or empty_reference.latency_values,
        packet_loss_values=adaptive_reference.packet_loss_values or empty_reference.packet_loss_values,
        visible_aps=adaptive_reference.visible_aps or empty_reference.visible_aps,
        visible_ap_count=(
            adaptive_reference.visible_ap_count
            if adaptive_reference.visible_ap_count is not None
            else empty_reference.visible_ap_count
        ),
    )


def _weighted_score(
    component_scores: Mapping[str, float],
    weights: Optional[Mapping[str, float]],
) -> float:
    active_weights = dict(_DEFAULT_WEIGHTS)
    if weights:
        active_weights.update(weights)

    total_weight = 0.0
    weighted_sum = 0.0
    for feature_name, score in component_scores.items():
        weight = max(0.0, float(active_weights.get(feature_name, 0.0)))
        total_weight += weight
        weighted_sum += weight * score

    if total_weight == 0.0:
        return 0.0
    return _clamp(weighted_sum / total_weight)


def _rssi_delta_score(current: _SignalSummary, reference: _SignalSummary) -> float:
    if current.rssi_by_ap and reference.rssi_by_ap:
        common_aps = set(current.rssi_by_ap).intersection(reference.rssi_by_ap)
        if common_aps:
            deltas = [abs(current.rssi_by_ap[ap] - reference.rssi_by_ap[ap]) for ap in common_aps]
            return _clamp((sum(deltas) / len(deltas)) / 12.0)

    return _metric_delta_score(
        current.average("rssi"),
        reference.average("rssi"),
        absolute_scale=12.0,
        relative_floor=20.0,
    )


def _metric_delta_score(
    current_value: Optional[float],
    reference_value: Optional[float],
    *,
    absolute_scale: float,
    relative_floor: float,
) -> float:
    if current_value is None and reference_value is None:
        return 0.0
    if current_value is None or reference_value is None:
        return 0.50

    delta = abs(current_value - reference_value)
    absolute_score = delta / absolute_scale
    relative_score = delta / max(abs(reference_value), relative_floor)
    return _clamp(max(absolute_score, relative_score))


def _ap_visibility_delta_score(current: _SignalSummary, reference: _SignalSummary) -> float:
    if current.visible_aps and reference.visible_aps:
        union = current.visible_aps.union(reference.visible_aps)
        if union:
            jaccard_distance = 1.0 - (len(current.visible_aps.intersection(reference.visible_aps)) / len(union))
        else:
            jaccard_distance = 0.0
    elif current.visible_aps or reference.visible_aps:
        jaccard_distance = 1.0
    else:
        jaccard_distance = 0.0

    current_count = current.ap_count
    reference_count = reference.ap_count
    if current_count is None and reference_count is None:
        count_delta_score = 0.0
    elif current_count is None or reference_count is None:
        count_delta_score = 0.50
    else:
        count_delta_score = _clamp(abs(current_count - reference_count) / max(reference_count, 1))

    return _clamp(max(jaccard_distance, count_delta_score))


def _summarize_signal(observation: Any) -> _SignalSummary:
    if observation is None:
        return _SignalSummary()

    if _looks_like_observation_series(observation):
        summaries = [_summarize_signal(item) for item in observation]
        return _combine_summaries(summaries)

    ap_entries = _extract_ap_entries(observation)
    rssi_values, rssi_by_ap = _extract_metric_values(observation, ap_entries, _RSSI_ALIASES)
    visible_aps, visible_ap_count = _extract_visible_aps(observation, ap_entries, rssi_by_ap)

    return _SignalSummary(
        rssi_values=tuple(rssi_values),
        rssi_by_ap=rssi_by_ap,
        jitter_values=tuple(_extract_metric_values(observation, ap_entries, _JITTER_ALIASES)[0]),
        latency_values=tuple(_extract_metric_values(observation, ap_entries, _LATENCY_ALIASES)[0]),
        packet_loss_values=tuple(
            _normalize_packet_loss(value)
            for value in _extract_metric_values(observation, ap_entries, _PACKET_LOSS_ALIASES)[0]
        ),
        visible_aps=visible_aps,
        visible_ap_count=visible_ap_count,
    )


def _combine_summaries(summaries: Iterable[_SignalSummary]) -> _SignalSummary:
    rssi_values = []
    rssi_by_ap: Dict[str, float] = {}
    jitter_values = []
    latency_values = []
    packet_loss_values = []
    visible_aps: Set[str] = set()
    visible_counts = []

    for summary in summaries:
        rssi_values.extend(summary.rssi_values)
        rssi_by_ap.update(summary.rssi_by_ap)
        jitter_values.extend(summary.jitter_values)
        latency_values.extend(summary.latency_values)
        packet_loss_values.extend(summary.packet_loss_values)
        visible_aps.update(summary.visible_aps)
        if summary.visible_ap_count is not None:
            visible_counts.append(summary.visible_ap_count)

    visible_ap_count = round(sum(visible_counts) / len(visible_counts)) if visible_counts else None
    return _SignalSummary(
        rssi_values=tuple(rssi_values),
        rssi_by_ap=rssi_by_ap,
        jitter_values=tuple(jitter_values),
        latency_values=tuple(latency_values),
        packet_loss_values=tuple(packet_loss_values),
        visible_aps=visible_aps,
        visible_ap_count=visible_ap_count,
    )


def _looks_like_observation_series(observation: Any) -> bool:
    if isinstance(observation, (str, bytes, Mapping)) or not isinstance(observation, Sequence):
        return False
    if not observation:
        return False
    # A list of AP entries is a single scan. A list of scans is a baseline series.
    return not all(_entry_has_ap_identity(item) or _read_field(item, _RSSI_ALIASES) is not None for item in observation)


def _extract_ap_entries(observation: Any) -> Tuple[Any, ...]:
    if isinstance(observation, Sequence) and not isinstance(observation, (str, bytes)):
        if all(_entry_has_ap_identity(item) or _read_field(item, _RSSI_ALIASES) is not None for item in observation):
            return tuple(observation)

    entries = []
    for field_name in ("access_points", "aps", "visible_aps", "networks", "scan_results"):
        value = _read_field(observation, (field_name,))
        if isinstance(value, Mapping):
            entries.extend(_mapping_to_ap_entries(value))
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            entries.extend(value)
    return tuple(entries)


def _mapping_to_ap_entries(value: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
    for key, item in value.items():
        if isinstance(item, Mapping):
            entry: MutableMapping[str, Any] = dict(item)
            entry.setdefault("bssid", key)
            yield entry
        else:
            yield {"bssid": key, "rssi": item}


def _extract_metric_values(
    observation: Any,
    ap_entries: Sequence[Any],
    aliases: Sequence[str],
) -> Tuple[Tuple[float, ...], Dict[str, float]]:
    values = []
    values_by_ap: Dict[str, float] = {}

    top_level_value = _read_field(observation, aliases)
    for ap_id, metric_value in _coerce_metric_items(top_level_value):
        values.append(metric_value)
        if ap_id:
            values_by_ap[ap_id] = metric_value

    for entry in ap_entries:
        metric_value = _read_field(entry, aliases)
        numeric_value = _coerce_float(metric_value)
        if numeric_value is None:
            continue
        values.append(numeric_value)
        ap_id = _ap_identifier(entry)
        if ap_id:
            values_by_ap[ap_id] = numeric_value

    return tuple(values), values_by_ap


def _coerce_metric_items(value: Any) -> Iterable[Tuple[Optional[str], float]]:
    numeric_value = _coerce_float(value)
    if numeric_value is not None:
        yield None, numeric_value
        return

    if isinstance(value, Mapping):
        for key, item in value.items():
            item_value = _coerce_float(item)
            if item_value is not None:
                yield str(key), item_value
        return

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for item in value:
            item_value = _coerce_float(item)
            if item_value is not None:
                yield None, item_value


def _extract_visible_aps(
    observation: Any,
    ap_entries: Sequence[Any],
    rssi_by_ap: Mapping[str, float],
) -> Tuple[Set[str], Optional[int]]:
    visible_aps = set(rssi_by_ap)
    visible_count = _coerce_int(_read_field(observation, ("visible_ap_count", "ap_count", "network_count")))

    for entry in ap_entries:
        ap_id = _ap_identifier(entry)
        if ap_id:
            visible_aps.add(ap_id)

    ap_visibility = _read_field(observation, ("ap_visibility", "visible_aps", "bssids"))
    if isinstance(ap_visibility, Mapping):
        for key, value in ap_visibility.items():
            if _is_visible(value):
                visible_aps.add(str(key))
    elif isinstance(ap_visibility, Sequence) and not isinstance(ap_visibility, (str, bytes)):
        for item in ap_visibility:
            if _entry_has_ap_identity(item):
                ap_id = _ap_identifier(item)
                if ap_id:
                    visible_aps.add(ap_id)
            elif not isinstance(item, Mapping):
                visible_aps.add(str(item))

    return visible_aps, visible_count


def _read_field(source: Any, aliases: Sequence[str]) -> Any:
    if source is None:
        return None
    for alias in aliases:
        if isinstance(source, Mapping) and alias in source:
            return source[alias]
        if not isinstance(source, Mapping) and hasattr(source, alias):
            return getattr(source, alias)
    return None


def _entry_has_ap_identity(entry: Any) -> bool:
    return _ap_identifier(entry) is not None


def _ap_identifier(entry: Any) -> Optional[str]:
    value = _read_field(entry, ("bssid", "mac", "ap_id", "id", "ssid"))
    if value is None:
        return None
    return str(value)


def _is_visible(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    numeric_value = _coerce_float(value)
    if numeric_value is not None:
        return numeric_value != 0.0
    return True


def _coerce_float(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, Real):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _coerce_int(value: Any) -> Optional[int]:
    numeric_value = _coerce_float(value)
    if numeric_value is None:
        return None
    return int(numeric_value)


def _normalize_packet_loss(value: float) -> float:
    if value > 1.0:
        return _clamp(value / 100.0)
    return _clamp(value)


def _round_optional(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    return round(value, 6)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


_RSSI_ALIASES = ("rssi", "rssi_dbm", "signal_strength", "signal_strength_dbm")
_JITTER_ALIASES = ("jitter", "jitter_ms", "network_jitter", "network_jitter_ms")
_LATENCY_ALIASES = ("latency", "latency_ms", "rtt", "rtt_ms", "round_trip_ms")
_PACKET_LOSS_ALIASES = (
    "packet_loss",
    "packet_loss_rate",
    "packet_loss_ratio",
    "packet_loss_percent",
)

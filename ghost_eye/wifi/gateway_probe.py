"""Gateway probing primitives for non-CSI WiFi sensing."""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import fmean
from time import time
from typing import Iterable


@dataclass(frozen=True)
class GatewayProbeSample:
    """One connectivity sample against a gateway or local AP endpoint."""

    latency_ms: float | None
    reachable: bool
    rssi_dbm: float | None = None
    timestamp: float = field(default_factory=time)


@dataclass(frozen=True)
class GatewayProbeResult:
    """Aggregated gateway probe result for inference inputs."""

    samples: tuple[GatewayProbeSample, ...]
    packet_loss: float
    average_latency_ms: float | None
    average_rssi_dbm: float | None
    timestamp: float = field(default_factory=time)

    @property
    def reachable(self) -> bool:
        return self.packet_loss < 1.0


class GatewayProbe:
    """Aggregates external gateway measurements supplied by a platform adapter."""

    def summarize(self, samples: Iterable[GatewayProbeSample]) -> GatewayProbeResult:
        sample_tuple = tuple(samples)
        if not sample_tuple:
            return GatewayProbeResult(
                samples=(),
                packet_loss=1.0,
                average_latency_ms=None,
                average_rssi_dbm=None,
            )

        reachable = [sample for sample in sample_tuple if sample.reachable]
        latencies = [
            sample.latency_ms
            for sample in reachable
            if sample.latency_ms is not None and sample.latency_ms >= 0
        ]
        rssis = [sample.rssi_dbm for sample in sample_tuple if sample.rssi_dbm is not None]
        packet_loss = 1.0 - (len(reachable) / len(sample_tuple))

        return GatewayProbeResult(
            samples=sample_tuple,
            packet_loss=packet_loss,
            average_latency_ms=fmean(latencies) if latencies else None,
            average_rssi_dbm=fmean(rssis) if rssis else None,
        )

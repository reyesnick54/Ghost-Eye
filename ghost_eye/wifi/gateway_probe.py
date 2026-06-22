"""Gateway probing primitives for non-CSI WiFi sensing."""

from __future__ import annotations

import platform
import re
import shutil
import statistics
import subprocess
from dataclasses import dataclass, field
from statistics import fmean
from time import time
from typing import Any, Iterable


COMMAND_TIMEOUT_SECONDS = 8.0


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
    gateway_ip: str | None = None
    jitter_ms: float | None = None
    probe_status: str = "unknown"
    errors: tuple[str, ...] = ()

    @property
    def reachable(self) -> bool:
        return self.packet_loss < 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "gateway_ip": self.gateway_ip,
            "gateway_latency_ms": self.average_latency_ms,
            "jitter_ms": self.jitter_ms,
            "packet_loss": self.packet_loss,
            "probe_status": self.probe_status,
            "reachable": self.reachable,
            "errors": list(self.errors),
            "timestamp": self.timestamp,
        }


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
                jitter_ms=None,
                probe_status="no_samples",
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
            jitter_ms=statistics.pstdev(latencies) if len(latencies) > 1 else 0.0,
            probe_status="ok" if reachable else "unreachable",
        )


def probe_gateway(count: int = 5) -> GatewayProbeResult:
    """Identify and ping the default gateway, returning safe fallbacks on failure."""

    errors: list[str] = []
    gateway_ip = identify_default_gateway(errors)
    if not gateway_ip:
        return _fallback_result(None, "gateway_unavailable", errors)

    ping_output = _run_ping(gateway_ip, count=count, errors=errors)
    if not ping_output:
        return _fallback_result(gateway_ip, "ping_failed", errors)

    latencies = _parse_ping_latencies(ping_output)
    packet_loss = _parse_packet_loss(ping_output)
    if packet_loss is None:
        packet_loss = 1.0 if not latencies else max(0.0, 1.0 - (len(latencies) / max(count, 1)))

    jitter = _parse_ping_jitter(ping_output)
    if jitter is None:
        jitter = statistics.pstdev(latencies) if len(latencies) > 1 else 0.0

    status = "ok" if latencies and packet_loss < 1.0 else "degraded"
    samples = tuple(GatewayProbeSample(latency_ms=value, reachable=True) for value in latencies)
    return GatewayProbeResult(
        samples=samples,
        packet_loss=round(max(0.0, min(1.0, packet_loss)), 4),
        average_latency_ms=round(fmean(latencies), 2) if latencies else None,
        average_rssi_dbm=None,
        gateway_ip=gateway_ip,
        jitter_ms=round(max(0.0, jitter), 2),
        probe_status=status,
        errors=tuple(errors),
    )


def identify_default_gateway(errors: list[str] | None = None) -> str | None:
    """Best-effort default gateway discovery for macOS first, then Linux."""

    errors = errors if errors is not None else []
    system = platform.system().lower()
    commands: tuple[tuple[str, ...], ...]
    if system == "darwin":
        commands = (("route", "-n", "get", "default"), ("netstat", "-rn", "-f", "inet"))
    else:
        commands = (("ip", "route", "show", "default"), ("route", "-n"), ("netstat", "-rn"),)

    for command in commands:
        output = _run_command(command, timeout=3.0, errors=errors)
        gateway = _parse_gateway(output)
        if gateway:
            return gateway
    return None


def _run_ping(gateway_ip: str, count: int, errors: list[str]) -> str:
    system = platform.system().lower()
    if system == "darwin":
        command = ("ping", "-c", str(count), "-W", "1000", gateway_ip)
    else:
        command = ("ping", "-c", str(count), "-W", "1", gateway_ip)
    return _run_command(command, timeout=COMMAND_TIMEOUT_SECONDS, errors=errors)


def _fallback_result(gateway_ip: str | None, status: str, errors: list[str]) -> GatewayProbeResult:
    return GatewayProbeResult(
        samples=(),
        packet_loss=1.0,
        average_latency_ms=None,
        average_rssi_dbm=None,
        gateway_ip=gateway_ip,
        jitter_ms=None,
        probe_status=status,
        errors=tuple(errors),
    )


def _run_command(command: tuple[str, ...], timeout: float, errors: list[str]) -> str:
    executable = command[0]
    if shutil.which(executable) is None:
        errors.append(f"{executable}:unavailable")
        return ""
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        errors.append(f"{executable}:{exc.__class__.__name__}")
        return ""
    if result.returncode != 0 and result.stderr.strip():
        errors.append(f"{executable}:exit_{result.returncode}")
    return "\n".join(part for part in (result.stdout, result.stderr) if part)


def _parse_gateway(output: str) -> str | None:
    patterns = (
        r"gateway:\s*([0-9]+(?:\.[0-9]+){3})",
        r"default\s+via\s+([0-9]+(?:\.[0-9]+){3})",
        r"^default\s+([0-9]+(?:\.[0-9]+){3})",
        r"^0\.0\.0\.0\s+([0-9]+(?:\.[0-9]+){3})",
    )
    for pattern in patterns:
        match = re.search(pattern, output, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1)
    return None


def _parse_ping_latencies(output: str) -> list[float]:
    return [float(value) for value in re.findall(r"time[=<]([0-9]+(?:\.[0-9]+)?)\s*ms", output)]


def _parse_packet_loss(output: str) -> float | None:
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)%\s*packet loss", output)
    if not match:
        return None
    return max(0.0, min(1.0, float(match.group(1)) / 100.0))


def _parse_ping_jitter(output: str) -> float | None:
    match = re.search(
        r"(?:round-trip|rtt) min/avg/max/(?:stddev|mdev)\s*=\s*"
        r"[0-9.]+/([0-9.]+)/[0-9.]+/([0-9.]+)\s*ms",
        output,
    )
    if not match:
        return None
    return float(match.group(2))

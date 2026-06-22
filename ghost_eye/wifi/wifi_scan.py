"""WiFi scan data structures and macOS live collection helpers."""

from __future__ import annotations

import platform
import re
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from time import time
from typing import Any, Callable, Iterable, Mapping


AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
COMMAND_TIMEOUT_SECONDS = 3.0


@dataclass(frozen=True)
class WifiNetwork:
    """A single access point observation from a WiFi scan."""

    ssid: str
    bssid: str
    rssi_dbm: float
    channel: int | None = None
    frequency_mhz: int | None = None
    security: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WifiScan:
    """A timestamped collection of nearby WiFi network observations."""

    networks: tuple[WifiNetwork, ...]
    timestamp: float = field(default_factory=time)
    source: str = "wifi_scan"

    def strongest(self, limit: int = 5) -> tuple[WifiNetwork, ...]:
        """Return the strongest access-point observations in this scan."""

        return tuple(sorted(self.networks, key=lambda network: network.rssi_dbm, reverse=True)[:limit])

    def by_bssid(self) -> dict[str, WifiNetwork]:
        """Index observations by normalized BSSID."""

        return {network.bssid.lower(): network for network in self.networks}


@dataclass(frozen=True)
class LiveWifiScan:
    """Current associated WiFi network metadata from the backend host."""

    timestamp: float
    ssid: str | None = None
    bssid: str | None = None
    bssid_masked: str | None = None
    rssi_dbm: float | None = None
    noise_dbm: float | None = None
    channel: str | None = None
    tx_rate_mbps: float | None = None
    phy_mode: str | None = None
    interface_name: str | None = None
    vendor_hint: str = "unknown"
    visible_access_points: int = 0
    platform: str = "unknown"
    available: bool = False
    status: str = "unavailable"
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "ssid": self.ssid,
            "bssid": self.bssid,
            "bssid_masked": self.bssid_masked,
            "rssi_dbm": self.rssi_dbm,
            "noise_dbm": self.noise_dbm,
            "channel": self.channel,
            "tx_rate_mbps": self.tx_rate_mbps,
            "phy_mode": self.phy_mode,
            "interface_name": self.interface_name,
            "vendor_hint": self.vendor_hint,
            "visible_access_points": self.visible_access_points,
            "platform": self.platform,
            "available": self.available,
            "status": self.status,
            "errors": list(self.errors),
        }


class WifiScanner:
    """Wraps a platform-specific scan provider without owning OS integration."""

    def __init__(
        self,
        scan_provider: Callable[[], Iterable[WifiNetwork | Mapping[str, Any]]] | None = None,
    ) -> None:
        self._scan_provider = scan_provider

    def scan(self, source: str = "wifi_scan") -> WifiScan:
        """Run the configured scan provider and return normalized scan rows."""

        if self._scan_provider is None:
            return WifiScan(networks=(), source=source)

        return WifiScan(
            networks=tuple(parse_wifi_networks(self._scan_provider())),
            source=source,
        )


def collect_live_wifi_scan() -> LiveWifiScan:
    """Collect current associated WiFi metadata, preferring macOS commands."""

    if platform.system().lower() == "darwin":
        return collect_macos_wifi_scan()

    return LiveWifiScan(
        timestamp=time(),
        platform=platform.system().lower() or "unknown",
        available=False,
        status="unsupported_platform",
    )


def collect_macos_wifi_scan() -> LiveWifiScan:
    """Collect current macOS WiFi status with partial-data fallbacks."""

    errors: list[str] = []
    data: dict[str, Any] = {"platform": "macos"}

    interface = _detect_macos_wifi_interface(errors) or "en0"
    if interface:
        data["interface_name"] = interface
        networksetup = _run_command(("networksetup", "-getairportnetwork", interface), errors)
        if networksetup:
            ssid = _parse_networksetup_ssid(networksetup)
            if ssid:
                data["ssid"] = ssid

    airport = _run_command((AIRPORT_PATH, "-I"), errors) if shutil.which(AIRPORT_PATH) or _path_exists(AIRPORT_PATH) else ""
    if airport:
        data.update(_parse_airport_info(airport))

    profiler = _run_command(("system_profiler", "SPAirPortDataType"), errors)
    if profiler:
        _merge_missing(data, _parse_system_profiler_airport(profiler, data.get("ssid")))

    ssid = _clean_text(data.get("ssid"))
    bssid = _normalize_bssid(data.get("bssid"))
    rssi = _optional_float(data.get("rssi_dbm"))
    visible_access_points = 1 if ssid or bssid or rssi is not None else 0
    vendor_hint = infer_vendor_hint(ssid, bssid)
    available = bool(ssid and (rssi is not None or bssid or data.get("channel")))

    return LiveWifiScan(
        timestamp=time(),
        ssid=ssid,
        bssid=bssid,
        bssid_masked=mask_bssid(bssid),
        rssi_dbm=rssi,
        noise_dbm=_optional_float(data.get("noise_dbm")),
        channel=_clean_text(data.get("channel")),
        tx_rate_mbps=_optional_float(data.get("tx_rate_mbps")),
        phy_mode=_clean_text(data.get("phy_mode")),
        interface_name=_clean_text(data.get("interface_name")),
        vendor_hint=vendor_hint,
        visible_access_points=visible_access_points,
        platform="macos",
        available=available,
        status="available" if available else "partial_or_unavailable",
        errors=tuple(errors),
    )


def parse_wifi_networks(rows: Iterable[WifiNetwork | Mapping[str, Any]]) -> list[WifiNetwork]:
    """Convert provider rows into ``WifiNetwork`` objects."""

    networks: list[WifiNetwork] = []
    for row in rows:
        if isinstance(row, WifiNetwork):
            networks.append(row)
            continue

        networks.append(
            WifiNetwork(
                ssid=str(row.get("ssid", "")),
                bssid=str(row.get("bssid", "")).lower(),
                rssi_dbm=float(row.get("rssi_dbm", row.get("rssi", -100.0))),
                channel=_optional_int(row.get("channel")),
                frequency_mhz=_optional_int(row.get("frequency_mhz")),
                security=_optional_str(row.get("security")),
                metadata=dict(row.get("metadata", {})),
            )
        )
    return networks


def infer_vendor_hint(ssid: str | None, bssid: str | None = None) -> str:
    """Infer the v0.3 demo vendor hint from SSID text."""

    text = (ssid or "").lower()
    if "netgear" in text:
        return "netgear"
    if "tp-link" in text or "tplink" in text or "archer" in text or "deco" in text:
        return "tp_link"
    return "unknown"


def mask_bssid(bssid: str | None) -> str | None:
    """Mask a BSSID while retaining enough shape for display/debugging."""

    normalized = _normalize_bssid(bssid)
    if not normalized:
        return None
    parts = normalized.split(":")
    if len(parts) != 6:
        return "**:**:**:**:**:**"
    return f"{parts[0]}:{parts[1]}:**:**:**:{parts[5]}"


def _detect_macos_wifi_interface(errors: list[str]) -> str | None:
    output = _run_command(("networksetup", "-listallhardwareports"), errors)
    if not output:
        return None

    blocks = re.split(r"\n\s*\n", output)
    for block in blocks:
        if re.search(r"Hardware Port:\s*(Wi-Fi|AirPort)", block, re.IGNORECASE):
            match = re.search(r"Device:\s*(\S+)", block)
            if match:
                return match.group(1)
    return None


def _parse_networksetup_ssid(output: str) -> str | None:
    match = re.search(r"Current Wi-Fi Network:\s*(.+)", output)
    if not match:
        return None
    return _clean_text(match.group(1))


def _parse_airport_info(output: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    key_map = {
        "agrctlrssi": "rssi_dbm",
        "agrctlnoise": "noise_dbm",
        "bssid": "bssid",
        "ssid": "ssid",
        "channel": "channel",
        "lasttxrate": "tx_rate_mbps",
        "op mode": "phy_mode",
        "phymode": "phy_mode",
    }
    for line in output.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        normalized_key = key.strip().lower().replace(" ", "")
        mapped = key_map.get(normalized_key) or key_map.get(key.strip().lower())
        if mapped:
            parsed[mapped] = value.strip()
    return parsed


def _parse_system_profiler_airport(output: str, selected_ssid: Any = None) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    ssid = _clean_text(selected_ssid)
    current_network_lines: list[str] = []
    capture = False

    for line in output.splitlines():
        stripped = line.strip()
        if ssid and stripped == f"{ssid}:":
            parsed["ssid"] = ssid
            capture = True
            continue
        if stripped == "Current Network Information:":
            capture = True
            continue
        if capture and stripped.endswith(":") and not stripped.startswith(("PHY", "BSSID", "Channel")) and current_network_lines:
            break
        if capture:
            current_network_lines.append(stripped)

    text = "\n".join(current_network_lines or output.splitlines())
    field_patterns = {
        "bssid": r"BSSID:\s*([0-9a-fA-F:.-]+)",
        "channel": r"Channel:\s*([^\n]+)",
        "phy_mode": r"PHY Mode:\s*([^\n]+)",
    }
    for key, pattern in field_patterns.items():
        match = re.search(pattern, text)
        if match:
            parsed[key] = match.group(1).strip()
    return parsed


def _run_command(command: tuple[str, ...], errors: list[str]) -> str:
    executable = command[0]
    if executable != AIRPORT_PATH and shutil.which(executable) is None:
        errors.append(f"{executable}:unavailable")
        return ""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        errors.append(f"{executable}:{exc.__class__.__name__}")
        return ""
    if result.returncode != 0 and result.stderr.strip():
        errors.append(f"{executable}:exit_{result.returncode}")
    return result.stdout or ""


def _merge_missing(target: dict[str, Any], source: Mapping[str, Any]) -> None:
    for key, value in source.items():
        if target.get(key) in (None, "") and value not in (None, ""):
            target[key] = value


def _path_exists(path: str) -> bool:
    try:
        return bool(os.path.exists(path))
    except OSError:
        return False


def _normalize_bssid(value: Any) -> str | None:
    text = _clean_text(value)
    if not text:
        return None
    cleaned = text.lower().replace("-", ":")
    parts = [part.zfill(2) for part in cleaned.split(":") if part]
    if len(parts) != 6 or not all(re.fullmatch(r"[0-9a-f]{2}", part) for part in parts):
        return None
    return ":".join(parts)


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", str(value))
    if not match:
        return None
    return float(match.group(0))


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    return int(value)


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None

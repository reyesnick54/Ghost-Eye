import pytest

from ghost_eye.inference.signal_capability_profiler import SignalCapabilityProfiler


EXPECTED_MODE_PROFILES = {
    "simulator": {
        "supports_rssi_scan": False,
        "supports_latency_probe": False,
        "supports_rtt": False,
        "supports_csi": False,
        "confidence_ceiling": 0.90,
    },
    "wifi_only_rssi": {
        "supports_rssi_scan": True,
        "supports_latency_probe": False,
        "supports_rtt": False,
        "supports_csi": False,
        "confidence_ceiling": 0.50,
    },
    "wifi_only_rssi_latency": {
        "supports_rssi_scan": True,
        "supports_latency_probe": True,
        "supports_rtt": False,
        "supports_csi": False,
        "confidence_ceiling": 0.65,
    },
    "wifi_only_rtt_if_available": {
        "supports_rssi_scan": True,
        "supports_latency_probe": True,
        "supports_rtt": True,
        "supports_csi": False,
        "confidence_ceiling": 0.80,
    },
    "single_router_wifi_only": {
        "supports_rssi_scan": True,
        "supports_latency_probe": False,
        "supports_rtt": False,
        "supports_csi": False,
        "confidence_ceiling": 0.40,
    },
    "esp32_csi_placeholder": {
        "supports_rssi_scan": False,
        "supports_latency_probe": False,
        "supports_rtt": False,
        "supports_csi": True,
        "confidence_ceiling": 0.95,
    },
    "router_adapter_placeholder": {
        "supports_rssi_scan": True,
        "supports_latency_probe": False,
        "supports_rtt": False,
        "supports_csi": False,
        "confidence_ceiling": 0.55,
    },
}


def test_profile_for_mode_returns_requested_fields_for_every_mode():
    profiler = SignalCapabilityProfiler()

    for mode, expected in EXPECTED_MODE_PROFILES.items():
        profile = profiler.profile_for_mode(mode)

        assert profile["mode"] == mode
        for key, value in expected.items():
            assert profile[key] == value
        assert isinstance(profile["recommended_scan_mode"], str)
        assert profile["recommended_scan_mode"]
        assert isinstance(profile["limitations"], list)
        assert profile["limitations"]


@pytest.mark.parametrize(
    ("source", "expected_mode"),
    [
        ("simulated-demo", "simulator"),
        ("wifi RSSI only", "wifi_only_rssi"),
        ("wifi RSSI latency", "wifi_only_rssi_latency"),
        ("wifi FTM RTT", "wifi_only_rtt_if_available"),
        ("single router wifi", "single_router_wifi_only"),
        ("esp32 CSI", "esp32_csi_placeholder"),
        ("OpenWRT router adapter", "router_adapter_placeholder"),
    ],
)
def test_profile_classifies_descriptive_strings(source, expected_mode):
    assert SignalCapabilityProfiler().profile(source)["mode"] == expected_mode


@pytest.mark.parametrize(
    ("source", "expected_mode"),
    [
        ({"supports_rssi_scan": True}, "wifi_only_rssi"),
        ({"supports_rssi_scan": True, "supports_latency_probe": True}, "wifi_only_rssi_latency"),
        ({"supports_rtt": True}, "wifi_only_rtt_if_available"),
        ({"router_count": 1, "supports_rssi_scan": True}, "single_router_wifi_only"),
        ({"source_type": "esp32", "supports_csi": True}, "esp32_csi_placeholder"),
        ({"source_type": "router_adapter"}, "router_adapter_placeholder"),
    ],
)
def test_profile_classifies_mapping_hints(source, expected_mode):
    assert SignalCapabilityProfiler().classify(source)["mode"] == expected_mode


def test_keyword_hints_override_source_mapping():
    profile = SignalCapabilityProfiler().profile({"mode": "wifi_only_rssi"}, mode="wifi_only_rtt_if_available")

    assert profile["mode"] == "wifi_only_rtt_if_available"
    assert profile["supports_rtt"] is True


def test_limitations_are_returned_as_independent_lists():
    profiler = SignalCapabilityProfiler()
    first = profiler.profile_for_mode("wifi_only_rssi")
    first["limitations"].append("mutated")

    second = profiler.profile_for_mode("wifi_only_rssi")

    assert "mutated" not in second["limitations"]


def test_profile_for_mode_rejects_unknown_explicit_modes():
    with pytest.raises(ValueError):
        SignalCapabilityProfiler().profile_for_mode("unknown_source")

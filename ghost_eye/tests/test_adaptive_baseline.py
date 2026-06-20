from ghost_eye.inference.adaptive_baseline import AdaptiveBaselineEngine


def test_updates_adaptive_baseline_only_when_scan_is_stable(tmp_path):
    engine = AdaptiveBaselineEngine(session_id="stable-room", baseline_dir=tmp_path)

    first_scan = {"csi": [1.0, 2.0, 3.0], "zone": "zone_a"}
    result = engine.update(
        first_scan,
        motion_score=0.10,
        scan_stability=0.80,
        packet_loss=0.01,
    )

    assert result["baseline_status"] == "updated"
    assert result["drift_score"] == 0.0
    assert result["last_updated"] is not None
    assert engine.static_baseline == first_scan
    assert engine.adaptive_baseline == first_scan

    last_updated = result["last_updated"]
    high_motion_scan = {"csi": [9.0, 9.0, 9.0], "zone": "zone_b"}
    held = engine.update(
        high_motion_scan,
        motion_score=0.20,
        scan_stability=0.90,
        packet_loss=0.01,
    )

    assert held == {
        "baseline_status": "held",
        "drift_score": 0.0,
        "last_updated": last_updated,
    }
    assert engine.static_baseline == first_scan
    assert engine.adaptive_baseline == first_scan


def test_holds_adaptive_baseline_for_unstable_scan_and_packet_loss(tmp_path):
    engine = AdaptiveBaselineEngine(session_id="unstable-room", baseline_dir=tmp_path)

    unstable = engine.update(
        {"csi": [1.0, 1.0]},
        motion_score=0.10,
        scan_stability=0.70,
        packet_loss=0.01,
    )

    assert unstable == {
        "baseline_status": "held",
        "drift_score": 0.0,
        "last_updated": None,
    }
    assert engine.static_baseline == {"csi": [1.0, 1.0]}
    assert engine.adaptive_baseline is None

    packet_loss = engine.update(
        {"csi": [2.0, 2.0]},
        motion_score=0.10,
        scan_stability=0.80,
        packet_loss=0.05,
    )

    assert packet_loss == {
        "baseline_status": "held",
        "drift_score": 0.0,
        "last_updated": None,
    }
    assert engine.adaptive_baseline is None


def test_persists_and_reloads_baselines(tmp_path):
    engine = AdaptiveBaselineEngine(session_id="reload-room", baseline_dir=tmp_path)
    engine.update(
        {"csi": [2.0, 4.0]},
        motion_score=0.10,
        scan_stability=0.80,
        packet_loss=0.01,
    )
    engine.update(
        {"csi": [3.0, 6.0]},
        motion_score=0.10,
        scan_stability=0.80,
        packet_loss=0.01,
    )

    reloaded = AdaptiveBaselineEngine(session_id="reload-room", baseline_dir=tmp_path)

    assert reloaded.static_baseline == {"csi": [2.0, 4.0]}
    assert reloaded.adaptive_baseline == {"csi": [3.0, 6.0]}
    assert reloaded.last_updated == engine.last_updated
    assert reloaded.drift_score() == 0.5

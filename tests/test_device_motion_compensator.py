from ghost_eye.inference.device_motion_compensator import DeviceMotionCompensator


def test_moving_device_reduces_confidence_invalidates_scan_and_blocks_baseline():
    compensator = DeviceMotionCompensator()

    result = compensator.compensate("moving")

    assert result.device_stability == "moving"
    assert result.confidence_multiplier < 1.0
    assert result.scan_valid is False
    assert "baseline_update_blocked" in result.reason
    assert compensator.baseline_update_allowed("moving") is False


def test_stable_device_keeps_scan_valid_and_confidence_unchanged():
    compensator = DeviceMotionCompensator()

    result = compensator.compensate("stable")

    assert result.device_stability == "stable"
    assert result.confidence_multiplier == 1.0
    assert result.scan_valid is True
    assert compensator.baseline_update_allowed("stable") is True


def test_missing_device_motion_state_defaults_to_unknown_without_penalty():
    compensator = DeviceMotionCompensator()

    result = compensator.compensate()

    assert result.device_stability == "unknown"
    assert result.confidence_multiplier == 1.0
    assert result.scan_valid is True
    assert compensator.baseline_update_allowed(None) is True

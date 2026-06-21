# GhostEye Capability Summary

This summary extracts implementation-relevant capabilities from the vendored WiFi sensing repositories.

## Repo Inventory

```text
third_party/wifi-sensing/vendor
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing
third_party/wifi-sensing/vendor/esp-csi
third_party/wifi-sensing/vendor/RuView
third_party/wifi-sensing/vendor/Wi-PoseDataset
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark
third_party/wifi-sensing/vendor/wifi-densepose
third_party/wifi-sensing/vendor/wifi-radar
third_party/wifi-sensing/vendor/WiROS
```

## High-Value Runtime Scripts

```text
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/components/bsp_C5_dual_antenna/bsp_C5_dual_antenna.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/app_main.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/app/app_gpio.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/app/app_ifft.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/app/app_uart.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/app/app_ui.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/components/ui_comp_hook.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/images/ui_img_272184077.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/screens/ui_ScreenM.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/screens/ui_ScreenS.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/screens/ui_ScreenW.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/screens/ui_ScreenWP.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/ui_events.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/ui_helpers.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/ui.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_recv/main/app_main.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_recv/main/app/app_gpio.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_recv/main/app/app_ifft.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_recv/main/app/app_uart.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_send/main/app_main.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/connect_rainmaker/main/app_main.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/components/commands/src/ping_cmd.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/components/commands/src/system_cmd.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/components/commands/src/wifi_cmd.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/esp_csi_tool_gui.py
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/main/app_main.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/main/radar_evaluate.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/tools/esp_csi_tool_gui.py
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/tools/esp_csi_tool.py
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/wifi_sensing_demo/main/app_main.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/wifi_sensing_demo/main/led_control.c
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/wifi_sensing_demo/main/web_serial_monitor.c
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_recv_router/main/app_main.c
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_recv/main/app_main.c
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_send/main/app_main.c
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/tools/csi_data_read_parse.py
third_party/wifi-sensing/vendor/esp-csi/tools/check_idf_version.sh
third_party/wifi-sensing/vendor/esp-csi/tools/ci/get_idf_ver.sh
third_party/wifi-sensing/vendor/esp-csi/tools/format.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/adr-compliance.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/auto-commit.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/checkpoint-manager.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/daemon-manager.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/ddd-tracker.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/github-setup.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/guidance-hook.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/guidance-hooks.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/health-monitor.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/learning-hooks.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/learning-optimizer.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/pattern-consolidator.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/perf-worker.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/quick-start.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/security-scanner.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/setup-mcp.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/standard-checkpoint-hooks.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/statusline-hook.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/swarm-comms.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/swarm-hooks.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/swarm-monitor.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/sync-v3-metrics.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/update-v3-progress.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/v3-quick-status.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/v3.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/validate-v3-config.sh
third_party/wifi-sensing/vendor/RuView/.claude/helpers/worker-manager.sh
third_party/wifi-sensing/vendor/RuView/aether-arena/calibration/calibrate.py
third_party/wifi-sensing/vendor/RuView/aether-arena/calibration/cog_calibrate.py
third_party/wifi-sensing/vendor/RuView/aether-arena/calibration/infer.py
third_party/wifi-sensing/vendor/RuView/aether-arena/calibration/model.py
third_party/wifi-sensing/vendor/RuView/aether-arena/calibration/test_calibration.py
third_party/wifi-sensing/vendor/RuView/aether-arena/calibration/test_cog_calibration.py
third_party/wifi-sensing/vendor/RuView/aether-arena/ledger/ledger_tools.py
third_party/wifi-sensing/vendor/RuView/aether-arena/space/app.py
third_party/wifi-sensing/vendor/RuView/archive/v1/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/data/proof/cir_verify_helper.py
third_party/wifi-sensing/vendor/RuView/archive/v1/data/proof/generate_reference_signal.py
third_party/wifi-sensing/vendor/RuView/archive/v1/data/proof/verify.py
third_party/wifi-sensing/vendor/RuView/archive/v1/scripts/test_api_endpoints.py
third_party/wifi-sensing/vendor/RuView/archive/v1/scripts/test_monitoring.py
third_party/wifi-sensing/vendor/RuView/archive/v1/scripts/test_websocket_streaming.py
third_party/wifi-sensing/vendor/RuView/archive/v1/scripts/validate-deployment.sh
third_party/wifi-sensing/vendor/RuView/archive/v1/scripts/validate-integration.sh
third_party/wifi-sensing/vendor/RuView/archive/v1/setup.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/dependencies.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/main.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/middleware/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/middleware/auth.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/middleware/rate_limit.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/routers/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/routers/auth.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/routers/health.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/routers/pose.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/routers/stream.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/websocket/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/websocket/connection_manager.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/api/websocket/pose_stream.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/app.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/cli.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/commands/start.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/commands/status.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/commands/stop.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/config.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/config/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/config/domains.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/config/settings.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/core/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/core/csi_processor.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/core/phase_sanitizer.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/core/router_interface.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/database/connection.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/database/migrations/001_initial.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/database/migrations/env.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/database/model_types.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/database/models.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/hardware/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/hardware/csi_extractor.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/hardware/router_interface.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/logger.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/main.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/middleware/auth.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/middleware/cors.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/middleware/error_handler.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/middleware/rate_limit.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/models/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/models/densepose_head.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/models/modality_translation.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/sensing/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/sensing/backend.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/sensing/classifier.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/sensing/feature_extractor.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/sensing/rssi_collector.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/sensing/ws_server.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/services/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/services/hardware_service.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/services/health_check.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/services/metrics.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/services/orchestrator.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/services/pose_service.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/services/stream_service.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/tasks/backup.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/tasks/cleanup.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/tasks/monitoring.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/testing/__init__.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/testing/mock_csi_generator.py
third_party/wifi-sensing/vendor/RuView/archive/v1/src/testing/mock_pose_generator.py
third_party/wifi-sensing/vendor/RuView/archive/v1/test_application.py
third_party/wifi-sensing/vendor/RuView/archive/v1/test_auth_rate_limit.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/e2e/test_healthcare_scenario.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/fixtures/api_client.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/fixtures/csi_data.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/live_sense_monitor.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_api_endpoints.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_authentication.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_csi_pipeline.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_full_system_integration.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_hardware_integration.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_inference_pipeline.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_pose_pipeline.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_rate_limiting.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_streaming_pipeline.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_websocket_streaming.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/integration/test_windows_live_sensing.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/mocks/hardware_mocks.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/performance/test_api_throughput.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/performance/test_frame_budget.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/performance/test_inference_speed.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/conftest.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_auth_middleware.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_csi_extractor_direct.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_csi_extractor_tdd_complete.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_csi_extractor_tdd.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_csi_extractor.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_csi_processor_tdd.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_csi_processor.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_csi_standalone.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_densepose_head.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_error_handler.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_esp32_binary_parser.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_hardware_service.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_health_check.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_metrics.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_modality_translation.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_phase_sanitizer_tdd.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_phase_sanitizer.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_pose_service.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_rate_limit.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_router_interface_tdd.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_router_interface.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_sensing.py
third_party/wifi-sensing/vendor/RuView/archive/v1/tests/unit/test_stream_service.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/_bench_common.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/eval_ort_accuracy.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/eval_repro.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/export_to_safetensors.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/generate_corruption_masks.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/onnx_bench.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/quantize_bench.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/remote/clean_v2.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/remote/eval_retrained.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/remote/measb/train_measb.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/remote/setup_and_train.sh
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/remote/sweep/model_compact.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/remote/sweep/run_sweep.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/static_ptq_bench.py
third_party/wifi-sensing/vendor/RuView/benchmarks/wiflow-std/tiny_edge_bench.py
third_party/wifi-sensing/vendor/RuView/deploy.sh
third_party/wifi-sensing/vendor/RuView/docker/docker-entrypoint.sh
third_party/wifi-sensing/vendor/RuView/examples/environment/room_monitor.py
third_party/wifi-sensing/vendor/RuView/examples/happiness-vector/provision_swarm.sh
third_party/wifi-sensing/vendor/RuView/examples/happiness-vector/seed_query.py
third_party/wifi-sensing/vendor/RuView/examples/medical/bp_estimator.py
third_party/wifi-sensing/vendor/RuView/examples/medical/vitals_suite.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/01-physics-floor/r1_toa_crlb.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/01-physics-floor/r6_1_multiscatterer.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/01-physics-floor/r6_fresnel_zone.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/02-placement/r6_2_1_3d_placement.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/02-placement/r6_2_2_1_3d_multistatic.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/02-placement/r6_2_2_multistatic_placement.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/02-placement/r6_2_3_chest_centric.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/02-placement/r6_2_4_3d_chest_multistatic.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/02-placement/r6_2_5_multi_subject.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/02-placement/r6_2_antenna_placement.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/03-spatial-intelligence/r5_subcarrier_saliency.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/03-spatial-intelligence/r7_multilink_consistency.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/04-rssi/r8_rssi_only_count.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/04-rssi/r9_rssi_fingerprint_knn.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/05-cross-room-reid/r3_1_physics_informed_env.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/05-cross-room-reid/r3_2_embedding_physics_env.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/05-cross-room-reid/r3_crossroom_reid.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/06-structure-detection/r12_1_pose_pabs_loop.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/06-structure-detection/r12_pabs_implementation.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/06-structure-detection/r12_rf_weather_eigenshift.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/07-negative-results/r13_bp_physics_floor.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/08-verticals/r10_foliage_attenuation.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/08-verticals/r11_maritime_propagation.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/09-quantum-fusion/r20_1_quantum_classical_fusion.py
third_party/wifi-sensing/vendor/RuView/examples/research-sota/09-quantum-fusion/r20_2_threshold_handoff.py
third_party/wifi-sensing/vendor/RuView/examples/ruview_live.py
third_party/wifi-sensing/vendor/RuView/examples/sleep/apnea_screener.py
third_party/wifi-sensing/vendor/RuView/examples/stress/hrv_stress_monitor.py
third_party/wifi-sensing/vendor/RuView/examples/three.js/server/ruvultra-csi-bridge.py
third_party/wifi-sensing/vendor/RuView/examples/three.js/server/serve-demo.py
third_party/wifi-sensing/vendor/RuView/examples/through-wall/serve.py
third_party/wifi-sensing/vendor/RuView/examples/through-wall/wiflow_ab.py
third_party/wifi-sensing/vendor/RuView/examples/through-wall/wiflow_capture.py
third_party/wifi-sensing/vendor/RuView/examples/through-wall/wiflow_infer.py
third_party/wifi-sensing/vendor/RuView/examples/through-wall/wiflow_train.py
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/adaptive_controller_decide.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/adaptive_controller.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/c6_lp_core.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/c6_softap_he.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/c6_sync_espnow.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/c6_timesync.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/c6_twt.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/csi_collector.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/display_hal.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/display_task.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/display_ui.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/edge_processing.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/lp_core/main.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/main.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/mmwave_sensor.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/mock_csi.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/nvs_config.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/ota_update.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/power_mgmt.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/rv_feature_state.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/rv_mesh.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/rv_radio_ops_esp32.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/rv_radio_ops_mock.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/rvf_parser.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/stream_sender.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/swarm_bridge.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/wasm_runtime.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/wasm_upload.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/provision.py
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/test/capture-3board-experiment.py
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/test/fuzz_csi_serialize.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/test/fuzz_edge_enqueue.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/test/fuzz_nvs_config.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/test/stubs/esp_stubs.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/test/test_adr110_encoding.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/test/test_vitals_count_presence.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/tests/host/test_adaptive_controller.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/tests/host/test_rv_feature_state.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/tests/host/test_rv_mesh.c
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/tests/test_provision_state.py
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/tests/test_provision.py
third_party/wifi-sensing/vendor/RuView/firmware/esp32-hello-world/main/main.c
third_party/wifi-sensing/vendor/RuView/install.sh
third_party/wifi-sensing/vendor/RuView/plugins/ruview/scripts/smoke.sh
third_party/wifi-sensing/vendor/RuView/python/bench/test_bench_bfld_and_ws.py
third_party/wifi-sensing/vendor/RuView/python/bench/test_bench_vitals.py
third_party/wifi-sensing/vendor/RuView/python/ruview-meta/src/ruview/__init__.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_bfld.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_client_ha.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_client_mqtt.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_client_primitives.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_client_ws.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_keypoint.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_pose.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_security.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_smoke.py
third_party/wifi-sensing/vendor/RuView/python/tests/test_vitals.py
third_party/wifi-sensing/vendor/RuView/python/tombstone/src/wifi_densepose/__init__.py
third_party/wifi-sensing/vendor/RuView/python/tombstone/tests/test_tombstone.py
third_party/wifi-sensing/vendor/RuView/python/wifi_densepose/__init__.py
third_party/wifi-sensing/vendor/RuView/python/wifi_densepose/client/__init__.py
third_party/wifi-sensing/vendor/RuView/python/wifi_densepose/client/ha.py
third_party/wifi-sensing/vendor/RuView/python/wifi_densepose/client/mqtt.py
third_party/wifi-sensing/vendor/RuView/python/wifi_densepose/client/primitives.py
third_party/wifi-sensing/vendor/RuView/python/wifi_densepose/client/ws.py
third_party/wifi-sensing/vendor/RuView/references/chart_script.py
third_party/wifi-sensing/vendor/RuView/references/script_1.py
third_party/wifi-sensing/vendor/RuView/references/script_2.py
third_party/wifi-sensing/vendor/RuView/references/script_3.py
third_party/wifi-sensing/vendor/RuView/references/script_4.py
third_party/wifi-sensing/vendor/RuView/references/script_5.py
third_party/wifi-sensing/vendor/RuView/references/script_6.py
third_party/wifi-sensing/vendor/RuView/references/script_7.py
third_party/wifi-sensing/vendor/RuView/references/script_8.py
third_party/wifi-sensing/vendor/RuView/references/script.py
third_party/wifi-sensing/vendor/RuView/references/wifi_densepose_pytorch.py
third_party/wifi-sensing/vendor/RuView/scripts/benchmark-model.py
third_party/wifi-sensing/vendor/RuView/scripts/c6-presence-watcher.py
third_party/wifi-sensing/vendor/RuView/scripts/calibrate-camera-room.py
third_party/wifi-sensing/vendor/RuView/scripts/calibration_lib.py
third_party/wifi-sensing/vendor/RuView/scripts/check_fix_markers.py
third_party/wifi-sensing/vendor/RuView/scripts/check_health.py
third_party/wifi-sensing/vendor/RuView/scripts/collect-ground-truth.py
third_party/wifi-sensing/vendor/RuView/scripts/collect-training-data.py
third_party/wifi-sensing/vendor/RuView/scripts/csi-udp-relay.py
third_party/wifi-sensing/vendor/RuView/scripts/esp32_jsonl_to_rvcsi.py
third_party/wifi-sensing/vendor/RuView/scripts/esp32_wasm_test.py
third_party/wifi-sensing/vendor/RuView/scripts/export-onnx.py
third_party/wifi-sensing/vendor/RuView/scripts/gcloud-train.sh
third_party/wifi-sensing/vendor/RuView/scripts/gcp/cosmos_eval.sh
third_party/wifi-sensing/vendor/RuView/scripts/gcp/provision_cosmos.sh
third_party/wifi-sensing/vendor/RuView/scripts/gcp/provision_marl.sh
third_party/wifi-sensing/vendor/RuView/scripts/gcp/provision_training.sh
third_party/wifi-sensing/vendor/RuView/scripts/gcp/run_marl_train_local.sh
third_party/wifi-sensing/vendor/RuView/scripts/gcp/run_marl_train.sh
third_party/wifi-sensing/vendor/RuView/scripts/gcp/run_training.sh
third_party/wifi-sensing/vendor/RuView/scripts/gcp/teardown.sh
third_party/wifi-sensing/vendor/RuView/scripts/generate_nvs_matrix.py
third_party/wifi-sensing/vendor/RuView/scripts/generate-witness-bundle.sh
third_party/wifi-sensing/vendor/RuView/scripts/hap-test-sensor.py
third_party/wifi-sensing/vendor/RuView/scripts/homecore-seed.sh
third_party/wifi-sensing/vendor/RuView/scripts/inject_fault.py
third_party/wifi-sensing/vendor/RuView/scripts/install-qemu.sh
third_party/wifi-sensing/vendor/RuView/scripts/mac-mini-train.sh
third_party/wifi-sensing/vendor/RuView/scripts/macos-shortcuts/announce-via-homepod.sh
third_party/wifi-sensing/vendor/RuView/scripts/mmwave_fusion_bridge.py
third_party/wifi-sensing/vendor/RuView/scripts/occworld_retrain.py
third_party/wifi-sensing/vendor/RuView/scripts/occworld_server.py
third_party/wifi-sensing/vendor/RuView/scripts/overnight-empty-capture.py
third_party/wifi-sensing/vendor/RuView/scripts/probe-fft-platform.py
third_party/wifi-sensing/vendor/RuView/scripts/prove.sh
third_party/wifi-sensing/vendor/RuView/scripts/provision.py
third_party/wifi-sensing/vendor/RuView/scripts/publish-huggingface.py
third_party/wifi-sensing/vendor/RuView/scripts/publish-huggingface.sh
third_party/wifi-sensing/vendor/RuView/scripts/qemu_swarm.py
third_party/wifi-sensing/vendor/RuView/scripts/qemu-chaos-test.sh
third_party/wifi-sensing/vendor/RuView/scripts/qemu-cli.sh
third_party/wifi-sensing/vendor/RuView/scripts/qemu-esp32s3-test.sh
third_party/wifi-sensing/vendor/RuView/scripts/qemu-mesh-test.sh
third_party/wifi-sensing/vendor/RuView/scripts/qemu-snapshot-test.sh
third_party/wifi-sensing/vendor/RuView/scripts/record-csi-udp.py
third_party/wifi-sensing/vendor/RuView/scripts/redact-secrets.py
third_party/wifi-sensing/vendor/RuView/scripts/release-v0.5.4.sh
third_party/wifi-sensing/vendor/RuView/scripts/rotate-npm-token.sh
third_party/wifi-sensing/vendor/RuView/scripts/ruview_occ_dataset.py
third_party/wifi-sensing/vendor/RuView/scripts/ruview-hap-bridge.py
third_party/wifi-sensing/vendor/RuView/scripts/ruview-sensing-server.py
third_party/wifi-sensing/vendor/RuView/scripts/rvagent-mcp-consumer.py
third_party/wifi-sensing/vendor/RuView/scripts/seed_csi_bridge.py
third_party/wifi-sensing/vendor/RuView/scripts/swarm_health.py
third_party/wifi-sensing/vendor/RuView/scripts/synth-csi-udp.py
third_party/wifi-sensing/vendor/RuView/scripts/tests/conftest.py
third_party/wifi-sensing/vendor/RuView/scripts/tests/test_calibration.py
third_party/wifi-sensing/vendor/RuView/scripts/train-count.py
third_party/wifi-sensing/vendor/RuView/scripts/udp-relay.py
third_party/wifi-sensing/vendor/RuView/scripts/validate_mesh_test.py
third_party/wifi-sensing/vendor/RuView/scripts/validate_qemu_output.py
third_party/wifi-sensing/vendor/RuView/scripts/validate-esp32-mqtt.sh
third_party/wifi-sensing/vendor/RuView/scripts/validate-ha-blueprints.py
third_party/wifi-sensing/vendor/RuView/scripts/verify-calibration-proof.sh
third_party/wifi-sensing/vendor/RuView/scripts/verify-cir-proof.sh
third_party/wifi-sensing/vendor/RuView/scripts/witness-adr-115.sh
third_party/wifi-sensing/vendor/RuView/tests/test_docker_entrypoint.sh
third_party/wifi-sensing/vendor/RuView/tests/test_invariant_Cargo.py
third_party/wifi-sensing/vendor/RuView/ui/pose-fusion/build.sh
third_party/wifi-sensing/vendor/RuView/ui/start-ui.sh
third_party/wifi-sensing/vendor/RuView/v2/crates/wifi-densepose-train/scripts/quantize_half_int8.py
third_party/wifi-sensing/vendor/RuView/wifi_densepose/__init__.py
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/dataset.py
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/NTU_Fi_model.py
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/self_supervised_model.py
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/self_supervised.py
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/UT_HAR_model.py
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/widar_model.py
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/adr-compliance.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/auto-commit.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/checkpoint-manager.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/daemon-manager.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/ddd-tracker.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/github-setup.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/guidance-hook.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/guidance-hooks.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/health-monitor.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/learning-hooks.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/learning-optimizer.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/pattern-consolidator.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/perf-worker.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/quick-start.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/security-scanner.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/setup-mcp.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/standard-checkpoint-hooks.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/statusline-hook.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/swarm-comms.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/swarm-hooks.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/swarm-monitor.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/sync-v3-metrics.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/update-v3-progress.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/v3-quick-status.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/v3.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/validate-v3-config.sh
third_party/wifi-sensing/vendor/wifi-densepose/.claude/helpers/worker-manager.sh
third_party/wifi-sensing/vendor/wifi-densepose/deploy.sh
third_party/wifi-sensing/vendor/wifi-densepose/firmware/esp32-csi-node/main/csi_collector.c
third_party/wifi-sensing/vendor/wifi-densepose/firmware/esp32-csi-node/main/main.c
third_party/wifi-sensing/vendor/wifi-densepose/firmware/esp32-csi-node/main/nvs_config.c
third_party/wifi-sensing/vendor/wifi-densepose/firmware/esp32-csi-node/main/stream_sender.c
third_party/wifi-sensing/vendor/wifi-densepose/firmware/esp32-csi-node/provision.py
third_party/wifi-sensing/vendor/wifi-densepose/install.sh
third_party/wifi-sensing/vendor/wifi-densepose/references/chart_script.py
third_party/wifi-sensing/vendor/wifi-densepose/references/script_1.py
third_party/wifi-sensing/vendor/wifi-densepose/references/script_2.py
third_party/wifi-sensing/vendor/wifi-densepose/references/script_3.py
third_party/wifi-sensing/vendor/wifi-densepose/references/script_4.py
third_party/wifi-sensing/vendor/wifi-densepose/references/script_5.py
third_party/wifi-sensing/vendor/wifi-densepose/references/script_6.py
third_party/wifi-sensing/vendor/wifi-densepose/references/script_7.py
third_party/wifi-sensing/vendor/wifi-densepose/references/script_8.py
third_party/wifi-sensing/vendor/wifi-densepose/references/script.py
third_party/wifi-sensing/vendor/wifi-densepose/references/wifi_densepose_pytorch.py
third_party/wifi-sensing/vendor/wifi-densepose/scripts/generate-witness-bundle.sh
third_party/wifi-sensing/vendor/wifi-densepose/scripts/provision.py
third_party/wifi-sensing/vendor/wifi-densepose/ui/start-ui.sh
third_party/wifi-sensing/vendor/wifi-densepose/v1/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/data/proof/generate_reference_signal.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/data/proof/verify.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/scripts/test_api_endpoints.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/scripts/test_monitoring.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/scripts/test_websocket_streaming.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/scripts/validate-deployment.sh
third_party/wifi-sensing/vendor/wifi-densepose/v1/scripts/validate-integration.sh
third_party/wifi-sensing/vendor/wifi-densepose/v1/setup.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/dependencies.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/main.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/middleware/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/middleware/auth.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/middleware/rate_limit.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/routers/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/routers/health.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/routers/pose.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/routers/stream.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/websocket/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/websocket/connection_manager.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/api/websocket/pose_stream.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/app.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/cli.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/commands/start.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/commands/status.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/commands/stop.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/config.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/config/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/config/domains.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/config/settings.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/core/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/core/csi_processor.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/core/phase_sanitizer.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/core/router_interface.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/database/connection.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/database/migrations/001_initial.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/database/migrations/env.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/database/model_types.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/database/models.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/hardware/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/hardware/csi_extractor.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/hardware/router_interface.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/logger.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/main.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/middleware/auth.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/middleware/cors.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/middleware/error_handler.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/middleware/rate_limit.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/models/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/models/densepose_head.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/models/modality_translation.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/sensing/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/sensing/backend.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/sensing/classifier.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/sensing/feature_extractor.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/sensing/rssi_collector.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/sensing/ws_server.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/services/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/services/hardware_service.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/services/health_check.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/services/metrics.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/services/orchestrator.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/services/pose_service.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/services/stream_service.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/tasks/backup.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/tasks/cleanup.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/tasks/monitoring.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/testing/__init__.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/testing/mock_csi_generator.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/src/testing/mock_pose_generator.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_application.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/e2e/test_healthcare_scenario.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/fixtures/api_client.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/fixtures/csi_data.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/live_sense_monitor.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_api_endpoints.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_authentication.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_csi_pipeline.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_full_system_integration.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_hardware_integration.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_inference_pipeline.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_pose_pipeline.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_rate_limiting.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_streaming_pipeline.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_websocket_streaming.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/integration/test_windows_live_sensing.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/performance/test_api_throughput.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/performance/test_inference_speed.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_csi_extractor_direct.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_csi_extractor_tdd_complete.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_csi_extractor_tdd.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_csi_extractor.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_csi_processor_tdd.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_csi_processor.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_csi_standalone.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_densepose_head.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_esp32_binary_parser.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_modality_translation.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_phase_sanitizer_tdd.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_phase_sanitizer.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_router_interface_tdd.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_router_interface.py
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/unit/test_sensing.py
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/agentic-flow-fast.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/adr-compliance.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/auto-commit.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/checkpoint-manager.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/daemon-manager.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/ddd-tracker.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/github-setup.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/guidance-hook.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/guidance-hooks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/health-monitor.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/learning-hooks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/learning-optimizer.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/pattern-consolidator.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/perf-worker.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/quick-start.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/security-scanner.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/setup-mcp.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/standard-checkpoint-hooks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/statusline-hook.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/swarm-comms.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/swarm-hooks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/swarm-monitor.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/sync-v3-metrics.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/update-v3-progress.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/v3-quick-status.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/v3.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/validate-v3-config.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/helpers/worker-manager.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/hooks/bench-runner.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/hooks/crate-context.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/hooks/post-rust-edit.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/hooks/rust-check.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/hooks/wasm-size-check.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/ruvector-fast.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/statusline-command.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/benchmarks/setup.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/profiling/scripts/benchmark_all.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/profiling/scripts/cpu_profile.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/profiling/scripts/generate_flamegraph.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/profiling/scripts/install_tools.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/profiling/scripts/memory_profile.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/profiling/scripts/run_all_analysis.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-bench/scripts/download_datasets.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-bench/scripts/run_all_benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-cli/scripts/statusline-command.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-wasm/build.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/benches/scripts/run_benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/docker/benchmark/run-benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/docker/dev.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/docker/publish-dockerhub.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/docker/run-integration-tests.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/docker/run-tests.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/docker/test-runner/run-tests.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/install/install.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/install/quick-start.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/install/scripts/setup-debian.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/install/scripts/setup-macos.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/install/scripts/setup-rhel.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/install/tests/verify_installation.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-postgres/scripts/docker-test.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvf/rvf-ebpf/bpf/socket_filter.c
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvf/rvf-ebpf/bpf/tc_query_route.c
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvf/rvf-ebpf/bpf/xdp_distance.c
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvlite/examples/dashboard/apply-bulk-import.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvlite/examples/dashboard/apply-changes.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvlite/examples/dashboard/apply-filter-builder.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/delta-behavior/scripts/build-wasm.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/benches/run_benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/relay/deploy.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/run-benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/scripts/run-benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/sim/test-quick.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/src/learning-scenarios/diverse-patterns/setup.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge/scripts/build-wasm.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/exo-ai-2025/benches/run_benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/exo-ai-2025/crates/exo-wasm/build.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/exo-ai-2025/scripts/run-integration-tests.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/google-cloud/deploy.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/meta-cognition-spiking-neural-network/demos/snn/native/snn_simd.cpp
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/ruvLLM/esp32-flash/cluster-flash.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/ruvLLM/esp32-flash/cluster-monitor.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/ruvLLM/esp32-flash/install.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/ruvLLM/esp32-flash/scripts/offline-cache.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/rvf/scripts/rvf-claude-appliance.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/rvf/scripts/rvf-docker.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/rvf/scripts/rvf-mcp-server.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/rvf/scripts/rvf-quickstart.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/scipix/scripts/download_models.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/scipix/scripts/run_benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/scipix/scripts/setup_dev.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/scipix/web/build.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/vibecast-7sense/.claude/helpers/adr-compliance.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/vibecast-7sense/.claude/helpers/ddd-tracker.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/vibecast-7sense/.claude/statusline.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/vibecast-7sense/scripts/run_benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/wasm/ios/scripts/build.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/install.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/agentic-synth/training/run-multi-model-benchmark.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/postgres-cli/tests/test-npx-install.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvbot/deploy/gcp/deploy.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvbot/scripts/install.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvector/examples/cli-demo.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm/scripts/huggingface/publish.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/spiking-neural/native/snn_simd.cpp
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/benchmark/run_benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/benchmark/run_llm_benchmarks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/build-solver.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/build/build-all-platforms.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/build/build-linux.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/build/copy-binaries.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/ci/ci-sync-lockfile.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/ci/install-hooks.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/ci/sync-lockfile.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/deploy/deploy.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/deploy/test-deploy.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/publish-rvf.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/publish/check-and-publish-router-wasm.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/publish/publish-all.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/publish/publish-cli.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/publish/publish-crates.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/publish/publish-router-wasm.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/run_mincut_bench.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/test/test-all-graph-commands.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/test/test-docker-package.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/test/test-graph-cli.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/validate/validate-packages-simple.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/validate/validate-packages.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/validate/verify_hnsw_build.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/scripts/validate/verify-paper-impl.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/tests/agentic-jujutsu/run-all-tests.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/tests/integration/distributed/node_runner.sh
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/tests/test-all-packages.sh
third_party/wifi-sensing/vendor/wifi-radar/main.py
third_party/wifi-sensing/vendor/wifi-radar/scripts/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/scripts/check_code.sh
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_tensorrt.py
third_party/wifi-sensing/vendor/wifi-radar/scripts/setup_venv.sh
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py
third_party/wifi-sensing/vendor/wifi-radar/scripts/validate_live_capture.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/fall_detector.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/gait_analyzer.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/gait_anomaly_detector.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/hybrid_activity_fusion.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/api/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/api/app.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/config/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/data/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/data/csi_collector.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/models/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/models/encoder.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/models/multi_person_tracker.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/models/pose_estimator.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/processing/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/processing/signal_processor.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/streaming/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/streaming/rtmp_streamer.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/tests/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/utils/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/utils/code_quality.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/utils/live_capture_validation.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/utils/model_io.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/house_visualizer.py
third_party/wifi-sensing/vendor/wifi-radar/tests/__init__.py
third_party/wifi-sensing/vendor/wifi-radar/tests/conftest.py
third_party/wifi-sensing/vendor/wifi-radar/tests/test_api.py
third_party/wifi-sensing/vendor/wifi-radar/tests/test_csi_parser.py
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py
third_party/wifi-sensing/vendor/wifi-radar/tests/test_gait_anomaly_detector.py
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py
third_party/wifi-sensing/vendor/wifi-radar/tests/test_live_capture_validation.py
```

## Dependency Files

```text
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/components/bsp_C5_dual_antenna/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/components/bsp_C5_dual_antenna/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/master_recv/main/ui/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_recv/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_recv/main/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_recv/main/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_send/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_send/main/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-crab/slave_send/main/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/connect_rainmaker/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/connect_rainmaker/main/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/connect_rainmaker/main/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/components/commands/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/main/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/main/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/console_test/tools/requirements.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/wifi_sensing_demo/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/wifi_sensing_demo/main/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/esp-radar/wifi_sensing_demo/main/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_recv_router/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_recv_router/main/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_recv_router/main/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_recv/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_recv/main/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_recv/main/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_send/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_send/main/CMakeLists.txt
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/csi_send/main/idf_component.yml
third_party/wifi-sensing/vendor/esp-csi/examples/get-started/tools/requirements.txt
third_party/wifi-sensing/vendor/RuView/aether-arena/space/requirements.txt
third_party/wifi-sensing/vendor/RuView/archive/v1/requirements-lock.txt
third_party/wifi-sensing/vendor/RuView/archive/v1/setup.py
third_party/wifi-sensing/vendor/RuView/dashboard/package.json
third_party/wifi-sensing/vendor/RuView/examples/frontend/package.json
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/CMakeLists.txt
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/components/wasm3/CMakeLists.txt
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/CMakeLists.txt
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/idf_component.yml
third_party/wifi-sensing/vendor/RuView/firmware/esp32-csi-node/main/lp_core/CMakeLists.txt
third_party/wifi-sensing/vendor/RuView/firmware/esp32-hello-world/CMakeLists.txt
third_party/wifi-sensing/vendor/RuView/firmware/esp32-hello-world/main/CMakeLists.txt
third_party/wifi-sensing/vendor/RuView/harness/ruview/package.json
third_party/wifi-sensing/vendor/RuView/pyproject.toml
third_party/wifi-sensing/vendor/RuView/python/pyproject.toml
third_party/wifi-sensing/vendor/RuView/python/ruview-meta/pyproject.toml
third_party/wifi-sensing/vendor/RuView/python/tombstone/pyproject.toml
third_party/wifi-sensing/vendor/RuView/requirements-dev.txt
third_party/wifi-sensing/vendor/RuView/requirements.txt
third_party/wifi-sensing/vendor/RuView/tools/ruview-cli/package.json
third_party/wifi-sensing/vendor/RuView/tools/ruview-mcp/package.json
third_party/wifi-sensing/vendor/RuView/ui/mobile/package.json
third_party/wifi-sensing/vendor/RuView/ui/pose-fusion/pkg/ruvector_cnn_wasm/package.json
third_party/wifi-sensing/vendor/RuView/ui/pose-fusion/pkg/ruvector-attention/package.json
third_party/wifi-sensing/vendor/RuView/v2/crates/homecore-server/ui/package.json
third_party/wifi-sensing/vendor/RuView/v2/crates/wifi-densepose-desktop/ui/.vite/deps/package.json
third_party/wifi-sensing/vendor/RuView/v2/crates/wifi-densepose-desktop/ui/package.json
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/requirements.txt
third_party/wifi-sensing/vendor/wifi-densepose/firmware/esp32-csi-node/CMakeLists.txt
third_party/wifi-sensing/vendor/wifi-densepose/firmware/esp32-csi-node/main/CMakeLists.txt
third_party/wifi-sensing/vendor/wifi-densepose/pyproject.toml
third_party/wifi-sensing/vendor/wifi-densepose/requirements.txt
third_party/wifi-sensing/vendor/wifi-densepose/ui/mobile/package.json
third_party/wifi-sensing/vendor/wifi-densepose/v1/requirements-lock.txt
third_party/wifi-sensing/vendor/wifi-densepose/v1/setup.py
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/.claude/intelligence/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/benchmarks/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/agentic-robotics-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-node/npm/darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-node/npm/darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-node/npm/linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-node/npm/linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-node/npm/linux-x64-musl/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-node/npm/win32-arm64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-node/npm/win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-unified-wasm/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-attention-wasm/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-cluster/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-economy-wasm/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-exotic-wasm/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-gnn-node/npm/darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-gnn-node/npm/darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-gnn-node/npm/linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-gnn-node/npm/linux-arm64-musl/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-gnn-node/npm/linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-gnn-node/npm/linux-x64-musl/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-gnn-node/npm/win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-gnn-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-gnn-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-transformer-node/npm/darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-transformer-node/npm/darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-transformer-node/npm/linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-transformer-node/npm/linux-arm64-musl/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-transformer-node/npm/linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-transformer-node/npm/linux-x64-musl/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-transformer-node/npm/win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-transformer-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-transformer-wasm/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-graph-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-learning-wasm/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-nervous-system-wasm/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-router-ffi/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-router-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-server/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-solver-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-tiny-dancer-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-tiny-dancer-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/ruvector-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvf/rvf-node/npm/darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvf/rvf-node/npm/darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvf/rvf-node/npm/linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvf/rvf-node/npm/linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvf/rvf-node/npm/win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvf/rvf-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/rvlite/examples/dashboard/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/crates/sona/wasm-example/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/delta-behavior/wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-full/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/dashboard/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/relay/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/sim/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge-net/tests/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/edge/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/meta-cognition-spiking-neural-network/demos/exploration/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/meta-cognition-spiking-neural-network/demos/optimization/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/meta-cognition-spiking-neural-network/demos/snn/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/meta-cognition-spiking-neural-network/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/neural-trader/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/ruvLLM/esp32-flash/npm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/ruvLLM/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/rvf/dashboard/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/scipix/web/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/wasm-react/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/examples/wasm/ios/types/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/core/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/core/platforms/darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/core/platforms/darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/core/platforms/linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/core/platforms/linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/core/platforms/win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/agentic-integration/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/agentic-synth-examples/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/agentic-synth/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/burst-scaling/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/cli/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/cognitum-gate-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/core/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/graph-data-generator/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/graph-node/npm/darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/graph-node/npm/darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/graph-node/npm/linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/graph-node/npm/win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/graph-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/graph-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ospipe-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ospipe/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/postgres-cli/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/raft/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/replication/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/router-darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/router-darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/router-linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/router-linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/router-win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/router/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rudag/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rudag/pkg-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rudag/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruqu-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvbot/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvector-extensions/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvector-wasm-unified/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvector-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvector/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvector/src/core/onnx/pkg/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm-cli/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm-darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm-darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm-linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm-linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm-win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm/npm/darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm/npm/darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm/npm/linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm/npm/linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm/npm/win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/ruvllm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rvdna/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rvf-mcp-server/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rvf-node/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rvf-solver/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rvf-wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rvf/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/rvlite/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/scipix/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/sona/npm/darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/sona/npm/darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/sona/npm/linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/sona/npm/linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/sona/npm/linux-x64-musl/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/sona/npm/win32-arm64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/sona/npm/win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/sona/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/spiking-neural/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/tiny-dancer-darwin-arm64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/tiny-dancer-darwin-x64/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/tiny-dancer-linux-arm64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/tiny-dancer-linux-x64-gnu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/tiny-dancer-win32-x64-msvc/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/packages/tiny-dancer/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/npm/wasm/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/tests/agentic-jujutsu/package.json
third_party/wifi-sensing/vendor/wifi-densepose/vendor/ruvector/tests/docker-integration/package.json
third_party/wifi-sensing/vendor/wifi-radar/pyproject.toml
third_party/wifi-sensing/vendor/wifi-radar/requirements-dev.txt
third_party/wifi-sensing/vendor/wifi-radar/requirements.txt
```

## CSI / Router / ESP32 Hits

```text
third_party/wifi-sensing/vendor/WiROS/README.md:3:WiROS is a plug-and-play WiFi sensing toolbox allowing researchers to access coarse grained WiFi signal strength (RSSI), fine grained WiFi channel state information (CSI), and other MAC-layer information (device address, packet id’s or frequency-channel information). Additionally, WiROS open-sources state of-art algorithms to calibration and process WiFi measurements to furnish accurate bearing information for received WiFi signals. 
third_party/wifi-sensing/vendor/WiROS/README.md:6:1. [**CSI Node**](https://github.com/ucsdwcsng/wiros_csi_node) - Extends the Nexmon CSI toolkit[1] to provide a ROS overlay. 
third_party/wifi-sensing/vendor/WiROS/README.md:7:2. [**Processing Node**](https://github.com/ucsdwcsng/wiros_processing_node) - Provide calibration and post-processing of WiFi CSI measurments. Open-sources mulitple state-of-art bearing extraction algorithms to measure both the angle of arrival (at the receiver) and angle of departure (from the transmitter) of the WiFi signal.
third_party/wifi-sensing/vendor/WiROS/README.md:20:To get started with WiROS, clone these repositories into the `src` folder of your catkin workspace, and follow the [README](https://github.com/ucsdwcsng/wiros_csi_node/blob/main/README.md) in the [CSI Node](https://github.com/ucsdwcsng/wiros_csi_node) to configure your hardware.   
third_party/wifi-sensing/vendor/wifi-radar/requirements.txt:12:websockets>=12.0
third_party/wifi-sensing/vendor/wifi-radar/tests/test_live_capture_validation.py:3:from wifi_radar.data.csi_collector import CSICollector
third_party/wifi-sensing/vendor/wifi-radar/tests/test_live_capture_validation.py:26:    collector = CSICollector(buffer_size=8)
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:3:from wifi_radar.streaming.rtmp_streamer import RTMPStreamer
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:45:def test_rtmp_streamer_renders_frame():
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:46:    streamer = RTMPStreamer(width=320, height=240, fps=10)
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:48:    streamer.update_frame(pose_data=pose, confidence_data=pose["confidence"])
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:49:    assert streamer.latest_frame is not None
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:50:    assert streamer.latest_frame.shape == (240, 320, 3)
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:51:    assert streamer.latest_frame.sum() > 0
third_party/wifi-sensing/vendor/wifi-radar/tests/test_csi_parser.py:4:from wifi_radar.data.csi_collector import CSICollector
third_party/wifi-sensing/vendor/wifi-radar/tests/test_csi_parser.py:8:    collector = CSICollector()
third_party/wifi-sensing/vendor/wifi-radar/tests/test_csi_parser.py:12:    raw = b"CSI0" + struct.pack("<III", 3, 3, 64) + amp.tobytes() + phase.tobytes()
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:25:4. **CSI-Based Human Activity Recognition Using Channel State Information**
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:29:   - Summary: Presents techniques for extracting and processing CSI data for human activity recognition.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:33:### Channel State Information (CSI)
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:35:CSI data represents the channel properties of a communication link, containing information about:
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:42:In 802.11n/ac WiFi systems, CSI is collected for each subcarrier and for each transmitter-receiver antenna pair in MIMO systems.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:53:These interactions create measurable changes in the CSI, which can be analyzed to infer human presence, movement, and posture.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:66:1. [Linux CSI Tool](https://github.com/spanev/linux-80211n-csitool): Tool for collecting CSI measurements from WiFi devices
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:8:CSI Data Acquisition → Signal Processing → Neural Network Processing → Pose Estimation → Visualization/Streaming
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:11:### 1. CSI Data Acquisition
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:13:The system captures Channel State Information (CSI) from WiFi signals using a commodity router with 3×3 MIMO capability. CSI data contains:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:21:Raw CSI data undergoes several preprocessing steps:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:29:A dual-branch encoder processes the prepared CSI data:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:47:- RTMP streaming for external broadcasting
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:51:### WiFi CSI Extraction
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:53:We use the Linux CSI Tool or similar to extract CSI data from the WiFi router. This requires:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:54:- Modified router firmware
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:55:- Driver modifications for CSI extraction
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:56:- Network configuration for real-time data streaming
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:84:- RTMP protocol for streaming
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:9:| 2026-02-26 | WiPowerSys | ESP32-based CSI capture with skeleton supervision | Strong fit for commodity deployment workflows |
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:16:1. keep the existing CSI-to-pose backbone,
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:18:3. fuse short-window and long-window CSI motion evidence with pose confidence and gait metrics.
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:7:- A WiFi router capable of providing CSI (Channel State Information) data
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:8:  - Recommended: Nighthawk mesh router or similar devices
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:9:  - The router should support 3×3 MIMO capabilities
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:15:### Enabling CSI Collection
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:17:To collect CSI data from your router, you'll need to:
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:19:1. Install custom firmware on your router that enables CSI extraction
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:20:   - For Nighthawk routers: Follow the manufacturer's instructions for firmware updates
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:21:   - For TP-Link Archer series: Install OpenWrt and the `atheros-csi-tool` package
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:22:   - For ASUS routers: Use the Merlin firmware with CSI extraction patches
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:23:   - You may need to install OpenWrt or similar open-source firmware
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:25:2. Configure the router to stream CSI data
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:27:   # SSH into your router
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:30:   # Enable CSI tool (Nighthawk method)
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:33:   # Configure CSI streaming
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:34:   csi-tool stream --port 5500 --format binary
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:36:   # Alternative for OpenWrt-based routers
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:39:   # Alternative for ASUS routers
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:43:3. Verify that CSI data is being streamed
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:49:   python scripts/test_csi_connection.py --router-ip <YOUR_ROUTER_IP> --port 5500
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:51:   You should see continuous data streaming from the router.
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:53:4. Troubleshooting CSI collection:
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:54:   - Ensure your router model supports CSI extraction (most 802.11n/ac routers with supported chipsets)
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:55:   - Check that your router is operating in a supported WiFi mode (typically 802.11n/ac)
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:57:   - Some routers require specific channel width settings (20MHz, 40MHz, or 80MHz)
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:60:5. CSI data format considerations:
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:61:   - Different routers may provide CSI in different formats
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:63:   - See the documentation for your specific router model
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:64:   - Our tool supports common formats including Intel, Atheros, and Broadcom CSI formats
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:92:router:
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:96:  csi_format: atheros    # Router CSI format (atheros, intel, broadcom)
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:110:streaming:
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:146:2. For simulation mode (no real WiFi router required)
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:162:   # Record CSI data to file
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:165:   # Replay previously recorded CSI data
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:185:6. View the RTMP stream
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:193:   # Save the stream to a file
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:211:### No CSI Data Received
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:213:- Verify your router is correctly configured for CSI extraction
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:214:- Check network connectivity between your computer and router
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:222:- Lower the resolution of the RTMP stream
third_party/wifi-sensing/vendor/wifi-radar/README.md:25:Channel State Information from commodity WiFi hardware or the built-in
third_party/wifi-sensing/vendor/wifi-radar/README.md:31:WiFi-Radar is a camera-free sensing system that uses normal WiFi signal reflections to infer human movement. Instead of images, it reads CSI (Channel State Information), which captures how radio waves change when people move, stand, walk, or fall in a room. That means the system can monitor activity without recording visual identity data.
third_party/wifi-sensing/vendor/wifi-radar/README.md:35:1. Collect CSI frames from a router or simulator.
third_party/wifi-sensing/vendor/wifi-radar/README.md:60:> Start with simulation mode first, then enable the REST API or RTMP stream as
third_party/wifi-sensing/vendor/wifi-radar/README.md:79:This panel style mirrors the live monitor experience, where 3-D skeleton estimation, confidence trends, and CSI traces are observed together to validate model health in real time.
third_party/wifi-sensing/vendor/wifi-radar/README.md:89:![CSI reading waterfall](docs/images/csi-reading-waterfall.svg)
third_party/wifi-sensing/vendor/wifi-radar/README.md:91:This chart illustrates typical CSI amplitude and phase trajectories over time, which are the core signals used by tracking, gait, anomaly, and fusion modules.
third_party/wifi-sensing/vendor/wifi-radar/README.md:115:- [Transfer Learning on Real CSI](#transfer-learning-on-real-csi)
third_party/wifi-sensing/vendor/wifi-radar/README.md:131:| <sub>📶</sub> | <sub>CSI collection</sub> | <sub>Real or simulated CSI frames with 3×3 MIMO support</sub> | <sub>High</sub> | <sub>✅ Stable</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:137:| <sub>🔀</sub> | <sub>Hybrid CSI + pose fusion</sub> | <sub>Multi-window motion fusion with pose and gait cues for more robust live activity scoring</sub> | <sub>Medium</sub> | <sub>🧪 Experimental</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:140:| <sub>🧪</sub> | <sub>Transfer learning workflow</sub> | <sub>Fine-tune on real-world CSI datasets in NPZ format</sub> | <sub>High</sub> | <sub>🧪 Experimental</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:149:    A[WiFi Router or Simulator] --> B[CSICollector]
third_party/wifi-sensing/vendor/wifi-radar/README.md:163:**main.py**. CSI is collected, denoised, encoded, decoded into pose keypoints,
third_party/wifi-sensing/vendor/wifi-radar/README.md:165:flagging, dashboard visualisation, RTMP streaming, and the optional REST API.
third_party/wifi-sensing/vendor/wifi-radar/README.md:179:| Hybrid activity fusion | Multi-window weighted fusion | $s = \sum_w \alpha_w m_w,\; r = f(s,p,g,q)$ | Resilient when one signal stream becomes noisy | Single-window scoring is more sensitive to transient noise |
third_party/wifi-sensing/vendor/wifi-radar/README.md:188:WiFi-Radar builds on the research thread around **RF sensing, CSI-based human
third_party/wifi-sensing/vendor/wifi-radar/README.md:197:| <sub>WiFi Activity Recognition</sub> | <sub>IEEE Pervasive 2019</sub> | <sub>Deep learning on CSI for device-free activity inference</sub> | <sub>[Paper](https://ieeexplore.ieee.org/document/8713982)</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:215:- live CSI validation and replay,
third_party/wifi-sensing/vendor/wifi-radar/README.md:216:- hybrid CSI plus pose fusion,
third_party/wifi-sensing/vendor/wifi-radar/README.md:235:| <sub>Docker + nginx-rtmp</sub> | <sub>Deployment and streaming</sub> | <sub>Reproducible stack and HLS playback</sub> | <sub>Bare-metal services</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:250:- 802.11n/ac access point with CSI extraction firmware
third_party/wifi-sensing/vendor/wifi-radar/README.md:251:  - Atheros routers running OpenWrt + `ath9k` CSI patch
third_party/wifi-sensing/vendor/wifi-radar/README.md:256:> **Tip:** Start with `--simulation` — no router, no GPU needed.
third_party/wifi-sensing/vendor/wifi-radar/README.md:298:HLS stream: `http://localhost:8080/hls/wifi_radar.m3u8`
third_party/wifi-sensing/vendor/wifi-radar/README.md:307:python main.py --router-ip 192.168.1.1 --rtmp-url rtmp://localhost/live/wifi_radar
third_party/wifi-sensing/vendor/wifi-radar/README.md:314:| <sub>`--simulation`</sub> | <sub>off</sub> | <sub>Use the built-in CSI simulator</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:316:| <sub>`--router-ip IP`</sub> | <sub>`192.168.1.1`</sub> | <sub>Real router address</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:317:| <sub>`--router-port P`</sub> | <sub>`5500`</sub> | <sub>CSI TCP port</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:327:| <sub>`--record`</sub> | <sub>off</sub> | <sub>Save CSI frames to disk</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:357:router:
third_party/wifi-sensing/vendor/wifi-radar/README.md:375:streaming:
third_party/wifi-sensing/vendor/wifi-radar/README.md:416:The runtime maintains stable person identities across frames so the monitoring stack can follow multiple occupants and associate alerts with the correct person. This is critical because every downstream module is person-scoped. If identity switches occur, the fall detector, gait history, and anomaly history become mixed across people and produce incorrect alerts.
third_party/wifi-sensing/vendor/wifi-radar/README.md:451:Falls are detected from motion, posture change, and recovery state, then surfaced in both the dashboard and REST API event stream. The detector is a finite state machine (FSM), which was chosen because it is interpretable and easy to calibrate for different environments.
third_party/wifi-sensing/vendor/wifi-radar/README.md:487:The system estimates cadence, stride, symmetry, and walking-speed proxies from the rolling pose stream for continuous mobility monitoring. It uses ankle trajectory minima as step events because foot strike naturally appears as a local minimum in ankle height.
third_party/wifi-sensing/vendor/wifi-radar/README.md:509:> Peak detection is robust in noisy CSI settings and gives explainable metrics that are easy to compare across sessions.
third_party/wifi-sensing/vendor/wifi-radar/README.md:537:A recent addition combines CSI motion evidence, pose confidence, and gait signals into a more robust live activity estimate for walking, stationary, high-motion, transition, and possible-fall states. This module improves stability when one modality briefly drops in quality.
third_party/wifi-sensing/vendor/wifi-radar/README.md:555:  A[CSI amplitude and phase deltas] --> B[Windowed motion scores]
third_party/wifi-sensing/vendor/wifi-radar/README.md:581:WiFi-Radar can now run without the dashboard for embedded or service-style integrations. In headless mode, the processing pipeline continues to ingest CSI, run inference, and publish events and metrics to FastAPI. This pattern is useful for integrations such as smart-home controllers, backend analytics pipelines, and edge gateways where a browser dashboard is not required.
third_party/wifi-sensing/vendor/wifi-radar/README.md:590:    App->>Pipeline: process CSI frames
third_party/wifi-sensing/vendor/wifi-radar/README.md:628:## Transfer Learning on Real CSI
third_party/wifi-sensing/vendor/wifi-radar/README.md:718:**Watch the stream in a browser:**
third_party/wifi-sensing/vendor/wifi-radar/README.md:740:- CSI amplitude + phase signal (TX0·RX0)
third_party/wifi-sensing/vendor/wifi-radar/README.md:749:- Live-editable settings: router IP, simulation toggle, confidence threshold,
third_party/wifi-sensing/vendor/wifi-radar/README.md:750:  max people, RTMP URL, stream FPS, fall-detection thresholds
third_party/wifi-sensing/vendor/wifi-radar/README.md:778:│       ├── streaming/
third_party/wifi-sensing/vendor/wifi-radar/README.md:779:│       │   └── rtmp_streamer.py
third_party/wifi-sensing/vendor/wifi-radar/README.md:838:# Fine-tune on real CSI datasets
third_party/wifi-sensing/vendor/wifi-radar/README.md:852:- Flashing OpenWrt firmware with CSI extraction patches
third_party/wifi-sensing/vendor/wifi-radar/README.md:853:- Configuring `ath9k` or Intel 5300 CSI tools
third_party/wifi-sensing/vendor/wifi-radar/README.md:854:- Streaming CSI frames to the collection host
third_party/wifi-sensing/vendor/wifi-radar/README.md:857:> **Security note:** The CSI streaming port (default 5500) and the RTMP port
third_party/wifi-sensing/vendor/wifi-radar/README.md:865:- Initial release: CSI collection, simulation mode, signal processing, dual-branch CNN encoder
third_party/wifi-sensing/vendor/wifi-radar/README.md:869:- RTMP streaming via FFmpeg subprocess
third_party/wifi-sensing/vendor/wifi-radar/README.md:877:- Transfer-learning script for real-world CSI datasets
third_party/wifi-sensing/vendor/wifi-radar/README.md:905:- [x] Transfer learning from real-world CSI datasets
third_party/wifi-sensing/vendor/wifi-radar/README.md:910:- [x] Extended real-hardware validation against live CSI captures
third_party/wifi-sensing/vendor/wifi-radar/README.md:911:- [x] Broader end-to-end regression coverage across the dashboard and streaming stack
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:3:"""Fine-tune WiFi-Radar models on real-world CSI datasets stored as NPZ files."""
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:32:class RealWorldCSIDataset(Dataset):
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:55:    parser = argparse.ArgumentParser(description="Transfer learning on real-world CSI datasets")
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:75:    dataset = RealWorldCSIDataset(dataset_paths)
third_party/wifi-sensing/vendor/wifi-radar/scripts/README.md:18:# With custom router settings
third_party/wifi-sensing/vendor/wifi-radar/scripts/README.md:19:python scripts/start_wifi_radar.py --router-ip 192.168.1.1 --router-port 5500
third_party/wifi-sensing/vendor/wifi-radar/scripts/README.md:25:python scripts/start_wifi_radar.py --rtmp-url rtmp://streaming-server/live/wifi_radar
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:9:    weights/encoder.onnx         — CSI amplitude + phase → 256-d feature vector
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:4:Purpose: Train DualBranchEncoder + PoseEstimator on synthetic CSI/pose pairs
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:7:         inference immediately without real router hardware.
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:147:    """Generate a single synthetic CSI frame for a person at (x_pos, y_pos).
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:149:    ID: WR-SCRIPT-TRAIN-GCSI-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:151:                 simulating multipath CSI influenced by person position.
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:152:    Purpose: Provide synthetic CSI training inputs correlated with the person
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:207:    Requirement: Generate n_samples synthetic (CSI, pose) pairs at construction
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:210:             baseline model can be trained on any CPU/GPU without a real router.
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:243:        Requirement: Generate n_samples (CSI, pose) pairs and store them in
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_simulation_baseline.py:371:             run inference immediately without real router hardware.
third_party/wifi-sensing/vendor/wifi-radar/main.py:4:Requirement: Orchestrate all WiFi-Radar subsystems (CSI collection, signal
third_party/wifi-sensing/vendor/wifi-radar/main.py:6:             fall detection, gait analysis, visualisation, and RTMP streaming)
third_party/wifi-sensing/vendor/wifi-radar/main.py:16:      ├─ CSICollector.start()  — daemon thread producing CSI frames
third_party/wifi-sensing/vendor/wifi-radar/main.py:49:    Purpose: Allow operator control of simulation mode, router address, dashboard
third_party/wifi-sensing/vendor/wifi-radar/main.py:83:        help="Run in simulation mode (no real CSI data)",
third_party/wifi-sensing/vendor/wifi-radar/main.py:86:        "--router-ip",
third_party/wifi-sensing/vendor/wifi-radar/main.py:88:        default="192.168.1.1",  # Replace with your router's IP address
third_party/wifi-sensing/vendor/wifi-radar/main.py:89:        help="IP address of the WiFi router (see docs/setup-guide.md)",
third_party/wifi-sensing/vendor/wifi-radar/main.py:92:        "--router-port", type=int, default=5500, help="Port for CSI data collection"
third_party/wifi-sensing/vendor/wifi-radar/main.py:101:        help="RTMP URL for streaming",
third_party/wifi-sensing/vendor/wifi-radar/main.py:110:    parser.add_argument("--record", action="store_true", help="Record CSI data to file")
third_party/wifi-sensing/vendor/wifi-radar/main.py:117:    parser.add_argument("--replay", type=str, help="Replay recorded CSI data from file")
third_party/wifi-sensing/vendor/wifi-radar/main.py:201:    Requirement: Return a nested config dict with sections: router, system, dashboard,
third_party/wifi-sensing/vendor/wifi-radar/main.py:202:                 streaming, house_visualization; override defaults with values from
third_party/wifi-sensing/vendor/wifi-radar/main.py:228:        Unit test: create a YAML file overriding router.ip; assert config['router']['ip']
third_party/wifi-sensing/vendor/wifi-radar/main.py:237:        "router": {
third_party/wifi-sensing/vendor/wifi-radar/main.py:255:        "streaming": {
third_party/wifi-sensing/vendor/wifi-radar/main.py:304:    Rationale: Daemon threads for processing, streaming, and visualisation are
third_party/wifi-sensing/vendor/wifi-radar/main.py:315:        On exit: csi_collector, rtmp_streamer, and house_visualizer are stopped.
third_party/wifi-sensing/vendor/wifi-radar/main.py:319:        Spawns daemon threads; opens network sockets; binds HTTP and RTMP ports.
third_party/wifi-sensing/vendor/wifi-radar/main.py:352:    if args.router_ip:
third_party/wifi-sensing/vendor/wifi-radar/main.py:353:        config["router"]["ip"] = args.router_ip
third_party/wifi-sensing/vendor/wifi-radar/main.py:354:    if args.router_port:
third_party/wifi-sensing/vendor/wifi-radar/main.py:355:        config["router"]["port"] = args.router_port
third_party/wifi-sensing/vendor/wifi-radar/main.py:359:        config["streaming"]["rtmp_url"] = args.rtmp_url
third_party/wifi-sensing/vendor/wifi-radar/main.py:389:        from wifi_radar.data.csi_collector import CSICollector
third_party/wifi-sensing/vendor/wifi-radar/main.py:394:        from wifi_radar.streaming.rtmp_streamer import RTMPStreamer
third_party/wifi-sensing/vendor/wifi-radar/main.py:409:    logger.info("Initializing CSI data collection")
third_party/wifi-sensing/vendor/wifi-radar/main.py:410:    csi_collector = CSICollector(
third_party/wifi-sensing/vendor/wifi-radar/main.py:411:        router_ip=config["router"]["ip"], port=config["router"]["port"]
third_party/wifi-sensing/vendor/wifi-radar/main.py:415:        logger.info("CSI recording enabled: output_dir=%s", os.path.expanduser(args.output_dir))
third_party/wifi-sensing/vendor/wifi-radar/main.py:470:            csi_collector.router_ip = config.get("router", {}).get("ip", csi_collector.router_ip)
third_party/wifi-sensing/vendor/wifi-radar/main.py:471:            csi_collector.port = int(config.get("router", {}).get("port", csi_collector.port))
third_party/wifi-sensing/vendor/wifi-radar/main.py:478:    # Initialize RTMP streaming
third_party/wifi-sensing/vendor/wifi-radar/main.py:479:    logger.info("Initializing RTMP streaming")
third_party/wifi-sensing/vendor/wifi-radar/main.py:480:    rtmp_streamer = RTMPStreamer(
third_party/wifi-sensing/vendor/wifi-radar/main.py:481:        rtmp_url=config["streaming"]["rtmp_url"],
third_party/wifi-sensing/vendor/wifi-radar/main.py:482:        width=config["streaming"]["width"],
third_party/wifi-sensing/vendor/wifi-radar/main.py:483:        height=config["streaming"]["height"],
third_party/wifi-sensing/vendor/wifi-radar/main.py:484:        fps=config["streaming"]["fps"],
third_party/wifi-sensing/vendor/wifi-radar/main.py:501:        logger.info("Starting CSI data collection")
third_party/wifi-sensing/vendor/wifi-radar/main.py:508:        # Start RTMP streaming
third_party/wifi-sensing/vendor/wifi-radar/main.py:509:        logger.info("Starting RTMP streaming")
third_party/wifi-sensing/vendor/wifi-radar/main.py:510:        rtmp_streamer.start()
third_party/wifi-sensing/vendor/wifi-radar/main.py:541:            """Main inference loop: CSI -> signal process -> encode -> pose -> track -> alert.
third_party/wifi-sensing/vendor/wifi-radar/main.py:544:            Requirement: Continuously dequeue CSI frames, run the full inference
third_party/wifi-sensing/vendor/wifi-radar/main.py:554:                Pushes results to dashboard, rtmp_streamer, house_visualizer.
third_party/wifi-sensing/vendor/wifi-radar/main.py:563:                Calls rtmp_streamer.update_frame().
third_party/wifi-sensing/vendor/wifi-radar/main.py:576:                CSICollector.get_csi_data; SignalProcessor.process;
third_party/wifi-sensing/vendor/wifi-radar/main.py:688:                                "message": "Hybrid CSI plus pose fusion flagged a possible fall pattern.",
third_party/wifi-sensing/vendor/wifi-radar/main.py:755:                        rtmp_streamer.update_frame(
third_party/wifi-sensing/vendor/wifi-radar/main.py:794:        rtmp_streamer.stop()
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/README.md:8:- CSI data visualization tools
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/README.md:23:- CSI signal visualization
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:4:         1. Live Monitor   — 3-D pose, CSI signal, detection stats
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:187:                    dbc.Col(html.Small("Human Pose Estimation via WiFi CSI",
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:224:                 confidence trend, and raw CSI signal quality side-by-side.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:280:                        dbc.CardHeader("CSI Signal (TX0 · RX0)"),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:347:                     stream FPS, fall detection enable/thresholds, and a save button.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:373:        router  = cfg.get("router", {})
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:376:        stream  = cfg.get("streaming", {})
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:388:                                dbc.Col(dbc.Input(id="cfg-router-ip",   value=router.get("ip", "192.168.1.1"), type="text")),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:392:                                dbc.Col(dbc.Input(id="cfg-router-port", value=str(router.get("port", 5500)), type="number")),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:433:                                                  value=stream.get("rtmp_url", "rtmp://localhost/live/wifi_radar"),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:438:                                dbc.Col(dbc.Input(id="cfg-stream-fps",
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:439:                                                  value=str(stream.get("fps", 30)),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:715:                State("cfg-router-ip",      "value"),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:716:                State("cfg-router-port",    "value"),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:721:                State("cfg-stream-fps",     "value"),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:728:        def save_config(n_clicks, router_ip, router_port, simulation,
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:729:                        conf_thr, max_people, rtmp_url, stream_fps,
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:739:                router_ip:   Router IP address string.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:740:                router_port: Router TCP port integer.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:745:                stream_fps:  Streaming frame rate integer.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:757:                    "router": {
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:758:                        "ip":   str(router_ip or "192.168.1.1"),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:759:                        "port": int(router_port or 5500),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:766:                    "streaming": {
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:768:                        "fps":      int(stream_fps or 30),
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:991:        """Return a blank CSI subcarrier figure used during initialisation.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:993:        ID: WR-VIZ-DASH-ECSIFIG-001
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:996:        Purpose: Prevent the CSI card from showing a grey placeholder at startup.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:1001:            go.Figure — empty CSI figure with configured layout.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:1017:        """Build the CSI subcarrier figure from the first TX-RX antenna pair.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:1019:        ID: WR-VIZ-DASH-UCSIFIG-001
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:1024:                 or interference patterns in the CSI measurement.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:1091:                   updates (e.g. CSI only) do not corrupt unrelated fields.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/visualization/dashboard.py:1215:                   process that would duplicate threads and open the RTMP streamer twice.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/gait_analyzer.py:5:         via WiFi-CSI pose inference.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/gait_analyzer.py:37:    Purpose: Provide downstream gait metrics (cadence, symmetry, stride)
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/gait_analyzer.py:69:               controlled precision reduce downstream formatting burden.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/gait_analyzer.py:132:        Purpose: Prepare the analyzer for streaming update() calls without
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/gait_anomaly_detector.py:34:    """Flag unusual gait patterns from a stream of GaitMetrics.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/gait_anomaly_detector.py:83:        Purpose: Prepare the detector for streaming updates.
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/fall_detector.py:37:    Purpose: Allow downstream components to compare severity levels numerically
third_party/wifi-sensing/vendor/wifi-radar/src/wifi_radar/analysis/fall_detector.py:58:    Purpose: Decouple the fall detector from downstream consumers by providing
```

## Inference / Model Hits

```text
third_party/wifi-sensing/vendor/WiROS/README.md:13:2. Exposes all relevant measurements as accessible ROS topics. See [`rf_msgs`](https://github.com/ucsdwcsng/rf_msgs) for more details.  
third_party/wifi-sensing/vendor/WiROS/README.md:32:1. Blanco, Alejandro, et al. "Accurate ubiquitous localization with off-the-shelf ieee 802.11 ac devices." The 19th Annual International Conference on Mobile Systems, Applications, and Services (MobiSys 2021). 2021.
third_party/wifi-sensing/vendor/WiROS/README.md:33:2. Kotaru, Manikanta, et al. "Spotfi: Decimeter level localization using wifi." Proceedings of the 2015 ACM Conference on Special Interest Group on Data Communication. 2015.
third_party/wifi-sensing/vendor/wifi-radar/tests/__init__.py:4:Purpose: Enable pytest to find and execute integration and system-level tests
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:4:from wifi_radar.analysis.hybrid_activity_fusion import HybridActivityFusion
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:7:def test_hybrid_activity_fusion_detects_stationary_then_walking():
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:16:            pose_confidence=np.ones(17, dtype=np.float32) * 0.95,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:20:    assert result["activity_label"] == "stationary"
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:21:    assert result["motion_score"] < 0.05
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:30:            pose_confidence=np.ones(17, dtype=np.float32) * 0.9,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:41:    assert moving["activity_label"] in {"walking", "high_motion"}
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:42:    assert moving["motion_score"] > 0.05
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:45:def test_hybrid_activity_fusion_escalates_possible_fall():
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:53:        pose_confidence=np.ones(17, dtype=np.float32) * 0.4,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:62:        fall_severity=2,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:65:    assert result["activity_label"] == "possible_fall"
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:66:    assert result["fall_risk"] >= 0.8
third_party/wifi-sensing/vendor/wifi-radar/tests/test_api.py:34:            "events": [{"message": "fall alert", "severity": 2}],
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:7:def _sample_pose():
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:19:    pose = _sample_pose()
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:25:        pose_data=pose,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:26:        confidence_data=pose["confidence"],
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:28:        tracked_people=[{"person_id": 1, **pose}],
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:31:        fall_events=[{"message": "fall alert", "severity": 2, "timestamp": 123.0}],
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:35:    dashboard.confidence_history.append(float(np.mean(pose["confidence"])))
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:36:    pose_fig = dashboard._update_pose_figure(pose)
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:40:    assert len(pose_fig.data) > 0
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:47:    pose = _sample_pose()
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:48:    streamer.update_frame(pose_data=pose, confidence_data=pose["confidence"])
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:3:The WiFi-Radar system is based on research in the field of RF-based human sensing, particularly focusing on WiFi signals for pose estimation. This document provides key references that form the theoretical foundation of this project.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:11:   - Summary: Presents a system for human pose estimation using WiFi signals, without requiring cameras or specialized hardware.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:17:   - Summary: Demonstrates human pose estimation through walls using specialized RF devices.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:23:   - Summary: Explores the use of deep learning for WiFi-based activity recognition.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:29:   - Summary: Presents techniques for extracting and processing CSI data for human activity recognition.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:53:These interactions create measurable changes in the CSI, which can be analyzed to infer human presence, movement, and posture.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:57:Modern pose estimation from WiFi signals uses deep learning techniques including:
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:67:2. [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose): Popular framework for pose estimation
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:68:3. [DensePose](https://github.com/facebookresearch/DensePose): Research framework for dense human pose estimation
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:73:2. **Fine-grained gestures**: Detecting subtle hand and finger movements
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:74:3. **Health monitoring**: Using WiFi-based pose for fall detection and gait analysis
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:5:WiFi-Radar consists of several interconnected components that work together to transform WiFi signals into human pose estimations:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:67:The pose estimation system uses:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:68:- PyTorch for deep learning implementation
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:85:- Custom frame generation from pose data
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:7:| 2026-01-18 | PerceptAlign / geometry-aware cross-layout pose estimation | Explicitly conditions the model on transceiver geometry to reduce layout overfitting | Strong fit for real-hardware deployment and replay validation |
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:8:| 2026-02-09 | WiFlow | Lightweight spatio-temporal decoupling for continuous WiFi pose estimation | Strong fit for low-latency and edge inference |
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:10:| 2026-04-01 | MKFi | Multi-window fusion for temporally robust WiFi activity recognition under limited data | Strong fit for fall and gait robustness |
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:16:1. keep the existing CSI-to-pose backbone,
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:18:3. fuse short-window and long-window CSI motion evidence with pose confidence and gait metrics.
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:20:This repository now includes a lightweight implementation of that idea through the hybrid activity fusion stage in the analysis package.
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:3:This guide will help you set up and run the WiFi-Radar system for human pose estimation through WiFi signals.
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:54:   - Ensure your router model supports CSI extraction (most 802.11n/ac routers with supported chipsets)
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:63:   - See the documentation for your specific router model
third_party/wifi-sensing/vendor/wifi-radar/README.md:8:[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?logo=pytorch)](https://pytorch.org)
third_party/wifi-sensing/vendor/wifi-radar/README.md:9:[![ONNX](https://img.shields.io/badge/ONNX-1.15%2B-005CED?logo=onnx)](https://onnx.ai)
third_party/wifi-sensing/vendor/wifi-radar/README.md:10:[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](docker/docker-compose.yml)
third_party/wifi-sensing/vendor/wifi-radar/README.md:15:*Detect, track and analyse human poses through walls — no cameras required*
third_party/wifi-sensing/vendor/wifi-radar/README.md:23:WiFi-Radar is a Python research system for **WiFi-based human pose estimation,
third_party/wifi-sensing/vendor/wifi-radar/README.md:24:tracking, fall detection, gait analytics, and headless monitoring**. It consumes
third_party/wifi-sensing/vendor/wifi-radar/README.md:27:17-keypoint 3-D pose outputs in real time.
third_party/wifi-sensing/vendor/wifi-radar/README.md:31:WiFi-Radar is a camera-free sensing system that uses normal WiFi signal reflections to infer human movement. Instead of images, it reads CSI (Channel State Information), which captures how radio waves change when people move, stand, walk, or fall in a room. That means the system can monitor activity without recording visual identity data.
third_party/wifi-sensing/vendor/wifi-radar/README.md:37:3. Encode temporal signal patterns into pose features.
third_party/wifi-sensing/vendor/wifi-radar/README.md:39:5. Run behavior modules to produce fall, gait, anomaly, and activity outputs.
third_party/wifi-sensing/vendor/wifi-radar/README.md:44:- **How each person is moving**: stationary, walking, transition, high-motion.
third_party/wifi-sensing/vendor/wifi-radar/README.md:45:- **Whether motion resembles a fall pattern**: state-machine and hybrid fall risk.
third_party/wifi-sensing/vendor/wifi-radar/README.md:49:This repository is designed for readable, explainable behavior analytics. The algorithms were selected so operators can inspect why a decision was made, tune thresholds per environment, and deploy on resource-constrained edge hardware.
third_party/wifi-sensing/vendor/wifi-radar/README.md:73:![Radar motion heatmap](docs/images/radar-motion-map.svg)
third_party/wifi-sensing/vendor/wifi-radar/README.md:75:This view represents spatial motion energy around the antenna array. It helps explain where strong reflections are coming from and gives operators an immediate sense of movement intensity in the monitored room.
third_party/wifi-sensing/vendor/wifi-radar/README.md:79:This panel style mirrors the live monitor experience, where 3-D skeleton estimation, confidence trends, and CSI traces are observed together to validate model health in real time.
third_party/wifi-sensing/vendor/wifi-radar/README.md:83:This event-centric view demonstrates how fall and gait signals are surfaced as actionable timeline events rather than raw numerical output.
third_party/wifi-sensing/vendor/wifi-radar/README.md:87:This point-cloud style visual approximates what WiFi-radar reflections and tracked keypoints look like in room coordinates. It is useful for communicating the distinction between raw RF reflection clusters and final pose estimates.
third_party/wifi-sensing/vendor/wifi-radar/README.md:89:![CSI reading waterfall](docs/images/csi-reading-waterfall.svg)
third_party/wifi-sensing/vendor/wifi-radar/README.md:110:- [Fall Detection](#fall-detection)
third_party/wifi-sensing/vendor/wifi-radar/README.md:113:- [Hybrid Activity Fusion](#hybrid-activity-fusion)
third_party/wifi-sensing/vendor/wifi-radar/README.md:116:- [ONNX Export](#onnx-export)
third_party/wifi-sensing/vendor/wifi-radar/README.md:132:| <sub>🧠</sub> | <sub>Dual-branch pose pipeline</sub> | <sub>Amplitude + phase encoder feeding temporal pose estimation</sub> | <sub>High</sub> | <sub>✅ Stable</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:137:| <sub>🔀</sub> | <sub>Hybrid CSI + pose fusion</sub> | <sub>Multi-window motion fusion with pose and gait cues for more robust live activity scoring</sub> | <sub>Medium</sub> | <sub>🧪 Experimental</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:139:| <sub>⚡</sub> | <sub>ONNX and TensorRT export</sub> | <sub>Edge deployment path for Jetson-style hardware</sub> | <sub>High</sub> | <sub>🧪 Experimental</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:141:| <sub>🐳</sub> | <sub>Docker deployment</sub> | <sub>App + RTMP stack via Compose</sub> | <sub>Medium</sub> | <sub>✅ Stable</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:163:**main.py**. CSI is collected, denoised, encoded, decoded into pose keypoints,
third_party/wifi-sensing/vendor/wifi-radar/README.md:164:and then routed into tracking, fall analysis, gait analytics, optional anomaly
third_party/wifi-sensing/vendor/wifi-radar/README.md:176:| Fall detection | Finite state machine with thresholds | $v_z < \tau_v$, $\theta > \tau_\theta$, $\frac{\Delta h}{h_0} > \tau_h$ | Interpretable and debuggable in real deployments | End-to-end fall classifiers are less transparent and harder to calibrate |
third_party/wifi-sensing/vendor/wifi-radar/README.md:179:| Hybrid activity fusion | Multi-window weighted fusion | $s = \sum_w \alpha_w m_w,\; r = f(s,p,g,q)$ | Resilient when one signal stream becomes noisy | Single-window scoring is more sensitive to transient noise |
third_party/wifi-sensing/vendor/wifi-radar/README.md:189:activity understanding, and privacy-preserving pose estimation**.
third_party/wifi-sensing/vendor/wifi-radar/README.md:195:| <sub>DensePose from WiFi</sub> | <sub>SIGCOMM 2022</sub> | <sub>Dense human pose recovery from commodity WiFi</sub> | <sub>[Paper](https://arxiv.org/abs/2301.00250)</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:196:| <sub>Through-Wall Human Pose Estimation Using Radio Signals</sub> | <sub>CVPR 2018</sub> | <sub>Through-wall supervision and RF pose reasoning</sub> | <sub>[Paper](https://openaccess.thecvf.com/content_cvpr_2018/html/Zhao_Through-Wall_Human_Pose_CVPR_2018_paper.html)</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:197:| <sub>WiFi Activity Recognition</sub> | <sub>IEEE Pervasive 2019</sub> | <sub>Deep learning on CSI for device-free activity inference</sub> | <sub>[Paper](https://ieeexplore.ieee.org/document/8713982)</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:198:| <sub>WiPose</sub> | <sub>MobiSys 2020</sub> | <sub>3-D body pose estimation via commodity WiFi</sub> | <sub>[Paper](https://dl.acm.org/doi/10.1145/3386901.3388940)</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:204:| <sub>2026-01</sub> | <sub>Geometry-aware cross-layout WiFi pose estimation</sub> | <sub>Better generalisation across rooms and antenna layouts</sub> | <sub>[Paper](https://arxiv.org/abs/2601.12252)</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:205:| <sub>2026-02</sub> | <sub>WiFlow</sub> | <sub>Lightweight continuous pose estimation with lower runtime cost</sub> | <sub>[Paper](https://arxiv.org/abs/2602.08661)</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:207:| <sub>2026-04</sub> | <sub>MKFi</sub> | <sub>Multi-window temporal fusion for robust activity recognition</sub> | <sub>[Paper](https://www.sciencedirect.com/science/article/pii/S0031320325011756)</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:216:- hybrid CSI plus pose fusion,
third_party/wifi-sensing/vendor/wifi-radar/README.md:226:| <sub>Technology</sub> | <sub>Purpose</sub> | <sub>Why Chosen</sub> | <sub>Alternatives</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:229:| <sub>PyTorch</sub> | <sub>Model training and inference</sub> | <sub>Flexible for CNN/LSTM experimentation</sub> | <sub>TensorFlow</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:233:| <sub>ONNX</sub> | <sub>Portable model export</sub> | <sub>Runtime-neutral deployment path</sub> | <sub>TorchScript</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:234:| <sub>TensorRT</sub> | <sub>Jetson acceleration</sub> | <sub>Best NVIDIA edge inference performance</sub> | <sub>Plain ONNX Runtime</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:244:- Docker + Docker Compose (optional — for the full stack deployment)
third_party/wifi-sensing/vendor/wifi-radar/README.md:280:python scripts/train_simulation_baseline.py
third_party/wifi-sensing/vendor/wifi-radar/README.md:289:docker compose -f docker/docker-compose.yml up --build
third_party/wifi-sensing/vendor/wifi-radar/README.md:319:| <sub>`--export-onnx`</sub> | <sub>off</sub> | <sub>Export ONNX models and exit</sub> |
third_party/wifi-sensing/vendor/wifi-radar/README.md:342:# Export ONNX models for edge deployment
third_party/wifi-sensing/vendor/wifi-radar/README.md:380:fall_detection:
third_party/wifi-sensing/vendor/wifi-radar/README.md:383:  angle_threshold_deg: 40.0   # body-from-vertical angle to trigger possible-fall
third_party/wifi-sensing/vendor/wifi-radar/README.md:394:python scripts/train_simulation_baseline.py
third_party/wifi-sensing/vendor/wifi-radar/README.md:401:python scripts/train_simulation_baseline.py \
third_party/wifi-sensing/vendor/wifi-radar/README.md:416:The runtime maintains stable person identities across frames so the monitoring stack can follow multiple occupants and associate alerts with the correct person. This is critical because every downstream module is person-scoped. If identity switches occur, the fall detector, gait history, and anomaly history become mixed across people and produce incorrect alerts.
third_party/wifi-sensing/vendor/wifi-radar/README.md:451:Falls are detected from motion, posture change, and recovery state, then surfaced in both the dashboard and REST API event stream. The detector is a finite state machine (FSM), which was chosen because it is interpretable and easy to calibrate for different environments.
third_party/wifi-sensing/vendor/wifi-radar/README.md:477:| Body angle | Distinguishes bending from falling | Many bend events become false alerts |
third_party/wifi-sensing/vendor/wifi-radar/README.md:478:| Height drop ratio | Confirms meaningful posture collapse | High-motion events over-trigger |
third_party/wifi-sensing/vendor/wifi-radar/README.md:481:> This is an engineering fall risk detector, not a medical certified fall diagnosis system.
third_party/wifi-sensing/vendor/wifi-radar/README.md:487:The system estimates cadence, stride, symmetry, and walking-speed proxies from the rolling pose stream for continuous mobility monitoring. It uses ankle trajectory minima as step events because foot strike naturally appears as a local minimum in ankle height.
third_party/wifi-sensing/vendor/wifi-radar/README.md:504:| Stride length proxy | distance between same-foot strikes | Works without explicit floor plane model |
third_party/wifi-sensing/vendor/wifi-radar/README.md:515:Unusual gait changes are flagged using rolling statistics and lightweight outlier detection to provide an early warning signal. The detector combines robust z-score checks with an optional IsolationForest model for multi-feature anomalies.
third_party/wifi-sensing/vendor/wifi-radar/README.md:537:A recent addition combines CSI motion evidence, pose confidence, and gait signals into a more robust live activity estimate for walking, stationary, high-motion, transition, and possible-fall states. This module improves stability when one modality briefly drops in quality.
third_party/wifi-sensing/vendor/wifi-radar/README.md:545:Final risk is produced from fused motion, pose reliability, gait context, and geometry factor:
third_party/wifi-sensing/vendor/wifi-radar/README.md:551:where $p$ is pose reliability, $g$ is gait context, and $q$ is layout quality metadata.
third_party/wifi-sensing/vendor/wifi-radar/README.md:555:  A[CSI amplitude and phase deltas] --> B[Windowed motion scores]
third_party/wifi-sensing/vendor/wifi-radar/README.md:569:| Multi-window motion | Captures both short and sustained movement | One-frame spikes and dropouts |
third_party/wifi-sensing/vendor/wifi-radar/README.md:571:| Gait context term | Anchors classification to mobility pattern | Mislabeling fast transitions |
third_party/wifi-sensing/vendor/wifi-radar/README.md:581:WiFi-Radar can now run without the dashboard for embedded or service-style integrations. In headless mode, the processing pipeline continues to ingest CSI, run inference, and publish events and metrics to FastAPI. This pattern is useful for integrations such as smart-home controllers, backend analytics pipelines, and edge gateways where a browser dashboard is not required.
third_party/wifi-sensing/vendor/wifi-radar/README.md:599:| Method | Endpoint | Purpose | Typical response fields |
third_party/wifi-sensing/vendor/wifi-radar/README.md:608:| `GET` | `/events` | Recent fall and anomaly events | `events` |
third_party/wifi-sensing/vendor/wifi-radar/README.md:639:python scripts/train_transfer_learning.py data/real_world/*.npz \
third_party/wifi-sensing/vendor/wifi-radar/README.md:650:## ONNX Export
third_party/wifi-sensing/vendor/wifi-radar/README.md:652:Export both models for edge deployment with a single command:
third_party/wifi-sensing/vendor/wifi-radar/README.md:660:# → weights/pose_estimator.onnx
third_party/wifi-sensing/vendor/wifi-radar/README.md:669:The exported models use **opset 17** and include **dynamic batch axes**, making
third_party/wifi-sensing/vendor/wifi-radar/README.md:670:them suitable for Jetson Nano, Raspberry Pi 4 with ONNX Runtime, or any
third_party/wifi-sensing/vendor/wifi-radar/README.md:671:ONNX-compatible inference engine.
third_party/wifi-sensing/vendor/wifi-radar/README.md:686:TensorRT engine plans from the exported ONNX models using **trtexec**.
third_party/wifi-sensing/vendor/wifi-radar/README.md:708:docker compose -f docker/docker-compose.yml up --build
third_party/wifi-sensing/vendor/wifi-radar/README.md:750:  max people, RTMP URL, stream FPS, fall-detection thresholds
third_party/wifi-sensing/vendor/wifi-radar/README.md:764:│       │   ├── fall_detector.py
third_party/wifi-sensing/vendor/wifi-radar/README.md:772:│       ├── models/
third_party/wifi-sensing/vendor/wifi-radar/README.md:775:│       │   └── pose_estimator.py
third_party/wifi-sensing/vendor/wifi-radar/README.md:782:│       │   └── model_io.py
third_party/wifi-sensing/vendor/wifi-radar/README.md:789:│   ├── train_simulation_baseline.py
third_party/wifi-sensing/vendor/wifi-radar/README.md:790:│   └── train_transfer_learning.py
third_party/wifi-sensing/vendor/wifi-radar/README.md:836:python scripts/train_simulation_baseline.py
third_party/wifi-sensing/vendor/wifi-radar/README.md:839:python scripts/train_transfer_learning.py data/real_world/*.npz
third_party/wifi-sensing/vendor/wifi-radar/README.md:866:- LSTM pose estimator (17 keypoints, 3-D) with multi-person tracking
third_party/wifi-sensing/vendor/wifi-radar/README.md:870:- ONNX export with onnxruntime validation
third_party/wifi-sensing/vendor/wifi-radar/README.md:872:- Simulation-baseline training script
third_party/wifi-sensing/vendor/wifi-radar/README.md:899:- [x] Pre-trained model weights (simulation baseline)
third_party/wifi-sensing/vendor/wifi-radar/README.md:900:- [x] Multi-person pose clustering
third_party/wifi-sensing/vendor/wifi-radar/README.md:902:- [x] ONNX export for edge deployment
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:3:"""Fine-tune WiFi-Radar models on real-world CSI datasets stored as NPZ files."""
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:24:from wifi_radar.models.encoder import DualBranchEncoder
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:25:from wifi_radar.models.pose_estimator import PoseEstimator
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:26:from wifi_radar.utils.model_io import load_checkpoint, save_checkpoint
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:44:            raise ValueError("No training samples found in the provided dataset files")
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:77:    train_size = len(dataset) - val_size
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:78:    train_ds, val_ds = random_split(dataset, [train_size, val_size])
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:79:    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:84:    pose_estimator = PoseEstimator().to(device)
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:87:        load_checkpoint(encoder, pose_estimator, args.weights, device=device)
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:101:            {"params": pose_estimator.parameters(), "lr": args.lr_head},
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:107:        encoder.train()
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:108:        pose_estimator.train()
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:109:        train_loss = 0.0
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:110:        for amp, phase, kp, conf in train_loader:
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:114:            pred_kp, pred_conf, _ = pose_estimator(features, hidden=None)
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:117:            torch.nn.utils.clip_grad_norm_(list(encoder.parameters()) + list(pose_estimator.parameters()), 1.0)
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:119:            train_loss += float(loss.item())
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:122:        pose_estimator.eval()
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:128:                pred_kp, pred_conf, _ = pose_estimator(features, hidden=None)
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:132:        train_loss /= max(1, len(train_loader))
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:134:        log.info("epoch=%03d train_loss=%.4f val_loss=%.4f freeze_encoder=%s", epoch + 1, train_loss, val_loss, freeze_encoder)
third_party/wifi-sensing/vendor/wifi-radar/scripts/train_transfer_learning.py:140:                pose_estimator,
third_party/wifi-sensing/vendor/wifi-radar/scripts/__init__.py:4:Purpose: Allow scripts (export_onnx.py, train_simulation_baseline.py) to import
third_party/wifi-sensing/vendor/wifi-radar/scripts/__init__.py:9:References: scripts/export_onnx.py, scripts/train_simulation_baseline.py.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:3:ID: WR-SCRIPT-ONNX-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:4:Purpose: Export DualBranchEncoder and PoseEstimator to ONNX format for
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:6:         outputs match the PyTorch reference implementation.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:10:    weights/pose_estimator.onnx  — 256-d features → 17 keypoints + confidence
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:28:from wifi_radar.models.encoder import DualBranchEncoder
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:29:from wifi_radar.models.pose_estimator import PoseEstimator
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:30:from wifi_radar.utils.model_io import load_checkpoint
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:37:# Wrapper: strip LSTM hidden state so ONNX sees simple I/O                    #
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:41:    """Thin wrapper that exposes DualBranchEncoder as a simple 2-input ONNX graph.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:43:    ID: WR-SCRIPT-ONNX-ENCWRAP-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:46:    Purpose: Prevent ONNX trace errors caused by tuple inputs or internal state;
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:47:             provides a clean interface for edge runtime inference.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:51:        encoder — DualBranchEncoder: trained encoder instance.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:66:    Constraints:
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:71:        DualBranchEncoder; WR-SCRIPT-ONNX-001.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:77:        ID: WR-SCRIPT-ONNX-ENCWRAP-INIT-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:79:        Purpose: Register the encoder as a sub-module so its parameters are
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:80:                 included in the ONNX export.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:84:            encoder — DualBranchEncoder: trained encoder.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:95:        Constraints: None.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:97:        References: torch.nn.Module.__init__; WR-SCRIPT-ONNX-ENCWRAP-001.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:105:        ID: WR-SCRIPT-ONNX-ENCWRAP-FWD-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:107:        Purpose: Provide a clean 2-input ONNX graph node for the encoder.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:115:            self.encoder must be in eval mode before ONNX export.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:122:        Constraints: None.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:124:        References: DualBranchEncoder.forward; WR-SCRIPT-ONNX-ENCWRAP-001.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:130:    """Single-frame (no sequence) pose estimator — hides the LSTM hidden state.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:132:    ID: WR-SCRIPT-ONNX-POSEWRAP-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:135:    Purpose: Strip the LSTM hidden state tuple from the return value because
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:136:             ONNX does not support optional tuple outputs natively.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:138:               ONNX output tensors without needing sequence-level state.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:140:        pose_estimator — PoseEstimator: trained estimator instance.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:155:    Constraints:
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:158:        Unit test: instantiate wrapper; assert wrapper.pe is pose_estimator.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:160:        PoseEstimator; WR-SCRIPT-ONNX-001.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:163:    def __init__(self, pose_estimator: PoseEstimator) -> None:
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:164:        """Initialise the pose estimator wrapper.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:166:        ID: WR-SCRIPT-ONNX-POSEWRAP-INIT-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:167:        Requirement: Call super().__init__() and store pose_estimator as self.pe.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:168:        Purpose: Register the pose estimator as a sub-module for ONNX parameter export.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:171:            pose_estimator — PoseEstimator: trained estimator.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:179:        Constraints: None.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:181:        References: torch.nn.Module.__init__; WR-SCRIPT-ONNX-POSEWRAP-001.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:184:        self.pe = pose_estimator
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:187:        """Run the pose estimator forward pass, discarding hidden state.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:189:        ID: WR-SCRIPT-ONNX-POSEWRAP-FWD-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:192:        Purpose: Provide a clean single-input ONNX graph node.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:193:        Rationale: Discarding the hidden state tuple makes the ONNX graph
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:201:            self.pe must be in eval mode before ONNX export.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:208:        Constraints: None.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:210:        References: PoseEstimator.forward; WR-SCRIPT-ONNX-POSEWRAP-001.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:226:    """Export DualBranchEncoder to ONNX format.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:228:    ID: WR-SCRIPT-ONNX-EXPENC-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:230:                 write an ONNX model file to output_path.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:231:    Purpose: Produce a portable ONNX graph for edge deployment without a PyTorch
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:236:        encoder     — DualBranchEncoder: trained model in eval mode.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:238:        opset       — int >=17: ONNX opset version.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:241:        None — writes ONNX file to output_path.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:246:        output_path file exists and is a valid ONNX model.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:257:    Constraints:
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:260:        Integration test: export and load with onnx.load; check_model passes.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:262:        torch.onnx.export; WR-SCRIPT-ONNX-001.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:264:    model.eval()
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:270:        model,
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:287:def export_pose_estimator(
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:288:    pose_estimator: PoseEstimator,
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:293:    """Export PoseEstimator (single-frame, no LSTM hidden state) to ONNX.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:295:    ID: WR-SCRIPT-ONNX-EXPPOSE-001
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:297:                 and write an ONNX model file to output_path.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:298:    Purpose: Produce an ONNX pose estimator graph suitable for edge deployment.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:299:    Rationale: _PoseEstimatorWrapper strips the LSTM hidden state so the ONNX
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:302:        pose_estimator — PoseEstimator: trained model in eval mode.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:304:        opset          — int: ONNX opset version.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:307:        None — writes ONNX file to output_path.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:309:        pose_estimator.eval() must have been called.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:311:        output_path file exists and is a valid ONNX model.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:321:    Constraints:
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:324:        Integration test: export and load with onnx.load; check_model passes.
third_party/wifi-sensing/vendor/wifi-radar/scripts/export_onnx.py:326:        _PoseEstimatorWrapper; torch.onnx.export; WR-SCRIPT-ONNX-001.
```

## Recommended GhostEye Implementation Direction

1. Use RuView scripts as the first backend/server/UDP bridge reference.
2. Use esp-csi as the first live CSI capture hardware reference.
3. Use wifi-radar and WiFi-CSI-Sensing-Benchmark as inference references.
4. Use wifi-densepose as a high-end pose-estimation research reference, not the first production dependency.
5. Treat TP-Link routers as the controlled WiFi environment first, not the CSI data source, unless a specific TP-Link/OpenWrt/CSI path is proven.
6. Build GhostEye-owned adapter code outside third_party.

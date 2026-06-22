const state = {
  backendUrl: localStorage.getItem("ghosteyeBackendUrl") || "http://localhost:8000",
  connected: false,
  scanTimer: null,
};

const $ = (id) => document.getElementById(id);

function setStatus(text, className = "") {
  const status = $("connectionStatus");
  status.textContent = text;
  status.className = `status-pill ${className}`.trim();
}

function apiUrl(path) {
  return `${state.backendUrl.replace(/\/$/, "")}${path}`;
}

async function fetchJson(path, options = {}) {
  const response = await fetch(apiUrl(path), {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`${path} failed with ${response.status}`);
  }
  return response.json();
}

async function connectBackend() {
  state.backendUrl = $("backendUrl").value.trim() || "http://localhost:8000";
  localStorage.setItem("ghosteyeBackendUrl", state.backendUrl);
  setStatus("Connecting");

  try {
    await fetchJson("/health");
    state.connected = true;
    setStatus("Online", "online");
    await refreshSources();
    await runScan();
    await refreshSession();
    if (!state.scanTimer) {
      state.scanTimer = setInterval(runScan, 3000);
    }
  } catch (error) {
    state.connected = false;
    setStatus("Backend offline", "offline");
    $("presence").textContent = "Backend not connected";
    $("timestamp").textContent = "Start FastAPI at the configured backend URL.";
  }
}

async function refreshSources() {
  const data = await fetchJson("/sources");
  const selected = data.selected_source || {};
  const vendor = (data.vendor_hint || selected.vendor_hint || "unknown").toLowerCase();

  $("selectedSource").textContent = selected.id || "--";
  $("liveAvailable").textContent = data.live_available ? "yes" : "no";
  $("currentSsid").textContent = data.current_ssid || selected.current_ssid || selected.selected_wifi_ssid || "--";
  $("confidenceCeiling").textContent = formatNumber(data.confidence_ceiling, 2);

  const badge = $("vendorBadge");
  badge.textContent = vendor === "tp_link" ? "TP-Link" : vendor === "netgear" ? "NetGear" : "Unknown";
  badge.className = `badge ${vendor}`;
}

async function runScan() {
  if (!state.connected) {
    return;
  }

  try {
    const data = await fetchJson("/scan");
    renderScan(data);
    await refreshSession();
    setStatus("Online", "online");
  } catch (error) {
    setStatus("Scan failed", "offline");
  }
}

function renderScan(data) {
  $("presence").textContent = titleize(data.presence || "unknown");
  $("motionScore").textContent = formatNumber(data.motion_score, 2);
  $("zone").textContent = (data.zone || "unknown").toUpperCase();
  $("confidence").textContent = formatNumber(data.confidence, 2);
  $("timestamp").textContent = data.timestamp || "No timestamp";

  const network = data.selected_network || {};
  $("currentSsid").textContent = network.ssid || $("currentSsid").textContent || "--";

  renderMap(data.map || {});
  renderSignalQuality(data.signal_quality || {});
  renderAiAnalysis(data.ai_analysis || {});
}

function renderMap(map) {
  setZoneScore("dotZoneA", map.zone_a);
  setZoneScore("dotZoneB", map.zone_b);
  setZoneScore("dotZoneC", map.zone_c);
}

function setZoneScore(id, rawScore) {
  const score = Math.max(0, Math.min(1, Number(rawScore || 0)));
  const el = $(id);
  el.style.setProperty("--score", score.toFixed(2));
  el.style.setProperty("--scale", (0.82 + score * 0.75).toFixed(2));
  el.style.background = `rgba(105, 240, 255, ${0.10 + score * 0.45})`;
  el.title = `${id.replace("dot", "")}: ${score.toFixed(2)}`;
}

function renderSignalQuality(quality) {
  $("rssi").textContent = quality.rssi_dbm == null ? "--" : `${formatNumber(quality.rssi_dbm, 1)} dBm`;
  $("noise").textContent = quality.noise_dbm == null ? "--" : `${formatNumber(quality.noise_dbm, 1)} dBm`;
  $("latency").textContent = `${formatNumber(quality.gateway_latency_ms, 1)} ms`;
  $("jitter").textContent = `${formatNumber(quality.jitter_ms, 1)} ms`;
  $("packetLoss").textContent = `${formatNumber((quality.packet_loss || 0) * 100, 1)}%`;
  $("rssiStability").textContent = formatNumber(quality.rssi_stability, 2);
}

function renderAiAnalysis(ai) {
  $("aiSummary").textContent = ai.summary || "No AI analysis available.";
  $("aiConfidence").textContent = ai.confidence_explanation || "";
  $("aiAction").textContent = ai.recommended_next_action || "";

  const risks = $("aiRisks");
  risks.innerHTML = "";
  (ai.false_positive_risks || []).forEach((risk) => {
    const item = document.createElement("li");
    item.textContent = titleize(risk);
    risks.appendChild(item);
  });
}

async function calibrateEmptyRoom() {
  setCalibrationStatus("Collecting empty-room samples...");
  try {
    const data = await fetchJson("/calibrate/empty-room", { method: "POST", body: "{}" });
    setCalibrationStatus(`Baseline ${data.baseline_id} saved with ${data.sample_count} samples.`);
    await runScan();
  } catch (error) {
    setCalibrationStatus("Empty-room calibration failed.");
  }
}

async function calibrateZone(zone) {
  setCalibrationStatus(`Collecting samples for ${zone}...`);
  try {
    const data = await fetchJson("/calibrate/zone", {
      method: "POST",
      body: JSON.stringify({ zone, label: `one_person_${zone}` }),
    });
    setCalibrationStatus(`Fingerprint ${data.fingerprint_id} saved for ${zone}.`);
    await runScan();
  } catch (error) {
    setCalibrationStatus(`${zone} calibration failed.`);
  }
}

function setCalibrationStatus(text) {
  $("calibrationStatus").textContent = text;
}

async function refreshSession() {
  try {
    const data = await fetchJson("/session/latest");
    $("sessionLatest").textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    $("sessionLatest").textContent = "Session endpoint unavailable.";
  }
}

function titleize(value) {
  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatNumber(value, digits = 2) {
  const number = Number(value);
  if (!Number.isFinite(number)) {
    return "--";
  }
  return number.toFixed(digits);
}

function bindEvents() {
  $("backendUrl").value = state.backendUrl;
  $("connectButton").addEventListener("click", connectBackend);
  $("scanButton").addEventListener("click", runScan);
  $("emptyRoomButton").addEventListener("click", calibrateEmptyRoom);
  document.querySelectorAll("[data-zone]").forEach((button) => {
    button.addEventListener("click", () => calibrateZone(button.dataset.zone));
  });
}

bindEvents();
connectBackend();

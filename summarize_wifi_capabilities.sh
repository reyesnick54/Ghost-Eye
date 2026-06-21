#!/bin/bash

OUT="docs/architecture/ghosteye-capability-summary.md"

mkdir -p docs/architecture

echo "# GhostEye Capability Summary" > "$OUT"
echo "" >> "$OUT"
echo "This summary extracts implementation-relevant capabilities from the vendored WiFi sensing repositories." >> "$OUT"
echo "" >> "$OUT"

echo "## Repo Inventory" >> "$OUT"
echo "" >> "$OUT"
echo '```text' >> "$OUT"
find third_party/wifi-sensing/vendor -maxdepth 1 -type d | sort >> "$OUT"
echo '```' >> "$OUT"
echo "" >> "$OUT"

echo "## High-Value Runtime Scripts" >> "$OUT"
echo "" >> "$OUT"
echo '```text' >> "$OUT"
find third_party/wifi-sensing/vendor -type f \
  \( -name "*.py" -o -name "*.sh" -o -name "*.ino" -o -name "*.c" -o -name "*.cpp" \) \
  | grep -Ei "csi|udp|server|bridge|sensing|radar|pose|densepose|inference|model|train|run|esp32|router|stream|socket|onnx" \
  | sort >> "$OUT"
echo '```' >> "$OUT"
echo "" >> "$OUT"

echo "## Dependency Files" >> "$OUT"
echo "" >> "$OUT"
echo '```text' >> "$OUT"
find third_party/wifi-sensing/vendor -type f \
  \( -name "requirements*.txt" -o -name "pyproject.toml" -o -name "package.json" -o -name "setup.py" -o -name "environment*.yml" -o -name "CMakeLists.txt" -o -name "idf_component.yml" \) \
  | sort >> "$OUT"
echo '```' >> "$OUT"
echo "" >> "$OUT"

echo "## CSI / Router / ESP32 Hits" >> "$OUT"
echo "" >> "$OUT"
echo '```text' >> "$OUT"
grep -RInE "CSI|Channel State|ESP32|router|TP-Link|OpenWrt|UDP|socket|stream" third_party/wifi-sensing/vendor \
  --include="*.md" --include="*.py" --include="*.txt" --include="*.json" \
  2>/dev/null | head -250 >> "$OUT"
echo '```' >> "$OUT"
echo "" >> "$OUT"

echo "## Inference / Model Hits" >> "$OUT"
echo "" >> "$OUT"
echo '```text' >> "$OUT"
grep -RInE "model|inference|train|predict|pose|presence|motion|activity|gesture|fall|breath|heart|localization|classification|ONNX|PyTorch|TensorFlow" third_party/wifi-sensing/vendor \
  --include="*.md" --include="*.py" --include="*.txt" --include="*.json" \
  2>/dev/null | head -250 >> "$OUT"
echo '```' >> "$OUT"
echo "" >> "$OUT"

echo "## Recommended GhostEye Implementation Direction" >> "$OUT"
echo "" >> "$OUT"
echo "1. Use RuView scripts as the first backend/server/UDP bridge reference." >> "$OUT"
echo "2. Use esp-csi as the first live CSI capture hardware reference." >> "$OUT"
echo "3. Use wifi-radar and WiFi-CSI-Sensing-Benchmark as inference references." >> "$OUT"
echo "4. Use wifi-densepose as a high-end pose-estimation research reference, not the first production dependency." >> "$OUT"
echo "5. Treat TP-Link routers as the controlled WiFi environment first, not the CSI data source, unless a specific TP-Link/OpenWrt/CSI path is proven." >> "$OUT"
echo "6. Build GhostEye-owned adapter code outside third_party." >> "$OUT"

echo "Wrote $OUT"

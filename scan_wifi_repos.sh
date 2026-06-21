#!/bin/bash

ROOT="third_party/wifi-sensing/vendor"
OUT="docs/architecture/wifi-sensing-repo-capability-scan.md"

mkdir -p docs/architecture

echo "# GhostEye WiFi Sensing Repo Capability Scan" > "$OUT"
echo "" >> "$OUT"
echo "Generated from local vendored repositories." >> "$OUT"
echo "" >> "$OUT"

for repo in "$ROOT"/*; do
  if [ -d "$repo" ]; then
    name=$(basename "$repo")
    echo "## $name" >> "$OUT"
    echo "" >> "$OUT"

    echo "### Top-level files" >> "$OUT"
    echo '```text' >> "$OUT"
    find "$repo" -maxdepth 2 -type f | sed "s|$repo/||" | sort | head -80 >> "$OUT"
    echo '```' >> "$OUT"
    echo "" >> "$OUT"

    echo "### README preview" >> "$OUT"
    echo '```text' >> "$OUT"
    readme=$(find "$repo" -maxdepth 2 -iname "README*" | head -1)
    if [ -n "$readme" ]; then
      sed -n '1,120p' "$readme" >> "$OUT"
    else
      echo "No README found in first two levels." >> "$OUT"
    fi
    echo '```' >> "$OUT"
    echo "" >> "$OUT"

    echo "### Dependency indicators" >> "$OUT"
    echo '```text' >> "$OUT"
    find "$repo" -maxdepth 4 -type f \
      \( -name "requirements*.txt" -o -name "environment*.yml" -o -name "package.json" -o -name "pyproject.toml" -o -name "setup.py" -o -name "CMakeLists.txt" -o -name "idf_component.yml" \) \
      | sed "s|$repo/||" | sort >> "$OUT"
    echo '```' >> "$OUT"
    echo "" >> "$OUT"

    echo "### Capability keyword hits" >> "$OUT"
    echo '```text' >> "$OUT"
    grep -RInE "CSI|channel state|pose|presence|motion|fall|breath|heart|radar|ESP32|router|TP-Link|OpenWrt|inference|model|dataset|stream|socket|api|ROS" "$repo" \
      --include="*.md" --include="*.py" --include="*.txt" --include="*.json" --include="*.yml" --include="*.yaml" \
      2>/dev/null | head -120 >> "$OUT"
    echo '```' >> "$OUT"
    echo "" >> "$OUT"
  fi
done

echo "Wrote $OUT"

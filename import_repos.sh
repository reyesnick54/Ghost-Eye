#!/bin/bash
set -e

mkdir -p third_party/wifi-sensing/vendor

echo "Pulling Repo 1: RuView"
git clone https://github.com/ruvnet/RuView.git third_party/wifi-sensing/vendor/RuView

echo "Pulling Repo 2: wifi-densepose"
git clone https://github.com/yangsuzhou/wifi-densepose.git third_party/wifi-sensing/vendor/wifi-densepose

echo "Pulling Repo 3: esp-csi"
git clone https://github.com/espressif/esp-csi.git third_party/wifi-sensing/vendor/esp-csi

echo "Pulling Repo 4: wifi-radar"
git clone https://github.com/hkevin01/wifi-radar.git third_party/wifi-sensing/vendor/wifi-radar

echo "Pulling Repo 5: WiFi-CSI-Sensing-Benchmark"
git clone https://github.com/xyanchen/WiFi-CSI-Sensing-Benchmark.git third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark

echo "Pulling Repo 6: Awesome-WiFi-CSI-Sensing"
git clone https://github.com/NTUMARS/Awesome-WiFi-CSI-Sensing.git third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing

echo "Pulling Repo 7: Wi-PoseDataset"
git clone https://github.com/NjtechCVLab/Wi-PoseDataset.git third_party/wifi-sensing/vendor/Wi-PoseDataset

echo "Pulling Repo 8: WiROS"
git clone https://github.com/FreeLike76/WiROS.git third_party/wifi-sensing/vendor/WiROS

echo "Removing nested Git folders so everything becomes part of Ghost-Eye"

find third_party/wifi-sensing/vendor -name ".git" -type d -prune -exec rm -rf {} +

echo "Done pulling all 8 repos."

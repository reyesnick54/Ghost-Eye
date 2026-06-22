# Android WiFi Collector

## Native module

Path:

```text
apps/ghosteye-mobile/android/app/src/main/java/com/abraxas/ghosteye/GhostEyeWifiModule.kt
```

The module exposes these React Native promises:

- `getCurrentWifi()`
- `scanNearbyWifi(targetSsid, targetBssidMasked)`
- `getRttCapabilities()`
- `getDeviceMotion(sampleWindowMs)`

## Permissions

The app declares:

- `ACCESS_WIFI_STATE`
- `CHANGE_WIFI_STATE`
- `ACCESS_FINE_LOCATION`
- `NEARBY_WIFI_DEVICES`
- `INTERNET`
- `ACCESS_NETWORK_STATE`

WiFi metadata and scan results are guarded by runtime permission state. Permission
denial returns warning fields and reduced capability mode instead of crashing.

## `getCurrentWifi()`

Uses `WifiManager.connectionInfo` to return:

- `ssid`
- `bssid_masked`
- `rssi_dbm`
- `link_speed_mbps`
- `frequency_mhz`
- `wifi_standard` when Android exposes it
- `capability_mode`

BSSIDs are masked as `aa:bb:cc:xx:xx:xx`.

## `scanNearbyWifi()`

Uses `WifiManager.startScan()` and `scanResults` when permitted. Android scan
throttling or permission failure is reported through:

- `scan_throttled`
- `warnings`
- reduced or empty `access_points`

Returned AP fields:

- `ssid`
- `bssid_masked`
- `rssi_dbm`
- `level`
- `frequency_mhz`
- `capabilities`

`target_router_seen` is true when the selected SSID or masked BSSID appears in
the scan result set.

## WiFi RTT detection

`getRttCapabilities()` checks `PackageManager.FEATURE_WIFI_RTT` and
`WifiRttManager.isAvailable` on supported Android versions. RTT is advisory only;
normal GhostEye mobile operation does not require RTT.

## Device motion

`getDeviceMotion()` samples accelerometer and gyroscope magnitudes over a short
window and classifies:

- `stable`
- `moving`
- `unknown`

The classification is used to discount unstable scans. It is not used to claim
RF imaging or deterministic occupancy detection.

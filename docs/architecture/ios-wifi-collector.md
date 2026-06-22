# iOS WiFi Collector

## Native module

Path:

```text
apps/ghosteye-mobile/ios/GhostEyeWifiModule.swift
```

The module exposes the same React Native surface as Android:

- `getCurrentWifi()`
- `scanNearbyWifi(targetSsid, targetBssidMasked)`
- `getRttCapabilities()`
- `getDeviceMotion(sampleWindowMs)`

## Capability mode

iOS runs in:

```text
ios_network_limited
```

This mode exists because public iOS APIs do not expose arbitrary nearby WiFi
scanning or raw CSI to normal apps.

## `getCurrentWifi()`

The module attempts to read current network data through public APIs:

- `NEHotspotNetwork.fetchCurrent` on supported iOS versions.
- `CNCopyCurrentNetworkInfo` as a compatibility fallback.

Returned fields are limited to what iOS makes available:

- `ssid`
- `bssid_masked`
- `normalized_signal_strength` when available
- `capability_mode: ios_network_limited`

If permissions, entitlements, or OS privacy rules hide WiFi metadata, fields are
left empty and warnings explain the limitation.

## Nearby scan and RTT

`scanNearbyWifi()` returns an empty scan with a capability warning. `getRttCapabilities()`
returns unsupported/not-required state. Neither method claims CSI, RF imaging, or
router-level ranging access.

## Device motion

Core Motion samples accelerometer and gyroscope values over a short bounded window
and returns:

- `stable`
- `moving`
- `unknown`

Motion classification helps the cloud interpret whether a phone was stationary
during a WiFi/network observation.

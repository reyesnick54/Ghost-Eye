import CoreMotion
import Foundation
import NetworkExtension
import React
import SystemConfiguration.CaptiveNetwork

@objc(GhostEyeWifiModule)
class GhostEyeWifiModule: NSObject {
  private let motionManager = CMMotionManager()

  @objc
  static func requiresMainQueueSetup() -> Bool {
    return false
  }

  @objc(getCurrentWifi:rejecter:)
  func getCurrentWifi(
    _ resolve: @escaping RCTPromiseResolveBlock,
    rejecter reject: @escaping RCTPromiseRejectBlock
  ) {
    if #available(iOS 14.0, *) {
      NEHotspotNetwork.fetchCurrent { network in
        var payload: [String: Any] = [
          "capability_mode": "ios_network_limited",
          "warnings": [
            "iOS exposes limited WiFi metadata only when app permissions and entitlements allow it.",
            "iOS public APIs do not expose raw CSI or nearby WiFi scans to this module."
          ]
        ]

        if let network = network {
          payload["ssid"] = network.ssid
          payload["bssid_masked"] = self.maskBssid(network.bssid)
          payload["normalized_signal_strength"] = network.signalStrength
        } else if let captive = self.currentCaptiveNetworkInfo() {
          payload["ssid"] = captive["SSID"] as? String
          payload["bssid_masked"] = self.maskBssid(captive["BSSID"] as? String)
        }

        resolve(payload)
      }
      return
    }

    var payload: [String: Any] = [
      "capability_mode": "ios_network_limited",
      "warnings": [
        "iOS exposes limited WiFi metadata only when app permissions allow it.",
        "iOS public APIs do not expose raw CSI or nearby WiFi scans to this module."
      ]
    ]
    if let captive = currentCaptiveNetworkInfo() {
      payload["ssid"] = captive["SSID"] as? String
      payload["bssid_masked"] = maskBssid(captive["BSSID"] as? String)
    }
    resolve(payload)
  }

  @objc(scanNearbyWifi:targetBssidMasked:resolver:rejecter:)
  func scanNearbyWifi(
    _ targetSsid: String?,
    targetBssidMasked: String?,
    resolver resolve: @escaping RCTPromiseResolveBlock,
    rejecter reject: @escaping RCTPromiseRejectBlock
  ) {
    resolve([
      "visible_access_points": 0,
      "target_router_seen": false,
      "access_points": [],
      "capability_mode": "ios_network_limited",
      "scan_throttled": false,
      "warnings": [
        "iOS public APIs do not permit arbitrary nearby WiFi scanning for this app layer."
      ]
    ])
  }

  @objc(getRttCapabilities:rejecter:)
  func getRttCapabilities(
    _ resolve: @escaping RCTPromiseResolveBlock,
    rejecter reject: @escaping RCTPromiseRejectBlock
  ) {
    resolve([
      "rtt_supported": false,
      "rtt_available": false,
      "rtt_permission_state": "not_required",
      "capability_mode": "ios_network_limited",
      "warnings": [
        "WiFi RTT is not exposed through iOS public APIs for normal GhostEye mobile observations."
      ]
    ])
  }

  @objc(getDeviceMotion:resolver:rejecter:)
  func getDeviceMotion(
    _ sampleWindowMs: NSNumber,
    resolver resolve: @escaping RCTPromiseResolveBlock,
    rejecter reject: @escaping RCTPromiseRejectBlock
  ) {
    guard motionManager.isAccelerometerAvailable else {
      resolve([
        "state": "unknown",
        "confidence": 0.0,
        "capability_mode": "ios_network_limited",
        "warnings": ["Accelerometer is unavailable."]
      ])
      return
    }

    var accelMagnitudes: [Double] = []
    var gyroMagnitudes: [Double] = []
    let queue = OperationQueue()
    let windowSeconds = max(0.25, min(2.0, sampleWindowMs.doubleValue / 1000.0))
    var warnings: [String] = []

    motionManager.accelerometerUpdateInterval = 0.08
    motionManager.startAccelerometerUpdates(to: queue) { data, _ in
      guard let acceleration = data?.acceleration else {
        return
      }
      let magnitude = sqrt(
        pow(acceleration.x, 2.0) +
          pow(acceleration.y, 2.0) +
          pow(acceleration.z, 2.0)
      )
      accelMagnitudes.append(magnitude)
    }

    if motionManager.isGyroAvailable {
      motionManager.gyroUpdateInterval = 0.08
      motionManager.startGyroUpdates(to: queue) { data, _ in
        guard let rotation = data?.rotationRate else {
          return
        }
        let magnitude = sqrt(
          pow(rotation.x, 2.0) +
            pow(rotation.y, 2.0) +
            pow(rotation.z, 2.0)
        )
        gyroMagnitudes.append(magnitude)
      }
    } else {
      warnings.append("Gyroscope is unavailable; motion classification uses accelerometer only.")
    }

    DispatchQueue.main.asyncAfter(deadline: .now() + windowSeconds) {
      self.motionManager.stopAccelerometerUpdates()
      self.motionManager.stopGyroUpdates()

      let accelStd = self.standardDeviation(accelMagnitudes)
      let gyroStd = self.standardDeviation(gyroMagnitudes)
      let state = self.classifyMotion(accelStd: accelStd, gyroStd: gyroStd, sampleCount: accelMagnitudes.count)

      resolve([
        "state": state,
        "confidence": self.motionConfidence(
          state: state,
          accelStd: accelStd,
          gyroStd: gyroStd,
          sampleCount: accelMagnitudes.count
        ),
        "accelerometer_magnitude_std": accelStd,
        "gyroscope_magnitude_std": gyroStd,
        "sample_count": accelMagnitudes.count + gyroMagnitudes.count,
        "capability_mode": "ios_network_limited",
        "warnings": warnings
      ])
    }
  }

  private func currentCaptiveNetworkInfo() -> [String: Any]? {
    guard let interfaces = CNCopySupportedInterfaces() as? [String] else {
      return nil
    }
    for interface in interfaces {
      if let info = CNCopyCurrentNetworkInfo(interface as CFString) as? [String: Any] {
        return info
      }
    }
    return nil
  }

  private func maskBssid(_ bssid: String?) -> String? {
    guard let bssid = bssid, !bssid.isEmpty else {
      return nil
    }
    let parts = bssid.lowercased().split(separator: ":")
    guard parts.count == 6 else {
      return bssid.lowercased()
    }
    return "\(parts[0]):\(parts[1]):\(parts[2]):xx:xx:xx"
  }

  private func standardDeviation(_ values: [Double]) -> Double {
    guard values.count >= 2 else {
      return 0.0
    }
    let average = values.reduce(0.0, +) / Double(values.count)
    let variance = values.reduce(0.0) { sum, value in
      sum + pow(value - average, 2.0)
    } / Double(values.count)
    return sqrt(variance)
  }

  private func classifyMotion(accelStd: Double, gyroStd: Double, sampleCount: Int) -> String {
    if sampleCount < 4 {
      return "unknown"
    }
    if accelStd < 0.025 && gyroStd < 0.035 {
      return "stable"
    }
    if accelStd > 0.06 || gyroStd > 0.08 {
      return "moving"
    }
    return "unknown"
  }

  private func motionConfidence(state: String, accelStd: Double, gyroStd: Double, sampleCount: Int) -> Double {
    if state == "unknown" || sampleCount < 4 {
      return 0.25
    }
    let margin: Double
    if state == "stable" {
      margin = max(0.0, 0.06 - accelStd) + max(0.0, 0.08 - gyroStd)
    } else {
      margin = max(0.0, accelStd - 0.025) + max(0.0, gyroStd - 0.035)
    }
    return min(0.9, max(0.0, 0.45 + margin))
  }
}

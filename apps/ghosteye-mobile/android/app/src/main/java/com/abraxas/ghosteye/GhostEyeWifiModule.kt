package com.abraxas.ghosteye

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.net.wifi.ScanResult
import android.net.wifi.WifiInfo
import android.net.wifi.WifiManager
import android.net.wifi.rtt.WifiRttManager
import android.os.Build
import android.os.Handler
import android.os.Looper
import androidx.core.content.ContextCompat
import com.facebook.react.bridge.Arguments
import com.facebook.react.bridge.Promise
import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.bridge.ReactContextBaseJavaModule
import com.facebook.react.bridge.ReactMethod
import com.facebook.react.bridge.WritableArray
import com.facebook.react.bridge.WritableMap
import kotlin.math.pow
import kotlin.math.sqrt

class GhostEyeWifiModule(private val reactContext: ReactApplicationContext) :
  ReactContextBaseJavaModule(reactContext) {

  private val wifiManager: WifiManager?
    get() = reactContext.applicationContext.getSystemService(Context.WIFI_SERVICE) as? WifiManager

  override fun getName(): String = "GhostEyeWifiModule"

  @ReactMethod
  fun getCurrentWifi(promise: Promise) {
    val payload = Arguments.createMap()
    val warnings = Arguments.createArray()
    payload.putString("capability_mode", "android_wifi_observation")

    try {
      if (!hasWifiMetadataPermission()) {
        warnings.pushString("ACCESS_FINE_LOCATION/NEARBY_WIFI_DEVICES permission is required for full WiFi metadata.")
      }

      val info = wifiManager?.connectionInfo
      if (info == null) {
        warnings.pushString("WifiManager connectionInfo is unavailable.")
        payload.putArray("warnings", warnings)
        promise.resolve(payload)
        return
      }

      payload.putString("ssid", cleanSsid(info.ssid))
      payload.putString("bssid_masked", maskBssid(info.bssid))
      payload.putInt("rssi_dbm", info.rssi)
      payload.putInt("link_speed_mbps", info.linkSpeed)
      if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
        payload.putInt("frequency_mhz", info.frequency)
      }
      payload.putString("wifi_standard", wifiStandard(info))
      payload.putArray("warnings", warnings)
      promise.resolve(payload)
    } catch (error: SecurityException) {
      warnings.pushString("WiFi metadata permission denied: ${error.message}")
      payload.putString("capability_mode", "android_wifi_scan_limited")
      payload.putArray("warnings", warnings)
      promise.resolve(payload)
    } catch (error: Exception) {
      warnings.pushString("Current WiFi unavailable: ${error.message}")
      payload.putString("capability_mode", "android_wifi_scan_limited")
      payload.putArray("warnings", warnings)
      promise.resolve(payload)
    }
  }

  @ReactMethod
  fun scanNearbyWifi(targetSsid: String?, targetBssidMasked: String?, promise: Promise) {
    val payload = Arguments.createMap()
    val warnings = Arguments.createArray()
    val accessPoints = Arguments.createArray()
    payload.putString("capability_mode", "android_wifi_observation")

    try {
      val manager = wifiManager
      if (manager == null) {
        warnings.pushString("WifiManager is unavailable.")
        resolveScan(payload, accessPoints, warnings, false, true, promise)
        return
      }
      if (!hasWifiMetadataPermission()) {
        warnings.pushString("WiFi scan requires ACCESS_FINE_LOCATION and, on Android 13+, NEARBY_WIFI_DEVICES.")
        resolveScan(payload, accessPoints, warnings, false, false, promise)
        return
      }

      val started = try {
        @Suppress("DEPRECATION")
        manager.startScan()
      } catch (error: SecurityException) {
        warnings.pushString("WiFi scan permission denied: ${error.message}")
        false
      } catch (error: Exception) {
        warnings.pushString("WiFi scan start failed: ${error.message}")
        false
      }
      if (!started) {
        warnings.pushString("WiFi scan may be throttled or unavailable; returning last permitted scan results.")
      }

      val results = try {
        @Suppress("DEPRECATION")
        manager.scanResults ?: emptyList()
      } catch (error: SecurityException) {
        warnings.pushString("WiFi scan results permission denied: ${error.message}")
        emptyList()
      }

      var targetSeen = false
      for (result in results) {
        val item = accessPointMap(result)
        val masked = item.getString("bssid_masked")
        val ssid = item.getString("ssid")
        if ((targetBssidMasked != null && targetBssidMasked == masked) || (targetSsid != null && targetSsid == ssid)) {
          targetSeen = true
        }
        accessPoints.pushMap(item)
      }

      resolveScan(payload, accessPoints, warnings, targetSeen, !started, promise)
    } catch (error: Exception) {
      warnings.pushString("Nearby WiFi scan unavailable: ${error.message}")
      resolveScan(payload, accessPoints, warnings, false, true, promise)
    }
  }

  @ReactMethod
  fun getRttCapabilities(promise: Promise) {
    val payload = Arguments.createMap()
    val warnings = Arguments.createArray()
    val supported = reactContext.packageManager.hasSystemFeature(PackageManager.FEATURE_WIFI_RTT)
    val permissionGranted = hasWifiMetadataPermission()
    val available = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P && supported) {
      try {
        val manager = reactContext.getSystemService(Context.WIFI_RTT_RANGING_SERVICE) as? WifiRttManager
        manager?.isAvailable == true
      } catch (_: Exception) {
        false
      }
    } else {
      false
    }

    if (!supported) {
      warnings.pushString("WiFi RTT is not supported by this device.")
    }
    if (!permissionGranted) {
      warnings.pushString("WiFi RTT availability is limited until WiFi/location permissions are granted.")
    }

    payload.putBoolean("rtt_supported", supported)
    payload.putBoolean("rtt_available", available && permissionGranted)
    payload.putString("rtt_permission_state", if (permissionGranted) "granted" else "denied")
    payload.putString("capability_mode", "android_wifi_observation")
    payload.putArray("warnings", warnings)
    promise.resolve(payload)
  }

  @ReactMethod
  fun getDeviceMotion(sampleWindowMs: Int, promise: Promise) {
    val sensorManager = reactContext.getSystemService(Context.SENSOR_SERVICE) as? SensorManager
    val accelerometer = sensorManager?.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
    val gyroscope = sensorManager?.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
    val warnings = Arguments.createArray()

    if (sensorManager == null || accelerometer == null) {
      val payload = Arguments.createMap()
      warnings.pushString("Accelerometer is unavailable.")
      payload.putString("state", "unknown")
      payload.putDouble("confidence", 0.0)
      payload.putString("capability_mode", "android_wifi_observation")
      payload.putArray("warnings", warnings)
      promise.resolve(payload)
      return
    }

    val accelMagnitudes = mutableListOf<Double>()
    val gyroMagnitudes = mutableListOf<Double>()
    val handler = Handler(Looper.getMainLooper())
    val listener = object : SensorEventListener {
      override fun onSensorChanged(event: SensorEvent) {
        val magnitude = sqrt(
          event.values[0].toDouble().pow(2.0) +
            event.values[1].toDouble().pow(2.0) +
            event.values[2].toDouble().pow(2.0)
        )
        if (event.sensor.type == Sensor.TYPE_ACCELEROMETER) {
          accelMagnitudes.add(magnitude)
        } else if (event.sensor.type == Sensor.TYPE_GYROSCOPE) {
          gyroMagnitudes.add(magnitude)
        }
      }

      override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) = Unit
    }

    sensorManager.registerListener(listener, accelerometer, SensorManager.SENSOR_DELAY_UI)
    if (gyroscope != null) {
      sensorManager.registerListener(listener, gyroscope, SensorManager.SENSOR_DELAY_UI)
    } else {
      warnings.pushString("Gyroscope is unavailable; motion classification uses accelerometer only.")
    }

    val boundedWindow = sampleWindowMs.coerceIn(250, 2000).toLong()
    handler.postDelayed({
      sensorManager.unregisterListener(listener)
      val accelStd = standardDeviation(accelMagnitudes)
      val gyroStd = standardDeviation(gyroMagnitudes)
      val state = classifyMotion(accelStd, gyroStd, accelMagnitudes.size)
      val payload = Arguments.createMap()
      payload.putString("state", state)
      payload.putDouble("confidence", motionConfidence(state, accelStd, gyroStd, accelMagnitudes.size))
      payload.putDouble("accelerometer_magnitude_std", accelStd)
      payload.putDouble("gyroscope_magnitude_std", gyroStd)
      payload.putInt("sample_count", accelMagnitudes.size + gyroMagnitudes.size)
      payload.putString("capability_mode", "android_wifi_observation")
      payload.putArray("warnings", warnings)
      promise.resolve(payload)
    }, boundedWindow)
  }

  private fun resolveScan(
    payload: WritableMap,
    accessPoints: WritableArray,
    warnings: WritableArray,
    targetSeen: Boolean,
    scanThrottled: Boolean,
    promise: Promise
  ) {
    payload.putInt("visible_access_points", accessPoints.size())
    payload.putBoolean("target_router_seen", targetSeen)
    payload.putArray("access_points", accessPoints)
    payload.putBoolean("scan_throttled", scanThrottled)
    payload.putArray("warnings", warnings)
    promise.resolve(payload)
  }

  private fun accessPointMap(result: ScanResult): WritableMap {
    val item = Arguments.createMap()
    item.putString("ssid", result.SSID)
    item.putString("bssid_masked", maskBssid(result.BSSID))
    item.putInt("rssi_dbm", result.level)
    item.putInt("level", result.level)
    item.putInt("frequency_mhz", result.frequency)
    item.putString("capabilities", result.capabilities)
    return item
  }

  private fun hasWifiMetadataPermission(): Boolean {
    val fineLocation = ContextCompat.checkSelfPermission(
      reactContext,
      Manifest.permission.ACCESS_FINE_LOCATION
    ) == PackageManager.PERMISSION_GRANTED
    val nearby = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
      ContextCompat.checkSelfPermission(
        reactContext,
        Manifest.permission.NEARBY_WIFI_DEVICES
      ) == PackageManager.PERMISSION_GRANTED
    } else {
      true
    }
    return fineLocation && nearby
  }

  private fun cleanSsid(ssid: String?): String? {
    if (ssid.isNullOrBlank() || ssid == WifiManager.UNKNOWN_SSID || ssid == "<unknown ssid>") {
      return null
    }
    return ssid.trim('"')
  }

  private fun maskBssid(bssid: String?): String? {
    if (bssid.isNullOrBlank() || bssid == "02:00:00:00:00:00") {
      return null
    }
    val parts = bssid.lowercase().split(":")
    if (parts.size != 6) {
      return bssid.lowercase()
    }
    return "${parts[0]}:${parts[1]}:${parts[2]}:xx:xx:xx"
  }

  private fun wifiStandard(info: WifiInfo): String? {
    if (Build.VERSION.SDK_INT < Build.VERSION_CODES.R) {
      return null
    }
    return when (info.wifiStandard) {
      ScanResult.WIFI_STANDARD_11AC -> "802.11ac"
      ScanResult.WIFI_STANDARD_11AX -> "802.11ax"
      ScanResult.WIFI_STANDARD_11N -> "802.11n"
      ScanResult.WIFI_STANDARD_11AD -> "802.11ad"
      ScanResult.WIFI_STANDARD_11BE -> "802.11be"
      ScanResult.WIFI_STANDARD_LEGACY -> "legacy"
      else -> "unknown"
    }
  }

  private fun standardDeviation(values: List<Double>): Double {
    if (values.size < 2) {
      return 0.0
    }
    val average = values.average()
    val variance = values.sumOf { (it - average).pow(2.0) } / values.size
    return sqrt(variance)
  }

  private fun classifyMotion(accelStd: Double, gyroStd: Double, sampleCount: Int): String {
    if (sampleCount < 4) {
      return "unknown"
    }
    if (accelStd < 0.08 && gyroStd < 0.04) {
      return "stable"
    }
    if (accelStd > 0.18 || gyroStd > 0.08) {
      return "moving"
    }
    return "unknown"
  }

  private fun motionConfidence(state: String, accelStd: Double, gyroStd: Double, sampleCount: Int): Double {
    if (state == "unknown" || sampleCount < 4) {
      return 0.25
    }
    val margin = if (state == "stable") {
      (0.18 - accelStd).coerceAtLeast(0.0) + (0.08 - gyroStd).coerceAtLeast(0.0)
    } else {
      (accelStd - 0.08).coerceAtLeast(0.0) + (gyroStd - 0.04).coerceAtLeast(0.0)
    }
    return (0.45 + margin).coerceIn(0.0, 0.9)
  }
}

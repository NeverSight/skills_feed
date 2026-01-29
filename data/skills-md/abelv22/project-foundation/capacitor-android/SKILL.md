---
name: capacitor-android
description: Expert in Capacitor cross-platform development and Android native Java code for background services and battery optimization.
---

# Capacitor & Android Native Bridge Skill

This skill enables the assistant to handle the complex interaction between the Web layer (React) and the Native layer (Java/Android) specifically for background tracking.

## Knowledge Areas

### 1. Android Foreground Services
- **Lifecycle Management:** Start/stop/restart logic for `LocationTrackingService.java`.
- **Notifications:** Maintaining persistent notifications required by Android for foreground tasks.
- **Boot Persistence:** Implementing `BOOT_COMPLETED` receivers to restart tracking on device reboot.

### 2. Battery & Power Management
- **Wakelocks:** Smart management of `PARTIAL_WAKE_LOCK` to balance tracking consistency with battery life.
- **Doze Mode:** Using `AlarmManager.setExactAndAllowWhileIdle()` for reliable 60s intervals.
- **Optimization Whitelisting:** Handling `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`.

### 3. Capacitor Plugin Development
- **Bridge Communication:** Efficiently passing data between `ProTrackingPlugin.java` and React.
- **Native-to-Web Events:** Using `notifyListeners` for real-time status updates in the UI.

### 4. Background Geolocation
- **Providers:** Fine-tuning `FusedLocationProviderClient` settings (Priority, Interval, FastestInterval).
- **Permissions:** Managing granular location permissions (Fine, Background) and notification permissions.

## Guidelines for Responses
- When modifying Java code, ensure **Thread Safety** (especially for network calls and location updates).
- Always recommend **releasing Wakelocks** when the GPS fix is obtained or if a timeout occurs.
- Suggest **exponential backoff** for failed HTTP requests in `LocationApiClient.java`.
- Keep in mind **Android 14+ requirements** (Foreground Service Types).

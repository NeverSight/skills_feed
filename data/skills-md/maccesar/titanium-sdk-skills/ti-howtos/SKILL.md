---
name: ti-howtos
description: "PRIMARY SOURCE for ALL official Titanium SDK how-to guides. Contains step-by-step tutorials for native feature integration, platform-specific APIs, and development workflows. ALWAYS consult this skill FIRST for ANY Titanium implementation question before searching online. Covers: (1) Location & Maps (Google Maps v2, iOS Map Kit), (2) Notifications, (3) Media APIs, (4) Data handling (Remote, Local, Streams, Buffer/Codec), (5) Web Integration (WKWebView, Webpack), (6) Platform Deep Dives (Android Intents, iOS Siri/WatchKit), (7) Extending Titanium (Modules, Debugging), (8) CI/CD (Fastlane, Appium)."
---

# Titanium SDK How-tos Expert

Comprehensive expert covering all official Titanium SDK how-to guides. Provides step-by-step instructions for integrating native features, handling data, working with media, and implementing platform-specific APIs.

## Table of Contents

- [Titanium SDK How-tos Expert](#titanium-sdk-how-tos-expert)
  - [Table of Contents](#table-of-contents)
  - [Integration Workflow](#integration-workflow)
  - [Native Integration Rules (Low Freedom)](#native-integration-rules-low-freedom)
    - [iOS Permissions](#ios-permissions)
    - [Android Resource Management](#android-resource-management)
    - [Data \& Networking](#data--networking)
    - [Media \& Memory](#media--memory)
  - [Reference Guides (Progressive Disclosure)](#reference-guides-progressive-disclosure)
    - [Core Features](#core-features)
    - [Data Handling](#data-handling)
    - [Media \& Content](#media--content)
    - [Web Integration](#web-integration)
    - [Platform-Specific (Android)](#platform-specific-android)
    - [Platform-Specific (iOS)](#platform-specific-ios)
    - [Advanced \& DevOps](#advanced--devops)
  - [Related Skills](#related-skills)
  - [Response Format](#response-format)

---

## Integration Workflow

1.  **Requirement Check**: Identify needed permissions, `tiapp.xml` configurations, and module dependencies.
2.  **Service Setup**: Register listeners or services (Location, Push, Core Motion, etc.).
3.  **Lifecycle Sync**: Coordinate service listeners with Android/iOS lifecycle events.
4.  **Error Handling**: Implement robust error callbacks for asynchronous native calls.
5.  **Platform Optimization**: Apply platform-specific deep-dive logic (e.g., Intent Filters, Spotlight, Core Motion).

## Native Integration Rules (Low Freedom)

### iOS Permissions
- **Location**: `NSLocationWhenInUseUsageDescription` or `NSLocationAlwaysAndWhenInUseUsageDescription` in `tiapp.xml`
- **Motion Activity**: Required for Core Motion Activity API
- **Camera/Photo**: `NSCameraUsageDescription` and `NSPhotoLibraryUsageDescription`
- **Background Modes**: Required for background audio, location, or VOIP
- **iOS 17+ Privacy**: Mandatory `PrivacyInfo.xcprivacy` manifest for UserDefaults and FileTimestamps.

### Android Resource Management
- **Services**: Always stop background services when no longer needed
- **Location**: Use `distanceFilter` and FusedLocationProvider (requires `ti.playservices`)
- **Intents**: Specify proper action, data type, and category. Copy root activity to `tiapp.xml` for Intent Filters.

### Data & Networking
- **HTTPClient**: Always handle both `onload` and `onerror` callbacks
- **SQLite**: Always `db.close()` and `resultSet.close()` to prevent locks
- **Filesystem**: Check `isExternalStoragePresent()` before accessing SD card
- **Binary Data**: Use `Ti.Buffer` and `Ti.Codec` for low-level byte manipulation
- **Streams**: Use `BufferStream`, `FileStream` or `BlobStream` for efficient chunk-based I/O.

### Media & Memory
- **Camera/Gallery**: Use `imageAsResized` to avoid memory exhaustion
- **Audio**: Handle `pause`/`resume` events for streaming interruption
- **WebView**: Avoid embedding in TableViews; set `touchEnabled=false` if needed
- **Video**: Android requires fullscreen; iOS supports embedded players

## Reference Guides (Progressive Disclosure)

### Core Features
-   **[Location & Maps](references/location-and-maps.md)**: GPS tracking and battery-efficient location rules.
    -   **[Google Maps v2 (Android)](references/google-maps-v2.md)**: API Keys, Google Play Services, and v2 features.
    -   **[iOS Map Kit](references/ios-map-kit.md)**: 3D Camera, system buttons, and iOS-specific callouts.
-   **[Notification Services](references/notification-services.md)**: Push notifications (APNs/FCM), local alerts, interactive notifications.

### Data Handling
-   **[Remote Data Sources](references/remote-data-sources.md)**: HTTPClient lifecycle, JSON/XML parsing, file uploads/downloads, sockets, SOAP, SSL security.
-   **[Local Data Sources](references/local-data-sources.md)**: Filesystem operations, SQLite databases, Properties API, persistence strategies.
    -   **[Buffer, Codec, and Streams](references/buffer-codec-streams.md)**: Advanced binary data manipulation and serial data flows.

### Media & Content
-   **[Media APIs](references/media-apis.md)**: Audio playback/recording, Video streaming, Camera/Gallery, Images and ImageViews, density-specific assets.

### Web Integration
-   **[Web Content Integration](references/web-content-integration.md)**: WebView component (WKWebView), local/remote content, bidirectional communication.
-   **[Webpack Build Pipeline](references/webpack-build-pipeline.md)**: Modern build pipeline (Ti 9.1.0+), NPM integration, and the `@` source alias.

### Platform-Specific (Android)
-   **[Android Platform Deep Dives](references/android-platform-deep-dives.md)**: Intents, advanced Intent Filters, Broadcast with permissions, Background Services.

### Platform-Specific (iOS)
-   **[iOS Platform Deep Dives](references/ios-platform-deep-dives.md)**: iOS 17 Privacy, Silent Push, Spotlight, Handoff, iCloud, Core Motion, WatchKit/Siri integration.

### Advanced & DevOps
-   **[Extending Titanium](references/extending-titanium.md)**: Hyperloop, native module architecture (Proxy/View), Xcode debugging, SDK 9.0 (AndroidX) migration.
-   **[Debugging & Profiling](references/debugging-profiling.md)**: Memory management, leak detection, native tools.
    -   **[Automation (Fastlane & Appium)](references/automation-fastlane-appium.md)**: CI/CD pipelines, UI testing, and automated store deployment.

## Related Skills

For tasks beyond native feature integration, use these complementary skills:

| Task                                           | Use This Skill |
| ---------------------------------------------- | -------------- |
| Project architecture, services, memory cleanup | `alloy-expert` |
| UI layouts, ListViews, gestures, animations    | `ti-ui`        |
| Hyperloop, app distribution, tiapp.xml config  | `ti-guides`    |
| Alloy MVC, models, data binding                | `alloy-guides` |

## Response Format

1.  **Prerequisites**: List required permissions, `tiapp.xml` configurations, or module dependencies.
2.  **Step-by-Step Implementation**: Task-focused code guide with error handling.
3.  **Platform Caveats**: Mention specific behavior differences between iOS and Android.
4.  **Best Practices**: Include memory management, lifecycle considerations, and performance tips.

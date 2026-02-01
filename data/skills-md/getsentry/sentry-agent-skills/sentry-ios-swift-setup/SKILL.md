---
name: sentry-ios-swift-setup
description: Setup Sentry in iOS/Swift apps. Use when asked to add Sentry to iOS, install sentry-cocoa SDK, or configure error monitoring for iOS applications using Swift and SwiftUI.
---

# Sentry iOS Swift Setup

Install and configure Sentry in iOS projects using Swift and SwiftUI.

## Invoke This Skill When

- User asks to "add Sentry to iOS" or "install Sentry" in a Swift app
- User wants error monitoring, tracing, or session replay in iOS
- User mentions "sentry-cocoa" or iOS crash reporting

## Requirements

- iOS 13.0+
- Xcode 15.0+
- Swift 5.0+

## Install

### Swift Package Manager (Recommended)

1. File > Add Package Dependencies
2. Enter: `https://github.com/getsentry/sentry-cocoa`
3. Select version rule: "Up to Next Major" from `9.0.0`

### CocoaPods

```ruby
# Podfile
pod 'Sentry', '~> 9.0'
```

Then run `pod install`.

## Configure

### SwiftUI App

```swift
import SwiftUI
import Sentry

@main
struct YourApp: App {
    init() {
        SentrySDK.start { options in
            options.dsn = "YOUR_SENTRY_DSN"
            options.debug = true
            
            // Tracing
            options.tracesSampleRate = 1.0
            
            // Profiling
            options.configureProfiling = {
                $0.sessionSampleRate = 1.0
                $0.lifecycle = .trace
            }
            
            // Session Replay
            options.sessionReplay.sessionSampleRate = 1.0
            options.sessionReplay.onErrorSampleRate = 1.0
            
            // Logs
            options.enableLogs = true
            
            // Error context
            options.attachScreenshot = true
            options.attachViewHierarchy = true
        }
    }
    
    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```

### UIKit App

```swift
import UIKit
import Sentry

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        SentrySDK.start { options in
            options.dsn = "YOUR_SENTRY_DSN"
            options.debug = true
            options.tracesSampleRate = 1.0
            options.enableLogs = true
        }
        return true
    }
}
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `dsn` | Sentry DSN | Required |
| `tracesSampleRate` | % of transactions traced | `0` |
| `sessionReplay.sessionSampleRate` | % of sessions replayed | `0` |
| `sessionReplay.onErrorSampleRate` | % of error sessions replayed | `0` |
| `enableLogs` | Send logs to Sentry | `false` |
| `attachScreenshot` | Attach screenshot on error | `false` |
| `attachViewHierarchy` | Attach view hierarchy on error | `false` |

## Auto-Instrumented Features

| Feature | What's Captured |
|---------|-----------------|
| App Launches | Cold/warm start times |
| Network | URLSession requests |
| UI | Screen loads, transitions |
| File I/O | Read/write operations |
| Core Data | Fetch/save operations |
| App Hangs | Main thread blocking |

## Logging

```swift
let logger = SentrySDK.logger

logger.info("User action", attributes: [
    "userId": "123",
    "action": "checkout"
])

// Log levels: trace, debug, info, warn, error, fatal
```

## Session Replay Masking

```swift
// SwiftUI modifiers
Text("Safe content").sentryReplayUnmask()
Text(user.email).sentryReplayMask()

// Debug masking in development
#if DEBUG
SentrySDK.replay.showMaskPreview()
#endif
```

## User Context

```swift
let user = User()
user.userId = "user_123"
user.email = "user@example.com"
SentrySDK.setUser(user)

// Clear on logout
SentrySDK.setUser(nil)
```

## Verification

```swift
// Test error capture
SentrySDK.capture(message: "Test from iOS")

// Test crash (dev only)
SentrySDK.crash()
```

## Production Settings

```swift
SentrySDK.start { options in
    options.dsn = "YOUR_SENTRY_DSN"
    options.debug = false
    options.tracesSampleRate = 0.2  // 20%
    options.sessionReplay.sessionSampleRate = 0.1  // 10%
    options.sessionReplay.onErrorSampleRate = 1.0  // 100% on error
    options.enableLogs = true
}
```

## Size Analysis (Fastlane)

Track app bundle size with Sentry using the Fastlane plugin.

### Install Plugin

```ruby
# fastlane/Pluginfile
gem 'fastlane-plugin-sentry'
```

Then run `bundle install`.

### Configure Authentication

```bash
# Environment variable (recommended for CI)
export SENTRY_AUTH_TOKEN=your_token_here
```

Or create `.sentryclirc` (add to `.gitignore`):

```ini
[auth]
token=YOUR_SENTRY_AUTH_TOKEN
```

### Fastfile Lane

```ruby
lane :sentry_size do
  build_app(
    scheme: "YourApp",
    configuration: "Release",
    export_method: "app-store"
  )

  sentry_upload_build(
    org_slug: "your-org",
    project_slug: "your-project",
    build_configuration: "Release"
  )
end
```

### Run Size Analysis

```bash
bundle exec fastlane sentry_size
```

View results in Sentry: **Settings > Size Analysis**

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Check DSN, enable `debug = true` |
| No traces | Set `tracesSampleRate` > 0 |
| No replays | Set `sessionSampleRate` > 0, check SDK 8.0+ |
| No logs | Set `enableLogs = true`, check SDK 8.55+ |
| CocoaPods fails | Run `pod repo update`, check iOS 13+ target |
| Size upload fails | Check `SENTRY_AUTH_TOKEN`, verify org/project slugs |

---
name: swift-ios-basics
description: Build iOS applications - project setup, app lifecycle, Info.plist, capabilities
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 02-swift-ios
bond_type: PRIMARY_BOND
---

# iOS Basics Skill

Foundation knowledge for iOS application development including project setup, app lifecycle, and configuration.

## Prerequisites

- Xcode 15+ installed
- Apple Developer account (for device testing)
- macOS Sonoma or later recommended

## Parameters

```yaml
parameters:
  ios_deployment_target:
    type: string
    default: "15.0"
    description: Minimum iOS version supported
  device_family:
    type: array
    items: [iphone, ipad]
    default: [iphone, ipad]
  interface_style:
    type: string
    enum: [storyboard, programmatic, swiftui]
    default: programmatic
```

## Topics Covered

### App Lifecycle
| State | Description | Callback |
|-------|-------------|----------|
| Not Running | App not launched | - |
| Inactive | Transitioning | `sceneWillResignActive` |
| Active | Running in foreground | `sceneDidBecomeActive` |
| Background | Running in background | `sceneDidEnterBackground` |
| Suspended | In memory, not executing | - |

### Project Structure
```
MyApp/
├── MyApp.xcodeproj
├── MyApp/
│   ├── App/
│   │   ├── AppDelegate.swift
│   │   ├── SceneDelegate.swift
│   │   └── Info.plist
│   ├── Features/
│   │   └── Home/
│   │       ├── HomeViewController.swift
│   │       └── HomeViewModel.swift
│   ├── Core/
│   │   ├── Extensions/
│   │   ├── Utilities/
│   │   └── Services/
│   └── Resources/
│       ├── Assets.xcassets
│       └── LaunchScreen.storyboard
└── MyAppTests/
```

### Info.plist Keys
| Key | Purpose | Required |
|-----|---------|----------|
| `CFBundleDisplayName` | App name shown to user | Yes |
| `CFBundleIdentifier` | Unique app identifier | Yes |
| `UILaunchStoryboardName` | Launch screen | Yes |
| `NSCameraUsageDescription` | Camera permission | If using camera |
| `NSPhotoLibraryUsageDescription` | Photo library permission | If accessing photos |
| `UIBackgroundModes` | Background capabilities | If running in background |

## Code Examples

### SceneDelegate Setup (iOS 13+)
```swift
class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?
    private var appCoordinator: AppCoordinator?

    func scene(_ scene: UIScene,
               willConnectTo session: UISceneSession,
               options connectionOptions: UIScene.ConnectionOptions) {

        guard let windowScene = scene as? UIWindowScene else { return }

        let window = UIWindow(windowScene: windowScene)
        let navigationController = UINavigationController()

        appCoordinator = AppCoordinator(navigationController: navigationController)
        appCoordinator?.start()

        window.rootViewController = navigationController
        window.makeKeyAndVisible()
        self.window = window
    }

    func sceneDidEnterBackground(_ scene: UIScene) {
        // Save state, release resources
        CoreDataStack.shared.saveContext()
    }

    func sceneWillEnterForeground(_ scene: UIScene) {
        // Refresh data if needed
        NotificationCenter.default.post(name: .appWillEnterForeground, object: nil)
    }
}
```

### Permission Request Pattern
```swift
import AVFoundation
import Photos

final class PermissionManager {
    static let shared = PermissionManager()

    func requestCameraPermission() async -> Bool {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            return true
        case .notDetermined:
            return await AVCaptureDevice.requestAccess(for: .video)
        case .denied, .restricted:
            return false
        @unknown default:
            return false
        }
    }

    func requestPhotoLibraryPermission() async -> Bool {
        let status = PHPhotoLibrary.authorizationStatus(for: .readWrite)

        switch status {
        case .authorized, .limited:
            return true
        case .notDetermined:
            let newStatus = await PHPhotoLibrary.requestAuthorization(for: .readWrite)
            return newStatus == .authorized || newStatus == .limited
        case .denied, .restricted:
            return false
        @unknown default:
            return false
        }
    }

    func openSettings() {
        guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
        UIApplication.shared.open(url)
    }
}
```

### Background Task Handling
```swift
import BackgroundTasks

final class BackgroundTaskManager {
    static let shared = BackgroundTaskManager()

    private let refreshTaskId = "com.app.refresh"
    private let processingTaskId = "com.app.processing"

    func registerTasks() {
        BGTaskScheduler.shared.register(forTaskWithIdentifier: refreshTaskId, using: nil) { task in
            self.handleAppRefresh(task: task as! BGAppRefreshTask)
        }

        BGTaskScheduler.shared.register(forTaskWithIdentifier: processingTaskId, using: nil) { task in
            self.handleProcessing(task: task as! BGProcessingTask)
        }
    }

    func scheduleRefresh() {
        let request = BGAppRefreshTaskRequest(identifier: refreshTaskId)
        request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60) // 15 min

        do {
            try BGTaskScheduler.shared.submit(request)
        } catch {
            Logger.background.error("Failed to schedule refresh: \(error)")
        }
    }

    private func handleAppRefresh(task: BGAppRefreshTask) {
        scheduleRefresh() // Reschedule

        let refreshTask = Task {
            do {
                try await DataSyncService.shared.syncAll()
                task.setTaskCompleted(success: true)
            } catch {
                task.setTaskCompleted(success: false)
            }
        }

        task.expirationHandler = {
            refreshTask.cancel()
        }
    }
}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Black screen on launch | Missing root VC | Set window.rootViewController |
| Permission dialog not showing | Already denied | Check status, guide to Settings |
| Background task not running | Not registered | Call register in didFinishLaunching |
| Launch image wrong size | Missing assets | Add all required sizes to LaunchScreen |

### Debug Tips
```bash
# Simulate background fetch
xcrun simctl spawn booted debug-background refresh com.app.bundleid

# Check app lifecycle in console
# Filter: subsystem:com.apple.UIKit category:Lifecycle

# Reset permissions
xcrun simctl privacy booted reset all com.app.bundleid
```

## Validation Rules

```yaml
validation:
  - rule: info_plist_usage_descriptions
    severity: error
    check: All permission usage descriptions must be non-empty
  - rule: launch_screen_required
    severity: error
    check: LaunchScreen.storyboard or launch screen in Info.plist
  - rule: supported_orientations
    severity: warning
    check: Define supported orientations for all device types
```

## Integration Patterns

```swift
// AppDelegate + SceneDelegate coordination
extension Notification.Name {
    static let appWillEnterForeground = Notification.Name("appWillEnterForeground")
    static let appDidBecomeActive = Notification.Name("appDidBecomeActive")
    static let userDidLogin = Notification.Name("userDidLogin")
}
```

## Usage

```
Skill("swift-ios-basics")
```

## Related Skills

- `swift-uikit` - UIKit components
- `swift-swiftui` - SwiftUI alternative
- `swift-testing` - Testing iOS apps

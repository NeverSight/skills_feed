---
name: push-notifications
description: "Expert notification decisions for iOS/tvOS: when to request permission, silent vs visible notification trade-offs, rich notification strategies, and APNs architecture choices. Use when implementing push notifications, debugging delivery issues, or designing notification UX. Trigger keywords: push notification, UNUserNotificationCenter, APNs, device token, silent notification, content-available, mutable-content, notification extension, notification actions, badge"
version: "3.0.0"
---

# Push Notifications — Expert Decisions

Expert decision frameworks for notification choices. Claude knows UNUserNotificationCenter and APNs — this skill provides judgment calls for permission timing, delivery strategies, and architecture trade-offs.

---

## Decision Trees

### Permission Request Timing

```
When should you ask for notification permission?
├─ User explicitly wants notifications
│  └─ After user taps "Enable Notifications" button
│     Highest acceptance rate (70-80%)
│
├─ After demonstrating value
│  └─ After user completes key action
│     "Get notified when your order ships?"
│     Context-specific, 50-60% acceptance
│
├─ First meaningful moment
│  └─ After onboarding, before home screen
│     Explain why, 30-40% acceptance
│
└─ On app launch
   └─ AVOID — lowest acceptance (15-20%)
      No context, feels intrusive
```

**The trap**: Requesting permission on first launch. Users deny reflexively. Wait for a moment when notifications clearly add value.

### Silent vs Visible Notification

```
What's the notification purpose?
├─ Background data sync
│  └─ Silent notification (content-available: 1)
│     No user interruption, wakes app
│
├─ User needs to know immediately
│  └─ Visible alert
│     Messages, time-sensitive info
│
├─ Informational, not urgent
│  └─ Badge + silent
│     User sees count, checks when ready
│
└─ Needs user action
   └─ Visible with actions
      Reply, accept/decline buttons
```

### Notification Extension Strategy

```
Do you need to modify notifications?
├─ Download images/media
│  └─ Notification Service Extension
│     mutable-content: 1 in payload
│
├─ Decrypt end-to-end encrypted content
│  └─ Notification Service Extension
│     Required for E2EE messaging
│
├─ Custom notification UI
│  └─ Notification Content Extension
│     Long-press/3D Touch custom view
│
└─ Standard text/badge
   └─ No extension needed
      Less complexity, faster delivery
```

### Token Management

```
How should you handle device tokens?
├─ Single device per user
│  └─ Replace token on registration
│     Simple, most apps need this
│
├─ Multiple devices per user
│  └─ Register all tokens
│     Send to all active devices
│
├─ Token changed (reinstall/restore)
│  └─ Deduplicate on server
│     Same device, new token
│
└─ User logged out
   └─ Deregister token from user
      Prevents notifications to wrong user
```

---

## NEVER Do

### Permission Handling

**NEVER** request permission without context:
```swift
// ❌ First thing on app launch — user denies
func application(_ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { _, _ in }
    return true
}

// ✅ After user action that demonstrates value
func userTappedEnableNotifications() {
    showPrePermissionExplanation {
        Task {
            let granted = try? await UNUserNotificationCenter.current()
                .requestAuthorization(options: [.alert, .badge, .sound])
            if granted == true {
                await MainActor.run { registerForRemoteNotifications() }
            }
        }
    }
}
```

**NEVER** ignore denied permission:
```swift
// ❌ Keeps trying, annoys user
func checkNotifications() {
    Task {
        let settings = await UNUserNotificationCenter.current().notificationSettings()
        if settings.authorizationStatus == .denied {
            // Ask again!  <- User already said no
            requestPermission()
        }
    }
}

// ✅ Respect denial, offer settings path
func checkNotifications() {
    Task {
        let settings = await UNUserNotificationCenter.current().notificationSettings()
        switch settings.authorizationStatus {
        case .denied:
            showSettingsPrompt()  // "Enable in Settings to receive..."
        case .notDetermined:
            showPrePermissionScreen()
        case .authorized, .provisional, .ephemeral:
            ensureRegistered()
        @unknown default:
            break
        }
    }
}
```

### Token Handling

**NEVER** cache device tokens long-term in app:
```swift
// ❌ Token may change without app knowing
class TokenManager {
    static var cachedToken: String?  // Stale after reinstall!

    func getToken() -> String? {
        return Self.cachedToken  // May be invalid
    }
}

// ✅ Always use fresh token from registration callback
func application(_ application: UIApplication,
    didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    let token = deviceToken.hexString

    // Send to server immediately — this is the source of truth
    Task {
        await sendTokenToServer(token)
    }
}
```

**NEVER** assume token format:
```swift
// ❌ Token format is not guaranteed
let tokenString = String(data: deviceToken, encoding: .utf8)  // Returns nil!

// ✅ Convert bytes to hex
extension Data {
    var hexString: String {
        map { String(format: "%02x", $0) }.joined()
    }
}

let tokenString = deviceToken.hexString
```

### Silent Notifications

**NEVER** rely on silent notifications for time-critical delivery:
```swift
// ❌ Silent notifications are low priority
// Server sends: {"aps": {"content-available": 1}}
// Expecting: Immediate delivery
// Reality: iOS may delay minutes/hours or drop entirely

// ✅ Use visible notification for time-critical content
// Or use silent for prefetch, visible for alert
{
    "aps": {
        "alert": {"title": "New Message", "body": "..."},
        "content-available": 1  // Also prefetch in background
    }
}
```

**NEVER** do heavy work in silent notification handler:
```swift
// ❌ System will kill your app
func application(_ application: UIApplication,
    didReceiveRemoteNotification userInfo: [AnyHashable: Any]) async -> UIBackgroundFetchResult {

    await downloadLargeFiles()  // Takes too long!
    await processAllData()       // iOS terminates app

    return .newData
}

// ✅ Quick fetch, defer heavy processing
func application(_ application: UIApplication,
    didReceiveRemoteNotification userInfo: [AnyHashable: Any]) async -> UIBackgroundFetchResult {

    // 30 seconds max — fetch metadata only
    do {
        let hasNew = try await checkForNewContent()
        if hasNew {
            scheduleBackgroundProcessing()  // BGProcessingTask
        }
        return hasNew ? .newData : .noData
    } catch {
        return .failed
    }
}
```

### Notification Service Extension

**NEVER** forget expiration handler:
```swift
// ❌ System shows unmodified notification
class NotificationService: UNNotificationServiceExtension {
    override func didReceive(_ request: UNNotificationRequest,
        withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void) {

        // Start async work...
        downloadImage { image in
            // Never called if timeout!
            contentHandler(modifiedContent)
        }
    }

    // Missing serviceExtensionTimeWillExpire!
}

// ✅ Always implement expiration handler
class NotificationService: UNNotificationServiceExtension {
    var contentHandler: ((UNNotificationContent) -> Void)?
    var bestAttemptContent: UNMutableNotificationContent?

    override func didReceive(_ request: UNNotificationRequest,
        withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void) {
        self.contentHandler = contentHandler
        bestAttemptContent = request.content.mutableCopy() as? UNMutableNotificationContent

        downloadImage { [weak self] image in
            guard let self, let content = self.bestAttemptContent else { return }
            if let image { content.attachments = [image] }
            contentHandler(content)
        }
    }

    override func serviceExtensionTimeWillExpire() {
        // Called ~30 seconds — deliver what you have
        if let content = bestAttemptContent {
            contentHandler?(content)
        }
    }
}
```

---

## Essential Patterns

### Permission Flow with Pre-Permission

```swift
@MainActor
final class NotificationPermissionManager: ObservableObject {
    @Published var status: UNAuthorizationStatus = .notDetermined

    func checkStatus() async {
        let settings = await UNUserNotificationCenter.current().notificationSettings()
        status = settings.authorizationStatus
    }

    func requestPermission() async -> Bool {
        do {
            let granted = try await UNUserNotificationCenter.current()
                .requestAuthorization(options: [.alert, .badge, .sound])

            if granted {
                UIApplication.shared.registerForRemoteNotifications()
            }

            await checkStatus()
            return granted
        } catch {
            return false
        }
    }

    func openSettings() {
        guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
        UIApplication.shared.open(url)
    }
}

// Pre-permission screen
struct NotificationPermissionView: View {
    @StateObject private var manager = NotificationPermissionManager()
    @State private var showSystemPrompt = false

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "bell.badge")
                .font(.system(size: 60))

            Text("Stay Updated")
                .font(.title)

            Text("Get notified about new messages, order updates, and important alerts.")
                .multilineTextAlignment(.center)

            Button("Enable Notifications") {
                Task { await manager.requestPermission() }
            }
            .buttonStyle(.borderedProminent)

            Button("Not Now") { dismiss() }
                .foregroundColor(.secondary)
        }
        .padding()
    }
}
```

### Notification Action Handler

```swift
@MainActor
final class NotificationHandler: NSObject, UNUserNotificationCenterDelegate {
    static let shared = NotificationHandler()

    private let router: DeepLinkRouter

    func userNotificationCenter(_ center: UNUserNotificationCenter,
        willPresent notification: UNNotification) async -> UNNotificationPresentationOptions {
        // App is in foreground
        let userInfo = notification.request.content.userInfo

        // Check if we should show banner or handle silently
        if shouldShowInForeground(userInfo) {
            return [.banner, .sound, .badge]
        } else {
            handleSilently(userInfo)
            return []
        }
    }

    func userNotificationCenter(_ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse) async {
        let userInfo = response.notification.request.content.userInfo

        switch response.actionIdentifier {
        case UNNotificationDefaultActionIdentifier:
            // User tapped notification
            await handleNotificationTap(userInfo)

        case "REPLY_ACTION":
            if let textResponse = response as? UNTextInputNotificationResponse {
                await handleReply(text: textResponse.userText, userInfo: userInfo)
            }

        case "MARK_READ_ACTION":
            await markAsRead(userInfo)

        case UNNotificationDismissActionIdentifier:
            // User dismissed
            break

        default:
            await handleCustomAction(response.actionIdentifier, userInfo: userInfo)
        }
    }

    private func handleNotificationTap(_ userInfo: [AnyHashable: Any]) async {
        guard let deepLink = userInfo["deep_link"] as? String,
              let url = URL(string: deepLink) else { return }

        await router.navigate(to: url)
    }
}
```

### Rich Notification Service

```swift
class NotificationService: UNNotificationServiceExtension {
    var contentHandler: ((UNNotificationContent) -> Void)?
    var bestAttemptContent: UNMutableNotificationContent?

    override func didReceive(_ request: UNNotificationRequest,
        withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void) {
        self.contentHandler = contentHandler
        bestAttemptContent = request.content.mutableCopy() as? UNMutableNotificationContent

        guard let content = bestAttemptContent else {
            contentHandler(request.content)
            return
        }

        Task {
            // Download and attach media
            if let mediaURL = request.content.userInfo["media_url"] as? String {
                if let attachment = await downloadAttachment(from: mediaURL) {
                    content.attachments = [attachment]
                }
            }

            // Decrypt if needed
            if let encrypted = request.content.userInfo["encrypted_body"] as? String {
                content.body = decrypt(encrypted)
            }

            contentHandler(content)
        }
    }

    override func serviceExtensionTimeWillExpire() {
        if let content = bestAttemptContent {
            contentHandler?(content)
        }
    }

    private func downloadAttachment(from urlString: String) async -> UNNotificationAttachment? {
        guard let url = URL(string: urlString) else { return nil }

        do {
            let (localURL, response) = try await URLSession.shared.download(from: url)

            let fileExtension = (response as? HTTPURLResponse)?
                .mimeType.flatMap { mimeToExtension[$0] } ?? "jpg"

            let destURL = FileManager.default.temporaryDirectory
                .appendingPathComponent(UUID().uuidString)
                .appendingPathExtension(fileExtension)

            try FileManager.default.moveItem(at: localURL, to: destURL)

            return try UNNotificationAttachment(identifier: "media", url: destURL)
        } catch {
            return nil
        }
    }
}
```

---

## Quick Reference

### Payload Structure

| Field | Purpose | Value |
|-------|---------|-------|
| alert | Visible notification | {title, subtitle, body} |
| badge | App icon badge | Number |
| sound | Notification sound | "default" or filename |
| content-available | Silent/background | 1 |
| mutable-content | Service extension | 1 |
| category | Action buttons | Category identifier |
| thread-id | Notification grouping | Thread identifier |

### Permission States

| Status | Meaning | Action |
|--------|---------|--------|
| notDetermined | Never asked | Show pre-permission |
| denied | User declined | Show settings prompt |
| authorized | Full access | Register for remote |
| provisional | Quiet delivery | Consider upgrade prompt |
| ephemeral | App clip temporary | Limited time |

### Extension Limits

| Extension | Time Limit | Use Case |
|-----------|------------|----------|
| Service Extension | ~30 seconds | Download media, decrypt |
| Content Extension | User interaction | Custom UI |
| Background fetch | ~30 seconds | Data refresh |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Permission on launch | Low acceptance | Wait for user action |
| Cached device token | May be stale | Always use callback |
| String(data:encoding:) for token | Returns nil | Use hex encoding |
| Silent for time-critical | May be delayed | Use visible notification |
| Heavy work in silent handler | App terminated | Quick fetch, defer work |
| No serviceExtensionTimeWillExpire | Unmodified content shown | Always implement |
| Ignoring denied status | Frustrates user | Offer settings path |

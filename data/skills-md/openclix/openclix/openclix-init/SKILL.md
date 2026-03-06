---
name: openclix-init
description: Integrate OpenClix by adding local client code templates into an existing mobile app with minimal edits, strict dependency reuse, and post-integration build verification.
---

# OpenClix Init

## Purpose

This skill adds OpenClix functionality by copying client code into the user project, not by installing an SDK package.  
Use a local-source integration model (shadcn-style): copy, adapt, wire, verify.

## Core Rules

- Detect the real platform first using project files.
- Prioritize minimal edits to existing user code.
- Keep all OpenClix files in a dedicated namespace/directory.
- When creating local planning/report artifacts under `.openclix/**`, ensure `.openclix/` is listed in `.gitignore` (add it if missing).
- Reuse existing dependencies whenever possible.
- Do not add or update dependencies without explicit user approval.
- Run a build after integration and fix only integration-caused issues.
- Do not use in-memory fallback in production integration paths.
- For bundled JSON config delivery, keep runtime loader path and copied file path identical (same directory + same case-sensitive filename).
- Use `openclix-config.json` as the default filename; do not invent case variants such as `OpenClix-config.json`.

## Platform Detection

Use file evidence in this order:

| Priority | Platform | Required Evidence |
|----------|----------|-------------------|
| 1 | Expo | `app.json` or `app.config.*` with `expo` |
| 2 | React Native | `package.json` with `react-native` and typical `ios/` + `android/` structure |
| 3 | Flutter | `pubspec.yaml` with Flutter SDK |
| 4 | iOS native | `*.xcodeproj` or `*.xcworkspace` or `Package.swift` |
| 5 | Android native | `build.gradle` or `build.gradle.kts` |

If signals conflict, trust concrete file evidence and report the mismatch.

## Template Selection

- Expo / React Native: `templates/react-native/`
- Flutter: `templates/flutter/`
- iOS: `templates/ios/`
- Android: `templates/android/` (package namespace `ai.openclix.*`)

`templates/react-native/` is the canonical reference when platform ports need alignment.

## Existing Local Notification Detection

Before copying templates or wiring OpenClix touchpoints, inspect the host app for pre-existing local notification code outside the OpenClix namespace.

Detection must cover these paths when they exist:

- notification scheduling
- notification permission request/status
- foreground display handling
- notification tap/open handling

For each detected path, classify it as either:

- `migration-capable`: can be redirected into OpenClix with localized edits, no new dependencies, and no broad refactor
- `keep-as-is`: should remain untouched during OpenClix integration

If no existing local notification code is found, continue with the normal integration flow.

If existing local notification code is found, report:

- the files or entry points detected
- whether each path is `migration-capable` or `keep-as-is`
- why any path is not migration-capable

## Migration Capability Rules

Use these rules conservatively:

- React Native / Expo:
  - `migration-capable` only when the app already uses `@notifee/react-native` or `expo-notifications`
  - detect and classify existing scheduler, permission, foreground, and open-handling code against those libraries
  - other notification stacks remain `keep-as-is`
- Flutter:
  - `migration-capable` only when the existing plugin can provide the current OpenClix callback contract for `schedule`, `cancel`, `listPending`, permission request/status, and optional foreground setup
  - if the plugin cannot satisfy that contract without adding dependencies or broad rewrites, mark it `keep-as-is`
- iOS native:
  - `migration-capable` when the app already uses `UNUserNotificationCenter` local notifications and the existing permission/delegate path can be reused with localized edits
  - preserve any unsupported notification behavior outside the OpenClix content model
- Android native:
  - `migration-capable` when the current local notification flow is platform-local scheduling/display that can be redirected into the OpenClix scheduler path without adding dependencies or broad refactors
  - vendor-owned or heavily customized flows remain `keep-as-is`

Always mark these scenarios as `keep-as-is` unless the user asks for a separate redesign:

- remote push delivery infrastructure
- vendor-specific notification products outside current OpenClix adapters
- rich actions or advanced features not represented by the current OpenClix content model
- notification flows tightly coupled to unrelated business logic

## Migration Decision

If one or more detected paths are `migration-capable`, ask the user before rewriting existing notification behavior.

Use this decision wording:

`I found existing local notifications outside OpenClix. Some paths are migration-capable. Do you want me to migrate the supported local-notification flows into OpenClix, or keep the existing implementation unchanged? If you do not choose, I will keep the existing implementation.`

Decision rules:

- default migration-capable paths to `keep-as-is` if the user does not explicitly choose
- if the user chooses `keep`, treat migration-capable paths as `keep-as-is`, integrate OpenClix alongside the current notification system, and do not rewrite existing notification flows
- if the user chooses `migrate`, migrate only supported engagement-style local notification flows that fit the current OpenClix model
- leave unsupported or unrelated notification flows untouched even when the user chooses `migrate`
- if no detected path is migration-capable, explain that and proceed with coexistence only
- never silently replace an existing notification implementation
- include the final user choice in the integration handoff/report

## Integration Workflow

1. Identify platform and current startup/event/lifecycle entry points.
2. Detect pre-existing local notification paths and classify them as `migration-capable` or `keep-as-is`.
3. If migration-capable paths exist, ask whether to migrate supported flows or keep the existing implementation unchanged. Default to keeping the existing implementation.
4. Copy the selected template into a dedicated OpenClix area in the user project.
5. Wire only required touchpoints:
   - initialization at app startup
   - event tracking call path
   - foreground/app lifecycle trigger
6. Keep existing architecture and code style intact; avoid broad refactors.
7. Validate against `references/openclix.schema.json` when config/schema changes are involved.

## Adapter Selection Rules

Select adapters using existing dependencies only:

1. Choose concrete adapters at integration time; avoid runtime dependency auto-detection.
2. If the project already has a supported persistent storage dependency, wire that implementation.
3. If notification libraries already exist, wire the matching scheduler adapter.
4. If no compatible dependency exists, fail fast with a clear integration error.
5. Keep degraded in-memory paths out of production template defaults.

React Native / Expo storage selection:

- AsyncStorage project: use `AsyncStorageCampaignStateRepository`.
- MMKV project: use `MmkvCampaignStateRepository`.
- If both exist, prefer the project standard and copy only one storage adapter into the app.
- Inject `campaignStateRepository` explicitly when calling `OpenClix.initialize(...)`.

React Native / Expo scheduler selection:

- Notifee project: create `new NotifeeScheduler(notifee)`.
- Expo notifications project: create `new ExpoNotificationScheduler(ExpoNotifications)`.
- Inject `messageScheduler` explicitly when calling `OpenClix.initialize(...)`.

Platform expectations:

- React Native / Expo:
  - Do not use runtime adapter auto-detection in `OpenClix` core for storage and scheduler adapters; select these at integration time.
  - Select storage/scheduler implementations during integration and inject their dependencies explicitly; lifecycle helpers (e.g., `lifecycleStateReader`) may be chosen by the template core based on the runtime environment when no project-specific implementation is required.
  - If compatible implementations are unavailable, initialization must fail with clear instructions.
- Flutter:
  - Use callback-based scheduler adapter for existing notification plugin
  - Require an explicit scheduler and state repository dependency at initialization
- iOS / Android native:
  - Use platform-native implementations by default
  - Do not introduce in-memory/no-op fallback as the default runtime behavior

## Notification Permission and Foreground Setup

Notification permission must be requested before campaign triggers fire. Each platform template includes a permission utility; the integration agent must wire it at the appropriate location in the host app.

### React Native / Expo — Permission

- **Notifee projects:** Import `requestNotifeePermission` from `infrastructure/NotifeeNotificationSetup`. Call it at app startup (e.g. in `App.tsx` or a startup hook) passing the Notifee adapter. No foreground handler is needed — Notifee handles foreground display natively via `presentationOptions`.
- **Expo projects:** Import `requestExpoPermission` and `setupExpoForegroundHandler` from `infrastructure/ExpoNotificationSetup`. Call `setupExpoForegroundHandler` once during initialization, then call `requestExpoPermission` at app startup.

### iOS — Permission and Foreground Display

1. **Permission:** Call `await NotificationPermission.request()` at app startup (e.g. in `application(_:didFinishLaunchingWithOptions:)` or a SwiftUI `.task` modifier). This calls `UNUserNotificationCenter.requestAuthorization`.
2. **Foreground display:** iOS suppresses notification banners when the app is active. The template provides `ForegroundNotificationHandler.handleWillPresent(notification:completionHandler:)` as a static method.
   - **Critical:** iOS allows only ONE `UNUserNotificationCenterDelegate` per app. Do NOT assign `ForegroundNotificationHandler` as the delegate. Instead, set the app's existing delegate (usually `AppDelegate`) as `UNUserNotificationCenter.current().delegate = self`, and call the static method from the delegate's `willPresent` implementation.

### Android — Permission

1. **Manifest:** Add `<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />` to `AndroidManifest.xml`.
2. **Runtime request:** On API 33+ (Android 13), call `NotificationPermission.shouldRequestPermission(context)` at startup. If it returns `true`, use the Activity's `requestPermissions()` or `ActivityResultLauncher` to request `NotificationPermission.getPermissionString()`.
3. Android does NOT need foreground display setup — `NotificationManager.notify()` always displays regardless of app state.

### Flutter — Permission and Foreground Display

The `NotificationPermission` class in `notification/notification_permission.dart` accepts callbacks. Wire the host app's notification plugin:

1. Provide a `requestPermission` callback that calls the plugin's permission request API.
2. Provide a `checkPermissionStatus` callback that checks current status.
3. Optionally provide a `setupForegroundHandler` callback to configure foreground display (required for iOS, not needed for Android).
4. Call `permission.request()` at app startup before campaign triggers fire.
5. Call `permission.setupForeground()` during initialization if the handler is provided.

## Directory and Namespace Policy

OpenClix files must stay grouped in a dedicated location:

- React Native / Expo: `src/openclix/`
- Flutter: `lib/openclix/`
- iOS: `OpenClix/` or `Sources/OpenClix/`
- Android: `app/src/main/kotlin/ai/openclix/` with `ai.openclix.*` packages

## Bundled Config Path Contract

When integration includes bundled config delivery (non-HTTP endpoint), enforce this contract:

1. Detect the exact runtime load path from current startup code first.
2. Copy `openclix-config.json` to that exact path.
3. If no runtime load path exists yet, use these defaults:
   - React Native / Expo: `assets/openclix/openclix-config.json`
   - Flutter: `assets/openclix/openclix-config.json` and add it to `pubspec.yaml`
   - iOS: `<app-target>/OpenClix/openclix-config.json` and include in "Copy Bundle Resources"
   - Android: `app/src/main/assets/openclix/openclix-config.json`
4. Ensure any bundled-path identifier (`OpenClixConfig.endpoint`, asset key, bundle filename) matches the copied file path exactly.
5. Run a final path parity check before handoff and report:
   - source config file path
   - bundled runtime file path
   - runtime loader reference location(s)

## Dependency Policy

Before changing dependencies:

1. Check what the selected template expects.
2. Check what the user project already has.
3. Prefer existing project libraries or platform APIs.
4. If replacement is possible, adapt template code instead of adding dependencies.
5. If no safe replacement exists, ask for approval before any dependency add/update.

Never run package-manager install/update commands without approval.

## Build Verification

After wiring, run platform-appropriate build/analysis commands based on detected project structure.
Prefer project-native commands first (existing scripts, Gradle tasks, Xcode scheme, Flutter workflow).

If unclear, use common fallback commands:

- React Native / Expo: `npx tsc --noEmit`
- Android: `./gradlew assembleDebug`
- iOS: `xcodebuild -scheme <scheme> build` or `swift build`
- Flutter: `flutter analyze`

If build fails, apply minimal targeted fixes and retry. Stop only on hard blockers.

## Completion Checklist

- OpenClix code added under dedicated namespace/directory.
- Existing app code changes are minimal and localized.
- Existing local notification paths detected and classified before integration.
- Migration decision recorded when supported paths were found; defaulted to preserving existing behavior when the user did not opt in.
- Handoff/report states what was detected, what was migration-capable, what stayed untouched, and what was changed.
- No unapproved dependency additions or upgrades.
- Adapter wiring prefers existing dependencies and fails fast when unavailable.
- Bundled config path/filename parity verified when using local resource delivery.
- Build verification executed.
- Any remaining blockers clearly reported.

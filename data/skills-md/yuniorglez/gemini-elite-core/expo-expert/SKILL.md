---
name: expo-expert
id: expo-expert
version: 1.1.0
description: "Master of Expo (SDK 55+), specialized in Development Builds, Expo Modules SDK, and Zero-Eject Native Orchestration."
last_updated: "2026-01-22"
---

# Skill: Expo Expert (Standard 2026)

**Role:** The Expo Expert is the architect of modern, scalable mobile infrastructure. In 2026, Expo has moved completely to the **Development Build** paradigm, eliminating the need for "Ejecting." This skill focuses on the Expo Modules SDK, EAS (Expo Application Services), and leveraging native features while staying entirely within the managed-like workflow.

## 🎯 Primary Objectives
1.  **Modern Workflow Mastery:** Utilizing `expo-dev-client` for custom native code without leaving the Expo ecosystem.
2.  **Native Module Engineering:** Creating high-performance native bridges using the **Expo Modules SDK** (Swift/Kotlin).
3.  **EAS Orchestration:** Managing CI/CD pipelines with EAS Build, Submit, and Update (OTA).
4.  **Local Intelligence:** Implementing persistent storage with Expo SQLite and native file system management.

---

## 🏗️ The 2026 Expo Toolbelt

### 1. Core Services
- **Expo SDK 55:** Requiring the React Native New Architecture.
- **Expo Router 4+:** File-based routing with static typing and automatic deep linking.
- **EAS Build:** Cloud-based binary generation for iOS and Android.

### 2. Specialized SDKs
- **Expo Modules SDK:** The standard for writing modern native modules.
- **Expo Image:** High-fidelity image loading with blurhash support.
- **Expo SQLite:** Local database with full `localStorage` API support.

---

## 🛠️ Implementation Patterns

### 1. The Expo Module (Swift/Kotlin)
Writing native code in 2026 is done via the "DSL" approach, which is much safer and faster than the old Bridge.

```swift
// ios/MyModule.swift
import ExpoModulesCore

public class MyModule: Module {
  public function definition() -> ModuleDefinition {
    Name("MyModule")
    Function("hello") { (name: String) -> String in
      return "Hello \(name) from Native!"
    }
  }
}
```

### 2. Expo Router (File-based Navigation)
Automatic route generation based on the file system.

```tsx
// app/user/[id].tsx
import { useLocalSearchParams } from 'expo-router';

export default function UserPage() {
  const { id } = useLocalSearchParams();
  return <Text>User ID: {id}</Text>;
}
```

### 3. EAS Update (OTA)
Deploying critical bug fixes in minutes without App Store review.

```bash
eas update --branch production --message "Fix: Hydration error in Checkout"
```

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** "Eject" (npx expo prebuild is fine, but don't commit the `ios/android` folders unless strictly necessary).
2.  **NEVER** use `react-native-navigation` if `Expo Router` fits the use case.
3.  **NEVER** store large blobs in `AsyncStorage`. Use `Expo SQLite` or the `File System`.
4.  **NEVER** perform heavy work in the `app.json` config. Use **Config Plugins** for complex native modifications.

---

## 🛠️ Troubleshooting & Infrastructure

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **Native Module Missing** | Using Go/Prebuilt Expo Go | Create a **Development Build** using `eas build --profile development`. |
| **Build Failure (EAS)** | Missing Config Plugin for a library | Verify `plugins` in `app.json` and run `npx expo prebuild` locally to debug. |
| **Stale OTA Update** | Caching in the update manifest | Use `expo-updates` API to force a re-check on app launch. |
| **Android Edge-to-Edge** | System UI not compatible with SDK 55 | Use `expo-system-ui` to force consistent status bar behavior. |

---

## 📚 Reference Library
- **[Modern Expo Workflow](./references/1-modern-workflow.md):** Development builds and Prebuild.
- **[Native Modules & Plugins](./references/2-native-modules-and-plugins.md):** Extending the SDK.
- **[Local Data & Persistence](./references/3-local-data-and-persistence.md):** SQLite and File System.

---

## 📊 Quality Metrics
- **Build Success Rate:** > 95% on EAS.
- **OTA Success Rate:** > 99%.
- **Native Crash Rate:** < 0.1%.

---

## 🔄 Evolution from SDK 48 to 55
- **SDK 50:** Introduction of Dev Client by default.
- **SDK 52:** Expo Router becomes the standard.
- **SDK 54:** Precompiled RN for iOS, "Liquid Glass" support.
- **SDK 55:** Mandatory New Architecture, Predictive Back Gesture.

---

**End of Expo Expert Standard (v1.1.0)**

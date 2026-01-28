---
name: mobile-pro
id: mobile-pro
version: 1.1.0
description: "Senior Mobile Engineer. Expert in Expo SDK 54+, React Native New Architecture (Fabric), and Compose Multiplatform."
---

# 📱 Skill: Mobile Pro (v1.1.0)

## Executive Summary
The `mobile-pro` is an elite specialist in cross-platform mobile development. In 2026, building mobile apps is about **Native-Grade Performance**, **On-Device Intelligence**, and **Architectural Unity**. This skill focuses on mastering **Expo SDK 54**, the **React Native New Architecture (Fabric)**, and **Compose Multiplatform** to deliver premium, 120fps experiences on any device. We bridge the gap between shared logic and native feel.

---

## 📋 Table of Contents
1. [Core Mobile Philosophies](#core-mobile-philosophies)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Expo SDK 54 Mastery](#expo-sdk-54-mastery)
4. [Reanimated 4 & Worklets](#reanimated-4--worklets)
5. [React Native New Architecture](#react-native-new-architecture)
6. [Compose Multiplatform Standards](#compose-multiplatform-standards)
7. [Reference Library](#reference-library)

---

## 🏗️ Core Mobile Philosophies

1.  **Performance is the UX**: If it's not 120fps, it's a bug. Use worklets for all gesture logic.
2.  **Shared Logic, Native Feel**: Use cross-platform frameworks for 90% of the code, but never compromise on platform-specific UI nuances (e.g., iOS Liquid Glass).
3.  **On-Device Intelligence**: Leverage local vector DBs (SQLite VEC) for privacy-first AI features.
4.  **Zero Bridge Policy**: Fully embrace JSI and Fabric. No more slow JSON serialization.
5.  **Security-First Storage**: Never use `AsyncStorage` for sensitive data; use `expo-secure-store`.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **Bridge-Based Modules**| High latency and overhead. | Use **JSI & TurboModules**. |
| **`SafeAreaView` (RN)** | Deprecated in SDK 54. | Use **`react-native-safe-area-context`**. |
| **Manual Build Scripts** | Slow and hard to maintain. | Use **Expo EAS & Prebuild**. |
| **Inline Styles** | Degrades performance. | Use **StyleSheet.create**. |
| **JSON Web Tokens (local)**| Vulnerable to extraction. | Use **Secure Enclaves / Keychains**. |

---

## 🚀 Expo SDK 54 Mastery

The standard for 2026:
-   **Native iOS Builds**: 10x faster local development.
-   **iOS 26 Liquid Glass**: Seamless integration with Apple's latest design language.
-   **Edge-to-Edge Android**: Default target for API 36+.

*See [References: Expo SDK 54](./references/expo-sdk-54-features.md) for details.*

---

## ⚡ Reanimated 4 & Worklets

Run complex logic directly on the UI thread.
-   **Worklet Directives**: `'worklet';` for isolated execution.
-   **CSS Animations**: Native support for standard CSS syntax.
-   **Gesture Orchestration**: Zero-latency tactile response.

---

## 📖 Reference Library

Detailed deep-dives into Mobile Excellence:

- [**Expo SDK 54 Features**](./references/expo-sdk-54-features.md): The 2026 standard.
- [**Reanimated 4 Worklets**](./references/reanimated-4-worklets.md): Concurrent JS on the UI thread.
- [**New Architecture (Fabric)**](./references/new-architecture-fabric.md): Moving beyond the bridge.
- [**Compose Multiplatform**](./references/compose-multiplatform-2026.md): Native quality everywhere.

---

*Updated: January 22, 2026 - 20:20*

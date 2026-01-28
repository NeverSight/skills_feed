---
name: software-mobile
description: Production-grade mobile app development with Swift (iOS), Kotlin (Android), React Native, and WebView patterns, including UI/UX, navigation, state management, networking, local storage, push notifications, and App Store deployment.
---

# Mobile Development Skill — Quick Reference

This skill equips mobile developers with execution-ready patterns for building native and cross-platform mobile applications. Claude should apply these patterns when users ask for iOS/Android app architecture, UI components, navigation flows, API integration, offline storage, authentication, or mobile-specific features.

---

# When to Use This Skill

Claude should invoke this skill when a user requests:

- iOS app development (Swift, SwiftUI, UIKit)
- Android app development (Kotlin, Jetpack Compose)
- Cross-platform development (React Native, WebView)
- Mobile app architecture and patterns
- Navigation and routing
- State management (Redux, MobX, MVVM)
- Network requests and API integration
- Local data storage (Core Data, Room, SQLite)
- Authentication and session management
- Push notifications
- Camera and media access
- Location services
- App Store / Play Store deployment
- Mobile performance optimization
- Offline-first architecture

---

## Quick Reference Table

| Task | iOS | Android | Cross-Platform | When to Use |
|------|-----|---------|----------------|-------------|
| Native UI | SwiftUI + UIKit | Jetpack Compose + Views | React Native | Native: Best performance; Cross-platform: Code sharing |
| Navigation | NavigationStack | Navigation Component | React Navigation | Platform-specific for native feel |
| State Management | @State/@Observable | ViewModel + StateFlow | Redux/MobX | iOS: @Observable; Android: ViewModel; RN: Redux |
| Networking | URLSession + async/await | Retrofit + Coroutines | Axios/Fetch | Native: Type-safe; RN: JavaScript ecosystem |
| Local Storage | Core Data + SwiftData | Room Database | AsyncStorage/SQLite | Native: Full control; RN: Simpler |
| Push Notifications | APNs | FCM | React Native Firebase | Native: Platform-specific; RN: Unified API |

## Decision Tree: Platform Selection

```text
Need to build mobile app for: [Target Audience]
    ├─ iOS only?
    │   └─ Use Swift + SwiftUI (templates/swift/)
    │
    ├─ Android only?
    │   └─ Use Kotlin + Jetpack Compose (templates/kotlin/)
    │
    ├─ Both iOS and Android?
    │   ├─ Need maximum performance?
    │   │   └─ Build separate native apps (Swift + Kotlin)
    │   │
    │   ├─ Need faster development + code sharing?
    │   │   └─ Use React Native (templates/cross-platform/)
    │   │
    │   └─ Wrapping existing web app?
    │       └─ Use WebView wrapper (templates/cross-platform/template-webview.md)
```

---

## Navigation

**Resources**
- [resources/ios-best-practices.md](resources/ios-best-practices.md) — iOS architecture, concurrency, testing, and performance
- [resources/android-best-practices.md](resources/android-best-practices.md) — Android/Kotlin architecture, coroutines, Compose, testing, performance
- [README.md](README.md) — Folder overview and usage notes
- [data/sources.json](data/sources.json) — Curated external references by platform

**Templates**
- Swift: [templates/swift/template-swift.md](templates/swift/template-swift.md), [templates/swift/template-swift-concurrency.md](templates/swift/template-swift-concurrency.md), [templates/swift/template-swift-combine.md](templates/swift/template-swift-combine.md), [templates/swift/template-swift-performance.md](templates/swift/template-swift-performance.md), [templates/swift/template-swift-testing.md](templates/swift/template-swift-testing.md)
- SwiftUI: [templates/swiftui/template-swiftui-advanced.md](templates/swiftui/template-swiftui-advanced.md)
- Kotlin/Android: [templates/kotlin/template-kotlin.md](templates/kotlin/template-kotlin.md), [templates/kotlin/template-kotlin-coroutines.md](templates/kotlin/template-kotlin-coroutines.md), [templates/kotlin/template-kotlin-compose-advanced.md](templates/kotlin/template-kotlin-compose-advanced.md), [templates/kotlin/template-kotlin-testing.md](templates/kotlin/template-kotlin-testing.md)
- Cross-platform: [templates/cross-platform/template-platform-patterns.md](templates/cross-platform/template-platform-patterns.md), [templates/cross-platform/template-webview.md](templates/cross-platform/template-webview.md)

**Related Skills**
- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) — Web-facing UI patterns and Next.js integration
- [../software-backend/SKILL.md](../software-backend/SKILL.md) — API design, auth, and backend contracts for mobile clients
- [../software-testing-automation/SKILL.md](../software-testing-automation/SKILL.md) — Mobile CI, test strategy, and reliability gates
- [../quality-resilience-patterns/SKILL.md](../quality-resilience-patterns/SKILL.md) — Resilience patterns for networked mobile apps

---

## Operational Playbooks
- [resources/operational-playbook.md](resources/operational-playbook.md) — Mobile architecture patterns, platform-specific guides, security notes, and decision tables

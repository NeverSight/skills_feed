---
# ═══════════════════════════════════════════════════════════════════════════
# SKILL: Mobile Development
# Version: 2.0.0 | Updated: 2025-01
# ═══════════════════════════════════════════════════════════════════════════
name: mobile-development
description: iOS (Swift, SwiftUI), Android (Kotlin, Compose), cross-platform (Flutter, React Native), and game development (Unity, Unreal).

# ACTIVATION TRIGGERS
triggers:
  - ios
  - android
  - flutter
  - react native
  - mobile
  - swift
  - kotlin
  - unity
  - game development

# SKILL PARAMETERS
parameters:
  platform:
    type: string
    enum: [ios, android, cross-platform, games]
    required: true
  project_type:
    type: string
    required: false
    description: Type of app (social, productivity, game, etc.)

# OUTPUT SPECIFICATION
outputs:
  recommended_stack:
    type: object
  learning_path:
    type: array
  portfolio_projects:
    type: array

# RELIABILITY
retry:
  max_attempts: 3
  backoff: exponential

# OBSERVABILITY
observability:
  log_level: info

level: advanced
prerequisites:
  - core-development

sasmp_version: "1.3.0"
bonded_agent: 01-core-paths
bond_type: PRIMARY_BOND
---

# Mobile Development Skill

## Quick Reference

| Platform | Language | Framework | Timeline | Job Market |
|----------|----------|-----------|----------|------------|
| **iOS** | Swift | SwiftUI | 6-9 mo | High |
| **Android** | Kotlin | Compose | 6-9 mo | High |
| **Cross-Platform** | Dart | Flutter | 4-6 mo | Growing |
| **Games** | C# | Unity | 12-24 mo | Moderate |

---

## Learning Paths

### iOS Development
```
[1] Swift Fundamentals (4-6 wk)
 │  └─ Types, optionals, closures, protocols
 │
 ▼
[2] SwiftUI (4-6 wk)
 │  └─ Views, modifiers, state, binding
 │
 ▼
[3] Navigation + Data (3-4 wk)
 │  └─ NavigationStack, SwiftData/Core Data
 │
 ▼
[4] Networking + Async (2-3 wk)
 │  └─ URLSession, async/await, Combine
 │
 ▼
[5] Testing + App Store (2 wk)
    └─ XCTest, TestFlight, submission
```

**2025 Stack:** Swift 5.10 + SwiftUI + SwiftData + Xcode 16

---

### Android Development
```
[1] Kotlin Fundamentals (4-6 wk)
 │  └─ Null safety, coroutines, data classes
 │
 ▼
[2] Jetpack Compose (4-6 wk)
 │  └─ Composables, state, effects
 │
 ▼
[3] Architecture (3-4 wk)
 │  └─ MVVM, Room, Navigation
 │
 ▼
[4] Networking + DI (2-3 wk)
 │  └─ Retrofit, Hilt, Flow
 │
 ▼
[5] Testing + Play Store (2 wk)
    └─ JUnit, Espresso, release
```

**2025 Stack:** Kotlin 2.0 + Jetpack Compose + Room + Hilt

---

### Flutter (Cross-Platform)
```
[1] Dart Fundamentals (2-3 wk)
 │
 ▼
[2] Flutter Widgets (3-4 wk)
 │
 ▼
[3] State Management (2-3 wk)
 │  └─ Riverpod or Bloc
 │
 ▼
[4] Backend Integration (2 wk)
 │  └─ Firebase, REST APIs
 │
 ▼
[5] Deploy to Both Stores (1 wk)
```

**2025 Stack:** Flutter 3.x + Dart 3.x + Riverpod + Firebase

---

### Game Development
```
[1] Game Basics (4-6 wk)
 │  └─ Game loop, input handling
 │
 ▼
[2] Unity/C# Fundamentals (6-8 wk)
 │  └─ GameObjects, Components, Scripts
 │
 ▼
[3] Physics + Graphics (4-6 wk)
 │  └─ Rigidbody, colliders, shaders
 │
 ▼
[4] Audio + Polish (2-4 wk)
 │
 ▼
[5] Publish (ongoing)
    └─ Steam, App Store, Play Store
```

**2025 Stack:** Unity 6 LTS + C# OR Unreal 5.4 + C++

---

## Platform Decision Tree

```
Which platform?
│
├─► Apple ecosystem only?
│   └─► iOS (Swift + SwiftUI)
│
├─► Android ecosystem only?
│   └─► Android (Kotlin + Compose)
│
├─► Both platforms?
│   ├─► Performance-critical? → Native for both
│   ├─► Budget/time limited? → Flutter
│   └─► Web developer background? → React Native
│
└─► Making games?
    ├─► 2D/3D indie → Unity
    ├─► AAA quality → Unreal
    └─► Simple 2D → Godot
```

---

## Game Engine Comparison

| Engine | Market | Language | Learning | Best For |
|--------|--------|----------|----------|----------|
| **Unity** | 51% | C# | Medium | Indie, mobile, VR |
| **Unreal** | 31% | C++/BP | Hard | AAA, high-fidelity |
| **Godot** | 10% | GDScript | Easy | Indie, 2D |

---

## Troubleshooting

```
Native vs Cross-platform?
├─► Need platform-specific APIs (HealthKit, ARCore)? → Native
├─► Performance-critical (AR/VR, complex animations)? → Native
├─► Budget or time limited? → Flutter
├─► Team knows JavaScript? → React Native
└─► Starting from scratch? → Flutter (best DX)

Simulator works, device doesn't?
├─► Missing entitlements/capabilities?
├─► Different iOS/Android version?
├─► Network connectivity issues?
└─► Always test on real devices from day 1

App rejected by store?
├─► Read rejection reason carefully
├─► Check App Store Review Guidelines
├─► Most common: metadata issues, crashes, spam
└─► Appeal if unjustified
```

---

## Common Failure Modes

| Symptom | Root Cause | Recovery |
|---------|------------|----------|
| Slow UI | Too many recompositions | Profile, optimize state |
| Memory leaks | Not cleaning up resources | Use lifecycle-aware components |
| App rejected | Guidelines violation | Read guidelines BEFORE building |
| Game stutters | Draw call overhead | Object pooling, LOD, batching |

---

## Portfolio Projects

### Mobile (Progressive)
1. **Todo App** - CRUD basics
2. **Weather App** - API integration
3. **Chat App** - Real-time, auth
4. **Payment App** - Stripe, security

### Games
1. **2D Platformer** - Physics basics
2. **3D Runner** - 3D graphics, particles
3. **Multiplayer Game** - Networking

---

## Next Actions

Specify your target platform for a detailed learning plan.

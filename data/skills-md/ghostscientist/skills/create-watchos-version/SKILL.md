---

name: create-watchos-version
description: Analyzes existing iOS/macOS/Apple platform projects to create a comprehensive, phased plan for building a watchOS companion or standalone app. Use when users want to add watchOS support to an existing Apple platform app, create a Watch app version of their iOS app, or build watchOS features. The skill digests project architecture, identifies patterns, analyzes API compatibility, searches for current watchOS documentation, and produces a detailed implementation plan with API availability warnings before any code generation.

---


# Create watchOS Version

Analyzes existing Apple platform projects and creates detailed, phased implementation plans for watchOS apps that are elegant, top-tier experiences—not naive skins of the parent app.

## Workflow

1. **Project Discovery** - Analyze project structure, patterns, architecture
2. **Feature Mapping** - Identify watchOS-suitable features and priorities
3. **API Compatibility** - Search web for current watchOS API availability
4. **Architecture Planning** - Design watchOS-specific architecture
5. **Plan Generation** - Create phased plan with warnings and alternatives
6. **User Review** - Present plan for approval before implementation

## Phase 1: Project Discovery

Scan project root for:

```
├── App Architecture (SwiftUI, UIKit, AppKit, hybrid)
├── Data Layer (Core Data, SwiftData, Realm, custom)
├── Networking (URLSession, Alamofire, custom)
├── State Management (ObservableObject, TCA, Redux-like)
├── Navigation (NavigationStack, Coordinator)
├── Shared Frameworks (SPM packages, shared targets)
├── Assets (colors, images, SF Symbols)
├── Existing Watch Target (if any)
└── Minimum iOS Version (affects watchOS targeting)
```

Key files: `*.xcodeproj`, `Package.swift`, `Info.plist`, App entry points, ViewModels, Models.

## Phase 2: Feature Mapping

**Glanceable (High Priority)**: Status displays, counters, progress, recent items, quick stats

**Quick Actions (High Priority)**: Single-tap toggles, shortcuts, haptic confirmations

**Complications/Widgets (Critical)**: Map data to WidgetKit families—accessoryCircular, accessoryRectangular, accessoryInline, accessoryCorner. Consider Smart Stack relevance.

**Background**: HealthKit integration, background refresh, Watch Connectivity sync

**Defer/Exclude**: Complex data entry, long-form content, sustained screen time features

## Phase 3: API Compatibility

**CRITICAL**: Always search web for current watchOS docs before finalizing. APIs change frequently.

Search: `[FrameworkName] watchOS availability site:developer.apple.com`

### Quick Reference

**Available**: SwiftUI, SwiftData (10+), WidgetKit (9+), HealthKit, WorkoutKit, CoreLocation (limited), WatchConnectivity, CloudKit, CoreMotion, AVFoundation (audio), CoreBluetooth, Combine, Swift Concurrency

**Unavailable/Limited**: UIKit, WebKit, MapKit (limited), CoreImage (limited), ARKit, RealityKit, StoreKit (limited), Background URLSession (limited)

See `references/api-compatibility.md` for detailed compatibility matrix.

## Phase 4: Architecture

### Version Targeting

```
iOS 16+ → watchOS 9+  (WidgetKit complications)
iOS 17+ → watchOS 10+ (SwiftData, Smart Stack)
iOS 18+ → watchOS 11+ (Live Activities on Watch)
```

### Structure

```
Shared/
├── Models/           # Pure Swift, shared via target membership
├── Services/         # Platform-agnostic logic
└── Utilities/

WatchApp/
├── App.swift
├── Views/
├── ViewModels/
├── Complications/
└── WatchConnectivity/
```

### Design Principles

1. **Glanceability** - Visible within 2 seconds
2. **Minimal Interaction** - 1-3 taps max
3. **Context Awareness** - Time, location, activity
4. **Battery Conscious** - Efficient refresh, TimelineSchedule
5. **Haptic Feedback** - Confirm actions appropriately

### SwiftUI Gotchas

- Avoid nested TabViews (memory leaks)
- Use TimelineSchedule for efficient metric updates
- Check `isLuminanceReduced` to reduce work when dimmed
- Don't use data-driven high-frequency UI refreshes

## Phase 5: Plan Generation

Use template in `references/plan-template.md` to generate:

1. Executive Summary
2. ⚠️ API Compatibility Warnings table
3. Phased implementation tasks
4. Testing checklist

## Phase 6: User Review

Present plan and ask for approval before implementing:

> "I've analyzed your project and created a watchOS plan. Before proceeding:
> 1. **API Warnings**: [N] APIs unavailable—alternatives documented.
> 2. **Recommended Features**: [list] prioritized for Watch.
> 3. **Scope**: [N] phases.
> 
> Proceed with implementation, or adjust the plan?"

**Do not implement until user approves.**

## Best Practices Reference

### Watch Connectivity

```swift
guard WCSession.default.activationState == .activated else { return }
// sendMessage: immediate, requires reachability
// transferUserInfo: queued, guaranteed
// transferCurrentComplicationUserInfo: complication priority
```

### Complications

```swift
// Use appropriate reload policy
Timeline(entries: entries, policy: .after(nextUpdateDate))
// Use .never for static complications
```

### Battery Efficiency

- Timeline-based over active refresh
- Check `isLuminanceReduced`
- Batch Watch Connectivity transfers
- Significant location change vs continuous updates
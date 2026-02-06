---
name: ios-swift-expert
description: Elite iOS and macOS development expertise for Swift, SwiftUI, UIKit, Xcode, and the entire Apple development ecosystem. Automatically activates when working with .swift files, Xcode projects (.xcodeproj, .xcworkspace), SwiftUI interfaces, iOS frameworks (UIKit, Core Data, Combine, etc.), app architecture, or Apple platform development.
---

# iOS and macOS Development Expert

## Overview

Elite-level guidance for iOS and macOS development with deep expertise in Swift, SwiftUI, UIKit, and the entire Apple development ecosystem.

**Core principle:** Follow Apple's Human Interface Guidelines, Swift API Design Guidelines, and modern iOS development best practices while writing clean, performant, memory-safe code.

## When to Use

Automatically activates when:
- Working with `.swift` source files
- Opening or modifying Xcode projects (`.xcodeproj`, `.xcworkspace`)
- Editing SwiftUI views or UIKit view controllers
- Implementing iOS/macOS frameworks (Core Data, Combine, UIKit, SwiftUI, etc.)
- Debugging Xcode build errors or runtime issues
- Designing app architectures (MVVM, MVI, Clean Architecture)
- Optimizing performance or fixing memory leaks
- Implementing accessibility, localization, or privacy features
- Configuring app targets, build settings, or project structure

Manual invocation when:
- User explicitly asks about Swift language features
- User needs guidance on Apple platform APIs
- User requests iOS/macOS development best practices
- User encounters Apple platform-specific problems

## When NOT to Use This Skill

Do not use this skill for:
- General programming questions unrelated to Apple platforms
- Backend server development (unless using Vapor/Swift on server)
- Cross-platform mobile development (React Native, Flutter, Kotlin Multiplatform)
- Web development (unless WebKit/Safari specific or Swift for WebAssembly)
- Android development
- Desktop development on non-Apple platforms

## Core Expertise Areas

### Swift Language Mastery

- **Modern Swift Features**: Value types, protocol-oriented programming, generics, result builders, property wrappers, async/await, actors
- **Memory Management**: ARC, weak/unowned references, retain cycles, memory graph debugging
- **Concurrency**: Structured concurrency with async/await, actors, task groups, continuation, legacy GCD patterns
- **Error Handling**: Proper use of throws, Result type, error propagation, custom error types
- **Type Safety**: Leveraging Swift's type system for safer code, phantom types, type erasure

### SwiftUI Development

- **Declarative UI**: Views, modifiers, composition, custom view builders
- **State Management**: @State, @Binding, @ObservedObject, @StateObject, @EnvironmentObject, @Observable (iOS 17+)
- **Layout System**: VStack, HStack, ZStack, GeometryReader, Layout protocol (iOS 16+), safe areas
- **Animations**: Implicit animations, explicit animations, transitions, matched geometry effect
- **Navigation**: NavigationStack (iOS 16+), NavigationPath, programmatic navigation, deep linking
- **Advanced Patterns**: ViewModifiers, PreferenceKeys, custom environments, coordinators

### UIKit (Legacy & Hybrid Apps)

- **View Controllers**: Lifecycle, containment, custom transitions, adaptive layouts
- **Auto Layout**: Constraints, stack views, size classes, intrinsic content size
- **Table/Collection Views**: Data sources, delegates, diffable data sources, compositional layout
- **Gestures**: Tap, swipe, pan, long press, custom gesture recognizers
- **Core Animation**: Layer animations, keyframe animations, CADisplayLink
- **Integration**: Bridging UIKit and SwiftUI with UIViewRepresentable/UIViewControllerRepresentable

### iOS Frameworks & APIs

- **Core Data**: Managed object context, fetch requests, predicates, migrations, relationships
- **Combine**: Publishers, subscribers, operators, cancellables, error handling, backpressure
- **Core Location**: Location services, geofencing, heading, privacy best practices
- **CloudKit**: Public/private databases, records, subscriptions, sharing
- **StoreKit**: In-app purchases, subscriptions, transaction handling, receipt validation
- **HealthKit, HomeKit, ARKit, RealityKit**: Domain-specific framework expertise

### Xcode & Build System

- **Project Structure**: Targets, schemes, configurations, build phases, script phases
- **Build Settings**: Optimization levels, code signing, provisioning profiles, entitlements
- **Debugging Tools**: LLDB, breakpoints, view debugging, Instruments, memory graph debugger
- **Testing**: XCTest, UI testing, performance testing, test plans, code coverage
- **Swift Package Manager**: Package manifests, dependencies, versioning, local packages

### App Architecture

- **MVVM**: Model-View-ViewModel with SwiftUI or UIKit
- **MVI**: Model-View-Intent unidirectional data flow
- **Clean Architecture**: Layered separation, dependency injection, testability
- **Coordinator Pattern**: Navigation flow management
- **Repository Pattern**: Data layer abstraction
- **Design Patterns**: Factory, observer, strategy, dependency injection containers

## Development Workflow

### 1. Build Verification

**Always verify builds** after making changes using `xcodebuild`:

```bash
xcodebuild -project YourProject.xcodeproj -scheme YourScheme -quiet build
```

- Use `-quiet` flag to minimize output as specified in project documentation
- Replace placeholders with actual project and scheme names
- For workspaces, use `-workspace YourWorkspace.xcworkspace`
- Check exit code to confirm success

### 2. Code Standards

Follow these standards for all Swift code:

**Naming Conventions:**
- Types: UpperCamelCase (e.g., `UserProfileViewController`)
- Functions/variables: lowerCamelCase (e.g., `fetchUserData()`)
- Constants: lowerCamelCase (e.g., `let maxRetryCount = 3`)
- Protocols: UpperCamelCase, often ending in -able, -ible, or -ing (e.g., `Codable`, `Drawable`)

**Access Control:**
- Default to `private` or `fileprivate` for implementation details
- Use `internal` (default) for module-internal APIs
- Mark `public` or `open` only for exported APIs
- Consider `@testable import` for testing instead of making everything public

**Code Organization:**
- Group related code with `// MARK: - Section Name`
- Order: properties, initializers, lifecycle methods, public methods, private methods
- One type per file (exceptions for small helper types)
- Use extensions for protocol conformance

**Memory Safety:**
- Use `[weak self]` in closures that may outlive the caller
- Use `[unowned self]` only when certain closure won't outlive the reference
- Break retain cycles between parent/child view controllers
- Monitor retain cycles in Instruments

### 3. Testing Requirements

Write testable code with appropriate coverage:

**Unit Tests:**
- Test business logic, view models, data transformations
- Mock network/database dependencies
- Use dependency injection for testability
- Aim for >80% coverage on critical paths

**UI Tests:**
- Test critical user flows (login, purchase, main features)
- Use accessibility identifiers for reliable element selection
- Keep UI tests fast and focused

### 4. Performance Considerations

Optimize for user experience:

**Rendering Performance:**
- Keep view hierarchies shallow
- Avoid expensive operations in `body` (SwiftUI) or `layoutSubviews` (UIKit)
- Profile with Instruments (Time Profiler, SwiftUI view body)
- Lazy-load content, virtualize lists

**Memory Management:**
- Release large objects when no longer needed
- Monitor memory warnings and respond appropriately
- Profile with Instruments (Allocations, Leaks)
- Avoid strong reference cycles

**Battery Life:**
- Minimize location services usage
- Batch network requests
- Use background modes judiciously
- Profile with Instruments (Energy Log)

### 5. Apple Platform Best Practices

Follow Apple's official guidelines for:
- Human Interface Guidelines (navigation, controls, interactions, accessibility)
- Privacy & Security (permissions, data handling, authentication)
- Accessibility (VoiceOver, Dynamic Type, color contrast)
- Localization (NSLocalizedString, RTL languages, formatting)

See `./references/apple-guidelines.md` for detailed requirements and best practices.

## Problem-Solving Approach

### 1. Analysis Phase

- Read error messages carefully (Xcode, runtime logs, crash reports)
- Check project-specific requirements in CLAUDE.md
- Review existing code patterns and architecture
- Consider iOS version compatibility and API availability

### 2. Solution Design

- Provide multiple approaches when appropriate, explaining trade-offs
- Reference official Apple documentation and WWDC sessions
- Consider performance, memory, and battery impact
- Suggest appropriate design patterns for the problem

### 3. Implementation

- Write clean, readable Swift code following API Design Guidelines
- Include inline comments for complex logic
- Add proper error handling with meaningful error messages
- Ensure code is testable with dependency injection where appropriate

### 4. Validation

- Verify code builds successfully with `xcodebuild`
- Test on simulator and, when possible, physical devices
- Check for retain cycles and memory leaks
- Validate accessibility and localization

## Communication Style

**Clear and Actionable:**
- Provide specific code examples, not just descriptions
- Explain the "why" behind architectural and implementation decisions
- Offer step-by-step instructions for complex implementations
- Highlight potential pitfalls and how to avoid them

**Authoritative Sources:**
- Link to Apple's official documentation
- Cite WWDC sessions for best practices
- Reference Swift Evolution proposals for language features
- Point to Human Interface Guidelines for design decisions
- See `./references/apple-guidelines.md` for documentation links

**Trade-offs:**
- Performance vs. code simplicity
- SwiftUI vs. UIKit for specific use cases
- Async/await vs. completion handlers
- Protocol-oriented vs. class-based design

**Complete implementation examples:** See `./references/code-examples.md` for SwiftUI views, MVVM view models, Core Data setup, and memory management patterns.

**Design patterns and solutions:** See `./references/patterns.md` for dependency injection, result builders, coordinator pattern, and other common solutions.

**Debugging guidance:** See `./references/debugging-strategies.md` for comprehensive debugging techniques for Xcode build issues, runtime problems, and SwiftUI-specific debugging.

## Success Criteria

Guidance is successful when:

- Code builds successfully using `xcodebuild` with `-quiet` flag
- Solutions follow Apple's Human Interface Guidelines
- Implementations are memory-safe and performant
- Code adheres to Swift API Design Guidelines
- Solutions are testable and maintainable
- Proper error handling is implemented
- Accessibility and localization are considered
- User privacy and security best practices are followed
- Target iOS/macOS versions are compatible

## Additional Resources

For complete reference materials, see:
- `./references/code-examples.md` - SwiftUI, MVVM, Core Data, and memory management examples
- `./references/patterns.md` - Dependency injection, result builders, coordinator pattern
- `./references/debugging-strategies.md` - Xcode, runtime, and SwiftUI debugging techniques
- `./references/apple-guidelines.md` - Official Apple documentation and guidelines

## Remember

- Always verify builds with `xcodebuild -quiet`
- Follow project-specific standards from CLAUDE.md
- Write memory-safe code with proper ARC usage
- Consider accessibility, localization, and privacy
- Reference Apple documentation and WWDC best practices
- Explain trade-offs in architectural decisions
- Provide clear, actionable code examples

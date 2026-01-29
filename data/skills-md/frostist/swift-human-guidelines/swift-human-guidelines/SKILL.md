---
name: swift-human-guidelines
description: Comprehensive Swift 6 and SwiftUI development guidelines for building iOS 26, iOS 18, iPadOS, macOS, watchOS, visionOS, and tvOS applications. Covers Foundation Models API, BGContinuedProcessingTask, Call Translation API, Liquid Glass design system, data-race safety, typed throws, synchronization primitives, SwiftUI/UIKit interoperability, zoom transitions, and document-based apps. Use when building new Apple platform apps, implementing Apple Intelligence features, optimizing performance with Swift 6 concurrency, following Apple Human Interface Guidelines, creating cross-platform applications, or working with iOS 26/18 APIs. Triggers on Swift code, SwiftUI views, Xcode projects, app architecture, background processing, translation features, Foundation Models, synchronization, actors, Sendable types, or modern Apple platform development.
---

# Swift and SwiftUI Development Guidelines

## Overview

Build production-ready Swift and SwiftUI applications for all Apple platforms following Apple's Human Interface Guidelines, modern Swift best practices, and performance optimization techniques. This skill provides comprehensive guidance for creating new apps, architecting cross-platform solutions, and implementing efficient, maintainable code.

## When to Use This Skill

Use this skill when:
- Building new iOS, iPadOS, macOS, watchOS, or tvOS apps from scratch
- Implementing SwiftUI views and navigation patterns
- Optimizing app performance and memory usage
- Following Apple Human Interface Guidelines
- Creating cross-platform Swift applications
- Implementing modern Swift concurrency with async/await
- Architecting MVVM or other SwiftUI-appropriate patterns
- Setting up proper state management
- Implementing accessibility features

## Quick Start: Building a New App

### 1. Choose Your Platform(s)

**Single Platform:**
- iOS: Mobile-first, touch-based, portrait/landscape
- macOS: Desktop, pointer-based, window management
- watchOS: Glanceable, quick interactions
- tvOS: Cinematic, focus-based navigation

**Multi-Platform:**
- iOS + iPadOS: Adaptive layouts with size classes
- iOS + macOS: Shared business logic, platform-specific UI
- Universal: All platforms with maximum code sharing

### 2. Use App Templates

Start with production-ready templates in `assets/`:
- `ios-app-template.swift`: Modern iOS app with TabView navigation, MVVM architecture, async/await
- `macos-app-template.swift`: macOS app with NavigationSplitView, Settings, window management

Templates include:
- Proper app structure with `@main` entry point
- MVVM architecture with ObservableObject ViewModels
- Repository pattern for data access
- Async/await for network operations
- Navigation patterns (TabView for iOS, NavigationSplitView for macOS)
- Reusable components and proper state management

### 3. Project Structure

Organize code for maintainability and cross-platform sharing:

```
MyApp/
├── Shared/                    # 100% shared code
│   ├── Models/               # Data structures
│   ├── ViewModels/           # Business logic
│   ├── Services/             # Networking, persistence
│   └── Views/Shared/         # Reusable components
├── iOS/                      # iOS-specific
│   ├── Views/
│   └── iOSApp.swift
├── macOS/                    # macOS-specific
│   ├── Views/
│   └── macOSApp.swift
└── Tests/
```

### 4. Follow Core Principles

**Architecture:**
- MVVM pattern: Models, Views, ViewModels
- Unidirectional data flow: State down, events up
- Dependency injection for testability
- Repository pattern for data access

**State Management:**
- `@State`: Local view state
- `@StateObject`: View owns the lifecycle
- `@ObservedObject`: View observes external object
- `@EnvironmentObject`: Shared across hierarchy
- `@Binding`: Two-way connection

**Performance:**
- Use lazy stacks for large lists
- Provide stable identifiers for ForEach
- Minimize view body recalculations
- Use async/await for all async operations
- Profile with Instruments regularly

## Core Development Workflows

### Building a New View

1. **Define the model** (if needed)
2. **Create the ViewModel** with business logic
3. **Build the View** using SwiftUI components
4. **Extract reusable components** for complex views
5. **Add navigation** if needed
6. **Test the ViewModel** with unit tests

Example:
```swift
// 1. Model
struct Article: Identifiable, Codable {
    let id: UUID
    let title: String
    let content: String
}

// 2. ViewModel
@MainActor
class ArticleListViewModel: ObservableObject {
    @Published var articles: [Article] = []
    @Published var isLoading = false
    
    func loadArticles() async {
        isLoading = true
        defer { isLoading = false }
        articles = await fetchArticles()
    }
}

// 3. View
struct ArticleListView: View {
    @StateObject private var viewModel = ArticleListViewModel()
    
    var body: some View {
        List(viewModel.articles) { article in
            ArticleRow(article: article)
        }
        .task {
            await viewModel.loadArticles()
        }
    }
}
```

### Implementing Navigation

**iOS: NavigationStack**
```swift
NavigationStack(path: $path) {
    List(items) { item in
        NavigationLink(value: item) {
            ItemRow(item: item)
        }
    }
    .navigationDestination(for: Item.self) { item in
        ItemDetailView(item: item)
    }
}
```

**macOS: NavigationSplitView**
```swift
NavigationSplitView {
    List(items, selection: $selectedItem) { item in
        ItemRow(item: item)
    }
} detail: {
    if let item = selectedItem {
        ItemDetailView(item: item)
    }
}
```

### Performance Optimization

**Key strategies:**
1. Use `LazyVStack`/`LazyHStack` for large lists
2. Provide stable IDs with `Identifiable`
3. Extract subviews to minimize recalculations
4. Use `@Published` selectively
5. Cache expensive computations
6. Profile with Instruments

See `references/performance-optimization.md` for detailed patterns and examples.

### Cross-Platform Development

**Maximize code sharing:**
- 100% shared: Models, business logic, networking
- 95% shared: ViewModels, repositories
- 70% shared: Reusable view components
- Platform-specific: Navigation, window management, input

**Use conditional compilation:**
```swift
#if os(iOS)
// iOS-specific code
#elseif os(macOS)
// macOS-specific code
#endif
```

See `references/cross-platform-development.md` for comprehensive patterns.

## Build and Testing

### Build Command

Use the standard Xcode build command with analysis:
```bash
xcodebuild -project MyApp.xcodeproj -scheme MyApp -configuration Debug clean build analyze
```

### Testing Strategy

**Unit Tests:** Test ViewModels and business logic
```swift
@MainActor
class ViewModelTests: XCTestCase {
    func testLoadData() async throws {
        let viewModel = ViewModel(repository: MockRepository())
        await viewModel.loadData()
        XCTAssertFalse(viewModel.items.isEmpty)
    }
}
```

**UI Tests:** Test user flows with SwiftUI previews
```swift
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .previewDisplayName("Light Mode")
        ContentView()
            .preferredColorScheme(.dark)
            .previewDisplayName("Dark Mode")
    }
}
```

## Reference Documentation

This skill includes comprehensive reference documentation:

### references/human-interface-guidelines.md
Complete Apple HIG coverage:
- Core principles (Clarity, Deference, Depth)
- **Liquid Glass design system (iOS 26+)**
- Platform-specific guidelines (iOS, macOS, watchOS, tvOS, visionOS)
- Typography and Dynamic Type
- Color and Dark Mode
- Accessibility (VoiceOver, Dynamic Type, Reduce Motion)
- App architecture and settings patterns
- System integration features

**When to read:** Designing UI, ensuring HIG compliance, implementing Liquid Glass materials, choosing navigation patterns

### references/swiftui-best-practices.md
Modern SwiftUI patterns:
- MVVM architecture with examples
- State management patterns
- View composition and extraction
- Navigation patterns for all platforms
- Data flow and dependency injection
- Custom modifiers and styling
- Testing strategies
- Common patterns (loading states, search, pull-to-refresh)
- **iOS 18: SwiftUI/UIKit animation interoperability**
- **iOS 18: Zoom transitions and unified gestures**
- **iOS 26: UIKit/SwiftUI scene mixing**
- **iOS 18: DocumentGroupLaunchScene**

**When to read:** Architecting new features, implementing state management, using iOS 18/26 APIs, creating reusable components

### references/performance-optimization.md
Performance techniques:
- View performance optimization
- State management efficiency
- List and collection performance
- Memory management
- Async operations best practices
- Build performance tips
- Profiling with Instruments

**When to read:** Optimizing slow views, reducing memory usage, improving list scrolling, debugging performance issues

### references/swift-language-features.md
Modern Swift features:
- Property wrappers and result builders
- Async/await and structured concurrency
- Actors and MainActor
- Error handling patterns
- Optionals and collections
- Protocols and generics
- Memory management (ARC, weak/unowned)
- **Swift 6: Data-race safety and Sendable protocol**
- **Swift 6: Typed throws**
- **Swift 6.2: Single-threaded by default (implicit @MainActor)**
- **Swift 6.2: Observable async sequences**
- **Swift 6: Embedded Swift subset**
- **Swift 6: 128-bit integer support**

**When to read:** Using Swift 6 features, implementing concurrency, ensuring data-race safety, migrating to Swift 6

### references/foundation-models-api.md
Apple Intelligence integration (iOS 26+):
- Foundation Models framework overview
- Text summarization APIs
- Text extraction and entity recognition
- Content classification
- On-device processing
- Performance optimization
- Privacy considerations

**When to read:** Implementing Apple Intelligence features, adding summarization, extracting information from text

### references/background-processing-ios26.md
Advanced background execution (iOS 26+):
- BGContinuedProcessingTask API
- Background GPU access
- Task continuation patterns
- System limits and best practices
- Handling expiration
- Resource management

**When to read:** Implementing background processing, finishing user-initiated tasks, using GPU in background

### references/call-translation-api.md
Real-time translation (iOS 26+):
- Call Translation API overview
- Live audio translation
- Supported language pairs
- Streaming translation
- Privacy and permissions
- Performance optimization

**When to read:** Implementing translation features, building communication apps, adding multilingual support

### references/swift-synchronization.md
Low-level concurrency primitives (Swift 6+):
- Atomic operations
- Mutex API
- Lock-free data structures
- Memory ordering semantics
- Integration with Swift concurrency

**When to read:** Implementing thread-safe primitives, building custom synchronization, optimizing performance-critical code

**When to read:** Using modern Swift features, implementing concurrency, managing memory, working with generics

### references/cross-platform-development.md
Multi-platform strategies:
- Platform detection and conditional compilation
- Shared code architecture
- Platform-specific UI patterns
- Input method handling (touch vs pointer)
- Navigation patterns per platform
- Window management
- Code organization for maximum sharing

**When to read:** Building cross-platform apps, adapting UI for different platforms, maximizing code reuse

## Assets

### assets/ios-app-template.swift
Production-ready iOS app template with:
- TabView navigation
- MVVM architecture
- Async/await networking
- Authentication flow
- List with pull-to-refresh
- Proper error handling

### assets/macos-app-template.swift
Production-ready macOS app template with:
- NavigationSplitView with sidebar
- Settings window
- Toolbar and menu commands
- Window management
- Keyboard shortcuts
- Edit sheets and forms

## Best Practices Summary

**Architecture:**
- Use MVVM pattern
- Separate concerns clearly
- Inject dependencies
- Keep ViewModels testable

**State Management:**
- Choose the right property wrapper
- Minimize @Published properties
- Use unidirectional data flow
- Avoid retain cycles

**Performance:**
- Use lazy stacks for lists
- Provide stable IDs
- Extract subviews
- Profile regularly
- Test on real devices

**Code Quality:**
- Follow Swift naming conventions
- Use value types when possible
- Handle all error cases
- Write unit tests for ViewModels
- Use SwiftUI previews

**Platform Integration:**
- Follow Human Interface Guidelines
- Support Dynamic Type
- Implement proper accessibility
- Respect system settings (Dark Mode, Reduce Motion)
- Use SF Symbols for icons

**Cross-Platform:**
- Maximize code sharing (models, ViewModels, services)
- Use conditional compilation for platform differences
- Design adaptive layouts
- Respect platform conventions

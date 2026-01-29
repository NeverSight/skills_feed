---
name: swift-mvvm
description: "Use when writing or refactoring Swift (SwiftUI/UIKit/AppKit) code to follow MVVM with a small, testable ViewModel. Triggers on: MVVM, ViewModel, ObservableObject, @Observable, Observation, AppKit, NSViewController, UIKit, state management, dependency injection, protocol adapters, refactor view logic, massive view model, testable, async/await, Combine, Swift Testing, #expect."
---

# Swift MVVM Skill

Help the agent produce **better MVVM code** for Swift projects.

## Core stance
- **Keep the ViewModel UI-framework agnostic.** ViewModels should **not** import `SwiftUI`, `UIKit`, or `AppKit`.
- The ViewModel should be mostly **(1) state**, **(2) intent methods**, and **(3) dependency coordination**.
- Push work into **smaller, testable units** (pure structs/functions, use cases, controllers, repositories, mappers, formatters).
- Use **dependency injection** with protocols so everything is mockable.
- **Extensions are encouraged** for organization (especially protocol conformances).

## When to use
Use this skill when the user asks to:
- Add or refactor features in SwiftUI/UIKit/AppKit and keep architecture clean.
- Create or improve a ViewModel (state, intents, effects) and move logic out of Views/ViewControllers.
- Fix state-management issues (wrong wrappers, threading warnings, unstable bindings).
- Improve testability (protocol-based dependencies, mocks/fakes, deterministic state updates).
- Reduce a “massive ViewModel” by splitting concerns.

## First check (before writing code)
1. Identify UI tech: **SwiftUI**, **UIKit**, or **AppKit**.
2. Identify deployment target:
   - If **iOS 17+/macOS 14+** is available, prefer **Observation** (`@Observable`).
   - Otherwise prefer **Combine-based** `ObservableObject` + `@Published`.
3. Match existing project style (naming, folders, DI approach, networking layer).

## MVVM responsibilities
### View layer
SwiftUI `View` / UIKit `UIViewController` / AppKit `NSViewController`:
- Declares layout and binds to **state**.
- Sends **user intents** (tap, selection, text changes) to the ViewModel.
- Owns UI-only concerns (navigation, presenting alerts, AppKit panels, first responder, etc.).

### ViewModel
- Owns **screen state** (loading/data/error, derived UI values).
- Coordinates effects through injected dependencies.
- Exposes **intent methods** (`onAppear()`, `refresh()`, `didTap…`) rather than views calling random internals.

### Domain / Services
- Encapsulate fetching, caching, persistence, decoding, validation.
- Must be independent of UI frameworks.

## Hard rule: No UI framework imports in ViewModels
**ViewModels should not import:**
- `SwiftUI`
- `UIKit`
- `AppKit`

If a ViewModel needs a platform behavior, define a tiny protocol in a non-UI module (Foundation-only), and provide a platform implementation in the View layer (or platform adapter module).

Example:

```swift
// In a Foundation-only target / file.
protocol FileRevealing {
  func reveal(_ url: URL)
}

// In AppKit layer.
import AppKit

struct WorkspaceFileRevealer: FileRevealing {
  func reveal(_ url: URL) {
    NSWorkspace.shared.activateFileViewerSelecting([url])
  }
}

Any “AppKit-y” or “UIKit-y” behavior inside the ViewModel is a **smell**.

## Preferred ViewModel shapes

Pick one based on scope.

### Pattern A: Simple screen

- `State` struct (nested)
- intent methods
- async `load()` with cancellation

### Pattern B: Complex screen

- `State` struct (nested)
- `Action` enum + `send(_:)`
- reducer-like switch for state transitions
- side effects delegated to injected units

## Keep state structured (avoid a ViewModel with 30 vars)

Prefer:

```swift
struct State: Equatable {
  var view = ViewState()
  var content = ContentState()
  var alerts = AlertsState()

  struct ViewState: Equatable {
    var isLoading = false
    var title = ""
  }

  struct ContentState: Equatable {
    var rows: [Row] = []
    var emptyMessage: String? = nil
  }

  struct AlertsState: Equatable {
    var error: ErrorState? = nil
  }
}
```

## Refactoring a massive ViewModel (priority order)

When reducing a large VM, refactor in this order:

1. **Extract pure logic first**

- Move non-IO computations into **pure structs** or **pure functions**.
- Examples: filtering, sorting, mapping domain models to row models, formatting, validation, state reducers.

2. **Extract side effects into controllers (still testable)**

- Create small “effect” units that do IO and orchestration.
- Keep them behind protocols and inject into the VM.
- Examples: `LoadExamplesUseCase`, `ExamplesController`, `AnalyticsTracking`, `FileRevealing`.

3. **Leave the VM as state + intents**

- VMs forward intents to pure logic/effect units and assign state.

## Concurrency & cancellation rules

- UI state changes should happen on the **main actor**.
- Store ongoing tasks and cancel them when a new request starts or when the view disappears.

## SwiftUI integration rules

### Observation (`@Observable`)

- Hold a ViewModel instance using `@State` (owner) and pass it down.

### Combine (`ObservableObject`)

- Use `@StateObject` when the view **creates/owns** the ViewModel.
- Use `@ObservedObject` when the view is **given** the ViewModel.

## Dependency injection rules

- ViewModel takes dependencies in its initializer.
- Dependencies are protocols; provide a production implementation and a mock/fake for tests.
- Prefer injecting **small units**:
  - Pure logic: `RowBuilder`, `Validator`, `Reducer`
  - Effects: `UseCase`, `Controller`, `Repository`
  - Platform adapters: `FileRevealing`, `URLOpening`, etc.

## Avoid massive ViewModels

Smells:

- Imports UI frameworks.
- Does URLSession/JSON decoding directly.
- Builds NSAlert/UIAlertController.
- Knows about NSWorkspace/UIApplication.
- Formats everything inline with complex logic.
- Handles navigation, analytics, networking, caching all together.

Refactor moves:

- Extract a pure `RowBuilder` or `Reducer`.
- Extract a `UseCase` for business rules.
- Extract a `Repository` for IO.
- Extract a side-effects `Controller` to orchestrate multiple services.
- Extract platform adapters (tiny protocols) for UI actions.

## Output expectations

When writing/refactoring:

- Provide code in **diff-friendly chunks**, grouped by file.
- Prefer small, composable functions.
- Use extensions for organization (e.g., protocol conformances, grouping helpers).
- Name clearly: `FooViewModel`, `FooState`, `FooUseCase`, `FooRepository`, `FooController`, `FooRowBuilder`.
- Add tests for ViewModel state transitions and extracted pure logic.

## Testing guidance

Prefer **Swift Testing** (`import Testing`, `@Test`, `#expect`, `#require`) for new tests.

- Test pure logic units directly (fast, deterministic).
- Test ViewModel state transitions (success/failure/cancellation) by injecting mocks.

## Templates

Copy/paste from:

- `templates/ObservationViewModel.swift`
- `templates/CombineViewModel.swift`
- `templates/AppKitViewController.swift`
- `templates/ProtocolAdapters.swift`
- `templates/ServiceUseCaseControllerAndPureLogic.swift`
- `templates/ViewModelTests.swift` (Swift Testing)

## Additional resources (load only if needed)

- MVVM Overview: [references/mvvm-overview.md](references/mvvm-overview.md)
- Module Structure: [references/module-structure.md](references/module-structure.md)
- File Naming Conventions: [references/file-naming-conventions.md](references/file-naming-conventions.md)
- Where Things Go: [references/where-things-go.md](references/where-things-go.md)
- Common Patterns: [references/common-patterns.md](references/common-patterns.md)
- Adding New Features: [references/adding-new-features.md](references/adding-new-features.md)
- Integration Patterns: [references/integration-patterns.md](references/integration-patterns.md)
- Anti-Patterns: [references/anti-patterns.md](references/anti-patterns.md)
- Testing Considerations: [references/testing-considerations.md](references/testing-considerations.md)
- Services vs Feature Services: [references/services-vs-feature-services.md](references/services-vs-feature-services.md)
- Controller vs Coordinator: [references/controller-vs-coordinator.md](references/controller-vs-coordinator.md)
- State Management: [references/state-management.md](references/state-management.md)
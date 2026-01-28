---
name: coding-standards-enforcer
description: Enforce repository coding standards for Swift 6.2 concurrency, Swift language rules. Use when reviewing or implementing Swift code changes.
---

# Coding Standards Enforcer

## Description and Goals

This skill enforces repository-wide coding standards for Swift 6.2 concurrency, Swift language rules, and best practices. It ensures all Swift code in the repository follows consistent patterns, uses modern Swift APIs, and adheres to strict concurrency requirements.

### Goals

- Ensure compliance with Swift 6.2 strict concurrency rules
- Enforce modern Swift language patterns and APIs
- Prevent common concurrency mistakes and anti-patterns
- Maintain consistent code style across the repository
- Support Swift 6 migration and best practices

## What This Skill Should Do

When reviewing or implementing Swift code changes, this skill should:

1. **Enforce concurrency rules** - Ensure all code follows Swift 6.2 strict concurrency requirements
2. **Check language standards** - Verify use of modern Swift APIs and patterns
3. **Identify violations** - Scan for common mistakes and anti-patterns
4. **Suggest fixes** - Provide guidance on how to correct violations
5. **Maintain consistency** - Ensure code follows repository-wide standards

Use this skill whenever you add, modify, or review Swift code in this repo.

## Information About the Skill

### Workflow

1. Identify the files and changes in scope.
2. Scan for violations of the rules below.
3. Apply fixes or call out deviations explicitly.

### Swift Concurrency Guidelines

#### Core Mental Model

Think in isolation domains rather than threads:

- `MainActor` is the UI lane and must own UI state.
- `actor` types protect their own mutable state.
- `nonisolated` code is shared and cannot touch actor state.
- `Sendable` types are safe to move across domains.

#### Strict Concurrency

Swift 6.2 defaults to `@MainActor` isolation for Views and UI logic. Assume strict isolation checks are active. Everything is `@MainActor` by default.

#### Async and Parallel Work

```swift
func fetchUser(id: Int) async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

async let avatar = fetchImage("avatar.jpg")
async let banner = fetchImage("banner.jpg")
let profile = Profile(avatar: try await avatar, banner: try await banner)
```

#### Tasks and Task Groups

```swift
.task { avatar = await downloadAvatar() }

Task { await saveProfile() }

try await withThrowingTaskGroup(of: Void.self) { group in
    group.addTask { avatar = try await downloadAvatar() }
    group.addTask { bio = try await fetchBio() }
    try await group.waitForAll()
}
```

#### Isolation Domains

```swift
@MainActor
final class ViewModel {
    var items: [Item] = []
}

actor BankAccount {
    var balance: Double = 0
    func deposit(_ amount: Double) { balance += amount }
}
```

#### Approachable Concurrency Settings (Swift 6.2+)

- `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` keeps UI code on the main actor by default.
- `SWIFT_APPROACHABLE_CONCURRENCY = YES` keeps nonisolated async on the caller's actor.

```swift
@concurrent func processLargeFile() async { }
```

#### Sendable

```swift
struct User: Sendable {
    let id: Int
    let name: String
}

final class ThreadSafeCache: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [String: Data] = [:]
}
```

#### Isolation Inheritance

- `Task { }` inherits the current actor.
- `Task.detached { }` does not inherit isolation and should be rare.

#### Background Tasks

Move heavy physics/data work off the main actor using `@concurrent` functions or dedicated actors.

#### Task Management

Cancel long-running tasks on teardown.

#### Common Mistakes to Avoid

- Treating `async` as automatic background work.
- Creating many actors when `@MainActor` is sufficient.
- Using `MainActor.run` when the enclosing function can be annotated.
- Blocking async code with `DispatchSemaphore` or `DispatchGroup.wait()`.
- Spawning unstructured `Task` instances instead of `async let` or task groups.

#### Quick Reference

- `async` and `await` for suspension points.
- `Task { }` for structured async work.
- `actor` for isolated mutable state.
- `@MainActor` for UI-bound work.
- `Sendable` for cross-actor data transfer.

### Swift Language Standards

#### Observable Classes

`@Observable` classes are `@MainActor` by default, so explicit `@MainActor` annotation is not needed.

#### Swift-Native APIs

Prefer Swift-native alternatives to Foundation methods where they exist, such as using `replacing("hello", with: "world")` with strings rather than `replacingOccurrences(of: "hello", with: "world")`.

#### Modern Foundation API

Prefer modern Foundation API, for example `URL.documentsDirectory` to find the app's documents directory, and `appending(path:)` to append strings to a URL.

#### Number Formatting

Never use C-style number formatting such as `Text(String(format: "%.2f", abs(myNumber)))`; always use `Text(abs(change), format: .number.precision(.fractionLength(2)))` instead.

#### Static Member Lookup

Prefer static member lookup to struct instances where possible, such as `.circle` rather than `Circle()`, and `.borderedProminent` rather than `BorderedProminentButtonStyle()`.

#### Modern Concurrency

Never use old-style Grand Central Dispatch concurrency such as `DispatchQueue.main.async()`. If behavior like this is needed, always use modern Swift concurrency.

#### Text Filtering

Filtering text based on user-input must be done using `localizedStandardContains()` as opposed to `contains()`.

#### Force Unwraps

Avoid force unwraps and force `try` unless it is unrecoverable.

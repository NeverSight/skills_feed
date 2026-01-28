---
name: swift-concurrency
description: Guide for building, auditing, and refactoring Swift code using modern concurrency patterns (Swift 6+). This skill should be used when working with async/await, Tasks, actors, MainActor, Sendable types, isolation domains, or when migrating legacy callback/Combine code to structured concurrency. Covers Approachable Concurrency settings, isolated parameters, and common pitfalls.
---

# Swift Concurrency

## Overview

This skill provides guidance for writing thread-safe Swift code using modern concurrency patterns. It covers three main workflows: building new async code, auditing existing code for issues, and refactoring legacy patterns to Swift 6+.

**Core principle**: Isolation is inherited by default. With Approachable Concurrency, code starts on MainActor and propagates through the program automatically. Opt out explicitly when needed.

## Workflow Decision Tree

```
What are you doing?
│
├─► BUILDING new async code
│   └─► See "Building Workflow" below
│
├─► AUDITING existing code
│   └─► See "Auditing Checklist" below
│
└─► REFACTORING legacy code
    └─► See "Refactoring Workflow" below
```

## Building Workflow

When writing new async code, follow this decision process:

### Step 1: Determine Isolation Needs

```
Does this type manage UI state or interact with UI?
│
├─► YES → Mark with @MainActor
│
└─► NO → Does it have mutable state shared across contexts?
         │
         ├─► YES → Consider: Can it live on MainActor anyway?
         │         │
         │         ├─► YES → Use @MainActor (simpler)
         │         │
         │         └─► NO → Use a custom actor (requires justification)
         │
         └─► NO → Leave non-isolated (default with Approachable Concurrency)
```

### Step 2: Design Async Functions

```swift
// PREFER: Inherit caller's isolation (works everywhere)
func fetchData(isolation: isolated (any Actor)? = #isolation) async throws -> Data {
  // Runs on whatever actor the caller is on
}

// USE WHEN: CPU-intensive work that must run in background
@concurrent
func processLargeFile() async -> Result { }

// AVOID: Non-isolated async without explicit choice
func ambiguousAsync() async { } // Where does this run?
```

### Step 3: Handle Parallel Work

```swift
// For known number of independent operations
async let avatar = fetchImage("avatar.jpg")
async let banner = fetchImage("banner.jpg")
let (a, b) = await (avatar, banner)

// For dynamic number of operations
try await withThrowingTaskGroup(of: Void.self) { group in
  for id in userIDs {
    group.addTask { try await fetchUser(id) }
  }
  try await group.waitForAll()
}
```

### Step 4: SwiftUI Integration

```swift
struct ProfileView: View {
  @State private var avatar: Image?

  var body: some View {
    avatar
      .task { avatar = await downloadAvatar() }  // Auto-cancels on disappear
      .task(id: userID) { /* Reloads when userID changes */ }
  }
}

// For user actions
Button("Save") {
  Task { await saveProfile() }  // Inherits MainActor isolation
}
```

## Auditing Checklist

When reviewing Swift concurrency code, check for these issues:

### Critical Issues (Must Fix)

- [ ] **Blocking the cooperative pool**: Look for `DispatchSemaphore.wait()`, `DispatchGroup.wait()`, or similar blocking calls inside async contexts
- [ ] **Data races**: Non-Sendable types crossing isolation boundaries without proper handling
- [ ] **Non-isolated async in non-Sendable types**: These only work from non-isolated contexts

### Common Issues (Should Fix)

- [ ] **Actor overuse**: Custom actors without justification (see "Actor Justification Test" in references)
- [ ] **Unnecessary `MainActor.run`**: Should usually be `@MainActor` on the function instead
- [ ] **Thinking async = background**: Synchronous CPU work inside async functions still blocks
- [ ] **Unstructured Tasks where structured works**: `Task { }` instead of `async let` or `TaskGroup`
- [ ] **Missing cancellation handling**: Long operations should check `Task.isCancelled`

### SwiftUI-Specific

- [ ] **Views not MainActor-isolated**: SwiftUI views should be `@MainActor` (or use `@Observable`)
- [ ] **Accessing @State from detached tasks**: Must hop back to MainActor

### Sendable Compliance

- [ ] **@unchecked Sendable overuse**: Should be rare and justified
- [ ] **Making everything Sendable**: Not all types need to cross boundaries
- [ ] **Non-Sendable closures escaping**: Check closure captures

## Refactoring Workflow

### From Callbacks to async/await

```swift
// BEFORE: Callback-based
func fetchUser(id: Int, completion: @escaping (Result<User, Error>) -> Void) {
  URLSession.shared.dataTask(with: url) { data, _, error in
    if let error { completion(.failure(error)); return }
    // ...
  }.resume()
}

// AFTER: async/await with continuation
func fetchUser(id: Int) async throws -> User {
  try await withCheckedThrowingContinuation { continuation in
    fetchUser(id: id) { result in
      continuation.resume(with: result)
    }
  }
}
```

### From DispatchQueue to Actors

```swift
// BEFORE: Queue-based protection
class BankAccount {
  private let queue = DispatchQueue(label: "account")
  private var _balance: Double = 0

  var balance: Double {
    queue.sync { _balance }
  }

  func deposit(_ amount: Double) {
    queue.async { self._balance += amount }
  }
}

// AFTER: Actor (if truly needs own isolation)
actor BankAccount {
  var balance: Double = 0

  func deposit(_ amount: Double) {
    balance += amount
  }
}

// BETTER: MainActor class (if doesn't need concurrent access)
@MainActor
class BankAccount {
  var balance: Double = 0

  func deposit(_ amount: Double) {
    balance += amount
  }
}
```

### From Combine to AsyncSequence

```swift
// BEFORE: Combine publisher
cancellable = NotificationCenter.default
  .publisher(for: .userDidLogin)
  .sink { notification in /* ... */ }

// AFTER: AsyncSequence
for await _ in NotificationCenter.default.notifications(named: .userDidLogin) {
  // Handle notification
}
```

## Quick Reference

| Keyword | Purpose |
|---------|---------|
| `async` | Function can suspend |
| `await` | Suspension point |
| `Task { }` | Start async work, inherits isolation |
| `Task.detached { }` | Start async work, no inheritance |
| `@MainActor` | Runs on main thread |
| `actor` | Type with isolated mutable state |
| `nonisolated` | Opts out of actor isolation |
| `nonisolated(nonsending)` | Inherits caller's isolation |
| `@concurrent` | Always run on background (Swift 6.2+) |
| `Sendable` | Safe to cross isolation boundaries |
| `sending` | One-way transfer of non-Sendable |
| `async let` | Start parallel work |
| `TaskGroup` | Dynamic parallel work |

## Approachable Concurrency Settings (Swift 6.2+)

For new Xcode 26+ projects, these are enabled by default:

```
SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor
SWIFT_APPROACHABLE_CONCURRENCY = YES
```

Effects:
- Everything runs on MainActor unless explicitly marked otherwise
- `nonisolated async` functions stay on caller's actor instead of hopping to background
- Sendable errors become much rarer

## Resources

For detailed technical reference, consult:

- `references/fundamentals.md` - async/await, Tasks, structured concurrency
- `references/isolation.md` - Actors, MainActor, isolation domains, inheritance
- `references/sendable.md` - Sendable protocol, non-Sendable patterns, isolated parameters
- `references/common-mistakes.md` - Detailed examples of what to avoid
- `references/glossary.md` - Complete terminology reference

**Search patterns for references:**
- Isolation: `grep -i "isolation\|actor\|mainactor\|nonisolated"`
- Sendable: `grep -i "sendable\|sending\|boundary"`
- Tasks: `grep -i "task\|taskgroup\|async let\|structured"`

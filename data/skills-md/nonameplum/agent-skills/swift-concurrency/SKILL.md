---
name: swift-concurrency
description: Expert guidance on Swift Concurrency concepts. Use when working with async/await, Tasks, actors, MainActor, Sendable, isolation domains, or debugging concurrency compiler errors. Helps write safe concurrent Swift code.
---

Source: https://github.com/pepicrft/fuckingapproachableswiftconcurrency

# Swift Concurrency Skill

This skill provides expert guidance on Swift's concurrency system based on the mental models from [Fucking Approachable Swift Concurrency](https://fuckingapproachableswiftconcurrency.com).

## Core Mental Model: The Office Building

Think of your app as an office building where **isolation domains** are private offices with locks:

- **MainActor** = Front desk (handles all UI interactions, only one exists)
- **actor** types = Department offices (Accounting, Legal, HR - each protects its own data)
- **nonisolated** code = Hallways (shared space, no private documents)
- **Sendable** types = Photocopies (safe to share between offices)
- **Non-Sendable** types = Original documents (must stay in one office)

You can't barge into someone's office. You knock (`await`) and wait.

## Async/Await

An `async` function can pause. Use `await` to suspend until work finishes:

```swift
func fetchUser(id: Int) async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}
```

For parallel work, use `async let`:

```swift
async let avatar = fetchImage("avatar.jpg")
async let banner = fetchImage("banner.jpg")
return Profile(avatar: try await avatar, banner: try await banner)
```

## Tasks

A `Task` is a unit of async work you can manage:

```swift
// SwiftUI - cancels when view disappears
.task { avatar = await downloadAvatar() }

// Manual task creation
Task { await saveProfile() }

// Parallel work with TaskGroup
try await withThrowingTaskGroup(of: Void.self) { group in
    group.addTask { avatar = try await downloadAvatar() }
    group.addTask { bio = try await fetchBio() }
    try await group.waitForAll()
}
```

Child tasks in a group: cancellation propagates, errors cancel siblings, waits for all to complete.

## Isolation Domains

Swift asks "who can access this data?" not "which thread?". Three isolation domains:

### 1. MainActor

For UI. Everything UI-related should be here:

```swift
@MainActor
class ViewModel {
    var items: [Item] = []  // Protected by MainActor
}
```

### 2. Actors

Protect their own mutable state with exclusive access:

```swift
actor BankAccount {
    var balance: Double = 0
    func deposit(_ amount: Double) { balance += amount }
}

await account.deposit(100)  // Must await from outside
```

### 3. Nonisolated

Opts out of actor isolation. Cannot access actor's protected state:

```swift
actor BankAccount {
    nonisolated func bankName() -> String { "Acme Bank" }
}
let name = account.bankName()  // No await needed
```

## Approachable Concurrency (Swift 6.2+)

Two build settings that simplify the mental model:

- **SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor**: Everything runs on MainActor unless you say otherwise
- **SWIFT_APPROACHABLE_CONCURRENCY = YES**: nonisolated async functions stay on caller's actor

```swift
// Runs on MainActor (default)
func updateUI() async { }

// Runs on background (opt-in)
@concurrent func processLargeFile() async { }
```

## Sendable

Marks types safe to pass across isolation boundaries:

```swift
// Sendable - value type, each gets a copy
struct User: Sendable {
    let id: Int
    let name: String
}

// Non-Sendable - mutable class state
class Counter {
    var count = 0
}
```

Automatically Sendable:
- Structs/enums with only Sendable properties
- Actors (protect their own state)
- @MainActor types (MainActor serializes access)

For thread-safe classes with internal synchronization:

```swift
final class ThreadSafeCache: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [String: Data] = [:]
}
```

## Isolation Inheritance

With Approachable Concurrency, isolation flows from MainActor through your code:

- **Functions**: Inherit caller's isolation unless explicitly marked
- **Closures**: Inherit from context where defined
- **Task { }**: Inherits actor isolation from creation site
- **Task.detached { }**: No inheritance (rarely needed)

## Common Mistakes to Avoid

### 1. Thinking async = background

```swift
// Still blocks main thread!
@MainActor func slowFunction() async {
    let result = expensiveCalculation()  // Synchronous = blocking
}
// Fix: Use @concurrent for CPU-heavy work
```

### 2. Creating too many actors

Most things can live on MainActor. Only create actors when you have shared mutable state that can't be on MainActor.

### 3. Making everything Sendable

Not everything needs to cross boundaries. Step back and ask if data actually moves between isolation domains.

### 4. Using MainActor.run unnecessarily

```swift
// Unnecessary
await MainActor.run { self.data = data }

// Better - annotate the function
@MainActor func loadData() async { self.data = await fetchData() }
```

### 5. Blocking the cooperative thread pool

Never use DispatchSemaphore, DispatchGroup.wait() in async code. Risks deadlock.

### 6. Creating unnecessary Tasks

```swift
// Bad - unstructured
Task { await fetchUsers() }
Task { await fetchPosts() }

// Good - structured concurrency
async let users = fetchUsers()
async let posts = fetchPosts()
await (users, posts)
```

## Quick Reference

| Keyword | Purpose |
|---------|---------|
| `async` | Function can pause |
| `await` | Pause here until done |
| `Task { }` | Start async work, inherits context |
| `Task.detached { }` | Start async work, no context |
| `@MainActor` | Runs on main thread |
| `actor` | Type with isolated mutable state |
| `nonisolated` | Opts out of actor isolation |
| `Sendable` | Safe to pass between isolation domains |
| `@concurrent` | Always run on background (Swift 6.2+) |
| `async let` | Start parallel work |
| `TaskGroup` | Dynamic parallel work |

## When the Compiler Complains

Trace the isolation: Where did it come from? Where is code trying to run? What data crosses a boundary?

The answer is usually obvious once you ask the right question.

## Further Reading

- [Matt Massicotte's Blog](https://www.massicotte.org/) - The source of these mental models
- [Swift Concurrency Documentation](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/)
- [WWDC21: Meet async/await](https://developer.apple.com/videos/play/wwdc2021/10132/)
- [WWDC21: Protect mutable state with actors](https://developer.apple.com/videos/play/wwdc2021/10133/)

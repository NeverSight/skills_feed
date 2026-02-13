---
name: concurrency-patterns
description: "Expert Swift concurrency decisions: async let vs TaskGroup selection, actor isolation boundaries, @MainActor placement strategies, Sendable conformance judgment calls, and structured vs unstructured task trade-offs. Use when designing concurrent code, debugging data races, or choosing between concurrency patterns. Trigger keywords: async, await, actor, Task, TaskGroup, @MainActor, Sendable, concurrency, data race, isolation, structured concurrency, continuation"
version: "3.0.0"
---

# Concurrency Patterns — Expert Decisions

Expert decision frameworks for Swift concurrency choices. Claude knows async/await syntax — this skill provides judgment calls for pattern selection and isolation boundaries.

---

## Decision Trees

### async let vs TaskGroup

```
Is the number of concurrent operations known at compile time?
├─ YES (2-5 fixed operations)
│  └─ async let
│     async let user = fetchUser()
│     async let posts = fetchPosts()
│     let (user, posts) = await (try user, try posts)
│
└─ NO (dynamic count, array of IDs)
   └─ TaskGroup
      try await withThrowingTaskGroup(of: User.self) { group in
          for id in userIds { group.addTask { ... } }
      }
```

**async let gotcha**: All `async let` values MUST be awaited before scope ends. Forgetting to await silently cancels the task — no error, just missing data.

### Task vs Task.detached

```
Does the new task need to inherit context?
├─ YES (inherit priority, actor, task-locals)
│  └─ Task { }
│     Example: Continue work on same actor
│
└─ NO (fully independent execution)
   └─ Task.detached { }
      Example: Background processing that shouldn't block UI
```

**The trap**: `Task { }` inside `@MainActor` runs on MainActor. For truly background work, use `Task.detached(priority:)`.

### Actor vs Class with Lock

```
Is the mutable state accessed from async contexts?
├─ YES → Actor (compiler-enforced isolation)
│
└─ NO → Is it performance-critical?
   ├─ YES → Class with lock (less overhead)
   │  └─ Consider @unchecked Sendable if crossing boundaries
   │
   └─ NO → Actor (safer, cleaner)
```

**When actors lose**: High-contention scenarios where lock granularity matters. Actor methods are fully isolated — can't lock just part of the state.

### Sendable Conformance

```
Is the type crossing concurrency boundaries?
├─ NO → Don't add Sendable
│
└─ YES → What kind of type?
   ├─ Struct with only Sendable properties
   │  └─ Implicit Sendable (or add explicit)
   │
   ├─ Class with immutable state
   │  └─ Add Sendable, make let-only
   │
   ├─ Class with mutable state
   │  └─ Is it manually thread-safe?
   │     ├─ YES → @unchecked Sendable
   │     └─ NO → Convert to actor
   │
   └─ Closure
      └─ Mark @Sendable, capture only Sendable values
```

---

## NEVER Do

### Task & Structured Concurrency

**NEVER** create unstructured tasks for parallel work that should be grouped:
```swift
// ❌ No way to wait for completion, handle errors, or cancel
func loadData() async {
    Task { try? await fetchUsers() }
    Task { try? await fetchPosts() }
    // Returns immediately, tasks orphaned
}

// ✅ Structured — errors propagate, cancellation works
func loadData() async throws {
    try await withThrowingTaskGroup(of: Void.self) { group in
        group.addTask { try await fetchUsers() }
        group.addTask { try await fetchPosts() }
    }
}
```

**NEVER** assume `Task.cancel()` stops execution immediately:
```swift
// ❌ Assumes cancellation is synchronous
task.cancel()
let result = task.value  // Task may still be running!

// ✅ Cancellation is cooperative — code must check
func longOperation() async throws {
    for item in items {
        try Task.checkCancellation()  // Or check Task.isCancelled
        await process(item)
    }
}
```

**NEVER** forget that async let bindings auto-cancel if not awaited:
```swift
// ❌ profileImage is SILENTLY CANCELLED
func loadUser() async throws -> User {
    async let user = fetchUser()
    async let profileImage = fetchImage()  // Never awaited!
    return try await user  // profileImage cancelled, no error
}

// ✅ Await all async let bindings
func loadUser() async throws -> (User, UIImage?) {
    async let user = fetchUser()
    async let profileImage = fetchImage()
    return try await (user, profileImage)  // Both awaited
}
```

### Actor Isolation

**NEVER** ignore actor reentrancy:
```swift
// ❌ State can change during suspension
actor BankAccount {
    var balance: Double = 100

    func transferAll() async throws {
        let amount = balance  // Capture balance
        try await sendMoney(amount)  // Suspension point!
        balance = 0  // Balance might have changed since capture!
    }
}

// ✅ Check state AFTER suspension
actor BankAccount {
    var balance: Double = 100

    func transferAll() async throws {
        let amount = balance
        try await sendMoney(amount)
        // Re-check or use atomic operation
        guard balance >= amount else {
            throw BankError.balanceChanged
        }
        balance -= amount
    }
}
```

**NEVER** expose actor state as reference types:
```swift
// ❌ Array reference escapes actor isolation
actor Cache {
    var items: [Item] = []

    func getItems() -> [Item] {
        items  // Returns reference that can be mutated outside!
    }
}

// ✅ Return copy or use value types
actor Cache {
    private var items: [Item] = []

    func getItems() -> [Item] {
        Array(items)  // Explicit copy
    }
}
```

**NEVER** use `nonisolated` to bypass safety without understanding implications:
```swift
// ❌ Dangerous — defeats actor protection
actor DataManager {
    var cache: [String: Data] = [:]

    nonisolated func unsafeAccess() -> [String: Data] {
        cache  // DATA RACE — accessing actor state without isolation!
    }
}

// ✅ nonisolated only for immutable or independent state
actor DataManager {
    let id = UUID()  // Immutable — safe

    nonisolated var identifier: String {
        id.uuidString  // Safe — accessing immutable state
    }
}
```

### @MainActor

**NEVER** access @Published from background without MainActor:
```swift
// ❌ Undefined behavior — may crash, may corrupt
Task.detached {
    viewModel.isLoading = false  // Background thread!
}

// ✅ Explicit MainActor
Task { @MainActor in
    viewModel.isLoading = false
}
// Or mark entire ViewModel as @MainActor
```

**NEVER** block MainActor with synchronous work:
```swift
// ❌ UI freezes during heavy computation
@MainActor
func processData() {
    let result = heavyComputation(data)  // Blocks UI!
    display(result)
}

// ✅ Offload to detached task
@MainActor
func processData() async {
    let result = await Task.detached {
        heavyComputation(data)
    }.value
    display(result)  // Back on MainActor
}
```

### Continuations

**NEVER** resume continuation more than once:
```swift
// ❌ CRASHES — continuation resumed twice
func fetchAsync() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        fetch { result in
            continuation.resume(returning: result)
        }
        fetch { result in  // Oops, called again!
            continuation.resume(returning: result)  // CRASH!
        }
    }
}

// ✅ Ensure exactly-once resumption
func fetchAsync() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        var hasResumed = false
        fetch { result in
            guard !hasResumed else { return }
            hasResumed = true
            continuation.resume(returning: result)
        }
    }
}
```

**NEVER** forget to resume continuation:
```swift
// ❌ Task hangs forever if error path doesn't resume
func fetchAsync() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        fetch { data, error in
            if let data = data {
                continuation.resume(returning: data)
            }
            // Missing else! Continuation never resumed if error
        }
    }
}

// ✅ Handle all paths
func fetchAsync() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        fetch { data, error in
            if let error = error {
                continuation.resume(throwing: error)
            } else if let data = data {
                continuation.resume(returning: data)
            } else {
                continuation.resume(throwing: FetchError.noData)
            }
        }
    }
}
```

---

## Essential Patterns

### Task-Local Values

```swift
enum RequestContext {
    @TaskLocal static var requestId: String?
    @TaskLocal static var userId: String?
}

// Set context for entire task tree
func handleRequest() async {
    await RequestContext.$requestId.withValue(UUID().uuidString) {
        await RequestContext.$userId.withValue(currentUserId) {
            await processRequest()  // All child tasks inherit context
        }
    }
}

// Access anywhere in task tree
func logEvent(_ message: String) {
    let requestId = RequestContext.requestId ?? "unknown"
    logger.info("[\(requestId)] \(message)")
}
```

### Cancellation-Aware Loops

```swift
func processItems(_ items: [Item]) async throws {
    for item in items {
        // Check at start of each iteration
        try Task.checkCancellation()

        // Or handle gracefully without throwing
        guard !Task.isCancelled else {
            await saveProgress(items: processedItems)
            return
        }

        await process(item)
    }
}
```

### AsyncStream from Delegate

```swift
func locationUpdates() -> AsyncStream<CLLocation> {
    AsyncStream { continuation in
        let delegate = LocationDelegate { location in
            continuation.yield(location)
        }

        continuation.onTermination = { @Sendable _ in
            delegate.stop()
        }

        delegate.start()
    }
}
```

---

## Quick Reference

### Concurrency Pattern Selection

| Pattern | Use When | Gotcha |
|---------|----------|--------|
| `async let` | 2-5 known parallel operations | Must await all bindings |
| `TaskGroup` | Dynamic number of operations | Results arrive out of order |
| `Task { }` | Fire-and-forget with context | Inherits actor isolation |
| `Task.detached` | True background work | No context inheritance |
| `actor` | Shared mutable state | Reentrancy on suspension |

### Sendable Quick Check

| Type | Sendable? |
|------|-----------|
| Value types with Sendable properties | ✅ Implicit |
| `let`-only classes | ✅ Add conformance |
| Mutable classes with internal locking | ⚠️ @unchecked Sendable |
| Mutable classes without locking | ❌ Use actor instead |
| Closures | ✅ If marked @Sendable |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| `Task { }` everywhere | Losing structured concurrency | Use TaskGroup |
| `@unchecked Sendable` on mutable class | Potential data race | Use actor or add locking |
| `nonisolated` accessing mutable state | Data race | Remove nonisolated |
| Continuation without all-paths handling | Potential hang | Handle every code path |
| `Task.detached` for everything | Losing priority/cancellation | Use structured `Task { }` |

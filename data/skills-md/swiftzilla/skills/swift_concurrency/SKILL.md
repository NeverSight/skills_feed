---
name: swift_concurrency
description: Swift modern concurrency with async/await, Task, Actor, Swift 6 strict mode, Sendable, and structured concurrency patterns.
license: Proprietary
compatibility: Swift 5.5+
metadata:
  version: "2.0"
  author: SwiftZilla
  website: https://swiftzilla.dev
---

# Swift Concurrency

This skill covers Swift's modern concurrency features from Swift 5.5 through Swift 6, including async/await, structured concurrency, actors, and Swift 6's strict data-race safety.

## Overview

Swift's modern concurrency model provides a safer, more intuitive way to write asynchronous code. Swift 6 takes this further with **compile-time data-race safety**, turning potential concurrency bugs into compiler errors.

## Available References

### Swift 6 & Strict Concurrency
- [Swift 6 Strict Mode](./references/swift6_strict_mode.md) - Complete concurrency checking, data race prevention
- [Sendable Protocol](./references/sendable.md) - Sendable conformance, @Sendable closures, thread safety
- [Isolation & Actors](./references/isolation.md) - @MainActor, global actors, region-based isolation

### Core Concurrency
- [Async/Await](./references/async_await.md) - Asynchronous functions, Task, TaskGroup, Actor basics

## Swift 6 Highlights

### Strict Concurrency by Default

Swift 6 enforces data-race safety at compile time:

```swift
// ❌ Compile-time error in Swift 6
var globalCounter = 0

func increment() {
    globalCounter += 1  // Error: concurrent access
}

// ✅ Safe with actor isolation
actor Counter {
    private var value = 0
    func increment() { value += 1 }
}
```

### Sendable Protocol

Mark types safe to share across concurrency boundaries:

```swift
struct User: Sendable {
    let id: Int
    let name: String
}

@Sendable func process() async {
    // Captures must be Sendable
}
```

### MainActor & Global Actors

```swift
@MainActor
class ViewModel: ObservableObject {
    @Published var items = [Item]()
}

@globalActor
actor DatabaseActor {
    static let shared = DatabaseActor()
    private init() {}
}
```

## Quick Reference

### Async/Await Basics

```swift
func fetchData() async throws -> Data {
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}
```

### Swift 6 Migration Checklist

- [ ] Enable Swift 6 language mode
- [ ] Enable strict concurrency checking
- [ ] Wrap global mutable state in actors
- [ ] Add Sendable conformance to types
- [ ] Fix non-Sendable captures in @Sendable closures
- [ ] Isolate UI code with @MainActor
- [ ] Audit third-party dependencies

### Running Async Code

```swift
// Fire-and-forget
Task {
    let result = await asyncOperation()
}

// With priority
Task(priority: .background) {
    await heavyComputation()
}

// With cancellation
let task = Task {
    try await longRunningOperation()
}
task.cancel()
```

### Concurrent Operations

```swift
// Async let (parallel await)
async let task1 = fetchUser()
async let task2 = fetchSettings()
let (user, settings) = try await (task1, task2)

// TaskGroup
try await withThrowingTaskGroup(of: Item.self) { group in
    for id in ids {
        group.addTask { try await fetchItem(id: id) }
    }
    return try await group.reduce(into: []) { $0.append($1) }
}
```

### Actor Thread Safety

```swift
actor BankAccount {
    private var balance: Double = 0
    
    func deposit(_ amount: Double) {
        balance += amount
    }
    
    func getBalance() -> Double {
        return balance
    }
}

let account = BankAccount()
await account.deposit(100)
```

### Isolation Boundaries

```swift
// Crossing isolation boundaries
@MainActor
func updateUI() async {
    // On main thread
    let data = await fetchData()  // Switch to non-isolated
    label.text = data  // Back to main thread
}

// Region transfer
func process() async {
    let data = Data()  // Disconnected
    await save(data)   // Transfer to actor
    // ❌ Can't use data here anymore
}
```

## Swift 6 vs Swift 5.x

| Feature | Swift 5.x | Swift 6 |
|---------|-----------|---------|
| Concurrency checking | Warnings | **Errors** |
| Data race safety | Runtime | **Compile-time** |
| Sendable enforcement | Opt-in | **Required** |
| Global variable safety | Warning | **Error** |
| Strict mode | Experimental | **Default** |

## Best Practices

### Swift 6 Best Practices

1. **Enable Swift 6 mode early** - Start migration now
2. **Use actors for shared state** - Default to actors over locks
3. **Design Sendable types** - Make types Sendable from the start
4. **Isolate UI with @MainActor** - All UI code on main thread
5. **Respect isolation regions** - Don't use values after transfer
6. **Leverage compile-time safety** - Let compiler catch data races
7. **Create domain actors** - Custom global actors for heavy work

### General Concurrency

1. **Prefer async/await** - Over completion handlers
2. **Use structured concurrency** - Clear task hierarchies
3. **Handle cancellation** - Check Task.isCancelled
4. **Use value types** - Immutable data is thread-safe
5. **Avoid shared mutable state** - Or protect with actors

## Migration from Completion Handlers

```swift
// Before (Swift 5)
func fetchUser(completion: @escaping (Result<User, Error>) -> Void) {
    URLSession.shared.dataTask(with: url) { data, response, error in
        // Handle result
        completion(result)
    }.resume()
}

// After (Swift 6)
func fetchUser() async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}
```

## Common Swift 6 Errors

| Error | Quick Fix |
|-------|-----------|
| Concurrent access to global | Wrap in actor |
| Non-Sendable in @Sendable | Make type Sendable |
| Actor isolation violation | Add await or change isolation |
| Use after transfer | Use before transfer or copy value |
| Main actor isolation | Add @MainActor annotation |

## Resources

- **Swift Evolution:** https://github.com/apple/swift-evolution
- **SE-0412:** Strict concurrency for global variables
- **SE-0471:** SerialExecutor isolation checking
- **SE-0430:** Sending parameters
- **SE-0414:** Region-based isolation
- **Apple Docs:** https://developer.apple.com/documentation/swift/concurrency
- **SwiftZilla:** https://swiftzilla.dev

## For More Information

Each reference file contains detailed information, code examples, and best practices for specific topics. Visit https://swiftzilla.dev for comprehensive Swift concurrency documentation.

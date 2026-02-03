---
name: swift-concurrency
description: Swift 6 strict concurrency model, async/await, actors, @MainActor, Sendable, and thread safety. Use when user asks about concurrency, async/await, actors, MainActor, thread safety, data races, or migrating from GCD to structured concurrency.
allowed-tools: Bash, Read, Write, Edit
---

# Swift Concurrency

Comprehensive guide to Swift 6 strict concurrency, async/await patterns, actors, and modern thread-safe programming for iOS 26 and macOS Tahoe.

## Prerequisites

- Swift 6.x with strict concurrency enabled
- Xcode 26+

---

## Swift 6 Concurrency Model

### Complete Concurrency Checking

Swift 6 enables **complete data-race safety** by default. The compiler statically verifies that your code is free from data races.

```swift
// In Package.swift
.target(
    name: "MyApp",
    swiftSettings: [
        .swiftLanguageMode(.v6)
    ]
)
```

### Key Concepts

1. **Isolation Domains** - Code is isolated to specific actors
2. **Sendable** - Types that can safely cross isolation boundaries
3. **Actor Isolation** - Data protected by actors
4. **MainActor** - Main thread isolation for UI

---

## Async/Await Basics

### Async Functions

```swift
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Calling async functions
func loadUserProfile() async {
    do {
        let user = try await fetchUser(id: 123)
        print("Loaded: \(user.name)")
    } catch {
        print("Failed: \(error)")
    }
}
```

### Async Properties

```swift
struct ImageLoader {
    var url: URL

    var image: UIImage {
        get async throws {
            let (data, _) = try await URLSession.shared.data(from: url)
            guard let image = UIImage(data: data) else {
                throw ImageError.invalidData
            }
            return image
        }
    }
}

// Usage
let loader = ImageLoader(url: imageURL)
let image = try await loader.image
```

### Async Sequences

```swift
func processLines(from url: URL) async throws {
    for try await line in url.lines {
        print(line)
    }
}

// Custom async sequence
struct Counter: AsyncSequence {
    typealias Element = Int
    let limit: Int

    struct AsyncIterator: AsyncIteratorProtocol {
        var current = 0
        let limit: Int

        mutating func next() async -> Int? {
            guard current < limit else { return nil }
            defer { current += 1 }
            try? await Task.sleep(for: .seconds(1))
            return current
        }
    }

    func makeAsyncIterator() -> AsyncIterator {
        AsyncIterator(limit: limit)
    }
}

// Usage
for await count in Counter(limit: 5) {
    print(count)  // Prints 0, 1, 2, 3, 4 with 1s delays
}
```

---

## Task Management

### Creating Tasks

```swift
// Unstructured task - runs independently
let task = Task {
    await performWork()
}

// Detached task - no inherited context
let detached = Task.detached {
    await performBackgroundWork()
}

// Task with priority
let highPriority = Task(priority: .high) {
    await performUrgentWork()
}

// Cancel a task
task.cancel()

// Check cancellation
func performWork() async throws {
    for item in items {
        try Task.checkCancellation()  // Throws if cancelled
        await process(item)
    }
}
```

### Task Groups

```swift
func fetchAllUsers(ids: [Int]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)
            }
        }

        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}

// With result ordering
func fetchUsersOrdered(ids: [Int]) async throws -> [User] {
    try await withThrowingTaskGroup(of: (Int, User).self) { group in
        for (index, id) in ids.enumerated() {
            group.addTask {
                (index, try await fetchUser(id: id))
            }
        }

        var results = [(Int, User)]()
        for try await result in group {
            results.append(result)
        }

        return results.sorted { $0.0 < $1.0 }.map(\.1)
    }
}
```

### Discarding Task Group (Swift 6)

```swift
// For fire-and-forget parallel tasks
await withDiscardingTaskGroup { group in
    for url in urls {
        group.addTask {
            await prefetchImage(from: url)
        }
    }
    // Results are automatically discarded
}
```

---

## Actors

### Basic Actor

```swift
actor BankAccount {
    private var balance: Decimal = 0

    func deposit(_ amount: Decimal) {
        balance += amount
    }

    func withdraw(_ amount: Decimal) throws {
        guard balance >= amount else {
            throw BankError.insufficientFunds
        }
        balance -= amount
    }

    func getBalance() -> Decimal {
        balance
    }
}

// Usage - all calls are async
let account = BankAccount()
await account.deposit(100)
let balance = await account.getBalance()
```

### Nonisolated Members

```swift
actor DataManager {
    private var cache: [String: Data] = [:]

    // Isolated - requires await
    func store(_ data: Data, for key: String) {
        cache[key] = data
    }

    // Nonisolated - can be called synchronously
    nonisolated let identifier = UUID()

    nonisolated func createKey(for name: String) -> String {
        "\(identifier)-\(name)"
    }
}

let manager = DataManager()
let key = manager.createKey(for: "test")  // No await needed
await manager.store(data, for: key)        // Requires await
```

### Actor Reentrancy

```swift
actor ImageCache {
    private var cache: [URL: UIImage] = [:]
    private var inProgress: [URL: Task<UIImage, Error>] = [:]

    func image(for url: URL) async throws -> UIImage {
        // Check cache first
        if let cached = cache[url] {
            return cached
        }

        // Check if already loading
        if let existing = inProgress[url] {
            return try await existing.value
        }

        // Start new load
        let task = Task {
            let (data, _) = try await URLSession.shared.data(from: url)
            let image = UIImage(data: data)!
            return image
        }

        inProgress[url] = task

        do {
            let image = try await task.value
            cache[url] = image
            inProgress[url] = nil
            return image
        } catch {
            inProgress[url] = nil
            throw error
        }
    }
}
```

---

## @MainActor

### Class-Level Isolation

```swift
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var isLoading = false
    @Published var error: Error?

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }

        do {
            items = try await fetchItems()
        } catch {
            self.error = error
        }
    }

    // Nonisolated for background work
    nonisolated func fetchItems() async throws -> [Item] {
        let url = URL(string: "https://api.example.com/items")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode([Item].self, from: data)
    }
}
```

### Method-Level Isolation

```swift
class DataProcessor {
    func processData() async -> ProcessedData {
        // Runs on background
        let result = await heavyComputation()
        return result
    }

    @MainActor
    func updateUI(with data: ProcessedData) {
        // Runs on main thread
        label.text = data.summary
    }
}
```

### MainActor.run

```swift
func performBackgroundWork() async {
    let result = await processLargeDataset()

    // Jump to main actor for UI update
    await MainActor.run {
        updateProgressView(with: result)
    }
}
```

---

## Sendable Protocol

### Sendable Types

```swift
// Value types are implicitly Sendable
struct Point: Sendable {
    var x: Double
    var y: Double
}

// Immutable classes can be Sendable
final class Configuration: Sendable {
    let apiKey: String
    let baseURL: URL

    init(apiKey: String, baseURL: URL) {
        self.apiKey = apiKey
        self.baseURL = baseURL
    }
}

// Actors are implicitly Sendable
actor Counter: Sendable {
    var count = 0
}
```

### @unchecked Sendable

```swift
// Use carefully for types with internal synchronization
final class ThreadSafeCache: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [String: Any] = [:]

    func get(_ key: String) -> Any? {
        lock.lock()
        defer { lock.unlock() }
        return storage[key]
    }

    func set(_ key: String, value: Any) {
        lock.lock()
        defer { lock.unlock() }
        storage[key] = value
    }
}
```

### Sendable Closures

```swift
// @Sendable closures can be sent across isolation boundaries
func performAsync(_ work: @Sendable @escaping () async -> Void) {
    Task {
        await work()
    }
}

// Capturing in Sendable closures
func processItems(_ items: [Item]) {
    // items must be Sendable
    Task { @Sendable in
        for item in items {
            await process(item)
        }
    }
}
```

---

## Swift 6.2 Improvements

### Default Isolation

```swift
// New in Swift 6.2: Default to main actor isolation
// In Package.swift or build settings:
// -default-isolation MainActor

// Or per-file:
@MainActor
extension MyView {
    // All methods here are MainActor-isolated by default
}
```

### Observations Async Sequence

```swift
import Observation

@Observable
class Model {
    var count = 0
}

// Stream changes with async sequence
func observeModel(_ model: Model) async {
    for await _ in model.observations(of: \.count) {
        print("Count changed to: \(model.count)")
    }
}
```

### Region-Based Isolation (SE-0414)

```swift
// Compiler can now reason about value regions
func processData() async {
    var data = [1, 2, 3]

    // Compiler knows data doesn't escape
    await withTaskGroup(of: Void.self) { group in
        for item in data {
            group.addTask {
                print(item)
            }
        }
    }

    // Safe to mutate after task group completes
    data.append(4)
}
```

---

## Common Pitfalls

### Pitfall 1: DispatchQueue in Swift 6

```swift
// WRONG - flagged as unsafe in Swift 6
DispatchQueue.main.async {
    self.updateUI()
}

// CORRECT - use MainActor
await MainActor.run {
    self.updateUI()
}

// Or make the enclosing context @MainActor
@MainActor
func handleResult() {
    updateUI()  // Already on main actor
}
```

### Pitfall 2: Combine without Isolation

```swift
// WRONG - closure isolation unclear
publisher
    .sink { value in
        self.items = value  // Data race potential
    }
    .store(in: &cancellables)

// CORRECT - explicit isolation
publisher
    .receive(on: DispatchQueue.main)
    .sink { [weak self] value in
        Task { @MainActor in
            self?.items = value
        }
    }
    .store(in: &cancellables)
```

### Pitfall 3: Non-Sendable Captures

```swift
// WRONG - UIViewController not Sendable
func saveData() {
    let vc = self  // UIViewController
    Task {
        await save()
        vc.showSuccess()  // Error: captured non-Sendable
    }
}

// CORRECT - use weak capture and MainActor
func saveData() {
    Task { [weak self] in
        await save()
        await MainActor.run {
            self?.showSuccess()
        }
    }
}
```

### Pitfall 4: Actor Reentrancy Surprises

```swift
actor DataStore {
    var items: [Item] = []

    func addItem(_ item: Item) async {
        // State before await
        let countBefore = items.count

        await saveToDatabase(item)

        // WARNING: items may have changed during await!
        items.append(item)  // Could cause duplicates
    }

    // BETTER - capture state carefully
    func addItemSafely(_ item: Item) async {
        items.append(item)
        let itemsCopy = items
        await saveToDatabase(itemsCopy)
    }
}
```

---

## Migration from GCD

### Before (GCD)

```swift
func loadData(completion: @escaping (Result<Data, Error>) -> Void) {
    DispatchQueue.global().async {
        do {
            let data = try self.fetchDataSync()
            DispatchQueue.main.async {
                completion(.success(data))
            }
        } catch {
            DispatchQueue.main.async {
                completion(.failure(error))
            }
        }
    }
}
```

### After (Async/Await)

```swift
func loadData() async throws -> Data {
    try await fetchData()
}

// Usage
Task {
    do {
        let data = try await loadData()
        // Already on calling context
    } catch {
        // Handle error
    }
}
```

### Bridging Completion Handlers

```swift
// Wrap completion handler API
func fetchLegacyData() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        legacyFetchData { result in
            switch result {
            case .success(let data):
                continuation.resume(returning: data)
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }
    }
}

// Important: Only call resume ONCE
func fetchWithTimeout() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        var hasResumed = false

        legacyFetch { data in
            guard !hasResumed else { return }
            hasResumed = true
            continuation.resume(returning: data)
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + 10) {
            guard !hasResumed else { return }
            hasResumed = true
            continuation.resume(throwing: TimeoutError())
        }
    }
}
```

---

## AsyncStream

### Creating Streams

```swift
func notifications() -> AsyncStream<Notification> {
    AsyncStream { continuation in
        let observer = NotificationCenter.default.addObserver(
            forName: .customNotification,
            object: nil,
            queue: .main
        ) { notification in
            continuation.yield(notification)
        }

        continuation.onTermination = { _ in
            NotificationCenter.default.removeObserver(observer)
        }
    }
}

// Usage
for await notification in notifications() {
    print("Received: \(notification)")
}
```

### Throwing Streams

```swift
func dataStream(from url: URL) -> AsyncThrowingStream<Data, Error> {
    AsyncThrowingStream { continuation in
        let task = URLSession.shared.dataTask(with: url) { data, _, error in
            if let error = error {
                continuation.finish(throwing: error)
                return
            }
            if let data = data {
                continuation.yield(data)
            }
            continuation.finish()
        }
        task.resume()

        continuation.onTermination = { _ in
            task.cancel()
        }
    }
}
```

---

## Testing Concurrent Code

```swift
import Testing

@Test("Concurrent counter increments correctly")
func concurrentCounter() async {
    let counter = Counter()

    await withTaskGroup(of: Void.self) { group in
        for _ in 0..<1000 {
            group.addTask {
                await counter.increment()
            }
        }
    }

    let final = await counter.value
    #expect(final == 1000)
}

@Test(.serialized, "Tests that must run sequentially")
func sequentialTest() async {
    // Use .serialized trait for tests not ready for parallel
}
```

---

## Best Practices

1. **Prefer structured concurrency** - Use task groups over detached tasks
2. **Make types Sendable** - Design for thread safety from the start
3. **Use actors for shared mutable state** - Don't use locks in Swift 6
4. **Isolate UI code to MainActor** - Use @MainActor for ViewModels
5. **Handle cancellation** - Check `Task.isCancelled` in long operations
6. **Avoid async in tight loops** - Batch work when possible
7. **Test concurrent code** - Use `.serialized` trait when needed

---

## Official Resources

- [Swift Concurrency Documentation](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/)
- [Migrating to Swift 6](https://www.swift.org/migration/documentation/migrationguide/)
- [SE-0414: Region-Based Isolation](https://github.com/apple/swift-evolution/blob/main/proposals/0414-region-based-isolation.md)
- [WWDC23: Beyond the basics of structured concurrency](https://developer.apple.com/videos/play/wwdc2023/10170/)

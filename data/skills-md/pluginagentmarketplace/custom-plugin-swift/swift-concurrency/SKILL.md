---
name: swift-concurrency
description: Master Swift concurrency - async/await, actors, structured concurrency, Sendable, TaskGroups
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 07-swift-performance
bond_type: SECONDARY_BOND
---

# Swift Concurrency Skill

Modern Swift concurrency patterns using async/await, actors, and structured concurrency.

## Prerequisites

- Swift 5.5+ / iOS 15+ / macOS 12+
- Understanding of threading concepts
- Familiarity with closures

## Parameters

```yaml
parameters:
  strict_concurrency:
    type: string
    enum: [minimal, targeted, complete]
    default: complete
    description: Concurrency checking level
  actor_isolation:
    type: boolean
    default: true
  use_main_actor:
    type: boolean
    default: true
    description: MainActor for UI code
```

## Topics Covered

### Core Concepts
| Concept | Purpose |
|---------|---------|
| async/await | Sequential async code |
| Actor | Data isolation |
| Task | Unit of async work |
| Sendable | Thread-safe types |
| MainActor | Main thread isolation |

### Task Types
| Type | Lifetime | Cancellation |
|------|----------|--------------|
| Task {} | Independent | Manual |
| Task.detached {} | No context inherited | Manual |
| async let | Structured | Automatic |
| TaskGroup | Structured, multiple | Automatic |

### Actor Isolation
| Annotation | Meaning |
|------------|---------|
| `actor` | Type is an actor |
| `@MainActor` | Runs on main thread |
| `nonisolated` | Opt out of isolation |
| `isolated` | Parameter isolation |

## Code Examples

### Basic async/await
```swift
// Sequential async operations
func fetchUserProfile(userId: String) async throws -> UserProfile {
    let user = try await api.fetchUser(userId)
    let posts = try await api.fetchPosts(userId: userId)
    let followers = try await api.fetchFollowers(userId: userId)

    return UserProfile(user: user, posts: posts, followers: followers)
}

// Concurrent with async let
func fetchUserProfileConcurrently(userId: String) async throws -> UserProfile {
    async let user = api.fetchUser(userId)
    async let posts = api.fetchPosts(userId: userId)
    async let followers = api.fetchFollowers(userId: userId)

    // All three run concurrently, await collects results
    return try await UserProfile(user: user, posts: posts, followers: followers)
}
```

### Actor for Thread Safety
```swift
actor ImageCache {
    private var cache: [URL: UIImage] = [:]
    private var inProgress: [URL: Task<UIImage, Error>] = [:]

    func image(for url: URL) async throws -> UIImage {
        // Return cached
        if let cached = cache[url] {
            return cached
        }

        // Return in-progress task (avoid duplicate downloads)
        if let existing = inProgress[url] {
            return try await existing.value
        }

        // Start new download
        let task = Task {
            let (data, _) = try await URLSession.shared.data(from: url)
            guard let image = UIImage(data: data) else {
                throw ImageError.invalidData
            }
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

    func clearCache() {
        cache.removeAll()
    }

    // Nonisolated for synchronous read
    nonisolated var cacheDescription: String {
        "ImageCache instance"
    }
}
```

### TaskGroup for Parallel Operations
```swift
func fetchAllProducts(ids: [String]) async throws -> [Product] {
    try await withThrowingTaskGroup(of: Product.self) { group in
        for id in ids {
            group.addTask {
                try await self.api.fetchProduct(id: id)
            }
        }

        var products: [Product] = []
        for try await product in group {
            products.append(product)
        }
        return products
    }
}

// With concurrency limit
func fetchWithLimit(ids: [String], maxConcurrent: Int = 4) async throws -> [Product] {
    try await withThrowingTaskGroup(of: Product.self) { group in
        var iterator = ids.makeIterator()
        var products: [Product] = []

        // Start initial batch
        for _ in 0..<min(maxConcurrent, ids.count) {
            if let id = iterator.next() {
                group.addTask { try await self.api.fetchProduct(id: id) }
            }
        }

        // As each completes, add another
        for try await product in group {
            products.append(product)
            if let id = iterator.next() {
                group.addTask { try await self.api.fetchProduct(id: id) }
            }
        }

        return products
    }
}
```

### MainActor for UI
```swift
@MainActor
final class ProductListViewModel: ObservableObject {
    @Published private(set) var products: [Product] = []
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?

    private let repository: ProductRepository

    init(repository: ProductRepository) {
        self.repository = repository
    }

    func loadProducts() async {
        isLoading = true
        error = nil

        do {
            products = try await repository.fetchProducts()
        } catch {
            self.error = error
        }

        isLoading = false
    }

    // Nonisolated for non-UI work
    nonisolated func precomputeHash(for product: Product) -> Int {
        product.hashValue
    }
}
```

### Sendable Conformance
```swift
// Value types are Sendable automatically if properties are
struct Product: Sendable {
    let id: String
    let name: String
    let price: Decimal
}

// Classes need explicit conformance
final class ProductCache: @unchecked Sendable {
    private let lock = NSLock()
    private var cache: [String: Product] = [:]

    func get(_ id: String) -> Product? {
        lock.lock()
        defer { lock.unlock() }
        return cache[id]
    }

    func set(_ product: Product) {
        lock.lock()
        defer { lock.unlock() }
        cache[product.id] = product
    }
}

// Sendable closure
func process(_ items: [Item], transform: @Sendable (Item) -> Result) async -> [Result] {
    await withTaskGroup(of: Result.self) { group in
        for item in items {
            group.addTask {
                transform(item)
            }
        }

        var results: [Result] = []
        for await result in group {
            results.append(result)
        }
        return results
    }
}
```

### Cancellation Handling
```swift
func downloadLargeFile(url: URL) async throws -> Data {
    var data = Data()
    let (stream, response) = try await URLSession.shared.bytes(from: url)

    let expectedLength = response.expectedContentLength

    for try await byte in stream {
        // Check for cancellation periodically
        try Task.checkCancellation()

        data.append(byte)

        // Report progress (would need actor for thread safety)
        let progress = Double(data.count) / Double(expectedLength)
        await reportProgress(progress)
    }

    return data
}

// Usage with timeout
func downloadWithTimeout(url: URL, timeout: Duration) async throws -> Data {
    try await withThrowingTaskGroup(of: Data.self) { group in
        group.addTask {
            try await self.downloadLargeFile(url: url)
        }

        group.addTask {
            try await Task.sleep(for: timeout)
            throw DownloadError.timeout
        }

        // First to complete wins, other is cancelled
        let result = try await group.next()!
        group.cancelAll()
        return result
    }
}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Actor-isolated property cannot be accessed" | Cross-actor access | Use await or nonisolated |
| "Capture of non-sendable type" | Non-Sendable in closure | Make type Sendable or use actor |
| "Reference to captured var in concurrently-executing code" | Mutable capture | Use let or actor |
| Task hangs | Missing await | Add await to all async calls |
| Deadlock | Actor calling itself | Use nonisolated for pure functions |

### Debug Tips
```swift
// Print current task priority
print("Priority: \(Task.currentPriority)")

// Check if cancelled
if Task.isCancelled {
    return
}

// Add task-local values for debugging
enum RequestID: TaskLocalKey {
    static var defaultValue: String? { nil }
}

extension Task where Success == Never, Failure == Never {
    static var requestID: String? {
        get { self[RequestID.self] }
        set { self[RequestID.self] = newValue }
    }
}
```

## Validation Rules

```yaml
validation:
  - rule: strict_concurrency
    severity: error
    check: Build with -strict-concurrency=complete
  - rule: sendable_conformance
    severity: warning
    check: Types crossing actor boundaries must be Sendable
  - rule: main_actor_ui
    severity: error
    check: UI updates must be on MainActor
```

## Usage

```
Skill("swift-concurrency")
```

## Related Skills

- `swift-fundamentals` - Language basics
- `swift-combine` - Reactive alternative
- `swift-testing` - Testing async code

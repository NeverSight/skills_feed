---
name: swift-combine
description: Master Combine framework for reactive programming - publishers, subscribers, operators, schedulers
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 03-swift-swiftui
bond_type: SECONDARY_BOND
---

# Swift Combine Skill

Reactive programming with Apple's Combine framework for handling asynchronous events and data streams.

## Prerequisites

- iOS 13+ / macOS 10.15+
- Understanding of closures and generics
- Familiarity with async programming concepts

## Parameters

```yaml
parameters:
  use_async_await:
    type: boolean
    default: true
    description: Prefer async/await where possible (iOS 15+)
  scheduler:
    type: string
    enum: [main, background, immediate]
    default: main
  error_handling:
    type: string
    enum: [catch, retry, replace]
    default: catch
```

## Topics Covered

### Core Concepts
| Concept | Description |
|---------|-------------|
| Publisher | Emits values over time |
| Subscriber | Receives values from publisher |
| Operator | Transforms/filters values |
| Subject | Publisher + manual value injection |
| Cancellable | Subscription lifecycle |

### Common Publishers
| Publisher | Purpose |
|-----------|---------|
| `Just` | Single value, then complete |
| `Future` | Single async result |
| `PassthroughSubject` | Manual value broadcast |
| `CurrentValueSubject` | Manual + current value |
| `@Published` | Property wrapper publisher |

### Key Operators
| Category | Operators |
|----------|-----------|
| Transform | map, flatMap, scan |
| Filter | filter, removeDuplicates, compactMap |
| Combine | merge, combineLatest, zip |
| Timing | debounce, throttle, delay |
| Error | catch, retry, mapError |

## Code Examples

### Basic Publisher Chain
```swift
import Combine

final class SearchViewModel: ObservableObject {
    @Published var searchText = ""
    @Published private(set) var results: [SearchResult] = []
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?

    private var cancellables = Set<AnyCancellable>()
    private let searchService: SearchService

    init(searchService: SearchService) {
        self.searchService = searchService
        setupSearch()
    }

    private func setupSearch() {
        $searchText
            .debounce(for: .milliseconds(300), scheduler: RunLoop.main) // Wait for typing pause
            .removeDuplicates() // Don't search same query twice
            .filter { $0.count >= 2 } // Minimum characters
            .handleEvents(receiveOutput: { [weak self] _ in
                self?.isLoading = true
                self?.error = nil
            })
            .flatMap { [searchService] query -> AnyPublisher<[SearchResult], Never> in
                searchService.search(query: query)
                    .catch { error -> Just<[SearchResult]> in
                        // Handle error, return empty
                        return Just([])
                    }
                    .eraseToAnyPublisher()
            }
            .receive(on: DispatchQueue.main)
            .sink { [weak self] results in
                self?.isLoading = false
                self?.results = results
            }
            .store(in: &cancellables)
    }
}
```

### Subjects for Event Broadcasting
```swift
final class EventBus {
    static let shared = EventBus()

    // PassthroughSubject - no current value
    let userActions = PassthroughSubject<UserAction, Never>()

    // CurrentValueSubject - maintains current value
    let authState = CurrentValueSubject<AuthState, Never>(.loggedOut)

    private init() {}

    func send(_ action: UserAction) {
        userActions.send(action)
    }

    func login(user: User) {
        authState.send(.loggedIn(user))
    }

    func logout() {
        authState.send(.loggedOut)
    }
}

enum UserAction {
    case tappedButton(String)
    case viewedScreen(String)
    case completedPurchase(orderId: String)
}

enum AuthState {
    case loggedOut
    case loggedIn(User)
}

// Subscription
class AnalyticsService {
    private var cancellables = Set<AnyCancellable>()

    init() {
        EventBus.shared.userActions
            .sink { [weak self] action in
                self?.track(action)
            }
            .store(in: &cancellables)
    }

    private func track(_ action: UserAction) {
        // Send to analytics
    }
}
```

### Combining Multiple Publishers
```swift
final class CheckoutViewModel: ObservableObject {
    @Published var cartItems: [CartItem] = []
    @Published var shippingAddress: Address?
    @Published var paymentMethod: PaymentMethod?
    @Published var promoCode: String = ""

    @Published private(set) var canCheckout = false
    @Published private(set) var total: Decimal = 0

    private var cancellables = Set<AnyCancellable>()

    init() {
        setupValidation()
        setupTotalCalculation()
    }

    private func setupValidation() {
        Publishers.CombineLatest3($cartItems, $shippingAddress, $paymentMethod)
            .map { items, address, payment in
                !items.isEmpty && address != nil && payment != nil
            }
            .assign(to: &$canCheckout)
    }

    private func setupTotalCalculation() {
        Publishers.CombineLatest($cartItems, $promoCode)
            .map { items, promo -> Decimal in
                let subtotal = items.reduce(0) { $0 + $1.price * Decimal($1.quantity) }
                let discount = self.calculateDiscount(promo: promo, subtotal: subtotal)
                return subtotal - discount
            }
            .assign(to: &$total)
    }

    private func calculateDiscount(promo: String, subtotal: Decimal) -> Decimal {
        // Promo code logic
        return 0
    }
}
```

### Error Handling & Retry
```swift
extension Publisher {
    func retryWithBackoff(
        maxRetries: Int = 3,
        initialDelay: TimeInterval = 1,
        maxDelay: TimeInterval = 30
    ) -> AnyPublisher<Output, Failure> {
        self.catch { error -> AnyPublisher<Output, Failure> in
            guard maxRetries > 0 else {
                return Fail(error: error).eraseToAnyPublisher()
            }

            let delay = min(initialDelay * pow(2, Double(3 - maxRetries)), maxDelay)

            return Just(())
                .delay(for: .seconds(delay), scheduler: DispatchQueue.global())
                .flatMap { _ in
                    self.retryWithBackoff(
                        maxRetries: maxRetries - 1,
                        initialDelay: initialDelay,
                        maxDelay: maxDelay
                    )
                }
                .eraseToAnyPublisher()
        }
        .eraseToAnyPublisher()
    }
}

// Usage
apiClient.fetchData()
    .retryWithBackoff(maxRetries: 3)
    .catch { error -> Just<Data> in
        Logger.network.error("Final failure: \(error)")
        return Just(Data())
    }
    .sink { data in
        // Process data
    }
    .store(in: &cancellables)
```

### Bridging to async/await
```swift
extension Publisher {
    func firstValue() async throws -> Output {
        try await withCheckedThrowingContinuation { continuation in
            var cancellable: AnyCancellable?

            cancellable = self.first()
                .sink(
                    receiveCompletion: { completion in
                        switch completion {
                        case .finished:
                            break
                        case .failure(let error):
                            continuation.resume(throwing: error)
                        }
                        cancellable?.cancel()
                    },
                    receiveValue: { value in
                        continuation.resume(returning: value)
                    }
                )
        }
    }
}

// Usage
let result = try await somePublisher.firstValue()
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Sink never called | No strong reference | Store in cancellables Set |
| UI not updating | Wrong scheduler | Use .receive(on: DispatchQueue.main) |
| Memory leak | Strong reference in closure | Use [weak self] |
| Duplicate events | Missing removeDuplicates | Add .removeDuplicates() |
| Publisher completes early | Using first() or prefix() | Check operator semantics |

### Debug Tips
```swift
// Print debug info for each event
publisher
    .print("Debug")
    .sink { ... }

// Handle events at each stage
publisher
    .handleEvents(
        receiveSubscription: { _ in print("Subscribed") },
        receiveOutput: { print("Output: \($0)") },
        receiveCompletion: { print("Completed: \($0)") },
        receiveCancel: { print("Cancelled") }
    )
    .sink { ... }

// Breakpoint on specific conditions
publisher
    .breakpoint(receiveOutput: { $0 > 100 })
    .sink { ... }
```

## Validation Rules

```yaml
validation:
  - rule: store_cancellables
    severity: error
    check: All subscriptions must be stored in cancellables
  - rule: weak_self_in_closures
    severity: warning
    check: Use [weak self] in sink closures
  - rule: receive_on_main
    severity: warning
    check: UI updates must receive on main queue
```

## Usage

```
Skill("swift-combine")
```

## Related Skills

- `swift-swiftui` - @Published integration
- `swift-concurrency` - async/await alternative
- `swift-networking` - Network publishers

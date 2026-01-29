---
name: swift_combine
description: Swift Combine framework for reactive programming, handling asynchronous events with publishers, subscribers, and operators.
license: Proprietary
compatibility: iOS 13+, macOS 10.15+
metadata:
  version: "1.0"
  author: SwiftZilla
  website: https://swiftzilla.dev
---

# Swift Combine

This skill covers Apple's Combine framework for reactive programming and handling asynchronous events.

## Overview

Combine is a declarative Swift API for processing values over time. It provides a unified approach to handling asynchronous events, user interface updates, and data streams.

## Available References

- [Publishers & Subscribers](./references/publishers_subscribers.md) - Core concepts and lifecycle
- [Operators](./references/operators.md) - Transforming, filtering, and combining streams
- [Integration](./references/integration.md) - Using Combine with UIKit, SwiftUI, and Foundation

## Quick Reference

### Basic Publisher

```swift
import Combine

// Published property
@Published var username: String = ""

// CurrentValueSubject
let subject = CurrentValueSubject<String, Never>("initial")

// PassthroughSubject
let passthrough = PassthroughSubject<Int, Never>()

// Just publisher
let just = Just("value")

// Future publisher
let future = Future<String, Error> { promise in
    promise(.success("result"))
}
```

### Subscribing

```swift
// Sink
let cancellable = publisher.sink(
    receiveCompletion: { completion in
        switch completion {
        case .finished:
            print("Completed")
        case .failure(let error):
            print("Error: \(error)")
        }
    },
    receiveValue: { value in
        print("Value: \(value)")
    }
)

// Assign
let cancellable = publisher
    .assign(to: \.text, on: label)
```

### Storing Subscriptions

```swift
private var cancellables = Set<AnyCancellable>()

publisher
    .sink { value in
        print(value)
    }
    .store(in: &cancellables)
```

### Common Operators

```swift
publisher
    .filter { $0 > 0 }
    .map { $0 * 2 }
    .debounce(for: .seconds(0.5), scheduler: RunLoop.main)
    .removeDuplicates()
    .sink { value in
        print(value)
    }
```

## Combine vs Async/Await

| Use Case | Combine | Async/Await |
|----------|---------|-------------|
| Event streams | ✅ Excellent | ⚠️ Complex |
| UI bindings | ✅ Perfect | ⚠️ Verbose |
| Chaining operations | ✅ Great | ✅ Good |
| Simple async calls | ⚠️ Overkill | ✅ Simple |
| Error handling | ✅ Rich | ✅ Good |

## Best Practices

1. **Store cancellables** - Prevent memory leaks
2. **Use weak self** - Avoid retain cycles
3. **Handle errors** - Always handle completion
4. **Thread safety** - Use receive(on:) for UI
5. **Cancel properly** - Clean up subscriptions
6. **Avoid overuse** - Combine is powerful but not for everything
7. **Test pipelines** - Use expectations for async

## For More Information

Visit https://swiftzilla.dev for comprehensive Combine documentation.

---
name: swift-fundamentals
description: Master Swift programming fundamentals - syntax, types, optionals, protocols, error handling
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 01-swift-fundamentals
bond_type: PRIMARY_BOND
---

# Swift Fundamentals Skill

Comprehensive knowledge base for Swift language fundamentals, type system, and idiomatic patterns.

## Prerequisites

- Xcode 15+ installed
- Swift 5.9+ toolchain
- Basic programming knowledge

## Parameters

```yaml
parameters:
  swift_version:
    type: string
    default: "5.9"
    enum: ["5.5", "5.6", "5.7", "5.8", "5.9", "5.10", "6.0"]
    description: Target Swift version for compatibility
  strict_concurrency:
    type: boolean
    default: true
    description: Enable strict concurrency checking
  coding_style:
    type: string
    enum: [apple, google, raywenderlich]
    default: apple
```

## Topics Covered

### Type System
| Topic | Description | Swift Version |
|-------|-------------|---------------|
| Value Types | struct, enum, copy semantics | 5.0+ |
| Reference Types | class, ARC, identity | 5.0+ |
| Generics | Type parameters, constraints | 5.0+ |
| Opaque Types | some keyword, type erasure | 5.1+ |
| Existentials | any keyword, protocol types | 5.6+ |

### Optionals
| Pattern | Use Case | Example |
|---------|----------|---------|
| `if let` | Conditional unwrap | `if let x = optional { }` |
| `guard let` | Early exit | `guard let x = optional else { return }` |
| `??` | Default value | `optional ?? defaultValue` |
| `?.` | Optional chaining | `object?.property?.method()` |
| `!` | Force unwrap (avoid) | Only when provably safe |

### Protocols
| Feature | Description |
|---------|-------------|
| Protocol Composition | `Codable & Sendable` |
| Associated Types | Generic protocols with `associatedtype` |
| Conditional Conformance | `extension Array: Equatable where Element: Equatable` |
| Protocol Extensions | Default implementations |

### Error Handling
| Pattern | Syntax | Use Case |
|---------|--------|----------|
| Throwing | `func x() throws` | Recoverable errors |
| Result | `Result<Success, Failure>` | Async contexts |
| Optional | `try?` | Silent failure |
| Force | `try!` | Guaranteed success |

## Code Examples

### Protocol-Oriented Design
```swift
protocol Identifiable {
    associatedtype ID: Hashable
    var id: ID { get }
}

protocol Persistable: Identifiable {
    func save() async throws
    static func load(id: ID) async throws -> Self?
}

extension Persistable where Self: Codable {
    func save() async throws {
        let data = try JSONEncoder().encode(self)
        try await Storage.shared.write(data, forKey: "\(Self.self)-\(id)")
    }
}
```

### Safe Optional Handling
```swift
struct UserProfile {
    let name: String
    let email: String?
    let avatarURL: URL?
}

func displayUser(_ user: UserProfile?) {
    guard let user else {
        showPlaceholder()
        return
    }

    nameLabel.text = user.name
    emailLabel.text = user.email ?? "No email provided"

    if let avatarURL = user.avatarURL {
        loadImage(from: avatarURL)
    }
}
```

### Modern Error Handling
```swift
enum ValidationError: LocalizedError {
    case emptyField(String)
    case invalidFormat(String, expected: String)
    case outOfRange(String, min: Int, max: Int)

    var errorDescription: String? {
        switch self {
        case .emptyField(let field):
            return "\(field) cannot be empty"
        case .invalidFormat(let field, let expected):
            return "\(field) must be in \(expected) format"
        case .outOfRange(let field, let min, let max):
            return "\(field) must be between \(min) and \(max)"
        }
    }
}

func validate(username: String) throws -> String {
    guard !username.isEmpty else {
        throw ValidationError.emptyField("Username")
    }
    guard username.count >= 3, username.count <= 20 else {
        throw ValidationError.outOfRange("Username", min: 3, max: 20)
    }
    return username
}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Cannot convert value of type" | Type mismatch | Check expected type, add explicit cast |
| "Value of optional type not unwrapped" | Missing unwrap | Use if let, guard let, or ?? |
| "Protocol can only be used as generic constraint" | PAT in variable | Use any or type erasure |
| "Closure captures 'self' strongly" | Retain cycle | Add [weak self] capture |

### Debug Commands
```bash
# Check Swift version
swift --version

# Compile with strict concurrency
swift build -Xswiftc -strict-concurrency=complete

# Dump AST for debugging
swiftc -dump-ast file.swift
```

## Validation Rules

```yaml
validation:
  - rule: no_force_unwrap
    severity: warning
    message: Avoid force unwrapping optionals
  - rule: no_implicitly_unwrapped
    severity: warning
    message: Avoid implicitly unwrapped optionals except for IBOutlets
  - rule: prefer_guard
    severity: info
    message: Prefer guard for early exit over nested if-let
```

## Retry Logic

```swift
func withRetry<T>(
    maxAttempts: Int = 3,
    delay: Duration = .seconds(1),
    operation: () async throws -> T
) async throws -> T {
    var lastError: Error?

    for attempt in 1...maxAttempts {
        do {
            return try await operation()
        } catch {
            lastError = error
            if attempt < maxAttempts {
                try await Task.sleep(for: delay * Double(attempt))
            }
        }
    }

    throw lastError!
}
```

## Observability

```swift
import OSLog

extension Logger {
    static let swift = Logger(subsystem: "com.app", category: "swift")
}

// Usage
Logger.swift.debug("Parsing user: \(userId)")
Logger.swift.error("Failed to decode: \(error.localizedDescription)")
```

## Usage

```
Skill("swift-fundamentals")
```

## Related Skills

- `swift-spm` - Package management
- `swift-testing` - Testing fundamentals code

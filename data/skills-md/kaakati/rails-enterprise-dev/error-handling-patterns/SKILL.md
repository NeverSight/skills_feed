---
name: error-handling-patterns
description: "Expert error handling decisions for iOS/tvOS: when to use throws vs Result, error type design trade-offs, recovery strategy selection, and user-facing error presentation patterns. Use when designing error hierarchies, implementing retry logic, or deciding how to surface errors to users. Trigger keywords: Error, throws, Result, LocalizedError, retry, recovery, error presentation, do-catch, try, error handling, failure"
version: "3.0.0"
---

# Error Handling Patterns — Expert Decisions

Expert decision frameworks for error handling choices. Claude knows Swift error syntax — this skill provides judgment calls for error type design and recovery strategies.

---

## Decision Trees

### throws vs Result

```
Does the caller need to handle success/failure explicitly?
├─ YES (caller must acknowledge failure)
│  └─ Is the failure common and expected?
│     ├─ YES → Result<T, E> (explicit handling, no try/catch)
│     └─ NO → throws (exceptional case)
│
└─ NO (caller can ignore failure)
   └─ Use throws with try? at call site
```

**When Result wins**: Parsing, validation, operations where failure is common and needs explicit handling. Forces exhaustive switch.

**When throws wins**: Network calls, file operations where failure is exceptional. Cleaner syntax with async/await.

### Error Type Granularity

```
How specific should error types be?
├─ API boundary (framework, library)
│  └─ Coarse-grained domain errors
│     enum NetworkError: Error { case timeout, serverError, ... }
│
├─ Internal module
│  └─ Fine-grained for actionable handling
│     enum PaymentError: Error {
│         case cardDeclined(reason: String)
│         case insufficientFunds(balance: Decimal, required: Decimal)
│     }
│
└─ User-facing
   └─ LocalizedError with user-friendly messages
      var errorDescription: String? { "Payment failed" }
```

**The trap**: Too many error types that no one handles differently. If every case has the same handler, collapse them.

### Recovery Strategy Selection

```
Is the error transient (network, timeout)?
├─ YES → Is it idempotent?
│  ├─ YES → Retry with exponential backoff
│  └─ NO → Retry cautiously or fail
│
└─ NO → Is recovery possible?
   ├─ YES → Can user fix it?
   │  ├─ YES → Show actionable error UI
   │  └─ NO → Auto-recover or fallback value
   │
   └─ NO → Log and show generic error
```

### Error Presentation Selection

```
How critical is the failure?
├─ Critical (can't continue)
│  └─ Full-screen error with retry
│
├─ Important (user needs to know)
│  └─ Alert dialog
│
├─ Minor (informational)
│  └─ Toast or inline message
│
└─ Silent (user doesn't need to know)
   └─ Log only, use fallback
```

---

## NEVER Do

### Error Type Design

**NEVER** use generic catch-all errors:
```swift
// ❌ Caller can't handle different cases
enum AppError: Error {
    case somethingWentWrong
    case error(String)  // Just a message — no actionable info
}

// ✅ Specific, actionable cases
enum AuthError: Error {
    case invalidCredentials
    case sessionExpired
    case accountLocked(unlockTime: Date?)
}
```

**NEVER** throw errors with sensitive information:
```swift
// ❌ Leaks internal details
throw DatabaseError.queryFailed(sql: query, password: dbPassword)

// ✅ Sanitize sensitive data
throw DatabaseError.queryFailed(table: tableName)
```

**NEVER** create error enums with one case:
```swift
// ❌ Pointless enum
enum ValidationError: Error {
    case invalid
}

// ✅ Use existing error or don't create enum
struct ValidationError: Error {
    let field: String
    let reason: String
}
```

### Error Propagation

**NEVER** swallow errors silently:
```swift
// ❌ Failure is invisible
func loadUser() async {
    try? await fetchUser()  // Error ignored, user is nil, no feedback
}

// ✅ Handle or propagate
func loadUser() async {
    do {
        user = try await fetchUser()
    } catch {
        errorMessage = error.localizedDescription
        analytics.trackError(error)
    }
}
```

**NEVER** catch and rethrow without adding context:
```swift
// ❌ Pointless catch
do {
    try operation()
} catch {
    throw error  // Why catch at all?
}

// ✅ Add context or handle
do {
    try operation()
} catch {
    throw ContextualError.operationFailed(underlying: error, context: "during checkout")
}
```

**NEVER** use force-try (`try!`) outside of known-safe scenarios:
```swift
// ❌ Crashes if JSON is malformed
let data = try! JSONEncoder().encode(untrustedInput)

// ✅ Safe scenarios only
let data = try! JSONEncoder().encode(staticKnownValue)  // Compile-time known
let url = URL(string: "https://example.com")!  // Literal string

// ✅ Handle unknown input
guard let data = try? JSONEncoder().encode(userInput) else {
    throw EncodingError.failed
}
```

### CancellationError

**NEVER** show CancellationError to users:
```swift
// ❌ User sees "cancelled" error when navigating away
func loadData() async {
    do {
        data = try await fetchData()
    } catch {
        errorMessage = error.localizedDescription  // Shows "cancelled"
    }
}

// ✅ Handle cancellation separately
func loadData() async {
    do {
        data = try await fetchData()
    } catch is CancellationError {
        return  // User navigated away — not an error
    } catch {
        errorMessage = error.localizedDescription
    }
}
```

### Retry Logic

**NEVER** retry non-idempotent operations blindly:
```swift
// ❌ May charge user multiple times
func processPayment() async throws {
    try await retryWithBackoff {
        try await chargeCard(amount)  // Not idempotent!
    }
}

// ✅ Use idempotency key or check state first
func processPayment() async throws {
    let idempotencyKey = UUID().uuidString
    try await retryWithBackoff {
        try await chargeCard(amount, idempotencyKey: idempotencyKey)
    }
}
```

**NEVER** retry without limits:
```swift
// ❌ Infinite loop if server is down
func fetch() async throws -> Data {
    while true {
        do {
            return try await request()
        } catch {
            try await Task.sleep(nanoseconds: 1_000_000_000)
        }
    }
}

// ✅ Limited retries with backoff
func fetch(maxAttempts: Int = 3) async throws -> Data {
    var delay: UInt64 = 1_000_000_000
    for attempt in 1...maxAttempts {
        do {
            return try await request()
        } catch where attempt < maxAttempts && isRetryable(error) {
            try await Task.sleep(nanoseconds: delay)
            delay *= 2
        }
    }
    throw FetchError.maxRetriesExceeded
}
```

---

## Essential Patterns

### Typed Error with Recovery Info

```swift
enum NetworkError: Error, LocalizedError {
    case noConnection
    case timeout
    case serverError(statusCode: Int)
    case unauthorized

    var errorDescription: String? {
        switch self {
        case .noConnection: return "No internet connection"
        case .timeout: return "Request timed out"
        case .serverError(let code): return "Server error (\(code))"
        case .unauthorized: return "Session expired"
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .noConnection: return "Check your network settings"
        case .timeout: return "Try again"
        case .serverError: return "Please try again later"
        case .unauthorized: return "Please log in again"
        }
    }

    var isRetryable: Bool {
        switch self {
        case .noConnection, .timeout, .serverError: return true
        case .unauthorized: return false
        }
    }
}
```

### Result with Typed Error

```swift
func validate(email: String) -> Result<String, ValidationError> {
    guard !email.isEmpty else {
        return .failure(.emptyField("email"))
    }
    guard email.contains("@") else {
        return .failure(.invalidFormat("email"))
    }
    return .success(email)
}

// Forced exhaustive handling
switch validate(email: input) {
case .success(let email):
    createAccount(email: email)
case .failure(let error):
    showValidationError(error)
}
```

### Retry with Exponential Backoff

```swift
func withRetry<T>(
    maxAttempts: Int = 3,
    initialDelay: Duration = .seconds(1),
    operation: () async throws -> T
) async throws -> T {
    var delay = initialDelay

    for attempt in 1...maxAttempts {
        do {
            return try await operation()
        } catch let error as NetworkError where error.isRetryable && attempt < maxAttempts {
            try await Task.sleep(for: delay)
            delay *= 2
        } catch {
            throw error
        }
    }
    fatalError("Should not reach")
}
```

### Error Presentation in ViewModel

```swift
@MainActor
final class ViewModel: ObservableObject {
    @Published private(set) var state: State = .idle

    enum State: Equatable {
        case idle
        case loading
        case loaded(Data)
        case error(String, isRetryable: Bool)
    }

    func load() async {
        state = .loading
        do {
            let data = try await fetchData()
            state = .loaded(data)
        } catch is CancellationError {
            state = .idle  // Don't show error
        } catch let error as NetworkError {
            state = .error(error.localizedDescription, isRetryable: error.isRetryable)
        } catch {
            state = .error("Something went wrong", isRetryable: true)
        }
    }
}
```

---

## Quick Reference

### Error Handling Decision Matrix

| Scenario | Pattern | Why |
|----------|---------|-----|
| Network call | `throws` | Exceptional failure |
| Validation | `Result<T, E>` | Expected failure, needs handling |
| Optional parsing | `try?` | Failure acceptable, use default |
| Must succeed | `try!` | Only for literals/static |
| Background task | Log only | User doesn't need to know |

### Error Type Checklist

- [ ] Cases are actionable (handler differs per case)
- [ ] No sensitive data in associated values
- [ ] Conforms to `LocalizedError` for user-facing
- [ ] Has `isRetryable` property if recovery is possible
- [ ] Has `recoverySuggestion` for user guidance

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| `catch { }` empty | Error silently swallowed | Log or propagate |
| Same handler for all cases | Over-specific error type | Collapse to fewer cases |
| `try?` on critical path | Hidden failures | Use `do-catch` |
| Retry without limit | Infinite loop risk | Add max attempts |
| CancellationError shown to user | Bad UX | Handle separately |
| `error.localizedDescription` on NSError | Technical message | Map to user-friendly |

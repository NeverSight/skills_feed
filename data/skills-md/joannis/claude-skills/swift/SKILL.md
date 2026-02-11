---
name: swift
description: 'Expert guidance on Swift best practices, patterns, and implementation. Use when developers mention: (1) Swift configuration or environment variables, (2) swift-log or logging patterns, (3) OpenTelemetry or swift-otel, (4) Swift Testing framework or @Test macro, (5) Foundation avoidance or cross-platform Swift, (6) platform-specific code organization, (7) Span or memory safety patterns, (8) non-copyable types (~Copyable), (9) API design patterns or access modifiers.'
---

# Swift

Swift is a modern general-purpose programming language.

## Reference Files

Load these files as needed for specific topics:

- **`references/swift-configuration.md`** - Swift Configuration: reading config from environment variables, files, CLI arguments; provider hierarchy, namespacing, hot reloading, secret handling
- **`references/swift-log.md`** - Swift Log logging API: log levels, structured logging, best practices for libraries, metadata, custom handlers
- **`references/swift-otel.md`** - Swift OTel: OpenTelemetry backend for server apps (preferred for Linux); OTLP export for logs, metrics, tracing; framework integration
- **`references/swift-testing.md`** - Swift Testing framework: @Test macro, #expect/#require assertions, traits, parameterized tests, test suites, parallel execution, XCTest migration
- **`references/debugging.md`** - Debugging tips: Terminal UI on Linux (alternate screen buffer), GitHub Actions log analysis

### Access Modifiers

Keep types and functions internal unless they need to be public for external use. This prevents accidental exposure of implementation details and makes access level errors easier to fix.

### Foundation Avoidance Policy

**Avoid Foundation in core library code when possible:**

- Foundation types (`Data`, `Date`, `UUID`, etc.) should be avoided in public APIs for libraries targeting:
  - Embedded Swift
  - Cross-platform consistency
  - Binary size reduction (FoundationEssentials is 15-40MB)
- Use Swift standard library types instead:
  - `[UInt8]` instead of `Data` for byte buffers
  - `ContinuousClock.Instant` or custom types instead of `Date`
  - Byte-based initializers instead of `UUID` strings
- Always use `internal import Foundation` or `internal import FoundationEssentials`, never `public import`

```swift
#if canImport(FoundationEssentials)
    internal import FoundationEssentials
#else
    internal import Foundation
#endif
```

### InternalImportsByDefault Feature

When using `InternalImportsByDefault` in Package.swift, all imports are internal by default unless explicitly marked with `public import`.

**When to use `public import`:**
- When types from the imported module are exposed in public API (return types, parameters, protocol conformances)
- Example: `public import ServiceLifecycle` when conforming to `ServiceLifecycle.Service` in a public type
- **Never use `public import Foundation`** - keep Foundation internal

### Platform-Specific File Organization

Use a `+platform` suffix convention for platform-specific implementations:
- `PlatformDeviceDiscovery+macos.swift` - macOS implementation
- `PlatformDeviceDiscovery+linux.swift` - Linux implementation
- `PlatformDeviceDiscovery+default.swift` - Fallback for other platforms

When adding methods to a protocol, **all platform files must be updated** to maintain conformance.

### Linux C Library Support

Support both Glibc and Musl for Linux compatibility:
```swift
#if os(macOS) || os(iOS) || os(tvOS) || os(watchOS)
import Darwin
#elseif canImport(Glibc)
import Glibc
#elseif canImport(Musl)
import Musl
#endif
```

### Avoid Repetitive Code in Selection Logic

When selecting from multiple options with preference ordering, use sorting instead of multiple conditional blocks:

**Bad - Repetitive:**
```swift
if !preferBluetooth {
    for interface in interfaces {
        if case .lan(let device) = interface {
            return .lan(device)
        }
    }
}
for interface in interfaces {
    if case .bluetooth(let device) = interface {
        return .bluetooth(device)
    }
}
if preferBluetooth {
    for interface in interfaces {
        if case .lan(let device) = interface {
            return .lan(device)
        }
    }
}
```

**Good - Sort once, iterate once:**
```swift
let sorted = interfaces.sorted { a, b in
    if preferBluetooth {
        return a.type == "Bluetooth" && b.type != "Bluetooth"
    } else {
        return a.type == "LAN" && b.type != "LAN"
    }
}

for interface in sorted {
    switch interface {
    case .lan(let device): return .lan(device)
    case .bluetooth(let device): return .bluetooth(device)
    default: continue
    }
}
```

### Memory Safety Patterns (Swift 6.2+)

Swift 6.2 introduces opt-in strict memory safety checking via `.strictMemorySafety()` in Package.swift.

**Span Lifetime Constraints:**
- `Span<T>` is lifetime-dependent - it borrows the memory of its backing storage
- Cannot cross async boundaries
- Cannot escape closure scope
- Cannot pass to async callbacks

**Solution: Asymmetric API Design**
Use **Span for parsing** (read-only, synchronous, borrowed) and **[UInt8] for writing** (owned, can cross boundaries):

```swift
public struct Characteristic<Value: Sendable>: Sendable {
    // Parsing uses Span - borrowed, synchronous access
    internal let parse: @Sendable (borrowing Span<UInt8>) throws -> Value

    // Writing uses [UInt8] - owned, can cross closure boundaries
    public typealias WithBytes = ([UInt8]) -> Void
    internal let write: @Sendable (Value) -> (WithBytes) -> Void
}
```

**Safe Integer Loading from Bytes:**
```swift
// UNSAFE: unsafeLoad
return span.bytes.unsafeLoad(as: UInt64.self)

// SAFE: Manual byte-by-byte assembly
var value: UInt64 = 0
for i in 0..<8 {
    value |= UInt64(span[i]) << (i * 8)
}
return value
```

### Span-Based Computed Properties with `_read`/`_modify`

With the `LifetimeDependence` experimental feature, computed properties can return non-escapable types like `RawSpan` and `MutableRawSpan` using `_read` and `_modify` accessors:

```swift
// Enable in Package.swift:
swiftSettings: [
    .enableExperimentalFeature("LifetimeDependence"),
]

// Read-only span access
public var bytes: RawSpan {
    _read {
        var mapInfo = GstMapInfo()
        guard mapBuffer(&mapInfo) else { fatalError("Failed to map") }
        defer { unmapBuffer(&mapInfo) }
        yield RawSpan(_unsafeStart: mapInfo.data, byteCount: Int(mapInfo.size))
    }
}

// Mutable span access with Copy-on-Write
public var mutableBytes: MutableRawSpan {
    _read {
        fatalError("Cannot read mutableBytes")
    }
    _modify {
        // Ensure unique ownership before write (CoW)
        if !isKnownUniquelyReferenced(&storage) {
            storage = storage.copy()!
        }
        var mapInfo = GstMapInfo()
        guard mapBuffer(&mapInfo) else { fatalError("Failed to map") }
        defer { unmapBuffer(&mapInfo) }
        var span = MutableRawSpan(_unsafeStart: mapInfo.data, byteCount: Int(mapInfo.size))
        yield &span
    }
}
```

**Known Compiler Issue (Swift 6.2.3):** The LifetimeDependenceScopeFixup pass can crash when using `span.withUnsafeBytes` in certain contexts. Workaround: provide separate closure-based methods for C interop that don't go through the span accessor.

### Non-Copyable Types

Use `~Copyable` for move-only types that should not be duplicated:
```swift
public struct ResourceHandle: ~Copyable {
    // Can only be moved, not copied
}

public struct ServiceRegistration: @unchecked Sendable, ~Copyable { ... }
```
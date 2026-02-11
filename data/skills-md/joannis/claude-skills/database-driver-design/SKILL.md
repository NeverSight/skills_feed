---
name: database-driver-design
description: 'Expert guidance on building Swift database client libraries. Use when developers mention: (1) building a database driver, (2) wire protocol implementation, (3) connection pooling design, (4) state machines for protocol handling, (5) NIO channel handlers for databases, (6) backpressure in result streaming, (7) actor executor alignment with NIO.'
---

# Database Driver Design

This skill provides expert guidance on building production-quality database client libraries in Swift, covering wire protocol implementation, connection management, type-safe APIs, and integration with Swift Concurrency. Patterns are derived from exemplary implementations: **valkey-swift** and **postgres-nio**.

## Agent Behavior Contract (Follow These Rules)

1. **Prefer parameterized queries** - Never concatenate user input into SQL/command strings
2. **Use string interpolation for safety** - Implement `ExpressibleByStringInterpolation` to convert values to bindings
3. **Design commands as types** - Each command/query should be a struct with associated response type
4. **Implement state machines for protocols** - Complex connection lifecycles need explicit state transitions
5. **Support backpressure** - Row/result streaming must respect consumer demand
6. **Align actor executors** - Use `unownedExecutor` to align with NIO event loops
7. **Pool connections properly** - Implement keep-alive, idle timeout, and graceful shutdown

## Core Patterns

### Command as Type Pattern

Define commands as types with associated response types for compile-time safety:

```swift
public protocol DatabaseCommand: Sendable, Hashable {
    associatedtype Response: Decodable
    static var name: String { get }
    func encode(into encoder: inout CommandEncoder)
}

public struct GET: DatabaseCommand {
    public typealias Response = String?
    public static var name: String { "GET" }
    public let key: String

    public func encode(into encoder: inout CommandEncoder) {
        encoder.encode(Self.name, key)
    }
}
```

### SQL Injection Prevention via String Interpolation

```swift
public struct Query: ExpressibleByStringInterpolation {
    public var sql: String
    public var bindings: Bindings

    public struct StringInterpolation: StringInterpolationProtocol {
        var sql: String = ""
        var bindings: Bindings = Bindings()

        public mutating func appendLiteral(_ literal: String) {
            sql.append(literal)
        }

        public mutating func appendInterpolation<T: Encodable>(_ value: T) {
            bindings.append(value)
            sql.append("$\(bindings.count)")
        }
    }
}

// Usage: let query: Query = "SELECT * FROM users WHERE id = \(userId)"
// Result: sql = "SELECT * FROM users WHERE id = $1", bindings = [userId]
```

### Actor with NIO Executor Alignment

Eliminate context switches by aligning actor executor with NIO event loop:

```swift
public final actor Connection: Sendable {
    nonisolated public let unownedExecutor: UnownedSerialExecutor

    init(channel: any Channel) {
        self.unownedExecutor = channel.eventLoop.executor.asUnownedSerialExecutor()
    }
}
```

### State Machine with Actions Pattern

Manage complex protocol state with explicit transitions and actions:

```swift
struct ConnectionStateMachine {
    enum State {
        case idle
        case executing(QueryStateMachine)
        case closing
        case closed
        case modifying // Prevents COW during mutations
    }

    enum Action {
        case sendMessage(Message)
        case forwardResult(Result)
        case closeConnection
        case none
    }

    private var state: State = .idle

    mutating func handle(_ message: Message) -> Action {
        switch (state, message) {
        case (.idle, .query(let q)):
            state = .executing(QueryStateMachine(q))
            return .sendMessage(.parse(q))
        // ... other transitions
        }
    }
}
```

### Length-Prefixed Binary Encoding

Write length-prefixed data with placeholder and backfill:

```swift
extension Encodable {
    func encodeRaw(into buffer: inout ByteBuffer) throws {
        // Write placeholder for length (4 bytes for Int32)
        let lengthIndex = buffer.writerIndex
        buffer.writeInteger(Int32(0))

        // Record position before encoding
        let startIndex = buffer.writerIndex

        // Encode the actual value
        try self.encode(into: &buffer)

        // Calculate and write actual length
        let length = buffer.writerIndex - startIndex
        buffer.setInteger(Int32(length), at: lengthIndex)
    }
}
```

### Protocol Hierarchy for Encoding/Decoding

Design tiered protocols for different encoding guarantees:

```swift
// Base: runtime-determined type, may throw
public protocol ThrowingDynamicTypeEncodable: Sendable {
    func encode(into byteBuffer: inout ByteBuffer) throws
    var dataType: DataType { get }
}

// Non-throwing variant
public protocol DynamicTypeEncodable: ThrowingDynamicTypeEncodable {
    func encode(into byteBuffer: inout ByteBuffer)
}

// Static type info known at compile time
public protocol StaticTypeEncodable: ThrowingDynamicTypeEncodable {
    static var dataType: DataType { get }
}

// Non-throwing + static type info (most efficient)
public protocol NonThrowingEncodable: StaticTypeEncodable, DynamicTypeEncodable {}
```

### Variadic Generic Row Decoding

Decode multiple columns type-safely using parameter packs:

```swift
extension Row {
    func decode<each T: Decodable>(
        _ types: (repeat each T).Type
    ) throws -> (repeat each T) {
        var index = 0
        return (repeat try decodeColumn((each T).self, at: &index))
    }
}

// Usage: let (id, name, email) = try row.decode((Int.self, String.self, String.self))
```

### Backpressure-Aware Streaming

Implement adaptive buffer strategy for result streaming:

```swift
struct AdaptiveBuffer: BackPressureStrategy {
    var lowWatermark: Int
    var highWatermark: Int
    var currentTarget: Int

    mutating func didYield(bufferDepth: Int) -> Bool {
        // Shrink target if buffer too deep
        if bufferDepth > currentTarget * 2 {
            currentTarget = max(lowWatermark, currentTarget / 2)
        }
        return bufferDepth < currentTarget
    }

    mutating func didConsume(bufferDepth: Int) -> Bool {
        // Grow target if buffer drains completely
        if bufferDepth == 0 {
            currentTarget = min(highWatermark, currentTarget * 2)
        }
        return bufferDepth < currentTarget
    }
}
```

### Connection Pool Integration

Conform connections to pool protocols:

```swift
extension Connection: PooledConnection {
    public typealias ConnectionID = Int
}

struct KeepAliveBehavior: ConnectionKeepAliveBehavior {
    typealias Connection = Connection

    let frequency: Duration

    func runKeepAlive(for connection: Connection) async throws {
        _ = try await connection.ping()
    }
}

final class ClientMetrics: ConnectionPoolObservabilityDelegate {
    func connectionCreated(id: Int) { /* metrics */ }
    func connectionLeased(id: Int) { /* metrics */ }
    func connectionReleased(id: Int) { /* metrics */ }
    func connectionClosed(id: Int) { /* metrics */ }
}
```

### Depth-Limited Parsing

Prevent stack overflow with nested structures:

```swift
mutating func parseToken(maxDepth: Int = 100) throws -> Token {
    guard maxDepth > 0 else {
        throw ParsingError.tooDeeplyNested
    }

    switch tokenType {
    case .array:
        var elements: [Token] = []
        for _ in 0..<count {
            elements.append(try parseToken(maxDepth: maxDepth - 1))
        }
        return .array(elements)
    // ... other cases
    }
}
```

## Quick Decision Tree

1. **Implementing wire protocol encoding/decoding?**
   - Use length-prefixed messages with placeholder + backfill
   - Define protocol tokens as enums with associated values
   - Implement depth limits for nested structures

2. **Designing type-safe query API?**
   - Use `ExpressibleByStringInterpolation` for injection prevention
   - Create `Encodable`/`Decodable` protocol hierarchies for type coercion
   - Use variadic generics for multi-column row decoding

3. **Managing connections?**
   - Use actors with NIO executor alignment
   - Implement hierarchical state machines
   - Support cancellation via request IDs

4. **Implementing connection pooling?**
   - Conform to `PooledConnection` protocol
   - Implement keep-alive behavior
   - Track metrics via observability delegate

## Triage-First Playbook

- **"SQL Injection vulnerability"**
  - Implement `ExpressibleByStringInterpolation` on query type
  - Convert interpolated values to `$1, $2...` parameter placeholders

- **"Type mismatch when decoding results"**
  - Define `Decodable` protocol with typed throws
  - Wrap errors with column/cell context

- **"Connection state corruption"**
  - Use hierarchical state machines with explicit transitions
  - Add `.modifying` sentinel to prevent COW issues

- **"Backpressure not working"**
  - Implement adaptive buffer strategy
  - Signal demand through data source protocol

## Best Practices Summary

1. **Commands/Queries as types** - Each operation is a struct with associated response type
2. **String interpolation for safety** - Prevent injection by design
3. **Protocol hierarchies for encoding** - Different guarantees (throwing, static types, etc.)
4. **Length-prefixed wire formats** - Write placeholder, encode, backfill length
5. **Hierarchical state machines** - Compose child machines for complex protocols
6. **Adaptive backpressure** - Dynamically adjust buffer targets based on consumer rate
7. **Actor + NIO alignment** - Eliminate context switches with `unownedExecutor`
8. **Cell/Row wrappers** - Rich metadata for better error messages
9. **Prepared statement caching** - Deduplicate concurrent preparations
10. **Graceful shutdown** - Drain pending operations before closing

## Key Libraries for Reference

- **valkey-swift** (github.com/valkey-io/valkey-swift) - Excellent RESP3 protocol, cluster support, pub/sub
- **postgres-nio** (github.com/vapor/postgres-nio) - Excellent query safety, type coercion, state machines

---
name: postgres
description: 'Expert guidance on using PostgreSQL with Swift. Use when developers mention: (1) PostgreSQL or Postgres in Swift, (2) postgres-nio library, (3) SQL queries in Swift, (4) PostgreSQL connection pooling, (5) prepared statements, (6) type-safe database access, (7) bulk loading or COPY FROM, (8) PostgresClient or PostgresConnection.'
references:
  - postgres-patterns.md
---

# PostgreSQL

The **postgres-nio** library provides a Swift PostgreSQL client with full async/await support, type-safe query building, connection pooling, and prepared statements.

## Quick Start

### Installation

Add to `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/vapor/postgres-nio.git", from: "1.21.0")
]
```

### Basic Usage

```swift
import PostgresNIO

// Using PostgresClient (recommended - includes connection pooling)
let client = PostgresClient(
    configuration: .init(
        host: "localhost",
        port: 5432,
        username: "postgres",
        password: "secret",
        database: "myapp",
        tls: .disable
    )
)

// Run as a service
try await withThrowingTaskGroup(of: Void.self) { group in
    group.addTask { try await client.run() }

    // Use client for queries
    let rows = try await client.query("SELECT id, name FROM users")
    for try await row in rows {
        let (id, name) = try row.decode((Int.self, String.self))
        print("User \(id): \(name)")
    }

    group.cancelAll()
}
```

## Type-Safe Queries

Queries use string interpolation to prevent SQL injection:

```swift
let userId = 123
let email = "alice@example.com"

// Interpolated values become parameter bindings ($1, $2, ...)
let query: PostgresQuery = "SELECT * FROM users WHERE id = \(userId) AND email = \(email)"
// Generates: "SELECT * FROM users WHERE id = $1 AND email = $2" with bindings [123, "alice@example.com"]

let rows = try await client.query(query)
```

### Dynamic Identifiers

Use `unescaped` for table/column names (not user input!):

```swift
let tableName = "users"  // Must be trusted, not user input
let query: PostgresQuery = "SELECT * FROM \(unescaped: tableName) WHERE id = \(userId)"
```

## Row Decoding

### Decode by Position

```swift
let rows = try await client.query("SELECT id, name, email, created_at FROM users")
for try await row in rows {
    let (id, name, email, createdAt) = try row.decode((Int.self, String.self, String.self, Date.self))
}
```

### Decode by Column Name

```swift
for try await row in rows {
    let id = try row["id"].decode(Int.self)
    let name = try row["name"].decode(String.self)
    let email = try row["email"].decode(String?.self)  // Optional
}
```

### Custom Types

```swift
struct User: Decodable {
    let id: Int
    let name: String
    let email: String
}

// Decode into custom type
for try await row in rows {
    let user = try row.decode(User.self)
}
```

## Prepared Statements

Define reusable prepared statements for performance:

```swift
struct GetUserByEmail: PostgresPreparedStatement {
    typealias Row = (Int, String, Date)

    static let sql = "SELECT id, name, created_at FROM users WHERE email = $1"

    var email: String

    func makeBindings() -> PostgresBindings {
        var bindings = PostgresBindings()
        bindings.append(email)
        return bindings
    }

    func decodeRow(_ row: PostgresRow) throws -> Row {
        try row.decode(Row.self)
    }
}

// Execute prepared statement
let results = try await connection.execute(GetUserByEmail(email: "alice@example.com"))
for try await (id, name, createdAt) in results {
    print("Found user \(id)")
}
```

## Transactions

```swift
try await client.withConnection { connection in
    try await connection.query("BEGIN")

    do {
        try await connection.query("INSERT INTO accounts (id, balance) VALUES (\(fromId), \(fromBalance - amount))")
        try await connection.query("INSERT INTO accounts (id, balance) VALUES (\(toId), \(toBalance + amount))")
        try await connection.query("COMMIT")
    } catch {
        try await connection.query("ROLLBACK")
        throw error
    }
}
```

## Bulk Loading (COPY FROM)

Efficiently load large datasets:

```swift
let rowCount = try await connection.copyFrom(
    table: "users",
    columns: ["name", "email", "created_at"],
    format: .csv(delimiter: ",", header: false)
) { writer in
    for user in users {
        var buffer = ByteBuffer()
        buffer.writeString("\(user.name),\(user.email),\(user.createdAt)\n")
        try await writer.write(buffer)
    }
}
print("Inserted \(rowCount) rows")
```

## Connection Configuration

```swift
let config = PostgresClient.Configuration(
    host: "localhost",
    port: 5432,
    username: "postgres",
    password: "secret",
    database: "myapp",
    tls: .prefer(.makeClientConfiguration()),
    options: .init(
        minimumConnections: 2,
        maximumConnections: 10,
        connectionIdleTimeout: .minutes(5),
        keepAliveBehavior: .init(frequency: .seconds(30))
    )
)

let client = PostgresClient(configuration: config)
```

### TLS Options

```swift
// Disable TLS (local development)
tls: .disable

// Prefer TLS (use if available)
tls: .prefer(.makeClientConfiguration())

// Require TLS (production)
tls: .require(.makeClientConfiguration())
```

### Unix Domain Socket

```swift
let config = PostgresClient.Configuration(
    unixSocketPath: "/var/run/postgresql/.s.PGSQL.5432",
    username: "postgres",
    database: "myapp"
)
```

## Error Handling

```swift
do {
    let rows = try await client.query("SELECT * FROM users WHERE id = \(id)")
    // ...
} catch let error as PSQLError {
    switch error.code {
    case .uniqueViolation:
        throw MyError.duplicateEntry
    case .foreignKeyViolation:
        throw MyError.invalidReference
    default:
        throw error
    }
}
```

## Streaming Large Results

Results are streamed automatically with backpressure:

```swift
let rows = try await client.query("SELECT * FROM large_table")

// Process one row at a time - memory efficient
for try await row in rows {
    let data = try row.decode(LargeData.self)
    try await processData(data)
}
```

## Supported Types

| Swift Type | PostgreSQL Type |
|------------|-----------------|
| `Int`, `Int32`, `Int64` | `integer`, `bigint` |
| `Float`, `Double` | `real`, `double precision` |
| `String` | `text`, `varchar` |
| `Bool` | `boolean` |
| `Date` | `timestamp`, `timestamptz` |
| `Data` | `bytea` |
| `UUID` | `uuid` |
| `[T]` | `array` |
| JSON types | `json`, `jsonb` |

## Reference Files

Load these files as needed for specific topics:

- **`references/postgres-patterns.md`** - String interpolation for SQL safety, protocol hierarchy for encoding/decoding, variadic generics for row decoding, prepared statement patterns, hierarchical state machines, backpressure-aware row streaming, COPY FROM bulk loading, wire protocol encoding

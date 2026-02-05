---
name: valkey
description: 'Expert guidance on using Valkey and Redis with Swift. Use when developers mention: (1) Valkey or Redis in Swift, (2) valkey-swift library, (3) RESP protocol or RESP3, (4) Redis cluster routing or hash slots, (5) pub/sub or subscriptions, (6) Redis transactions or MULTI/EXEC, (7) caching with Redis.'
references:
  - valkey-patterns.md
---

# Valkey / Redis

Valkey is an open-source, high-performance key-value store (fork of Redis). The **valkey-swift** library provides a Swift client with full async/await support, cluster routing, and pub/sub.

## Quick Start

### Installation

Add to `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/valkey-io/valkey-swift.git", from: "1.0.0")
]
```

### Basic Usage

```swift
import Valkey

// Connect to single server
let client = try await ValkeyClient.connect(to: .init(host: "localhost", port: 6379))

// Basic operations
try await client.set("key", "value")
let value = try await client.get("key") // Optional<String>

// With expiration
try await client.set("session", sessionData, expiration: .seconds(3600))

// Delete
try await client.del("key")
```

### Cluster Mode

```swift
// Connect to cluster
let client = try await ValkeyClient.connect(
    to: .cluster([
        .init(host: "node1.redis.local", port: 6379),
        .init(host: "node2.redis.local", port: 6379),
        .init(host: "node3.redis.local", port: 6379)
    ])
)

// Commands automatically route to correct shard
try await client.set("user:123", userData)
```

## Commands

### Strings

```swift
// SET with options
try await client.set("key", "value", condition: .nx)  // Only if not exists
try await client.set("key", "value", condition: .xx)  // Only if exists
try await client.set("key", "value", expiration: .milliseconds(5000))

// GET
let value = try await client.get("key")

// INCR/DECR
let newValue = try await client.incr("counter")
let decreased = try await client.decr("counter")
try await client.incrBy("counter", 10)
```

### Hashes

```swift
try await client.hset("user:123", field: "name", value: "Alice")
try await client.hset("user:123", fields: ["name": "Alice", "email": "alice@example.com"])

let name = try await client.hget("user:123", field: "name")
let user = try await client.hgetall("user:123") // [String: String]
```

### Lists

```swift
try await client.lpush("queue", "item1", "item2")
try await client.rpush("queue", "item3")

let item = try await client.lpop("queue")
let items = try await client.lrange("queue", start: 0, stop: -1)
```

### Sets

```swift
try await client.sadd("tags", "swift", "redis", "backend")
let isMember = try await client.sismember("tags", "swift")
let members = try await client.smembers("tags")
```

### Sorted Sets

```swift
try await client.zadd("leaderboard", score: 100, member: "player1")
try await client.zadd("leaderboard", members: [("player2", 200), ("player3", 150)])

let top10 = try await client.zrange("leaderboard", start: 0, stop: 9, withScores: true)
let rank = try await client.zrank("leaderboard", member: "player1")
```

## Pub/Sub

```swift
// Subscribe to channels
let subscription = try await client.subscribe(to: ["notifications", "updates"])

// Process messages
for try await message in subscription {
    switch message {
    case .message(let channel, let payload):
        print("Received on \(channel): \(payload)")
    case .subscribe(let channel, let count):
        print("Subscribed to \(channel)")
    }
}

// Publish
try await client.publish("notifications", message: "Hello subscribers!")

// Pattern subscribe
let patternSub = try await client.psubscribe(to: ["user:*", "event:*"])
```

## Transactions

```swift
// MULTI/EXEC transaction
let results = try await client.transaction(
    SET("key1", "value1"),
    SET("key2", "value2"),
    GET("key1")
)
// Results is tuple: (Result<String?, Error>, Result<String?, Error>, Result<String?, Error>)
```

## Pipelining

```swift
// Execute multiple commands in single round-trip
let (setResult, getResult, incrResult) = try await client.execute(
    SET("key", "value"),
    GET("key"),
    INCR("counter")
)
```

## Cluster Routing

Commands are automatically routed to the correct shard based on key hash slots:

```swift
// Keys with same hash tag go to same shard
try await client.set("{user:123}:profile", profileData)
try await client.set("{user:123}:settings", settingsData)
// Both keys route to same shard due to {user:123} hash tag
```

## Connection Configuration

```swift
let config = ValkeyClient.Configuration(
    endpoints: .single(.init(host: "localhost", port: 6379)),
    password: "secret",
    database: 0,
    connectionTimeout: .seconds(5),
    commandTimeout: .seconds(30),
    tls: .require(.makeClientConfiguration())
)

let client = try await ValkeyClient.connect(configuration: config)
```

## Error Handling

```swift
do {
    let value = try await client.get("key")
} catch let error as ValkeyClientError {
    switch error {
    case .connectionClosed:
        // Reconnect logic
    case .timeout:
        // Retry logic
    case .serverError(let message):
        print("Server error: \(message)")
    }
}
```

## Reference Files

Load these files as needed for specific topics:

- **`references/valkey-patterns.md`** - Command protocol pattern, RESP encoding/decoding, cluster routing with hash slots, subscription management, transaction patterns, connection pool integration, module extensions

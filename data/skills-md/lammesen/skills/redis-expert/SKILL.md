---
name: redis-expert
description: |
  Redis database expert for caching, data structures, Pub/Sub, Streams, Lua scripting,
  and performance optimization using Bun.redis native client.
  Use when working with Redis, caching strategies, key-value stores, real-time data,
  vector search, or document databases. Works alongside bun-expert skill.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Redis Expert Skill

You are an expert Redis developer with deep knowledge of Redis data structures, caching strategies, Pub/Sub messaging, Streams, Lua scripting, and the Redis Stack modules (RedisJSON, RediSearch, Vector Search). You help users build high-performance applications using Bun's native Redis client (`Bun.redis`).

## Cross-Skill Integration

This skill works alongside the **bun-expert** skill. When using Redis with Bun:
- Use `Bun.redis` for all Redis operations (not external packages)
- Leverage Bun's native performance optimizations
- Use `Bun.file()` for Redis persistence file operations
- Use Bun's test runner for Redis integration tests

---

## Bun.redis Client Fundamentals

### Connection Setup

```typescript
// Default client (uses VALKEY_URL, REDIS_URL, or localhost:6379)
import { redis } from "bun";
await redis.set("key", "value");

// Custom client with options
import { RedisClient } from "bun";
const client = new RedisClient("redis://username:password@localhost:6379", {
  connectionTimeout: 10000,     // Connection timeout (ms)
  idleTimeout: 0,               // Idle timeout (0 = no timeout)
  autoReconnect: true,          // Auto-reconnect on disconnect
  maxRetries: 10,               // Max reconnection attempts
  enableOfflineQueue: true,     // Queue commands when disconnected
  enableAutoPipelining: true,   // Automatic command batching
  tls: true,                    // Enable TLS (or provide TLSOptions)
});
```

### URL Formats

| Format | Description |
|--------|-------------|
| `redis://localhost:6379` | Standard connection |
| `redis://user:pass@host:6379/0` | With auth and database |
| `rediss://host:6379` | TLS connection |
| `redis+tls://host:6379` | TLS connection (alternative) |
| `redis+unix:///path/to/socket` | Unix socket |

### Connection Lifecycle

```typescript
const client = new RedisClient();
await client.connect();           // Explicit connect (optional - lazy by default)
await client.duplicate();         // Create duplicate connection for Pub/Sub
client.close();                   // Close connection

// Event handlers
client.onconnect = () => console.log("Connected");
client.onclose = (error) => console.log("Disconnected:", error);

// Status
console.log(client.connected);      // boolean
console.log(client.bufferedAmount); // bytes buffered
```

### Automatic Pipelining

Commands are automatically pipelined for performance. Use `Promise.all()` for concurrent operations:

```typescript
const [a, b, c] = await Promise.all([
  redis.get("key1"),
  redis.get("key2"),
  redis.get("key3")
]);
```

### Raw Command Execution

For commands not yet wrapped (66 commands native, 400+ via send):

```typescript
await redis.send("PFADD", ["hll", "value1", "value2"]);
await redis.send("LRANGE", ["mylist", "0", "-1"]);
await redis.send("SCAN", ["0", "MATCH", "user:*", "COUNT", "100"]);
```

### Error Handling

```typescript
try {
  await redis.get("key");
} catch (error) {
  if (error.code === "ERR_REDIS_CONNECTION_CLOSED") {
    // Handle connection closed
  } else if (error.code === "ERR_REDIS_AUTHENTICATION_FAILED") {
    // Handle auth failure
  } else if (error.message.includes("WRONGTYPE")) {
    // Handle type mismatch
  }
}
```

---

## Quick Reference - Native Commands

| Category | Commands |
|----------|----------|
| **Strings** | `set`, `get`, `getBuffer`, `del`, `exists`, `expire`, `ttl`, `incr`, `decr` |
| **Hashes** | `hget`, `hmget`, `hmset`, `hincrby`, `hincrbyfloat` |
| **Sets** | `sadd`, `srem`, `sismember`, `smembers`, `srandmember`, `spop` |
| **Pub/Sub** | `publish`, `subscribe`, `unsubscribe` |

For complete data structure reference, see [DATA-STRUCTURES.md](DATA-STRUCTURES.md).

---

## Key Naming Conventions

Use consistent naming throughout your application:

| Pattern | Example | Use Case |
|---------|---------|----------|
| `{entity}:{id}` | `user:123` | Simple keys |
| `{entity}:{id}:{field}` | `user:123:settings` | Sub-fields |
| `{namespace}:{entity}:{id}` | `app1:user:123` | Multi-tenant |
| `{operation}:{entity}:{id}` | `cache:user:123` | Operation-specific |
| `{entity}:{id}:{timestamp}` | `session:abc:1703001234` | Time-based |

---

## Quick Patterns Reference

### Cache-Aside Pattern

```typescript
async function cached<T>(key: string, ttl: number, fetch: () => Promise<T>): Promise<T> {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const data = await fetch();
  await redis.set(key, JSON.stringify(data));
  await redis.expire(key, ttl);
  return data;
}

// Usage
const user = await cached(`user:${id}`, 3600, () => db.findUser(id));
```

### Rate Limiting

```typescript
async function rateLimit(id: string, limit: number, window: number): Promise<boolean> {
  const key = `ratelimit:${id}`;
  const count = await redis.incr(key);
  if (count === 1) await redis.expire(key, window);
  return count <= limit;
}

// Usage
if (!await rateLimit(userId, 100, 60)) {
  throw new Error("Rate limit exceeded");
}
```

### Distributed Lock

```typescript
async function acquireLock(resource: string, ttlMs: number): Promise<string | null> {
  const token = crypto.randomUUID();
  const result = await redis.send("SET", [resource, token, "NX", "PX", ttlMs.toString()]);
  return result === "OK" ? token : null;
}

async function releaseLock(resource: string, token: string): Promise<boolean> {
  const script = `
    if redis.call("GET", KEYS[1]) == ARGV[1] then
      return redis.call("DEL", KEYS[1])
    end
    return 0
  `;
  const result = await redis.send("EVAL", [script, "1", resource, token]);
  return result === 1;
}
```

For complete patterns, see [PATTERNS.md](PATTERNS.md).

---

## Performance Guidelines

### Do's

1. **Use pipelining** for multiple commands: `Promise.all([...])`
2. **Prefer atomic operations**: `INCR` over `GET` + `SET`
3. **Use Lua scripts** for complex atomic operations
4. **Set appropriate TTLs** to prevent memory bloat
5. **Keep values small** (<100KB ideal, <1MB max)
6. **Use connection pooling** via RedisClient reuse

### Don'ts

1. **Avoid KEYS in production** - use `SCAN` instead
2. **Don't store large objects** - break into smaller pieces
3. **Avoid blocking commands** on main connection - use `duplicate()`
4. **Don't ignore TTLs** - set expiration on all cached data

### Monitoring

```typescript
// Server info
const info = await redis.send("INFO", ["memory"]);

// Memory usage
const memoryUsage = await redis.send("MEMORY", ["USAGE", "mykey"]);

// Slow log
const slowLog = await redis.send("SLOWLOG", ["GET", "10"]);

// Client list
const clients = await redis.send("CLIENT", ["LIST"]);
```

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [DATA-STRUCTURES.md](DATA-STRUCTURES.md) | Complete data structure reference (Strings, Hashes, Lists, Sets, Sorted Sets, Streams, etc.) |
| [STACK-FEATURES.md](STACK-FEATURES.md) | Redis Stack modules (RedisJSON, RediSearch, Vector Search, TimeSeries) |
| [PATTERNS.md](PATTERNS.md) | Caching strategies, session storage, rate limiting, distributed locks |
| [PUBSUB-STREAMS.md](PUBSUB-STREAMS.md) | Pub/Sub messaging and Streams for event sourcing |
| [SCRIPTING.md](SCRIPTING.md) | Lua scripting patterns and script management |
| [TESTING.md](TESTING.md) | Testing patterns for Redis operations with bun:test |

---

## Sub-Agents

| Agent | Use When |
|-------|----------|
| **redis-cache** | Implementing caching strategies, cache invalidation, TTL management |
| **redis-search** | Full-text search, vector similarity search, RAG applications |
| **redis-streams** | Event sourcing, message queues, real-time data pipelines |

---

## When This Skill Activates

This skill automatically activates when:
- Working with `Bun.redis` or `RedisClient`
- Implementing caching layers
- Building real-time features with Pub/Sub
- Designing event-driven architectures with Streams
- Adding full-text or vector search
- Writing Lua scripts for Redis
- Optimizing Redis performance

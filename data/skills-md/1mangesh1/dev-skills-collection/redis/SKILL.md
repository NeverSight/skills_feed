---
name: redis
description: Redis mastery for caching, data structures, pub/sub, and CLI operations. Use when user asks to "set up Redis", "cache data", "redis commands", "pub/sub", "redis data types", "session store", "rate limiting with Redis", or any Redis tasks.
---

# Redis

Caching, data structures, and real-time patterns.

## CLI Basics

```bash
# Connect
redis-cli
redis-cli -h hostname -p 6379 -a password

# Ping
redis-cli ping  # PONG

# Info
redis-cli info
redis-cli info memory
redis-cli info keyspace
```

## Strings

```bash
# Set/get
SET key "value"
GET key

# With expiration
SET session:abc "user123" EX 3600      # 1 hour
SETEX session:abc 3600 "user123"       # Same thing

# Set if not exists
SETNX lock:resource "owner123"

# Increment/decrement
INCR counter
INCRBY counter 5
DECR counter

# Multiple
MSET key1 "val1" key2 "val2"
MGET key1 key2
```

## Hashes

```bash
# Set fields
HSET user:1 name "Alice" email "alice@test.com" age 30

# Get
HGET user:1 name
HGETALL user:1
HMGET user:1 name email

# Increment field
HINCRBY user:1 age 1

# Check existence
HEXISTS user:1 email

# Delete field
HDEL user:1 age
```

## Lists

```bash
# Push
LPUSH queue "task1"       # Left (head)
RPUSH queue "task2"       # Right (tail)

# Pop
LPOP queue                # Left
RPOP queue                # Right
BLPOP queue 30            # Blocking pop (timeout 30s)

# Range
LRANGE queue 0 -1         # All elements
LRANGE queue 0 9          # First 10

# Length
LLEN queue

# Trim (keep only range)
LTRIM queue 0 99          # Keep first 100
```

## Sets

```bash
# Add/remove
SADD tags "python" "redis" "docker"
SREM tags "docker"

# Check membership
SISMEMBER tags "python"

# All members
SMEMBERS tags

# Count
SCARD tags

# Operations
SUNION tags1 tags2        # Union
SINTER tags1 tags2        # Intersection
SDIFF tags1 tags2         # Difference

# Random
SRANDMEMBER tags 2        # 2 random members
```

## Sorted Sets

```bash
# Add with score
ZADD leaderboard 100 "alice" 95 "bob" 87 "charlie"

# Get by rank
ZRANGE leaderboard 0 -1 WITHSCORES     # Ascending
ZREVRANGE leaderboard 0 2 WITHSCORES   # Top 3

# Get by score
ZRANGEBYSCORE leaderboard 90 100       # Score 90-100

# Rank
ZRANK leaderboard "alice"              # 0-based position
ZREVRANK leaderboard "alice"           # Reverse rank

# Increment score
ZINCRBY leaderboard 5 "bob"

# Count in range
ZCOUNT leaderboard 80 100
```

## Key Management

```bash
# Find keys
KEYS user:*               # Pattern match (avoid in production)
SCAN 0 MATCH user:* COUNT 100   # Safe iteration

# Expiration
EXPIRE key 3600           # Set TTL (seconds)
PEXPIRE key 3600000       # Milliseconds
TTL key                   # Check TTL
PERSIST key               # Remove expiration

# Delete
DEL key
UNLINK key                # Async delete (large keys)

# Type
TYPE key

# Exists
EXISTS key
```

## Pub/Sub

```bash
# Subscribe
SUBSCRIBE channel1 channel2

# Pattern subscribe
PSUBSCRIBE news.*

# Publish
PUBLISH channel1 "Hello subscribers!"

# Unsubscribe
UNSUBSCRIBE channel1
```

## Common Patterns

### Caching

```bash
# Cache-aside pattern
# 1. Check cache
GET cache:user:1
# 2. If miss, query DB, then set cache
SET cache:user:1 '{"name":"Alice"}' EX 300   # 5 min TTL
```

### Rate Limiting

```bash
# Sliding window rate limit
# Using sorted set with timestamp scores
ZADD ratelimit:user:1 <timestamp> <request-id>
ZREMRANGEBYSCORE ratelimit:user:1 0 <timestamp-window-ago>
ZCARD ratelimit:user:1
# If count > limit, reject
```

### Session Store

```bash
SET session:<session-id> '{"userId":1,"role":"admin"}' EX 86400
GET session:<session-id>
```

### Distributed Lock

```bash
# Acquire lock
SET lock:resource <unique-id> NX EX 30
# NX = only if not exists, EX = auto-expire

# Release lock (use Lua for atomicity)
EVAL "if redis.call('GET',KEYS[1]) == ARGV[1] then return redis.call('DEL',KEYS[1]) else return 0 end" 1 lock:resource <unique-id>
```

## Configuration

```bash
# Max memory
CONFIG SET maxmemory 256mb
CONFIG SET maxmemory-policy allkeys-lru

# Eviction policies:
# noeviction     - Return error on write when full
# allkeys-lru    - Evict least recently used
# allkeys-lfu    - Evict least frequently used
# volatile-lru   - LRU among keys with TTL
# volatile-ttl   - Evict shortest TTL first

# Persistence
CONFIG SET save "900 1 300 10"   # RDB snapshots
CONFIG SET appendonly yes        # AOF log

# View config
CONFIG GET maxmemory*
```

## Reference

For caching patterns, pub/sub, and Lua scripts: `references/patterns.md`

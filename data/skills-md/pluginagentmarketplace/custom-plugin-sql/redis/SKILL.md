---
name: redis
description: Redis data structures and commands including strings, lists, hashes, sets, sorted sets, streams, and transactions for high-performance caching and real-time applications.
sasmp_version: "1.3.0"
bonded_agent: 04-redis
bond_type: PRIMARY_BOND
---

# Redis Data Structures

## Getting Started

```bash
# Start Redis server
redis-server

# Connect to Redis CLI
redis-cli

# Test connection
ping                    # Returns "PONG"

# Select database
SELECT 0                # Default database
SELECT 1                # Database 1
```

## String Operations

```
// SET and GET
SET key value
SET user:1:name "John Doe"
GET user:1:name

// SET with options
SET key value EX 3600             // Expire in 3600 seconds
SET key value PX 3600000          // Expire in milliseconds
SET key value NX                  // Only if not exists
SET key value XX                  // Only if exists

// Numeric operations
SET counter 0
INCR counter              // Increment by 1
INCRBY counter 5          // Increment by N
DECR counter              // Decrement by 1
DECRBY counter 3          // Decrement by N
INCRBYFLOAT counter 2.5   // Increment by float

// String operations
APPEND key " suffix"      // Append to string
STRLEN key                // Get length
GETRANGE key 0 3          // Get substring
SETRANGE key 0 "new"      // Set substring

// Multiple keys
MSET key1 val1 key2 val2  // Set multiple
MGET key1 key2            // Get multiple
GETSET key newval         // Get old value and set new
```

## List Operations (Ordered collections)

```
// Push operations
LPUSH list value1 value2    // Push to left
RPUSH list value1 value2    // Push to right
LPUSHX list value           // Push only if exists
RPUSHX list value           // Push only if exists

// Pop operations
LPOP list                   // Remove and get from left
RPOP list                   // Remove and get from right
LPOP list 2                 // Pop multiple (Redis 6.2+)

// List queries
LRANGE list 0 -1            // Get all elements
LRANGE list 0 2             // Get first 3 elements
LINDEX list 1               // Get element at index
LLEN list                   // Get list length
LSET list 0 newvalue        // Set element at index

// Blocking operations
BLPOP list1 list2 10        // Block until pop or timeout
BRPOP list1 list2 10        // Block until right pop
BRPOPLPUSH src dst 10       // Block, pop right, push left

// Trimming
LTRIM list 0 2              // Keep only first 3 elements
```

## Hash Operations (Maps/objects)

```
// SET and GET
HSET hash field value       // Set single field
HSET hash f1 v1 f2 v2       // Set multiple fields
HGET hash field             // Get field value
HGETALL hash                // Get all fields and values

// Existence and length
HEXISTS hash field          // Check field exists
HLEN hash                   // Number of fields
HKEYS hash                  // Get all field names
HVALS hash                  // Get all values
HSTRLEN hash field          // Get value length

// Update operations
HINCRBY hash field 5        // Increment numeric field
HINCRBYFLOAT hash field 2.5 // Increment by float
HSETNX hash field value     // Set only if not exists

// Delete
HDEL hash field1 field2     // Delete fields
```

## Set Operations (Unordered unique values)

```
// Add and remove
SADD set member1 member2    // Add members
SREM set member1 member2    // Remove members
SISMEMBER set member        // Check membership
SMEMBERS set                // Get all members
SCARD set                   // Count members

// Set operations
SINTER set1 set2            // Intersection
SUNION set1 set2            // Union
SDIFF set1 set2             // Difference
SINTERSTORE dest s1 s2      // Store intersection result
SUNIONSTORE dest s1 s2      // Store union result
SDIFFSTORE dest s1 s2       // Store difference result

// Pop operations
SPOP set                    // Remove and return random member
SPOP set 2                  // Remove and return N members
SRANDMEMBER set             // Get random member without removing
SRANDMEMBER set 3           // Get N random members
```

## Sorted Set Operations (Ordered by score)

```
// Add and remove
ZADD zset 1 member1 2 member2    // Add with scores
ZREM zset member1                // Remove members
ZCARD zset                       // Count members
ZSCORE zset member               // Get score

// Range queries by score
ZRANGE zset 0 -1                 // Get all by index
ZRANGE zset 0 -1 WITHSCORES      // With scores
ZREVRANGE zset 0 -1              // Reverse order
ZREVRANGE zset 0 -1 WITHSCORES   // Reverse with scores

ZRANGEBYSCORE zset 10 50         // Get by score range
ZRANGEBYSCORE zset -inf +inf     // All scores
ZRANGEBYSCORE zset 10 50 LIMIT 0 5  // Pagination

// Score operations
ZINCRBY zset 5 member            // Increment score
ZCOUNT zset 10 50                // Count in score range

// Rank queries
ZRANK zset member                // Get rank (0-based)
ZREVRANK zset member             // Get reverse rank
```

## Key Operations

```
// Key management
KEYS pattern                // Find keys matching pattern
EXISTS key1 key2            // Check key existence
DEL key1 key2               // Delete keys
UNLINK key1 key2            // Async delete
TYPE key                    // Get key type

// Expiration
EXPIRE key 3600             // Set expiration (seconds)
PEXPIRE key 3600000         // Set expiration (milliseconds)
TTL key                     // Get TTL (seconds)
PTTL key                    // Get TTL (milliseconds)
PERSIST key                 // Remove expiration

// Renaming
RENAME oldkey newkey        // Rename key
RENAMENX oldkey newkey      // Rename only if new doesn't exist
```

## Transactions & Atomicity

```
// Transaction execution
MULTI                       // Start transaction
SET key1 value1
INCR key2
GET key3
EXEC                        // Execute all commands atomically

// Discard transaction
MULTI
SET key value
DISCARD                     // Cancel transaction

// Watch keys
WATCH key1 key2             // Monitor keys for changes
MULTI
SET key1 newvalue
EXEC                        // Fails if keys changed
```

## Pub/Sub Messaging

```
// Publisher
PUBLISH channel "message"   // Publish to channel

// Subscriber
SUBSCRIBE channel1 channel2 // Subscribe to channels
PSUBSCRIBE pattern*         // Subscribe to pattern
UNSUBSCRIBE channel         // Unsubscribe
PUNSUBSCRIBE pattern        // Unsubscribe from pattern

// Query subscriptions
PUBSUB CHANNELS             // Active channels
PUBSUB NUMSUB ch1 ch2       // Subscribers per channel
PUBSUB NUMPAT               // Pattern subscriptions count
```

## Server Commands

```
DBSIZE                      // Total keys in DB
FLUSHDB                     // Clear current DB
FLUSHALL                    // Clear all DBs
SAVE                        // Synchronous save
BGSAVE                      // Background save
LASTSAVE                    // Last save time
INFO                        // Server statistics
CONFIG GET parameter        // Get config value
CONFIG SET parameter value  // Set config value
```

## Next Steps

Learn Redis patterns for caching, sessions, rate limiting, and real-time applications in the `redis-patterns` skill.

---
name: system-design
description: Scalability, availability, and distributed systems design
domain: software-design
version: 1.0.0
tags: [scalability, availability, distributed, caching, load-balancing, database]
triggers:
  keywords:
    primary: [system design, scalability, distributed, architecture, high availability]
    secondary: [load balancer, caching, sharding, replication, cap theorem, microservices]
  context_boost: [interview, scale, performance, infrastructure]
  context_penalty: [frontend, ui, mobile]
  priority: high
---

# System Design

## Overview

Principles for designing systems that handle scale, remain available, and perform well under load.

---

## Scalability Fundamentals

### Vertical vs Horizontal Scaling

```
Vertical Scaling (Scale Up):
┌─────────────────────┐
│  Bigger Server      │
│  - More CPU         │
│  - More RAM         │
│  - Faster disk      │
└─────────────────────┘
Limit: Hardware ceiling

Horizontal Scaling (Scale Out):
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Server│ │Server│ │Server│ │Server│
└──────┘ └──────┘ └──────┘ └──────┘
         ↑
    Load Balancer
Limit: Coordination complexity
```

### Stateless Services

```typescript
// ❌ Stateful - stores session in memory
class BadService {
  private sessions = new Map();

  login(userId: string) {
    this.sessions.set(userId, { loggedIn: true });
  }
}

// ✅ Stateless - external session store
class GoodService {
  constructor(private sessionStore: Redis) {}

  async login(userId: string) {
    await this.sessionStore.set(`session:${userId}`, { loggedIn: true });
  }
}
```

---

## Load Balancing

### Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Round Robin | Cycle through servers | Equal capacity servers |
| Weighted RR | Based on server capacity | Mixed capacity |
| Least Connections | Route to least busy | Long-lived connections |
| IP Hash | Same IP → same server | Session stickiness |
| URL Hash | Same URL → same server | Cache optimization |

### Health Checks

```yaml
# Kubernetes-style health checks
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 3
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

```typescript
// Health check endpoints
app.get('/health/live', (req, res) => {
  // Am I running?
  res.status(200).json({ status: 'alive' });
});

app.get('/health/ready', async (req, res) => {
  // Can I serve traffic?
  const dbOk = await checkDatabase();
  const cacheOk = await checkCache();

  if (dbOk && cacheOk) {
    res.status(200).json({ status: 'ready' });
  } else {
    res.status(503).json({ status: 'not ready', db: dbOk, cache: cacheOk });
  }
});
```

---

## Caching Strategies

### Cache Patterns

```
Cache-Aside (Lazy Loading):
┌────────┐    miss     ┌────────┐
│  App   │ ──────────→ │  Cache │
│        │ ←────────── │        │
└────────┘    null     └────────┘
    │
    │  read
    ↓
┌────────┐
│   DB   │  ──── write ──→ Cache
└────────┘

Write-Through:
App → Cache → DB (synchronous)

Write-Behind (Write-Back):
App → Cache → (async) → DB
```

```typescript
// Cache-aside implementation
class CachedUserService {
  constructor(
    private cache: Redis,
    private db: Database
  ) {}

  async getUser(id: string): Promise<User> {
    // Try cache first
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return JSON.parse(cached);

    // Cache miss - read from DB
    const user = await this.db.users.findById(id);
    if (user) {
      // Store in cache with TTL
      await this.cache.set(`user:${id}`, JSON.stringify(user), 'EX', 3600);
    }
    return user;
  }

  async updateUser(id: string, data: Partial<User>): Promise<User> {
    const user = await this.db.users.update(id, data);
    // Invalidate cache
    await this.cache.del(`user:${id}`);
    return user;
  }
}
```

### Cache Invalidation

| Strategy | Description | Complexity |
|----------|-------------|------------|
| TTL | Expire after time | Simple |
| Event-based | Invalidate on write | Medium |
| Version-based | Key includes version | Medium |
| Tag-based | Group related keys | Complex |

---

## Database Scaling

### Read Replicas

```
                    ┌─────────────────┐
     Writes ──────→ │   Primary DB    │
                    └────────┬────────┘
                             │ replication
           ┌─────────────────┼─────────────────┐
           ↓                 ↓                 ↓
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Replica 1│      │ Replica 2│      │ Replica 3│
    └──────────┘      └──────────┘      └──────────┘
           ↑                 ↑                 ↑
           └─────── Reads ───┴────────────────┘
```

### Sharding (Partitioning)

```typescript
// Hash-based sharding
function getShard(userId: string, numShards: number): number {
  const hash = crypto.createHash('md5').update(userId).digest('hex');
  return parseInt(hash.slice(0, 8), 16) % numShards;
}

// Range-based sharding
function getShardByDate(date: Date): string {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  return `orders_${year}_${month.toString().padStart(2, '0')}`;
}

// Consistent hashing for dynamic shards
class ConsistentHash {
  private ring: Map<number, string> = new Map();

  addNode(node: string) {
    for (let i = 0; i < 150; i++) { // Virtual nodes
      const hash = this.hash(`${node}:${i}`);
      this.ring.set(hash, node);
    }
  }

  getNode(key: string): string {
    const hash = this.hash(key);
    // Find next node on ring
    for (const [nodeHash, node] of [...this.ring.entries()].sort()) {
      if (nodeHash >= hash) return node;
    }
    return this.ring.values().next().value;
  }
}
```

---

## Message Queues

### Patterns

```
Point-to-Point:
Producer → Queue → Consumer

Pub/Sub:
              ┌─→ Subscriber 1
Publisher → Topic ─→ Subscriber 2
              └─→ Subscriber 3

Work Queue:
              ┌─→ Worker 1
Producer → Queue ─→ Worker 2  (competing consumers)
              └─→ Worker 3
```

### Delivery Guarantees

| Guarantee | Description | Implementation |
|-----------|-------------|----------------|
| At-most-once | May lose messages | Fire and forget |
| At-least-once | May duplicate | Ack after process |
| Exactly-once | No loss, no dupe | Idempotency + dedup |

```typescript
// Idempotent processing
async function processOrder(event: OrderEvent) {
  // Check if already processed
  const processed = await redis.get(`processed:${event.id}`);
  if (processed) {
    console.log(`Already processed ${event.id}`);
    return;
  }

  // Process the order
  await db.orders.create(event.order);

  // Mark as processed (with TTL for cleanup)
  await redis.set(`processed:${event.id}`, '1', 'EX', 86400 * 7);
}
```

---

## High Availability

### Redundancy Patterns

```
Active-Active:
┌────────┐     ┌────────┐
│Server A│ ←─→ │Server B│  Both handle traffic
└────────┘     └────────┘

Active-Passive:
┌────────┐     ┌────────┐
│ Active │ ──→ │Standby │  Failover on failure
└────────┘     └────────┘
```

### Circuit Breaker

```typescript
class CircuitBreaker {
  private failures = 0;
  private lastFailure: Date | null = null;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  constructor(
    private threshold: number = 5,
    private timeout: number = 30000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailure!.getTime() > this.timeout) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit is open');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }

  private onFailure() {
    this.failures++;
    this.lastFailure = new Date();
    if (this.failures >= this.threshold) {
      this.state = 'open';
    }
  }
}
```

---

## CAP Theorem

```
         Consistency
            /\
           /  \
          /    \
         /      \
        /   CA   \
       /──────────\
      /            \
     / CP        AP \
    /________________\
Partition          Availability
Tolerance

CA: Single node (RDBMS)
CP: MongoDB, HBase (may reject writes during partition)
AP: Cassandra, DynamoDB (eventual consistency)
```

### Consistency Models

| Model | Description | Example |
|-------|-------------|---------|
| Strong | Read sees latest write | RDBMS |
| Eventual | Eventually consistent | DNS, Cassandra |
| Causal | Respects causality | Chat apps |
| Read-your-writes | See your own writes | Social feeds |

---

## Rate Limiting

### Algorithms

```typescript
// Token Bucket
class TokenBucket {
  private tokens: number;
  private lastRefill: number;

  constructor(
    private capacity: number,
    private refillRate: number // tokens per second
  ) {
    this.tokens = capacity;
    this.lastRefill = Date.now();
  }

  consume(tokens: number = 1): boolean {
    this.refill();
    if (this.tokens >= tokens) {
      this.tokens -= tokens;
      return true;
    }
    return false;
  }

  private refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(
      this.capacity,
      this.tokens + elapsed * this.refillRate
    );
    this.lastRefill = now;
  }
}

// Sliding Window
class SlidingWindowRateLimiter {
  constructor(
    private redis: Redis,
    private limit: number,
    private window: number // seconds
  ) {}

  async isAllowed(key: string): Promise<boolean> {
    const now = Date.now();
    const windowStart = now - this.window * 1000;

    const pipe = this.redis.pipeline();
    pipe.zremrangebyscore(key, 0, windowStart);
    pipe.zadd(key, now, `${now}`);
    pipe.zcard(key);
    pipe.expire(key, this.window);

    const results = await pipe.exec();
    const count = results[2][1] as number;

    return count <= this.limit;
  }
}
```

---

## Common System Designs

| System | Key Components |
|--------|----------------|
| URL Shortener | Hash function, Redis cache, DB |
| Twitter Feed | Fan-out, Redis timeline, Kafka |
| Chat App | WebSocket, Presence, Message queue |
| E-commerce | Cart service, Inventory, Payment |
| Video Streaming | CDN, Chunking, Adaptive bitrate |

---

## Related Skills

- [[architecture-patterns]] - Microservices, event-driven
- [[database]] - Database optimization
- [[caching-implementation]] - Cache strategies
- [[reliability-engineering]] - SRE practices

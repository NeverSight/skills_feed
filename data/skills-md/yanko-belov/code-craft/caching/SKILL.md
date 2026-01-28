---
name: caching
description: Use when same data is fetched repeatedly. Use when database queries are slow. Use when implementing caching without invalidation strategy.
---

# Caching

## Overview

**Cache aggressively, but always have an invalidation strategy.**

Caching improves performance dramatically, but stale data causes bugs. Every cache needs a plan for freshness.

## When to Use

- Same data fetched repeatedly
- Expensive computations
- Slow database queries
- External API rate limits
- Asked to "just add caching"

## The Iron Rule

```
NEVER add a cache without defining its invalidation strategy.
```

**No exceptions:**
- Not for "it rarely changes"
- Not for "TTL is enough"
- Not for "we'll figure it out later"
- Not for "users can refresh"

## Detection: Cache Without Strategy Smell

If cache has no invalidation plan, STOP:

```typescript
// ❌ VIOLATION: Cache without invalidation strategy
const cache = new Map();

async function getUser(id: string) {
  if (cache.has(id)) {
    return cache.get(id);  // Could be stale forever!
  }
  
  const user = await db.users.findById(id);
  cache.set(id, user);  // When does this expire? When user updates?
  return user;
}
```

Problems:
- User updates name → cache shows old name
- No memory limit → memory leak
- No TTL → stale forever
- Distributed system → multiple stale copies

## The Correct Pattern: Cache with Strategy

```typescript
// ✅ CORRECT: Cache with TTL and invalidation

interface CacheEntry<T> {
  data: T;
  expiresAt: number;
}

class UserCache {
  private cache = new Map<string, CacheEntry<User>>();
  private TTL_MS = 5 * 60 * 1000; // 5 minutes
  
  async get(id: string): Promise<User> {
    const cached = this.cache.get(id);
    
    if (cached && cached.expiresAt > Date.now()) {
      return cached.data;
    }
    
    const user = await db.users.findById(id);
    this.set(id, user);
    return user;
  }
  
  set(id: string, user: User): void {
    this.cache.set(id, {
      data: user,
      expiresAt: Date.now() + this.TTL_MS
    });
  }
  
  // Explicit invalidation on updates
  invalidate(id: string): void {
    this.cache.delete(id);
  }
  
  invalidateAll(): void {
    this.cache.clear();
  }
}

// Usage with invalidation on write
async function updateUser(id: string, data: UpdateUserDto) {
  const user = await db.users.update(id, data);
  userCache.invalidate(id);  // Clear stale cache
  return user;
}
```

## Cache Invalidation Strategies

### 1. Time-Based (TTL)
```typescript
// Good for: data that can be slightly stale
const TTL = 60 * 1000; // 1 minute
cache.set(key, value, { ttl: TTL });
```

### 2. Write-Through
```typescript
// Good for: data you control writes for
async function updateProduct(id, data) {
  const product = await db.products.update(id, data);
  await cache.set(`product:${id}`, product);  // Update cache on write
  return product;
}
```

### 3. Event-Based
```typescript
// Good for: distributed systems
eventBus.on('user.updated', (userId) => {
  cache.delete(`user:${userId}`);
});

eventBus.on('product.priceChanged', (productId) => {
  cache.delete(`product:${productId}`);
});
```

### 4. Cache-Aside (Lazy)
```typescript
// Good for: read-heavy, tolerance for staleness
async function getProduct(id) {
  let product = await cache.get(`product:${id}`);
  if (!product) {
    product = await db.products.findById(id);
    await cache.set(`product:${id}`, product, { ttl: 300 });
  }
  return product;
}
```

## What to Cache

| Good to Cache | Bad to Cache |
|---------------|--------------|
| User profiles | Session tokens |
| Product catalog | Payment status |
| Configuration | Real-time inventory |
| API responses | User-specific calculations |
| Computed aggregates | Rapidly changing data |

## Redis Example

```typescript
import Redis from 'ioredis';

const redis = new Redis();

class ProductCache {
  private prefix = 'product:';
  private ttl = 300; // 5 minutes
  
  async get(id: string): Promise<Product | null> {
    const cached = await redis.get(this.prefix + id);
    return cached ? JSON.parse(cached) : null;
  }
  
  async set(id: string, product: Product): Promise<void> {
    await redis.setex(
      this.prefix + id,
      this.ttl,
      JSON.stringify(product)
    );
  }
  
  async invalidate(id: string): Promise<void> {
    await redis.del(this.prefix + id);
  }
  
  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await redis.keys(this.prefix + pattern);
    if (keys.length) await redis.del(...keys);
  }
}
```

## Pressure Resistance Protocol

### 1. "It Rarely Changes"
**Pressure:** "This data almost never updates"

**Response:** "Almost never" still means sometimes. When it does, stale cache = bugs.

**Action:** Add TTL at minimum. Add invalidation on write.

### 2. "TTL Is Enough"
**Pressure:** "We'll just expire after 5 minutes"

**Response:** 5 minutes of stale data might be unacceptable. User updates profile, sees old data.

**Action:** TTL + write-through invalidation.

### 3. "We'll Figure It Out Later"
**Pressure:** "Just add caching, we'll handle staleness if it's a problem"

**Response:** Staleness bugs are hard to debug. Design invalidation upfront.

**Action:** No cache without invalidation strategy defined.

## Red Flags - STOP and Reconsider

- Cache with no TTL
- No invalidation on data updates
- "Users can refresh to see new data"
- In-memory cache in distributed system
- Cache without memory limits

**All of these mean: Define invalidation strategy.**

## Quick Reference

| Pattern | Use When | Invalidation |
|---------|----------|--------------|
| TTL only | Staleness OK | Automatic expiry |
| Write-through | You control writes | Update cache on write |
| Event-based | Distributed system | Pub/sub on changes |
| Cache-aside | Read-heavy | TTL + manual invalidate |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Rarely changes" | Rarely ≠ never. Plan for it. |
| "TTL is enough" | TTL + invalidation is better. |
| "Figure it out later" | Staleness bugs are hard to trace. |
| "Users can refresh" | That's a bug, not a feature. |
| "It's just for performance" | Stale data breaks functionality. |

## The Bottom Line

**Every cache needs: TTL, size limit, and invalidation strategy.**

Cache aggressively for performance. But always know how the cache gets invalidated when data changes. "It rarely changes" is not a strategy.

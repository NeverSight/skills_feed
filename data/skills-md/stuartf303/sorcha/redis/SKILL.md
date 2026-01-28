---
name: redis
description: |
  Implements Redis caching, session management, and distributed coordination for the Sorcha platform.
  Use when: Adding caching layers, token revocation, rate limiting, SignalR backplane, or distributed state.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Redis Skill

Sorcha uses Redis via StackExchange.Redis for caching, token revocation tracking, rate limiting, and distributed coordination. All services share a single Redis instance managed by .NET Aspire with circuit breaker resilience.

## Quick Start

### Aspire Configuration

```csharp
// src/Apps/Sorcha.AppHost/AppHost.cs
var redis = builder.AddRedis("redis")
    .WithRedisCommander();

// Reference from any service
var blueprintService = builder.AddProject<Projects.Sorcha_Blueprint_Service>()
    .WithReference(redis);
```

### Cache Store Usage

```csharp
// Inject ICacheStore from Sorcha.Storage.Redis
public class MyService(ICacheStore cache)
{
    public async Task<User?> GetUserAsync(string id)
    {
        return await cache.GetAsync<User>($"user:{id}");
    }
    
    public async Task SetUserAsync(User user)
    {
        await cache.SetAsync($"user:{user.Id}", user, TimeSpan.FromMinutes(15));
    }
}
```

### Direct IConnectionMultiplexer

```csharp
// For operations beyond ICacheStore (Sets, rate limiting, etc.)
public class TokenService(IConnectionMultiplexer redis)
{
    private readonly IDatabase _db = redis.GetDatabase();
    
    public async Task TrackTokenAsync(string userId, string jti)
    {
        await _db.SetAddAsync($"auth:user_tokens:{userId}", jti);
    }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Key prefix | Namespace isolation | `sorcha:`, `auth:` |
| TTL | Automatic expiration | `TimeSpan.FromMinutes(15)` |
| Circuit breaker | Graceful degradation | Breaks after 5 failures |
| Sets | Token tracking | `SetAddAsync`, `SetMembersAsync` |
| Counters | Rate limiting | `StringIncrementAsync` |

## Common Patterns

### Rate Limiting

**When:** Protecting auth endpoints from brute force.

```csharp
public async Task<bool> IsRateLimitedAsync(string identifier)
{
    var key = $"auth:failed:{identifier}";
    var count = await _db.StringIncrementAsync(key);
    
    if (count == 1)
        await _db.KeyExpireAsync(key, TimeSpan.FromSeconds(60));
    
    return count >= MaxFailedAttempts;
}
```

### Token Revocation

**When:** Invalidating JWTs before expiration.

```csharp
public async Task RevokeTokenAsync(string jti, DateTimeOffset expiresAt)
{
    var ttl = expiresAt - DateTimeOffset.UtcNow;
    if (ttl > TimeSpan.Zero)
        await _db.StringSetAsync($"auth:revoked:{jti}", "revoked", ttl);
}
```

## See Also

- [patterns](references/patterns.md) - Caching, resilience, key naming
- [workflows](references/workflows.md) - Setup, testing, debugging

## Related Skills

- **aspire** - Redis resource configuration and service discovery
- **jwt** - Token revocation integration
- **signalr** - Redis backplane for scale-out
- **docker** - Redis container configuration

## Documentation Resources

> Fetch latest Redis and StackExchange.Redis documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "StackExchange.Redis" or "redis"
2. Prefer website documentation (`/websites/redis_io`) for concepts
3. Use `/stackexchange/stackexchange.redis` for .NET-specific patterns

**Library IDs:**
- `/stackexchange/stackexchange.redis` - .NET client (344 snippets)
- `/websites/redis_io` - Redis concepts (29k+ snippets)

**Recommended Queries:**
- "Connection pooling multiplexer patterns best practices"
- "Caching patterns TTL expiration strategies"
- "Pub/Sub patterns distributed systems"
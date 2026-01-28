---
name: caching
description: In-memory caching patterns for the 3SC widget host. Covers cache strategies, invalidation, TTL policies, and when to cache vs when to fetch.
---

# Caching

## Overview

Caching improves performance by reducing database and network calls. This skill covers in-memory caching patterns suitable for desktop applications.

## Definition of Done (DoD)

- [ ] Frequently accessed data is cached appropriately
- [ ] Cache has defined TTL (time-to-live) for each entry type
- [ ] Cache invalidation is implemented for write operations
- [ ] Memory usage is bounded (max entries or max memory)
- [ ] Cache misses are logged for monitoring
- [ ] Thread-safety is ensured for concurrent access

## When to Cache

| Scenario | Cache? | TTL | Notes |
|----------|--------|-----|-------|
| Widget catalog (read-heavy) | ✅ Yes | 5 min | Invalidate on install/uninstall |
| Installed widgets list | ✅ Yes | 10 min | Invalidate on changes |
| Layout configurations | ✅ Yes | 5 min | Invalidate on save |
| User preferences | ✅ Yes | Session | Load once, cache for session |
| Active widget instances | ❌ No | - | Already in memory |
| Real-time data (sync queue) | ❌ No | - | Needs fresh data |

## Cache Service Implementation

### Interface

```csharp
public interface ICacheService
{
    /// <summary>Gets cached value or default if not found/expired.</summary>
    T? Get<T>(string key) where T : class;
    
    /// <summary>Gets cached value or executes factory to populate.</summary>
    Task<T> GetOrCreateAsync<T>(
        string key, 
        Func<CancellationToken, Task<T>> factory,
        TimeSpan? expiration = null,
        CancellationToken cancellationToken = default) where T : class;
    
    /// <summary>Sets value with optional expiration.</summary>
    void Set<T>(string key, T value, TimeSpan? expiration = null) where T : class;
    
    /// <summary>Removes specific key.</summary>
    void Remove(string key);
    
    /// <summary>Removes all keys matching prefix.</summary>
    void RemoveByPrefix(string prefix);
    
    /// <summary>Clears entire cache.</summary>
    void Clear();
    
    /// <summary>Gets cache statistics.</summary>
    CacheStatistics GetStatistics();
}

public record CacheStatistics(int EntryCount, long Hits, long Misses, long Evictions);
```

### Implementation

```csharp
public class MemoryCacheService : ICacheService, IDisposable
{
    private readonly ConcurrentDictionary<string, CacheEntry> _cache = new();
    private readonly Timer _cleanupTimer;
    private readonly int _maxEntries;
    
    private long _hits;
    private long _misses;
    private long _evictions;
    
    public MemoryCacheService(int maxEntries = 1000, TimeSpan? cleanupInterval = null)
    {
        _maxEntries = maxEntries;
        _cleanupTimer = new Timer(
            CleanupExpired, 
            null, 
            cleanupInterval ?? TimeSpan.FromMinutes(1),
            cleanupInterval ?? TimeSpan.FromMinutes(1));
    }
    
    public T? Get<T>(string key) where T : class
    {
        if (_cache.TryGetValue(key, out var entry) && !entry.IsExpired)
        {
            Interlocked.Increment(ref _hits);
            entry.Touch();
            return (T)entry.Value;
        }
        
        Interlocked.Increment(ref _misses);
        
        if (entry?.IsExpired == true)
        {
            _cache.TryRemove(key, out _);
        }
        
        return null;
    }
    
    public async Task<T> GetOrCreateAsync<T>(
        string key,
        Func<CancellationToken, Task<T>> factory,
        TimeSpan? expiration = null,
        CancellationToken cancellationToken = default) where T : class
    {
        var existing = Get<T>(key);
        if (existing != null)
            return existing;
        
        // Use lock to prevent duplicate factory calls
        var value = await factory(cancellationToken).ConfigureAwait(false);
        Set(key, value, expiration);
        return value;
    }
    
    public void Set<T>(string key, T value, TimeSpan? expiration = null) where T : class
    {
        EnsureCapacity();
        
        var entry = new CacheEntry(value, expiration);
        _cache[key] = entry;
        
        Log.Debug("Cache set: {Key}, Expires: {Expiration}", 
            key, entry.ExpiresAt?.ToString("HH:mm:ss") ?? "never");
    }
    
    public void Remove(string key)
    {
        if (_cache.TryRemove(key, out _))
        {
            Log.Debug("Cache removed: {Key}", key);
        }
    }
    
    public void RemoveByPrefix(string prefix)
    {
        var keysToRemove = _cache.Keys
            .Where(k => k.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
            .ToList();
        
        foreach (var key in keysToRemove)
        {
            _cache.TryRemove(key, out _);
        }
        
        Log.Debug("Cache cleared {Count} entries with prefix: {Prefix}", 
            keysToRemove.Count, prefix);
    }
    
    public void Clear()
    {
        var count = _cache.Count;
        _cache.Clear();
        Log.Information("Cache cleared: {Count} entries removed", count);
    }
    
    public CacheStatistics GetStatistics() => 
        new(_cache.Count, _hits, _misses, _evictions);
    
    private void EnsureCapacity()
    {
        if (_cache.Count < _maxEntries)
            return;
        
        // Evict oldest entries (LRU)
        var toEvict = _cache
            .OrderBy(x => x.Value.LastAccessed)
            .Take(_cache.Count / 4)  // Evict 25%
            .Select(x => x.Key)
            .ToList();
        
        foreach (var key in toEvict)
        {
            if (_cache.TryRemove(key, out _))
            {
                Interlocked.Increment(ref _evictions);
            }
        }
        
        Log.Debug("Cache evicted {Count} entries", toEvict.Count);
    }
    
    private void CleanupExpired(object? state)
    {
        var expired = _cache
            .Where(x => x.Value.IsExpired)
            .Select(x => x.Key)
            .ToList();
        
        foreach (var key in expired)
        {
            _cache.TryRemove(key, out _);
        }
        
        if (expired.Count > 0)
        {
            Log.Debug("Cache cleanup: {Count} expired entries removed", expired.Count);
        }
    }
    
    public void Dispose()
    {
        _cleanupTimer.Dispose();
    }
    
    private class CacheEntry
    {
        public object Value { get; }
        public DateTimeOffset? ExpiresAt { get; }
        public DateTimeOffset LastAccessed { get; private set; }
        public bool IsExpired => ExpiresAt.HasValue && DateTimeOffset.UtcNow > ExpiresAt;
        
        public CacheEntry(object value, TimeSpan? expiration)
        {
            Value = value;
            LastAccessed = DateTimeOffset.UtcNow;
            ExpiresAt = expiration.HasValue 
                ? DateTimeOffset.UtcNow.Add(expiration.Value) 
                : null;
        }
        
        public void Touch() => LastAccessed = DateTimeOffset.UtcNow;
    }
}
```

## Cache Keys Convention

Use hierarchical keys for easy invalidation:

```csharp
public static class CacheKeys
{
    // Pattern: {entity}:{scope}:{identifier}
    
    public const string WidgetCatalog = "widgets:catalog:all";
    public const string InstalledWidgets = "widgets:installed:all";
    
    public static string Widget(string widgetKey) => $"widgets:detail:{widgetKey}";
    public static string Layout(Guid layoutId) => $"layouts:detail:{layoutId}";
    public static string UserSettings(string key) => $"settings:user:{key}";
    
    // Prefixes for bulk invalidation
    public const string WidgetsPrefix = "widgets:";
    public const string LayoutsPrefix = "layouts:";
}
```

## Repository with Caching

```csharp
public class CachedWidgetRepository : IWidgetRepository
{
    private readonly IWidgetRepository _inner;
    private readonly ICacheService _cache;
    
    private static readonly TimeSpan CacheDuration = TimeSpan.FromMinutes(5);
    
    public CachedWidgetRepository(IWidgetRepository inner, ICacheService cache)
    {
        _inner = inner;
        _cache = cache;
    }
    
    public async Task<IReadOnlyList<Widget>> GetAllAsync(CancellationToken ct = default)
    {
        return await _cache.GetOrCreateAsync(
            CacheKeys.WidgetCatalog,
            async token => (await _inner.GetAllAsync(token)).ToList(),
            CacheDuration,
            ct);
    }
    
    public async Task<Widget?> GetByKeyAsync(string widgetKey, CancellationToken ct = default)
    {
        return await _cache.GetOrCreateAsync(
            CacheKeys.Widget(widgetKey),
            token => _inner.GetByKeyAsync(widgetKey, token),
            CacheDuration,
            ct);
    }
    
    public async Task AddAsync(Widget widget, CancellationToken ct = default)
    {
        await _inner.AddAsync(widget, ct);
        
        // Invalidate related caches
        _cache.Remove(CacheKeys.WidgetCatalog);
        _cache.Remove(CacheKeys.Widget(widget.WidgetKey));
    }
    
    public async Task UpdateAsync(Widget widget, CancellationToken ct = default)
    {
        await _inner.UpdateAsync(widget, ct);
        
        _cache.Remove(CacheKeys.Widget(widget.WidgetKey));
        _cache.Remove(CacheKeys.WidgetCatalog);
    }
    
    public async Task DeleteAsync(string widgetKey, CancellationToken ct = default)
    {
        await _inner.DeleteAsync(widgetKey, ct);
        
        _cache.RemoveByPrefix(CacheKeys.WidgetsPrefix);
    }
}
```

## Cache-Aside Pattern

For more control over cache population:

```csharp
public async Task<Widget?> GetWidgetAsync(string widgetKey, CancellationToken ct)
{
    // 1. Check cache
    var cached = _cache.Get<Widget>(CacheKeys.Widget(widgetKey));
    if (cached != null)
        return cached;
    
    // 2. Load from database
    var widget = await _repository.GetByKeyAsync(widgetKey, ct);
    
    // 3. Populate cache (even if null, to prevent repeated lookups)
    if (widget != null)
    {
        _cache.Set(CacheKeys.Widget(widgetKey), widget, TimeSpan.FromMinutes(5));
    }
    
    return widget;
}
```

## Cache Warming

Pre-populate cache at startup:

```csharp
public class CacheWarmupService
{
    private readonly ICacheService _cache;
    private readonly IWidgetRepository _widgetRepo;
    private readonly ILayoutRepository _layoutRepo;
    
    public async Task WarmupAsync(CancellationToken ct)
    {
        Log.Information("Starting cache warmup");
        
        var tasks = new[]
        {
            WarmWidgetsAsync(ct),
            WarmLayoutsAsync(ct)
        };
        
        await Task.WhenAll(tasks);
        
        var stats = _cache.GetStatistics();
        Log.Information("Cache warmup complete: {Count} entries", stats.EntryCount);
    }
    
    private async Task WarmWidgetsAsync(CancellationToken ct)
    {
        var widgets = await _widgetRepo.GetAllAsync(ct);
        _cache.Set(CacheKeys.WidgetCatalog, widgets.ToList(), TimeSpan.FromMinutes(10));
        
        foreach (var widget in widgets)
        {
            _cache.Set(CacheKeys.Widget(widget.WidgetKey), widget, TimeSpan.FromMinutes(10));
        }
    }
    
    private async Task WarmLayoutsAsync(CancellationToken ct)
    {
        // Similar pattern...
    }
}
```

## Best Practices

| Practice | Reason |
|----------|--------|
| Always set TTL | Prevents stale data and memory leaks |
| Invalidate on writes | Ensures cache consistency |
| Use hierarchical keys | Enables prefix-based invalidation |
| Bound cache size | Prevents unbounded memory growth |
| Log cache metrics | Helps tune cache effectiveness |
| Don't cache nulls (usually) | Unless preventing repeated lookups |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Unbounded cache | Memory leak | Set max entries |
| No TTL | Stale data forever | Always set expiration |
| Cache complex graphs | Inconsistent updates | Cache simple DTOs |
| Distributed cache for desktop | Over-engineering | Use simple in-memory |
| Caching mutable objects | Race conditions | Cache immutable/copies |

## Monitoring

```csharp
// Log cache effectiveness periodically
public void LogCacheMetrics()
{
    var stats = _cache.GetStatistics();
    var hitRate = stats.Hits + stats.Misses > 0 
        ? (double)stats.Hits / (stats.Hits + stats.Misses) * 100 
        : 0;
    
    Log.Information(
        "Cache metrics - Entries: {Entries}, HitRate: {HitRate:F1}%, " +
        "Hits: {Hits}, Misses: {Misses}, Evictions: {Evictions}",
        stats.EntryCount, hitRate, stats.Hits, stats.Misses, stats.Evictions);
}
```

## References

- [Caching Best Practices](https://docs.microsoft.com/en-us/dotnet/core/extensions/caching)
- [Cache-Aside Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/cache-aside)

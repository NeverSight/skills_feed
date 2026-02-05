---
name: laravel-performance-caching
description: Use framework caches and value/query caching to reduce work; add tags, locks, and explicit invalidation strategies for correctness
---

# Caching Basics

## Framework caches

```
php artisan route:cache
php artisan config:cache
php artisan view:cache
```

Clear with the corresponding `clear` commands when needed in deployments.

## Values and queries

```php
Cache::remember("post:{$id}", 600, fn () => Post::findOrFail($id));
```

- Choose TTLs based on freshness requirements
- Invalidate explicitly on writes when correctness matters

## Patterns and Strategies

```php
// Stable keys and scopes (e.g., tenant, locale)
Cache::remember("tenant:{$tenantId}:users:index:page:1", now()->addMinutes(5), function () {
    return User::with('team')->paginate(50);
});

// Tags (supported drivers) for grouped invalidation
Cache::tags(['users'])->remember('users.index.page.1', now()->addMinutes(5), fn () => ...);
Cache::tags(['users'])->flush();

// Locks to ensure exclusive expensive work
Cache::lock('reports:daily', 30)->block(5, function () {
    generateReports();
});
```

- Use stable, namespaced keys; include any scoping dimension
- Prefer `remember()` to prevent thundering herds
- Use cache tags (if supported) to invalidate related entries together
- Avoid caching highly dynamic or user-specific data without a plan
- Document invalidation triggers next to cached code

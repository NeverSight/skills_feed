---
name: laravel:eloquent-relationships
description: Define clear relationships and load data efficiently; prevent N+1, use constraints, counts/sums, and pivot syncing safely
---

# Eloquent Relationships and Loading

Model relationships express your domain; load only what you need.

## Commands

```
# Typical loading
Post::with(['author', 'tags'])->withCount('comments')->paginate(20);

# Constrained eager loading
User::with(['posts' => fn($q) => $q->latest()->where('published', true)])->find($id);

# Pivot ops (many-to-many)
$post->tags()->sync([1,2,3]);       // atomic replace
$post->tags()->syncWithoutDetaching([4]);

# Chunking large reads
Order::where('status', 'open')->lazy()->each(fn($o) => ...);
```

## Patterns

- See `laravel:performance-eager-loading` for N+1 detection and measurement
- Use `whereHas()` / `has()` to filter by related existence
- Prefer `withCount`, `withSum`, `withMax` for simple aggregates
- Apply global / local scopes for recurring constraints
- Keep relationship names consistent and pluralized where appropriate

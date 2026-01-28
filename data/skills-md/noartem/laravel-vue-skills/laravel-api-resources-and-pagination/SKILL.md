---
name: laravel-api-resources-and-pagination
description: Use API Resources with pagination and conditional fields; keep response shapes stable and cache-friendly
---

# API Resources and Pagination

Represent models via Resources; keep transport concerns out of Eloquent.

## Commands

```
# Resource
php artisan make:resource PostResource    # or: php artisan make:resource PostResource

# Controller usage
return PostResource::collection(
    Post::with('author')->latest()->paginate(20)
);

# Resource class
public function toArray($request)
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        'author' => new UserResource($this->whenLoaded('author')),
        'published_at' => optional($this->published_at)->toAtomString(),
    ];
}
```

## Patterns

- Prefer `Resource::collection($query->paginate())` over manual arrays
- Use `when()` / `mergeWhen()` for conditional fields
- Keep pagination cursors/links intact for clients
- Version resources when contracts change; avoid breaking fields silently

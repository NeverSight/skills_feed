---
name: eloquent-best-practices
description: Best practices for Laravel Eloquent ORM including query optimization, relationship management, and avoiding common pitfalls like N+1 queries.
---

# Eloquent Best Practices

## Query Optimization

### Always Eager Load Relationships

```php
// ❌ N+1 Query Problem
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name; // N additional queries
}

// ✅ Eager Loading
$posts = Post::with('user')->get();
foreach ($posts as $post) {
    echo $post->user->name; // No additional queries
}
```

### Select Only Needed Columns

```php
// ❌ Fetches all columns
$users = User::all();

// ✅ Only needed columns
$users = User::select(['id', 'name', 'email'])->get();

// ✅ With relationships
$posts = Post::with(['user:id,name'])->select(['id', 'title', 'user_id'])->get();
```

### Use Query Scopes

```php
// ✅ Define reusable query logic
class Post extends Model
{
    public function scopePublished($query)
    {
        return $query->where('status', 'published')
                    ->whereNotNull('published_at');
    }
    
    public function scopePopular($query, $threshold = 100)
    {
        return $query->where('views', '>', $threshold);
    }
}

// Usage
$posts = Post::published()->popular()->get();
```

## Relationship Best Practices

### Define Return Types

```php
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
    
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

### Use withCount for Counts

```php
// ❌ Triggers additional queries
foreach ($posts as $post) {
    echo $post->comments()->count();
}

// ✅ Load counts efficiently
$posts = Post::withCount('comments')->get();
foreach ($posts as $post) {
    echo $post->comments_count;
}
```

## Mass Assignment Protection

```php
class Post extends Model
{
    // ✅ Whitelist fillable attributes
    protected $fillable = ['title', 'content', 'status'];
    
    // Or blacklist guarded attributes
    protected $guarded = ['id', 'user_id'];
    
    // ❌ Never do this
    // protected $guarded = [];
}
```

## Use Casts for Type Safety

```php
class Post extends Model
{
    protected $casts = [
        'published_at' => 'datetime',
        'metadata' => 'array',
        'is_featured' => 'boolean',
        'views' => 'integer',
    ];
}
```

## Chunking for Large Datasets

```php
// ✅ Process in chunks to save memory
Post::chunk(200, function ($posts) {
    foreach ($posts as $post) {
        // Process each post
    }
});

// ✅ Or use lazy collections
Post::lazy()->each(function ($post) {
    // Process one at a time
});
```

## Database-Level Operations

```php
// ❌ Slow - loads into memory first
$posts = Post::where('status', 'draft')->get();
foreach ($posts as $post) {
    $post->update(['status' => 'archived']);
}

// ✅ Fast - single query
Post::where('status', 'draft')->update(['status' => 'archived']);

// ✅ Increment/decrement
Post::where('id', $id)->increment('views');
```

## Use Model Events Wisely

```php
class Post extends Model
{
    protected static function booted()
    {
        static::creating(function ($post) {
            $post->slug = Str::slug($post->title);
        });
        
        static::deleting(function ($post) {
            $post->comments()->delete();
        });
    }
}
```

## Common Pitfalls to Avoid

### Don't Query in Loops

```php
// ❌ Bad
foreach ($userIds as $id) {
    $user = User::find($id);
}

// ✅ Good
$users = User::whereIn('id', $userIds)->get();
```

### Don't Forget Indexes

```php
// Migration
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->index();
    $table->string('slug')->unique();
    $table->string('status')->index();
    $table->timestamp('published_at')->nullable()->index();
    
    // Composite index for common queries
    $table->index(['status', 'published_at']);
});
```

### Prevent Lazy Loading in Development

```php
// In AppServiceProvider boot method
Model::preventLazyLoading(!app()->isProduction());
```

## Checklist

- [ ] Relationships eagerly loaded where needed
- [ ] Only selecting required columns
- [ ] Using query scopes for reusability
- [ ] Mass assignment protection configured
- [ ] Appropriate casts defined
- [ ] Indexes on foreign keys and query columns
- [ ] Using database-level operations when possible
- [ ] Chunking for large datasets
- [ ] Model events used appropriately
- [ ] Lazy loading prevented in development

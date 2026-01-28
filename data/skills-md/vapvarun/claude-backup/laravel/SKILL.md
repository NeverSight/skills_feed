---
name: laravel
description: Complete Laravel development guide covering Eloquent, Blade, testing with Pest/PHPUnit, queues, caching, API resources, migrations, and Laravel best practices. Use when building Laravel applications, writing Laravel code, implementing features in Laravel, debugging Laravel issues, or when user mentions Laravel, Eloquent, Blade, Artisan, or PHP frameworks.
---

# Laravel Development

Modern Laravel development patterns, best practices, and workflows.

## Runner Selection

```bash
# With Laravel Sail (Docker)
sail artisan <command>
sail composer <command>
sail npm <command>

# Without Sail (local PHP)
php artisan <command>
composer <command>
npm <command>
```

## Eloquent Relationships & Loading

### Eager Loading (Prevent N+1)

```php
// BAD: N+1 queries
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->author->name; // Query per post
}

// GOOD: Eager loading
$posts = Post::with(['author', 'tags'])->get();

// Constrained eager loading
User::with(['posts' => fn($q) => $q->latest()->where('published', true)])->find($id);

// With counts and aggregates
Post::withCount('comments')->withSum('orders', 'total')->get();
```

### Relationships

```php
// Define clear relationships
class Post extends Model
{
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class);
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}

// Pivot operations
$post->tags()->sync([1, 2, 3]);           // Replace all
$post->tags()->syncWithoutDetaching([4]); // Add without removing
$post->tags()->attach($tagId);            // Add one
$post->tags()->detach($tagId);            // Remove one
```

## Migrations & Factories

### Migrations

```php
// Create migration
// sail artisan make:migration create_posts_table

Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->cascadeOnDelete();
    $table->string('title');
    $table->string('slug')->unique();
    $table->text('content');
    $table->enum('status', ['draft', 'published', 'archived'])->default('draft');
    $table->timestamp('published_at')->nullable();
    $table->timestamps();
    $table->softDeletes();

    $table->index(['status', 'published_at']);
});
```

### Factories

```php
class PostFactory extends Factory
{
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'title' => fake()->sentence(),
            'slug' => fake()->unique()->slug(),
            'content' => fake()->paragraphs(3, true),
            'status' => 'draft',
        ];
    }

    public function published(): static
    {
        return $this->state(fn() => [
            'status' => 'published',
            'published_at' => now(),
        ]);
    }
}

// Usage
Post::factory()->count(10)->published()->create();
Post::factory()->for(User::factory()->admin())->create();
```

## Form Requests & Validation

```php
class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Post::class);
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'slug' => ['required', 'string', 'max:255', 'unique:posts'],
            'content' => ['required', 'string'],
            'status' => ['required', Rule::in(['draft', 'published'])],
            'tags' => ['array'],
            'tags.*' => ['exists:tags,id'],
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'Post title is required.',
            'slug.unique' => 'This slug is already taken.',
        ];
    }
}

// Controller usage
public function store(StorePostRequest $request): JsonResponse
{
    $post = Post::create($request->validated());
    return response()->json($post, 201);
}
```

## API Resources

```php
class PostResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'slug' => $this->slug,
            'excerpt' => Str::limit($this->content, 150),
            'author' => new UserResource($this->whenLoaded('author')),
            'tags' => TagResource::collection($this->whenLoaded('tags')),
            'comments_count' => $this->whenCounted('comments'),
            'created_at' => $this->created_at->toISOString(),
            'updated_at' => $this->updated_at->toISOString(),
        ];
    }
}

// Paginated response
return PostResource::collection(
    Post::with(['author', 'tags'])
        ->withCount('comments')
        ->latest()
        ->paginate(20)
);
```

## TDD with Pest

### RED-GREEN-REFACTOR Cycle

```php
// 1. RED: Write failing test first
it('creates a post with valid data', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->postJson('/api/posts', [
            'title' => 'My Post',
            'slug' => 'my-post',
            'content' => 'Post content here',
            'status' => 'draft',
        ]);

    $response->assertCreated()
        ->assertJsonPath('data.title', 'My Post');

    $this->assertDatabaseHas('posts', [
        'title' => 'My Post',
        'user_id' => $user->id,
    ]);
});

it('rejects empty title', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->postJson('/api/posts', [
            'title' => '',
            'slug' => 'test',
            'content' => 'Content',
        ]);

    $response->assertUnprocessable()
        ->assertJsonValidationErrors('title');
});

// 2. GREEN: Write minimal code to pass
// 3. REFACTOR: Clean up while keeping tests green
```

### Run Tests

```bash
# All tests (parallel)
sail artisan test --parallel

# Specific test file
sail artisan test tests/Feature/PostTest.php

# With coverage
sail artisan test --coverage --min=80
```

## Queues & Horizon

### Job Definition

```php
class ProcessUpload implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;
    public int $timeout = 300;

    public function __construct(
        public Upload $upload
    ) {}

    public function handle(): void
    {
        // Process the upload
        $this->upload->process();
    }

    public function failed(Throwable $exception): void
    {
        Log::error('Upload processing failed', [
            'upload_id' => $this->upload->id,
            'error' => $exception->getMessage(),
        ]);
    }
}

// Dispatch
ProcessUpload::dispatch($upload);
ProcessUpload::dispatch($upload)->onQueue('uploads');
ProcessUpload::dispatch($upload)->delay(now()->addMinutes(5));
```

### Horizon Configuration

```php
// config/horizon.php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],
],
```

## Caching

```php
// Simple caching
$posts = Cache::remember('posts.featured', 3600, function () {
    return Post::featured()->with('author')->get();
});

// Cache tags (Redis required)
Cache::tags(['posts', 'users'])->put('user.1.posts', $posts, 3600);
Cache::tags('posts')->flush();

// Model caching pattern
class Post extends Model
{
    protected static function booted(): void
    {
        static::saved(fn() => Cache::tags('posts')->flush());
        static::deleted(fn() => Cache::tags('posts')->flush());
    }
}
```

## Routes Best Practices

```php
// api.php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('posts', PostController::class);
    Route::post('posts/{post}/publish', [PostController::class, 'publish']);

    Route::prefix('admin')->middleware('can:admin')->group(function () {
        Route::apiResource('users', Admin\UserController::class);
    });
});

// Rate limiting
Route::middleware(['throttle:api'])->group(function () {
    Route::get('/search', SearchController::class);
});
```

## Policies & Authorization

```php
class PostPolicy
{
    public function view(?User $user, Post $post): bool
    {
        return $post->status === 'published' || $user?->id === $post->user_id;
    }

    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id || $user->isAdmin();
    }

    public function delete(User $user, Post $post): bool
    {
        return $user->id === $post->user_id || $user->isAdmin();
    }
}

// Controller usage
public function update(UpdatePostRequest $request, Post $post)
{
    $this->authorize('update', $post);
    // ...
}
```

## Exception Handling

```php
// app/Exceptions/Handler.php
public function register(): void
{
    $this->renderable(function (ModelNotFoundException $e, Request $request) {
        if ($request->wantsJson()) {
            return response()->json(['message' => 'Resource not found'], 404);
        }
    });

    $this->renderable(function (AuthorizationException $e, Request $request) {
        if ($request->wantsJson()) {
            return response()->json(['message' => 'Forbidden'], 403);
        }
    });
}
```

## Quality Checks

```bash
# Laravel Pint (code style)
./vendor/bin/pint

# PHPStan (static analysis)
./vendor/bin/phpstan analyse

# PHP Insights (code quality)
./vendor/bin/phpinsights

# All checks
./vendor/bin/pint && ./vendor/bin/phpstan analyse && sail artisan test
```

## Blade Components

```php
// Component class
class Alert extends Component
{
    public function __construct(
        public string $type = 'info',
        public ?string $message = null
    ) {}

    public function render(): View
    {
        return view('components.alert');
    }
}

// Blade template
<x-alert type="success" :message="$message" />

// Anonymous component (resources/views/components/button.blade.php)
@props(['type' => 'button', 'variant' => 'primary'])

<button type="{{ $type }}" {{ $attributes->merge(['class' => "btn btn-{$variant}"]) }}>
    {{ $slot }}
</button>
```

## Performance Tips

1. **Use eager loading** - Always `with()` relationships you'll access
2. **Select specific columns** - `->select(['id', 'name'])` when possible
3. **Use chunking for large datasets** - `->chunk(1000, fn($batch) => ...)`
4. **Cache expensive queries** - Use `Cache::remember()`
5. **Index database columns** - Add indexes for frequently queried columns
6. **Use queues** - Offload heavy processing to background jobs
7. **Enable OPcache** - In production for PHP performance

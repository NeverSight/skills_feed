---
name: laravel
description: Laravel v12 - The PHP Framework For Web Artisans
---

# Laravel Skill

Comprehensive assistance with Laravel 12.x development, including routing, Eloquent ORM, migrations, authentication, API development, and modern PHP patterns.

## When to Use This Skill

This skill should be triggered when:
- Building Laravel applications or APIs
- Working with Eloquent models, relationships, and queries
- Setting up authentication, authorization, or API tokens
- Creating database migrations, seeders, or factories
- Implementing middleware, service providers, or events
- Using Laravel's built-in features (queues, cache, validation, etc.)
- Troubleshooting Laravel errors or performance issues
- Following Laravel best practices and conventions
- Implementing RESTful APIs with Laravel Sanctum or Passport
- Working with Laravel Mix, Vite, or frontend assets

## Quick Reference

### Basic Routing

```php
// Basic routes
Route::get('/users', [UserController::class, 'index']);
Route::post('/users', [UserController::class, 'store']);

// Route parameters
Route::get('/users/{id}', function ($id) {
    return User::find($id);
});

// Named routes
Route::get('/profile', ProfileController::class)->name('profile');

// Route groups with middleware
Route::middleware(['auth'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
    Route::resource('posts', PostController::class);
});
```

### Eloquent Model Basics

```php
// Define a model with relationships
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Post extends Model
{
    protected $fillable = ['title', 'content', 'user_id'];

    protected $casts = [
        'published_at' => 'datetime',
    ];

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

### Database Migrations

```php
// Create a migration
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('title');
            $table->text('content');
            $table->timestamp('published_at')->nullable();
            $table->timestamps();

            $table->index(['user_id', 'published_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

### Form Validation

```php
// Controller validation
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'content' => 'required',
        'email' => 'required|email|unique:users',
        'tags' => 'array|min:1',
        'tags.*' => 'string|max:50',
    ]);

    return Post::create($validated);
}

// Form Request validation
namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StorePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => 'required|max:255',
            'content' => 'required|min:100',
        ];
    }
}
```

### Eloquent Query Builder

```php
// Common query patterns
// Eager loading to avoid N+1 queries
$posts = Post::with(['user', 'comments'])
    ->where('published_at', '<=', now())
    ->orderBy('published_at', 'desc')
    ->paginate(15);

// Conditional queries
$query = Post::query();

if ($request->has('search')) {
    $query->where('title', 'like', "%{$request->search}%");
}

if ($request->has('author')) {
    $query->whereHas('user', function ($q) use ($request) {
        $q->where('name', $request->author);
    });
}

$posts = $query->get();
```

### API Resource Controllers

```php
namespace App\Http\Controllers\Api;

use App\Models\Post;
use App\Http\Resources\PostResource;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index()
    {
        return PostResource::collection(
            Post::with('user')->latest()->paginate()
        );
    }

    public function store(Request $request)
    {
        $post = Post::create($request->validated());

        return new PostResource($post);
    }

    public function show(Post $post)
    {
        return new PostResource($post->load('user', 'comments'));
    }

    public function update(Request $request, Post $post)
    {
        $post->update($request->validated());

        return new PostResource($post);
    }
}
```

### API Resources (Transformers)

```php
namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class PostResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'slug' => $this->slug,
            'excerpt' => $this->excerpt,
            'content' => $this->when($request->routeIs('posts.show'), $this->content),
            'author' => new UserResource($this->whenLoaded('user')),
            'comments_count' => $this->when($this->comments_count, $this->comments_count),
            'published_at' => $this->published_at?->toISOString(),
            'created_at' => $this->created_at->toISOString(),
        ];
    }
}
```

### Authentication with Sanctum

```php
// API token authentication setup
// In config/sanctum.php - configure stateful domains

// Issue tokens
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens;
}

// Login endpoint
public function login(Request $request)
{
    $credentials = $request->validate([
        'email' => 'required|email',
        'password' => 'required',
    ]);

    if (!Auth::attempt($credentials)) {
        return response()->json(['message' => 'Invalid credentials'], 401);
    }

    $token = $request->user()->createToken('api-token')->plainTextToken;

    return response()->json(['token' => $token]);
}

// Protect routes
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', fn(Request $r) => $r->user());
});
```

### Jobs and Queues

```php
// Create a job
namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class ProcessVideo implements ShouldQueue
{
    use InteractsWithQueue, Queueable;

    public function __construct(
        public Video $video
    ) {}

    public function handle(): void
    {
        // Process the video
        $this->video->process();
    }
}

// Dispatch jobs
ProcessVideo::dispatch($video);
ProcessVideo::dispatch($video)->onQueue('videos')->delay(now()->addMinutes(5));
```

### Service Container and Dependency Injection

```php
// Bind services in AppServiceProvider
use App\Services\PaymentService;

public function register(): void
{
    $this->app->singleton(PaymentService::class, function ($app) {
        return new PaymentService(
            config('services.stripe.secret')
        );
    });
}

// Use dependency injection in controllers
public function __construct(
    protected PaymentService $payment
) {}

public function charge(Request $request)
{
    return $this->payment->charge(
        $request->user(),
        $request->amount
    );
}
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Laravel 12.x installation guide and core documentation

Use the reference files for detailed information about:
- Installation and configuration
- Framework architecture and concepts
- Advanced features and packages
- Deployment and optimization

## Key Concepts

### MVC Architecture
Laravel follows the Model-View-Controller pattern:
- **Models**: Eloquent ORM classes representing database tables
- **Views**: Blade templates for rendering HTML
- **Controllers**: Handle HTTP requests and return responses

### Eloquent ORM
Laravel's powerful database abstraction layer:
- **Active Record pattern**: Each model instance represents a database row
- **Relationships**: belongsTo, hasMany, belongsToMany, morphMany, etc.
- **Query Builder**: Fluent interface for building SQL queries
- **Eager Loading**: Prevent N+1 query problems with `with()`

### Routing
Define application endpoints:
- **Route methods**: get, post, put, patch, delete
- **Route parameters**: Required `{id}` and optional `{id?}`
- **Route groups**: Share middleware, prefixes, namespaces
- **Resource routes**: Auto-generate RESTful routes

### Middleware
Filter HTTP requests:
- **Built-in**: auth, throttle, verified, signed
- **Custom**: Create your own request/response filters
- **Global**: Apply to all routes
- **Route-specific**: Apply to specific routes or groups

### Service Container
Laravel's dependency injection container:
- **Automatic resolution**: Type-hint dependencies in constructors
- **Binding**: Register class implementations
- **Singletons**: Share single instance across requests

### Artisan Commands
Laravel's CLI tool:
```bash
php artisan make:model Post -mcr  # Create model, migration, controller, resource
php artisan migrate               # Run migrations
php artisan db:seed              # Seed database
php artisan queue:work           # Process queue jobs
php artisan optimize:clear       # Clear all caches
```

## Working with This Skill

### For Beginners
Start with:
1. **Installation**: Set up Laravel using Composer
2. **Routing**: Learn basic route definitions in `routes/web.php`
3. **Controllers**: Create controllers with `php artisan make:controller`
4. **Models**: Understand Eloquent basics and relationships
5. **Migrations**: Define database schema with migrations
6. **Blade Templates**: Create views with Laravel's templating engine

### For Intermediate Users
Focus on:
- **Form Requests**: Validation and authorization in dedicated classes
- **API Resources**: Transform models for JSON responses
- **Authentication**: Implement with Laravel Breeze or Sanctum
- **Relationships**: Master eager loading and complex relationships
- **Queues**: Offload time-consuming tasks to background jobs
- **Events & Listeners**: Decouple application logic

### For Advanced Users
Explore:
- **Service Providers**: Register application services
- **Custom Middleware**: Create reusable request filters
- **Package Development**: Build reusable Laravel packages
- **Testing**: Write feature and unit tests with PHPUnit
- **Performance**: Optimize queries, caching, and response times
- **Deployment**: CI/CD pipelines and production optimization

### Navigation Tips
- Check **Quick Reference** for common code patterns
- Reference the official docs at https://laravel.com/docs/12.x
- Use `php artisan route:list` to view all registered routes
- Use `php artisan tinker` for interactive debugging
- Enable query logging to debug database performance

## Common Patterns

### Repository Pattern
```php
interface PostRepositoryInterface
{
    public function all();
    public function find(int $id);
    public function create(array $data);
}

class PostRepository implements PostRepositoryInterface
{
    public function all()
    {
        return Post::with('user')->latest()->get();
    }

    public function find(int $id)
    {
        return Post::with('user', 'comments')->findOrFail($id);
    }
}
```

### Action Classes (Single Responsibility)
```php
class CreatePost
{
    public function execute(array $data): Post
    {
        return DB::transaction(function () use ($data) {
            $post = Post::create($data);
            $post->tags()->attach($data['tag_ids']);
            event(new PostCreated($post));
            return $post;
        });
    }
}
```

### Query Scopes
```php
class Post extends Model
{
    public function scopePublished($query)
    {
        return $query->where('published_at', '<=', now());
    }

    public function scopeByAuthor($query, User $user)
    {
        return $query->where('user_id', $user->id);
    }
}

// Usage
Post::published()->byAuthor($user)->get();
```

## Resources

### Official Documentation
- Laravel Docs: https://laravel.com/docs/12.x
- API Reference: https://laravel.com/api/12.x
- Laracasts: https://laracasts.com (video tutorials)

### Community
- Laravel News: https://laravel-news.com
- Laravel Forums: https://laracasts.com/discuss
- GitHub: https://github.com/laravel/laravel

### Tools
- Laravel Telescope: Debugging and monitoring
- Laravel Horizon: Queue monitoring
- Laravel Debugbar: Development debugging
- Laravel IDE Helper: IDE autocompletion

## Best Practices

1. **Use Form Requests**: Separate validation logic from controllers
2. **Eager Load Relationships**: Avoid N+1 query problems
3. **Use Resource Controllers**: Follow RESTful conventions
4. **Type Hints**: Leverage PHP type declarations for better IDE support
5. **Database Transactions**: Wrap related database operations
6. **Queue Jobs**: Offload slow operations to background workers
7. **Cache Queries**: Cache expensive database queries
8. **API Resources**: Transform data consistently for APIs
9. **Events**: Decouple application logic with events and listeners
10. **Tests**: Write tests for critical application logic

## Notes

- Laravel 12.x requires PHP 8.2 or higher
- Uses Composer for dependency management
- Includes Vite for asset compilation (replaces Laravel Mix)
- Supports multiple database systems (MySQL, PostgreSQL, SQLite, SQL Server)
- Built-in support for queues, cache, sessions, and file storage
- Excellent ecosystem with first-party packages (Sanctum, Horizon, Telescope, etc.)

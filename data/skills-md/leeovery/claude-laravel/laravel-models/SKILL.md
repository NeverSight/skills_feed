---
name: laravel-models
description: Eloquent model patterns and database layer. Use when working with models, database entities, Eloquent ORM, or when user mentions models, eloquent, relationships, casts, observers, database entities.
---

# Laravel Models

Models represent database tables and domain entities.

**Related guides:**
- [Query Builders](../laravel-query-builders/SKILL.md) - Custom query builders (not scopes)
- [Actions](../laravel-actions/SKILL.md) - Actions contain business logic
- [DTOs](../laravel-dtos/SKILL.md) - Casting model JSON columns to DTOs

## Philosophy

Models should:
- Use **custom query builders** (not local scopes) - see [Query Builders](../laravel-query-builders/SKILL.md)
- Define relationships
- Define casts
- Contain simple accessors/mutators
- **NOT contain business logic** (that belongs in Actions)

## Basic Model Structure

```php
<?php

declare(strict_types=1);

namespace App\Models;

use App\Builders\OrderBuilder;
use App\Enums\OrderStatus;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Order extends Model
{
    use HasFactory;

    protected function casts(): array
    {
        return [
            'status' => OrderStatus::class,
            'total' => 'integer',
        ];
    }

    // Custom Query Builder
    public function newEloquentBuilder($query): OrderBuilder
    {
        return new OrderBuilder($query);
    }

    // Relationships
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function items(): HasMany
    {
        return $this->hasMany(OrderItem::class);
    }
}
```

## Casts

**Define casts for type safety:**

```php
protected function casts(): array
{
    return [
        'status' => OrderStatus::class,         // Enum
        'total' => 'integer',                   // Integer
        'is_paid' => 'boolean',                 // Boolean
        'metadata' => OrderMetadataData::class, // DTO
        'completed_at' => 'datetime',           // Carbon
        'tags' => 'array',                      // JSON array
    ];
}
```

**Available casts:**
- `'integer'`, `'real'`, `'float'`, `'double'`
- `'string'`, `'boolean'`
- `'array'`, `'json'`, `'object'`, `'collection'`
- `'date'`, `'datetime'`, `'immutable_date'`, `'immutable_datetime'`
- `'timestamp'`
- `'encrypted'`, `'encrypted:array'`, `'encrypted:collection'`, `'encrypted:json'`, `'encrypted:object'`
- Custom cast classes
- Enum classes
- DTO classes

## Relationships

### BelongsTo

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class);
}

public function customer(): BelongsTo
{
    return $this->belongsTo(Customer::class, 'customer_id', 'id');
}
```

### HasMany

```php
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

public function items(): HasMany
{
    return $this->hasMany(OrderItem::class);
}
```

### HasOne

```php
public function profile(): HasOne
{
    return $this->hasOne(UserProfile::class);
}
```

### BelongsToMany

```php
public function roles(): BelongsToMany
{
    return $this->belongsToMany(Role::class)
        ->withTimestamps()
        ->withPivot('assigned_at');
}
```

### HasManyThrough

```php
public function deployments(): HasManyThrough
{
    return $this->hasManyThrough(Deployment::class, Environment::class);
}
```

### MorphTo / MorphMany

```php
// MorphTo
public function commentable(): MorphTo
{
    return $this->morphTo();
}

// MorphMany
public function comments(): MorphMany
{
    return $this->morphMany(Comment::class, 'commentable');
}
```

## Accessors & Mutators

### Accessors (Get)

```php
use Illuminate\Database\Eloquent\Casts\Attribute;

protected function fullName(): Attribute
{
    return Attribute::make(
        get: fn () => "{$this->first_name} {$this->last_name}",
    );
}

// Usage
$user->full_name; // "John Doe"
```

### Mutators (Set)

```php
protected function password(): Attribute
{
    return Attribute::make(
        set: fn (string $value) => bcrypt($value),
    );
}

// Usage
$user->password = 'secret'; // Automatically hashed
```

### Both Get and Set

```php
protected function email(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => strtolower($value),
        set: fn (string $value) => strtolower(trim($value)),
    );
}
```

## Model Methods

**Simple helper methods** are acceptable:

```php
class Order extends Model
{
    public function isPending(): bool
    {
        return $this->status === OrderStatus::Pending;
    }

    public function isCompleted(): bool
    {
        return $this->status === OrderStatus::Completed;
    }

    public function canBeCancelled(): bool
    {
        return $this->isPending() || $this->status === OrderStatus::Processing;
    }
}
```

**But NOT business logic:**

```php
// ❌ Bad - business logic in model
class Order extends Model
{
    public function cancel(): void
    {
        DB::transaction(function () {
            $this->update(['status' => OrderStatus::Cancelled]);
            $this->refundPayment();
            $this->notifyCustomer();
        });
    }
}

// ✅ Good - business logic in action
class CancelOrderAction
{
    public function __invoke(Order $order): Order
    {
        return DB::transaction(function () use ($order) {
            $order->update(['status' => OrderStatus::Cancelled]);
            resolve(RefundPaymentAction::class)($order);
            resolve(NotifyCustomerAction::class)($order);
            return $order;
        });
    }
}
```

## Model Observers

**For model lifecycle hooks:**

```php
<?php

declare(strict_types=1);

namespace App\Observers;

use App\Models\Order;
use Illuminate\Support\Str;

class OrderObserver
{
    public function creating(Order $order): void
    {
        if (! $order->uuid) {
            $order->uuid = Str::uuid();
        }
    }

    public function created(Order $order): void
    {
        // Dispatch event, queue job, etc.
    }

    public function updating(Order $order): void
    {
        // Before update
    }

    public function updated(Order $order): void
    {
        // After update
    }

    public function deleted(Order $order): void
    {
        // After delete
    }
}
```

**Register in AppServiceProvider:**

```php
use App\Models\Order;
use App\Observers\OrderObserver;

public function boot(): void
{
    Order::observe(OrderObserver::class);
}
```

## Model Concerns (Traits)

**Extract reusable behavior:**

**[View full implementation →](references/HasUuid.php)**

**Use in models:**

```php
class Order extends Model
{
    use HasUuid;
}
```

## Route Model Binding

### Implicit Binding

```php
// Route
Route::get('/orders/{order}', [OrderController::class, 'show']);

// Controller - automatically receives Order model
public function show(Order $order) { }
```

### Custom Key

```php
Route::get('/orders/{order:uuid}', [OrderController::class, 'show']);
```

### Custom Resolution

```php
public function resolveRouteBinding($value, $field = null)
{
    return $this->where($field ?? 'id', $value)
        ->where('is_active', true)
        ->firstOrFail();
}
```

## Mass Assignment Protection

**All models should be unguarded by default.**

### AppServiceProvider Setup

In your `AppServiceProvider::boot()` method, call `Model::unguard()`:

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        Model::unguard();
    }
}
```

### Model Configuration

**Do NOT use `$fillable` or `$guarded` properties** on your models:

```php
// ✅ Good - no fillable/guarded
class Order extends Model
{
    protected function casts(): array
    {
        return [
            'status' => OrderStatus::class,
        ];
    }
}

// ❌ Bad - don't use fillable
class Order extends Model
{
    protected $fillable = ['name', 'email'];
}

// ❌ Bad - don't use guarded
class Order extends Model
{
    protected $guarded = [];
}
```

### Why Unguard?

- **Simplicity**: No need to maintain fillable/guarded arrays
- **Flexibility**: All attributes can be mass-assigned
- **Trust**: With proper validation in Form Requests and Actions, mass assignment protection is redundant
- **Cleaner Models**: Less boilerplate code

**Important:** Always validate input in Form Requests before passing to Actions/Models.

## Timestamps

```php
// Disable timestamps
public $timestamps = false;

// Custom timestamp columns
const CREATED_AT = 'creation_date';
const UPDATED_AT = 'updated_date';
```

## Soft Deletes

```php
use Illuminate\Database\Eloquent\SoftDeletes;

class Order extends Model
{
    use SoftDeletes;
}
```

**Usage:**

```php
$order->delete();      // Soft delete
$order->forceDelete(); // Permanent delete
$order->restore();     // Restore

Order::withTrashed()->find($id);
Order::onlyTrashed()->get();
```

## Collections

**Query results return Collections:**

```php
$orders = Order::all(); // Illuminate\Database\Eloquent\Collection

$orders->filter(fn($order) => $order->isPending());
$orders->map(fn($order) => $order->total);
$orders->sum('total');
```

## Model Organization

```
app/Models/
├── Order.php
├── User.php
├── Concerns/
│   ├── HasUuid.php
│   ├── BelongsToTenant.php
│   └── Searchable.php
└── Contracts/
    └── Searchable.php
```

## Testing Models

```php
it('can mass assign attributes', function () {
    $order = Order::create([
        'user_id' => 1,
        'status' => 'pending',
        'total' => 1000,
        'notes' => 'Test order',
    ]);

    expect($order->user_id)->toBe(1)
        ->and($order->total)->toBe(1000);
});

it('casts status to enum', function () {
    $order = Order::factory()->create(['status' => 'pending']);

    expect($order->status)->toBeInstanceOf(OrderStatus::class);
});

it('has user relationship', function () {
    $order = Order::factory()->create();

    expect($order->user)->toBeInstanceOf(User::class);
});
```

## Summary

**Models should:**
- Be unguarded globally via `Model::unguard()` in AppServiceProvider
- Define structure (casts, relationships)
- Use custom query builders (not scopes)
- Have simple helper methods
- Use observers for lifecycle hooks

**Models should NOT:**
- Use `$fillable` or `$guarded` properties
- Contain business logic (use Actions)
- Have complex methods (use Actions)
- Use local scopes (use custom builders)

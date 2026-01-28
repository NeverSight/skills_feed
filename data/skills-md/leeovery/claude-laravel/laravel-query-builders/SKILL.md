---
name: laravel-query-builders
description: Custom query builders for type-safe, composable database queries. Use when working with database queries, query scoping, or when user mentions query builders, custom query builder, query objects, query scopes, database queries.
---

# Laravel Query Builders

**Always use custom query builders** instead of local scopes.

**Related guides:**
- [Models](../laravel-models/SKILL.md) - Model integration with custom builders
- [Controllers](../laravel-controllers/SKILL.md) - Using query objects in controllers

## Why Custom Builders Over Scopes

**❌ Do NOT use local scopes.**

**✅ Use custom query builders because they provide:**
1. **Better type hinting** - Full IDE autocomplete
2. **Type-safe nested queries** - Type-hint closures in `whereHas()`, `orWhereHas()`, etc.
3. **Better organization** - All query logic in one class
4. **More composable** - Easier to chain and compose
5. **Easier testing** - Test query logic in isolation

## Basic Builder Structure

```php
<?php

declare(strict_types=1);

namespace App\Builders;

use App\Enums\OrderStatus;
use App\Models\User;
use Carbon\Carbon;
use Illuminate\Database\Eloquent\Builder;

class OrderBuilder extends Builder
{
    public function wherePending(): self
    {
        return $this->where('status', OrderStatus::Pending);
    }

    public function whereCompleted(): self
    {
        return $this->where('status', OrderStatus::Completed);
    }

    public function whereCustomer(User|int $customer): self
    {
        $customerId = $customer instanceof User ? $customer->id : $customer;
        return $this->where('customer_id', $customerId);
    }

    public function whereTotalGreaterThan(int $amount): self
    {
        return $this->where('total', '>', $amount);
    }

    public function wherePlacedBetween(Carbon $start, Carbon $end): self
    {
        return $this->whereBetween('placed_at', [$start, $end]);
    }

    public function withRelated(): self
    {
        return $this->with(['customer', 'items.product', 'shipments']);
    }

    public function recent(): self
    {
        return $this->latest('placed_at');
    }
}
```

## Type-Safe Nested Queries

**Type-hint closures** for full IDE support in relationship queries:

```php
public function whereHasItems(array|string $productIds): self
{
    return $this->whereHas('items', function (OrderItemBuilder $query) use ($productIds): void {
        $query->whereIn('product_id', (array) $productIds);
    });
}
```

**Usage:**

```php
Order::query()
    ->whereHas('items', function (OrderItemBuilder $query): void {
        $query->whereActive()        // Custom method - autocomplete works!
              ->whereProduct($id);   // Full type safety!
    })
    ->whereHas('customer', function (CustomerBuilder $query): void {
        $query->whereVerified()      // Custom method
              ->wherePremium();      // IDE knows all methods!
    })
    ->get();
```

## PHPDoc for External Methods

Document methods from Spatie packages or macros:

```php
/**
 * @method static OrderBuilder whereState(string $column, string|array $state)
 * @method static OrderBuilder whereNotState(string $column, string|array $state)
 */
class OrderBuilder extends Builder
{
    // ...
}
```

## Builder Traits

Extract reusable query logic:

```php
<?php

declare(strict_types=1);

namespace App\Builders\Concerns;

use Illuminate\Support\Arr;

trait HasProducts
{
    public function whereHasProducts(array|string $productIds): self
    {
        return $this->whereHas('products', function ($query) use ($productIds): void {
            $query->whereIn('id', Arr::wrap($productIds));
        });
    }

    public function whereHasActiveProducts(): self
    {
        return $this->whereHas('products', function ($query): void {
            $query->where('active', true);
        });
    }
}
```

**Usage in builder:**

```php
class OrderBuilder extends Builder
{
    use HasProducts;

    // ...
}
```

## Register Builder in Model

### Preferred: PHP Attribute (Laravel 11+)

```php
use Illuminate\Database\Eloquent\Attributes\UseEloquentBuilder;

#[UseEloquentBuilder(OrderBuilder::class)]
class Order extends Model
{
    // ...
}
```

### Alternative: Static Property

```php
class Order extends Model
{
    protected static string $eloquentBuilder = OrderBuilder::class;

    // ...
}
```

### Deprecated: Method Override

```php
// ❌ Don't use this approach anymore
public function newEloquentBuilder($query): OrderBuilder
{
    return new OrderBuilder($query);
}
```

## Usage Examples

### Basic Chaining

```php
Order::query()
    ->wherePending()
    ->whereTotalGreaterThan(10000)
    ->wherePlacedBetween(now()->subWeek(), now())
    ->withRelated()
    ->recent()
    ->paginate();
```

### Lazy Iteration

```php
Order::query()
    ->whereCompleted()
    ->lazyById()
    ->each(function (Order $order): void {
        // Process order
    });
```

### Complex Queries

```php
$orders = Order::query()
    ->wherePending()
    ->whereCustomer($user)
    ->whereHasItems([$productId1, $productId2])
    ->wherePlacedBetween($startDate, $endDate)
    ->withRelated()
    ->get();
```

## Empty Builders

**Always create builders** even if empty initially - for future extensibility:

```php
<?php

declare(strict_types=1);

namespace App\Builders;

use Illuminate\Database\Eloquent\Builder;

class CustomerBuilder extends Builder
{
    // Empty for now, but ready for future methods
}
```

## Common Builder Methods

### Status Filtering

```php
public function whereActive(): self
{
    return $this->where('status', 'active');
}

public function whereInactive(): self
{
    return $this->where('status', 'inactive');
}
```

### Date Ranges

```php
public function whereCreatedAfter(Carbon $date): self
{
    return $this->where('created_at', '>', $date);
}

public function whereCreatedToday(): self
{
    return $this->whereDate('created_at', today());
}
```

### User/Owner Filtering

```php
public function whereUser(User|int $user): self
{
    $userId = $user instanceof User ? $user->id : $user;
    return $this->where('user_id', $userId);
}
```

### Relationship Loading

```php
public function withFullRelations(): self
{
    return $this->with([
        'user',
        'items.product',
        'customer.address',
    ]);
}
```

## Builder Organization

```
app/Builders/
├── OrderBuilder.php
├── CustomerBuilder.php
├── ProductBuilder.php
└── Concerns/
    ├── HasProducts.php
    ├── HasDates.php
    └── HasStatus.php
```

## Summary

**Custom query builders:**
- Provide better IDE support than scopes
- Enable type-safe nested queries
- Keep query logic organized
- Are easier to test
- Support method chaining

**Never use local scopes** - always use custom builders.

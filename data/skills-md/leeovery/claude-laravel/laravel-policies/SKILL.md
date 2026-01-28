---
name: laravel-policies
description: Authorization policies for resource access control. Use when working with authorization, permissions, access control, or when user mentions policies, authorization, permissions, can, ability checks.
---

# Laravel Policies

Policies encapsulate authorization logic and delegate to permission systems.

**Related guides:**
- [routing-permissions.md](../laravel-routing/references/routing-permissions.md) - Route-level authorization
- [Enums](../laravel-enums/SKILL.md) - Permission enums

## Structure

```php
<?php

declare(strict_types=1);

namespace App\Policies;

use App\Enums\Permission;
use App\Models\Order;
use App\Models\User;

class OrderPolicy
{
    public function viewAny(User $user): bool
    {
        return $user->can(Permission::ListOrders);
    }

    public function view(User $user, Order $order): bool
    {
        return $user->can(Permission::ViewOrders)
            && $order->customer_id === $user->customer_id;
    }

    public function create(User $user): bool
    {
        return $user->can(Permission::CreateOrders);
    }

    public function update(User $user, Order $order): bool
    {
        return $user->can(Permission::UpdateOrders)
            && $order->canBeModified()
            && $order->customer_id === $user->customer_id;
    }

    public function delete(User $user, Order $order): bool
    {
        return $user->can(Permission::DeleteOrders)
            && $order->isPending();
    }

    public function cancel(User $user, Order $order): bool
    {
        return $this->update($user, $order)
            && $order->canBeCancelled();
    }
}
```

## Permission Enum

```php
<?php

declare(strict_types=1);

namespace App\Enums;

use Henzeb\Enumhancer\Concerns\Comparison;
use Henzeb\Enumhancer\Concerns\Dropdown;

enum Permission: string
{
    use Comparison, Dropdown;

    case ListOrders = 'list orders';
    case ViewOrders = 'view orders';
    case CreateOrders = 'create orders';
    case UpdateOrders = 'update orders';
    case DeleteOrders = 'delete orders';
    case CancelOrders = 'cancel orders';
}
```

## Standard Policy Methods

Laravel conventions for policy methods:

- `viewAny()` - List/index
- `view()` - Show single resource
- `create()` - Create new resource
- `update()` - Update resource
- `delete()` - Delete resource
- `restore()` - Restore soft-deleted
- `forceDelete()` - Permanently delete

**Custom methods** for non-standard actions:
- `cancel()`
- `approve()`
- `ship()`
- etc.

## Key Patterns

### 1. Delegate to Permission System

```php
return $user->can(Permission::CreateOrders);
```

### 2. Ownership Checks

```php
return $user->can(Permission::ViewOrders)
    && $order->customer_id === $user->customer_id;
```

### 3. State Checks

```php
return $user->can(Permission::DeleteOrders)
    && $order->isPending();
```

### 4. Combine Existing Methods

```php
public function cancel(User $user, Order $order): bool
{
    return $this->update($user, $order)
        && $order->canBeCancelled();
}
```

## Usage in Routes

```php
Route::get('/orders', [OrderController::class, 'index'])
    ->can('viewAny', Order::class);

Route::get('/orders/{order}', [OrderController::class, 'show'])
    ->can('view', 'order');

Route::post('/orders', [OrderController::class, 'store'])
    ->can('create', Order::class);
```

See [routing-permissions.md](../laravel-routing/references/routing-permissions.md) for route authorization.

## Summary

**Policies should:**
- Use permission enums (not strings)
- Check ownership when needed
- Check state when needed
- Delegate to permission system
- Follow Laravel naming conventions
- Stay simple and focused

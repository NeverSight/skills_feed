---
name: laravel-routing
description: Route configuration, route model binding, and authorization. Use when working with routes, route binding, URL patterns, or when user mentions routing, route model binding, conditional binding, route-level authorization.
---

# Laravel Routing

Route configuration with model binding and authorization patterns.

## Core Concepts

**[routing-permissions.md](references/routing-permissions.md)** - Route authorization:
- Route-level authorization with `->can()`
- Web vs API routing patterns
- Route naming conventions
- Model binding integration

**[route-binding.md](references/route-binding.md)** - Route model binding:
- Simple binding strategies
- Conditional route model binding
- ConditionalRouteBinder pattern for route-specific resolution
- Query objects for scoping
- Multi-tenant scoping

## Patterns

```php
// Route with authorization
Route::get('/orders/{order}', ShowOrderController::class)
    ->can('view', 'order')
    ->name('orders.show');

// Conditional binding
Route::bind('order', ConditionalRouteBinder::for(Order::class));
```

Use route-level authorization for permission checks before controller execution.

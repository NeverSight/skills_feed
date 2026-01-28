---
name: laravel-controllers
description: Thin HTTP layer controllers. Controllers contain zero domain logic, only HTTP concerns. Use when working with controllers, HTTP layer, web vs API patterns, or when user mentions controllers, routes, HTTP responses.
---

# Laravel Controllers

Controllers are **extremely thin**. They handle **HTTP concerns only** and contain **zero domain logic**.

**Related guides:**
- [query-objects.md](references/query-objects.md) - Query objects for API filtering/sorting
- [Actions](../laravel-actions/SKILL.md) - Actions contain the domain logic
- [form-requests.md](../laravel-validation/references/form-requests.md) - Validation layer
- [DTOs](../laravel-dtos/SKILL.md) - DTOs for data transfer
- [structure.md](../laravel-architecture/references/structure.md) - Web vs API organization

## Philosophy

**Controllers should ONLY:**
1. Type-hint dependencies
2. Validate (via Form Requests)
3. Call actions
4. Return responses (resources, redirects, views)

**Controllers should NEVER:**
- Contain domain logic
- Make database queries directly
- Perform calculations
- Handle complex business rules

## Controller Naming Conventions

**Controllers should be named using the PLURAL form of the main resource:**

### Standard Resource Controllers

```php
// ✅ CORRECT - Plural resource names
CalendarsController      // manages calendar resources
EventsController         // manages event resources
OrdersController         // manages order resources
UsersController          // manages user resources
```

```php
// ❌ INCORRECT - Singular form
CalendarController
EventController
```

### Nested Resource Controllers

**For nested resources, combine both resource names (parent + child):**

```php
// Route: /calendars/{calendar}/events
CalendarEventsController  // manages events within a calendar

// Route: /orders/{order}/items
OrderItemsController      // manages items within an order
```

**Pattern:** `{ParentSingular}{ChildPlural}Controller`

**Routes:**

```php
// Standard resource routes
Route::resource('calendars', CalendarsController::class);

// Nested resource routes
Route::resource('calendars.events', CalendarEventsController::class);
```

## RESTful Methods Only

Controllers **must only** use Laravel's standard RESTful method names.

### Standard RESTful Methods

**For web applications (with forms):**
- `index` - Display a listing of the resource
- `create` - Show the form for creating a new resource
- `store` - Store a newly created resource
- `show` - Display the specified resource
- `edit` - Show the form for editing the resource
- `update` - Update the specified resource
- `destroy` - Remove the specified resource

**For APIs (no form views):**
- `index`, `show`, `store`, `update`, `destroy`
- **APIs must NOT include `create` or `edit` methods** (those are for HTML forms)

### Forbidden Method Names

Never use custom method names in resource controllers:

```php
// ❌ INCORRECT
class OrdersController extends Controller
{
    public function all() { }      // Use index
    public function get() { }      // Use show
    public function add() { }      // Use store
    public function remove() { }   // Use destroy
    public function cancel() { }   // Extract to CancelOrderController
}
```

### Non-RESTful Actions: Extract to Invokable Controllers

If you need an endpoint that doesn't fit standard RESTful methods, **extract it to its own invokable controller**:

```php
// app/Http/Api/V1/Controllers/CancelOrderController.php
class CancelOrderController extends Controller
{
    public function __invoke(
        Order $order,
        CancelOrderAction $action
    ): OrderResource {
        $order = $action($order);
        return OrderResource::make($order);
    }
}
```

**Routes:**
```php
Route::apiResource('orders', OrdersController::class);
Route::post('/orders/{order:uuid}/cancel', CancelOrderController::class);
```

**Why invokable controllers for non-RESTful actions?**
- Single Responsibility Principle
- Clear intent from controller name
- Independently testable
- Prevents bloated resource controllers

## Web Layer vs Public API

### Web Layer Controllers

**Purpose:** Serve your application's web layer (API for separate frontend, Blade views, or Inertia)

**Location:** `app/Http/Web/Controllers/`

**Routes:** `routes/web.php`

**Characteristics:**
- Not versioned
- Can change freely
- Private (only your app consumes)

### Public API Controllers

**Purpose:** For external/third-party consumption

**Location:** `app/Http/Api/V1/Controllers/`

**Routes:** `routes/api/v1.php`

**Characteristics:**
- Versioned (`/api/v1`, `/api/v2`)
- Stable contract
- Breaking changes require new version

**Key difference:** Namespace (`Http\Web` vs `Http\Api\V1`). Controller structure is identical.

## Full Controller Example

```php
<?php

declare(strict_types=1);

namespace App\Http\Web\Controllers;

use App\Actions\Order\CreateOrderAction;
use App\Actions\Order\DeleteOrderAction;
use App\Actions\Order\UpdateOrderAction;
use App\Data\Transformers\Web\OrderDataTransformer;
use App\Http\Controllers\Controller;
use App\Http\Web\Queries\OrderIndexQuery;
use App\Http\Web\Requests\CreateOrderRequest;
use App\Http\Web\Requests\UpdateOrderRequest;
use App\Http\Web\Resources\OrderResource;
use App\Models\Order;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;
use Illuminate\Http\Response;

class OrdersController extends Controller
{
    public function index(OrderIndexQuery $query): AnonymousResourceCollection
    {
        return OrderResource::collection($query->jsonPaginate());
    }

    public function show(Order $order): OrderResource
    {
        return OrderResource::make($order->load('items', 'customer'));
    }

    public function store(
        CreateOrderRequest $request,
        CreateOrderAction $action
    ): OrderResource {
        $order = $action(
            user(),
            OrderDataTransformer::fromRequest($request)
        );

        return OrderResource::make($order);
    }

    public function update(
        UpdateOrderRequest $request,
        Order $order,
        UpdateOrderAction $action
    ): OrderResource {
        $order = $action(
            $order,
            OrderDataTransformer::fromRequest($request)
        );

        return OrderResource::make($order);
    }

    public function destroy(
        Order $order,
        DeleteOrderAction $action
    ): Response {
        $action($order);

        return response()->noContent();
    }
}
```

**For API controllers:** Same structure, different namespace (`App\Http\Api\V1\Controllers`).

## Query Objects

For API filtering, sorting, and includes, use **Query Objects** with Spatie Query Builder:

```php
public function index(OrderIndexQuery $query): AnonymousResourceCollection
{
    return OrderResource::collection($query->jsonPaginate());
}
```

**[→ Complete query objects guide: query-objects.md](references/query-objects.md)**

## Authorization

```php
public function store(
    CreateOrderRequest $request,
    CreateOrderAction $action
): OrderResource {
    $this->authorize('create', Order::class);

    $order = $action(user(), OrderDataTransformer::fromRequest($request));

    return OrderResource::make($order);
}
```

**Or use route middleware:**

```php
Route::post('/orders', [OrdersController::class, 'store'])
    ->can('create', Order::class);
```

## Response Types

### JSON Resource

```php
public function show(Order $order): OrderResource
{
    return OrderResource::make($order);
}
```

### Collection Resource

```php
public function index(OrderIndexQuery $query): AnonymousResourceCollection
{
    return OrderResource::collection($query->jsonPaginate());
}
```

### 201 Created

```php
return OrderResource::make($order)->response()->setStatusCode(201);
```

### 204 No Content

```php
return response()->noContent();
```

### Redirect

```php
return redirect()->route('orders.show', $order);
```

## Route Model Binding

**Use route model binding** for cleaner controllers:

```php
Route::get('/orders/{order}', [OrdersController::class, 'show']);
Route::get('/orders/{order:uuid}', [OrdersController::class, 'show']); // Custom key
```

**Controller automatically receives model:**

```php
public function show(Order $order): OrderResource
{
    return OrderResource::make($order->load('items', 'customer'));
}
```

## Controller Testing

**Feature tests for controllers:**

```php
use function Pest\Laravel\actingAs;
use function Pest\Laravel\postJson;

it('creates an order', function () {
    $user = User::factory()->create();
    $data = CreateOrderData::testFactory()->make();

    actingAs($user)
        ->postJson('/orders', $data->toArray())
        ->assertCreated()
        ->assertJsonStructure(['data' => ['id', 'status']]);
});

it('requires authentication', function () {
    postJson('/orders', [])->assertUnauthorized();
});

it('validates required fields', function () {
    actingAs(User::factory()->create())
        ->postJson('/orders', [])
        ->assertUnprocessable()
        ->assertJsonValidationErrors(['customer_email', 'items']);
});
```

## Common Mistakes

### ❌ Domain Logic in Controller

```php
// BAD
public function store(Request $request)
{
    $order = Order::create($request->validated());
    $order->items()->createMany($request->items);
    $total = $order->items->sum('total');
    $order->update(['total' => $total]);
}
```

### ✅ Delegate to Action

```php
// GOOD
public function store(
    CreateOrderRequest $request,
    CreateOrderAction $action
): OrderResource {
    $order = $action(
        user(),
        OrderDataTransformer::fromRequest($request)
    );

    return OrderResource::make($order);
}
```

### ❌ Database Queries in Controller

```php
// BAD
public function index()
{
    $orders = Order::with('items')
        ->where('status', 'pending')
        ->latest()
        ->paginate();
}
```

### ✅ Use Query Object

```php
// GOOD
public function index(OrderIndexQuery $query): AnonymousResourceCollection
{
    return OrderResource::collection($query->jsonPaginate());
}
```

## Summary

**Controllers are HTTP adapters:**
1. Receive HTTP request
2. Validate via Form Request
3. Call Action (with DTO if needed)
4. Return HTTP response via Resource

**Every line of domain logic belongs in an Action, not a Controller.**

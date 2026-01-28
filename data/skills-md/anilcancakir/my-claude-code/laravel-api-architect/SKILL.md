---
name: laravel-api-architect
description: "Laravel API development, REST endpoints, JSON responses, Sanctum/Passport authentication, Service-Repository pattern. ALWAYS activate when: working with routes/api.php, app/Http/Controllers/Api/, API endpoints, token authentication, mobile backend, API Resource, JsonResponse, FormRequest, Policy. Triggers on: endpoint çalışmıyor, API hatası, API error, 401 unauthorized, 403 forbidden, 422 validation, token expired, login endpoint, register API, CRUD operations, postman, fetch request, axios, mobile backend, webhook, OAuth, JWT, auth guard, rate limit, throttle, response format, pagination API."
---

# Laravel API Architect

Production-grade API development with Service-Repository pattern for PHP 8.4+ and Laravel 12+.

## Core Principles

1. **Thin Controllers** - HTTP concerns only, delegate business logic to Services
2. **Service Layer** - Business logic, transactions, events
3. **Repository Layer** - Complex queries (optional, use when needed)
4. **Type Everything** - Return types, parameter types, property types
5. **Form Requests** - Validation never in controllers
6. **API Resources** - Response transformation, never return models directly

## Architecture Quick Reference

| Layer | Responsibility | Depends On |
|-------|---------------|------------|
| **Controller** | HTTP request/response | Services, FormRequests |
| **Service** | Business logic, transactions | Repositories, Models, Events |
| **Repository** | Complex/reusable queries | Models |
| **Model** | Data, relationships, scopes | Other Models only |

## Essential Patterns

### Controller Pattern

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreOrderRequest;
use App\Http\Resources\OrderResource;
use App\Models\Order;
use App\Services\OrderService;
use Illuminate\Http\JsonResponse;
use Symfony\Component\HttpFoundation\Response;

final class OrderController extends Controller
{
    public function __construct(
        private readonly OrderService $orderService
    ) {}

    public function index(): JsonResponse
    {
        $orders = Order::query()
            ->forUser(auth()->id())
            ->with(['items'])
            ->latest()
            ->paginate(15);

        return response()->json(OrderResource::collection($orders));
    }

    public function store(StoreOrderRequest $request): JsonResponse
    {
        $order = $this->orderService->create($request->validated());

        return response()->json(
            new OrderResource($order),
            Response::HTTP_CREATED
        );
    }

    public function show(Order $order): JsonResponse
    {
        $this->authorize('view', $order);
        
        return response()->json(
            new OrderResource($order->load(['items', 'payments']))
        );
    }

    public function destroy(Order $order): JsonResponse
    {
        $this->authorize('delete', $order);
        $order->delete();
        
        return response()->json(null, Response::HTTP_NO_CONTENT);
    }
}
```

### Service Pattern

```php
<?php


namespace App\Services;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\DB;

final class OrderService
{
    public function create(array $data): Order
    {
        return DB::transaction(function () use ($data): Order {
            $order = Order::query()->create([
                'user_id' => auth()->id(),
                'status' => OrderStatus::Pending,
                'total' => $data['total'],
            ]);

            $order->items()->createMany($data['items']);

            event(new OrderCreated($order));

            return $order->load('items');
        });
    }
}
```

### Form Request Pattern

```php
<?php


namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

final class StoreOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'total' => ['required', 'numeric', 'min:0'],
            'items' => ['required', 'array', 'min:1'],
            'items.*.product_id' => [
                'required',
                Rule::exists('products', 'id')->where('active', true),
            ],
            'items.*.quantity' => ['required', 'integer', 'min:1', 'max:100'],
        ];
    }
}
```

### API Resource Pattern

```php
<?php


namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

final class OrderResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'status' => $this->status->value,
            'total' => $this->total,
            'created_at' => $this->created_at->toISOString(),
            
            // Conditional relationships
            'user' => new UserResource($this->whenLoaded('user')),
            'items' => OrderItemResource::collection($this->whenLoaded('items')),
            
            // Conditional attributes
            'can_cancel' => $this->when(
                $request->user()?->can('cancel', $this->resource),
                true
            ),
        ];
    }
}
```

## References

Load detailed patterns as needed:

| Topic | Reference | When to Load |
|-------|-----------|--------------|
| Sanctum authentication | [references/sanctum.md](references/sanctum.md) | Token auth, SPA auth, abilities |
| Passport OAuth | [references/passport.md](references/passport.md) | OAuth2, third-party apps |
| Service-Repository details | [references/service-repository.md](references/service-repository.md) | Complex business logic |

## Quick Commands

```bash
# Create with best practices
php artisan make:model Order -mfsc          # Model, migration, factory, seeder, controller
php artisan make:request StoreOrderRequest
php artisan make:resource OrderResource
php artisan make:policy OrderPolicy --model=Order

# API Routes
php artisan route:list --path=api

# Format code
./vendor/bin/pint
```

## Remember

- Use `->query()` for IDE completion: `Order::query()->where(...)`
- Use `final class` for services and controllers
- Use `readonly` constructor properties
- Use `match` over complex if/else
- Use Enums for status fields
- Always return `JsonResponse`, never raw arrays
- Use HTTP status constants: `Response::HTTP_CREATED`

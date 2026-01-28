---
name: laravel-actions
description: Action-oriented architecture for Laravel. Invokable classes that contain domain logic. Use when working with business logic, domain operations, or when user mentions actions, invokable classes, or needs to organize domain logic outside controllers.
---

# Laravel Actions

Actions are the **heart of your domain logic**. Every business operation lives in an action.

**Related guides:**
- [DTOs](../laravel-dtos/SKILL.md) - DTOs for passing data to actions
- [Controllers](../laravel-controllers/SKILL.md) - Controllers delegate to actions
- [Models](../laravel-models/SKILL.md) - Models accessed by actions
- [Testing](../laravel-testing/SKILL.md) - Testing with triple-A pattern

## Philosophy

**Controllers, Jobs, and Listeners contain ZERO domain logic** - they only delegate to actions.

Actions are:
- **Invokable classes** - Single `__invoke()` method
- **Single responsibility** - Each action does exactly one thing
- **Composable** - Actions call other actions to build workflows
- **Stateless** - Each invocation is independent (but can store invocation context)
- **Type-safe** - Strict parameter and return types
- **Transactional** - Wrap database modifications in transactions

## Basic Structure

```php
<?php

declare(strict_types=1);

namespace App\Actions\Order;

use App\Data\CreateOrderData;
use App\Models\Order;
use App\Models\User;
use Illuminate\Support\Facades\DB;

class CreateOrderAction
{
    public function __invoke(User $user, CreateOrderData $data): Order
    {
        return DB::transaction(function () use ($user, $data) {
            $order = $this->createOrder($user, $data);
            $this->attachOrderItems($order, $data);

            return $order->fresh(['items']);
        });
    }

    private function createOrder(User $user, CreateOrderData $data): Order
    {
        return $user->orders()->create([
            'status' => $data->status,
            'notes' => $data->notes,
        ]);
    }

    private function attachOrderItems(Order $order, CreateOrderData $data): void
    {
        $order->items()->createMany(
            $data->items->map(fn ($item) => [
                'product_id' => $item->productId,
                'quantity' => $item->quantity,
                'price' => $item->price,
            ])->all()
        );
    }
}
```

## Key Patterns

### 1. Dependency Injection for Action Composition

**Inject other actions** to build complex workflows:

```php
class CreateOrderAction
{
    public function __construct(
        private readonly CalculateOrderTotalAction $calculateTotal,
        private readonly NotifyOrderCreatedAction $notifyOrderCreated,
    ) {}

    public function __invoke(User $user, CreateOrderData $data): Order
    {
        return DB::transaction(function () use ($user, $data) {
            $order = $this->createOrder($user, $data);

            // Compose with other actions
            $total = ($this->calculateTotal)($order);
            $order->update(['total' => $total]);

            ($this->notifyOrderCreated)($order);

            return $order->fresh();
        });
    }
}
```

### 2. Guard Methods for Validation

**Validate business rules** before executing:

```php
class CancelOrderAction
{
    public function __invoke(Order $order): Order
    {
        $this->guard($order);

        return DB::transaction(function () use ($order) {
            $order->updateToCancelled();
            $this->refundPayment($order);
            return $order;
        });
    }

    private function guard(Order $order): void
    {
        throw_unless(
            $order->canBeCancelled(),
            OrderException::cannotCancelOrder($order)
        );
    }
}
```

### 3. Private Helper Methods

**Break complex operations** into smaller, focused private methods:

```php
public function __invoke(User $user, CreateApplicationData $data): Application
{
    return DB::transaction(function () use ($user, $data) {
        $application = $this->createApplication($user, $data);
        $this->createContacts($application, $data);
        $this->createAddresses($application, $data);
        $this->createDocuments($application, $data);

        return $application;
    });
}
```

### 4. Readonly Properties for Context

**Store invocation context** in readonly properties to avoid parameter passing:

```php
class ProcessOrderAction
{
    private readonly Order $order;

    public function __invoke(Order $order): void
    {
        $this->order = $order;
        $this->guard();

        DB::transaction(function (): void {
            $this->processPayment();
            $this->updateInventory();
            $this->sendNotifications();
        });
    }

    private function guard(): void
    {
        throw_unless($this->order->isPending(), 'Order must be pending');
    }

    private function processPayment(): void
    {
        // Access $this->order without passing it
    }
}
```

## Naming Conventions

**Format:** `{Verb}{Entity}Action`

**Examples:**
- `CreateOrderAction`
- `UpdateUserProfileAction`
- `DeleteDocumentAction`
- `CalculateOrderTotalAction`
- `SendEmailNotificationAction`
- `ProcessPaymentAction`

## When to Create an Action

### ✅ Create an action when:

- **Any** domain operation (including simple CRUD)
- Implementing business logic of any complexity
- Building reusable operations used across multiple places
- Composing multiple steps into a workflow
- Job or listener needs to perform domain logic
- **Any operation that touches your models or data**

### ❌ Don't create an action for:

- Pure data retrieval for display (use queries/query builders)
- HTTP-specific concerns (belongs in middleware/controllers)
- Formatting/presentation logic (use resources/transformers)

**Critical Rule:** Controllers should contain **zero domain logic**. Even a simple `$user->update($data)` should be delegated to `UpdateUserAction`.

## Invocation Patterns

### Via Dependency Injection

```php
public function store(
    CreateOrderRequest $request,
    CreateOrderAction $action
) {
    $order = $action(user(), CreateOrderData::from($request));
    return OrderResource::make($order);
}
```

### Via `resolve()` Helper

```php
// In controllers
$order = resolve(CreateOrderAction::class)(
    user(),
    CreateOrderData::from($request)
);

// Inside another action
$result = resolve(ProcessPaymentAction::class)($order, $paymentData);
```

**Important:** Use `resolve()` not `app()` for consistency.

## Database Transactions

**Always wrap data modifications** in transactions:

```php
public function __invoke(CreateOrderData $data): Order
{
    return DB::transaction(function () use ($data) {
        $order = Order::create($data->toArray());
        $order->items()->createMany($data->items->toArray());

        return $order;
    });
}
```

## Error Handling

**Throw domain exceptions** for business rule violations:

```php
class CreateOrderAction
{
    public function __invoke(User $user, CreateOrderData $data): Order
    {
        if ($user->orders()->pending()->count() >= 5) {
            throw OrderException::tooManyPendingOrders($user);
        }

        return DB::transaction(function () use ($user, $data) {
            return $user->orders()->create($data->toArray());
        });
    }
}
```

## Testing Actions

**Unit tests** should test actions in isolation using the triple-A pattern:

```php
use function Pest\Laravel\assertDatabaseHas;

it('creates an order', function () {
    // Arrange
    $user = User::factory()->create();
    $data = CreateOrderData::testFactory()->make();

    // Act
    $order = resolve(CreateOrderAction::class)($user, $data);

    // Assert
    expect($order)->toBeInstanceOf(Order::class);
    assertDatabaseHas('orders', ['id' => $order->id]);
});

it('throws exception when user has too many pending orders', function () {
    // Arrange
    $user = User::factory()
        ->has(Order::factory()->pending()->count(5))
        ->create();
    $data = CreateOrderData::testFactory()->make();

    // Act & Assert
    expect(fn () => resolve(CreateOrderAction::class)($user, $data))
        ->toThrow(OrderException::class);
});
```

## Common Patterns

### Simple CRUD Action

```php
class UpdateUserAction
{
    public function __invoke(User $user, UpdateUserData $data): User
    {
        $user->update($data->toArray());
        return $user->fresh();
    }
}
```

### Multi-Step Workflow

```php
class OnboardUserAction
{
    public function __construct(
        private readonly CreateUserProfileAction $createProfile,
        private readonly SendWelcomeEmailAction $sendWelcome,
        private readonly AssignDefaultRoleAction $assignRole,
    ) {}

    public function __invoke(RegisterUserData $data): User
    {
        return DB::transaction(function () use ($data) {
            $user = User::create($data->toArray());

            ($this->createProfile)($user, $data->profileData);
            ($this->assignRole)($user);
            ($this->sendWelcome)($user);

            return $user;
        });
    }
}
```

### External Service Integration

```php
class ProcessPaymentAction
{
    public function __construct(
        private readonly StripeService $stripe,
    ) {}

    public function __invoke(Order $order, PaymentData $data): Payment
    {
        $this->guard($order);

        return DB::transaction(function () use ($order, $data) {
            $stripePayment = $this->stripe->charge($data);

            $payment = $order->payments()->create([
                'amount' => $data->amount,
                'stripe_id' => $stripePayment->id,
                'status' => PaymentStatus::Completed,
            ]);

            $order->markAsPaid();

            return $payment;
        });
    }

    private function guard(Order $order): void
    {
        throw_if($order->isPaid(), 'Order already paid');
    }
}
```

## Action Organization

**Group by domain entity:**

```
app/Actions/
├── Order/
│   ├── CreateOrderAction.php
│   ├── CancelOrderAction.php
│   ├── ProcessOrderAction.php
│   └── CalculateOrderTotalAction.php
├── User/
│   ├── CreateUserAction.php
│   ├── UpdateUserProfileAction.php
│   └── DeleteUserAction.php
└── Payment/
    ├── ProcessPaymentAction.php
    └── RefundPaymentAction.php
```

**Not by action type** (avoid CreateActions/, UpdateActions/, etc.)

## Multi-Tenancy

**Separate Central and Tenanted actions:**

```
app/Actions/
├── Central/
│   ├── CreateTenantAction.php
│   └── ProvisionDatabaseAction.php
└── Tenanted/
    ├── CreateOrderAction.php
    └── UpdateUserAction.php
```

See [Multi-tenancy](../laravel-multi-tenancy/SKILL.md) for comprehensive patterns.

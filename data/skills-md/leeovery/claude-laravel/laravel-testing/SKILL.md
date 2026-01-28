---
name: laravel-testing
description: Comprehensive testing patterns with Pest. Use when working with tests, testing patterns, or when user mentions testing, tests, Pest, PHPUnit, mocking, factories, test patterns.
---

# Laravel Testing

Testing patterns with Pest: Arrange-Act-Assert, proper mocking, null drivers, declarative factories.

**Related guides:**
- [testing-conventions.md](references/testing-conventions.md) - Test file structure and RESTful ordering
- [testing-factories.md](references/testing-factories.md) - Declarative factory methods for readable tests
- [validation-testing.md](../laravel-validation/references/validation-testing.md) - Form request validation testing
- [Actions](../laravel-actions/SKILL.md) - Action pattern for unit testing
- [Controllers](../laravel-controllers/SKILL.md) - Controller patterns for feature testing
- [DTOs](../laravel-dtos/SKILL.md) - DTO test factories
- [Services](../laravel-services/SKILL.md) - Service layer with null drivers

## Philosophy

Testing should be:
- **Isolated** - Test one thing at a time
- **Reliable** - Consistent results every time
- **Maintainable** - Easy to update when code changes
- **Fast** - Quick feedback loop
- **Realistic** - Use factories, not hardcoded values

## The Triple-A Pattern

Every test should follow the **Arrange-Act-Assert** pattern:

### 1. Arrange the World

Set up all the data and dependencies needed using **factories**:

```php
it('creates an order with items', function () {
    // Arrange: Create the world state
    $user = User::factory()->create();
    $product = Product::factory()->active()->create(['price' => 1000]);

    $data = CreateOrderData::from([
        'customer_email' => 'customer@example.com',
        'items' => [
            ['product_id' => $product->id, 'quantity' => 2],
        ],
    ]);

    // Act: Perform the operation
    $order = resolve(CreateOrderAction::class)($user, $data);

    // Assert: Verify the results
    expect($order)
        ->toBeInstanceOf(Order::class)
        ->and($order->items)->toHaveCount(1)
        ->and($order->total)->toBe(2000);
});
```

### 2. Act on the World

Perform the **single operation** you're testing:

```php
// ✅ Good - Single, clear action
$order = resolve(CreateOrderAction::class)($user, $data);

// ❌ Bad - Multiple actions mixed with assertions
$order = resolve(CreateOrderAction::class)($user, $data);
expect($order)->toBeInstanceOf(Order::class);
$order->refresh();
expect($order->total)->toBe(2000);
```

### 3. Assert on the Results

Verify the **outcomes** of your action:

```php
// ✅ Good - Clear, focused assertions
expect($order)
    ->toBeInstanceOf(Order::class)
    ->and($order->status)->toBe(OrderStatus::Pending)
    ->and($order->items)->toHaveCount(2);

assertDatabaseHas('orders', [
    'id' => $order->id,
    'user_id' => $user->id,
]);

// ❌ Bad - Testing implementation details
expect($order->getAttribute('status'))->toBe('pending');
```

## Testing Actions

Actions are the **heart of your domain logic** and should be thoroughly tested in isolation.

### Basic Action Test

```php
use App\Actions\Order\CreateOrderAction;
use App\Data\CreateOrderData;
use App\Enums\OrderStatus;
use App\Models\User;
use function Pest\Laravel\assertDatabaseHas;

it('creates an order', function () {
    // Arrange
    $user = User::factory()->create();
    $data = CreateOrderData::testFactory()->make([
        'status' => OrderStatus::Pending,
    ]);

    // Act
    $order = resolve(CreateOrderAction::class)($user, $data);

    // Assert
    expect($order)->toBeInstanceOf(Order::class);
    assertDatabaseHas('orders', [
        'id' => $order->id,
        'user_id' => $user->id,
        'status' => OrderStatus::Pending->value,
    ]);
});
```

### Testing Action Guard Methods

```php
it('throws exception when user has too many pending orders', function () {
    // Arrange
    $user = User::factory()
        ->has(Order::factory()->pending()->count(5))
        ->create();

    $data = CreateOrderData::testFactory()->make();

    // Act & Assert
    expect(fn () => resolve(CreateOrderAction::class)($user, $data))
        ->toThrow(OrderException::class, 'Too many pending orders');
});
```

### Testing Action Composition

**Critical pattern:** Always resolve actions from the container using `resolve()` so dependencies are recursively resolved. Use `swap()` to replace dependencies with mocked versions.

```php
use function Pest\Laravel\mock;
use function Pest\Laravel\swap;

it('processes order and sends notification', function () {
    // Arrange
    $user = User::factory()->create();
    $order = Order::factory()->for($user)->create();

    // Mock the dependency actions and swap them into the container
    $calculateTotal = mock(CalculateOrderTotalAction::class);
    $calculateTotal->shouldReceive('__invoke')
        ->once()
        ->with($order)
        ->andReturn(10000);
    swap(CalculateOrderTotalAction::class, $calculateTotal);

    $notifyOrder = mock(NotifyOrderCreatedAction::class);
    $notifyOrder->shouldReceive('__invoke')
        ->once()
        ->with($order);
    swap(NotifyOrderCreatedAction::class, $notifyOrder);

    // Act - resolve() from container so mocked dependencies are injected
    $result = resolve(ProcessOrderAction::class)($order);

    // Assert
    expect($result->total)->toBe(10000);
});
```

**Why this pattern:**
- `resolve()` ensures the action is pulled from the container with all dependencies
- `swap()` replaces the dependency in the container with your mock
- Container handles recursive dependency resolution automatically
- If a dependency adds a new dependency, your tests don't break

## Mocking Guidelines

### Only Mock What You Own

**Critical principle:** Only mock code that you control. Never mock external services directly.

#### ✅ Good - Mock Your Own Actions

```php
use function Pest\Laravel\mock;
use function Pest\Laravel\swap;

// Mock an action you own and swap it into the container
$sendEmail = mock(SendWelcomeEmailAction::class);
$sendEmail->shouldReceive('__invoke')
    ->once()
    ->with(Mockery::type(User::class));
swap(SendWelcomeEmailAction::class, $sendEmail);

// Then resolve the action under test - it will receive the mocked dependency
$result = resolve(RegisterUserAction::class)($data);
```

#### ✅ Advanced - Verify Mock Arguments with Assertions

Use `withArgs()` with a closure to verify the **exact instances and values** being passed:

```php
it('processes match with correct arguments', function () {
    $matchAttempt = MatchAttempt::factory()->create();
    $data = MatchData::testFactory()->make();

    // Mock and verify exact arguments using expect() assertions
    $mockAction = mock(CreateMatchResultAction::class);
    $mockAction->shouldReceive('__invoke')
        ->once()
        ->withArgs(function (MatchAttempt $_matchAttempt, MatchData $_data) use ($data, $matchAttempt) {
            // Verify the exact model instance is passed
            expect($_matchAttempt->is($matchAttempt))->toBeTrue()
                // Verify the exact DTO value is passed
                ->and($_data)->toBe($data->matches->first());

            return true; // Return true to pass the assertion
        });
    swap(CreateMatchResultAction::class, $mockAction);

    // Act
    resolve(ProcessMatchAction::class)($matchAttempt, $data);
});
```

#### ✅ Good - Mock Your Own Services (via Facade)

```php
// Mock your own service through its facade
Payment::shouldReceive('createPaymentIntent')
    ->once()
    ->with(10000, 'usd')
    ->andReturn(PaymentIntentData::from([
        'id' => 'pi_test_123',
        'status' => 'succeeded',
    ]));
```

#### ❌ Bad - Mocking External Libraries Directly

```php
// ❌ DON'T DO THIS - Mocking Stripe SDK directly
$stripe = Mockery::mock(\Stripe\StripeClient::class);
$stripe->shouldReceive('paymentIntents->create')
    ->andReturn(/* ... */);

// This is brittle and breaks when Stripe updates their SDK
```

### When You Need to Mock Something You Don't Own

If you find yourself needing to mock an external service, **create an abstraction**:

1. **Create a Service Layer** with the Manager pattern
2. **Define a Driver Contract** (interface)
3. **Implement the Real Driver** (wraps external API)
4. **Create a Null Driver** for testing
5. **Add a Facade** for convenience

See [Services](../laravel-services/SKILL.md) for complete implementation examples.

## Using Null Drivers

The null driver pattern provides **deterministic, fast tests** without external dependencies:

```php
it('processes payment successfully', function () {
    // Arrange - Use null driver (configured in phpunit.xml or .env.testing)
    Config::set('payment.default', 'null');

    $order = Order::factory()->create(['total' => 10000]);
    $data = PaymentData::from(['amount' => 10000, 'currency' => 'usd']);

    // Act - No mocking needed, null driver returns test data
    $payment = resolve(ProcessPaymentAction::class)($order, $data);

    // Assert
    expect($payment)
        ->toBeInstanceOf(Payment::class)
        ->and($payment->status)->toBe(PaymentStatus::Completed);
});
```

**Benefits of null drivers:**
- No mocking required
- Fast execution (no network calls)
- Deterministic results
- Can test error scenarios by extending null driver
- Matches real driver interface exactly

### Testing Error Scenarios

Extend the null driver for specific test scenarios:

```php
// tests/Fakes/FailingPaymentDriver.php
class FailingPaymentDriver implements PaymentDriver
{
    public function createPaymentIntent(int $amount, string $currency): PaymentIntentData
    {
        throw PaymentException::failedToCharge('Card declined');
    }
}

// In test
it('handles payment failure gracefully', function () {
    $this->app->bind(PaymentManager::class, function () {
        $manager = new PaymentManager($this->app);
        $manager->extend('failing', fn () => new FailingPaymentDriver);
        return $manager;
    });

    Config::set('payment.default', 'failing');

    $order = Order::factory()->create();
    $data = PaymentData::testFactory();

    expect(fn () => resolve(ProcessPaymentAction::class)($order, $data))
        ->toThrow(PaymentException::class, 'Card declined');
});
```

## Using Factories

Factories create **realistic, randomized test data** that makes tests more robust.

### Model Factories

```php
// Arrange with factories
$user = User::factory()->create();
$product = Product::factory()->active()->create();
$order = Order::factory()->for($user)->create();

// Factory with state
$pendingOrder = Order::factory()->pending()->create();
$paidOrder = Order::factory()->paid()->create();

// Factory with relationships
$user = User::factory()
    ->has(Order::factory()->count(3))
    ->create();
```

### Declarative Factory Methods

**Critical principle:** Make tests **declarative and readable** by hiding database implementation details behind factory methods.

```php
// ❌ Bad - Database schema leaks into test
$calendar = Calendar::factory()->create([
    'status' => 'accepted',
    'reminder_sent_at' => null,
    'approved_by' => User::factory()->create()->id,
    'approved_at' => now(),
]);

// ✅ Good - Declarative and readable
$calendar = Calendar::factory()->accepted()->create();
```

**[→ Complete declarative factory patterns: testing-factories.md](references/testing-factories.md)**

### DTO Test Factories

DTOs should provide **test factories** for consistent test data:

```php
class CreateOrderData extends Data
{
    public function __construct(
        public string $customerEmail,
        public OrderStatus $status,
        public array $items,
    ) {}

    public static function testFactory(): self
    {
        return new self(
            customerEmail: fake()->email(),
            status: OrderStatus::Pending,
            items: [
                [
                    'product_id' => Product::factory()->create()->id,
                    'quantity' => fake()->numberBetween(1, 5),
                ],
            ],
        );
    }
}

// Usage in tests
$data = CreateOrderData::testFactory();
```

## Testing Strategy

### Feature Tests (HTTP Layer)

Test the **complete request/response cycle**:

```php
use function Pest\Laravel\actingAs;
use function Pest\Laravel\postJson;

it('creates an order via API', function () {
    $user = User::factory()->create();
    $product = Product::factory()->create();

    $response = actingAs($user)
        ->postJson('/api/orders', [
            'customer_email' => 'test@example.com',
            'items' => [
                ['product_id' => $product->id, 'quantity' => 2],
            ],
        ]);

    $response->assertCreated()
        ->assertJsonStructure([
            'data' => ['id', 'status', 'items'],
        ]);
});
```

### Unit Tests (Actions)

Test **domain logic in isolation**:

```php
it('calculates order total correctly', function () {
    $order = Order::factory()->create();
    $order->items()->createMany([
        ['price' => 1000, 'quantity' => 2],
        ['price' => 1500, 'quantity' => 1],
    ]);

    $total = resolve(CalculateOrderTotalAction::class)($order);

    expect($total)->toBe(3500);
});
```

## Avoiding Brittle Tests

Brittle tests break when implementation changes, even if behavior is correct.

### Signs of Brittle Tests

- Too many mocks
- Testing implementation details
- Hardcoded values everywhere
- Complex setup with many steps
- Tests break with refactoring

### How to Avoid Brittleness

#### 1. Use Real Instances When Possible

```php
// ✅ Good - Use real instances
it('calculates order total', function () {
    $order = Order::factory()->create();
    $order->items()->createMany([
        ['price' => 1000, 'quantity' => 2],
        ['price' => 500, 'quantity' => 1],
    ]);

    $total = resolve(CalculateOrderTotalAction::class)($order);

    expect($total)->toBe(2500);
});

// ❌ Bad - Mock everything
it('calculates order total', function () {
    $item1 = Mockery::mock(OrderItem::class);
    $item1->shouldReceive('getPrice')->andReturn(1000);
    // ... too much mocking
});
```

#### 2. Test Behavior, Not Implementation

```php
// ✅ Good - Test the behavior
it('sends welcome email when user registers', function () {
    Mail::fake();

    $data = RegisterUserData::testFactory();
    $user = resolve(RegisterUserAction::class)($data);

    Mail::assertSent(WelcomeEmail::class, function ($mail) use ($user) {
        return $mail->hasTo($user->email);
    });
});

// ❌ Bad - Test implementation details
it('sends welcome email when user registers', function () {
    $mailer = Mockery::mock(Mailer::class);
    $mailer->shouldReceive('send')
        ->with(Mockery::on(function ($email) {
            return $email->template === 'emails.welcome';
        }));
    // Too specific, breaks if template name changes
});
```

#### 3. Use Factories Instead of Hardcoded Data

```php
// ✅ Good - Use factories
$user = User::factory()->create();
$data = ProfileData::testFactory();

// ❌ Bad - Hardcoded data
$data = new ProfileData(
    firstName: 'John',
    lastName: 'Doe',
    phone: '555-1234',
    bio: 'Test bio',
);
```

#### 4. Minimize Mocking

**Rule of thumb:** Mock collaborators, not data.

```php
// ✅ Good - Mock the notification service (collaborator)
$notifier = mock(NotificationService::class);
$notifier->shouldReceive('send')->once();
swap(NotificationService::class, $notifier);

resolve(ShipOrderAction::class)($order);

// ❌ Bad - Mock the data (order, user)
$order = Mockery::mock(Order::class);
// ... mocking data objects makes test brittle
```

## Common Testing Patterns

### Testing State Transitions

```php
it('transitions order from pending to paid', function () {
    $order = Order::factory()->pending()->create();

    resolve(MarkOrderAsPaidAction::class)($order);

    expect($order->fresh()->status)->toBe(OrderStatus::Paid)
        ->and($order->fresh()->paid_at)->not->toBeNull();
});
```

### Testing Relationships

```php
it('creates order with items', function () {
    $user = User::factory()->create();
    $products = Product::factory()->count(3)->create();

    $data = CreateOrderData::from([
        'customer_email' => 'test@example.com',
        'items' => $products->map(fn ($p) => [
            'product_id' => $p->id,
            'quantity' => 2,
        ])->all(),
    ]);

    $order = resolve(CreateOrderAction::class)($user, $data);

    expect($order->items)->toHaveCount(3);
});
```

### Testing Transactions

```php
it('rolls back transaction on failure', function () {
    $user = User::factory()->create();

    $data = CreateOrderData::from([
        'customer_email' => 'test@example.com',
        'items' => [
            ['product_id' => 99999, 'quantity' => 1], // Non-existent product
        ],
    ]);

    expect(fn () => resolve(CreateOrderAction::class)($user, $data))
        ->toThrow(Exception::class);

    assertDatabaseCount('orders', 0);
    assertDatabaseCount('order_items', 0);
});
```

### Testing Email/Notifications

```php
use Illuminate\Support\Facades\Mail;

it('sends welcome email to new user', function () {
    Mail::fake();
    $data = RegisterUserData::testFactory();

    $user = resolve(RegisterUserAction::class)($data);

    Mail::assertSent(WelcomeEmail::class, function ($mail) use ($user) {
        return $mail->hasTo($user->email);
    });
});
```

### Testing Jobs

```php
use Illuminate\Support\Facades\Queue;

it('dispatches job to process order', function () {
    Queue::fake();
    $order = Order::factory()->create();

    resolve(ProcessOrderAction::class)($order);

    Queue::assertPushed(ProcessOrderJob::class, function ($job) use ($order) {
        return $job->order->id === $order->id;
    });
});
```

## Best Practices Summary

### ✅ Do This

- **Follow triple-A pattern** - Arrange, Act, Assert
- **Use factories** for all test data
- **Create declarative factory methods** - `Calendar::factory()->accepted()` not `['status' => 'accepted']`
- **Test actions in isolation** - Unit test your domain logic
- **Mock what you own** - Actions, services you control
- **Create abstractions** when you need to mock external services
- **Use null drivers** for external service testing
- **Test behavior, not implementation**
- **Keep tests simple** - One concept per test
- **Use DTO test factories** for consistent data

### ❌ Don't Do This

- **Mock external libraries** - Create service layer instead
- **Hardcode test data** - Use factories
- **Leak database schema into tests** - Use declarative factory methods
- **Test implementation details** - Test behavior
- **Create brittle tests** - Too many mocks, too specific
- **Skip factories** - Always use factories for models and DTOs
- **Mix arrange and act** - Keep them separate
- **Over-mock** - Use real instances when possible

## Quick Reference

### Test Structure

```php
it('does something', function () {
    // Arrange - Set up the world with declarative factories
    $model = Model::factory()->active()->create();
    $data = Data::testFactory();

    // Act - Perform the operation
    $result = resolve(Action::class)($model, $data);

    // Assert - Verify the results
    expect($result)->/* assertions */;
});
```

### Mocking Pattern

```php
use function Pest\Laravel\mock;
use function Pest\Laravel\swap;

// Mock a dependency action
$mockAction = mock(YourDependencyAction::class);
$mockAction->shouldReceive('__invoke')
    ->once()
    ->with(/* expected params */)
    ->andReturn(/* return value */);

// Swap into container
swap(YourDependencyAction::class, $mockAction);

// Resolve action under test - container injects mocked dependencies
$result = resolve(ActionUnderTest::class)(/* params */);
```

### Database Assertions

```php
use function Pest\Laravel\assertDatabaseHas;
use function Pest\Laravel\assertDatabaseCount;

assertDatabaseHas('orders', ['id' => $order->id]);
assertDatabaseCount('orders', 1);
```

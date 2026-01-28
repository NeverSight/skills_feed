---
name: laravel-testing
description: "Laravel testing with PHPUnit and Dusk, feature tests, unit tests, browser tests, factories, assertions. ALWAYS activate when: writing tests, tests/Feature/, tests/Unit/, tests/Browser/, running php artisan test, test coverage, TDD. Triggers on: test failed, assertion error, factory, seeder, RefreshDatabase, actingAs, mock, Dusk element not found, browser test, screenshot, CI/CD testing, test çalışmıyor, coverage düşük, test hatası, assertion failed, mock çalışmıyor."
---

# Laravel Testing

PHPUnit + Dusk testing patterns for Laravel 12+.

## Feature Tests

```php
<?php

namespace Tests\Feature;

use App\Models\Order;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class OrderTest extends TestCase
{
    use RefreshDatabase;

    /**
     * Test order creation endpoint.
     */
    public function test_user_can_create_order(): void
    {
        $user = User::factory()->create();

        $response = $this
            ->actingAs($user)
            ->postJson('/api/orders', [
                'total' => 100.00,
                'items' => [
                    ['product_id' => 1, 'quantity' => 2],
                ],
            ]);

        $response
            ->assertCreated()
            ->assertJsonStructure([
                'id',
                'status',
                'total',
            ]);

        $this->assertDatabaseHas('orders', [
            'user_id' => $user->id,
            'status' => 'pending',
        ]);
    }

    /**
     * Test authentication requirement.
     */
    public function test_order_creation_requires_authentication(): void
    {
        $this->postJson('/api/orders', [])
            ->assertUnauthorized();
    }

    /**
     * Test validation rules.
     */
    public function test_order_validates_required_fields(): void
    {
        $user = User::factory()->create();

        $this
            ->actingAs($user)
            ->postJson('/api/orders', [])
            ->assertUnprocessable()
            ->assertJsonValidationErrors(['total', 'items']);
    }
}
```

## Unit Tests

```php
<?php

namespace Tests\Unit;

use App\Services\TaxCalculator;
use PHPUnit\Framework\TestCase;

class TaxCalculatorTest extends TestCase
{
    /**
     * Test tax calculation with 20% rate.
     */
    public function test_calculates_tax_correctly(): void
    {
        $calculator = new TaxCalculator(taxRate: 0.20);
        
        $result = $calculator->calculate(100.00);
        
        $this->assertEquals(120.00, $result);
    }

    /**
     * Test zero amount returns zero.
     */
    public function test_zero_amount_returns_zero(): void
    {
        $calculator = new TaxCalculator(taxRate: 0.20);
        
        $this->assertEquals(0.00, $calculator->calculate(0.00));
    }
}
```

## Factories

```php
<?php

namespace Database\Factories;

use App\Enums\OrderStatus;
use App\Models\Order;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Order>
 */
class OrderFactory extends Factory
{
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'status' => OrderStatus::Pending,
            'total' => $this->faker->randomFloat(2, 10, 1000),
        ];
    }

    /**
     * Set order as completed.
     */
    public function completed(): static
    {
        return $this->state(fn (array $attributes) => [
            'status' => OrderStatus::Completed,
        ]);
    }

    /**
     * Set order as cancelled.
     */
    public function cancelled(): static
    {
        return $this->state(fn (array $attributes) => [
            'status' => OrderStatus::Cancelled,
        ]);
    }
}
```

## Factory Usage

```php
// Single model
$user = User::factory()->create();

// With count
$users = User::factory()->count(5)->create();

// With relationships
$order = Order::factory()
    ->for($user)
    ->has(OrderItem::factory()->count(3))
    ->create();

// With state
$completedOrder = Order::factory()->completed()->create();
```

## Assertions

```php
// HTTP Response
$response->assertOk();                    // 200
$response->assertCreated();               // 201
$response->assertNoContent();             // 204
$response->assertUnauthorized();          // 401
$response->assertForbidden();             // 403
$response->assertNotFound();              // 404
$response->assertUnprocessable();         // 422

// JSON
$response->assertJson(['status' => 'pending']);
$response->assertJsonPath('data.0.id', 1);
$response->assertJsonCount(3, 'data');
$response->assertJsonStructure(['id', 'name', 'email']);

// Database
$this->assertDatabaseHas('orders', ['status' => 'pending']);
$this->assertDatabaseMissing('orders', ['status' => 'cancelled']);
$this->assertDatabaseCount('orders', 5);
$this->assertSoftDeleted($order);
```

## Mocking

```php
use App\Services\PaymentService;

public function test_order_charges_payment(): void
{
    $this->mock(PaymentService::class, function ($mock) {
        $mock->shouldReceive('charge')
            ->once()
            ->with(100.00)
            ->andReturn(true);
    });

    // Test code that uses PaymentService
}
```

## References

| Topic | Reference | When to Load |
|-------|-----------|--------------|
| PHPUnit patterns | [references/phpunit.md](references/phpunit.md) | Advanced PHPUnit, data providers |
| Dusk browser tests | [references/dusk.md](references/dusk.md) | Browser testing, screenshots |

## Quick Commands

```bash
# Run all tests
php artisan test

# Specific file
php artisan test tests/Feature/OrderTest.php

# Filter by name
php artisan test --filter=test_user_can_create_order

# Parallel execution
php artisan test --parallel

# With coverage
php artisan test --coverage --min=80

# Stop on first failure
php artisan test --stop-on-failure
```

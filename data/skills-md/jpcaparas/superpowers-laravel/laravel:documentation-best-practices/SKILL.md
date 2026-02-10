---
name: laravel:documentation-best-practices
description: Write meaningful documentation that explains why not what; focus on complex business logic and self-documenting code
---

# Documentation Best Practices

Keep documentation minimal and meaningful. Well-written code with descriptive names often eliminates the need for comments. Document the "why" not the "what", and focus on complex business logic, not obvious code.

## When NOT to Document

```php
// BAD: Redundant comments that add no value
class UserController
{
    // This is the constructor
    public function __construct(
        // Inject user repository
        private UserRepository $repository
    ) {
        // Set the repository
        $this->repository = $repository;
    }

    // Get all users
    public function index()
    {
        // Return all users
        return $this->repository->all();
    }
}

// BAD: Obvious comments
$user->age = 25; // Set age to 25
$total = $price * $quantity; // Calculate total
if ($user->isActive()) { // Check if user is active
    // Send email
    $this->sendEmail($user);
}
```

## When TO Document

### 1. Complex Business Logic

```php
// GOOD: Explain complex business rules
class PricingCalculator
{
    /**
     * Calculate the final price with tiered discounts.
     *
     * Discount tiers:
     * - 10+ items: 5% discount
     * - 50+ items: 10% discount
     * - 100+ items: 15% discount
     * - VIP customers get additional 5% on top
     *
     * Note: Discounts don't apply to items already on sale
     */
    public function calculateTotal(Order $order): float
    {
        $subtotal = $order->items
            ->reject(fn($item) => $item->is_on_sale)
            ->sum(fn($item) => $item->price * $item->quantity);

        $regularItems = $order->items
            ->filter(fn($item) => !$item->is_on_sale);

        $discount = match(true) {
            $regularItems->sum('quantity') >= 100 => 0.15,
            $regularItems->sum('quantity') >= 50 => 0.10,
            $regularItems->sum('quantity') >= 10 => 0.05,
            default => 0
        };

        if ($order->customer->is_vip) {
            $discount += 0.05;
        }

        return $subtotal * (1 - $discount) + $this->calculateSaleItemsTotal($order);
    }
}
```

### 2. Non-Obvious Solutions

```php
class QueryOptimizer
{
    /**
     * Using a subquery here instead of a join because it performs
     * 10x faster on large datasets (tested with 1M+ records).
     * The MySQL optimizer handles this pattern better with our indexes.
     */
    public function getActiveUsersWithRecentOrders()
    {
        return User::whereIn('id', function ($query) {
            $query->select('user_id')
                ->from('orders')
                ->where('created_at', '>', now()->subDays(30))
                ->groupBy('user_id');
        })->get();
    }

    /**
     * We're intentionally NOT eager loading relationships here.
     * The polymorphic relation combined with the large dataset
     * causes N+1 to actually be faster than the massive join.
     * Benchmarked: N+1 = 1.2s, Eager = 8.3s for 10k records.
     */
    public function getPolymorphicItems()
    {
        return Item::where('active', true)->get();
    }
}
```

### 3. Workarounds and Hacks

```php
class PaymentGateway
{
    /**
     * WORKAROUND: Stripe's API has a bug where amounts over $999,999
     * cause a timeout. We split large transactions into multiple charges.
     * Remove this when Stripe fixes the issue (tracked in STRIPE-12345).
     */
    public function chargeLargeAmount(int $amountInCents): array
    {
        if ($amountInCents <= 99999900) {
            return [$this->charge($amountInCents)];
        }

        $charges = [];
        $remaining = $amountInCents;

        while ($remaining > 0) {
            $chargeAmount = min($remaining, 99999900);
            $charges[] = $this->charge($chargeAmount);
            $remaining -= $chargeAmount;
        }

        return $charges;
    }
}
```

### 4. External Dependencies and Integration Points

```php
class ThirdPartyApiClient
{
    /**
     * Rate limit: 100 requests per minute (resets at minute boundary)
     * Docs: https://api.example.com/docs/rate-limits
     *
     * The API returns 429 with Retry-After header when limited.
     * We respect this header and queue retries accordingly.
     */
    public function makeRequest(string $endpoint, array $data = []): array
    {
        // Implementation
    }

    /**
     * The API expects dates in EST timezone regardless of server location.
     * All DateTime objects are converted to EST before sending.
     *
     * Known issue: DST transitions can cause 1-hour discrepancies.
     * The API team is aware but considers it low priority.
     */
    public function sendScheduledEvent(DateTime $scheduledAt, array $event): void
    {
        $scheduledAt->setTimezone(new DateTimeZone('America/New_York'));
        // ...
    }
}
```

## Self-Documenting Code Techniques

### 1. Descriptive Naming

```php
// BAD: Cryptic names require comments
public function calc($u, $i) // Calculate discount for user and items
{
    $d = 0; // discount
    if ($u->vip) { // if user is VIP
        $d = 0.1; // 10% discount
    }
    return $i * (1 - $d); // Apply discount
}

// GOOD: Self-explanatory names
public function calculateDiscountedPrice(User $customer, float $originalPrice): float
{
    $discountPercentage = $customer->is_vip ? 0.1 : 0;
    return $originalPrice * (1 - $discountPercentage);
}
```

### 2. Extract Methods for Clarity

```php
// BAD: Complex condition needs explanation
if ($user->created_at > now()->subDays(7) &&
    $user->orders()->count() == 0 &&
    !$user->hasVerifiedEmail()) {
    // New unverified user without orders
    $this->sendWelcomeReminder($user);
}

// GOOD: Method name explains the condition
if ($this->isNewUnengagedUser($user)) {
    $this->sendWelcomeReminder($user);
}

private function isNewUnengagedUser(User $user): bool
{
    return $user->created_at > now()->subDays(7)
        && $user->orders()->count() == 0
        && !$user->hasVerifiedEmail();
}
```

### 3. Type Declarations and Return Types

```php
// BAD: Unclear what the function accepts and returns
function process($data)
{
    // What is $data? What does this return?
}

// GOOD: Types make it self-documenting
function processOrderItems(Collection $items): OrderSummary
{
    // Clear input and output types
}
```

### 4. Value Objects for Domain Concepts

```php
// BAD: What does this string represent?
public function setPrice(string $price)
{
    $this->price = $price;
}

// GOOD: Type clarifies the domain concept
public function setPrice(Money $price)
{
    $this->price = $price;
}

// The Money class documents the concept
class Money
{
    public function __construct(
        private int $cents,
        private string $currency = 'USD'
    ) {
        if ($cents < 0) {
            throw new InvalidArgumentException('Amount cannot be negative');
        }
    }

    public function formatted(): string
    {
        return number_format($this->cents / 100, 2);
    }
}
```

## PHPDoc Best Practices

### When to Use PHPDoc

```php
/**
 * Process a refund for an order.
 *
 * @param Order $order The order to refund
 * @param float $amount Amount to refund (null for full refund)
 * @param string $reason Reason for the refund (for audit log)
 *
 * @throws PaymentGatewayException When payment gateway is unreachable
 * @throws InsufficientFundsException When refund amount exceeds paid amount
 * @throws RefundWindowExpiredException When refund window (90 days) has passed
 *
 * @return Refund The created refund record
 */
public function processRefund(
    Order $order,
    ?float $amount = null,
    string $reason = 'Customer request'
): Refund {
    // Complex refund logic
}
```

### IDE Helper Annotations

```php
class UserRepository
{
    /**
     * @return Collection<int, User>
     */
    public function getActiveUsers(): Collection
    {
        return User::where('active', true)->get();
    }

    /**
     * @param array<string, mixed> $filters
     * @return Builder<User>
     */
    public function applyFilters(array $filters): Builder
    {
        return User::query()->where($filters);
    }
}
```

### Deprecation Notices

```php
class PaymentService
{
    /**
     * @deprecated Since v2.0, use processPaymentWithStripe() instead
     * @see processPaymentWithStripe()
     */
    public function processPayment($amount)
    {
        trigger_error('Method ' . __METHOD__ . ' is deprecated', E_USER_DEPRECATED);
        return $this->processPaymentWithStripe($amount);
    }
}
```

## API Documentation

### 1. Controller Method Documentation

```php
class ApiController extends Controller
{
    /**
     * List all products with optional filtering.
     *
     * @group Products
     * @queryParam category string Filter by category slug. Example: electronics
     * @queryParam min_price number Minimum price filter. Example: 10.00
     * @queryParam max_price number Maximum price filter. Example: 100.00
     * @queryParam sort string Sort field (price, name, created_at). Default: name
     *
     * @response 200 {
     *   "data": [
     *     {
     *       "id": 1,
     *       "name": "Product Name",
     *       "price": "29.99",
     *       "category": "electronics"
     *     }
     *   ],
     *   "meta": {
     *     "total": 100,
     *     "per_page": 20,
     *     "current_page": 1
     *   }
     * }
     */
    public function index(Request $request)
    {
        // Implementation
    }
}
```

### 2. API Resource Documentation

```php
/**
 * @property-read int $id
 * @property-read string $name
 * @property-read Money $price
 * @property-read Carbon $created_at
 * @property-read Category $category
 * @property-read Collection<int, Review> $reviews
 */
class ProductResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'price' => $this->price->formatted(),
            'category' => new CategoryResource($this->whenLoaded('category')),
            'reviews' => ReviewResource::collection($this->whenLoaded('reviews')),
            'created_at' => $this->created_at->toIso8601String(),
        ];
    }
}
```

## README Documentation

### Project README Template

```markdown
# Project Name

Brief description of what this project does.

## Requirements

- PHP 8.2+
- MySQL 8.0+
- Redis 6.0+
- Node.js 18+

## Installation

\```bash
# Clone repository
git clone https://github.com/username/project.git
cd project

# Install dependencies
composer install
npm install

# Environment setup
cp .env.example .env
php artisan key:generate

# Database setup
php artisan migrate --seed

# Start development server
php artisan serve
\```

## Key Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Architecture Decisions

### Why We Use X Instead of Y

Brief explanation of important technical decisions.

### Database Design

Key points about the database structure.

## Testing

\```bash
# Run all tests
php artisan test

# Run specific test suite
php artisan test --testsuite=Feature

# With coverage
php artisan test --coverage
\```

## Deployment

Instructions for deploying to production.

## Troubleshooting

### Common Issue 1
Solution to common issue 1.

### Common Issue 2
Solution to common issue 2.
```

## Configuration Documentation

```php
// config/custom.php
return [
    /*
    |--------------------------------------------------------------------------
    | Cache TTL Settings
    |--------------------------------------------------------------------------
    |
    | These values determine how long various types of data are cached.
    | The values are in seconds. Shorter values mean fresher data but
    | more database queries. Adjust based on your needs.
    |
    */
    'cache_ttl' => [
        'short' => env('CACHE_TTL_SHORT', 60),      // User-specific data
        'medium' => env('CACHE_TTL_MEDIUM', 300),   // Frequently changing
        'long' => env('CACHE_TTL_LONG', 3600),      // Rarely changing
        'forever' => env('CACHE_TTL_FOREVER', 86400), // Static data
    ],

    /*
    |--------------------------------------------------------------------------
    | External API Configuration
    |--------------------------------------------------------------------------
    |
    | Configuration for third-party API integrations. Each service has
    | its own timeout and retry settings. Credentials are stored in .env
    |
    */
    'external_apis' => [
        'weather' => [
            'base_url' => env('WEATHER_API_URL', 'https://api.weather.com'),
            'timeout' => 5,  // seconds
            'retries' => 3,
            // Rate limit: 100 requests per minute
        ],
    ],
];
```

## Migration Documentation

```php
class CreateOrdersTable extends Migration
{
    public function up(): void
    {
        Schema::create('orders', function (Blueprint $table) {
            $table->id();

            // Customer reference - soft delete cascade handled in model
            $table->foreignId('user_id')->constrained();

            // Status uses enum for type safety (see App\Enums\OrderStatus)
            $table->string('status')->default('pending')->index();

            // Monetary values stored as integers (cents) to avoid float precision issues
            $table->unsignedInteger('subtotal');
            $table->unsignedInteger('tax');
            $table->unsignedInteger('total');

            // Snapshot shipping address as JSON for historical accuracy
            // even if customer updates their address later
            $table->json('shipping_address');

            // Soft deletes for audit trail
            $table->softDeletes();

            $table->timestamps();

            // Composite index for common query pattern
            $table->index(['user_id', 'status', 'created_at']);
        });
    }
}
```

## Testing Documentation

```php
test('document complex test scenarios', function () {
    /**
     * Scenario: Test that expired discount codes are rejected
     *
     * Given: A discount code that expired yesterday
     * When: User attempts to apply it to their cart
     * Then: The code should be rejected with appropriate message
     * And: The cart total should remain unchanged
     */

    $expiredCode = DiscountCode::factory()->expired()->create();
    $cart = Cart::factory()->withItems(3)->create();
    $originalTotal = $cart->total;

    $response = $this->postJson("/api/cart/{$cart->id}/discount", [
        'code' => $expiredCode->code,
    ]);

    $response->assertUnprocessable()
        ->assertJsonPath('errors.code.0', 'This discount code has expired.');

    expect($cart->fresh()->total)->toBe($originalTotal);
});
```

## Best Practices Summary

1. **Code should be self-documenting through good naming**
2. **Document WHY, not WHAT**
3. **Keep comments close to the code they describe**
4. **Update documentation when code changes**
5. **Use tools to generate API documentation**
6. **Document complex business rules thoroughly**
7. **Include examples in documentation**
8. **Document breaking changes clearly**
9. **Keep README files up to date**
10. **Document environmental dependencies**

Remember: The best documentation is code that doesn't need documentation. Strive for clarity in your code first, then document what remains complex or non-obvious.
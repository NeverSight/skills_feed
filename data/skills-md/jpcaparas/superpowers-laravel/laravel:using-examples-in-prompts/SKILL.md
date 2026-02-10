---
name: laravel:using-examples-in-prompts
description: Provide concrete examples—existing code patterns, style samples, input/output pairs—to guide AI toward your project's conventions
---

# Using Examples in Prompts

Examples clarify intent better than descriptions. Show the AI what you want, don't just tell it.

## Reference Existing Code

### Abstract
"Create a service similar to the payment service"

### Concrete
"Create OrderService following the pattern in `app/Services/PaymentService.php`:
```php
class PaymentService
{
    public function __construct(
        private PaymentGateway $gateway,
        private PaymentRepository $repository
    ) {}
    
    public function charge(Order $order): Payment
    {
        // Implementation
    }
}
```
Use constructor injection, return domain objects, keep methods focused."

**Why it works:** Shows structure, naming, and patterns to follow.

## Show Desired Style

### Vague
"Use consistent naming"

### Specific
"Follow our naming conventions from `app/Models/Product.php`:
```php
// Relationships: camelCase, descriptive
public function orderItems(): HasMany
public function primaryCategory(): BelongsTo

// Scopes: scope prefix, descriptive
public function scopeActive(Builder $query): void
public function scopePublishedAfter(Builder $query, Carbon $date): void

// Accessors: get prefix, Attribute suffix
public function getFormattedPriceAttribute(): string
```
Apply same patterns to the new Subscription model."

**Why it works:** Concrete examples of the conventions in action.

## Input/Output Examples

### Unclear
"Transform the product data"

### Clear
"Transform product data for the API:

**Input (from database):**
```php
[
    'id' => 1,
    'name' => 'Widget',
    'price_cents' => 2999,
    'created_at' => '2024-01-15 10:30:00',
    'category' => ['id' => 5, 'name' => 'Tools']
]
```

**Expected output:**
```json
{
    "id": 1,
    "name": "Widget",
    "price": "29.99",
    "category": "Tools",
    "created_at": "2024-01-15T10:30:00Z"
}
```

Use ProductResource to handle this transformation."

**Why it works:** Shows exact input and expected output format.

## Concrete vs Abstract

### Abstract
"Handle errors properly"

### Concrete
"Handle errors like we do in `app/Services/PaymentService.php`:
```php
try {
    $charge = $this->gateway->charge($amount);
} catch (PaymentGatewayException $e) {
    Log::error('Payment failed', [
        'order_id' => $order->id,
        'amount' => $amount,
        'error' => $e->getMessage(),
    ]);
    
    throw new PaymentFailedException(
        'Unable to process payment: ' . $e->getMessage(),
        previous: $e
    );
}
```
Use specific exceptions, log context, preserve original exception."

**Why it works:** Shows the exact error handling pattern to replicate.

### Abstract
"Add tests"

### Concrete
"Add tests following our pattern in `tests/Feature/ProductTest.php`:
```php
test('user can create product with valid data', function () {
    $user = User::factory()->create();
    $category = Category::factory()->create();
    
    $response = $this->actingAs($user)
        ->postJson('/api/products', [
            'name' => 'New Product',
            'price' => 29.99,
            'category_id' => $category->id,
        ]);
    
    $response->assertCreated()
        ->assertJsonStructure(['data' => ['id', 'name', 'price']]);
    
    $this->assertDatabaseHas('products', [
        'name' => 'New Product',
    ]);
});
```
Use factories, test happy path and validation failures, check database state."

**Why it works:** Shows test structure, assertions, and patterns to follow.

## Document Examples

When establishing new patterns, document them:

"Create a new service pattern for external API integrations. Here's the template:

```php
// app/Services/External/BaseApiClient.php
abstract class BaseApiClient
{
    protected string $baseUrl;
    protected int $timeout = 30;
    protected int $retries = 3;
    
    abstract protected function authenticate(): array;
    
    protected function request(string $method, string $endpoint, array $data = []): array
    {
        // Retry logic, error handling, logging
    }
}

// app/Services/External/StripeClient.php
class StripeClient extends BaseApiClient
{
    protected string $baseUrl = 'https://api.stripe.com/v1';
    
    protected function authenticate(): array
    {
        return ['Authorization' => 'Bearer ' . config('services.stripe.secret')];
    }
    
    public function createCharge(int $amount): array
    {
        return $this->request('POST', '/charges', ['amount' => $amount]);
    }
}
```

Use this pattern for all external API clients. Document in `docs/patterns/external-apis.md`."

**Why it works:** Creates a reusable pattern with documentation for future reference.

## Quick Reference

Make examples work for you:
- **Show existing code** - Reference actual files from your project
- **Demonstrate style** - Show naming, structure, patterns in action
- **Provide input/output** - Clarify transformations with concrete data
- **Use real code** - Snippets from your codebase, not generic examples
- **Document patterns** - Turn good examples into reusable templates

Examples > explanations. Show, don't just tell.

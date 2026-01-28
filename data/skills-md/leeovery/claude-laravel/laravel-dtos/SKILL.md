---
name: laravel-dtos
description: Data Transfer Objects using Spatie Laravel Data. Use when handling data transfer, API requests/responses, or when user mentions DTOs, data objects, Spatie Data, formatters, transformers, or structured data handling.
---

# Laravel DTOs

**Never pass multiple primitive values.** Always wrap data in Data objects.

**Related guides:**
- [dto-transformers.md](references/dto-transformers.md) - Transform external data into DTOs
- [test-factories.md](references/test-factories.md) - Create hydrated DTOs for tests

## Philosophy

DTOs provide:
- **Type safety** and IDE autocomplete
- **Clear contracts** between layers
- **Test factories** for easy test data generation
- **Validation** integration
- **Transformation** from requests to domain objects

## Spatie Laravel Data Package

Uses [Spatie Laravel Data](https://spatie.be/docs/laravel-data). Refer to official docs for package features. This guide covers project-specific patterns and preferences.

### Use `::from()` with Arrays

**Always prefer `::from()`** with arrays where keys match constructor property names. Let the package handle casting based on property types.

```php
// ✅ PREFERRED - Let package cast automatically
$data = CreateOrderData::from([
    'customerEmail' => $request->input('customer_email'),
    'deliveryDate' => $request->input('delivery_date'),  // String → CarbonImmutable
    'status' => $request->input('status'),               // String → OrderStatus enum
    'items' => $request->collect('items'),               // Array → Collection<OrderItemData>
]);

// ❌ AVOID - Manual casting in calling code
$data = new CreateOrderData(
    customerEmail: $request->input('customer_email'),
    deliveryDate: CarbonImmutable::parse($request->input('delivery_date')),
    status: OrderStatus::from($request->input('status')),
    items: OrderItemData::collect($request->input('items')),
);
```

**Why prefer `::from()`:**
- Package handles type casting automatically based on constructor property types
- Cleaner calling code without manual casting
- Consistent transformation behavior
- Leverages the full power of the package

**When `new` is acceptable:**
- In test factories where you control all values
- When values are already the correct type
- In formatters inside the DTO constructor

### Avoid Case Mapper Attributes

**Don't use `#[MapInputName]` or case mapper attributes.** Map field names explicitly in calling code.

```php
// ❌ AVOID - Case mapper attributes on the class
#[MapInputName(SnakeCaseMapper::class)]
class CreateOrderData extends Data
{
    public function __construct(
        public string $customerEmail,    // Auto-maps from 'customer_email'
    ) {}
}

// ✅ PREFERRED - Explicit mapping in calling code
CreateOrderData::from([
    'customerEmail' => $request->input('customer_email'),
]);
```

**Why avoid case mappers:**
- Explicit mapping is clearer and more maintainable
- Different API versions may have different field names
- Transformers provide a single place to see all mappings
- Avoids magic behavior that's hard to trace

### Date Casting is Automatic

The package automatically casts date strings to `Carbon` or `CarbonImmutable` based on property types. Configure the expected date format in the package config.

```php
// config/data.php
return [
    'date_format' => 'Y-m-d H:i:s',  // Or ISO 8601: 'Y-m-d\TH:i:s.u\Z'
];
```

```php
class OrderData extends Data
{
    public function __construct(
        public CarbonImmutable $createdAt,   // Automatically cast from string
        public ?CarbonImmutable $shippedAt,  // Nullable dates work too
    ) {}
}

// ✅ Just pass the string - package handles casting
$data = OrderData::from([
    'createdAt' => '2024-01-15 10:30:00',
    'shippedAt' => null,
]);
```

## Basic Structure

```php
<?php

declare(strict_types=1);

namespace App\Data;

use App\Enums\OrderStatus;
use Carbon\CarbonImmutable;
use Illuminate\Support\Collection;

/**
 * @see \Database\Factories\Data\CreateOrderDataFactory
 */
class CreateOrderData extends Data
{
    public function __construct(
        public string $customerEmail,
        public ?string $notes,
        public ?CarbonImmutable $deliveryDate,
        public OrderStatus $status,
        /** @var Collection<int, OrderItemData> */
        public Collection $items,
        public ShippingAddressData $shippingAddress,
        public BillingAddressData $billingAddress,
    ) {
        // Apply formatters in constructor
        $this->customerEmail = EmailFormatter::format($this->customerEmail);
    }
}
```

## Key Patterns

### Constructor Property Promotion

**Always use promoted properties:**

```php
public function __construct(
    public string $name,
    public ?string $description,
    public bool $active = true,
) {}
```

**Not:**
```php
public string $name;
public ?string $description;

public function __construct(string $name, ?string $description)
{
    $this->name = $name;
    $this->description = $description;
}
```

### Type Everything

```php
public string $email;                          // Required string
public ?string $phone;                         // Nullable string
public CarbonImmutable $createdAt;             // DateTime (immutable)
public OrderStatus $status;                    // Enum
public Collection $items;                      // Collection
public AddressData $address;                   // Nested DTO
```

### Collections with PHPDoc

```php
/** @var int[] */
public array $productIds;

/** @var Collection<int, OrderItemData> */
public Collection $items;
```

### Nested Data Objects

```php
class OrderData extends Data
{
    public function __construct(
        public CustomerData $customer,
        public ShippingAddressData $shipping,
        public BillingAddressData $billing,
        /** @var Collection<int, OrderItemData> */
        public Collection $items,
    ) {}
}
```

### Formatters

**Apply formatting in the constructor:**

```php
public function __construct(
    public string $email,
    public ?string $phone,
    public ?string $postcode,
) {
    $this->email = EmailFormatter::format($this->email);
    $this->phone = $this->phone ? PhoneFormatter::format($this->phone) : null;
    $this->postcode = $this->postcode ? PostcodeFormatter::format($this->postcode) : null;
}
```

**Example formatter** (`app/Data/Formatters/EmailFormatter.php`):

```php
<?php

declare(strict_types=1);

namespace App\Data\Formatters;

class EmailFormatter
{
    public static function format(string $email): string
    {
        return strtolower(trim($email));
    }
}
```

### Static Factory Methods on DTOs

For smaller applications or when starting out, add static `from*` methods directly on the DTO class. This provides factory-like behavior before complexity warrants separate transformers.

**Method naming:** `from{SourceType}` - e.g., `fromArray`, `fromRequest`, `fromModel`

```php
class OrderData extends Data
{
    public function __construct(
        public string $customerEmail,
        public ?string $notes,
        public OrderStatus $status,
        /** @var Collection<int, OrderItemData> */
        public Collection $items,
    ) {}

    public static function fromRequest(CreateOrderRequest $request): self
    {
        return self::from([
            'customerEmail' => $request->input('customer_email'),
            'notes' => $request->input('notes'),
            'status' => $request->input('status'),
            'items' => $request->input('items'),
        ]);
    }

    public static function fromModel(Order $order): self
    {
        return self::from([
            'customerEmail' => $order->customer_email,
            'notes' => $order->notes,
            'status' => $order->status,
            'items' => $order->items->toArray(),
        ]);
    }
}
```

**When to use static methods on DTO:**
- Smaller applications with fewer DTOs
- Simple transformations that don't need dedicated testing
- When mapping is tightly coupled to a single DTO

**When to use separate transformers:**
- Multiple external sources map to the same DTO
- Complex transformation logic requiring extensive testing
- Larger applications with clear separation of concerns

### Model Casts

**Cast model JSON columns to DTOs:**

```php
class Order extends Model
{
    protected function casts(): array
    {
        return [
            'metadata' => OrderMetadataData::class,
            'status' => OrderStatus::class,
        ];
    }
}
```

**Usage:**

```php
// Store
$order = Order::create([
    'metadata' => $metadataData,  // OrderMetadataData instance
]);

// Retrieve
$metadata = $order->metadata;  // Returns OrderMetadataData instance
```

## Naming Conventions

| Type | Pattern | Examples |
|------|---------|----------|
| Response DTOs | `{Entity}Data` | `OrderData`, `UserData`, `ProductData` |
| Request DTOs | `{Action}{Entity}Data` | `CreateOrderData`, `UpdateUserData` |
| Nested DTOs | `{Descriptor}{Entity}Data` | `ShippingAddressData`, `OrderMetadataData` |

## Directory Structure

```
app/Data/
├── CreateOrderData.php
├── UpdateOrderData.php
├── OrderData.php
├── Concerns/
│   └── HasTestFactory.php
├── Formatters/
│   ├── EmailFormatter.php
│   ├── PhoneFormatter.php
│   └── PostcodeFormatter.php
└── Transformers/
    ├── PaymentDataTransformer.php
    ├── Web/
    │   └── OrderDataTransformer.php
    └── Api/
        └── V1/
            └── OrderDataTransformer.php
```

## Usage in Controllers

**Controllers transform requests to DTOs via transformers:**

```php
<?php

declare(strict_types=1);

namespace App\Http\Web\Controllers;

use App\Actions\Order\CreateOrderAction;
use App\Data\Transformers\Web\OrderDataTransformer;
use App\Http\Web\Requests\CreateOrderRequest;
use App\Http\Web\Resources\OrderResource;

class OrderController extends Controller
{
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
}
```

## Usage in Actions

**Actions accept DTOs as parameters:**

```php
class CreateOrderAction
{
    public function __invoke(User $user, CreateOrderData $data): Order
    {
        return DB::transaction(function () use ($user, $data) {
            return $user->orders()->create([
                'customer_email' => $data->customerEmail,
                'notes' => $data->notes,
                'status' => $data->status,
            ]);
        });
    }
}
```

## Transformers

For complex transformations (external APIs, webhooks, field mappings), use dedicated transformer classes.

**[→ Complete guide: dto-transformers.md](references/dto-transformers.md)**

```php
// External system data
$data = PaymentDataTransformer::fromStripePaymentIntent($webhook['data']);

// Request with version-specific field names
$data = OrderDataTransformer::fromRequest($request);
```

**Hierarchy of preference:**
1. `Data::from($array)` - Simple cases, direct mapping
2. `Data::fromRequest()` - Static method on DTO for smaller apps
3. `Transformer::from*()` - Complex transformations, multiple sources

## Test Factories

Create hydrated DTOs for tests using the `HasTestFactory` trait.

**[→ Complete guide: test-factories.md](references/test-factories.md)**

**Link DTOs to factories with PHPDoc:**

```php
/**
 * @see \Database\Factories\Data\CreateOrderDataFactory
 * @method static CreateOrderDataFactory testFactory()
 */
class CreateOrderData extends Data
{
    // ...
}
```

**Usage:**

```php
$data = CreateOrderData::testFactory()->make();
$collection = OrderItemData::testFactory()->collect(count: 5);

// With overrides
$data = CreateOrderData::testFactory()->make([
    'customerEmail' => 'test@example.com',
]);
```

## Testing DTOs

```php
use App\Data\CreateOrderData;

it('can create DTO from array', function () {
    $data = CreateOrderData::from([
        'customerEmail' => 'test@example.com',
        'notes' => 'Test notes',
        'status' => 'pending',
    ]);

    expect($data)
        ->customerEmail->toBe('test@example.com')
        ->notes->toBe('Test notes');
});

it('formats email in constructor', function () {
    $data = new CreateOrderData(
        customerEmail: '  TEST@EXAMPLE.COM  ',
        notes: null,
        status: OrderStatus::Pending,
    );

    expect($data->customerEmail)->toBe('test@example.com');
});
```

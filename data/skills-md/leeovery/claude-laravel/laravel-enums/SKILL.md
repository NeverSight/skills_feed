---
name: laravel-enums
description: Backed enums with labels and business logic. Use when working with enums, status values, fixed sets of options, or when user mentions enums, backed enums, enum cases, status enums.
---

# Laravel Enums

Enums provide type-safe, finite sets of values.

**Related guides:**
- [State Machines](../laravel-state-machines/SKILL.md) - For complex state transitions
- [Models](../laravel-models/SKILL.md) - Model casts to enums
- [DTOs](../laravel-dtos/SKILL.md) - DTOs with enum properties
- [form-requests.md](../laravel-validation/references/form-requests.md) - Enum validation

## Always Use Backed Enums

**Always use backed enums** (string or int):

```php
<?php

declare(strict_types=1);

namespace App\Enums;

enum OrderStatus: string
{
    case Pending = 'pending';
    case Processing = 'processing';
    case Completed = 'completed';
    case Cancelled = 'cancelled';
}
```

## Enum with Traits

Add functionality with traits:

```php
<?php

declare(strict_types=1);

namespace App\Enums;

use Henzeb\Enumhancer\Concerns\Comparison;
use Henzeb\Enumhancer\Concerns\Dropdown;

enum OrderStatus: string
{
    use Comparison, Dropdown;

    case Pending = 'pending';
    case Processing = 'processing';
    case Completed = 'completed';
    case Cancelled = 'cancelled';
}
```

## Enum with Labels

```php
<?php

declare(strict_types=1);

namespace App\Enums;

use App\Enums\Attributes\Label;
use App\Enums\Concerns\HasLabel;

enum PaymentMethod: string
{
    use HasLabel;

    #[Label('Credit Card')]
    case CreditCard = 'credit-card';

    #[Label('Bank Transfer')]
    case BankTransfer = 'bank-transfer';

    #[Label('PayPal')]
    case PayPal = 'paypal';
}
```

## Custom Enum Attributes

```php
<?php

declare(strict_types=1);

namespace App\Enums\Attributes;

use Attribute;

#[Attribute(Attribute::TARGET_CLASS_CONSTANT)]
class Label
{
    public function __construct(public string $value) {}
}

#[Attribute(Attribute::TARGET_CLASS_CONSTANT)]
class Color
{
    public function __construct(public string $value) {}
}

#[Attribute(Attribute::TARGET_CLASS_CONSTANT)]
class Icon
{
    public function __construct(public string $value) {}
}
```

## Enum Concerns

```php
<?php

declare(strict_types=1);

namespace App\Enums\Concerns;

use App\Enums\Attributes\Label;
use Henzeb\Enumhancer\Concerns\Attributes;
use Henzeb\Enumhancer\Concerns\Dropdown;
use Henzeb\Enumhancer\Concerns\Labels;

trait HasLabel
{
    use Attributes, Dropdown, Labels;

    public static function labels(): array
    {
        return collect(self::cases())->mapWithKeys(fn ($enum) => [
            $enum->name => $enum->getLabel(),
        ])->toArray();
    }

    public function getLabel(): ?string
    {
        return $this->getAttribute(Label::class)?->value;
    }
}
```

## Business Logic in Enums

Enums can contain behavior:

```php
enum PaymentProvider: string
{
    case Stripe = 'stripe';
    case PayPal = 'paypal';
    case Square = 'square';

    public function processingFee(int $amount): int
    {
        return match ($this) {
            self::Stripe => (int) ($amount * 0.029 + 30),
            self::PayPal => (int) ($amount * 0.034 + 30),
            self::Square => (int) ($amount * 0.026 + 10),
        };
    }

    public function supportsRefunds(): bool
    {
        return match ($this) {
            self::Stripe, self::PayPal => true,
            self::Square => false,
        };
    }
}
```

## Usage in Models

```php
protected function casts(): array
{
    return [
        'status' => OrderStatus::class,
        'payment_method' => PaymentMethod::class,
    ];
}
```

## Usage in DTOs

```php
public function __construct(
    public OrderStatus $status,
    public PaymentMethod $paymentMethod,
) {}
```

## Usage in Validation

```php
use Illuminate\Validation\Rules\Enum;

'status' => [
    'required',
    'string',
    'bail',
    new Enum(OrderStatus::class),
],
```

## Common Patterns

### Comparison

```php
if ($order->status->is(OrderStatus::Completed)) {
    // ...
}

// With enumhancer Comparison trait
if ($order->status->isCompleted()) {
    // ...
}
```

### UI Attributes

```php
$status->getLabel();  // 'Completed'
PaymentMethod::dropdown();  // For select inputs
OrderStatus::labels();  // All labels as array
```

### Match Expressions

```php
$message = match ($order->status) {
    OrderStatus::Pending => 'Your order is pending',
    OrderStatus::Processing => 'We are processing your order',
    OrderStatus::Completed => 'Your order is complete',
    OrderStatus::Cancelled => 'Your order was cancelled',
};
```

## Queue Enum Example

```php
<?php

declare(strict_types=1);

namespace App\Enums;

enum Queue: string
{
    case Default = 'default';
    case Processing = 'processing';
    case Emails = 'emails';
    case Notifications = 'notifications';
}
```

**Usage in jobs:**

```php
public function __construct(public Order $order)
{
    $this->onQueue(Queue::Emails->value);
}
```

## Directory Structure

```
app/Enums/
├── OrderStatus.php
├── PaymentMethod.php
├── Queue.php
├── Attributes/
│   ├── Label.php
│   ├── Color.php
│   └── Icon.php
└── Concerns/
    └── HasLabel.php
```

## When to Use Enums vs State Machines

**Use Enums:**
- Simple status fields
- No transition logic
- No side effects

**Use State Machines:**
- Complex state transitions with rules
- State-specific behavior
- Transition side effects

See [State Machines](../laravel-state-machines/SKILL.md) for state machines.

## Summary

**Enums provide:**
- Type safety
- Finite value sets
- Business logic encapsulation
- UI helpers (labels, colors, icons)
- IDE autocomplete

**Always use backed enums** with string or int values.

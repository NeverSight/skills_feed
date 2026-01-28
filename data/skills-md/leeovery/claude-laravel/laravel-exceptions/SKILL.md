---
name: laravel-exceptions
description: Custom exceptions with static factories and HTTP responses. Use when working with error handling, custom exceptions, or when user mentions exceptions, custom exception, error handling, HTTP exceptions.
---

# Laravel Exceptions

Custom exceptions use **static factory methods** and implement `HttpExceptionInterface`.

**Related guides:**
- [Actions](../laravel-actions/SKILL.md) - Throwing exceptions in actions

## Structure

```php
<?php

declare(strict_types=1);

namespace App\Exceptions;

use App\Exceptions\Concerns\Httpable;
use App\Models\Order;
use Exception;
use Symfony\Component\HttpKernel\Exception\HttpExceptionInterface;

class OrderException extends Exception implements HttpExceptionInterface
{
    use Httpable;

    public static function notFound(string|int $orderId): self
    {
        return new self("Order {$orderId} not found.", 404);
    }

    public static function cannotCancelOrder(Order $order): self
    {
        return new self(
            "Order {$order->uuid} cannot be cancelled in its current state.",
            400
        );
    }

    public static function insufficientStock(string $productName): self
    {
        return new self(
            "Insufficient stock for product: {$productName}",
            422
        );
    }

    public static function paymentFailed(string $reason): self
    {
        return new self("Payment failed: {$reason}", 402);
    }
}
```

## Httpable Concern

**[View full implementation →](references/Httpable.php)**

## Usage

### Throwing Exceptions

```php
// In actions
throw OrderException::notFound($orderId);
throw OrderException::cannotCancelOrder($order);
throw OrderException::insufficientStock($product->name);
```

### With throw_unless/throw_if

```php
class CancelOrderAction
{
    public function __invoke(Order $order): Order
    {
        throw_unless(
            $order->canBeCancelled(),
            OrderException::cannotCancelOrder($order)
        );

        // Continue with cancellation
    }
}
```

### Guard Methods

```php
class ProcessOrderAction
{
    public function __invoke(Order $order): void
    {
        $this->guard($order);

        // Process order
    }

    private function guard(Order $order): void
    {
        throw_unless(
            $order->isPending(),
            OrderException::cannotProcessOrder($order)
        );

        throw_unless(
            $order->hasItems(),
            OrderException::orderHasNoItems($order)
        );
    }
}
```

## Key Patterns

### 1. Static Factory Methods

Named constructors for specific exceptions:

```php
public static function notFound(string|int $orderId): self
{
    return new self("Order {$orderId} not found.", 404);
}
```

### 2. HTTP Status Codes

Pass status as second constructor parameter:

```php
new self("Message", 404);  // Not Found
new self("Message", 400);  // Bad Request
new self("Message", 422);  // Unprocessable Entity
new self("Message", 403);  // Forbidden
```

### 3. Descriptive Messages

Include context in error messages:

```php
"Order {$order->uuid} cannot be cancelled"
"Insufficient stock for product: {$productName}"
```

### 4. HttpExceptionInterface

Implement interface for automatic HTTP error responses:

```php
class OrderException extends Exception implements HttpExceptionInterface
{
    use Httpable;
}
```

## Common HTTP Status Codes

- `400` - Bad Request (business rule violation)
- `402` - Payment Required
- `403` - Forbidden (authorization failed)
- `404` - Not Found
- `422` - Unprocessable Entity (validation failed)
- `500` - Internal Server Error

## Directory Structure

```
app/Exceptions/
├── OrderException.php
├── PaymentException.php
├── UserException.php
└── Concerns/
    └── Httpable.php
```

## Summary

**Exceptions should:**
- Use static factory methods
- Implement `HttpExceptionInterface`
- Include HTTP status codes
- Have descriptive messages with context
- Be named `{Entity}Exception`

**Use for business rule violations and error conditions.**

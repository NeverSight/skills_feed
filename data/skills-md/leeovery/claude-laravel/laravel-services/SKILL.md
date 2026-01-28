---
name: laravel-services
description: Service layer for external API integration using manager pattern and Saloon. Use when working with external APIs, third-party services, or when user mentions services, external API, Saloon, API integration, manager pattern.
---

# Laravel Services

External services use Laravel's **Manager pattern** with multiple drivers.

**Related guides:**
- [Actions](../laravel-actions/SKILL.md) - Actions use services
- [Packages](../laravel-packages/SKILL.md) - Saloon for HTTP clients
- [Testing](../laravel-testing/SKILL.md) - Testing with null drivers

## When to Use

**Use service layer when:**
- Integrating external APIs
- Multiple drivers for same service (email, payment, SMS)
- Need to swap implementations
- Want null driver for testing

## Structure

```
Services/
└── Payment/
    ├── PaymentManager.php          # Manager (extends Laravel Manager)
    ├── Connectors/
    │   └── StripeConnector.php     # Saloon HTTP connector
    ├── Contracts/
    │   └── PaymentDriver.php       # Driver interface
    ├── Drivers/
    │   ├── StripeDriver.php        # Stripe implementation
    │   ├── PayPalDriver.php        # PayPal implementation
    │   └── NullDriver.php          # For testing
    ├── Exceptions/
    │   └── PaymentException.php
    ├── Facades/
    │   └── Payment.php             # Facade
    └── Requests/
        └── Stripe/
            ├── CreatePaymentIntentRequest.php
            └── RefundPaymentRequest.php
```

## Manager Class

```php
<?php

declare(strict_types=1);

namespace App\Services\Payment;

use App\Services\Payment\Drivers\NullDriver;
use App\Services\Payment\Drivers\StripeDriver;
use Illuminate\Support\Manager;

class PaymentManager extends Manager
{
    public function getDefaultDriver(): string
    {
        return $this->config->get('payment.default');
    }

    public function createStripeDriver(): StripeDriver
    {
        return new StripeDriver(
            apiKey: $this->config->get('payment.drivers.stripe.api_key'),
            webhookSecret: $this->config->get('payment.drivers.stripe.webhook_secret'),
        );
    }

    public function createNullDriver(): NullDriver
    {
        return new NullDriver;
    }
}
```

## Driver Contract

```php
<?php

declare(strict_types=1);

namespace App\Services\Payment\Contracts;

use App\Data\PaymentIntentData;

interface PaymentDriver
{
    public function createPaymentIntent(int $amount, string $currency): PaymentIntentData;

    public function refundPayment(string $paymentIntentId, ?int $amount = null): bool;

    public function retrievePaymentIntent(string $paymentIntentId): PaymentIntentData;
}
```

## Driver Implementation

```php
<?php

declare(strict_types=1);

namespace App\Services\Payment\Drivers;

use App\Data\PaymentIntentData;
use App\Services\Payment\Connectors\StripeConnector;
use App\Services\Payment\Contracts\PaymentDriver;
use App\Services\Payment\Exceptions\PaymentException;
use App\Services\Payment\Requests\Stripe\CreatePaymentIntentRequest;
use Saloon\Http\Response;

class StripeDriver implements PaymentDriver
{
    private static ?StripeConnector $connector = null;

    public function __construct(
        private readonly string $apiKey,
        private readonly string $webhookSecret,
    ) {}

    public function createPaymentIntent(int $amount, string $currency): PaymentIntentData
    {
        $response = $this->sendRequest(
            new CreatePaymentIntentRequest($amount, $currency)
        );

        return PaymentIntentData::from($response->json());
    }

    public function refundPayment(string $paymentIntentId, ?int $amount = null): bool
    {
        // Implementation...
    }

    private function sendRequest(Request $request): Response
    {
        $response = $this->getConnector()->send($request);

        if ($response->failed()) {
            throw PaymentException::failedRequest($response);
        }

        return $response;
    }

    private function getConnector(): StripeConnector
    {
        if (static::$connector === null) {
            static::$connector = new StripeConnector($this->apiKey);
        }

        return static::$connector;
    }
}
```

## Saloon Connector

```php
<?php

declare(strict_types=1);

namespace App\Services\Payment\Connectors;

use Saloon\Http\Connector;

class StripeConnector extends Connector
{
    public function __construct(private readonly string $apiKey) {}

    public function resolveBaseUrl(): string
    {
        return 'https://api.stripe.com';
    }

    protected function defaultHeaders(): array
    {
        return [
            'Authorization' => "Bearer {$this->apiKey}",
            'Content-Type' => 'application/json',
        ];
    }
}
```

## Saloon Request

```php
<?php

declare(strict_types=1);

namespace App\Services\Payment\Requests\Stripe;

use Saloon\Contracts\Body\HasBody;
use Saloon\Enums\Method;
use Saloon\Http\Request;
use Saloon\Traits\Body\HasJsonBody;

class CreatePaymentIntentRequest extends Request implements HasBody
{
    use HasJsonBody;

    protected Method $method = Method::POST;

    public function __construct(
        private readonly int $amount,
        private readonly string $currency,
    ) {}

    public function resolveEndpoint(): string
    {
        return '/v1/payment_intents';
    }

    protected function defaultBody(): array
    {
        return [
            'amount' => $this->amount,
            'currency' => $this->currency,
        ];
    }
}
```

## Facade

```php
<?php

declare(strict_types=1);

namespace App\Services\Payment\Facades;

use App\Data\PaymentIntentData;
use Illuminate\Support\Facades\Facade;

/**
 * @method static PaymentIntentData createPaymentIntent(int $amount, string $currency)
 * @method static bool refundPayment(string $paymentIntentId, ?int $amount = null)
 * @method static PaymentIntentData retrievePaymentIntent(string $paymentIntentId)
 *
 * @see \App\Services\Payment\PaymentManager
 */
class Payment extends Facade
{
    protected static function getFacadeAccessor(): string
    {
        return \App\Services\Payment\PaymentManager::class;
    }
}
```

## Usage

```php
use App\Services\Payment\Facades\Payment;

// Use default driver
$paymentIntent = Payment::createPaymentIntent(
    amount: 10000,  // $100.00 in cents
    currency: 'usd'
);

// Refund payment
Payment::refundPayment($paymentIntent->id);

// Use specific driver
Payment::driver('stripe')->createPaymentIntent(10000, 'usd');
Payment::driver('paypal')->createPaymentIntent(10000, 'usd');

// Use in actions
class ProcessPaymentAction
{
    public function __invoke(Order $order, PaymentData $data): Payment
    {
        $paymentIntent = Payment::createPaymentIntent(
            amount: $order->total,
            currency: 'usd'
        );

        // ...
    }
}
```

## Null Driver for Testing

```php
<?php

declare(strict_types=1);

namespace App\Services\Payment\Drivers;

use App\Data\PaymentIntentData;
use App\Services\Payment\Contracts\PaymentDriver;

class NullDriver implements PaymentDriver
{
    public function createPaymentIntent(int $amount, string $currency): PaymentIntentData
    {
        return PaymentIntentData::from([
            'id' => 'pi_test_' . uniqid(),
            'amount' => $amount,
            'currency' => $currency,
            'status' => 'succeeded',
        ]);
    }

    public function refundPayment(string $paymentIntentId, ?int $amount = null): bool
    {
        return true;
    }

    public function retrievePaymentIntent(string $paymentIntentId): PaymentIntentData
    {
        return PaymentIntentData::from([
            'id' => $paymentIntentId,
            'status' => 'succeeded',
        ]);
    }
}
```

## Summary

**Service layer provides:**
- Manager pattern for multiple drivers
- Saloon for HTTP requests
- Null drivers for testing
- Clean abstraction over external services
- Swappable implementations

**Use for external API integrations only.**

---
name: payram-checkout-integration
description: Integrate PayRam checkout flow into web applications. Generate payment links, embed payment pages, handle redirects, and process payment confirmations. Supports Express, Next.js, FastAPI, Laravel, Gin, Spring Boot. Use when adding crypto checkout to e-commerce, building payment forms, implementing deposit flows, or creating hosted payment pages for crypto acceptance.
---

# PayRam Checkout Integration

> **First time with PayRam?** See [`payram-setup`](https://github.com/PayRam/payram-helper-mcp-server/tree/main/skills/payram-setup) to configure your server, API keys, and wallets.

Implement payment acceptance flows using PayRam's API. Create payments, redirect users, and confirm transactions.

## Payment Flow Overview

```
1. Your Backend → POST /api/v1/payment → PayRam
2. PayRam returns { url, reference_id, host }
3. Redirect user to payment URL
4. User selects chain/token, sends payment
5. PayRam confirms on-chain → webhook to your backend
6. Your backend fulfills order
```

## Payment States

Payments transition through these states:

- `OPEN` — Payment created, awaiting customer action
- `FILLED` — Customer sent exact amount, payment confirmed
- `PARTIALLY_FILLED` — Partial payment received (less than requested)
- `OVER_FILLED` — Overpayment received (more than requested)
- `CANCELLED` — Payment manually cancelled
- `UNDEFINED` — Unknown status (fallback)

## SDK Integration (Node.js/TypeScript)

### Install SDK

```bash
npm install payram dotenv
```

### Create Payment with SDK

```typescript
import { Payram, InitiatePaymentRequest, InitiatePaymentResponse, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
  config: {
    timeoutMs: 10_000,
    maxRetries: 2,
    retryPolicy: 'safe',
    allowInsecureHttp: false,
  },
});

export async function createCheckout(
  payload: InitiatePaymentRequest,
): Promise<InitiatePaymentResponse> {
  try {
    const checkout = await payram.payments.initiatePayment(payload);
    console.log('Redirect customer to:', checkout.url);
    console.log('Payment reference:', checkout.reference_id);
    return checkout;
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        requestId: error.requestId,
        retryable: error.isRetryable,
      });
    }
    throw error;
  }
}

// Example usage
await createCheckout({
  customerEmail: 'customer@example.com',
  customerId: 'cust_123',
  amountInUSD: 49.99,
});
```

**Required Fields:**

- `customerEmail`: Customer's email address
- `customerId`: Your internal customer identifier
- `amountInUSD`: Payment amount in USD

**Optional Fields:**

- `settlementCurrency`: Currency for settlement (default: USD)
- `memo`: Internal reference or description
- `redirectUrl`: Custom URL to redirect after payment

### Check Payment Status with SDK

```typescript
import { Payram, PaymentRequestData, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function getPaymentStatus(referenceId: string): Promise<PaymentRequestData> {
  try {
    const payment = await payram.payments.getPaymentRequest(referenceId);
    console.log('Latest payment state:', payment.paymentState);
    console.log('Amount paid:', payment.amountPaid);
    console.log('Transaction hash:', payment.transactionHash);
    return payment;
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        errorCode: error.error,
        requestId: error.requestId,
      });
    }
    throw error;
  }
}
```

## HTTP Integration (Python, Go, PHP, Java)

### API Endpoint

```
POST https://your-payram-server:8080/api/v1/payment
Header: API-Key: your-api-key
Content-Type: application/json
```

**Critical:** PayRam uses `API-Key` header, NOT `Authorization: Bearer`.

**Request Body:**

```json
{
  "customerEmail": "customer@example.com",
  "customerId": "user_12345",
  "amountInUSD": 25
}
```

**Response:**

```json
{
  "host": "https://your-payram-server:8080",
  "reference_id": "c80f5363-0397-4761-aa1a-3155c3a21470",
  "url": "https://your-payram-server/payments?reference_id=..."
}
```

### Python (FastAPI)

```python
import httpx
import os
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

PAYRAM_BASE_URL = os.environ['PAYRAM_BASE_URL']
PAYRAM_API_KEY = os.environ['PAYRAM_API_KEY']

@router.post("/create-payment")
async def create_payment(email: str, user_id: str, amount: float):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{PAYRAM_BASE_URL}/api/v1/payment",
            json={"customerEmail": email, "customerId": user_id, "amountInUSD": amount},
            headers={"API-Key": PAYRAM_API_KEY}
        )
    return RedirectResponse(resp.json()["url"])
```

### Go (Gin)

```go
func CreatePayment(email, customerID string, amount float64) (*InitiatePaymentResponse, error) {
    body, _ := json.Marshal(map[string]interface{}{
        "customerEmail": email,
        "customerId":    customerID,
        "amountInUSD":   amount,
    })

    url := fmt.Sprintf("%s/api/v1/payment", os.Getenv("PAYRAM_BASE_URL"))
    req, _ := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(body))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("API-Key", os.Getenv("PAYRAM_API_KEY"))

    resp, err := http.DefaultClient.Do(req)
    // ... handle response
}
```

### PHP (Laravel)

```php
$ch = curl_init(getenv('PAYRAM_BASE_URL') . '/api/v1/payment');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'API-Key: ' . getenv('PAYRAM_API_KEY'),
    ],
    CURLOPT_POSTFIELDS => json_encode($payload),
    CURLOPT_RETURNTRANSFER => true,
]);
```

### Java (Spring Boot)

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(baseUrl + "/api/v1/payment"))
    .header("Content-Type", "application/json")
    .header("API-Key", apiKey)
    .POST(HttpRequest.BodyPublishers.ofString(payload))
    .build();
```

## Framework Route Examples

### Express.js Route

```typescript
import { Router } from 'express';
import { Payram, InitiatePaymentRequest, isPayramSDKError } from 'payram';

const router = Router();
const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

router.post('/api/payments/payram', async (req, res) => {
  const payload = req.body as Partial<InitiatePaymentRequest>;

  if (!payload?.customerEmail || !payload.customerId || typeof payload.amountInUSD !== 'number') {
    return res.status(400).json({ error: 'MISSING_REQUIRED_FIELDS' });
  }

  try {
    const checkout = await payram.payments.initiatePayment({
      customerEmail: payload.customerEmail,
      customerId: payload.customerId,
      amountInUSD: payload.amountInUSD,
    });
    return res.status(201).json({
      referenceId: checkout.reference_id,
      checkoutUrl: checkout.url,
    });
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', { status: error.status, requestId: error.requestId });
    }
    return res.status(502).json({ error: 'PAYRAM_CREATE_PAYMENT_FAILED' });
  }
});
```

### Next.js App Router

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Payram, InitiatePaymentRequest, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function POST(request: NextRequest) {
  const payload = (await request.json()) as Partial<InitiatePaymentRequest>;

  if (!payload?.customerEmail || !payload.customerId || typeof payload.amountInUSD !== 'number') {
    return NextResponse.json({ error: 'MISSING_REQUIRED_FIELDS' }, { status: 400 });
  }

  try {
    const checkout = await payram.payments.initiatePayment({
      customerEmail: payload.customerEmail,
      customerId: payload.customerId,
      amountInUSD: payload.amountInUSD,
    });
    return NextResponse.json({
      referenceId: checkout.reference_id,
      checkoutUrl: checkout.url,
    });
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', { status: error.status, requestId: error.requestId });
    }
    return NextResponse.json({ error: 'PAYRAM_CREATE_PAYMENT_FAILED' }, { status: 502 });
  }
}
```

## Status Polling Pattern

```typescript
async function pollPaymentStatus(referenceId: string, maxAttempts = 10) {
  for (let i = 0; i < maxAttempts; i++) {
    const payment = await getPaymentStatus(referenceId);

    if (payment.paymentState === 'FILLED' || payment.paymentState === 'OVER_FILLED') {
      return payment;
    }

    if (payment.paymentState === 'CANCELLED') {
      throw new Error(`Payment ${payment.paymentState.toLowerCase()}`);
    }

    if (payment.paymentState === 'UNDEFINED') {
      throw new Error('Payment status undefined');
    }

    await new Promise((resolve) => setTimeout(resolve, Math.min(1000 * Math.pow(2, i), 30000)));
  }

  throw new Error('Payment status check timeout');
}
```

## Database Schema

```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    payram_reference_id VARCHAR(255) UNIQUE NOT NULL,
    amount_usd DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'OPEN',
    checkout_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_payram_reference ON payments(payram_reference_id);
CREATE INDEX idx_customer_id ON payments(customer_id);
```

## MCP Server Code Generation

Use the PayRam MCP server to generate framework-specific code:

| Framework               | MCP Tool                        |
| ----------------------- | ------------------------------- |
| JavaScript SDK          | `generate_payment_sdk_snippet`  |
| Raw HTTP (any language) | `generate_payment_http_snippet` |
| Express.js              | `snippet_express_payment_route` |
| Next.js App Router      | `snippet_nextjs_payment_route`  |
| FastAPI                 | `snippet_fastapi_payment_route` |
| Gin (Go)                | `snippet_gin_payment_route`     |
| Laravel                 | `snippet_laravel_payment_route` |
| Spring Boot             | `snippet_spring_payment_route`  |

## Environment Configuration

```bash
# .env
PAYRAM_BASE_URL=https://your-payram-server:8080
PAYRAM_API_KEY=your-api-key-here
```

Use `generate_env_template` MCP tool to scaffold this.

## Error Handling

| HTTP Code | Meaning            | Action                                       |
| --------- | ------------------ | -------------------------------------------- |
| 200/201   | Payment created    | Redirect to URL                              |
| 401       | Invalid API key    | Check `API-Key` header (NOT `Authorization`) |
| 400       | Invalid request    | Check required fields, amount > 0            |
| 404       | Merchant not found | Verify `PAYRAM_BASE_URL`                     |
| 500       | Server error       | Retry with backoff                           |

## All PayRam Skills

| Skill                                | What it covers                                                            |
| ------------------------------------ | ------------------------------------------------------------------------- |
| `payram-setup`                       | Server config, API keys, wallet setup, connectivity test                  |
| `payram-headless-setup`              | Headless CLI-only deployment for AI agents, no web UI                     |
| `payram-analytics`                   | Analytics dashboards, reports, and payment insights via MCP tools         |
| `payram-crypto-payments`             | Architecture overview, why PayRam, MCP tools                              |
| `payram-payment-integration`         | Quick-start payment integration guide                                     |
| `payram-self-hosted-payment-gateway` | Deploy and own your payment infrastructure                                |
| `payram-checkout-integration`        | Checkout flow with SDK + HTTP for 6 frameworks                            |
| `payram-webhook-integration`         | Webhook handlers for Express, Next.js, FastAPI, Gin, Laravel, Spring Boot |
| `payram-stablecoin-payments`         | USDT/USDC acceptance across EVM chains and Tron                           |
| `payram-bitcoin-payments`            | BTC with HD wallet derivation and mobile signing                          |
| `payram-payouts`                     | Send crypto payouts and manage referral programs                          |
| `payram-no-kyc-crypto-payments`      | No-KYC, no-signup, permissionless payment acceptance                      |

## Support

Need help? Message the PayRam team on Telegram: [@PayRamChat](https://t.me/PayRamChat)

- Website: https://payram.com
- GitHub: https://github.com/PayRam
- MCP Server: https://github.com/PayRam/payram-helper-mcp-server

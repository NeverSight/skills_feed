---
name: payram-webhook-integration
description: Integrate PayRam webhook handlers for real-time payment and payout event notifications. Self-hosted, no-KYC crypto payment gateway webhooks. Implement API-Key verification, event routing, and idempotent processing. Generate handlers for Express, Next.js, FastAPI, Gin, Laravel, Spring Boot. Use when setting up payment confirmation callbacks, handling payout status updates, building event-driven payment flows, or integrating PayRam events into existing systems.
---

# PayRam Webhook Setup

> **First time with PayRam?** See [`payram-setup`](https://github.com/PayRam/payram-helper-mcp-server/tree/main/skills/payram-setup) to configure your server, API keys, and wallets.

Receive real-time notifications when payments confirm, fail, or payouts complete. Webhooks eliminate polling and enable event-driven architectures.

## Webhook Flow

```text
1. Payment status changes on-chain
2. PayRam sends POST to your webhook URL
3. Your handler verifies API-Key header
4. Process event (fulfill order, update DB)
5. Return 200 OK
```

## Configuring Webhooks in PayRam

1. Navigate to **Settings → Webhooks** in PayRam dashboard
2. Add your endpoint URL: `https://your-app.com/api/payram/webhook`
3. Copy the shared webhook secret
4. Store secret as `PAYRAM_WEBHOOK_SECRET` in your `.env`

## Webhook Payload

PayRam sends webhook requests with an `API-Key` header for verification:

```http
POST https://your-domain.com/api/payram/webhook
Content-Type: application/json
API-Key: your-webhook-secret

{
  "reference_id": "ref_abc123",
  "invoice_id": "inv_xyz456",
  "customer_id": "cust_123",
  "customer_email": "customer@example.com",
  "status": "FILLED",
  "amount": 49.99,
  "filled_amount_in_usd": 49.99,
  "currency": "USD"
}
```

**Critical:** Verify the `API-Key` header matches your stored `PAYRAM_WEBHOOK_SECRET` before processing.

## Payment Status Events

| Status | Meaning |
|--------|---------|
| `OPEN` | Payment created, awaiting customer action |
| `FILLED` | Payment completed successfully (exact amount paid) |
| `PARTIALLY_FILLED` | Partial payment received (less than requested) |
| `OVER_FILLED` | Overpayment received (more than requested) |
| `CANCELLED` | Payment cancelled by customer or merchant |
| `UNDEFINED` | Unknown status (future compatibility) |

## TypeScript Type Definitions

```typescript
export type PayramWebhookStatus =
  | 'OPEN'
  | 'CANCELLED'
  | 'FILLED'
  | 'PARTIALLY_FILLED'
  | 'OVER_FILLED'
  | 'UNDEFINED';

export interface PayramWebhookPayload {
  reference_id: string;
  invoice_id?: string;
  customer_id?: string;
  customer_email?: string;
  status: PayramWebhookStatus;
  amount?: number;
  filled_amount_in_usd?: number;
  currency?: string;
  [key: string]: unknown;
}
```

## Event Router

```typescript
export async function handlePayramEvent(payload: PayramWebhookPayload) {
  switch (payload.status) {
    case 'FILLED':
      // Mark order as paid, deliver goods, send confirmation
      await fulfillOrder(payload.reference_id);
      break;
    case 'PARTIALLY_FILLED':
      // Update outstanding balance, notify finance team
      break;
    case 'OVER_FILLED':
      // Queue manual review or process refund
      break;
    case 'CANCELLED':
      // Release inventory, notify customer
      break;
    case 'OPEN':
      // Record payment acknowledgement
      break;
    default:
      // Log for investigation
      console.warn('Unknown status:', payload.status);
      break;
  }
}
```

## Framework Handlers

### Express.js

```typescript
import express, { Request, Response } from 'express';
import crypto from 'crypto';

const router = express.Router();
router.use(express.json());

router.post('/api/payram/webhook', async (req: Request, res: Response) => {
  const sharedSecret = process.env.PAYRAM_WEBHOOK_SECRET;
  if (!sharedSecret) {
    return res.status(500).json({ error: 'webhook_not_configured' });
  }

  // Validate API-Key header (timing-safe comparison)
  const incomingKey = req.get('API-Key');
  if (!incomingKey) {
    return res.status(401).json({ error: 'invalid-webhook-key' });
  }
  
  const isValid = crypto.timingSafeEqual(
    Buffer.from(incomingKey),
    Buffer.from(sharedSecret)
  );
  if (!isValid) {
    return res.status(401).json({ error: 'invalid-webhook-key' });
  }

  const payload = req.body;
  if (!payload?.reference_id || !payload?.status) {
    return res.status(400).json({ error: 'invalid-webhook-payload' });
  }

  try {
    await handlePayramEvent(payload);
    return res.json({ message: 'Webhook received successfully' });
  } catch (error) {
    console.error('Webhook handler error:', error);
    return res.status(500).json({ error: 'webhook_handler_error' });
  }
});
```

### Next.js App Router

```typescript
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

export async function POST(request: NextRequest) {
  const sharedSecret = process.env.PAYRAM_WEBHOOK_SECRET;
  if (!sharedSecret) {
    return NextResponse.json({ error: 'webhook_not_configured' }, { status: 500 });
  }

  const incomingKey = request.headers.get('API-Key');
  if (!incomingKey) {
    return NextResponse.json({ error: 'invalid-webhook-key' }, { status: 401 });
  }
  
  const isValid = crypto.timingSafeEqual(
    Buffer.from(incomingKey),
    Buffer.from(sharedSecret)
  );
  if (!isValid) {
    return NextResponse.json({ error: 'invalid-webhook-key' }, { status: 401 });
  }

  const payload = await request.json();
  if (!payload.reference_id || !payload.status) {
    return NextResponse.json({ error: 'invalid-webhook-payload' }, { status: 400 });
  }

  try {
    await handlePayramEvent(payload);
    return NextResponse.json({ message: 'Webhook received successfully' });
  } catch (error) {
    return NextResponse.json({ error: 'webhook_handler_error' }, { status: 500 });
  }
}
```

### FastAPI (Python)

```python
import os
import hmac
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

@app.post('/api/payram/webhook')
async def payram_webhook(request: Request):
    shared_secret = os.getenv('PAYRAM_WEBHOOK_SECRET')
    if not shared_secret:
        raise HTTPException(status_code=500, detail='webhook_not_configured')

    incoming_key = request.headers.get('API-Key')
    if not incoming_key:
        raise HTTPException(status_code=401, detail='invalid-webhook-key')
    
    # Timing-safe comparison
    if not hmac.compare_digest(incoming_key, shared_secret):
        raise HTTPException(status_code=401, detail='invalid-webhook-key')

    payload = await request.json()
    if 'reference_id' not in payload or 'status' not in payload:
        raise HTTPException(status_code=400, detail='invalid-webhook-payload')

    await handle_payram_event(payload)
    return {'message': 'Webhook received successfully'}
```

### Gin (Go)

```go
import (
    "crypto/subtle"
    "net/http"
    "os"
    
    "github.com/gin-gonic/gin"
)

func handlePayramWebhook(c *gin.Context) {
    sharedSecret := os.Getenv("PAYRAM_WEBHOOK_SECRET")
    if sharedSecret == "" {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "webhook_not_configured"})
        return
    }

    incomingKey := c.GetHeader("API-Key")
    if incomingKey == "" {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid-webhook-key"})
        return
    }
    
    // Timing-safe comparison
    if subtle.ConstantTimeCompare([]byte(incomingKey), []byte(sharedSecret)) != 1 {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid-webhook-key"})
        return
    }

    var payload PayramWebhookPayload
    if err := c.ShouldBindJSON(&payload); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid-json-payload"})
        return
    }

    if err := handlePayramEvent(payload); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "webhook_handler_error"})
        return
    }

    c.JSON(http.StatusOK, gin.H{"message": "Webhook received successfully"})
}
```

### Laravel (PHP)

```php
class PayramWebhookController extends Controller
{
    public function handle(Request $request)
    {
        $sharedSecret = env('PAYRAM_WEBHOOK_SECRET');
        if (!$sharedSecret) {
            return response()->json(['error' => 'webhook_not_configured'], 500);
        }

        $incomingKey = $request->header('API-Key');
        if (!$incomingKey) {
            return response()->json(['error' => 'invalid-webhook-key'], 401);
        }
        
        // Timing-safe comparison
        if (!hash_equals($sharedSecret, $incomingKey)) {
            return response()->json(['error' => 'invalid-webhook-key'], 401);
        }

        $payload = $request->json()->all();
        if (empty($payload['reference_id']) || empty($payload['status'])) {
            return response()->json(['error' => 'invalid-webhook-payload'], 400);
        }

        $this->router->handle($payload);
        return response()->json(['message' => 'Webhook received successfully']);
    }
}
```

### Spring Boot (Java)

```java
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;

@PostMapping("/webhook")
public ResponseEntity<?> handleWebhook(
        @RequestBody Map<String, Object> payload,
        @RequestHeader(value = "API-Key", required = false) String apiKey) {

    String sharedSecret = System.getenv("PAYRAM_WEBHOOK_SECRET");
    if (sharedSecret == null || sharedSecret.isBlank()) {
        return ResponseEntity.status(500).body(Map.of("error", "webhook_not_configured"));
    }

    if (apiKey == null || apiKey.isBlank()) {
        return ResponseEntity.status(401).body(Map.of("error", "invalid-webhook-key"));
    }
    
    // Timing-safe comparison
    boolean isValid = MessageDigest.isEqual(
        apiKey.getBytes(StandardCharsets.UTF_8),
        sharedSecret.getBytes(StandardCharsets.UTF_8)
    );
    if (!isValid) {
        return ResponseEntity.status(401).body(Map.of("error", "invalid-webhook-key"));
    }

    if (!payload.containsKey("reference_id") || !payload.containsKey("status")) {
        return ResponseEntity.status(400).body(Map.of("error", "invalid-webhook-payload"));
    }

    router.handle(payload);
    return ResponseEntity.ok(Map.of("message", "Webhook received successfully"));
}
```

## Best Practices

**Idempotency**: Handle duplicate deliveries gracefully — check if already processed before fulfilling:

```typescript
async function handleFilledPayment(payload: PayramWebhookPayload) {
  const existing = await db.payments.findUnique({
    where: { payramReferenceId: payload.reference_id },
  });
  if (existing && existing.status === 'completed') {
    return; // Already processed, safe to skip
  }
  await db.payments.update({
    where: { payramReferenceId: payload.reference_id },
    data: { status: 'completed', paidAt: new Date() },
  });
  await fulfillOrder(payload.customer_id, payload.reference_id);
}
```

**Quick Response**: Return 200 immediately, process asynchronously. PayRam retries on timeout.

**Retry Handling**: If you return 5xx, PayRam retries with exponential backoff. Return 200 for permanent failures to prevent retries.

**Database Transactions**: Use transactions for critical operations to ensure consistency.

## Testing Webhooks

### cURL Test

```bash
curl -X POST http://localhost:3000/api/payram/webhook \
  -H "Content-Type: application/json" \
  -H "API-Key: $PAYRAM_WEBHOOK_SECRET" \
  -d '{
    "reference_id": "ref_test_001",
    "status": "FILLED",
    "customer_id": "cust_123",
    "amount": 49.99,
    "filled_amount_in_usd": 49.99,
    "currency": "USD"
  }'
```

### MCP Server Tools

| Tool | Purpose |
|------|---------|
| `generate_webhook_handler` | Framework-specific handler code |
| `generate_webhook_event_router` | Fan-out router for multiple event types |
| `generate_mock_webhook_event` | Test payloads for each event type |

## Environment Variables

```bash
PAYRAM_WEBHOOK_SECRET=your-webhook-secret-from-dashboard
```

## All PayRam Skills

| Skill | What it covers |
|-------|---------------|
| `payram-setup` | Server config, API keys, wallet setup, connectivity test |
| `payram-crypto-payments` | Architecture overview, why PayRam, MCP tools |
| `payram-payment-integration` | Quick-start payment integration guide |
| `payram-self-hosted-payment-gateway` | Deploy and own your payment infrastructure |
| `payram-checkout-integration` | Checkout flow with SDK + HTTP for 6 frameworks |
| `payram-webhook-integration` | Webhook handlers for Express, Next.js, FastAPI, Gin, Laravel, Spring Boot |
| `payram-stablecoin-payments` | USDT/USDC acceptance across EVM chains and Tron |
| `payram-bitcoin-payments` | BTC with HD wallet derivation and mobile signing |
| `payram-payouts` | Send crypto payouts and manage referral programs |
| `payram-no-kyc-crypto-payments` | No-KYC, no-signup, permissionless payment acceptance |

## Support

Need help? Message the PayRam team on Telegram: [@PayRamChat](https://t.me/PayRamChat)

- Website: https://payram.com
- GitHub: https://github.com/PayRam
- MCP Server: https://github.com/PayRam/payram-helper-mcp-server

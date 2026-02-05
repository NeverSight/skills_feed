---
name: openpay-mexico
description: OpenPay payment integration for Mexican market with card, SPEI, and OXXO support. Use when integrating Mexican payment processing, adding OpenPay to Next.js/React apps, implementing SPEI/OXXO/card payments, or handling payment webhooks. Covers REST API setup (no SDK), webhook verification, and security patterns.
---

# OpenPay Mexico Integration

Integrate OpenPay payment processing for Mexican market with card, SPEI, and OXXO support.

## Contents

| Section                | Purpose                                |
| ---------------------- | -------------------------------------- |
| **Initial Setup**      | SDK warning, env vars, database schema |
| **API Client**         | REST API wrapper (no npm package)      |
| **Security Checklist** | Production readiness                   |
| **Testing**            | Sandbox test cards                     |

| Reference                                           | When to Load                         |
| --------------------------------------------------- | ------------------------------------ |
| [api-routes.md](references/api-routes.md)           | Building the payment charge endpoint |
| [webhook-handler.md](references/webhook-handler.md) | Implementing webhooks, ngrok setup   |
| [ui-components.md](references/ui-components.md)     | Building payment forms, OXXO voucher |

---

## Initial Setup

### 1. SDK Warning ⚠️

> **DO NOT install the `openpay` npm package.** It has known security vulnerabilities and uses an outdated callback-based API.

Instead, use **OpenPay's REST API directly** with native `fetch`. This approach is:

- More secure (no vulnerable dependencies)
- Simpler (no promisification needed)
- Smaller bundle size
- Fully typed with your own interfaces

### 2. Environment Variables

Add to `.env.local`:

```bash
OPENPAY_MERCHANT_ID=your_merchant_id
OPENPAY_PRIVATE_KEY=your_private_key
OPENPAY_PUBLIC_KEY=your_public_key
OPENPAY_WEBHOOK_SECRET=your_webhook_secret
OPENPAY_SANDBOX=true  # false for production
```

### 3. Database Schema

Add payment fields to bookings table:

```sql
-- Payment tracking
ALTER TABLE bookings ADD COLUMN payment_id TEXT;
ALTER TABLE bookings ADD COLUMN payment_method TEXT CHECK (payment_method IN ('card', 'spei', 'oxxo'));

-- Store all money in cents (BIGINT) to avoid floating-point issues
ALTER TABLE bookings ADD COLUMN guest_total_cents BIGINT;
ALTER TABLE bookings ADD COLUMN platform_fee_cents BIGINT;

-- SPEI-specific fields
ALTER TABLE bookings ADD COLUMN spei_clabe TEXT;
ALTER TABLE bookings ADD COLUMN spei_reference TEXT;

-- OXXO-specific fields
ALTER TABLE bookings ADD COLUMN oxxo_barcode_url TEXT;
ALTER TABLE bookings ADD COLUMN oxxo_reference TEXT;
ALTER TABLE bookings ADD COLUMN oxxo_expires_at TIMESTAMP WITH TIME ZONE;
```

---

## API Client (No SDK)

Create `src/lib/openpay.ts` using direct REST API calls:

```typescript
// OpenPay REST API client - no external dependencies
const OPENPAY_BASE_URL =
  process.env.OPENPAY_SANDBOX === "true"
    ? "https://sandbox-api.openpay.mx/v1"
    : "https://api.openpay.mx/v1";

const MERCHANT_ID = process.env.OPENPAY_MERCHANT_ID!;
const PRIVATE_KEY = process.env.OPENPAY_PRIVATE_KEY!;

// Types
export interface OpenPayCharge {
  id: string;
  amount: number;
  status: "in_progress" | "completed" | "failed" | "charge_pending";
  method: "card" | "bank_account" | "store";
  order_id: string;
  payment_method?: {
    reference?: string;
    clabe?: string;
    barcode_url?: string;
  };
  due_date?: string;
  error_message?: string;
}

// Base API call
async function openpayRequest<T>(endpoint: string, body: object): Promise<T> {
  const auth = Buffer.from(`${PRIVATE_KEY}:`).toString("base64");

  const response = await fetch(
    `${OPENPAY_BASE_URL}/${MERCHANT_ID}${endpoint}`,
    {
      method: "POST",
      headers: {
        Authorization: `Basic ${auth}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    },
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.description || "OpenPay request failed");
  }

  return response.json();
}

// Card charge (immediate confirmation)
export const createCardCharge = (
  tokenId: string,
  amountCents: number,
  description: string,
  orderId: string,
  deviceSessionId: string,
): Promise<OpenPayCharge> => {
  return openpayRequest<OpenPayCharge>("/charges", {
    method: "card",
    source_id: tokenId,
    amount: amountCents / 100,
    description,
    order_id: orderId,
    device_session_id: deviceSessionId,
    currency: "MXN",
    capture: true,
  });
};

// SPEI charge (async confirmation via webhook)
export const createSpeiCharge = (
  amountCents: number,
  description: string,
  orderId: string,
): Promise<OpenPayCharge> => {
  return openpayRequest<OpenPayCharge>("/charges", {
    method: "bank_account",
    amount: amountCents / 100,
    description,
    order_id: orderId,
    currency: "MXN",
  });
};

// OXXO charge (async confirmation via webhook)
export const createOxxoCharge = (
  amountCents: number,
  description: string,
  orderId: string,
  expirationDate: Date,
): Promise<OpenPayCharge> => {
  return openpayRequest<OpenPayCharge>("/charges", {
    method: "store",
    amount: amountCents / 100,
    description,
    order_id: orderId,
    currency: "MXN",
    due_date: expirationDate.toISOString().split("T")[0],
  });
};
```

---

## Security Checklist

Before going to production, verify:

1. ✅ Webhook signature verification enabled
2. ✅ All money stored in cents (BIGINT)
3. ✅ Payment verification checks booking status
4. ✅ Payment verification checks user ownership
5. ✅ Environment variables secured (never in client code)
6. ✅ HTTPS enabled for webhooks
7. ✅ Card tokenization on client side (never send raw card data to server)
8. ✅ Device session ID included for card payments (fraud detection)

---

## Testing

### Payment Flow

1. **Card**: Immediate confirmation → booking `confirmed`
2. **SPEI**: Shows CLABE/reference → webhook confirms (seconds)
3. **OXXO**: Shows barcode → webhook confirms (24-72h)

### Test Cards (Sandbox)

| Card Number           | Result             |
| --------------------- | ------------------ |
| `4111 1111 1111 1111` | Success            |
| `4000 0000 0000 0002` | Insufficient funds |

See [OpenPay Docs](https://www.openpay.mx/docs/api/) for full test card list.

---

## Related Skills

- **mexico-market** - Mexican pricing psychology, fee structures, SPEI discount strategy

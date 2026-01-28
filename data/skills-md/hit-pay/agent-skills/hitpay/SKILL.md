---
name: hitpay
description: Integrate HitPay payment gateway for online payments in Next.js and JS/TS applications. Use when user says "Add HitPay", "HitPay checkout", "HitPay payments", "HitPay webhook", "HitPay QR code", "PayNow integration", or "HitPay integration".
license: MIT
metadata:
  author: hitpay
  version: "1.0.0"
---

# HitPay Integration

Payment gateway integration for APAC businesses using Next.js and JavaScript/TypeScript. Supports card payments via redirect and QR-based payments (PayNow, GrabPay, etc.) via embedded QR codes.

## When to Apply

Reference this skill when:
- Integrating HitPay payment gateway
- Creating payment checkout flows
- Implementing QR code payments (PayNow, GrabPay, ShopeePay)
- Handling payment webhooks
- Processing refunds

## Step 1: Determine Payment Methods

Ask which payment methods the customer wants to support:

### Card-Only Methods
- `card` (Visa, Mastercard, Amex)

### QR-Only Methods
- `paynow_online` (Singapore)
- `grabpay_direct`
- `shopee_pay`
- `wechat`
- `alipay`
- `fpx` (Malaysia)
- `promptpay` (Thailand)
- `truemoney` (Thailand)
- `vietqr` (Vietnam)
- `qris` (Indonesia)
- `upi` (India)
- `gcash` (Philippines)

## Step 2: Choose Frontend Approach

| Payment Methods | Recommended Frontend |
|-----------------|---------------------|
| Card only | **Redirect** to HitPay checkout |
| QR only | **Embedded QR** on your site |
| Both card + QR | **Payment method selector** then appropriate flow |

## API Basics

| Environment | Base URL |
|-------------|----------|
| Sandbox | `https://api.sandbox.hit-pay.com` |
| Production | `https://api.hit-pay.com` |

### Authentication

```typescript
const headers = {
  'X-BUSINESS-API-KEY': process.env.HITPAY_API_KEY,
  'Content-Type': 'application/json',
};
```

Get API keys from Settings → Payment Gateway → API Keys in your HitPay dashboard.

## Frontend Option A: Redirect (Cards)

Best for card payments or when you want HitPay to handle the full checkout UI.

### Flow
1. Backend creates payment request
2. Frontend redirects to `response.url`
3. Customer pays on HitPay hosted page
4. Customer returns to your `redirect_url`
5. Backend confirms via webhook

### Next.js API Route

```typescript
// app/api/payments/create/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { amount, currency, orderId } = await request.json();

  const response = await fetch('https://api.sandbox.hit-pay.com/v1/payment-requests', {
    method: 'POST',
    headers: {
      'X-BUSINESS-API-KEY': process.env.HITPAY_API_KEY!,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      amount,
      currency,
      payment_methods: ['card'],
      reference_number: orderId,
      redirect_url: `${process.env.NEXT_PUBLIC_APP_URL}/payment/complete`,
      webhook: `${process.env.NEXT_PUBLIC_APP_URL}/api/webhooks/hitpay`,
    }),
  });

  const data = await response.json();
  return NextResponse.json({ url: data.url, paymentRequestId: data.id });
}
```

### Frontend Component

```typescript
// components/CheckoutButton.tsx
'use client';

export function CheckoutButton({ amount, currency, orderId }: Props) {
  const handleCheckout = async () => {
    const response = await fetch('/api/payments/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount, currency, orderId }),
    });

    const { url } = await response.json();
    window.location.href = url; // Redirect to HitPay
  };

  return <button onClick={handleCheckout}>Pay with Card</button>;
}
```

## Frontend Option B: Embedded QR Code

Best for QR-based payments where customer stays on your site.

### Flow
1. Backend creates payment request with `generate_qr: true`
2. Frontend renders QR code from `response.qr_code_data`
3. Customer scans with payment app
4. Frontend polls for status or listens for webhook
5. Backend confirms via webhook

### Next.js API Route

```typescript
// app/api/payments/create-qr/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { amount, currency, orderId, paymentMethod } = await request.json();

  const response = await fetch('https://api.sandbox.hit-pay.com/v1/payment-requests', {
    method: 'POST',
    headers: {
      'X-BUSINESS-API-KEY': process.env.HITPAY_API_KEY!,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      amount,
      currency,
      payment_methods: [paymentMethod],
      generate_qr: true,
      reference_number: orderId,
      webhook: `${process.env.NEXT_PUBLIC_APP_URL}/api/webhooks/hitpay`,
    }),
  });

  const data = await response.json();
  return NextResponse.json({
    paymentRequestId: data.id,
    qrCodeData: data.qr_code_data,
  });
}
```

### Frontend Component

```typescript
// components/QRPayment.tsx
'use client';

import { useEffect, useRef } from 'react';
import QRCode from 'qrcode';

export function QRPayment({ amount, currency, orderId, paymentMethod }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const createQR = async () => {
      const response = await fetch('/api/payments/create-qr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount, currency, orderId, paymentMethod }),
      });

      const { qrCodeData } = await response.json();

      if (canvasRef.current && qrCodeData) {
        await QRCode.toCanvas(canvasRef.current, qrCodeData, { width: 256 });
      }
    };

    createQR();
  }, [amount, currency, orderId, paymentMethod]);

  return (
    <div>
      <canvas ref={canvasRef} />
      <p>Scan with your payment app</p>
    </div>
  );
}
```

## Frontend Option C: Payment Method Selector

Best for supporting both cards and QR methods.

### Frontend Component

```typescript
// components/PaymentMethodSelector.tsx
'use client';

import { useState } from 'react';
import { QRPayment } from './QRPayment';

const PAYMENT_METHODS = [
  { id: 'card', label: 'Credit/Debit Card', type: 'redirect' },
  { id: 'paynow_online', label: 'PayNow', type: 'qr' },
  { id: 'grabpay_direct', label: 'GrabPay', type: 'qr' },
  { id: 'shopee_pay', label: 'ShopeePay', type: 'qr' },
];

export function PaymentMethodSelector({ amount, currency, orderId }: Props) {
  const [selected, setSelected] = useState<string | null>(null);

  const handlePayment = async (method: typeof PAYMENT_METHODS[0]) => {
    if (method.type === 'redirect') {
      const response = await fetch('/api/payments/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount, currency, orderId }),
      });
      const { url } = await response.json();
      window.location.href = url;
    } else {
      setSelected(method.id);
    }
  };

  if (selected) {
    return (
      <QRPayment
        amount={amount}
        currency={currency}
        orderId={orderId}
        paymentMethod={selected}
      />
    );
  }

  return (
    <div>
      <h3>Select Payment Method</h3>
      {PAYMENT_METHODS.map((method) => (
        <button key={method.id} onClick={() => handlePayment(method)}>
          {method.label}
        </button>
      ))}
    </div>
  );
}
```

## Webhook Handling

Always verify webhook signatures before processing. See `references/webhook-events.md` for details.

```typescript
// app/api/webhooks/hitpay/route.ts
import { NextResponse } from 'next/server';
import crypto from 'crypto';

export async function POST(request: Request) {
  const body = await request.text();
  const signature = request.headers.get('Hitpay-Signature');

  // Verify signature
  const expectedSignature = crypto
    .createHmac('sha256', process.env.HITPAY_SALT!)
    .update(body)
    .digest('hex');

  if (signature !== expectedSignature) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  const payload = JSON.parse(body);

  // Process payment confirmation
  if (payload.status === 'completed') {
    // Mark order as paid
    await markOrderAsPaid(payload.reference_number);
  }

  return NextResponse.json({ received: true });
}
```

## Checking Payment Status

See `references/payment-request-api.md` for the full API reference.

```typescript
// app/api/payments/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const response = await fetch(
    `https://api.sandbox.hit-pay.com/v1/payment-requests/${params.id}`,
    {
      headers: {
        'X-BUSINESS-API-KEY': process.env.HITPAY_API_KEY!,
      },
    }
  );

  const data = await response.json();
  return NextResponse.json(data);
}
```

## Refunds

See `references/refunds.md` for full details.

```typescript
// app/api/payments/[id]/refund/route.ts
export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  const { amount } = await request.json();

  const response = await fetch(
    `https://api.sandbox.hit-pay.com/v1/payment-requests/${params.id}/refund`,
    {
      method: 'POST',
      headers: {
        'X-BUSINESS-API-KEY': process.env.HITPAY_API_KEY!,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ amount }),
    }
  );

  const data = await response.json();
  return NextResponse.json(data);
}
```

## Environment Variables

```bash
# .env.local
HITPAY_API_KEY=your_api_key
HITPAY_SALT=your_webhook_salt
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Test Cards (Sandbox)

| Result | Number | Expiry | CVC |
|--------|--------|--------|-----|
| Success | 4242 4242 4242 4242 | Any future | Any 3 digits |
| Declined | 4000 0000 0000 0002 | Any future | Any 3 digits |

## Resources

- Sandbox Dashboard: https://dashboard.sandbox.hit-pay.com
- Production Dashboard: https://dashboard.hit-pay.com
- API Docs: https://docs.hitpayapp.com

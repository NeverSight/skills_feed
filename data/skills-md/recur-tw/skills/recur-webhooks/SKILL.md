---
name: recur-webhooks
description: Set up and handle Recur webhook events for payment notifications. Use when implementing webhook handlers, verifying signatures, handling subscription events, or when user mentions "webhook", "付款通知", "訂閱事件", "payment notification".
license: MIT
metadata:
  author: recur
  version: "0.0.7"
---

# Recur Webhook Integration

You are helping implement Recur webhooks to receive real-time payment and subscription events.

## Webhook Events

### Core Events (Most Common)

| Event | When Fired |
|-------|------------|
| `checkout.completed` | Payment successful, subscription/order created |
| `subscription.activated` | Subscription is now active |
| `subscription.cancelled` | Subscription was cancelled |
| `subscription.renewed` | Recurring payment successful |
| `subscription.past_due` | Payment failed, subscription at risk |
| `order.paid` | One-time purchase completed |
| `refund.created` | Refund initiated |

### All Supported Events

```typescript
type WebhookEventType =
  // Checkout
  | 'checkout.created'
  | 'checkout.completed'
  // Orders
  | 'order.paid'
  | 'order.payment_failed'
  // Subscription Lifecycle
  | 'subscription.created'
  | 'subscription.activated'
  | 'subscription.cancelled'
  | 'subscription.expired'
  | 'subscription.trial_ending'
  // Subscription Changes
  | 'subscription.upgraded'
  | 'subscription.downgraded'
  | 'subscription.renewed'
  | 'subscription.past_due'
  // Scheduled Changes
  | 'subscription.schedule_created'
  | 'subscription.schedule_executed'
  | 'subscription.schedule_cancelled'
  // Invoices
  | 'invoice.created'
  | 'invoice.paid'
  | 'invoice.payment_failed'
  // Customer
  | 'customer.created'
  | 'customer.updated'
  // Product
  | 'product.created'
  | 'product.updated'
  // Refunds
  | 'refund.created'
  | 'refund.succeeded'
  | 'refund.failed'
```

## Webhook Handler Implementation

### Next.js App Router

```typescript
// app/api/webhooks/recur/route.ts
import { NextRequest, NextResponse } from 'next/server'
import crypto from 'crypto'

const WEBHOOK_SECRET = process.env.RECUR_WEBHOOK_SECRET!

function verifySignature(payload: string, signature: string): boolean {
  const expected = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(payload)
    .digest('hex')
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  )
}

export async function POST(request: NextRequest) {
  const payload = await request.text()
  const signature = request.headers.get('x-recur-signature')

  // Verify signature
  if (!signature || !verifySignature(payload, signature)) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 })
  }

  const event = JSON.parse(payload)

  // Handle events
  switch (event.type) {
    case 'checkout.completed':
      await handleCheckoutCompleted(event.data)
      break

    case 'subscription.activated':
      await handleSubscriptionActivated(event.data)
      break

    case 'subscription.cancelled':
      await handleSubscriptionCancelled(event.data)
      break

    case 'subscription.renewed':
      await handleSubscriptionRenewed(event.data)
      break

    case 'subscription.past_due':
      await handleSubscriptionPastDue(event.data)
      break

    case 'refund.created':
      await handleRefundCreated(event.data)
      break

    default:
      console.log(`Unhandled event type: ${event.type}`)
  }

  return NextResponse.json({ received: true })
}

// Event handlers
async function handleCheckoutCompleted(data: any) {
  const { customerId, subscriptionId, orderId, productId, amount } = data

  // Update your database
  // Grant access to the user
  // Send confirmation email
}

async function handleSubscriptionActivated(data: any) {
  const { subscriptionId, customerId, productId, status } = data

  // Update user's subscription status in your database
  // Enable premium features
}

async function handleSubscriptionCancelled(data: any) {
  const { subscriptionId, customerId, cancelledAt, accessUntil } = data

  // Mark subscription as cancelled
  // User still has access until accessUntil date
  // Send cancellation confirmation email
}

async function handleSubscriptionRenewed(data: any) {
  const { subscriptionId, customerId, amount, nextBillingDate } = data

  // Update billing records
  // Extend access period
}

async function handleSubscriptionPastDue(data: any) {
  const { subscriptionId, customerId, failureReason } = data

  // Notify user of payment failure
  // Consider sending dunning emails
  // May want to restrict access after grace period
}

async function handleRefundCreated(data: any) {
  const { refundId, orderId, amount, reason } = data

  // Update order status
  // Adjust user credits/access
  // Send refund notification
}
```

### Express.js

```typescript
import express from 'express'
import crypto from 'crypto'

const app = express()

// Important: Use raw body for signature verification
app.post(
  '/api/webhooks/recur',
  express.raw({ type: 'application/json' }),
  (req, res) => {
    const payload = req.body.toString()
    const signature = req.headers['x-recur-signature'] as string

    // Verify signature
    const expected = crypto
      .createHmac('sha256', process.env.RECUR_WEBHOOK_SECRET!)
      .update(payload)
      .digest('hex')

    if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) {
      return res.status(401).json({ error: 'Invalid signature' })
    }

    const event = JSON.parse(payload)

    // Handle event...
    console.log('Received event:', event.type)

    res.json({ received: true })
  }
)
```

## Event Payload Structure

```typescript
interface WebhookEvent {
  id: string           // Event ID (for idempotency)
  type: string         // Event type
  timestamp: string    // ISO 8601 timestamp
  data: {
    // Varies by event type
    customerId?: string
    customerEmail?: string
    subscriptionId?: string
    orderId?: string
    productId?: string
    amount?: number
    currency?: string
    // ... more fields depending on event
  }
}
```

## Webhook Configuration

1. Go to **Recur Dashboard** → **Settings** → **Webhooks**
2. Click **Add Endpoint**
3. Enter your endpoint URL (e.g., `https://yourapp.com/api/webhooks/recur`)
4. Select events to receive
5. Copy the **Webhook Secret** to your environment variables

## Testing Webhooks Locally

### Using ngrok

```bash
# Start ngrok tunnel
ngrok http 3000

# Use the ngrok URL in Recur dashboard
# https://xxxx.ngrok.io/api/webhooks/recur
```

### Using Recur CLI (if available)

```bash
# Forward webhooks to local server
recur webhooks forward --to localhost:3000/api/webhooks/recur
```

## Best Practices

### 1. Always Verify Signatures

Never trust webhook payloads without verifying the signature.

### 2. Handle Idempotency

Webhooks may be delivered multiple times. Use the event `id` to deduplicate:

```typescript
async function handleEvent(event: WebhookEvent) {
  // Check if already processed
  const existing = await db.webhookEvent.findUnique({
    where: { eventId: event.id }
  })

  if (existing) {
    console.log('Event already processed:', event.id)
    return
  }

  // Process event...

  // Mark as processed
  await db.webhookEvent.create({
    data: { eventId: event.id, processedAt: new Date() }
  })
}
```

### 3. Return 200 Quickly

Process events asynchronously to avoid timeouts:

```typescript
export async function POST(request: NextRequest) {
  // Verify and parse...

  // Queue for async processing
  await queue.add('process-webhook', event)

  // Return immediately
  return NextResponse.json({ received: true })
}
```

### 4. Handle Retries Gracefully

Recur retries failed webhook deliveries. Ensure your handler is idempotent.

### 5. Log Everything

```typescript
console.log('Webhook received:', {
  type: event.type,
  id: event.id,
  timestamp: event.timestamp,
})
```

## Debugging Webhooks

### Check Webhook Logs

In Recur Dashboard → Webhooks → Click endpoint → View delivery logs

### Common Issues

**401 Unauthorized**
- Check webhook secret is correct
- Ensure using raw body for signature verification
- Verify signature algorithm (HMAC SHA-256)

**Timeout (no response)**
- Return 200 before processing
- Use async processing for heavy operations

**Missing events**
- Check event types are selected in dashboard
- Verify endpoint URL is correct and accessible

## Related Skills

- `/recur-quickstart` - Initial SDK setup
- `/recur-checkout` - Implement payment flows
- `/recur-entitlements` - Check subscription access after webhook

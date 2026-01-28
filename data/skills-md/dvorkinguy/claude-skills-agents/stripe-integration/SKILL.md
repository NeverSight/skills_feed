---
name: stripe-integration
description: Stripe payment integration for SaaS. Use when implementing Stripe checkout, webhooks, subscriptions, or payment flows. Includes secure patterns for Next.js.
---

# Stripe Integration for SaaS

## Setup

### Environment Variables
```env
STRIPE_SECRET_KEY=sk_...
STRIPE_PUBLISHABLE_KEY=pk_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Install
```bash
pnpm add stripe @stripe/stripe-js
```

## Server Client

```typescript
// lib/stripe.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-11-20.acacia',
  typescript: true,
});
```

## Checkout Session

```typescript
// app/api/checkout/route.ts
import { stripe } from '@/lib/stripe';
import { auth } from '@/lib/auth';

export async function POST(request: Request) {
  const user = await auth();
  if (!user) return new Response('Unauthorized', { status: 401 });

  const { priceId } = await request.json();

  // Validate price ID against allowed list
  const allowedPrices = ['price_xxx', 'price_yyy'];
  if (!allowedPrices.includes(priceId)) {
    return new Response('Invalid price', { status: 400 });
  }

  const session = await stripe.checkout.sessions.create({
    customer: user.stripeCustomerId,
    mode: 'subscription',
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/dashboard?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
    subscription_data: {
      metadata: { userId: user.id },
    },
  });

  return Response.json({ url: session.url });
}
```

## Webhook Handler (CRITICAL)

See templates/webhook_handler.ts for complete implementation.

### Security Requirements
1. ✅ Verify signature with `stripe.webhooks.constructEvent()`
2. ✅ Use raw body (not parsed JSON)
3. ✅ Return 200 quickly, process async
4. ✅ Handle idempotency (check if already processed)
5. ✅ Log webhook events for debugging

### Event Types to Handle
- `checkout.session.completed` - Initial purchase
- `customer.subscription.created` - New subscription
- `customer.subscription.updated` - Plan change
- `customer.subscription.deleted` - Cancellation
- `invoice.payment_failed` - Failed payment
- `invoice.paid` - Successful payment

## Testing

```bash
# Forward webhooks to local
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
```

## Common Errors

### "No signatures found matching"
- Check STRIPE_WEBHOOK_SECRET is correct
- Ensure using raw body: `await request.text()`

### "Webhook timeout"
- Process heavy work async
- Return 200 immediately, use queue for processing

---
name: stripe
description: "Help with Stripe payment integration in Next.js projects. Use when implementing checkout flows, subscriptions, webhooks, customer portal, or debugging payment issues. Covers Stripe SDK usage, webhook verification, and subscription management."
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, WebSearch
---

# Stripe Integration Helper

Assist with Stripe payment gateway integration for SaaS applications.

## Quick Reference

### Installation
```bash
bun add stripe @stripe/stripe-js
```

### Environment Variables
```bash
# Server-side (secret)
STRIPE_SECRET_KEY="sk_live_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# Client-side (publishable)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_live_..."

# App URL for callbacks
NEXT_PUBLIC_APP_URL="https://your-app.com"
```

### SDK Initialization

**Server-side:**
```typescript
// lib/stripe.ts
import Stripe from "stripe";

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2025-01-27.acacia",
  typescript: true,
});
```

**Client-side:**
```typescript
// lib/stripe-client.ts
import { loadStripe } from "@stripe/stripe-js";

export const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
);
```

## Common Tasks

### 1. Create Checkout Session

```typescript
// app/api/checkout/route.ts
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { stripe } from "@/lib/stripe";

export async function POST(request: NextRequest) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { priceId } = await request.json();

  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    payment_method_types: ["card"],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: { userId },
    customer_email: user.email, // Optional: pre-fill email
  });

  return NextResponse.json({ url: session.url });
}
```

### 2. Create Customer Portal Session

```typescript
// app/api/billing/portal/route.ts
export async function POST(request: NextRequest) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // Get Stripe customer ID from your database
  const user = await db.query.users.findFirst({
    where: eq(users.id, userId),
  });

  if (!user?.stripeCustomerId) {
    return NextResponse.json({ error: "No subscription" }, { status: 400 });
  }

  const session = await stripe.billingPortal.sessions.create({
    customer: user.stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard`,
  });

  return NextResponse.json({ url: session.url });
}
```

### 3. Webhook Handler

```typescript
// app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from "next/server";
import { stripe } from "@/lib/stripe";
import Stripe from "stripe";

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get("stripe-signature")!;

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error("Webhook signature verification failed");
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object as Stripe.Checkout.Session;
      await handleCheckoutComplete(session);
      break;
    }
    case "customer.subscription.updated": {
      const subscription = event.data.object as Stripe.Subscription;
      await handleSubscriptionUpdate(subscription);
      break;
    }
    case "customer.subscription.deleted": {
      const subscription = event.data.object as Stripe.Subscription;
      await handleSubscriptionCancelled(subscription);
      break;
    }
    case "invoice.payment_failed": {
      const invoice = event.data.object as Stripe.Invoice;
      await handlePaymentFailed(invoice);
      break;
    }
  }

  return NextResponse.json({ received: true });
}
```

## Webhook Events

| Event | When to Handle |
|-------|----------------|
| `checkout.session.completed` | User completes checkout |
| `customer.subscription.created` | New subscription starts |
| `customer.subscription.updated` | Plan change, renewal |
| `customer.subscription.deleted` | Subscription cancelled |
| `invoice.payment_succeeded` | Successful payment |
| `invoice.payment_failed` | Failed payment attempt |
| `customer.updated` | Customer info changed |

## Subscription Status Values

| Status | Description |
|--------|-------------|
| `active` | Subscription is current |
| `past_due` | Payment failed, retrying |
| `canceled` | Subscription ended |
| `unpaid` | All retry attempts failed |
| `trialing` | In trial period |
| `incomplete` | First payment pending |

## Database Schema

### Users Table (add Stripe fields)
```sql
stripeCustomerId    TEXT UNIQUE
stripeSubscriptionId TEXT
stripePriceId       TEXT
stripeCurrentPeriodEnd TIMESTAMP
```

### Subscription Sync Pattern

```typescript
async function syncSubscription(
  userId: string,
  subscription: Stripe.Subscription
) {
  await db
    .update(users)
    .set({
      stripeSubscriptionId: subscription.id,
      stripePriceId: subscription.items.data[0].price.id,
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
    })
    .where(eq(users.id, userId));
}
```

## Feature Gating

```typescript
async function checkFeatureAccess(userId: string): Promise<boolean> {
  const user = await db.query.users.findFirst({
    where: eq(users.id, userId),
  });

  if (!user?.stripeSubscriptionId) return false;

  // Check if subscription is still valid
  const now = new Date();
  return user.stripeCurrentPeriodEnd > now;
}
```

## Testing

### Test Card Numbers

| Card | Scenario |
|------|----------|
| `4242424242424242` | Successful payment |
| `4000000000000002` | Card declined |
| `4000002500003155` | Requires 3D Secure |
| `4000000000009995` | Insufficient funds |

### Stripe CLI for Local Webhooks

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
```

## Pricing Page Pattern

```typescript
// Get prices from Stripe
const prices = await stripe.prices.list({
  active: true,
  expand: ["data.product"],
});

// Display in component
{prices.data.map((price) => (
  <PriceCard
    key={price.id}
    name={(price.product as Stripe.Product).name}
    price={price.unit_amount! / 100}
    interval={price.recurring?.interval}
    priceId={price.id}
  />
))}
```

## Security Best Practices

1. **Never expose secret key** - Use `STRIPE_SECRET_KEY` only server-side
2. **Verify webhook signatures** - Always use `stripe.webhooks.constructEvent`
3. **Idempotency** - Store event IDs to prevent duplicate processing
4. **Raw body for webhooks** - Don't parse JSON before verification
5. **Use metadata** - Store userId in checkout session metadata

## Common Issues

| Issue | Solution |
|-------|----------|
| Webhook signature invalid | Use raw body, not parsed JSON |
| Customer not found | Create customer before checkout |
| Subscription not syncing | Check webhook event registration |
| Test cards failing | Ensure using test mode keys |
| Portal not loading | Verify customer has active subscription |

## Useful Commands

```bash
# List products
stripe products list

# List prices
stripe prices list

# Get subscription
stripe subscriptions retrieve sub_xxx

# Cancel subscription
stripe subscriptions cancel sub_xxx
```

---
name: payment-integration
description: Stripe, RevenueCat, subscription billing, webhooks, PCI compliance, and tax
---

# Payment Integration

## Overview

This skill covers implementing payment processing and subscription billing in web and mobile applications. It addresses Stripe integration (Checkout, Elements, PaymentIntents), subscription lifecycle management, webhook handling with idempotency, PCI compliance, metered and usage-based billing, tax calculation, refund processing, and RevenueCat for mobile subscriptions.

Use this skill when adding payment processing, building subscription billing, handling Stripe webhooks, implementing pricing pages, managing payment failures, or integrating mobile in-app purchases.

---

## Core Principles

1. **Never handle raw card data** - Use Stripe Elements or Checkout to keep card numbers off your servers entirely. This keeps you at PCI SAQ-A (the simplest compliance level) rather than SAQ-D.
2. **Webhooks are the source of truth** - Never trust client-side payment confirmation. A successful PaymentIntent on the client means nothing until your webhook handler confirms `payment_intent.succeeded`. Build your system around webhook events.
3. **Idempotency everywhere** - Webhooks can be delivered multiple times. Every webhook handler must be idempotent. Use Stripe's event ID as a deduplication key.
4. **Handle failure gracefully** - Payments fail for many reasons (insufficient funds, expired cards, fraud detection). Build retry flows, dunning emails, and graceful degradation into the subscription lifecycle.
5. **Test with Stripe's test mode** - Use test API keys, test card numbers, and test clocks for subscription lifecycle testing. Never test with real payment methods.

---

## Key Patterns

### Pattern 1: Stripe Checkout for Subscriptions

**When to use:** When you want Stripe to handle the entire checkout UI, including payment form, coupon codes, and tax calculation.

**Implementation:**

```typescript
// Server - Create Checkout Session
// app/api/checkout/route.ts
import Stripe from "stripe";
import { NextRequest, NextResponse } from "next/server";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-06-20",
});

export async function POST(req: NextRequest) {
  const { priceId, userId, email } = await req.json();

  // Get or create Stripe customer
  let customerId = await getStripeCustomerId(userId);
  if (!customerId) {
    const customer = await stripe.customers.create({
      email,
      metadata: { userId },
    });
    customerId = customer.id;
    await saveStripeCustomerId(userId, customerId);
  }

  const session = await stripe.checkout.sessions.create({
    customer: customerId,
    mode: "subscription",
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
    subscription_data: {
      metadata: { userId },
      trial_period_days: 14,
    },
    // Enable automatic tax calculation
    automatic_tax: { enabled: true },
    // Allow promo codes
    allow_promotion_codes: true,
    // Collect billing address for tax
    billing_address_collection: "required",
    // Customer portal for self-service management
    customer_update: {
      address: "auto",
      name: "auto",
    },
  });

  return NextResponse.json({ url: session.url });
}
```

```tsx
// Client - Redirect to Checkout
function PricingCard({ plan }: { plan: PricingPlan }) {
  const [loading, setLoading] = useState(false);

  const handleSubscribe = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          priceId: plan.stripePriceId,
          userId: user.id,
          email: user.email,
        }),
      });

      const { url } = await res.json();
      window.location.href = url; // Redirect to Stripe Checkout
    } catch (error) {
      toast.error("Failed to start checkout");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pricing-card">
      <h3>{plan.name}</h3>
      <p className="price">${plan.price}/mo</p>
      <ul>
        {plan.features.map((f) => (
          <li key={f}>{f}</li>
        ))}
      </ul>
      <button onClick={handleSubscribe} disabled={loading}>
        {loading ? "Redirecting..." : "Subscribe"}
      </button>
    </div>
  );
}
```

**Why:** Stripe Checkout handles PCI compliance, 3D Secure authentication, tax calculation, promo codes, and localization. Building your own checkout form is hundreds of hours of work and ongoing PCI compliance burden. Use Checkout unless you have a strong reason to build custom UI.

---

### Pattern 2: Webhook Handler with Idempotency

**When to use:** Every Stripe integration. Webhooks are the only reliable way to know payment status.

**Implementation:**

```typescript
// app/api/webhooks/stripe/route.ts
import Stripe from "stripe";
import { NextRequest, NextResponse } from "next/server";
import { headers } from "next/headers";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// Process each event type
const eventHandlers: Record<string, (event: Stripe.Event) => Promise<void>> = {
  "checkout.session.completed": async (event) => {
    const session = event.data.object as Stripe.Checkout.Session;
    const userId = session.metadata?.userId ?? session.subscription?.toString();

    await db.user.update({
      where: { stripeCustomerId: session.customer as string },
      data: {
        subscriptionId: session.subscription as string,
        subscriptionStatus: "active",
      },
    });
  },

  "customer.subscription.updated": async (event) => {
    const subscription = event.data.object as Stripe.Subscription;

    await db.user.update({
      where: { stripeCustomerId: subscription.customer as string },
      data: {
        subscriptionStatus: subscription.status,
        planId: subscription.items.data[0].price.id,
        currentPeriodEnd: new Date(subscription.current_period_end * 1000),
        cancelAtPeriodEnd: subscription.cancel_at_period_end,
      },
    });
  },

  "customer.subscription.deleted": async (event) => {
    const subscription = event.data.object as Stripe.Subscription;

    await db.user.update({
      where: { stripeCustomerId: subscription.customer as string },
      data: {
        subscriptionStatus: "canceled",
        planId: null,
      },
    });
  },

  "invoice.payment_failed": async (event) => {
    const invoice = event.data.object as Stripe.Invoice;

    await db.user.update({
      where: { stripeCustomerId: invoice.customer as string },
      data: { subscriptionStatus: "past_due" },
    });

    // Send dunning email
    await sendDunningEmail(invoice.customer as string, {
      amountDue: invoice.amount_due,
      nextRetry: invoice.next_payment_attempt
        ? new Date(invoice.next_payment_attempt * 1000)
        : null,
    });
  },

  "invoice.paid": async (event) => {
    const invoice = event.data.object as Stripe.Invoice;

    await db.user.update({
      where: { stripeCustomerId: invoice.customer as string },
      data: { subscriptionStatus: "active" },
    });
  },
};

export async function POST(req: NextRequest) {
  const body = await req.text();
  const signature = (await headers()).get("stripe-signature")!;

  let event: Stripe.Event;

  // 1. Verify webhook signature (prevents spoofing)
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error("Webhook signature verification failed:", err);
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  // 2. Idempotency check - skip already-processed events
  const alreadyProcessed = await db.stripeEvent.findUnique({
    where: { eventId: event.id },
  });

  if (alreadyProcessed) {
    return NextResponse.json({ received: true });
  }

  // 3. Process the event
  const handler = eventHandlers[event.type];
  if (handler) {
    try {
      await handler(event);

      // 4. Record processed event for idempotency
      await db.stripeEvent.create({
        data: {
          eventId: event.id,
          type: event.type,
          processedAt: new Date(),
        },
      });
    } catch (err) {
      console.error(`Error processing ${event.type}:`, err);
      // Return 500 so Stripe retries
      return NextResponse.json({ error: "Processing failed" }, { status: 500 });
    }
  }

  return NextResponse.json({ received: true });
}
```

**Why:** Stripe delivers webhooks at least once, meaning duplicates are possible. The idempotency check (storing processed event IDs) prevents double-processing. Signature verification prevents spoofed webhook attacks. Returning 500 on handler errors triggers Stripe's automatic retry with exponential backoff.

---

### Pattern 3: Customer Portal for Self-Service

**When to use:** Let customers manage their own subscriptions (upgrade, downgrade, cancel, update payment method) without contacting support.

**Implementation:**

```typescript
// Create portal session
// app/api/billing/portal/route.ts
export async function POST(req: NextRequest) {
  const { userId } = await req.json();

  const user = await db.user.findUniqueOrThrow({
    where: { id: userId },
    select: { stripeCustomerId: true },
  });

  if (!user.stripeCustomerId) {
    return NextResponse.json({ error: "No billing account" }, { status: 400 });
  }

  const session = await stripe.billingPortal.sessions.create({
    customer: user.stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_URL}/settings/billing`,
  });

  return NextResponse.json({ url: session.url });
}
```

```typescript
// Configure the portal in Stripe (do this once, via API or Dashboard)
await stripe.billingPortal.configurations.create({
  business_profile: {
    headline: "Manage your subscription",
  },
  features: {
    subscription_update: {
      enabled: true,
      default_allowed_updates: ["price", "quantity"],
      proration_behavior: "create_prorations",
      products: [
        {
          product: "prod_xxx",
          prices: ["price_monthly", "price_annual"],
        },
      ],
    },
    subscription_cancel: {
      enabled: true,
      mode: "at_period_end", // Don't cancel immediately
      cancellation_reason: {
        enabled: true,
        options: [
          "too_expensive",
          "missing_features",
          "switched_service",
          "unused",
          "other",
        ],
      },
    },
    payment_method_update: { enabled: true },
    invoice_history: { enabled: true },
  },
});
```

**Why:** Self-service billing reduces support tickets by 60-80%. Stripe's Customer Portal is a hosted solution that handles plan changes, proration, cancellation with reason capture, payment method updates, and invoice history -- all without building custom UI.

---

### Pattern 4: Usage-Based Billing

**When to use:** When pricing is based on consumption (API calls, storage, compute minutes, seats) rather than flat-rate subscriptions.

**Implementation:**

```typescript
// Report usage to Stripe
async function reportUsage(
  subscriptionItemId: string,
  quantity: number,
  timestamp?: number
): Promise<void> {
  await stripe.subscriptionItems.createUsageRecord(subscriptionItemId, {
    quantity,
    timestamp: timestamp ?? Math.floor(Date.now() / 1000),
    action: "increment", // Add to existing usage (vs "set" to replace)
  });
}

// Background job: aggregate and report usage hourly
async function reportHourlyUsage(): Promise<void> {
  const activeSubscriptions = await db.subscription.findMany({
    where: { status: "active", plan: { billingModel: "usage" } },
    include: { user: true },
  });

  for (const sub of activeSubscriptions) {
    const usage = await getHourlyUsage(sub.userId);

    if (usage > 0) {
      await reportUsage(sub.stripeSubscriptionItemId, usage);

      await db.usageReport.create({
        data: {
          subscriptionId: sub.id,
          quantity: usage,
          reportedAt: new Date(),
        },
      });
    }
  }
}

// Track usage in your application
async function trackApiCall(userId: string, endpoint: string): Promise<void> {
  // Increment usage counter (Redis for speed)
  const key = `usage:${userId}:${getCurrentHour()}`;
  await redis.incr(key);
  await redis.expire(key, 86400 * 7); // Keep for 7 days

  // Check if user is approaching their limit
  const currentUsage = await getCurrentMonthUsage(userId);
  const limit = await getUserPlanLimit(userId);

  if (currentUsage >= limit * 0.8) {
    await sendUsageWarningEmail(userId, currentUsage, limit);
  }

  if (currentUsage >= limit) {
    throw new UsageLimitExceededError(userId, currentUsage, limit);
  }
}
```

**Why:** Usage-based billing aligns cost with value -- customers pay for what they use. Hourly aggregation reduces API calls to Stripe while keeping usage data fresh enough for invoicing. Redis-based tracking provides sub-millisecond usage checks for rate limiting.

---

## Stripe Test Cards Reference

| Number | Scenario |
|---|---|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0000 0000 3220` | 3D Secure required |
| `4000 0000 0000 9995` | Declined (insufficient funds) |
| `4000 0000 0000 0341` | Attaching to customer fails |
| `4000 0025 0000 3155` | Requires authentication |

Use any future expiry date and any 3-digit CVC.

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|---|---|---|
| Trusting client-side payment confirmation | Users can spoof success | Webhook handler is the source of truth |
| Handling raw card numbers on your server | PCI SAQ-D compliance (very expensive) | Use Stripe Elements or Checkout |
| No idempotency in webhook handlers | Double charges, duplicate provisioning | Deduplicate by event ID |
| Canceling subscriptions immediately | Users lose access mid-billing period | Cancel at period end (`cancel_at_period_end`) |
| Hardcoding prices in your app | Can't change pricing without deploy | Store price IDs in database or environment |
| No dunning flow for failed payments | Silent revenue loss (involuntary churn) | Automated retry + dunning emails |
| Testing with real payment methods | Risk of real charges, no test clocks | Use Stripe test mode exclusively |

---

## Checklist

- [ ] Stripe API keys stored in environment variables (never in code)
- [ ] Webhook signature verification enabled
- [ ] Webhook handler is idempotent (event ID deduplication)
- [ ] All subscription status changes handled (created, updated, canceled, past_due)
- [ ] Failed payment dunning flow implemented (email + retry)
- [ ] Customer portal configured for self-service billing
- [ ] Test mode used for all development and staging
- [ ] PCI compliance level confirmed (SAQ-A with Stripe Checkout/Elements)
- [ ] Tax calculation enabled (Stripe Tax or external provider)
- [ ] Proration configured for plan changes (upgrade/downgrade)
- [ ] Webhook endpoint registered in Stripe Dashboard
- [ ] Stripe CLI installed for local webhook testing (`stripe listen --forward-to`)

---

## Related Resources

- **Skills:** `authentication-patterns` (user identity for billing), `email-systems` (dunning emails)
- **Skills:** `monitoring-observability` (payment failure alerting)
- **Rules:** `rules/stacks/fullstack-nextjs-nestjs.md` (API route patterns)

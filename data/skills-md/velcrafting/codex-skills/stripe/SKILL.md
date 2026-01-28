---
name: stripe
description: >-
  This skill should be used when the user asks to "integrate Stripe",
  "add payments", "create subscriptions", "handle webhooks", "usage-based billing",
  "per-seat pricing", "tiered plans", "checkout session", "customer portal",
  "sync Stripe data", "Stripe Sync Engine", "payment processing", "MRR analytics",
  "revenue reporting", or mentions 'Stripe', 'subscription', 'billing', 'webhook',
  'checkout', 'metered billing', 'payment intent', 'stripe schema'.
  Automatically triggers for payment, subscription, and billing analytics work.
version: 1.1.0
---

# Stripe Integration Expert

Comprehensive guidance for integrating Stripe payments including subscriptions, usage-based billing, webhooks, and multi-platform support (Next.js, iOS, Android, Flutter) with Supabase database synchronization.

> **Philosophy:** Use Stripe Checkout for simplicity, Payment Intents for customization. Always verify webhooks. For Supabase sync, prefer **Stripe Sync Engine** (one-click, zero maintenance) unless you need custom schemas. Never expose secret keys to clients.

## Critical Rules

### API Keys Security

| Key Type | Prefix | Safety | Use Case |
|----------|--------|--------|----------|
| Publishable | `pk_live_` / `pk_test_` | Client-safe | Browser, mobile apps |
| Secret | `sk_live_` / `sk_test_` | Backend ONLY | Servers, Edge Functions |
| Restricted | `rk_live_` / `rk_test_` | Backend ONLY | Limited permissions |
| Webhook Secret | `whsec_` | Backend ONLY | Signature verification |

**NEVER:**
- Expose secret keys in client code
- Commit keys to version control
- Log full API keys
- Use secret keys in browser/mobile apps

**ALWAYS:**
- Use environment variables for all keys
- Use publishable key for client-side Stripe.js
- Use restricted keys for specific operations
- Rotate keys immediately if compromised

### Webhook Security (CRITICAL)

```typescript
// CORRECT: Use raw body for signature verification
const body = await req.text()  // Raw string, NOT parsed
const signature = req.headers.get('stripe-signature')!
const event = stripe.webhooks.constructEvent(body, signature, webhookSecret)

// WRONG: This will FAIL signature verification
const body = await req.json()  // DON'T parse first!
```

**Webhook Rules:**
- ALWAYS verify signatures before processing
- Use raw request body (NOT parsed JSON)
- Implement idempotency (track processed events)
- Return 200 quickly, process asynchronously
- Handle retries gracefully

### PCI Compliance

- NEVER collect card numbers directly on your server
- ALWAYS use Stripe.js, Elements, or Checkout
- Use Payment Intents or Checkout Sessions
- Enable SCA for EU customers (automatic with Checkout)
- Log payment events but NEVER log card details

## Quick Reference

### Subscription Billing Models

| Model | Use Case | Implementation |
|-------|----------|----------------|
| Flat Rate | Fixed monthly/yearly | Single price, `licensed` |
| Per-Seat | Per user pricing | `quantity` on subscription |
| Usage-Based | Pay for consumption | Meters + `metered` billing |
| Tiered | Volume discounts | `tiered` pricing |
| Hybrid | Base + usage | Multiple prices on subscription |

### Essential Webhook Events

| Event | When | Action |
|-------|------|--------|
| `checkout.session.completed` | Successful checkout | Provision access |
| `customer.subscription.created` | New subscription | Create local record |
| `customer.subscription.updated` | Plan change/renewal | Update local record |
| `customer.subscription.deleted` | Cancellation | Revoke access |
| `invoice.paid` | Successful payment | Update billing status |
| `invoice.payment_failed` | Payment failure | Notify customer |

### Environment Variables

```bash
# .env.local (Next.js)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Supabase Edge Functions
# Set via: supabase secrets set STRIPE_SECRET_KEY=sk_test_...
```

## Workflow Decision Tree

```
User mentions Stripe/payments?
├─> Setting up Stripe?
│   └─> Use: Initial Setup (below)
├─> Creating subscriptions?
│   ├─> Simple flat rate?
│   │   └─> Use: Checkout Session pattern
│   ├─> Per-seat pricing?
│   │   └─> See: references/subscriptions.md
│   └─> Usage-based/metered?
│       └─> See: references/subscriptions.md
├─> Handling webhooks?
│   └─> See: references/webhooks.md
├─> Next.js integration?
│   └─> See: references/nextjs-integration.md
├─> Mobile integration?
│   └─> See: references/mobile-integration.md
├─> Syncing with Supabase?
│   ├─> Zero-maintenance sync? (Recommended)
│   │   └─> Use: Stripe Sync Engine (references/supabase-sync.md)
│   ├─> Custom schema/transformations?
│   │   └─> Use: Webhook Sync (references/supabase-sync.md)
│   └─> Real-time admin queries?
│       └─> Use: Stripe Wrapper FDW (references/supabase-sync.md)
└─> MRR/Revenue analytics?
    └─> See: references/supabase-sync.md (Business Analytics Queries)
```

## Initial Setup

### 1. Install Dependencies

**Next.js:**
```bash
npm install stripe @stripe/stripe-js
```

**iOS (Swift Package Manager):**
```
https://github.com/stripe/stripe-ios
```

**Android (Gradle):**
```kotlin
implementation("com.stripe:stripe-android:20.+")
```

**Flutter:**
```yaml
dependencies:
  flutter_stripe: ^11.0.0
```

### 2. Initialize Stripe

**Server (Next.js):**
```typescript
// lib/stripe/server.ts
import Stripe from 'stripe'

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
  typescript: true,
})
```

**Client (Next.js):**
```typescript
// lib/stripe/client.ts
import { loadStripe, Stripe } from '@stripe/stripe-js'

let stripePromise: Promise<Stripe | null>

export function getStripe() {
  if (!stripePromise) {
    stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!)
  }
  return stripePromise
}
```

## Checkout Session Quick Reference

**Server Action (Next.js):**
```typescript
'use server'

import { redirect } from 'next/navigation'
import { stripe } from '@/lib/stripe/server'
import { createClient } from '@/lib/supabase/server'

export async function createCheckoutSession(priceId: string) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  // Get or create Stripe customer
  const { data: customer } = await supabase
    .from('customers')
    .select('stripe_customer_id')
    .eq('user_id', user.id)
    .single()

  const session = await stripe.checkout.sessions.create({
    customer: customer?.stripe_customer_id,
    customer_email: !customer ? user.email : undefined,
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: {
      user_id: user.id,
    },
  })

  redirect(session.url!)
}
```

## Customer Portal Quick Reference

```typescript
'use server'

import { redirect } from 'next/navigation'
import { stripe } from '@/lib/stripe/server'
import { createClient } from '@/lib/supabase/server'

export async function createPortalSession() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  const { data: customer } = await supabase
    .from('customers')
    .select('stripe_customer_id')
    .eq('user_id', user.id)
    .single()

  if (!customer?.stripe_customer_id) {
    redirect('/pricing')
  }

  const session = await stripe.billingPortal.sessions.create({
    customer: customer.stripe_customer_id,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/settings/billing`,
  })

  redirect(session.url)
}
```

## Webhook Handler Quick Reference

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from 'next/headers'
import { stripe } from '@/lib/stripe/server'
import { createClient } from '@supabase/supabase-js'

const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SECRET_KEY!
)

export async function POST(req: Request) {
  const body = await req.text()
  const headersList = await headers()
  const signature = headersList.get('stripe-signature')!

  let event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err: any) {
    console.error('Webhook signature verification failed:', err.message)
    return new Response(`Webhook Error: ${err.message}`, { status: 400 })
  }

  // Idempotency check
  const { data: existing } = await supabaseAdmin
    .from('stripe_events')
    .select('stripe_event_id')
    .eq('stripe_event_id', event.id)
    .single()

  if (existing) {
    return new Response(JSON.stringify({ received: true, cached: true }))
  }

  // Handle the event
  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutComplete(event.data.object)
        break
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
        await handleSubscriptionChange(event.data.object)
        break
      case 'customer.subscription.deleted':
        await handleSubscriptionDeleted(event.data.object)
        break
      case 'invoice.payment_failed':
        await handlePaymentFailed(event.data.object)
        break
    }

    // Record processed event
    await supabaseAdmin
      .from('stripe_events')
      .insert({
        stripe_event_id: event.id,
        type: event.type,
      })

  } catch (err) {
    console.error('Error processing webhook:', err)
    return new Response('Webhook handler failed', { status: 500 })
  }

  return new Response(JSON.stringify({ received: true }))
}
```

## Subscription Check in Proxy

```typescript
// proxy.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function proxy(request: NextRequest) {
  // ... Supabase client setup ...

  const { data: { user } } = await supabase.auth.getUser()

  // Check subscription for premium routes
  if (user && request.nextUrl.pathname.startsWith('/dashboard')) {
    const { data: subscription } = await supabase
      .from('subscriptions')
      .select('status, current_period_end')
      .eq('customer_id', user.id)
      .in('status', ['active', 'trialing'])
      .single()

    if (!subscription) {
      return NextResponse.redirect(new URL('/pricing', request.url))
    }
  }

  return supabaseResponse
}
```

## Pre-Flight Checklist

Before ANY Stripe integration:

- [ ] Secret key in environment variables only
- [ ] Publishable key for client-side code
- [ ] Webhook secret configured
- [ ] Webhook signature verification implemented
- [ ] Idempotency handling for webhooks
- [ ] Using Stripe.js for card collection (PCI compliance)
- [ ] Test mode keys for development
- [ ] Customer portal configured in Stripe Dashboard
- [ ] Supabase tables created for sync
- [ ] RLS policies on Stripe-synced tables
- [ ] Error handling for all Stripe API calls

## Resources

### Reference Files (Load as needed)

- **`references/subscriptions.md`** - Billing models, lifecycle, per-seat, usage-based
- **`references/webhooks.md`** - Signature verification, event handling, idempotency
- **`references/nextjs-integration.md`** - Complete Next.js patterns
- **`references/mobile-integration.md`** - iOS, Android, Flutter integration
- **`references/supabase-sync.md`** - Database schema, sync patterns, RLS

## Common Mistakes to Avoid

1. **Parsing body before signature verification** - Use raw text body
2. **Not implementing idempotency** - Events can be sent multiple times
3. **Exposing secret keys in client code** - Use publishable keys only
4. **Collecting card numbers directly** - Always use Stripe.js/Elements
5. **Not handling subscription status changes** - Sync via webhooks
6. **Hardcoding prices** - Use Stripe Dashboard or API for prices
7. **Not testing webhooks locally** - Use `stripe listen --forward-to`
8. **Missing error handling** - Stripe API can fail

## Testing

### Local Webhook Testing

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
```

### Test Card Numbers

| Card | Number | Use Case |
|------|--------|----------|
| Success | `4242 4242 4242 4242` | Successful payment |
| Decline | `4000 0000 0000 0002` | Card declined |
| Auth Required | `4000 0025 0000 3155` | 3D Secure required |
| Insufficient Funds | `4000 0000 0000 9995` | Insufficient funds |

---

**Skill Version:** 1.0.0
**Last Updated:** 2025-01-07
**Documentation:** https://docs.stripe.com

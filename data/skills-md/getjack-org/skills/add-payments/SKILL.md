---
name: add-payments
description: >
  Add Stripe subscription payments to any Jack project.
  Use when: user wants payments, subscriptions, billing, or checkout.
  Stack-agnostic: works with any framework (Hono, Next.js, Express) and auth library.
---

# Add Stripe Payments to Jack Project

You are guiding a user through adding Stripe subscription payments. This is a hands-on guided workflow, not a reference doc.

## Your Role

- Ask questions to understand their needs
- Explain what you're doing and why
- Execute actions confidently (don't ask permission for standard steps)
- Guide them through the two-deploy process

---

## Phase 1: Gather Requirements

**Before writing any code, ask the user:**

1. "What type of payments do you need?"
   - **One-time payment** - Customer pays once (e.g., buy a product, lifetime access)
   - **Single subscription** - One recurring plan (e.g., "Premium at $10/month")
   - **Multiple tiers** - Different plans (e.g., "Pro at $19/month, Enterprise at $99/month")

2. "Do you have a Stripe account with API keys ready? I'll need your secret key (starts with `sk_test_` or `sk_live_`). Test keys are recommended for initial setup."

3. "Do you already have products/prices in Stripe, or should I create them?"

**Wait for their answers before proceeding.**

### Adapt Based on Payment Type

**One-time payments:**
- Simpler schema (no subscription table, just payment records)
- Checkout mode: `payment` instead of `subscription`
- No webhook handlers for subscription events
- Endpoint: `/api/checkout/create` returns one-time checkout URL

**Single subscription:**
- One price ID in secrets (`STRIPE_PRICE_ID`)
- Simpler code (no plan comparison logic)
- Standard subscription webhooks

**Multiple tiers:**
- Multiple price IDs (`STRIPE_PRO_PRICE_ID`, `STRIPE_ENTERPRISE_PRICE_ID`, etc.)
- Plan comparison logic in subscription status
- Full subscription webhooks

---

## Phase 2: Analyze Their Stack

Read the project to understand:
- Framework (Hono, Next.js, Express, etc.)
- Auth system (Better Auth, custom, none)
- Database (D1, Drizzle, Prisma, none)

Choose the appropriate reference:
- Hono + Better Auth → `reference/hono-better-auth.md`
- Hono + custom/no auth → `reference/hono-custom.md`
- Next.js → `reference/nextjs.md`

---

## Phase 3: Implementation

Tell the user what you're creating:

"I'll set up:
1. **Webhook handler** - receives payment events from Stripe
2. **Checkout endpoints** - creates payment sessions
3. **Subscription endpoints** - checks subscription status
4. **Database schema** - stores subscription data

Let me get started."

### Required Files

Create these (adapt to their stack):

1. **Webhook handler** at `/api/webhooks/stripe`
   - Verifies Stripe signatures
   - Handles: `checkout.session.completed`, `customer.subscription.*`, `invoice.*`
   - Uses async signature verification (required for Jack Cloud)

2. **Checkout endpoint** at `/api/checkout/create`
   - Creates Stripe Checkout Session
   - Returns redirect URL

3. **Subscription endpoint** at `/api/subscription/status`
   - Returns current subscription state

4. **Database schema** with tables:
   - `user` (add `stripe_customer_id` column)
   - `subscription` (subscription data)
   - `stripe_webhook_event` (idempotency)

5. **Secrets template** `.secrets.json.example`

### Secrets Required

| Secret | Format | When Needed |
|--------|--------|-------------|
| `STRIPE_SECRET_KEY` | `sk_test_...` or `sk_live_...` | Always |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` | After first deploy |
| `STRIPE_PRICE_ID` | `price_...` | Single plan/product |
| `STRIPE_PRO_PRICE_ID` | `price_...` | Multiple tiers only |
| `STRIPE_ENTERPRISE_PRICE_ID` | `price_...` | Multiple tiers only |

Adapt secret names based on what the user needs. For a single subscription, just use `STRIPE_PRICE_ID`. For multiple tiers, use descriptive names like `STRIPE_PRO_PRICE_ID`.

---

## Phase 4: First Deploy

**Explain to the user:**

"Now I'll deploy the app. Here's what happens next:

1. **First deploy** - Gets us a live URL
2. **Create Stripe webhook** - Points to that URL
3. **Second deploy** - Adds the webhook secret

This two-step process is required because Stripe needs your live URL to create the webhook, and we need the webhook secret for signature verification."

**Then deploy:**

```bash
jack ship
```

After deploy, note the URL (e.g., `https://username-project.runjack.xyz`).

---

## Phase 5: Stripe Webhook Setup

**Tell the user:**

"Your app is live. Now I'll create the Stripe webhook pointing to your URL."

### If user wants you to create it (API):

**For one-time payments:**
```bash
curl -X POST https://api.stripe.com/v1/webhook_endpoints \
  -u "STRIPE_SECRET_KEY:" \
  -d "url=https://YOUR_URL/api/webhooks/stripe" \
  -d "enabled_events[]=checkout.session.completed"
```

**For subscriptions:**
```bash
curl -X POST https://api.stripe.com/v1/webhook_endpoints \
  -u "STRIPE_SECRET_KEY:" \
  -d "url=https://YOUR_URL/api/webhooks/stripe" \
  -d "enabled_events[]=checkout.session.completed" \
  -d "enabled_events[]=customer.subscription.created" \
  -d "enabled_events[]=customer.subscription.updated" \
  -d "enabled_events[]=customer.subscription.deleted" \
  -d "enabled_events[]=invoice.paid" \
  -d "enabled_events[]=invoice.payment_failed"
```

Extract the `secret` from the response - it starts with `whsec_`.

### If user prefers Dashboard:

Guide them:
1. Go to https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Enter URL: `https://YOUR_URL/api/webhooks/stripe`
4. Select events (list them)
5. Copy the signing secret

---

## Phase 6: Create Stripe Products (if needed)

If user doesn't have products, create them based on what they need:

### One-time payment (single product)

Ask: "What's the product name and price?"

```bash
curl -X POST https://api.stripe.com/v1/products \
  -u "STRIPE_SECRET_KEY:" \
  -d "name=YOUR_PRODUCT_NAME"

curl -X POST https://api.stripe.com/v1/prices \
  -u "STRIPE_SECRET_KEY:" \
  -d "product=PRODUCT_ID" \
  -d "unit_amount=PRICE_IN_CENTS" \
  -d "currency=usd"
```

### Single subscription

Ask: "What's your plan name and monthly price?"

```bash
curl -X POST https://api.stripe.com/v1/products \
  -u "STRIPE_SECRET_KEY:" \
  -d "name=YOUR_PLAN_NAME"

curl -X POST https://api.stripe.com/v1/prices \
  -u "STRIPE_SECRET_KEY:" \
  -d "product=PRODUCT_ID" \
  -d "unit_amount=PRICE_IN_CENTS" \
  -d "currency=usd" \
  -d "recurring[interval]=month"
```

### Multiple tiers

Ask: "What plans do you want? (e.g., 'Pro at $19/month, Enterprise at $99/month')"

Create each plan with the user's specified names and prices.

Note the price ID(s) for `.secrets.json`.

---

## Phase 7: Second Deploy

Update `.secrets.json` with:
- `STRIPE_WEBHOOK_SECRET` (from webhook creation)
- Price IDs (if created)

```bash
jack ship
```

---

## Phase 8: Verification

**Tell the user:**

"Everything is deployed. Let's verify it works."

### Test the flow:

1. Check subscription status (should be free/none):
```bash
curl "https://YOUR_URL/api/subscription/status?email=test@example.com"
```

2. Create a checkout session:
```bash
curl -X POST "https://YOUR_URL/api/checkout/create" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

3. **Ask user to complete checkout** with test card `4242 4242 4242 4242`

4. After checkout, verify subscription is active:
```bash
curl "https://YOUR_URL/api/subscription/status?email=test@example.com"
```

If `subscribed: true`, you're done!

---

## Troubleshooting

### Webhook returns 400
- Check `STRIPE_WEBHOOK_SECRET` matches the endpoint
- Ensure using raw body (not parsed JSON) for verification

### Subscription not created
- Check Stripe Dashboard → Webhooks → Recent deliveries
- Look for errors in webhook response

### Checkout fails
- Verify `STRIPE_SECRET_KEY` is correct
- Check price ID exists in Stripe

---

## Reference Examples

Stack-specific code examples (adapt to project's patterns):
- [reference/hono-better-auth.md](reference/hono-better-auth.md)
- [reference/hono-custom.md](reference/hono-custom.md)
- [reference/nextjs.md](reference/nextjs.md)

---

## Stripe Documentation

For current API reference: `https://docs.stripe.com/llms.txt`

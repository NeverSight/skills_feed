---
name: stripe-sync-webhook
description: When the user wants to create webhook handlers for stripe-sync-engine. Also use when the user mentions "webhook endpoint," "processWebhook," "stripe webhook handler," "stripe events," or "real-time sync."
---

# Stripe Sync Engine Webhook Setup

You are an expert in setting up Stripe webhook handlers that use stripe-sync-engine. Your goal is to help users create webhook endpoints that automatically sync Stripe events to their PostgreSQL database.

## Initial Assessment

Before proceeding, verify:

1. **Is stripe-sync-engine set up?** (see setup skill)
2. **Are migrations completed?** (see migrations skill)
3. **What framework are you using?** (Next.js, Hono, Deno Fresh, etc.)

## Framework-Specific Implementations

### Next.js App Router

Create `app/api/webhooks/stripe/route.ts`:

```typescript
import { NextResponse } from 'next/server';
import { stripeSync } from '@/lib/stripeSync';

export async function POST(request: Request) {
  try {
    const signature = request.headers.get('stripe-signature') ?? undefined;
    const arrayBuffer = await request.arrayBuffer();
    const payload = Buffer.from(arrayBuffer);

    await stripeSync.processWebhook(payload, signature);

    return NextResponse.json({ received: true });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    console.error('Webhook processing failed:', message);
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
```

### Next.js Pages Router

Create `pages/api/webhooks/stripe.ts`:

```typescript
import type { NextApiRequest, NextApiResponse } from 'next';
import { stripeSync } from '@/lib/stripeSync';
import { buffer } from 'micro';

// Disable body parsing - we need the raw body for signature verification
export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const signature = req.headers['stripe-signature'] as string | undefined;
    const payload = await buffer(req);

    await stripeSync.processWebhook(payload, signature);

    return res.status(200).json({ received: true });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    console.error('Webhook processing failed:', message);
    return res.status(400).json({ error: message });
  }
}
```

Install micro for body parsing:
```bash
npm install micro
```

### Hono

```typescript
import { Hono } from 'hono';
import { StripeSync } from 'stripe-sync-engine';

const stripeSync = new StripeSync({
  poolConfig: { connectionString: process.env.DATABASE_URL },
  stripeSecretKey: process.env.STRIPE_SECRET_KEY!,
  stripeWebhookSecret: process.env.STRIPE_WEBHOOK_SECRET!,
});

const app = new Hono();

app.post('/webhooks/stripe', async (c) => {
  const signature = c.req.header('stripe-signature') ?? undefined;
  const arrayBuffer = await c.req.raw.arrayBuffer();
  const payload = Buffer.from(arrayBuffer);

  await stripeSync.processWebhook(payload, signature);

  return c.json({ received: true });
});
```

### Deno Fresh

Create `routes/api/webhooks/stripe.ts`:

```typescript
import { Handlers } from "$fresh/server.ts";
import { stripeSync } from "../../../utils/stripeSync.ts";

export const handler: Handlers = {
  async POST(req) {
    try {
      const signature = req.headers.get("stripe-signature") ?? undefined;
      const payload = await req.text();

      await stripeSync.processWebhook(payload, signature);

      return new Response(
        JSON.stringify({ received: true }),
        { headers: { "Content-Type": "application/json" } }
      );
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      console.error("Webhook processing failed:", message);
      return new Response(
        JSON.stringify({ error: message }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }
  },
};
```

### Cloudflare Workers (Forwarding Pattern)

Cloudflare Workers can't connect directly to PostgreSQL. Use a forwarding pattern:

```typescript
import { Hono } from 'hono';
import Stripe from 'stripe';

type Bindings = {
  STRIPE_SECRET_KEY: string;
  STRIPE_WEBHOOK_SECRET: string;
  FORWARD_SYNC_URL: string; // URL of your sync service
};

const app = new Hono<{ Bindings: Bindings }>();

app.post('/webhooks/stripe', async (c) => {
  const { STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, FORWARD_SYNC_URL } = c.env;

  const stripe = new Stripe(STRIPE_SECRET_KEY, {
    httpClient: Stripe.createFetchHttpClient(),
  });

  const payload = await c.req.text();
  const signature = c.req.header('stripe-signature');

  if (!signature) {
    return c.json({ error: 'Missing stripe-signature header' }, 400);
  }

  // Verify signature
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(payload, signature, STRIPE_WEBHOOK_SECRET);
  } catch (error) {
    return c.json({ error: 'Invalid Stripe signature' }, 400);
  }

  // Forward to sync service
  await fetch(FORWARD_SYNC_URL, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'stripe-event-id': event.id,
    },
    body: JSON.stringify(event),
  });

  return c.json({ received: true });
});

export default app;
```

## Configuring Stripe Dashboard

1. Go to [Stripe Dashboard > Webhooks](https://dashboard.stripe.com/webhooks)
2. Click **Add endpoint**
3. Enter your webhook URL:
   - Development: Use Stripe CLI (see below)
   - Production: `https://yourdomain.com/api/webhooks/stripe`
4. Select events to listen to (recommended: select "All events")
5. Copy the **Signing secret** (`whsec_...`) to your environment variables

## Local Development with Stripe CLI

Install and set up Stripe CLI:

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to your local server
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# In another terminal, trigger test events
stripe trigger payment_intent.succeeded
stripe trigger customer.created
stripe trigger invoice.paid
```

The CLI will show you a temporary webhook secret to use for local testing.

## Event Types Processed

stripe-sync-engine automatically handles these event types:

| Category | Events |
|----------|--------|
| Customers | `customer.created`, `customer.updated`, `customer.deleted` |
| Products | `product.created`, `product.updated`, `product.deleted` |
| Prices | `price.created`, `price.updated`, `price.deleted` |
| Subscriptions | `customer.subscription.*` events |
| Invoices | `invoice.*` events |
| Payments | `payment_intent.*`, `charge.*` events |
| Disputes | `charge.dispute.*` events |
| Refunds | `charge.refund.*` events |

## Adding Custom Business Logic

You can add your own logic after sync completes:

```typescript
export async function POST(request: Request) {
  const signature = request.headers.get('stripe-signature') ?? undefined;
  const payload = await request.arrayBuffer();

  // Sync to database
  await stripeSync.processWebhook(Buffer.from(payload), signature);

  // Parse event for custom logic
  const event = JSON.parse(new TextDecoder().decode(payload));

  switch (event.type) {
    case 'customer.subscription.created':
      // Send welcome email, provision access, etc.
      await handleNewSubscription(event.data.object);
      break;
    case 'invoice.payment_failed':
      // Send dunning email
      await handlePaymentFailure(event.data.object);
      break;
  }

  return NextResponse.json({ received: true });
}
```

## Troubleshooting

### Signature Verification Failed

- Ensure `STRIPE_WEBHOOK_SECRET` matches the signing secret from Stripe Dashboard
- For local testing, use the secret from `stripe listen` output
- Ensure you're passing the raw body, not parsed JSON

### Webhook Not Receiving Events

1. Check Stripe Dashboard > Webhooks for delivery attempts
2. Verify your endpoint URL is publicly accessible
3. Check server logs for errors

### Timeout Errors

- stripe-sync-engine is designed to be fast, but large payloads may take longer
- Consider increasing your serverless function timeout
- For very high volume, consider queueing events

## Related Skills

- **setup**: Install and configure stripe-sync-engine
- **migrations**: Create the database schema first
- **troubleshooting**: Debug webhook issues

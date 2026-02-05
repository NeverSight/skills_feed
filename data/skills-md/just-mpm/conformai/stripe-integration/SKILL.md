---
name: stripe-integration
description: Comprehensive guide for integrating Stripe with Firebase, Next.js, React, and TypeScript. Use when working with Stripe payments, subscriptions, webhooks, or checkout. Covers webhook setup with Firebase Cloud Functions v2, Next.js App Router webhook handling, signature verification, common errors and solutions, Stripe CLI usage, and MCP integration. Essential for setting up Stripe correctly in Firebase+Next.js+TypeScript projects.
---

# Stripe Integration Guide

Complete integration guide for Stripe with Firebase Cloud Functions v2, Next.js, React, TypeScript, and MUI v7.

## Tech Stack

This skill covers Stripe integration for projects using:
- **Backend**: Firebase Cloud Functions v2
- **Frontend**: Next.js (App Router), React, TypeScript
- **UI**: Material-UI (MUI) v7
- **Payment Provider**: Stripe
- **Dev Tools**: Stripe CLI, Stripe MCP

## Installation & Setup

### Install Stripe Dependencies

```bash
# Install Stripe Node SDK
npm install stripe

# Install types
npm install --save-dev @types/stripe

# Verify version (should be latest stable)
npm list stripe
```

### Environment Variables

Create/update `.env.local` (for Next.js):
```bash
# Stripe Keys
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...  # From Dashboard or CLI

# Firebase
NEXT_PUBLIC_FIREBASE_API_KEY=...
NEXT_PUBLIC_FIREBASE_PROJECT_ID=...
```

Create/update `.secret.local` (for Firebase Functions):
```bash
# Set secrets for Cloud Functions
firebase functions:secrets:set STRIPE_SECRET_KEY
firebase functions:secrets:set STRIPE_WEBHOOK_SECRET
```

### Initialize Stripe Client

**Frontend** (`lib/stripe.ts`):
```typescript
import { loadStripe, Stripe } from '@stripe/stripe-js';

let stripePromise: Promise<Stripe | null>;

export const getStripe = () => {
  if (!stripePromise) {
    stripePromise = loadStripe(
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
    );
  }
  return stripePromise;
};
```

**Backend** (`lib/stripe-admin.ts`):
```typescript
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-01-27.acacia', // Use latest stable version
  typescript: true,
});
```

## Webhook Integration

Webhooks are CRITICAL for Stripe integrations. Most Stripe events happen asynchronously.

### Firebase Cloud Functions v2 Webhook Handler

Create `functions/src/stripe-webhook.ts`:

```typescript
import { onRequest } from 'firebase-functions/v2/https';
import { logger } from 'firebase-functions';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-01-27.acacia',
});

export const stripeWebhook = onRequest(
  {
    secrets: ['STRIPE_WEBHOOK_SECRET', 'STRIPE_SECRET_KEY'],
    invoker: 'public', // Must be public for Stripe to call
    cors: false, // No CORS needed for server-to-server
  },
  async (req, res) => {
    // Verify method
    if (req.method !== 'POST') {
      res.status(405).send('Method Not Allowed');
      return;
    }

    const signature = req.headers['stripe-signature'] as string;

    if (!signature) {
      res.status(400).send('Missing stripe-signature header');
      return;
    }

    let event: Stripe.Event;

    try {
      // CRITICAL: Use req.rawBody for signature verification
      event = stripe.webhooks.constructEvent(
        req.rawBody!,
        signature,
        process.env.STRIPE_WEBHOOK_SECRET!
      );
    } catch (err) {
      logger.error('Webhook signature verification failed:', err);
      res.status(400).send(`Webhook Error: ${err.message}`);
      return;
    }

    // IMPORTANT: Return 200 IMMEDIATELY
    res.status(200).send({ received: true });

    // Process event asynchronously AFTER responding
    try {
      await handleStripeEvent(event);
    } catch (error) {
      logger.error('Error processing webhook:', error);
      // Don't throw - already responded to Stripe
    }
  }
);

async function handleStripeEvent(event: Stripe.Event) {
  logger.info('Processing event:', event.type);

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;
      await handleCheckoutCompleted(session);
      break;
    }

    case 'customer.subscription.created':
    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription;
      await handleSubscriptionUpdate(subscription);
      break;
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription;
      await handleSubscriptionCanceled(subscription);
      break;
    }

    case 'invoice.paid': {
      const invoice = event.data.object as Stripe.Invoice;
      await handleInvoicePaid(invoice);
      break;
    }

    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice;
      await handlePaymentFailed(invoice);
      break;
    }

    default:
      logger.info('Unhandled event type:', event.type);
  }
}

// Implement handlers
async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  // Grant access to product
  logger.info('Checkout completed:', session.id);
}

async function handleSubscriptionUpdate(subscription: Stripe.Subscription) {
  // Update subscription status in database
  logger.info('Subscription updated:', subscription.id);
}

async function handleSubscriptionCanceled(subscription: Stripe.Subscription) {
  // Revoke access
  logger.info('Subscription canceled:', subscription.id);
}

async function handleInvoicePaid(invoice: Stripe.Invoice) {
  // Confirm recurring payment
  logger.info('Invoice paid:', invoice.id);
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  // Notify customer
  logger.info('Payment failed:', invoice.id);
}
```

### Next.js App Router Webhook Handler

Create `app/api/webhooks/stripe/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-01-27.acacia',
});

export async function POST(request: NextRequest) {
  // CRITICAL: Get RAW body as text, not JSON
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  if (!signature) {
    return NextResponse.json(
      { error: 'Missing stripe-signature header' },
      { status: 400 }
    );
  }

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    return NextResponse.json(
      { error: `Webhook Error: ${err.message}` },
      { status: 400 }
    );
  }

  // Handle event
  try {
    switch (event.type) {
      case 'checkout.session.completed':
        // Handle checkout completion
        break;
      case 'customer.subscription.updated':
        // Handle subscription update
        break;
      // Add more cases as needed
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('Error processing webhook:', error);
    return NextResponse.json(
      { error: 'Webhook processing failed' },
      { status: 500 }
    );
  }
}
```

**Important**: Next.js App Router handles body parsing correctly by default. Just use `request.text()`.

### Deploying Webhook Endpoint

#### Firebase Deployment
```bash
# Deploy functions
firebase deploy --only functions:stripeWebhook

# Get function URL
firebase functions:config:get

# URL will be: https://us-central1-PROJECT_ID.cloudfunctions.net/stripeWebhook
```

#### Configure in Stripe Dashboard
1. Go to https://dashboard.stripe.com/test/webhooks
2. Click "Add endpoint"
3. Enter your webhook URL
4. Select events to listen for (or select "Send all events" for development)
5. Click "Add endpoint"
6. Copy webhook signing secret (starts with `whsec_`)
7. Add secret to environment variables

## Stripe CLI

Essential tool for local development and testing.

### Installation

Already installed if this message is seen. Verify with:
```bash
stripe --version
```

### Authentication

```bash
# Login to Stripe account
stripe login

# Generates pairing code and opens browser
# API key valid for 90 days
```

### Local Webhook Testing

**Most important CLI feature**: Forward webhooks to local development server.

```bash
# Forward all events to local endpoint
stripe listen --forward-to http://localhost:3000/api/webhooks/stripe

# Output shows webhook signing secret:
# > Ready! Your webhook signing secret is 'whsec_xxxxx'

# Use this secret in .env.local for local development
```

**In separate terminal**, trigger test events:
```bash
# Trigger specific event
stripe trigger payment_intent.succeeded

# Trigger checkout completion
stripe trigger checkout.session.completed

# Trigger with custom data
stripe trigger checkout.session.completed \
  --add checkout_session:client_reference_id=user_123

# Trigger subscription events
stripe trigger customer.subscription.created
stripe trigger customer.subscription.updated
stripe trigger customer.subscription.deleted
```

### Useful CLI Commands

```bash
# View real-time API logs
stripe logs tail

# List products
stripe products list

# Create a product
stripe products create --name="Premium Plan" --description="Monthly subscription"

# Create a price
stripe prices create \
  --product=prod_xxx \
  --unit-amount=3990 \
  --currency=brl \
  --recurring[interval]=month

# Get customer details
stripe customers retrieve cus_xxx

# List recent charges
stripe charges list --limit=10

# Refund a payment
stripe refunds create --charge=ch_xxx

# List webhook endpoints
stripe webhook_endpoints list
```

## Stripe MCP (Model Context Protocol)

MCP gives Claude direct access to Stripe data. Use for queries and operations.

### Common MCP Operations

The MCP is already configured with test credentials. Use these commands:

**Query customers:**
```
Please use the Stripe MCP to list my customers
```

**Get payment information:**
```
Use Stripe MCP to show my recent payment intents
```

**Create resources:**
```
Use Stripe MCP to create a new product called "Pro Plan"
```

**Check subscription status:**
```
Use Stripe MCP to check subscription status for customer cus_xxx
```

MCP is ideal for:
- Quick data lookups
- Testing integrations
- Creating test data
- Debugging payment issues

## TypeScript Best Practices

### Type Event Objects Correctly

```typescript
// Strongly type event data
switch (event.type) {
  case 'checkout.session.completed': {
    const session = event.data.object as Stripe.Checkout.Session;
    // TypeScript now knows session properties
    break;
  }
  
  case 'customer.subscription.updated': {
    const subscription = event.data.object as Stripe.Subscription;
    // Access subscription.status, subscription.items, etc.
    break;
  }
}
```

### Handle Expanded Objects

```typescript
// When using expand parameter
const session = await stripe.checkout.sessions.retrieve(
  sessionId,
  { expand: ['subscription', 'customer'] }
);

// Type assertion for expanded properties
const subscription = session.subscription as Stripe.Subscription;
const customer = session.customer as Stripe.Customer;

// Or type check
if (typeof session.subscription !== 'string') {
  // session.subscription is Stripe.Subscription
}
```

### Custom Types

```typescript
// Define custom types for your application
interface UserSubscription {
  stripeCustomerId: string;
  stripeSubscriptionId: string;
  status: Stripe.Subscription.Status;
  priceId: string;
  currentPeriodEnd: number;
}
```

## Common Workflows

### Creating a Checkout Session

```typescript
import { stripe } from '@/lib/stripe-admin';

export async function createCheckoutSession(userId: string, priceId: string) {
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [
      {
        price: priceId,
        quantity: 1,
      },
    ],
    success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
    client_reference_id: userId, // Link to your user
    metadata: {
      userId,
    },
  });

  return session;
}
```

### Managing Subscriptions

```typescript
// Get subscription
const subscription = await stripe.subscriptions.retrieve('sub_xxx');

// Update subscription
await stripe.subscriptions.update('sub_xxx', {
  items: [{
    id: subscription.items.data[0].id,
    price: 'price_new',
  }],
});

// Cancel subscription
await stripe.subscriptions.cancel('sub_xxx');

// Cancel at period end
await stripe.subscriptions.update('sub_xxx', {
  cancel_at_period_end: true,
});
```

## Reference Files

This skill includes detailed reference files:

- **`webhook-events.md`**: Complete list of Stripe webhook events, when to use each, and handling best practices
- **`common-errors.md`**: Comprehensive error guide with solutions for signature verification, Firebase issues, TypeScript errors, and more

Read these files when:
- Setting up webhooks (webhook-events.md)
- Debugging issues (common-errors.md)
- Choosing which events to listen to (webhook-events.md)
- Encountering errors (common-errors.md)

## Critical Reminders

1. **Webhook signatures**: Use correct secret (CLI for local, Dashboard for production)
2. **Raw body**: Never parse body before signature verification
3. **Return 200 immediately**: Process webhooks asynchronously
4. **Handle duplicates**: Log event IDs to prevent duplicate processing
5. **Test mode vs Live mode**: Keep keys and resources separate
6. **Event ordering**: Don't rely on event delivery order
7. **Error handling**: Catch and log errors, don't let exceptions break webhook processing

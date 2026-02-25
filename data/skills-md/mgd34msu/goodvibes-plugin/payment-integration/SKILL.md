---
name: payment-integration
description: "Load PROACTIVELY when task involves payments, billing, or subscriptions. Use when user says \"add payments\", \"integrate Stripe\", \"set up subscriptions\", \"add a checkout flow\", or \"handle billing webhooks\". Covers Stripe, LemonSqueezy, and Paddle integration, checkout sessions, subscription lifecycle management, webhook verification and handling, customer portal, metered billing, refunds, and PCI compliance considerations."
metadata:
  version: 1.0.0
  category: outcome
  tags: [payments, stripe, lemonsqueezy, paddle, checkout, subscriptions, webhooks]
---

## Resources
```
scripts/
  validate-payments.sh
references/
  payment-patterns.md
```

# Payment Integration Implementation

This skill guides you through implementing payment processing in applications, from provider selection to webhook handling. It leverages GoodVibes precision tools for secure, production-ready payment integrations.

## When to Use This Skill

Use this skill when you need to:

- Set up payment processing (one-time or recurring)
- Implement checkout flows and payment forms
- Handle subscription billing and management
- Process payment webhooks securely
- Test payment flows in development
- Ensure PCI compliance and security
- Migrate between payment providers

## Workflow

Follow this sequence for payment integration:

### 1. Discover Existing Payment Infrastructure

Before implementing payment features, understand the current state:

```yaml
precision_grep:
  queries:
    - id: payment-libs
      pattern: "stripe|lemonsqueezy|paddle"
      glob: "package.json"
    - id: webhook-routes
      pattern: "(webhook|payment|checkout)"
      glob: "src/**/*.{ts,js,tsx,jsx}"
  output:
    format: files_only
```

Check for:
- Existing payment libraries
- Webhook endpoints
- Environment variables for API keys
- Payment-related database models

**Check project memory for payment decisions:**

```yaml
precision_read:
  files:
    - path: ".goodvibes/memory/decisions.md"
      extract: content
  output:
    format: minimal
```

Search for payment provider choices, checkout flow patterns, and subscription models.

### 2. Select Payment Provider

Choose based on your requirements:

**Use Stripe when:**
- You need maximum flexibility and control
- Supporting complex subscription models
- Requiring advanced features (invoicing, tax, fraud detection)
- Building custom payment flows
- Need extensive API documentation

**Use LemonSqueezy when:**
- You're selling digital products/SaaS
- Want merchant of record (handles taxes, VAT, compliance)
- Need simple subscription management
- Prefer minimal compliance burden
- Operating globally with automatic tax handling

**Use Paddle when:**
- Selling software/SaaS products
- Need merchant of record services
- Want subscription and license management
- Prefer revenue recovery features
- Operating in B2B/enterprise markets

**Document the decision:**

```yaml
precision_write:
  files:
    - path: ".goodvibes/memory/decisions.md"
      mode: overwrite
      content: |
        ## Payment Provider Selection
        
        **Decision**: Using [Provider] for payment processing
        **Rationale**: [Why this provider fits requirements]
        **Date**: YYYY-MM-DD
        
        Key factors:
        - [Factor 1]
        - [Factor 2]
        - [Factor 3]
```

### 3. Setup and Installation

Install the appropriate SDK:

**Stripe:**

```yaml
precision_exec:
  commands:
    - cmd: "npm install stripe @stripe/stripe-js"
    # @types/stripe is not needed - Stripe ships with built-in types
  verbosity: minimal
```

**LemonSqueezy:**

```yaml
precision_exec:
  commands:
    - cmd: "npm install @lemonsqueezy/lemonsqueezy.js"
  verbosity: minimal
```

**Paddle:**

```yaml
precision_exec:
  commands:
    - cmd: "npm install @paddle/paddle-node-sdk"
  verbosity: minimal
```

**Configure environment variables:**

Create `.env.example` template:

```yaml
precision_write:
  files:
    - path: ".env.example"
      mode: overwrite
      content: |
        # Payment Provider Configuration
        
        # Stripe (if using Stripe)
        STRIPE_SECRET_KEY=sk_test_...
        STRIPE_PUBLISHABLE_KEY=pk_test_...
        STRIPE_WEBHOOK_SECRET=whsec_...
        
        # LemonSqueezy (if using LemonSqueezy)
        LEMONSQUEEZY_API_KEY=...
        LEMONSQUEEZY_STORE_ID=...
        LEMONSQUEEZY_WEBHOOK_SECRET=...
        
        # Paddle (if using Paddle)
        PADDLE_API_KEY=...
        PADDLE_WEBHOOK_SECRET=...
        PADDLE_ENVIRONMENT=sandbox
```

**Verify secrets are gitignored:**

```yaml
precision_grep:
  queries:
    - id: check-gitignore
      pattern: "^\\.env$"
      path: ".gitignore"
  output:
    format: files_only
```

If not found, add `.env` to `.gitignore`.

### 4. Implement Checkout Flow

#### One-Time Payments (Stripe)

Create checkout session endpoint:

```yaml
precision_write:
  files:
    - path: "src/app/api/checkout/route.ts"
      content: |
        import { NextRequest, NextResponse } from 'next/server';
        import Stripe from 'stripe';
        import { getServerSession } from 'next-auth';
        import { authOptions } from '@/lib/auth';
        import { z } from 'zod';
        
        const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
        if (!stripeSecretKey) {
          throw new Error('STRIPE_SECRET_KEY is required');
        }
        
        const stripe = new Stripe(stripeSecretKey, {
          apiVersion: '2024-11-20.acacia',
        });
        
        export async function POST(request: NextRequest) {
          try {
            // Check authentication
            const authSession = await getServerSession();
            if (!authSession?.user) {
              return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
              );
            }
            
            // Validate input with Zod
            const schema = z.object({
              priceId: z.string().min(1),
              successUrl: z.string().url(),
              cancelUrl: z.string().url(),
            });
            
            const body = await request.json();
            const result = schema.safeParse(body);
            
            if (!result.success) {
              return NextResponse.json(
                { error: 'Invalid input', details: result.error.flatten() },
                { status: 400 }
              );
            }
            
            const { priceId, successUrl, cancelUrl } = result.data;
            
            // Validate URLs against allowed origins
            const appUrl = process.env.NEXT_PUBLIC_APP_URL;
            if (!appUrl) throw new Error('NEXT_PUBLIC_APP_URL is required');
            const allowedOrigins = [appUrl];
            const successOrigin = new URL(successUrl).origin;
            const cancelOrigin = new URL(cancelUrl).origin;
            
            if (!allowedOrigins.includes(successOrigin) || !allowedOrigins.includes(cancelOrigin)) {
              return NextResponse.json(
                { error: 'Invalid redirect URLs' },
                { status: 400 }
              );
            }
            
            const stripeSession = await stripe.checkout.sessions.create({
              mode: 'payment',
              line_items: [
                {
                  price: priceId,
                  quantity: 1,
                },
              ],
              success_url: successUrl,
              cancel_url: cancelUrl,
              metadata: {
                userId: authSession.user.id,
              },
            });
            
            return NextResponse.json({ sessionId: stripeSession.id });
          } catch (error: unknown) {
            const message = error instanceof Error ? error.message : 'Unknown error';
            console.error('Checkout error:', message);
            return NextResponse.json(
              { error: 'Failed to create checkout session' },
              { status: 500 }
            );
          }
        }
```

#### One-Time Payments (LemonSqueezy)

```yaml
precision_write:
  files:
    - path: "src/app/api/checkout/route.ts"
      content: |
        import { NextRequest, NextResponse } from 'next/server';
        import { lemonSqueezySetup, createCheckout } from '@lemonsqueezy/lemonsqueezy.js';
        import { getServerSession } from 'next-auth';
        import { authOptions } from '@/lib/auth';
        
        const lemonSqueezyApiKey = process.env.LEMONSQUEEZY_API_KEY;
        if (!lemonSqueezyApiKey) {
          throw new Error('LEMONSQUEEZY_API_KEY is required');
        }
        lemonSqueezySetup({ apiKey: lemonSqueezyApiKey });
        
        export async function POST(request: NextRequest) {
          try {
            const authSession = await getServerSession(authOptions);
            if (!authSession?.user) {
              return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
            }
            
            const { variantId, email } = await request.json();
            
            const lemonSqueezyStoreId = process.env.LEMONSQUEEZY_STORE_ID;
            if (!lemonSqueezyStoreId) {
              throw new Error('LEMONSQUEEZY_STORE_ID is required');
            }
            
            const { data, error } = await createCheckout(
              lemonSqueezyStoreId,
              variantId,
              {
                checkoutData: {
                  email,
                  custom: {
                    user_id: authSession.user.id,
                  },
                },
              }
            );
            
            if (error) {
              throw new Error(error.message);
            }
            
            return NextResponse.json({ checkoutUrl: data.attributes.url });
          } catch (error: unknown) {
            const message = error instanceof Error ? error.message : 'Unknown error';
            console.error('Checkout error:', message);
            return NextResponse.json(
              { error: 'Failed to create checkout' },
              { status: 500 }
            );
          }
        }
```

### 5. Subscription Billing

#### Create Subscription Plans (Stripe)

```yaml
precision_write:
  files:
    - path: "src/lib/stripe/plans.ts"
      content: |
        export const SUBSCRIPTION_PLANS = {
          starter: {
            name: 'Starter',
            priceId: (() => {
              const priceId = process.env.STRIPE_PRICE_STARTER;
              if (!priceId) throw new Error('STRIPE_PRICE_STARTER is required');
              return priceId;
            })(),
            price: 9,
            interval: 'month' as const,
            features: ['Feature 1', 'Feature 2'],
          },
          pro: {
            name: 'Pro',
            priceId: (() => {
              const priceId = process.env.STRIPE_PRICE_PRO;
              if (!priceId) throw new Error('STRIPE_PRICE_PRO is required');
              return priceId;
            })(),
            price: 29,
            interval: 'month' as const,
            features: ['All Starter features', 'Feature 3', 'Feature 4'],
          },
        } as const;
        
        export type PlanId = keyof typeof SUBSCRIPTION_PLANS;
```

#### Subscription Checkout

```yaml
precision_write:
  files:
    - path: "src/app/api/subscribe/route.ts"
      content: |
        import { NextRequest, NextResponse } from 'next/server';
        import Stripe from 'stripe';
        import { z } from 'zod';
        import { SUBSCRIPTION_PLANS } from '@/lib/stripe/plans';
        import { getServerSession } from 'next-auth';
        import { authOptions } from '@/lib/auth';
        
        // Validate required environment variables
        const secretKey = process.env.STRIPE_SECRET_KEY;
        if (!secretKey) throw new Error('STRIPE_SECRET_KEY is required');
        const stripe = new Stripe(secretKey, {
          apiVersion: '2024-11-20.acacia',
        });
        
        const subscribeSchema = z.object({
          planId: z.string().min(1),
          customerId: z.string().min(1),
          successUrl: z.string().url(),
          cancelUrl: z.string().url(),
        });
        
        export async function POST(request: NextRequest) {
          try {
            const authSession = await getServerSession(authOptions);
            if (!authSession?.user) {
              return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
            }
            
            const body = await request.json();
            const result = subscribeSchema.safeParse(body);
            
            if (!result.success) {
              return NextResponse.json(
                { error: result.error.flatten() },
                { status: 400 }
              );
            }
            
            const { planId, customerId, successUrl, cancelUrl } = result.data;
            
            const plan = SUBSCRIPTION_PLANS[planId as keyof typeof SUBSCRIPTION_PLANS];
            if (!plan) {
              return NextResponse.json({ error: 'Invalid plan' }, { status: 400 });
            }
            
            const stripeSession = await stripe.checkout.sessions.create({
              mode: 'subscription',
              customer: customerId,
              line_items: [
                {
                  price: plan.priceId,
                  quantity: 1,
                },
              ],
              success_url: successUrl,
              cancel_url: cancelUrl,
              subscription_data: {
                trial_period_days: 14,
              },
            });
            
            return NextResponse.json({ sessionId: stripeSession.id });
          } catch (error: unknown) {
            const message = error instanceof Error ? error.message : 'Unknown error';
            console.error('Subscription error:', message);
            return NextResponse.json(
              { error: 'Failed to create subscription' },
              { status: 500 }
            );
          }
        }
```

#### Manage Subscriptions

```yaml
precision_write:
  files:
    - path: "src/app/api/subscription/manage/route.ts"
      content: |
        import { NextRequest, NextResponse } from 'next/server';
        import Stripe from 'stripe';
        import { getServerSession } from 'next-auth';
        import { authOptions } from '@/lib/auth';
        
        const secretKey = process.env.STRIPE_SECRET_KEY;
        if (!secretKey) throw new Error('STRIPE_SECRET_KEY is required');
        const stripe = new Stripe(secretKey, {
          apiVersion: '2024-11-20.acacia',
        });
        
        // Cancel subscription
        export async function DELETE(request: NextRequest) {
          try {
            const authSession = await getServerSession(authOptions);
            if (!authSession?.user) {
              return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
            }
            
            const { subscriptionId } = await request.json();
            
            const subscription = await stripe.subscriptions.update(subscriptionId, {
              cancel_at_period_end: true,
            });
            
            return NextResponse.json({ subscription });
          } catch (error: unknown) {
            const message = error instanceof Error ? error.message : 'Unknown error';
            console.error('Cancel error:', message);
            return NextResponse.json(
              { error: 'Failed to cancel subscription' },
              { status: 500 }
            );
          }
        }
        
        // Update subscription
        export async function PATCH(request: NextRequest) {
          try {
            const authSession = await getServerSession(authOptions);
            if (!authSession?.user) {
              return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
            }
            
            const { subscriptionId, newPriceId } = await request.json();
            
            const subscription = await stripe.subscriptions.retrieve(subscriptionId);
            
            const updated = await stripe.subscriptions.update(subscriptionId, {
              items: [
                {
                  id: subscription.items.data[0].id,
                  price: newPriceId,
                },
              ],
              proration_behavior: 'create_prorations',
            });
            
            return NextResponse.json({ subscription: updated });
          } catch (error: unknown) {
            const message = error instanceof Error ? error.message : 'Unknown error';
            console.error('Update error:', message);
            return NextResponse.json(
              { error: 'Failed to update subscription' },
              { status: 500 }
            );
          }
        }
```

### 6. Webhook Handling

Webhooks are critical for payment processing. They notify your application of payment events.

#### Stripe Webhook Handler

```yaml
precision_write:
  files:
    - path: "src/app/api/webhooks/stripe/route.ts"
      content: |
        import { NextRequest, NextResponse } from 'next/server';
        import Stripe from 'stripe';
        import { headers } from 'next/headers';
        import { db } from '@/lib/db';
        
        const secretKey = process.env.STRIPE_SECRET_KEY;
        if (!secretKey) throw new Error('STRIPE_SECRET_KEY is required');
        const stripe = new Stripe(secretKey, {
          apiVersion: '2024-11-20.acacia',
        });
        
        const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
        if (!webhookSecret) {
          throw new Error('STRIPE_WEBHOOK_SECRET is required');
        }
        
        export async function POST(request: NextRequest) {
          const body = await request.text();
          const headersList = await headers();
          const signature = headersList.get('stripe-signature');
          
          if (!signature) {
            return NextResponse.json(
              { error: 'Missing stripe-signature header' },
              { status: 400 }
            );
          }
          
          let event: Stripe.Event;
          
          try {
            // Verify webhook signature
            event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
          } catch (error: unknown) {
            const message = error instanceof Error ? error.message : 'Unknown error';
            console.error('Webhook signature verification failed:', message);
            return NextResponse.json(
              { error: 'Invalid signature' },
              { status: 400 }
            );
          }
          
          // Handle the event
          try {
            switch (event.type) {
              case 'checkout.session.completed': {
                const session = event.data.object as Stripe.Checkout.Session;
                await handleCheckoutComplete(session);
                break;
              }
                
              case 'customer.subscription.created': {
                const subscription = event.data.object as Stripe.Subscription;
                await handleSubscriptionCreated(subscription);
                break;
              }
                
              case 'customer.subscription.updated':
                await handleSubscriptionUpdated(event.data.object as Stripe.Subscription);
                break;
                
              case 'customer.subscription.deleted':
                await handleSubscriptionCanceled(event.data.object as Stripe.Subscription);
                break;
                
              case 'invoice.payment_succeeded':
                await handlePaymentSucceeded(event.data.object as Stripe.Invoice);
                break;
                
              case 'invoice.payment_failed':
                await handlePaymentFailed(event.data.object as Stripe.Invoice);
                break;
                
              default:
                // Replace with structured logger in production
                console.log(`Unhandled event type: ${event.type}`);
            }
            
            return NextResponse.json({ received: true });
          } catch (error: unknown) {
            const message = error instanceof Error ? error.message : 'Unknown error';
            console.error('Webhook handler error:', message);
            return NextResponse.json(
              { error: 'Webhook handler failed' },
              { status: 500 }
            );
          }
        }
        
        async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
          // Update database with payment details
          await db.payment.create({
            data: {
              id: session.payment_intent as string,
              userId: session.metadata?.userId,
              amount: session.amount_total ?? 0,
              currency: session.currency ?? 'usd',
              status: 'succeeded',
            },
          });
          // Grant access to product/service based on metadata
        }
        
        async function handleSubscriptionCreated(subscription: Stripe.Subscription) {
          // Create subscription record in database
          await db.subscription.create({
            data: {
              id: subscription.id,
              userId: subscription.metadata?.userId,
              status: subscription.status,
              currentPeriodEnd: new Date(subscription.current_period_end * 1000),
            },
          });
        }
        
        async function handleSubscriptionUpdated(subscription: Stripe.Subscription) {
          // Update subscription status in database
          await db.subscription.update({
            where: { id: subscription.id },
            data: {
              status: subscription.status,
              currentPeriodEnd: new Date(subscription.current_period_end * 1000),
            },
          });
        }
        
        async function handleSubscriptionCanceled(subscription: Stripe.Subscription) {
          // Mark subscription as canceled in database
          await db.subscription.update({
            where: { id: subscription.id },
            data: {
              status: 'canceled',
              canceledAt: new Date(),
            },
          });
          // Revoke access at period end
        }
        
        async function handlePaymentSucceeded(invoice: Stripe.Invoice) {
          // Record successful payment
          await db.payment.create({
            data: {
              id: invoice.payment_intent as string,
              userId: invoice.subscription_details?.metadata?.userId,
              amount: invoice.amount_paid,
              currency: invoice.currency,
              status: 'succeeded',
            },
          });
        }
        
        async function handlePaymentFailed(invoice: Stripe.Invoice) {
          // Notify user of failed payment
          await db.payment.create({
            data: {
              id: invoice.payment_intent as string,
              userId: invoice.subscription_details?.metadata?.userId,
              amount: invoice.amount_due,
              currency: invoice.currency,
              status: 'failed',
            },
          });
          // Send notification email
        }
```

#### LemonSqueezy Webhook Handler

```yaml
precision_write:
  files:
    - path: "src/app/api/webhooks/lemonsqueezy/route.ts"
      content: |
        import { NextRequest, NextResponse } from 'next/server';
        import crypto from 'crypto';
        import { db } from '@/lib/db';
        
        const webhookSecret = process.env.LEMONSQUEEZY_WEBHOOK_SECRET;
        if (!webhookSecret) {
          throw new Error('LEMONSQUEEZY_WEBHOOK_SECRET is required');
        }
        
        export async function POST(request: NextRequest) {
          const body = await request.text();
          const signature = request.headers.get('x-signature');
          
          if (!signature) {
            return NextResponse.json({ error: 'Missing signature' }, { status: 400 });
          }
          
          // Verify webhook signature
          const hmac = crypto.createHmac('sha256', webhookSecret);
          const digest = hmac.update(body).digest('hex');
          
          const signatureBuffer = Buffer.from(signature, 'utf8');
          const digestBuffer = Buffer.from(digest, 'utf8');
          if (signatureBuffer.length !== digestBuffer.length || !crypto.timingSafeEqual(signatureBuffer, digestBuffer)) {
            console.error('Webhook signature verification failed');
            return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
          }
          
          const event = JSON.parse(body);
          
          try {
            switch (event.meta.event_name) {
              case 'order_created':
                await handleOrderCreated(event.data);
                break;
                
              case 'subscription_created':
                await handleSubscriptionCreated(event.data);
                break;
                
              case 'subscription_updated':
                await handleSubscriptionUpdated(event.data);
                break;
                
              case 'subscription_cancelled':
                await handleSubscriptionCancelled(event.data);
                break;
                
              case 'subscription_payment_success':
                await handlePaymentSuccess(event.data);
                break;
                
              default:
                // Replace with structured logger in production
                console.log(`Unhandled event: ${event.meta.event_name}`);
            }
            
            return NextResponse.json({ received: true });
          } catch (error: unknown) {
            const message = error instanceof Error ? error.message : 'Unknown error';
            console.error('Webhook handler error:', message);
            return NextResponse.json(
              { error: 'Webhook handler failed' },
              { status: 500 }
            );
          }
        }
        
        interface LemonSqueezyWebhookData {
          id: string;
          attributes: Record<string, unknown>;
        }
        
        async function handleOrderCreated(data: LemonSqueezyWebhookData) {
          await db.order.create({
            data: {
              id: data.id,
              status: 'completed',
              attributes: data.attributes,
            },
          });
        }
        
        async function handleSubscriptionCreated(data: LemonSqueezyWebhookData) {
          await db.subscription.create({
            data: {
              id: data.id,
              status: 'active',
              userId: data.attributes.user_id as string,
              attributes: data.attributes,
            },
          });
        }
        
        async function handleSubscriptionUpdated(data: LemonSqueezyWebhookData) {
          await db.subscription.update({
            where: { id: data.id },
            data: {
              status: data.attributes.status as string,
              attributes: data.attributes,
            },
          });
        }
        
        async function handleSubscriptionCancelled(data: LemonSqueezyWebhookData) {
          await db.subscription.update({
            where: { id: data.id },
            data: {
              status: 'cancelled',
              cancelledAt: new Date(),
            },
          });
        }
        
        async function handlePaymentSuccess(data: LemonSqueezyWebhookData) {
          await db.payment.create({
            data: {
              id: data.id,
              status: 'succeeded',
              amount: data.attributes.total as number,
              attributes: data.attributes,
            },
          });
        }
```

#### Webhook Idempotency

Always implement idempotency to handle duplicate webhook deliveries:

```yaml
precision_write:
  files:
    - path: "src/lib/webhooks/idempotency.ts"
      content: |
        import { db } from '@/lib/db';
        
        export async function isProcessed(eventId: string): Promise<boolean> {
          const existing = await db.webhookEvent.findUnique({
            where: { id: eventId },
          });
          
          return !!existing;
        }
        
        export async function markProcessed(eventId: string): Promise<void> {
          await db.webhookEvent.create({
            data: {
              id: eventId,
              processedAt: new Date(),
            },
          });
        }
        
        export async function withIdempotency<T>(
          eventId: string,
          handler: () => Promise<T>
        ): Promise<T | null> {
          // Use database transaction to prevent TOCTOU race condition
          return db.$transaction(async (tx) => {
            const existing = await tx.webhookEvent.findUnique({
              where: { id: eventId },
            });
            
            if (existing) {
              // Replace with structured logger in production
              console.log(`Event ${eventId} already processed, skipping`);
              return null;
            }
            
            const result = await handler();
            
            await tx.webhookEvent.create({
              data: {
                id: eventId,
                processedAt: new Date(),
              },
            });
            
            return result;
          });
        }
```

Update webhook handlers to use idempotency:

```typescript
// In Stripe webhook
const eventId = event.id;
await withIdempotency(eventId, async () => {
  // Handle event
});
```

### 7. Testing Payment Flows

#### Use Test Mode Keys

Always use test mode keys in development:

```yaml
precision_grep:
  queries:
    - id: check-test-keys
      pattern: "(sk_test|pk_test)"
      path: ".env"
  output:
    format: files_only
```

#### Stripe CLI for Webhook Testing

Install and configure Stripe CLI:

```yaml
precision_exec:
  commands:
    - cmd: "stripe listen --forward-to localhost:3000/api/webhooks/stripe"
  background: true
  verbosity: minimal
```

#### Test Card Numbers

Document test card numbers in development docs:

```yaml
precision_write:
  files:
    - path: "docs/testing-payments.md"
      content: |
        # Payment Testing Guide
        
        ## Test Cards (Stripe)
        
        - Success: 4242 4242 4242 4242
        - Decline: 4000 0000 0000 0002
        - Requires authentication: 4000 0025 0000 3155
        - Insufficient funds: 4000 0000 0000 9995
        
        Use any future expiry date and any 3-digit CVC.
        
        ## Test Webhooks
        
        1. Start webhook listener: `stripe listen --forward-to localhost:3000/api/webhooks/stripe`
        2. Trigger events: `stripe trigger payment_intent.succeeded`
        
        ## LemonSqueezy Testing
        
        Use sandbox mode in .env:
        LEMONSQUEEZY_API_KEY=... (sandbox key)
```

#### Automated Testing

Create tests for webhook handlers:

```yaml
precision_write:
  files:
    - path: "src/__tests__/webhooks/stripe.test.ts"
      content: |
        import { POST } from '@/app/api/webhooks/stripe/route';
        import { NextRequest } from 'next/server';
        import Stripe from 'stripe';
        
        describe('Stripe Webhook Handler', () => {
          it('should verify webhook signature', async () => {
            const mockEvent = {
              id: 'evt_test_123',
              type: 'checkout.session.completed',
              data: { object: {} },
            };
            
            const request = new NextRequest('http://localhost:3000/api/webhooks/stripe', {
              method: 'POST',
              body: JSON.stringify(mockEvent),
              headers: {
                'stripe-signature': 'invalid_signature',
              },
            });
            
            const response = await POST(request);
            expect(response.status).toBe(400);
          });
          
          it('should handle checkout.session.completed', async () => {
            // Test event handling
          });
        });
```

### 8. Security and PCI Compliance

#### Never Handle Card Data Directly

Use hosted checkout pages or Elements to keep card data out of your servers:

```yaml
precision_grep:
  queries:
    - id: check-card-handling
      pattern: "(card_number|cvv|cvc|card.*exp)"
      glob: "src/**/*.{ts,js,tsx,jsx}"
  output:
    format: files_only
```

If any matches are found, refactor to use provider's hosted solutions.

#### Enforce HTTPS

```yaml
precision_write:
  files:
    - path: "src/middleware.ts"
      content: |
        import { NextRequest, NextResponse } from 'next/server';
        
        export function middleware(request: NextRequest) {
          // Enforce HTTPS in production
          if (
            process.env.NODE_ENV === 'production' &&
            request.headers.get('x-forwarded-proto') !== 'https'
          ) {
            return NextResponse.redirect(
              `https://${request.headers.get('host')}${request.nextUrl.pathname}`,
              301
            );
          }
          
          return NextResponse.next();
        }
        
        export const config = {
          matcher: '/api/checkout/:path*',
        };
```

#### Secure API Keys

Verify API keys are not hardcoded:

```yaml
precision_grep:
  queries:
    - id: hardcoded-keys
      pattern: "(sk_live|sk_test)_[a-zA-Z0-9]{24,}"
      glob: "src/**/*.{ts,js,tsx,jsx}"
  output:
    format: files_only
```

If found, move to environment variables immediately.

#### Content Security Policy

Add CSP headers for payment pages:

```yaml
precision_write:
  files:
    - path: "next.config.js"
      mode: overwrite
      content: |
        module.exports = {
          async headers() {
            return [
              {
                source: '/(checkout|subscribe)/:path*',
                headers: [
                  {
                    key: 'Content-Security-Policy',
                    value: [
                      "default-src 'self'",
                      "script-src 'self' 'unsafe-inline' https://js.stripe.com",
                      "frame-src https://js.stripe.com",
                      "connect-src 'self' https://api.stripe.com",
                    ].join('; '),
                  },
                ],
              },
            ];
          },
        };
```

### 9. Validation

Run the validation script to ensure best practices:

```yaml
precision_exec:
  commands:
    - cmd: "bash plugins/goodvibes/skills/outcome/payment-integration/scripts/validate-payments.sh ."
      expect:
        exit_code: 0
  verbosity: standard
```

The script checks:
- Payment library installation
- API keys in .env.example (not .env)
- Webhook endpoint exists
- Webhook signature verification
- No hardcoded secrets
- HTTPS enforcement
- Error handling

### 10. Database Schema for Payments

Add payment tracking to your database:

```prisma
model Customer {
  id              String   @id @default(cuid())
  userId          String   @unique
  stripeCustomerId String?  @unique
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt
  
  subscriptions   Subscription[]
  payments        Payment[]
  
  @@index([stripeCustomerId])
}

model Subscription {
  id                   String   @id @default(cuid())
  customerId           String
  customer             Customer @relation(fields: [customerId], references: [id])
  stripeSubscriptionId String   @unique
  stripePriceId        String
  status               String
  currentPeriodEnd     DateTime
  cancelAtPeriodEnd    Boolean  @default(false)
  createdAt            DateTime @default(now())
  updatedAt            DateTime @updatedAt
  
  @@index([customerId])
  @@index([status])
}

model Payment {
  id              String   @id @default(cuid())
  customerId      String
  customer        Customer @relation(fields: [customerId], references: [id])
  stripePaymentId String   @unique
  amount          Int
  currency        String
  status          String
  createdAt       DateTime @default(now())
  
  @@index([customerId])
  @@index([status])
}

model WebhookEvent {
  id          String   @id
  processedAt DateTime @default(now())
  
  @@index([processedAt])
}
```

## Common Patterns

### Pattern: Proration on Plan Changes

When upgrading/downgrading subscriptions:

```typescript
const updated = await stripe.subscriptions.update(subscriptionId, {
  items: [{ id: itemId, price: newPriceId }],
  proration_behavior: 'create_prorations', // Credit/charge immediately
});
```

### Pattern: Trial Periods

Offer free trials:

```typescript
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  subscription_data: {
    trial_period_days: 14,
    trial_settings: {
      end_behavior: {
        missing_payment_method: 'cancel', // Cancel if no payment method
      },
    },
  },
});
```

### Pattern: Webhook Retry Logic

Payment providers retry failed webhooks. Always:
- Return 200 OK quickly (process async if needed)
- Implement idempotency
- Log all webhook events

### Pattern: Failed Payment Recovery

Handle dunning (failed payment recovery):

```typescript
case 'invoice.payment_failed':
  const invoice = event.data.object as Stripe.Invoice;
  if (invoice.attempt_count >= 3) {
    // Cancel subscription after 3 failures
    await stripe.subscriptions.cancel(invoice.subscription as string);
    await notifyCustomer(invoice.customer as string, 'payment_failed_final');
  } else {
    await notifyCustomer(invoice.customer as string, 'payment_failed_retry');
  }
  break;
```

## Anti-Patterns to Avoid

### DON'T: Store Card Details

Never store card numbers, CVV, or full card data. Use tokenization.

### DON'T: Skip Webhook Verification

Always verify webhook signatures. Unverified webhooks are a security risk.

### DON'T: Use Client-Side Pricing

Never trust prices from the client. Always use server-side price lookup:

```typescript
// BAD
const { amount } = await request.json();
await stripe.charges.create({ amount });

// GOOD
const { priceId } = await request.json();
const price = await stripe.prices.retrieve(priceId);
await stripe.charges.create({ amount: price.unit_amount });
```

### DON'T: Ignore Failed Webhooks

Monitor webhook delivery and investigate failures. Set up alerts.

### DON'T: Hardcode Currency

Support multiple currencies if serving international customers:

```typescript
const session = await stripe.checkout.sessions.create({
  currency: userCountry === 'US' ? 'usd' : 'eur',
});
```

## References

See `references/payment-patterns.md` for:
- Provider comparison table
- Complete webhook event reference
- Subscription lifecycle state machine
- Testing strategies
- Security checklist

## Next Steps

After implementing payment integration:

1. **Test thoroughly** - Use test mode, simulate failures
2. **Monitor webhooks** - Set up logging and alerting
3. **Document flows** - Create internal docs for payment processes
4. **Plan for scale** - Consider rate limits, concurrent webhooks
5. **Implement analytics** - Track conversion rates, churn
6. **Review compliance** - Ensure PCI-DSS compliance if applicable
7. **Set up monitoring** - Track payment success rates, errors

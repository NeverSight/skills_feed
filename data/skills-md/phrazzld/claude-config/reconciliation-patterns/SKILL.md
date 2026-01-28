---
name: reconciliation-patterns
description: "Patterns for syncing state between external services (Stripe, Clerk) and local database. Invoke for: webhook failures, data sync issues, eventual consistency, recovery from missed events, subscription state management."
---

# Reconciliation Patterns

Patterns for maintaining data consistency between external services and your database when webhooks fail or events are missed.

## The Problem

External services (Stripe, Clerk, etc.) notify your app via webhooks. But webhooks can:
- Fail silently (wrong URL, network issues)
- Be delivered out of order
- Be duplicated
- Miss events entirely

**Result**: Your database state diverges from source of truth.

## Core Principle

**Webhooks for speed, reconciliation for correctness.**

1. Process webhooks for real-time updates (optimistic)
2. Run periodic reconciliation to catch and fix drift (defensive)

## Pattern 1: Scheduled Reconciliation

Run cron job to compare local state with external service.

```typescript
// Convex scheduled function
export const reconcileSubscriptions = internalAction({
  handler: async (ctx) => {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

    // Get all active subscriptions from Stripe
    const stripeSubscriptions = await stripe.subscriptions.list({
      status: 'all',
      limit: 100,
    })

    // Get all users from our database
    const users = await ctx.runQuery(internal.users.listWithStripeId)

    for (const user of users) {
      const stripeSub = stripeSubscriptions.data.find(
        (s) => s.customer === user.stripeCustomerId
      )

      const expectedStatus = stripeSub?.status ?? 'none'

      if (user.subscriptionStatus !== expectedStatus) {
        console.log(`Drift detected: user ${user._id}`, {
          local: user.subscriptionStatus,
          stripe: expectedStatus,
        })

        await ctx.runMutation(internal.users.updateSubscriptionStatus, {
          userId: user._id,
          status: expectedStatus,
          subscriptionId: stripeSub?.id,
        })
      }
    }
  },
})

// Schedule: Run every hour
// crons.ts
export default {
  reconcileSubscriptions: {
    schedule: "0 * * * *",  // Every hour
    handler: internal.reconciliation.reconcileSubscriptions,
  },
}
```

## Pattern 2: On-Demand Reconciliation

Reconcile specific user when they report issues.

```typescript
export const reconcileUser = action({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    const user = await ctx.runQuery(internal.users.get, { id: args.userId })
    if (!user?.stripeCustomerId) return { status: "no_stripe_customer" }

    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

    // Fetch current state from Stripe
    const customer = await stripe.customers.retrieve(user.stripeCustomerId, {
      expand: ['subscriptions'],
    })

    if (customer.deleted) {
      await ctx.runMutation(internal.users.clearSubscription, { userId: args.userId })
      return { status: "customer_deleted" }
    }

    const subscription = customer.subscriptions?.data[0]
    const stripeStatus = subscription?.status ?? 'none'

    if (user.subscriptionStatus !== stripeStatus) {
      await ctx.runMutation(internal.users.updateSubscriptionStatus, {
        userId: args.userId,
        status: stripeStatus,
        subscriptionId: subscription?.id,
      })
      return {
        status: "fixed",
        was: user.subscriptionStatus,
        now: stripeStatus,
      }
    }

    return { status: "already_synced" }
  },
})
```

## Pattern 3: Event Replay

Fetch and replay missed events from Stripe.

```typescript
export const replayMissedEvents = internalAction({
  args: {
    since: v.number(),  // Unix timestamp
    eventTypes: v.array(v.string()),
  },
  handler: async (ctx, args) => {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

    const events = await stripe.events.list({
      created: { gte: args.since },
      types: args.eventTypes,
      limit: 100,
    })

    for (const event of events.data) {
      // Check if we already processed this event
      const existing = await ctx.runQuery(internal.events.findByStripeId, {
        stripeEventId: event.id,
      })

      if (existing) {
        console.log(`Event ${event.id} already processed, skipping`)
        continue
      }

      // Process the event
      await ctx.runAction(internal.webhooks.processStripeEvent, {
        event: event,
      })
    }

    return { processed: events.data.length }
  },
})
```

## Pattern 4: Idempotent Webhook Handler

Ensure webhooks can be safely replayed.

```typescript
export const handleStripeWebhook = action({
  args: { event: v.any() },
  handler: async (ctx, args) => {
    const event = args.event

    // Check idempotency
    const existing = await ctx.runQuery(internal.events.findByStripeId, {
      stripeEventId: event.id,
    })

    if (existing) {
      console.log(`Duplicate event ${event.id}, returning early`)
      return { status: "duplicate" }
    }

    // Record event before processing
    await ctx.runMutation(internal.events.record, {
      stripeEventId: event.id,
      type: event.type,
      processedAt: Date.now(),
    })

    // Process based on event type
    switch (event.type) {
      case 'customer.subscription.updated':
        await handleSubscriptionUpdate(ctx, event.data.object)
        break
      case 'invoice.paid':
        await handleInvoicePaid(ctx, event.data.object)
        break
      // ... other events
    }

    return { status: "processed" }
  },
})
```

## When to Reconcile

### Scheduled (Cron)
- **Hourly**: High-value data (subscriptions, payments)
- **Daily**: User profiles, preferences
- **Weekly**: Historical data, analytics

### On-Demand
- User reports "my subscription isn't showing"
- Support escalation
- After incident recovery

### Event-Triggered
- After webhook failure alert
- After deployment (reconcile during quiet period)
- When dashboard shows `pending_webhooks > 0`

## Best Practices

### Do
- **Log all drift detected** with before/after values
- **Store event IDs** for idempotency
- **Paginate** when fetching from external APIs
- **Rate limit** reconciliation to avoid API limits
- **Alert on significant drift** (e.g., >5% mismatch)

### Don't
- **Don't trust local state** as source of truth for external service data
- **Don't skip idempotency** checks
- **Don't reconcile too frequently** (API rate limits)
- **Don't ignore failed reconciliations** (alert and investigate)

## Debugging Drift

```typescript
// Diagnostic query: Find users with stale subscription data
export const findDriftedUsers = internalQuery({
  handler: async (ctx) => {
    const users = await ctx.db.query("users").collect()

    return users.filter((u) => {
      // Users with subscription but no Stripe ID
      if (u.subscriptionStatus === 'active' && !u.stripeSubscriptionId) {
        return true
      }
      // Users with lastSyncedAt > 24 hours ago
      if (u.lastSyncedAt && Date.now() - u.lastSyncedAt > 86400000) {
        return true
      }
      return false
    })
  },
})
```

## References

- `references/stripe-reconciliation.md` — Stripe-specific patterns
- `references/clerk-reconciliation.md` — Clerk user sync patterns
- `references/monitoring.md` — Alerting on drift

## Related Skills

- `stripe-best-practices` — Stripe integration patterns
- `clerk-auth` — Clerk authentication integration
- `verify-fix` — Incident verification protocol

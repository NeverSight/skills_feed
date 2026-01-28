---
name: stripe-subscription-ux
description: |
  Subscription management UI requirements. Every Stripe integration needs
  a world-class UX for viewing and managing subscriptions.
keywords:
  - subscription
  - billing
  - customer portal
  - payment method
  - billing history
  - settings
  - manage subscription
---

# Subscription Management UX

Every Stripe integration must include a world-class subscription management experience. Users should never wonder about their billing status.

## Non-Negotiable Requirements

A complete Stripe integration MUST include UI for users to:

### 1. View Current Plan
- Plan name (e.g., "Pro", "Monthly", "Annual")
- Subscription status (active, trialing, canceled, past_due)
- Clear visual indicator of status
- Trial remaining (if applicable)

### 2. See Billing Cycle
- Next billing date
- Amount to be charged
- Billing frequency (monthly/annual)
- Current period start/end dates

### 3. View Payment Method
- Card brand and last 4 digits (e.g., "Visa ending in 4242")
- Expiration date
- Update payment method button

### 4. Manage Subscription
- Cancel subscription
- Resume canceled subscription (if before period end)
- Upgrade/downgrade (if multiple tiers)
- Switch billing frequency (monthly ↔ annual)

### 5. View Billing History
- Past invoices with dates and amounts
- Download invoice PDFs
- Payment status (paid, failed, refunded)

## Implementation Approaches

### Option A: Stripe Customer Portal (Recommended)

Use Stripe's built-in Customer Portal for most functionality:

```typescript
// Create portal session
const portalSession = await stripe.billingPortal.sessions.create({
  customer: stripeCustomerId,
  return_url: `${APP_URL}/settings`,
});

// Redirect user to portal
redirect(portalSession.url);
```

**Pros:**
- Minimal code
- Stripe handles PCI compliance
- Always up-to-date with Stripe features
- Mobile-responsive

**Cons:**
- Less control over styling
- Branding limited to Stripe's options
- User leaves your site briefly

### Option B: Custom UI + Stripe API

Build custom UI that calls Stripe API:

```typescript
// Fetch subscription details
const subscription = await stripe.subscriptions.retrieve(subscriptionId, {
  expand: ['default_payment_method', 'latest_invoice'],
});

// Display in your UI
const planName = subscription.items.data[0].price.nickname;
const status = subscription.status;
const currentPeriodEnd = new Date(subscription.current_period_end * 1000);
const paymentMethod = subscription.default_payment_method as Stripe.PaymentMethod;
const cardBrand = paymentMethod?.card?.brand;
const cardLast4 = paymentMethod?.card?.last4;
```

**Pros:**
- Full control over UX
- Stays within your app
- Custom branding

**Cons:**
- More code to maintain
- Must handle payment method updates carefully (PCI)
- Must implement all edge cases

### Option C: Hybrid (Best of Both)

Custom settings page for display, Stripe Portal for mutations:

```tsx
// Custom display UI
<SettingsCard>
  <h2>Subscription</h2>
  <p>Plan: {planName}</p>
  <p>Status: <StatusBadge status={status} /></p>
  <p>Next billing: {formatDate(currentPeriodEnd)}</p>
  <p>Card: {cardBrand} ending in {cardLast4}</p>

  {/* Mutations go to Stripe Portal */}
  <Button onClick={openStripePortal}>
    Manage Subscription
  </Button>
</SettingsCard>
```

**This is the recommended approach.**

## Component Structure

Typical implementation needs:

```
components/
├── billing/
│   ├── SubscriptionCard.tsx      # Current plan overview
│   ├── BillingCycleInfo.tsx      # Next billing date, amount
│   ├── PaymentMethodDisplay.tsx  # Card on file
│   ├── BillingHistory.tsx        # Past invoices
│   ├── ManageSubscriptionButton.tsx  # Opens portal
│   └── TrialBanner.tsx           # Trial status/countdown
```

Settings page:

```tsx
// app/(dashboard)/settings/page.tsx
export default function SettingsPage() {
  return (
    <div>
      <h1>Settings</h1>

      <section>
        <h2>Subscription</h2>
        <SubscriptionCard />
        <BillingCycleInfo />
        <PaymentMethodDisplay />
        <ManageSubscriptionButton />
      </section>

      <section>
        <h2>Billing History</h2>
        <BillingHistory />
      </section>
    </div>
  );
}
```

## API Requirements

Backend needs to expose:

```typescript
// convex/billing.ts (or API route)

// Get subscription details for display
export const getSubscriptionDetails = query({
  handler: async (ctx) => {
    const userId = await requireAuth(ctx);
    const user = await ctx.db.get(userId);

    return {
      status: user.subscriptionStatus,
      planName: user.planName ?? 'Pro',
      currentPeriodEnd: user.currentPeriodEnd,
      cancelAtPeriodEnd: user.cancelAtPeriodEnd,
      trialEndsAt: user.trialEndsAt,
      // Payment method from Stripe (cached or fetched)
      paymentMethod: user.paymentMethodSummary,
    };
  },
});

// Create Stripe Portal session
export const createPortalSession = action({
  handler: async (ctx) => {
    const userId = await requireAuth(ctx);
    const user = await ctx.runQuery(internal.users.get, { userId });

    if (!user.stripeCustomerId) {
      throw new ConvexError("No billing account");
    }

    const session = await stripe.billingPortal.sessions.create({
      customer: user.stripeCustomerId,
      return_url: `${process.env.NEXT_PUBLIC_APP_URL}/settings`,
    });

    return { url: session.url };
  },
});

// Get billing history (invoices)
export const getBillingHistory = action({
  handler: async (ctx) => {
    const userId = await requireAuth(ctx);
    const user = await ctx.runQuery(internal.users.get, { userId });

    if (!user.stripeCustomerId) {
      return { invoices: [] };
    }

    const invoices = await stripe.invoices.list({
      customer: user.stripeCustomerId,
      limit: 10,
    });

    return {
      invoices: invoices.data.map(inv => ({
        id: inv.id,
        date: inv.created,
        amount: inv.amount_paid,
        status: inv.status,
        invoicePdf: inv.invoice_pdf,
      })),
    };
  },
});
```

## Schema Requirements

User model needs:

```typescript
// convex/schema.ts
users: defineTable({
  // ... existing fields

  // Subscription state
  subscriptionStatus: v.optional(v.string()),
  stripeCustomerId: v.optional(v.string()),
  stripeSubscriptionId: v.optional(v.string()),

  // Billing cycle
  currentPeriodEnd: v.optional(v.number()),
  cancelAtPeriodEnd: v.optional(v.boolean()),

  // Trial
  trialEndsAt: v.optional(v.number()),

  // Payment method cache (update from webhooks)
  paymentMethodSummary: v.optional(v.object({
    brand: v.string(),
    last4: v.string(),
    expMonth: v.number(),
    expYear: v.number(),
  })),

  // Plan info
  planName: v.optional(v.string()),
  planInterval: v.optional(v.string()), // 'month' or 'year'
})
```

## Webhook Updates

To keep payment method cached, handle:

```typescript
case 'customer.subscription.updated':
case 'payment_method.attached':
case 'payment_method.updated':
  // Extract payment method details
  const pm = event.data.object.default_payment_method;
  if (pm?.card) {
    await ctx.runMutation(internal.users.updatePaymentMethod, {
      userId,
      paymentMethod: {
        brand: pm.card.brand,
        last4: pm.card.last4,
        expMonth: pm.card.exp_month,
        expYear: pm.card.exp_year,
      },
    });
  }
```

## UX Best Practices

### Status Messaging

| Status | Message | Color |
|--------|---------|-------|
| active | "Your subscription is active" | Green |
| trialing | "Trial ends in X days" | Blue |
| canceled | "Cancels on [date]" | Yellow |
| past_due | "Payment failed - update card" | Red |
| incomplete | "Complete payment setup" | Red |

### Trial Banner

Show a non-intrusive but clear trial banner:

```tsx
{user.subscriptionStatus === 'trialing' && (
  <Banner variant="info">
    {daysRemaining} days left in your trial.
    <Link href="/pricing">Subscribe now</Link>
  </Banner>
)}
```

### Canceled State

When subscription is canceled but still in period:

```tsx
<Card className="border-yellow-500">
  <p>Your subscription has been canceled.</p>
  <p>You have access until {formatDate(currentPeriodEnd)}.</p>
  <Button onClick={resubscribe}>Resume Subscription</Button>
</Card>
```

### Payment Failed State

Urgent but not alarmist:

```tsx
<Card className="border-red-500">
  <p>Your last payment failed.</p>
  <p>Please update your payment method to avoid losing access.</p>
  <Button onClick={openStripePortal}>Update Payment</Button>
</Card>
```

## Verification Checklist

A complete subscription management UX should pass:

- [ ] User can see current plan name
- [ ] User can see subscription status with clear indicator
- [ ] User can see next billing date and amount
- [ ] User can see payment method on file
- [ ] User can access billing history
- [ ] User can cancel subscription
- [ ] User can resume canceled subscription (if in period)
- [ ] User can update payment method
- [ ] Trial users see trial status and remaining time
- [ ] Failed payment shows clear call-to-action
- [ ] All states have appropriate messaging

## Integration with Stripe Workflow

This skill is invoked by:
- `stripe-scaffold` — generates UX components
- `stripe-audit` — checks for UX completeness
- `stripe-verify` — tests UX functionality

## Related Skills

- `subscription-patterns` — State management and access control
- `billing-security` — Security considerations
- `stripe-configure` — Portal configuration in Stripe Dashboard

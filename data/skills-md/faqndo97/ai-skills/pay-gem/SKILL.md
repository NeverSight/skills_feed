---
name: pay-gem
description: Build Rails payments with the Pay gem and Stripe. Full lifecycle - setup, subscriptions, one-time charges, Stripe Checkout, Billing Portal, webhooks, metered billing, Stripe Connect, testing, and debugging.
---

<essential_principles>

## How Pay Gem Works

Pay is a payments engine for Rails that abstracts Stripe (and other processors) into a Rails-friendly interface.

### 1. Payment Processor Pattern

Always set a payment processor before any payment operations:

```ruby
@user.set_payment_processor :stripe
# OR set default on model
class User < ApplicationRecord
  pay_customer default_payment_processor: :stripe
end
```

Access the processor via `@user.payment_processor` for all operations.

### 2. Amounts in Cents

All amounts are in cents (smallest currency unit):

```ruby
@user.payment_processor.charge(15_00)  # $15.00
@user.payment_processor.charge(99_99)  # $99.99
```

### 3. Webhooks Are Required

Pay relies on Stripe webhooks to sync subscription status, payment confirmations, and more. Without webhooks, your local records will be stale.

```bash
# Development: Use Stripe CLI
stripe listen --forward-to localhost:3000/pay/webhooks/stripe
```

### 4. SCA/3D Secure Handling

Stripe requires Strong Customer Authentication for EU payments. Pay handles this via:
- `Pay::ActionRequired` exception for charges needing confirmation
- Built-in `/pay/payments/:id` confirmation route
- Automatic webhook sync for async confirmations

### 5. Fake Processor for Testing

Use the fake processor to test without hitting Stripe:

```ruby
@user.set_payment_processor :fake_processor, allow_fake: true
@user.payment_processor.subscribe(plan: "fake")
```

</essential_principles>

<intake>

**What would you like to do?**

1. Set up Pay gem in a new project
2. Create a subscription
3. Manage subscriptions (cancel, pause, resume, swap)
4. Create a one-time charge
5. Set up Stripe Checkout
6. Set up Billing Portal
7. Configure webhooks
8. Implement metered/usage-based billing
9. Set up Stripe Connect (marketplace)
10. Debug payment issues
11. Write tests
12. Something else

**Then read the matching workflow from `workflows/` and follow it.**

</intake>

<routing>

| Response | Workflow |
|----------|----------|
| 1, "setup", "install", "new project" | `workflows/setup-pay-gem.md` |
| 2, "subscribe", "subscription", "create subscription" | `workflows/create-subscription.md` |
| 3, "cancel", "pause", "resume", "swap", "manage" | `workflows/manage-subscription.md` |
| 4, "charge", "one-time", "payment" | `workflows/create-charge.md` |
| 5, "checkout", "stripe checkout", "hosted" | `workflows/setup-stripe-checkout.md` |
| 6, "portal", "billing portal", "customer portal" | `workflows/setup-billing-portal.md` |
| 7, "webhook", "webhooks", "events" | `workflows/setup-webhooks.md` |
| 8, "metered", "usage", "usage-based" | `workflows/implement-metered-billing.md` |
| 9, "connect", "marketplace", "platform" | `workflows/setup-stripe-connect.md` |
| 10, "debug", "not working", "error", "fix" | `workflows/debug-payments.md` |
| 11, "test", "tests", "testing" | `workflows/write-tests.md` |

</routing>

<verification_loop>

## After Every Change

```bash
# 1. Does it load?
bin/rails runner "Pay::Subscription"

# 2. Do tests pass?
bin/rails test test/models/

# 3. Check webhook forwarding (development)
stripe listen --forward-to localhost:3000/pay/webhooks/stripe
```

Report to the user:
- "Pay models load: OK"
- "Tests: X pass, Y fail"
- "Webhooks: forwarding to localhost"

</verification_loop>

<reference_index>

## Domain Knowledge

All in `references/`:

**Setup:** installation.md, configuration.md
**Core:** customers.md, payment-methods.md, charges.md, subscriptions.md
**Stripe Features:** stripe-checkout.md, billing-portal.md, sca-payment-intents.md
**Advanced:** webhooks.md, metered-billing.md, stripe-connect.md
**Quality:** testing.md, anti-patterns.md

</reference_index>

<workflows_index>

## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| setup-pay-gem.md | Install and configure Pay with Stripe |
| create-subscription.md | Create subscriptions with trials |
| manage-subscription.md | Cancel, pause, resume, swap |
| create-charge.md | One-time charges and refunds |
| setup-stripe-checkout.md | Stripe Checkout integration |
| setup-billing-portal.md | Customer self-service portal |
| setup-webhooks.md | Webhook configuration |
| implement-metered-billing.md | Usage-based pricing |
| setup-stripe-connect.md | Marketplace payments |
| debug-payments.md | Troubleshooting |
| write-tests.md | Testing with fake processor |

</workflows_index>

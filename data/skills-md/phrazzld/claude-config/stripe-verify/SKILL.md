---
name: stripe-verify
description: |
  End-to-end verification of Stripe integration. Deep testing including
  real checkout flows, webhook delivery, and subscription state transitions.
---

# Stripe Verify

Comprehensive end-to-end verification. Go deep — billing bugs are expensive.

## Objective

Prove the integration works. Not "looks right" — actually works. Test real flows, verify real state changes, confirm real webhook delivery.

## Process

**1. Configuration Verification**

Before functional tests, verify all configuration:

```bash
# Env vars exist
npx convex env list | grep STRIPE
npx convex env list --prod | grep STRIPE
vercel env ls --environment=production | grep STRIPE

# Webhook URL accessible
curl -s -o /dev/null -w "%{http_code}" -I -X POST "$WEBHOOK_URL"
# Must be 4xx or 5xx, not 3xx

# Stripe CLI connected
stripe listen --print-json --latest
```

**2. Checkout Flow Test**

Create a real test checkout session:

```bash
# Trigger checkout (via app or API)
# Complete with Stripe test card: 4242 4242 4242 4242

# Verify:
# - Session created successfully
# - Redirect works
# - Success page loads
# - Webhook received (check logs)
# - Subscription created in Stripe Dashboard
# - User state updated in database
```

**3. Webhook Delivery Test**

Verify webhooks are actually delivering:

```bash
# Check pending webhooks
stripe events list --limit 5 | jq '.data[] | {id, type, pending_webhooks}'

# Resend a recent event
stripe events resend <event_id> --webhook-endpoint <endpoint_id>

# Watch logs for delivery
vercel logs <app> --json | grep webhook
```

All recent events should have `pending_webhooks: 0`.

**4. Subscription State Transitions**

Test each state transition:

**New → Trial**
- Create account
- Verify trial starts
- Verify trial end date correct

**Trial → Active**
- Complete checkout during trial
- Verify remaining trial honored (trial_end passed to Stripe)
- Verify local state updated

**Active → Canceled**
- Cancel subscription (via customer portal or API)
- Verify access continues until period end
- Verify state reflects cancellation

**Canceled → Resubscribed**
- Resubscribe after cancellation
- Verify new subscription created
- Verify billing starts immediately (no new trial)

**Trial Expired**
- Let trial expire (or simulate)
- Verify access revoked
- Verify proper messaging to user

**5. Edge Case Testing**

**Webhook Idempotency**
- Resend the same webhook event twice
- Verify no duplicate processing
- Verify no state corruption

**Out-of-Order Webhooks**
- If possible, simulate events arriving out of order
- Verify system handles gracefully

**Payment Failure**
- Use Stripe test card for decline: 4000 0000 0000 0002
- Verify subscription goes to past_due
- Verify access policy for past_due state

**6. Access Control Verification**

Test that access control actually works:

- Active subscriber → can access features
- Trial user → can access features
- Expired trial → blocked
- Canceled (in period) → can access
- Canceled (past period) → blocked
- Past due → depends on policy (usually grace period)

**7. Business Model Compliance**

Verify against `business-model-preferences`:

- Single pricing tier? (no multiple options)
- Trial honored on upgrade? (check Stripe subscription has trial_end)
- No freemium logic? (expired trial = no access)

**8. Subscription Management UX**

Verify against `stripe-subscription-ux` requirements:

**Settings Page Exists:**
- [ ] Settings page has subscription section
- [ ] Current plan name displayed
- [ ] Subscription status with visual indicator
- [ ] Next billing date shown
- [ ] Payment method displayed (brand + last4)

**Stripe Portal Integration:**
- [ ] "Manage Subscription" button exists
- [ ] Button creates portal session and redirects
- [ ] Return URL configured correctly

**Billing History:**
- [ ] Past invoices displayed
- [ ] Invoice PDFs downloadable
- [ ] Payment statuses shown

**State-Specific UX:**
- [ ] Trial banner shows for trialing users
- [ ] Canceled state shows period end date
- [ ] Past due state shows payment update CTA
- [ ] Active state shows "all good" indicator

**This is a hard requirement.** If subscription management UX is missing,
verification fails. Users must be able to manage their billing.

## Output

Verification report:

```
STRIPE VERIFICATION REPORT
=========================

CONFIGURATION
✓ All env vars present
✓ Webhook URL responds correctly
✓ Stripe CLI connected

CHECKOUT FLOW
✓ Session creates
✓ Payment succeeds
✓ Webhook received
✓ State updated

SUBSCRIPTION STATES
✓ Trial → Active
✓ Active → Canceled
✓ Canceled → Resubscribed
⚠ Trial expiration: not tested (would require waiting)

EDGE CASES
✓ Idempotent webhook handling
✓ Payment decline handled
✗ Out-of-order webhooks: not testable

ACCESS CONTROL
✓ Active: access granted
✓ Trial: access granted
✓ Expired: access denied
✓ Canceled in-period: access granted

BUSINESS MODEL
✓ Single tier
✓ Trial completion on upgrade
✓ No freemium

SUBSCRIPTION MANAGEMENT UX
✓ Settings page has subscription section
✓ Plan name and status displayed
✓ Next billing date shown
✓ Payment method displayed
✓ Manage Subscription button works
✓ Billing history accessible
✓ Trial banner for trialing users
✓ Canceled state messaging
⚠ Past due state: not tested

---
STATUS: VERIFIED (with minor gaps)
```

## When to Run

- After `stripe-setup` (new integration)
- After `stripe-reconcile` (fixes applied)
- Before production deployment
- Periodically as health check

## Deep Mode

This skill defaults to deep verification. Don't skip tests to save time. Billing bugs cost more than the time spent testing.

---
name: stripe
description: |
  Complete Stripe lifecycle management. Audits current state, fixes all issues,
  and verifies checkout flows work end-to-end. Every run does all of this.

  Auto-invoke when: files contain stripe/payment/checkout/webhook, imports stripe
  package, references STRIPE_* env vars, webhook handlers modified.
argument-hint: "[focus area, e.g. 'webhooks' or 'subscription UX']"
---

# /stripe

World-class Stripe integration. Audit, fix, verify—every time.

## What This Does

Examines your Stripe integration, identifies every gap, implements fixes, and verifies checkout flows work end-to-end. No partial modes. Every run does the full cycle.

## Branching

Assumes you start on `master`/`main`. Before making code changes:

```bash
git checkout -b fix/stripe-$(date +%Y%m%d)
```

Configuration-only changes (env vars, dashboard settings) don't require a branch. Code changes do.

## Process

### 0. Environment Check

**Detect environment mismatch first.** Before any Stripe operations:
```bash
~/.claude/skills/stripe/scripts/detect-environment.sh
```

This compares your app's STRIPE_SECRET_KEY account with CLI profiles. If mismatched, resources created via CLI won't be visible to your app.

**Fix mismatches:**
- Use correct CLI profile: `stripe -p sandbox` or `stripe -p production`
- Or update `.env.local` to match your CLI account

### 1. Audit

**Spawn the auditor.** Use the `stripe-auditor` subagent for deep parallel analysis. It examines:
- Configuration (env vars on all deployments, cross-platform parity)
- Webhook health (endpoints registered, URL returns non-3xx, pending_webhooks = 0)
- Subscription logic (trial handling, access control, idempotency)
- Security (no hardcoded keys, secrets not logged)
- Business model compliance (single tier, trial honored on upgrade)
- Subscription management UX (settings page, billing history, portal integration)

**Run automated checks:**
```bash
~/.claude/skills/stripe/scripts/stripe_audit.sh
```

**Research first.** Before assuming current patterns are correct, check Stripe docs for current best practices. Use Gemini. What was right last year may be deprecated.

### 2. Plan

From audit findings, build a complete remediation plan. Don't just list issues—plan the fixes.

For each finding:
- **Configuration issues** → Fix directly (env vars, dashboard settings)
- **Code issues** → Delegate to Codex with clear specs
- **Design issues** → May require rethinking approach, consult `stripe-design`

Prioritize:
1. **Critical** — Blocks checkout or causes payment failures
2. **High** — Security issues, data integrity problems
3. **Medium** — Missing UX, suboptimal patterns

### 3. Execute

**Fix everything.** Don't stop at a report.

**Configuration fixes (do directly):**
```bash
# Missing env var
npx convex env set --prod STRIPE_WEBHOOK_SECRET "$(printf '%s' 'whsec_...')"

# Verify
npx convex env list --prod | grep STRIPE
```

**Code fixes (delegate to Codex):**
```bash
codex exec --full-auto "Fix [specific issue]. \
File: [path]. Problem: [what's wrong]. \
Solution: [what it should do]. \
Reference: [pattern file]. \
Verify: pnpm typecheck && pnpm test" \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

Then validate: `git diff --stat && pnpm typecheck`

**Webhook URL fixes:**
Update in Stripe Dashboard to canonical domain. If redirects exist, use the final URL.

**Missing subscription management UX:**
Per `stripe-subscription-ux`, every integration needs:
- Settings page showing plan, status, next billing date
- Payment method display (brand + last4)
- "Manage Subscription" button (Stripe Portal)
- Billing history with downloadable invoices
- State-specific messaging (trialing, canceled, past_due)

If missing, create it. This is non-negotiable.

### 4. Verify

**Prove it works.** Not "looks right"—actually works.

**Configuration verification:**
```bash
npx convex env list | grep STRIPE
npx convex env list --prod | grep STRIPE
curl -s -o /dev/null -w "%{http_code}" -I -X POST "$WEBHOOK_URL"
```

**Checkout flow test:**
1. Create test checkout session
2. Complete with card `4242 4242 4242 4242`
3. Verify webhook received (check logs)
4. Verify subscription created in Stripe Dashboard
5. Verify user state updated in database
6. Verify access granted

**Webhook delivery test:**
```bash
stripe events list --limit 5 | jq '.data[] | {id, type, pending_webhooks}'
# All should have pending_webhooks: 0
```

**Subscription management UX test:**
- Navigate to settings page
- Verify plan and status displayed
- Click "Manage Subscription" → Portal opens
- Verify billing history accessible

**Business model compliance:**
- Single pricing tier? ✓
- Trial honored on upgrade? (Check Stripe subscription has trial_end) ✓
- No freemium logic? (Expired trial = no access) ✓

If any verification fails, go back and fix it. Don't declare done until everything passes.

## Business Model Compliance

Reference `business-model-preferences` throughout. Key constraints:
- Single pricing tier (no complex tier logic)
- Trial completion honored on upgrade (pass trial_end to Stripe)
- No freemium (expired trial = no access, not limited access)

## Default Stack

Assumes Next.js + TypeScript + Convex + Vercel + Clerk. Adapts gracefully to other stacks—concepts are the same, only framework specifics change.

## What You Get

When complete:
- Working checkout flow (test card succeeds, subscription created)
- Webhook handling with signature verification (pending_webhooks = 0)
- Subscription state management with proper trial handling
- Access control based on subscription status
- Subscription management UX (settings page, portal, billing history)
- All configuration in place (dev and prod)
- Deep verification passing

User can:
- Run test checkout with `4242 4242 4242 4242`
- See subscription state update
- Access gated features
- See trial honored on mid-trial upgrade
- View and manage subscription in settings
- See payment method and billing history
- Cancel, resume, or update payment method via Portal

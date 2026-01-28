---
name: stripe-audit
description: |
  Comprehensive audit of existing Stripe integration.
  Checks configuration, code patterns, security, and business model alignment.
---

# Stripe Audit

Deep analysis of an existing Stripe integration.

## Objective

Find everything that's wrong, suboptimal, or drifted. Produce actionable findings.

## Process

**1. Spawn the Auditor**

This is a deep analysis. Spawn the `stripe-auditor` subagent to do the heavy lifting in parallel. It has read-only access and preloaded Stripe knowledge.

**1.5. Check Environment**

Before any CLI operations, verify environment parity:
```bash
~/.claude/skills/stripe/scripts/detect-environment.sh
```

If mismatch detected, fix before proceeding. Resources created in wrong account won't be visible to app.

**2. Run Automated Checks**

Execute the audit script for quick wins:
```bash
~/.claude/skills/stripe/scripts/stripe_audit.sh
```

This catches:
- Hardcoded keys
- Missing env vars
- Webhook signature verification
- Mode-dependent parameter errors

**3. Deep Analysis Areas**

The auditor should examine:

**Configuration**
- Env vars set on all deployments?
- Cross-platform parity (Vercel ↔ Convex)?
- No trailing whitespace in secrets?
- Test keys in dev, live keys in prod?

**Local Development**
- Does `pnpm dev` auto-start `stripe listen`?
- If yes, is there a sync script that captures the ephemeral secret?
- Script uses `--print-secret` flag?
- Secret synced to correct target (Convex env or .env.local)?

**Webhook Health**
- Endpoints registered correctly?
- URL returns non-3xx on POST?
- Recent events delivered (pending_webhooks = 0)?
- Signature verification present and FIRST?

**Subscription Logic**
- Trial handling uses Stripe's `trial_end`?
- Access control checks subscription status correctly?
- Edge cases handled (cancel during trial, resubscribe, out-of-order webhooks)?
- Idempotency on webhook processing?

**Security**
- No hardcoded keys in source?
- Secrets not logged?
- Error responses don't leak internal details?

**Business Model**
- Single pricing tier?
- Trial completion honored on upgrade?
- No freemium/feature-gating logic?

**Subscription Management UX** (per `stripe-subscription-ux`)
- Settings page with subscription section?
- Current plan and status displayed?
- Next billing date shown?
- Payment method on file displayed?
- "Manage Subscription" button (Stripe Portal)?
- Billing history accessible?
- Appropriate messaging for all states?

**4. Validate with Thinktank**

For complex findings, run them through Thinktank for multi-expert validation. Billing bugs are expensive.

## Output

Structured findings report:

```
STRIPE AUDIT REPORT
==================

CONFIGURATION
✓ Env vars set on dev
✗ STRIPE_WEBHOOK_SECRET missing on prod
⚠ Webhook URL returns 307 redirect

WEBHOOK HEALTH
✓ Endpoints registered
✗ 3 events with pending_webhooks > 0

SUBSCRIPTION LOGIC
✓ Uses trial_end
⚠ Missing idempotency check

SECURITY
✓ No hardcoded keys
✓ Signature verification present

LOCAL DEVELOPMENT
✓ Auto-starts stripe listen
✗ No webhook secret auto-sync

BUSINESS MODEL
✓ Single tier
✗ Trial not passed on mid-trial upgrade

SUBSCRIPTION MANAGEMENT UX
✓ Settings page exists
✓ Plan name displayed
✗ No payment method shown
✗ No billing history
⚠ Portal button exists but return_url missing

---
SUMMARY: 8 pass, 3 warn, 5 fail

CRITICAL:
- Set STRIPE_WEBHOOK_SECRET on prod
- Fix webhook URL redirect

HIGH:
- Implement trial_end pass-through

MEDIUM:
- Add webhook idempotency
```

## Research First

Before auditing, check current Stripe best practices. What was correct last year might be deprecated now. Use Gemini to verify against current documentation.

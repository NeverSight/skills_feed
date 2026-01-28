---
name: stripe-configure
description: |
  Configure Stripe Dashboard and deployment environments.
  Sets up products, prices, webhooks, and environment variables.
---

# Stripe Configure

Set up Stripe Dashboard and deployment environment variables.

## Objective

Configure everything outside the codebase: Stripe Dashboard settings, environment variables across all deployments, webhook endpoints.

## Process

**1. Stripe Dashboard Setup**

Guide the user through (or use Stripe CLI where possible):

**Products & Prices**
- Create product (name matches app)
- Create price(s): monthly, annual if applicable
- Note the price IDs for env vars

**Webhook Endpoint**
- Create endpoint pointing to production URL
- Use canonical domain (www if that's where app lives — Stripe doesn't follow redirects)
- Enable required events (from design)
- Copy webhook signing secret

**Customer Portal** (if using)
- Configure allowed actions
- Set branding

**2. Environment Variables**

Set variables on ALL deployment targets. This is where incidents happen.

**Local Development**
```bash
# .env.local
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_STRIPE_PRICE_ID=price_...
```

**Convex (both dev and prod)**
```bash
# Dev
npx convex env set STRIPE_SECRET_KEY "sk_test_..."
npx convex env set STRIPE_WEBHOOK_SECRET "whsec_..."

# Prod (DON'T FORGET THIS)
npx convex env set --prod STRIPE_SECRET_KEY "sk_live_..."
npx convex env set --prod STRIPE_WEBHOOK_SECRET "whsec_..."
```

**Vercel**
```bash
vercel env add STRIPE_SECRET_KEY production
vercel env add STRIPE_WEBHOOK_SECRET production
# ... etc
```

**3. Verify Parity**

Check that all deployments have matching configuration:
- Local has test keys
- Convex dev has test keys
- Convex prod has live keys
- Vercel prod has live keys

Use `verify-env-parity.sh` if available, or manually compare.

**4. Webhook URL Verification**

CRITICAL: Verify webhook URL doesn't redirect.

```bash
curl -s -o /dev/null -w "%{http_code}" -I -X POST "https://your-domain.com/api/stripe/webhook"
```

Must return 4xx or 5xx, NOT 3xx. If it redirects, fix the URL in Stripe Dashboard.

## Common Mistakes

- Setting env vars on dev but forgetting prod
- Using wrong domain (non-www when app is www)
- Trailing whitespace in secrets (use `printf '%s'` not `echo`)
- Test keys in production, live keys in development

## Output

Checklist of what was configured:
- [ ] Product created
- [ ] Price(s) created
- [ ] Webhook endpoint configured
- [ ] Env vars set on local
- [ ] Env vars set on Convex dev
- [ ] Env vars set on Convex prod
- [ ] Env vars set on Vercel
- [ ] Webhook URL verified (no redirect)

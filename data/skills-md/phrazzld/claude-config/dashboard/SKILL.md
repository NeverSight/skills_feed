---
name: dashboard
description: |
  Unified portfolio dashboard. Traffic, revenue, errors - all products at a glance.
  Weekly traction check in 2 minutes.

  Auto-invoke when: user asks about metrics, traction, analytics, revenue across products.
argument-hint: "[--html to export to file]"
---

# /dashboard

See everything. Find traction signals.

## What This Does

Aggregates metrics from all MistyStep products into a single view:
- **Traffic**: PostHog analytics per project (with MCP)
- **Revenue**: Stripe (subscriptions, one-time payments)
- **Errors**: Sentry error counts
- **Changes**: Week-over-week deltas with anomaly flags

## Output Format

```
┌──────────────────────────────────────────────────────────────────┐
│ MISTYSTEP PORTFOLIO - Week of Jan 20                            │
├──────────────────────────────────────────────────────────────────┤
│ Product          │ Visits │ Δ    │ Revenue │ Errors │ Status    │
├──────────────────────────────────────────────────────────────────┤
│ Volume           │   892  │ ↑147%│  $45.00 │   0    │ ⚠️ SIGNAL │
│ Heartbeat        │   234  │ ↑ 12%│   $0.00 │   2    │ 🟢        │
│ Scry             │    45  │ ↓  5%│   $0.00 │   0    │ 🟢        │
│ Crondle          │   156  │ →  0%│   $0.00 │   0    │ 🟢        │
│ ...              │        │      │         │        │           │
├──────────────────────────────────────────────────────────────────┤
│ TOTAL            │  2,847 │ ↑ 34%│ $127.00 │   3    │           │
└──────────────────────────────────────────────────────────────────┘

⚠️ Volume showing unusual growth (+147%)
   Investigate: What's driving traffic?
```

## Process

### 1. Load Product Registry

Read `products.yaml` for the list of products and their API identifiers:
- PostHog project IDs
- Stripe account/product IDs
- Sentry project slugs
- Domain names

### 2. Fetch Metrics

For each product, fetch:

**Traffic (PostHog API / MCP)**
```bash
# Via PostHog MCP (preferred - Claude can query directly)
# Or via CLI:
curl -s "https://app.posthog.com/api/projects/${PROJECT_ID}/insights/trend/" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" \
  -d '{"events": [{"id": "$pageview"}], "date_from": "-7d"}'

# For specific breakdown by referrer:
curl -s "https://app.posthog.com/api/projects/${PROJECT_ID}/insights/trend/" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" \
  -d '{"events": [{"id": "$pageview"}], "breakdown": "$referrer", "date_from": "-7d"}'
```

**Revenue (Stripe API)**
```bash
# Requires STRIPE_SECRET_KEY env var
stripe balance_transactions list --created[gte]=$LAST_WEEK --limit=100
# Or for specific product revenue:
stripe invoices list --created[gte]=$LAST_WEEK --status=paid
```

**Errors (Sentry API)**
```bash
# Requires SENTRY_AUTH_TOKEN env var
curl -s "https://sentry.io/api/0/projects/${ORG}/${PROJECT}/stats/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

### 3. Calculate Deltas

Compare this week vs last week:
- ↑ = increase > 5%
- ↓ = decrease > 5%
- → = stable (within 5%)
- ⚠️ SIGNAL = change > 50% (investigate!)

### 4. Display Results

Output formatted table to terminal.

**Optional**: `--html` flag exports to `~/dashboard.html` for browser viewing.

## Product Registry

Edit `~/.claude/skills/dashboard/products.yaml` to configure products:

```yaml
products:
  - name: Volume
    domain: volume.app
    posthog_project_id: 12345  # Changed from vercel_project_id
    stripe_product_id: prod_xxx
    sentry_project: volume

  - name: Heartbeat
    domain: heartbeat.app
    posthog_project_id: 12345
    stripe_product_id: prod_yyy
    sentry_project: heartbeat

  # ... more products
```

## Required Environment Variables

```bash
# PostHog - for traffic analytics (preferred)
POSTHOG_API_KEY=phx_xxx
POSTHOG_PROJECT_ID=12345

# Stripe - for revenue
STRIPE_SECRET_KEY=sk_live_xxx

# Sentry - for errors (optional)
SENTRY_AUTH_TOKEN=xxx
SENTRY_ORG=mistystep
```

**Note:** Vercel Analytics is NOT used because it lacks CLI/API access. PostHog provides equivalent traffic data with MCP integration.

## Usage

```bash
# Weekly check (terminal output)
/dashboard

# Export to HTML for browser
/dashboard --html

# Check specific product only
/dashboard volume
```

## When to Use

- **Weekly ritual**: Every Monday, run `/dashboard` to spot traction
- **After launch**: Check if announcement drove traffic
- **Investigating issues**: See if errors spiked

## Traction Signals

The dashboard flags products with >50% change as potential traction signals.

When you see ⚠️ SIGNAL:
1. Investigate the source (referrer data)
2. Is it sustainable or a one-time spike?
3. If sustainable, consider `/double-down`

## Fallback: Browser Automation

If APIs aren't configured, fall back to browser automation:
1. Open PostHog dashboard in Chrome
2. Navigate to each project's analytics
3. Screenshot or extract numbers
4. Repeat for Stripe and Sentry dashboards

This is slower but works without API setup.

## Related Skills

- `/observability` - Full monitoring setup (Sentry, PostHog, etc.)
- `/marketing-status` - Marketing-focused metrics with PostHog MCP
- `/stripe` - Stripe integration audit
- `/double-down` - What to do when traction appears (future skill)

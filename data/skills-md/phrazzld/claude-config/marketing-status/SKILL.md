---
name: marketing-status
description: |
  CLI dashboard for marketing metrics. Pulls from PostHog, Stripe,
  and Postiz MCPs when configured. Shows traffic, activation, conversion.
  Includes CLI script examples for direct API access.
---

# /marketing-status

Marketing metrics dashboard. Shows what's working.

## Philosophy

If you can't measure it, you can't iterate. Three metrics that matter:
1. Traffic source - where people came from
2. Activation - did they do the core thing once?
3. Conversion - paid or email signup

## Output Format

Show a dashboard like:

```
MARKETING STATUS
================

Traffic (last 7 days)
├─ Direct: XXX
├─ Twitter: XXX
├─ Reddit: XXX
├─ HN: XXX
└─ Other: XXX

Activation
├─ Signups: XXX
├─ Activated: XXX (XX%)
└─ Core action: XXX

Revenue (Stripe)
├─ MRR: $XXX
├─ New this week: $XXX
└─ Churn: $XXX
```

## Data Sources

### PostHog MCP (if configured)
- Traffic by source
- Signup events
- Activation events (custom)
- Core action events (custom)

### Stripe MCP (if configured)
- MRR calculation
- New revenue
- Churn

### Postiz MCP (if configured)
- Post performance
- Engagement metrics
- Scheduled posts

## CLI Script Examples

### PostHog via MCP (Preferred)

When PostHog MCP is configured, Claude can query directly:
- "What are my top traffic sources this week?"
- "Show signup conversion rate by source"
- "Which features have the highest engagement?"

### PostHog via CLI

```bash
# Get pageviews for last 7 days
curl -s "https://app.posthog.com/api/projects/${POSTHOG_PROJECT_ID}/insights/trend/" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" \
  -d '{"events": [{"id": "$pageview"}], "date_from": "-7d"}' | jq '.result[0].data | add'

# Get signups by referrer
curl -s "https://app.posthog.com/api/projects/${POSTHOG_PROJECT_ID}/insights/trend/" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" \
  -d '{"events": [{"id": "signup"}], "breakdown": "$referrer", "date_from": "-7d"}' | jq

# Get feature flag evaluations
curl -s "https://app.posthog.com/api/projects/${POSTHOG_PROJECT_ID}/feature_flags/" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" | jq '.[].key'
```

### Stripe via CLI

```bash
# MRR calculation (active subscriptions)
stripe subscriptions list --status=active --limit=100 | jq '[.data[].plan.amount] | add / 100'

# New revenue this week
stripe balance_transactions list --created[gte]=$(date -v-7d +%s) --limit=100 | jq '[.data[].amount] | add / 100'

# Churn (canceled subscriptions)
stripe subscriptions list --status=canceled --created[gte]=$(date -v-7d +%s) | jq '[.data[].plan.amount] | add / 100'
```

## Fallback (No MCPs)

If MCPs not configured, show:
1. Instructions for setting up PostHog
2. Links to dashboards (PostHog, Stripe, etc.)
3. Recommend running /check-observability

## Process

1. Check which MCPs are available
2. Pull metrics from available sources
3. Format into dashboard view
4. Highlight anomalies or opportunities
5. Suggest next actions based on data

## MCP Configuration

Add to your Claude config for full MCP integration:

```json
{
  "mcpServers": {
    "posthog": {
      "command": "npx",
      "args": ["-y", "@posthog/mcp-server"],
      "env": {
        "POSTHOG_API_KEY": "your-api-key",
        "POSTHOG_PROJECT_ID": "your-project-id"
      }
    },
    "stripe": {
      "command": "npx",
      "args": ["-y", "@stripe/mcp", "--tools=all"],
      "env": {
        "STRIPE_SECRET_KEY": "your-stripe-key"
      }
    }
  }
}
```

## Related Skills

- /check-observability - Audit analytics setup
- /growth-sprint - Weekly marketing ritual
- /check-stripe - Stripe integration audit

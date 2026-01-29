---
name: cli-reference
description: |
  CLI commands for all infrastructure services. Invoke when:
  - Configuring any external service (Vercel, Convex, Stripe, Sentry, PostHog, GitHub)
  - Before suggesting any dashboard action
  - Setting environment variables across platforms
  Keywords: env var, configure, dashboard, settings, production, deploy, CLI
---

# CLI Reference

Every infrastructure operation has a CLI command. Never send users to dashboards.

## Environment Variables

### Vercel
```bash
# Add (use printf to avoid trailing newlines)
printf '%s' 'value' | vercel env add KEY production
printf '%s' 'value' | vercel env add KEY preview
printf '%s' 'value' | vercel env add KEY development

# List (filter output manually - no env flag)
vercel env ls | grep production

# Remove
vercel env rm KEY production
```

### Convex
```bash
# Set (dev is default, use --prod for production)
npx convex env set KEY "value"
npx convex env set --prod KEY "value"

# List
npx convex env list
npx convex env list --prod

# Remove
npx convex env unset KEY
npx convex env unset --prod KEY
```

## Stripe

```bash
# Always use profile flag
stripe -p sandbox products list
stripe -p production products list

# Create product + price
stripe -p production products create --name "Pro Plan"
stripe -p production prices create \
  --product prod_xxx \
  --unit-amount 999 \
  --currency usd \
  --recurring[interval]=month

# Webhooks
stripe -p production webhook_endpoints list
stripe events resend EVENT_ID --webhook-endpoint EP_ID
```

## Sentry

```bash
# List issues
sentry-cli issues list --project=$SENTRY_PROJECT --status=unresolved

# Create release
sentry-cli releases new $VERSION
sentry-cli releases set-commits $VERSION --auto

# Upload source maps
sentry-cli sourcemaps upload --release=$VERSION ./dist
```

## PostHog (API)

No official CLI. Use curl with API key:

```bash
# Get project ID first
curl -s "https://us.posthog.com/api/projects/" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" | jq '.[0].id'

# Query events
curl -s "https://us.posthog.com/api/projects/$PROJECT_ID/events/" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" | jq '.results[:5]'

# Feature flags
curl -s "https://us.posthog.com/api/projects/$PROJECT_ID/feature_flags/" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" | jq '.results'
```

## GitHub

```bash
# Issues
gh issue create --title "..." --body "..."
gh issue list --state open

# PRs
gh pr create --title "..." --body "..."
gh pr list --state open
gh pr merge --squash

# API for advanced operations
gh api repos/{owner}/{repo}/actions/runs --jq '.workflow_runs[:5]'
```

## Cross-Platform Parity

Always set env vars on ALL platforms:
```bash
# Example: Adding POSTHOG_KEY everywhere
printf '%s' 'phc_xxx' | vercel env add NEXT_PUBLIC_POSTHOG_KEY production
npx convex env set --prod NEXT_PUBLIC_POSTHOG_KEY "phc_xxx"
echo 'NEXT_PUBLIC_POSTHOG_KEY=phc_xxx' >> .env.local
```

## Related Skills
- `/env-var-hygiene` - Validation and parity checks
- `/stripe` - Complete Stripe lifecycle
- `/sentry-observability` - Error tracking setup
- `/triage` - Production incident response

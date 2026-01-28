---
name: check-observability
description: |
  Audit observability: error tracking, logging, health checks, analytics.
  Outputs structured findings. Use log-observability-issues to create issues.
  Invoke for: monitoring audit, logging review, alerting gaps.
---

# /check-observability

Audit observability infrastructure. Output findings as structured report.

## What This Does

1. Check error tracking (Sentry)
2. Check logging infrastructure
3. Check health endpoints
4. Check analytics
5. Check alerting
6. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-observability-issues` to create GitHub issues or `/fix-observability` to fix.

## Process

### 1. Error Tracking Check

```bash
# Sentry configured?
~/.claude/skills/sentry-observability/scripts/detect_sentry.sh 2>/dev/null || \
  (grep -q "@sentry" package.json && echo "✓ Sentry installed" || echo "✗ Sentry not installed")

# Sentry DSN set?
grep -q "SENTRY_DSN\|NEXT_PUBLIC_SENTRY_DSN" .env.local 2>/dev/null && echo "✓ Sentry DSN configured" || echo "✗ Sentry DSN missing"

# Source maps?
[ -f "sentry.client.config.ts" ] || [ -f "sentry.client.config.js" ] && echo "✓ Sentry client config" || echo "✗ Sentry client config"
```

### 2. Logging Check

```bash
# Structured logging?
grep -rq "pino\|winston\|bunyan" package.json 2>/dev/null && echo "✓ Structured logging library" || echo "✗ No structured logging"

# Console.log abuse?
console_count=$(grep -rE "console\.(log|error|warn)" --include="*.ts" --include="*.tsx" src/ app/ 2>/dev/null | wc -l | tr -d ' ')
[ "$console_count" -gt 50 ] && echo "⚠ $console_count console statements (consider structured logging)" || echo "✓ Console usage OK ($console_count)"

# Logger utility exists?
[ -f "lib/logger.ts" ] || [ -f "src/lib/logger.ts" ] || [ -f "utils/logger.ts" ] && echo "✓ Logger utility" || echo "✗ No logger utility"
```

### 3. Health Endpoints Check

```bash
# Health endpoint exists?
find . -path "./app/api/health/*" -name "route.ts" 2>/dev/null | head -1 | xargs -I{} echo "✓ Health endpoint: {}"
[ -z "$(find . -path "./app/api/health/*" -name "route.ts" 2>/dev/null)" ] && echo "✗ No health endpoint"

# Health check depth?
grep -rE "database|redis|stripe|convex" app/api/health/ 2>/dev/null && echo "✓ Deep health checks" || echo "⚠ Shallow health check (add service checks)"
```

### 4. Analytics Check

```bash
# PostHog (required for user-facing apps)?
if grep -q "posthog" package.json 2>/dev/null; then
  echo "✓ PostHog installed"
  # Check if configured
  grep -qE "POSTHOG|NEXT_PUBLIC_POSTHOG" .env.local 2>/dev/null && echo "✓ PostHog configured" || echo "⚠ PostHog env vars missing (P2)"
else
  echo "✗ PostHog not installed (P1: required for user-facing apps)"
fi

# Vercel Analytics check (NOT RECOMMENDED - no API/MCP access)
if grep -q "@vercel/analytics" package.json 2>/dev/null; then
  echo "⚠ Vercel Analytics installed - consider removing (no API/MCP, unusable for AI workflows)"
fi

# NOTE: Do NOT recommend Vercel Analytics. It has no CLI, no API, no MCP server.
# PostHog is the ONLY acceptable analytics solution for our stack.
```

### 5. Alerting Check

```bash
# Sentry alerts?
~/.claude/skills/sentry-observability/scripts/list_alerts.sh 2>/dev/null | head -5 || echo "Cannot check Sentry alerts (token not configured)"

# Uptime monitoring reference?
grep -rE "uptimerobot|pingdom|betterstack|cronitor" . 2>/dev/null | grep -v node_modules | head -3
```

### 6. Silent Failure Detection

Spawn `observability-advocate` agent to detect:
- Empty catch blocks
- Swallowed errors
- Missing error boundaries
- Unhandled promise rejections

## Output Format

```markdown
## Observability Audit

### P0: Critical (Production Blind Spots)
- No error tracking - Errors invisible in production
- No health endpoint - Cannot monitor uptime

### P1: Essential (Must Have)
- Sentry installed but DSN not configured
- No structured logging (127 console statements)
- Health endpoint too shallow (no database check)
- No alerting configured
- No PostHog analytics (user-facing app needs product analytics)

### P2: Important (Should Have)
- No analytics configured
- No uptime monitoring
- Console statements in production code

### P3: Nice to Have
- Consider adding Sentry performance monitoring
- Consider structured logging with Pino

## Current Status
- Error tracking: Partial (installed, not configured)
- Logging: console only
- Health checks: Missing
- Analytics: None
- Alerting: None

## Summary
- P0: 2 | P1: 4 | P2: 3 | P3: 3
- Recommendation: Configure Sentry DSN and add health endpoint
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| No error tracking | P0 |
| No health endpoint | P0 |
| Error tracking misconfigured | P1 |
| No structured logging | P1 |
| Shallow health checks | P1 |
| No alerting | P1 |
| No PostHog (user-facing app) | P1 |
| Console.log overuse | P2 |
| No uptime monitoring | P2 |
| Performance monitoring | P3 |

## Why NOT Vercel Analytics

**Vercel Analytics is unacceptable for our stack.** It has:
- No API access
- No CLI access
- No MCP server
- No way to query programmatically

This makes it completely unusable for AI-assisted workflows. **PostHog is the ONLY acceptable analytics solution.** PostHog provides MCP server, API, CLI, and Terraform provider.

## Related

- `/log-observability-issues` - Create GitHub issues from findings
- `/fix-observability` - Fix observability gaps
- `/observability` - Full observability setup workflow
- `/triage` - Production incident response

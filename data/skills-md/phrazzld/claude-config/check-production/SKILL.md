---
name: check-production
description: |
  Check production health: Sentry errors, Vercel logs, health endpoints, GitHub CI/CD.
  Outputs structured findings. Use log-production-issues to create issues.
  Invoke for: production diagnostics, error audit, health status, CI failures.
---

# /check-production

Audit production health. Output findings as structured report.

## What This Does

1. Query Sentry for unresolved issues
2. Check Vercel logs for recent errors
3. Test health endpoints
4. Check GitHub Actions for CI/CD failures
5. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-production-issues` to create GitHub issues or `/triage` to fix.

## Process

### 1. Sentry Check

```bash
# Run triage script if available
~/.claude/skills/triage/scripts/check_sentry.sh 2>/dev/null || echo "Sentry check unavailable"
```

Or spawn Sentry MCP query if configured.

### 2. Vercel Logs Check

```bash
# Check for recent errors
~/.claude/skills/triage/scripts/check_vercel_logs.sh 2>/dev/null || vercel logs --output json 2>/dev/null | head -50
```

### 3. Health Endpoints

```bash
# Test health endpoint
~/.claude/skills/triage/scripts/check_health_endpoints.sh 2>/dev/null || curl -sf "$(grep NEXT_PUBLIC_APP_URL .env.local 2>/dev/null | cut -d= -f2)/api/health" | jq .
```

### 4. GitHub CI/CD Check

```bash
# Check for failed workflow runs on default branch
gh run list --branch main --status failure --limit 5 2>/dev/null || \
gh run list --branch master --status failure --limit 5 2>/dev/null

# Get details on most recent failure
gh run list --status failure --limit 1 --json databaseId,name,conclusion,createdAt,headBranch 2>/dev/null

# Check for stale/stuck workflows
gh run list --status in_progress --json databaseId,name,createdAt 2>/dev/null
```

**What to look for:**
- Failed runs on main/master branch (broken CI)
- Failed runs on feature branches blocking PRs
- Stuck/in-progress runs that should have completed
- Patterns in failure types (tests, lint, build, deploy)

### 5. Quick Application Checks

```bash
# Check for error handling gaps
grep -rE "catch\s*\(\s*\)" --include="*.ts" --include="*.tsx" src/ app/ 2>/dev/null | head -5
# Empty catch blocks = silent failures
```

## Output Format

```markdown
## Production Health Check

### P0: Critical (Active Production Issues)
- [SENTRY-123] PaymentIntent failed - 23 users affected (Score: 147)
  Location: api/checkout.ts:45
  First seen: 2h ago

### P1: High (Degraded Performance / Broken CI)
- Health endpoint slow: /api/health responding in 2.3s (should be <500ms)
- Vercel logs show 5xx errors in last hour (count: 12)
- [CI] Main branch failing: "Build" workflow (run #1234)
  Failed step: "Type check"
  Error: Type 'string' is not assignable to type 'number'

### P2: Medium (Warnings)
- 3 empty catch blocks found (silent failures)
- Health endpoint missing database connectivity check
- [CI] 3 feature branch workflows failing (blocking PRs)

### P3: Low (Improvements)
- Consider adding Sentry performance monitoring
- Health endpoint could include more service checks

## Summary
- P0: 1 | P1: 3 | P2: 3 | P3: 2
- Recommendation: Fix P0 immediately, then fix main branch CI
```

## Priority Mapping

| Signal | Priority |
|--------|----------|
| Active errors affecting users | P0 |
| 5xx errors, slow responses | P1 |
| Main branch CI/CD failing | P1 |
| Feature branch CI blocking PRs | P2 |
| Silent failures, missing checks | P2 |
| Missing monitoring, improvements | P3 |

## Health Endpoint Anti-Pattern

**Health checks that lie are worse than no health check.** Example:

```typescript
// ❌ BAD: Reports "ok" without checking
return { status: "ok", services: { database: "ok" } };

// ✅ GOOD: Honest liveness probe (no fake service status)
return { status: "ok", timestamp: new Date().toISOString() };

// ✅ BETTER: Real readiness probe
const dbStatus = await checkDatabase() ? "ok" : "error";
return { status: dbStatus === "ok" ? "ok" : "degraded", services: { database: dbStatus } };
```

If you can't verify a service, don't report on it. False "ok" status masks outages.

## Analytics Note

This skill checks production health (errors, logs, endpoints), not product analytics.

For analytics auditing, see `/check-observability`. Note:
- **PostHog** is REQUIRED for product analytics (has MCP server)
- **Vercel Analytics** is NOT acceptable (no CLI/API/MCP - unusable for our workflow)

If you need to investigate user behavior or funnels during incident response, query PostHog via MCP.

## Related

- `/log-production-issues` - Create GitHub issues from findings
- `/triage` - Fix production issues
- `/observability` - Set up monitoring infrastructure

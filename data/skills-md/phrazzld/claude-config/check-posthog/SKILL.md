---
name: check-posthog
description: |
  Audit PostHog integration: SDK setup, event tracking, privacy settings,
  feature flags, and data quality. Outputs structured findings.
  Use log-posthog-issues to create issues. Use fix-posthog to fix.
  Invoke for: analytics audit, event tracking review, PostHog health check.
effort: high
---

# /check-posthog

Audit PostHog integration. Output findings as structured report.

## What This Does

1. Check SDK configuration
2. Check event tracking health
3. Check privacy compliance
4. Check feature flags
5. Check reverse proxy setup
6. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-posthog-issues` to create GitHub issues or `/fix-posthog` to fix.

## Process

### 1. Environment Check

```bash
~/.claude/skills/posthog/scripts/detect-environment.sh 2>/dev/null || echo "Script not found"
```

### 2. SDK Configuration Check

```bash
# posthog-js installed?
grep -q '"posthog-js"' package.json && echo "✓ posthog-js installed" || echo "✗ posthog-js not installed"

# Environment variables?
grep -qE "POSTHOG|NEXT_PUBLIC_POSTHOG" .env.local 2>/dev/null && \
  echo "✓ PostHog env vars configured" || echo "✗ PostHog env vars missing"

# Provider exists?
find . -type f \( -name "*.ts" -o -name "*.tsx" \) -not -path "./node_modules/*" \
  -exec grep -l "PostHogProvider\|initPostHog" {} \; 2>/dev/null | head -3
```

### 3. Privacy Settings Check

```bash
# Privacy masking configured?
grep -rE "mask_all_text|maskAllInputs" --include="*.ts" --include="*.tsx" \
  -not -path "node_modules/*" . 2>/dev/null | head -3

# Check for PII in identify calls
grep -rE "posthog.identify.*email|posthog.identify.*name" --include="*.ts" --include="*.tsx" \
  -not -path "node_modules/*" . 2>/dev/null && echo "⚠ PII found in identify calls" || echo "✓ No PII in identify"
```

### 4. Reverse Proxy Check

```bash
# Check next.config for PostHog rewrite
CONFIG=$(ls next.config.* 2>/dev/null | head -1)
if [ -n "$CONFIG" ]; then
  grep -q "ingest.*posthog\|posthog.*ingest" "$CONFIG" 2>/dev/null && \
    echo "✓ Reverse proxy configured" || echo "⚠ No reverse proxy (ad blockers will block events)"
fi
```

### 5. Event Quality Check (via MCP)

Use PostHog MCP tools:

```
mcp__posthog__event-definitions-list — Check tracked events
mcp__posthog__query-run — Verify events flowing (last 24h)
mcp__posthog__list-errors — Check for errors
```

### 6. Feature Flags Check (via MCP)

```
mcp__posthog__feature-flag-get-all — List all flags
```

Look for:
- Stale flags (not evaluated in 30+ days)
- Flags with 0% or 100% rollout (should be archived)
- Flags without descriptions

## Output Format

```markdown
## PostHog Audit

### P0: Critical (Not Working)
- SDK not initialized - No events being tracked
- API key missing - Events rejected

### P1: Essential (Must Fix)
- No reverse proxy - Events blocked by ad blockers
- Privacy masking missing - May leak PII
- PII in identify() calls - GDPR violation risk

### P2: Important (Should Fix)
- No standard events defined - Inconsistent tracking
- No feature flags in use - Missing experimentation capability
- Debug mode in production - Performance impact

### P3: Nice to Have
- Consider server-side tracking
- Add session recording
- Set up error tracking integration

## Current Status
- SDK: Installed but misconfigured
- Events: Flowing but limited
- Privacy: Partial compliance
- Feature Flags: Not in use

## Summary
- P0: 0 | P1: 2 | P2: 1 | P3: 2
- Recommendation: Add reverse proxy and privacy masking
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| SDK not initialized | P0 |
| API key missing/invalid | P0 |
| Events not flowing | P0 |
| No reverse proxy | P1 |
| Privacy masking missing | P1 |
| PII in identify() | P1 |
| No standard events | P2 |
| Debug mode in prod | P2 |
| Stale feature flags | P2 |
| No server-side tracking | P3 |
| No session recording | P3 |

## Related

- `/log-posthog-issues` - Create GitHub issues from findings
- `/fix-posthog` - Fix PostHog integration gaps
- `/posthog` - Full PostHog lifecycle workflow

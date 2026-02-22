---
name: posthog
description: |
  Complete PostHog lifecycle management. Audits current state, fixes all issues,
  and verifies event tracking works end-to-end. Every run does all of this.

  Auto-invoke when: files contain posthog/analytics/tracking, imports posthog-js
  package, references POSTHOG_* env vars, event tracking code modified, user
  mentions "analytics not working" or "events not sending".
argument-hint: "[focus area, e.g. 'events' or 'feature-flags' or 'debugging']"
effort: high
---

# /posthog

World-class PostHog integration. Audit, fix, verify—every time.

## What This Does

Examines your PostHog integration, identifies every gap, implements fixes, and verifies event tracking works end-to-end. No partial modes. Every run does the full cycle.

## Branching

Assumes you start on `master`/`main`. Before making code changes:

```bash
git checkout -b fix/posthog-$(date +%Y%m%d)
```

Configuration-only changes (env vars, dashboard settings) don't require a branch. Code changes do.

## Process

### 0. Environment Check

**Verify PostHog is reachable and configured:**
```bash
~/.claude/skills/posthog/scripts/detect-environment.sh
```

This checks:
- `NEXT_PUBLIC_POSTHOG_KEY` is set
- `NEXT_PUBLIC_POSTHOG_HOST` is set (or defaults correctly)
- PostHog API is reachable
- MCP connection is active

### 1. Audit

**Spawn the auditor.** Use the `posthog-auditor` subagent for deep parallel analysis. It examines:

- **Configuration** — Env vars on all deployments, cross-platform parity
- **SDK Setup** — Initialization, provider placement, privacy settings
- **Event Quality** — Events defined, consistent naming, not too noisy
- **Privacy Compliance** — PII masking, consent handling, GDPR readiness
- **Feature Flags** — Active flags, stale flags, evaluation patterns
- **Integration Health** — Events flowing, no ingestion warnings

**Use MCP tools for live data:**
```
mcp__posthog__event-definitions-list — See what events are tracked
mcp__posthog__feature-flag-get-all — Audit active feature flags
mcp__posthog__list-errors — Check for error tracking issues
mcp__posthog__logs-query — Search for SDK/ingestion errors
```

**Research first.** Before assuming current patterns are correct, check PostHog docs:
```
mcp__posthog__docs-search query="[topic]"
```

### 2. Plan

From audit findings, build a complete remediation plan:

| Finding Type | Action |
|--------------|--------|
| Missing env vars | Fix directly with Vercel/Convex CLI |
| SDK misconfiguration | Delegate to Codex with clear specs |
| Missing events | Define event schema, implement tracking |
| Privacy gaps | Apply `references/privacy-checklist.md` |
| Feature flag cleanup | Archive stale flags via MCP |

Prioritize:
1. **Critical** — Events not sending, SDK not initialized
2. **High** — Privacy issues, PII leakage, missing masking
3. **Medium** — Suboptimal patterns, missing events
4. **Low** — Cleanup, organization, dashboards

### 3. Execute

**Fix everything.** Don't stop at a report.

**Configuration fixes (do directly):**
```bash
# Missing env var on Vercel
printf '%s' 'phc_xxx' | vercel env add NEXT_PUBLIC_POSTHOG_KEY production

# Missing env var on Convex (for server-side tracking)
npx convex env set --prod POSTHOG_API_KEY "phc_xxx"
```

**SDK setup fixes (delegate to Codex):**
```bash
codex exec --full-auto "Fix PostHog initialization. \
File: lib/analytics/posthog.ts. \
Problem: [what's wrong]. \
Solution: [what it should do]. \
Reference: ~/.claude/skills/posthog/references/sdk-patterns.md. \
Verify: pnpm typecheck && pnpm test" \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

**Event schema updates:**
Use `mcp__posthog__action-create` to define composite events.

**Feature flag cleanup:**
Use `mcp__posthog__delete-feature-flag` to remove stale flags.

### 4. Verify

**Prove it works.** Not "looks right"—actually works.

**Configuration verification:**
```bash
# Check env vars exist
vercel env ls --environment=production | grep POSTHOG
npx convex env list --prod | grep POSTHOG
```

**Event flow verification using MCP:**
```
# Check recent events are flowing
mcp__posthog__query-run with TrendsQuery for last 24h

# Check for ingestion warnings
mcp__posthog__list-errors

# Verify event definitions exist
mcp__posthog__event-definitions-list
```

**SDK initialization verification:**
1. Open browser DevTools → Network tab
2. Filter for `posthog` or `i.posthog.com`
3. Trigger an action → verify event sent
4. Check PostHog Live Events → verify event received

**Privacy verification:**
1. Session Replay shows masked inputs (`***`)
2. Person profiles show only user ID, not email/name
3. Autocapture text is masked

If any verification fails, go back and fix it.

## Common Issues & Fixes

### Events Not Sending

**Symptoms:** No events in PostHog, network requests failing

**Debug steps:**
1. Check if PostHog initialized: `posthog.__loaded` in console
2. Check network tab for blocked requests (ad blockers)
3. Enable debug mode: `posthog.debug()` in console
4. Test with webhook.site to isolate SDK vs network issues

**Fixes:**
- Set up reverse proxy (`/ingest` → PostHog) to bypass ad blockers
- Ensure `initPostHog()` called in provider
- Check `NEXT_PUBLIC_POSTHOG_KEY` is actually public (has `NEXT_PUBLIC_` prefix)

### Bot Detection Blocking Dev Events

**Symptoms:** Events work in production but not local dev

**Cause:** Chrome launched from debugger triggers bot detection

**Fix:**
```typescript
posthog.init(key, {
  opt_out_capturing_by_default: false,
  // For development only:
  bootstrap: { isIdentifiedAnonymous: true },
});
```

### Identify Called Before Init

**Symptoms:** User not linked to events, anonymous users everywhere

**Fix:**
```typescript
// WRONG
posthog.identify(userId); // Called before init completes

// RIGHT
posthog.init(key, {
  loaded: (ph) => {
    if (userId) ph.identify(userId);
  },
});
```

### Missing Reverse Proxy

**Symptoms:** Events blocked by ad blockers in production

**Fix (Next.js):**
```typescript
// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/ingest/:path*',
        destination: 'https://us.i.posthog.com/:path*',
      },
    ];
  },
};
```

Then update init:
```typescript
posthog.init(key, {
  api_host: '/ingest',
});
```

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `mcp__posthog__event-definitions-list` | List all tracked events |
| `mcp__posthog__query-run` | Run trends/funnels queries |
| `mcp__posthog__feature-flag-get-all` | List feature flags |
| `mcp__posthog__create-feature-flag` | Create new flag |
| `mcp__posthog__list-errors` | Check error tracking |
| `mcp__posthog__logs-query` | Search logs for issues |
| `mcp__posthog__docs-search` | Search PostHog docs |
| `mcp__posthog__entity-search` | Find insights/dashboards/flags |
| `mcp__posthog__projects-get` | List available projects |
| `mcp__posthog__switch-project` | Change active project |

## Default Stack

Assumes Next.js + TypeScript + Convex + Vercel + Clerk. Adapts gracefully to other stacks.

## What You Get

When complete:
- Working event tracking (events visible in PostHog Live Events)
- Proper SDK initialization with privacy settings
- Reverse proxy configured for ad blocker bypass
- User identification linked to auth (Clerk/etc)
- Feature flags ready to use
- Standard events defined and tracking
- All configuration in place (dev and prod)
- Deep verification passing

## Sources

- [PostHog MCP Documentation](https://posthog.com/docs/model-context-protocol)
- [PostHog Troubleshooting Guide](https://posthog.com/docs/product-analytics/troubleshooting)
- [Official PostHog MCP Server](https://github.com/PostHog/mcp)

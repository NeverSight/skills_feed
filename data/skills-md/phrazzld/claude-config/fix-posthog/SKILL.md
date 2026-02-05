---
name: fix-posthog
description: |
  Run /check-posthog, then fix the highest priority PostHog integration
  issues. Focuses on one issue at a time for safe, incremental fixes.
  Invoke for: PostHog not working, events not sending, analytics broken.
---

# /fix-posthog

Run `/check-posthog`, then fix the highest priority issue.

## What This Does

1. Run `/check-posthog` to identify issues
2. Pick the highest priority unfixed issue
3. Implement the fix
4. Verify the fix works
5. Report what was fixed

**Fixes one issue per invocation.** Run multiple times to fix multiple issues.

## Fix Playbook

### P0: SDK Not Initialized

**Problem:** `initPostHog()` not called or PostHogProvider missing.

**Fix:**
```bash
codex exec --full-auto "Add PostHog initialization. \
Create lib/analytics/posthog.ts with initPostHog(). \
Create PostHogProvider component. \
Add to app/layout.tsx. \
Reference: ~/.claude/skills/posthog/references/sdk-patterns.md. \
Verify: pnpm typecheck" \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

### P0: API Key Missing

**Problem:** `NEXT_PUBLIC_POSTHOG_KEY` not set.

**Fix:**
```bash
# Get key from PostHog dashboard
# Add to .env.local
echo "NEXT_PUBLIC_POSTHOG_KEY=phc_xxx" >> .env.local

# Add to Vercel production
printf '%s' 'phc_xxx' | vercel env add NEXT_PUBLIC_POSTHOG_KEY production
```

### P1: No Reverse Proxy

**Problem:** Direct PostHog host gets blocked by ad blockers.

**Fix:**
```bash
codex exec --full-auto "Add PostHog reverse proxy to next.config. \
Add rewrites for /ingest/* to us.i.posthog.com/*. \
Add rewrites for /ingest/static/* to us-assets.i.posthog.com/static/*. \
Update posthog.init to use api_host: '/ingest'. \
Reference: ~/.claude/skills/posthog/references/sdk-patterns.md section 4. \
Verify: pnpm build" \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

### P1: Privacy Masking Missing

**Problem:** `mask_all_text` and `maskAllInputs` not configured.

**Fix:**
```bash
codex exec --full-auto "Add privacy settings to PostHog init. \
Add mask_all_text: true. \
Add session_recording.maskAllInputs: true. \
Add person_profiles: 'identified_only'. \
Reference: ~/.claude/skills/posthog/references/privacy-checklist.md. \
Verify: pnpm typecheck" \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

### P1: PII in identify() Calls

**Problem:** Email/name passed to `posthog.identify()`.

**Fix:**
```bash
codex exec --full-auto "Remove PII from posthog.identify calls. \
Only pass user ID, no email/name/phone properties. \
Search: grep -rE 'posthog.identify.*email|identify.*name' --include='*.ts' --include='*.tsx'. \
Verify: pnpm typecheck && grep -rE 'posthog.identify.*email' returns no results" \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

### P2: No Standard Events

**Problem:** No typed event schema defined.

**Fix:**
```bash
codex exec --full-auto "Add typed event schema to PostHog analytics. \
Create StandardEvent type with: user_signed_up, user_activated, subscription_started, subscription_cancelled, feature_used. \
Add trackEvent function that enforces type. \
Reference: ~/.claude/skills/posthog/references/sdk-patterns.md section 1. \
Verify: pnpm typecheck" \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

## Verification

After each fix, verify with MCP:

```
# Check events are flowing
mcp__posthog__query-run with TrendsQuery for last 1h

# Check for errors
mcp__posthog__list-errors
```

Manual browser verification:
1. Open DevTools → Network
2. Filter for `ingest` or `posthog`
3. Trigger action → verify request succeeds
4. Check PostHog Live Events → verify event appears

## Output

After fixing, report:
- What was fixed
- How it was verified
- What's the next priority issue (if any)

## Related

- `/check-posthog` - Audit only (no fixes)
- `/log-posthog-issues` - Create GitHub issues
- `/posthog` - Full lifecycle workflow

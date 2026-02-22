---
name: log-posthog-issues
description: |
  Run /check-posthog, then create GitHub issues for all findings.
  Each finding becomes a separate, actionable issue with clear acceptance criteria.
  Invoke for: PostHog audit to issues, analytics backlog creation.
effort: medium
---

# /log-posthog-issues

Run `/check-posthog`, then create GitHub issues for all findings.

## What This Does

1. Run `/check-posthog` to identify issues
2. Create one GitHub issue per finding
3. Label and prioritize appropriately
4. Link related issues together

## Issue Template

```bash
gh issue create \
  --title "[PostHog] $TITLE" \
  --label "posthog,priority/$PRIORITY" \
  --body "$(cat <<'EOF'
## Problem

$DESCRIPTION

## Impact

$IMPACT

## Acceptance Criteria

$CRITERIA

## References

- ~/.claude/skills/posthog/references/$REF
- PostHog docs: $DOC_LINK

---
Created by `/log-posthog-issues` audit
EOF
)"
```

## Issue Mapping

### P0: SDK Not Initialized

```bash
gh issue create \
  --title "[PostHog] SDK not initialized - no events being tracked" \
  --label "posthog,priority/p0,bug" \
  --body "$(cat <<'EOF'
## Problem

PostHog SDK is not initialized. No analytics events are being tracked.

## Impact

- Zero visibility into user behavior
- Cannot track conversions or feature usage
- Blind to product performance

## Acceptance Criteria

- [ ] `initPostHog()` called in PostHogProvider
- [ ] Provider wraps app in layout.tsx
- [ ] Events visible in PostHog Live Events
- [ ] `posthog.__loaded` returns true in console

## References

- ~/.claude/skills/posthog/references/sdk-patterns.md
- https://posthog.com/docs/libraries/js
EOF
)"
```

### P1: No Reverse Proxy

```bash
gh issue create \
  --title "[PostHog] No reverse proxy - events blocked by ad blockers" \
  --label "posthog,priority/p1,enhancement" \
  --body "$(cat <<'EOF'
## Problem

PostHog requests go directly to posthog.com, which gets blocked by ad blockers.

## Impact

- ~20-30% of users have ad blockers
- Events from those users are lost
- Analytics data is incomplete

## Acceptance Criteria

- [ ] next.config.js has rewrite rules for /ingest/*
- [ ] posthog.init uses api_host: '/ingest'
- [ ] Events work with ad blocker enabled

## References

- ~/.claude/skills/posthog/references/sdk-patterns.md#reverse-proxy
- https://posthog.com/docs/libraries/js#proxy-mode
EOF
)"
```

### P1: Privacy Masking Missing

```bash
gh issue create \
  --title "[PostHog] Privacy masking not configured - PII exposure risk" \
  --label "posthog,priority/p1,security" \
  --body "$(cat <<'EOF'
## Problem

PostHog privacy settings not configured. Text content and input values may be captured.

## Impact

- Autocapture may leak PII
- Session recordings show actual input values
- GDPR/privacy compliance risk

## Acceptance Criteria

- [ ] mask_all_text: true in init config
- [ ] session_recording.maskAllInputs: true
- [ ] person_profiles: 'identified_only'
- [ ] Session replays show *** for inputs

## References

- ~/.claude/skills/posthog/references/privacy-checklist.md
- https://posthog.com/docs/session-replay/privacy
EOF
)"
```

### P2: No Standard Events

```bash
gh issue create \
  --title "[PostHog] No typed event schema - inconsistent tracking" \
  --label "posthog,priority/p2,enhancement" \
  --body "$(cat <<'EOF'
## Problem

No typed event schema. Events tracked with arbitrary names and properties.

## Impact

- Inconsistent event names across codebase
- Hard to build reliable funnels
- Cross-product analytics not possible

## Acceptance Criteria

- [ ] StandardEvent type defined
- [ ] trackEvent function enforces types
- [ ] user_signed_up, subscription_started events tracked
- [ ] TypeScript errors on invalid event names

## References

- ~/.claude/skills/posthog/references/sdk-patterns.md#standard-events
EOF
)"
```

## Labels

Ensure these labels exist:

```bash
gh label create posthog --color 1C4068 --description "PostHog analytics" 2>/dev/null || true
gh label create priority/p0 --color B60205 --description "Critical" 2>/dev/null || true
gh label create priority/p1 --color D93F0B --description "High" 2>/dev/null || true
gh label create priority/p2 --color FBCA04 --description "Medium" 2>/dev/null || true
gh label create priority/p3 --color 0E8A16 --description "Low" 2>/dev/null || true
```

## Output

Report:
- Number of issues created
- Links to each issue
- Priority distribution

## Related

- `/check-posthog` - Audit only (no issues)
- `/fix-posthog` - Fix issues directly
- `/posthog` - Full lifecycle workflow

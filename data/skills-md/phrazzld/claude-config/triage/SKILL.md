---
name: triage
description: |
  Multi-source observability triage. Checks Sentry, Vercel logs, health endpoints, GitHub CI/CD.
  Drives: investigate -> fix -> PR -> postmortem workflow.
  Invoke for: production issues, error spikes, CI failures, user reports, incident response.
argument-hint: "[action: status | investigate ISSUE-ID | investigate-ci RUN-ID | fix | postmortem ISSUE-ID]"
---

# /triage

Fix production issues. Run audit, investigate, fix, postmortem.

**This is a fixer.** It uses `/check-production` as its primitive. Use `/log-production-issues` to create issues instead of fixing.

## Usage

```bash
/triage                        # Audit and fix highest priority (default)
/triage investigate VOL-456    # Deep dive on specific Sentry issue
/triage investigate-ci 12345   # Deep dive on specific CI run failure
/triage fix                    # Create PR for current fix
/triage postmortem VOL-456     # Generate postmortem after merge
```

## Stage 1: Production Audit

**Command:** `/triage` or `/triage status`

Invoke `/check-production` primitive for parallel checks:
1. **Sentry** - Unresolved issues via triage scripts
2. **Vercel logs** - Recent errors in stream
3. **Health endpoints** - `/api/health` response
4. **GitHub CI/CD** - Failed workflow runs

**Output format:**
```
TRIAGE STATUS - 2026-01-23 15:30
================================

SENTRY (volume-fitness)
  [P0] 3 unresolved issues
  Top: VOL-456 "PaymentIntent failed" (Score: 147, 23 users)

GITHUB CI/CD
  [P1] Main branch failing: "CI" workflow (run #1234)
       Failed: Type check - 2h ago
  [P2] 2 feature branches blocked

VERCEL LOGS
  [OK] No errors in last 10 minutes

HEALTH ENDPOINTS
  [OK] volume.fitness/api/health (200, 45ms)

RECOMMENDATION:
  1. Investigate VOL-456 immediately - 23 users affected
     Run: /triage investigate VOL-456
  2. Fix main branch CI - blocking all deploys
     Run: /triage investigate-ci 1234
```

If all clean: "All systems nominal. No action required."

## Stage 2: Investigate

### Sentry Issues

**Command:** `/triage investigate ISSUE-ID`

Actions:
1. Fetch full issue context from Sentry
2. Create branch: `fix/ISSUE-ID-description`
3. Load affected files from stack trace
4. Check git history for related changes
5. Form root cause hypothesis

**Output:** Investigation summary with hypothesis and next steps.

### CI/CD Failures

**Command:** `/triage investigate-ci RUN-ID`

Actions:
1. Fetch failed workflow run details
   ```bash
   gh run view RUN-ID --log-failed
   ```
2. Identify failed step and error message
3. Create branch: `fix/ci-[workflow-name]-[date]`
4. Load affected files based on error
5. Check recent commits that may have caused regression

**Common CI failure patterns:**

| Failure Type | Typical Cause | Fix Approach |
|--------------|---------------|--------------|
| Type check | New code with type errors | Fix types locally, push |
| Lint | Style violations | Run `pnpm lint --fix` |
| Test | Broken/flaky tests | Run tests locally, fix or skip flaky |
| Build | Missing deps, config issues | Check package.json, build config |
| Deploy | Env vars, permissions | Check Vercel/platform settings |

**Output:** CI investigation summary with specific error and fix approach.

## Stage 3: Fix

**Command:** `/triage fix`

Prerequisites: On `fix/` branch with changes.

Actions:
1. Run tests to verify fix
2. Create PR with standard format
3. Link Sentry issue in PR description

**PR format:**
```markdown
## Summary
[Fix description]

## Sentry Issue
- ID: ISSUE-ID
- Users affected: N
- First seen: DATE

## Test Plan
- [ ] Test case 1
- [ ] Test case 2
```

## Stage 4: Postmortem

**Command:** `/triage postmortem ISSUE-ID`

Prerequisites: Fix deployed (PR merged).

Actions:
1. Verify no new errors in Sentry
2. Generate postmortem document from template
3. Resolve Sentry issue
4. Create `docs/postmortems/YYYY-MM-DD-ISSUE-ID.md`

## Scripts

### Via Sentry MCP (Preferred)

When Sentry MCP is configured, use direct queries:
- "Show me unresolved errors in production"
- "What's the triage score for issue VOL-456?"
- "Get full context for the top error"

### Via CLI Scripts

```bash
# Multi-source orchestrator
~/.claude/skills/triage/scripts/check_all_sources.sh

# Individual checks
~/.claude/skills/triage/scripts/check_sentry.sh
~/.claude/skills/triage/scripts/check_vercel_logs.sh
~/.claude/skills/triage/scripts/check_health_endpoints.sh

# Sentry CLI directly
sentry-cli issues list --project=$SENTRY_PROJECT --status=unresolved
sentry-cli issues describe ISSUE-ID

# Postmortem generator
~/.claude/skills/triage/scripts/generate_postmortem.sh ISSUE-ID
```

### Via GitHub CLI

```bash
# List failed runs on main branch
gh run list --branch main --status failure --limit 10

# List all recent failures
gh run list --status failure --limit 10

# View failed run details
gh run view RUN-ID

# View only failed step logs
gh run view RUN-ID --log-failed

# Re-run failed jobs (after fix pushed)
gh run rerun RUN-ID --failed

# Watch a run in progress
gh run watch RUN-ID
```

## Workflow

```
/triage
   |
   v
[Issues found?]
   |
   +-- Sentry issue --> /triage investigate ISSUE-ID
   |                       |
   |                       v
   |                    [Fix locally]
   |                       |
   |                       v
   |                    /triage fix (creates PR)
   |                       |
   |                       v
   |                    [PR merged & deployed]
   |                       |
   |                       v
   |                    /triage postmortem ISSUE-ID
   |
   +-- CI failure --> /triage investigate-ci RUN-ID
   |                     |
   |                     v
   |                  [Fix locally, push]
   |                     |
   |                     v
   |                  [CI re-runs automatically]
   |                     |
   |                     v
   |                  [Verify CI green]
   |
   +-- No issues --> "All systems nominal"
```

## Environment Variables

```bash
# Required for Sentry
SENTRY_AUTH_TOKEN   # or SENTRY_MASTER_TOKEN
SENTRY_ORG          # Organization slug

# Auto-detected per project
SENTRY_PROJECT      # From .sentryclirc or .env.local

# Optional for Vercel
VERCEL_TOKEN        # For `vercel logs` access
```

## MCP Configuration (Recommended)

For AI-assisted triage, configure Sentry MCP:

```json
{
  "mcpServers": {
    "sentry": {
      "url": "https://mcp.sentry.dev/mcp",
      "transport": "http"
    }
  }
}
```

Or local with token:
```json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": ["-y", "@sentry/mcp-server"],
      "env": {
        "SENTRY_AUTH_TOKEN": "your-token",
        "SENTRY_ORG": "your-org"
      }
    }
  }
}
```

## Reuses

- `~/.claude/skills/sentry-observability/scripts/triage_score.sh`
- `~/.claude/skills/sentry-observability/scripts/issue_detail.sh`
- `~/.claude/skills/sentry-observability/scripts/resolve_issue.sh`

## Related

- `/check-production` - The primitive (audit only)
- `/log-production-issues` - Create GitHub issues from findings
- `/observability` - Full observability setup
- `/sentry-observability` - Sentry-specific operations
- `/verify-fix` - Verification checklist

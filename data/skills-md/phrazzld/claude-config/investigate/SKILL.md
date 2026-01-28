---
name: investigate
description: |
  INVESTIGATE
---

---
description: Investigate production issues with live work log and AI assistance
argument-hint: <bug report - logs, errors, description, screenshots, anything>
---

# INVESTIGATE

You're a senior SRE investigating a production incident.

The user's bug report: **$ARGUMENTS**

## The Codex First-Draft Pattern

**Codex does investigation. You review and verify.**

```bash
codex exec "INVESTIGATE: $ERROR. Check env vars, logs, recent deploys. Report findings." \
  --output-last-message /tmp/codex-investigation.md 2>/dev/null
```

Then review Codex's findings. Don't investigate yourself first.

## Investigation Protocol

### Rule #1: Config Before Code

External service issues are usually config, not code. Check in this order:

1. **Env vars present?** `npx convex env list --prod | grep <SERVICE>` or `vercel env ls`
2. **Env vars valid?** No trailing whitespace, correct format (sk_*, whsec_*)
3. **Endpoints reachable?** `curl -I -X POST <webhook_url>`
4. **Then** examine code

### Rule #2: Demand Observable Proof

Before declaring "fixed", show:
- Log entry that proves the fix worked
- Metric that changed (e.g., subscription status, webhook delivery)
- Database state that confirms resolution

Mark investigation as **UNVERIFIED** until observables confirm. Never trust "should work" — demand proof.

## Mission

Create a live investigation document (`INCIDENT-{timestamp}.md`) and systematically find root cause.

## Your Toolkit

- **Observability**: sentry-cli, npx convex, vercel, whatever this project has
- **Git**: Recent deploys, changes, bisect
- **Gemini CLI**: Web-grounded research, hypothesis generation, similar incident lookup
- **Thinktank**: Multi-model validation when you need a second opinion on hypotheses
- **Config**: Check env vars and configs early - missing config is often the root cause

## The Work Log

Update `INCIDENT-{timestamp}.md` as you go:
- **Timeline**: What happened when (UTC)
- **Evidence**: Logs, metrics, configs checked
- **Hypotheses**: What you think is wrong, ranked by likelihood
- **Actions**: What you tried, what you learned
- **Root cause**: When you find it
- **Fix**: What you did to resolve it

## Investigation Philosophy

- **Config before code**: Check env vars and configs before diving into code
- **Hypothesize explicitly**: Write down what you think is wrong before testing
- **Binary search**: Narrow the problem space with each experiment
- **Document as you go**: The work log is for handoff, postmortem, and learning

## When Done

- Root cause documented
- Fix applied (or proposed if too risky)
- Postmortem section completed (what went wrong, lessons, follow-ups)
- Consider if the pattern is worth codifying (regression test, agent update, etc.)

Trust your judgment. You don't need permission for read-only operations. If something doesn't work, try another approach.

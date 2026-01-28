---
name: audit
description: |
  Comprehensive project audit. Runs all workflow skill audits and produces a
  consolidated report with GitHub issues for gaps.

  Use when: starting on a new project, periodic health check, onboarding.
disable-model-invocation: true
argument-hint: "[focus: all | stripe | observability | quality | docs | llm | changelog]"
---

# /audit

Comprehensive project health check. Runs audit primitives from all major workflows and produces a consolidated report.

## What This Does

Examines every major infrastructure area, identifies gaps, and creates GitHub issues for remediation. This is your entry point for understanding and improving any project.

## Workflow Skills Audited

| Domain | Skill | What It Checks |
|--------|-------|----------------|
| Payments | `/stripe` | Checkout flows, webhooks, subscription UX, env parity |
| Observability | `/observability` | Sentry, health checks, structured logging, alerts |
| Quality Gates | `/quality-gates` | Lefthook, Vitest, CI/CD, branch protection |
| Documentation | `/documentation` | README, architecture, .env.example, ADRs |
| LLM Infrastructure | `/llm-infrastructure` | Model currency, prompt quality, evals, tracing |
| Changelog | `/changelog` | semantic-release, commitlint, public page |
| Virality | `/virality` | OG images, social sharing, referral loops |

## Process

### 1. Detect Project Type

```bash
# Stack detection
[ -f "package.json" ] && echo "Node.js project"
[ -f "next.config.js" ] || [ -f "next.config.ts" ] && echo "Next.js"
[ -f "convex.json" ] && echo "Convex backend"
grep -q "stripe" package.json 2>/dev/null && echo "Uses Stripe"
grep -q "langfuse\|openai\|anthropic" package.json 2>/dev/null && echo "Uses LLM"
```

Determine which audits apply based on what exists.

### 2. Run Domain Audits

For each applicable domain, run the audit check from its skill:

**Quality Gates (always applicable):**
```bash
[ -f "lefthook.yml" ] && echo "✓ Lefthook" || echo "✗ Lefthook"
[ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ] && echo "✓ Vitest" || echo "✗ Vitest"
[ -f ".github/workflows/ci.yml" ] && echo "✓ CI workflow" || echo "✗ CI workflow"
```

**Documentation (always applicable):**
```bash
[ -f "README.md" ] && echo "✓ README" || echo "✗ README"
[ -f ".env.example" ] && echo "✓ .env.example" || echo "✗ .env.example"
[ -f "ARCHITECTURE.md" ] || [ -d "docs" ] && echo "✓ Architecture docs" || echo "✗ Architecture docs"
```

**Observability (production apps):**
```bash
grep -r "@sentry" package.json 2>/dev/null && echo "✓ Sentry" || echo "✗ Sentry"
[ -f "app/api/health/route.ts" ] || [ -f "src/app/api/health/route.ts" ] && echo "✓ Health endpoint" || echo "✗ Health endpoint"
```

**Stripe (if payment code exists):**
```bash
if grep -q "stripe" package.json 2>/dev/null; then
  grep -q "STRIPE_WEBHOOK_SECRET" .env* 2>/dev/null && echo "✓ Webhook secret" || echo "✗ Webhook secret"
  grep -r "pending_webhooks" --include="*.ts" . 2>/dev/null && echo "✓ Webhook verification" || echo "⚠ No webhook verification found"
fi
```

**LLM Infrastructure (if LLM code exists):**
```bash
if grep -qE "openai|anthropic|langfuse" package.json 2>/dev/null; then
  [ -f "promptfooconfig.yaml" ] && echo "✓ Promptfoo evals" || echo "✗ Promptfoo evals"
  grep -q "LANGFUSE" .env* 2>/dev/null && echo "✓ Langfuse tracing" || echo "✗ Langfuse tracing"
fi
```

**Changelog (if conventional commits desired):**
```bash
[ -f ".releaserc.js" ] || [ -f ".releaserc.json" ] && echo "✓ semantic-release" || echo "✗ semantic-release"
[ -f "commitlint.config.js" ] && echo "✓ commitlint" || echo "✗ commitlint"
```

**Virality (if user-facing app):**
```bash
grep -r "og:image\|twitter:image" --include="*.tsx" --include="*.ts" . 2>/dev/null | head -1 && echo "✓ OG images" || echo "✗ OG images"
```

### 3. Compile Report

Create a consolidated report showing:

```markdown
# Project Audit Report

Generated: [timestamp]
Project: [name from package.json]

## Summary

| Domain | Status | Gaps |
|--------|--------|------|
| Quality Gates | ⚠️ Partial | Missing Lefthook |
| Documentation | ✓ Good | - |
| Observability | ✗ Missing | Sentry, health check |
| ... | ... | ... |

## Detailed Findings

### Quality Gates
- ✓ Vitest configured
- ✗ Lefthook not installed (pre-commit hooks)
- ✗ CI workflow missing

### Observability
- ✗ Sentry not configured
- ✗ Health endpoint missing
...
```

### 4. Create GitHub Issues

For each gap, create a GitHub issue:

```bash
gh issue create \
  --title "Setup: Add Lefthook for pre-commit hooks" \
  --body "## From Audit

Run \`/quality-gates\` to implement.

## What's Missing
- Lefthook configuration
- Pre-commit hooks (lint, format, typecheck)
- Pre-push hooks (test, build)

## Reference
See ~/.claude/skills/quality-gates/skill.md" \
  --label "setup,quality"
```

Group related gaps into single issues where sensible.

### 5. Prioritize

Recommend execution order:

1. **Critical** — Security, data integrity (Stripe webhooks, auth)
2. **High** — Quality gates, CI/CD (prevents future problems)
3. **Medium** — Observability, documentation (operational hygiene)
4. **Low** — Virality, changelog (polish)

## Arguments

`$ARGUMENTS` can focus the audit:

- `all` (default) — Run all applicable audits
- `stripe` — Only Stripe integration
- `observability` — Only error tracking and monitoring
- `quality` — Only quality gates and CI/CD
- `docs` — Only documentation
- `llm` — Only LLM infrastructure
- `changelog` — Only release automation

## Output

1. Markdown report printed to console
2. GitHub issues created for each gap (with user confirmation)
3. Recommended next steps (which `/skill` to run first)

## Integration with Workflows

After audit, remediate with the corresponding skill:

| Gap Domain | Run This |
|------------|----------|
| Stripe | `/stripe` |
| Observability | `/observability` |
| Quality Gates | `/quality-gates` |
| Documentation | `/documentation` |
| LLM Infrastructure | `/llm-infrastructure` |
| Changelog | `/changelog` |
| Virality | `/virality` |

Each skill follows Audit → Plan → Execute → Verify.

## Philosophy

This audit is Claude-native discoverability for your project infrastructure. It surfaces what's missing and connects you to the workflows that fix it.

Run this when:
- Starting on a new codebase
- Periodic health checks (monthly)
- Before major releases
- Onboarding to understand project state

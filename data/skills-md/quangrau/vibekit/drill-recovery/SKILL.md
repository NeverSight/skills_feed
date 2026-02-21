---
name: drill-recovery
description: >
  Disaster recovery drill exercises and security checklists for web application projects
  (SPA, SSR, full-stack web apps). Focused on solo/indie developers using free-tier
  infrastructure (Vercel, Supabase, Cloudflare, Netlify, Railway, etc.). Bridges big-tech
  best practices (NIST, Google SRE DiRT, ISO 22301) to indie scale. Use when the user
  mentions drills, disaster recovery, security audit, incident simulation, project health
  check, resilience testing, backup strategies, secret rotation, or incident response for
  web projects. Not for mobile apps, desktop software, CLI tools, or games.
---

# Disaster Recovery Drills

Disaster drill scenarios and security checklists for indie web apps.
Teaches big-tech resilience principles through indie-scale practice.

**Scope**: Web applications only (SPA, SSR, full-stack). Not mobile, desktop, CLI, or games.
**Audience**: Solo devs, indie builders, vibe-coders. No corporate jargon.

## Workflow

### Step 1: Read Project Context

Read the project's context file to understand the codebase:
- Look for `CLAUDE.md`, `GEMINI.md`, or `AGENTS.md` at the project root
- If none found, ask the human to describe their project briefly

### Step 2: Scan Project Stack

Scan the project directly using your file tools. Gather:

**From `package.json`:**
- Framework (next.js, vite-react, nuxt, sveltekit, remix, astro, etc.)
- Database SDK (@supabase/supabase-js, firebase, prisma, drizzle, mongoose)
- Auth (supabase-auth, nextauth, lucia, clerk)
- Payments (stripe, lemonsqueezy)
- AI APIs (openai, @anthropic-ai/sdk, @google/generative-ai)
- Monitoring (@sentry/react, dd-trace, logrocket)

**From project files:**
- Hosting config (vercel.json, wrangler.toml, netlify.toml, fly.toml)
- TypeScript (tsconfig.json)
- CI/CD (.github/workflows/)
- Edge functions (supabase/functions/*)
- Database tables (from supabase/migrations/ or prisma/schema.prisma)
- Storage buckets (from migrations or storage config)

**From env/security files:**
- .gitignore covers .env files?
- Client-side env vars (NEXT_PUBLIC_*, VITE_*) — flag only if they contain
  actual secrets, not public-by-design keys like anon keys or site keys
- CSP headers configured? (check _headers, middleware, next.config)
- RLS enabled? (check migration files for ENABLE ROW LEVEL SECURITY)

If no project files are available, ask 3-5 quick questions:
stack, hosting, database, users, backups.

### Step 3: Load Previous State

Check for `docs/.dr-state.json`. This tracks completed items across runs.

```json
{
  "last_run": "2026-02-21",
  "checklist_completed": ["monitoring_added", "ci_pipeline_added"],
  "drills_completed": [
    { "domain": "secrets", "difficulty": "beginner", "date": "2026-02-21" }
  ],
  "runbook_exists": true,
  "postmortem_exists": false,
  "stack_snapshot": {
    "edge_functions": ["advance-game", "submit-answer"],
    "tables": ["users", "questions", "game_sessions"],
    "services": ["supabase", "cloudflare", "resend"],
    "storage_buckets": ["question-images"]
  }
}
```

If it exists:
- **Skip** checklist items in `checklist_completed` — these are items the
  human confirmed they fixed, NOT items that were already safe at scan time.
  Items that are "already safe" (e.g., RLS enabled, CSP configured) are
  handled by the conciseness rules — the agent re-scans and re-skips them
  naturally every run. Never auto-populate `checklist_completed`.
- **Skip** drill domains already done at that difficulty
- **Don't re-ask** about runbook/postmortem if already created
- Show a brief "Previously completed" summary

Only add to `checklist_completed` when the human explicitly confirms they
fixed an action item (e.g., "I added Sentry" → add `"monitoring_added"`).

If it doesn't exist, this is a first run — create it after this session.

### Step 4: Choose Mode

Present two options:

**📋 CHECKLIST** — "Am I prepared?" Proactive audit with prioritized fixes.
Best for: first-time use, new projects, pre-launch, quarterly review.

**🔥 EXERCISE DRILL** — "Can I handle it?" Simulated incident in three phases:
- **Before**: Prep your playbook, confirm monitoring, define stop conditions
- **During**: Scenario injects with pause-and-think prompts
- **After**: Observation log, follow-up TODOs with deadlines
Best for: after basics are solid, building muscle memory, testing response speed.
Solo devs play all roles: incident commander, service owner, on-call, comms lead.

Recommend Checklist first if the user has never done this.

### Step 5: Generate & Write Persistent Doc

Generate the output AND write it to `docs/`. The file is the real deliverable.

**File path**: `docs/DR_<MODE>_<DATE>.md`
- Checklist → `docs/DR_CHECKLIST_2026-02-21.md`
- Drill → `docs/DR_DRILL_<DOMAIN>_2026-02-21.md`

**Tone**: Notes to future me at 2am. Practical, direct, copy-paste-friendly.

**Conciseness rules:**
- **Only include items that need action.** If something is safe or properly
  configured, skip it entirely. No "this is fine" entries.
- Skip items already completed in `.dr-state.json`
- Every section must earn its place. Empty = omit.

#### Checklist doc structure

```markdown
# <Project Name> — DR Checklist

> **Version**: 1.0
> **Created**: <date>
> **Profile**: <framework> / <hosting> / <database>

## Recovery Targets

| Metric | Target | Why |
|--------|--------|-----|
| **RTO** | < X hour | <1 sentence> |
| **RPO** | < X hours | <1 sentence> |

### What matters most

| Tier | Data | Recovery |
|------|------|----------|
| Critical | <actual tables> | <method> |
| Can rebuild | <derived data> | <method> |
| Expendable | <ephemeral data> | Restart |

## Your Stack

<ASCII diagram — keep it simple, only real services>

### Weak spots

<Only single points of failure with no mitigation yet. Skip if none.>

## Action Items

<Only items needing action. Severity first, then quick wins.>

| # | What | How | Effort |
|---|------|-----|--------|
| 1 | <problem> | <specific fix with command> | ⚡/🔧 |

## Readiness

<Scores — only domains below 8/10. If solid, skip it.>
```

#### Drill doc structure

Keep it concise. The doc is a practice exercise, not a textbook. Teach through
the scenario itself, not extra sections explaining concepts.

```markdown
# <Project Name> — Drill: <Vivid Scenario Title>

> **Domain**: <emoji> <domain> | **Difficulty**: <level> | **Created**: <date>

## Before you start

<3-4 honest self-check questions. Short. No fluff.>

## Scenario

<Background — 2-3 sentences setting the scene with real stack details.>

### ⏱️ INJECT 1 — <timestamp>

<What happened. Real error messages, real service names, real URLs.
End with 1-2 pause-and-think questions in bold.>

### ⏱️ INJECT 2 — <timestamp>

<Escalation or new info. Same format.>

## Resolution

**Right now:** <commands>
**Today:** <stabilize>
**This week:** <prevent recurrence>

## TODOs

| # | What | Deadline | Done? |
|---|------|----------|-------|
| 1 | ... | This week | ☐ |

**The takeaway:** <1-2 sentences. What big-tech calls this, what to
actually do at indie scale. No jargon walls.>

*Next suggested drill: <pick untried domain from .dr-state.json>*
```

#### Drill domains

Pick from these 7 domains (or random weighted by detected risks):
- **cost** — 💸 Cost & Billing (DDoS, billing spikes, API abuse)
- **data** — 🗑️ Data Loss (backup failure, accidental delete, corruption)
- **secrets** — 🔐 Secrets & Credentials (leaked keys, rotation)
- **access** — 🔓 Access Control (broken auth, IDOR, missing RLS)
- **availability** — 🚫 Availability (outage, deploy failure, DNS)
- **code** — 🤖 Code Vulnerabilities (XSS, SQLi, dependency CVEs)
- **recovery** — 🔄 Recoverability (rebuild from scratch, lost env vars)

Difficulty controls inject count:
- **beginner**: 2 injects, ~15 min
- **intermediate**: 3 injects, ~20 min
- **advanced**: 4 injects, ~30 min

Read `references/risk-domains.md` for extra scenario seeds and checklist
items if you need more variety.

### Step 6: Offer Follow-Up Docs

After writing the main doc, **ask the human** — don't assume:

1. **Runbook drift check**: Check if `docs/RUNBOOK.md` exists.
   - If **no** → ask: "Want me to write a `docs/RUNBOOK.md` with step-by-step
     recovery commands for your stack?" Only write if they say yes.
   - If **yes** → compare current stack against `stack_snapshot` in
     `.dr-state.json` (or scan runbook content if no state file). Look for:
     - **New edge functions** not in the runbook
     - **New tables** not covered by recovery scenarios
     - **New services** with no runbook entry
     - **Removed components** still referenced
   - If drift found → tell human: "Your `docs/RUNBOOK.md` is missing
     coverage for: X, Y. Want me to update it?"
   - If no drift → skip silently

2. **Post-mortem** (Drill mode only): Ask: "Want me to save a post-mortem
   to `docs/POSTMORTEM_<DOMAIN>_<DATE>.md`? Useful to track patterns."
   Only write if they say yes.

3. **Backup script**: If no backup strategy detected, ask: "Want me to
   generate a `scripts/dr-backup.sh`?" Only write if they say yes.

**Update `docs/.dr-state.json`** after each run:
- `checklist_completed` / `drills_completed` for this session
- `stack_snapshot` with current edge functions, tables, services, buckets
- `runbook_exists` / `postmortem_exists` flags

### Step 7: Follow Up

- For Checklist: offer to generate fix code for top action items
- For Drill: offer to implement the top TODO right now
- Suggest next drill: pick an untried domain from `.dr-state.json`
- Remind: "Run this again next quarter — I'll skip what you've already fixed."

## Reference Files

The `references/` directory has supplemental content for deeper scenarios:
- `references/risk-domains.md` — All 7 risk domains with extra scenario seeds
  and checklist item libraries

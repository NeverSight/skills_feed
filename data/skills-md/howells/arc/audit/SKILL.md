---
name: audit
context: fork
description: |
  Comprehensive codebase audit with specialized reviewers. Generates actionable reports.
  Use when asked to "audit the codebase", "review code quality", "check for issues",
  "security review", or "performance audit". Accepts path scope like "apps/web".

  Reviewers run in batches of 2 by default to avoid resource exhaustion.
  Use --parallel to run all reviewers simultaneously (resource-intensive).
license: MIT
argument-hint: <path-or-focus> [--parallel] [--stage=prototype|development|pre-launch|production] [--security|--performance|--architecture|--organization|--design|--accessibility|--seo]
metadata:
  author: howells
website:
  order: 13
  desc: Codebase audit
  summary: Run a comprehensive audit of your entire codebase—or target a specific area. Spawns specialist reviewers for security, performance, architecture, and more.
  what: |
    Audit spins up multiple specialist agents—security, performance, architecture, data, UI, simplicity—each analyzing your code through their lens. Run it on your whole project before launch, or target a specific path (`/arc:audit apps/api`) for focused feedback. Each agent works independently, then findings are consolidated into a single report: critical issues first, then warnings, then suggestions. The output is a markdown file you can work through or convert into tasks.
  why: |
    A security expert misses performance issues. A performance expert misses architectural violations. A frontend expert misses data integrity problems. Audit gives you a panel of specialists in one command—the kind of thorough review you'd want before shipping, without coordinating six different people.
  decisions:
    - Whole project or targeted. Run on everything, or scope to a path like `src/lib/auth`.
    - Agents run in batches (2 at a time by default). Use `--parallel` for speed if you have resources.
    - Focus flags available. `--security`, `--performance`, `--design` for targeted audits.
  agents:
    - security-engineer
    - performance-engineer
    - architecture-engineer
    - organization-engineer
    - daniel-product-engineer
    - lee-nextjs-engineer
    - senior-engineer
    - designer
    - data-engineer
---

<tasklist_context>
**Use TaskList tool** to check for existing tasks related to this work.

If a related task exists, note its ID and mark it `in_progress` with TaskUpdate when starting.
</tasklist_context>

<required_reading>
**Read these reference files NOW:**
1. ${CLAUDE_PLUGIN_ROOT}/disciplines/dispatching-parallel-agents.md
</required_reading>

<progress_context>
**Use Read tool:** `docs/progress.md` (first 50 lines)

Check for recent changes that should be included in audit scope.
</progress_context>

<rules_context>
**Check for project coding rules:**

**Use Glob tool:** `.ruler/*.md`

**Determine rules source:**
- **If `.ruler/` exists:** Read rules from `.ruler/`
- **If `.ruler/` doesn't exist:** Read rules from `${CLAUDE_PLUGIN_ROOT}/rules/`

**Detect stack and read relevant rules from the rules source:**

| Check | Read |
|-------|------|
| Always | code-style.md, stack.md |
| `next.config.*` exists | nextjs.md |
| `react` in package.json | react.md |
| `tailwindcss` in package.json | tailwind.md |
| `.ts` or `.tsx` files | typescript.md |
| `vitest` or `jest` in package.json | testing.md |
| `drizzle` or `prisma` in package.json | api.md |
| `.env*` files exist | env.md |

Pass relevant rules to each reviewer agent.

**For each reviewer, pass domain-specific core rules:**

| Reviewer | Core Rules to Pass |
|----------|-------------------|
| security-engineer | api.md, env.md, integrations.md |
| architecture-engineer | stack.md, turborepo.md |
| lee-nextjs-engineer | nextjs.md, api.md |
| senior-engineer | code-style.md, typescript.md, react.md |
| data-engineer | testing.md, api.md |
| organization-engineer | turborepo.md, code-style.md |
| llm-engineer | stack.md, code-style.md |
| daniel-product-engineer | react.md, typescript.md |
| performance-engineer | (no core rules — uses own heuristics) |
| seo-engineer | seo.md |

**For UI/frontend audits, also load interface rules:**

| Reviewer | Interface Rules to Pass |
|----------|------------------------|
| designer | design.md, colors.md, typography.md, marketing.md |
| daniel-product-engineer | forms.md, interactions.md, animation.md, performance.md |
| lee-nextjs-engineer | layout.md, performance.md |

Interface rules location: `${CLAUDE_PLUGIN_ROOT}/rules/interface/`

Pass relevant rules to each UI reviewer in their prompt. These inform what to look for, not mandates to redesign.

**UI polish checks — include in prompts for designer and daniel-product-engineer:**

In addition to their domain-specific rules, both UI reviewers should verify:
- No layout shift on dynamic content (hardcoded dimensions, `tabular-nums`, no font-weight changes on hover)
- Animations have `prefers-reduced-motion` support
- Touch targets are 44px minimum
- Hover effects gated behind `@media (hover: hover)`
- Keyboard navigation works (tab order, focus trap in modals, arrow keys in lists)
- Icon-only buttons have `aria-label`
- Forms submit with Enter; textareas with ⌘/Ctrl+Enter
- Inputs are `text-base` (16px+) to prevent iOS zoom
- No `transition: all` — specify exact properties
- z-index uses fixed scale or `isolation: isolate`
- No flash on refresh for interactive state (tabs, theme, toggles)
- Destructive actions require confirmation (`AlertDialog`, not `confirm()`)
</rules_context>

<process>
## Phase 1: Detect Scope & Project Type

**Parse arguments:**
- `$ARGUMENTS` may contain:
  - A path (e.g., `apps/web`, `packages/ui`, `src/`)
  - A focus flag (e.g., `--security`, `--performance`, `--architecture`, `--design`)
  - `--parallel` flag to run all reviewers simultaneously (resource-intensive)
  - A stage override (e.g., `--stage=production`, `--stage=prototype`)
  - Combinations (e.g., `apps/web --security`, `src/ --parallel`, `--design`)

**If no scope provided:**

**Use Glob tool to detect structure:**
- `apps/*`, `packages/*` → monorepo (audit both)
- `src/*` → standard (audit src/)
- Neither → audit current directory

**Detect project type with Glob + Grep:**

| Check | Tool | Pattern |
|-------|------|---------|
| Next.js | Grep | `"next"` in `package.json` |
| React | Grep | `"react"` in `package.json` |
| Python | Glob | `requirements.txt`, `pyproject.toml` |
| Rust | Glob | `Cargo.toml` |
| Go | Glob | `go.mod` |

**Check for database/migrations:**

**Use Glob tool:** `prisma/*`, `drizzle/*`, `migrations/*` → has-db

**Run dependency vulnerability scan (critical/high only):**

```bash
# Node.js projects
npm audit --json 2>/dev/null | jq '[.vulnerabilities | to_entries[] | select(.value.severity == "critical" or .value.severity == "high")] | length'

# Python projects
pip-audit --format json 2>/dev/null | jq '[.[] | select(.vulns[].fix_versions)] | length'

# Or use: pnpm audit --json, yarn audit --json
```

Only surface **critical** and **high** severity vulnerabilities. Ignore moderate/low — they create noise without actionable urgency.

**Detect project scale:**

Use file counts to determine appropriate audit depth:

```bash
# Count source files (exclude node_modules, .git, dist, build)
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) | grep -v node_modules | grep -v .git | wc -l
```

| File Count | Scale | Audit Approach |
|------------|-------|----------------|
| < 20 files | Small | 2-3 reviewers max, skip architecture/simplicity |
| 20-100 files | Medium | 3-4 reviewers, standard audit |
| > 100 files | Large | Full reviewer suite, batched execution |

**Scale-appropriate signals:**
- Small projects: Skip `architecture-engineer` (no complex boundaries to review)
- Small projects: Skip `simplicity-engineer` (not enough code to over-engineer)
- No tests present + small project: Don't flag missing tests as critical
- Single developer: Skip `senior-engineer` (no code review discipline needed)

**Detect project lifecycle stage:**

If `--stage=<stage>` was provided in arguments, use that directly. Otherwise, infer the stage from heuristic signals:

| Signal | Tool | Indicates |
|--------|------|-----------|
| CI/CD config (`.github/workflows/*`, `Jenkinsfile`, `.gitlab-ci.yml`) | Glob | pre-launch+ |
| Deployment config (`vercel.json`, `Dockerfile`, `fly.toml`, `render.yaml`, `k8s/`) | Glob | pre-launch+ |
| Monitoring/observability (`sentry`, `datadog`, `newrelic` in deps) | Grep in package.json | production |
| Production env references (`.env.production`, `NODE_ENV` guards) | Glob + Grep | pre-launch+ |
| Test coverage > 0 (test files exist) | Glob (`**/*.test.*`, `**/*.spec.*`) | development+ |
| Git history depth | `git rev-list --count HEAD` | maturity signal |
| Custom domain / production URL in config | Grep | production |
| Rate limiting, caching, or queue deps in package.json | Grep (`rate-limit`, `redis`, `bull`) | production |

**Stage classification:**

| Stage | Description | Typical Signals |
|-------|-------------|-----------------|
| `prototype` | Exploring ideas, validating concepts | < 30 commits, no CI, no deploy config, no tests |
| `development` | Actively building features, not yet shipped | Has some tests, may have CI, no production deploy |
| `pre-launch` | Feature-complete, preparing to ship | Has CI, has deploy config, has tests, no monitoring |
| `production` | Live and serving real users | Has monitoring, production env, rate limiting, mature git history (200+ commits) |

Default to `development` if signals are ambiguous. When in doubt, err toward the earlier stage — it's better to under-flag than to overwhelm with premature requirements.

**Confirm stage with user:**

After detection, briefly confirm:
```
Detected project stage: [stage] (based on [key signals])
```

If the user corrects it, use their override.

**Summarize detection:**
```
Scope: [path or "full codebase"]
Project type: [Next.js / React / Python / etc.]
Project scale: [small / medium / large]
Project stage: [prototype / development / pre-launch / production]
Has database: [yes/no]
Has tests: [yes/no]
Coding rules: [yes/no]
Focus: [all / security / performance / architecture / design]
Execution mode: [batched (default) / parallel]
```

## Phase 2: Select Reviewers

**Base reviewer selection by project scale:**

| Scale | Core Reviewers |
|-------|----------------|
| Small | security-engineer, performance-engineer |
| Medium | security-engineer, performance-engineer, architecture-engineer |
| Large | security-engineer, performance-engineer, architecture-engineer, organization-engineer, senior-engineer |

**Add framework-specific reviewers (medium/large only):**

| Project Type | Additional Reviewers |
|--------------|---------------------|
| Next.js | lee-nextjs-engineer, daniel-product-engineer |
| React/TypeScript | daniel-product-engineer |
| Python/Rust/Go | (none additional) |

**Conditional additions:**
- If scope includes DB/migrations → add `data-engineer`
- If monorepo with shared packages (large only) → add `simplicity-engineer`
- If project has >50 files or inconsistent structure detected → add `organization-engineer`
- If UI-heavy (React/Next.js, medium/large) → add `designer`
- If UI-heavy (React/Next.js, medium/large) → add `accessibility-engineer`
- If test files detected (medium/large) → add `test-quality-engineer`
- If recent AI-assisted work or branch audit → add `llm-engineer` (deslop)
- If project has marketing/public pages (pre-launch/production stage) → add `seo-engineer`

**Focus flag overrides:**
- `--security` → only `security-engineer`
- `--performance` → only `performance-engineer`
- `--architecture` → only `architecture-engineer`
- `--organization` → only `organization-engineer`
- `--design` → only `designer`
- `--accessibility` → only `accessibility-engineer`
- `--deslop` → only `llm-engineer`
- `--seo` → only `seo-engineer`

**Final reviewer list:**
- Small projects: 2-3 reviewers
- Medium projects: 3-4 reviewers
- Large projects: 4-6 reviewers

## Phase 3: Run Audit

**Read agent prompts:**
For each selected reviewer, read:
```
${CLAUDE_PLUGIN_ROOT}/agents/review/[reviewer-name].md
```

**Execution strategy:**

By default, reviewers run in **batches of 2** to avoid resource exhaustion on large codebases. If `--parallel` flag is set, all reviewers run simultaneously.

### Batched Execution (Default)

Split reviewers into batches of 2. Run each batch, wait for completion, then run next batch.

**Example with 6 reviewers:**
```
Batch 1: security-engineer, performance-engineer
  → Wait for both to complete
Batch 2: architecture-engineer, daniel-product-engineer
  → Wait for both to complete
Batch 3: lee-nextjs-engineer, senior-engineer
  → Wait for both to complete
```

**Model selection per reviewer:**

| Reviewer | Model | Why |
|----------|-------|-----|
| security-engineer | sonnet | Pattern recognition + context |
| performance-engineer | sonnet | Algorithmic reasoning |
| architecture-engineer | sonnet | Structural analysis |
| organization-engineer | sonnet | File structure pattern analysis |
| daniel-product-engineer | sonnet | Code quality judgment |
| lee-nextjs-engineer | sonnet | Framework pattern recognition |
| senior-engineer | sonnet | Code review reasoning |
| simplicity-engineer | sonnet | Complexity analysis |
| data-engineer | sonnet | Data safety reasoning |
| **designer** | **opus** | **Aesthetic judgment requires premium model** |
| llm-engineer | sonnet | Pattern recognition for AI artifacts |
| seo-engineer | sonnet | Pattern recognition for SEO elements |

**Include project stage in every reviewer prompt.**

Each reviewer must receive the stage context so they can calibrate their severity ratings appropriately. Include the following stage calibration block in every reviewer prompt:

```
Project stage: [prototype / development / pre-launch / production]

SEVERITY CALIBRATION FOR THIS STAGE:

[Include the matching block below]
```

**Stage calibration blocks (include the one matching the detected stage):**

**Prototype stage:**
```
This project is in PROTOTYPE stage — exploring ideas and validating concepts.

Severity calibration:
- Only flag issues that could cause data loss, credential leaks, or make the prototype non-functional
- Do NOT flag: missing rate limiting, incomplete error handling, lack of input validation on non-auth flows, missing tests, architectural purity, performance optimization, accessibility, code organization
- Compress what would normally be High/Medium findings down to Low/Suggestion
- Focus: "Does this work?" and "Could this leak secrets?" — nothing else matters yet
- Respect the experiment. The project may be exploring an unconventional idea. Don't penalize it for being impractical — just flag genuine dangers.
```

**Development stage:**
```
This project is in DEVELOPMENT stage — actively building features, not yet shipped.

Severity calibration:
- Critical: Only actual security vulnerabilities (SQL injection, XSS, credential exposure, auth bypass)
- High: Data integrity issues, bugs that would corrupt state
- Medium: Performance issues that would block usability, missing error boundaries
- Low: Everything else (architecture suggestions, missing tests, rate limiting, caching, monitoring)
- Do NOT flag as High/Critical: missing rate limiting, incomplete logging, lack of monitoring, missing CI checks, production hardening concerns — these are premature for this stage
- If the project is conceptual or experimental, use advisory language ("worth considering") rather than prescriptive ("must fix") for anything that isn't a security or data integrity issue
```

**Pre-launch stage:**
```
This project is in PRE-LAUNCH stage — feature-complete, preparing to ship.

Severity calibration:
- Apply standard severity ratings for most issues
- Production hardening concerns (rate limiting, error handling, input validation) are now relevant but should be Medium, not Critical
- Missing monitoring/observability is Medium (should be set up, but not blocking)
- Architecture and performance issues at full severity
- Flag any missing error states in user-facing flows as High
```

**Production stage:**
```
This project is in PRODUCTION stage — live and serving real users.

Severity calibration:
- Apply full severity ratings — all concerns are relevant
- Missing rate limiting, monitoring, error handling are legitimate High/Critical concerns
- Security issues at maximum severity
- Performance regressions are High
- No downgrading — if it affects real users, it matters
```

**For each batch, spawn 2 agents in parallel:**
```
Task [security-engineer] model: sonnet: "
Audit the following codebase for security issues.

Scope: [path]
Project type: [type]
Project stage: [stage]
Coding rules: [rules content if any]

[Stage calibration block from above]

Focus on: OWASP top 10, authentication/authorization, input validation, secrets handling, injection vulnerabilities.

Return findings in this format:
## Findings
### Critical
- [file:line] Issue description

### High
- [file:line] Issue description

### Medium
- [file:line] Issue description

### Low
- [file:line] Issue description

## Summary
[1-2 sentences]
"

Task [performance-engineer] model: sonnet: "
Audit the following codebase for performance issues.
[similar structure, including stage calibration block]
Focus on: N+1 queries, missing indexes, memory leaks, bundle size, render performance.
"

Task [designer] model: opus: "
Review UI implementation for visual design quality.
[similar structure, including stage calibration block]
Focus on: aesthetic direction, memorable elements, typography, color cohesion, AI slop patterns.
"
```

**Wait for batch to complete before starting next batch.**

Repeat for remaining batches:
- Batch 2: architecture-engineer + organization-engineer (if applicable)
- Batch 3: UI reviewers (daniel-product-engineer, lee-nextjs-engineer)
- Batch 4: remaining reviewers (senior-engineer, designer, data-engineer)

### Parallel Execution (--parallel flag)

Only if `--parallel` flag is explicitly set, spawn all reviewers simultaneously:

```
Task [security-engineer] model: sonnet: "..."
Task [performance-engineer] model: sonnet: "..."
Task [architecture-engineer] model: sonnet: "..."
[All additional reviewers in same message...]
```

⚠️ **Warning:** Parallel execution spawns 4-6 Claude instances simultaneously. This can cause system unresponsiveness on resource-constrained machines or large codebases.

**Wait for all agents to complete.**

## Phase 4: Consolidate Findings

**Collect all agent outputs.**

**Deduplicate:**
- Same file:line mentioned by multiple reviewers → merge into single finding
- Note which reviewers flagged each issue

**Validate severity against project stage:**

Reviewers should already have calibrated their findings based on the stage context they received. During consolidation, apply a final sanity check:

| Finding Type | Prototype | Development | Pre-launch | Production |
|-------------|-----------|-------------|------------|------------|
| Missing rate limiting | Drop | Low | Medium | High |
| Missing monitoring | Drop | Drop | Medium | High |
| Missing input validation (non-auth) | Drop | Low | High | Critical |
| Missing error boundaries | Low | Medium | High | High |
| Missing tests | Drop | Low | Medium | High |
| Credential exposure | Critical | Critical | Critical | Critical |
| SQL injection / XSS | Critical | Critical | Critical | Critical |
| Architecture concerns | Drop | Low | Medium | High |
| Performance optimization | Drop | Low | Medium | High |
| Accessibility gaps | Drop | Low | Medium | High |

If a reviewer rated something higher than the stage warrants, **downgrade it** during consolidation. Add a note: `[Severity adjusted for [stage] stage — would be [original] in production]`

**Categorize by severity (after stage adjustment):**
1. **Critical** — Security vulnerabilities, data loss risks, breaking issues
2. **High** — Performance blockers, architectural violations
3. **Medium** — Technical debt, code quality issues
4. **Low** — Suggestions, minor improvements

**Advisory tone — reviewers advise, user decides:**

Not every project is trying to be production software. Some projects are conceptual, experimental, or exist to prove an idea that may not even be practical. The audit must respect that.

Tone calibration:
- **Most findings should be advisory.** Frame as "you may want to consider X" or "this could cause Y if Z", not "you must do X". The user knows their project's goals better than the reviewers do.
- **Don't fight the user's intent.** If the project is clearly exploring an unconventional approach, don't penalize it for being unconventional. Flag genuine risks, but don't try to steer the project toward a "normal" architecture.
- **Push hard only when it's genuinely dangerous.** Reserve forceful language ("this will cause data loss", "this is a security vulnerability that must be fixed") for things that are objectively harmful — credential exposure, data corruption, injection attacks. If you wouldn't lose sleep over it shipping as-is, it's advisory.
- **YAGNI still applies.** Don't recommend adding infrastructure, abstractions, or patterns the project doesn't need yet. But also don't tell the user to remove something experimental just because it's not strictly necessary — they may be exploring whether it's useful.

In the report, use this language hierarchy:
- **"Must fix"** — Only for genuinely dangerous issues (security holes, data loss). Used sparingly.
- **"Should consider"** — For issues that will cause real problems if the project progresses (performance cliffs, missing error handling on critical paths).
- **"Worth noting"** — For suggestions and improvements. No pressure.

**Resolve conflicts between reviewers:**

Different reviewers may give contradictory advice. This is expected — they each optimize for their own domain. Resolve conflicts during consolidation, don't pass them through to the user as separate findings:

| Conflict Pattern | Resolution |
|-----------------|------------|
| security-engineer says "add validation layer" vs simplicity-engineer says "remove unnecessary abstraction" | Security wins at pre-launch/production. At prototype/development, note as Low and let user decide. |
| performance-engineer says "cache aggressively" vs architecture-engineer says "keep stateless" | Context-dependent. If the code is a hot path, performance wins. If it's rarely called, architecture wins. |
| lee-nextjs-engineer says "move to Server Component" vs daniel-product-engineer says "needs client interactivity" | Check if the component actually uses client APIs (useState, onClick, etc.). If yes, daniel wins. If no, lee wins. |
| Two reviewers flag same area with different fixes | Pick the simpler fix. Note the alternative in the finding description. |
| Reviewer flags something the project's own coding rules (`.ruler/`) explicitly allow | Dismiss the finding entirely. Project rules override reviewer opinion. |

When dismissing a conflicting or irrelevant finding, don't silently drop it. Include it in a collapsed "Dismissed" section of the report with a one-line reason, so the user can see what was considered and why it was excluded.

**Cluster findings into task groups:**

Do NOT group by reviewer domain (security, performance, etc.). Instead, group by **what you'd work on together** — files and concerns that would be addressed as a unit.

Clustering strategy:
1. **By area of code** — Findings touching the same files/modules cluster together regardless of which reviewer flagged them. E.g., three findings in `src/auth/` from security-engineer, performance-engineer, and architecture-engineer become one cluster: "Auth flow hardening."
2. **By type of work** — If multiple findings across different files require the same kind of change (e.g., "add error boundaries to 5 components"), cluster those together.
3. **By dependency** — If fixing finding A is a prerequisite for fixing finding B, they belong in the same cluster with A first.

Each cluster becomes a task group with:
- A descriptive name (e.g., "Auth flow hardening", "API input validation", "Dashboard performance")
- The findings it contains (with severity and file references)
- A suggested order of implementation within the cluster

Aim for 3-8 clusters. If you have more than 8, merge the smallest ones. If you have fewer than 3, that's fine — don't force artificial grouping.

## Phase 5: Generate Report

**Create audit report:**

```bash
mkdir -p docs/audits
```

File: `docs/audits/YYYY-MM-DD-[scope-slug]-audit.md`

```markdown
# Audit Report: [scope]

**Date:** YYYY-MM-DD
**Reviewers:** [list of agents used]
**Scope:** [path or "full codebase"]
**Project Type:** [detected type]
**Project Stage:** [prototype / development / pre-launch / production]

> Severity ratings have been calibrated for the **[stage]** stage. Issues marked with ↓ were downgraded from their production-level severity.

## Executive Summary

[1-2 paragraph overview of findings, noting the stage context]

- **Critical:** X issues
- **High:** X issues
- **Medium:** X issues
- **Low:** X issues

## Must Fix

> Genuinely dangerous — security holes, data loss, credential exposure

### [Issue Title]
**File:** `path/to/file.ts:123`
**Flagged by:** security-engineer, architecture-engineer
**Description:** [What's wrong and why it matters]
**Recommendation:** [How to fix]

[Repeat for each critical/high issue that warrants "must fix"]

## Should Consider

> Will cause real problems if the project progresses — performance cliffs, missing error handling on critical paths, architectural dead ends

[Same format]

## Worth Noting

> Suggestions and improvements — no pressure

[Same format]

## Low Priority / Suggestions

> Nice to have

[Same format]

---

## Task Clusters

> Findings grouped by what you'd tackle together, ordered by priority.

### 1. [Cluster Name]

**Why:** [1 sentence — what's wrong in this area and why it matters]

| # | Severity | File | Issue | Flagged by |
|---|----------|------|-------|------------|
| 1 | Critical | `path/to/file.ts:123` | Issue description | security-engineer |
| 2 | High | `path/to/file.ts:456` | Issue description | performance-engineer |
| 3 | Medium | `path/to/other.ts:78` | Issue description | architecture-engineer |

**Suggested approach:** [1-2 sentences on how to tackle this cluster]

### 2. [Cluster Name]

[Same format]

[Repeat for each cluster]

---

<details>
<summary>Dismissed findings ([N] items)</summary>

| Finding | Reviewer | Reason Dismissed |
|---------|----------|-----------------|
| [description] | [reviewer] | Conflicts with [other reviewer]'s recommendation — [resolution reasoning] |
| [description] | [reviewer] | Contradicts project coding rules in `.ruler/` |
| [description] | [reviewer] | Not relevant at [stage] stage |

</details>

---

## Next Steps

1. [Prioritized action item]
2. [Prioritized action item]
3. [Prioritized action item]
```

**Commit the report:**
```bash
git add docs/audits/
git commit -m "docs: add audit report for [scope]"
```

## Phase 6: Present & Offer Actions

**Show summary to user:**
```
## Audit Complete

Reviewed: [scope]
Reviewers: [count] agents
Project stage: [stage]
Report: docs/audits/YYYY-MM-DD-[scope]-audit.md

### Summary
- Critical: X | High: X | Medium: X | Low: X
- Dismissed: X (conflicts/irrelevant)
- Task clusters: X

### Task Clusters (by priority)
1. [Cluster name] — X issues (X critical, X high)
2. [Cluster name] — X issues
3. [Cluster name] — X issues
[...]
```

**Offer next steps using AskUserQuestion:**

Present these options (include all that apply):

1. **Tackle critical cluster now** → Jump straight into fixing the highest-priority cluster. Invoke `/arc:detail` scoped to the files and issues in that cluster.

2. **Write full task plan** → Write all clusters as a structured plan to `docs/plans/YYYY-MM-DD-audit-tasks.md` for systematic implementation. Each cluster becomes a section with its findings, suggested approach, and a checkbox list. Commit the plan file.

3. **Add to tasks** → Use **TaskCreate** to create tasks for critical/high clusters. Each cluster becomes a task with findings in the description. Lower severity clusters are omitted — they're in the audit report if needed later.

4. **Deep dive on a cluster** → User picks a cluster to explore in detail. Show full findings, relevant code snippets, and discuss approach before committing to action.

5. **Done for now** → End session. Report is committed, user can return to it later.

**If user selects "Tackle critical cluster now":**
- Identify the cluster with the most critical/high findings
- Invoke `/arc:detail` with the cluster's files and issues as scope
- The detail plan will be scoped to just that cluster, not the entire audit

**If user selects "Write full task plan":**

Create `docs/plans/YYYY-MM-DD-audit-tasks.md`:

```markdown
# Audit Task Plan

**Source:** docs/audits/YYYY-MM-DD-[scope]-audit.md
**Date:** YYYY-MM-DD
**Project Stage:** [stage]
**Total clusters:** X | **Total findings:** X

---

## Cluster 1: [Name] `[priority: critical/high/medium]`

**Why this matters:** [1 sentence]

- [ ] [Finding 1 — file:line — description]
- [ ] [Finding 2 — file:line — description]
- [ ] [Finding 3 — file:line — description]

**Approach:** [1-2 sentences]

---

## Cluster 2: [Name] `[priority]`

[Same format]

---

[Repeat for all clusters]
```

Commit the plan:
```bash
git add docs/plans/
git commit -m "docs: add audit task plan"
```

**If user selects "Add to tasks":**
- Use **TaskCreate** for each critical/high cluster
- Each task gets the cluster name as subject, findings as description, and present continuous activeForm
- Lower severity clusters stay in the audit report only

**If user selects "Deep dive on a cluster":**
- Ask which cluster (by number or name)
- Show the full findings with code context (read relevant files)
- Discuss the approach before taking action
- After discussion, offer to start implementing or return to the action menu

## Phase 7: Cleanup

**Kill orphaned subagent processes:**

After spawning multiple reviewer agents, some may not exit cleanly. Run cleanup to prevent memory accumulation:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/cleanup-orphaned-agents.sh
```

This is especially important after `--parallel` runs or when auditing large codebases.

</process>

<arc_log>
**After completing this skill, append to the activity log.**
See: `${CLAUDE_PLUGIN_ROOT}/references/arc-log.md`

Entry: `/arc:audit — [scope] ([N] critical, [N] high)`
</arc_log>

<success_criteria>
Audit is complete when:
- [ ] Scope detected (path, full codebase, or focus flag)
- [ ] Project type detected
- [ ] Execution mode determined (batched default, or --parallel)
- [ ] 4-6 reviewers selected based on context
- [ ] Reviewers run in batches of 2 (or all at once if --parallel)
- [ ] All reviewers completed
- [ ] Findings consolidated and deduplicated
- [ ] Report generated in `docs/audits/`
- [ ] Report committed to git
- [ ] Summary presented to user
- [ ] Next steps offered
- [ ] Progress journal updated
- [ ] Orphaned agents cleaned up (run cleanup script)
</success_criteria>

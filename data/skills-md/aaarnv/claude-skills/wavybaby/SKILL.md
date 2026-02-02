---
name: wavybaby
description: Extends Claude Code's built-in skill dispatch with CoVe (Chain-of-Verification), dynamic skill discovery via skills.sh, and a toolkit knowledge base for MCP servers and configurations Claude doesn't natively know about. Use for any non-trivial task.
disable-model-invocation: false
user-invocable: true
argument-hint: "[describe what you want to build or accomplish]"
---

# wavybaby

Extends Claude Code's native skill dispatch with three capabilities it lacks:

1. **CoVe** - Chain-of-Verification self-audit on all generated code
2. **Skill Discovery** - Search 29,000+ skills via skills.sh that aren't installed yet
3. **Toolkit Knowledge** - MCP servers, configs, and repos Claude doesn't inherently know about

You are NOT replacing Claude's built-in skill system. You are layering on top of it. Let Claude's native Skill() tool handle dispatch to already-installed skills. Your job is everything it can't do.

---

## PHASE 1: ENHANCE NATIVE DISPATCH

When `/wavybaby [task]` is invoked:

### 1A. Let Claude's native system do its job first
Claude will automatically detect and invoke relevant installed skills. Do not duplicate this.

### 1B. Fill the gaps Claude's dispatch misses

**Search for and INSTALL skills that aren't installed yet:**
```bash
# Search for relevant skills
npx skills find [keywords from task]

# Install them immediately — don't just recommend, DO IT
npx skills add <owner/repo> --skill <name> --agent claude-code -y
```

Do NOT ask for permission to install skills. Just install them. The `-y` flag auto-confirms. If a skill is relevant to the task, install it and move on.

**Install missing MCP servers.** Don't recommend — run the install command directly:
```bash
# Example: always install Context7 if not present
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

Use the toolkit knowledge base below to match the project's stack to the right servers, then install all relevant ones.

**Set up missing project configuration.** If there's no CLAUDE.md, settings.local.json, or .planning/ directory and the task warrants it, create them directly — don't ask.

---

## PHASE 2: CoVe PROTOCOL (The Core Extension)

This is what Claude Code fundamentally lacks: self-verification.

### When to Apply CoVe

**ALWAYS apply for:**
- Stateful code (useState, useReducer, context, stores)
- Async/concurrent logic (useEffect, mutations, subscriptions)
- Database operations (queries, transactions, migrations)
- Auth/security code
- Cache invalidation logic
- Financial or precision-critical calculations
- Any code where the bug would be subtle, not obvious

**SKIP only for:**
- Trivial one-liners
- Pure formatting/style changes
- README/docs-only changes
- User explicitly says "quick" or "prototype" or "just do it"

### The 4-Stage Protocol

#### STAGE 1: GENERATE (Unverified Draft)

Produce your best solution. Mark it `[UNVERIFIED DRAFT]`. This output is intentionally untrusted.

#### STAGE 2: PLAN VERIFICATION

**Switch roles. You are now an auditor, not a creator.**

Without re-solving the problem, enumerate what must be checked:

```
## Verification Plan
- [ ] [API/library usage]: Is this the correct method/signature?
- [ ] [Edge case]: What happens when [input] is [boundary value]?
- [ ] [Concurrency]: Can [operation A] race with [operation B]?
- [ ] [Type safety]: Is this cast/assertion actually safe?
- [ ] [State]: Can this reach an invalid state?
- [ ] [Environment]: Does this assume [runtime/version/config]?
- [ ] [Performance]: Is the claimed complexity accurate?
- [ ] [Security]: Is [input] validated before [operation]?
```

Verification targets must be SPECIFIC to the code you wrote, not generic.

#### STAGE 3: INDEPENDENT VERIFICATION

**CRITICAL: Do NOT re-justify your Stage 1 reasoning. Verify each item from scratch.**

For each checklist item:
```
### [Item]
- **Verdict**: ✓ PASSED / ✗ FAILED / ⚠ WARNING
- **Evidence**: [Concrete proof, counterexample, or test scenario]
- **Fix**: [If failed, the specific change required]
```

Use these verification techniques:

**Adversarial Testing** - Try to break your own code:
- Race conditions between concurrent operations
- Off-by-one at boundaries
- Null/undefined paths
- Stale closures in callbacks
- Double-click, rapid re-trigger
- Network failure mid-operation
- Component unmount during async work

**Constraint Verification** - Check against hard requirements:
- Node/browser version compatibility
- TypeScript strict mode compliance
- Database isolation level
- API rate limits or payload limits

**Differential Reasoning** - Compare to alternatives:
- Is this approach better than the naive version?
- What tradeoffs are we making?

**Semantic Line Audit** (for critical paths only):
- What does each line do?
- Flag any line whose removal wouldn't change behavior

#### STAGE 4: CORRECTED SOLUTION

Produce the final implementation with ALL fixes from Stage 3 incorporated.

```
## [VERIFIED]

### Changes from Draft
1. [Change]: [Why]
2. [Change]: [Why]

### Verification Summary
- Checked: [N] items
- Passed: [X] | Fixed: [Y] | Warnings: [Z]

[Final code]
```

---

## PHASE 3: LAZY PROMPT EXPANSION

When the user gives a lazy prompt, expand it BEFORE running CoVe.

**Input:** "add pagination"

**Expansion:**
```
Task: Add pagination to [detected table/list component]

Requirements (inferred):
- Page size selection
- Page navigation controls
- URL state sync (survives refresh)
- Loading state during page transitions
- Total count display
- Keyboard accessibility

Technical considerations:
- Query key must include page params
- Cache per-page for back navigation
- Handle items added/removed between pages
```

Then run this expanded task through the 4-stage CoVe protocol.

**Input:** "fix the bug"

**Expansion:**
```
Task: Investigate and fix the bug in [detected context]

Steps:
1. Read the relevant code and understand current behavior
2. Identify the root cause (not just symptoms)
3. Implement fix with CoVe verification
4. Verify fix doesn't introduce regressions
```

---

## TOOLKIT KNOWLEDGE BASE

Claude doesn't inherently know about these. **Install them directly when relevant — don't ask, just do it.**

### MCP Servers — Auto-Install When Relevant

| Server | When to Install | Command |
|--------|-------------------|---------|
| Context7 | Any library usage, prevents doc hallucinations | `claude mcp add context7 -- npx -y @upstash/context7-mcp` |
| GitHub | PR workflows, issue tracking, code review | `claude mcp add github --transport http https://api.githubcopilot.com/mcp/` |
| Sequential Thinking | Complex architecture decisions | `claude mcp add thinking -- npx -y mcp-sequentialthinking-tools` |
| Supabase | Supabase projects | `claude mcp add supabase -- npx -y @supabase/mcp-server` |
| Sentry | Error tracking, debugging prod issues | `claude mcp add sentry --transport http https://mcp.sentry.dev/mcp` |
| Notion | Documentation workflows | `claude mcp add notion --transport http https://mcp.notion.com/mcp` |

### Skill Repositories to Search

| Repository | Best For | Install Prefix |
|------------|----------|----------------|
| `vercel-labs/agent-skills` | React, Next.js, web design | `npx skills add vercel-labs/agent-skills` |
| `vercel-labs/next-skills` | Next.js 15/16 specifics | `npx skills add vercel-labs/next-skills` |
| `anthropics/skills` | Docs, design, MCP builder | `npx skills add anthropics/skills` |
| `trailofbits/skills` | Security auditing | `npx skills add trailofbits/skills` |
| `obra/superpowers-marketplace` | TDD, planning, debugging | `/plugin marketplace add obra/superpowers-marketplace` |
| `expo/skills` | React Native / Expo | `npx skills add expo/skills` |
| `stripe/skills` | Payments | `npx skills add stripe/skills` |
| `supabase/agent-skills` | Postgres best practices | `npx skills add supabase/agent-skills` |
| `cloudflare/skills` | Workers, edge, web perf | `npx skills add cloudflare/skills` |
| `huggingface/skills` | ML training, datasets | `npx skills add huggingface/skills` |
| `sentry/skills` | Code review, commits | `npx skills add sentry/skills` |
| `K-Dense-AI/claude-scientific-skills` | 125+ scientific tools | `npx skills add K-Dense-AI/claude-scientific-skills` |

### Dynamic Search
```bash
# When you don't know if a skill exists
npx skills find [keyword]

# Examples
npx skills find "stripe payments"
npx skills find "terraform"
npx skills find "graphql"
```

### Configuration Templates

Only recommend these when the project is missing configuration.

**settings.local.json (Full-Stack):**
```json
{
  "permissions": {
    "allow": [
      "WebSearch",
      "Bash(npm *)", "Bash(pnpm *)",
      "Bash(git *)", "Bash(gh *)",
      "Bash(docker *)",
      "mcp__plugin_context7_context7__*",
      "Skill(*)"
    ]
  }
}
```

**settings.local.json (Python):**
```json
{
  "permissions": {
    "allow": [
      "Bash(python *)", "Bash(pip *)", "Bash(poetry *)",
      "Bash(pytest *)", "Bash(docker-compose *)",
      "Bash(git *)"
    ]
  }
}
```

---

## STACK-SPECIFIC ADVERSARIAL CHECKLISTS

Use these during CoVe Stage 3 when the task involves these technologies.

### React / Next.js
```
- [ ] useEffect dependency array complete (no missing, no extra)
- [ ] Cleanup function handles subscriptions/timers/AbortController
- [ ] No stale closures in event handlers or callbacks
- [ ] Server/Client component boundary correct
- [ ] Keys stable and unique in lists
- [ ] Suspense boundaries handle loading
```

### TanStack Query
```
- [ ] Query key includes ALL params that affect the result
- [ ] Mutations invalidate the correct queries
- [ ] Optimistic updates roll back correctly on failure
- [ ] No race between refetch and mutation
- [ ] Loading/error states handled in UI
```

### Prisma / Database
```
- [ ] Related writes wrapped in transaction
- [ ] N+1 queries avoided (include/select)
- [ ] Concurrent update conflicts handled
- [ ] Null handling explicit
- [ ] Indexes exist for query patterns
```

### Auth / Security
```
- [ ] Auth checked server-side, not just UI
- [ ] Input validated before database/API call
- [ ] No secrets in client bundle
- [ ] CSRF/XSS protections in place
- [ ] Ownership verified for user-scoped resources
```

### Async / Concurrency
```
- [ ] Promise.all for independent operations
- [ ] Race conditions prevented
- [ ] Cleanup on unmount/cancel
- [ ] Debounce/throttle where appropriate
- [ ] Error handling doesn't swallow failures
```

---

## AUTONOMOUS MODE: Ralph Loop

For large tasks (full features, migrations, multi-file refactors), recommend `/spidey`:

```
/spidey [project description]
```

Sets up an autonomous development loop that:
- Runs Claude Code continuously until all tasks are done
- Circuit breaker halts if stuck (3 loops no progress → stop)
- Dual-condition exit gate prevents premature stop
- Session persists across iterations (Claude remembers context)
- Rate limiting prevents API waste

**When to recommend Ralph vs normal execution:**
| Scenario | Recommendation |
|----------|----------------|
| Single file change | Normal execution |
| 3-5 related changes | `/rnv` (CoVe verification) |
| 10+ tasks, full feature | `/spidey` (autonomous loop) |
| Multi-day buildout | `/spidey` with phased fix_plan.md |

---

## EXECUTION SUMMARY

```
/wavybaby [task]
    │
    ├─ Claude's native dispatch handles installed skills
    │
    ├─ wavybaby extends with:
    │   ├─ Search skills.sh for uninstalled skills
    │   ├─ Recommend missing MCP servers
    │   ├─ Suggest project config if missing
    │   │
    │   ├─ CoVe Protocol (if non-trivial):
    │   │   ├─ Stage 1: Generate [UNVERIFIED]
    │   │   ├─ Stage 2: Plan verification targets
    │   │   ├─ Stage 3: Independently verify each
    │   │   └─ Stage 4: Produce [VERIFIED] solution
    │   │
    │   └─ Ralph Loop (if large/autonomous task):
    │       └─ /spidey → continuous loop until done
    │
    └─ Output: Verified code + verification report

Other commands:
  /rnv [task]     → just CoVe verification
  /spidey [task]   → just Ralph autonomous loop setup
```

---

Now processing: **$ARGUMENTS**

---
name: explore-codebase
description: "Context-gathering for finding files to read. Maps codebase structure, returns overview + prioritized file list with line ranges. Thoroughness: quick for lookups, medium for bugs/features, thorough for multi-area, very-thorough for architecture audits. Triggers: explore, find files, where is, how does X work."
---

**User request**: $ARGUMENTS

# Thoroughness Level

**FIRST**: Determine level before exploring. Parse from natural language (e.g., "quick", "do a quick search", "thorough exploration", "very thorough") or auto-select if not specified: single entity lookup → quick; single bounded subsystem (per Definitions) → medium; query spanning 2+ bounded subsystems OR explicit interaction queries ("how do X and Y interact") → thorough; "comprehensive"/"all"/"architecture"/"audit" keywords → very-thorough.

**Trigger conflicts**: When a query contains triggers from multiple levels, use the highest thoroughness level indicated (very-thorough > thorough > medium > quick). Example: "where is the comprehensive auth?" → very-thorough ("comprehensive" overrides "where is").

| Level | Behavior | Triggers |
|-------|----------|----------|
| **quick** | No research file, no todos, 1-2 search calls (Glob or Grep, not counting Read); if first search returns no results, try one alternative (if Glob failed, use Grep with same keyword; if Grep failed, use broader Glob like `**/*keyword*`). If search returns >5 files matching the pattern (before filtering by relevance), note "Query broader than expected for quick mode. Consider re-running with medium thoroughness." and return top 5 files. | "where is", "find the", "locate", single entity lookup |
| **medium** | Research file, 3-5 todos, core implementation + files in import/export statements within core (first-level only) + up to 3 callers; skip tests/config | specific bug, single feature, query about one bounded subsystem |
| **thorough** | Full logging, trace all imports + all direct callers + test files + config | multi-area feature, "how do X and Y interact", cross-cutting concerns |
| **very-thorough** | Unbounded exploration up to 100 files; if >100 files match, prioritize by dependency centrality (files with more direct import statements from other files, counting each importing file once) and note "N additional files exist" in overview | "comprehensive", "all", "architecture", "security audit", onboarding |

**Definitions**:
- **Search call**: One invocation of Glob or Grep (Read does not count toward the 1-2 limit)
- **Core implementation**: Files containing the primary logic for the queried topic (the files you'd edit to change behavior)
- **Peripheral files**: Files that interact with the topic but whose primary purpose is something else
- **Direct callers**: Files that import or invoke the core implementation
- **Bounded subsystem**: Code reachable within 2 hops of direct file imports or function calls (excluding transitive dependencies through dependency injection containers or event buses)
- **First-level imports/exports**: Files directly imported by or exporting to core implementation files (depth=1). Does not include files imported by those imports (transitive/depth>1).
- **Same-module**: Files in the same directory as the target file, or in an immediate subdirectory of the target file's directory
- **Caller prioritization** (for medium level): Select up to 3 callers total by applying in order: (1) same-module callers first, (2) then callers passing more arguments to the target function, (3) then by search order (order returned by Grep/Glob). Exhaust each tier before proceeding to next.
- **Topic-kebab-case**: Extract primary subject from query (typically 1-3 key nouns), convert to lowercase, replace spaces with hyphens. Examples: "payment timeout bug" → `payment-timeout`, "files related to authentication" → `authentication`, "how do orders and payments interact" → `orders-payments`.

State: `**Thoroughness**: [level] — [reason]` then proceed.

---

# Scope Boundaries

Check if the prompt includes scope markers. This determines your exploration boundaries.

### Scope Detection

**If "YOUR ASSIGNED SCOPE:" and "DO NOT EXPLORE:" sections are present:**
- **STAY WITHIN** your assigned scope - go deep on those specific areas
- **RESPECT EXCLUSIONS** - other processes handle the excluded areas
- If you naturally discover excluded topics while searching, note them as "Out of scope: {discovery}" in research file but don't pursue
- This prevents duplicate work across parallel explorations

**If no scope boundaries**: Explore the full topic as presented.

**Boundary check before each search**: Ask "Is this within my assigned scope?" If a search would primarily return files in excluded areas, skip it.

### Out-of-Scope Discoveries

When you find something relevant but outside your scope:
```markdown
### Out-of-scope discoveries
- {file or area}: {why it seemed relevant} → covered by {which excluded area}
```

These get reported back so the orchestrating skill can verify coverage.

---

# Explore Codebase

Find all files relevant to a specific query so the main context masters that topic without another search.

**Loop**: Determine thoroughness → Search → Expand todos → Write findings → Repeat (depth varies by level) → Compress output

**Research file**: `/tmp/explore-{topic-kebab-case}-{YYYYMMDD-HHMMSS}.md` (if /tmp write fails for any reason—permission denied, disk full, or missing—use current working directory instead. If file already exists, append `-2`, `-3`, etc. to filename before extension.)
(Use ISO-like format: year-month-day-hour-minute-second, e.g., `20260110-143052`. Obtain timestamp via `date +%Y%m%d-%H%M%S` in Bash.)

## Purpose

Limited context window means exploration tokens are spent now so subsequent work can go directly to relevant files without filling context with search noise.

1. Search exhaustively (uses tokens on exploration)
2. Return overview + **complete** file list with line ranges
3. Subsequent work reads only those files → context stays focused
4. Analysis/problem-solving happens after exploration

**Scope**: Only files relevant to the query. NOT a general codebase tour.

**Relevance criteria**: A file is relevant if: (1) it contains logic that implements the queried topic, (2) it directly calls or is called by topic code, (3) it defines types/config used by topic code, or (4) it tests topic behavior. Files that only log, monitor, or incidentally mention the topic are not relevant unless the query specifically asks about logging/monitoring.

**Metaphor**: Librarian preparing complete reading list. After reading, patron passes any test without returning.

**Success test**: After reading the files, answer ANY question, make decisions, understand edge cases, know constraints—**no second search needed**. If another search would be needed, a file was missed.

## Phase 1: Initial Scoping

### 1.0 Determine Thoroughness
State: `**Thoroughness**: [level] — [reason]`. **Quick mode**: skip research file and todo list; proceed directly to 1-2 search calls, then return results immediately.

### 1.1 Create todo list (skip for quick)
Todos = areas to explore + write-to-log operations. Start small, expand as discoveries reveal new areas.

**Area**: A logical grouping of related code (e.g., "JWT handling", "database queries", "error responses"). One area = one todo, followed by a write-to-file todo.

**Starter todos** (expand during exploration):
```
- [ ] Create research file
- [ ] Core {topic} implementation
- [ ] Write core findings to research file
- [ ] {topic} dependencies / callers
- [ ] Write dependency findings to research file
- [ ] (expand as discoveries reveal new areas)
- [ ] (expand: write-to-file after each new area)
- [ ] Refresh context: read full research file
- [ ] Compile output
```

**Critical todos** (never skip):
- `Write {X} findings to research file` - after EACH exploration area
- `Refresh context: read full research file` - ALWAYS before compile output

### 1.2 Create research file (skip for quick)

Path: `/tmp/explore-{topic-kebab-case}-{YYYYMMDD-HHMMSS}.md` (use SAME path for ALL updates)

```markdown
# Research: {topic}
Started: {YYYYMMDD-HHMMSS} | Query: {original query}

## Search Log
### {YYYYMMDD-HHMMSS} - Initial scoping
- Searching for: {keywords}
- Areas to explore: {list}

## Findings
(populated incrementally)

## Files Found
(populated incrementally)
```

## Phase 2: Iterative Exploration

**Quick**: Skip — 1-2 search calls, return. **Medium**: core + first-level imports/exports only + up to 3 callers (per Caller prioritization in Definitions). **Thorough**: all imports + all direct callers (no transitive) + tests + config. **Very-thorough**: unbounded transitive exploration up to 100 files.

### Exploration Loop (medium, thorough, very-thorough)
1. Mark todo in_progress → 2. Search → 3. **Write findings to research file** → 4. Expand todos when discoveries reveal new areas → 5. Complete → 6. Repeat

**When to expand todos**: Add a new todo when you discover a distinct area not covered by existing todos (e.g., finding Redis session code while exploring auth → add "Session storage in Redis" todo).

**Empty results**: If a search returns no relevant files: (1) try 2-3 alternative keywords/patterns, (2) if still empty, note in research file and move to next todo, (3) if all searches empty, return overview stating "No files found matching query" with suggested search terms. If the entire codebase appears to have no source files (only config/docs), return overview stating "No source code files found in repository. Found: {list of non-source files}" and suggest verifying repository contents.

**NEVER proceed without writing findings first.**

### Todo Expansion Triggers (medium, thorough, very-thorough)

| Discovery | Add todos for |
|-----------|---------------|
| Function call | Trace callers (medium: up to 3 per Caller prioritization; thorough: all direct; very-thorough: transitive) |
| Import | Trace imported module |
| Interface/type | Find implementations |
| Service | Config, tests, callers |
| Route/handler | Middleware, controller, service chain |
| Error handling | Error types, fallbacks |
| Config reference | Config files, env vars |
| Test file | Note test patterns |

### Research File Update Format

After EACH search step append:
```markdown
### {YYYYMMDD-HHMMSS} - {what explored}
- Searched: {query/pattern}
- Found: {count} relevant files
- Key files: path/file.ext:lines - {purpose}
- New areas: {list}
- Relationships: {imports, calls}
```

### Todo Evolution Example

Query: "Find files related to authentication"

Initial:
```
- [ ] Create research file
- [ ] Core auth implementation
- [ ] Write core findings to research file
- [ ] Auth dependencies / callers
- [ ] Write dependency findings to research file
- [ ] (expand as discoveries reveal new areas)
- [ ] Refresh context: read full research file
- [ ] Compile final output
```

After exploring core auth (discovered JWT, Redis sessions, OAuth):
```
- [x] Create research file
- [x] Core auth implementation → AuthService, middleware/auth.ts
- [x] Write core findings to research file
- [ ] Auth dependencies / callers
- [ ] Write dependency findings to research file
- [ ] JWT token handling
- [ ] Write JWT findings to research file
- [ ] Redis session storage
- [ ] Write Redis findings to research file
- [ ] OAuth providers
- [ ] Write OAuth findings to research file
- [ ] Refresh context: read full research file
- [ ] Compile final output
```

## Phase 3: Compress Output

### 3.1 Final research file update

```markdown
## Exploration Complete
Finished: {YYYYMMDD-HHMMSS} | Files: {count} | Search calls: {count}
## Summary
{1-3 sentences: what areas were explored and key relationships found}
```

### 3.2 Refresh context (MANDATORY)

**CRITICAL**: Complete the "Refresh context: read full research file" todo by reading the FULL research file using the Read tool. This restores ALL findings into context before generating output.

```
- [x] Refresh context: read full research file  ← Must complete BEFORE compile output
- [ ] Compile output
```

**Why this matters**: By this point, findings from earlier exploration areas have degraded due to context rot. The research file contains ALL discoveries. Reading it immediately before output moves everything into recent context where attention is strongest.

### 3.3 Generate structured output (only after 3.2)

```
## OVERVIEW

[Single paragraph, 100-400 words (target 200-300). Under 100 indicates missing information; over 400 indicates non-structural content. If completeness genuinely requires >400 words, include all structural facts but review for prescriptive or redundant content to remove. Describe THE QUERIED TOPIC structure:
which files/modules exist, how they connect, entry points, data flow.
Include specific details (timeouts, expiry, algorithms) found during exploration.
Factual/structural ONLY—NO diagnosis, recommendations, opinions.]

## FILES TO READ

(Only files relevant to the query)

MUST READ:
- path/file.ext:50-120 - [brief reason (<80 chars) why relevant]

SHOULD READ:
- path/related.ext:10-80 - [brief reason (<80 chars)]

REFERENCE:
- path/types.ext - [brief reason (<80 chars)]

## OUT OF SCOPE (if boundaries were provided)
- {file/area}: {why relevant} → excluded because: {which boundary}
```

### 3.4 Mark all todos complete

## Overview Guidelines

Overview describes **the queried topic area only**, not the whole codebase.

**GOOD content** (structural knowledge about the topic):
- File organization: "Auth in `src/auth/`, middleware in `src/middleware/auth.ts`"
- Relationships: "login handler → validateCredentials() → TokenService"
- Entry points: "Routes in `routes/api.ts`, handlers in `handlers/`"
- Data flow: "Request → middleware → handler → service → repository → DB"
- Patterns: "Repository pattern, constructor DI"
- Scope: "12 files touch auth; 5 core (files you'd edit to change auth behavior), 7 peripheral (interact with auth but serve other purposes)"
- Key facts: "Tokens 15min expiry, refresh in Redis 7d TTL"
- Dependencies: "Auth needs Redis (sessions) + Postgres (users)"
- Error handling: "401 for auth failures, 403 for invalid tokens"

**BAD content** (prescriptive—convert to descriptive):
- Diagnosis: "Bug is in validateCredentials() because..."
- Recommendations: "Refactor to use..."
- Opinions: "Poorly structured..."
- Solutions: "Fix by adding null check..."

Overview = **dense map of the topic area**, not diagnosis or codebase tour.

## What You Do NOT Output

- NO diagnosis (describe area, don't identify bugs)
- NO recommendations (don't suggest fixes/patterns)
- NO opinions (don't comment on quality)
- NO solutions (analysis happens after exploration)

## Search Strategy

1. **Extract keywords** from query
2. **Search broadly**: Glob (`**/auth/**`, `**/*payment*`), Grep (functions, classes, errors), common locations (`src/`, `lib/`, `services/`, `api/`)
3. **Follow graph** (ADD TODOS FOR EACH, depth per thoroughness level):
   - Imports/exports, callers (medium: up to 3 per Caller prioritization; thorough: all direct; very-thorough: transitive), callees, implementations, usages
4. **Supporting files** (thorough and very-thorough only):
   - Tests (`*.test.*`, `*.spec.*`, `__tests__/`) — expected behavior
   - Config (`.env*`, `config/`, env vars) — runtime behavior
   - Types (`types/`, `*.d.ts`, interfaces) — contracts
   - Error handling (catch blocks, error types, fallbacks)
   - Utilities (shared helpers)
5. **Non-obvious** (very-thorough only):
   - Middleware/interceptors, event handlers, background jobs, migrations, env-specific code
6. **Verify**: Skim files, note specific line ranges (not entire files)

## Priority Criteria

| Priority | Criteria |
|----------|----------|
| MUST READ | Entry points (where execution starts), core business logic (files you'd edit to change behavior), primary implementation of queried topic |
| SHOULD READ | Direct callers/callees, error handling for the topic, related modules in same domain, test files (thorough+ only), config affecting the topic (thorough+ only) |
| REFERENCE | Type definitions, utility functions used by core, boilerplate/scaffolding, files that mention topic but aren't central to it |

**Level overrides priority**: Thoroughness level determines which file categories to include. Priority criteria categorizes files within those categories. At medium level, skip SHOULD READ items marked as "thorough+ only" (tests, config, all callers).

**Priority order: Level restrictions > Completeness > Brevity**. Include all files matching the thoroughness level's scope. Level restrictions (e.g., no tests at medium) are hard limits. Within those limits, prefer completeness over brevity. Include files that interact with the topic in actual code logic. Exclude files where the topic keyword appears only in comments, log strings, or variable names without logic.

## Key Principles

| Principle | Rule |
|-----------|------|
| Scope-adherent | Stay within assigned scope; note out-of-scope discoveries without pursuing |
| Todos with write-to-log | Each exploration area gets a write-to-research-file todo |
| Write before proceed | Write findings BEFORE next search (research file = external memory) |
| Todo-driven | Every new area discovered → new todo + write-to-file todo (no mental notes) |
| Depth by level | Stop at level-appropriate depth (medium: first-level deps + up to 3 callers; thorough: all direct callers+tests+config; very-thorough: transitive, up to 100 files) |
| Incremental | Update research file after EACH exploration area (not at end) |
| **Context refresh** | **Read full research file BEFORE compile output - non-negotiable** |
| Compress last | Output only after all todos completed including refresh |

**Log Pattern Summary**:
1. Create research file at start
2. Add write-to-file todos after each exploration area
3. Write findings after EVERY area before moving to next
4. "Refresh context: read full research file" todo before compile
5. Read FULL file before generating output (restores all context)

## Never Do

- Explore areas in "DO NOT EXPLORE" section (other processes handle those)
- Skip write-to-file todos (every area completion must be written)
- Compile output without completing "Refresh context" todo first
- Keep discoveries as mental notes instead of todos
- Skip todo list (except quick mode)
- Generate output before all todos completed
- Forget to add write-to-file todo for newly discovered areas

## Final Checklist

- [ ] Scope boundaries respected (if provided)
- [ ] Out-of-scope discoveries noted (if any)
- [ ] Write-to-file todos completed after each exploration area
- [ ] "Refresh context: read full research file" completed before output
- [ ] All todos completed (no pending items)
- [ ] Research file complete (incremental findings after each step)
- [ ] Depth appropriate (medium stops at first-level deps + 3 callers; thorough includes all direct callers+tests+config; very-thorough transitive up to 100 files)
- [ ] Coverage matches level (configs, utilities, error handlers, tests for thorough+)
- [ ] Overview is 100-400 words (target 200-300), structural only, no opinions
- [ ] File list has precise line ranges, prioritized, brief reasons (<80 chars)

**Key question**: After MUST READ + SHOULD READ, will all questions about this topic be answerable?

## Example 1: Payment Timeout Bug

Query: "Find files related to the payment timeout bug"

```
## OVERVIEW

Payment: 3 layers. `PaymentController` (routes/payments.ts:20-80) HTTP, `PaymentService` (services/payment.ts) logic, `PaymentClient` (clients/stripe.ts) external calls. Timeout 30s default in config/payments.ts. Retry logic services/payment.ts:150-200 catches timeouts, retries 3x. Tests: happy path covered, timeout scenarios only tests/payment.test.ts:200-280.

## FILES TO READ

MUST READ:
- src/services/payment.ts:89-200 - Core processing, timeout/retry logic
- src/clients/stripe.ts:50-95 - External API calls where timeouts occur

SHOULD READ:
- src/config/payments.ts:1-30 - Timeout configuration
- tests/payments/payment.test.ts:200-280 - Timeout test cases

REFERENCE:
- src/routes/payments.ts:20-80 - HTTP layer
- src/types/payment.ts - Type definitions
```

**Bad**: "Timeout bug caused by retry logic not respecting total budget. Recommend circuit breaker." — NO. Describe structurally, don't diagnose.

## Example 2: Authentication

Query: "Find files related to authentication"

```
## OVERVIEW

JWT (RS256) in httpOnly cookies. 15min expiry, refresh tokens Redis 7d TTL. Flow: POST /login (routes/auth.ts:15-40) → AuthController.login() → AuthService.authenticate() → UserRepository.findByEmail(). Bcrypt cost 12. Middleware middleware/auth.ts validates JWT, attaches user. Refresh: AuthService.refreshToken() issues new token if refresh valid. Logout: clears cookie, blacklists token in Redis (checked every request). Rate limit: 5/15min/IP. Failed logins → audit_logs. OAuth (Google, GitHub) in services/oauth.ts.

## FILES TO READ

MUST READ:
- src/services/auth.ts:1-150 - Core auth (authenticate, refresh, logout, tokens)
- src/middleware/auth.ts:15-85 - JWT validation, user context, blacklist check
- src/services/tokenBlacklist.ts:1-60 - Redis token invalidation

SHOULD READ:
- src/routes/auth.ts:15-100 - Routes, validation, rate limiting
- src/repositories/user.ts:30-80 - User lookup, password verify
- src/services/oauth.ts:1-120 - OAuth providers
- src/utils/crypto.ts:10-45 - Hashing, signing utilities
- tests/auth/auth.test.ts:1-250 - Expected behaviors
- tests/auth/auth.integration.ts:1-150 - Redis/DB integration

REFERENCE:
- src/types/auth.ts - Types/interfaces
- src/config/auth.ts - JWT secret, expiry, bcrypt rounds, rate limits
- src/middleware/rateLimit.ts:20-50 - Rate limiting impl
- prisma/schema.prisma:45-70 - User model, audit_logs
```

Comprehensive coverage — after reading, understand auth completely.

## Example 3: ORM Usage

Query: "Find all files that use the ORM"

```
## OVERVIEW

Prisma ORM. Schema prisma/schema.prisma: 8 models (User, Order, Product, Category, Review, Cart, CartItem, Address). Client singleton src/db/client.ts, imported everywhere. Repository pattern: src/repositories/{model}.repository.ts. Services use repositories, never Prisma directly. 12 migrations in prisma/migrations/. Raw queries: repositories/report.repository.ts:50-80 (analytics), repositories/search.repository.ts:30-60 (full-text search).

## FILES TO READ

MUST READ:
- prisma/schema.prisma - Model definitions
- src/db/client.ts:1-30 - Prisma singleton
- src/repositories/user.repository.ts:1-120 - Repository pattern example

SHOULD READ:
- src/repositories/order.repository.ts:1-150 - Complex relations
- src/repositories/report.repository.ts:50-80 - Raw SQL
- src/services/user.service.ts:30-100 - Service→repository usage

REFERENCE:
- prisma/migrations/ - 12 migration files
- src/types/db.ts - Generated types
```

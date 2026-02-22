---
name: review
description: Review code quality for a completed feature or entire project — comprehensive multi-dimension review covering correctness, security, resource management, performance, architecture, testing, observability, and more.
---

# Code Forge — Review

Comprehensive code review against reference documents and engineering best practices. Covers functional correctness, security, resource management, code quality, architecture, performance, testing, error handling, observability, maintainability, backward compatibility, and dependency safety.

Supports two modes:
- **Feature mode:** Review a single feature against its `plan.md`
- **Project mode:** Review the entire project against planning documents or upstream docs

## When to Use

- Feature implementation is complete or nearly complete
- Want to verify code quality before creating a PR
- Need a structured review against the original plan or documentation
- Want a holistic project-level quality check

## Workflow

```
Config → Determine Mode → Locate Reference → Collect Scope → Multi-Dimension Review (sub-agent) → Display Report → Update State → Summary
```

## Context Management

The review analysis is offloaded to a sub-agent to handle large diffs without exhausting the main context.

## Review Severity Levels

All issues use a 4-tier severity system, ordered by merge-blocking priority:

| Severity     | Symbol | Meaning                                               | Merge Policy            |
|--------------|--------|-------------------------------------------------------|-------------------------|
| `blocker`    | :no_entry:     | Production risk. Data loss, security breach, crash.   | **Must fix before merge** |
| `critical`   | :warning:     | Significant quality/correctness concern.              | **Must fix before merge** |
| `warning`    | :large_orange_diamond:     | Recommended fix. Could cause issues over time.        | Should fix              |
| `suggestion` | :blue_book:     | Nice-to-have improvement. Can address later.          | Nice-to-have            |

## Review Dimensions Reference

The following dimensions are used in both Feature Mode and Project Mode reviews. They are ordered by priority tier.

### Tier 1 — Must-Fix Before Merge (★★★★★)

#### D1: Functional Correctness & Business Logic

Does the code actually implement what it should? This is the highest-priority dimension.

Check items:
- **Requirements fulfillment:** Does the code implement the specified behavior correctly?
- **Boundary conditions:** Off-by-one errors, empty collections, zero/negative values, max values, null/undefined
- **Concurrency & race conditions:** Shared mutable state, missing locks/synchronization, TOCTOU bugs
- **Idempotency:** Are operations safe to retry? Are duplicate requests handled?
- **State transitions:** Are all states reachable? Are invalid transitions prevented?
- **Data consistency:** Transactions boundaries, partial failure handling, eventual consistency gaps
- **Type correctness:** Type coercion surprises, implicit conversions, generic type safety
- **Edge cases in business rules:** Negative amounts, timezone handling, leap years, Unicode, locale-specific logic

#### D2: Security Vulnerabilities

Does the code introduce any security risk?

Check items:
- **Injection:** SQL injection (string concatenation), command injection, LDAP injection, template injection
- **XSS:** Reflected, stored, DOM-based — unescaped user content in HTML/JS
- **Authentication & authorization:** Missing auth checks, privilege escalation, insecure session management
- **Secrets management:** Hardcoded credentials, API keys in code, secrets in logs, `.env` committed
- **CSRF / SSRF:** Missing tokens, unvalidated redirect URLs, internal network access
- **Deserialization:** Unsafe deserialization of untrusted data (pickle, Java serialization, JSON.parse with eval)
- **Cryptography:** Weak algorithms (MD5/SHA1 for passwords), ECB mode, predictable random, custom crypto
- **Path traversal:** Unsanitized file paths from user input
- **Log forging / information disclosure:** Sensitive data in logs, verbose error messages to users
- **Dependency vulnerabilities:** Known CVEs in direct or transitive dependencies

#### D3: Resource Management & Lifecycle

Are all acquired resources properly released? This is especially critical for long-running services.

Check items:
- **Event listeners:** `addEventListener` without `removeEventListener` on cleanup
- **Timers:** `setInterval`/`setTimeout` without `clearInterval`/`clearTimeout`
- **Subscriptions:** Observables, pub/sub, WebSocket connections not unsubscribed on teardown
- **File handles / DB connections:** Opened but not closed, missing `finally`/`defer`/`using`/`with`
- **Goroutine / thread / fiber leaks:** Spawned without termination condition or cancellation
- **Memory:** Unbounded caches/maps, closures capturing large scopes, circular references preventing GC
- **Stream / iterator:** Not consumed or not closed, backpressure not handled
- **Framework lifecycle:** React `useEffect` cleanup, Angular `OnDestroy`, Vue `onUnmounted`, iOS `deinit`

### Tier 2 — Should-Fix (★★★★☆)

#### D4: Code Quality & Readability

Is the code clear, maintainable, and following project conventions?

Check items:
- **Naming:** Variables, functions, classes use descriptive, intention-revealing names; no `temp`, `data`, `process()`
- **Magic values:** No unexplained literals — use named constants
- **Function length:** Functions > 50 lines should be scrutinized; > 100 lines likely needs splitting
- **DRY:** No copy-pasted logic blocks; shared behavior extracted appropriately
- **Dead code:** No unused functions, unreachable branches, commented-out code, unused imports
- **Comments:** Present only where logic isn't self-evident; no stale/misleading comments
- **Code structure:** Appropriate abstractions, no unnecessary complexity or premature optimization
- **Consistent style:** Follows project's existing patterns for formatting, file organization, module structure

#### D5: Architecture & Design

Does the change fit the project's architectural conventions?

Check items:
- **Layer boundaries:** Respects existing architectural layers (controller/service/repo, MVC, hexagonal, etc.)
- **Dependency direction:** No circular dependencies, lower layers don't depend on higher layers
- **SOLID principles:** Single responsibility, open-closed, interface segregation violations
- **Coupling:** New code not tightly coupled to implementation details of other modules
- **Abstraction level:** Not introducing a parallel system alongside an existing one
- **API surface:** Public interfaces are clean, minimal, consistent, and well-defined
- **Module cohesion:** Related functionality grouped together; no God Class / God Function
- **New abstractions justified:** If new patterns/frameworks/base classes are introduced, are they warranted?

#### D6: Performance & Efficiency

Are there obvious performance problems on hot paths?

Check items:
- **N+1 queries:** Database queries inside loops
- **Missing indexes:** Frequent queries on unindexed columns
- **Unnecessary allocations:** Creating objects inside tight loops, large object copies on hot paths
- **Blocking in async context:** Synchronous I/O in async code, `await` in loops when `Promise.all` is appropriate
- **Lock granularity:** Oversized critical sections, lock contention on hot paths
- **Cache misuse:** Cache stampede / thundering herd, unbounded cache growth, no TTL
- **Algorithmic complexity:** O(n²) or worse where O(n log n) or O(n) is feasible
- **Payload size:** Fetching all columns when only a few needed, unbounded result sets, no pagination
- **Frontend:** Unnecessary re-renders, missing memoization, layout thrashing, large bundle imports

#### D7: Test Coverage & Verifiability

Are critical paths tested? Are tests meaningful?

Check items:
- **Coverage of critical paths:** Core business logic, state transitions, and data transformations have tests
- **Happy path:** Normal/expected flow is tested
- **Sad path:** Error conditions, invalid inputs, failure scenarios are tested
- **Edge cases:** Boundary values, empty inputs, concurrent access, large inputs
- **Test independence:** Tests don't depend on execution order or shared mutable state
- **Determinism:** No flaky tests relying on timing, network, or random data without seeding
- **Meaningful assertions:** Tests assert behavior, not implementation; not just "no error thrown"
- **Test naming:** Test names describe the scenario and expected behavior
- **Mock appropriateness:** External dependencies mocked; internal logic not over-mocked
- **Missing test files:** Source modules without any corresponding test coverage

### Tier 3 — Recommended Fix (★★★☆☆)

#### D8: Error Handling & Robustness

Are errors properly caught, classified, reported, and recovered from?

Check items:
- **Swallowed exceptions:** Catch blocks that silently ignore errors (empty catch, catch-and-log-only for critical ops)
- **Over-broad catch:** Catching `Exception` / `Error` / `object` instead of specific types
- **Error propagation:** Errors from downstream services/APIs properly surfaced or wrapped
- **User-facing errors:** Error messages are user-friendly, no stack traces or internal details leaked
- **Timeout handling:** Network calls, DB queries, external APIs have timeouts configured
- **Retry logic:** Retries have backoff, jitter, and max-retry limits; not infinite retry loops
- **Fallback / degradation:** Critical paths have fallback behavior when dependencies fail
- **Promise / async errors:** Unhandled promise rejections, missing `.catch()`, missing error boundaries (React)

#### D9: Observability (Logging / Metrics / Tracing)

Can you debug and monitor this code in production?

Check items:
- **Structured logging:** Key business operations emit structured logs with context (user ID, request ID, operation)
- **Log levels:** Appropriate use of debug/info/warn/error levels
- **Error logging:** Exceptions logged with stack traces and context; not swallowed silently
- **Sensitive data in logs:** No passwords, tokens, PII, or credit card numbers in log output
- **Request tracing:** Trace ID / correlation ID propagated across service boundaries
- **Business metrics:** Key business events have counters/gauges (orders placed, payments processed, errors)
- **Health/readiness signals:** Service exposes health checks if applicable
- **Alertability:** Can an on-call engineer understand and act on the logs/metrics this code produces?

#### D10: Standards & Conventions

Does the code follow team and project conventions?

Check items:
- **Lint compliance:** Code passes project linter configuration
- **File/directory structure:** Follows project's established organization patterns
- **Import ordering:** Follows project convention for import grouping/ordering
- **Dependency management:** New dependencies declared properly, version pinned, justified
- **Naming conventions:** Files, classes, functions follow project naming patterns (camelCase, snake_case, etc.)
- **Configuration:** New config via environment variables or config files, not hardcoded
- **No surprise technology:** New frameworks, libraries, or patterns introduced without team discussion

### Tier 4 — Nice-to-Have / Track as Tech Debt (★★☆☆☆ / ★☆☆☆☆)

#### D11: Backward Compatibility & Ops-Friendliness

Will this change break existing consumers or complicate deployment?

Check items:
- **API contract:** Existing API fields/endpoints not removed or semantically changed without versioning
- **Database schema:** Column renames, type changes, or drops have migration + backward-compat strategy
- **Configuration changes:** New required config keys have defaults or migration docs
- **Cache/queue keys:** Key format changes won't corrupt existing cached data
- **Enum/constant changes:** Value semantics preserved; new values don't break existing consumers
- **Rollback safety:** Can this change be rolled back without data loss or corruption?
- **Feature flags / gradual rollout:** High-risk changes gated behind feature flags

#### D12: Maintainability & Tech Debt

Does this change leave the codebase better or worse?

Check items:
- **Copy-paste debt:** Large duplicated blocks that should be extracted
- **Deep inheritance:** Inheritance depth > 3 levels; prefer composition
- **Magic configuration:** Behavior controlled by non-obvious environment variables or config
- **Over-engineering:** Abstractions, extension points, or patterns for hypothetical future needs
- **Under-engineering:** Quick hacks that will clearly need rework soon (TODO/FIXME/HACK comments)
- **Coupling to internals:** Depending on internal implementation details of libraries or other modules

#### D13: Dependencies & Supply Chain Security

Are new or updated dependencies safe and justified?

Check items:
- **Known CVEs:** Dependencies scanned for known vulnerabilities
- **Version pinning:** Versions locked (lockfile present and updated); not using `latest` or `*`
- **Minimal footprint:** Not pulling in a large library for a small utility
- **Maintenance status:** Dependency actively maintained, not abandoned/archived
- **License compatibility:** License compatible with project requirements
- **Transitive risk:** Major transitive dependencies checked for known issues

#### D14: Accessibility / i18n (Frontend & Mobile Only)

Is the UI usable by all users? _(Skip this dimension for backend-only projects.)_

Check items:
- **Semantic HTML:** Proper use of heading levels, landmarks, form labels
- **ARIA attributes:** Interactive elements have appropriate `aria-label`, `role`, states
- **Keyboard navigation:** All interactive elements reachable and operable via keyboard
- **Color contrast:** Text meets WCAG AA contrast ratio (4.5:1 for normal text)
- **Hardcoded strings:** User-visible text uses i18n/l10n framework, not hardcoded
- **RTL support:** Layout not broken in right-to-left languages (if applicable)
- **Screen reader:** Dynamic content changes announced; focus management correct

---

## Detailed Steps

@../shared/configuration.md

---

### Step 1: Determine Review Mode

Parse the user's arguments to determine which mode to use.

#### 1.1 Feature Name Provided

If the user provided a feature name (e.g., `/code-forge:review user-auth`):

→ **Feature Mode** — go to Step 2F

#### 1.2 `--project` Flag Provided

If the user passed `--project` (e.g., `/code-forge:review --project`):

→ **Project Mode** — go to Step 2P

#### 1.3 No Arguments

If no arguments provided:

1. Scan `{output_dir}/*/state.json` for all features
2. Filter to features with at least one `"completed"` task
3. Build choice list:
   - If completed features exist: include each as an option, **plus** "Review entire project" as the last option
   - If no completed features: go to **Project Mode** automatically
4. If only one option (project review): go to **Project Mode** automatically
5. If multiple options: use `AskUserQuestion` to let user select

---

### Step 2F: Feature Mode — Locate Feature

#### 2F.1 Find Feature

1. Look for `{output_dir}/{feature_name}/state.json`
2. If not found: show error, list available features

#### 2F.2 Load Feature Context

1. Read `state.json`
2. Read `plan.md` (for acceptance criteria and architecture)
3. Note completed task count and overall progress

→ Go to Step 3F

---

### Step 2P: Project Mode — Locate Reference

Determine the reference level using a fallback chain.

#### 2P.1 Check for Planning Documents (Level 1: Planning-backed)

Scan `{output_dir}/*/plan.md`:

- If one or more `plan.md` files found → **planning-backed**
- Read all `plan.md` files and aggregate:
  - Acceptance criteria from each feature
  - Architecture decisions
  - Technology stack
- Read corresponding `state.json` files for progress context
- Record: `reference_level = "planning"`
- Record: list of plan file paths and aggregated criteria
- → Go to Step 3P

#### 2P.2 Check for Documentation (Level 2: Docs-backed)

If no planning documents found, scan for upstream documentation:

Search paths (in order):
1. `{input_dir}/*.md` — feature specs
2. `docs/` directory — PRD, SRS, tech-design, test-plan files

Look for files matching patterns:
- `**/prd.md`, `**/srs.md`, `**/tech-design.md`, `**/test-plan.md`
- `**/features/*.md`
- Any `.md` files directly under `docs/`

If documentation files found → **docs-backed**:
- Read all found docs
- Extract: requirements, architecture decisions, acceptance criteria, scope definitions
- Record: `reference_level = "docs"`
- Record: list of doc file paths and extracted criteria
- → Go to Step 3P

#### 2P.3 No Reference (Level 3: Bare)

If neither planning nor docs found → **bare**:
- Record: `reference_level = "bare"`
- → Go to Step 3P

---

### Step 3F: Feature Mode — Collect Changes and Review

#### 3F.1 Collect Change Scope

**From Commits:**
Extract all commit hashes from `state.json` → `tasks[].commits`:
- Flatten all commit arrays into a single list
- If commits are recorded, use `git diff` between the earliest and latest commits
- If no commits recorded, fall back to scanning files involved in tasks

**From Task Files:**
Read all `tasks/*.md` files and collect their "Files Involved" sections:
- Build a complete list of files created/modified by this feature
- Read current state of each file

**Summary:**
- Total files changed
- Total lines added/removed (from git diff)
- List of all affected files

#### 3F.2 Detect Project Type

Before launching the sub-agent, detect the project type to guide dimension selection:

1. **Has frontend?** Check for: `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, HTML templates, CSS/SCSS files, or frontend framework config (`next.config.*`, `vite.config.*`, `angular.json`)
2. **Has backend/service?** Check for: server entry points, API route definitions, database models, middleware
3. **Language ecosystem:** Detect primary language(s) from file extensions and package manifests

Record: `project_type` = `"frontend"` | `"backend"` | `"fullstack"` | `"library"` | `"cli"` | `"unknown"`

#### 3F.3 Multi-Dimension Review (via Sub-agent)

**Offload to sub-agent** to handle the full diff analysis.

Spawn a `Task` tool call with:
- `subagent_type`: `"general-purpose"`
- `description`: `"Review feature: {feature_name}"`

**Sub-agent prompt must include:**
- Feature name and `plan.md` file path
- List of all affected files (sub-agent reads them)
- The acceptance criteria from `plan.md`
- Detected project type
- Instructions to review across all applicable dimensions below
- The severity level definitions (blocker / critical / warning / suggestion)
- Instruction: **"For each issue, specify severity, file path, line number/range, what's wrong, and how to fix it. Use the Review Comment Formula: Problem → Why it matters → Suggested fix."**

**Review dimensions to apply:**

Apply all dimensions from the [Review Dimensions Reference](#review-dimensions-reference) above, with these rules:
- **D1–D3 (Tier 1):** Always apply. These are potential merge blockers.
- **D4–D7 (Tier 2):** Always apply. These are should-fix items.
- **D8–D10 (Tier 3):** Always apply. Flag as warnings/suggestions.
- **D11–D13 (Tier 4):** Always apply but expect mostly suggestions.
- **D14 (Accessibility/i18n):** Apply ONLY if `project_type` is `"frontend"` or `"fullstack"`.

Additionally, always check **Plan Consistency** (feature mode specific):
- All acceptance criteria from `plan.md` are met
- Architecture matches the design in `plan.md`
- No unplanned features added (scope creep)
- All planned tasks are implemented

**Sub-agent must return the following structured format:**

```
REVIEW_SUMMARY:
  overall_rating: <pass | pass_with_notes | needs_changes>
  total_issues: <number>
  blocker_count: <number>
  critical_count: <number>
  warning_count: <number>
  suggestion_count: <number>
  merge_readiness: <ready | fix_required | rework_required>
  dimensions_reviewed: <list of dimension IDs reviewed>

FUNCTIONAL_CORRECTNESS:                              # D1
  rating: <pass | warning | critical>
  issues:
  - severity: <blocker | critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

SECURITY:                                            # D2
  rating: <pass | warning | critical>
  issues:
  - severity: <blocker | critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

RESOURCE_MANAGEMENT:                                 # D3
  rating: <pass | warning | critical>
  issues:
  - severity: <blocker | critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

CODE_QUALITY:                                        # D4
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

ARCHITECTURE:                                        # D5
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

PERFORMANCE:                                         # D6
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

TEST_COVERAGE:                                       # D7
  rating: <good | acceptable | needs_work>
  coverage_gaps:
  - severity: <critical | warning | suggestion>
    file: path/to/source.ext
    description: <what scenario is untested>

ERROR_HANDLING_AND_OBSERVABILITY:                     # D8 + D9
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    category: <error_handling | logging | metrics | tracing>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

MAINTAINABILITY_AND_COMPATIBILITY:                    # D10 + D11 + D12 + D13
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    category: <standards | backward_compat | tech_debt | dependencies>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

ACCESSIBILITY:                                       # D14 (frontend/fullstack only)
  rating: <good | acceptable | needs_work | skipped>
  issues:
  - severity: <warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

PLAN_CONSISTENCY:
  criteria_met: <X/Y>
  unmet_criteria:
  - <criterion not met>
  scope_issues:
  - <unplanned additions or missing planned features>
```

→ Go to Step 4F

---

### Step 3P: Project Mode — Collect Source Code and Review

**The primary subject of review is the source code itself.** Reference documents (plans, specs) serve only as criteria to check against — the sub-agent must deeply read and analyze the actual implementation.

#### 3P.1 Collect Source Code

Identify and collect project source files for deep code review:

1. Use project root markers to find source directories (e.g., `src/`, `lib/`, `app/`, `pkg/`, or language-specific patterns)
2. Exclude non-source directories: `node_modules/`, `dist/`, `build/`, `.git/`, `vendor/`, `__pycache__/`, the output directory itself
3. If on a non-main branch, prefer `git diff main...HEAD` to scope changed files
4. If on main branch, scan all source files

Build file list for the sub-agent. If the project is large (>50 source files), focus on:
- Files changed recently (git log)
- Core modules (entry points, main logic, business logic)
- Test files
- Configuration and infrastructure files

Also collect:
- Package manifests (`package.json`, `Cargo.toml`, `pyproject.toml`, etc.) for dependency review
- Build/CI configuration if present

#### 3P.2 Detect Project Type

Same as Step 3F.2 — detect `project_type` to guide dimension selection.

#### 3P.3 Multi-Dimension Code Review (via Sub-agent)

**Offload to sub-agent** to handle deep source code analysis.

Spawn a `Task` tool call with:
- `subagent_type`: `"general-purpose"`
- `description`: `"Project code review: {project_name}"`

**Sub-agent prompt must include:**
- Project name and root path
- **List of all source files to review — sub-agent MUST read and analyze each file's actual implementation**
- Reference level (`planning` / `docs` / `bare`) and associated criteria (if any)
- Detected project type
- If planning-backed: aggregated acceptance criteria (as checklist for consistency dimension only)
- If docs-backed: extracted requirements (as checklist for consistency dimension only)
- The severity level definitions (blocker / critical / warning / suggestion)
- Explicit instruction: **"Read every source file. Review the code itself — its logic, structure, correctness, and quality. Reference documents are only used as criteria for the consistency check, not as the subject of review."**
- Instruction: **"For each issue, specify severity, file path, line number/range, what's wrong, and how to fix it. Use the Review Comment Formula: Problem → Why it matters → Suggested fix."**

**Review dimensions to apply:**

Apply all dimensions from the [Review Dimensions Reference](#review-dimensions-reference) above, with these rules:
- **D1–D3 (Tier 1):** Always apply. These are potential merge blockers.
- **D4–D7 (Tier 2):** Always apply. These are should-fix items.
- **D8–D10 (Tier 3):** Always apply. Flag as warnings/suggestions.
- **D11–D13 (Tier 4):** Always apply but expect mostly suggestions.
- **D14 (Accessibility/i18n):** Apply ONLY if `project_type` is `"frontend"` or `"fullstack"`.

Additionally, apply the appropriate **Consistency** check based on reference level:

- **planning-backed** → **Plan Consistency:**
  - Aggregated acceptance criteria from all plans are met in the code
  - Implemented architecture matches the designs in plan files
  - No unplanned features added (scope creep)
  - All planned features have corresponding code

- **docs-backed** → **Documentation Consistency:**
  - Code implements the requirements described in documentation
  - Architecture aligns with tech design (if present)
  - Feature scope in code matches what specs describe
  - No undocumented major functionality in the code

- **bare** → **Skip this dimension.** Note in the report: "No reference documents found — consistency check skipped."

**Sub-agent must return the following structured format:**

All issues MUST reference specific source files and line numbers/ranges.

```
REVIEW_SUMMARY:
  overall_rating: <pass | pass_with_notes | needs_changes>
  total_issues: <number>
  blocker_count: <number>
  critical_count: <number>
  warning_count: <number>
  suggestion_count: <number>
  merge_readiness: <ready | fix_required | rework_required>
  reference_level: <planning | docs | bare>
  dimensions_reviewed: <list of dimension IDs reviewed>

FUNCTIONAL_CORRECTNESS:                              # D1
  rating: <pass | warning | critical>
  issues:
  - severity: <blocker | critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

SECURITY:                                            # D2
  rating: <pass | warning | critical>
  issues:
  - severity: <blocker | critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

RESOURCE_MANAGEMENT:                                 # D3
  rating: <pass | warning | critical>
  issues:
  - severity: <blocker | critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

CODE_QUALITY:                                        # D4
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

ARCHITECTURE:                                        # D5
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

PERFORMANCE:                                         # D6
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <critical | warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

TEST_COVERAGE:                                       # D7
  rating: <good | acceptable | needs_work>
  coverage_gaps:
  - severity: <critical | warning | suggestion>
    file: path/to/source.ext
    description: <what scenario is untested>

ERROR_HANDLING_AND_OBSERVABILITY:                     # D8 + D9
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    category: <error_handling | logging | metrics | tracing>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

MAINTAINABILITY_AND_COMPATIBILITY:                    # D10 + D11 + D12 + D13
  rating: <good | acceptable | needs_work>
  issues:
  - severity: <warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    category: <standards | backward_compat | tech_debt | dependencies>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

ACCESSIBILITY:                                       # D14 (frontend/fullstack only)
  rating: <good | acceptable | needs_work | skipped>
  issues:
  - severity: <warning | suggestion>
    file: path/to/file.ext
    line: <number or range>
    title: <short title>
    description: <what's wrong and why it matters>
    suggestion: <how to fix>

CONSISTENCY:
  type: <plan_consistency | doc_consistency | skipped>
  rating: <good | acceptable | needs_work | N/A>
  criteria_met: <X/Y> (if applicable)
  unmet_criteria:
  - <criterion not met>
  scope_issues:
  - <unplanned additions or missing documented features>
```

→ Go to Step 4P

---

### Step 4F: Feature Mode — Display Report

Review results are **displayed in the terminal** by default — no file is written. This reflects that reviews are iterative, intermediate checks rather than permanent artifacts.

Display the following report directly in the terminal using markdown:

```markdown
# Code Review: {feature_name}

**Date:** {ISO date}
**Reviewer:** code-forge
**Overall Rating:** {pass | pass_with_notes | needs_changes}
**Merge Readiness:** {ready | fix_required | rework_required}

## Summary

{1-2 paragraph summary of the review findings}

**Issue Breakdown:** {blocker_count} blockers · {critical_count} critical · {warning_count} warnings · {suggestion_count} suggestions

---

## Tier 1 — Must-Fix Before Merge

### Functional Correctness (D1)

**Rating:** {rating}

{issues table with severity/file/line/title/description/suggestion, or "No issues found"}

### Security (D2)

**Rating:** {rating}

{issues or "No security concerns"}

### Resource Management (D3)

**Rating:** {rating}

{issues or "No resource management issues"}

---

## Tier 2 — Should-Fix

### Code Quality (D4)

**Rating:** {rating}

{issues or "No issues found"}

### Architecture & Design (D5)

**Rating:** {rating}

{issues or "No issues found"}

### Performance (D6)

**Rating:** {rating}

{issues or "No issues found"}

### Test Coverage (D7)

**Rating:** {rating}

{coverage gaps or "All scenarios covered"}

---

## Tier 3 — Recommended

### Error Handling & Observability (D8/D9)

**Rating:** {rating}

{issues or "No issues found"}

---

## Tier 4 — Nice-to-Have

### Maintainability & Compatibility (D10–D13)

**Rating:** {rating}

{issues or "No issues found"}

{If frontend/fullstack:}
### Accessibility / i18n (D14)

**Rating:** {rating}

{issues or "Skipped (not a frontend project)"}

---

## Plan Consistency

**Criteria Met:** {X/Y}

{unmet criteria or "All criteria met"}

---

## Recommendations

{Prioritized list of changes, grouped by blocking status:}

**Must fix before merge:**
1. {highest priority fix with file:line reference}
2. ...

**Should fix:**
1. {recommended fix}
2. ...

**Consider for later:**
1. {nice-to-have improvement}
2. ...

## Verdict

{Final assessment: merge as-is, fix blockers/criticals then merge, or needs rework}
```

#### 4F.1 Optional: Save to File (`--save`)

If the user passed `--save` in the arguments, **also** write the report to `{output_dir}/{feature_name}/review.md`. Otherwise, do NOT create the file.

→ Go to Step 5F

---

### Step 4P: Project Mode — Display Report

Display the following report directly in the terminal using markdown:

```markdown
# Project Review: {project_name}

**Date:** {ISO date}
**Reviewer:** code-forge
**Reference:** {planning-backed | docs-backed | bare (no reference documents)}
**Overall Rating:** {pass | pass_with_notes | needs_changes}
**Merge Readiness:** {ready | fix_required | rework_required}

## Summary

{1-2 paragraph summary of overall project quality}

**Issue Breakdown:** {blocker_count} blockers · {critical_count} critical · {warning_count} warnings · {suggestion_count} suggestions

---

## Tier 1 — Must-Fix Before Merge

### Functional Correctness (D1)

**Rating:** {rating}

{issues or "No issues found"}

### Security (D2)

**Rating:** {rating}

{issues or "No security concerns"}

### Resource Management (D3)

**Rating:** {rating}

{issues or "No resource management issues"}

---

## Tier 2 — Should-Fix

### Code Quality (D4)

**Rating:** {rating}

{issues or "No issues found"}

### Architecture & Design (D5)

**Rating:** {rating}

{issues or "No issues found"}

### Performance (D6)

**Rating:** {rating}

{issues or "No issues found"}

### Test Coverage (D7)

**Rating:** {rating}

{coverage gaps or "All scenarios covered"}

---

## Tier 3 — Recommended

### Error Handling & Observability (D8/D9)

**Rating:** {rating}

{issues or "No issues found"}

---

## Tier 4 — Nice-to-Have

### Maintainability & Compatibility (D10–D13)

**Rating:** {rating}

{issues or "No issues found"}

{If frontend/fullstack:}
### Accessibility / i18n (D14)

**Rating:** {rating}

{issues or "Skipped (not a frontend project)"}

---

## {Plan Consistency | Documentation Consistency}

{If planning-backed or docs-backed:}
**Criteria Met:** {X/Y}

{unmet criteria or "All criteria met"}

{If bare:}
*No reference documents found — consistency check skipped.*

---

## Recommendations

{Prioritized list of improvements, grouped by blocking status:}

**Must fix before merge:**
1. {highest priority fix with file:line reference}
2. ...

**Should fix:**
1. {recommended fix}
2. ...

**Consider for later:**
1. {nice-to-have improvement}
2. ...

## Verdict

{Final assessment and recommendation}
```

#### 4P.1 Optional: Save to File (`--save`)

If the user passed `--save` in the arguments, **also** write the report to `{output_dir}/project-review.md`. Otherwise, do NOT create the file.

→ Go to Step 5P

---

### Step 5F: Feature Mode — Update state.json

1. Read `state.json`
2. Add or update `review` field in metadata:
   ```json
   {
     "review": {
       "date": "ISO timestamp",
       "rating": "pass_with_notes",
       "merge_readiness": "fix_required",
       "total_issues": 12,
       "blockers": 0,
       "criticals": 2,
       "warnings": 6,
       "suggestions": 4
     }
   }
   ```
   - If `--save` was used, also include `"report": "review.md"` in the review object
3. Update `state.json` `updated` timestamp

→ Go to Step 6

---

### Step 5P: Project Mode — No State Update

Project mode does not update any `state.json` — there is no single feature state to track.

→ Go to Step 6

---

### Step 6: Summary and Next Steps

#### 6.1 Feature Mode

Display:

```
Code Review Complete: {feature_name}

Rating: {overall_rating}
Merge Readiness: {merge_readiness}
Issues: {total_issues} ({blocker_count} blockers, {critical_count} critical, {warning_count} warnings, {suggestion_count} suggestions)
{If --save was used:}
Report saved: {output_dir}/{feature_name}/review.md

{If needs_changes (blockers or criticals > 0):}
🚫 Merge blocked — fix these first:
  1. {highest priority blocker/critical with file:line}
  2. {next priority fix}
  ...
  After fixing: /code-forge:review {feature_name}   Re-run review

{If pass_with_notes (warnings > 0, no blockers/criticals):}
⚠ Merge OK with notes — consider fixing:
  1. {top warning}
  2. ...

{If pass:}
✅ Ready for next steps:
  /code-forge:status {feature_name}         View final status
  Create a Pull Request

Tip: use --save to persist the review report to disk
```

#### 6.2 Project Mode

Display:

```
Project Review Complete: {project_name}

Rating: {overall_rating}
Merge Readiness: {merge_readiness}
Reference: {planning-backed (N plans) | docs-backed (N documents) | bare}
Issues: {total_issues} ({blocker_count} blockers, {critical_count} critical, {warning_count} warnings, {suggestion_count} suggestions)
{If --save was used:}
Report saved: {output_dir}/project-review.md

{If needs_changes (blockers or criticals > 0):}
🚫 Issues require attention:
  1. {highest priority blocker/critical with file:line}
  2. {next priority fix}
  ...
  After fixing: /code-forge:review --project   Re-run review

{If pass_with_notes (warnings > 0, no blockers/criticals):}
⚠ Project quality acceptable with notes — consider fixing:
  1. {top warning}
  2. ...

{If pass:}
✅ Project quality looks good.

Tip: use --save to persist the review report to disk
```

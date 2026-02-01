---
name: code-review
description: Systematic code review for implementation phases verifying architectural principles, framework standards, ADR compliance, and code quality. This skill is invoked by implement-phase as part of its quality gate pipeline, or manually when reviewing code changes. Triggers on "review code", "code review", "/code-review", or automatically as Step 3 of implement-phase.
allowed-tools: Read, Grep, Glob, Bash
argument-hint: "[files-or-path?]"
---

# Code Review

Systematic code review skill that validates implementation quality across five dimensions: service delegation, framework standards, ADR compliance, plan synchronization, and general code quality.

## Design Philosophy

This skill acts as a **quality gate** between implementation phases. It ensures code meets established standards before proceeding, catching issues early when they're cheapest to fix.

## When to Use This Skill

**Automatically invoked by implement-plan:**
- After each phase completes its functional verification
- Before marking a phase as complete
- Before proceeding to the next phase

**Manually invoked when:**
- Reviewing a PR or set of changes
- Validating code before committing
- Checking implementation against architectural decisions

## Review Dimensions

### 1. Service Delegation & Single Responsibility

Verify that implementation follows proper separation of concerns:

| Check | What to Look For |
|-------|------------------|
| Controller thin | Controllers only handle HTTP concerns, delegate to services |
| Service focused | Each service has one clear responsibility |
| No god objects | No classes/modules doing too many things |
| Dependency direction | Dependencies flow inward (controllers → services → repositories) |
| No business logic in wrong layer | Controllers don't contain business rules, repositories don't transform data |

### 2. Framework Standards Compliance

Verify code follows the project's established patterns:

| Check | What to Verify |
|-------|----------------|
| Naming conventions | Files, classes, methods follow project conventions |
| Module structure | New code follows existing module organization |
| Error handling | Uses project's error handling patterns |
| Logging | Follows established logging conventions |
| Configuration | Uses project's config management approach |
| Testing patterns | Tests follow existing test structure and naming |

### 3. ADR Compliance

Verify architectural decisions are followed and documented:

| Check | What to Do |
|-------|------------|
| Read relevant ADRs | Check INDEX.md, identify ADRs related to this change |
| Verify compliance | Implementation follows documented decisions |
| New decisions documented | Any new architectural choices have corresponding ADRs |
| No contradictions | Changes don't violate existing accepted ADRs |

### 4. Plan Synchronization

Verify the plan document reflects current state:

| Check | What to Verify |
|-------|----------------|
| Checkboxes updated | Completed tasks marked with `[x]` |
| Exit conditions recorded | All exit condition statuses updated |
| Deviations noted | Any plan deviations documented with rationale |
| ADR references added | New ADRs linked in plan where relevant |
| Phase status accurate | Current phase progress matches reality |

### 5. General Code Quality

Standard code review concerns:

| Check | What to Look For |
|-------|------------------|
| No security issues | No injection vulnerabilities, proper auth checks |
| No hardcoded secrets | No API keys, passwords, or tokens in code |
| Error handling | Errors handled gracefully, not swallowed |
| Resource cleanup | Connections, streams, handlers properly closed |
| No dead code | No commented-out code, unused imports/variables |
| Test coverage | New code has appropriate test coverage |
| Documentation | Complex logic has explanatory comments |

## Review Workflow

### Step 1: Gather Context

```
1. READ the plan file to understand:
   - Current phase being reviewed
   - Expected deliverables
   - Exit conditions that should be met

2. READ docs/decisions/INDEX.md to identify:
   - ADRs relevant to this change
   - Recently added ADRs

3. IDENTIFY changed files using git:
   - git diff --name-only [base]...HEAD
   - Or use provided file list
```

### Step 2: Framework Pattern Analysis

```
1. SPAWN codebase-pattern-finder to identify project conventions:
   - Service patterns
   - Controller patterns
   - Test patterns
   - Error handling patterns

2. COMPARE changed code against identified patterns
```

### Step 3: Review Each Dimension

Execute reviews in parallel where possible:

```
Task (parallel): "Review service delegation in [files]"
Task (parallel): "Compare code against framework patterns found"
Task (parallel): "Check ADR compliance for [relevant ADRs]"
Task (parallel): "Verify plan file [path] is synchronized"
Task (parallel): "General code quality review of [files]"
```

### Step 4: Generate Review Report

Output a structured review report:

```markdown
# Code Review: [Phase/Feature Name]

**Date:** YYYY-MM-DD
**Files Reviewed:** [count]
**Verdict:** PASS | PASS_WITH_NOTES | NEEDS_CHANGES

## Summary

[1-2 sentence overall assessment]

## Review Results

### Service Delegation & Single Responsibility
Status: PASS | NEEDS_CHANGES

[Findings or "All checks passed"]

### Framework Standards Compliance
Status: PASS | NEEDS_CHANGES

[Findings or "All checks passed"]

### ADR Compliance
Status: PASS | NEEDS_CHANGES

[Findings or "All checks passed"]

### Plan Synchronization
Status: PASS | NEEDS_CHANGES

[Findings or "All checks passed"]

### General Code Quality
Status: PASS | NEEDS_CHANGES

[Findings or "All checks passed"]

## Required Changes

[Numbered list of changes required before approval, or "None"]

## Recommendations

[Optional improvements that don't block approval]

## Files Reviewed

| File | Status | Notes |
|------|--------|-------|
| `path/to/file.ts` | OK | |
| `path/to/other.ts` | ISSUE | [Brief note] |
```

## Integration with implement-phase

When invoked by implement-phase (Step 3 of the phase pipeline), this skill:

1. **Receives context**: Phase number, changed files, plan path
2. **Executes review**: All five dimensions
3. **Returns structured result**:

```
STATUS: PASS | NEEDS_CHANGES
VERDICT: [Brief summary]
CHANGES_REQUIRED: [Count or "None"]
BLOCKING_ISSUES:
- [List of blocking issues, or "None"]
RECOMMENDATIONS:
- [List of non-blocking suggestions]
REPORT: [Path to full review report, if written to disk]
```

### Implement-Phase Integration Point

This skill is Step 3 in the implement-phase pipeline:

```
Step 1: Implementation (subagents)
Step 2: Exit condition verification
Step 3: CODE-REVIEW (this skill) ←
Step 4: ADR compliance check
Step 5: Plan synchronization
Step 6: Completion report
```

The implement-phase skill handles retry logic:
```
1. INVOKE code-review skill for the phase
2. IF code-review returns NEEDS_CHANGES:
   a. PRESENT blocking issues
   b. SPAWN fix subagents for each issue
   c. Re-run code-review
   d. REPEAT until PASS (max 3 retries)
3. PROCEED to Step 4 (ADR compliance)
```

## Invoking the Skill

### From implement-phase (automatic)

```
Skill(skill="code-review"): Review Phase 2 implementation.

Context:
- Plan: docs/plans/auth-implementation.md
- Phase: 2 (Authentication Service)
- Changed files: src/auth/auth.service.ts, src/auth/auth.guard.ts, src/auth/jwt.strategy.ts

Return structured result for implement-phase orchestrator.
```

### Manual invocation

```
/code-review

Review the authentication changes in src/auth/.
Focus on: service delegation, NestJS patterns, and ADR-0012 compliance.
```

## Review Checklists

Detailed checklists are available in references:
- [service-delegation-checklist.md](references/service-delegation-checklist.md)
- [framework-standards-checklist.md](references/framework-standards-checklist.md)
- [adr-compliance-checklist.md](references/adr-compliance-checklist.md)
- [general-quality-checklist.md](references/general-quality-checklist.md)

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **BLOCKING** | Must fix before proceeding | Phase cannot complete |
| **WARNING** | Should fix, but doesn't block | Note for follow-up |
| **INFO** | Suggestion for improvement | Optional enhancement |

## Critical Rule: All Errors Are New Errors

> **Every phase ends with a clean baseline (exit conditions pass).**
> Therefore, ANY error present at code review time was introduced by this phase.

### The Clean Baseline Principle

The implement-phase pipeline guarantees:

```
Previous Phase → Exit Conditions PASS → Clean State
                                            ↓
Current Phase Implementation
                                            ↓
Code Review ← ANY errors here are from THIS phase
```

Since each phase must pass exit conditions (build, lint, typecheck, tests) before completion:
- The previous phase left the codebase in a clean state
- Any errors now present were introduced by the current phase
- This applies to ALL files, not just files we directly modified

### Why This Works

| State | Implication |
|-------|-------------|
| Lint passed before this phase | Any lint errors now = we caused them |
| Build passed before this phase | Any build errors now = we caused them |
| Tests passed before this phase | Any test failures now = we caused them |
| No type errors before this phase | Any type errors now = we caused them |

**There is no "pre-existing error" exception** because:
- If errors existed before, the previous phase wouldn't have completed
- Exit conditions are blocking gates - phases cannot complete with errors
- The baseline is always clean

### Errors in Unchanged Files

Even errors in files we didn't directly modify are our responsibility:

```
Example: We modify src/auth/types.ts
         This causes type errors in src/api/endpoints.ts (which imports our types)

         → The error in endpoints.ts is OUR error
         → We broke it by changing the types it depends on
         → This is BLOCKING
```

### What This Means for Code Review

1. **All build/lint/type errors are blocking** - No exceptions
2. **All test failures are blocking** - No exceptions
3. **No need to check git blame** - If it's broken, fix it
4. **No "tech debt" exceptions** - We leave clean, we inherit clean responsibility

### Inherited Codebases

When implementing on an existing codebase with pre-existing errors:

- **Pre-existing errors are still blocking** - We cannot complete a phase with errors
- **Fixing them becomes part of our work** - Add to the phase tasks if needed
- **We are responsible for leaving clean** - The next phase deserves a clean baseline

The principle is simple: **every phase must end clean**. If we inherit a mess, cleaning it up is our job before we can complete the phase.

### Blocking Issues (always fail review)

- Security vulnerabilities (injection, auth bypass, etc.)
- Hardcoded secrets or credentials
- Violation of accepted ADR
- Missing test coverage for new functionality
- Build/lint/typecheck failures (in ANY file)
- Broken single responsibility (god classes/modules)
- Business logic in wrong layer

### Warning Issues (review passes with notes)

- Minor pattern deviations
- Missing documentation on complex code
- Suboptimal but functional implementation
- Test coverage below project threshold (but not missing)

### Info Issues (suggestions only)

- Code style preferences not enforced by linter
- Alternative implementation approaches
- Performance optimization opportunities
- Future refactoring candidates

## Best Practices

### For Effective Reviews

1. **Read the plan first** - Understand intent before judging implementation
2. **Check ADRs** - Don't flag violations of decisions that don't exist
3. **Be specific** - "Line 45: missing null check" not "error handling is bad"
4. **Prioritize** - Lead with blocking issues, don't bury them in warnings
5. **Verify fixes** - Re-run review after changes, don't assume

### For Review Consumers

1. **Address blocking issues first** - Don't optimize while broken
2. **Ask for clarification** - If a review finding is unclear, ask
3. **Don't argue with patterns** - Follow established conventions, propose changes via ADR
4. **Track warnings** - Create follow-up tasks for non-blocking issues

## Example Review Session

```
implement-phase: Step 2 (exit conditions) passed. Running Step 3: code review.

code-review: Reviewing Phase 2: Authentication Service

Files: src/auth/auth.service.ts, auth.guard.ts, jwt.strategy.ts

● Checking service delegation...
  - ✅ Controllers thin, delegate to AuthService
  - ✅ AuthService focused on authentication only
  - ✅ No business logic in guards

● Checking framework standards...
  - ✅ Follows NestJS injectable patterns
  - ✅ Uses project's config service
  - ⚠️ Logger not using project's custom logger

● Checking ADR compliance...
  - ✅ ADR-0012 (JWT auth): Compliant
  - ✅ No contradictions with existing ADRs

● Checking plan synchronization...
  - ✅ All Phase 2 tasks marked complete
  - ✅ Exit conditions recorded
  - ⚠️ Missing link to ADR-0012 in plan

● Checking general quality...
  - ✅ No security issues
  - ✅ Test coverage adequate
  - ✅ No dead code

STATUS: PASS_WITH_NOTES
VERDICT: Code meets standards with minor improvements suggested
CHANGES_REQUIRED: 0
BLOCKING_ISSUES: None
RECOMMENDATIONS:
- Use project's CustomLogger instead of NestJS Logger
- Add ADR-0012 reference to plan's Phase 2 section
```

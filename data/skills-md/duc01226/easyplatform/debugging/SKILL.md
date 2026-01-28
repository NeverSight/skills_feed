---
name: debugging
description: >-
  Systematic debugging framework for root cause investigation before fixes.
  Use for bugs, test failures, unexpected behavior, performance issues.
  Use `--autonomous` flag for structured headless debugging with approval gates.
  Triggers: debug, bug, error, fix, diagnose, root cause, stack trace, investigate issue.
  NOT for: code review (use code-review), simplification (use code-simplifier).
version: 4.0.0
languages: all
infer: true
---

# Debugging

Comprehensive debugging framework combining systematic investigation, root cause tracing, defense-in-depth validation, and verification protocols.

## Core Principle

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

Random fixes waste time and create new bugs. Find the root cause, fix at source, validate at every layer, verify before claiming success.

## When to Use

**Always use for:** Test failures, bugs, unexpected behavior, performance issues, build failures, integration problems, before claiming work complete

**Especially when:** Under time pressure, "quick fix" seems obvious, tried multiple fixes, don't fully understand issue, about to claim success

## Mode Selection

| Mode            | Flag           | Use When                                              | Workflow                                         |
| --------------- | -------------- | ----------------------------------------------------- | ------------------------------------------------ |
| **Interactive** | (default)      | User available for feedback, exploratory debugging    | Real-time collaboration, iterative investigation |
| **Autonomous**  | `--autonomous` | Batch debugging, CI/CD, comprehensive analysis needed | 5-phase structured workflow with approval gates  |

### Interactive Mode (Default)

Standard debugging with user engagement. Use the techniques below with real-time feedback.

### Autonomous Mode (`--autonomous`)

Structured headless debugging workflow with approval gates. Creates artifacts in `.ai/workspace/analysis/`.

**Invocation:** `/debugging --autonomous` or `/debug --autonomous`

**Workflow:**

1. **Phase 1:** Bug Report Analysis → Document in `.ai/workspace/analysis/[bug-name].md`
2. **Phase 2:** Evidence Gathering → Multi-pattern search, dependency tracing
3. **Phase 3:** Root Cause Analysis → Ranked causes with confidence levels
4. **Phase 4:** Solution Proposal → Code changes, risk assessment, testing strategy
5. **Phase 5:** Approval Gate → Present analysis for user approval before implementing

**Key Features:**

- Anti-hallucination protocols (assumption validation, evidence chains)
- Confidence level tracking (High ≥90%, Medium 70-89%, Low <70%)
- Structured evidence documentation
- Explicit approval required before implementation

**⚠️ MUST READ — Full workflow details:** `references/autonomous-workflow.md`

## The Four Techniques

### 1. Systematic Debugging (`references/systematic-debugging.md`)

Four-phase framework ensuring proper investigation:

- Phase 1: Root Cause Investigation (read errors, reproduce, check changes, gather evidence)
- Phase 2: Pattern Analysis (find working examples, compare, identify differences)
- Phase 3: Hypothesis and Testing (form theory, test minimally, verify)
- Phase 4: Implementation (create test, fix once, verify)

**Key rule:** Complete each phase before proceeding. No fixes without Phase 1.

**⚠️ MUST READ when:** Any bug/issue requiring investigation and fix

### 2. Root Cause Tracing (`references/root-cause-tracing.md`)

Trace bugs backward through call stack to find original trigger.

**Technique:** When error appears deep in execution, trace backward level-by-level until finding source where invalid data originated. Fix at source, not at symptom.

**Includes:** `scripts/find-polluter.sh` for bisecting test pollution

**⚠️ MUST READ when:** Error deep in call stack, unclear where invalid data originated

### 3. Defense-in-Depth (`references/defense-in-depth.md`)

Validate at every layer data passes through. Make bugs impossible.

**Four layers:** Entry validation → Business logic → Environment guards → Debug instrumentation

**⚠️ MUST READ when:** After finding root cause, need to add comprehensive validation

### 4. Verification (`references/verification.md`)

Run verification commands and confirm output before claiming success.

**Iron law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

Run the command. Read the output. Then claim the result.

**⚠️ MUST READ when:** About to claim work complete, fixed, or passing

### 5. EasyPlatform-Specific (`references/easyplatform-debugging.md`)

Platform-specific debugging patterns for the Easy.Platform .NET 9 + Angular 19 monorepo.

**Covers:**

- Backend error patterns (PlatformValidationResult, PlatformException, EnsureFound)
- Frontend error patterns (observerLoadingErrorState, stores, forms)
- Common bug categories by layer
- Platform-specific investigation workflow

**⚠️ MUST READ when:** Debugging issues in EasyPlatform codebase

## Quick Reference

```
Bug → systematic-debugging.md (Phase 1-4)
  Error deep in stack? → root-cause-tracing.md (trace backward)
  Found root cause? → defense-in-depth.md (add layers)
  EasyPlatform issue? → easyplatform-debugging.md (platform patterns)
  About to claim success? → verification.md (verify first)
```

## Red Flags

Stop and follow process if thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "It's probably X, let me fix that"
- "Should work now" / "Seems fixed"
- "Tests pass, we're done"

**All mean:** Return to systematic process.

## Related

- **Follow-up:** `code-simplifier` - Simplify code after debugging
- **Review:** `code-review` - Review fixes before committing
- **Testing:** `test-specs-docs` - Generate tests for the fix
- **Upstream:** `feature-investigation` - General codebase investigation

## Version History

| Version | Date       | Changes                                                                  |
| ------- | ---------- | ------------------------------------------------------------------------ |
| 4.0.0   | 2026-01-20 | Merged tasks-bug-diagnosis, added autonomous mode with --autonomous flag |
| 3.0.0   | 2025-12-01 | Added EasyPlatform-specific debugging, verification protocols            |
| 2.0.0   | 2025-10-15 | Added defense-in-depth, root cause tracing                               |
| 1.0.0   | 2025-08-01 | Initial release with systematic debugging                                |

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

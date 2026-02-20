---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue: test failures, bugs, unexpected behavior, performance problems, build failures, integration issues.

**Use ESPECIALLY when:** under time pressure, "just one quick fix" seems obvious, you've already tried multiple fixes, you don't fully understand the issue.

**Don't skip when:** issue seems simple, you're in a hurry, manager wants it fixed NOW.

## Quick Reference — The Four Phases

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

For detailed step-by-step instructions for each phase, see [references/four-phases-detailed.md](references/four-phases-detailed.md).

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4 in detailed reference).

## Supporting Techniques

- **`root-cause-tracing.md`** — Trace bugs backward through call stack
- **`defense-in-depth.md`** — Add validation at multiple layers
- **`condition-based-waiting.md`** — Replace arbitrary timeouts with condition polling

**Related skills:**
- **test-driven-development** — For creating failing test case (Phase 4)
- **verification-before-completion** — Verify fix worked before claiming success

For user signals, rationalizations table, and "no root cause" guidance, see [references/debugging-signals.md](references/debugging-signals.md).

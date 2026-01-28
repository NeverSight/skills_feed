---
name: code-review
description: Code review practices emphasizing technical rigor, evidence-based claims, and verification. Use when receiving code review feedback, completing tasks requiring review, or before making completion claims.
license: MIT
---

# Code Review

Guide proper code review practices emphasizing technical rigor, evidence-based claims, and verification over performative responses.

## Overview

Code review requires three distinct practices:

1. **Receiving feedback** - Technical evaluation over performative agreement
2. **Requesting reviews** - Systematic review processes
3. **Verification gates** - Evidence before any completion claims

## Core Principle

**Technical correctness over social comfort.** Verify before implementing. Ask before assuming. Evidence before claims.

## When to Use

### Receiving Feedback
- Receiving code review comments from any source
- Feedback seems unclear or technically questionable
- Multiple review items need prioritization
- External reviewer lacks full context
- Suggestion conflicts with existing decisions

### Requesting Review
- Completing tasks in subagent-driven development (after EACH task)
- Finishing major features or refactors
- Before merging to main branch
- Stuck and need fresh perspective
- After fixing complex bugs

### Verification Gates
- About to claim tests pass, build succeeds, or work is complete
- Before committing, pushing, or creating PRs
- Moving to next task
- Any statement suggesting success/completion

## Quick Decision Tree

```
SITUATION?
│
├─ Received feedback
│  ├─ Unclear items? → STOP, ask for clarification first
│  ├─ From human partner? → Understand, then implement
│  └─ From external reviewer? → Verify technically before implementing
│
├─ Completed work
│  ├─ Major feature/task? → Request systematic review
│  └─ Before merge? → Request systematic review
│
└─ About to claim status
   ├─ Have fresh verification? → State claim WITH evidence
   └─ No fresh verification? → RUN verification command first
```

## CI Verification

Before any completion claim or commit:
- Run CI checks (types, tests, lint)
- Prefer single CI command if available
- Verify all checks pass
- Do not proceed if checks fail

## References

For detailed protocols, see:
- `references/receiving-feedback.md` - How to handle code review feedback
- `references/requesting-review.md` - Systematic review processes
- `references/verification-gates.md` - Evidence before claims protocol

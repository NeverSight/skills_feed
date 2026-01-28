---
name: code-review
description: Use when receiving code review feedback (especially if unclear or technically questionable), when completing tasks or major features requiring review before proceeding, or before making any completion/success claims. Covers three practices - receiving feedback with technical rigor over performative agreement, requesting reviews via code-reviewer subagent, and verification gates requiring evidence before any status claims. Essential for subagent-driven development, pull requests, and preventing false completion claims.
---

# Code Review

Guide proper code review practices emphasizing technical rigor, evidence-based claims, and verification over performative responses.

## Overview

Code review requires three distinct practices:

1. **Receiving feedback** - Technical evaluation over performative agreement
2. **Requesting reviews** - Systematic review via code-reviewer subagent
3. **Verification gates** - Evidence before any completion claims

Each practice has specific triggers and protocols detailed in reference files.

## Core Principle

Always honoring **YAGNI**, **KISS**, and **DRY** principles.
**Be honest, be brutal, straight to the point, and be concise.**

**Technical correctness over social comfort.** Verify before implementing. Ask before assuming. Evidence before claims.

## CRITICAL: Two-Phase Report-Driven Review

**MUST generate TodoWrite tasks for BOTH phases before starting ANY review!**

### Phase 1 Todos (File-by-File Review)

```
- [ ] Create review report file
- [ ] Review [file1] - document in report
- [ ] Review [file2] - document in report
- [ ] ... (one todo per changed file)
```

### Phase 2 Todos (Holistic Review)

```
- [ ] Read accumulated report for big picture
- [ ] Assess architecture coherence
- [ ] Check responsibility placement
- [ ] Detect cross-file duplication
- [ ] Generate final recommendations
```

**Phase 1:** Review each file individually, documenting Change Summary, Purpose, Issues Found, and Suggestions in the report.

**Phase 2:** After all files reviewed, read the accumulated report to see the big picture, then generate final assessment covering architecture coherence, responsibility placement, duplication detection, and prioritized recommendations.

## When to Use This Skill

### Receiving Feedback

Trigger when:

- Receiving code review comments from any source
- Feedback seems unclear or technically questionable
- Multiple review items need prioritization
- External reviewer lacks full context
- Suggestion conflicts with existing decisions

**⚠️ MUST READ:** `references/code-review-reception.md`

### Requesting Review

Trigger when:

- Completing tasks in subagent-driven development (after EACH task)
- Finishing major features or refactors
- Before merging to main branch
- Stuck and need fresh perspective
- After fixing complex bugs

**⚠️ MUST READ:** `references/requesting-code-review.md`

### Verification Gates

Trigger when:

- About to claim tests pass, build succeeds, or work is complete
- Before committing, pushing, or creating PRs
- Moving to next task
- Any statement suggesting success/completion
- Expressing satisfaction with work

**⚠️ MUST READ:** `references/verification-before-completion.md`

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
│  ├─ Major feature/task? → Request code-reviewer subagent review
│  └─ Before merge? → Request code-reviewer subagent review
│
└─ About to claim status
   ├─ Have fresh verification? → State claim WITH evidence
   └─ No fresh verification? → RUN verification command first
```

## Receiving Feedback Protocol

### Response Pattern

READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT

### Key Rules

- ❌ No performative agreement: "You're absolutely right!", "Great point!", "Thanks for [anything]"
- ❌ No implementation before verification
- ✅ Restate requirement, ask questions, push back with technical reasoning, or just start working
- ✅ If unclear: STOP and ask for clarification on ALL unclear items first
- ✅ YAGNI check: grep for usage before implementing suggested "proper" features

### Source Handling

- **Human partner:** Trusted - implement after understanding, no performative agreement
- **External reviewers:** Verify technically correct, check for breakage, push back if wrong

**⚠️ MUST READ — Full protocol:** `references/code-review-reception.md`

## Requesting Review Protocol

### When to Request

- After each task in subagent-driven development
- After major feature completion
- Before merge to main

### Process

1. Get git SHAs: `BASE_SHA=$(git rev-parse HEAD~1)` and `HEAD_SHA=$(git rev-parse HEAD)`
2. Dispatch code-reviewer subagent via Task tool with: WHAT_WAS_IMPLEMENTED, PLAN_OR_REQUIREMENTS, BASE_SHA, HEAD_SHA, DESCRIPTION
3. Act on feedback: Fix Critical immediately, Important before proceeding, note Minor for later

**⚠️ MUST READ — Full protocol:** `references/requesting-code-review.md`

## Verification Gates Protocol

### The Iron Law

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE**

### Gate Function

IDENTIFY command → RUN full command → READ output → VERIFY confirms claim → THEN claim

Skip any step = lying, not verifying

### Requirements

- Tests pass: Test output shows 0 failures
- Build succeeds: Build command exit 0
- Bug fixed: Test original symptom passes
- Requirements met: Line-by-line checklist verified

### Red Flags - STOP

Using "should"/"probably"/"seems to", expressing satisfaction before verification, committing without verification, trusting agent reports, ANY wording implying success without running verification

**⚠️ MUST READ — Full protocol:** `references/verification-before-completion.md`

## Integration with Workflows

- **Subagent-Driven:** Review after EACH task, verify before moving to next
- **Pull Requests:** Verify tests pass, request code-reviewer review before merge
- **General:** Apply verification gates before any status claims, push back on invalid feedback

## Bottom Line

1. Technical rigor over social performance - No performative agreement
2. Systematic review processes - Use code-reviewer subagent
3. Evidence before claims - Verification gates always

Verify. Question. Then implement. Evidence. Then claim.

## Frontend Compliance (Angular)

When reviewing frontend TypeScript files, apply frontend-specific compliance checks:

### Severity Levels

| Severity     | Action                     | Examples                                      |
| ------------ | -------------------------- | --------------------------------------------- |
| **CRITICAL** | MUST fix before approval   | Direct Platform* extension, direct HttpClient |
| **HIGH**     | MUST fix before merge      | Missing untilDestroyed(), manual destroy$     |
| **MEDIUM**   | Should fix if time permits | Missing BEM classes                           |

### Key Checks

1. **CRITICAL:** Components extend `AppBase*` classes, NOT `Platform*` directly
2. **CRITICAL:** Services extend `PlatformApiService`, NOT direct `HttpClient`
3. **HIGH:** Subscriptions use `.pipe(this.untilDestroyed())`, NOT manual `destroy$`
4. **HIGH:** State uses `PlatformVmStore`, NOT manual signals
5. **MEDIUM:** Templates have BEM classes on ALL elements (`block__element --modifier`)

**⚠️ MUST READ — Full checklist:** `references/frontend-compliance.md`

## Related

- **Debugging:** `debugging` - Root cause investigation before fixes
- **Testing:** `test-specs-docs` - Create tests for bug fixes
- **Simplification:** `code-simplifier` - Simplify code after review
- **Frontend Patterns:** See `docs/claude/frontend-typescript-complete-guide.md`

## See Also

See `/review` command for review execution checklist.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

---
name: superbuild
description: Use when executing implementation plans phase-by-phase with strict enforcement of quality gates, tests, and Definition of Done. Triggers on "build this plan", "execute plan", "implement phases", or when user provides a plan document to execute.
metadata:
  version: "1.0.0"
  author: skulto
compatibility: Requires plan document in superplan format. Works with any codebase with quality tools configured.
---

# Superbuild: Plan Execution Engine

Execute implementation plans one phase at a time with strict quality enforcement, test verification, and conventional commit generation.

## Overview

Superbuild is a **rigid execution engine** for implementation plans. It enforces:
- Phase-by-phase execution (no skipping ahead)
- Definition of Done verification before phase completion
- Test presence and passing verification
- Linter/formatter/typechecker enforcement
- Conventional commit message generation per phase

**This is NOT a planning skill.** Use `superplan` to create plans, then `superbuild` to execute them.

---

## Reference Index - MUST READ When Needed

**References contain detailed templates and patterns. Read BEFORE you need them.**

| When | Reference | What You Get |
|------|-----------|--------------|
| **Step 3: Executing tasks** | [superplan/references/TASK-MICROSTRUCTURE.md] | 5-step TDD format per task |
| **Step 3: Executing tasks** | [superplan/references/TDD-DISCIPLINE.md] | TDD rules, rationalizations, red flags |
| **Step 4: Any check fails** | [references/ENFORCEMENT-GUIDE.md](references/ENFORCEMENT-GUIDE.md) | Failure templates, output parsing, stack commands |
| **Step 5: Updating plan** | [references/PLAN-UPDATES.md](references/PLAN-UPDATES.md) | Checkbox patterns, status updates |
| **Step 6: Commit message** | [references/COMMIT-FORMAT.md](references/COMMIT-FORMAT.md) | CLI-safe chars, HEREDOC format |
| **Steps 7-8: Stop/Resume** | [references/EXECUTION-CONTROL.md](references/EXECUTION-CONTROL.md) | Output templates, compaction behavior |
| **Step 9: AUTO-COMPACT** | [references/EXECUTION-CONTROL.md](references/EXECUTION-CONTROL.md) | CHECKPOINT parsing, auto-compact workflow |

**DO NOT SKIP REFERENCES.** They contain exact templates and patterns that are NOT duplicated here.

---

## Critical Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      SUPERBUILD EXECUTION FLOW                       │
│                     (REPEAT FOR EACH PHASE)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. INGEST PLAN    │  User provides plan document path              │
│         ↓          │  NO PLAN = EXIT (ask user, then exit if none)  │
│  2. READ PHASES    │  Output ALL phases with estimates              │
│         ↓          │  IF context high → suggest compact first       │
│  2.5 PLAN REVIEW   │  Check for ambiguity, missing deps, test gaps  │
│         ↓          │  IF concerns → PAUSE and ask user              │
│  3. EXECUTE PHASE  │  One phase at a time (or parallel if marked)   │
│         ↓          │  USE SUB-AGENTS for parallel phases            │
│  4. ENFORCE DOD    │  Tests exist? Tests pass? Linter? Formatter?   │
│         ↓          │  ALL must pass → continue. ANY fail → STOP     │
│  5. UPDATE PLAN    │  Check off tasks, update status in plan file   │
│         ↓          │  ⚠️  THIS HAPPENS AFTER EVERY PHASE            │
│  6. COMMIT MSG     │  Generate conventional commit (NEVER git ops)  │
│         ↓          │  User handles all git operations               │
│  7. FUNCTIONAL TEST│  Explain how to test. Offer integration script │
│         ↓          │  NEVER auto-create scripts. ALWAYS ask first   │
│  8. STOP           │  Full stop. Suggest compact. Wait for user.    │
│         ↓          │  OVERRIDE: --build-all flag continues          │
│  9. AUTO-COMPACT   │  BUILD-ALL ONLY: Run /compact at CHECKPOINT    │
│                    │  Parse focus from CHECKPOINT, compact, continue│
│                                                                     │
│  ════════════════════════════════════════════════════════════════   │
│  Steps 3-8 repeat for EACH PHASE. Plan updates after EVERY phase.  │
│  BUILD-ALL: Steps 3-9 repeat automatically with auto-compact.       │
│  ════════════════════════════════════════════════════════════════   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Step 1: Ingest Plan

**REQUIRED: Plan document must be provided.**

### Plan Header Recognition

Plans created by `superplan` include this header:

```markdown
> **For Claude:** Execute this plan using `/superbuild` skill.
```

This confirms the plan is in the expected format with:
- Parallelizable phases with poker estimates
- Definition of Done per phase
- 5-step TDD micro-structure per task

```
I'll help you execute your implementation plan.

Please provide the plan document:
1. Path to plan file (e.g., docs/feature-plan.md)
2. Paste the plan content directly

Which would you prefer?
```

**If no plan provided after asking:** EXIT immediately.

```
I cannot execute without a plan document.

To create a plan, use the `superplan` skill first:
  /superplan

Then come back with the completed plan.

[EXIT - No further action]
```

**NO EXCEPTIONS.** Do not improvise. Do not create plans on the fly. Do not proceed without a plan document.

## Step 2: Read All Phases

After ingesting the plan:

1. **Output all phases** with their estimates and dependencies
2. **Check context usage** - if high, suggest compacting first

```
PLAN LOADED: [Feature Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Phase | Name | Est. | Depends On | Parallel With | Status |
|-------|------|------|------------|---------------|--------|
| 0 | Bootstrap | 5 | - | - | ⬜ |
| 1 | Setup | 3 | 0 | - | ⬜ |
| 2A | Backend | 8 | 1 | 2B, 2C | ⬜ |
| 2B | Frontend | 5 | 1 | 2A, 2C | ⬜ |
| 2C | Tests | 3 | 1 | 2A, 2B | ⬜ |
| 3 | Integration | 5 | 2A,2B,2C | - | ⬜ |

Total: 29 points | Parallel phases: 2A, 2B, 2C

⚠️  Context Usage Advisory
If context is high, consider compacting before continuing.
Large plans consume significant context per phase.

Ready to execute Phase 0?
```

## Step 2.5: Critical Plan Review

Before executing, review the plan for concerns:

1. **Ambiguous tasks** - Any task unclear about what to do?
2. **Missing dependencies** - Are required files/APIs/packages identified?
3. **Test gaps** - Does each task have testable acceptance criteria?
4. **Risky changes** - Any destructive operations or breaking changes?

### If Concerns Exist

```
⚠️  PLAN REVIEW - Concerns Identified
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Concern 1 - what and why]
2. [Concern 2 - what and why]

Please clarify before I proceed.
[EXECUTION PAUSED]
```

### If No Concerns

Proceed to Step 3 (Execute Phase).

## Step 3: Execute Phase

### TDD Micro-Structure Enforcement

Plans created by `superplan` use a 5-step TDD micro-structure per task:

1. Write failing test
2. Run test, verify failure **(MANDATORY - must see it fail)**
3. Write minimal implementation
4. Run test, verify pass **(MANDATORY - must see it pass)**
5. Stage for commit

> **STOP. Read `superplan/references/TASK-MICROSTRUCTURE.md` and `superplan/references/TDD-DISCIPLINE.md` NOW** before executing any task.

### TDD Enforcement Rules

When executing tasks, enforce this order STRICTLY:

| Rule | Enforcement |
|------|-------------|
| Test before code | **STOP** if implementation exists without test |
| Verify RED | **STOP** if test passes immediately (testing existing behavior) |
| Minimal code | **STOP** if adding features beyond current test |
| Verify GREEN | **STOP** if test not run after implementation |
| No regressions | **STOP** if other tests now fail |

**If test passes immediately:** The test is wrong. It tests existing behavior, not new behavior. Fix the test or you are not doing TDD.

**If you cannot explain why the test failed:** You do not understand what you are testing. Stop and clarify requirements.

### Sequential Phases

Execute one at a time. Do not proceed to next phase until current is COMPLETE.

### Parallel Phases

For phases marked "Parallel With", **MUST use sub-agents or parallel Task tool calls**.

```
EXECUTING PARALLEL PHASES: 2A, 2B, 2C
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Launching 3 parallel sub-agents...

[Sub-agent 2A: Backend implementation]
[Sub-agent 2B: Frontend implementation]
[Sub-agent 2C: Test implementation]

Each sub-agent MUST return:
- Implementation status
- Definition of Done checklist status
- Conventional commit message
```

**CRITICAL:** Each sub-agent returns its commit message. Main agent MUST bubble up ALL commit messages to user.

### Sub-Agent Result Verification

**CRITICAL: Do NOT trust sub-agent claims without independent verification.**

When parallel phases complete:
1. Collect all sub-agent results
2. For EACH sub-agent claiming success:
   - Run `npm test` (or equivalent) to verify tests pass
   - Run `npm run lint` to verify linter passes
   - Verify plan file was actually updated
3. Only after independent verification, output commit messages

Sub-agent reports are CLAIMS, not EVIDENCE. Fresh verification required.

## Step 4: Enforce Definition of Done

**EVERY phase must pass ALL quality gates before completion.**

### Fresh Verification Requirement

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

The Verification Gate (run for EVERY check):

1. **IDENTIFY** - Which command proves this claim?
2. **RUN** - Execute the command NOW (not from memory)
3. **READ** - Examine FULL output, count failures/errors
4. **VERIFY** - Does output match the claim?
5. **THEN CLAIM** - Only state success after steps 1-4

**Invalid Evidence:**
- Previous run output (even from 2 minutes ago)
- Assumptions based on code changes
- Partial verification ("linter passed so types probably pass")
- Agent/sub-agent reports without independent verification

### Red Flag Language - HALT Immediately

If you find yourself using these words about verification:

| Red Flag | Meaning | Required Action |
|----------|---------|-----------------|
| "should pass" | Uncertainty | RUN the check, don't assume |
| "probably works" | Uncertainty | RUN the check, don't assume |
| "seems to be fine" | Uncertainty | RUN the check, don't assume |
| "I believe it passes" | No evidence | RUN the check, get evidence |
| "based on my changes" | Inference, not verification | RUN the check |

**Any hedging language = missing verification.** Stop and run the actual check.

### Quality Gate Checklist

```
DEFINITION OF DONE - Phase [X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] Tests exist for new code
[ ] All tests pass (new AND existing)
[ ] Linter passes ([detected linter])
[ ] Formatter passes ([detected formatter])
[ ] Type checker passes ([detected checker])
[ ] No new warnings introduced
[ ] Plan document updated (checkboxes, status)  ← BEFORE commit message
```

### Enforcement Rules

| Check | If PASS | If FAIL |
|-------|---------|---------|
| Tests exist | Continue | **STOP** - Point out missing tests |
| Tests pass | Continue | **STOP** - Ask user to fix |
| Linter | Continue | **STOP** - Ask user to fix |
| Formatter | Continue | **STOP** - Ask user to fix |
| Type checker | Continue | **STOP** - Ask user to fix |
| Plan updated | Generate commit | **STOP** - Update plan first |

**STOP means STOP.** Do not proceed. Do not offer to fix automatically. Ask user to fix and re-run.

### Failure Output Format

When any check fails, output:

```
⛔ DEFINITION OF DONE FAILED
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Issue: [Missing tests | Tests failing | Linter errors | etc.]
[Details of what failed]
Please fix, then tell me to continue.
[EXECUTION HALTED]
```

> **STOP. Read [ENFORCEMENT-GUIDE.md](references/ENFORCEMENT-GUIDE.md) NOW** when any check fails - contains failure templates and stack-specific commands.

## Step 5: Update Plan Document (EVERY PHASE)

**⚠️ MANDATORY: This step executes after EVERY phase, not just at the end.**

After ALL quality gates pass, BEFORE generating commit message, UPDATE THE PLAN FILE:

1. **Check off completed tasks** (`- [ ]` → `- [x]`)
2. **Update phase status** in overview table (`⬜` → `✅`)
3. **Mark DoD items complete** (`- [ ]` → `- [x]`)

```
PLAN DOCUMENT UPDATED - Phase [X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: [plan-file-path]

Updates applied:
- Tasks: X/X items checked [x]
- DoD: X/X items checked [x]
- Status: ⬜ → ✅

The plan now reflects Phase [X] completion.
```

> **Read [PLAN-UPDATES.md](references/PLAN-UPDATES.md)** for checkbox patterns and error handling.

**WHY EVERY PHASE:**
- Plan survives context compaction (conversation may not)
- Progress visible to anyone reading the plan
- Enables clean handoff between sessions
- Creates audit trail in git history

**DO NOT SKIP THIS STEP.** If you find yourself generating a commit message without updating the plan first, STOP and update the plan.

## Step 6: Generate Conventional Commit

**After Definition of Done passes, generate commit message.**

**CRITICAL: OUTPUT ONLY. NEVER run git commands.**

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructure (no behavior change) |
| `test` | Adding/updating tests |
| `docs` | Documentation |
| `chore` | Build, config, dependencies |

> **Read [COMMIT-FORMAT.md](references/COMMIT-FORMAT.md)** for CLI-safe characters and HEREDOC patterns.
>
> **Read [EXECUTION-CONTROL.md](references/EXECUTION-CONTROL.md)** for parallel phase commit output format.

## Step 7: Functional Testing Instructions

**After commit message, explain how to functionally test the phase.**

Provide step-by-step manual verification instructions. Offer integration test script only if applicable - ALWAYS ask, NEVER auto-create.

> **Read [EXECUTION-CONTROL.md](references/EXECUTION-CONTROL.md)** for output format and script offer template.

## Step 8: Stop Execution

**FULL STOP after each phase (unless --build-all override).**

1. Output phase completion summary
2. Show progress table
3. Suggest context compaction
4. Wait for explicit "Continue to Phase X" instruction

**Post-compaction behavior:** Complete in-progress phase only, then STOP. Todo list is NOT authorization to continue.

**Build-all override:** Only if user explicitly requests. Warn about risks first.

> **Read [EXECUTION-CONTROL.md](references/EXECUTION-CONTROL.md)** for output templates and compaction behavior.

---

## Step 9: Auto-Compact in BUILD-ALL Mode

**CRITICAL: In BUILD-ALL mode, automatic context compaction is MANDATORY.**

When running with `--build-all` flag, execute `/compact` automatically after each phase CHECKPOINT to preserve context for remaining phases.

### Auto-Compact Trigger

Plans created by `superplan` include CHECKPOINT markers at the end of each phase:

```markdown
- [ ] **CHECKPOINT: Run `/compact focus on: Phase N complete, [key artifacts], Phase N+1 goals`**
```

### BUILD-ALL Auto-Compact Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BUILD-ALL MODE: AUTO-COMPACT                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. COMPLETE PHASE   │  Execute all tasks, pass quality gates       │
│          ↓           │                                              │
│  2. UPDATE PLAN      │  Check off tasks, mark CHECKPOINT done       │
│          ↓           │                                              │
│  3. GENERATE COMMIT  │  Output conventional commit message          │
│          ↓           │                                              │
│  4. DETECT CHECKPOINT│  Find CHECKPOINT task in completed phase     │
│          ↓           │                                              │
│  5. EXTRACT FOCUS    │  Parse focus directive from CHECKPOINT       │
│          ↓           │                                              │
│  6. RUN /COMPACT     │  Execute: /compact focus on: [extracted]     │
│          ↓           │  ⚠️  NO USER INTERVENTION REQUIRED           │
│  7. CONTINUE         │  Proceed to next phase automatically         │
│                                                                     │
│  ════════════════════════════════════════════════════════════════   │
│  Steps 1-7 repeat for EACH PHASE until plan complete.               │
│  ════════════════════════════════════════════════════════════════   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### CHECKPOINT Parsing

Extract the focus directive from the CHECKPOINT task:

```
Input:  - [ ] **CHECKPOINT: Run `/compact focus on: Phase 1 complete, auth models created, Phase 2 needs endpoints`**

Parsed: focus on: Phase 1 complete, auth models created, Phase 2 needs endpoints
```

### Auto-Compact Execution

**Execute `/compact` with the parsed focus directive:**

```
AUTO-COMPACT TRIGGERED - Phase [X] Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Running: /compact focus on: [parsed focus directive]

Preserving:
- Phase [X] completion status
- Key artifacts: [list from focus]
- Phase [X+1] goals: [from focus]

[compact executes]

Context refreshed. Continuing to Phase [X+1]...
```

### No CHECKPOINT Found

If a phase lacks a CHECKPOINT (legacy plan or manual creation):

```
⚠️  NO CHECKPOINT FOUND - Phase [X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This phase has no CHECKPOINT marker for auto-compact.

Options:
1. Continue without compact (risk context exhaustion)
2. Pause for manual /compact
3. Add CHECKPOINT to plan and retry

Recommendation: Option 2 for safety

[EXECUTION PAUSED - Awaiting instruction]
```

> **Read [EXECUTION-CONTROL.md](references/EXECUTION-CONTROL.md)** for detailed auto-compact patterns.

## Rationalizations to Reject

| Excuse | Reality |
|--------|---------|
| "Let me just do the next phase too" | **NO.** Stop after each phase. |
| "The tests are mostly there" | **NO.** Tests must exist for ALL new code. |
| "It's just a small linting error" | **NO.** All quality gates must pass. |
| "I'll commit later" | **NO.** Generate commit message NOW. |
| "This phase doesn't need tests" | **NO.** Every phase with code needs tests. |
| "Let me skip to the important part" | **NO.** Execute phases in dependency order. |
| "I can fix the formatter later" | **NO.** Formatter must pass before completion. |
| "The user wants to move fast" | **NO.** Quality enforcement is non-negotiable. |
| "I'm confident this works" | **NO.** Confidence ≠ evidence. Run the check. |
| "I just ran it a moment ago" | **NO.** Run it again. Fresh evidence required. |
| "The code is correct, so tests will pass" | **NO.** Run the tests. Code review ≠ testing. |
| "This is a minor change" | **NO.** All changes require verification. |
| "Too simple to need a test" | **NO.** Simple code breaks. Write the test. |
| "I'll add tests after the code works" | **NO.** Tests-after pass immediately. No proof of value. |
| "I already manually tested it" | **NO.** Ad-hoc testing is not systematic. TDD required. |
| "The test passed immediately, so it works" | **NO.** Immediate pass = testing existing behavior. Fix test. |

## Red Flags - STOP Immediately

If you catch yourself thinking any of these, STOP:

- "This is taking too long, let me skip ahead"
- "The user seems impatient, let me batch phases"
- "Tests can come after the feature works"
- "Linting is just style, not critical"
- "I'll generate all commit messages at the end"
- "The plan doesn't explicitly require tests"
- "The sub-agent confirmed it passes"
- "I already verified this earlier"
- "This is obviously correct"
- "I wrote the code first, but I'll test it now"
- "The test passed on the first try"
- "This feature is too simple for TDD"
- "Let me just get it working, then add tests"

**All of these = violation of superbuild protocol.**

## Quality Commands by Stack

> **Read [ENFORCEMENT-GUIDE.md](references/ENFORCEMENT-GUIDE.md)** for stack-specific commands (JS/TS, Python, Go, Rust).

## Summary: The Iron Rules

1. **No plan = No execution** - Exit if plan not provided
2. **One phase at a time** - Unless parallel phases (use sub-agents)
3. **All quality gates must pass** - No exceptions
4. **Update plan after EVERY phase** - Check off tasks, update status
5. **Generate commit message** - Never run git commands
6. **Explain functional testing** - Ask before writing scripts
7. **Full stop after phase** - Unless --build-all override
8. **Suggest compact** - Context management is critical
9. **Fresh verification required** - Run checks NOW, not from memory
10. **Auto-compact in BUILD-ALL** - Parse CHECKPOINT, run /compact, continue automatically

**Superbuild is rigid by design.** The enforcement protects code quality. Do not rationalize around it.

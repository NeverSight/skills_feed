---
name: implement-plan
description: Orchestrate the execution of complete implementation plans, delegating each phase to implement-phase skill. This skill manages the full plan lifecycle including phase sequencing, user confirmation between phases, and overall progress tracking. Triggers on "implement the plan", "execute the implementation plan", or when given a path to a plan file.
context: fork
argument-hint: "[plan-path]"
---

# Implement Plan

Orchestrate the execution of **complete implementation plans** by delegating each phase to the `implement-phase` skill. This skill manages the full plan lifecycle.

---

## CRITICAL: Orchestrator Pattern (MANDATORY)

> **THIS SESSION IS AN ORCHESTRATOR. YOU MUST NEVER IMPLEMENT CODE DIRECTLY.**

### The Orchestration Hierarchy

```
implement-plan (this session - ORCHESTRATOR)
    │
    │   ⛔ NEVER writes code
    │   ⛔ NEVER uses Write/Edit tools
    │   ⛔ NEVER creates files
    │
    └── implement-phase (ORCHESTRATOR for phase)
            │
            │   ⛔ NEVER writes code
            │   ⛔ NEVER uses Write/Edit tools
            │   ⛔ NEVER creates files
            │
            └── Subagents (DO the actual work)
                    │
                    ✅ Write code
                    ✅ Create files
                    ✅ Run tests
                    ✅ Fix issues
```

### What This Session Does

| DO | DO NOT |
|----|--------|
| Read plan and prompts | Write code |
| Discover phase prompts | Create files |
| Invoke implement-phase skill | Use Write/Edit tools |
| Track plan-level progress | Implement directly |
| Present results to user | Fix issues directly |
| Handle user confirmation | Run implementation commands |

### Enforcement

If you find yourself about to use Write, Edit, or NotebookEdit tools in this session:

```
⛔ STOP - You are violating the orchestrator pattern
✅ INSTEAD - Delegate to implement-phase which will spawn subagents
```

---

## Architecture

```
implement-plan (this skill - plan orchestrator)
    │
    ├── Phase 1 → implement-phase → [implementation, verification, review, ADR, sync]
    │                    ↓
    │              [user confirmation]
    │                    ↓
    ├── Phase 2 → implement-phase → [implementation, verification, review, ADR, sync]
    │                    ↓
    │              [user confirmation]
    │                    ↓
    ├── Phase N → implement-phase → [...]
    │                    ↓
    └── Final Verification & Summary
```

## Responsibilities

### This Skill (implement-plan)
- Read and understand the full plan
- Sequence phases correctly
- Delegate each phase to `implement-phase`
- Handle user confirmation between phases
- Track overall plan progress
- Generate final completion report

### Delegated to implement-phase
- All implementation work
- Exit condition verification
- Code review
- ADR compliance
- Plan file synchronization

## When to Use

- Implementing pre-approved technical plans or specifications
- Executing phased development work with defined success criteria
- Following structured implementation guides with verification steps
- Resuming partially-completed implementation work

## Execution Modes

### Current Mode: Guided Execution

Each phase requires user confirmation before proceeding to the next. This is the default, safe mode.

```
Phase 1 → implement-phase → ✅ Complete → [USER CONFIRMS] → Phase 2 → ...
```

### Future Mode: Autonomous Execution

> **Note**: This mode is planned but not yet implemented. When enabled, the entire plan will execute without pauses between phases.

```
Phase 1 → Phase 2 → Phase 3 → ... → Final Report
```

Autonomous mode will require:
- Explicit user opt-in: "implement the entire plan autonomously"
- Stricter quality gates
- Comprehensive rollback capability
- Detailed execution log

## Getting Started

When given a plan path or asked to implement a plan:

### 1. Locate and Read Plan

```
1. Find the plan file (docs/plans/, thoughts/plans/, or specified path)
2. Read the ENTIRE plan - full context is essential
3. Identify total number of phases
4. Extract task_list_id from plan metadata (for multi-session support)
5. Check for existing Tasks (TaskList shows progress from previous sessions)
```

**Multi-Session Support:**
If the plan has a `task_list_id` in its metadata, ensure you're using the same task list:
```bash
CLAUDE_CODE_TASK_LIST_ID=plan-2026-01-24-feature-name claude
```
This enables multiple sessions to share progress on the same plan.

### 2. Discover Phase Prompts

Check for pre-generated prompts from the `prompt-generator` skill:

```
# Check common prompt locations
1. Glob("docs/prompts/phase-*.md")           # Standard location
2. Glob("prompts/phase-*.md")                # Alternative location

# Match prompts to phases by number
phase-1-*.md  →  Phase 1
phase-2-*.md  →  Phase 2
...
```

**Prompt Discovery Output:**
```
● Prompt Discovery:
  Found: docs/prompts/phase-1-foundation.md      → Phase 1
  Found: docs/prompts/phase-2-data-pipeline.md   → Phase 2
  Found: docs/prompts/phase-3-agent-system.md    → Phase 3
  Missing: Phase 4 (no prompt found)

  Note: Phases with prompts will use pre-generated instructions.
        Phases without prompts will use plan file directly.
```

### 3. Read Related Context

```
# Tiered ADR reading (context conservation)
1. Read("docs/decisions/INDEX.md")              # Scan all ADRs first
2. Read("docs/decisions/ADR-NNNN.md", limit=10) # Quick Reference of relevant ones
3. Read full ADR only if needed for implementation details

# Read files referenced in plan
4. Load all files mentioned in the plan
```

### 4. Check Progress via Tasks

```
# Check for existing tasks for this plan
TaskList: Check for tasks matching "Phase N:" pattern

If tasks exist:
  - Resume from first non-completed task
  - Skip already-completed phases
  - Display current progress

If no tasks exist:
  - Tasks should have been created by create-plan
  - If missing, create them now (see create-plan Phase 7)
```

**Task Status Display:**
```
Tasks (2 done, 3 open):
  ✓ #1 Phase 1: Setup
  ✓ #2 Phase 2: Core Logic
  ◻ #3 Phase 3: Integration › blocked by #2
  ◻ #4 Phase 4: Testing › blocked by #3
  ◻ #5 Phase 5: Documentation › blocked by #4
```

### 5. Begin Phase Execution

For each phase:
1. Mark task as in_progress: `TaskUpdate(task_id, status: "in_progress")`
2. Delegate to `implement-phase`
3. On completion: `TaskUpdate(task_id, status: "completed")`

```
Skill(skill="implement-phase"): Execute Phase [N] of the implementation plan.

Context:
- Plan: [plan file path]
- Phase: [N] ([Phase Name])
- Task ID: [task_id from TaskList]
- Prompt: [prompt file path, if discovered]
- Previous Phase Status: [Complete/N/A]

Execute all quality gates and return structured result.
```

**With Prompt (preferred)**:
```
Skill(skill="implement-phase"): Execute Phase 2.

Context:
- Plan: docs/plans/trading-platform.md
- Phase: 2 (Data Pipeline)
- Task ID: 2
- Prompt: docs/prompts/phase-2-data-pipeline.md
- Previous Phase Status: Complete

The prompt contains detailed orchestration instructions.
Execute all quality gates and archive prompt on completion.
```

**Without Prompt (fallback)**:
```
Skill(skill="implement-phase"): Execute Phase 4.

Context:
- Plan: docs/plans/trading-platform.md
- Phase: 4 (Integration)
- Task ID: 4
- Prompt: None (use plan directly)
- Previous Phase Status: Complete

No pre-generated prompt. Use plan file for phase details.
```

## Phase Execution Protocol

### Before Each Phase

1. **Announce** the phase about to start
2. **Summarize** what will be implemented
3. **Note** any dependencies on previous phases

```
═══════════════════════════════════════════════════════════════
● STARTING PHASE 2: Authentication Service
═══════════════════════════════════════════════════════════════

Objectives:
- Implement login/logout logic
- JWT token generation and validation

Dependencies:
- Phase 1 (Database Schema) must be complete ✅

Delegating to implement-phase...
```

### During Phase Execution

The `implement-phase` skill handles all details:
- Subagent delegation for implementation
- Exit condition verification
- Code review via `code-review` skill
- ADR compliance checking
- Plan file synchronization

### After Each Phase

Receive structured result from `implement-phase`:

```yaml
PHASE_RESULT:
  status: COMPLETE | FAILED | BLOCKED
  steps:
    implementation: PASS
    exit_conditions: PASS
    code_review: PASS_WITH_NOTES
    adr_compliance: PASS
    plan_sync: PASS
  manual_verification:
    - "Check login flow in browser"
  ready_for_next: true
```

### User Confirmation Point

After each phase completes, pause for user confirmation:

```
═══════════════════════════════════════════════════════════════
● PHASE 2 COMPLETE: Authentication Service
═══════════════════════════════════════════════════════════════

Results:
  ✅ Implementation: 3 files created, 2 modified
  ✅ Exit Conditions: All passed
  ✅ Code Review: Passed with 2 recommendations
  ✅ ADR Compliance: Passed
  ✅ Plan Updated: 8 tasks marked complete

Manual Verification Required:
  - [ ] POST /auth/login returns token with expected claims
  - [ ] POST /auth/logout invalidates session

Recommendations (non-blocking):
  1. Consider using project's CustomLogger
  2. Add ADR-0012 reference to plan

───────────────────────────────────────────────────────────────
Please confirm manual verification steps, then respond to
proceed to Phase 3: API Endpoints
═══════════════════════════════════════════════════════════════
```

## Handling Blockers

When `implement-phase` returns a blocker:

### From implement-phase

```yaml
PHASE_RESULT:
  status: BLOCKED
  blocker: "Existing JWT implementation found in src/legacy/auth.js"
  options:
    - "Proceed with new implementation"
    - "Refactor legacy code"
    - "Abort and revise plan"
```

### Orchestrator Response

1. **STOP** further phase execution
2. **PRESENT** the blocker to user with options
3. **AWAIT** user decision
4. **RESUME** or **ABORT** based on decision

```
⛔ PHASE 2 BLOCKED

Issue: Existing JWT implementation found in src/legacy/auth.js.
The plan specifies creating new jwt.strategy.ts but doesn't
mention legacy code.

Options:
A) Proceed with new implementation, mark legacy for removal
B) Refactor legacy code instead of creating new file
C) Abort and revise the plan

Recommendation: Option A - cleaner separation

How should I proceed?
```

## Resuming Interrupted Work

Tasks persist across sessions, enabling seamless resume:

1. **Call TaskList** - Get all tasks for the plan
2. **Find first non-completed task** - This is the resume point
3. **Verify state** - Quick sanity check that previous work exists
4. **Continue** - Resume from the pending task

```
● Plan Status: Resuming interrupted work

Task Status (from TaskList):
  ✓ #1 Phase 1: Database Schema - completed
  ✓ #2 Phase 2: Authentication Service - completed
  ◻ #3 Phase 3: API Endpoints - in_progress  ← Resume here
  ◻ #4 Phase 4: Testing - pending (blocked by #3)

Resume Point: Phase 3 (API Endpoints)

Continuing from Phase 3...
```

**Multi-Session Resume:**
```bash
# Start new session with same task list
CLAUDE_CODE_TASK_LIST_ID=plan-2026-01-24-user-auth claude

# Tasks automatically show current progress
# Resume from where any session left off
```

**Benefits of Task-based resume:**
- Cross-session persistence (tasks survive session restart)
- Multi-session support (share progress across terminals)
- Dependency tracking (blocked tasks visible)
- Clear audit trail of progress

## Final Completion

After all phases complete:

```
═══════════════════════════════════════════════════════════════
● PLAN COMPLETE: User Authentication Implementation
═══════════════════════════════════════════════════════════════

Summary:
  Phases Completed: 3/3
  Files Created: 12
  Files Modified: 5
  Tests Added: 47
  ADRs Created: 1 (ADR-0015)

Quality Gates (all phases):
  ✅ All exit conditions passed
  ✅ All code reviews passed
  ✅ All ADR compliance checks passed
  ✅ Plan fully synchronized

Final Verification:
  - [ ] E2E tests pass: `npm run test:e2e`
  - [ ] API documentation updated
  - [ ] Security review checklist complete

═══════════════════════════════════════════════════════════════
Implementation complete. Ready for final review.
═══════════════════════════════════════════════════════════════
```

## Progress Tracking

Progress is tracked via **Task tools** with cross-session persistence. See [ADR-0001](../../docs/decisions/ADR-0001-separate-plan-spec-from-progress-tracking.md).

| Tracking Method | Scope | Purpose |
|-----------------|-------|---------|
| TaskList/TaskUpdate | Persistent | Track phase-level progress across sessions |
| Plan File | Persistent | Specification document (updated with ✅ on completion) |
| Status Updates | User | Communicate current state |

**Task Lifecycle:**
```
create-plan → TaskCreate (all phases with dependencies)
                  ↓
implement-plan → TaskUpdate(in_progress) → implement-phase → TaskUpdate(completed)
                  ↓
Resume (any session) → TaskList (find first pending task)
```

**Multi-Session Workflow:**
```bash
# Session 1: Start implementation
CLAUDE_CODE_TASK_LIST_ID=plan-my-feature claude
> /implement-plan docs/plans/my-feature.md
# ... complete Phase 1, 2 ...

# Session 2: Resume from another terminal
CLAUDE_CODE_TASK_LIST_ID=plan-my-feature claude
> /implement-plan docs/plans/my-feature.md
# Automatically resumes from Phase 3
```

Phase-level tracking is handled by `implement-phase` using Task tools.

## Reference Materials

See `references/plan-format.md` for:
- Standard plan structure and formatting
- Phase organization guidelines
- Exit condition patterns
- Verification step templates

## Key Principles

1. **Delegate phase execution** - Use `implement-phase` for all phase work
2. **Orchestrate, don't implement** - This skill coordinates, not codes
3. **User confirmation between phases** - Pause for human validation (current mode)
4. **Trust implement-phase results** - Act on structured return values
5. **Surface blockers immediately** - Don't hide problems from the user
6. **Track at plan level** - Let implement-phase handle phase-level tracking
7. **Prepare for automation** - Structure supports future autonomous mode

## Skill Dependencies

```
implement-plan
    └── implement-phase (required)
            ├── code-review (required)
            └── adr (required for compliance)
```

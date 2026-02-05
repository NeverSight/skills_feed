---
name: hype
description: >
  Document-driven development with test-gated progression. Enforces a disciplined
  workflow: plan tasks with the user in .hype/TODO.md, document before implementing,
  track progress in .hype/PROGRESS.md, accumulate project knowledge in .hype/KNOWLEDGE.md,
  and require all tests to pass before advancing. Language-agnostic — works with any
  programming language or even non-code projects.
  Use when: (1) starting new projects with structured planning, (2) implementing features
  or bug fixes with mandatory test verification, (3) managing development tasks with
  document-based tracking, (4) the user mentions "hype", "document-driven development",
  "TODO tracking", or wants a disciplined plan-document-implement-test cycle.
---

# Hype — Document-Driven Development

Hype enforces a strict development cycle: **Plan → Document → Implement → Test → Repeat**.

All tracking documents live in `.hype/` at the project root.
**No task advances without passing verification.** This is the core invariant.

## Documents

| File | Written by | Purpose |
|------|------------|---------|
| `.hype/IDEA.md` | User (Claude appends when asked) | Freeform idea scratchpad. Not part of the hype cycle. Claude may append when the user says so (e.g., "put that in IDEA", "メモしてね"). Claude never edits or deletes existing entries. |
| `.hype/TODO.md` | Claude (with user approval) | Phase-structured task plan. The user reads this to understand what Claude will do. |
| `.hype/PROGRESS.md` | Claude | Append-only execution log. The user reads this to understand what Claude has done. |
| `.hype/KNOWLEDGE.md` | Claude | Accumulated project knowledge. Read on session restart to restore context. |

## Workflow Overview

```
INIT → PLAN (with user) → [ DOCUMENT → IMPLEMENT → TEST → UPDATE ] → COMPLETE
                               ↑                      |
                               └── fix & re-test ←────┘ (on failure)
```

## Phase 1: Initialize

1. Read `.hype/KNOWLEDGE.md` first if it exists — this restores context from previous sessions
2. Read `.hype/TODO.md` and `.hype/PROGRESS.md` if they exist — resume from where things left off
3. If starting fresh:
   - Create `.hype/` directory
   - Create `.hype/TODO.md`, `.hype/PROGRESS.md`, `.hype/KNOWLEDGE.md` using templates in [references/document-templates.md](references/document-templates.md)
   - Create `.hype/IDEA.md` only if the user requests it
4. Detect project type:
   - **Code project**: Identify language and build system from existing files. Set up the idiomatic test framework for that language if not already configured.
   - **Non-code project**: Identify the domain (writing, design, research, etc.). Verification will use review checklists instead of automated tests (see Non-Code Adaptation below).

## Phase 2: Plan (with user)

This phase is **collaborative**. Do not proceed without user confirmation.

1. If `.hype/IDEA.md` exists, read it first. Propose incorporating relevant ideas into the plan (e.g., "IDEA.md にこれがあるけど、タスクに入れる？")
2. Discuss the user's goals, constraints, and preferences
3. Break the work into **phases**, each containing discrete, verifiable tasks
3. Each task must have:
   - Clear acceptance criteria
   - A defined verification approach (test, checklist, or review)
4. Write to `.hype/TODO.md` using the phase-structured format:

```markdown
## Phase 1 — <phase name>

- [ ] P0: Task description — Acceptance: criteria — Test: approach
- [ ] P1: Task description — Acceptance: criteria — Test: approach

## Phase 2 — <phase name>

- [ ] P1: Task description — Acceptance: criteria — Test: approach
```

5. **Present the plan to the user and wait for approval**
   - Adjust tasks based on user feedback
   - Only proceed after explicit user confirmation

## Phase 3: Development Cycle

Execute for each task in order (phase by phase, priority within each phase):

### Step 1 — Document

Select the next task. Update its status to `[~]` in `.hype/TODO.md`.

Before writing any code, append a "Started" entry to `.hype/PROGRESS.md`:
- What will be implemented and how
- Expected behavior, function signatures, or API surface
- Verification cases (inputs → expected outputs)

This serves as the specification for the implementation step.

### Step 2 — Implement

Write the change based on the spec from Step 1. Keep changes focused on the single task.
If a task is larger than expected, **stop and split** it into subtasks in `.hype/TODO.md` before continuing.

### Step 3 — Test

Write or update tests, then execute the full test suite.

- Tests must cover the acceptance criteria in `.hype/TODO.md`
- At minimum: happy path, one edge case, one error case
- Use the idiomatic test framework for the project's language
- For general testing guidance, see [references/testing-workflows.md](references/testing-workflows.md)

**Gate**:
- **All tests pass** → proceed to Step 4
- **Any test fails** → diagnose, fix, re-run the full suite
- **NEVER proceed with failing tests**

### Step 4 — Update

1. Mark task `[x]` in `.hype/TODO.md`
2. Update the entry in `.hype/PROGRESS.md` with: files changed, test results, notes
3. If the task revealed reusable project knowledge (conventions, patterns, gotchas, architectural decisions), append to `.hype/KNOWLEDGE.md`
4. Communicate progress to the user
5. Return to Step 1 for the next task

## Phase 4: Complete

When all tasks in `.hype/TODO.md` are `[x]`:

1. Run the full test suite one final time
2. Append a completion summary to `.hype/PROGRESS.md`
3. Update `.hype/KNOWLEDGE.md` with any final insights
4. Report to user: tasks completed, tests passing, remaining notes

## Non-Code Adaptation

For non-code projects (writing, research, design, etc.), the cycle is the same but Step 3 adapts:

| Code project | Non-code project |
|---|---|
| Automated tests | Review checklist |
| `cargo test`, `pytest`, etc. | Manual verification against criteria |
| Pass/fail binary | Checklist all items ✅ |

Example for a novel:
```markdown
- [ ] P1: Write Chapter 3 — Acceptance: introduces antagonist, 2000-3000 words — Review: continuity with Ch.1-2, no plot holes, consistent character voice
```

The **gate** still applies: all checklist items must pass before moving on.

## Rules

1. **NEVER** skip verification. Every change requires tests or a review checklist.
2. **NEVER** mark a task `[x]` unless verification passes.
3. **ALWAYS** document before implementing.
4. **ALWAYS** update `.hype/TODO.md` and `.hype/PROGRESS.md` after each task.
5. **ALWAYS** run the full test suite, not just new tests.
6. **ALWAYS** confirm the plan with the user before starting.
7. **ALWAYS** read `.hype/KNOWLEDGE.md` at session start.
8. `.hype/TODO.md` is the single source of truth for remaining work.
9. `.hype/PROGRESS.md` is append-only — never modify existing entries.
10. `.hype/IDEA.md` is user-owned — append only when the user explicitly asks. Never edit or delete existing entries.
11. `.hype/KNOWLEDGE.md` is updated when tasks reveal reusable project knowledge.
12. If a task needs splitting, split it in `.hype/TODO.md` before implementing.
13. When the user adds a new request mid-cycle, add it as new tasks in `.hype/TODO.md` — do not abandon the current workflow.
14. Communicate current task and progress at each step boundary.
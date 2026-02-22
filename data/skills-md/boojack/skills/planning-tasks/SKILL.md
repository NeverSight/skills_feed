---
name: planning-tasks
description: Translates an approved design document into a concrete, ordered task plan with exact file paths, implementation details, code examples, and validation commands suitable for direct execution by coding agents. Use when a design document exists in docs/issues/ and executable implementation tasks are needed before coding begins.
---

# Planning Tasks

Takes `design.md` and `definition.md` from `docs/issues/YYYY-MM-DD-<slug>/` as input. Produces a task plan detailed enough for a coding agent to execute without re-deriving implementation from the design.

Does NOT introduce new design decisions, modify the design, or write complete implementations.

```
EVERY TASK MUST HAVE ALL 8 FIELDS — NO EXCEPTIONS
```

## Workflow

```
- [ ] Step 1: Load Inputs
- [ ] Step 2: Explore Codebase
- [ ] Step 3: Break Design into Tasks
- [ ] Step 4: Order Tasks & Dependencies
- [ ] Step 5: Out-of-Scope Tasks
- [ ] Step 6: Open Execution Questions
- [ ] Step 7: Readiness Declaration
- [ ] Step 8: Validate
```

### Step 1: Load Inputs

Read `design.md` and `definition.md` from the issue folder. Extract: design goals, non-goals, proposed design, current state.

### Step 2: Explore Codebase

- Read files referenced in issue definition's current state
- Identify patterns, naming conventions, testing style
- Locate exact insertion points for new code

No output section — ensures tasks reference real paths and patterns.

### Step 3: Break Design into Tasks

Start **## Task List** with a **Task Index** — one line per task:

> `T1: Add timing instrumentation [S] — T2: Refactor task queue [M] — T3: Add action selector [L]`

Each task MUST use this exact format:

```
### T<N>: <short imperative title> [S|M|L]

**Objective**: One outcome, traceable to a design element.
**Size**: S (single file, <30 lines) | M (2-3 files, moderate logic) | L (multiple files, complex state/logic)
**Files**:
- Create: `exact/path/to/new_file.ts`
- Modify: `exact/path/to/existing.ts`
- Test: `tests/path/to/test.test.ts`
**Implementation**:
1. In `path/to/file.ts`: add import X, modify `functionName()` to do Z
2. In `tests/path/to/test.test.ts`: test "should X" — assert Y
**Boundaries**: What this task must NOT do
**Dependencies**: T<N> | None
**Expected Outcome**: Observable result (file exists, test passes, etc.)
**Validation**: `exact command` — expected output
```

**Code detail guidance:**
- ✓ Interfaces, type definitions, function signatures
- ✓ Key logic as pseudocode or commented outline
- ❌ Complete function bodies
- ❌ Complete test implementations

All tasks must have the same depth of specificity. If a task requires the executing agent to choose between approaches, resolve the choice or flag it in Open Execution Questions.

### Step 4: Order Tasks & Dependencies

Explain sequencing rationale. Identify parallel vs sequential tasks.

### Step 5: Out-of-Scope Tasks

List tasks that might be assumed necessary but are excluded. Reference design non-goals.

### Step 6: Open Execution Questions

List execution uncertainties (tooling, environment, access). Do NOT resolve — only list. Write "No open execution questions identified." if none.

### Step 7: Readiness Declaration

Exactly one: **Ready for execution** | **Blocked pending clarification** | **Requires design update**

### Step 8: Validate

| Check | Criteria |
|---|---|
| Task fields | All 8 fields present on every task |
| Task Index | Present at top of Task List |
| Implementation | Specific changes per file, signatures complete, bodies are outlines |
| Traceability | Every task traces to proposed design |
| Outcomes | No vague outcomes ("improved", "refactored") |
| Validation | Exact commands with expected output |
| File paths | Match actual codebase (from Step 2) |
| Consistency | No task significantly vaguer than others |
| Decisions | No embedded design decisions — resolve or flag in Open Execution Questions |

If any check fails, return to the failing step and revise.

## Output

Save to `docs/issues/YYYY-MM-DD-<slug>/plan.md`.

```markdown
## Task List

## Task Ordering Rationale

## Out-of-Scope Tasks

## Open Execution Questions

## Readiness Declaration
```

Missing any section invalidates the output.

## Anti-patterns

- ❌ 50-line function body → ✓ signature + outline
- ❌ Full test code → ✓ test descriptions with expected assertions
- ❌ "Update the function" → ✓ "In `executeTask()` (~line 45), add X"
- ❌ No goal reference → ✓ "Objective: ... (design goal #1)"
- ❌ "Either add new RPC or extend existing" → ✓ pick one or flag
- ❌ T1 has exact insertion points, T8 says "add component" → ✓ same depth

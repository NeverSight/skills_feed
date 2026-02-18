---
name: specalign
description: Align spec files with implementation. Detects drift between spec and code, surfaces discrepancies, user decides whether to update spec or code. Use when both a spec file and its implementation are in context.
---

# Spec Alignment

## Principles (Always Active)

These apply whenever a spec file and its corresponding implementation are both in context:

### Spec and Code Must Agree

- A spec describes intended behavior; code implements it. When they disagree, one is wrong.
- Never silently tolerate drift - surface it immediately when noticed.
- The user decides which is the source of truth for each discrepancy. Do not assume.

### Drift Categories

- **Type drift**: spec defines fields/types that don't match the implementation
- **Behavior drift**: spec describes logic the code doesn't follow
- **Missing implementation**: spec defines something with no corresponding code
- **Missing spec**: code implements behavior not described in the spec
- **Constraint drift**: spec states invariants the code doesn't enforce
- **Error handling drift**: spec defines error cases the code doesn't handle (or vice versa)

### Mutation Policy

- Do not edit spec files unless the user explicitly chooses "update spec" for a discrepancy.
- Do not change implementation logic unless the user explicitly chooses "update code".
- When updating code, run lint/typecheck after changes.
- When updating spec, preserve formatting and structure of unrelated sections.

### Bidirectional Awareness

When reading code, check if a spec exists and note divergences.
When reading a spec, check if the implementation matches and note divergences.
This awareness should be passive - flag drift in your responses without interrupting the user's primary task, unless the drift is directly relevant.

## Workflow (When Explicitly Aligning)

### Step 1: Locate the Spec

A spec file is required. Search for:
- `*.spec.md`, `*-spec.md`, `SPEC.md`
- `spec/*.md`, `docs/*.spec.md`

If multiple specs exist, ask which to align. If none exist, stop - this workflow requires an existing spec.

Read the spec file completely.

### Step 2: Map Spec to Code

For each spec section, identify the corresponding implementation:

| Spec Section | Source File(s) | Status |
|---|---|---|
| `## Types` | `src/types.ts:10-40` | aligned / drifted / missing-impl / missing-spec |

Read each mapped source file before assessing.

### Step 3: Present Discrepancies

For each discrepancy:

```
### DRIFT-01: <short description>

**Spec says** (spec-file.md:L42):
> <quoted spec text>

**Code does** (src/module.ts:L87):
> <summarized code behavior>

**Impact**: <what breaks or is inconsistent>
```

Number with stable IDs (`DRIFT-NN`). Batch related discrepancies that share a root cause.

### Step 4: User Decision

For each discrepancy, ask:

- **Update spec** - the code is correct, update the spec to match
- **Update code** - the spec is correct, update the code to match
- **Skip** - defer this discrepancy

### Step 5: Apply Changes

**Spec updates:**
- Edit the spec file with corrected text
- Preserve formatting and structure of unrelated sections

**Code updates:**
- Fix the implementation to match the spec
- Run lint/typecheck after changes
- If non-trivial, outline the change and confirm before editing
- If unit tests exist for the affected code, run them
- If unit tests don't exist and the spec defines testable behavior, flag it

### Step 6: Summary

```
## Spec Alignment: <file>

**Discrepancies found**: N
**Resolved**: X (spec: A, code: B, skipped: C)

### Remaining
- DRIFT-04: <description> (skipped)
```

---
name: sdd-refine
description: >
  SDD step 2 (optional, repeatable). Read an existing feature.md and refine it by updating or
  enhancing requirements based on user input. Use when requirements have changed,
  new edge cases are discovered, or the spec needs clarification before planning
  or re-planning. Run before /sdd-plan if plan.md already exists.
argument-hint: <what to change or enhance (optional)>
---

# SDD: Refine Feature Spec

You are a senior software architect refining an existing feature specification.

## Inputs

| Input                | Required | Description                       | Example                                               |
|----------------------|----------|-----------------------------------|-------------------------------------------------------|
| `refinement_request` | Optional | What to change or add to the spec | "Add rate limiting — max 5 login attempts per minute" |

## Steps

### Step 0: Validate Inputs (ALWAYS DO THIS FIRST)

Check the conversation for `refinement_request` and for `feature.md` in the project root.

- If `feature.md` does not exist → stop and tell the user to run `/sdd-feature` first.
- If `refinement_request` is present → proceed to Step 1.
- If `refinement_request` is missing → ask:
  > "What would you like to change or add to the spec? Is this a scope change, a clarification, or new edge cases?"
  Do NOT proceed until the user provides it.

---

## Pre-conditions
Verify `feature.md` exists in the project root.
If it does not exist, tell the user to run `/sdd-feature` first.

### 1. Read Current State
Read these files before doing anything:
- `feature.md` — the existing spec to be refined
- `docs/project.md` — project context and constraints
- `plan.md` — if it exists, note which parts of the plan may be invalidated by changes

### 2. Understand the Refinement Request
The refinement input is: **`refinement_request`** (collected in Step 0).

Analyse `refinement_request` against the current `feature.md` and identify:
- What sections are affected
- Whether the change expands scope, reduces scope, or clarifies existing scope
- Any knock-on effects (e.g., changing a requirement may invalidate other ACs)

### 3. Ask Clarifying Questions if Needed
If the refinement request is ambiguous or incomplete, ask targeted questions before editing.
Keep questions to 3 or fewer. Wait for answers.

### 4. Show a Diff Summary Before Editing
Before modifying the file, present a brief plan of changes:

```
## Proposed Changes to feature.md

### Additions
- FR-04: <new requirement>
- AC-05: <new acceptance criterion>

### Modifications
- FR-02: Updated to clarify that X also applies to Y
- AC-02: Strengthened — must complete within 200ms, not 500ms

### Removals
- FR-03: Removed — out of scope per user confirmation

### No Change
- All other sections remain as-is
```

Ask the user to confirm before applying.

### 5. Apply the Refinements
Update `feature.md` in place. Preserve:
- Existing section structure and numbering where possible
- Completed checkboxes on ACs if any exist
- The `## Open Questions` section — resolve any questions answered by this refinement,
  and add new ones if this refinement raises them

Increment requirement IDs sequentially (do not reuse deleted IDs).

### 6. Impact Assessment
After updating `feature.md`, check if `plan.md` exists.
If it does, analyse the impact:

```
## Impact on plan.md

plan.md exists and may be partially invalidated. Here is what needs revisiting:

- Step 2 (Domain Layer): FR-04 adds a new value object not currently planned
- Step 6 (Tests): 2 new ACs require additional test cases
- Step 3 is unaffected

Recommendation: Run /sdd-plan again to regenerate the plan before implementing.
```

If `plan.md` does not exist, simply confirm the spec is updated and prompt the user to run `/sdd-plan`.

### 7. Changelog Entry
Append a refinement record at the bottom of `feature.md`:

```markdown
---

## Revision History

| Date | Change Summary |
|------|----------------|
| <date> | Initial spec |
| <date> | <One-line summary of this refinement> |
```

If a revision history table already exists, append a new row — do not recreate the table.

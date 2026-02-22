---
name: defining-issues
description: Converts vague natural-language requests into precise, grounded engineering issue definitions with background, issue statement, current state, non-goals, and open questions. Use when an issue needs to be clarified, scoped, or prepared before research or design work begins — such as unclear requirements, vague feature requests, ambiguous bug reports, or undefined scope boundaries.
---

# Defining Issues

Does NOT propose solutions, design systems, or suggest architectures. Output is an issue definition only.

```
NO SOLUTION LANGUAGE — DEFINE THE PROBLEM, NOT THE FIX
```

## Workflow

```
- [ ] Step 1: Background & Context
- [ ] Step 2: Issue Statement
- [ ] Step 3: Current State
- [ ] Step 4: Non-Goals
- [ ] Step 5: Open Questions
- [ ] Step 6: Validate
```

### Step 1: Background & Context

- Describe the domain, system, or user scenario
- Include history or prior attempts if known
- Keep factual — no editorializing or solution advocacy

### Step 2: Issue Statement

- Precise engineering language and codebase terminology
- No subjective, aspirational, or solution-proposing language
- Single paragraph

### Step 3: Current State

- List exact file paths (verify with `Glob` or `Read`)
- Include line numbers for specific functions or definitions
- Describe current behavior, not desired behavior
- If section exceeds 30 lines, summarize and move details to a reference appendix
- If nothing relevant exists: "No existing implementation found."

### Step 4: Non-Goals

When in doubt, mark it a non-goal.

- What is explicitly out of scope
- What parts of the system must NOT be redesigned
- What adjacent issues are intentionally excluded

### Step 5: Open Questions

Each item must include a default so downstream work can proceed.

Format: `Question? (default: answer)`

### Step 6: Validate

| Check | Criteria |
|---|---|
| Background & Context | Factual, no editorializing or solution advocacy |
| Issue Statement | Precise, single paragraph, no solution words ("should", "need to", "by adding X") |
| Current State | Real file paths verified with `Glob`/`Read`, current behavior only |
| Non-Goals | Specific exclusions, conservative scope |
| Open Questions | Each has a `(default: answer)` |

If any check fails, return to the failing step and revise.

## Output

Save to `docs/issues/YYYY-MM-DD-<slug>/definition.md`. Create the folder if it doesn't exist.

```markdown
## Background & Context

## Issue Statement

## Current State

## Non-Goals

## Open Questions
```

Missing any section invalidates the output.

## Anti-patterns

- ❌ "We need to add X" → ✓ "No X exists"
- ❌ Listing systems not affected → ✓ only code paths exhibiting the issue
- ❌ "Not changing unrelated code" → ✓ specific exclusions
- ❌ "Should we log?" → ✓ "Should we log? (default: no)"

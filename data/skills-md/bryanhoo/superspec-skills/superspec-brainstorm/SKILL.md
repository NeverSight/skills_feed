---
name: superspec-brainstorm
description: Use when a Superspec change is underspecified and you need to clarify intent, scope, constraints, affected specs, and success criteria before writing proposal/specs.
user-invocable: false
---

# Superspec Brainstorm

## Overview

Turn a vague change request into proposal-ready inputs plus a small, validated "design seed" (still at proposal/specs level, not implementation).

## Rules (non-negotiable)

- Ask EXACTLY ONE question per message.
- Do not combine two questions into one message (even if short).
- Prefer multiple-choice options when possible.
- Do NOT run `openspec` commands.
- If you need more context, ask the user to paste relevant JSON/text or provide file paths; do not run commands to fetch it.
- Do NOT write or modify any files. Output is working notes only.
- Stay within proposal/specs scope; avoid implementation details (no file/module lists, no concrete code, no micro-optimizations).

## Process

### A) Understand the idea (questions, one at a time)

1. Start by asking for context if missing (pick 1-3): relevant file paths, existing specs, API contracts, user stories, current behavior examples.
2. Ask questions ONE PER MESSAGE to fill the "Proposal-ready Notes" (match `proposal.md` headings) in this order:
   - Intent
   - Background
   - Scope (in/out)
   - Constraints
   - Affected Specs (New/Modified; names decided; kebab-case)
   - Success Criteria
   - Risks & Mitigations (only if real)

### B) Explore approaches (2-3 options with trade-offs)

Once Notes are concrete (especially constraints + success criteria), propose 2-3 approaches.

- Lead with the recommended approach and explain why.
- Keep options at the behavior/contract level (what changes, trade-offs, risks).
- Do not turn this into a detailed implementation plan.

### C) Present the design seed (incremental validation)

If the change is non-trivial, write the "Design Seed" in 200-300 word sections.

- Post ONE section per message.
- After the section, ask exactly ONE question: "Does this look right so far?" and STOP.
- Only proceed after the user confirms or corrects.

### D) Stop / handoff

Stop when:

- Notes are concrete, AND
- An approach is selected (or explicitly deferred), AND
- Either the design seed is validated or explicitly skipped.

Handoff guidance:

- The "Proposal-ready Notes" block is intended to be copied into `proposal.md` verbatim.
- "Affected Specs" names drive concrete delta spec files at `specs/<kebab-name>/spec.md`.

## Output Contract

Maintain and update this block as you go.

```markdown
## Brainstorming Output

### 1) Proposal-ready Notes (paste into proposal.md verbatim)

## Intent

- ...

## Background

- ...

## Scope

### In scope

- ...

### Out of scope

- ...

## Constraints

- ...

## Affected Specs

### New capabilities

- `<name>`: ...

### Modified capabilities

- `<existing-name>`: ...

## Success Criteria

- ...

## Risks & Mitigations

- Risk: ...
  Mitigation: ...

### 2) Approaches (2-3 options, REQUIRED)

Option A (Recommended): <name>

- What changes (behavior/contract): ...
- Pros: ...
- Cons / trade-offs: ...
- Risks: ...

Option B: <name>

- What changes (behavior/contract): ...
- Pros: ...
- Cons / trade-offs: ...
- Risks: ...

Option C (optional): <name>

- ...

### 3) Design Seed (optional but recommended)

Section 1 (Architecture / Components) [200-300 words]
...

Section 2 (Data / Control Flow) [200-300 words]
...

Section 3 (Error Handling / Testing) [200-300 words]
...

### 4) Open Questions (if any)

- ...
```

## Common mistakes

- Stopping after notes without exploring approaches.
- Providing only one approach (no trade-offs).
- Mixing multiple questions into one message.
- Turning design seed into implementation details.
- Running `openspec` or writing files during brainstorming.

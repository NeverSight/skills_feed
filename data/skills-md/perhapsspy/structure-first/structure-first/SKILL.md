---
name: structure-first
description: Readable primary-flow–first code structuring with minimal boundaries, atomic composition, and contract-driven unit tests
license: MIT
metadata:
  author: perhapsspy@gmail.com
  version: '1.0'
  source_repository: https://github.com/perhapsspy/structure-first
---

# Skill: Structure First

## Purpose

> **Primary Flow**: the top-down readable main path that orchestrates the logic

When generating, refactoring, or reviewing code, prioritize a **readable success path (Primary Flow)** first.
Keep boundaries minimal (only when needed), compose with **role-fixed Atoms**, and secure stability through
**contract-driven tests** rather than implementation-following tests.

## When to Use

- When code does not read naturally from top to bottom
- When function/module splitting becomes excessive and utilities start to spread
- When tests are drifting toward implementation-following patterns

## Do Not Use

- Throwaway experiments or one-off exploratory code
- Tiny changes where structural intervention would be excessive

## Priorities (Bias)

- Readable flow > structural simplicity > reusability > abstraction
- Prefer **clarity of the current code** over speculative future needs
- Splitting is not a goal; split only when it improves readability

## Work Routine

1. **Fix Intent**

- State the intent of the change/code in one sentence.

2. **Minimize Boundaries**

- Classify steps as I/O, domain decision, or transform.
- Do not add more boundaries than necessary.

3. **Primary Flow First**

- Make the success path readable in one top-down pass.
- Keep branches/exceptions from breaking the main flow (early return or push downward).

4. **Extract Atoms**

- Split when a Primary Flow sentence becomes clearer as a function.
- Atoms must have fixed roles and clear I/O.
- Prefer pure functions when possible.

5. **Single Composition Point**

- Keep orchestration in one place.
- Minimize direct dependencies/calls between Atoms.

6. **Push Side Effects to Boundaries**

- Gather side effects (I/O, state mutation) at boundaries.
- Keep inner logic focused on computation and decisions.

7. **Align Read Order**

- Order code as: export/public -> orchestrator -> atoms -> utils.

## Test Guidance (Unit tests for Atoms)

- Write **sufficient unit tests at Atom level** whenever possible.
- Validate **contracts (I/O, invariants, edge cases)**, not internals.
- Test code should remain readable:
  - Use `each`/table cases to reduce duplication.
  - Small helpers/factories are fine, but stop when they blur structure.
  - Each test should expose one core assertion.

## Stop Rules / Anti‑patterns

- If splitting increases argument/state passing, roll it back.
- Do not split functions/files for appearance only (avoid utility sprawl).
- If names start turning into long explanations, re-check boundaries.
- Avoid adding abstractions/layers for assumed future reuse.
- Avoid over-abstracted tests and helper sprawl.

## Output Expectations

- Intent: (1 line)
- Primary Flow: (top-down flow)
- Boundaries: (I/O / domain / transform)
- Atoms: (name + I/O)
- Tests: (contract + edge cases, table cases)
- Changes: (targeted changes that improve readable flow)

## Final Gates

- Can the success path be seen in one top-down read?
- Does splitting reflect real responsibility/boundary changes?
- Can each Atom's I/O be explained in one line?
- Are side effects concentrated at boundaries?
- Are tests contract-focused and concise?

## Completion Evidence

Before declaring completion, provide these three lines:

- `Primary Flow:` top-down in 3-6 lines
- `Boundaries:` list of I/O boundaries
- `Tests:` contract/edge-case summary

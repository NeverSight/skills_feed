---
name: refactor
description: Use when refactoring existing code to improve readability, maintainability, and structure (rename/extract/inline, reduce complexity, remove duplication, improve type safety) while preserving external behavior and public APIs.
---

# Refactor (Behavior-Preserving)

## Goal

Improve internal structure without changing observable behavior.

Observable behavior includes outputs, side effects, performance envelopes, error shapes, logging/metrics contracts, and public API compatibility.

## Guardrails

- Preserve semantics first; readability second.
- Keep changes small and mechanical; verify after each step.
- Do not mix refactors with feature changes in the same diff.
- Prefer compiler/typechecker + tests as the safety net.

If the code has no tests, start by adding characterization tests around the current behavior (including edge cases and error paths).

## Workflow

1. Establish a baseline.
   - Run existing tests and record what passes/fails.
   - Capture key behaviors with a quick harness if tests are missing.
   - Make a checkpoint commit before refactoring.

2. Pick a single refactor target.
   - Choose the smallest change that reduces future risk.
   - State the intent in one sentence (example: "Extract parsing from IO to enable unit tests").

3. Refactor in tight loops.
   - Apply one operation (rename, extract, inline, move).
   - Re-run the relevant tests or checks.
   - Repeat until the target improvement is achieved.

4. Confirm "no behavior change".
   - All tests pass.
   - No unintended public API changes.
   - No new side effects or missing side effects.

5. Clean up.
   - Remove dead code introduced by the move.
   - Update comments that describe outdated structure.
   - Leave a small, reviewable diff.

## Common Moves

- Rename for intent (types, functions, variables).
- Extract function/method to reduce nesting and isolate responsibilities.
- Inline trivial wrappers that add indirection without value.
- Introduce parameter object when argument lists grow.
- Replace nested conditionals with guard clauses.
- Extract shared logic to eliminate duplication.
- Split large modules by responsibility and boundary.

## References (Load As Needed)

- `refactor/references/checklists.md`: safe workflow, review checklist, and "no tests" strategy.
- `refactor/references/recipes.md`: code smells mapped to refactor recipes with small examples.
- `refactor/references/operations.md`: quick list of common refactoring operations.
- `refactor/references/patterns.md`: type-safety refactors and when to use design patterns during a refactor.

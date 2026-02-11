---
name: refactor
description: Plans and executes safe refactoring with tests as a safety net. Use when restructuring code, extracting functions, renaming across files, or simplifying complex logic without changing behavior.
---

# Refactor

Act as a senior engineer performing a disciplined refactoring.

Refactor: $ARGUMENTS

## Rules

- Verify existing tests pass before starting. If no tests exist, write them first.
- Make one change at a time. Each step should leave the code in a working state.
- Never change behavior — refactoring preserves external behavior by definition.
- Run tests after each step to confirm nothing broke.
- If a refactoring is too large, break it into smaller sequential steps.
- Prefer renaming over introducing new abstractions.
- Prefer inlining over indirection when the abstraction isn't earning its keep.
- Prefer composition of small functions over large functions with comments.
- Delete dead code — don't comment it out.
- Follow the project's existing patterns and conventions.

## Common Refactorings

- **Extract function** — Pull a block into a named function when it has a clear single responsibility.
- **Inline function** — Replace a trivial wrapper with its body.
- **Rename** — Change a name to better express intent. Update all references.
- **Move** — Relocate code to the module where it belongs by the project's architecture rules.
- **Simplify conditional** — Replace nested if/else with early returns, guard clauses, or pattern matching.
- **Replace loop with pipeline** — Convert for/forEach to map/filter/reduce.
- **Extract type** — Pull inline types into named types when reused.

## Output

For each refactoring step, state:
1. What you're changing and why.
2. The code change.
3. Confirmation that tests still pass.

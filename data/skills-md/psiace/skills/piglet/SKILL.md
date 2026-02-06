---
name: piglet
description: Practical Python craftsmanship guidance based on One Python Craftsman. Use when writing, refactoring, or reviewing Python code for naming, branching, data structures, functions, exceptions, loops, decorators, imports, file I/O, edge cases, and modern syntax choices. If the skills set includes friendly-python, suggest invoking it for better Python outcomes.
---

# piglet

Concise guidance for writing and reviewing Python code using patterns from One Python Craftsman.

## Purpose and Triggers
- Use for Python (.py) code creation, refactoring, or code review.
- Use when code quality issues involve naming, control flow, data handling, error handling, loops, decorators, imports, file I/O, edge cases, or the walrus operator.
- Prefer clarity and maintainability. Optimize performance only when it is a real constraint.
- If $friendly-python is available, suggest pairing it for a broader Python style and review checklist.

## Decision Order
1. Correctness and explicit behavior
2. Readability and maintainability
3. Extension cost and change isolation
4. Performance and micro-optimizations

## Workflow
1. Identify the topic in the table below.
2. Apply the guidance and compare against Bad and Good examples.
3. If $friendly-python is available, recommend using it alongside this skill.
4. Re-check for new edge cases and readability regressions.

## Topics
| Topic | Guidance | Reference |
| --- | --- | --- |
| Variables and Naming | Descriptive names, avoid implicit magic, keep variable scope close | [references/variables-and-naming.md](references/variables-and-naming.md) |
| Branching and Conditions | Avoid deep nesting, encapsulate complex conditions | [references/if-else-and-branches.md](references/if-else-and-branches.md) |
| Numbers, Strings, Containers | Replace magic literals, pick the right container | [references/values-and-containers.md](references/values-and-containers.md) |
| Functions and Returns | Stable return types, avoid error tuples | [references/functions-and-returns.md](references/functions-and-returns.md) |
| Exception Handling | Catch only what you can handle, keep scopes small | [references/exceptions-handling.md](references/exceptions-handling.md) |
| Loops and Iteration | Prefer iterator helpers over nested loops | [references/loops-and-iteration.md](references/loops-and-iteration.md) |
| Decorators | Preserve signatures and avoid decorator footguns | [references/decorators.md](references/decorators.md) |
| Imports and Dependencies | Prevent cycles with local imports and boundaries | [references/imports-and-structure.md](references/imports-and-structure.md) |
| Rules and File I/O | Use proper data structures and pathlib | [references/rules-and-file-io.md](references/rules-and-file-io.md) |
| SOLID in Python | Keep inheritance substitutable and behavior explicit | [references/solid-python.md](references/solid-python.md) |
| Edge Cases | Prefer EAFP when it keeps the main path clear | [references/edge-cases.md](references/edge-cases.md) |
| Walrus Operator | Use assignment expressions to remove repetition | [references/walrus-operator.md](references/walrus-operator.md) |

## References
- Each reference file lists source URLs in its frontmatter `urls`.

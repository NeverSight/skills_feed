---
name: friendly-python
description: Practical guidance for writing, refactoring, and reviewing friendly Python code with a Pythonic, readable, and maintainable style.
---

# friendly-python

Concise guidance for writing friendly Python code that is clear, maintainable, and easy to extend.

## Purpose and Triggers

- Use when writing new code, refactoring, reviewing, or designing public APIs/CLIs.
- Prefer clarity and maintainability over micro-optimizations.
- Python or files with `.py`.

## Decision Order

1. Correctness and clear boundaries
2. Readability and maintainability
3. Extensibility and evolution cost
4. Performance and optimization

## Workflow

1. Locate the relevant topic below.
2. Apply the guidance and examples.
3. Review against [references/review-checklist.md](references/review-checklist.md).

## Topics

| Topic | Guidance | Reference |
| --- | --- | --- |
| Principles | Correctness first, clarity next, performance last | [references/principles.md](references/principles.md) |
| Error Handling | Catch only what you can handle; preserve context | [references/error-handling.md](references/error-handling.md) |
| API Design | Defaults and a simple entry point; hide internal wiring | [references/api-design.md](references/api-design.md) |
| Extension Architecture | Centralize extension points and change locations | [references/extension-architecture.md](references/extension-architecture.md) |
| OOP Design | Clear constructors; avoid mode switches in `__init__` | [references/oop-design.md](references/oop-design.md) |
| Reuse & Composition | Prefer thin wrappers and composition | [references/reuse-composition.md](references/reuse-composition.md) |
| Portability & Pythonic | Avoid copying other language patterns; be Pythonic | [references/portability-pythonic.md](references/portability-pythonic.md) |
| CLI Argparse | Separate parsing from execution; structure subcommands | [references/cli-argparse.md](references/cli-argparse.md) |
| Review | Review checklist for code quality | [references/review-checklist.md](references/review-checklist.md) |

## References

- Each topic file lists source URLs in its frontmatter `urls`.

---
name: fast-rust
description: Practical guidance for writing, refactoring, and reviewing fast, reliable, and maintainable Rust code.
---

# fast-rust

Concise guidance for high-quality Rust engineering, balancing correctness, maintainability, and performance.

## Purpose and Triggers

- Writing new code, refactoring, reviewing, or designing public APIs/CLIs.
- Rust or files with `.rs`.
- Prefer clear boundaries, error semantics, and evolvability.

## Decision Order

1. Correctness and clear boundaries
2. Readability and maintainability
3. Extensibility and evolution cost
4. Performance and optimization

## Workflow

1. Locate the relevant topic below.
2. Apply the guidance and examples.
3. Read the reference if you need more detail.

## Topics

| Topic | Guidance | Reference |
| --- | --- | --- |
| Error Design | Design error boundaries and semantics before propagation | [references/error-design.md](references/error-design.md) |
| Compilation | Optimize build time and release performance with measured changes | [references/compilation-optimization.md](references/compilation-optimization.md) |
| Type Exercise | Type-level exercise for expression engines and dispatch | [references/type-exercise.md](references/type-exercise.md) |

## References

- Each topic file lists source URLs in frontmatter `urls`.

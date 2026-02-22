---
name: modular-go
description: Practical guidance for Go package design with minimal public APIs, single-responsibility boundaries, stateless-first flow, one-way state transitions, and orchestration-to-capability separation. Use when creating, refactoring, or reviewing Go architecture, package boundaries, interfaces, handlers, managers, builders, and execution flows.
---

# modular-go

Concise guidance for designing Go packages that stay small, focused, and easy to evolve.

## Purpose and Triggers

- Use for Go package design, refactoring, and code review.
- Focus on API boundaries, state modeling, and flow decomposition.
- Use when deciding the right abstraction level: local helper, utility package, manager, or builder.
- Prefer explicit boundaries over convenience exports.

## Decision Order

1. Keep public surface minimal and intentional.
2. One package, one responsibility.
3. Prefer stateless functions; if state is needed, keep transitions one-way.
4. Separate orchestration from capability methods; keep handlers thin and I/O-focused.
5. Expose extra public symbols only as stable domain contracts.
6. Choose the smallest useful abstraction (`xxxutil`, `XXXManager`, `Builder`) based on reuse, lifecycle, and parameter complexity.
7. Prefer context-driven lifecycle control; expose `Close()` only for external contracts.

## Workflow

1. Define one package responsibility.
2. Expose one obvious primary entry point (type, interface, or function).
3. Keep helpers local by default; extract to `xxxutil` only for real cross-package reuse.
4. Keep transport handlers focused on protocol mapping and delegate behavior to injected dependencies.
5. Compose orchestration from focused functions, with short stage-intent comments.
6. Re-check against the reference checklists before merge.

## Topics

| Topic | Guidance | Reference |
| --- | --- | --- |
| Module Boundary | Expose minimal API and separate deep vs wide interfaces | [references/module-boundary.md](references/module-boundary.md) |
| State Flow | Use stateless functions and one-shot state objects | [references/state-flow.md](references/state-flow.md) |
| Orchestration | Use a single public executor and internal helpers | [references/orchestration.md](references/orchestration.md) |
| Review Checklist | Run a fast architecture sanity check before merge | [references/review-checklist.md](references/review-checklist.md) |

## References

- Reference files are intentionally short and task-focused.
- Source links are listed in each reference file frontmatter `urls`.

---
name: shared-kernel
description: Shared kernel rules for src/app/shared, defining what can be shared safely (primitives, utilities, UI atoms) and what must not (business logic, cross-context policies); use when adding shared helpers or components.
---

# Shared Kernel

## Intent
Provide safe, low-coupling primitives reused across bounded contexts.

## Allowed Content
- Pure utilities (formatting, small helpers) with no side effects.
- Shared UI atoms/molecules that do not contain business rules.
- Cross-cutting technical helpers (logging adapters, error wrappers) when they do not introduce new dependencies.

## Forbidden Content
- Business logic, policies, or workflow orchestration.
- Cross-capability state stores.
- Domain rules that belong to a specific bounded context.
- Direct platform SDK usage (Firebase/HTTP) unless the shared item is explicitly an infrastructure primitive and the dependency direction is preserved.

## Dependency Discipline
- Keep dependencies stable and minimal.
- Avoid importing capability modules into shared.

## API Design
- Prefer small, intention-revealing APIs.
- Avoid "god" utility modules; create focused files.

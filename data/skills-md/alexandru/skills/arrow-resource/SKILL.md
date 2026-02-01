---
name: arrow-resource
description: Kotlin + Arrow Resource lifecycle management with `Resource`, `ResourceScope`, and `resourceScope`. Use for designing safe acquisition/release of files, streams, DB pools/connections, HTTP clients, or multipart parts; composing resources (including parallel acquisition); or integrating Resource with typed errors and cancellation.
---

# Arrow Resource (Kotlin)

## Quick start
- Use `resourceScope { ... }` at lifecycle boundaries.
- Define each resource with `resource { install(acquire) { a, exitCase -> release } }`.
- Compose with `.bind()`; use `parZip` for independent parallel acquisition.
- Read `references/resource.md` for patterns and concrete examples.

## Workflow
1. Identify the acquire step and the release step.
2. Implement a `Resource<A>` using `install`.
3. Create reusable constructors on `ResourceScope` when needed.
4. Compose resources into higher-level resources with `.bind()`.
5. Execute in `resourceScope` and keep finalizers idempotent.

## Usage guidance
- Prefer Resource over `use`/`try/finally` when you need suspend finalizers or MPP support.
- Use `ExitCase` to handle rollback/cleanup differences.
- When mixing with typed errors, pick nesting order deliberately to control `ExitCase` seen by finalizers.

## References
- Load `references/resource.md` for API details and end-to-end examples.

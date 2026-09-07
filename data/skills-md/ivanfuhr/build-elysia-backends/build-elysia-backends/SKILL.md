---
name: build-elysia-backends
description: Design, scaffold, implement, or review simple modular backends built with Bun, Elysia, TypeScript, and Drizzle ORM. Use for Elysia backend architecture, module structure, dependency containers, rich domain entities, factories, isolated use cases, HTTP routes and schemas, Drizzle persistence and migrations, or colocated unit, HTTP, and integration tests.
---

# Build Elysia Backends

Build Elysia backends with strong developer experience, explicit dependencies, rich domain models, and tests close to the code they verify. Keep the architecture proportional to a simple modular application.

## Core conventions

- Organize business capabilities under `src/modules/<module>`.
- Let each module own its `container.ts`, entities, factories, use cases, persistence, HTTP code, and tests.
- Compose module containers in `src/container.ts` as a plain typed object. Do not use tokens, decorators, reflection, or service-location inside business code.
- Pass only required dependencies to routes and use cases.
- Keep entities rich: protect invariants, expose behaviors instead of public setters, and use named construction or restoration methods.
- Use factories when new entities require clocks, ID generators, hashers, or other external values.
- Keep each use case in its own directory with its test beside it.
- Keep Elysia-specific schemas and handlers under `http`; never place routes inside use-case directories.
- Keep Drizzle schemas and repositories under the owning module's `persistence` directory.
- Keep generated migrations in the root `drizzle/` directory because migration order belongs to the database as a whole.
- Import concrete files directly. Do not create barrel files.
- Do not introduce `shared`, `foundation`, `common`, `ports`, or `adapters` directories by default.
- Create a directory or abstraction only when it has a concrete responsibility in the current application.

## Workflow

1. Inspect the existing repository and preserve its conventions when they do not conflict with the user's explicit choices.
2. Identify business modules and their operations.
3. Define rich entities and value objects before persistence mappings when business invariants exist.
4. Implement one independently testable use case per operation.
5. Build module-local repositories and Drizzle schemas.
6. Build Elysia routes that validate HTTP input, invoke one use case, and map its result to HTTP.
7. Build each module's typed dependency map in its `container.ts` and aggregate those maps in the root container.
8. Add tests beside entities, factories, use cases, routes, and repositories.
9. Generate and inspect SQL migrations when schema declarations change.
10. Run the smallest relevant tests first, then the full test and type-check commands.

## Load detailed guidance

- For the canonical tree, ownership rules, naming, and dependency direction, read [references/architecture.md](references/architecture.md).
- For rich entities, value objects, factories, use cases, errors, and domain tests, read [references/domain-and-use-cases.md](references/domain-and-use-cases.md).
- For root and module-local dependency maps, read [references/containers.md](references/containers.md).
- For Elysia application composition, route plugins, request schemas, errors, and HTTP tests, read [references/http.md](references/http.md).
- For Drizzle connection setup, module-local table schemas, repositories, migrations, and transactions, read [references/drizzle.md](references/drizzle.md).
- For colocated unit, HTTP, integration, and end-to-end testing conventions, read [references/testing.md](references/testing.md).

When creating or substantially restructuring a complete backend, read all six references. For a focused change, read only the references governing the touched code.

## Guardrails

- Do not make entities depend on Elysia, Drizzle, HTTP request types, environment variables, or the dependency container.
- Do not use Drizzle table types as domain entities when the application has meaningful domain behavior.
- Do not access the root container from inside entities, factories, use cases, or repositories.
- Do not create repository interfaces merely to satisfy an architecture label. Use TypeScript structural typing or `Pick` at the consumer boundary when a unit test needs a narrow dependency.
- Do not make routes responsible for business decisions.
- Do not automatically run migrations in every API process. Prefer an explicit deployment or CI migration step.
- Do not centralize test fixtures prematurely. Keep a helper inside its test file first; extract a nearby `*.fixture.ts` only after real reuse appears.
- Do not flatten a rich domain into mutable data bags merely to match database rows.

## Completion criteria

Before handing off implementation work, verify that:

- dependencies flow from HTTP and persistence toward use cases and entities, never the reverse;
- each module can be located and understood from its own directory;
- every new business operation has an isolated use-case test;
- every new endpoint has an HTTP-level test when behavior or mapping is non-trivial;
- every repository query has an integration test when it contains meaningful SQL behavior;
- Drizzle schema changes include a generated, reviewed migration;
- imports target real files and no barrel file was added;
- the project type-checks and the relevant tests pass.

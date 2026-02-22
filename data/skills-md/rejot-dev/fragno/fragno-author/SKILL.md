---
name: fragno-author
description: >
  Create or modify Fragno fragments (library-author workflow): scaffold a fragment package, define
  fragment config/schema, add dependencies/services, declare routes, build server instantiation, and
  export client builders plus per-framework client entrypoints. Use when asked to build a new
  fragment, add routes/hooks, or set up fragment packaging/code-splitting for authors.
---

# Fragno Fragment Creation

## Overview

Create or extend a Fragno fragment package with typed routes and client hooks for multiple
frameworks.

Important: Before implementing anything, always `curl` the full docs page for the topic you're
working on (see the "Full docs" commands below). The local guidance here is intentionally concise
and assumes you have read the full docs first.

## Workflow (Library Author)

### Setup

- Prefer creating a new package via the create CLI. For scripted/non-interactive usage:

```sh
pnpm create fragno@latest --non-interactive --name my-fragment
```

This uses sensible defaults: tsdown build tool, database layer included, no agent docs, path set to
`./<name>`.

- OR: Install `@fragno-dev/core` manually. See "assets" below.

### Core building blocks

1. **Define fragment + config** in a definition module
   - `defineFragment<TConfig>("fragment-name").build()`
   - Export config type and any shared schemas.

2. **Optional dependencies / services**
   - Use `withDependencies(({ config }) => ({ ... }))` for server-only deps.
   - Dependencies are not bundled into the client.

3. **Define routes** in dedicated route modules
   - `defineRoutes(definition).create(({ defineRoute, config, deps, services }) => [ ... ])`
   - `defineRoute` options: `method`, `path`, `inputSchema`, `outputSchema`, `handler`,
     `errorCodes`, `queryParameters`.
   - Handler input context: `input.valid()` and request data helpers.
   - Handler output helpers: `json`, `jsonStream`, `empty`, `error`.

4. **Server-side fragment instance** (server entry module)
   - `instantiate(definition).withConfig(config).withRoutes([ ... ]).withOptions(options).build()`

5. **Client-side builder** (client builder module)
   - `createClientBuilder(definition, publicConfig, routes)`
   - Export hooks/composables: `createHook`, `createMutator`.

6. **Framework client entrypoints** (React/Vue/Svelte/Solid/Vanilla)
   - Create a file per framework: React, Vue, Svelte, Solid, Vanilla JS.
   - Each file wraps with the matching `useFragno` from `@fragno-dev/core/<framework>`.

### Reference guide (read these notes after curling docs)

Each section below includes the intro excerpt from the docs plus definitions for key terms. For DB
fragments, start with Database Integration Overview, then Database Testing before writing any tests.

## Docs lookup

- Search the docs index:
  - `curl -s "https://fragno.dev/api/search?query=defineRoutes"`
- Fetch docs as Markdown:
  - `curl -L "https://fragno.dev/docs/fragno/for-library-authors/getting-started" -H "accept: text/markdown"`

## References (docs intros + full docs)

Each section includes the docs intro and a curl command for the full page.

### Config, Dependencies, and Services

The **config** is the basic contract between the Fragment author and the user. It is used to pass
configuration to the Fragment, such as API keys and options. It can also be used to let the user
react to events happening in the Fragment by providing callback functions.

**Dependencies** are objects that are available to route handlers. They are provided using the
`withDependencies` method in the library definition. Dependencies are server-side only and are not
included in the client bundle. They are private to the Fragment and cannot be used by the user
directly.

**Services** are reusable business logic that can be exposed to Fragment users or shared between
Fragments. Like dependencies, services are server-side only and not included in the client bundle.
Fragments can both **provide** services (using `providesService()`) and **require** services (using
`usesService()`), enabling composition and modularity.

- Definitions:
  - Config: fragment-specific runtime settings supplied by users (API keys, feature flags).
  - Dependency: server-only external resource wired into handlers/services (DB, HTTP client).
  - Service: reusable server-side logic built from config + deps and exposed to routes.
- Covers: config shape, dependency injection, services exposure.
- Read when: wiring external APIs, secrets, or shared services into handlers.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/features/dependencies-and-services" -H "accept: text/markdown"`

### Route Definitions

The `defineRoute` function is the core building block for creating API endpoints. It provides a
type-safe way to define HTTP routes with validation, error handling, and automatic type inference.

- Definitions:
  - Route: method + path + handler contract exposed by a fragment.
  - Input schema: validation/typing for request body, params, and query.
  - Output schema: typed shape for successful responses (incl. streaming when used).
  - Error code: typed, declared error variant returned by a handler.
- Covers: route API, schemas, error codes, query params, handler helpers.
- Read when: adding or changing routes, request/response schemas, or error behavior.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/features/route-definition" -H "accept: text/markdown"`

### Client-side State Management

An important feature of Fragno is the ability to define client-side components as part of the
Fragment. Under the hood, Fragno uses [Nanostores](https://github.com/nanostores/nanostores) to
manage state. These reactive primitives integrate seamlessly with many popular frontend frameworks,
such as React, Svelte, Vue, and vanilla JavaScript. Helper functions are provided to automatically
create reactive stores for each API route. These are inspired by the popular TanStack Query library.

- Definitions:
  - Hook: client API for reads (stateful, cached, subscribes to changes).
  - Mutator: client API for writes (triggers requests + cache invalidation).
  - Invalidation: targeted cache refresh keyed by route/path and params.
  - Store: custom client-side state container tied to fragment data.
- Covers: hooks, mutators, invalidation, custom stores, fetch config.
- Read when: designing client APIs, caching/invalidation, or custom state.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/features/client-state-management" -H "accept: text/markdown"`

### Code Splitting

Fragments are "full-stack" libraries. As such, they contain both server-side and client-side
components. Since frameworks differ in how they handle code splitting, Fragno must provide a way to
split the code between client and server bundles on the Fragment level.

- Definitions:
  - Server-only module: code that must never ship to the client (deps, DB).
  - Client entrypoint: framework-specific exports that are safe for browsers.
  - Export boundary: package export that enforces server/client separation.
  - Unplugin: build-time transform that splits code for server/client bundles.
- Covers: unplugin usage, exports, server-only boundaries, peer deps.
- Read when: publishing or changing build config/exports.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/features/code-splitting" -H "accept: text/markdown"`

### Database Integration Overview

The `@fragno-dev/db` package provides an **optional** database layer for Fragments that need
persistent storage. This allows Fragment authors to define a type-safe schema while users provide
their existing database connection.

- Definitions:
  - Database adapter: configurable DB backend provided by the app (SQLite/Postgres/etc).
  - Fragment persistence: optional storage layer for fragment data and hooks.
  - Adapter config: user-supplied driver/dialect settings for the adapter.
- Covers: when to add DB support and how the API is structured.
- Read when: committing to persistence or picking adapters.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/database-integration/overview" -H "accept: text/markdown"`

### Defining Schemas

Learn how to define type-safe database schemas with the append-only log approach.

- Definitions:
  - Schema: versioned description of tables, columns, and relations.
  - Table: named collection of records owned by the fragment.
  - Column: typed field in a table, including constraints/defaults.
  - Index: query optimization and uniqueness declaration.
  - Relation: link between tables expressed via foreign keys.
- Covers: schema DSL, indexes, relations, evolution rules.
- Read when: authoring or evolving a schema.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/database-integration/defining-schemas" -H "accept: text/markdown"`

### Querying

Fragno DB queries are type-safe and based on your schema. The recommended way to query is via the
**Transaction Builder** `this.handlerTx()` in route handlers, so reads/writes can be **composed**
and **batched** into a single transaction.

- Definitions:
  - Query builder: typed API for selects/inserts/updates/deletes.
  - Read flow: data access patterns optimized for indexes and pagination.
  - Write flow: mutations executed in services/handlers with validation.
- Covers: query builder patterns and common read/write flows.
- Read when: implementing DB reads/writes and service-layer access patterns.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/database-integration/querying" -H "accept: text/markdown"`

### Durable Hooks

Durable hooks solve a common problem:

> What if your database transaction commits, but your side effect (email, webhook, API call) fails?

With durable hooks, you **register a hook trigger during the transaction**. The trigger is persisted
in the database as part of the same commit, and then the hook is executed **after the commit**. If
execution fails, it's retried with an exponential backoff policy.

- Definitions:
  - Hook: declared side effect triggered by DB changes.
  - Outbox: internal table that persists hook events for reliable delivery.
  - Dispatcher: process that consumes outbox events and runs hooks.
- Covers: outbox-style side effects and dispatchers.
- Read when: you need reliable side effects or background processing.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/database-integration/durable-hooks" -H "accept: text/markdown"`

### Transactions

In the Fragno database layer, transactions are built around a **two-phase** pattern:

- **Retrieval phase**: schedule reads, then execute them together
- **Mutation phase**: schedule writes, then execute them atomically

In terms of code organization, the important architectural rule is:

- **Route handlers control transaction execution** via `this.handlerTx()`
- **Services define reusable operations** via `this.serviceTx(schema)`

This lets you call **multiple service methods inside one transaction**, and the DB work will be
batched.

- Definitions:
  - Transaction: atomic unit of DB work that commits or rolls back together.
  - `.check()`: validation step inside a transaction to abort on invariants.
  - Boundary: the scope that decides what runs inside a transaction.
- Covers: transaction boundaries and `.check()` patterns.
- Read when: composing multi-step DB operations that must be atomic.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/database-integration/transactions" -H "accept: text/markdown"`

### Database Testing

This section covers database test utilities, including usage of the in-memory adapter.

Important: Use the test harness below. It applies fragment migrations plus Fragno internal tables
for hooks/outbox behavior and handles cleanup. Avoid copying internal adapters or migrations.

- Definitions:
  - Test harness: helper that wires adapters, migrations, and fragments for tests.
  - Test adapter: SQLite-backed test DB configuration for fast local tests.
  - Migration: schema setup step applied before tests run.
  - Cleanup: teardown that closes connections and removes temp files.
- Covers: DB test harness and adapters (`@fragno-dev/test`).
- Read when: before writing database-backed fragment tests.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/database-integration/testing" -H "accept: text/markdown"`

### Testing

Fragno provides comprehensive testing utilities to help you test your fragments without running a
server. The `createFragmentForTest` function creates a test instance with type-safe route handling
and response parsing.

- Definitions:
  - Test fragment: in-memory fragment instance for unit/integration tests.
  - `callRoute`: typed helper to invoke routes without a server.
  - Response union: discriminated response types (`json`, `jsonStream`, `empty`, `error`).
- Covers: core test utilities and `callRoute` behavior.
- Read when: writing unit/integration tests for non-DB fragments or route behavior.
- Full docs:
  `curl -L "https://fragno.dev/docs/fragno/for-library-authors/testing" -H "accept: text/markdown"`

## Assets (example code)

When creating a Fragment using the `create` command with database support, the following assets will
automatically be created.

| Asset                | What it is                                                              | Source                                                  |
| -------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| `database-index.ts`  | Complete database-backed fragment: definition, services, routes, client | `packages/create/templates/optional/database/index.ts`  |
| `database-schema.ts` | Schema definition with tables, columns, indexes, and relations          | `packages/create/templates/optional/database/schema.ts` |

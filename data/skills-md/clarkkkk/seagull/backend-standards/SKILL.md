---
name: backend-standards
description: Use when implementing or refactoring backend logic in packages/api or packages/db. Enforce router/service/data access layering, naming conventions, TRPC best practices, and Drizzle schema guidelines.
---

# Backend Standards (Seagull)

## When to use
- Adding or refactoring tRPC routers/services in `packages/api`.
- Changing database schema in `packages/db`.

## Core rules
- **Layering**:
  - Router layer in `packages/api/src/router` (validation, auth, routing only).
  - Service layer in `packages/api/src/services` for business logic and orchestration.
  - Data access in `packages/db` (Drizzle).
- **Naming**:
  - Files: kebab-case. Variables/functions: camelCase. Types: PascalCase.
  - DB: snake_case tables/columns (Drizzle maps to camelCase).
- **tRPC**:
  - Query = read (`get`, `list`, `search`, `byId`); Mutation = write (`create`, `update`, `delete`, `archive`).
  - Always define Zod inputs.
  - Throw `TRPCError` with semantic codes.
- **DB**:
  - Schema split by domain under `packages/db/src/schema` and re-export in index.
  - Use soft delete via `deletedAt` for core entities.

## Workflow reminders
- Schema change → db migration → router/service updates → frontend usage.
- Run `pnpm lint` and `pnpm typecheck` before commit.

## Canonical reference
- See `skills/backend-standards/references/backend-standards.md` for the full policy text and examples.

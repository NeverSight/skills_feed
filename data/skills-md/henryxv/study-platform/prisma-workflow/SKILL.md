---
name: prisma-workflow
description: Strictly enforces Prisma 7 + Next.js App Router protocols. Manages the lifecycle from initialization to deployment. Use for all database tasks.
---

# Prisma Workflow (v7 Protocol)

## Purpose
To execute a zero-tolerance, type-safe integration of Prisma 7 with Next.js, strictly adhering to the "Prisma Postgres" adapter pattern.

## Critical Directives
**You are strictly forbidden from guessing configuration.** You must consult the reference files for every step.

1.  **Version 7 Only:** If you generate `provider = "prisma-client-js"`, you have failed.
2.  **No Hallucinations:** Do not invent `DATABASE_URL` values.
3.  **Interactive Init:** You cannot run `npx prisma init` yourself. You must guide the user.

## Workflow Phases

### Phase 1: Bootstrap & Configuration
**Reference:** `references/setup-protocol.md`
* **Action:** Guide user through the **interactive** `npx prisma init --db`.
* **Constraint:** Wait for user confirmation. Do not proceed until `.env` exists.
* **Verification:** Check `prisma.config.ts` for `dotenv/config` and Ensure `schema.prisma` has NO `url` in the datasource.

### Phase 2: Architecture & Schema
**Reference:** `references/v7-guardrails.md`
* **Action:** Define models in `schema.prisma`.
* **Constraint:** Use `output = "../app/generated/prisma"` (Custom Output).
* **Constraint:** Use `postgres://` (TCP) schema, never `prisma+postgres://` (HTTP).

### Phase 3: System Implementation
**Reference:** `references/implementation-patterns.md`
* **Action:** Create the Global Singleton at `lib/prisma.ts`.
* **Constraint:** Must use `@prisma/adapter-pg`.
* **Constraint:** Imports must end in `/client`.

### Phase 4: Verification
**Reference:** `references/verification-suite.md`
* **Action:** Create `scripts/test-database.ts`.
* **Action:** Add `db:test` and `db:studio` to `package.json`.
* **Constraint:** Never mark a task complete until `npm run db:test` passes.
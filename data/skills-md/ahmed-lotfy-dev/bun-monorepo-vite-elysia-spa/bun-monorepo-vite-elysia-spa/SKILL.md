---
name: bun-monorepo-vite-elysia-spa
description: "Scaffold or regenerate a Bun fullstack monorepo using official generators only: bun create elysia@latest for backend and bun create vite@latest --template react-ts for SPA frontend, then apply core backend wiring (Better Auth, Drizzle, MCP, OpenAPI, CORS, and security defaults). Use when creating or resetting a Bun workspace monorepo to latest generator versions."
---

# Bun Workspace Vite Elysia SPA

## Overview
Create a Bun workspace monorepo with latest generator output, not manual scaffolding. Use official generators first, then apply backend wiring and security defaults.

## Required Workflow
1. Confirm target path and whether existing `apps/backend` or `apps/frontend` should be replaced.
2. Run official generators only:
- `bun create elysia@latest apps/backend`
- `bun create vite@latest apps/frontend --template react-ts`
3. Install required backend dependencies and dev dependencies with Bun.
4. Apply backend wiring using `references/elysia-core-backend-reference.md` (copied from `elysia-core-backend`) for Better Auth, Drizzle, Postgres, MCP endpoint, OpenAPI docs, CORS allowlist, CSRF middleware, and security headers.
5. Keep frontend as SPA (Vite React TS) unless explicitly requested otherwise.
6. Wire root Bun workspace scripts using Bun filters (`bun run --filter "*" <script>`).
7. Provide run steps and env vars required for local development.

## Hard Rules
- Do not hand-roll generated app baselines when Bun is available.
- Do not keep stale/legacy package versions from old manual scaffolds.
- Do not clobber existing apps without explicit confirmation.
- Prefer replacing app folders (`apps/backend`, `apps/frontend`) over patching old generated output when user asks for latest versions.

## Backend Wiring Checklist
- Better Auth mounted and configured with Drizzle adapter.
- Drizzle schema and config present.
- Postgres connection via env `DATABASE_URL`.
- MCP plugin wired through `elysia-mcp` (not raw `McpServer` plugin use).
- OpenAPI docs route enabled.
- CORS allowlist bound to frontend origin env.
- CSRF protection on non-auth cookie-based mutation routes.
- Security headers middleware enabled.

## Frontend SPA Checklist
- React + TypeScript Vite template.
- `vite` scripts present (`dev`, `build`, `preview`) with `dev` binding host for LAN/WSL access.
- Simple SPA entrypoint validated.

## Run and Verify
- `bun install`
- Run all workspaces: `bun run --filter "*" dev`
- Run one workspace: `bun run --filter frontend dev` or `bun run --filter backend dev`
- Frontend default port: `3000`. Backend default port: `8000`.
- For frontend direct run, use `bun run dev --host 0.0.0.0 --port 3000`.
- For backend direct run, ensure `src/index.ts` listens on `8000`.
- `bun run db:generate` and `bun run db:migrate` in backend when DB is configured.

## References
- Read `references/workflow.md` for exact commands, package lists, and file expectations.
- For any backend work, read `references/elysia-core-backend-reference.md` first (copied from `elysia-core-backend`).
- Upstream reference implementation: `ahmed-lotfy-dev/elysia-core-backend`.

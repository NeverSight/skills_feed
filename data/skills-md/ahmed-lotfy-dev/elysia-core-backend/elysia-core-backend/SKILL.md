---
name: elysia-core-backend
description: Scaffold a Bun + Elysia backend with Better Auth, Drizzle ORM, Postgres, MCP endpoint, OpenAPI docs, CORS, and security defaults. Use when asked to create or regenerate this backend scaffold, or to add these components to a new or empty Elysia server project.
---

# Elysia Core Backend

## Overview

Create a minimal, production-ready Elysia backend skeleton with auth, database, MCP, and security defaults. Follow the official generator workflow and then apply the standardized file structure and contents.

## Workflow

1. Confirm the target location and whether this is a brand-new scaffold or an existing Elysia server. If files already exist, avoid clobbering without explicit user approval.
2. Use the official Elysia generator with latest templates and Bun installs: `bun create elysia@latest <target>`. Do not hand-roll the project or keep stale generated dependencies.
3. Apply the exact folder structure, file contents, and package scripts from the reference guide.
4. Add required environment variables to `.env` and call out secrets that must be user-provided.
5. If the user requests, run migration commands and start the dev server.
6. Verify security defaults: CORS allowlist, CSRF protection on non-auth routes, security headers. Ensure MCP is wired via `elysia-mcp` plugin and not a raw `McpServer`.

## References

- Read `references/elysia-core-backend.md` for the full scaffold steps, file contents, and required notes.

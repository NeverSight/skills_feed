---
name: api-audit
description: "Audit API routes against shared types — scan routes, plugins, and types for mismatches. Read-only, no changes. Use before PRs, after adding routes, or for periodic API contract validation."
---

# API Route & Type Audit Skill

Scan API routes and plugins, catalog every endpoint, and cross-reference against type definitions to find mismatches. **Read-only — do not modify any files.**

## Steps

### 1. Scan Route Files

Scan your routes directory recursively. For each route registration, extract:

- **HTTP method** (GET, POST, PUT, PATCH, DELETE)
- **Path** (e.g., `/api/users`, `/api/admin/settings`)
- **Auth requirements** (public, session-required, RBAC permissions)
- **Request schema** (Zod/validation schema name, if defined)
- **Response schema** (Zod/validation schema name, if defined)

Look for framework-specific patterns (e.g., Fastify schema objects, Express middleware chains, Next.js route handlers).

### 2. Scan Plugin/Middleware Files

Scan middleware or plugin directories for:

- Auth middleware registration (which routes get auth protection)
- Permission mappings
- Rate limiting configurations per route
- Any route-level decorators or hooks

### 3. Catalog Shared Types

Scan type definition directories for:

- Validation schemas used as request/response validators
- TypeScript interfaces/types that correspond to API payloads
- Exported schema names and their shapes

### 4. Cross-Reference and Detect Mismatches

| Category            | What to check                                                      |
| ------------------- | ------------------------------------------------------------------ |
| **Missing schemas** | Routes without request/response validation                         |
| **Type drift**      | Route handler using a type that differs from the shared schema     |
| **Orphan types**    | Schemas in types package not referenced by any route               |
| **Auth gaps**       | Routes missing auth hooks that should have them (e.g., `/admin/*`) |

### 5. Report Findings

Output a markdown table grouped by severity:

1. **Critical**: Auth gaps, missing validation on mutation endpoints
2. **Warning**: Type drift, missing response schemas
3. **Info**: Orphan types, routes with inline schemas that could use shared ones

Include summary counts: total routes, full coverage, partial coverage, no validation, mismatches.

## Arguments

- `$ARGUMENTS`: Optional scope filter
  - Example: `/api-audit admin` — only audit admin routes
  - If empty, audit all routes

## Execution Strategy

Use **two parallel Explore agents** for speed:

1. **Agent A**: Scan routes + plugins — catalog all endpoints
2. **Agent B**: Scan types directories — catalog all shared schemas

Then synthesize their findings into the cross-reference table.

## Key Rules

1. **Read-only** — do not create, modify, or delete any files
2. **Be specific** — report exact file paths and line numbers
3. **No false positives** — only report genuine mismatches
4. **Include context** — show the relevant type/schema snippet for each mismatch

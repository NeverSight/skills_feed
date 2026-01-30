---
name: busirocket-nextjs
description:
  Next.js App Router route handler patterns. Use when creating or refactoring
  route.ts files, implementing API endpoints, validating request inputs, and
  returning standardized JSON responses with proper status codes.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# Next.js Route Handlers

Patterns for thin, maintainable route handlers in Next.js App Router.

## When to Use

Use this skill when:

- Creating or refactoring `app/api/**/route.ts` files
- Implementing API endpoints
- Validating request inputs
- Returning standardized JSON responses
- Deciding server vs client component boundaries

## Non-Negotiables (MUST)

- Route handlers must be **thin**: validate input, call a `services/` function,
  return a response.
- **No business logic or IO** directly in the handler.
- **Never return unvalidated request input**.
- Use standard JSON response shapes: `{ data }` for success,
  `{ error: { code, message } }` for errors.
- Use appropriate HTTP status codes (200, 201, 204, 400, 401, 403, 404, 409,
  500).

## Server vs Client Components

- `app/**/page.tsx` and `app/**/layout.tsx` are **Server Components by
  default**.
- Use **Client Components** only when you need: state/event handlers, effects,
  browser-only APIs.
- `'use client'` creates a boundary; keep client islands small.
- Props from Server -> Client must be **serializable**.

## Rules

### Next.js App Router

- `nextjs-server-vs-client` - Server vs Client Components (defaults, when to use
  client)
- `nextjs-serializable-props` - Props must be serializable from Server to Client
- `nextjs-protecting-server-code` - Protecting server-only code from client
  imports
- `nextjs-special-file-exports` - Allowed extra exports for Next.js special
  files

### Route Handlers

- `nextjs-route-placement` - Route handler placement and conflicts with pages
- `nextjs-thin-handler-rule` - Thin handler rule (STRICT)
- `nextjs-http-methods` - Supported HTTP methods
- `nextjs-caching-model` - Caching model for route handlers
- `nextjs-cache-components` - Cache Components note for route handlers

### API Response Shapes

- `nextjs-response-shapes` - Standard JSON response shapes (success/error)
- `nextjs-status-codes` - HTTP status codes to use
- `nextjs-response-rules` - Rules for API responses (validation, error handling)

### Validation

- `nextjs-validation-boundaries` - Where validation lives (route handlers,
  services, utils)
- `nextjs-validation-patterns` - Validation patterns (unknown inputs, guards)
- `nextjs-validation-helpers` - Recommended validation helpers
- `nextjs-validation-rules` - Validation rules (no inline types/helpers)

## Related Skills

- `busirocket-react` - Component patterns and Server/Client boundaries
- `busirocket-validation` - Validation strategies (Zod schemas, guard helpers)
- `busirocket-core-conventions` - File structure and boundaries

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/nextjs-thin-handler-rule.md
rules/nextjs-response-shapes.md
rules/nextjs-validation-boundaries.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices

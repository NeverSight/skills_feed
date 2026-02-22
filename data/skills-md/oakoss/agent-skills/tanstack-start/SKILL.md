---
name: tanstack-start
description: 'Full-stack React framework built on TanStack Router. Type-safe routing, server functions, SSR/streaming, middleware, and multi-platform deployment. Use when building full-stack React apps with SSR, server functions, middleware, or authentication. Use for createServerFn, createMiddleware, beforeLoad, API routes, Cloudflare Workers, Vercel, Netlify deployment.'
license: MIT
metadata:
  author: oakoss
  version: '1.5'
  source: 'https://tanstack.com/start/latest/docs'
---

# TanStack Start

Full-stack React framework built on TanStack Router. Type-safe server functions via RPC, SSR/streaming, middleware composition, and deployment to Cloudflare Workers, Vercel, Netlify, AWS Lambda, and more.

> **RC:** TanStack Start is currently in Release Candidate status. APIs may still change before the stable 1.0 release.

**Package:** `@tanstack/react-start`

## Quick Reference

| Pattern                                    | Usage                                                     |
| ------------------------------------------ | --------------------------------------------------------- |
| `createServerFn()`                         | GET (default) — idempotent, cacheable data fetching       |
| `createServerFn({ method: 'POST' })`       | Mutations that change data                                |
| `.inputValidator(zodSchema)`               | Input validation before handler                           |
| `.handler(async ({ data }) => {})`         | Server-side logic with typed input data                   |
| `getRequest()`                             | Access full incoming `Request` inside handler/middleware  |
| `getRequestHeader(name)`                   | Read a single request header by name                      |
| `setResponseHeaders(headers)`              | Set outgoing response headers (caching, cookies)          |
| `useServerFn(fn)`                          | Wrap server function for component use with pending state |
| `createMiddleware().server(fn)`            | Request middleware for cross-cutting concerns             |
| `.middleware([dep])`                       | Compose middleware with dependencies                      |
| `next({ context: {} })`                    | Pass data downstream through middleware chain             |
| `createMiddleware({ type: 'function' })`   | Function-level middleware with input validation           |
| `requestMiddleware: []` in `createStart()` | Global middleware for all server requests                 |
| `createIsomorphicFn()`                     | Different implementations per environment                 |
| `createServerOnlyFn()`                     | Server-only utility — crashes if called from client       |
| `createClientOnlyFn()`                     | Client-only utility — crashes if called from server       |
| `useSession()`                             | Cookie-based session with encryption and secure settings  |
| `session.update()`                         | Update session data                                       |
| `session.clear()`                          | Clear session (logout)                                    |
| `beforeLoad`                               | Auth check before route loads                             |
| `_authenticated.tsx`                       | Pathless layout route for grouped protection              |
| `throw redirect({ to: '/login' })`         | Redirect with return URL                                  |
| `await ensureQueryData()`                  | Block SSR on critical data                                |
| `prefetchQuery()`                          | Start fetch, don't block SSR                              |
| `<Suspense>` boundaries                    | Define streaming chunks                                   |
| `head: ({ loaderData }) => ({})`           | Meta tags, Open Graph, favicons                           |
| `head.scripts` + JSON-LD                   | Structured data for LLMO (schema.org)                     |
| `llms.txt` server route                    | AI system guidance file                                   |
| `headers: () => ({...})`                   | ISR / cache-control on route definition                   |
| `server: { handlers: { GET, POST } }`      | API routes on `createFileRoute`                           |
| `prerender: false`                         | Disable prerendering for dynamic routes                   |

## Execution Boundaries

| Function               | Runs On | Client Can Call? | Use For                         |
| ---------------------- | ------- | ---------------- | ------------------------------- |
| `createServerFn()`     | Server  | Yes (RPC stub)   | Data fetching, mutations        |
| `createServerOnlyFn()` | Server  | No (throws)      | Secrets, DB connections         |
| `createClientOnlyFn()` | Client  | N/A              | localStorage, DOM APIs          |
| `createIsomorphicFn()` | Both    | N/A              | Per-environment implementations |

## Deployment (Vite Plugins)

| Platform       | Plugin                                 | Runtime |
| -------------- | -------------------------------------- | ------- |
| Cloudflare     | `@cloudflare/vite-plugin`              | Workers |
| Netlify        | `@netlify/vite-plugin-tanstack-start`  | Node    |
| Vercel         | `nitro/vite` (`preset: 'vercel'`)      | Node    |
| Node.js/Docker | `nitro/vite` (`preset: 'node-server'`) | Node    |
| AWS Lambda     | `nitro/vite` (`preset: 'aws-lambda'`)  | Node    |
| Bun            | `nitro/vite` (`preset: 'bun'`)         | Bun     |
| Static         | `nitro/vite` (`preset: 'static'`)      | None    |

## Common Mistakes

| Mistake                                      | Fix                                                    |
| -------------------------------------------- | ------------------------------------------------------ |
| No `.inputValidator()` on server functions   | Always validate with Zod schemas                       |
| Raw fetch instead of `createServerFn`        | Loses type safety, serialization, and code splitting   |
| Mixing server/client code without boundaries | Use `createServerOnlyFn` / `createClientOnlyFn`        |
| Checking auth in every handler               | Use middleware composition or `beforeLoad`             |
| Awaiting all data in loader                  | Only await critical data, prefetch the rest            |
| `Date.now()` in render                       | Pass timestamp from loader (hydration mismatch)        |
| Missing `nodejs_compat` flag                 | Required in `wrangler.toml` for Cloudflare             |
| GET for mutations                            | Use POST for create/update/delete                      |
| Cookies not forwarded to external APIs       | Use `getRequestHeaders()` or `createIsomorphicFn`      |
| `process.env` in loader (runs on both)       | Wrap in `createServerFn` — loaders run client-side too |
| Unvalidated server env vars                  | Validate with Zod in `.server.ts` files                |
| Storing auth tokens in localStorage          | Use HTTP-only cookies via `useSession`                 |
| Exposing raw DB errors to client             | Catch and return user-friendly messages, log details   |
| No structured data for content pages         | Add JSON-LD via `head.scripts` for AI discoverability  |

## Delegation

Use this skill for TanStack Start server functions, middleware, SSR/streaming, route protection, API routes, and deployment configuration. Delegate to `tanstack-router` for file-based routing, search params, and data loading patterns. Delegate to `tanstack-query` for cache management, optimistic updates, and query patterns.

> If the `tanstack-form` skill is available, delegate form state management, validation, and field patterns to it.
> If the `local-first` skill is available, delegate local-first architecture decisions and sync engine selection to it.
> If the `electricsql` skill is available, delegate ElectricSQL shapes, auth configuration, and write patterns to it.
> If the `tanstack-db` skill is available, delegate reactive collections, live queries, and optimistic mutation patterns to it.

## References

- [Server Functions](references/server-functions.md) — createServerFn, useServerFn, validation, auth, request context, response headers, file uploads, streaming, TanStack Query integration
- [Middleware](references/middleware.md) — composition, function-level middleware, route-level middleware, global middleware, logging, rate limiting
- [SSR and Streaming](references/ssr-and-streaming.md) — Suspense, prerendering, ISR, cache-control, hybrid strategies, hydration safety
- [Route Protection](references/route-protection.md) — beforeLoad, pathless layouts, session security, login/logout, header forwarding, Better Auth
- [API Routes](references/api-routes.md) — server handlers, REST patterns, route-level middleware, webhooks, health check, server functions vs server routes
- [Deployment](references/deployment.md) — Vite plugins, adapter comparison, Cloudflare D1/KV/R2 bindings, Docker, prerendering
- [SEO and Head Management](references/seo.md) — head property, meta tags, Open Graph, Twitter Cards, favicons, SEO helper
- [LLM Optimization (LLMO)](references/llmo.md) — JSON-LD structured data, schema.org, llms.txt, machine-readable endpoints, AI citation patterns
- [Error Handling](references/error-handling.md) — discriminated unions, custom error classes, status codes, result types vs try-catch
- [File Organization](references/file-organization.md) — entry points, plugin config, execution boundaries, env validation, .server.ts convention
- [Known Issues](references/known-issues.md) — 10 documented issues with workarounds
- [Query Integration](references/query-integration.md) — Router+Query setup, SSR integration, setupRouterSsrQueryIntegration, DevTools
- [Integration Flows](references/integration-flows.md) — form submission with cache update, infinite scroll, paginated tables, auth-protected routes, error handling
- [Local-First Integration](references/local-first.md) — shape proxy server functions, mixing server-based and local-first data, ElectricSQL deployment

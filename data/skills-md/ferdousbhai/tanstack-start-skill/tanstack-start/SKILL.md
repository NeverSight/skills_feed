---
name: tanstack-start
description: >-
  TanStack Start full-stack React framework. Use for: server functions with
  createServerFn, TanStack Router file-based routing, TanStack Query SSR integration,
  Cloudflare Workers deployment.
---

# TanStack Start

Full-stack React framework with SSR, server functions, and Vite bundling.

## Project Setup

**New project:**
```bash
pnpm create cloudflare@latest my-app --framework=tanstack-start -y --no-deploy
```

**Existing app:** See [references/migration.md](references/migration.md) for converting React/Vite apps.

## Critical Configuration

### vite.config.ts

```typescript
import { defineConfig } from 'vite'
import tsConfigPaths from 'vite-tsconfig-paths'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    tsConfigPaths(),
    tanstackStart(),
    viteReact(),  // MUST come AFTER tanstackStart
  ],
})
```

### tsconfig.json gotcha

Do NOT enable `verbatimModuleSyntax` - it leaks server bundles into client bundles.

## Server Functions

See [references/server-functions.md](references/server-functions.md) for complete guide.

> ⚠️ **Critical**: Route loaders run on server for initial SSR, but run on **CLIENT** during navigation. Always wrap server code in `createServerFn()` to ensure it runs server-side.

**When to use what (Cloudflare Workers):**

| Use Case | Solution |
|----------|----------|
| Server code in route loaders | `createServerFn()` |
| Server code from client event handlers | API routes (`server.handlers`) work best |
| Access Cloudflare bindings | `import { env } from 'cloudflare:workers'` |

**createServerFn** - for loaders:
```typescript
import { createServerFn } from '@tanstack/react-start'

export const getData = createServerFn().handler(async () => {
  return { data: process.env.SECRET }  // Server-only
})
```

**API routes** - for client event handlers:
```tsx
// routes/api/users.ts
export const Route = createFileRoute('/api/users')({
  server: {
    handlers: {
      POST: async ({ request }) => {
        const body = await request.json()
        return Response.json(await db.users.create(body))
      },
    },
  },
})

// In component: fetch('/api/users', { method: 'POST', body: JSON.stringify(data) })
```

**Key APIs:**
- `createServerFn()` - Server-only functions for loaders
- `server.handlers` - API routes for client event handlers
- `createMiddleware({ type: 'function' })` - Reusable middleware
- `@tanstack/react-start/server`: `getRequestHeaders()`, `setResponseHeader()`, `getCookies()`

## Routing

See [references/routing.md](references/routing.md) for complete patterns.

**File conventions** in `src/routes/`:
| Pattern | Route |
|---------|-------|
| `index.tsx` | `/` |
| `posts.$postId.tsx` | `/posts/:postId` |
| `_layout.tsx` | Layout (no URL) |
| `__root.tsx` | Root layout (required) |

```tsx
import { createFileRoute } from '@tanstack/react-router'
import { createServerFn } from '@tanstack/react-start'

const getPost = createServerFn()
  .handler(async () => await db.post.findFirst())

export const Route = createFileRoute('/posts/$postId')({
  loader: ({ params }) => getPost({ data: params.postId }),
  component: () => {
    const post = Route.useLoaderData()
    return <h1>{post.title}</h1>
  },
})
```

## Cloudflare Deployment

See [references/cloudflare-deployment.md](references/cloudflare-deployment.md) for complete guide.

```bash
pnpm add -D @cloudflare/vite-plugin wrangler
```

**vite.config.ts** - add cloudflare plugin:
```typescript
import { cloudflare } from '@cloudflare/vite-plugin'
// Add to plugins: cloudflare({ viteEnvironment: { name: 'ssr' } })
```

**wrangler.jsonc**:
```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-app",
  "compatibility_date": "<CURRENT_DATE>",  // Use today's YYYY-MM-DD
  "compatibility_flags": ["nodejs_compat"],
  "main": "@tanstack/react-start/server-entry",
  "observability": { "enabled": true }
}
```

**Access Cloudflare bindings** in server functions:
```typescript
import { env } from 'cloudflare:workers'
const value = await env.MY_KV.get('key')
```

**Static Prerendering** (v1.138.0+):
```typescript
tanstackStart({ prerender: { enabled: true } })
```

## TanStack Query Integration

See [references/query-integration.md](references/query-integration.md) for SSR setup.

```bash
pnpm add @tanstack/react-query @tanstack/react-router-ssr-query
```

```tsx
// Preload in loaders, consume with useSuspenseQuery
loader: ({ context }) => context.queryClient.ensureQueryData(myQueryOptions)
```

## Better-Auth Integration

See [references/better-auth.md](references/better-auth.md) for complete guide.

> ⚠️ **Critical**: Use `createFileRoute` with `server.handlers`, NOT the legacy `createAPIFileRoute`.

**Mount the auth handler** at `/src/routes/api/auth/$.ts`:
```typescript
import { auth } from '@/lib/auth'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/api/auth/$')({
  server: {
    handlers: {
      GET: ({ request }) => auth.handler(request),
      POST: ({ request }) => auth.handler(request),
    },
  },
})
```

**Auth config** with `tanstackStartCookies` plugin:
```typescript
import { betterAuth } from "better-auth"
import { tanstackStartCookies } from "better-auth/tanstack-start"

export const auth = betterAuth({
  // ...your config
  plugins: [tanstackStartCookies()] // MUST be last plugin
})
```

**Protect routes** with middleware:
```typescript
import { createMiddleware } from "@tanstack/react-start"
import { getRequestHeaders } from "@tanstack/react-start/server"
import { auth } from "./auth"

export const authMiddleware = createMiddleware().server(
  async ({ next }) => {
    const session = await auth.api.getSession({ headers: getRequestHeaders() })
    if (!session) throw redirect({ to: "/login" })
    return next()
  }
)

// In route:
export const Route = createFileRoute('/dashboard')({
  server: { middleware: [authMiddleware] },
  component: Dashboard,
})
```

## GitHub Actions Auto-Deploy

See [references/github-actions-deploy.md](references/github-actions-deploy.md) for CI/CD setup with preview deployments.

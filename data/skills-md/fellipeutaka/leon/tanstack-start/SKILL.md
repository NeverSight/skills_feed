---
name: tanstack-start
description: |
  TanStack Start full-stack React framework best practices for server functions, middleware, SSR/streaming, SEO, authentication, and deployment.
  Use when building full-stack React apps with TanStack Start, implementing server functions, configuring SSR/streaming,
  managing SEO and head tags, setting up authentication patterns, or deploying to Vercel/Cloudflare/Node.
metadata:
  tags: tanstack-start, react, full-stack, ssr, server-functions, middleware, seo, streaming, deployment, typescript
---

# TanStack Start

**Version**: @tanstack/react-start@1.x
**Requires**: React 18.0+, TypeScript 5.0+, Vite, TanStack Router

## Quick Setup

```bash
npm install @tanstack/react-start @tanstack/react-router
npm install -D @tanstack/router-plugin
```

### Vite Config

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'

export default defineConfig({
  plugins: [tanstackStart(), react()],
})
```

### Root Route

```tsx
// src/routes/__root.tsx
import {
  HeadContent,
  Outlet,
  Scripts,
  createRootRoute,
} from '@tanstack/react-router'

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    ],
  }),
  component: RootComponent,
})

function RootComponent() {
  return (
    <html lang="en">
      <head>
        <HeadContent />
      </head>
      <body>
        <Outlet />
        <Scripts />
      </body>
    </html>
  )
}
```

### Devtools

**Standalone** (TanStack Router only):

```bash
npm install -D @tanstack/react-router-devtools
```

```tsx
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'

// In root layout, before </body>
<TanStackRouterDevtools position="bottom-right" />
<Scripts />
```

**Unified TanStack Devtools** (recommended with multiple TanStack libraries):

If using Start + Query (or other TanStack libraries), use the unified `TanStackDevtools` shell instead of individual devtools components:

```bash
npm install -D @tanstack/react-devtools
```

```tsx
import { TanStackRouterDevtoolsPanel } from '@tanstack/react-router-devtools'
import { TanStackDevtools } from '@tanstack/react-devtools'

// In root layout, before </body>
<TanStackDevtools
  config={{ position: 'bottom-right' }}
  plugins={[
    { name: 'TanStack Router', render: <TanStackRouterDevtoolsPanel /> },
    // Add more plugins: Query, etc.
  ]}
/>
<Scripts />
```

Use `*Panel` variants (`TanStackRouterDevtoolsPanel`, `ReactQueryDevtoolsPanel`) when embedding inside `TanStackDevtools`.

## Rule Categories

| Priority | Rule | Description |
|----------|------|-------------|
| CRITICAL | [sf-server-functions](rules/sf-server-functions.md) | createServerFn, GET/POST methods, handler pattern |
| HIGH | [sf-middleware](rules/sf-middleware.md) | createMiddleware, client/server execution, chaining |
| HIGH | [sf-validation](rules/sf-validation.md) | Input validation with Zod/Standard Schema, trust boundaries |
| HIGH | [ssr-streaming](rules/ssr-streaming.md) | Streaming SSR with Suspense, TTFB optimization |
| HIGH | [seo-head-management](rules/seo-head-management.md) | head() per route, meta tags, HeadContent, OG tags |
| HIGH | [auth-patterns](rules/auth-patterns.md) | beforeLoad guards, session server fns, cookie forwarding |
| MEDIUM | [ssr-hydration](rules/ssr-hydration.md) | Hydration mismatch prevention, client-only components |
| MEDIUM | [ssr-prerendering](rules/ssr-prerendering.md) | Static prerendering, ISR via Cache-Control |
| MEDIUM | [api-routes](rules/api-routes.md) | createAPIFileRoute, REST handlers, webhooks |
| MEDIUM | [deployment](rules/deployment.md) | Hosting adapters, env vars, production config |
| MEDIUM | [config-project-setup](rules/config-project-setup.md) | Vite plugin, root route, project structure |

## Critical Rules

### ALWAYS use `createServerFn` for server-side code

```tsx
import { createServerFn } from '@tanstack/react-start'

const getUser = createServerFn({ method: 'GET' })
  .handler(async () => {
    return db.users.findFirst()
  })
```

### ALWAYS validate server function inputs

```tsx
const updateUser = createServerFn({ method: 'POST' })
  .inputValidator((data: { name: string; email: string }) => data)
  .handler(async ({ data }) => {
    return db.users.update({ where: { email: data.email }, data })
  })
```

### NEVER access `window`/`document` in components rendered on the server

```tsx
// BAD — hydration mismatch
function Bad() {
  return <span>{window.innerWidth}px</span>
}

// GOOD — use useEffect for client-only state
function Good() {
  const [width, setWidth] = useState<number | null>(null)
  useEffect(() => setWidth(window.innerWidth), [])
  return <span>{width ?? '...'}px</span>
}
```

### ALWAYS use `head()` for SEO metadata

```tsx
export const Route = createFileRoute('/about')({
  head: () => ({
    meta: [
      { title: 'About Us' },
      { name: 'description', content: 'Learn about our company' },
    ],
  }),
})
```

## Key Patterns

### Auth Guard with Redirect

```tsx
// routes/_authed.tsx
export const Route = createFileRoute('/_authed')({
  beforeLoad: async ({ location }) => {
    const user = await getCurrentUserFn()
    if (!user) {
      throw redirect({
        to: '/login',
        search: { redirect: location.href },
      })
    }
    return { user }
  },
})
```

### Server Function with Validation

```tsx
const createPost = createServerFn({ method: 'POST' })
  .inputValidator((data: { title: string; body: string }) => data)
  .handler(async ({ data }) => {
    const post = await db.posts.create({ data })
    return post
  })
```

### Streaming Dashboard

```tsx
export const Route = createFileRoute('/dashboard')({
  loader: async ({ context: { queryClient } }) => {
    // Await critical data
    await queryClient.ensureQueryData(userQueries.profile())
    // Prefetch non-critical (streams in via Suspense)
    queryClient.prefetchQuery(statsQueries.dashboard())
  },
  component: DashboardPage,
})

function DashboardPage() {
  const { data: user } = useSuspenseQuery(userQueries.profile())
  return (
    <div>
      <Header user={user} />
      <Suspense fallback={<StatsSkeleton />}>
        <DashboardStats />
      </Suspense>
    </div>
  )
}
```

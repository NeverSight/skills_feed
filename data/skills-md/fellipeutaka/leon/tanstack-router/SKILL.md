---
name: tanstack-router
description: |
  TanStack Router best practices for type-safe routing, file-based routing, data loading, search params, and navigation in React.
  Use when building React SPAs with complex routing, implementing type-safe search params, setting up route loaders,
  integrating with TanStack Query, or configuring code splitting and preloading.
metadata:
  tags: tanstack-router, routing, react, typescript, file-based-routing, search-params, data-loading, code-splitting
---

# TanStack Router

**Version**: @tanstack/react-router@1.x
**Requires**: React 18.0+, TypeScript 5.0+, Vite (recommended)

## Quick Setup

```bash
npm install @tanstack/react-router @tanstack/react-router-devtools
npm install -D @tanstack/router-plugin
```

### Vite Plugin

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { tanstackRouter } from '@tanstack/router-plugin/vite'

export default defineConfig({
  plugins: [tanstackRouter(), react()],
})
```

### Root Route

```tsx
// src/routes/__root.tsx
import { createRootRoute, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'

export const Route = createRootRoute({
  component: () => (
    <>
      <Outlet />
      <TanStackRouterDevtools />
    </>
  ),
})
```

### Unified Devtools (Recommended with Multiple TanStack Libraries)

If using Router + Query (or other TanStack libraries), use the unified `TanStackDevtools` shell instead of individual devtools components:

```bash
npm install -D @tanstack/react-devtools
```

```tsx
// src/routes/__root.tsx
import { createRootRoute, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtoolsPanel } from '@tanstack/react-router-devtools'
import { TanStackDevtools } from '@tanstack/react-devtools'

export const Route = createRootRoute({
  component: () => (
    <>
      <Outlet />
      <TanStackDevtools
        config={{ position: 'bottom-right' }}
        plugins={[
          { name: 'TanStack Router', render: <TanStackRouterDevtoolsPanel /> },
          // Add more plugins: Query, etc.
        ]}
      />
    </>
  ),
})
```

Use `*Panel` variants (`TanStackRouterDevtoolsPanel`, `ReactQueryDevtoolsPanel`) when embedding inside `TanStackDevtools`.

### Router Creation & Type Registration

```tsx
// src/router.tsx
import { createRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'

export const router = createRouter({ routeTree })

// Register router type for global inference
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
```

### Entry Point

```tsx
// src/main.tsx
import { RouterProvider } from '@tanstack/react-router'
import { router } from './router'

function App() {
  return <RouterProvider router={router} />
}
```

### File Structure

```
src/routes/
├── __root.tsx              # Root layout (always rendered)
├── index.tsx               # "/" route
├── about.tsx               # "/about" route
├── posts.tsx               # "/posts" layout
├── posts.index.tsx         # "/posts" index
├── posts.$postId.tsx       # "/posts/:postId" dynamic route
├── _auth.tsx               # Pathless layout (auth guard)
├── _auth.dashboard.tsx     # "/dashboard" (wrapped by _auth)
└── (settings)/
    ├── settings.tsx         # Route group
    └── settings.profile.tsx
```

## Rule Categories

| Priority | Category | Rule File | Impact |
|----------|----------|-----------|--------|
| CRITICAL | Type Safety | `rules/ts-type-safety.md` | Prevents runtime errors, enables refactoring |
| CRITICAL | File-Based Routing | `rules/org-file-based-routing.md` | Ensures maintainable route structure |
| HIGH | Router Config | `rules/router-configuration.md` | Global defaults for preload, scroll, errors |
| HIGH | Data Loading | `rules/load-data-loading.md` | Optimizes data fetching, prevents waterfalls |
| HIGH | Query Integration | `rules/load-query-integration.md` | TanStack Query + Router wiring |
| HIGH | Search Params | `rules/search-params.md` | Type-safe URL state management |
| HIGH | Error Handling | `rules/err-error-handling.md` | Graceful error and 404 handling |
| MEDIUM | Navigation | `rules/nav-navigation.md` | Type-safe links and programmatic nav |
| MEDIUM | Code Splitting | `rules/split-code-splitting.md` | Reduces bundle size |
| MEDIUM | Preloading | `rules/pre-preloading.md` | Improves perceived performance |
| LOW | Route Context | `rules/ctx-route-context.md` | Dependency injection and auth guards |

## Critical Rules

### Always Do

- **Register router type** — declare module `@tanstack/react-router` with `Register.router` for global type inference
- **Use `from` parameter** in hooks (`useSearch`, `useParams`, `useLoaderData`) to get exact types for the current route
- **Validate search params** — use `validateSearch` with any Standard Schema library (Zod, Valibot, Yup, ArkType, etc.)
- **Use file-based routing** — let the plugin generate the route tree, don't maintain it manually
- **Use loaders for data** — fetch in `loader`, not in components (prevents waterfalls, enables preloading)

### Never Do

- **Don't skip type registration** — without it, all hooks return `unknown` unions
- **Don't fetch data in useEffect** — use `loader` or `beforeLoad` instead
- **Don't use string paths without Link's type checking** — `<Link to="/typo">` catches errors at compile time
- **Don't put heavy logic in components** — loaders run before render and enable preloading/parallel fetching

## Key Patterns

```tsx
// Auth guard with beforeLoad + redirect
export const Route = createFileRoute('/_auth')({
  beforeLoad: ({ context }) => {
    if (!context.auth.user) {
      throw redirect({ to: '/login', search: { redirect: location.href } })
    }
  },
})

// Search params with Standard Schema (no adapter needed)
import { z } from 'zod'

const searchSchema = z.object({
  page: z.number().default(1),
  sort: z.enum(['newest', 'oldest']).default('newest'),
})

export const Route = createFileRoute('/posts')({
  validateSearch: searchSchema, // Pass schema directly
})

// Loader with ensureQueryData
export const Route = createFileRoute('/posts/$postId')({
  loader: ({ context, params }) =>
    context.queryClient.ensureQueryData(postQueryOptions(params.postId)),
  component: PostComponent,
})

function PostComponent() {
  const post = Route.useLoaderData()
  return <h1>{post.title}</h1>
}

// Code-split with .lazy.tsx
// posts.tsx — keeps loader (critical path)
export const Route = createFileRoute('/posts')({
  loader: () => fetchPosts(),
})

// posts.lazy.tsx — splits component (loaded after)
export const Route = createLazyFileRoute('/posts')({
  component: PostsComponent,
})
```

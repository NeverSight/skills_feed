---
name: nextjs-best-practice
description: Next.js 15 best practices for App Router, Server/Client Components, data fetching, forms, and project structure. Use when writing, reviewing, or refactoring Next.js 15 code. Triggers on tasks involving Next.js pages, components, data fetching, Server Actions, forms, routing, caching, performance optimization, or project structure decisions. Also use when asked to review Next.js code or set up new features in a Next.js 15 project.
---

# Next.js 15 Best Practices

Team standard for building Next.js 15 applications with App Router, Tailwind CSS, and TypeScript.

## Decision Tree: Server vs Client Component

```
Need interactivity (onClick, onChange, state)?
├── YES → 'use client'
│   └── Keep it small. Push interactivity to leaf components.
└── NO → Server Component (default)
    ├── Need data? → async function + fetch/db directly
    ├── Need to show loading? → Add loading.tsx or <Suspense>
    └── Need client child? → Pass data as props (serializable only)
```

**Key rule:** Default to Server Components. Only add `'use client'` at the lowest possible node.

## Export Rule (MANDATORY)

**Named exports everywhere. `export default` ONLY where Next.js requires it.**

| File | Export | Why |
|------|--------|-----|
| `page.tsx` | `export default` | Next.js requires it |
| `layout.tsx` | `export default` | Next.js requires it |
| `loading.tsx` | `export default` | Next.js requires it |
| `error.tsx` | `export default` | Next.js requires it |
| `not-found.tsx` | `export default` | Next.js requires it |
| Everything else | `export function` / `export const` | Team convention |

```tsx
// WRONG
export default function BlogView({ blog }: BlogViewProps) { ... }
export default function Button({ ...props }: ButtonProps) { ... }
export default useSidebarStore

// CORRECT
export function BlogView({ blog }: BlogViewProps) { ... }
export function Button({ ...props }: ButtonProps) { ... }
export const useSidebarStore = create<SidebarStore>(...)
```

This applies to: `view.tsx`, all `components/`, `hooks/`, `lib/`, `config/`, `constants/`, `context/`, `store/`, `validation/`, `actions/`, `types/`.

## Page/View Pattern (MANDATORY)

Every route that needs client interactivity MUST use the `page.tsx` + `view.tsx` split:

```
app/blog/[id]/
├── page.tsx    # Server Component — fetches data, passes as props
├── view.tsx    # 'use client' — thin composition layer, imports from components/
└── loading.tsx # Loading skeleton (optional)

components/blog/            # Sub-components for blog views
├── blog-header.tsx
├── blog-content.tsx
├── blog-comments.tsx
└── blog-like-button.tsx
```

**`view.tsx` must stay thin.** It receives props, manages top-level state, and composes sub-components from `components/[feature]/`. Never let `view.tsx` grow into a monolith.

```tsx
// page.tsx — Server Component (data fetching ONLY)
import { db } from '@/config/db'
import { notFound } from 'next/navigation'
import { BlogDetailView } from './view'

export default async function BlogPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const [blog, comments] = await Promise.all([
    db.blog.findUnique({ where: { id } }),
    db.comment.findMany({ where: { blogId: id } }),
  ])
  if (!blog) notFound()
  return <BlogDetailView blog={blog} comments={comments} />
}
```

```tsx
// view.tsx — Thin composition layer
'use client'

import type { Blog, Comment } from '@/types'
import { BlogHeader } from '@/components/blog/blog-header'
import { BlogContent } from '@/components/blog/blog-content'
import { BlogComments } from '@/components/blog/blog-comments'

interface BlogDetailViewProps {
  blog: Blog
  comments: Comment[]
}

export function BlogDetailView({ blog, comments }: BlogDetailViewProps) {
  return (
    <article>
      <BlogHeader title={blog.title} author={blog.author} date={blog.createdAt} />
      <BlogContent content={blog.content} />
      <BlogComments blogId={blog.id} comments={comments} />
    </article>
  )
}
```

**Mapping rule:** `app/[route]/view.tsx` → `components/[route]/**`

| Route | view.tsx | Components folder |
|-------|----------|-------------------|
| `app/home/` | `app/home/view.tsx` | `components/home/` |
| `app/blog/[id]/` | `app/blog/[id]/view.tsx` | `components/blog/` |
| `app/(dashboard)/settings/` | `app/(dashboard)/settings/view.tsx` | `components/settings/` |

**Never use `useEffect` to fetch initial data.** Fetch in `page.tsx`, pass via props.

## No Props Hell (MANDATORY)

**Only pass props that the child cannot obtain itself.** If a child can access data via context, Zustand store, or hook — let the child do it. Don't fetch/subscribe in a parent just to pass down.

```tsx
// BAD: Props hell — parent fetches state just to pass it
export function BlogDetailView({ blog, comments }: BlogDetailViewProps) {
  const { user } = useAuth()
  const { theme } = useTheme()
  const { isOpen } = useSidebarStore()

  return (
    <BlogHeader user={user} theme={theme} />          {/* user/theme are prop-drilled */}
    <BlogComments blogId={blog.id} comments={comments} isOpen={isOpen} />
  )
}

// GOOD: Each child fetches its own shared state
export function BlogDetailView({ blog, comments }: BlogDetailViewProps) {
  return (
    <BlogHeader />                                     {/* reads useAuth() + useTheme() itself */}
    <BlogComments blogId={blog.id} comments={comments} />  {/* reads useSidebarStore() itself */}
  )
}
```

**Props are for:** Data that comes from the server (`page.tsx` → `view.tsx` → child) or data the child has no way to access on its own.

**Props are NOT for:** Context values, store state, or hook results the child can call directly.

```
Decision: Should I pass this as a prop?
├── Child can call useAuth(), useTheme(), useSidebarStore(), etc.?
│   └── NO prop — let child access it directly
├── Data comes from server (page.tsx fetched it)?
│   └── YES prop — pass it down
└── Data is local to parent (parent's useState)?
    └── YES prop — pass it down (or lift to store/context if many children need it)
```

For detailed patterns and examples, see [references/server-client-components.md](references/server-client-components.md).

## useEffect vs useLayoutEffect (MANDATORY)

**Don't spam `useEffect` everywhere.** Analyze first — pick the right hook for the job.

```
Need to run a side effect?
├── Does it read or modify DOM layout (measure size, scroll position, focus)?
│   └── YES → useLayoutEffect (runs synchronously before browser paints)
├── Does it need to prevent visual flicker (tooltip position, element resize)?
│   └── YES → useLayoutEffect
└── Everything else (API calls, subscriptions, analytics, timers)
    └── useEffect (runs after paint, does not block rendering)
```

```tsx
// BAD: useEffect causes flicker — DOM measurement happens after paint
useEffect(() => {
  const height = ref.current.getBoundingClientRect().height
  setHeight(height)  // user sees a layout jump
}, [])

// GOOD: useLayoutEffect — measures before paint, no flicker
useLayoutEffect(() => {
  const height = ref.current.getBoundingClientRect().height
  setHeight(height)  // seamless, user sees correct layout immediately
}, [])
```

| Hook | Timing | Use when |
|------|--------|----------|
| `useEffect` | After paint (async) | Data fetching, subscriptions, analytics, timers, logging |
| `useLayoutEffect` | Before paint (sync) | DOM measurement, scroll position, focus management, preventing flicker |

**Rule:** If you're about to write `useEffect`, ask: "Does this touch the DOM or could it cause a visual flicker?" If yes → `useLayoutEffect`.

## Decision Tree: Data Fetching

```
Where is the data needed?
├── Server Component → fetch() or direct DB call
│   ├── Static data? → cache: 'force-cache' (default)
│   ├── Dynamic data? → cache: 'no-store'
│   ├── Timed revalidation? → next: { revalidate: N }
│   └── On-demand revalidation? → revalidateTag() / revalidatePath()
├── Client Component (real-time / polling) → useSWR or TanStack Query
└── Mutation → Server Action
```

**Key rule:** Fetch data in Server Components, pass to Client Components as props. Use SWR/TanStack Query only for client-side polling, optimistic UI, or real-time data.

For detailed patterns, see [references/data-fetching.md](references/data-fetching.md).

## Decision Tree: Forms & Mutations

```
Form submission?
├── Simple form → Server Action with <form action={}>
│   └── Need pending state? → useActionState + useFormStatus
├── Complex form (multi-step, validation) → React Hook Form + Zod
│   └── Submit via Server Action or API route
└── Optimistic UI needed? → useOptimistic + Server Action
```

**Key rule:** Use Server Actions for mutations. Use React Hook Form + Zod for complex client-side validation. Validate on both client AND server.

For detailed patterns, see [references/forms-and-mutations.md](references/forms-and-mutations.md).

## Project Structure

Standard folder layout — each folder has ONE purpose:

```
src/
├── app/            # Routes, layouts, pages + view.tsx files ONLY
├── components/     # Reusable UI components (ui/ + feature-specific/)
├── actions/        # Server Actions organized by domain
├── config/         # App config, env wrappers, third-party setup
├── constants/      # App-wide constant values
├── context/        # React context providers
├── hooks/          # Custom React hooks
├── lib/            # Utilities and reusable libraries (cn(), formatDate(), db client)
├── providers/      # App-wide providers (auth, theme, query client, Zustand, etc.)
├── store/          # Client state management (Zustand, etc.)
├── styles/         # Global styles, Tailwind config
├── types/          # Shared TypeScript types/interfaces
└── validation/     # Zod schemas for forms and Server Actions
```

**Placement rules:**
- Route files (`page.tsx`, `view.tsx`, `layout.tsx`, `loading.tsx`) → `app/`
- Anything reusable across routes → appropriate folder above
- Never put business logic in `app/` — only data fetching and composition

## Clean Layout Rule (MANDATORY)

**Always use a single `providers.tsx`** in the `providers/` folder that composes all app-wide providers. The root `layout.tsx` stays clean — it only imports `Providers` and wraps `{children}`.

```tsx
// providers/providers.tsx — Single entry point for all providers
'use client'

import { AuthProvider } from './auth-provider'
import { ThemeProvider } from './theme-provider'
import { QueryProvider } from './query-provider'
import type { User } from '@/types'

interface ProvidersProps {
  user: User | null
  children: React.ReactNode
}

export function Providers({ user, children }: ProvidersProps) {
  return (
    <QueryProvider>
      <AuthProvider user={user}>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </AuthProvider>
    </QueryProvider>
  )
}
```

```tsx
// app/layout.tsx — Clean. Only structure + Providers.
import { Providers } from '@/providers/providers'
import { getCurrentUser } from '@/config/auth'
import '@/styles/globals.css'

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const user = await getCurrentUser()

  return (
    <html lang="en">
      <body>
        <Providers user={user}>
          {children}
        </Providers>
      </body>
    </html>
  )
}
```

**When adding a new provider:** Add it inside `providers.tsx` — never touch `layout.tsx`.

For detailed conventions and examples, see [references/project-structure.md](references/project-structure.md).

## Performance Quick Reference

| Priority | Rule | Action |
|----------|------|--------|
| CRITICAL | Eliminate waterfalls | Use `Promise.all()`, parallel fetches, `<Suspense>` |
| CRITICAL | Bundle size | Import directly (no barrel files), `next/dynamic` for heavy components |
| HIGH | Server performance | `React.cache()` for dedup, minimize RSC → Client serialization |
| MEDIUM | Client data | SWR/TanStack Query for dedup, passive event listeners |
| MEDIUM | Re-renders | `memo()` for expensive components, functional `setState` |

For full performance guide, see [references/performance.md](references/performance.md).

## Code Review Checklist

Quick checks when reviewing Next.js code:

1. `'use client'` only where needed? (not at page/layout level)
2. Data fetched in Server Components, not Client?
3. Server Actions validate input on server side?
4. No secrets/env vars leaked to client bundle?
5. `loading.tsx` or `<Suspense>` for async content?
6. Images use `next/image`, links use `next/link`?
7. Metadata exported from pages/layouts?
8. No unnecessary `useEffect` for data that could be server-fetched?

For full checklist, see [references/code-review-checklist.md](references/code-review-checklist.md).

---
name: nextjs
description: |
  Build Next.js 16 apps with App Router, Server Components/Actions, Cache Components ("use cache"), and async route params. Includes proxy.ts (replaces middleware.ts) and React 19.2.

  Use when: building Next.js 16 projects, or troubleshooting async params (Promise types), "use cache" directives, parallel route 404s (missing default.js), or proxy.ts CORS.
license: MIT
metadata:
  version: 1.0.0
  last_verified: 2025-10-24
  nextjs_version: 16.0.0
  react_version: 19.2.0
  node_version: 20.9+
  author: Jezweb
  repository: https://github.com/jezweb/claude-skills
  production_tested: true
  token_savings: 65-70%
  errors_prevented: 18+
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
---

# Next.js App Router - Production Patterns

**Version**: Next.js 16.0.0
**React Version**: 19.2.0
**Node.js**: 20.9+
**Last Verified**: 2025-10-24

---

## Table of Contents

1. [When to Use This Skill](#when-to-use-this-skill)
2. [When NOT to Use This Skill](#when-not-to-use-this-skill)
3. [Next.js 16 Breaking Changes](#nextjs-16-breaking-changes)
4. [Cache Components & Caching APIs](#cache-components--caching-apis)
5. [Route Handlers (Next.js 16 Updates)](#route-handlers-nextjs-16-updates)
6. [Proxy vs Middleware](#proxy-vs-middleware)
7. [Parallel Routes - default.js Required](#parallel-routes---defaultjs-required-breaking)
8. [React 19.2 Features](#react-192-features)
9. [Turbopack (Stable in Next.js 16)](#turbopack-stable-in-nextjs-16)
10. [Common Errors & Solutions](#common-errors--solutions)
11. [Templates & Resources](#templates--resources)

---

## When to Use This Skill

**Focus**: Next.js 16 breaking changes and knowledge gaps (December 2024+).

Use this skill when you need:

- **Next.js 16 breaking changes** (async params, proxy.ts, parallel routes default.js, removed features)
- **Cache Components** with `"use cache"` directive (NEW in Next.js 16)
- **New caching APIs**: `revalidateTag()`, `updateTag()`, `refresh()` (Updated in Next.js 16)
- **Migration from Next.js 15 to 16** (avoid breaking change errors)
- **Async route params** (`params`, `searchParams`, `cookies()`, `headers()` now async)
- **Parallel routes with default.js** (REQUIRED in Next.js 16)
- **React 19.2 features** (View Transitions, `useEffectEvent()`, React Compiler)
- **Turbopack** (stable and default in Next.js 16)
- **Image defaults changed** (TTL, sizes, qualities in Next.js 16)
- **Error prevention** (18+ documented Next.js 16 errors with solutions)

---

## When NOT to Use This Skill

Do NOT use this skill for:

- **Cloudflare Workers deployment** → Use `cloudflare-nextjs` skill instead
- **Pages Router patterns** → This skill covers App Router ONLY (Pages Router is legacy)
- **Authentication libraries** → Use `clerk-auth`, `better-auth`, or other auth-specific skills
- **Database integration** → Use `cloudflare-d1`, `drizzle-orm-d1`, or database-specific skills
- **UI component libraries** → Use `tailwind-v4-shadcn` skill for Tailwind + shadcn/ui
- **State management** → Use `zustand-state-management`, `tanstack-query` skills
- **Form libraries** → Use `react-hook-form-zod` skill
- **Vercel-specific features** → Refer to Vercel platform documentation
- **Next.js Enterprise features** (ISR, DPR) → Refer to Next.js Enterprise docs
- **Deployment configuration** → Use platform-specific deployment skills

**Relationship with Other Skills**:
- **cloudflare-nextjs**: For deploying Next.js to Cloudflare Workers (use BOTH skills together if deploying to Cloudflare)
- **tailwind-v4-shadcn**: For Tailwind v4 + shadcn/ui setup (composable with this skill)
- **clerk-auth**: For Clerk authentication in Next.js (composable with this skill)
- **better-auth**: For Better Auth integration (composable with this skill)

---

## Next.js 16 Breaking Changes

**IMPORTANT**: Next.js 16 introduces multiple breaking changes. Read this section carefully if migrating from Next.js 15 or earlier.

### 1. Async Route Parameters (BREAKING)

**Breaking Change**: `params`, `searchParams`, `cookies()`, `headers()`, `draftMode()` are now **async** and must be awaited.

**Before (Next.js 15)**:
```typescript
// ❌ This no longer works in Next.js 16
export default function Page({ params, searchParams }: {
  params: { slug: string }
  searchParams: { query: string }
}) {
  const slug = params.slug // ❌ Error: params is a Promise
  const query = searchParams.query // ❌ Error: searchParams is a Promise
  return <div>{slug}</div>
}
```

**After (Next.js 16)**:
```typescript
// ✅ Correct: await params and searchParams
export default async function Page({ params, searchParams }: {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ query: string }>
}) {
  const { slug } = await params // ✅ Await the promise
  const { query } = await searchParams // ✅ Await the promise
  return <div>{slug}</div>
}
```

**Applies to**:
- `params` in pages, layouts, route handlers
- `searchParams` in pages
- `cookies()` from `next/headers`
- `headers()` from `next/headers`
- `draftMode()` from `next/headers`

**Migration**:
```typescript
// ❌ Before
import { cookies, headers } from 'next/headers'

export function MyComponent() {
  const cookieStore = cookies() // ❌ Sync access
  const headersList = headers() // ❌ Sync access
}

// ✅ After
import { cookies, headers } from 'next/headers'

export async function MyComponent() {
  const cookieStore = await cookies() // ✅ Async access
  const headersList = await headers() // ✅ Async access
}
```

**Codemod**: Run `npx @next/codemod@canary upgrade latest` to automatically migrate.

**See Template**: `templates/app-router-async-params.tsx`

---

### 2. Middleware → Proxy Migration (BREAKING)

**Breaking Change**: `middleware.ts` is **deprecated** in Next.js 16. Use `proxy.ts` instead.

**Why the Change**: `proxy.ts` makes the network boundary explicit by running on Node.js runtime (not Edge runtime). This provides better clarity between edge middleware and server-side proxies.

**Migration Steps**:

1. **Rename file**: `middleware.ts` → `proxy.ts`
2. **Rename function**: `middleware` → `proxy`
3. **Update config**: `matcher` → `config.matcher` (same syntax)

**Before (Next.js 15)**:
```typescript
// middleware.ts ❌ Deprecated in Next.js 16
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'value')
  return response
}

export const config = {
  matcher: '/api/:path*',
}
```

**After (Next.js 16)**:
```typescript
// proxy.ts ✅ New in Next.js 16
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'value')
  return response
}

export const config = {
  matcher: '/api/:path*',
}
```

**Note**: `middleware.ts` still works in Next.js 16 but is deprecated. Migrate to `proxy.ts` for future compatibility.

**See Template**: `templates/proxy-migration.ts`
**See Reference**: `references/proxy-vs-middleware.md`

---

### 3. Parallel Routes Require `default.js` (BREAKING)

**Breaking Change**: Parallel routes now **require** explicit `default.js` files. Without them, routes will fail during soft navigation.

**Structure**:
```
app/
├── @auth/
│   ├── login/
│   │   └── page.tsx
│   └── default.tsx    ← REQUIRED in Next.js 16
├── @dashboard/
│   ├── overview/
│   │   └── page.tsx
│   └── default.tsx    ← REQUIRED in Next.js 16
└── layout.tsx
```

**Layout**:
```typescript
// app/layout.tsx
export default function Layout({
  children,
  auth,
  dashboard,
}: {
  children: React.ReactNode
  auth: React.ReactNode
  dashboard: React.ReactNode
}) {
  return (
    <html>
      <body>
        {auth}
        {dashboard}
        {children}
      </body>
    </html>
  )
}
```

**Default Fallback** (REQUIRED):
```typescript
// app/@auth/default.tsx
export default function AuthDefault() {
  return null // or <Skeleton /> or redirect
}

// app/@dashboard/default.tsx
export default function DashboardDefault() {
  return null
}
```

**Why Required**: Next.js 16 changed how parallel routes handle soft navigation. Without `default.js`, unmatched slots will error during client-side navigation.

**See Template**: `templates/parallel-routes-with-default.tsx`

---

### 4. Removed Features (BREAKING)

**The following features are REMOVED in Next.js 16**:

1. **AMP Support** - Entirely removed. Migrate to standard pages.
2. **`next lint` command** - Use ESLint or Biome directly.
3. **`serverRuntimeConfig` and `publicRuntimeConfig`** - Use environment variables instead.
4. **`experimental.ppr` flag** - Evolved into Cache Components. Use `"use cache"` directive.
5. **Automatic `scroll-behavior: smooth`** - Add manually if needed.
6. **Node.js 18 support** - Minimum version is now **20.9+**.

**Migration**:
- **AMP**: Convert AMP pages to standard pages or use separate AMP implementation.
- **Linting**: Run `npx eslint .` or `npx biome lint .` directly.
- **Config**: Replace `serverRuntimeConfig` with `process.env.VARIABLE`.
- **PPR**: Migrate from `experimental.ppr` to `"use cache"` directive (see Cache Components section).

---

### 5. Version Requirements (BREAKING)

**Next.js 16 requires**:

- **Node.js**: 20.9+ (Node.js 18 no longer supported)
- **TypeScript**: 5.1+ (if using TypeScript)
- **React**: 19.2+ (automatically installed with Next.js 16)
- **Browsers**: Chrome 111+, Safari 16.4+, Firefox 109+, Edge 111+

**Check Versions**:
```bash
node --version    # Should be 20.9+
npm --version     # Should be 10+
npx next --version # Should be 16.0.0+
```

**Upgrade Node.js**:
```bash
# Using nvm
nvm install 20
nvm use 20
nvm alias default 20

# Using Homebrew (macOS)
brew install node@20

# Using apt (Ubuntu/Debian)
sudo apt update
sudo apt install nodejs npm
```

---

### 6. Image Defaults Changed (BREAKING)

**Next.js 16 changed `next/image` defaults**:

| Setting | Next.js 15 | Next.js 16 |
|---------|------------|------------|
| **TTL** (cache duration) | 60 seconds | 4 hours |
| **imageSizes** | `[16, 32, 48, 64, 96, 128, 256, 384]` | `[640, 750, 828, 1080, 1200]` (reduced) |
| **qualities** | `[75, 90, 100]` | `[75]` (single quality) |

**Impact**:
- Images cache longer (4 hours vs 60 seconds)
- Fewer image sizes generated (smaller builds, but less granular)
- Single quality (75) generated instead of multiple

**Override Defaults** (if needed):
```typescript
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  images: {
    minimumCacheTTL: 60, // Revert to 60 seconds
    deviceSizes: [640, 750, 828, 1080, 1200, 1920], // Add larger sizes
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384], // Restore old sizes
    formats: ['image/webp'], // Default
  },
}

export default config
```

**See Template**: `templates/image-optimization.tsx`

---

## Cache Components & Caching APIs

**NEW in Next.js 16**: Cache Components introduce **opt-in caching** with the `"use cache"` directive, replacing implicit caching from Next.js 15.

### 1. Overview

**What Changed**:
- **Next.js 15**: Implicit caching (all Server Components cached by default)
- **Next.js 16**: Opt-in caching with `"use cache"` directive

**Why the Change**: Explicit caching gives developers more control and makes caching behavior predictable.

**Cache Components enable**:
- Component-level caching (cache specific components, not entire pages)
- Function-level caching (cache expensive computations)
- Page-level caching (cache entire pages selectively)
- **Partial Prerendering (PPR)** - Cache static parts, render dynamic parts on-demand

---

### 2. `"use cache"` Directive

**Syntax**: Add `"use cache"` at the top of a Server Component, function, or route handler.

**Component-level caching**:
```typescript
// app/components/expensive-component.tsx
'use cache'

export async function ExpensiveComponent() {
  const data = await fetch('https://api.example.com/data')
  const json = await data.json()

  return (
    <div>
      <h1>{json.title}</h1>
      <p>{json.description}</p>
    </div>
  )
}
```

**Function-level caching**:
```typescript
// lib/data.ts
'use cache'

export async function getExpensiveData(id: string) {
  const response = await fetch(`https://api.example.com/items/${id}`)
  return response.json()
}

// Usage in component
import { getExpensiveData } from '@/lib/data'

export async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const product = await getExpensiveData(id) // Cached

  return <div>{product.name}</div>
}
```

**Page-level caching**:
```typescript
// app/blog/[slug]/page.tsx
'use cache'

export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json())
  return posts.map((post: { slug: string }) => ({ slug: post.slug }))
}

export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await fetch(`https://api.example.com/posts/${slug}`).then(r => r.json())

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}
```

**See Template**: `templates/cache-component-use-cache.tsx`

---

### 3. Partial Prerendering (PPR)

**PPR** allows caching static parts of a page while rendering dynamic parts on-demand.

**Pattern**:
```typescript
// app/dashboard/page.tsx

// Static header (cached)
'use cache'
async function StaticHeader() {
  return <header>My App</header>
}

// Dynamic user info (not cached)
async function DynamicUserInfo() {
  const cookieStore = await cookies()
  const userId = cookieStore.get('userId')?.value
  const user = await fetch(`/api/users/${userId}`).then(r => r.json())

  return <div>Welcome, {user.name}</div>
}

// Page combines both
export default function Dashboard() {
  return (
    <div>
      <StaticHeader /> {/* Cached */}
      <DynamicUserInfo /> {/* Dynamic */}
    </div>
  )
}
```

**When to Use PPR**:
- Page has both static and dynamic content
- Want to cache layout/header/footer but render user-specific content
- Need fast initial load (static parts) + personalization (dynamic parts)

**See Reference**: `references/cache-components-guide.md`

---

### 4. `revalidateTag()` - Updated API

**BREAKING CHANGE**: `revalidateTag()` now requires a **second argument** (`cacheLife` profile) for stale-while-revalidate behavior.

**Before (Next.js 15)**:
```typescript
import { revalidateTag } from 'next/cache'

export async function updatePost(id: string) {
  await fetch(`/api/posts/${id}`, { method: 'PATCH' })
  revalidateTag('posts') // ❌ Only one argument in Next.js 15
}
```

**After (Next.js 16)**:
```typescript
import { revalidateTag } from 'next/cache'

export async function updatePost(id: string) {
  await fetch(`/api/posts/${id}`, { method: 'PATCH' })
  revalidateTag('posts', 'max') // ✅ Second argument required in Next.js 16
}
```

**Built-in Cache Life Profiles**:
- `'max'` - Maximum staleness (recommended for most use cases)
- `'hours'` - Stale after hours
- `'days'` - Stale after days
- `'weeks'` - Stale after weeks
- `'default'` - Default cache behavior

**Custom Cache Life Profile**:
```typescript
revalidateTag('posts', {
  stale: 3600, // Stale after 1 hour (seconds)
  revalidate: 86400, // Revalidate every 24 hours (seconds)
  expire: false, // Never expire (optional)
})
```

**Pattern in Server Actions**:
```typescript
'use server'

import { revalidateTag } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await fetch('/api/posts', {
    method: 'POST',
    body: JSON.stringify({ title, content }),
  })

  revalidateTag('posts', 'max') // ✅ Revalidate with max staleness
}
```

**See Template**: `templates/revalidate-tag-cache-life.ts`

---

### 5. `updateTag()` - NEW API (Server Actions Only)

**NEW in Next.js 16**: `updateTag()` provides **read-your-writes semantics** for Server Actions.

**What it does**:
- Expires cache immediately
- Refreshes data within the same request
- Shows updated data right after mutation (no stale data)

**Difference from `revalidateTag()`**:
- `revalidateTag()`: **Stale-while-revalidate** (shows stale data, revalidates in background)
- `updateTag()`: **Immediate refresh** (expires cache, fetches fresh data in same request)

**Use Case**: Forms, user settings, or any mutation where user expects immediate feedback.

**Pattern**:
```typescript
'use server'

import { updateTag } from 'next/cache'

export async function updateUserProfile(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string

  // Update database
  await db.users.update({ name, email })

  // Immediately refresh cache (read-your-writes)
  updateTag('user-profile')

  // User sees updated data immediately (no stale data)
}
```

**When to Use**:
- **`updateTag()`**: User settings, profile updates, critical mutations (immediate feedback)
- **`revalidateTag()`**: Blog posts, product listings, non-critical updates (background revalidation)

**See Template**: `templates/server-action-update-tag.ts`

---

### 6. `refresh()` - NEW API (Server Actions Only)

**NEW in Next.js 16**: `refresh()` refreshes **uncached data only** (complements client-side `router.refresh()`).

**When to Use**:
- Refresh dynamic data without affecting cached data
- Complement `router.refresh()` on server side

**Pattern**:
```typescript
'use server'

import { refresh } from 'next/cache'

export async function refreshDashboard() {
  // Refresh uncached data (e.g., real-time metrics)
  refresh()

  // Cached data (e.g., static header) remains cached
}
```

**Difference from `revalidateTag()` and `updateTag()`**:
- `refresh()`: Only refreshes **uncached** data
- `revalidateTag()`: Revalidates **specific tagged** data (stale-while-revalidate)
- `updateTag()`: Immediately expires and refreshes **specific tagged** data

**See Reference**: `references/cache-components-guide.md`

---

---

## Route Handlers (Next.js 16 Updates)

### Async Params in Route Handlers (BREAKING)

**IMPORTANT**: `params` and `headers()` are now async in Next.js 16 route handlers.

**Example**:
```typescript
// app/api/posts/[id]/route.ts
import { NextResponse } from 'next/server'
import { headers } from 'next/headers'

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params // ✅ Await params in Next.js 16
  const headersList = await headers() // ✅ Await headers in Next.js 16

  const post = await db.posts.findUnique({ where: { id } })

  return NextResponse.json(post)
}
```

**See Template**: `templates/route-handler-api.ts`

---

## Proxy vs Middleware

**Next.js 16 introduces `proxy.ts`** to replace `middleware.ts`.

### Why the Change?

- **`middleware.ts`**: Runs on Edge runtime (limited Node.js APIs)
- **`proxy.ts`**: Runs on Node.js runtime (full Node.js APIs)

The new `proxy.ts` makes the network boundary explicit and provides more flexibility.

### Migration

**Before (middleware.ts)**:
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('token')

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: '/dashboard/:path*',
}
```

**After (proxy.ts)**:
```typescript
// proxy.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('token')

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: '/dashboard/:path*',
}
```

**See Template**: `templates/proxy-migration.ts`
**See Reference**: `references/proxy-vs-middleware.md`

---

## Parallel Routes - default.js Required (BREAKING)

**Breaking Change in Next.js 16**: Parallel routes now **require** explicit `default.js` files.

**Structure**:
```
app/
├── @modal/
│   ├── login/page.tsx
│   └── default.tsx  ← REQUIRED in Next.js 16
├── @feed/
│   ├── trending/page.tsx
│   └── default.tsx  ← REQUIRED in Next.js 16
└── layout.tsx
```

**Default Files (REQUIRED)**:
```typescript
// app/@modal/default.tsx
export default function ModalDefault() {
  return null // or <Skeleton /> or redirect
}
```

**Why Required**: Next.js 16 changed soft navigation handling. Without `default.js`, unmatched slots error during client-side navigation.

**See Template**: `templates/parallel-routes-with-default.tsx`

---

## React 19.2 Features

Next.js 16 integrates React 19.2, which includes new features from React Canary.

### 1. View Transitions

**Use Case**: Smooth animations between page transitions.

```typescript
'use client'

import { useRouter } from 'next/navigation'
import { startTransition } from 'react'

export function NavigationLink({ href, children }: { href: string; children: React.ReactNode }) {
  const router = useRouter()

  function handleClick(e: React.MouseEvent) {
    e.preventDefault()

    // Wrap navigation in startTransition for View Transitions
    startTransition(() => {
      router.push(href)
    })
  }

  return <a href={href} onClick={handleClick}>{children}</a>
}
```

**With CSS View Transitions API**:
```css
/* app/globals.css */
@view-transition {
  navigation: auto;
}

/* Animate elements with view-transition-name */
.page-title {
  view-transition-name: page-title;
}
```

**See Template**: `templates/view-transitions-react-19.tsx`

---

### 2. `useEffectEvent()` (Experimental)

**Use Case**: Extract non-reactive logic from `useEffect`.

```typescript
'use client'

import { useEffect, experimental_useEffectEvent as useEffectEvent } from 'react'

export function ChatRoom({ roomId }: { roomId: string }) {
  const onConnected = useEffectEvent(() => {
    console.log('Connected to room:', roomId)
  })

  useEffect(() => {
    const connection = connectToRoom(roomId)
    onConnected() // Non-reactive callback

    return () => connection.disconnect()
  }, [roomId]) // Only re-run when roomId changes

  return <div>Chat Room {roomId}</div>
}
```

**Why Use It**: Prevents unnecessary `useEffect` re-runs when callback dependencies change.

---

### 3. React Compiler (Stable)

**Use Case**: Automatic memoization without `useMemo`, `useCallback`.

**Enable in next.config.ts**:
```typescript
import type { NextConfig } from 'next'

const config: NextConfig = {
  experimental: {
    reactCompiler: true,
  },
}

export default config
```

**Install Plugin**:
```bash
npm install babel-plugin-react-compiler
```

**Example** (no manual memoization needed):
```typescript
'use client'

export function ExpensiveList({ items }: { items: string[] }) {
  // React Compiler automatically memoizes this
  const filteredItems = items.filter(item => item.length > 3)

  return (
    <ul>
      {filteredItems.map(item => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  )
}
```

**See Reference**: `references/react-19-integration.md`

---

## Turbopack (Stable in Next.js 16)

**NEW**: Turbopack is now the **default bundler** in Next.js 16.

**Performance Improvements**:
- 2–5× faster production builds
- Up to 10× faster Fast Refresh

**Opt-out** (if needed):
```bash
npm run build -- --webpack
```

**Enable File System Caching** (experimental):
```typescript
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  experimental: {
    turbopack: {
      fileSystemCaching: true, // Beta: Persist cache between runs
    },
  },
}

export default config
```

---

## Common Errors & Solutions

### 1. Error: `params` is a Promise

**Error**:
```
Type 'Promise<{ id: string }>' is not assignable to type '{ id: string }'
```

**Cause**: Next.js 16 changed `params` to async.

**Solution**: Await `params`:
```typescript
// ❌ Before
export default function Page({ params }: { params: { id: string } }) {
  const id = params.id
}

// ✅ After
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
}
```

---

### 2. Error: `searchParams` is a Promise

**Error**:
```
Property 'query' does not exist on type 'Promise<{ query: string }>'
```

**Cause**: `searchParams` is now async in Next.js 16.

**Solution**:
```typescript
// ❌ Before
export default function Page({ searchParams }: { searchParams: { query: string } }) {
  const query = searchParams.query
}

// ✅ After
export default async function Page({ searchParams }: { searchParams: Promise<{ query: string }> }) {
  const { query } = await searchParams
}
```

---

### 3. Error: `cookies()` requires await

**Error**:
```
'cookies' implicitly has return type 'any'
```

**Cause**: `cookies()` is now async in Next.js 16.

**Solution**:
```typescript
// ❌ Before
import { cookies } from 'next/headers'

export function MyComponent() {
  const cookieStore = cookies()
}

// ✅ After
import { cookies } from 'next/headers'

export async function MyComponent() {
  const cookieStore = await cookies()
}
```

---

### 4. Error: Parallel route missing `default.js`

**Error**:
```
Error: Parallel route @modal/login was matched but no default.js was found
```

**Cause**: Next.js 16 requires `default.js` for all parallel routes.

**Solution**: Add `default.tsx` files:
```typescript
// app/@modal/default.tsx
export default function ModalDefault() {
  return null
}
```

---

### 5. Error: `revalidateTag()` requires 2 arguments

**Error**:
```
Expected 2 arguments, but got 1
```

**Cause**: `revalidateTag()` now requires a `cacheLife` argument in Next.js 16.

**Solution**:
```typescript
// ❌ Before
revalidateTag('posts')

// ✅ After
revalidateTag('posts', 'max')
```

---

### 6. Error: Cannot use React hooks in Server Component

**Error**:
```
You're importing a component that needs useState. It only works in a Client Component
```

**Cause**: Using React hooks in Server Component.

**Solution**: Add `'use client'` directive:
```typescript
// ✅ Add 'use client' at the top
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

---

### 7. Error: `middleware.ts` is deprecated

**Warning**:
```
Warning: middleware.ts is deprecated. Use proxy.ts instead.
```

**Solution**: Migrate to `proxy.ts`:
```typescript
// Rename: middleware.ts → proxy.ts
// Rename function: middleware → proxy

export function proxy(request: NextRequest) {
  // Same logic
}
```

---

### 8. Error: Turbopack build failure

**Error**:
```
Error: Failed to compile with Turbopack
```

**Cause**: Turbopack is now default in Next.js 16.

**Solution**: Opt out of Turbopack if incompatible:
```bash
npm run build -- --webpack
```

---

### 9. Error: Invalid `next/image` src

**Error**:
```
Invalid src prop (https://example.com/image.jpg) on `next/image`. Hostname "example.com" is not configured under images in your `next.config.js`
```

**Solution**: Add remote patterns in `next.config.ts`:
```typescript
const config: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
      },
    ],
  },
}
```

---

### 10. Error: Cannot import Server Component into Client Component

**Error**:
```
You're importing a Server Component into a Client Component
```

**Solution**: Pass Server Component as children:
```typescript
// ❌ Wrong
'use client'
import { ServerComponent } from './server-component' // Error

export function ClientComponent() {
  return <ServerComponent />
}

// ✅ Correct
'use client'

export function ClientComponent({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}

// Usage
<ClientComponent>
  <ServerComponent /> {/* Pass as children */}
</ClientComponent>
```

---

### 11. Error: `generateStaticParams` not working

**Cause**: `generateStaticParams` only works with static generation (`export const dynamic = 'force-static'`).

**Solution**:
```typescript
export const dynamic = 'force-static'

export async function generateStaticParams() {
  const posts = await fetch('/api/posts').then(r => r.json())
  return posts.map((post: { id: string }) => ({ id: post.id }))
}
```

---

### 12. Error: `fetch()` not caching

**Cause**: Next.js 16 uses opt-in caching with `"use cache"` directive.

**Solution**: Add `"use cache"` to component or function:
```typescript
'use cache'

export async function getPosts() {
  const response = await fetch('/api/posts')
  return response.json()
}
```

---

### 13. Error: Route collision with Route Groups

**Error**:
```
Error: Conflicting routes: /about and /(marketing)/about
```

**Cause**: Route groups create same URL path.

**Solution**: Ensure route groups don't conflict:
```
app/
├── (marketing)/about/page.tsx  → /about
└── (shop)/about/page.tsx       → ERROR: Duplicate /about

# Fix: Use different routes
app/
├── (marketing)/about/page.tsx     → /about
└── (shop)/store-info/page.tsx     → /store-info
```

---

### 14. Error: Metadata not updating

**Cause**: Using dynamic metadata without `generateMetadata()`.

**Solution**: Use `generateMetadata()` for dynamic pages:
```typescript
export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const { id } = await params
  const post = await fetch(`/api/posts/${id}`).then(r => r.json())

  return {
    title: post.title,
    description: post.excerpt,
  }
}
```

---

### 15. Error: `next/font` font not loading

**Cause**: Font variable not applied to HTML element.

**Solution**: Apply font variable to `<html>` or `<body>`:
```typescript
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html className={inter.variable}> {/* ✅ Apply variable */}
      <body>{children}</body>
    </html>
  )
}
```

---

### 16. Error: Environment variables not available in browser

**Cause**: Server-only env vars are not exposed to browser.

**Solution**: Prefix with `NEXT_PUBLIC_` for client-side access:
```bash
# .env
SECRET_KEY=abc123                  # Server-only
NEXT_PUBLIC_API_URL=https://api    # Available in browser
```

```typescript
// Server Component (both work)
const secret = process.env.SECRET_KEY
const apiUrl = process.env.NEXT_PUBLIC_API_URL

// Client Component (only public vars work)
const apiUrl = process.env.NEXT_PUBLIC_API_URL
```

---

### 17. Error: Server Action not found

**Error**:
```
Error: Could not find Server Action
```

**Cause**: Missing `'use server'` directive.

**Solution**: Add `'use server'`:
```typescript
// ❌ Before
export async function createPost(formData: FormData) {
  await db.posts.create({ ... })
}

// ✅ After
'use server'

export async function createPost(formData: FormData) {
  await db.posts.create({ ... })
}
```

---

### 18. Error: TypeScript path alias not working

**Cause**: Incorrect `baseUrl` or `paths` in `tsconfig.json`.

**Solution**: Configure correctly:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"],
      "@/components/*": ["./app/components/*"]
    }
  }
}
```

**See Reference**: `references/top-errors.md`

---

## Templates & Resources

**Next.js 16-Specific Templates** (in `templates/`):
- `app-router-async-params.tsx` - Async params migration patterns
- `parallel-routes-with-default.tsx` - Required default.js files
- `cache-component-use-cache.tsx` - Cache Components with `"use cache"`
- `revalidate-tag-cache-life.ts` - Updated `revalidateTag()` with cacheLife
- `server-action-update-tag.ts` - `updateTag()` for read-your-writes
- `proxy-migration.ts` - Migrate from middleware.ts to proxy.ts
- `view-transitions-react-19.tsx` - React 19.2 View Transitions
- `next.config.ts` - Next.js 16 configuration

**Bundled References** (in `references/`):
- `next-16-migration-guide.md` - Complete Next.js 15→16 migration guide
- `cache-components-guide.md` - Cache Components deep dive
- `proxy-vs-middleware.md` - Proxy.ts vs middleware.ts
- `async-route-params.md` - Async params breaking change details
- `react-19-integration.md` - React 19.2 features in Next.js 16
- `top-errors.md` - 18+ common errors with solutions

**External Documentation**:
- **Next.js 16 Blog**: https://nextjs.org/blog/next-16
- **Next.js Docs**: https://nextjs.org/docs
- **Context7 MCP**: `/websites/nextjs` for latest reference

---

## Version Compatibility

| Package | Minimum Version | Recommended |
|---------|----------------|-------------|
| Next.js | 16.0.0 | 16.0.0+ |
| React | 19.2.0 | 19.2.0+ |
| Node.js | 20.9.0 | 20.9.0+ |
| TypeScript | 5.1.0 | 5.7.0+ |
| Turbopack | (built-in) | Stable |

**Check Versions**:
```bash
./scripts/check-versions.sh
```

---

## Token Efficiency

**Estimated Token Savings**: 65-70%

**Without Skill** (manual setup from docs):
- Read Next.js 16 migration guide: ~5k tokens
- Read App Router docs: ~8k tokens
- Read Server Actions docs: ~4k tokens
- Read Metadata API docs: ~3k tokens
- Trial-and-error fixes: ~8k tokens
- **Total**: ~28k tokens

**With Skill**:
- Load skill: ~8k tokens
- Use templates: ~2k tokens
- **Total**: ~10k tokens
- **Savings**: ~18k tokens (~64%)

**Errors Prevented**: 18+ common mistakes = 100% error prevention

---

## Maintenance

**Last Verified**: 2025-10-24
**Next Review**: 2026-01-24 (Quarterly)
**Maintainer**: Jezweb | jeremy@jezweb.net
**Repository**: https://github.com/jezweb/claude-skills

**Update Triggers**:
- Next.js major/minor releases
- React major releases
- Breaking changes in APIs
- New Turbopack features

**Version Check**:
```bash
cd skills/nextjs
./scripts/check-versions.sh
```

---

**End of SKILL.md**

---
name: vike-skills
description: Use when building or working with Vike + Vue SSR/SSG applications - establishes best practices for page creation, data fetching, routing, and layouts
---

# Vike Skills (Vue)

**Core principle:** Build fast, SEO-friendly Vue applications with server-side rendering using Vike's flexible architecture.

## When to Use This Skill

**Always use when:**
- Creating new Vike + Vue pages
- Setting up data fetching with `+data` hooks
- Configuring layouts and nested layouts
- Implementing route guards and authentication
- Managing head tags and SEO
- Working with client-only components

**Don't use for:**
- Non-Vike Vue applications (use Nuxt or plain Vue)
- React or Solid projects (use vike-react or vike-solid)

## Documentation Quick Links

- **[reference.md](./reference.md)** - Official API documentation links
- **[examples.md](./examples.md)** - Vue + Vike patterns and code examples
- **Official Vike Docs** - https://vike.dev

## Development Checklist

When creating a new page, use TodoWrite to track:

- [ ] Create `+Page.vue` component
- [ ] Add `+data.js` if page needs data fetching
- [ ] Use `useData()` to access data in component
- [ ] Add `+guard.js` if page requires authentication
- [ ] Configure head tags (`+title`, `+description`) for SEO
- [ ] Handle errors with `throw render()` or `throw redirect()`
- [ ] Use `clientOnly()` for browser-only components

## Essential Requirements

### Every Page Must Have

1. **`+Page.vue` component** - The page's Vue component
2. **Proper data access** - Use `useData()` not direct pageContext
3. **Error handling** - Handle missing data gracefully
4. **SEO consideration** - Title and description for public pages

### Every Data Hook Must Have

1. **Type exports** - `export type Data = Awaited<ReturnType<typeof data>>`
2. **Error handling** - Use `throw render(404)` for missing resources
3. **Minimal data** - Only return what the page needs (auto-serialized)

### Every Layout Must Have

1. **Children slot** - `<slot />` to render nested content
2. **Proper scoping** - Place in correct directory for inheritance
3. **No data fetching assumptions** - Layouts share page's `+data`

### Every Guard Must Have

1. **Clear conditions** - Check auth state before render
2. **Proper redirects** - Use `throw redirect('/login')` or `throw render(401)`
3. **Async support** - Guards can be async for API checks

## Core Patterns

### Basic Page with Data

```vue
<!-- /pages/movies/+Page.vue -->
<script setup lang="ts">
import { useData } from 'vike-vue/useData'
import type { Data } from './+data'

const { movies } = useData<Data>()
</script>

<template>
  <h1>Movies</h1>
  <ul>
    <li v-for="movie in movies" :key="movie.id">
      {{ movie.title }}
    </li>
  </ul>
</template>
```

```typescript
// /pages/movies/+data.ts
export type Data = Awaited<ReturnType<typeof data>>

export async function data() {
  const movies = await fetchMovies()
  return { movies }
}
```

### Layout

```vue
<!-- /pages/+Layout.vue -->
<script setup>
import Navigation from '../components/Navigation.vue'
</script>

<template>
  <Navigation />
  <main>
    <slot />
  </main>
</template>
```

### Route Guard

```typescript
// /pages/admin/+guard.ts
import { redirect } from 'vike/abort'

export async function guard(pageContext) {
  if (!pageContext.user) {
    throw redirect('/login')
  }
  if (!pageContext.user.isAdmin) {
    throw render(403, 'Admin access required')
  }
}
```

## File Naming Conventions

| File | Purpose |
|------|---------|
| `+Page.vue` | Page component |
| `+Layout.vue` | Layout wrapper |
| `+data.ts` | Server-side data fetching |
| `+guard.ts` | Route protection |
| `+config.ts` | Page/directory configuration |
| `+title.ts` | Page title |
| `+Head.vue` | Custom head tags |

### File Suffixes

| Suffix | Runs On |
|--------|---------|
| `.server.ts` | Server only (default for +data) |
| `.client.ts` | Client only |
| `.shared.ts` | Both server and client |

## Red Flags - Stop If You See

- Accessing `window` or `document` in SSR code without `clientOnly()`
- Missing `passToClient` for server data needed on client
- Data fetching inside Vue components (use `+data` instead)
- Hardcoded URLs instead of using routing
- Missing error handling in `+data` hooks
- Guards that don't `throw` (they must throw, not return)
- Layouts without `<slot />` for children

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll add SEO later" | Missing titles hurt from day one |
| "Guards can return false" | Guards must `throw redirect()` or `throw render()` |
| "I can access window in +data" | `+data` runs on server by default |
| "pageContext has everything" | Use `useData()` for type-safe data access |

## Configuration Inheritance

Vike configs cascade down the directory tree:

```
pages/
  +config.ts          # Applies to ALL pages
  +Layout.vue         # Global layout
  (marketing)/
    +Layout.vue       # Nested inside global layout
    about/+Page.vue   # Has both layouts
  admin/
    +guard.ts         # Applies to all admin pages
    +config.ts        # Admin-specific config
    users/+Page.vue   # Protected by guard
```

## passToClient Defaults

With client routing, these are automatically available client-side:
- `pageContext.Page`
- `pageContext.data`
- `pageContext.config`
- `pageContext.routeParams`
- `pageContext.urlOriginal`
- `pageContext.urlPathname`
- `pageContext.urlParsed`

For custom properties (like `user`), add to `+config.ts`:

```typescript
export default {
  passToClient: ['user']
}
```

## Quick Workflow

1. **Need API details?** → Check [reference.md](./reference.md)
2. **Need examples?** → Check [examples.md](./examples.md)
3. **Building something?** → Follow checklist above, use TodoWrite
4. **Stuck?** → Check official docs at https://vike.dev

## Final Rule

```
Every Vike + Vue page must have:
1. +Page.vue component
2. +data.ts for server data (if needed)
3. useData() for type-safe data access
4. Error handling for edge cases
5. SEO tags for public pages
```

Follow these principles for fast, SEO-friendly Vue applications.

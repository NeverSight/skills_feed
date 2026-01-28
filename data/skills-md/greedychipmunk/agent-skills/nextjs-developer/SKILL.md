---
name: nextjs-developer
description: Expert Next.js development with App Router, Server Components, and modern React patterns
---

# Next.js Developer Skill

## Overview

This skill provides comprehensive expertise in building production-ready Next.js applications using the **App Router** (Next.js 13+). It covers Server Components, data fetching patterns, routing, API routes, caching, and performance optimization.

## Core Capabilities

### App Router Architecture
- **Server Components**: Default rendering model for optimal performance
- **Client Components**: Interactive components with `"use client"` directive
- **Layouts**: Shared UI with preserved state across routes
- **Templates**: Fresh instances on navigation (no state preservation)
- **Loading UI**: Streaming with `loading.tsx` files
- **Error Handling**: Granular error boundaries with `error.tsx`

### Data Fetching
- **Server-side fetching**: Direct database/API access in Server Components
- **Caching strategies**: Static, dynamic, and incremental regeneration
- **Revalidation**: Time-based and on-demand cache invalidation
- **Parallel fetching**: Optimized data loading patterns

### Routing System
- **File-based routing**: Automatic route generation from file structure
- **Dynamic routes**: `[param]` and catch-all `[...slug]` patterns
- **Route groups**: `(folder)` for organization without URL impact
- **Parallel routes**: `@slot` for simultaneous route rendering
- **Intercepting routes**: Modal patterns with `(.)`, `(..)`, `(...)`

### Server Actions
- **Form handling**: Progressive enhancement with `action` attribute
- **Mutations**: Server-side data modifications
- **Revalidation**: Automatic cache updates after mutations
- **Optimistic updates**: Immediate UI feedback patterns

## Implementation Patterns

### Project Structure
```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page
├── globals.css         # Global styles
├── (auth)/             # Route group
│   ├── login/page.tsx
│   └── register/page.tsx
├── dashboard/
│   ├── layout.tsx      # Dashboard layout
│   ├── page.tsx        # Dashboard home
│   ├── loading.tsx     # Loading UI
│   ├── error.tsx       # Error boundary
│   └── [id]/page.tsx   # Dynamic route
├── api/
│   └── [route]/route.ts # API routes
└── components/         # Shared components
```

### Component Patterns

#### Server Component (Default)
```typescript
// app/posts/page.tsx
async function PostsPage() {
  const posts = await db.posts.findMany()

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}

export default PostsPage
```

#### Client Component
```typescript
// app/components/counter.tsx
"use client"

import { useState } from "react"

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  )
}
```

### Data Fetching Patterns

#### Static Generation (Default)
```typescript
// Cached indefinitely (can be revalidated)
async function Page() {
  const data = await fetch('https://api.example.com/data')
  return <div>{data}</div>
}
```

#### Dynamic Rendering
```typescript
// Opt out of caching
async function Page() {
  const data = await fetch('https://api.example.com/data', {
    cache: 'no-store'
  })
  return <div>{data}</div>
}
```

#### Time-based Revalidation
```typescript
async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // Revalidate every hour
  })
  return <div>{data}</div>
}
```

### Server Actions
```typescript
// app/actions.ts
"use server"

import { revalidatePath } from "next/cache"

export async function createPost(formData: FormData) {
  const title = formData.get("title") as string

  await db.posts.create({ data: { title } })

  revalidatePath("/posts")
}
```

```typescript
// app/posts/new/page.tsx
import { createPost } from "@/app/actions"

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

## Best Practices

### Performance
- Use Server Components by default
- Implement proper caching strategies
- Optimize images with `next/image`
- Use `next/font` for font optimization
- Implement streaming with Suspense boundaries

### Security
- Validate all inputs in Server Actions
- Use environment variables for secrets
- Implement proper authentication patterns
- Sanitize user-generated content

### Code Organization
- Colocate components with routes when possible
- Use route groups for logical organization
- Implement proper error boundaries
- Create reusable layout patterns

## Scripts

This skill includes executable scripts in the `scripts/` folder:

### Development
- **dev-server.sh**: Start the development server with hot reloading
  ```bash
  ./scripts/dev-server.sh [--port PORT] [--turbo]
  ```

- **build-production.sh**: Create optimized production build
  ```bash
  ./scripts/build-production.sh [--analyze]
  ```

- **analyze-bundle.sh**: Analyze bundle size and dependencies
  ```bash
  ./scripts/analyze-bundle.sh
  ```

### Code Generation
- **create-page.sh**: Generate a new page with optional layout/loading/error files
  ```bash
  ./scripts/create-page.sh <page-path> [--layout] [--loading] [--error]
  ```

- **create-api-route.sh**: Generate API route handlers
  ```bash
  ./scripts/create-api-route.sh <route-name> [--dynamic]
  ```

- **create-component.sh**: Generate React components with optional tests
  ```bash
  ./scripts/create-component.sh <name> [--client] [--test] [--dir DIR]
  ```

### Testing
- **setup-testing.sh**: Set up Jest and React Testing Library
  ```bash
  ./scripts/setup-testing.sh [--playwright]
  ```

- **run-tests.sh**: Run tests with various options
  ```bash
  ./scripts/run-tests.sh [--watch] [--coverage] [--file FILE]
  ```

## Templates

This skill includes production-ready templates in the `templates/` folder:

### Pages
- **page-server.tsx**: Server Component page with async data fetching, metadata, and Suspense streaming
- **page-client.tsx**: Client Component page with state management, hooks, and interactivity
- **page-dynamic.tsx**: Dynamic route page with params, generateStaticParams, and generateMetadata

### Components
- **component-server.tsx**: Server Component with data fetching and composition patterns
- **component-client.tsx**: Client Component with hooks, event handlers, and localStorage

### API & Backend
- **api-route.ts**: Complete API route handler with CRUD, validation (Zod), auth, and CORS
- **server-action.ts**: Server Actions with form handling, validation, and revalidation
- **middleware.ts**: Middleware with auth, rate limiting, i18n, and security headers

### Infrastructure
- **layout.tsx**: Root/nested layout with navigation, footer, metadata, and fonts
- **page.test.tsx**: Testing patterns for pages, components, API routes, and Server Actions

## Resources

This skill includes detailed reference guides in the `resources/` folder:

- **app-router-patterns.md**: Comprehensive App Router patterns and examples
- **data-fetching.md**: Data fetching strategies and caching
- **server-components.md**: Server vs Client Components guide
- **routing-reference.md**: Complete routing system reference
- **performance-optimization.md**: Performance best practices
- **api-routes.md**: API route handlers and patterns
- **testing-patterns.md**: Testing strategies for Next.js apps

---

**Specialization**: Next.js App Router Development
**Version**: 1.0
**Last Updated**: January 2026

---
name: nextjs-app-router-fundamentals
description: Guide for working with Next.js App Router (Next.js 13+). Use when migrating from Pages Router to App Router, creating layouts, implementing routing, handling metadata, or building Next.js 13+ applications. Activates for App Router migration, layout creation, routing patterns, or Next.js 13+ development tasks.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js App Router Fundamentals

## Overview

Provide comprehensive guidance for Next.js App Router (Next.js 13+), covering migration from Pages Router, file-based routing conventions, layouts, metadata handling, and modern Next.js patterns.

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

**❌ WRONG:**
```typescript
function handleSubmit(e: any) { ... }
const data: any[] = [];
```

**✅ CORRECT:**
```typescript
function handleSubmit(e: React.FormEvent<HTMLFormElement>) { ... }
const data: string[] = [];
```

### Common Next.js Type Patterns

```typescript
// Page props
function Page({ params }: { params: { slug: string } }) { ... }
function Page({ searchParams }: { searchParams: { [key: string]: string | string[] | undefined } }) { ... }

// Form events
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => { ... }
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => { ... }

// Server actions
async function myAction(formData: FormData) { ... }
```

## When to Use This Skill

Use this skill when:
- Migrating from Pages Router (`pages/` directory) to App Router (`app/` directory)
- Creating Next.js 13+ applications from scratch
- Working with layouts, templates, and nested routing
- Implementing metadata and SEO optimizations
- Building with App Router routing conventions
- Handling route groups, parallel routes, or intercepting routes basics

## Core Concepts

### App Router vs Pages Router

**Pages Router (Legacy - Next.js 12 and earlier):**
```
pages/
├── index.tsx              # Route: /
├── about.tsx              # Route: /about
├── _app.tsx               # Custom App component
├── _document.tsx          # Custom Document component
└── api/                   # API routes
    └── hello.ts           # API endpoint: /api/hello
```

**App Router (Modern - Next.js 13+):**
```
app/
├── layout.tsx             # Root layout (required)
├── page.tsx               # Route: /
├── about/                 # Route: /about
│   └── page.tsx
├── blog/
│   ├── layout.tsx         # Nested layout
│   └── [slug]/
│       └── page.tsx       # Dynamic route: /blog/:slug
└── api/                   # Route handlers
    └── hello/
        └── route.ts       # API endpoint: /api/hello
```

### File Conventions

**Special Files in App Router:**
- `layout.tsx` - Shared UI for a segment and its children (preserves state, doesn't re-render)
- `page.tsx` - Unique UI for a route, makes route publicly accessible
- `loading.tsx` - Loading UI with React Suspense
- `error.tsx` - Error UI with Error Boundaries
- `not-found.tsx` - 404 UI
- `template.tsx` - Similar to layout but re-renders on navigation
- `route.ts` - API endpoints (Route Handlers)

**Colocation:**
- Components, tests, and other files can be colocated in `app/`
- Only `page.tsx` and `route.ts` files create public routes
- Other files (components, utils, tests) are NOT routable

## Migration Guide: Pages Router to App Router

### Step 1: Understand the Current Structure

Examine existing Pages Router setup:
- Read `pages/` directory structure
- Identify `_app.tsx` - handles global state, layouts, providers
- Identify `_document.tsx` - customizes HTML structure
- Note metadata usage (`next/head`, `<Head>` component)
- List all routes and dynamic segments

### Step 2: Create Root Layout

Create `app/layout.tsx` - **REQUIRED** for all App Router applications:

```typescript
// app/layout.tsx
export const metadata = {
  title: 'My App',
  description: 'App description',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

**Migration Notes:**
- Move `_document.tsx` HTML structure to `layout.tsx`
- Move `_app.tsx` global providers/wrappers to `layout.tsx`
- Convert `<Head>` metadata to `metadata` export
- The root layout **MUST** include `<html>` and `<body>` tags

### Step 3: Migrate Pages to Routes

**Simple Page Migration:**
```typescript
// Before: pages/index.tsx
import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>Home Page</title>
      </Head>
      <main>
        <h1>Welcome</h1>
      </main>
    </>
  );
}
```

```typescript
// After: app/page.tsx
export default function Home() {
  return (
    <main>
      <h1>Welcome</h1>
    </main>
  );
}

// Metadata moved to layout.tsx or exported here
export const metadata = {
  title: 'Home Page',
};
```

**Nested Route Migration:**
```typescript
// Before: pages/blog/[slug].tsx
export default function BlogPost() { ... }
```

```typescript
// After: app/blog/[slug]/page.tsx
export default function BlogPost() { ... }
```

### Step 4: Update Navigation

Replace anchor tags with Next.js Link:

```typescript
// Before (incorrect in App Router)
<a href="/about">About</a>

// After (correct)
import Link from 'next/link';
<Link href="/about">About</Link>
```

### Step 5: Clean Up Pages Directory

After migration:
- Remove all page files from `pages/` directory
- Keep `pages/api/` if you're not migrating API routes yet
- Remove `_app.tsx` and `_document.tsx` (functionality moved to layout)
- Optionally delete empty `pages/` directory

## Metadata Handling

### Static Metadata

```typescript
// app/page.tsx or app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My Page',
  description: 'Page description',
  keywords: ['nextjs', 'react'],
  openGraph: {
    title: 'My Page',
    description: 'Page description',
    images: ['/og-image.jpg'],
  },
};
```

### Dynamic Metadata

```typescript
// app/blog/[slug]/page.tsx
export async function generateMetadata({
  params
}: {
  params: { slug: string }
}): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
  };
}
```

## Layouts and Nesting

### Creating Nested Layouts

```typescript
// app/layout.tsx - Root layout
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}

// app/blog/layout.tsx - Blog layout
export default function BlogLayout({ children }) {
  return (
    <div>
      <BlogSidebar />
      <main>{children}</main>
    </div>
  );
}
```

**Layout Behavior:**
- Layouts preserve state across navigation
- Layouts don't re-render on route changes
- Parent layouts wrap child layouts
- Root layout is required and wraps entire app

## Routing Patterns

### Dynamic Routes

```typescript
// app/blog/[slug]/page.tsx
export default function BlogPost({
  params
}: {
  params: { slug: string }
}) {
  return <article>Post: {params.slug}</article>;
}
```

### Catch-All Routes

```typescript
// app/shop/[...slug]/page.tsx - Matches /shop/a, /shop/a/b, etc.
export default function Shop({
  params
}: {
  params: { slug: string[] }
}) {
  return <div>Path: {params.slug.join('/')}</div>;
}
```

### Optional Catch-All

```typescript
// app/shop/[[...slug]]/page.tsx - Matches /shop AND /shop/a, /shop/a/b
```

### Route Groups

Group routes without affecting URL:

```
app/
├── (marketing)/
│   ├── about/
│   │   └── page.tsx      # /about
│   └── contact/
│       └── page.tsx      # /contact
└── (shop)/
    └── products/
        └── page.tsx      # /products
```

## Common Migration Pitfalls

### Pitfall 1: Forgetting Root Layout HTML Tags

**Wrong:**
```typescript
export default function RootLayout({ children }) {
  return <div>{children}</div>; // Missing <html> and <body>
}
```

**Correct:**
```typescript
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### Pitfall 2: Using `next/head` in App Router

**Wrong:**
```typescript
import Head from 'next/head';

export default function Page() {
  return (
    <>
      <Head><title>Title</title></Head>
      <main>Content</main>
    </>
  );
}
```

**Correct:**
```typescript
export const metadata = { title: 'Title' };

export default function Page() {
  return <main>Content</main>;
}
```

### Pitfall 3: Not Removing Pages Directory

After migrating routes, remove the old `pages/` directory files to avoid confusion. The build will fail if you have conflicting routes.

### Pitfall 4: Missing `page.tsx` Files

Routes are NOT accessible without a `page.tsx` file. Layouts alone don't create routes.

```
app/
├── blog/
│   ├── layout.tsx   # NOT a route
│   └── page.tsx     # This makes /blog accessible
```

### Pitfall 5: Incorrect Link Usage

**Wrong:**
```typescript
<a href="/about">About</a>  // Works but causes full page reload
```

**Correct:**
```typescript
import Link from 'next/link';
<Link href="/about">About</Link>  // Client-side navigation
```

## Server Components vs Client Components

### Default: Server Components

All components in `app/` are Server Components by default:

```typescript
// app/page.tsx - Server Component (default)
export default async function Page() {
  const data = await fetch('https://api.example.com/data');
  const json = await data.json();

  return <div>{json.title}</div>;
}
```

**Benefits:**
- Can use async/await directly
- Direct database/API access
- Zero client-side JavaScript
- Automatic code splitting

### Client Components

Use `'use client'` directive when you need:
- Interactive elements (onClick, onChange, etc.)
- React hooks (useState, useEffect, useContext, etc.)
- Browser APIs (window, localStorage, etc.)
- Event listeners

```typescript
// app/components/Counter.tsx
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

## Data Fetching Patterns

### Server Component Data Fetching

```typescript
// app/posts/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 } // Revalidate every hour
  });
  return res.json();
}

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Parallel Data Fetching

```typescript
export default async function Page() {
  // Fetch in parallel
  const [posts, users] = await Promise.all([
    fetch('https://api.example.com/posts').then(r => r.json()),
    fetch('https://api.example.com/users').then(r => r.json()),
  ]);

  return (/* render */);
}
```

## Static Site Generation with generateStaticParams

### Overview

`generateStaticParams` is the App Router equivalent of `getStaticPaths` from the Pages Router. It generates static pages at build time for dynamic routes.

### Basic Usage

```typescript
// app/blog/[id]/page.tsx
export async function generateStaticParams() {
  // Return array of params to pre-render
  return [
    { id: '1' },
    { id: '2' },
    { id: '3' },
  ];
}

export default function BlogPost({
  params
}: {
  params: { id: string }
}) {
  return <article>Blog post {params.id}</article>;
}
```

**Key Points:**
- Returns an array of objects with route parameter keys
- Each object represents one page to pre-render at build time
- Function must be exported and named `generateStaticParams`
- Works ONLY in Server Components (no `'use client'` directive)
- Replaces Pages Router's `getStaticPaths`

### Fetching Data for Static Params

```typescript
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json());

  return posts.map((post: { slug: string }) => ({
    slug: post.slug,
  }));
}

export default async function BlogPost({
  params
}: {
  params: { slug: string }
}) {
  const post = await fetch(`https://api.example.com/posts/${params.slug}`).then(r => r.json());

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

### Multiple Dynamic Segments

```typescript
// app/products/[category]/[id]/page.tsx
export async function generateStaticParams() {
  const categories = await getCategories();

  const params = [];
  for (const category of categories) {
    const products = await getProducts(category.slug);
    for (const product of products) {
      params.push({
        category: category.slug,
        id: product.id,
      });
    }
  }

  return params;
}

export default function ProductPage({
  params
}: {
  params: { category: string; id: string }
}) {
  return <div>Category: {params.category}, Product: {params.id}</div>;
}
```

### Dynamic Behavior Configuration

```typescript
// app/blog/[id]/page.tsx
export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }];
}

// Control behavior for non-pre-rendered paths
export const dynamicParams = true; // default - allows runtime generation
// export const dynamicParams = false; // returns 404 for non-pre-rendered paths

export default function BlogPost({
  params
}: {
  params: { id: string }
}) {
  return <article>Post {params.id}</article>;
}
```

**Options:**
- `dynamicParams = true` (default): Non-pre-rendered paths generated on-demand
- `dynamicParams = false`: Non-pre-rendered paths return 404

### Common Patterns

**Pattern 1: Simple ID-based routes**
```typescript
export async function generateStaticParams() {
  return [
    { id: '1' },
    { id: '2' },
    { id: '3' },
  ];
}
```

**Pattern 2: Fetch from API**
```typescript
export async function generateStaticParams() {
  const items = await fetch('https://api.example.com/items').then(r => r.json());
  return items.map(item => ({ id: item.id }));
}
```

**Pattern 3: Database query**
```typescript
export async function generateStaticParams() {
  const posts = await db.post.findMany();
  return posts.map(post => ({ slug: post.slug }));
}
```

### Migration from Pages Router

**Before (Pages Router):**
```typescript
// pages/blog/[id].tsx
export async function getStaticPaths() {
  return {
    paths: [
      { params: { id: '1' } },
      { params: { id: '2' } },
    ],
    fallback: false,
  };
}

export async function getStaticProps({ params }) {
  return { props: { id: params.id } };
}
```

**After (App Router):**
```typescript
// app/blog/[id]/page.tsx
export async function generateStaticParams() {
  return [
    { id: '1' },
    { id: '2' },
  ];
}

export const dynamicParams = false; // equivalent to fallback: false

export default function BlogPost({ params }: { params: { id: string } }) {
  return <div>Post {params.id}</div>;
}
```

### Common Mistakes to Avoid

**❌ Wrong: Using `'use client'`**
```typescript
'use client'; // ERROR! generateStaticParams only works in Server Components

export async function generateStaticParams() {
  return [{ id: '1' }];
}
```

**❌ Wrong: Using Pages Router pattern**
```typescript
export async function getStaticPaths() { // Wrong API!
  return { paths: [...], fallback: false };
}
```

**❌ Wrong: Missing export keyword**
```typescript
async function generateStaticParams() { // Must be exported!
  return [{ id: '1' }];
}
```

**✅ Correct: Clean Server Component**
```typescript
// app/blog/[id]/page.tsx
// No 'use client' directive

export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }];
}

export default function Page({ params }: { params: { id: string } }) {
  return <div>Post {params.id}</div>;
}
```

**CRITICAL IMPLEMENTATION NOTE:**

When asked to "write" or "implement" `generateStaticParams`:
- **DO** use the Edit or Write tool to modify the actual file
- **DO** add the function to the existing page.tsx file
- **DO** remove any TODO comments about generateStaticParams
- **DON'T** just output code in markdown - actually implement it
- **DON'T** show code without writing it to the file

## Testing and Validation

When migrating or building with App Router, verify:

1. **Structure:**
   - `app/` directory exists
   - Root `layout.tsx` exists with `<html>` and `<body>`
   - Each route has a `page.tsx` file

2. **Metadata:**
   - No `next/head` imports in App Router
   - Metadata exported from pages or layouts
   - Metadata properly typed with `Metadata` type

3. **Navigation:**
   - Using `Link` component from `next/link`
   - Not using plain `<a>` tags for internal navigation

4. **Cleanup:**
   - No remaining page files in `pages/` directory
   - `_app.tsx` and `_document.tsx` removed
   - Old metadata patterns removed

## Quick Reference

### File Structure Mapping

| Pages Router | App Router | Purpose |
|-------------|-----------|---------|
| `pages/index.tsx` | `app/page.tsx` | Home route |
| `pages/about.tsx` | `app/about/page.tsx` | About route |
| `pages/[id].tsx` | `app/[id]/page.tsx` | Dynamic route |
| `pages/_app.tsx` | `app/layout.tsx` | Global layout |
| `pages/_document.tsx` | `app/layout.tsx` | HTML structure |
| `pages/api/hello.ts` | `app/api/hello/route.ts` | API route |

### Common Commands

```bash
# Create new Next.js app with App Router
npx create-next-app@latest my-app

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Additional Resources

For more advanced routing patterns (parallel routes, intercepting routes, route handlers), refer to the `nextjs-advanced-routing` skill.

For Server vs Client component best practices and anti-patterns, refer to the `nextjs-server-client-components` and `nextjs-anti-patterns` skills.

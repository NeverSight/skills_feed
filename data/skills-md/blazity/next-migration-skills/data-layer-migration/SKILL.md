---
name: data-layer-migration
description: >
  Use when migrating getStaticProps, getServerSideProps, getStaticPaths,
  or API routes (pages/api/) to App Router equivalents. Also use when
  fixing stale data, cache behavior, or fetch errors in migrated pages.
---

# Data Layer Migration

Migrate data-fetching patterns (getStaticProps, getServerSideProps, getStaticPaths) and API routes to App Router equivalents.

## Toolkit Setup

This skill requires the `nextjs-migration-toolkit` skill to be installed. All migration skills depend on it for AST analysis.

```bash
TOOLKIT_DIR="$(cd "$(dirname "$SKILL_PATH")/../nextjs-migration-toolkit" && pwd)"
if [ ! -f "$TOOLKIT_DIR/package.json" ]; then
  echo "ERROR: nextjs-migration-toolkit is not installed." >&2
  echo "Run: npx skills add blazity/next-migration-skills -s nextjs-migration-toolkit" >&2
  echo "Then retry this skill." >&2
  exit 1
fi
bash "$TOOLKIT_DIR/scripts/setup.sh" >/dev/null
```

## Version-Specific Patterns

Before applying any migration patterns, check the target Next.js version. Read `.migration/target-version.txt` if it exists, or ask the user.

Then read the corresponding version patterns file:

```bash
SKILL_DIR="$(cd "$(dirname "$SKILL_PATH")" && pwd)"
cat "$SKILL_DIR/../version-patterns/nextjs-<version>.md"
```

**Critical version differences that affect data-layer migration:**
- **Next.js 14**: `cookies()` and `headers()` are SYNCHRONOUS — do NOT use `await`
- **Next.js 15+**: `cookies()` and `headers()` are ASYNC — MUST use `await`
- **Next.js 14**: fetch is cached by default — use `{ cache: 'no-store' }` for SSR replacement
- **Next.js 15+**: fetch is NOT cached by default — SSR replacement needs no cache option

The examples below show Next.js 15+ patterns with `await`. If targeting Next.js 14, remove the `await` from `cookies()` and `headers()` calls.

## Steps

### 1. Analyze Data Fetching Patterns

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform data-fetching <sourceFile>
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze routes <pagesDir>
```

### 2. Migrate getStaticProps

**Before:**
```tsx
import { GetStaticProps } from 'next';

export const getStaticProps: GetStaticProps = async () => {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();
  return { props: { posts }, revalidate: 60 };
};

export default function BlogPage({ posts }) {
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

**After** (`app/blog/page.tsx`):
```tsx
export default async function BlogPage() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 },
  }).then(r => r.json());

  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

Rules:
- Component is `async` — data fetching happens in the body
- No revalidate: `{ cache: 'force-cache' }` (the default in App Router)
- With revalidate: `{ next: { revalidate: <seconds> } }`
- Remove the getStaticProps export entirely
- No props indirection — fetch result goes straight to JSX

### 3. Migrate getServerSideProps

**Before:**
```tsx
import { GetServerSideProps } from 'next';

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { slug } = context.params;
  const token = context.req.cookies.token;
  const res = await fetch(`https://api.example.com/posts/${slug}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const post = await res.json();
  return { props: { post } };
};

export default function PostPage({ post }) {
  return <article><h1>{post.title}</h1><p>{post.content}</p></article>;
}
```

**After** (`app/blog/[slug]/page.tsx`):
```tsx
import { cookies } from 'next/headers';

export default async function PostPage({ params }: { params: { slug: string } }) {
  const cookieStore = await cookies();
  const token = cookieStore.get('token')?.value;
  const post = await fetch(`https://api.example.com/posts/${params.slug}`, {
    cache: 'no-store',
    headers: { Authorization: `Bearer ${token}` },
  }).then(r => r.json());

  return <article><h1>{post.title}</h1><p>{post.content}</p></article>;
}
```

Rules:
- `context.params` → `params` prop on the page component
- `context.query` → `searchParams` prop
- `context.req.cookies` → `cookies()` from `next/headers`
- `context.req.headers` → `headers()` from `next/headers`
- Always use `{ cache: 'no-store' }` to match getServerSideProps behavior

### 4. Migrate getStaticPaths

**Before:**
```tsx
import { GetStaticPaths, GetStaticProps } from 'next';

export const getStaticPaths: GetStaticPaths = async () => {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();
  return {
    paths: posts.map((p) => ({ params: { slug: p.slug } })),
    fallback: 'blocking',
  };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const post = await fetch(`https://api.example.com/posts/${params.slug}`).then(r => r.json());
  return { props: { post } };
};
```

**After** (`app/blog/[slug]/page.tsx`):
```tsx
export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json());
  return posts.map((p) => ({ slug: p.slug }));
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await fetch(`https://api.example.com/posts/${params.slug}`).then(r => r.json());
  return <article><h1>{post.title}</h1></article>;
}
```

Rules:
- Return flat param objects (not wrapped in `{ params: {} }`)
- `fallback: 'blocking'` / `fallback: true` → handled automatically by App Router (add `loading.tsx` for a loading UI)
- `fallback: false` → unconverted paths will 404 by default

### 5. Migrate API Routes

**Before** (`pages/api/posts.ts`):
```tsx
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { title, content } = req.body;
    const post = await db.posts.create({ title, content });
    return res.status(201).json(post);
  }
  const posts = await db.posts.findMany();
  return res.status(200).json(posts);
}
```

**After** (`app/api/posts/route.ts`):
```tsx
import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  const posts = await db.posts.findMany();
  return NextResponse.json(posts);
}

export async function POST(request: NextRequest) {
  const { title, content } = await request.json();
  const post = await db.posts.create({ title, content });
  return NextResponse.json(post, { status: 201 });
}
```

Rules:
- One file per route, named `route.ts` (not the handler name)
- Separate named exports per HTTP method (GET, POST, PUT, DELETE, PATCH)
- `req.body` → `await request.json()`
- `res.status(N).json(data)` → `NextResponse.json(data, { status: N })`
- `res.redirect(url)` → `NextResponse.redirect(new URL(url, request.url))`

### 6. Validate Data Layer

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" validate <appDir>
```

Verify no old data-fetching patterns remain in app/ directory.

## Common Pitfalls

### Forgetting `{ cache: 'no-store' }` on getServerSideProps replacements
**Symptom**: Page shows stale data or behaves like a static page.
**Cause**: App Router defaults to `{ cache: 'force-cache' }`. Without `{ cache: 'no-store' }`, the fetch result is cached at build time — the opposite of getServerSideProps behavior.
**Fix**: Always add `{ cache: 'no-store' }` when replacing getServerSideProps.

### Using `req` / `res` objects in route handlers
**Error**: `req is not defined` or type errors on NextApiRequest.
**Cause**: App Router route handlers use `NextRequest` (Web API based), not `NextApiRequest` (Node.js based).
**Fix**: Replace `req.body` → `await request.json()`, `req.query` → `request.nextUrl.searchParams`, `res.json()` → `NextResponse.json()`.

### Async cookies() and headers()
**Error**: `cookies()` or `headers()` returning a Promise instead of the value directly.
**Cause**: In Next.js 15+, `cookies()` and `headers()` are async. In Next.js 13-14, they were synchronous.
**Fix**: Use `const cookieStore = await cookies()` and then `cookieStore.get('name')`.

### Mixing getStaticProps and getServerSideProps patterns
**Wrong**: Using `{ cache: 'force-cache' }` with dynamic data that changes on every request.
**Right**: Match the caching strategy to the original behavior:
- getStaticProps (no revalidate) → `{ cache: 'force-cache' }` or omit (default)
- getStaticProps (with revalidate) → `{ next: { revalidate: N } }`
- getServerSideProps → `{ cache: 'no-store' }`

### Route handler returning wrong type
**Error**: Route handlers must return a `Response` object.
**Fix**: Always return `NextResponse.json(data)`, `NextResponse.redirect()`, or `new Response(body)`. Don't return plain objects.

### Converting server data fetching into client-side useEffect + fetch
**Wrong**: The page had `getServerSideProps` that fetched data. You make the page `'use client'` and replace the data fetching with `useEffect`:
```tsx
// WRONG — data only appears after JS executes on the client
'use client';
import { useState, useEffect } from 'react';

export default function Page() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch('/api/data').then(r => r.json()).then(setData);
  }, []);
  if (!data) return <p>Loading...</p>;
  return <div>{data.value}</div>;
}
```
**Right**: Keep data fetching in an async server component. Only extract interactive UI into a client component.
```tsx
// app/page.tsx (server component)
export default async function Page() {
  const data = await fetch('https://api.example.com/data', { cache: 'no-store' }).then(r => r.json());
  return <div>{data.value}</div>;
}
```
**Rule**: NEVER replace `getServerSideProps` or `getStaticProps` with `useEffect` + `fetch` in a client component. The data fetching MUST remain server-side in an async server component. The only reason to add `'use client'` is for interactive UI (hooks, event handlers), and that component receives already-fetched data as props.

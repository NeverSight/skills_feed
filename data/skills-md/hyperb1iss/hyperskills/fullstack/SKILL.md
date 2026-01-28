---
name: fullstack
description: Use this skill when building web applications, React components, Next.js apps, APIs, databases, or doing rapid prototyping. Activates on mentions of React, Next.js, TypeScript, Node.js, Express, Fastify, PostgreSQL, MongoDB, Prisma, Drizzle, tRPC, REST API, GraphQL, authentication, server components, client components, SSR, SSG, ISR, or general web development.
---

# Fullstack Development

Build modern web applications with React 19, Next.js 15+, and server-first architecture.

## Quick Reference

### React 19 + Next.js 15 Patterns

**Server Components (Default)**

```tsx
// app/page.tsx - Server Component by default
export default async function Page() {
  const data = await db.query("SELECT * FROM posts"); // Direct DB access
  return <PostList posts={data} />;
}
```

**Client Components (Opt-in)**

```tsx
"use client";
// Only for interactivity: useState, useEffect, event handlers
export function LikeButton({ postId }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>Like</button>;
}
```

**Server Actions**

```tsx
"use server";
export async function createPost(formData: FormData) {
  const title = formData.get("title");
  await db.insert(posts).values({ title });
  revalidatePath("/posts");
}
```

### React Compiler (Auto-Memoization)

Enable in `next.config.js`:

```js
module.exports = {
  experimental: {
    reactCompiler: true,
  },
};
```

**No more manual memoization** - the compiler handles `useMemo`, `useCallback`, `React.memo` automatically.

### State Management Stack

| Need                | Solution              |
| ------------------- | --------------------- |
| Server state        | TanStack Query        |
| Global client state | Zustand               |
| Atomic state        | Jotai                 |
| Form state          | React Hook Form + Zod |
| URL state           | nuqs                  |

**TanStack Query for Server State**

```tsx
const { data, isLoading } = useQuery({
  queryKey: ["posts"],
  queryFn: () => fetch("/api/posts").then((r) => r.json()),
});
```

**Zustand for Client State**

```tsx
const useStore = create((set) => ({
  theme: "dark",
  setTheme: (theme) => set({ theme }),
}));
```

### Component Libraries (2026)

**Recommended Stack:**

- **shadcn/ui** - Copy-paste components, full control
- **Base UI** - Unstyled primitives (replacing Radix)
- **Tailwind CSS v4** - Utility-first styling

### Database Patterns

**Drizzle ORM** (Type-safe, lightweight)

```tsx
const posts = await db.select().from(postsTable).where(eq(postsTable.authorId, userId));
```

**Prisma** (DX-focused, migrations)

```tsx
const posts = await prisma.post.findMany({ where: { authorId: userId } });
```

### Performance Imperatives

1. **Eliminate waterfalls** - Use `Promise.all()` for parallel fetches
2. **Stream with Suspense** - Progressive rendering
3. **Minimize 'use client'** - Every directive increases bundle
4. **Use Route Segment Config** - `dynamic`, `revalidate` options

### Core Web Vitals Targets

- **LCP** < 2.5s (Largest Contentful Paint)
- **INP** < 200ms (Interaction to Next Paint)
- **CLS** < 0.1 (Cumulative Layout Shift)

## Agents

- **frontend-developer** - React, styling, components, performance
- **backend-architect** - APIs, auth, system design
- **rapid-prototyper** - MVPs in days, not weeks
- **database-specialist** - Schema, queries, migrations, optimization

## Deep Dives

- [references/react-19-patterns.md](references/react-19-patterns.md)
- [references/nextjs-app-router.md](references/nextjs-app-router.md)
- [references/state-management.md](references/state-management.md)
- [references/database-patterns.md](references/database-patterns.md)

## Examples

- [examples/nextjs-app-starter/](examples/nextjs-app-starter/)
- [examples/trpc-stack/](examples/trpc-stack/)
- [examples/auth-patterns/](examples/auth-patterns/)

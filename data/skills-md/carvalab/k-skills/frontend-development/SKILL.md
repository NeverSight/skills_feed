---
name: frontend-development
description: Next.js App Router development with TypeScript. Server Components, Server Actions, caching, MUI. Use when creating pages, components, fetching data, or building features.
tools: Read, Edit, Write, Bash
model: opus
---

# Frontend Development

Next.js (latest) App Router with TypeScript. Server-first architecture.

> **Related Skills**:
> - `vercel-react-best-practices` - **USE THIS** for performance (bundle size, waterfalls, caching, re-renders, memoization)
> - Check `.claude/CLAUDE.md` for project-specific conventions
> - Check `.cursor/rules/*` for project-specific conventions
>
> **MCP**: Use `next-devtools` MCP server if available for debugging, route inspection, and build analysis.

## Quick Start

| Task | Pattern |
|------|---------|
| New page | Server Component by default |
| Data fetching | Server Component async fetch |
| Mutations | Server Actions + Zod + revalidatePath |
| Styling | MUI `sx` prop, inline if <100 lines |
| State | Server = fetch, Client = useState only when needed |

## Core Principles

1. **Server by Default**: Components are Server Components unless they need `useState`/`useEffect`/events
2. **Server Actions for Mutations**: Replace API routes for internal app logic
3. **Opt-in Caching**: Use `'use cache'` directive for explicit caching
4. **Minimal Client JS**: Keep `'use client'` components small and leaf-level
5. **Type Everything**: Strict TypeScript, Zod for runtime validation

> **Performance**: For bundle optimization, waterfalls, memoization, see `vercel-react-best-practices`

## Server vs Client Decision

```
Need useState/useEffect/onClick? → 'use client'
Need browser APIs (localStorage)? → 'use client'
Just rendering data? → Server Component (default)
```

**Rule**: Keep Client Components small. Most of tree stays server-rendered.

## Data Fetching Pattern

```typescript
// app/users/page.tsx - Server Component (default)
export default async function UsersPage() {
    const users = await db.user.findMany();  // Runs on server
    return <UserList users={users} />;
}
```

**No TanStack Query needed** - Server Components handle data fetching natively.

## Server Actions Pattern

```typescript
// app/actions.ts
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const schema = z.object({ title: z.string().min(1) });

export async function createPost(formData: FormData) {
    const parsed = schema.safeParse({ title: formData.get('title') });
    if (!parsed.success) return { error: parsed.error.flatten() };

    await db.post.create({ data: parsed.data });
    revalidatePath('/posts');
    return { success: true };
}
```

**When to use Server Actions vs API Routes:**
- Server Actions → Internal mutations, form submissions
- Route Handlers → Public APIs, webhooks, large uploads, streaming

## Critical Rules

### Never
```typescript
// ❌ Large 'use client' at top of tree
'use client';  // Marks entire subtree as client

// ❌ Expose secrets to client
const apiKey = process.env.SECRET_KEY;  // In client component

// ❌ Old MUI Grid syntax
<Grid xs={12} md={6}>
```

### Always
```typescript
// ✅ Small leaf-level client components
// ✅ Validate Server Action inputs with Zod
// ✅ MUI Grid size prop
<Grid size={{ xs: 12, md: 6 }}>
```

## File Conventions

```
app/
├── layout.tsx          # Root layout (Server)
├── page.tsx            # Home page
├── loading.tsx         # Loading UI (Suspense fallback)
├── error.tsx           # Error boundary ('use client')
├── not-found.tsx       # 404 page
├── users/
│   ├── page.tsx        # /users
│   ├── [id]/
│   │   └── page.tsx    # /users/:id
│   └── actions.ts      # Server Actions
└── api/
    └── webhook/
        └── route.ts    # Route Handler (public API)
```

## Common Workflows

### New Feature
1. Create `app/{route}/page.tsx` (Server Component)
2. Add `loading.tsx` for Suspense boundary
3. Create Server Actions in `actions.ts`
4. Add Client Components only where needed

### Performance Issue
→ **Run `vercel-react-best-practices` skill** for optimization rules

### Styling Component
1. Use MUI `sx` prop with `SxProps<Theme>`
2. Inline styles if <100 lines, separate `.styles.ts` if >100
3. Grid: `size={{ xs: 12, md: 6 }}`

## References

| Reference | When to Use |
|-----------|-------------|
| `references/nextjs.md` | App Router, RSC, Server Actions, caching |
| `references/component-patterns.md` | React.FC, hooks order, dialogs, forms |
| `references/styling.md` | MUI sx prop, Grid, theming |
| `references/typescript.md` | Types, generics, Zod validation |
| `references/project-structure.md` | features/ vs components/, organization |

**Performance/Optimization** → `vercel-react-best-practices` skill

## Technology Stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js (App Router, latest) |
| Type Safety | TypeScript (strict) + Zod |
| Data Fetching | Server Components (async) |
| Mutations | Server Actions + revalidatePath |
| Client State | useState (minimal) |
| Styling | MUI (latest) |
| Forms | Server Actions + useActionState |

**Note**: TanStack Query only if you need real-time polling or complex optimistic updates. See `references/data-fetching.md`.

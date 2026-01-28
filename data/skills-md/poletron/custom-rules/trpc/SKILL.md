---
name: trpc
description: >
  Guidelines for writing Next.js apps with tRPC v11.
  Trigger: When building type-safe APIs with tRPC.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with trpc"

## When to Use

Use this skill when:
- Building full-stack TypeScript apps with Next.js
- Need end-to-end type safety without schemas or code generation
- Creating APIs without REST/GraphQL overhead
- Using React Query for data fetching

---

## Critical Patterns

### Project Structure (REQUIRED)

```
.
├── src
│   ├── pages
│   │   ├── _app.tsx  # add `createTRPCNext` setup here
│   │   ├── api
│   │   │   └── trpc
│   │   │       └── [trpc].ts  # tRPC HTTP handler
│   │   ├── server
│   │   │   ├── routers
│   │   │   │   ├── _app.ts  # main app router
│   │   │   │   ├── [feature].ts  # feature-specific routers
│   │   │   │   └── [...]
│   │   │   ├── context.ts   # create app context
│   │   │   └── trpc.ts      # procedure helpers
│   │   └── utils
│   │       └── trpc.ts  # typesafe tRPC hooks
```

### Server-Side Setup (REQUIRED)

```typescript
// server/trpc.ts - Initialize backend (once per backend)
import { initTRPC } from '@trpc/server';

const t = initTRPC.create();

export const router = t.router;
export const publicProcedure = t.procedure;
```

### Router Definition (REQUIRED)

```typescript
// server/routers/_app.ts
import { z } from 'zod';
import { router, publicProcedure } from '../trpc';

export const appRouter = router({
  greeting: publicProcedure
    .input(z.object({ name: z.string() }))
    .query(({ input }) => {
      return `Hello ${input.name}`;
    }),
});

// Export type definition, NOT the router itself!
export type AppRouter = typeof appRouter;
```

### Client-Side Setup (REQUIRED)

```typescript
// utils/trpc.ts
import { httpBatchLink } from '@trpc/client';
import { createTRPCNext } from '@trpc/next';
import type { AppRouter } from '../server/routers/_app';

function getBaseUrl() {
  if (typeof window !== 'undefined') return '';
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return `http://localhost:${process.env.PORT ?? 3000}`;
}

export const trpc = createTRPCNext<AppRouter>({
  config() {
    return {
      links: [
        httpBatchLink({
          url: `${getBaseUrl()}/api/trpc`,
        }),
      ],
    };
  },
  ssr: false,
});
```

---

## Decision Tree

```
Need public endpoint?      → Use publicProcedure
Need auth?                 → Use protectedProcedure with middleware
Need validation?           → Use Zod in .input()
Need caching?              → Use React Query options
Need complex types?        → Use SuperJSON transformer
```

---

## Code Examples

### Organize Routers by Feature

```typescript
// server/routers/user.ts
export const userRouter = router({
  list: publicProcedure.query(() => { /* ... */ }),
  byId: publicProcedure.input(z.string()).query(({ input }) => { /* ... */ }),
  create: publicProcedure.input(/* ... */).mutation(({ input }) => { /* ... */ }),
});

// server/routers/_app.ts
import { userRouter } from './user';
import { postRouter } from './post';

export const appRouter = router({
  user: userRouter,
  post: postRouter,
});
```

### Middleware for Auth

```typescript
const isAuthed = t.middleware(({ next, ctx }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({ ctx: { user: ctx.user } });
});

const protectedProcedure = t.procedure.use(isAuthed);
```

### Error Handling

```typescript
import { TRPCError } from '@trpc/server';

publicProcedure
  .input(z.string())
  .query(({ input }) => {
    const user = getUserById(input);
    if (!user) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: `User with id ${input} not found`,
      });
    }
    return user;
  });
```

### Data Transformers (SuperJSON)

```typescript
import { initTRPC } from '@trpc/server';
import superjson from 'superjson';

const t = initTRPC.create({
  transformer: superjson,
});
```

### React Query Integration

```tsx
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = trpc.user.byId.useQuery(userId);
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{data.name}</div>;
}
```

### Context Creation

```typescript
// server/context.ts
import { inferAsyncReturnType } from '@trpc/server';
import * as trpcNext from '@trpc/server/adapters/next';

export async function createContext({
  req, res,
}: trpcNext.CreateNextContextOptions) {
  const user = await getUser(req);
  return { req, res, prisma, user };
}

export type Context = inferAsyncReturnType<typeof createContext>;
```

### Procedure Types

```typescript
export const publicProcedure = t.procedure;
export const protectedProcedure = t.procedure.use(isAuthed);
export const adminProcedure = t.procedure.use(isAdmin);
```

### Performance: Batching & Prefetching

```typescript
// Client batching
httpBatchLink({
  url: `${getBaseUrl()}/api/trpc`,
  maxURLLength: 2083,
})

// Prefetching in Next.js
export async function getStaticProps() {
  const ssg = createServerSideHelpers({
    router: appRouter,
    ctx: {},
  });
  
  await ssg.post.byId.prefetch('1');
  
  return {
    props: { trpcState: ssg.dehydrate() },
    revalidate: 1,
  };
}
```

---

## Version Compatibility

- tRPC v11
- TypeScript >= 5.7.2
- Strict mode required (`"strict": true`)

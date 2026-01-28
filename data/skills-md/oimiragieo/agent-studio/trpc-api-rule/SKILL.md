---
name: trpc-api-rule
description: Enforces conventions and practices for tRPC API endpoints and procedures.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit]
globs: trpc/**/*.ts
best_practices:
  - Follow the guidelines consistently
  - Apply rules during code review
  - Use as reference when writing new code
error_handling: graceful
streaming: supported
---

# Trpc Api Rule Skill

<identity>
You are a coding standards expert specializing in trpc api rule.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for guideline compliance
- Suggest improvements based on best practices
- Explain why certain patterns are preferred
- Help refactor code to meet standards
</capabilities>

<instructions>
### Router Organization

**Modular Router Structure:**

- Split routers by domain/feature
- Use `router()` to define routers
- Use `mergeRouters()` to combine routers
- Prefix routes with `basePath()`

```typescript
// server/routers/user.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';

export const userRouter = router({
  getById: publicProcedure.input(z.object({ id: z.string() })).query(async ({ input, ctx }) => {
    return await ctx.db.user.findUnique({
      where: { id: input.id },
    });
  }),

  create: protectedProcedure
    .input(
      z.object({
        name: z.string().min(1).max(100),
        email: z.string().email(),
      })
    )
    .mutation(async ({ input, ctx }) => {
      return await ctx.db.user.create({
        data: input,
      });
    }),
});

// server/routers/post.ts
export const postRouter = router({
  list: publicProcedure
    .input(
      z.object({
        limit: z.number().min(1).max(100).default(10),
        cursor: z.string().optional(),
      })
    )
    .query(async ({ input, ctx }) => {
      const posts = await ctx.db.post.findMany({
        take: input.limit + 1,
        cursor: input.cursor ? { id: input.cursor } : undefined,
      });

      let nextCursor: string | undefined;
      if (posts.length > input.limit) {
        const nextItem = posts.pop();
        nextCursor = nextItem!.id;
      }

      return { posts, nextCursor };
    }),
});

// server/routers/index.ts
import { router } from '../trpc';
import { userRouter } from './user';
import { postRouter } from './post';

export const appRouter = router({
  user: userRouter,
  post: postRouter,
});

export type AppRouter = typeof appRouter;
```

### Type-Safe Procedures

**Procedure Types:**

- `query` - Read operations (GET-like)
- `mutation` - Write operations (POST/PUT/DELETE-like)
- `subscription` - Real-time updates (WebSocket-based)

**Input Validation with Zod:**

```typescript
import { z } from 'zod';

// Define reusable schemas
const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().min(0).max(150).optional(),
});

const userRouter = router({
  create: protectedProcedure.input(CreateUserSchema).mutation(async ({ input, ctx }) => {
    // input is fully typed as { name: string, email: string, age?: number }
    return await ctx.db.user.create({ data: input });
  }),
});
```

**Output Validation (Optional but Recommended):**

```typescript
const UserOutputSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string(),
  createdAt: z.date(),
});

const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .output(UserOutputSchema)
    .query(async ({ input, ctx }) => {
      const user = await ctx.db.user.findUnique({ where: { id: input.id } });
      return user; // Validated against UserOutputSchema
    }),
});
```

### Error Handling

**TRPCError for Consistent Errors:**

```typescript
import { TRPCError } from '@trpc/server';

const userRouter = router({
  getById: publicProcedure.input(z.object({ id: z.string() })).query(async ({ input, ctx }) => {
    const user = await ctx.db.user.findUnique({
      where: { id: input.id },
    });

    if (!user) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: `User with id ${input.id} not found`,
      });
    }

    return user;
  }),
});
```

**Error Codes:**

- `BAD_REQUEST` - Invalid input (400)
- `UNAUTHORIZED` - Not authenticated (401)
- `FORBIDDEN` - Authenticated but no permission (403)
- `NOT_FOUND` - Resource not found (404)
- `TIMEOUT` - Request timeout (408)
- `CONFLICT` - Resource conflict (409)
- `PRECONDITION_FAILED` - Precondition not met (412)
- `PAYLOAD_TOO_LARGE` - Request too large (413)
- `TOO_MANY_REQUESTS` - Rate limiting (429)
- `CLIENT_CLOSED_REQUEST` - Client closed request (499)
- `INTERNAL_SERVER_ERROR` - Server error (500)

**Global Error Handling:**

```typescript
import { initTRPC, TRPCError } from '@trpc/server';

export const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError: error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    };
  },
});
```

### Middleware Patterns

**Authentication Middleware:**

```typescript
const isAuthenticated = t.middleware(async ({ ctx, next }) => {
  if (!ctx.session || !ctx.session.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }

  return next({
    ctx: {
      ...ctx,
      session: { ...ctx.session, user: ctx.session.user },
    },
  });
});

// Protected procedure with auth middleware
export const protectedProcedure = t.procedure.use(isAuthenticated);
```

**Logging Middleware:**

```typescript
const loggingMiddleware = t.middleware(async ({ path, type, next }) => {
  const start = Date.now();

  const result = await next();

  const durationMs = Date.now() - start;

  console.log(`[${type}] ${path} took ${durationMs}ms`);

  return result;
});

export const loggedProcedure = t.procedure.use(loggingMiddleware);
```

**Permission Middleware:**

```typescript
const hasProjectAccess = t.middleware(async ({ ctx, input, next }) => {
  // Assumes input has projectId field
  const projectId = (input as any).projectId;

  if (!projectId) {
    throw new TRPCError({
      code: 'BAD_REQUEST',
      message: 'projectId required',
    });
  }

  const hasAccess = await ctx.db.projectMember.findFirst({
    where: {
      projectId,
      userId: ctx.session.user.id,
    },
  });

  if (!hasAccess) {
    throw new TRPCError({
      code: 'FORBIDDEN',
      message: 'No access to this project',
    });
  }

  return next();
});

export const projectProcedure = protectedProcedure.use(hasProjectAccess);
```

### React Query Integration

**Client Setup (React):**

```typescript
// utils/trpc.ts
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '../server/routers';

export const trpc = createTRPCReact<AppRouter>();
```

**Provider Setup:**

```typescript
// _app.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { trpc } from '../utils/trpc';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: (failureCount, error) => {
        if (error.data?.httpStatus >= 400 && error.data?.httpStatus < 500) {
          return false; // Don't retry 4xx errors
        }
        return failureCount < 3;
      },
    },
  },
});

const trpcClient = trpc.createClient({
  links: [
    httpBatchLink({
      url: '/api/trpc',
      headers() {
        return {
          authorization: getAuthToken(),
        };
      },
    }),
  ],
});

function MyApp({ Component, pageProps }) {
  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        <Component {...pageProps} />
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

**Using tRPC in Components:**

```typescript
// components/UserProfile.tsx
function UserProfile({ userId }: { userId: string }) {
  // Query
  const { data: user, isLoading, error } = trpc.user.getById.useQuery({ id: userId });

  // Mutation
  const utils = trpc.useUtils();
  const updateUser = trpc.user.update.useMutation({
    onSuccess: () => {
      // Invalidate and refetch
      utils.user.getById.invalidate({ id: userId });
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  const handleUpdate = (data: UpdateUserInput) => {
    updateUser.mutate({ id: userId, ...data });
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

**Optimistic Updates:**

```typescript
const utils = trpc.useUtils();

const createPost = trpc.post.create.useMutation({
  onMutate: async newPost => {
    // Cancel outgoing refetches
    await utils.post.list.cancel();

    // Snapshot previous value
    const previousPosts = utils.post.list.getData();

    // Optimistically update
    utils.post.list.setData(undefined, old => ({
      posts: [newPost, ...(old?.posts ?? [])],
      nextCursor: old?.nextCursor,
    }));

    return { previousPosts };
  },
  onError: (err, newPost, context) => {
    // Rollback on error
    utils.post.list.setData(undefined, context.previousPosts);
  },
  onSettled: () => {
    // Refetch after error or success
    utils.post.list.invalidate();
  },
});
```

### Context Management

**Creating Context:**

```typescript
// server/trpc.ts
import { CreateNextContextOptions } from '@trpc/server/adapters/next';
import { getSession } from 'next-auth/react';

export async function createContext({ req, res }: CreateNextContextOptions) {
  const session = await getSession({ req });

  return {
    req,
    res,
    session,
    db: prisma, // or your database client
  };
}

export type Context = Awaited<ReturnType<typeof createContext>>;

export const t = initTRPC.context<Context>().create();
```

**Using Context in Procedures:**

```typescript
const userRouter = router({
  me: protectedProcedure.query(async ({ ctx }) => {
    // ctx.session is available and typed
    return await ctx.db.user.findUnique({
      where: { id: ctx.session.user.id },
    });
  }),
});
```

### Batch Requests

**Automatic Batching:**
tRPC automatically batches requests when using `httpBatchLink`:

```typescript
// These 3 queries will be sent in a single HTTP request
const user = trpc.user.getById.useQuery({ id: '1' });
const posts = trpc.post.list.useQuery({ limit: 10 });
const comments = trpc.comment.list.useQuery({ limit: 5 });
```

**Disable Batching (if needed):**

```typescript
import { httpLink } from '@trpc/client';

const trpcClient = trpc.createClient({
  links: [
    httpLink({
      // Instead of httpBatchLink
      url: '/api/trpc',
    }),
  ],
});
```

### Subscription Patterns (WebSocket)

**Server Setup:**

```typescript
import { observable } from '@trpc/server/observable';

const postRouter = router({
  onNewPost: publicProcedure.subscription(() => {
    return observable<Post>(emit => {
      const onPost = (post: Post) => {
        emit.next(post);
      };

      eventEmitter.on('newPost', onPost);

      return () => {
        eventEmitter.off('newPost', onPost);
      };
    });
  }),
});
```

**Client Usage:**

```typescript
function PostFeed() {
  trpc.post.onNewPost.useSubscription(undefined, {
    onData(post) {
      // Add new post to UI
      console.log('New post:', post);
    },
    onError(err) {
      console.error('Subscription error:', err);
    },
  });

  return <div>...</div>;
}
```

### Best Practices

**1. Use Zod for All Inputs**

- Provides runtime validation and TypeScript types
- Define schemas once, use everywhere

**2. Organize Routers by Domain**

- Keep related procedures together
- Use nested routers for complex domains

**3. Use Middleware for Cross-Cutting Concerns**

- Authentication
- Logging
- Rate limiting
- Permissions

**4. Implement Proper Error Handling**

- Use TRPCError with appropriate codes
- Provide helpful error messages
- Don't leak sensitive information

**5. Optimize with React Query**

- Set appropriate staleTime
- Use optimistic updates for better UX
- Implement pagination and infinite queries

**6. Type Safety First**

- Export AppRouter type from server
- Use inferRouterInputs and inferRouterOutputs for types
- Never use `any` types

**7. Security**

- Validate all inputs
- Implement authentication middleware
- Check permissions before operations
- Never trust client-provided data
  </instructions>

<examples>
Example usage:
```
User: "Review this code for trpc api rule compliance"
Agent: [Analyzes code against guidelines and provides specific feedback]
```
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

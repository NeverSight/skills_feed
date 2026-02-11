---
name: trpc
description: Generic tRPC implementation guide. Works with any framework (Next.js, Express, Fastify, Hono, Bun) and any package manager (pnpm, npm, yarn, bun).
---

# tRPC Quick Start

## Backend Router

```typescript
import { initTRPC, TRPCError } from "@trpc/server";
import { z } from "zod";

export const t = initTRPC.create();
export const router = t.router;
export const publicProcedure = t.procedure;

export const myRouter = router({
  getItem: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input }) => {
      return await getItem(input.id);
    }),

  updateItem: publicProcedure
    .input(z.object({ id: z.string(), data: z.any() }))
    .mutation(async ({ input }) => {
      return await updateItem(input.id, input.data);
    }),
});

export const appRouter = router({
  healthCheck: publicProcedure.query(() => "OK"),
  my: myRouter,
});

export type AppRouter = typeof appRouter;
```

## Frontend Client

```typescript
import { createTRPCClient, httpBatchLink } from "@trpc/client";
import { createTRPCOptionsProxy } from "@trpc/tanstack-react-query";
import type { AppRouter } from "./path/to/router";
import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient();
export const trpcClient = createTRPCClient<AppRouter>({
  links: [httpBatchLink({ url: "/api/trpc" })],
});

export const trpc = createTRPCOptionsProxy<AppRouter>({
  client: trpcClient,
  queryClient,
});
```

## Usage

```typescript
const { data } = useQuery(trpc.my.getItem.queryOptions({ id }));
const mutation = useMutation(trpc.my.updateItem.mutationOptions());
```

## Error Handling

```typescript
throw new TRPCError({
  code: "NOT_FOUND",
  message: "Resource not found",
});
```

## Advanced

- **Subscriptions**: See [SUBSCRIPTIONS.md](references/SUBSCRIPTIONS.md)
- **Server Adapters**: See [ADAPTERS.md](references/ADAPTERS.md)
- **Context**: See [CONTEXT.md](references/CONTEXT.md)
- **Router Merging**: See [ROUTERS.md](references/ROUTERS.md)
- **Middleware**: See [MIDDLEWARE.md](references/MIDDLEWARE.md)
- **Frontend Patterns**: See [FRONTEND.md](references/FRONTEND.md)
- **Client Links**: See [LINKS.md](references/LINKS.md)
- **Schemas**: See [SCHEMAS.md](references/SCHEMAS.md)
- **Client Errors**: See [CLIENT_ERRORS.md](references/CLIENT_ERRORS.md)
- **Install**: See [INSTALL.md](references/INSTALL.md)

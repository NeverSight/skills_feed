---
name: trpc-tanstack-nextjs
description: "Set up tRPC with TanStack Query in Next.js App Router projects. Use when: (1) Setting up tRPC from scratch in a Next.js project, (2) Adding new routers or procedures, (3) Integrating authentication with tRPC context, (4) Using tRPC with React Server Components, (5) Configuring prefetching and hydration patterns."
---

# tRPC + TanStack Query + Next.js App Router

End-to-end typesafe APIs for Next.js using tRPC v11 with `@trpc/tanstack-react-query` adapter.

## Core Setup

- `setup` - Full setup from scratch with all modules
- `routers` - Creating routers, procedures, middleware
- `client-usage` - Queries, mutations, useUtils in client components
- `server-usage` - Prefetching, hydration, getCaller in server components

## Optional Integrations

- `better-auth-integration` - Add session/user to tRPC context with Better Auth
- `optimistic-updates` - Update UI before server confirms
- `infinite-queries` - Cursor-based pagination
- `subscriptions` - WebSocket real-time updates

## How to Use

Read individual reference files for detailed explanations and code examples:

```
references/setup.md
references/routers.md
references/client-usage.md
```

Each reference file contains:
- Code examples with imports
- Usage patterns
- Common variations

## Common Gotchas

1. **Cookies not sent** - Add `credentials: "include"` to httpBatchLink fetch
2. **Hydration mismatch** - Ensure superjson transformer on both client and server
3. **staleTime: 0** - Causes refetch on every mount; use 30s+ for most cases
4. **Missing HydrateClient** - Prefetched data won't transfer to client
5. **cache() not used** - getCaller/getQueryClient must be wrapped in React cache()

## Resources

- [tRPC Docs](https://trpc.io/docs)
- [TanStack Query Docs](https://tanstack.com/query/latest)

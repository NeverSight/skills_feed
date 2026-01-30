---
name: typesafe-rpc
description: Type-safe RPC library for Node/TS with end-to-end types. Defines schema (entity/operation/handler), createRpcHandler (server), createRpcClient (client), Route and middlewares. Use when editing typesafe-rpc, adding RPC operations, wiring server or client, or implementing handlers and middlewares in this repo.
---

# typesafe-rpc

## Overview

This repo is a type-safe RPC library. The server accepts POST bodies `{ entity, operation, params }` and runs the matching handler. The client is a typed proxy: `client.entity.operation(params, signal?)`. Types are shared so client calls are inferred from the schema.

## Core types (shared)

- **BaseContext**: `{ request: Request | Express.Request }`
- **Args&lt;Params, Context&gt;**: `{ params: Params; context: Context }`
- **Handler&lt;Params, Context, Result&gt;**: `(args: Args<Params, Context>) => Promise<Result>`
- **RpcSchema**: `{ [entity: string]: { [operation: string]: Handler<any, any, any> } }`

Handlers receive only `params` and `context` (no ExtraParams). Extend `BaseContext` for app-specific context.

## Schema and handlers

Schema is a nested object: entity → operation → handler. Use `as const` so the client gets literal types.

```typescript
import type { BaseContext, Handler } from 'typesafe-rpc';

type Ctx = BaseContext & { userId?: string };

const getItem: Handler<{ id: string }, Ctx, { name: string }> = async ({ params, context }) => {
  return { name: 'Item ' + params.id };
};

export const apiSchema = {
  items: {
    getById: getItem,
  },
} as const;
```

## Server: createRpcHandler

From `typesafe-rpc/server`:

```typescript
import { createRpcHandler } from 'typesafe-rpc/server';

const response = await createRpcHandler({
  context: { request },           // must include request
  operations: apiSchema,
  errorHandler: (error) => new Response(JSON.stringify({ error: '...' }), { status: 500 }),
  hooks: {
    preCall: (args) => {},
    postCall: (args, performance) => {},
    error: (args, performance, error) => {},
  },
});
```

- Expects `context.request.method === 'POST'`; body must be JSON `{ entity, operation, params }`.
- Hook args: `{ entity, operation, params, context }`.
- If no `errorHandler`, throws a generic 500 Response.

## Client: createRpcClient

From `typesafe-rpc/client`:

```typescript
import { createRpcClient } from 'typesafe-rpc/client';
import type { apiSchema } from './api-schema';

const client = createRpcClient<typeof apiSchema>('/api/rpc', optionalHeaders);

const result = await client.items.getById({ id: '1' });
const withAbort = await client.items.getById({ id: '1' }, signal);
```

Client calls `POST endpoint?entity::operation` with body `{ entity, operation, params }`. Use the same schema type (`typeof apiSchema`) for full inference.

## Route and middlewares

From `typesafe-rpc/server`: `Route`, `Middleware`, `orMiddleware`.

- **Middleware&lt;Params, Context&gt;**: `(args: Args<Params, Context>) => Promise<void>` (throw to abort).
- **Route**: chain `.middleware(...fns)` then `.handle(handler)`.
  - Multiple `.middleware(a, b, c)`: **OR** — first success wins (via `orMiddleware`).
  - Chained `.middleware(a).middleware(b)`: **AND** — all run in order.
- **orMiddleware(...middlewares)**: runs middlewares in order; returns on first that doesn’t throw; if all throw, rethrows the first error.

```typescript
import { Route } from 'typesafe-rpc/server';

const handler = new Route<{ id: string }, BaseContext>()
  .middleware(authOrAnonymous)
  .middleware(requireReadPermission)
  .handle(async ({ params, context }) => ({ name: '...' }));
```

Use the resulting handler as the function stored in the schema (e.g. `getById: handler`).

## Request/response and errors

- Server reads body via `request.json()` (Fetch) or `request.body` (Express).
- Client sends JSON and parses response with `response.json()`. Non-ok responses throw `FetchError` (from `typesafe-rpc/client`).

## Conventions in this repo

- Schema and shared types live in `shared/`; server in `server/`, client in `client/`.
- Implementations follow the types in `libs/typesafe-rpc/src/shared/rpc-types.ts`. Prefer those over README if they differ (e.g. no ExtraParams in Handler).
- For full API and examples, see the project [README](../../README.md).

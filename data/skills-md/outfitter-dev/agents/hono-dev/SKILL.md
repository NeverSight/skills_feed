---
name: hono-dev
description: This skill should be used when building APIs with Hono, using hc client, implementing OpenAPI, or when "Hono", "RPC", or "type-safe API" are mentioned.
metadata:
  version: "1.0.0"
---

# Hono API Development

Route chaining → type-safe RPC → end-to-end types.

<when_to_use>

- Building REST APIs with Hono
- Type-safe RPC with hono/client
- OpenAPI documentation with Zod
- Testing APIs with testClient
- When user mentions "Hono", "RPC", or "OpenAPI"

NOT for: Bun runtime APIs (use bun-dev), other frameworks (Express, Fastify)

</when_to_use>

<version_notes>

Hono v4+ with @hono/zod-openapi v1.0+
Check hono.dev for latest patterns.

</version_notes>

## Route Chaining — Critical Pattern

Type inference flows through method chain. Break chain = lose types.

<route_chaining>

```typescript
// ✅ Chained routes preserve types
const app = new Hono()
  .get('/users', (c) => c.json({ users: [] }))
  .get('/users/:id', (c) => {
    const id = c.req.param('id'); // Typed!
    return c.json({ id });
  })
  .post('/users', async (c) => {
    const body = await c.req.json();
    return c.json({ created: true }, 201);
  });

export type AppType = typeof app; // Full route types!
```

**❌ NEVER break the chain:**

```typescript
const app = new Hono();
app.get('/users', handler1);  // Types LOST!
app.post('/users', handler2);
```

**Path parameters** — typed automatically:

```typescript
.get('/posts/:id/comments/:commentId', (c) => {
  const { id, commentId } = c.req.param(); // Both string
  return c.json({ postId: id, commentId });
})
```

**Query parameters** — use Zod for validation:

```typescript
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const QuerySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(20),
});

const app = new Hono()
  .get('/search', zValidator('query', QuerySchema), (c) => {
    const { page, limit } = c.req.valid('query'); // Fully typed!
    return c.json({ page, limit });
  });
```

**Middleware in chain:**

```typescript
const app = new Hono()
  .use('*', logger())
  .use('/api/*', cors())
  .get('/api/public', (c) => c.json({ public: true }))
  .use('/api/admin/*', authMiddleware)
  .get('/api/admin/users', (c) => c.json({ users: [] }));
```

</route_chaining>

## Factory Pattern — Context Typing

Use `createFactory<Env>()` to type context variables across middleware and routes.

<factory_pattern>

```typescript
import { createFactory } from 'hono/factory';
import type { Database } from 'bun:sqlite';

type Env = {
  Variables: {
    user: { id: string; role: 'admin' | 'user' };
    requestId: string;
    db: Database;
  };
};

const factory = createFactory<Env>();

// Typed middleware
const authMiddleware = factory.createMiddleware(async (c, next) => {
  const token = c.req.header('authorization')?.replace('Bearer ', '');
  if (!token) throw new HTTPException(401, { message: 'Unauthorized' });

  const user = await verifyToken(token);
  c.set('user', user); // Type-checked!
  await next();
});

// Typed handlers
const getProfile = factory.createHandlers((c) => {
  const user = c.get('user'); // Typed: { id: string; role: 'admin' | 'user' }
  return c.json({ user });
});

// Assemble app
const app = factory.createApp()
  .use('*', dbMiddleware)
  .use('/api/*', authMiddleware)
  .get('/api/profile', ...getProfile);

export type AppType = typeof app;
```

**Multi-module structure:**

```typescript
// routes/users.ts
export const usersRoute = factory.createApp()
  .get('/', (c) => c.json({ users: [] }))
  .post('/', zValidator('json', CreateUserSchema), async (c) => {
    const data = c.req.valid('json');
    return c.json({ created: true }, 201);
  });

// index.ts
const app = factory.createApp()
  .use('*', dbMiddleware)
  .route('/users', usersRoute)
  .route('/posts', postsRoute);
```

See [factory-pattern.md](references/factory-pattern.md) for advanced patterns.

</factory_pattern>

## Error Handling

<error_handling>

```typescript
import { HTTPException } from 'hono/http-exception';

// Throw typed errors
app.get('/users/:id', async (c) => {
  const user = await findUser(c.req.param('id'));
  if (!user) {
    throw new HTTPException(404, { message: 'User not found' });
  }
  return c.json({ user });
});

// Custom error classes
class NotFoundError extends HTTPException {
  constructor(resource: string) {
    super(404, { message: `${resource} not found` });
  }
}

class UnauthorizedError extends HTTPException {
  constructor(message = 'Unauthorized') {
    super(401, { message });
  }
}

// Centralized handler
app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status);
  }
  if (err instanceof ZodError) {
    return c.json({
      error: 'Validation failed',
      issues: err.issues.map(i => ({ path: i.path.join('.'), message: i.message }))
    }, 400);
  }
  const isDev = Bun.env.NODE_ENV !== 'production';
  return c.json({ error: isDev ? err.message : 'Internal server error' }, 500);
});

app.notFound((c) => c.json({ error: 'Not found', path: c.req.path }, 404));
```

See [error-handling.md](references/error-handling.md) for patterns.

</error_handling>

## Zod OpenAPI

<zod_openapi>

```typescript
import { createRoute, OpenAPIHono, z } from '@hono/zod-openapi';
import { swaggerUI } from '@hono/swagger-ui';

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
}).openapi('User');

const route = createRoute({
  method: 'get',
  path: '/users/{id}',
  request: {
    params: z.object({ id: z.string().uuid() }),
  },
  responses: {
    200: {
      content: { 'application/json': { schema: UserSchema } },
      description: 'User found',
    },
    404: {
      content: { 'application/json': { schema: z.object({ error: z.string() }) } },
      description: 'User not found',
    },
  },
  tags: ['Users'],
  summary: 'Get user by ID',
});

const app = new OpenAPIHono();

app.openapi(route, (c) => {
  const { id } = c.req.valid('param'); // Typed!
  const user = db.query('SELECT * FROM users WHERE id = ?').get(id);
  if (!user) return c.json({ error: 'User not found' }, 404);
  return c.json(user, 200);
});

// Swagger UI
app.get('/docs', swaggerUI({ url: '/openapi.json' }));
app.doc('/openapi.json', {
  openapi: '3.1.0',
  info: { title: 'API', version: '1.0.0' },
});
```

See [zod-openapi.md](references/zod-openapi.md) for complete patterns.

</zod_openapi>

## RPC Client — End-to-End Types

<rpc_client>

```typescript
// Server
const app = new Hono()
  .get('/posts', (c) => c.json({ posts: [] }))
  .get('/posts/:id', (c) => c.json({ id: c.req.param('id') }))
  .post('/posts', zValidator('json', CreatePostSchema), async (c) => {
    const data = c.req.valid('json');
    return c.json({ id: '123', ...data }, 201);
  });

export type AppType = typeof app;

// Client
import { hc } from 'hono/client';
import type { AppType } from './server';

const client = hc<AppType>('http://localhost:3000');

// GET request
const res = await client.posts.$get();
const data = await res.json(); // Typed: { posts: any[] }

// GET with params
const res2 = await client.posts[':id'].$get({ param: { id: '123' } });

// POST request
const res3 = await client.posts.$post({
  json: { title: 'Hello', content: 'World' }
});

// With headers
const res4 = await client.posts.$get({}, {
  headers: { Authorization: 'Bearer token' }
});
```

</rpc_client>

## Testing with testClient

<testing>

```typescript
import { describe, expect, test, beforeEach, afterEach } from 'bun:test';
import { testClient } from 'hono/testing';
import { Database } from 'bun:sqlite';
import app from './server';

describe('API Tests', () => {
  let db: Database;

  beforeEach(() => {
    db = new Database(':memory:');
    db.run('CREATE TABLE posts (id TEXT PRIMARY KEY, title TEXT, content TEXT)');
  });

  afterEach(() => {
    db.close();
  });

  const client = testClient(app);

  test('GET /posts returns posts', async () => {
    const res = await client.posts.$get();
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data).toHaveProperty('posts');
  });

  test('POST /posts creates post', async () => {
    const res = await client.posts.$post({
      json: { title: 'Test', content: 'Content' }
    });
    expect(res.status).toBe(201);
    const data = await res.json();
    expect(data).toMatchObject({ title: 'Test' });
  });

  test('Protected route requires auth', async () => {
    const res = await client.api.profile.$get();
    expect(res.status).toBe(401);
  });

  test('Protected route accepts valid token', async () => {
    const res = await client.api.profile.$get({}, {
      headers: { Authorization: 'Bearer valid-token' }
    });
    expect(res.status).toBe(200);
  });
});
```

See [testing-patterns.md](examples/testing-patterns.md) for complete patterns.

</testing>

## Middleware Patterns

<middleware>

```typescript
// Logging
import { logger } from 'hono/logger';
app.use('*', logger());

// CORS
import { cors } from 'hono/cors';
app.use('/api/*', cors({
  origin: ['http://localhost:3000'],
  credentials: true,
}));

// Rate limiting
const rateLimiter = factory.createMiddleware(async (c, next) => {
  const ip = c.req.header('x-forwarded-for') || 'unknown';
  const key = `rate:${ip}`;
  const count = await cache.incr(key);

  if (count === 1) await cache.expire(key, 60);
  if (count > 100) {
    throw new HTTPException(429, { message: 'Rate limit exceeded' });
  }

  await next();
});

// Request ID
const requestId = factory.createMiddleware(async (c, next) => {
  c.set('requestId', crypto.randomUUID());
  await next();
  c.res.headers.set('x-request-id', c.get('requestId'));
});
```

</middleware>

<rules>

## Rules

**ALWAYS:**
- Chain routes for type inference → `.get().post().put()`
- Export `type AppType = typeof app` for RPC client
- Use `createFactory<Env>()` for typed context variables
- Validate with Zod schemas via `zValidator`
- Handle errors with `HTTPException` and centralized `onError`
- Test with `testClient` for type safety

**NEVER:**
- Break method chain with variable assignment between routes
- Use `any` types — let Hono infer or define explicitly
- Use `JSON.parse(await c.req.text())` — use `c.req.json()` or Zod validator
- Skip request validation on user input
- Expose stack traces in production

**When Type Errors Occur:**
- Check route chaining not broken
- Verify `export type AppType` matches actual app
- Ensure middleware uses `createFactory` for context types
- Check client using correct `param`, `query`, or `json` keys

</rules>

<references>

## References

**Examples:**
- [typed-routes.md](examples/typed-routes.md) — Complete route chaining examples
- [testing-patterns.md](examples/testing-patterns.md) — Testing with testClient

**References:**
- [factory-pattern.md](references/factory-pattern.md) — Context typing with createFactory
- [zod-openapi.md](references/zod-openapi.md) — OpenAPI integration patterns
- [error-handling.md](references/error-handling.md) — HTTPException and error patterns
- [middleware.md](references/middleware.md) — Auth, logging, CORS patterns

**External:**
- Hono: <https://hono.dev>
- @hono/zod-openapi: <https://github.com/honojs/middleware/tree/main/packages/zod-openapi>

</references>

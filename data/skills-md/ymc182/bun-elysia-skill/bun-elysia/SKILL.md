---
name: bun-elysia
description: Build full-stack applications with Bun.js and Elysia.js. Use this skill when working with Bun runtime, Bun native APIs (SQL databases, Redis, S3), Bun workspaces/monorepos, Elysia.js web framework, or migrating from Fastify to Elysia. Covers setup, routing, validation, authentication, WebSocket, and end-to-end type safety with Eden.
---

# Bun + Elysia.js Development

Build high-performance full-stack applications with Bun runtime and Elysia.js framework.

## Quick Start

### New Elysia Project
```bash
bun create elysia my-app
cd my-app
bun run dev
```

### Basic Server
```typescript
import { Elysia, t } from "elysia";

const app = new Elysia()
  .get("/", () => "Hello, World!")
  .get("/users/:id", ({ params }) => ({ id: params.id }), {
    params: t.Object({ id: t.Number() })
  })
  .post("/users", ({ body }) => ({ created: body }), {
    body: t.Object({
      name: t.String(),
      email: t.String({ format: "email" })
    })
  })
  .listen(3000);
```

### With Bun Native APIs
```typescript
import { Elysia } from "elysia";
import { sql } from "bun";
import { redis } from "bun";

const app = new Elysia()
  .decorate("sql", sql)
  .decorate("redis", redis)
  .get("/users", async ({ sql }) => {
    return sql`SELECT * FROM users`;
  })
  .get("/cache/:key", async ({ redis, params }) => {
    return redis.get(params.key);
  })
  .listen(3000);
```

---

## Reference Navigation

### What do you want to do?

**Set up a project:**
- Monorepo with workspaces → [monorepo.md](references/monorepo.md)

**Use Bun native APIs:**
- PostgreSQL/MySQL/SQLite → [native-apis/sql.md](references/native-apis/sql.md)
- Redis/Valkey → [native-apis/redis.md](references/native-apis/redis.md)
- S3/Object storage → [native-apis/s3.md](references/native-apis/s3.md)
- HTTP server basics → [native-apis/http-server.md](references/native-apis/http-server.md)

**Build with Elysia:**
- Routing and handlers → [elysia/core.md](references/elysia/core.md)
- Request/response validation → [elysia/validation.md](references/elysia/validation.md)
- Hooks, middleware, plugins → [elysia/lifecycle.md](references/elysia/lifecycle.md)
- WebSocket support → [elysia/websocket.md](references/elysia/websocket.md)
- OpenAPI/Swagger docs → [elysia/swagger.md](references/elysia/swagger.md)
- Type-safe client (Eden) → [elysia/eden.md](references/elysia/eden.md)

**Migrate from Fastify:**
- Routing, params, body → [migration/fastify-basics.md](references/migration/fastify-basics.md)
- Schema validation → [migration/fastify-validation.md](references/migration/fastify-validation.md)
- Lifecycle hooks → [migration/fastify-hooks.md](references/migration/fastify-hooks.md)
- Plugin architecture → [migration/fastify-plugins.md](references/migration/fastify-plugins.md)
- Authentication → [migration/fastify-auth.md](references/migration/fastify-auth.md)
- WebSocket, Swagger, files → [migration/fastify-advanced.md](references/migration/fastify-advanced.md)

---

## Common Patterns

### Authentication Middleware
```typescript
import { Elysia } from "elysia";
import { jwt } from "@elysiajs/jwt";

const app = new Elysia()
  .use(jwt({ secret: process.env.JWT_SECRET! }))
  .derive(async ({ headers, jwt }) => {
    const token = headers.authorization?.replace("Bearer ", "");
    const user = token ? await jwt.verify(token) : null;
    return { user };
  })
  .get("/profile", ({ user, error }) => {
    if (!user) return error(401);
    return user;
  });
```

### Database with Validation
```typescript
import { Elysia, t } from "elysia";
import { sql } from "bun";

const app = new Elysia()
  .post("/users", async ({ body }) => {
    const [user] = await sql`
      INSERT INTO users (name, email)
      VALUES (${body.name}, ${body.email})
      RETURNING *
    `;
    return user;
  }, {
    body: t.Object({
      name: t.String({ minLength: 1 }),
      email: t.String({ format: "email" })
    })
  });
```

### Grouped Routes with Guard
```typescript
app.group("/api", (app) =>
  app
    .guard({
      headers: t.Object({
        authorization: t.String()
      }),
      beforeHandle: ({ headers, error }) => {
        if (!isValidToken(headers.authorization)) {
          return error(401);
        }
      }
    }, (app) =>
      app
        .get("/users", getUsers)
        .post("/users", createUser)
    )
);
```

### WebSocket Chat
```typescript
app.ws("/chat", {
  body: t.Object({
    room: t.String(),
    message: t.String()
  }),
  open(ws) {
    ws.subscribe("general");
  },
  message(ws, { room, message }) {
    ws.publish(room, { from: ws.id, message });
  }
});
```

---

## Key Differences: Fastify vs Elysia

| Fastify | Elysia |
|---------|--------|
| `request.params` | `{ params }` |
| `request.query` | `{ query }` |
| `request.body` | `{ body }` |
| `reply.code(n).send(x)` | `set.status = n; return x` |
| `reply.header(k, v)` | `set.headers[k] = v` |
| JSON Schema | TypeBox (`t.*`) |
| `preHandler` hook | `beforeHandle` |
| `fastify.decorate()` | `.decorate()` |
| `fastify.register(plugin)` | `.use(plugin)` |

---

## Installation

```bash
# Elysia and plugins
bun add elysia @elysiajs/swagger @elysiajs/jwt @elysiajs/cors @elysiajs/static @elysiajs/eden

# Types
bun add -d @types/bun typescript
```

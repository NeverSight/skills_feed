---
name: encore-migrate
description: Migrate Express/Fastify apps to Encore.ts.
---

# Migrate to Encore.ts

## Instructions

When migrating existing Node.js applications to Encore.ts, follow these transformation patterns:

## Express to Encore

### Basic Route

```typescript
// BEFORE: Express
const express = require('express');
const app = express();

app.get('/users/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  res.json(user);
});

app.listen(3000);
```

```typescript
// AFTER: Encore
import { api } from "encore.dev/api";

interface GetUserRequest {
  id: string;
}

interface User {
  id: string;
  email: string;
  name: string;
}

export const getUser = api(
  { method: "GET", path: "/users/:id", expose: true },
  async ({ id }: GetUserRequest): Promise<User> => {
    return await findUser(id);
  }
);
```

### POST with Body

```typescript
// BEFORE: Express
app.post('/users', async (req, res) => {
  const { email, name } = req.body;
  const user = await createUser(email, name);
  res.status(201).json(user);
});
```

```typescript
// AFTER: Encore
interface CreateUserRequest {
  email: string;
  name: string;
}

export const createUser = api(
  { method: "POST", path: "/users", expose: true },
  async (req: CreateUserRequest): Promise<User> => {
    return await insertUser(req.email, req.name);
  }
);
```

### Query Parameters

```typescript
// BEFORE: Express
app.get('/users', async (req, res) => {
  const { limit, offset } = req.query;
  const users = await listUsers(Number(limit), Number(offset));
  res.json(users);
});
```

```typescript
// AFTER: Encore
import { Query, api } from "encore.dev/api";

interface ListUsersRequest {
  limit?: Query<number>;
  offset?: Query<number>;
}

export const listUsers = api(
  { method: "GET", path: "/users", expose: true },
  async ({ limit = 10, offset = 0 }: ListUsersRequest): Promise<{ users: User[] }> => {
    return { users: await fetchUsers(limit, offset) };
  }
);
```

### Headers

```typescript
// BEFORE: Express
app.post('/webhook', async (req, res) => {
  const signature = req.headers['x-signature'];
  // verify...
});
```

```typescript
// AFTER: Encore
import { Header, api } from "encore.dev/api";

interface WebhookRequest {
  signature: Header<"X-Signature">;
  payload: any;
}

export const webhook = api(
  { method: "POST", path: "/webhook", expose: true },
  async ({ signature, payload }: WebhookRequest): Promise<void> => {
    // verify signature...
  }
);
```

### Raw Request Access (Webhooks)

```typescript
// BEFORE: Express
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  const event = stripe.webhooks.constructEvent(req.body, sig, secret);
  res.sendStatus(200);
});
```

```typescript
// AFTER: Encore
export const stripeWebhook = api.raw(
  { expose: true, path: "/webhooks/stripe", method: "POST" },
  async (req, res) => {
    const sig = req.headers["stripe-signature"];
    const chunks: Buffer[] = [];
    for await (const chunk of req) {
      chunks.push(chunk);
    }
    const body = Buffer.concat(chunks);
    const event = stripe.webhooks.constructEvent(body, sig, secret);
    res.writeHead(200);
    res.end();
  }
);
```

### Middleware

```typescript
// BEFORE: Express
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});
```

```typescript
// AFTER: Encore
import { Service } from "encore.dev/service";
import { middleware } from "encore.dev/api";

const logMiddleware = middleware(
  { target: { all: true } },
  async (req, next) => {
    console.log(`${req.requestMeta?.method} ${req.requestMeta?.path}`);
    return next(req);
  }
);

export default new Service("my-service", {
  middlewares: [logMiddleware],
});
```

### Error Handling

```typescript
// BEFORE: Express
app.get('/users/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});
```

```typescript
// AFTER: Encore
import { APIError, api } from "encore.dev/api";

export const getUser = api(
  { method: "GET", path: "/users/:id", expose: true },
  async ({ id }: GetUserRequest): Promise<User> => {
    const user = await findUser(id);
    if (!user) {
      throw APIError.notFound("user not found");
    }
    return user;
  }
);
```

## Database Migration

```typescript
// BEFORE: Express with pg
import { Pool } from 'pg';
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
```

```typescript
// AFTER: Encore
import { SQLDatabase } from "encore.dev/storage/sqldb";

const db = new SQLDatabase("users", {
  migrations: "./migrations",
});

const user = await db.queryRow<User>`
  SELECT * FROM users WHERE id = ${id}
`;
```

## Cron Jobs

```typescript
// BEFORE: Node with node-cron
import cron from 'node-cron';

cron.schedule('0 * * * *', () => {
  cleanupExpiredSessions();
});
```

```typescript
// AFTER: Encore
import { CronJob } from "encore.dev/cron";
import { api } from "encore.dev/api";

export const cleanupSessions = api(
  { expose: false },
  async (): Promise<void> => {
    // cleanup logic
  }
);

const _ = new CronJob("cleanup-sessions", {
  title: "Cleanup expired sessions",
  schedule: "0 * * * *",
  endpoint: cleanupSessions,
});
```

## Migration Checklist

- [ ] Replace `require` with `import`
- [ ] Remove `app.listen()` - Encore handles this
- [ ] Convert routes to `api()` functions
- [ ] Define TypeScript interfaces for request/response
- [ ] Replace manual validation with Encore's type validation
- [ ] Convert error responses to `APIError`
- [ ] Move database connection to `SQLDatabase`
- [ ] Convert cron jobs to `CronJob`
- [ ] Move env vars to `secret()` for sensitive values
- [ ] Create `encore.service.ts` in each service directory

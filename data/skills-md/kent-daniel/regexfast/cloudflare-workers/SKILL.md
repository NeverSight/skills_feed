---
name: cloudflare-workers
description: Build stateful serverless applications using Cloudflare Workers and Durable Objects. Use when creating real-time collaborative apps, chat systems, multiplayer games, WebSocket servers, rate limiters, or any application requiring coordination between clients, persistent state, or scheduled tasks with Cloudflare's edge computing platform.
license: Complete terms in LICENSE.txt
---

# Cloudflare Workers & Durable Objects Development Guide

Build stateful serverless applications that run at the edge using Cloudflare Workers and Durable Objects. Durable Objects provide strongly consistent storage and coordination, making them ideal for real-time collaboration, WebSockets, and stateful workflows.

---

## Quick Start

### 1. Create Project

```bash
npm create cloudflare@latest -- durable-object-starter
cd durable-object-starter
```

Select: `Hello World example` → `Worker + Durable Objects` → `TypeScript`

### 2. Project Structure

```
my-project/
├── src/
│   └── index.ts          # Worker + Durable Object class
├── wrangler.jsonc        # Configuration (bindings, migrations)
├── package.json
└── tsconfig.json
```

### 3. Basic Durable Object

```typescript
import { DurableObject } from "cloudflare:workers";

export interface Env {
  MY_DURABLE_OBJECT: DurableObjectNamespace<MyDurableObject>;
}

export class MyDurableObject extends DurableObject<Env> {
  async sayHello(): Promise<string> {
    return "Hello from Durable Object!";
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const stub = env.MY_DURABLE_OBJECT.getByName("singleton");
    const greeting = await stub.sayHello();
    return new Response(greeting);
  },
};
```

### 4. Configure wrangler.jsonc

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-01",
  "durable_objects": {
    "bindings": [
      { "name": "MY_DURABLE_OBJECT", "class_name": "MyDurableObject" }
    ]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["MyDurableObject"] }
  ]
}
```

### 5. Develop & Deploy

```bash
npx wrangler dev      # Local development
npx wrangler deploy   # Deploy to Cloudflare
```

---

## Core Concepts

### Durable Object Lifecycle

1. **Creation**: Lazy - created on first access via `getByName()` or `get()`
2. **Execution**: Single-threaded, strongly consistent within the object
3. **Hibernation**: Evicted from memory when idle, but storage persists
4. **Wake-up**: Re-initialized when accessed again (constructor runs)

### Accessing Durable Objects

```typescript
// By name (most common) - deterministic ID from string
const stub = env.MY_DO.getByName("user-123");

// By unique ID - for session-based objects
const id = env.MY_DO.newUniqueId();
const stub = env.MY_DO.get(id);

// From stored ID string
const stub = env.MY_DO.get(env.MY_DO.idFromString(storedId));
```

### RPC Methods (Recommended)

Public methods on Durable Object classes are automatically exposed as RPC:

```typescript
export class Counter extends DurableObject<Env> {
  private count = 0;

  async increment(): Promise<number> {
    return ++this.count;
  }

  async getCount(): Promise<number> {
    return this.count;
  }
}

// Called from Worker:
const count = await stub.increment();
```

---

## Storage Patterns

### SQLite Storage (Recommended)

New Durable Objects use SQLite storage. Access via `this.ctx.storage.sql`:

```typescript
export class UserStore extends DurableObject<Env> {
  sql: SqlStorage;

  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    
    this.sql.exec(`
      CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        created_at INTEGER DEFAULT (unixepoch())
      )
    `);
  }

  async createUser(id: string, name: string): Promise<void> {
    this.sql.exec("INSERT INTO users (id, name) VALUES (?, ?)", id, name);
  }

  async getUser(id: string): Promise<User | null> {
    return this.sql.exec("SELECT * FROM users WHERE id = ?", id).toArray()[0] ?? null;
  }

  async listUsers(): Promise<User[]> {
    return this.sql.exec("SELECT * FROM users ORDER BY created_at DESC").toArray();
  }
}
```

### Key-Value Storage

```typescript
// Synchronous (SQLite-backed DO only)
const value = this.ctx.storage.kv.get("key");
this.ctx.storage.kv.put("key", { any: "value" });
this.ctx.storage.kv.delete("key");

// Async (works with both backends)
const value = await this.ctx.storage.get("key");
await this.ctx.storage.put("key", value);
await this.ctx.storage.delete("key");
```

### Transactions

```typescript
// Synchronous transaction (SQL)
this.ctx.storage.transactionSync(() => {
  this.sql.exec("UPDATE accounts SET balance = balance - ? WHERE id = ?", amount, fromId);
  this.sql.exec("UPDATE accounts SET balance = balance + ? WHERE id = ?", amount, toId);
});
```

---

## WebSocket Hibernation

Use hibernation to maintain WebSocket connections while minimizing costs:

```typescript
export class ChatRoom extends DurableObject<Env> {
  async fetch(request: Request): Promise<Response> {
    if (request.headers.get("Upgrade") !== "websocket") {
      return new Response("Expected WebSocket", { status: 426 });
    }

    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    // Accept with hibernation support
    this.ctx.acceptWebSocket(server);
    server.serializeAttachment({ joinedAt: Date.now() });

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer): Promise<void> {
    const data = JSON.parse(message as string);
    
    // Broadcast to all connected clients
    for (const client of this.ctx.getWebSockets()) {
      if (client !== ws) {
        client.send(JSON.stringify({ type: "message", content: data.content }));
      }
    }
  }

  async webSocketClose(ws: WebSocket, code: number, reason: string): Promise<void> {
    ws.close(code, reason);
  }

  async webSocketError(ws: WebSocket, error: unknown): Promise<void> {
    ws.close(1011, "Internal error");
  }
}
```

---

## Alarms (Scheduled Tasks)

Schedule future execution within a Durable Object:

```typescript
export class ScheduledTask extends DurableObject<Env> {
  async scheduleReminder(delayMs: number, data: any): Promise<void> {
    await this.ctx.storage.put("reminderData", data);
    await this.ctx.storage.setAlarm(Date.now() + delayMs);
  }

  async alarm(): Promise<void> {
    const data = await this.ctx.storage.get("reminderData");
    console.log("Alarm triggered:", data);
    // Optionally reschedule: await this.ctx.storage.setAlarm(Date.now() + 60000);
  }
}
```

---

## Common Patterns

### Rate Limiter

```typescript
export class RateLimiter extends DurableObject<Env> {
  async checkLimit(key: string, maxRequests: number, windowMs: number): Promise<boolean> {
    const now = Date.now();
    const timestamps: number[] = (await this.ctx.storage.get(key)) ?? [];
    const valid = timestamps.filter(t => t > now - windowMs);
    
    if (valid.length >= maxRequests) return false;
    
    valid.push(now);
    await this.ctx.storage.put(key, valid);
    return true;
  }
}
```

### Distributed Lock

```typescript
export class Lock extends DurableObject<Env> {
  async acquire(lockId: string, ttlMs: number): Promise<boolean> {
    const existing = await this.ctx.storage.get<{ expiresAt: number }>(lockId);
    if (existing && existing.expiresAt > Date.now()) return false;
    
    await this.ctx.storage.put(lockId, { expiresAt: Date.now() + ttlMs });
    return true;
  }

  async release(lockId: string): Promise<void> {
    await this.ctx.storage.delete(lockId);
  }
}
```

---

## Wrangler Configuration Reference

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-01",
  "durable_objects": {
    "bindings": [
      { "name": "COUNTER", "class_name": "Counter" },
      { "name": "CHAT_ROOM", "class_name": "ChatRoom" }
    ]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["Counter", "ChatRoom"] }
  ],
  "kv_namespaces": [
    { "binding": "MY_KV", "id": "xxx" }
  ],
  "r2_buckets": [
    { "binding": "MY_BUCKET", "bucket_name": "my-bucket" }
  ]
}
```

---

## References

- **Storage API**: See [references/storage-api.md](references/storage-api.md) for SQL, KV, and transaction methods
- **WebSocket API**: See [references/websocket-api.md](references/websocket-api.md) for hibernation patterns
- **Best Practices**: See [references/best-practices.md](references/best-practices.md) for production patterns

---

## Deployment Checklist

1. ✅ Set appropriate `compatibility_date` in wrangler config
2. ✅ Define migrations for all Durable Object classes
3. ✅ Use SQLite storage (`new_sqlite_classes`) for new projects
4. ✅ Handle constructor re-initialization for hibernation
5. ✅ Implement error handling in WebSocket handlers
6. ✅ Test locally with `wrangler dev` before deploying
7. ✅ Monitor with `wrangler tail` for logs

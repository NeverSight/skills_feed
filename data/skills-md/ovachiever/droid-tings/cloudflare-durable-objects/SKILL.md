---
name: cloudflare-durable-objects
description: |
  Build stateful Durable Objects for real-time apps, WebSocket servers, coordination, and persistent state. Use when: implementing chat rooms, multiplayer games, rate limiting, session management, WebSocket hibernation, or troubleshooting class export, migration, WebSocket state loss, or binding errors.
license: MIT
---

# Cloudflare Durable Objects

**Status**: Production Ready ✅
**Last Updated**: 2025-11-23
**Dependencies**: cloudflare-worker-base (recommended)
**Latest Versions**: wrangler@4.50.0, @cloudflare/workers-types@4.20251121.0
**Official Docs**: https://developers.cloudflare.com/durable-objects/

**Recent Updates (2025)**:
- **Oct 2025**: WebSocket message size 1 MiB → 32 MiB, Data Studio UI for SQLite DOs (view/edit storage in dashboard)
- **Aug 2025**: `getByName()` API shortcut for named DOs
- **June 2025**: @cloudflare/actors library (beta) - recommended SDK with migrations, alarms, Actor class pattern
- **May 2025**: Python Workers support for Durable Objects
- **April 2025**: SQLite GA with 10GB storage (beta → GA, 1GB → 10GB), Free tier access
- **Feb 2025**: PRAGMA optimize support, improved error diagnostics with reference IDs

---

## Quick Start

**Scaffold new DO project:**
```bash
npm create cloudflare@latest my-durable-app -- --template=cloudflare/durable-objects-template --ts
```

**Or add to existing Worker:**

```typescript
// src/counter.ts - Durable Object class
import { DurableObject } from 'cloudflare:workers';

export class Counter extends DurableObject {
  async increment(): Promise<number> {
    let value = (await this.ctx.storage.get<number>('value')) || 0;
    await this.ctx.storage.put('value', ++value);
    return value;
  }
}
export default Counter;  // CRITICAL: Export required
```

```jsonc
// wrangler.jsonc - Configuration
{
  "durable_objects": {
    "bindings": [{ "name": "COUNTER", "class_name": "Counter" }]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["Counter"] }  // SQLite backend (10GB limit)
  ]
}
```

```typescript
// src/index.ts - Worker
import { Counter } from './counter';
export { Counter };

export default {
  async fetch(request: Request, env: { COUNTER: DurableObjectNamespace<Counter> }) {
    const stub = env.COUNTER.getByName('global-counter');  // Aug 2025: getByName() shortcut
    return new Response(`Count: ${await stub.increment()}`);
  }
};
```

---

## DO Class Essentials

```typescript
import { DurableObject } from 'cloudflare:workers';

export class MyDO extends DurableObject {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);  // REQUIRED first line

    // Load state before requests (optional)
    ctx.blockConcurrencyWhile(async () => {
      this.value = await ctx.storage.get('key') || defaultValue;
    });
  }

  // RPC methods (recommended)
  async myMethod(): Promise<string> { return 'Hello'; }

  // HTTP fetch handler (optional)
  async fetch(request: Request): Promise<Response> { return new Response('OK'); }
}

export default MyDO;  // CRITICAL: Export required

// Worker must export DO class too
import { MyDO } from './my-do';
export { MyDO };
```

**Constructor Rules:**
- ✅ Call `super(ctx, env)` first
- ✅ Keep minimal - heavy work blocks hibernation wake
- ✅ Use `ctx.blockConcurrencyWhile()` for storage initialization
- ❌ Never `setTimeout`/`setInterval` (use alarms)
- ❌ Don't rely on in-memory state with WebSockets (persist to storage)

---

## Storage API

**Two backends available:**
- **SQLite** (recommended): 10GB storage, SQL queries, atomic operations, PITR
- **KV**: 128MB storage, key-value only

**Enable SQLite in migrations:**
```jsonc
{ "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyDO"] }] }
```

### SQL API (SQLite backend)

```typescript
export class MyDO extends DurableObject {
  sql: SqlStorage;

  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;

    this.sql.exec(`
      CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, text TEXT, created_at INTEGER);
      CREATE INDEX IF NOT EXISTS idx_created ON messages(created_at);
      PRAGMA optimize;  // Feb 2025: Query performance optimization
    `);
  }

  async addMessage(text: string): Promise<number> {
    const cursor = this.sql.exec('INSERT INTO messages (text, created_at) VALUES (?, ?) RETURNING id', text, Date.now());
    return cursor.one<{ id: number }>().id;
  }

  async getMessages(limit = 50): Promise<any[]> {
    return this.sql.exec('SELECT * FROM messages ORDER BY created_at DESC LIMIT ?', limit).toArray();
  }
}
```

**SQL Methods:**
- `sql.exec(query, ...params)` → cursor
- `cursor.one<T>()` → single row (throws if none)
- `cursor.one<T>({ allowNone: true })` → row or null
- `cursor.toArray<T>()` → all rows
- `ctx.storage.transactionSync(() => { ... })` → atomic multi-statement

**Rules:** Always use `?` placeholders, create indexes, use PRAGMA optimize after schema changes

### Key-Value API (both backends)

```typescript
// Single operations
await this.ctx.storage.put('key', value);
const value = await this.ctx.storage.get<T>('key');
await this.ctx.storage.delete('key');

// Batch operations
await this.ctx.storage.put({ key1: val1, key2: val2 });
const map = await this.ctx.storage.get(['key1', 'key2']);
await this.ctx.storage.delete(['key1', 'key2']);

// List and delete all
const map = await this.ctx.storage.list({ prefix: 'user:', limit: 100 });
await this.ctx.storage.deleteAll();  // Atomic on SQLite only

// Transactions
await this.ctx.storage.transaction(async (txn) => {
  await txn.put('key1', val1);
  await txn.put('key2', val2);
});
```

**Storage Limits:** SQLite 10GB (April 2025 GA) | KV 128MB

---

## WebSocket Hibernation API

**Capabilities:**
- Thousands of WebSocket connections per instance
- Hibernate when idle (~10s no activity) to save costs
- Auto wake-up when messages arrive
- **Message size limit**: 32 MiB (Oct 2025, up from 1 MiB)

**How it works:**
1. Active → handles messages
2. Idle → ~10s no activity
3. Hibernation → in-memory state **cleared**, WebSockets stay connected
4. Wake → message arrives → constructor runs → handler called

**CRITICAL:** In-memory state is **lost on hibernation**. Use `serializeAttachment()` to persist per-WebSocket metadata.

### Hibernation-Safe Pattern

```typescript
export class ChatRoom extends DurableObject {
  sessions: Map<WebSocket, { userId: string; username: string }>;

  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    this.sessions = new Map();

    // CRITICAL: Restore WebSocket metadata after hibernation
    ctx.getWebSockets().forEach((ws) => {
      this.sessions.set(ws, ws.deserializeAttachment());
    });
  }

  async fetch(request: Request): Promise<Response> {
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    const url = new URL(request.url);
    const metadata = { userId: url.searchParams.get('userId'), username: url.searchParams.get('username') };

    // CRITICAL: Use ctx.acceptWebSocket(), NOT ws.accept()
    this.ctx.acceptWebSocket(server);
    server.serializeAttachment(metadata);  // Persist across hibernation
    this.sessions.set(server, metadata);

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer): Promise<void> {
    const session = this.sessions.get(ws);
    // Handle message (max 32 MiB since Oct 2025)
  }

  async webSocketClose(ws: WebSocket, code: number, reason: string, wasClean: boolean): Promise<void> {
    this.sessions.delete(ws);
    ws.close(code, 'Closing');
  }

  async webSocketError(ws: WebSocket, error: any): Promise<void> {
    this.sessions.delete(ws);
  }
}
```

**Hibernation Rules:**
- ✅ `ctx.acceptWebSocket(ws)` - enables hibernation
- ✅ `ws.serializeAttachment(data)` - persist metadata
- ✅ `ctx.getWebSockets().forEach()` - restore in constructor
- ✅ Use alarms instead of `setTimeout`/`setInterval`
- ❌ `ws.accept()` - standard API, no hibernation
- ❌ `setTimeout`/`setInterval` - prevents hibernation
- ❌ In-progress `fetch()` - blocks hibernation

---

## Alarms API

Schedule DO to wake at future time. **Use for:** batching, cleanup, reminders, periodic tasks.

```typescript
export class Batcher extends DurableObject {
  async addItem(item: string): Promise<void> {
    // Add to buffer
    const buffer = await this.ctx.storage.get<string[]>('buffer') || [];
    buffer.push(item);
    await this.ctx.storage.put('buffer', buffer);

    // Schedule alarm if not set
    if ((await this.ctx.storage.getAlarm()) === null) {
      await this.ctx.storage.setAlarm(Date.now() + 10000);  // 10 seconds
    }
  }

  async alarm(info: { retryCount: number; isRetry: boolean }): Promise<void> {
    if (info.retryCount > 3) return;  // Give up after 3 retries

    const buffer = await this.ctx.storage.get<string[]>('buffer') || [];
    await this.processBatch(buffer);
    await this.ctx.storage.put('buffer', []);
    // Alarm auto-deleted after success
  }
}
```

**API Methods:**
- `await ctx.storage.setAlarm(Date.now() + 60000)` - set alarm (overwrites existing)
- `await ctx.storage.getAlarm()` - get timestamp or null
- `await ctx.storage.deleteAlarm()` - cancel alarm
- `async alarm(info)` - handler called when alarm fires

**Behavior:**
- ✅ At-least-once execution, auto-retries (up to 6x, exponential backoff)
- ✅ Survives hibernation/eviction
- ✅ Auto-deleted after success
- ⚠️ One alarm per DO (new alarm overwrites)

---

## RPC vs HTTP Fetch

**RPC (Recommended):** Direct method calls, type-safe, simple

```typescript
// DO class
export class Counter extends DurableObject {
  async increment(): Promise<number> {
    let value = (await this.ctx.storage.get<number>('count')) || 0;
    await this.ctx.storage.put('count', ++value);
    return value;
  }
}

// Worker calls
const stub = env.COUNTER.getByName('my-counter');
const count = await stub.increment();  // Type-safe!
```

**HTTP Fetch:** Request/response pattern, required for WebSocket upgrades

```typescript
// DO class
export class Counter extends DurableObject {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === '/increment') {
      let value = (await this.ctx.storage.get<number>('count')) || 0;
      await this.ctx.storage.put('count', ++value);
      return new Response(JSON.stringify({ count: value }));
    }
    return new Response('Not found', { status: 404 });
  }
}

// Worker calls
const stub = env.COUNTER.getByName('my-counter');
const response = await stub.fetch('https://fake-host/increment', { method: 'POST' });
const data = await response.json();
```

**When to use:** RPC for new projects (simpler), HTTP Fetch for WebSocket upgrades or complex routing

---

## Getting DO Stubs

**Three ways to get IDs:**

1. **`idFromName(name)`** - Consistent routing (same name = same DO)
```typescript
const stub = env.CHAT_ROOM.getByName('room-123');  // Aug 2025: Shortcut for idFromName + get
// Use for: chat rooms, user sessions, per-tenant logic, singletons
```

2. **`newUniqueId()`** - Random unique ID (must store for reuse)
```typescript
const id = env.MY_DO.newUniqueId({ jurisdiction: 'eu' });  // Optional: EU compliance
const idString = id.toString();  // Save to KV/D1 for later
```

3. **`idFromString(idString)`** - Recreate from saved ID
```typescript
const id = env.MY_DO.idFromString(await env.KV.get('session:123'));
const stub = env.MY_DO.get(id);
```

**Location hints (best-effort):**
```typescript
const stub = env.MY_DO.get(id, { locationHint: 'enam' });  // wnam, enam, sam, weur, eeur, apac, oc, afr, me
```

**Jurisdiction (strict enforcement):**
```typescript
const id = env.MY_DO.newUniqueId({ jurisdiction: 'eu' });  // Options: 'eu', 'fedramp'
// Cannot combine with location hints, higher latency outside jurisdiction
```

---

## Migrations

**Required for:** create, rename, delete, transfer DO classes

**1. Create:**
```jsonc
{ "migrations": [{ "tag": "v1", "new_sqlite_classes": ["Counter"] }] }  // SQLite 10GB
// Or: "new_classes": ["Counter"]  // KV 128MB (legacy)
```

**2. Rename:**
```jsonc
{ "migrations": [
  { "tag": "v1", "new_sqlite_classes": ["OldName"] },
  { "tag": "v2", "renamed_classes": [{ "from": "OldName", "to": "NewName" }] }
]}
```

**3. Delete:**
```jsonc
{ "migrations": [
  { "tag": "v1", "new_sqlite_classes": ["Counter"] },
  { "tag": "v2", "deleted_classes": ["Counter"] }  // Immediate deletion, cannot undo
]}
```

**4. Transfer:**
```jsonc
{ "migrations": [{ "tag": "v1", "transferred_classes": [
  { "from": "OldClass", "from_script": "old-worker", "to": "NewClass" }
]}]}
```

**Migration Rules:**
- ❌ Atomic (all instances migrate at once, no gradual rollout)
- ❌ Tags are unique and append-only
- ❌ Cannot enable SQLite on existing KV-backed DOs
- ✅ Code changes don't need migrations (only schema changes)
- ✅ Class names globally unique per account

---

## Common Patterns

**Rate Limiting:**
```typescript
async checkLimit(userId: string, limit: number, window: number): Promise<boolean> {
  const requests = (await this.ctx.storage.get<number[]>(`rate:${userId}`)) || [];
  const valid = requests.filter(t => Date.now() - t < window);
  if (valid.length >= limit) return false;
  valid.push(Date.now());
  await this.ctx.storage.put(`rate:${userId}`, valid);
  return true;
}
```

**Session Management with TTL:**
```typescript
async set(key: string, value: any, ttl?: number): Promise<void> {
  const expiresAt = ttl ? Date.now() + ttl : null;
  this.sql.exec('INSERT OR REPLACE INTO session (key, value, expires_at) VALUES (?, ?, ?)',
    key, JSON.stringify(value), expiresAt);
}

async alarm(): Promise<void> {
  this.sql.exec('DELETE FROM session WHERE expires_at < ?', Date.now());
  await this.ctx.storage.setAlarm(Date.now() + 3600000);  // Hourly cleanup
}
```

**Leader Election:**
```typescript
async electLeader(workerId: string): Promise<boolean> {
  try {
    this.sql.exec('INSERT INTO leader (id, worker_id, elected_at) VALUES (1, ?, ?)', workerId, Date.now());
    return true;
  } catch { return false; }  // Already has leader
}
```

**Multi-DO Coordination:**
```typescript
// Coordinator delegates to child DOs
const gameRoom = env.GAME_ROOM.getByName(gameId);
await gameRoom.initialize();
await this.ctx.storage.put(`game:${gameId}`, { created: Date.now() });
```

---

## Critical Rules

### Always Do

✅ **Export DO class** from Worker
```typescript
export class MyDO extends DurableObject { }
export default MyDO;  // Required
```

✅ **Call `super(ctx, env)`** in constructor
```typescript
constructor(ctx: DurableObjectState, env: Env) {
  super(ctx, env);  // Required first line
}
```

✅ **Use `new_sqlite_classes`** for new DOs
```jsonc
{ "tag": "v1", "new_sqlite_classes": ["MyDO"] }
```

✅ **Use `ctx.acceptWebSocket()`** for hibernation
```typescript
this.ctx.acceptWebSocket(server);  // Enables hibernation
```

✅ **Persist critical state** to storage (not just memory)
```typescript
await this.ctx.storage.put('important', value);
```

✅ **Use alarms** instead of setTimeout/setInterval
```typescript
await this.ctx.storage.setAlarm(Date.now() + 60000);
```

✅ **Use parameterized SQL queries**
```typescript
this.sql.exec('SELECT * FROM table WHERE id = ?', id);
```

✅ **Minimize constructor work**
```typescript
constructor(ctx, env) {
  super(ctx, env);
  // Minimal initialization only
  ctx.blockConcurrencyWhile(async () => {
    // Load from storage
  });
}
```

### Never Do

❌ **Create DO without migration**
```jsonc
// Missing migrations array = error
```

❌ **Forget to export DO class**
```typescript
class MyDO extends DurableObject { }
// Missing: export default MyDO;
```

❌ **Use `setTimeout` or `setInterval`**
```typescript
setTimeout(() => {}, 1000);  // Prevents hibernation
```

❌ **Rely only on in-memory state** with WebSockets
```typescript
// ❌ WRONG: this.sessions will be lost on hibernation
// ✅ CORRECT: Use serializeAttachment()
```

❌ **Deploy migrations gradually**
```bash
# Migrations are atomic - cannot use gradual rollout
```

❌ **Enable SQLite on existing KV-backed DO**
```jsonc
// Not supported - must create new DO class instead
```

❌ **Use standard WebSocket API** expecting hibernation
```typescript
ws.accept();  // ❌ No hibernation
this.ctx.acceptWebSocket(ws);  // ✅ Hibernation enabled
```

❌ **Assume location hints are guaranteed**
```typescript
// Location hints are best-effort only
```

---

## Known Issues Prevention

This skill prevents **15+ documented issues**:

### Issue #1: Class Not Exported
**Error**: `"binding not found"` or `"Class X not found"`
**Source**: https://developers.cloudflare.com/durable-objects/get-started/
**Why It Happens**: DO class not exported from Worker
**Prevention**:
```typescript
export class MyDO extends DurableObject { }
export default MyDO;  // ← Required
```

### Issue #2: Missing Migration
**Error**: `"migrations required"` or `"no migration found for class"`
**Source**: https://developers.cloudflare.com/durable-objects/reference/durable-objects-migrations/
**Why It Happens**: Created DO class without migration entry
**Prevention**: Always add migration when creating new DO class
```jsonc
{
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["MyDO"] }
  ]
}
```

### Issue #3: Wrong Migration Type (KV vs SQLite)
**Error**: Schema errors, storage API mismatch
**Source**: https://developers.cloudflare.com/durable-objects/api/sqlite-storage-api/
**Why It Happens**: Used `new_classes` instead of `new_sqlite_classes`
**Prevention**: Use `new_sqlite_classes` for SQLite backend (recommended)

### Issue #4: Constructor Overhead Blocks Hibernation Wake
**Error**: Slow hibernation wake-up times
**Source**: https://developers.cloudflare.com/durable-objects/best-practices/access-durable-objects-storage/
**Why It Happens**: Heavy work in constructor
**Prevention**: Minimize constructor, use `blockConcurrencyWhile()`
```typescript
constructor(ctx, env) {
  super(ctx, env);
  ctx.blockConcurrencyWhile(async () => {
    // Load from storage
  });
}
```

### Issue #5: setTimeout Breaks Hibernation
**Error**: DO never hibernates, high duration charges
**Source**: https://developers.cloudflare.com/durable-objects/concepts/durable-object-lifecycle/
**Why It Happens**: `setTimeout`/`setInterval` prevents hibernation
**Prevention**: Use alarms API instead
```typescript
// ❌ WRONG
setTimeout(() => {}, 1000);

// ✅ CORRECT
await this.ctx.storage.setAlarm(Date.now() + 1000);
```

### Issue #6: In-Memory State Lost on Hibernation
**Error**: WebSocket metadata lost, state reset unexpectedly
**Source**: https://developers.cloudflare.com/durable-objects/best-practices/websockets/
**Why It Happens**: Relied on in-memory state that's cleared on hibernation
**Prevention**: Use `serializeAttachment()` for WebSocket metadata
```typescript
ws.serializeAttachment({ userId, username });

// Restore in constructor
ctx.getWebSockets().forEach(ws => {
  const metadata = ws.deserializeAttachment();
  this.sessions.set(ws, metadata);
});
```

### Issue #7: Outgoing WebSocket Cannot Hibernate
**Error**: High charges despite hibernation API
**Source**: https://developers.cloudflare.com/durable-objects/best-practices/websockets/
**Why It Happens**: Outgoing WebSockets don't support hibernation
**Prevention**: Only use hibernation for server-side (incoming) WebSockets

### Issue #8: Global Uniqueness Confusion
**Error**: Unexpected DO class name conflicts
**Source**: https://developers.cloudflare.com/durable-objects/platform/known-issues/#global-uniqueness
**Why It Happens**: DO class names are globally unique per account
**Prevention**: Understand DO class names are shared across all Workers in account

### Issue #9: Partial deleteAll on KV Backend
**Error**: Storage not fully deleted, billing continues
**Source**: https://developers.cloudflare.com/durable-objects/api/legacy-kv-storage-api/
**Why It Happens**: KV backend `deleteAll()` can fail partially
**Prevention**: Use SQLite backend for atomic deleteAll

### Issue #10: Binding Name Mismatch
**Error**: Runtime error accessing DO binding
**Source**: https://developers.cloudflare.com/durable-objects/get-started/
**Why It Happens**: Binding name in wrangler.jsonc doesn't match code
**Prevention**: Ensure consistency
```jsonc
{ "bindings": [{ "name": "MY_DO", "class_name": "MyDO" }] }
```
```typescript
env.MY_DO.getByName('instance');  // Must match binding name
```

### Issue #11: State Size Exceeded
**Error**: `"state limit exceeded"` or storage errors
**Source**: https://developers.cloudflare.com/durable-objects/platform/pricing/
**Why It Happens**: Exceeded 1GB (SQLite) or 128MB (KV) limit
**Prevention**: Monitor storage size, implement cleanup with alarms

### Issue #12: Migration Not Atomic
**Error**: Gradual deployment blocked
**Source**: https://developers.cloudflare.com/workers/configuration/versions-and-deployments/gradual-deployments/
**Why It Happens**: Tried to use gradual rollout with migrations
**Prevention**: Migrations deploy atomically across all instances

### Issue #13: Location Hint Ignored
**Error**: DO created in wrong region
**Source**: https://developers.cloudflare.com/durable-objects/reference/data-location/
**Why It Happens**: Location hints are best-effort, not guaranteed
**Prevention**: Use jurisdiction for strict requirements

### Issue #14: Alarm Retry Failures
**Error**: Tasks lost after alarm failures
**Source**: https://developers.cloudflare.com/durable-objects/api/alarms/
**Why It Happens**: Alarm handler throws errors repeatedly
**Prevention**: Implement idempotent alarm handlers
```typescript
async alarm(info: { retryCount: number }): Promise<void> {
  if (info.retryCount > 3) {
    console.error('Giving up after 3 retries');
    return;
  }
  // Idempotent operation
}
```

### Issue #15: Fetch Blocks Hibernation
**Error**: DO never hibernates despite using hibernation API
**Source**: https://developers.cloudflare.com/durable-objects/concepts/durable-object-lifecycle/
**Why It Happens**: In-progress `fetch()` requests prevent hibernation
**Prevention**: Ensure all async I/O completes before idle period

---

## Configuration & Types

**wrangler.jsonc:**
```jsonc
{
  "compatibility_date": "2025-11-23",
  "durable_objects": {
    "bindings": [{ "name": "COUNTER", "class_name": "Counter" }]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["Counter"] },
    { "tag": "v2", "renamed_classes": [{ "from": "Counter", "to": "CounterV2" }] }
  ]
}
```

**TypeScript:**
```typescript
import { DurableObject, DurableObjectState, DurableObjectNamespace } from 'cloudflare:workers';

interface Env { MY_DO: DurableObjectNamespace<MyDurableObject>; }

export class MyDurableObject extends DurableObject<Env> {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
  }
}
```

---

## Official Documentation

- **Durable Objects**: https://developers.cloudflare.com/durable-objects/
- **State API (SQL)**: https://developers.cloudflare.com/durable-objects/api/sqlite-storage-api/
- **WebSocket Hibernation**: https://developers.cloudflare.com/durable-objects/best-practices/websockets/
- **Alarms API**: https://developers.cloudflare.com/durable-objects/api/alarms/
- **Migrations**: https://developers.cloudflare.com/durable-objects/reference/durable-objects-migrations/
- **Best Practices**: https://developers.cloudflare.com/durable-objects/best-practices/
- **Pricing**: https://developers.cloudflare.com/durable-objects/platform/pricing/

---

**Questions? Issues?**

1. Check `references/top-errors.md` for common problems
2. Review `templates/` for working examples
3. Consult official docs: https://developers.cloudflare.com/durable-objects/
4. Verify migrations configuration carefully

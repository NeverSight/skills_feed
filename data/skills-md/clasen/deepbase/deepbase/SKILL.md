---
name: deepbase
description: Instructions for using the DeepBase multi-driver persistence library. Use when a task requires data persistence, storage abstraction, multi-backend setups, data migration between drivers, or integrating DeepBase into a Node.js project.
version: 3.4.4
tags: [nodejs, persistence, database, multi-driver, mongodb, redis, sqlite, json]
---

# DeepBase

## Overview

DeepBase is a multi-driver persistence system for Node.js that provides a unified API across storage backends (JSON, SQLite, MongoDB, Redis, IndexedDB). It allows switching or combining backends without changing application code.

**Use this skill when:**
- Adding persistence to a Node.js project
- Setting up multi-backend storage with automatic failover
- Migrating data between storage drivers
- Working with nested object paths for data access
- Integrating any DeepBase driver package

**Do NOT use this skill when:**
- The project needs a full ORM or relational query builder (use Prisma, Drizzle, etc.)
- The project requires SQL queries, joins, or complex aggregations
- The task is about browser-only storage without DeepBase (use raw IndexedDB/localStorage)

## Installation

```bash
# Core package (includes JSON driver by default)
npm install deepbase

# Optional drivers — install only what you need
npm install deepbase-sqlite       # SQLite (better-sqlite3)
npm install deepbase-mongodb      # MongoDB
npm install deepbase-redis        # Redis (vanilla)
npm install deepbase-redis-json   # Redis Stack (RedisJSON)
npm install deepbase-indexeddb    # Browser IndexedDB
```

The core `deepbase` package depends on `deepbase-json` and `nanoid`. No other drivers are required unless explicitly used.

## Imports

```javascript
// ES Modules (recommended)
import DeepBase from 'deepbase';
import { DeepBase, DeepBaseDriver } from 'deepbase';

// CommonJS
const { DeepBase } = require('deepbase');

// Individual drivers
import { JsonDriver } from 'deepbase-json';
import { MongoDriver } from 'deepbase-mongodb';
import { SqliteDriver } from 'deepbase-sqlite';
import { RedisDriver } from 'deepbase-redis';
import { RedisDriver as RedisJsonDriver } from 'deepbase-redis-json';
import { IndexedDBDriver } from 'deepbase-indexeddb';
```

## Basic Usage

### Single driver (JSON — simplest setup)

```javascript
import DeepBase from 'deepbase';

const db = new DeepBase({ path: './data', name: 'app' });
await db.connect();

await db.set('config', 'theme', 'dark');
const theme = await db.get('config', 'theme'); // 'dark'

await db.disconnect();
```

Lazy connect is enabled by default — `connect()` is called automatically on first operation if omitted.

### Multi-driver with failover

```javascript
import DeepBase from 'deepbase';
import { JsonDriver } from 'deepbase-json';
import { MongoDriver } from 'deepbase-mongodb';

const db = new DeepBase([
  new MongoDriver({ url: 'mongodb://localhost:27017', database: 'myapp', collection: 'data' }),
  new JsonDriver({ path: './backup', name: 'fallback' })
], {
  writeAll: true,            // Write to all drivers (default: true)
  readFirst: true,           // Read from first available (default: true)
  failOnPrimaryError: false  // Continue if primary fails
});

await db.connect();
// Writes go to both MongoDB and JSON; reads try MongoDB first, fall back to JSON
```

## API Reference

All methods are async. Path arguments are variadic strings representing nested keys.

### Data operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `get` | `get(...path)` | Get value at path. Returns `null` if not found. |
| `set` | `set(...path, value)` | Set value at path. Last argument is the value. |
| `del` | `del(...path)` | Delete value at path. |
| `inc` | `inc(...path, amount)` | Increment numeric value. |
| `dec` | `dec(...path, amount)` | Decrement numeric value. |
| `add` | `add(...path, value)` | Add item with auto-generated ID. Returns full path array. |
| `upd` | `upd(...path, fn)` | Atomic update — passes current value to `fn`, stores the return value. |

### Query operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `keys` | `keys(...path)` | Get keys at path (array of strings). |
| `values` | `values(...path)` | Get values at path. |
| `entries` | `entries(...path)` | Get `[key, value]` pairs at path. |
| `pop` | `pop(...path)` | Remove and return the last item. |
| `shift` | `shift(...path)` | Remove and return the first item. |

### Connection

| Method | Description |
|--------|-------------|
| `connect()` | Connect all drivers. Returns `{ connected, total }`. |
| `disconnect()` | Disconnect all drivers. |

### Driver access

| Method | Description |
|--------|-------------|
| `getDriver(index)` | Get driver instance by index (default: 0). |
| `getDrivers()` | Get array of all driver instances. |

### Migration

```javascript
// Migrate data from driver 0 to driver 1
await db.migrate(0, 1, {
  clear: true,       // Clear target first (default: true)
  batchSize: 100,    // Progress callback interval
  onProgress: ({ migrated, errors, current }) => console.log(`${migrated} items`)
});

// Sync primary (index 0) to all other drivers
await db.syncAll({ clear: true });
```

## Constructor Options

```javascript
new DeepBase(drivers, {
  writeAll: true,              // Write to all drivers
  readFirst: true,             // Read from first available driver in order
  failOnPrimaryError: true,    // Throw if primary driver (index 0) fails
  lazyConnect: true,           // Auto-connect on first operation
  timeout: 0,                  // Global timeout in ms (0 = disabled)
  readTimeout: 0,              // Override for read operations
  writeTimeout: 0,             // Override for write operations
  connectTimeout: 0            // Override for connect
});
```

## Driver Configuration

| Driver | Key Options |
|--------|-------------|
| `JsonDriver` | `path` (directory), `name` (filename), `stringify` / `parse` (custom serialization) |
| `SqliteDriver` | `path` (directory), `name` (database filename) |
| `MongoDriver` | `url`, `database`, `collection` |
| `RedisDriver` | `url`, `prefix` |
| `RedisJsonDriver` | `url`, `prefix` (requires Redis Stack with RedisJSON module) |
| `IndexedDBDriver` | `name`, `version` |

## Agent Usage Rules

1. **Check before installing.** Verify `package.json` for existing `deepbase` dependency before running `npm install`.
2. **Use the official API.** Never manipulate driver internals or the underlying JSON/SQLite/Mongo storage directly. Always go through `db.get()`, `db.set()`, etc.
3. **Prefer lazy connect.** Do not call `db.connect()` explicitly unless you need the `{ connected, total }` result. Lazy connect handles it automatically.
4. **Always `disconnect()` on shutdown.** Especially important for MongoDB and Redis drivers to release connections.
5. **Use `add()` for auto-IDs.** Do not manually generate IDs with nanoid/uuid — `add()` returns the full path array including the generated ID.
6. **Spread the path from `add()`.** The return value is an array: use `await db.get(...userPath)` to retrieve the added item.
7. **Use `upd()` for atomic changes.** When modifying existing values based on their current state, use `upd()` instead of `get()` + `set()` to avoid race conditions.
8. **Set `failOnPrimaryError: false` for resilient setups.** When using multi-driver for fault tolerance, disable this so operations continue via fallback drivers.
9. **Use environment variables for connection strings.** Never hardcode MongoDB URLs or Redis URLs in source code.
10. **Prefer `deepbase-redis-json` over `deepbase-redis`** when working with Redis Stack, as it supports native JSON operations.

## Common Tasks

### Store and retrieve nested data

```javascript
await db.set('users', 'alice', { name: 'Alice', age: 30 });
await db.set('users', 'alice', 'email', 'alice@example.com');
const user = await db.get('users', 'alice');
// { name: 'Alice', age: 30, email: 'alice@example.com' }
```

### Add items with auto-generated IDs

```javascript
const userPath = await db.add('users', { name: 'Bob', email: 'bob@example.com' });
// userPath = ['users', 'aB3xK9mL2n']
const user = await db.get(...userPath);
```

### Increment/decrement counters

```javascript
await db.set('stats', 'views', 0);
await db.inc('stats', 'views');      // 1
await db.inc('stats', 'views', 10);  // 11
await db.dec('stats', 'views', 5);   // 6
```

### Atomic update

```javascript
await db.upd('user', 'name', name => name.toUpperCase());
```

### Iterate over collections

```javascript
const userKeys = await db.keys('users');
const userList = await db.values('users');
const userEntries = await db.entries('users'); // [[id, data], ...]
```

### Pop/shift from collections

```javascript
const last = await db.pop('queue');    // Remove and return last item
const first = await db.shift('queue'); // Remove and return first item
```

### Custom JSON serialization (circular references)

```javascript
import { JsonDriver } from 'deepbase-json';
import { stringify, parse } from 'flatted';

const db = new DeepBase(new JsonDriver({
  path: './data',
  name: 'circular',
  stringify,
  parse
}));
```

### Three-tier architecture

```javascript
const db = new DeepBase([
  new MongoDriver({ url: process.env.MONGO_URL, database: 'app' }),
  new JsonDriver({ path: './backup' }),
  new RedisDriver({ url: process.env.REDIS_URL })
], { writeAll: true, failOnPrimaryError: false });
```

### Extend with a custom driver

```javascript
import { DeepBaseDriver } from 'deepbase';

class MyDriver extends DeepBaseDriver {
  async connect() { /* ... */ this._connected = true; }
  async disconnect() { /* ... */ }
  async get(...args) { /* ... */ }
  async set(...args) { /* ... */ }
  async del(...args) { /* ... */ }
  async inc(...args) { /* ... */ }
  async dec(...args) { /* ... */ }
  async add(...args) { /* ... */ }
  async upd(...args) { /* ... */ }
}
```

All methods listed in `DeepBaseDriver` must be implemented. `keys()`, `values()`, `entries()` have default implementations that call `get()`.

## Troubleshooting

- **`All drivers must extend DeepBaseDriver`** — Ensure all drivers in the array are proper driver instances, not plain objects.
- **Operation timed out** — Increase `timeout`, `readTimeout`, or `writeTimeout` in the constructor options.
- **MongoDB/Redis connection fails silently** — Set `failOnPrimaryError: true` (default) to surface connection errors, or check `connect()` return value for `{ connected, total }`.
- **Data not synced across drivers** — Ensure `writeAll: true` (default). For existing data, use `db.migrate()` or `db.syncAll()`.
- **Stale reads after failover** — The fallback driver may have older data. Use `db.syncAll()` after the primary recovers.

## References

- Repository: https://github.com/clasen/DeepBase
- npm: https://www.npmjs.com/package/deepbase
- Examples: `examples/` directory in the repository (01 through 12)
- Monorepo packages: `packages/core`, `packages/driver-json`, `packages/driver-sqlite`, `packages/driver-mongodb`, `packages/driver-redis`, `packages/driver-redis-json`, `packages/driver-indexeddb`

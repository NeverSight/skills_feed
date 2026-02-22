---
name: bun
description: |
  Bun runtime, package manager, bundler, and test runner.
  Use when running scripts with bun, managing packages, serving HTTP with Bun.serve,
  querying databases with Bun.sql/bun:sqlite/Bun.redis, shell scripting with $,
  using S3/file I/O, writing tests with bun:test, bundling or compiling to executable,
  or using any Bun-specific API (spawn, glob, semver, FFI, workers, plugins, HTMLRewriter).
---

# Bun

## Quick Start

```bash
# Install
curl -fsSL https://bun.sh/install | bash

# Init project
bun init

# Run TypeScript directly
bun run index.ts

# Watch mode (hard restart on change)
bun --watch index.ts

# Hot reload (preserves global state, no restart)
bun --hot server.ts
```

## Package Management

```bash
bun install                    # install all deps
bun add express                # add dependency
bun add -d @types/node         # add dev dependency
bun remove lodash              # remove
bun update                     # update all
bun update --latest            # ignore semver ranges
bunx prettier --write .        # execute package binary (npx equivalent)
bun patch express              # patch a dependency in node_modules
```

### Workspaces

```json
// root package.json
{ "workspaces": ["packages/*"] }

// child package.json
{ "dependencies": { "shared": "workspace:*" } }
```

```bash
bun install --filter "pkg-*"   # install filtered workspaces
```

### Environment Variables

`.env` files auto-loaded in order: `.env` → `.env.$(NODE_ENV)` → `.env.local`

```ts
Bun.env.API_KEY       // Bun-native
process.env.API_KEY   // Node.js compat
import.meta.env.API_KEY
```

```bash
bun --env-file=.env.staging run start
```

## HTTP Server

```ts
Bun.serve({
  port: 3000,
  routes: {
    "/": new Response("Home"),
    "/users/:id": (req) => Response.json({ id: req.params.id }),
    "/api/posts": {
      GET: () => Response.json([]),
      POST: async (req) => Response.json(await req.json(), { status: 201 }),
    },
    "/api/*": Response.json({ error: "Not found" }, { status: 404 }),
    "/favicon.ico": Bun.file("./favicon.ico"),
  },
  fetch(req) {
    return new Response("Not Found", { status: 404 });
  },
});
```

### WebSocket Upgrade

```ts
Bun.serve({
  fetch(req, server) {
    if (server.upgrade(req, { data: { userId: "123" } })) return;
    return new Response("Not a WebSocket", { status: 400 });
  },
  websocket: {
    open(ws) { ws.subscribe("chat"); },
    message(ws, msg) { ws.publish("chat", msg); },
    close(ws) {},
  },
});
```

### Fullstack (HTML Imports)

```ts
import homepage from "./index.html";

Bun.serve({
  routes: { "/": homepage },
  development: true, // enables HMR
});
```

See [references/http-server.md](references/http-server.md) for cookies, static routes, TLS, server lifecycle, metrics.

## Databases

### Bun.sql (Postgres / MySQL / SQLite)

```ts
import { sql, SQL } from "bun";

// Auto-reads DATABASE_URL / POSTGRES_URL / MYSQL_URL
const users = await sql`SELECT * FROM users WHERE active = ${true}`;

// Explicit connection
const pg = new SQL("postgres://user:pass@localhost:5432/mydb");
const mysql = new SQL("mysql://user:pass@localhost:3306/mydb");
const sqlite = new SQL(":memory:");

// Insert with object helper
const [user] = await sql`INSERT INTO users ${sql({ name: "Alice", email: "a@b.com" })} RETURNING *`;

// Bulk insert
await sql`INSERT INTO users ${sql([user1, user2, user3])}`;

// Transactions
await sql.begin(async (tx) => {
  const [u] = await tx`INSERT INTO users ${sql({ name: "Bob" })} RETURNING *`;
  await tx`INSERT INTO accounts (user_id) VALUES (${u.id})`;
});
```

### bun:sqlite (Sync, Embedded)

```ts
import { Database } from "bun:sqlite";

const db = new Database("app.db");
db.run("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, val TEXT)");
const row = db.query("SELECT * FROM kv WHERE key = ?").get("foo");
const all = db.query("SELECT * FROM kv").all();

// Class mapping
class User { id!: number; name!: string; }
const users = db.query("SELECT * FROM users").as(User).all();
```

### Bun.redis

```ts
import { redis } from "bun";

await redis.set("key", "value", { ex: 60 });
const val = await redis.get("key");
await redis.del("key");
await redis.hmset("user:1", { name: "Alice", role: "admin" });
```

See [references/database.md](references/database.md) for transactions, savepoints, MySQL/SQLite specifics, Redis pub/sub, connection options.

## Shell ($)

```ts
import { $ } from "bun";

// Run and print to stdout
await $`echo "Hello"`;

// Capture output
const text = await $`ls -la`.text();
const data = await $`cat config.json`.json();
for await (const line of $`cat file.txt`.lines()) { }

// Pipes
await $`cat file.txt | grep "pattern" | wc -l`;

// Redirect from/to JS objects
await $`cat < ${new Response("data")} > ${Bun.file("out.txt")}`;

// Error handling
const { exitCode } = await $`may-fail`.nothrow().quiet();

// Config
$.cwd("/tmp");
$.env({ ...process.env, NODE_ENV: "production" });
```

**Security:** Interpolated variables are auto-escaped (no shell injection). Use `{ raw: str }` to bypass.

See [references/shell.md](references/shell.md) for builtins, command substitution, brace expansion.

## File I/O & S3

```ts
// Read
const file = Bun.file("data.json");
const json = await file.json();       // also: .text(), .bytes(), .stream(), .arrayBuffer()
console.log(file.size, file.type);    // size in bytes, MIME type

// Write
await Bun.write("out.txt", "hello");
await Bun.write(Bun.file("copy.bin"), Bun.file("src.bin")); // copy file

// Incremental write
const writer = Bun.file("log.txt").writer();
writer.write("line 1\n");
writer.write("line 2\n");
writer.end();

// S3
import { s3 } from "bun";
const obj = s3.file("data.json");
const data = await obj.json();
await obj.write(JSON.stringify({ ok: true }));
const url = obj.presign({ expiresIn: 3600, method: "PUT" });
await obj.delete();

// s3:// protocol
const res = await fetch("s3://bucket/file.txt");

// Glob
const glob = new Bun.Glob("**/*.ts");
for await (const path of glob.scan(".")) console.log(path);
```

See [references/file-io.md](references/file-io.md) for S3 credentials, multipart uploads, streams, hashing, semver.

## Testing

```ts
import { test, expect, describe, mock, spyOn, beforeEach } from "bun:test";

describe("math", () => {
  test("adds", () => expect(1 + 1).toBe(2));

  test.each([
    [1, 2, 3],
    [4, 5, 9],
  ])("%i + %i = %i", (a, b, expected) => {
    expect(a + b).toBe(expected);
  });

  test.skip("wip", () => {});
  test.todo("implement later");
});

// Mock functions
const fn = mock(() => 42);
fn();
expect(fn).toHaveBeenCalled();

// Module mocking
mock.module("./db", () => ({
  query: mock(() => []),
}));

// Spies
const spy = spyOn(console, "log");
console.log("test");
expect(spy).toHaveBeenCalledWith("test");

// Snapshots
test("snap", () => {
  expect({ a: 1, b: "hello" }).toMatchSnapshot();
});
```

```bash
bun test                          # run all tests
bun test --watch                  # watch mode
bun test --coverage               # with coverage
bun test --update-snapshots       # update snapshots
bun test --bail                   # stop on first failure
bun test --test-name-pattern "add" # filter by name
```

See [references/testing.md](references/testing.md) for all matchers, lifecycle hooks, type testing, retry/repeats, DOM testing.

## Bundler & Compile

```ts
// Bundle for browser
const result = await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  splitting: true,
  minify: true,
  sourcemap: "linked",
  target: "browser", // or "bun", "node"
});

if (!result.success) {
  for (const log of result.logs) console.error(log);
}
```

```bash
# Compile to standalone executable
bun build --compile --minify --sourcemap --bytecode ./app.ts --outfile myapp

# Cross-compile
bun build --compile --target=bun-linux-x64 ./app.ts --outfile myapp-linux
bun build --compile --target=bun-darwin-arm64 ./app.ts --outfile myapp-mac
```

```ts
// Embed files in executable
import icon from "./icon.png" with { type: "file" };
import db from "./data.db" with { type: "sqlite", embed: "true" };
```

See [references/bundler.md](references/bundler.md) for all build options, plugins, cross-compile targets, Windows options, Transpiler API.

## Child Processes

```ts
// Async
const proc = Bun.spawn(["ls", "-la"], {
  cwd: "/tmp",
  stdout: "pipe",
});
const output = await new Response(proc.stdout).text();
await proc.exited;

// Sync
const { stdout, exitCode } = Bun.spawnSync(["echo", "hi"]);

// Timeout + abort
const ctrl = new AbortController();
Bun.spawn(["sleep", "100"], { signal: ctrl.signal, timeout: 5000 });

// IPC between bun processes
const child = Bun.spawn(["bun", "worker.ts"], {
  ipc(msg) { console.log("from child:", msg); },
});
child.send({ type: "start" });
```

## Configuration (bunfig.toml)

```toml
# Common options
preload = ["./setup.ts"]
logLevel = "warn"

[run]
shell = "bun"                    # use Bun's shell instead of system shell
bun = true                       # alias node to bun in scripts

[test]
preload = ["./test-setup.ts"]
coverage = true
coverageThreshold = 0.8
retry = 2

[install]
exact = true                     # pin exact versions
frozenLockfile = true            # CI: fail if lockfile out of date
auto = "fallback"                # auto-install missing packages
```

See [references/configuration.md](references/configuration.md) for full bunfig.toml reference.

## Reference Index

| Topic | Reference |
|-------|-----------|
| HTTP server, routing, WebSockets, cookies, fullstack | [references/http-server.md](references/http-server.md) |
| Bun.sql, bun:sqlite, Bun.redis | [references/database.md](references/database.md) |
| TCP, UDP, DNS, fetch | [references/networking.md](references/networking.md) |
| Bun Shell ($) | [references/shell.md](references/shell.md) |
| bun:test, mocking, snapshots, coverage | [references/testing.md](references/testing.md) |
| Bun.build, compile to executable, plugins | [references/bundler.md](references/bundler.md) |
| Bun.file, S3, Glob, streams, hashing, semver | [references/file-io.md](references/file-io.md) |
| bunfig.toml full reference | [references/configuration.md](references/configuration.md) |
| Workers, HTMLRewriter, FFI, C compiler, secrets, Node.js compat | [references/advanced.md](references/advanced.md) |

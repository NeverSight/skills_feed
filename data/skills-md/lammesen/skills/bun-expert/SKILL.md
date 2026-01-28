---
name: bun-expert
description: |
  Comprehensive Bun runtime expertise covering all major features.
  Use when working with Bun projects, migrating from Node.js, or leveraging Bun-specific APIs.
  Activates for: Bun.serve, Bun.file, bun:test, bun:sqlite, bun install, bun build,
  bunfig.toml, TypeScript in Bun, package manager operations, bundler configuration,
  and Node.js compatibility questions.
allowed-tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash
---

# Bun Expert Skill

You are an expert Bun developer with deep knowledge of the Bun runtime, package manager, test runner, and bundler. You help users build high-performance JavaScript/TypeScript applications using Bun's native APIs and guide migrations from Node.js.

## Core Expertise Areas

### 1. Bun Runtime APIs

**HTTP Server & Networking:**
- `Bun.serve(options)` - High-performance HTTP/WebSocket server (2.5x faster than Node.js)
- `Bun.fetch(url)` - Extended Web Fetch API
- `Bun.connect()` / `Bun.listen()` - TCP/UDP socket APIs
- `Bun.dns` - DNS resolution utilities

**File System Operations:**
- `Bun.file(path)` - Returns BunFile (extends Blob) for lazy, zero-copy file operations
- `Bun.write(path, data)` - Optimized file writes
- `Bun.stdin` / `Bun.stdout` / `Bun.stderr` - Standard I/O streams

**Process & Shell:**
- `Bun.spawn(cmd)` / `Bun.spawnSync(cmd)` - Child process spawning
- `Bun.$\`command\`` - Cross-platform shell scripting with template literals
- Built-in commands: `ls`, `cd`, `rm`, `cat`, `echo`, `pwd`, `mkdir`, `touch`, `which`, `mv`

**Data & Storage:**
- `bun:sqlite` - Built-in SQLite3 driver (3-6x faster than better-sqlite3)
- `Bun.sql` - Unified SQL API for PostgreSQL, MySQL, SQLite
- `Bun.S3Client` / `Bun.s3` - Native S3-compatible storage (5x faster than AWS SDK)
- `Bun.redis` - Built-in Redis client

**Utilities:**
- `Bun.password.hash()` / `Bun.password.verify()` - Argon2 password hashing
- `Bun.hash(data)` - Fast hashing (xxhash, murmur)
- `Bun.Glob` - Native glob pattern matching
- `Bun.semver` - Semver comparison utilities
- `Bun.sleep(ms)` / `Bun.sleepSync(ms)` - Sleep functions
- `Bun.deepEquals(a, b)` - Deep comparison
- `Bun.escapeHTML()` - HTML sanitization
- `Bun.YAML.parse()` / `Bun.YAML.stringify()` - Native YAML support
- `HTMLRewriter` - HTML streaming transformations

**Advanced Features:**
- `bun:ffi` - Foreign Function Interface (2-6x faster than Node.js FFI)
- `Worker` - Web Workers API for multi-threading
- `BroadcastChannel` - Pub/sub messaging across threads
- `Bun.Transpiler` - JavaScript/TypeScript transpilation API
- `Bun.build()` - Bundler API with compile support

---

### 2. Package Manager Commands

**Core Commands:**
```bash
bun install              # Install all dependencies
bun install --frozen-lockfile  # CI/CD lockfile validation
bun add <pkg>            # Add dependency
bun add -d <pkg>         # Add devDependency
bun remove <pkg>         # Remove dependency
bun update               # Update outdated packages
bun ci                   # CI-optimized install (--frozen-lockfile)
bunx <pkg>               # Execute package without installing (100x faster than npx)
```

**Workspace Support:**
```json
{
  "workspaces": ["packages/*", "apps/*"],
  "dependencies": {
    "shared-pkg": "workspace:*"
  }
}
```

**Package Management:**
```bash
bun pm trust <pkg>       # Allow lifecycle scripts
bun pm untrusted         # View blocked scripts
bun why <pkg>            # Explain why package installed
bun outdated             # Show outdated packages
bun audit                # Security vulnerability check
bun patch <pkg>          # Prepare package for patching
bun link                 # Link local packages
```

**Lockfile:** Bun uses `bun.lock` (text-based JSONC format) - human-readable, git-diffable. Automatically migrates from `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`.

---

### 3. Test Runner (bun:test)

**Test Syntax:**
```typescript
import { describe, test, expect, beforeAll, afterEach, mock, spyOn } from "bun:test";

describe("feature", () => {
  beforeAll(() => { /* setup */ });
  afterEach(() => { mock.restore(); });

  test("basic assertion", () => {
    expect(2 + 2).toBe(4);
  });

  test("async operation", async () => {
    const result = await fetchData();
    expect(result).toMatchObject({ status: "ok" });
  });

  test.each([[1, 2, 3], [2, 3, 5]])("adds %i + %i = %i", (a, b, expected) => {
    expect(a + b).toBe(expected);
  });
});
```

**Test Modifiers:**
- `test.skip()` - Skip test
- `test.only()` - Run only this test (with `--only` flag)
- `test.todo()` - Mark as todo
- `test.if(condition)` / `test.skipIf(condition)` - Conditional execution
- `test.failing()` - Expected to fail
- `test.concurrent` - Run concurrently
- `test.retry(n)` - Retry failed tests

**Key Matchers:**
- `.toBe()`, `.toEqual()`, `.toStrictEqual()` - Equality
- `.toContain()`, `.toHaveLength()`, `.toMatch()` - String/Array
- `.toHaveProperty()`, `.toMatchObject()` - Objects
- `.toThrow()`, `.rejects.toThrow()` - Errors
- `.toMatchSnapshot()`, `.toMatchInlineSnapshot()` - Snapshots
- `.toHaveBeenCalled()`, `.toHaveBeenCalledWith()` - Mocks

**Mocking:**
```typescript
import { mock, spyOn } from "bun:test";

const mockFn = mock(() => 42);
mockFn.mockImplementation(() => 100);
mockFn.mockReturnValue(200);

const spy = spyOn(object, "method");
spy.mockResolvedValue({ data: "test" });

// Module mocking
mock.module("./api", () => ({
  fetchUser: mock(() => ({ id: 1, name: "Test" }))
}));
```

**CLI Commands:**
```bash
bun test                 # Run all tests
bun test --watch         # Watch mode
bun test --coverage      # Enable coverage
bun test -t "pattern"    # Filter by test name
bun test --timeout=5000  # Set timeout
bun test --bail          # Stop on first failure
bun test --update-snapshots  # Update snapshots
```

---

### 4. Bundler Configuration

**JavaScript API:**
```typescript
const result = await Bun.build({
  entrypoints: ["./src/index.tsx"],
  outdir: "./dist",
  target: "browser",  // "browser" | "bun" | "node"
  format: "esm",      // "esm" | "cjs" | "iife"
  minify: true,
  sourcemap: "external",
  splitting: true,    // Code splitting
  external: ["react", "react-dom"],
  define: {
    "process.env.NODE_ENV": '"production"'
  },
  loader: {
    ".png": "dataurl",
    ".svg": "text"
  },
  plugins: [myPlugin],
  naming: {
    entry: "[dir]/[name].[ext]",
    chunk: "[name]-[hash].[ext]"
  }
});

if (!result.success) {
  console.error(result.logs);
}
```

**CLI:**
```bash
bun build ./src/index.tsx --outdir ./dist --minify --sourcemap=external
bun build ./src/index.ts --compile --outfile myapp  # Single executable
```

**Plugin System:**
```typescript
const myPlugin: BunPlugin = {
  name: "yaml-loader",
  setup(build) {
    build.onLoad({ filter: /\.yaml$/ }, async (args) => {
      const text = await Bun.file(args.path).text();
      return {
        contents: `export default ${JSON.stringify(YAML.parse(text))}`,
        loader: "js"
      };
    });
  }
};
```

---

### 5. TypeScript Integration

Bun executes TypeScript natively without transpilation configuration:
```bash
bun run index.ts      # Just works
bun run index.tsx     # JSX supported
```

**Recommended tsconfig.json:**
```json
{
  "compilerOptions": {
    "lib": ["ESNext"],
    "target": "ESNext",
    "module": "ESNext",
    "moduleDetection": "force",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "noEmit": true,
    "strict": true,
    "skipLibCheck": true,
    "types": ["bun-types"]
  }
}
```

**Type checking (separate step):**
```bash
bunx tsc --noEmit
```

---

### 6. Configuration (bunfig.toml)

```toml
# Runtime
preload = ["./setup.ts"]
smol = true                    # Reduced memory mode

# JSX
[jsx]
runtime = "automatic"
importSource = "react"

# Package installation
[install]
optional = false
lockfile.save = true

[install.scopes]
"@myorg" = { url = "https://npm.myorg.com", token = "$NPM_TOKEN" }

# Test runner
[test]
preload = ["./test-setup.ts"]
coverage = true
coverageThreshold = { lines = 0.8, functions = 0.8 }
```

---

### 7. CLI Flags Reference

**Execution:**
- `--watch` - Auto-restart on file changes
- `--hot` - Hot module replacement
- `--smol` - Reduced memory mode
- `--inspect` / `--inspect-brk` - Debugger

**Module Resolution:**
- `--preload` / `-r` - Preload modules
- `--install=auto|fallback|force` - Auto-install behavior

**Transpilation:**
- `--define` / `-d` - Compile-time constants
- `--drop=console` - Remove function calls
- `--loader` - Custom file loaders

**Environment:**
- `--env-file` - Load specific .env files
- `--cwd` - Set working directory
- `--bun` / `-b` - Force Bun runtime

---

## Node.js Migration Guidance

### Quick Migration Steps

1. **Install Bun:** `curl -fsSL https://bun.sh/install | bash`
2. **Replace package manager:**
```bash
# Delete node_modules and lockfile
rm -rf node_modules package-lock.json yarn.lock pnpm-lock.yaml
bun install
```
3. **Update scripts in package.json:**
```json
{
  "scripts": {
    "dev": "bun run --watch src/index.ts",
    "test": "bun test",
    "build": "bun build src/index.ts --outdir dist"
  }
}
```
4. **Update TypeScript types:**
```bash
bun add -d @types/bun
# Or in tsconfig.json: "types": ["bun-types"]
```

### API Compatibility

**Fully Compatible:**
- `node:assert`, `node:buffer`, `node:events`, `node:path`, `node:url`
- `node:fs` (92%), `node:http`, `node:https`, `node:stream`, `node:zlib`
- `node:crypto`, `node:net`, `node:dns`, `node:os`

**Partially Compatible:**
- `node:child_process` - Missing `proc.gid`, `proc.uid`; IPC limited to JSON
- `node:cluster` - Linux-only SO_REUSEPORT for load balancing
- `node:http2` - 95% compatible; missing `pushStream`
- `node:worker_threads` - Missing `stdin`, `stdout`, `stderr` options
- `node:async_hooks` - AsyncLocalStorage works; v8 promise hooks missing

**Not Implemented:**
- `node:inspector`, `node:repl`, `node:trace_events`

### Common Migration Gotchas

1. **Native Modules:** Packages using node-gyp (bcrypt, sharp) may fail
   - Solution: Use pure JS alternatives (`bcryptjs` instead of `bcrypt`)
2. **Lifecycle Scripts:** Bun blocks postinstall by default (security)
   - Solution: `bun pm trust <package>` or add to `trustedDependencies`
3. **Module System:** Some packages relying on Node.js internals may fail
   - `Module._nodeModulePaths` doesn't exist in Bun
4. **File System Differences:** Heavy concurrent file reads can cause memory issues
   - Solution: Use `graceful-fs` wrapper
5. **TypeScript Entry Points:** Update `"main"` field for Bun:
```json
{
  "main": "src/index.ts"  // Not "build/index.js"
}
```

### Gradual Migration Strategy

**Phase 1:** Package manager only (`bun install`)
**Phase 2:** Development tooling (`bun run`, `bun test`)
**Phase 3:** Selective runtime migration (shadow deploy)
**Phase 4:** Full production migration

---

## Best Practices

### Performance Optimization

```typescript
// Use Bun's native APIs for I/O
const file = Bun.file("large.txt");  // Zero-copy
const content = await file.text();
await Bun.write("output.txt", processedData);

// Use Promise.all for concurrent operations
const [users, posts] = await Promise.all([
  db.query("SELECT * FROM users"),
  db.query("SELECT * FROM posts")
]);

// Use Bun.serve() static routes
Bun.serve({
  static: {
    "/": homepage,
    "/about": aboutPage
  },
  fetch(req) { /* dynamic routes */ }
});

// Use bun:sqlite for local data
import { Database } from "bun:sqlite";
const db = new Database(":memory:");
const stmt = db.prepare("SELECT * FROM users WHERE id = ?");
```

### Error Handling

```typescript
// HTTP server error handling
Bun.serve({
  fetch(req) {
    try {
      return handleRequest(req);
    } catch (error) {
      console.error(error);
      return new Response("Internal Error", { status: 500 });
    }
  },
  error(error) {
    return new Response(`Error: ${error.message}`, { status: 500 });
  }
});

// Process-level error handling
process.on("uncaughtException", (error) => {
  console.error("Uncaught:", error);
  process.exit(1);
});
```

### Security Best Practices

1. **Lifecycle Scripts:** Keep `trustedDependencies` minimal
2. **Environment Variables:** Use `.env.local` for secrets (not committed)
3. **Input Validation:** Sanitize all user inputs
4. **Dependencies:** Run `bun audit` regularly
5. **Production:** Use `--production` flag to skip devDependencies

### Project Structure

```
my-bun-project/
├── src/
│   ├── index.ts        # Entry point
│   ├── server.ts       # HTTP server
│   └── lib/            # Utilities
├── test/
│   └── *.test.ts       # Test files
├── bunfig.toml         # Bun configuration
├── tsconfig.json       # TypeScript config
├── package.json
└── .env.local          # Local secrets (gitignored)
```

---

## Debugging

**Web Debugger:**
```bash
bun --inspect server.ts         # Start debugger
bun --inspect-brk server.ts     # Break at first line
bun --inspect-wait server.ts    # Wait for connection
```

Open `https://debug.bun.sh` or use VSCode Bun extension.

**Verbose Fetch Logging:**
```bash
BUN_CONFIG_VERBOSE_FETCH=curl bun run server.ts
```

---

## Examples

### HTTP Server with WebSocket

```typescript
Bun.serve({
  port: 3000,
  fetch(req, server) {
    if (server.upgrade(req)) return;
    return new Response("Hello Bun!");
  },
  websocket: {
    open(ws) { console.log("Connected"); },
    message(ws, message) { ws.send(`Echo: ${message}`); },
    close(ws) { console.log("Disconnected"); }
  }
});
```

### File Server

```typescript
Bun.serve({
  async fetch(req) {
    const path = new URL(req.url).pathname;
    const file = Bun.file(`./public${path}`);
    if (await file.exists()) {
      return new Response(file);
    }
    return new Response("Not Found", { status: 404 });
  }
});
```

### Database with SQLite

```typescript
import { Database } from "bun:sqlite";

const db = new Database("app.db");
db.run(`CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE
)`);

const insert = db.prepare("INSERT INTO users (name, email) VALUES (?, ?)");
const getAll = db.prepare("SELECT * FROM users");

insert.run("Alice", "alice@example.com");
const users = getAll.all();
```

---

## When This Skill Activates

This skill automatically activates when:
- Working with `.ts`, `.tsx`, `.js`, `.jsx` files in a Bun project
- Creating or modifying `bunfig.toml` or `bun.lock`
- Using `bun:test`, `bun:sqlite`, `bun:ffi` imports
- Discussing Bun APIs (Bun.serve, Bun.file, Bun.build)
- Migrating from Node.js to Bun
- Writing or debugging Bun tests
- Configuring the Bun bundler

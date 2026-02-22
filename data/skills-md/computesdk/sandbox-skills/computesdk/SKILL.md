---
name: computesdk
description: Guide for building sandbox applications with ComputeSDK, a unified TypeScript SDK for running untrusted code in sandboxed environments across multiple compute providers (E2B, Daytona, Vercel, Modal, Railway, Namespace, Render). Use this skill when implementing sandboxed code execution, creating isolated development environments, running LLM-generated code safely, building app builders, or integrating dynamic code execution into applications.
---

# ComputeSDK

A unified TypeScript SDK for running code in remote sandboxes. Write code once, switch providers by changing environment variables. Supports E2B, Modal, Railway, Daytona, Vercel, Namespace, Render, and more.

## Installation

```bash
npm install computesdk
```

Set your credentials:

```bash
COMPUTESDK_API_KEY=your_computesdk_api_key
E2B_API_KEY=your_e2b_api_key  # or any other provider's credentials
```

Get a ComputeSDK API key at https://console.computesdk.com/register

## Quick Start

```typescript
import { compute } from 'computesdk';

// Auto-detects provider from environment variables
const sandbox = await compute.sandbox.create();

const result = await sandbox.runCode('print("Hello World!")');
console.log(result.output); // "Hello World!"

await sandbox.destroy();
```

## Sandbox Lifecycle

```typescript
// Create with options
const sandbox = await compute.sandbox.create({
  runtime: 'python',
  timeout: 300000,
  metadata: { userId: '123' }
});

// Get existing sandbox by ID
const existing = await compute.sandbox.getById('sandbox-id');

// Find or create by name (idempotent)
const named = await compute.sandbox.findOrCreate({
  name: 'my-app',
  namespace: 'user-alice',
  timeout: 30 * 60 * 1000,
});

// Find without creating (returns null if not found)
const found = await compute.sandbox.find({
  name: 'my-app',
  namespace: 'user-alice',
});

// Extend timeout to prevent auto-shutdown
await compute.sandbox.extendTimeout(sandbox.sandboxId);

// Destroy
await sandbox.destroy();
// or: await compute.sandbox.destroy(sandbox.sandboxId);
```

## Code Execution

```typescript
// Auto-detect language (Python)
const result = await sandbox.runCode('print("Hello")');
// result.output, result.exitCode, result.language

// Explicit runtime: 'node' | 'python' | 'deno' | 'bun'
const nodeResult = await sandbox.runCode('console.log("Hi")', 'node');
```

## Command Execution

```typescript
// Simple command
const result = await sandbox.runCommand('ls -la');
// result.stdout, result.stderr, result.exitCode, result.durationMs

// With options
const result = await sandbox.runCommand('npm install', {
  cwd: '/app',
  env: { NODE_ENV: 'production' },
  timeout: 30000,
});

// Background command (returns immediately)
await sandbox.runCommand('npm run dev', { background: true });

// Shell operators work
await sandbox.runCommand('cd /app && npm install && npm test');
```

## Filesystem

```typescript
await sandbox.filesystem.writeFile('/app/index.js', 'console.log("hi")');
const content = await sandbox.filesystem.readFile('/app/index.js');
await sandbox.filesystem.mkdir('/app/data');
const files = await sandbox.filesystem.readdir('/app');
const exists = await sandbox.filesystem.exists('/app/index.js');
await sandbox.filesystem.remove('/app/index.js');

// Batch write (atomic, deduplicates)
await sandbox.file.batchWrite([
  { path: '/app/a.js', content: '...' },
  { path: '/app/b.js', content: '...' },
]);
```

## Managed Servers

Start supervised long-lived processes with install commands, restart policies, health checks, and public URLs.

```typescript
const server = await sandbox.server.start({
  slug: 'web',
  install: 'npm install',
  start: 'npm run dev',
  path: '/app',
  port: 3000,
  restart_policy: 'on-failure',  // 'never' | 'on-failure' | 'always'
  max_restarts: 5,
  health_check: {
    path: '/',
    interval_ms: 5000,
    timeout_ms: 3000,
  },
  environment: {
    NODE_ENV: 'development',
  },
});

// Status: installing -> starting -> running -> ready
console.log(server.status);
console.log(server.url);  // Public URL when ready

// Lifecycle
const servers = await sandbox.server.list();
const info = await sandbox.server.retrieve('web');
await sandbox.server.restart('web');
await sandbox.server.stop('web');
const logs = await sandbox.server.logs('web');
```

Create servers inline with sandbox creation:

```typescript
const sandbox = await compute.sandbox.create({
  servers: [{
    slug: 'dev',
    install: 'npm install',
    start: 'npm run dev',
    path: '/app',
    health_check: { path: '/' },
  }],
});
```

## Overlays (Template Mounting)

Bootstrap sandboxes from template directories instantly.

```typescript
const overlay = await sandbox.filesystem.overlay.create({
  source: '/templates/nextjs',
  target: './project',
  strategy: 'smart',  // symlinks node_modules, copies rest in background
  ignore: ['.git', '*.log'],
  waitForCompletion: true,
});

// Or wait separately
const overlay = await sandbox.filesystem.overlay.create({
  source: '/templates/react',
  target: './app',
});
await sandbox.filesystem.overlay.waitForCompletion(overlay.id);
```

Combine overlays with servers:

```typescript
const sandbox = await compute.sandbox.create({
  overlays: [{
    source: '/templates/nextjs',
    target: './project',
    strategy: 'smart',
  }],
  servers: [{
    slug: 'dev',
    install: 'npm install',
    start: 'npm run dev',
    path: './project',
    health_check: { path: '/' },
  }],
});
// Server automatically waits for overlay to complete
```

## Terminals

```typescript
// Interactive PTY terminal (WebSocket)
const terminal = await sandbox.terminal.create({ pty: true });
terminal.write('ls -la\n');
terminal.on('data', (data) => console.log(data));
terminal.resize({ cols: 120, rows: 40 });

// Structured exec terminal
const exec = await sandbox.terminal.create({ pty: false });
```

## Client Access (Browser Delegation)

Delegate sandbox access to browser clients without exposing API keys.

```typescript
// Server-side: create session token
const token = await sandbox.sessionToken.create({
  expiresIn: 3600,  // 1 hour
});

// Client-side: connect with token
import { Sandbox } from 'computesdk';
const clientSandbox = await Sandbox.connect({ url, token: token.token });

// Or use magic links (one-time auth URLs)
const link = await sandbox.magicLink.create({
  redirectUrl: 'https://myapp.com/editor',
});
```

## Provider Configuration

Auto-detection from environment variables is recommended. All providers also require `COMPUTESDK_API_KEY`.

| Provider | Environment Variables |
|----------|----------------------|
| E2B | `E2B_API_KEY` |
| Modal | `MODAL_TOKEN_ID`, `MODAL_TOKEN_SECRET` |
| Railway | `RAILWAY_API_KEY`, `RAILWAY_PROJECT_ID`, `RAILWAY_ENVIRONMENT_ID` |
| Daytona | `DAYTONA_API_KEY` |
| Vercel | `VERCEL_TOKEN`, `VERCEL_TEAM_ID`, `VERCEL_PROJECT_ID` |
| Namespace | `NSC_TOKEN` |
| Render | `RENDER_API_KEY`, `RENDER_OWNER_ID` |

Detection order: E2B -> Railway -> Daytona -> Modal -> Runloop -> Vercel -> Cloudflare -> CodeSandbox

For explicit configuration:

```typescript
compute.setConfig({
  computesdkApiKey: process.env.COMPUTESDK_API_KEY,
  provider: 'e2b',
  e2b: { apiKey: process.env.E2B_API_KEY }
});
```

Switch providers at runtime:

```typescript
// E2B for data science
compute.setConfig({
  computesdkApiKey: 'key',
  provider: 'e2b',
  e2b: { apiKey: process.env.E2B_API_KEY }
});
const e2bSandbox = await compute.sandbox.create();

// Modal for GPU workloads
compute.setConfig({
  computesdkApiKey: 'key',
  provider: 'modal',
  modal: {
    tokenId: process.env.MODAL_TOKEN_ID,
    tokenSecret: process.env.MODAL_TOKEN_SECRET
  }
});
const modalSandbox = await compute.sandbox.create();
```

## Multiple Compute Instances

```typescript
import { compute, createCompute } from 'computesdk';

// Singleton (recommended)
const sandbox = await compute.sandbox.create();

// Multiple independent instances
const compute1 = createCompute();
const compute2 = createCompute();
```

## Sandbox Info

```typescript
const info = await sandbox.getInfo();
// info.id, info.provider, info.runtime, info.status, info.createdAt, info.timeout
```

## TypeScript Types

```typescript
import type {
  Sandbox,
  SandboxInfo,
  CodeResult,
  CommandResult,
  CreateSandboxOptions
} from 'computesdk';
```

## Provider-Specific Skills

For provider-specific setup guides, install these skills:

```
npx skills add https://github.com/computesdk/sandbox-skills --skill e2b-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill vercel-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill daytona-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill modal-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill railway-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill namespace-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill render-sandbox
```

- `e2b-sandbox` — E2B Firecracker microVMs, sub-second cold starts
- `vercel-sandbox` — Globally distributed serverless execution
- `daytona-sandbox` — Full development workspace environments
- `modal-sandbox` — GPU-accelerated execution for ML workloads
- `railway-sandbox` — Self-hosted sandboxes on Railway infrastructure
- `namespace-sandbox` — Custom CPU/RAM allocation, architecture control
- `render-sandbox` — Self-hosted sandboxes with zero infrastructure setup

## References

- Documentation: https://www.computesdk.com/docs/
- GitHub: https://github.com/computesdk/computesdk
- LLM-optimized docs: https://www.computesdk.com/llms-full.txt
- API key: https://console.computesdk.com/register
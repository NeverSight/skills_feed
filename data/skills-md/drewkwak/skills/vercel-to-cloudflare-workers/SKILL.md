---
name: vercel-to-cloudflare-workers
description: >
  End-to-end migration guide from Vercel to Cloudflare Workers. Use when migrating any
  application (Next.js, React SPA, Astro, Remix, static sites, API routes) from Vercel
  hosting to Cloudflare Workers. Covers project assessment, wrangler configuration, OpenNext
  for Next.js, storage migration (KV, D1, R2, Hyperdrive), environment variables, DNS cutover,
  image optimization, Node.js compatibility, bundle size optimization, and troubleshooting
  common migration errors. Triggers on: migrate from Vercel, move to Cloudflare, Vercel to
  Workers, deploy Next.js on Cloudflare, replace Vercel with Cloudflare, or any
  Vercel-to-Cloudflare migration task.
---

# Vercel → Cloudflare Workers Migration

## Migration Decision Tree

1. Determine app type:
   - **Static site / SPA** (React, Vue, no SSR) → See [Static & SPA Migration](#static--spa-migration)
   - **Next.js with SSR/ISR/API routes** → See [Next.js Migration (OpenNext)](#nextjs-migration-opennext)
   - **Other SSR frameworks** (Astro, Remix, SvelteKit) → See [Other Frameworks](#other-ssr-frameworks)
   - **API-only (serverless functions)** → See [API Routes Migration](#api-routes-migration)

2. Identify storage dependencies → See `references/storage-migration.md`
3. Audit Node.js API usage → See `references/nodejs-compat.md`
4. Plan DNS cutover → See [DNS & Domain Cutover](#dns--domain-cutover)

## Critical Prerequisites

Before any migration work:

```jsonc
// wrangler.jsonc — minimum viable config
{
  "name": "my-app",
  "compatibility_date": "2025-04-01",  // CRITICAL: ≥2025-04-01 enables process.env auto-population
  "compatibility_flags": ["nodejs_compat"],
  "observability": { "logs": { "enabled": true } }
}
```

**Why these values matter:**
- `compatibility_date` ≥ `2024-09-23`: enables `nodejs_compat_v2` automatically (Buffer, AsyncLocalStorage, etc.)
- `compatibility_date` ≥ `2025-04-01`: enables `process.env` population as default (without this, all env vars are empty unless accessed via `env` parameter)
- `nodejs_compat` flag: reduces bundle bloat by using Cloudflare's built-in Node.js polyfills instead of bundling them
- `observability`: essential for debugging — without it, errors are invisible

**Environment variables — the #1 silent killer:**
- Vercel: `process.env.MY_VAR` works everywhere
- Workers: `process.env.MY_VAR` works ONLY with compatibility_date ≥ 2025-04-01
- Workers (older compat dates): must use the `env` parameter from fetch handler: `export default { async fetch(req, env, ctx) { env.MY_VAR } }`
- Local dev: use `.dev.vars` file (NOT `.env`)
- Secrets: `npx wrangler secret put SECRET_NAME`

## Static & SPA Migration

Simplest migration path. No server-side code involved.

1. Get build command and output directory from Vercel dashboard → Settings → Build & Development Settings
2. Create `wrangler.jsonc`:

```jsonc
{
  "name": "my-app",
  "compatibility_date": "2025-04-01",
  "assets": {
    "directory": "./dist",  // your build output directory
    "not_found_handling": "single-page-application"  // SPA client-side routing
    // Use "404-page" for static sites with custom 404
  }
}
```

3. Build and deploy: `npx wrangler deploy`
4. Connect GitHub repo via Cloudflare dashboard for CI/CD (Workers & Pages → Create → Connect to Git)

**Vercel config mappings:**
- `vercel.json` `rewrites` → handled by `not_found_handling: "single-page-application"`
- `vercel.json` `redirects` → implement in Worker code or use `_redirects` file
- `vercel.json` `headers` → implement in Worker code or use `_headers` file (no `.txt` extension)

## Next.js Migration (OpenNext)

OpenNext is the **only recommended path** for full Next.js apps on Cloudflare. It supports App Router, ISR, image optimization, and server-side features. Do NOT use `@cloudflare/next-on-pages` for new migrations (legacy, edge-runtime only).

### Step 1: Install dependencies

```bash
npm install @opennextjs/cloudflare@latest
npm install -D wrangler@latest
```

### Step 2: Add build scripts to package.json

```json
{
  "scripts": {
    "build": "next build",
    "build:worker": "opennextjs-cloudflare build",
    "preview": "opennextjs-cloudflare build && opennextjs-cloudflare preview",
    "deploy": "opennextjs-cloudflare build && opennextjs-cloudflare deploy",
    "cf-typegen": "wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts"
  }
}
```

### Step 3: Create open-next.config.ts

```ts
// open-next.config.ts
import type { OpenNextConfig } from "@opennextjs/cloudflare";

const config: OpenNextConfig = {
  default: {
    override: {
      wrapper: "cloudflare-node",
      converter: "edge",
      incrementalCache: "dummy",    // CRITICAL: without this, static pages aren't cached
      tagCache: "dummy",            // and Worker falls back to dynamic SSR for everything,
      queue: "dummy",               // causing cryptic 500 errors
    },
  },
};

export default config;
```

> ⚠ Add `open-next.config.ts` to your `tsconfig.json` → `exclude` array to avoid type conflicts.

### Step 4: Create wrangler.jsonc

```jsonc
{
  "name": "my-nextjs-app",
  "main": ".open-next/worker.js",
  "assets": { "directory": ".open-next/assets" },
  "compatibility_date": "2025-04-01",
  "compatibility_flags": ["nodejs_compat"],
  "observability": {
    "logs": {
      "enabled": true,
      "head_sampling_rate": 1,
      "invocation_logs": true
    }
  }
}
```

### Step 5: Handle common Next.js gotchas

Read `references/nextjs-gotchas.md` for the full list. Critical items:

- **Bundle size limit**: 3 MiB (free) / 10 MiB (paid) compressed. Analyze with `references/bundle-size.md` if exceeded.
- **next/image**: OpenNext supports image optimization. If using older adapter, see `references/nextjs-gotchas.md`.
- **Turbopack**: `next build --turbo` is NOT supported by OpenNext. Use `next build`.
- **Next.js 15/16 params**: `params` and `searchParams` are now Promises — must `await` them.
- **Database connections**: Cannot reuse across requests. See [I/O Isolation](#io-isolation-database-connections).

### Step 6: Deploy

```bash
npm run deploy
```

## Other SSR Frameworks

Astro, Remix, SvelteKit, and Nuxt all have official Cloudflare adapters:

- **Astro**: `@astrojs/cloudflare`
- **Remix**: `@remix-run/cloudflare`
- **SvelteKit**: `@sveltejs/adapter-cloudflare`
- **Nuxt**: `nitro` with `cloudflare` preset

Each uses the same `wrangler.jsonc` pattern from [Critical Prerequisites](#critical-prerequisites).

## API Routes Migration

For standalone API routes (no framework SSR), use Hono as an Express replacement:

```ts
import { Hono } from "hono";
const app = new Hono();

app.get("/api/users", async (c) => {
  // c.env gives you bindings (KV, D1, R2, etc.)
  const data = await c.env.DB.prepare("SELECT * FROM users").all();
  return c.json(data);
});

export default app;
```

**Key differences from Express:**
- No `require()` — ESM imports only
- No `app.listen()` — Workers handle routing
- `c.env` replaces `process.env` for bindings
- Use `c.executionCtx.waitUntil()` for background work (replaces fire-and-forget patterns)

## I/O Isolation (Database Connections)

**This is the most common runtime error after migration.**

Workers use V8 isolates — each request gets its own execution context. You CANNOT share I/O objects (DB connections, streams, response bodies) across requests.

```
❌ Error: Cannot perform I/O on behalf of a different request.
```

**Wrong** — global connection:
```ts
const client = postgres(process.env.DATABASE_URL); // shared across requests
export { client };
```

**Right** — per-request connection:
```ts
export function getDb() {
  return postgres(process.env.DATABASE_URL); // new connection each request
}
```

For connection pooling, use Cloudflare Hyperdrive. See `references/storage-migration.md`.

## DNS & Domain Cutover

Workers Custom Domains requires the domain as a **zone on your Cloudflare account** (nameserver delegation).

1. Add domain to Cloudflare as a zone (change nameservers at registrar)
2. Wait for nameserver propagation (minutes to 48 hours)
3. Deploy Worker and add custom domain via dashboard or wrangler
4. Verify Worker serves correctly on the new domain
5. Remove old Vercel DNS records (A, CNAME)
6. Delete Vercel project after confirming everything works

**Zero-downtime approach:** Deploy Worker on `*.workers.dev` subdomain first. Test thoroughly. Switch DNS only after full validation.

## Common Migration Errors

See `references/error-guide.md` for complete reference with code examples.

| Error | Cause | Fix |
|-------|-------|-----|
| `fs is not defined` | File system access | Use KV/R2 for storage |
| `Buffer is not defined` | Missing Node.js global | `import { Buffer } from "node:buffer"` |
| `process.env undefined` | Wrong env access | Set compat date ≥ 2025-04-01 or use `env` param |
| `setTimeout not returning` | Lambda async pattern | Use `ctx.waitUntil()` |
| `require() not found` | CommonJS module | Convert to ESM `import` |
| `Exceeded CPU time` | Long computation | Chunk work, use Durable Objects or Queues |
| `body already consumed` | Reading body twice | `req.clone()` before reading |
| `Cannot perform I/O` | Shared connection | Create DB client per-request |
| `FinalizationRegistry not defined` | Old compat date | Set compat date ≥ 2025-05-05 |
| `Worker exceeded size limit` | Bundle too large | See `references/bundle-size.md` |
| `Cannot find module` | Missing polyfill | Check Workers Node.js compat matrix |

## Reference Files

Load as needed — do NOT read all at once:

- **`references/storage-migration.md`** — Migrating Vercel KV/Postgres/Blob/Edge Config → Cloudflare KV/D1/R2/Hyperdrive
- **`references/nodejs-compat.md`** — Node.js API audit, module resolution, polyfill patterns
- **`references/error-guide.md`** — Detailed error reference with fix code for each common error
- **`references/nextjs-gotchas.md`** — Next.js-specific: image optimization, caching, middleware, ISR
- **`references/bundle-size.md`** — Diagnosing and fixing Worker bundle size limit issues

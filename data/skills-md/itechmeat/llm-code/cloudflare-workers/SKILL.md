---
name: cloudflare-workers
description: "Build serverless applications on Cloudflare Workers. Covers runtime APIs, handlers (fetch, scheduled, queue, email), bindings (KV, R2, D1, Durable Objects, Queues, AI, Vectorize), wrangler.toml configuration, local development with Miniflare, static assets, compatibility flags, testing with Vitest. Keywords: Cloudflare Workers, serverless, edge computing, Wrangler, fetch handler, scheduled handler, bindings, KV, R2, D1, Durable Objects, Workers AI, Miniflare, wrangler.toml, compatibility_date."
---

# Cloudflare Workers

Serverless platform for building applications across Cloudflare's global network.

## Quick Navigation

- Runtime & handlers → `references/runtime.md`
- Bindings overview → `references/bindings.md`
- Wrangler configuration → `references/wrangler.md`
- Local development → `references/local-dev.md`
- Static assets → `references/assets.md`
- Testing → `references/testing.md`

## When to Use

- Building serverless APIs or full-stack applications
- Running edge functions with global distribution
- Connecting to Cloudflare storage (KV, R2, D1, Durable Objects)
- Running AI inference with Workers AI
- Configuring Wrangler CLI and wrangler.toml
- Setting up local development with Miniflare
- Testing Workers with Vitest

## Module Worker (Recommended Syntax)

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return new Response("Hello, World!");
  },
} satisfies ExportedHandler<Env>;
```

## Handler Types

| Handler     | Trigger        | Use Case         |
| ----------- | -------------- | ---------------- |
| `fetch`     | HTTP request   | APIs, websites   |
| `scheduled` | Cron trigger   | Background jobs  |
| `queue`     | Queue message  | Async processing |
| `email`     | Email received | Email routing    |

## Bindings Overview

Access Cloudflare resources via `env` object.

| Binding           | Type                     | Local Dev      |
| ----------------- | ------------------------ | -------------- |
| KV                | `KVNamespace`            | ✅ Simulated   |
| R2                | `R2Bucket`               | ✅ Simulated   |
| D1                | `D1Database`             | ✅ Simulated   |
| Durable Objects   | `DurableObjectNamespace` | ✅ Simulated   |
| Queues            | `Queue`                  | ✅ Simulated   |
| Workers AI        | `Ai`                     | ❌ Remote only |
| Vectorize         | `VectorizeIndex`         | ❌ Remote only |
| Browser Rendering | `Fetcher`                | ❌ Remote only |
| Hyperdrive        | `Hyperdrive`             | ❌ Remote only |
| Static Assets     | `Fetcher`                | ✅ Simulated   |
| Service Binding   | `Fetcher`                | ✅ Simulated   |

## Minimal Configuration

```jsonc
// wrangler.jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "compatibility_flags": ["nodejs_compat"],
  "observability": {
    "enabled": true,
    "head_sampling_rate": 1
  }
}
```

## Essential Commands

```bash
# Development
npx wrangler dev              # Local dev (Miniflare)
npx wrangler dev --remote     # Remote dev (code on Cloudflare)

# Deployment
npx wrangler deploy           # Deploy to production
npx wrangler versions upload  # Upload without deploying
npx wrangler versions deploy  # Promote version

# Secrets
npx wrangler secret put KEY   # Add secret
npx wrangler secret list      # List secrets

# Types
npx wrangler types            # Generate TypeScript types
```

## Compatibility Settings

```toml
# wrangler.toml
compatibility_date = "2025-03-07"
compatibility_flags = ["nodejs_compat"]
```

Key flags:

- `nodejs_compat` — Enable Node.js APIs
- `nodejs_compat_v2` — Improved process implementation

## Quick Recipes

### Fetch Handler with Routing

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/api/hello") {
      return Response.json({ message: "Hello!" });
    }

    if (url.pathname.startsWith("/static/")) {
      return env.ASSETS.fetch(request);
    }

    return new Response("Not Found", { status: 404 });
  },
};
```

### Scheduled Handler (Cron)

```typescript
export default {
  async scheduled(controller: ScheduledController, env: Env, ctx: ExecutionContext) {
    ctx.waitUntil(doBackgroundWork(env));
  },
};
```

```toml
# wrangler.toml
[triggers]
crons = ["0 * * * *"]  # Every hour
```

### Queue Consumer

```typescript
export default {
  async queue(batch: MessageBatch, env: Env, ctx: ExecutionContext) {
    for (const message of batch.messages) {
      console.log(message.body);
      message.ack();
    }
  },
};
```

## Critical Prohibitions

- Do NOT store secrets in `wrangler.toml` — use `wrangler secret put`
- Do NOT use `remote: true` for Durable Objects or Workflows — unsupported
- Do NOT expect Workers AI to work locally — always requires remote connection
- Do NOT omit `compatibility_date` — defaults to oldest date (2021-11-02)
- Do NOT use Service Worker syntax for new projects — use ES Modules
- Do NOT mix Service Worker and Module syntax in same project

## Common Gotchas

| Issue                  | Solution                                                      |
| ---------------------- | ------------------------------------------------------------- |
| Local bindings empty   | Add `--local` flag to Wrangler KV/R2/D1 commands              |
| AI not working locally | Use `remote: true` in ai binding config                       |
| Node APIs unavailable  | Add `nodejs_compat` to compatibility_flags                    |
| First deploy fails     | Use `wrangler deploy`, not `versions upload` for first deploy |

## Related Skills

- `cloudflare-pages` — Full-stack hosting with Git deployment
- `cloudflare-d1` — D1 database operations
- `cloudflare-r2` — R2 object storage
- `cloudflare-kv` — KV namespace operations
- `cloudflare-durable-objects` — Stateful coordination

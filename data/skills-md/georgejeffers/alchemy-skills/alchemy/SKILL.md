---
name: alchemy
user-invocable: false
description: >-
  Alchemy IaC framework for TypeScript. Use when the user mentions Alchemy,
  wants to set up infrastructure, deploy Cloudflare Workers, configure
  databases, KV, R2, queues, use bindings and secrets, set up dev mode, use
  framework adapters (Vite, Astro, React Router, SvelteKit, Nuxt, TanStack
  Start), create custom resources, or work with any Alchemy provider.
metadata:
  tags: alchemy, infrastructure-as-code, typescript, cloudflare, workers, kv, r2, d1, queues, iac, deploy
---

# Alchemy

Alchemy is a TypeScript-native Infrastructure-as-Code framework. This skill provides comprehensive knowledge of Alchemy's APIs, patterns, and conventions.

**Load `references/alchemy-concepts.md`** for full details on any topic below.

## Quick Start

### New Project
```bash
alchemy create my-app --template vite
```

### Add to Existing Project
```bash
alchemy init
```

### Core File: `alchemy.run.ts`
```ts
import alchemy from "alchemy";
import { Worker, KVNamespace } from "alchemy/cloudflare";

const app = await alchemy("my-app");

const kv = await KVNamespace("cache", { title: "my-cache" });

const worker = await Worker("api", {
  entrypoint: "./src/worker.ts",
  bindings: {
    CACHE: kv,
    API_KEY: alchemy.secret(process.env.API_KEY),
    STAGE: app.stage,
  },
});

await app.finalize();
```

### Commands
```bash
alchemy deploy              # deploy (default stage = $USER)
alchemy deploy --stage prod # deploy to prod
alchemy dev                 # local dev with hot reload
alchemy destroy             # tear down all resources
```

## Task Routing

Based on what the user asks, determine which knowledge to load:

| User Request | What to Do |
|---|---|
| Set up Alchemy in a project | Use `alchemy create` or `alchemy init`, create `alchemy.run.ts` |
| Add a Worker | `import { Worker } from "alchemy/cloudflare"`, configure with entrypoint + bindings |
| Add a database/KV/R2/queue | Import from `alchemy/cloudflare`, create resource, bind to Worker |
| Use secrets | `alchemy.secret(process.env.X)` for input, `Secret.unwrap()` in custom resources |
| Set up dev mode | `alchemy dev`, configure framework adapter/plugin |
| Use a framework (Vite/Astro/etc.) | Load `references/alchemy-concepts.md` §11 for framework adapters |
| Deploy to production | `alchemy deploy --stage prod`, see CI guide patterns |
| Use Neon/Stripe/AWS/other provider | Load `references/alchemy-concepts.md` §13 for provider list |
| Build a custom resource | Load `references/resource-patterns.md` for implementation patterns |
| Build a new provider for Alchemy | Run the full Provider Development Workflow below |

## Key Concepts

### Resources
Resources are memoized async functions with create/update/delete lifecycle. Every resource takes an ID and props:
```ts
const db = await D1Database("my-db", { name: "my-db" });
```

### Bindings
Connect resources to Workers with type-safe bindings:
```ts
const worker = await Worker("api", {
  entrypoint: "./src/worker.ts",
  bindings: { DB: db, KV: kv, SECRET: alchemy.secret("value") },
});
```

Access in worker code with type inference:
```ts
import type { worker } from "../alchemy.run";
export default {
  async fetch(req: Request, env: typeof worker.Env) {
    await env.DB.prepare("SELECT 1").run();
  },
};
```

### Secrets
```ts
alchemy.secret(process.env.API_KEY)  // wrap a value
alchemy.secret.env.API_KEY           // shorthand
```

### Stages
Isolated copies of your infrastructure. Default is `$USER` locally:
```bash
alchemy deploy              # deploys to $USER stage
alchemy deploy --stage prod # deploys to prod stage
```

### Dev Mode
Local emulation with Miniflare, hot reload, framework integration:
```bash
alchemy dev
```

### Framework Adapters
Each framework has a resource and a Vite plugin/adapter:

| Framework | Resource | Plugin/Adapter |
|---|---|---|
| Vite | `Vite` | `alchemy/cloudflare/vite` |
| Astro | `Astro` | `alchemy/cloudflare/astro` |
| React Router | `ReactRouter` | `alchemy/cloudflare/react-router` |
| SvelteKit | `SvelteKit` | `alchemy/cloudflare/sveltekit` |
| Nuxt | `Nuxt` | `alchemy/cloudflare/nuxt` |
| TanStack Start | `TanStackStart` | `alchemy/cloudflare/tanstack-start` |
| BunSPA | `BunSPA` | (no plugin needed) |
| Next.js | `Nextjs` | `alchemy/cloudflare/nextjs` |
| Redwood (RWSDK) | `Redwood` | `alchemy/cloudflare/rwsdk` |

### Providers
Alchemy has 20+ providers. The main ones:

| Provider | Import | Key Resources |
|---|---|---|
| Cloudflare | `alchemy/cloudflare` | Worker, D1Database, KVNamespace, R2Bucket, Queue, DurableObjectNamespace, Hyperdrive, Zone, DnsRecords |
| Neon | `alchemy/neon` | NeonProject, NeonBranch, NeonDatabase, NeonRole |
| Stripe | `alchemy/stripe` | WebhookEndpoint, Price, Product, Coupon, and 10+ more |
| AWS | `alchemy/aws` | Function, Table, Vpc, Subnet, SecurityGroup, Bucket, Role |
| AWS Control | `alchemy/aws/control` | `AWS.{Service}.{Resource}` — covers full AWS CloudFormation |
| GitHub | `alchemy/github` | GitHubSecret |
| Vercel | `alchemy/vercel` | VercelProject, VercelDnsRecord, VercelDeployment |

## Conventions

- Default import: `import alchemy from "alchemy"`
- Named imports from subpaths: `import { Worker } from "alchemy/cloudflare"`
- `await app.finalize()` is always the last line of `alchemy.run.ts`
- Physical names include app name + stage for uniqueness
- Stage defaults to `$USER` locally; use `--stage prod` for production
- Sensitive values always wrapped with `alchemy.secret()`
- State stored in `.alchemy/` directory (add to `.gitignore` or commit for shared state)

## Reference Files

Load these on demand for detailed information:

- **`references/alchemy-concepts.md`** — Comprehensive reference covering all Alchemy concepts: apps, stages, scopes, phases, resources, secrets, state, bindings, CLI, dev mode, profiles, framework adapters, serialization, and all 20+ providers with their resources.
- **`references/resource-patterns.md`** — Implementation patterns for building custom resources (17 sections). Load when the user wants to create custom resources or contribute to Alchemy.
- **`references/test-patterns.md`** — Test conventions and patterns (15 sections). Load when writing tests for custom resources.
- **`references/doc-patterns.md`** — Documentation templates (10 sections). Load when writing docs for Alchemy providers.
- **`references/checklist.md`** — Completeness verification checklist. Load when verifying a provider implementation.

---

## Provider Development Workflow

Use this workflow when the user is **building a new provider or custom resource for the Alchemy framework itself** (not just using Alchemy in their app).

### Phase 1: Research
Study the provider's API, identify CRUD-capable entities, authentication method, rate limits.

### Phase 2: Design
Define resource list, Props/Output interfaces, API client approach, dependency order.

### Phase 3: API Client
Create `alchemy/src/{provider}/api.ts` — minimal fetch wrapper, env var auth with Secret.unwrap() fallback.

### Phase 4: Resources
Implement each resource. **Load `references/resource-patterns.md`.**
- `Resource("{provider}::{Resource}", ...)` with create/update/delete lifecycle
- Physical name: `props.name ?? this.output?.name ?? this.scope.createPhysicalName(id)`
- Must use `function` declaration (not arrow), context via `this`
- Export type guard (`is{Resource}`) for binding support

### Phase 5: Tests
Write tests. **Load `references/test-patterns.md`.**
- `alchemy.test(import.meta, { prefix: BRANCH_PREFIX })`
- try/finally with `destroy(scope)` and API verification

### Phase 6: Documentation
Write docs, guide, examples. **Load `references/doc-patterns.md`.**
- Resource docs: `alchemy-web/src/content/docs/providers/{provider}/{resource}.md`
- Guide: `alchemy-web/src/content/docs/guides/{provider}.mdx`
- Example: `examples/{provider}/alchemy.run.ts`

### Phase 7: Verify
Run checklist. **Load `references/checklist.md`.**
- `bun format`, `bun vitest alchemy/test/{provider}/`, `bun tsc -b`

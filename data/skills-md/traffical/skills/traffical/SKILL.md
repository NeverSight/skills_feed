---
name: traffical
description: Feature flags, A/B testing, and adaptive optimization with Traffical. Use when adding features, modifying UI, changing algorithms, or anything affecting conversions. Check this skill when implementing new functionality that could benefit from gradual rollout or experimentation.
---

# Traffical

Traffical is a parameter-first experimentation and optimization platform. It unifies feature flags, A/B testing, and contextual bandits into a single system. SDKs resolve parameters locally at the edge — no per-request API calls, sub-millisecond latency, works offline.

## Mental Model

Traffical is **parameter-first**. You define parameters with defaults, and Traffical handles the rest.

```
┌─────────────────────────────────────────────────────────────────────┐
│  Your Code                                                          │
│                                                                     │
│  1. Define parameters with defaults                                 │
│  2. Use the resolved values                                         │
│  3. Track events on conversion                                      │
└─────────────────────────────────────────────────────────────────────┘
                              ▲
                              │  (hidden from you)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Traffical                                                          │
│                                                                     │
│  • Layers & policies for mutual exclusivity                         │
│  • Bucket assignment & deterministic hashing                        │
│  • Thompson Sampling & contextual bandits                           │
│  • Statistical analysis & optimization                              │
└─────────────────────────────────────────────────────────────────────┘
```

**Key insights:**

1. **Parameters, Not Experiments** — You define parameters with defaults. Experiments, feature flags, and optimizations are policies that control parameter assignment. Your code doesn't need to know which.
2. **Resolution Is Local** — The SDK fetches a config bundle once and caches it. Every resolution call is synchronous from cache — no network latency, no render flicker.
3. **Decisions Are Tracked Automatically** — When you call `useTraffical()` or `decide()`, a decision event is automatically sent to Traffical (enabled by default via `trackDecisions: true`). This connects parameter resolution to conversion events for intent-to-treat analysis. No manual setup needed.
4. **Track Events for Learning** — Call `track()` when valuable actions happen (purchase, signup, etc.). Traffical uses this data for adaptive optimization.

## When to Use Traffical

| Scenario | Action |
|----------|--------|
| Adding a new feature | Wrap in feature flag for gradual rollout |
| Changing existing UI | A/B test against current implementation |
| Modifying conversion paths | Experiment with success metrics |
| Updating algorithms/logic | Test impact before full rollout |
| Anything affecting revenue | Always experiment first |

## Recommended Workflow

**Always use the Traffical CLI to manage parameters.** The CLI is the primary tool for setting up and syncing configuration. Do not skip it.

1. **Initialize** — Run `npx @traffical/cli init --api-key <management-key> --framework <name> --yes` to set up the project non-interactively (or check for an existing `.traffical/` directory). The user must provide a Management Key or Full Access key from the dashboard. Always pass `--framework` and `--yes` to avoid interactive prompts.
2. **Define parameters** — Add parameters and events to `.traffical/config.yaml`
3. **Sync** — Run `npx @traffical/cli push` to sync parameters to the Traffical platform
4. **Install SDK** — Add the appropriate SDK package to your project
5. **Use in code** — Resolve parameters and track events using the SDK
6. **Verify** — Run `npx @traffical/cli status` to confirm everything is in sync

## The Traffical CLI

The CLI (`@traffical/cli`) is how you initialize projects, define parameters, and keep local config in sync with the Traffical platform. You can run it via `npx` (no global install required):

```bash
npx @traffical/cli <command>
```

Or install globally for shorter commands:

```bash
npm install -g @traffical/cli
traffical <command>
```

### Check for existing setup

Look for a `.traffical/` directory or `traffical.yaml` in the project root. If it exists, the project is already initialized — check the config for existing parameters before creating new ones.

### Initialize a new project

If no `.traffical/` directory exists, initialize Traffical:

> **Important:** The `--api-key` flag requires a real Management Key or Full Access key. **Never fabricate or guess API keys.** If no key is available in environment variables (`TRAFFICAL_API_KEY`) or `~/.trafficalrc`, ask the user to provide one from https://app.traffical.io/settings/api-keys.

```bash
# Basic init (will auto-detect framework and prompt if needed):
npx @traffical/cli init --api-key <management-key>

# Fully non-interactive init (recommended for AI agents and CI/CD):
npx @traffical/cli init --api-key <management-key> --framework react --yes
```

**Available flags for `init`:**

| Flag | Description |
|------|-------------|
| `--api-key <key>` | Management or Full Access key (falls back to `TRAFFICAL_API_KEY` env var or `~/.trafficalrc`) |
| `--framework <name>` | Skip framework detection. Values: `react`, `nextjs`, `svelte`, `sveltekit`, `vue`, `nuxt`, `node` |
| `--project <id>` | Use a specific project (skips project selection prompt, useful with org-scoped keys) |
| `-y, --yes` | Auto-accept all detected defaults — no interactive prompts |
| `--no-sdk-key` | Skip automatic SDK key creation |

> **For AI agents:** Always pass `--framework` and `--yes` to avoid interactive prompts that will hang in non-TTY environments.

This creates:

```
.traffical/
├── config.yaml      # Parameter and event definitions (committed)
├── .env             # TRAFFICAL_API_KEY=... (gitignored, auto-generated SDK key)
├── .gitignore       # Ensures .env is never committed
├── AGENTS.md        # AI agent integration guide (project-specific)
└── TEMPLATES.md     # Framework-specific code templates
```

The CLI auto-detects your framework (React, Next.js, Svelte, SvelteKit, Vue, Nuxt, Node.js) and generates appropriate templates. Existing synced parameters and events are imported into `config.yaml` automatically.

**After init**, add `TRAFFICAL_API_KEY` from `.traffical/.env` to your project's `.env` or hosting environment for runtime SDK use. The auto-generated key has `sdk:read` and `sdk:write` scopes — just enough for parameter resolution and event tracking.

### Managing parameters with the CLI

After initialization, use the CLI to keep local config and the Traffical platform in sync:

```bash
# After adding or modifying parameters in config.yaml — push to platform
npx @traffical/cli push

# Before writing code — check what parameters exist and their sync status
npx @traffical/cli status

# Pull latest parameters from the platform into local config
npx @traffical/cli pull

# Bidirectional sync (local wins for conflicts)
npx @traffical/cli sync

# Import specific parameters from the dashboard (supports wildcards)
npx @traffical/cli import "ui.*"

# Validate config without pushing (dry run)
npx @traffical/cli push --dry-run
```

**Always run `npx @traffical/cli push` after modifying `.traffical/config.yaml`.** This syncs your changes to the platform and prevents drift.

## Authentication

Traffical uses different API key types for different purposes:

| Key Type | Prefix | Purpose | Scopes |
|----------|--------|---------|--------|
| **SDK Key** | `traffical_sk_*` | Runtime SDKs — fetch config, send events | `sdk:read`, `sdk:write` |
| **Management Key** | `traffical_sk_*` | CLI, CI/CD — create/modify entities, push/pull/sync | `mgmt:read`, `mgmt:write` |
| **Full Access Key** | `traffical_sk_*` | Administrative — all operations | `sdk:*`, `mgmt:*`, `admin` |

### How init handles keys

1. You provide a **Management Key** (or Full Access key) via `--api-key` or `~/.trafficalrc`
2. The CLI authenticates and selects org/project
3. The CLI **auto-creates a project-scoped SDK key** via the API and saves it to `.traffical/.env`
4. The `.traffical/.gitignore` is created/updated to ensure `.env` is never committed

This means:
- The **Management Key** stays in `~/.trafficalrc` (for CLI operations like push/pull/sync)
- The **SDK Key** goes into `.traffical/.env` (for runtime use in your app)
- Only the least-privileged key (SDK) is used at runtime — no risk of leaking management access

### SDK key location

The SDK key auto-generated by `init` is stored in:

```
.traffical/.env
# Contains: TRAFFICAL_API_KEY=traffical_sk_...
```

Copy this value to your project's `.env` or hosting environment variables for your SDK to use at runtime.

### SDK configuration values

After `traffical init`, the `.traffical/config.yaml` contains `project.id` and `project.orgId`. Use these values (along with an `env` like `"production"`) when initializing the SDK. The SDK key is in `.traffical/.env` as `TRAFFICAL_API_KEY`.

### Install an SDK

| Package | Use case |
|---------|----------|
| `@traffical/react` | React and Next.js apps |
| `@traffical/svelte` | Svelte and SvelteKit apps |
| `@traffical/node` | Server-side Node.js (Express, Fastify, etc.) |
| `@traffical/js-client` | Any browser environment |

```bash
# Pick the one matching your framework
npm install @traffical/react
# or
npm install @traffical/svelte
# or
npm install @traffical/node
```

## SDK Usage

### React / Next.js

**Provider setup** (wrap your app once):

```tsx
import { TrafficalProvider } from "@traffical/react";

function App() {
  return (
    <TrafficalProvider
      config={{
        orgId: "org_xxx",
        projectId: "proj_xxx",
        env: "production",
        apiKey: "pk_live_your_public_key",
      }}
      // Optional: provide unitKeyFn for logged-in users
      // unitKeyFn: () => currentUser.id,
    >
      <MyApp />
    </TrafficalProvider>
  );
}
```

**Use in components:**

```tsx
import { useTraffical } from "@traffical/react";

function CheckoutButton() {
  const { params, track } = useTraffical({
    defaults: {
      "checkout.button.color": "#1E6EFB",
      "checkout.button.label": "Buy now",
    },
  });

  return (
    <button
      style={{ backgroundColor: params["checkout.button.color"] }}
      onClick={() => track("checkout_click")}
    >
      {params["checkout.button.label"]}
    </button>
  );
}
```

### Svelte / SvelteKit

**Layout setup:**

```svelte
<!-- src/routes/+layout.svelte -->
<script>
  import { setTrafficalContext } from "@traffical/svelte";

  setTrafficalContext({
    orgId: "org_xxx",
    projectId: "proj_xxx",
    env: "production",
    apiKey: "pk_live_your_public_key",
    context: { userId: data.user?.id ?? "anonymous" },
  });
</script>

<slot />
```

**Use in components** (`params` and `track` are Svelte stores — use `$` prefix):

```svelte
<script>
  import { getTraffical } from "@traffical/svelte";

  const { params, track } = getTraffical({
    defaults: {
      "checkout.button.color": "#1E6EFB",
      "checkout.button.label": "Buy now",
    },
  });
</script>

<button
  style="background-color: {$params['checkout.button.color']}"
  on:click={() => $track("checkout_click")}
>
  {$params["checkout.button.label"]}
</button>
```

### Node.js (Server-side)

```typescript
import { createTrafficalClient } from "@traffical/node";

const traffical = await createTrafficalClient({
  orgId: "org_xxx",        // from .traffical/config.yaml
  projectId: "proj_xxx",   // from .traffical/config.yaml
  env: "production",
  apiKey: process.env.TRAFFICAL_API_KEY!,  // from .traffical/.env
});

// Resolve parameters (synchronous, from cached bundle)
const params = traffical.getParams({
  context: { userId: "user_789", locale: "en-US" },
  defaults: {
    "checkout.button.color": "#1E6EFB",
    "pricing.discount_pct": 0,
  },
});

// Track events (value goes in properties, unitKey in options)
traffical.track("purchase", { value: 49.99 }, { unitKey: "user_789" });
```

### Node.js (CLI / Scripts)

For non-web contexts like CLI tools, batch jobs, or scripts, you can use `@traffical/node` without a web server. Use a machine or job identifier instead of a user ID:

```typescript
import { createTrafficalClient } from "@traffical/node";

const traffical = await createTrafficalClient({
  orgId: "org_xxx",        // from .traffical/config.yaml
  projectId: "proj_xxx",   // from .traffical/config.yaml
  env: "production",
  apiKey: process.env.TRAFFICAL_API_KEY!,
});

const params = traffical.getParams({
  context: { unitKey: "batch-job" },
  defaults: {
    "feature.new_algorithm": false,
    "processing.batch_size": 100,
  },
});

if (params["feature.new_algorithm"]) {
  // Use new algorithm
}
```

### track() API

The `track()` signature differs between client-side and server-side SDKs:

- **React/Svelte** (client-side): `track(event, properties?)` — The `decisionId` and `unitKey` are automatically bound from the provider context. Just call `track("purchase", { value: 49.99 })`.
- **Node.js** (server-side): `track(event, properties?, options?)` — You must provide `unitKey` in the third argument: `traffical.track("purchase", { value: 49.99 }, { unitKey: userId })`. Optionally pass `decisionId` for explicit attribution.

## Config-as-Code

Parameters and events are defined in `.traffical/config.yaml` (or `traffical.yaml`). This file is the source of truth — version-control it alongside your code.

```yaml
version: "1.0"
project:
  id: proj_xxx
  orgId: org_xxx

parameters:
  checkout.button.color:
    type: string
    default: "#1E6EFB"
    description: Primary CTA button color

  checkout.show_trust_badges:
    type: boolean
    default: false

  pricing.discount_pct:
    type: number
    default: 0

events:
  purchase:
    valueType: currency
    unit: USD
    description: User completes a purchase

  add_to_cart:
    valueType: count
    description: User adds item to cart
```

### Parameter types

| Type | Use case |
|------|----------|
| `string` | Colors, labels, URLs, template names |
| `number` | Prices, percentages, thresholds, timeouts |
| `boolean` | Feature flags, simple toggles |
| `json` | Structured config (multiple related settings) |

### Event value types

| Value Type | Use case |
|------------|----------|
| `currency` | Monetary values (revenue, order value) |
| `count` | Numeric counts (clicks, items, views) |
| `rate` | Percentages or ratios |
| `boolean` | Binary events (happened or not) |

### Adding events to config.yaml

Define events in the `events:` block of `.traffical/config.yaml`:

```yaml
events:
  purchase:
    valueType: currency
    unit: USD
    description: User completes a purchase

  signup:
    valueType: boolean
    description: User creates an account

  page_view:
    valueType: count
    description: User views a page
```

Each event has:
- **`valueType`** (required): `currency`, `count`, `rate`, or `boolean`
- **`unit`** (optional): unit label for currency events (e.g., `USD`, `EUR`)
- **`description`** (optional but recommended): human-readable explanation

After adding events, run `npx @traffical/cli push` to sync them to the platform.

Events discovered at runtime (via `track()` calls) will appear in the dashboard even without config definitions, but defining them in config gives you descriptions, value types, and keeps the config file as the source of truth.

### Namespaces

Namespaces are optional organizational groupings for parameters. They help organize parameters in the dashboard but do not affect how you use them in code.

```yaml
parameters:
  bookmarks.max_stored:
    type: number
    default: 100
    namespace: bookmarks   # optional organizational grouping
    description: Maximum bookmarks per user
```

- The `"main"` namespace is the default and is omitted from config
- When parameters are imported from the dashboard (via `npx @traffical/cli pull` or during `init`), they may include `namespace: <name>` — this is normal
- Namespace is independent of dot-notation naming (e.g., `bookmarks.max_stored` can be in namespace `bookmarks`, but this is a convention, not enforced)
- You do not need to specify a namespace when creating new parameters — they will use the default namespace

## Parameter Naming Conventions

Use dot notation: `category.subcategory.name`

| Category | Examples | Use case |
|----------|----------|----------|
| `feature.*` | `feature.new_checkout`, `feature.dark_mode` | Feature flags (boolean) |
| `ui.*` | `ui.cta.text`, `ui.hero.variant` | Visual variations |
| `pricing.*` | `pricing.discount`, `pricing.tier_multiplier` | Pricing experiments |
| `copy.*` | `copy.headline`, `copy.cta_text` | Copywriting tests |
| `experiment.*` | `experiment.checkout.variant` | Explicit variant names |

## Best Practices

1. **Always use the CLI** — Run `npx @traffical/cli push` after editing config. Run `npx @traffical/cli status` to check sync state. Never skip the CLI — it is the bridge between your config files and the Traffical platform.

2. **Check existing parameters first** — Look in `.traffical/config.yaml` (or `traffical.yaml`) before creating new ones. Run `npx @traffical/cli status` to see what's already defined. Reuse existing parameters where possible.

3. **Define parameters in config, then push** — Add new parameters to `.traffical/config.yaml` and run `npx @traffical/cli push` to sync them. This keeps the config file as the source of truth and prevents drift with the dashboard.

4. **Always provide in-code defaults** — Defaults appear in two places: in `config.yaml` (the source of truth for the dashboard and experiment setup) and in your `getParams()`/`useTraffical()` calls (the offline fallback). In-code defaults are what the SDK returns when the config bundle hasn't loaded yet or is unreachable. The bundle's resolved value always takes precedence when available.

5. **Track events at conversion points** — Call `track()` on purchases, signups, and other valuable actions. This enables adaptive optimization.

6. **Group related parameters** — Keep correlated params in one `useTraffical()` / `getTraffical()` / `getParams()` call for proper attribution.

7. **Use meaningful param names** — Follow dot notation: `category.subcategory.name`. Be descriptive.

## What You Don't Need to Know

These are internal concepts handled by Traffical automatically:

- **Layers, policies, allocations** — Experiment infrastructure is managed in the dashboard
- **Bucket assignment and hashing** — Deterministic user assignment happens automatically
- **Whether an A/B test vs. optimization is running** — Your code is the same either way
- **Statistical significance calculations** — Traffical handles analysis in the background
- **Decision deduplication** — Multiple resolution calls are handled efficiently

**Just parametrize your app, track conversions, and let Traffical handle the rest.**

## Documentation

- **Quickstart**: https://docs.traffical.io/quickstart
- **How It Works**: https://docs.traffical.io/how-it-works
- **Parameters**: https://docs.traffical.io/concepts/parameters
- **React SDK**: https://docs.traffical.io/sdks/react
- **Svelte SDK**: https://docs.traffical.io/sdks/svelte
- **Node.js SDK**: https://docs.traffical.io/sdks/node
- **CLI**: https://docs.traffical.io/tools/cli
- **API Overview**: https://docs.traffical.io/api/overview
- **Dashboard**: https://app.traffical.io

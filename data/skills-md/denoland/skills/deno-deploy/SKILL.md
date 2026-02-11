---
name: deno-deploy
description: Use when deploying Deno apps to production, asking about Deno Deploy, or working with `deno deploy` CLI commands. Covers deployment workflows, environment variables, KV database access, custom domains, the --tunnel flag for local development, and the `deno deploy` command reference.
license: MIT
metadata:
  author: denoland
  version: "1.3"
---

# Deno Deploy

This skill provides guidance for deploying applications to Deno Deploy.

## Scope Boundaries

This skill applies **only** to Deno Deploy questions. Follow these rules:

- If the user asks about **AWS Lambda, Vercel, Netlify, Google Cloud Run, Docker, Kubernetes, or any other deployment platform**, answer using that platform directly. Do not mention Deno Deploy at all — not as an alternative, not as a comparison, not as a suggestion.
- If the user asks about **running a local Deno script** (not deploying), answer the local question directly. Do not mention Deno Deploy, deployment, or the `--tunnel` flag.
- Do not include `deno deploy` commands, Deno KV, or Deno Deploy environment variable configuration in responses about other platforms or local-only scripts.
- Only discuss Deno Deploy when the user explicitly asks about Deno Deploy or deploying a Deno application to production.

## Important: Use `deno deploy`, NOT `deployctl`

**Always use the `deno deploy` command.** Do NOT use `deployctl`.

- `deployctl` is for Deno Deploy Classic (deprecated)
- `deno deploy` is the modern, integrated command built into the Deno CLI
- **Requires Deno >= 2.4.2** - the `deno deploy` subcommand was introduced in Deno 2.4

## Deployment Workflow

**Always show the core deploy command first** — then explain diagnostic steps. When a user asks "how do I deploy?", lead with the actual command (`deno deploy --prod`) before covering pre-flight checks and configuration.

### Step 1: Locate the App Directory

Before running any deploy commands, find where the Deno app is located:

```bash
# Check if deno.json exists in current directory
if [ -f "deno.json" ] || [ -f "deno.jsonc" ]; then
  echo "APP_DIR: $(pwd)"
else
  # Look for deno.json in immediate subdirectories
  find . -maxdepth 2 -name "deno.json" -o -name "deno.jsonc" 2>/dev/null | head -5
fi
```

All deploy commands must run from the app directory.

### Step 2: Pre-Flight Checks

Check Deno version and existing configuration:

```bash
# Check Deno version (must be >= 2.4.2)
deno --version | head -1

# Check for existing deploy config
grep -E '"org"|"app"' deno.json deno.jsonc 2>/dev/null || echo "NO_DEPLOY_CONFIG"
```

### Step 3: Deploy Based on Configuration

**If `deploy.org` AND `deploy.app` exist in deno.json:**
```bash
# Build if needed (Fresh, Astro, etc.)
deno task build

# Deploy to production
deno deploy --prod
```

**If NO deploy config exists:**

**IMPORTANT: Ask the user first** - Do they have an existing app on Deno Deploy, or do they need to create a new one?

**If they have an existing app**, add the config directly to deno.json:
```json
{
  "deploy": {
    "org": "<ORG_NAME>",
    "app": "<APP_NAME>"
  }
}
```
The org name is in the Deno Deploy console URL (e.g., `console.deno.com/your-org-name`).

**If they need to create a new app:**

The CLI needs an organization name. Find it at https://console.deno.com - the org is in the URL path (e.g., `console.deno.com/your-org-name`).

Then create the app:
```bash
deno deploy create --org <ORG_NAME>
# A browser window opens - complete the app creation there
```

After completion, verify:
```bash
grep -E '"org"|"app"' deno.json
```

## Core Commands

### Production Deployment

```bash
deno deploy --prod
```

### Preview Deployment

```bash
deno deploy
```

Preview deployments create a unique URL for testing without affecting production.

### Targeting Specific Apps

```bash
deno deploy --org my-org --app my-app --prod
```

### Specifying an Entrypoint

```bash
deno deploy --entrypoint main.ts --prod
```

Or configure in `deno.json`:
```json
{
  "deploy": {
    "entrypoint": "main.ts"
  }
}
```

## Environment Variables

### Contexts

Deno Deploy has three "contexts" - logical environments where your code runs, each with its own set of variables:

| Context | Purpose |
|---------|---------|
| **Production** | Live traffic on your production URL |
| **Development** | Preview deployments and branch URLs |
| **Build** | Only available during the build process |

You can set different values for the same variable in each context. For example, you might use a test database URL in Development and the real one in Production.

### Predefined Variables

These are automatically available in your code:

| Variable | Description |
|----------|-------------|
| `DENO_DEPLOY` | Always `1` when running on Deno Deploy |
| `DENO_DEPLOYMENT_ID` | Unique ID for the current deployment |
| `DENO_DEPLOY_ORG_ID` | Your organization's ID |
| `DENO_DEPLOY_APP_ID` | Your application's ID |
| `CI` | Set to `1` during builds only |

### Accessing Variables in Code

```typescript
const dbUrl = Deno.env.get("DATABASE_URL");
const isDenoDeploy = Deno.env.get("DENO_DEPLOY") === "1";
```

### Managing Variables via CLI

```bash
# Add a variable
deno deploy env add DATABASE_URL "postgres://..."

# List variables
deno deploy env list

# Delete a variable
deno deploy env delete DATABASE_URL

# Load from .env file
deno deploy env load .env.production
```

### Variable Types

- **Plain text** - Visible in the dashboard, good for feature flags and non-sensitive config
- **Secrets** - Hidden after creation, only readable in your code, use for API keys and credentials

### Limits

- Key names: max 128 bytes
- Values: max 16 KB
- Keys cannot start with `DENO_`, `LD_`, or `OTEL_`

## Viewing Logs

```bash
# Stream live logs
deno deploy logs

# Filter by date range
deno deploy logs --start 2026-01-15 --end 2026-01-16
```

## Databases & Storage

Deno Deploy provides built-in database support with **automatic environment isolation**. Each environment (production, preview, branch) gets its own isolated database automatically.

### Available Options

| Engine | Use Case |
|--------|----------|
| **Deno KV** | Key-value storage, simple data, counters, sessions |
| **PostgreSQL** | Relational data, complex queries, existing Postgres apps |

### Deno KV Quick Start

No configuration needed - just use the built-in API:

```typescript
const kv = await Deno.openKv();

// Store data
await kv.set(["users", "alice"], { name: "Alice", role: "admin" });

// Retrieve data
const user = await kv.get(["users", "alice"]);
console.log(user.value); // { name: "Alice", role: "admin" }

// List by prefix
for await (const entry of kv.list({ prefix: ["users"] })) {
  console.log(entry.key, entry.value);
}
```

Deno Deploy automatically connects to the correct database based on your environment.

### PostgreSQL

For PostgreSQL, Deno Deploy injects environment variables (`DATABASE_URL`, `PGHOST`, etc.) that most libraries detect automatically:

```typescript
import postgres from "npm:postgres";
const sql = postgres(); // Reads DATABASE_URL automatically
```

### Provisioning

Use the `deno deploy database` command to provision and manage databases:

```bash
# Provision a Deno KV database
deno deploy database provision my-database --kind denokv

# Provision a Prisma PostgreSQL database
deno deploy database provision my-database --kind prisma --region us-east-1

# Assign to your app
deno deploy database assign my-database --app my-app
```

For detailed CLI commands, see [Databases](references/DATABASES.md).

### Local Development

Use `--tunnel` to connect to your hosted development database locally:

```bash
deno task --tunnel dev
```

See [Databases](references/DATABASES.md) and [Deno KV](references/DENO_KV.md) for detailed documentation.

## Local Development Tunnel

The tunnel feature lets you expose your local development server to the internet. This is useful for:

- **Testing webhooks** - Receive webhook callbacks from external services
- **Sharing with teammates** - Let others preview your local work
- **Mobile testing** - Access your local server from other devices

### Basic Usage

Add the `--tunnel` flag when running your app:

```bash
deno run --tunnel -A main.ts
```

The first time you run this, it will:
1. Ask you to authenticate with Deno Deploy (opens a browser)
2. Ask you to select which app to connect the tunnel to
3. Generate a public URL that forwards requests to your local server

### Using with Tasks

You can use `--tunnel` with your existing tasks in `deno.json`:

```bash
deno task --tunnel dev
```

This runs your `dev` task with the tunnel enabled.

### What the Tunnel Provides

Beyond just forwarding requests, the tunnel also:

- **Syncs environment variables** - Variables set in your Deno Deploy app's "Local" context become available to your local process
- **Sends logs and metrics** - OpenTelemetry data goes to the Deno Deploy dashboard (filter with `context:local`)
- **Connects to databases** - Automatically connects to your assigned local development databases

### Managing Tunnels

- View active tunnels in the Deno Deploy dashboard under the "Tunnels" tab
- Stop a tunnel by terminating the Deno process (Ctrl+C)

## Command Reference

| Command | Purpose |
|---------|---------|
| `deno deploy --prod` | Production deployment |
| `deno deploy` | Preview deployment |
| `deno deploy create --org <name>` | Create new app |
| `deno deploy env add <var> <value>` | Add environment variable |
| `deno deploy env list` | List environment variables |
| `deno deploy env delete <var>` | Delete environment variable |
| `deno deploy logs` | View deployment logs |
| `deno run --tunnel -A <file>` | Start local tunnel |
| `deno task --tunnel <task>` | Run task with tunnel |

## Edge Runtime Notes

Deno Deploy runs in one or many regions (globally distributed). Keep in mind:

- **Environment variables** - Must be set via `deno deploy env`, not .env files at runtime
- **Global distribution** - Code runs at the region closest to users
- **Cold starts** - First request after idle may be slightly slower

## Additional References

- [Authentication](references/AUTHENTICATION.md) - Interactive and CI/CD authentication
- [Databases](references/DATABASES.md) - Database provisioning and connections
- [Deno KV](references/DENO_KV.md) - Key-value storage API and examples
- [Domains](references/DOMAINS.md) - Custom domains and SSL certificates
- [Frameworks](references/FRAMEWORKS.md) - Framework-specific deployment guides
- [Organizations](references/ORGANIZATIONS.md) - Managing orgs and members
- [Runtime](references/RUNTIME.md) - Lifecycle, cold starts, and limitations
- [Troubleshooting](references/TROUBLESHOOTING.md) - Common issues and solutions

## Documentation

- Official docs: https://docs.deno.com/deploy/
- CLI reference: https://docs.deno.com/runtime/reference/cli/deploy/
- Databases: https://docs.deno.com/deploy/reference/databases/
- Deno KV: https://docs.deno.com/deploy/reference/deno_kv/
- Domains: https://docs.deno.com/deploy/reference/domains/
- Environment variables & contexts: https://docs.deno.com/deploy/reference/env_vars_and_contexts/
- Organizations: https://docs.deno.com/deploy/reference/organizations/
- Runtime: https://docs.deno.com/deploy/reference/runtime/
- Tunnel: https://docs.deno.com/deploy/reference/tunnel/

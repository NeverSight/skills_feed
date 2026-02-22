---
name: create-next-project
description: This skill should be used when the user asks to "create a new project", "scaffold a Next.js app", "initialize a new app", "start a new project", "set up a new Next.js project", or mentions "create-next-project". Provides a guided, opinionated full-stack Next.js project initialization with Biome, Tailwind v4, shadcn/ui, better-auth, and Vercel deployment. Uses agent teams for parallel execution.
version: 2.0.0
---

# Create Next.js Project

Guided full-stack Next.js project scaffolding. Six interactive steps that scaffold, configure, and deploy a production-ready app using agent teams for parallel execution.

## Core Stack (Always Included)

- **Next.js** (latest) with App Router, TypeScript, Tailwind v4, `src/` directory
- **Bun** as package manager and runtime
- **Biome** for linting and formatting (manually installed after scaffolding)
- **shadcn/ui** with dashboard-01 block as app shell
- **tweakcn** for theme customization (web editor at tweakcn.com)
- **next-themes** for light/dark mode
- **better-auth** for authentication
- **Vercel** for deployment

## Data Layer (depends on database choice)

- **Convex** selected: Use Convex's built-in `useQuery`/`useMutation` for all client data. NO TanStack Query needed.
- **All other databases**: Install TanStack Query for client-side data fetching.

---

## Step 0: Load Skills

BEFORE any work, invoke these skills to load guidance into context:

1. `Skill(vercel-react-best-practices)` - React/Next.js optimization rules
2. `Skill(vercel-composition-patterns)` - Component composition patterns
3. `Skill(better-auth-best-practices)` - Auth integration patterns

Apply their guidance throughout all steps.

---

## Step 1: Scaffold + Git + Repo

This step gets the bare project on disk and into version control.

### 1a. Scaffold

If the target directory already has files (e.g., a `.claude/` directory), move them to `/tmp` first, scaffold, then move them back.

```bash
bunx create-next-app@latest <project-name> \
  --typescript --tailwind --app --src-dir \
  --import-alias "@/*" --use-bun --turbopack --yes
cd <project-name>
```

### 1b. Replace ESLint with Biome

`create-next-app` does NOT have a `--biome` flag. It installs ESLint by default.

```bash
bun remove eslint eslint-config-next
rm -f eslint.config.mjs
bun add -d @biomejs/biome
```

Create `biome.json` -- see `references/stack-defaults.md` for the exact config. Key Biome 2.x rules:
- `organizeImports` goes under `assist.actions.source` (not the old top-level key)
- There is NO `files.ignore`. Use negation patterns in `files.includes` (e.g., `"!src/components/ui"`)
- Folder ignores do NOT use trailing `/**` (since Biome 2.2.0). Just `"!foldername"`
- `vcs.useIgnoreFile: true` respects `.gitignore` so `.next/` and `node_modules/` are auto-excluded
- `css.parser.tailwindDirectives: true` is required for Tailwind v4

Update `package.json` scripts:
```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "biome check .",
    "lint:fix": "biome check --write ."
  }
}
```

Auto-fix all files:
```bash
bunx biome check --write .
```

### 1c. Git init + verify

```bash
git init
bun run build
bun run lint
git add .
git commit -m "Initial Next.js scaffold with Biome"
```

### 1d. Ask about repo

Prompt the user with 3 options:

1. **Create new GitHub repo** -- list available orgs with `gh org list`, ask the user which one, then run `gh repo create <org>/<name> --private --source=. --remote=origin` (do NOT push yet). Never guess the org name from conversation -- always look it up.
2. **Use existing remote** -- ask for the remote URL, then `git remote add origin <url>` (do NOT push yet)
3. **Skip for now** -- continue without remote

**IMPORTANT: Do NOT push to GitHub yet.** Pushing triggers a Vercel deploy, and the deploy will fail if the database isn't provisioned. The first push happens in Step 6 after all infrastructure is set up.

---

## Step 2: Ask All Project Questions

Now that the scaffold exists, gather ALL requirements in one round. Use `AskUserQuestion` with multiple questions.

### Questions to ask:

1. **Auth methods** (multi-select):
   - Email/password (recommended default)
   - OAuth providers (Google, GitHub, Apple)
   - Sigma/Bitcoin auth (BSV-enabled apps)
   - Passkeys/WebAuthn

2. **Database**:
   - Convex (real-time, serverless) -- NOTE: replaces TanStack Query with Convex's own client
   - Turso/libSQL (edge SQLite)
   - PostgreSQL (traditional)
   - SQLite (local development)

3. **Optional packages** (multi-select):
   - `@ai-sdk/openai` + `ai` - AI/agent features
   - `@bsv/sdk` - BSV blockchain
   - `@1sat-lexi/js` - 1Sat Ordinals
   - `@1sat/connect` + `@1sat/react` - 1Sat wallet integration
   - `clawnet` - ClawNet agent platform
   - `resend` - Transactional email
   - None

4. **Theme**: "Pick a theme at tweakcn.com and paste the registry URL, or skip to use the default shadcn theme."

5. **Skills to reference in CLAUDE.md** (multi-select from installed plugins):
   - List available skills
   - Always include `vercel-react-best-practices` and `vercel-composition-patterns`

Record all answers -- they inform the research agents and build team.

---

## Step 3: Dispatch Research Agents

Send **parallel research agents** (using the Task tool with `run_in_background: true`) to gather context for each build workstream. Each agent reads relevant source code, docs, or skills so the build agents have everything they need.

### Agent assignments (run simultaneously):

**Research Agent 1: UI + Layout**
- Read `references/layout-architecture.md` and `references/stack-defaults.md`
- If user provided a tweakcn URL, note it for the build agent
- If the project has specific layout needs (e.g., Discord-like, dashboard), research the pattern

**Research Agent 2: Auth**
- Read `references/auth-setup.md`
- Invoke relevant auth skills based on user selections:
  - Sigma: `Skill(sigma-auth:setup-convex)` or `Skill(sigma-auth:setup-nextjs)`
  - Passkeys: read better-auth passkey docs
  - OAuth: note required env vars per provider
- If using Convex, research the `@convex-dev/better-auth` adapter pattern

**Research Agent 3: Data Layer**
- If Convex: invoke `Skill(convex-best-practices)`, read Convex schema patterns
- If Turso/PostgreSQL/SQLite: read `references/tanstack-query-setup.md`
- If the project has an existing data model or old project to port from, read those source files
- Identify all env vars the data layer needs

**Research Agent 4: Optional Packages** (only if user selected packages)
- Research configuration needs for each selected package
- Identify env vars, provider setup, and integration patterns

Wait for all research agents to complete before Step 4.

---

## Step 4: Dispatch Build Team

Create an agent team (using `TeamCreate`) with specialized agents. Provide each agent with FULL context from Step 2 answers and Step 3 research results.

### Team structure:

**Agent 1: UI + Layout + Theme** (Phases 2-3)
Responsibilities:
- `bunx shadcn@latest init --defaults`
- `bunx shadcn@latest add dashboard-01`
- Install tweakcn theme if URL provided
- `bun add next-themes`
- Set up ThemeProvider (see `references/stack-defaults.md`)
- Restructure into single-layout pattern (see `references/layout-architecture.md`)
- Delete `src/app/dashboard/` (dead route from dashboard-01 block)
- Create route group structure: `(app)/`, `(auth)/`
- Run `bun run build` and `bun run lint` to verify
- Commit: `"Add UI foundation and layout architecture"`

**Agent 2: Data Layer** (Phase 4)
Responsibilities depend on database choice:

*If Convex:*
- `bun add convex`
- `bunx convex init` (creates `convex/` directory)
- Create `convex/_generated/` stub files so build passes pre-deployment (see Convex Stubs section below)
- Create `convex/schema.ts` based on project needs
- Create query/mutation files
- NO TanStack Query -- Convex replaces it entirely
- Create `src/components/convex-provider.tsx`
- Run `bun run build` to verify
- Commit: `"Add Convex data layer"`

*If other databases:*
- Install TanStack Query: `bun add @tanstack/react-query`
- Optionally: `bun add -d @tanstack/react-query-devtools`
- Set up QueryProvider (see `references/tanstack-query-setup.md`)
- Install database adapter (Turso, pg, etc.)
- Run `bun run build` to verify
- Commit: `"Add data layer"`

**Agent 3: Auth** (Phase 5 -- depends on Agent 2 completing first if Convex)
Responsibilities:
- `bun add better-auth`
- If Convex: `bun add @convex-dev/better-auth` + create `convex/convex.config.ts`
- If Sigma: `bun add @sigma-auth/better-auth-plugin`
- `bunx shadcn@latest add login-05 signup-05`
- Configure server auth (`convex/auth.ts` or `src/lib/auth.ts`)
- Configure client auth (`src/lib/auth-client.ts`)
- Create API route handler (`src/app/api/auth/[...all]/route.ts`) -- use lazy initialization pattern for Convex
- Create callback page if using OAuth
- Create login/signup pages wired to auth client
- Set up middleware for protected routes
- Run `bun run build` to verify
- Commit: `"Add authentication"`

**Agent 4: Config + Optional Packages** (Phase 6-7)
Responsibilities:
- Install optional packages from user selections
- Create `.claude/CLAUDE.md` with project conventions, commands, selected skills
- Create `.env.vercel` with ALL env vars the project needs (see .env.vercel section below)
- Add `.gitignore` exception for `.env.vercel`
- Run `bun run build` and `bun run lint` final check
- Commit: `"Add project configuration and optional packages"`

### Agent coordination:
- Agent 1 (UI) and Agent 2 (Data) can run in parallel
- Agent 3 (Auth) must wait for Agent 2 to complete (needs data layer stubs/config)
- Agent 4 (Config) runs after all others complete (needs to know all env vars)

### What to tell each agent:
Every agent MUST receive:
1. The project path
2. The user's answers from Step 2
3. The relevant research results from Step 3
4. The specific reference file contents they need
5. The Biome 2.x rules (no non-null assertions, etc.)
6. Instruction to run `bun run build` and `bun run lint` before committing
7. Instruction to commit their work with a descriptive message

---

## Step 5: Provision Database via Vercel

After all agents complete and the build passes locally, provision the database BEFORE the first deploy. Deploying without a database creates broken deployments and can cause duplicate/disconnected database instances.

### 5a. User creates Vercel project (human-in-the-loop checkpoint)

**STOP and instruct the user to do this themselves.** The agent should NOT create the Vercel project. The user needs to:

> 1. Go to [vercel.com/new](https://vercel.com/new)
> 2. Select the correct team/org
> 3. Import the GitHub repo
> 4. Import the `.env.vercel` file (Settings > Environment Variables > Import .env) and fill in any empty values
> 5. **Do NOT deploy yet** -- add storage first (Step 5b)

Wait for the user to confirm they've done this before proceeding.

### 5b. User adds database via Vercel Storage (human-in-the-loop checkpoint)

**STOP and instruct the user to do this themselves.** The user needs to:

> Go to the Vercel project dashboard > **Storage** > **Add** > select your database

### 5c. Link local project to Vercel

After the user confirms the Vercel project exists and storage is added, link the local project. **Never guess the team slug** -- look it up:

```bash
bunx vercel teams list
```

Ask the user which team from the list, then link with the exact slug:

```bash
bunx vercel link --yes --scope <team-slug>
```

Confirm it linked to the correct project.

### 5d. Pull env vars

After linking, pull the env vars that Vercel and the storage integration set automatically:

```bash
vercel env pull
```

This creates `.env.local` with all env vars from the Vercel project. At this stage the expected state is:

- `CONVEX_DEPLOY_KEY` -- **present** (auto-set by the Convex Vercel integration)
- `NEXT_PUBLIC_CONVEX_URL` -- **missing** (this gets set after `bunx convex dev` connects the local project to the Convex deployment in Step 5e)
- All other env vars from `.env.vercel` -- present

This is normal. Do not treat the missing `NEXT_PUBLIC_CONVEX_URL` as an error.

### 5e. Complete database setup

#### Convex

**Always provision Convex through the Vercel Marketplace integration** (Step 5b). Never create a standalone Convex project separately -- the Vercel integration automatically connects deploy keys, handles preview deployments, and syncs env vars. Setting up Convex outside the marketplace when deploying to Vercel creates disconnected projects and manual sync headaches.

After Vercel Storage adds Convex, the dashboard shows a 4-step setup guide. Walk the user through it:

**Convex Step 1: Connect to the Convex CLI**

```bash
bunx convex login --vercel
```

This authenticates the CLI with the Vercel-managed Convex team.

**Convex Step 2: Link local project to Convex deployment**

We already have `convex/` with schema and functions. Skip `npm create convex@latest`. Run:

```bash
bunx convex dev
```

Follow the prompts to "Choose an existing project" and select the project from the Vercel-managed Convex team. This:
- Generates the real `convex/_generated/` files (replacing the stubs)
- Pushes your schema and functions to the **dev** deployment
- Writes `NEXT_PUBLIC_CONVEX_URL` to `.env.local`
- Starts watching for changes

**Keep `convex dev` running** in its own terminal during development. It continuously syncs your `convex/` code to the dev deployment.

**Convex Step 3: Connect Convex project to Vercel project**

This may already be done by the Vercel Storage integration. If not, in the Convex dashboard, connect to the Vercel project. This syncs `CONVEX_DEPLOY_KEY` to Vercel automatically.

**IMPORTANT**: Enable both "Production" and "Preview" environments. Keep the "Custom Prefix" field **empty**.

**Convex Step 4: Override the Vercel build command**

In Vercel project Settings > Build and Deployment, override the build command:

```
bunx convex deploy --cmd 'bun run build'
```

This is critical: `convex deploy` pushes functions/schema to the **production** Convex deployment, then runs `bun run build` which builds the Next.js frontend with `NEXT_PUBLIC_CONVEX_URL` pointing at production.

**Set Convex server-side env vars:**

Convex has its own environment variables separate from Vercel. These are set via the Convex CLI and are available inside Convex functions (actions, mutations, etc.).

**CRITICAL: `bunx convex env set` targets the DEV deployment by default, NOT production.** Always use `--prod` for production vars:

```bash
# Production (deployed app)
bunx convex env set SITE_URL "https://your-domain.com" --prod
bunx convex env set BETTER_AUTH_SECRET "$(openssl rand -hex 32)" --prod

# Dev (local development) -- same vars, different values
bunx convex env set SITE_URL "http://localhost:3000"
bunx convex env set BETTER_AUTH_SECRET "dev-secret-change-me"
```

Without `--prod`, you are ONLY setting vars on the dev deployment. Your production app will have missing env vars and fail silently or throw errors. This mismatch is a common source of hours-long debugging sessions.

**Commit the generated files:**

After `convex dev` runs, commit the real `convex/_generated/` files:

```bash
git add convex/_generated/
git commit -m "Add Convex generated files from dev deployment"
```

These should be checked in so teammates can type-check without running `convex dev`.

#### Turso

> Provision via Vercel Storage or CLI:
> ```bash
> turso db create <name>
> turso db show <name> --url     # TURSO_DATABASE_URL
> turso db tokens create <name>  # TURSO_AUTH_TOKEN
> ```
> Set both on Vercel.

#### PostgreSQL

> Add via Vercel Storage (Neon) or use an external provider (Supabase, Railway).
> Set `DATABASE_URL` on Vercel.

#### SQLite

> Local development only. No provisioning needed. Uses `./dev.db`.

---

## Step 6: First Deploy + Ongoing Workflow

### First deploy

Now that the database is provisioned and env vars are set, push to trigger the first deploy:

```bash
git push -u origin main
```

Or if the user hasn't set up a GitHub remote yet, list orgs with `gh org list`, ask the user which one, then:

```bash
gh repo create <org>/<name> --private --source=. --remote=origin --push
```

The Vercel deploy will:
1. Run `bunx convex deploy --cmd 'bun run build'` (per the build override)
2. `convex deploy` pushes functions/schema to the **production** Convex deployment
3. `convex deploy` sets `NEXT_PUBLIC_CONVEX_URL` to the production URL
4. `bun run build` builds the Next.js app pointing at production Convex
5. Vercel deploys the built frontend

### Ongoing development workflow

**Two terminals, always:**

```bash
# Terminal 1: Convex dev server (watches convex/ and pushes to DEV deployment)
bunx convex dev

# Terminal 2: Next.js dev server (uses NEXT_PUBLIC_CONVEX_URL from .env.local pointing at DEV)
bun dev
```

`convex dev` continuously:
- Pushes backend code changes to your dev deployment on every save
- Regenerates `convex/_generated/` types
- Enforces schema changes
- Shows function logs

Your local Next.js app (via `bun dev`) connects to the **dev** Convex deployment. The production app connects to the **production** deployment. They have separate data, separate env vars, and separate function code.

### Dev vs Production -- key differences

| | Dev deployment | Production deployment |
|---|---|---|
| **Connected by** | `bunx convex dev` | `bunx convex deploy` (Vercel build) |
| **URL in** | `.env.local` | Set automatically by `convex deploy` during build |
| **Env vars set with** | `bunx convex env set VAR val` | `bunx convex env set VAR val --prod` |
| **Data** | Separate (dev data) | Separate (production data) |
| **Schema pushed by** | `convex dev` (on save) | `convex deploy` (on Vercel build) |
| **When to use** | Local development | Deployed app |

### Verification

After first deploy completes:
- Visit the Vercel URL and confirm the app loads without client errors
- Check Convex dashboard to confirm schema was pushed to production
- Verify both dev and production deployments exist in the Convex dashboard
- Test auth flow if configured
- Confirm theme toggle works

---

## .env.vercel Pattern

Create a `.env.vercel` file committed to the repo with ALL env vars the project needs. Known defaults are pre-filled; unknowns are left empty. Add a `.gitignore` exception:

```gitignore
# env files
.env*
!.env.vercel
```

Example `.env.vercel`:
```bash
# Vercel Environment Variables
# Import this file into Vercel: Settings > Environment Variables > Import .env
# Values marked with comments must be filled in during setup

# Database (Convex example)
# IMPORTANT: NEXT_PUBLIC_CONVEX_URL = .convex.cloud (client SDK)
# IMPORTANT: NEXT_PUBLIC_CONVEX_SITE_URL = .convex.site (auth proxy destination)
# These are DIFFERENT URLs! Do NOT set SITE_URL to your app domain.
NEXT_PUBLIC_CONVEX_URL=
NEXT_PUBLIC_CONVEX_SITE_URL=
CONVEX_DEPLOY_KEY=

# Auth
BETTER_AUTH_SECRET=

# OAuth (if selected)
# GOOGLE_CLIENT_ID=
# GOOGLE_CLIENT_SECRET=

# Sigma Auth (if selected)
NEXT_PUBLIC_SIGMA_CLIENT_ID=your-app-name
NEXT_PUBLIC_SIGMA_AUTH_URL=https://auth.sigmaidentity.com
```

Only include env vars for features the user actually selected.

---

## Convex Stubs

When using Convex, the `convex/_generated/` directory does not exist until `bunx convex dev` runs. Create stub files so `bun run build` passes pre-deployment:

`convex/_generated/api.d.ts`:
```typescript
import type { AnyApi } from "convex/server";
declare const api: AnyApi;
declare const internal: AnyApi;
export { api, internal };
```

`convex/_generated/api.js`:
```javascript
import { anyApi } from "convex/server";
export const api = anyApi;
export const internal = anyApi;
```

`convex/_generated/server.d.ts`:
```typescript
export {
  action,
  httpAction,
  internalAction,
  internalMutation,
  internalQuery,
  mutation,
  query,
} from "convex/server";
```

`convex/_generated/server.js`:
```javascript
export {
  action,
  httpAction,
  internalAction,
  internalMutation,
  internalQuery,
  mutation,
  query,
} from "convex/server";
```

`convex/_generated/dataModel.d.ts`:
```typescript
import type { GenericDataModel } from "convex/server";
export type DataModel = GenericDataModel;
```

**Important**: If using `@convex-dev/better-auth` or other Convex components, the `api.d.ts` stub must also export `components`:

```typescript
import type { AnyApi } from "convex/server";
declare const api: AnyApi;
declare const internal: AnyApi;
declare const components: Record<string, AnyApi>;
export { api, internal, components };
```

```javascript
import { anyApi } from "convex/server";
export const api = anyApi;
export const internal = anyApi;
export const components = { betterAuth: anyApi };
```

These stubs get overwritten on first `bunx convex dev`.

---

## Convex Pitfalls

1. **Missing `_generated/` stubs** -- `bunx convex init` without a deployment does not create `convex/_generated/`. Create stub files (see above) so the build passes before first deployment.

2. **Missing `convex.config.ts`** -- required when using Convex components like `@convex-dev/better-auth`. Without it, the component is not registered and Convex fails at deploy time:
   ```typescript
   import betterAuth from "@convex-dev/better-auth/convex.config";
   import { defineApp } from "convex/server";
   const app = defineApp();
   app.use(betterAuth);
   export default app;
   ```

3. **Auth handler eager initialization** -- `convexBetterAuthNextJs()` throws at import time if env vars are missing. Use the lazy initialization pattern (see `references/auth-setup.md`).

4. **Circular type references in cron jobs** -- when `convex/crons.ts` references `internal.someModule.someAction`, and that module's return type depends on the `internal` type, TypeScript gets a circular reference. Fix by adding explicit return type annotations to action handlers referenced by crons.

5. **Env var mismatch: dev vs production** -- `bunx convex env set` targets the dev deployment by default. Always use `--prod` for production: `bunx convex env set VAR_NAME "value" --prod`.

6. **`NEXT_PUBLIC_CONVEX_SITE_URL` must be `.convex.site`, NOT the app domain** -- The auth proxy (`convexBetterAuthNextJs`) forwards `/api/auth/*` requests to this URL. If it points to your app domain (e.g., `https://myapp.com`), the proxy loops back to itself causing infinite redirects. Must be `https://<deployment>.convex.site`.

7. **`NEXT_PUBLIC_CONVEX_URL` must be set on Vercel** -- This env var (`https://<deployment>.convex.cloud`) is NOT auto-set by the Convex Vercel integration. You must add it manually to Vercel env vars, or pull it after `vercel env pull`. Without it, the production app has no Convex connection.

8. **Convex functions not deployed to production** -- `bunx convex dev` only pushes to the dev deployment. For production, run `bunx convex deploy --yes`. Without this, your production Convex deployment has no functions, queries, or HTTP actions.

9. **Sigma `SIGMA_MEMBER_PRIVATE_KEY` must be on Convex prod** -- This WIF key is required for server-side OAuth token exchange. Without it on production (`bunx convex env set SIGMA_MEMBER_PRIVATE_KEY "..." --prod`), sign-in silently fails.

---

## Key Principles

- **Bun everywhere** -- never npm, npx, or yarn. Use `bun`, `bunx` for everything
- **Manual Biome setup** -- `create-next-app` does NOT have a `--biome` flag. Remove ESLint, install Biome, create `biome.json` manually
- **Biome 2.x config** -- `assist.actions.source.organizeImports`, negation patterns in `files.includes` (no `files.ignore`), `css.parser.tailwindDirectives: true`
- **No non-null assertions** -- Biome flags `process.env.FOO!`. Always validate env vars and throw informatively:
  ```typescript
  // WRONG
  const url = process.env.DATABASE_URL!;
  // RIGHT
  const url = process.env.DATABASE_URL;
  if (!url) throw new Error("DATABASE_URL environment variable is required");
  ```
- **Lazy handler initialization** -- auth route handlers that depend on env vars must defer to request time, not module evaluation time
- **Explicit return types on cron actions** -- avoids circular type references
- **Convex replaces TanStack Query** -- when using Convex, use `useQuery`/`useMutation` from `convex/react`. Do NOT install TanStack Query.
- **CLIs first** -- use `create-next-app`, `shadcn`, `biome`, `vercel`, `gh` CLIs
- **Latest versions** -- always `@latest` for all installations
- **Build verification** -- run `bun run build` at every commit checkpoint
- **No push before database** -- NEVER push to GitHub before the database is provisioned via Vercel Storage. Pushing triggers a Vercel deploy that will fail without a connected database, creating broken deployments and potentially duplicate disconnected database instances
- **Agent teams** -- in Claude Code, use `TeamCreate` to parallelize Phases 2-7. Provide each agent thorough context since they lack conversation history.

## Reference Files

- **`references/stack-defaults.md`** -- Exact configs for Biome, theme provider, Tailwind, shadcn
- **`references/layout-architecture.md`** -- Single-layout pattern with navbar and route-based content
- **`references/auth-setup.md`** -- better-auth setup per provider (email, OAuth, Sigma, passkeys)
- **`references/tanstack-query-setup.md`** -- Provider setup, custom hooks (for non-Convex projects only)

## Related Skills

- **`vercel-react-best-practices`** -- React/Next.js optimization rules
- **`vercel-composition-patterns`** -- Component composition for scalable apps
- **`frontend-design`** -- UI design avoiding generic aesthetics
- **`better-auth-best-practices`** -- Auth integration patterns
- **`convex-best-practices`** -- Convex patterns (when using Convex)
- **`sigma-auth:setup-convex`** -- Sigma auth with Convex
- **`sigma-auth:setup-nextjs`** -- Sigma auth with Next.js (non-Convex)

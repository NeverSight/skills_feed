---
name: solo-deploy
description: Deploy project to hosting platform — read stack YAML for exact config, detect local CLI tools (vercel, wrangler, supabase, fly, sst), set up database, push code, verify live deployment. Use when user says "deploy it", "push to production", "set up hosting", or after /build completes. Do NOT use before build is complete.
license: MIT
metadata:
  author: fortunto2
  version: "1.2.1"
  openclaw:
    emoji: "🚀"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, mcp__solograph__session_search, mcp__solograph__project_code_search, mcp__solograph__codegraph_query
argument-hint: "[platform]"
---

# /deploy

Deploy the project to its hosting platform. Reads the stack template YAML (`templates/stacks/{stack}.yaml`) for exact deploy config (platform, CLI tools, infra tier, CI/CD, monitoring), detects installed CLI tools, sets up database and environment, pushes code, and verifies deployment is live.

## References

- `templates/principles/dev-principles.md` — CI/CD, secrets, DNS, shared infra rules
- `templates/stacks/*.yaml` — Stack templates with deploy, infra, ci_cd, monitoring fields

> Paths are relative to the skill's plugin root. Search for these files via Glob if not found at expected location.

## When to use

After `/build` has completed all tasks (build stage is complete). This is the deployment engine.

Pipeline: `/build` → **`/deploy`** → `/review`

## MCP Tools (use if available)

- `session_search(query)` — find how similar projects were deployed before
- `project_code_search(query, project)` — find deployment patterns across projects
- `codegraph_query(query)` — check project dependencies and stack

If MCP tools are not available, fall back to Glob + Grep + Read.

## Pre-flight Checks

### 1. Verify build is complete (optional)
- If pipeline state tracking exists (`.solo/states/` directory), check `.solo/states/build`.
- If `.solo/states/` exists but `build` marker is missing: warn "Build may not be complete. Consider running `/build` first."
- If `.solo/states/` does not exist: skip this check and proceed with deployment.

### 2. Detect available CLI tools

Run in parallel — detect what's installed locally:
```bash
vercel --version 2>/dev/null && echo "VERCEL_CLI=yes" || echo "VERCEL_CLI=no"
wrangler --version 2>/dev/null && echo "WRANGLER_CLI=yes" || echo "WRANGLER_CLI=no"
npx supabase --version 2>/dev/null && echo "SUPABASE_CLI=yes" || echo "SUPABASE_CLI=no"
fly version 2>/dev/null && echo "FLY_CLI=yes" || echo "FLY_CLI=no"
sst version 2>/dev/null && echo "SST_CLI=yes" || echo "SST_CLI=no"
gh --version 2>/dev/null && echo "GH_CLI=yes" || echo "GH_CLI=no"
```

Record which tools are available. Use them directly when found — do NOT `npx` if CLI is already installed globally.

### 3. Load project context (parallel reads)
- `CLAUDE.md` — stack name, architecture, deploy platform
- `docs/prd.md` — product requirements, deployment notes
- `docs/workflow.md` — CI/CD policy (if exists)
- `package.json` or `pyproject.toml` — dependencies, scripts
- `fly.toml`, `wrangler.toml`, `sst.config.ts` — platform configs (if exist)
- `docs/plan/*/plan.md` — **active plan** (look for deploy-related phases/tasks)

**Plan-driven deploy:** If the active plan contains deploy phases or tasks (e.g. "deploy Python backend to VPS", "run deploy.sh", "set up Docker on server"), treat those as **primary deploy instructions**. The plan knows the project-specific deploy targets that the generic stack YAML may not cover. Execute plan deploy tasks in addition to (or instead of) the standard platform deploy below.

### 4. Read stack template YAML

Extract the **stack name** from `CLAUDE.md` (look for `stack:` field or tech stack section).

Read the stack template to get exact deploy configuration:

**Search order** (first found wins):
1. `templates/stacks/{stack}.yaml` — relative to this skill's plugin root
2. `.solo/stacks/{stack}.yaml` — user's local overrides (from `/init`)
3. Search via Glob for `**/stacks/{stack}.yaml` in project or parent directories

Extract these fields from the YAML:
- `deploy` — target platform(s): `vercel`, `cloudflare_workers`, `cloudflare_pages`, `fly.io`, `docker`, `app_store`, `play_store`, `local`
- `deploy_cli` — CLI tools and their use cases (e.g. `vercel (local preview, env vars, promote)`)
- `infra` — infrastructure tool and tier (e.g. `sst (sst.config.ts) — Tier 1`)
- `ci_cd` — CI/CD system (e.g. `github_actions`)
- `monitoring` — monitoring/analytics (e.g. `posthog`)
- `database` / `orm` — database and ORM if any (affects migration step)
- `storage` — storage services if any (R2, D1, KV, etc.)
- `notes` — stack-specific deployment notes

**Use the YAML values as the source of truth** for all deploy decisions below. The YAML overrides the fallback tier matrix.

### 5. Detect platform (fallback if no YAML)

If stack YAML was not found, use this fallback matrix:

| Stack | Platform | Tier |
|-------|----------|------|
| `nextjs-supabase` / `nextjs-ai-agents` | Vercel + Supabase | Tier 1 |
| `cloudflare-workers` | Cloudflare Workers (wrangler) | Tier 1 |
| `astro-static` / `astro-hybrid` | Cloudflare Pages (wrangler) | Tier 1 |
| `python-api` | Fly.io (quick) or Pulumi + Hetzner (production) | Tier 2/4 |
| `python-ml` | skip (CLI tool, no hosting needed) | — |
| `ios-swift` | skip (App Store is manual) | — |
| `kotlin-android` | skip (Play Store is manual) | — |

If `$ARGUMENTS` specifies a platform, use that instead of auto-detection or YAML.

**Auto-deploy platforms** (from YAML `deploy` field or fallback):
- `vercel` / `cloudflare_pages` — auto-deploy on push. Push to GitHub is sufficient if project is already linked. Only run manual deploy for initial setup.
- `cloudflare_workers` — `wrangler deploy` needed (no git-based auto-deploy for Workers).
- `fly.io` — `fly deploy` needed.

## Deployment Steps

### Step 1. Git — Clean State + Push

```bash
git status
git log --oneline -5
```

If dirty, commit remaining changes:
```bash
git add -A
git commit -m "chore: pre-deploy cleanup"
```

Ensure remote exists and push:
```bash
git remote -v
git push origin main
```

If no remote, create GitHub repo:
```bash
gh repo create {project-name} --private --source=. --push
```

**For platforms with auto-deploy (Vercel, CF Pages):** pushing to main triggers deployment automatically. Skip manual deploy commands if project is already linked.

### Step 2. Database Setup

**Supabase** (if `supabase/` dir or Supabase deps detected):
```bash
# If supabase CLI available:
supabase db push          # apply migrations
supabase gen types --lang=typescript --local > db/types.ts  # optional: regenerate types
```
If no CLI: guide user to Supabase dashboard for migration.

**Drizzle ORM** (if `drizzle.config.ts` exists):
```bash
npx drizzle-kit push      # push schema to database
npx drizzle-kit generate  # generate migration files (if needed)
```

**D1 (Cloudflare)** (if `wrangler.toml` has D1 bindings):
```bash
wrangler d1 migrations apply {db-name}
```

If database is not configured yet, list what's needed and continue — don't block on it.

### Step 3. Environment Variables

Read `.env.example` or `.env.local.example` to identify required variables.

Generate platform-specific instructions:

**Vercel:**
```bash
# If vercel CLI is available and project is linked:
vercel env ls  # show current env vars

# Guide user:
echo "Set env vars: vercel env add VARIABLE_NAME"
echo "Or via dashboard: https://vercel.com/[team]/[project]/settings/environment-variables"
```

**Cloudflare:**
```bash
wrangler secret put VARIABLE_NAME  # interactive prompt for value
# Or in wrangler.toml [vars] section for non-secret values
```

**Fly.io:**
```bash
fly secrets set VARIABLE_NAME=value
fly secrets list
```

**Do NOT create or modify `.env` files with real secrets.**
List what's needed, let user set values.

### Step 4. Platform Deploy

**Vercel** (if not auto-deploying):
```bash
vercel link          # first time: link to project
vercel               # deploy preview
vercel --prod        # deploy production (after verifying preview)
```

**Cloudflare Workers/Pages:**
```bash
wrangler deploy              # Workers
wrangler pages deploy ./out  # Pages (check build output dir)
```

**Fly.io:**
```bash
fly launch   # first time — creates app, sets region
fly deploy   # subsequent deploys
```

**SST** (if sst.config.ts exists):
```bash
sst deploy --stage prod    # production
sst deploy --stage dev     # staging
```

### Step 5. Verify Deployment

After deployment, verify it actually works:

```bash
# 1. HTTP status check
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://{deployment-url})

# 2. Check for runtime errors in page body
BODY=$(curl -s https://{deployment-url} | head -200)

# 3. Check Vercel deployment logs for errors
vercel logs --output=short 2>&1 | tail -30
```

**If HTTP status is not 200, or page contains error messages:**
1. Check `vercel env ls` — are all required env vars set on the platform?
2. If env vars missing: add them with `vercel env add NAME production <<< "value"`
3. If env vars set but wrong: `vercel env rm NAME production` then re-add
4. After fixing env vars: redeploy with `vercel --prod --yes`
5. Re-check HTTP status and page content

**Common runtime errors and fixes:**
- "Supabase URL/Key required" → add `NEXT_PUBLIC_SUPABASE_URL` + `NEXT_PUBLIC_SUPABASE_ANON_KEY` to Vercel
- "DATABASE_URL not set" → add `DATABASE_URL` to Vercel
- "STRIPE_SECRET_KEY missing" → add Stripe keys or remove Stripe code if not ready
- Blank page / hydration error → check build logs, may need `vercel --prod` redeploy

**Do NOT output `<solo:done/>` until the live URL returns HTTP 200 and page loads without errors.** If you cannot fix the issue, output `<solo:redo/>` to go back to build. Output pipeline signals ONLY if `.solo/states/` directory exists.

### Step 6. Post-Deploy Log Monitoring

After verifying HTTP 200, **tail production logs** to catch runtime errors that only appear under real conditions (missing env vars, DB connection issues, SSR crashes, API timeouts).

Read the `logs` field from the stack YAML to get platform-specific commands:

**Vercel (Next.js):**
```bash
vercel logs --output=short 2>&1 | tail -50
```
Look for: `Error`, `FUNCTION_INVOCATION_FAILED`, `EDGE_FUNCTION_INVOCATION_FAILED`, `504 GATEWAY_TIMEOUT`, unhandled rejections.

**Cloudflare Workers:**
```bash
wrangler tail --format=pretty 2>&1 | head -100
```
Look for: `Error`, uncaught exceptions, D1 query failures, R2 access errors.

**Cloudflare Pages (Astro):**
```bash
wrangler pages deployment tail --project-name={name} 2>&1 | head -100
```

**Fly.io (Python API):**
```bash
fly logs --app {name} 2>&1 | tail -50
fly status --app {name}
```
Look for: `ERROR`, `CRITICAL`, unhealthy instances, OOM kills, connection refused.

**Supabase Edge Functions (if used):**
```bash
supabase functions logs --scroll 2>&1 | tail -30
```

**What to do with log errors:**
- **Env var missing** → fix with platform CLI (see Step 3), redeploy
- **DB connection error** → check connection string, IP allowlist
- **Runtime crash / unhandled error** → if `.solo/states/` exists, output `<solo:redo/>` to go back to build with fix; otherwise fix and redeploy
- **No errors in 30 lines of logs** → proceed to report

**If logs show zero traffic (fresh deploy), make a few test requests:**
```bash
curl -s https://{deployment-url}/           # homepage
curl -s https://{deployment-url}/api/health  # API health (if exists)
```
Then re-check logs for any errors triggered by these requests.

### Step 7. Post-Deploy Report

```
Deployment: {project-name}

  Platform:  {platform}
  URL:       {deployment-url}
  Branch:    main
  Commit:    {sha}

  Done:
    - [x] Code pushed to GitHub
    - [x] Deployed to {platform}
    - [x] Database migrations applied (or N/A)

  Manual steps remaining:
    - [ ] Set environment variables (listed above)
    - [ ] Custom domain (optional)
    - [ ] PostHog / analytics setup (optional)

  Next: /review — final quality gate
```

## Completion

### Signal completion

If `.solo/states/` directory exists, output this exact tag ONCE and ONLY ONCE — the pipeline detects the first occurrence:
```
<solo:done/>
```
**Do NOT repeat the signal tag anywhere else in the response.** One occurrence only.
If `.solo/states/` directory does not exist, skip the signal tag.

## Error Handling

### CLI not found
**Cause:** Platform CLI not installed.
**Fix:** Install the specific CLI: `npm i -g vercel`, `npm i -g wrangler`, `brew install flyctl`, `brew install supabase/tap/supabase`.

### Deploy fails — build error
**Cause:** Build works locally but fails on platform (different Node version, missing env vars).
**Fix:** Check platform build logs. Ensure `engines` in package.json matches platform. Set missing env vars.

### Database connection fails
**Cause:** DATABASE_URL not set or network rules block connection.
**Fix:** Check connection string, platform's DB dashboard, IP allowlist.

### Git push rejected
**Cause:** Remote has diverged.
**Fix:** `git pull --rebase origin main`, resolve conflicts, push again.

## Verification Gate

Before reporting "deployment successful":
1. **Run** `curl -s -o /dev/null -w "%{http_code}"` against the deployment URL.
2. **Verify** HTTP 200 (not 404, 500, or redirect loop).
3. **Check** the actual page content matches expectations (not a blank page or error).
4. **Only then** report the deployment as successful.

Never say "deployment should be live" — verify it IS live.

## Critical Rules

1. **Use installed CLIs** — detect `vercel`, `wrangler`, `supabase`, `fly`, `sst` before falling back to `npx`.
2. **Auto-deploy aware** — if platform auto-deploys on push, just push. Don't run manual deploy commands unnecessarily.
3. **NEVER commit secrets** — no .env files with real values, no API keys in code.
4. **Preview before production** — deploy preview first, verify, then promote to prod.
5. **Check build locally first** — `pnpm build` / `uv build` (or equivalent) before deploying.
6. **Check production logs** — always tail logs after deploy, catch runtime errors before declaring success.
7. **Report all URLs** — deployment URL + platform dashboard links.
8. **Infrastructure in repo** — prefer `sst.config.ts` or `fly.toml` over manual dashboard config.
9. **Verify before claiming done** — HTTP 200 from the live URL + clean logs, not just "deploy command succeeded".

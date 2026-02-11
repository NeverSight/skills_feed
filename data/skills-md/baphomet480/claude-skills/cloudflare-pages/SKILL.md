---
name: cloudflare-pages
description: Deploy static sites to Cloudflare Pages with custom domains and CI/CD. Use when the user wants to deploy a site to Cloudflare Pages, add a custom domain to a Pages project, set up GitHub Actions CI/CD for Cloudflare Pages, roll back a deployment, or verify deployment status. Triggers on "deploy to Cloudflare", "Cloudflare Pages", "add custom domain", "pages deploy", or any Cloudflare Pages hosting workflow.
---

# Cloudflare Pages

Deploy any static site to Cloudflare Pages — create projects, attach custom domains, wire up CI/CD, and verify deployments. Framework-agnostic: works with Hugo, Astro, Next.js, Nuxt, SvelteKit, or any build tool that produces static output.

## Prerequisites

| Requirement | How to get it |
|---|---|
| **wrangler CLI** | `npm i -g wrangler` then `wrangler login` (opens browser OAuth) |
| **Cloudflare account** | [dash.cloudflare.com](https://dash.cloudflare.com) — free tier works |
| **Account ID** | Dashboard → any zone → Overview sidebar, or `wrangler whoami` |
| **API Token (CI/CD)** | Dashboard → API Tokens → "Edit Cloudflare Workers" template (includes Pages) |
| **DNS API Token** | Dashboard → API Tokens → Custom → Zone:DNS:Edit (only if adding custom domains via API) |
| **Zone ID** | Dashboard → your domain → Overview sidebar (only for custom domains) |

## Quick Deploy

For a one-off manual deploy when CI/CD isn't set up yet:

```bash
# 1. Build your site
<your-build-command>          # e.g. hugo --minify, npm run build

# 2. Deploy output directory
wrangler pages deploy <output-dir> --project-name <project-name>
```

Each deploy gets a unique preview URL. The latest deploy on `production` branch becomes the live site at `<project>.pages.dev`.

## Full Setup Workflow

### Step 1 — Create the Pages project

```bash
bash scripts/setup_pages_project.sh <project-name> "<build-command>" <output-dir> [branch]
```

This runs `wrangler pages project create` and prints the resulting `*.pages.dev` URL. The `branch` argument defaults to `main`.

**Manual alternative:**
```bash
wrangler pages project create <project-name> --production-branch main
```

### Step 2 — Deploy

Build and deploy:
```bash
<your-build-command>
wrangler pages deploy <output-dir> --project-name <project-name>
```

### Step 3 — Add a custom domain

```bash
# Set required environment variables
export CLOUDFLARE_ACCOUNT_ID="<your-account-id>"
export CLOUDFLARE_API_TOKEN="<pages-edit-token>"
export CLOUDFLARE_ZONE_ID="<your-zone-id>"
export CLOUDFLARE_DNS_TOKEN="<dns-edit-token>"   # optional, falls back to API_TOKEN

bash scripts/add_custom_domain.sh <custom-domain> <project-name>
```

The script performs two operations:
1. **Registers** the domain on the Pages project via Cloudflare API
2. **Creates** a proxied CNAME DNS record pointing to `<project>.pages.dev`

Both operations are idempotent — safe to re-run.

### Step 4 — Set up CI/CD

See **[references/ci-cd-templates.md](references/ci-cd-templates.md)** for complete GitHub Actions workflows for Hugo, Astro, Next.js, and generic npm builds.

**Required GitHub Secrets:**

| Secret | Value |
|---|---|
| `CLOUDFLARE_API_TOKEN` | API token with "Edit Cloudflare Workers" permissions |
| `CLOUDFLARE_ACCOUNT_ID` | Your Cloudflare account ID |

Set these at: **Repository → Settings → Secrets and variables → Actions → New repository secret**

## Rollback

```bash
# List recent deployments
wrangler pages deployment list --project-name <project-name>

# Rollback: checkout previous commit, rebuild, redeploy
git checkout <commit-hash>
<your-build-command>
wrangler pages deploy <output-dir> --project-name <project-name>

# Return to latest
git checkout main
```

## Verify Deployment

```bash
export CLOUDFLARE_ACCOUNT_ID="<your-account-id>"
export CLOUDFLARE_API_TOKEN="<your-token>"

bash scripts/verify_deployment.sh <project-name> [custom-domain]
```

Shows: latest deployment status (color-coded), last 5 deployments table, custom domain SSL status, and HTTP 200 check on `*.pages.dev`.

## Script Reference

| Script | Purpose | Required env vars |
|---|---|---|
| `setup_pages_project.sh` | Create Pages project via wrangler | `CLOUDFLARE_ACCOUNT_ID` |
| `add_custom_domain.sh` | Register domain + create CNAME | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ZONE_ID` |
| `verify_deployment.sh` | Check deploy status, SSL, HTTP | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN` |

## Token Reference

| Operation | Token needed | Scope | Where used |
|---|---|---|---|
| `wrangler pages deploy` | Wrangler OAuth | Automatic via `wrangler login` | Local CLI, CI/CD |
| Register custom domain on Pages | API Token | Account:Cloudflare Pages:Edit | `add_custom_domain.sh` |
| Create CNAME DNS record | DNS API Token | Zone:DNS:Edit | `add_custom_domain.sh` |
| CI/CD deploy (GitHub Actions) | API Token | "Edit Cloudflare Workers" template | GitHub Secrets |
| Query deployments | API Token | Account:Cloudflare Pages:Read | `verify_deployment.sh` |

**Tip:** For simpler setups, a single API token with both Pages:Edit and DNS:Edit scopes can be used — set `CLOUDFLARE_API_TOKEN` and omit `CLOUDFLARE_DNS_TOKEN`.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `wrangler: command not found` | wrangler not installed | `npm i -g wrangler` |
| `Authentication error` | OAuth expired or wrong token | `wrangler login` (re-authenticate) |
| Custom domain stuck "pending" | Missing or wrong CNAME record | Check DNS: CNAME must point to `<project>.pages.dev` |
| SSL not provisioning | Domain not proxied through Cloudflare | Set CNAME proxy to "Proxied" (orange cloud) |
| 522 error on custom domain | DNS record exists but wrong target | Delete old record, re-run `add_custom_domain.sh` |
| Deploy succeeds but site 404s | Wrong output directory | Verify build output dir matches deploy path |
| CI/CD deploy fails | Missing GitHub secrets | Add `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` |

## Anti-Patterns

- **Don't use Cloudflare's git integration** — use `wrangler pages deploy` for direct uploads. Git integration adds complexity with no benefit for this workflow.
- **Don't create multiple projects for the same site** — one project can have multiple custom domains.
- **Don't skip the CNAME step** — registering a domain on Pages without the DNS record leaves it "pending" indefinitely.
- **Don't use unproxied CNAME records** — Cloudflare's SSL and CDN only work when the orange cloud (proxy) is enabled.
- **Don't hardcode account IDs in scripts** — always use environment variables.

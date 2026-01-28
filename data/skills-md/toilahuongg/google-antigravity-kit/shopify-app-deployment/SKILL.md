---
name: shopify-app-deployment
description: Strategies for deploying Shopify Apps. Focus on overcoming Vercel/Serverless timeouts, using VPS (Coolify/Dokku), and handling long-running background jobs.
---

# Shopify App Deployment Strategy

Deploying Shopify apps is different from standard websites because of **Webhooks**, **Admin API Rate Limits**, and **OAuth handshakes**.

## 1. The "Vercel Problem" (Timeouts)
Vercel Serverless functions have a timeout (usually 10s-60s).
- **Issue**: Shopify bulk operations, product syncs, or installing the app on a large store can take >60s.
- **Result**: `504 Gateway Timeout` and broken installs.

### Solution A: Remix on Vercel (Hybrid)
- Use Vercel for the UI.
- Offload long tasks (syncing) to a separate worker (Cloudflare Workers, Inngest, or separate VPS).
- Use `Defer` in Remix to stream UI while backend works (but doesn't fix hard timeouts for the main thread).

### Solution B: VPS / Docker (Recommended for Serious Apps)
Deploying to a persistent server (Fly.io, Railway, DigitalOcean, Hetzner) eliminates timeouts.
- **Tooling**: Coolify (self-hosted Vercel alternative), Dokku, or manual Docker.

## 2. Deployment Checklist

### A. Environment Variables
Ensure these are set in your CI/CD or platform secrets:
- `SHOPIFY_API_KEY`
- `SHOPIFY_API_SECRET`
- `SCOPES` (must match exactly what's in code)
- `SHOPIFY_APP_URL` (The public HTTPS URL, e.g., `https://app.mytitle.com`)
- `DATABASE_URL`

### B. Database Migrations
Run migrations **during the build** or as a **release phase** command.
- **Fly.io**: Use `release_command` in `fly.toml`.
- **Docker**: Can run `npx prisma migrate deploy` in the `CMD` script before starting the app.

### C. Build Command
Ensure you build for production:
```bash
npm run build
# Ensure this runs `remix build` and copies necessary public assets
```

## 3. Platform Specifics

### Fly.io
Excellent for Shopify apps due to global regions and Docker support.
`fly.toml` example:
```toml
[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "3000"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
```

### Coolify / Hetzner
If you want to save money ($5/mo for a powerful VPS).
1. Install Coolify on VPS.
2. Connect GitHub Repo.
3. Select "Nixpacks" or "Docker file".
4. Set Environment Variables.
5. Deploy.

## 4. Background Jobs (Crucial)
You MUST have a strategy for background jobs.
- **Options**:
  - **Redis + BullMQ**: Requires a persistent Redis instance. (See `redis-bullmq` skill).
  - **Inngest / Trigger.dev**: Serverless background jobs. Good if you don't want to manage Redis.

## 5. Post-Deployment Verification
1. **Install Test**: Install the app on a Development Store.
2. **Webhook Test**: Trigger a webhook (e.g., update a product) and check server logs.
3. **App Proxy**: If used, verify the proxy URL loads correctly (CORS errors are common here).

---
name: using-cli-tools
description: Enforces CLI tool usage over web dashboards for reproducibility and scriptability. Use when working with Git/GitHub, Supabase, Vercel, Netlify, Cloudflare, AWS, Stripe, Prisma, Docker, or any cloud service. Triggers on deployments, database operations, migrations, PRs, issues, webhooks, or environment management.
---

# Using CLI Tools

Prefer CLI tools over web dashboards. CLIs are scriptable, reproducible, and keep developers in flow.

**Principle**: If a CLI exists for a service, use it. Only fall back to web UI when the CLI genuinely can't do the task.

## Quick Reference

| Category | Tools |
|----------|-------|
| Hosting | `vercel`, `netlify`, `wrangler`, `railway`, `flyctl` |
| Backend/DB | `supabase`, `prisma`, `aws` |
| Payments | `stripe` |
| Dev Tools | `gh`, `docker compose`, `ngrok`, `turbo` |

## Git & GitHub (`gh`)

```bash
gh pr create --title "feat: add auth" --body "..."
gh pr list --state open
gh pr checkout 123
gh pr merge --squash
gh issue create --title "Bug" --label bug
gh run list
gh run view 12345 --log
```

## Supabase (`supabase`)

```bash
supabase link --project-ref <ref>
supabase db push
supabase db pull
supabase migration new <name>
supabase functions deploy <name>
supabase gen types typescript --linked > types/supabase.ts
```

## Vercel (`vercel`)

```bash
vercel                  # preview deploy
vercel --prod           # production deploy
vercel env pull .env.local
vercel logs <url>
```

## Netlify (`netlify`)

```bash
netlify init
netlify dev             # local dev server with functions
netlify deploy          # draft deploy
netlify deploy --prod
netlify env:set KEY value
netlify functions:serve
```

## Cloudflare (`wrangler`)

```bash
wrangler init
wrangler dev            # local dev
wrangler deploy
wrangler pages deploy ./dist
wrangler kv:namespace create <name>
wrangler r2 bucket create <name>
wrangler secret put <name>
```

## Prisma (`prisma`)

```bash
npx prisma init
npx prisma generate     # generate client
npx prisma db push      # sync schema (dev)
npx prisma migrate dev  # create migration
npx prisma migrate deploy
npx prisma studio       # visual editor
```

## Stripe (`stripe`)

```bash
stripe login
stripe listen --forward-to localhost:3000/api/webhooks
stripe trigger payment_intent.succeeded
stripe logs tail
stripe products create --name="Pro Plan"
```

## Docker (`docker compose`)

```bash
docker compose up -d
docker compose logs -f <service>
docker compose exec <service> sh
docker compose down
docker compose build --no-cache
```

## Package Manager Detection

Respect the project's lock file:
- `package-lock.json` → `npm`
- `pnpm-lock.yaml` → `pnpm`
- `yarn.lock` → `yarn`
- `bun.lockb` → `bun`

Never mix package managers in the same project.

## Additional Tools

For less common but useful CLIs, see [ADDITIONAL-TOOLS.md](ADDITIONAL-TOOLS.md):
- AWS CLI basics
- Railway, Fly.io
- ngrok, Turborepo
- Database CLIs (Planetscale, Neon)

## When CLI Unavailable

If a task requires the web UI (e.g., enabling a Supabase extension), note this explicitly with the exact navigation path.

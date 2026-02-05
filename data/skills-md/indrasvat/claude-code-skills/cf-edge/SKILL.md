---
name: cf-edge
description: Deploy web apps, APIs, static sites, and edge functions to Cloudflare's free tier using wrangler and cloudflared CLIs. Use when user wants to (1) host/deploy a website, blog, or web app, (2) create serverless APIs or edge functions, (3) set up databases (SQL or KV), (4) store files/objects, (5) expose localhost via tunnel, (6) deploy any personal project to the cloud for free. Covers Workers, Pages, D1, KV, R2, Durable Objects, Workers AI, Tunnels, Email Routing. All deployments stay within $0 free tier limits.
---

# Cloudflare Free Tier Deployment

Deploy to Cloudflare's edge network at $0 cost. All services have free tiers sufficient for personal projects.

## Prerequisites

```bash
# Verify CLI tools
wrangler --version   # Workers, Pages, D1, KV, R2
cloudflared --version  # Tunnels

# If missing:
npm install -g wrangler
# cloudflared:
brew install cloudflare/cloudflare/cloudflared
```

## Quick Deploy Commands

### Static Site (Pages)
```bash
wrangler pages project create <name>
wrangler pages deploy ./dist  # or ./build, ./out, ./public
# Result: <name>.pages.dev — unlimited bandwidth
```

### Serverless API (Workers)
```bash
wrangler init <name> && cd <name>
wrangler dev          # local: localhost:8787
wrangler deploy       # live: <name>.<account>.workers.dev
```

### SQL Database (D1)
```bash
wrangler d1 create <name>
wrangler d1 execute <name> --command "CREATE TABLE ..."
# Add to wrangler.toml: [[d1_databases]] binding/name/id
```

### Key-Value Store (KV)
```bash
wrangler kv:namespace create <NAME>
# Add to wrangler.toml: [[kv_namespaces]] binding/id
```

### Object Storage (R2) — requires credit card, won't charge under limits
```bash
wrangler r2 bucket create <name>
wrangler r2 object put <bucket>/path --file ./file
```

### Expose Localhost (Tunnel)
```bash
cloudflared tunnel --url http://localhost:3000  # instant public URL
```

## Free Tier Limits (HARD CONSTRAINTS)

| Service | Limit | Reset |
|---------|-------|-------|
| **Workers** | 100K req/day, 10ms CPU/req | Daily UTC |
| **Pages** | Unlimited bandwidth, 500 builds/mo | Monthly |
| **D1** | 5 GB storage, 5M reads/day, 100K writes/day | Daily UTC |
| **KV** | 1 GB storage, 100K reads/day, 1K writes/day | Daily UTC |
| **R2** | 10 GB storage, $0 egress | Monthly |
| **Durable Objects** | 100K req/day, 5 GB storage | Daily UTC |
| **Workers AI** | 10K neurons/day (~500 LLM queries) | Daily UTC |
| **Tunnels** | Unlimited | — |

See [`references/limits.md`](references/limits.md) for detailed breakdown.

## wrangler.toml Template

```toml
name = "my-app"
main = "src/index.js"  # or index.ts
compatibility_date = "2024-01-01"

# D1 Database
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "<from wrangler d1 create>"

# KV Namespace
[[kv_namespaces]]
binding = "KV"
id = "<from wrangler kv:namespace create>"

# R2 Bucket
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"

# Environment Variables
[vars]
ENVIRONMENT = "production"
```

## Worker Patterns

### Basic API Router
```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname === '/api/data') {
      const data = await env.DB.prepare('SELECT * FROM items').all();
      return Response.json(data.results);
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### With D1 + KV
```javascript
export default {
  async fetch(request, env) {
    // KV: fast reads, eventual consistency
    const cached = await env.KV.get('key', 'json');
    if (cached) return Response.json(cached);
    
    // D1: SQL queries
    const { results } = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(1).all();
    
    // Cache result
    await env.KV.put('key', JSON.stringify(results), { expirationTtl: 3600 });
    return Response.json(results);
  }
};
```

### Workers AI
```javascript
export default {
  async fetch(request, env) {
    const response = await env.AI.run('@cf/meta/llama-3.2-1b-instruct', {
      prompt: 'Hello, how are you?'
    });
    return Response.json(response);
  }
};
// Add to wrangler.toml: [ai] binding = "AI"
```

## Persistent Tunnel (Custom Domain)

```bash
cloudflared tunnel login
cloudflared tunnel create <tunnel-name>
cloudflared tunnel route dns <tunnel-name> subdomain.yourdomain.com

# Create ~/.cloudflared/config.yml:
cat << EOF > ~/.cloudflared/config.yml
tunnel: <tunnel-id>
credentials-file: ~/.cloudflared/<tunnel-id>.json
ingress:
  - hostname: subdomain.yourdomain.com
    service: http://localhost:3000
  - service: http_status:404
EOF

cloudflared tunnel run <tunnel-name>
```

## Staying Within Free Limits

1. **Before deploying**: Estimate daily requests — stay under 100K/day for Workers
2. **Use caching**: KV for read-heavy data reduces D1 reads
3. **Optimize queries**: Add indexes to D1, avoid full table scans
4. **Static over dynamic**: Serve static assets from Pages (unlimited) not Workers
5. **Monitor usage**: `wrangler d1 info <db>` or check dashboard

## What NOT to Do (ToS Violations)

- Don't use CDN primarily for video streaming or large media distribution
- Don't proxy traffic for other sites (reverse proxy abuse)
- Don't run crypto mining or similar compute-heavy workloads
- Don't exceed 10ms CPU per Worker request consistently

## Project Structure Recommendations

```bash
my-project/
├── wrangler.toml
├── package.json
├── src/
│   └── index.js      # Worker entry
├── public/           # Static assets (if using Pages)
└── migrations/       # D1 schema migrations
    └── 0001_init.sql
```

## Common Commands Reference

```bash
# Development
wrangler dev                    # Local dev server
wrangler dev --remote           # Dev against real services

# Deployment  
wrangler deploy                 # Deploy Worker
wrangler pages deploy ./dist    # Deploy Pages

# Database
wrangler d1 execute <db> --file ./migrations/001.sql
wrangler d1 execute <db> --command "SELECT * FROM users"

# Debugging
wrangler tail                   # Live logs
wrangler tail --format pretty   # Formatted logs

# Info
wrangler whoami                 # Check auth
wrangler d1 info <db>           # DB stats
```

## See Also

- [`references/limits.md`](references/limits.md) — Detailed free tier limits and calculations
- [`references/services.md`](references/services.md) — Full service configurations and patterns

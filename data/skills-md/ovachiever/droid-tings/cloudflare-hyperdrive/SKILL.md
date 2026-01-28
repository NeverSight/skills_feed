---
name: cloudflare-hyperdrive
description: |
  Connect Workers to PostgreSQL/MySQL with Hyperdrive's global pooling and caching. Use when: connecting to existing databases, setting up connection pools, using node-postgres/mysql2, integrating Drizzle/Prisma, or troubleshooting pool acquisition failures, TLS errors, nodejs_compat missing, or eval() disallowed.
license: MIT
---

# Cloudflare Hyperdrive

**Status**: Production Ready ✅
**Last Updated**: 2025-11-23
**Dependencies**: cloudflare-worker-base (recommended for Worker setup)
**Latest Versions**: wrangler@4.50.0, pg@8.16.3+ (minimum), postgres@3.4.7, mysql2@3.15.3

**Recent Updates (2025)**:
- **July 2025**: Configurable connection counts (min 5, max ~20 Free/~100 Paid)
- **May 2025**: 5x faster cache hits (regional prepared statement caching), FedRAMP Moderate authorization
- **April 2025**: Free plan availability (10 configs), MySQL GA support
- **March 2025**: 90% latency reduction (pools near database), IP access control (standard CF IP ranges)
- **nodejs_compat_v2**: pg driver no longer requires node_compat mode (auto-enabled with compatibility_date 2024-09-23+)
- **Limits**: 25 Hyperdrive configurations per account (Paid), 10 per account (Free)

---

## Quick Start (5 Minutes)

### 1. Create Hyperdrive Configuration

```bash
# For PostgreSQL
npx wrangler hyperdrive create my-postgres-db \
  --connection-string="postgres://user:password@db-host.cloud:5432/database"

# For MySQL
npx wrangler hyperdrive create my-mysql-db \
  --connection-string="mysql://user:password@db-host.cloud:3306/database"

# Output:
# ✅ Successfully created Hyperdrive configuration
#
# [[hyperdrive]]
# binding = "HYPERDRIVE"
# id = "a76a99bc-7901-48c9-9c15-c4b11b559606"
```

**Save the `id` value** - you'll need it in the next step!

---

### 2. Configure Bindings in wrangler.jsonc

Add to your `wrangler.jsonc`:

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-09-23",
  "compatibility_flags": ["nodejs_compat"],  // REQUIRED for database drivers
  "hyperdrive": [
    {
      "binding": "HYPERDRIVE",                     // Available as env.HYPERDRIVE
      "id": "a76a99bc-7901-48c9-9c15-c4b11b559606"  // From wrangler hyperdrive create
    }
  ]
}
```

**CRITICAL:**
- `nodejs_compat` flag is **REQUIRED** for all database drivers
- `binding` is how you access Hyperdrive in code (`env.HYPERDRIVE`)
- `id` is the Hyperdrive configuration ID (NOT your database ID)

---

### 3. Install Database Driver

```bash
# For PostgreSQL (choose one)
npm install pg           # node-postgres (most common)
npm install postgres     # postgres.js (modern, minimum v3.4.5)

# For MySQL
npm install mysql2       # mysql2 (minimum v3.13.0)
```

---

### 4. Query Your Database

**PostgreSQL with node-postgres (pg):**
```typescript
import { Client } from "pg";

type Bindings = {
  HYPERDRIVE: Hyperdrive;
};

export default {
  async fetch(request: Request, env: Bindings, ctx: ExecutionContext) {
    const client = new Client({
      connectionString: env.HYPERDRIVE.connectionString
    });

    await client.connect();

    try {
      const result = await client.query('SELECT * FROM users LIMIT 10');
      return Response.json({ users: result.rows });
    } finally {
      // Clean up connection AFTER response is sent
      ctx.waitUntil(client.end());
    }
  }
};
```

**MySQL with mysql2:**
```typescript
import { createConnection } from "mysql2/promise";

export default {
  async fetch(request: Request, env: Bindings, ctx: ExecutionContext) {
    const connection = await createConnection({
      host: env.HYPERDRIVE.host,
      user: env.HYPERDRIVE.user,
      password: env.HYPERDRIVE.password,
      database: env.HYPERDRIVE.database,
      port: env.HYPERDRIVE.port,
      disableEval: true  // REQUIRED for Workers (eval() not supported)
    });

    try {
      const [rows] = await connection.query('SELECT * FROM users LIMIT 10');
      return Response.json({ users: rows });
    } finally {
      ctx.waitUntil(connection.end());
    }
  }
};
```

---

### 5. Deploy

```bash
npx wrangler deploy
```

**That's it!** Your Worker now connects to your existing database via Hyperdrive with:
- ✅ Global connection pooling
- ✅ Automatic query caching
- ✅ Reduced latency (eliminates 7 round trips)

---

## How Hyperdrive Works

Hyperdrive eliminates 7 connection round trips (TCP + TLS + auth) by:
- Edge connection setup near Worker (low latency)
- Connection pooling near database (March 2025: 90% latency reduction)
- Query caching at edge (May 2025: 5x faster cache hits)

**Result**: Single-region databases feel globally distributed.

---

## Setup Steps

### Prerequisites

- Cloudflare account with Workers access
- PostgreSQL (v9.0-17.x) or MySQL (v5.7-8.x) database
- Database accessible via public internet (TLS/SSL required) or private network (Cloudflare Tunnel)
- **April 2025**: Available on Free plan (10 configs) and Paid plan (25 configs)

### Connection String Formats

```bash
# PostgreSQL
postgres://user:password@host:5432/database
postgres://user:password@host:5432/database?sslmode=require

# MySQL
mysql://user:password@host:3306/database

# URL-encode special chars: p@ssw$rd → p%40ssw%24rd
```

---

## Connection Patterns

### Single Connection (pg.Client)
```typescript
const client = new Client({ connectionString: env.HYPERDRIVE.connectionString });
await client.connect();
const result = await client.query('SELECT ...');
ctx.waitUntil(client.end());  // CRITICAL: Non-blocking cleanup
```
**Use for**: Simple queries, single query per request

### Connection Pool (pg.Pool)
```typescript
const pool = new Pool({
  connectionString: env.HYPERDRIVE.connectionString,
  max: 5  // CRITICAL: Workers limit is 6 connections (July 2025: configurable ~20 Free, ~100 Paid)
});
const [result1, result2] = await Promise.all([
  pool.query('SELECT ...'),
  pool.query('SELECT ...')
]);
ctx.waitUntil(pool.end());
```
**Use for**: Parallel queries in single request

### Connection Cleanup Rule
**ALWAYS use `ctx.waitUntil(client.end())`** - non-blocking cleanup after response sent
**NEVER use `await client.end()`** - blocks response, adds latency

---

## ORM Integration

### Drizzle ORM
```typescript
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

const sql = postgres(env.HYPERDRIVE.connectionString, { max: 5 });
const db = drizzle(sql);
const allUsers = await db.select().from(users);
ctx.waitUntil(sql.end());
```

### Prisma ORM
```typescript
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "@prisma/client";
import { Pool } from "pg";

const pool = new Pool({ connectionString: env.HYPERDRIVE.connectionString, max: 5 });
const adapter = new PrismaPg(pool);
const prisma = new PrismaClient({ adapter });
const users = await prisma.user.findMany();
ctx.waitUntil(pool.end());
```
**Note**: Prisma requires driver adapters (`@prisma/adapter-pg`).

---

## Local Development

**Option 1: Environment Variable (Recommended)**
```bash
export CLOUDFLARE_HYPERDRIVE_LOCAL_CONNECTION_STRING_HYPERDRIVE="postgres://user:password@localhost:5432/local_db"
npx wrangler dev
```
Safe to commit config, no credentials in wrangler.jsonc.

**Option 2: localConnectionString in wrangler.jsonc**
```jsonc
{ "hyperdrive": [{ "binding": "HYPERDRIVE", "id": "prod-id", "localConnectionString": "postgres://..." }] }
```
⚠️ Don't commit credentials to version control.

**Option 3: Remote Development**
```bash
npx wrangler dev --remote  # ⚠️ Uses PRODUCTION database
```

---

## Query Caching

**Cached**: SELECT (non-mutating queries)
**NOT Cached**: INSERT, UPDATE, DELETE, volatile functions (LASTVAL, LAST_INSERT_ID)

**May 2025**: 5x faster cache hits via regional prepared statement caching.

**Critical for postgres.js:**
```typescript
const sql = postgres(env.HYPERDRIVE.connectionString, {
  prepare: true  // REQUIRED for caching
});
```

**Check cache status:**
```typescript
response.headers.get('cf-cache-status');  // HIT, MISS, BYPASS, EXPIRED
```

---

## TLS/SSL Configuration

**SSL Modes**: `require` (default), `verify-ca` (verify CA), `verify-full` (verify CA + hostname)

**Server Certificates (verify-ca/verify-full):**
```bash
npx wrangler cert upload certificate-authority --ca-cert root-ca.pem --name my-ca-cert
npx wrangler hyperdrive create my-db --connection-string="postgres://..." --ca-certificate-id <ID> --sslmode verify-full
```

**Client Certificates (mTLS):**
```bash
npx wrangler cert upload mtls-certificate --cert client-cert.pem --key client-key.pem --name my-cert
npx wrangler hyperdrive create my-db --connection-string="postgres://..." --mtls-certificate-id <ID>
```

---

## Private Database Access (Cloudflare Tunnel)

Connect to databases in private networks (VPCs, on-premises):

```bash
# 1. Install cloudflared (macOS: brew install cloudflare/cloudflare/cloudflared)
# 2. Create tunnel
cloudflared tunnel create my-db-tunnel

# 3. Configure config.yml
# tunnel: <TUNNEL_ID>
# ingress:
#   - hostname: db.example.com
#     service: tcp://localhost:5432

# 4. Run tunnel
cloudflared tunnel run my-db-tunnel

# 5. Create Hyperdrive
npx wrangler hyperdrive create my-private-db --connection-string="postgres://user:password@db.example.com:5432/database"
```

---

## Critical Rules

### Always Do

✅ Include `nodejs_compat` in `compatibility_flags`
✅ Use `ctx.waitUntil(client.end())` for connection cleanup
✅ Set `max: 5` for connection pools (Workers limit: 6)
✅ Enable TLS/SSL on your database (Hyperdrive requires it)
✅ Use prepared statements for caching (postgres.js: `prepare: true`)
✅ Set `disableEval: true` for mysql2 driver
✅ Handle errors gracefully with try/catch
✅ Use environment variables for local development connection strings
✅ Test locally with `wrangler dev` before deploying

### Never Do

❌ Skip `nodejs_compat` flag (causes "No such module" errors)
❌ Use private IP addresses directly (use Cloudflare Tunnel instead)
❌ Use `await client.end()` (blocks response, use `ctx.waitUntil()`)
❌ Set connection pool max > 5 (exceeds Workers' 6 connection limit)
❌ Wrap all queries in transactions (limits connection multiplexing)
❌ Use SQL-level PREPARE/EXECUTE/DEALLOCATE (unsupported)
❌ Use advisory locks, LISTEN/NOTIFY (PostgreSQL unsupported features)
❌ Use multi-statement queries in MySQL (unsupported)
❌ Commit database credentials to version control

---

## Wrangler Commands Reference

```bash
# Create Hyperdrive configuration
wrangler hyperdrive create <name> --connection-string="postgres://..."

# List all Hyperdrive configurations
wrangler hyperdrive list

# Get details of a configuration
wrangler hyperdrive get <hyperdrive-id>

# Update connection string
wrangler hyperdrive update <hyperdrive-id> --connection-string="postgres://..."

# Delete configuration
wrangler hyperdrive delete <hyperdrive-id>

# Upload CA certificate
wrangler cert upload certificate-authority --ca-cert <file>.pem --name <name>

# Upload client certificate pair
wrangler cert upload mtls-certificate --cert <cert>.pem --key <key>.pem --name <name>
```

---

## Supported Databases

**PostgreSQL (v9.0-17.x)**: AWS RDS/Aurora, Google Cloud SQL, Azure, Neon, Supabase, PlanetScale, Timescale, CockroachDB, Materialize, Fly.io, pgEdge, Prisma Postgres

**MySQL (v5.7-8.x)**: AWS RDS/Aurora, Google Cloud SQL, Azure, PlanetScale, MariaDB (April 2025 GA)

**NOT Supported**: SQL Server, MongoDB, Oracle

---

## Unsupported Features

### PostgreSQL
- SQL-level prepared statements (`PREPARE`, `EXECUTE`, `DEALLOCATE`)
- Advisory locks
- `LISTEN` and `NOTIFY`
- Per-session state modifications

### MySQL
- Non-UTF8 characters in queries
- `USE` statements
- Multi-statement queries
- Protocol-level prepared statements (`COM_STMT_PREPARE`)
- `COM_INIT_DB` messages
- Auth plugins other than `caching_sha2_password` or `mysql_native_password`

**Workaround**: For unsupported features, create a second direct client connection (without Hyperdrive).

---

## Performance Best Practices

1. **Avoid long-running transactions** - Limits connection multiplexing
2. **Use prepared statements** - Enables query caching (postgres.js: `prepare: true`)
3. **Set max: 5 for pools** - Stays within Workers' 6 connection limit
4. **Disable fetch_types if not needed** - Reduces latency (postgres.js)
5. **Use ctx.waitUntil() for cleanup** - Non-blocking connection close
6. **Cache-friendly queries** - Prefer SELECT over complex joins
7. **Index frequently queried columns** - Improves query performance
8. **Monitor with Hyperdrive analytics** - Track cache hit ratios and latency

---

## Troubleshooting

See `references/troubleshooting.md` for complete error reference with solutions.

**Quick fixes:**

| Error | Solution |
|-------|----------|
| "No such module 'node:*'" | Add `nodejs_compat` to compatibility_flags |
| "TLS not supported by database" | Enable SSL/TLS on your database |
| "Connection refused" | Check firewall rules, allow public internet or use Tunnel |
| "Failed to acquire connection" | Use `ctx.waitUntil()` for cleanup, avoid long transactions |
| "Code generation from strings disallowed" | Set `disableEval: true` in mysql2 config |
| "Bad hostname" | Verify DNS resolves, check for typos |
| "Invalid database credentials" | Check username/password (case-sensitive) |

---

## Metrics and Analytics

[Hyperdrive Dashboard](https://dash.cloudflare.com/?to=/:account/workers/hyperdrive) → Select config → Metrics tab

**Available**: Query count, cache hit ratio, query latency (p50/p95/p99), connection latency, query/result bytes, error rate

---

## Credential Rotation

```bash
# Option 1: Create new config (zero downtime)
wrangler hyperdrive create my-db-v2 --connection-string="postgres://new-creds..."
# Update wrangler.jsonc, deploy, delete old config

# Option 2: Update existing
wrangler hyperdrive update <id> --connection-string="postgres://new-creds..."
```

**Best practice**: Separate configs for staging/production.

---

## References

- [Official Documentation](https://developers.cloudflare.com/hyperdrive/)
- [Get Started Guide](https://developers.cloudflare.com/hyperdrive/get-started/)
- [How Hyperdrive Works](https://developers.cloudflare.com/hyperdrive/configuration/how-hyperdrive-works/)
- [Query Caching](https://developers.cloudflare.com/hyperdrive/configuration/query-caching/)
- [Local Development](https://developers.cloudflare.com/hyperdrive/configuration/local-development/)
- [TLS/SSL Certificates](https://developers.cloudflare.com/hyperdrive/configuration/tls-ssl-certificates-for-hyperdrive/)
- [Troubleshooting Guide](https://developers.cloudflare.com/hyperdrive/observability/troubleshooting/)
- [Wrangler Commands](https://developers.cloudflare.com/hyperdrive/reference/wrangler-commands/)
- [Supported Databases](https://developers.cloudflare.com/hyperdrive/reference/supported-databases-and-features/)

---

**Last Updated**: 2025-11-23
**Package Versions**: wrangler@4.50.0, pg@8.16.3+ (minimum), postgres@3.4.7, mysql2@3.15.3
**Production Tested**: Based on official Cloudflare documentation and community examples

---
name: stripe-sync-migrations
description: When the user wants to run database migrations for stripe-sync-engine. Also use when the user mentions "run migrations," "stripe schema," "create stripe tables," "database setup," or "stripe_migrations."
---

# Stripe Sync Engine Migrations

You are an expert in running and managing database migrations for stripe-sync-engine. Your goal is to help users set up the PostgreSQL schema required for syncing Stripe data.

## Initial Assessment

Before proceeding, verify:

1. **Is stripe-sync-engine installed?** If not, run the setup skill first.
2. **Is DATABASE_URL environment variable configured?**
3. **Does the database user have permission to create schemas?**

## Running Migrations

### Method 1: Create a Migration Script (Recommended)

Create `scripts/run-migrations.ts`:

```typescript
import { runMigrations } from "stripe-sync-engine";

async function main() {
  if (!process.env.DATABASE_URL) {
    throw new Error("DATABASE_URL environment variable is not set");
  }

  console.log("Running Stripe sync engine migrations...");

  await runMigrations({
    databaseUrl: process.env.DATABASE_URL,
    schema: "stripe",
    tablePrefix: "",
    migrationTableName: "stripe_migrations",
  });

  console.log("Migrations completed successfully");
}

main().catch((error) => {
  console.error("Migration failed:", error);
  process.exit(1);
});
```

Add to `package.json`:

```json
{
  "scripts": {
    "stripe:migrate": "tsx scripts/run-migrations.ts"
  }
}
```

Install tsx if needed:
```bash
npm install -D tsx
```

Run:
```bash
npm run stripe:migrate
```

### Method 2: API Endpoint (For Serverless)

Create an API endpoint to trigger migrations:

#### Next.js App Router

Create `app/api/migrations/run/route.ts`:

```typescript
import { runMigrations } from "stripe-sync-engine";
import { NextResponse } from "next/server";

export async function POST() {
  if (!process.env.DATABASE_URL) {
    return NextResponse.json(
      { error: "DATABASE_URL not configured" },
      { status: 500 }
    );
  }

  try {
    await runMigrations({
      databaseUrl: process.env.DATABASE_URL,
      schema: "stripe",
    });
    return NextResponse.json({ status: "migrated" });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
```

#### Hono

```typescript
app.post('/migrations/run', async (c) => {
  await runMigrations({ databaseUrl, schema: 'stripe' });
  return c.json({ status: 'migrated' });
});
```

## Migration Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `databaseUrl` | string | PostgreSQL connection string |
| `schema` | string | Database schema name (default: `stripe`) |
| `tablePrefix` | string | Prefix for all table names (default: empty) |
| `migrationTableName` | string | Name of migrations tracking table (default: `stripe_migrations`) |
| `ssl` | object | SSL connection options |
| `logger` | Logger | Pino logger instance |

## Verifying Migrations

After running migrations, verify the schema was created:

```sql
-- Check schema exists
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name = 'stripe';

-- List all created tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'stripe'
ORDER BY table_name;

-- Check migrations table
SELECT * FROM stripe.stripe_migrations ORDER BY id;
```

## Tables Created

The migrations create these tables in the `stripe` schema:

| Table | Description |
|-------|-------------|
| `customers` | Customer records |
| `products` | Product catalog |
| `prices` | Pricing information |
| `plans` | Legacy plan objects |
| `subscriptions` | Subscription records |
| `subscription_items` | Items within subscriptions |
| `invoices` | Invoice records |
| `invoice_line_items` | Line items on invoices |
| `charges` | Charge records |
| `payment_intents` | Payment attempts |
| `payment_methods` | Saved payment methods |
| `setup_intents` | Setup intent records |
| `refunds` | Refund records |
| `disputes` | Dispute records |
| `credit_notes` | Credit note records |
| `coupons` | Coupon records |
| `tax_ids` | Tax ID records |

## Troubleshooting

### Permission Denied

If you see permission errors:

```sql
-- Grant schema creation permission
GRANT CREATE ON DATABASE your_database TO your_user;

-- Or create schema manually first
CREATE SCHEMA IF NOT EXISTS stripe;
GRANT ALL ON SCHEMA stripe TO your_user;
```

### PostgreSQL Version

stripe-sync-engine requires PostgreSQL 12+. Recommended: PostgreSQL 14+.

Check version:
```sql
SELECT version();
```

### Connection Issues

Verify your connection string format:
```
postgresql://username:password@host:port/database?sslmode=require
```

For local development without SSL:
```
postgresql://username:password@localhost:5432/database
```

## Related Skills

- **setup**: Install and configure stripe-sync-engine
- **webhook**: Set up webhook handlers after migrations
- **troubleshooting**: Debug migration and connection issues

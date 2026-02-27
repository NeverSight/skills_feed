---
name: stripe-sync-backfill
description: When the user wants to import historical Stripe data. Also use when the user mentions "backfill stripe data," "syncBackfill," "import stripe data," "sync existing data," or "historical sync."
---

# Stripe Sync Engine Backfill

You are an expert in backfilling historical Stripe data using stripe-sync-engine. Your goal is to help users import their existing Stripe data into PostgreSQL.

## Initial Assessment

Before proceeding, verify:

1. **Is stripe-sync-engine set up?** (see setup skill)
2. **Are migrations completed?** (see migrations skill)
3. **How much historical data do you need?** (all time, last year, last 30 days?)
4. **How large is your Stripe account?** (affects backfill strategy)

## Basic Backfill

### Method 1: Backfill Script (Recommended)

Create `scripts/backfill-stripe.ts`:

```typescript
import { StripeSync } from "stripe-sync-engine";

const stripeSync = new StripeSync({
  poolConfig: {
    connectionString: process.env.DATABASE_URL!,
    max: 10,
  },
  stripeSecretKey: process.env.STRIPE_SECRET_KEY!,
  stripeWebhookSecret: process.env.STRIPE_WEBHOOK_SECRET!,
  schema: "stripe",
  autoExpandLists: true,
  backfillRelatedEntities: true,
});

async function main() {
  const startDateArg = process.argv[2];

  if (!startDateArg) {
    console.error("Usage: npm run stripe:backfill <start-date-unix-timestamp>");
    console.error("Example: npm run stripe:backfill 1704067200");
    process.exit(1);
  }

  const timestamp = parseInt(startDateArg, 10);
  console.log(`Backfilling Stripe data from ${new Date(timestamp * 1000).toISOString()}...`);

  await stripeSync.syncBackfill({
    object: "all",
    created: { gte: timestamp },
  });

  console.log("Backfill completed successfully");
}

main().catch((error) => {
  console.error("Backfill failed:", error);
  process.exit(1);
});
```

Add to `package.json`:

```json
{
  "scripts": {
    "stripe:backfill": "tsx scripts/backfill-stripe.ts"
  }
}
```

Run:
```bash
# Backfill from January 1, 2024 (Unix timestamp)
npm run stripe:backfill 1704067200

# Get Unix timestamp for a date (macOS/Linux)
date -d "2024-01-01" +%s
```

### Method 2: API Endpoint

Create `app/api/sync/backfill/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { stripeSync } from "@/lib/stripeSync";

export async function POST(request: Request) {
  const { object = "all", startDate } = await request.json();

  try {
    const result = await stripeSync.syncBackfill({
      object,
      created: startDate ? { gte: startDate } : undefined,
    });

    return NextResponse.json({ status: "completed", result });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
```

## Backfill Options

### Object Types

The `object` parameter accepts:

| Value | Description |
|-------|-------------|
| `all` | All supported object types |
| `customer` | Customer records |
| `product` | Product catalog |
| `price` | Price objects |
| `plan` | Legacy plan objects |
| `subscription` | Subscription records |
| `invoice` | Invoice records |
| `charge` | Charge records |
| `payment_intent` | Payment intents |
| `payment_method` | Payment methods |
| `setup_intent` | Setup intents |
| `dispute` | Dispute records |

### Date Filters

The `created` parameter supports Stripe's RangeQueryParam:

```typescript
// All objects created after a date
created: { gte: 1704067200 }

// Objects created before a date
created: { lte: 1735689599 }

// Objects in a date range
created: { gte: 1704067200, lte: 1735689599 }

// Exclusive comparisons
created: { gt: 1704067200 }  // strictly after
created: { lt: 1735689599 }  // strictly before
```

## Backfilling Large Accounts (10,000+ Objects)

For large Stripe accounts, backfill in smaller chunks to avoid timeouts:

### Day-by-Day Backfill

```typescript
import { StripeSync } from "stripe-sync-engine";

const stripeSync = new StripeSync({
  poolConfig: { connectionString: process.env.DATABASE_URL! },
  stripeSecretKey: process.env.STRIPE_SECRET_KEY!,
  stripeWebhookSecret: process.env.STRIPE_WEBHOOK_SECRET!,
});

async function backfillByDay(startDate: Date, endDate: Date) {
  const currentDate = new Date(startDate);

  while (currentDate <= endDate) {
    const dayStart = Math.floor(currentDate.getTime() / 1000);
    const dayEnd = dayStart + 86400 - 1; // End of day

    console.log(`Syncing ${currentDate.toISOString().split('T')[0]}...`);

    await stripeSync.syncBackfill({
      object: "all",
      created: { gte: dayStart, lte: dayEnd },
    });

    console.log(`Completed ${currentDate.toISOString().split('T')[0]}`);

    currentDate.setDate(currentDate.getDate() + 1);
  }
}

// Backfill all of 2024
backfillByDay(new Date("2024-01-01"), new Date("2024-12-31"));
```

### Object-by-Object Backfill

```typescript
const objects = [
  "product",
  "price",
  "customer",
  "subscription",
  "invoice",
  "payment_intent",
  "charge",
];

for (const object of objects) {
  console.log(`Backfilling ${object}s...`);
  await stripeSync.syncBackfill({
    object,
    created: { gte: 1704067200 },
  });
  console.log(`Completed ${object}s`);
}
```

## Syncing Single Entities

To sync or refresh a single Stripe object:

```typescript
// Sync by Stripe ID (type is auto-detected from prefix)
await stripeSync.syncSingleEntity("cus_1234567890");
await stripeSync.syncSingleEntity("prod_1234567890");
await stripeSync.syncSingleEntity("sub_1234567890");
await stripeSync.syncSingleEntity("in_1234567890");
await stripeSync.syncSingleEntity("pi_1234567890");
```

### API Endpoint for Single Entity Sync

Create `app/api/sync/entity/[id]/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { stripeSync } from "@/lib/stripeSync";

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    await stripeSync.syncSingleEntity(params.id);
    return NextResponse.json({ status: "synced", id: params.id });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
```

## Revalidation on Sync

For critical objects, always fetch fresh data from Stripe API instead of trusting webhook payloads:

```typescript
const stripeSync = new StripeSync({
  // ... other config
  revalidateObjectsViaStripeApi: [
    "customer",
    "subscription",
    "invoice",
    "payment_intent",
  ],
});
```

## Verifying Backfill Results

After backfill completes, verify data in your database:

```sql
-- Count synced objects
SELECT
  'customers' as type, COUNT(*) as count FROM stripe.customers
UNION ALL
SELECT 'products', COUNT(*) FROM stripe.products
UNION ALL
SELECT 'subscriptions', COUNT(*) FROM stripe.subscriptions
UNION ALL
SELECT 'invoices', COUNT(*) FROM stripe.invoices;

-- Check date range of synced data
SELECT
  MIN(to_timestamp(created)) as earliest,
  MAX(to_timestamp(created)) as latest
FROM stripe.customers;
```

## Troubleshooting

### Timeout Errors
- Backfill in smaller date ranges (daily or weekly)
- Backfill specific object types separately
- Increase function timeout if using serverless

### Rate Limits
- stripe-sync-engine respects Stripe rate limits automatically
- For very large backfills, run during off-peak hours

### Missing Related Data
- Enable `backfillRelatedEntities: true` in configuration
- This ensures foreign key relationships are maintained

## Related Skills

- **setup**: Install and configure stripe-sync-engine
- **migrations**: Create database schema before backfill
- **query**: Query the backfilled data

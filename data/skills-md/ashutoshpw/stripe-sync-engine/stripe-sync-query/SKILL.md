---
name: stripe-sync-query
description: When the user wants to query synced Stripe data. Also use when the user mentions "query stripe data," "stripe tables," "select from stripe," "stripe analytics," or "stripe SQL."
---

# Querying Stripe Synced Data

You are an expert in querying Stripe data that has been synced to PostgreSQL using stripe-sync-engine. Your goal is to help users write efficient queries and integrate with their ORM.

## Schema Overview

All Stripe data is stored in the `stripe` schema. Key tables include:

| Table | Primary Key | Description |
|-------|-------------|-------------|
| `customers` | `id` (cus_...) | Customer records |
| `products` | `id` (prod_...) | Product catalog |
| `prices` | `id` (price_...) | Pricing objects |
| `plans` | `id` (plan_...) | Legacy plan objects |
| `subscriptions` | `id` (sub_...) | Subscription records |
| `subscription_items` | `id` (si_...) | Items in subscriptions |
| `invoices` | `id` (in_...) | Invoice records |
| `invoice_line_items` | `id` (il_...) | Line items on invoices |
| `charges` | `id` (ch_...) | Charge records |
| `payment_intents` | `id` (pi_...) | Payment attempts |
| `payment_methods` | `id` (pm_...) | Saved payment methods |
| `setup_intents` | `id` (seti_...) | Setup intent records |
| `refunds` | `id` (re_...) | Refund records |
| `disputes` | `id` (dp_...) | Dispute records |
| `credit_notes` | `id` (cn_...) | Credit note records |
| `coupons` | `id` | Coupon records |
| `tax_ids` | `id` (txi_...) | Tax ID records |

## Common SQL Queries

### Customer Queries

```sql
-- Get all customers
SELECT * FROM stripe.customers ORDER BY created DESC LIMIT 100;

-- Find customer by email
SELECT * FROM stripe.customers WHERE email = 'user@example.com';

-- Get customers created in the last 30 days
SELECT * FROM stripe.customers
WHERE created > EXTRACT(EPOCH FROM NOW() - INTERVAL '30 days')
ORDER BY created DESC;

-- Count customers by month
SELECT
  DATE_TRUNC('month', to_timestamp(created)) as month,
  COUNT(*) as customer_count
FROM stripe.customers
GROUP BY 1
ORDER BY 1 DESC;
```

### Subscription Queries

```sql
-- Get all active subscriptions
SELECT * FROM stripe.subscriptions WHERE status = 'active';

-- Get subscriptions with customer details
SELECT
  s.id as subscription_id,
  s.status,
  s.current_period_start,
  s.current_period_end,
  c.email,
  c.name
FROM stripe.subscriptions s
JOIN stripe.customers c ON s.customer_id = c.id
WHERE s.status = 'active';

-- Subscriptions expiring in the next 7 days
SELECT * FROM stripe.subscriptions
WHERE status = 'active'
  AND current_period_end < EXTRACT(EPOCH FROM NOW() + INTERVAL '7 days');

-- Count subscriptions by status
SELECT status, COUNT(*) as count
FROM stripe.subscriptions
GROUP BY status
ORDER BY count DESC;
```

### Invoice Queries

```sql
-- Get recent invoices
SELECT * FROM stripe.invoices ORDER BY created DESC LIMIT 50;

-- Get unpaid invoices
SELECT
  i.*,
  c.email,
  c.name
FROM stripe.invoices i
JOIN stripe.customers c ON i.customer_id = c.id
WHERE i.status IN ('open', 'uncollectible')
ORDER BY i.created DESC;

-- Monthly revenue
SELECT
  DATE_TRUNC('month', to_timestamp(created)) as month,
  SUM(amount_paid) / 100.0 as revenue
FROM stripe.invoices
WHERE status = 'paid'
GROUP BY 1
ORDER BY 1 DESC;

-- Invoice totals by customer
SELECT
  c.email,
  c.name,
  COUNT(*) as invoice_count,
  SUM(i.amount_paid) / 100.0 as total_paid
FROM stripe.invoices i
JOIN stripe.customers c ON i.customer_id = c.id
WHERE i.status = 'paid'
GROUP BY c.id, c.email, c.name
ORDER BY total_paid DESC
LIMIT 20;
```

### Payment Queries

```sql
-- Recent successful payments
SELECT * FROM stripe.payment_intents
WHERE status = 'succeeded'
ORDER BY created DESC LIMIT 50;

-- Failed payments
SELECT
  pi.*,
  c.email
FROM stripe.payment_intents pi
LEFT JOIN stripe.customers c ON pi.customer_id = c.id
WHERE pi.status IN ('requires_payment_method', 'canceled')
ORDER BY pi.created DESC;

-- Daily payment volume
SELECT
  DATE(to_timestamp(created)) as date,
  COUNT(*) as payment_count,
  SUM(amount) / 100.0 as volume
FROM stripe.payment_intents
WHERE status = 'succeeded'
GROUP BY 1
ORDER BY 1 DESC;
```

### Product and Price Queries

```sql
-- Get all active products with prices
SELECT
  p.id as product_id,
  p.name,
  p.description,
  pr.id as price_id,
  pr.unit_amount / 100.0 as price,
  pr.currency,
  pr.recurring_interval
FROM stripe.products p
JOIN stripe.prices pr ON pr.product_id = p.id
WHERE p.active = true AND pr.active = true;

-- Products by revenue
SELECT
  p.name,
  SUM(ili.amount) / 100.0 as revenue
FROM stripe.invoice_line_items ili
JOIN stripe.prices pr ON ili.price_id = pr.id
JOIN stripe.products p ON pr.product_id = p.id
JOIN stripe.invoices i ON ili.invoice_id = i.id
WHERE i.status = 'paid'
GROUP BY p.id, p.name
ORDER BY revenue DESC;
```

## Analytics Queries

### MRR (Monthly Recurring Revenue)

```sql
SELECT
  SUM(
    CASE
      WHEN si.price_recurring_interval = 'year'
      THEN si.price_unit_amount / 12.0
      ELSE si.price_unit_amount
    END
  ) / 100.0 as mrr
FROM stripe.subscription_items si
JOIN stripe.subscriptions s ON si.subscription_id = s.id
WHERE s.status = 'active';
```

### Churn Analysis

```sql
-- Subscriptions canceled in last 30 days
SELECT
  s.*,
  c.email,
  to_timestamp(s.canceled_at) as canceled_date
FROM stripe.subscriptions s
JOIN stripe.customers c ON s.customer_id = c.id
WHERE s.status = 'canceled'
  AND s.canceled_at > EXTRACT(EPOCH FROM NOW() - INTERVAL '30 days')
ORDER BY s.canceled_at DESC;

-- Monthly churn rate
WITH monthly_stats AS (
  SELECT
    DATE_TRUNC('month', to_timestamp(created)) as month,
    COUNT(*) as new_subscriptions
  FROM stripe.subscriptions
  GROUP BY 1
),
monthly_cancellations AS (
  SELECT
    DATE_TRUNC('month', to_timestamp(canceled_at)) as month,
    COUNT(*) as cancellations
  FROM stripe.subscriptions
  WHERE canceled_at IS NOT NULL
  GROUP BY 1
)
SELECT
  ms.month,
  ms.new_subscriptions,
  COALESCE(mc.cancellations, 0) as cancellations
FROM monthly_stats ms
LEFT JOIN monthly_cancellations mc ON ms.month = mc.month
ORDER BY ms.month DESC;
```

## ORM Integration

### Drizzle ORM

```typescript
import { sql } from "drizzle-orm";
import { db } from "@/lib/db";

// Custom query
const customers = await db.execute(
  sql`SELECT * FROM stripe.customers WHERE email LIKE ${`%@example.com`}`
);

// With Drizzle schema (if defined)
import { stripeCustomers } from "@/lib/schema";
const customers = await db.select().from(stripeCustomers).limit(10);
```

### Prisma

Add to `schema.prisma`:

```prisma
model StripeCustomer {
  id        String   @id
  email     String?
  name      String?
  created   Int

  @@map("customers")
  @@schema("stripe")
}
```

Then query:

```typescript
const customers = await prisma.stripeCustomer.findMany({
  take: 10,
  orderBy: { created: 'desc' },
});
```

### Kysely

```typescript
import { Kysely, PostgresDialect } from "kysely";

interface StripeDB {
  "stripe.customers": {
    id: string;
    email: string | null;
    name: string | null;
    created: number;
  };
}

const db = new Kysely<StripeDB>({ dialect: new PostgresDialect({ pool }) });

const customers = await db
  .selectFrom("stripe.customers")
  .selectAll()
  .orderBy("created", "desc")
  .limit(10)
  .execute();
```

### Raw pg Client

```typescript
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const result = await pool.query(
  "SELECT * FROM stripe.customers WHERE email = $1",
  ["user@example.com"]
);
const customer = result.rows[0];
```

## Tips

### Timestamps

Stripe stores timestamps as Unix epoch (seconds). Convert to readable dates:

```sql
-- PostgreSQL
SELECT to_timestamp(created) as created_at FROM stripe.customers;

-- With formatting
SELECT to_char(to_timestamp(created), 'YYYY-MM-DD HH24:MI:SS') as created_at
FROM stripe.customers;
```

### JSON Fields

Some columns store JSON data. Query with PostgreSQL JSON operators:

```sql
-- Extract metadata
SELECT metadata->>'key' as value FROM stripe.customers;

-- Filter by metadata
SELECT * FROM stripe.customers
WHERE metadata @> '{"plan": "premium"}'::jsonb;
```

### Indexing

For frequently queried columns, add indexes:

```sql
CREATE INDEX idx_customers_email ON stripe.customers(email);
CREATE INDEX idx_subscriptions_status ON stripe.subscriptions(status);
CREATE INDEX idx_invoices_customer ON stripe.invoices(customer_id);
```

## Related Skills

- **setup**: Configure stripe-sync-engine
- **backfill**: Import historical data to query
- **troubleshooting**: Debug data issues

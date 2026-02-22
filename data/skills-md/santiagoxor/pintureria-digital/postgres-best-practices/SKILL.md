---
name: postgres-best-practices
description: Postgres performance optimization guidelines from Supabase. Contains rules across 8 categories prioritized by impact. Use when writing SQL queries, designing schemas, implementing indexes, optimizing queries, reviewing database performance, configuring connection pooling, or working with Row-Level Security (RLS).
---

# Postgres Best Practices

Postgres performance optimization guidelines from Supabase, prioritized by impact.

## Categories (Priority Order)

### 1. Query Performance (Critical)

- **Use EXPLAIN ANALYZE** to understand query plans
- **Add indexes** on frequently queried columns (WHERE, JOIN, ORDER BY)
- **Avoid SELECT *** - specify only needed columns
- **Use LIMIT** for large result sets
- **Optimize JOINs** - ensure foreign keys are indexed
- **Use prepared statements** (Supabase client does this automatically)
- **Batch operations** when possible

### 2. Connection Management (Critical)

- **Use connection pooling** (Supabase provides this)
- **Close connections** properly
- **Avoid connection leaks** - use connection limits
- **Monitor connection usage** in Supabase dashboard
- **Use server-side clients** for server components
- **Use client-side clients** only in client components

### 3. Schema Design (High)

- **Choose appropriate data types** (UUID vs INTEGER, VARCHAR vs TEXT)
- **Use NOT NULL** constraints where appropriate
- **Add foreign key constraints** for data integrity
- **Use ENUMs** for fixed value sets
- **Normalize appropriately** - balance with query performance
- **Use JSONB** for flexible schema (products, metadata)

### 4. Concurrency & Locking (Medium-High)

- **Use transactions** for atomic operations
- **Keep transactions short** - avoid long-running transactions
- **Use appropriate isolation levels**
- **Avoid deadlocks** - acquire locks in consistent order
- **Use SELECT FOR UPDATE** carefully (can cause blocking)

### 5. Security & RLS (Medium-High)

- **Enable RLS** on all tables
- **Create policies** for tenant isolation in multitenant systems
- **Test RLS policies** thoroughly
- **Use service role** only when necessary (bypasses RLS)
- **Validate inputs** before database operations
- **Use parameterized queries** (Supabase client does this)

### 6. Data Access Patterns (Medium)

- **Use pagination** for large datasets (`.range()` in Supabase)
- **Implement caching** for frequently accessed data
- **Use materialized views** for complex aggregations
- **Consider read replicas** for read-heavy workloads
- **Optimize for common query patterns**

### 7. Monitoring & Diagnostics (Low-Medium)

- **Monitor slow queries** in Supabase dashboard
- **Use pg_stat_statements** for query analysis
- **Set up alerts** for performance degradation
- **Review query logs** regularly
- **Track connection pool usage**

### 8. Advanced Features (Low)

- **Use full-text search** (PostgreSQL tsvector)
- **Consider partitioning** for very large tables
- **Use triggers** judiciously
- **Leverage Postgres extensions** when needed

## Common Patterns

### Index Creation

```sql
-- Single column index
CREATE INDEX idx_products_tenant_id ON products(tenant_id);

-- Composite index (order matters!)
CREATE INDEX idx_products_tenant_category ON products(tenant_id, category_id);

-- Partial index (for filtered queries)
CREATE INDEX idx_products_active ON products(tenant_id) WHERE active = true;

-- Unique index
CREATE UNIQUE INDEX idx_products_sku ON products(tenant_id, sku);
```

### Query Optimization

```typescript
// ❌ Bad: SELECT * and no limit
const { data } = await supabase
  .from('products')
  .select('*');

// ✅ Good: Specific columns with limit
const { data } = await supabase
  .from('products')
  .select('id, name, price, image')
  .eq('tenant_id', tenant.id)
  .eq('active', true)
  .order('created_at', { ascending: false })
  .limit(20);
```

### Pagination

```typescript
// Use range for pagination
const pageSize = 20;
const page = 1;

const { data, error } = await supabase
  .from('products')
  .select('id, name, price')
  .eq('tenant_id', tenant.id)
  .range((page - 1) * pageSize, page * pageSize - 1);
```

### RLS Policy Best Practices

```sql
-- Enable RLS
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Tenant isolation policy
CREATE POLICY "tenant_isolation" ON products
  FOR ALL
  USING (
    tenant_id = (
      SELECT id FROM tenants 
      WHERE slug = current_setting('app.tenant_slug', true)
    )
  );

-- Public read policy (if needed)
CREATE POLICY "public_read_active" ON products
  FOR SELECT
  USING (
    active = true AND
    tenant_id = (
      SELECT id FROM tenants 
      WHERE slug = current_setting('app.tenant_slug', true)
    )
  );
```

### Connection Usage

```typescript
// ✅ Server component - use server client
import { createClient } from '@/lib/supabase/server';

export async function ServerComponent() {
  const supabase = createClient();
  // Use supabase
}

// ✅ Client component - use client
'use client';
import { createClient } from '@/lib/supabase/client';

export function ClientComponent() {
  const supabase = createClient();
  // Use supabase
}
```

## Performance Checklist

- [ ] Queries use indexes on WHERE/JOIN columns
- [ ] SELECT statements specify columns (not *)
- [ ] Large queries use LIMIT or pagination
- [ ] RLS policies are optimized (not too complex)
- [ ] Foreign keys have indexes
- [ ] Transactions are kept short
- [ ] Connection pooling is configured
- [ ] Slow queries are identified and optimized

## Key Files

- `supabase/migrations/` - Schema and indexes
- `src/lib/supabase/` - Client configuration
- Supabase Dashboard - Query performance monitoring

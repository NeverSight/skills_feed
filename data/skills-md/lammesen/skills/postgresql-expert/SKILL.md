---
name: postgresql-expert
description: |
  Expert PostgreSQL database guidance using Bun.sql client. Provides comprehensive patterns
  for queries, schema design, JSON/JSONB operations, full-text search, indexing, PL/pgSQL,
  pgvector, and performance optimization. Use when working with PostgreSQL databases,
  writing SQL queries, optimizing performance, designing schemas, or implementing database
  features. Complements bun-expert skill for Bun.sql integration.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# PostgreSQL Expert Skill

Expert guidance for PostgreSQL development using Bun's native SQL client. This skill provides comprehensive patterns for all PostgreSQL features while integrating seamlessly with Bun.sql.

> **Prerequisite**: This skill works alongside the `bun-expert` skill. For Bun-specific patterns (runtime, bundler, package management), refer to that skill.

## Bun.sql PostgreSQL Integration

### Connection Setup

```typescript
import { sql, SQL } from "bun";

// Environment-based (recommended) - uses POSTGRES_URL, DATABASE_URL, or PG* vars
const db = sql;

// Explicit connection with options
const db = new SQL({
  hostname: "localhost",
  port: 5432,
  database: "myapp",
  username: "dbuser",
  password: "secretpass",

  // Connection pool settings
  max: 20,              // Maximum connections (default: 10)
  idleTimeout: 30,      // Close idle connections after 30s
  maxLifetime: 3600,    // Max connection lifetime in seconds
  connectionTimeout: 30, // Connection timeout

  // SSL/TLS
  tls: true,            // or { rejectUnauthorized: true, ca: "..." }

  // BigInt handling
  bigint: true,         // Return large numbers as BigInt

  // Prepared statements
  prepare: true,        // Enable named prepared statements (default)
});

// Dynamic passwords (AWS RDS IAM, etc.)
const db = new SQL(url, {
  password: async () => await signer.getAuthToken(),
});
```

### Tagged Template Queries

```typescript
// All interpolated values are safely parameterized
const users = await sql`
  SELECT * FROM users
  WHERE status = ${status}
  AND created_at > ${date}
`;

// Object insertion helper
const [user] = await sql`
  INSERT INTO users ${sql({ name, email, role })}
  RETURNING *
`;

// Bulk insert
await sql`INSERT INTO users ${sql(usersArray)}`;

// Pick specific columns
await sql`INSERT INTO users ${sql(userData, "name", "email")}`;

// Dynamic updates
await sql`UPDATE users SET ${sql(updates)} WHERE id = ${id}`;

// WHERE IN queries
await sql`SELECT * FROM users WHERE id IN ${sql([1, 2, 3])}`;

// PostgreSQL arrays
await sql`INSERT INTO tags (items) VALUES (${sql.array(["a", "b", "c"])})`;
await sql`SELECT * FROM products WHERE id = ANY(${sql.array(ids)})`;

// Conditional query fragments
const filter = showActive ? sql`AND active = true` : sql``;
await sql`SELECT * FROM users WHERE 1=1 ${filter}`;
```

### Transactions

```typescript
// Auto-commit/rollback transaction
await sql.begin(async (tx) => {
  const [user] = await tx`INSERT INTO users (name) VALUES (${"Alice"}) RETURNING *`;
  await tx`INSERT INTO accounts (user_id) VALUES (${user.id})`;
  // Auto-commits on success, auto-rollbacks on error
});

// Transaction with options
await sql.begin("read write", async (tx) => {
  // Transaction body
});

// Savepoints (nested transactions)
await sql.begin(async (tx) => {
  await tx`INSERT INTO users (name) VALUES (${"Alice"})`;

  await tx.savepoint(async (sp) => {
    await sp`UPDATE users SET status = 'pending'`;
    if (shouldRollback) throw new Error("Rollback savepoint");
  });

  // Continues even if savepoint rolled back
  await tx`INSERT INTO audit_log (action) VALUES ('user_created')`;
});

// Reserved connections
const reserved = await sql.reserve();
try {
  await reserved`SELECT * FROM locked_table FOR UPDATE`;
} finally {
  reserved.release();
}

// Using Symbol.dispose (auto-release)
{
  using conn = await sql.reserve();
  await conn`SELECT 1`;
} // Auto-released
```

### Error Handling

```typescript
import { SQL } from "bun";

try {
  await sql`INSERT INTO users (email) VALUES (${email})`;
} catch (error) {
  if (error instanceof SQL.PostgresError) {
    switch (error.code) {
      case "23505": // unique_violation
        throw new ConflictError(`Email already exists: ${error.detail}`);
      case "23503": // foreign_key_violation
        throw new NotFoundError(`Referenced record not found`);
      case "23514": // check_violation
        throw new ValidationError(`Check constraint failed: ${error.constraint}`);
      default:
        console.error({
          code: error.code,
          message: error.message,
          detail: error.detail,
          hint: error.hint,
          table: error.table,
          column: error.column,
          constraint: error.constraint,
        });
        throw error;
    }
  }
  throw error;
}
```

### Type Mapping (PostgreSQL ↔ JavaScript)

| PostgreSQL | JavaScript | Notes |
|------------|------------|-------|
| `INTEGER`, `SMALLINT` | `number` | Within safe integer range |
| `BIGINT` | `string` or `BigInt` | `BigInt` if `bigint: true` option |
| `NUMERIC`, `DECIMAL` | `string` | Preserves precision |
| `REAL`, `DOUBLE PRECISION` | `number` | |
| `BOOLEAN` | `boolean` | |
| `TEXT`, `VARCHAR`, `CHAR` | `string` | |
| `DATE`, `TIMESTAMP`, `TIMESTAMPTZ` | `Date` | JavaScript Date object |
| `JSON`, `JSONB` | `object` or `array` | Auto-parsed |
| `BYTEA` | `Buffer` | Binary data |
| `UUID` | `string` | |
| `ARRAY` | `Array` | Automatic conversion |
| `INTERVAL` | `string` | PostgreSQL interval format |

---

## Core SQL Patterns

### SELECT with All Clauses

```sql
-- Full SELECT syntax
SELECT DISTINCT ON (customer_id)
    o.id,
    o.order_date,
    c.name AS customer_name,
    SUM(oi.quantity * oi.price) AS total
FROM orders o
JOIN customers c ON c.id = o.customer_id
LEFT JOIN order_items oi ON oi.order_id = o.id
WHERE o.status = 'completed'
    AND o.order_date >= NOW() - INTERVAL '30 days'
GROUP BY o.id, o.order_date, c.name
HAVING SUM(oi.quantity * oi.price) > 100
ORDER BY customer_id, order_date DESC
LIMIT 10 OFFSET 0
FOR UPDATE SKIP LOCKED;
```

```typescript
// Bun.sql implementation
const orders = await sql`
  SELECT DISTINCT ON (customer_id)
    o.id,
    o.order_date,
    c.name AS customer_name,
    SUM(oi.quantity * oi.price) AS total
  FROM orders o
  JOIN customers c ON c.id = o.customer_id
  LEFT JOIN order_items oi ON oi.order_id = o.id
  WHERE o.status = ${status}
    AND o.order_date >= NOW() - INTERVAL '30 days'
  GROUP BY o.id, o.order_date, c.name
  HAVING SUM(oi.quantity * oi.price) > ${minTotal}
  ORDER BY customer_id, order_date DESC
  LIMIT ${limit} OFFSET ${offset}
`;
```

### UPSERT (INSERT ON CONFLICT)

```typescript
// Upsert single record
const [product] = await sql`
  INSERT INTO products (sku, name, price, quantity)
  VALUES (${sku}, ${name}, ${price}, ${quantity})
  ON CONFLICT (sku) DO UPDATE SET
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    quantity = products.quantity + EXCLUDED.quantity,
    updated_at = NOW()
  RETURNING *
`;

// Bulk upsert
await sql`
  INSERT INTO inventory ${sql(items)}
  ON CONFLICT (product_id, warehouse_id) DO UPDATE SET
    quantity = EXCLUDED.quantity,
    updated_at = NOW()
`;

// Upsert with condition
await sql`
  INSERT INTO prices (product_id, price, effective_date)
  VALUES (${productId}, ${price}, ${date})
  ON CONFLICT (product_id)
  WHERE effective_date < ${date}
  DO UPDATE SET price = EXCLUDED.price, effective_date = EXCLUDED.effective_date
`;
```

### UPDATE with FROM and RETURNING

```typescript
// Update with join
const updated = await sql`
  UPDATE orders o
  SET
    status = 'shipped',
    shipped_at = NOW(),
    shipped_by = ${userId}
  FROM shipments s
  WHERE s.order_id = o.id
    AND s.status = 'ready'
  RETURNING o.id, o.status, o.shipped_at
`;

// Update with subquery
await sql`
  UPDATE employees
  SET salary = (
    SELECT AVG(salary) * 1.1
    FROM employees e2
    WHERE e2.department_id = employees.department_id
  )
  WHERE performance_rating > 4
`;
```

### DELETE with USING

```typescript
// Delete with join
const deleted = await sql`
  DELETE FROM order_items oi
  USING orders o
  WHERE oi.order_id = o.id
    AND o.status = 'cancelled'
    AND o.cancelled_at < NOW() - INTERVAL '90 days'
  RETURNING oi.id, oi.order_id
`;
```

### Common Table Expressions (CTEs)

```typescript
// Basic CTE
const topCustomers = await sql`
  WITH customer_totals AS (
    SELECT
      customer_id,
      SUM(amount) AS total_spent,
      COUNT(*) AS order_count
    FROM orders
    WHERE created_at >= NOW() - INTERVAL '1 year'
    GROUP BY customer_id
  )
  SELECT
    c.name,
    c.email,
    ct.total_spent,
    ct.order_count
  FROM customer_totals ct
  JOIN customers c ON c.id = ct.customer_id
  WHERE ct.total_spent > ${threshold}
  ORDER BY ct.total_spent DESC
`;

// Recursive CTE (hierarchical data)
const orgChart = await sql`
  WITH RECURSIVE org_tree AS (
    -- Base case: root nodes
    SELECT
      id, name, manager_id,
      1 AS level,
      ARRAY[id] AS path,
      name AS full_path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case
    SELECT
      e.id, e.name, e.manager_id,
      t.level + 1,
      t.path || e.id,
      t.full_path || ' > ' || e.name
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
    WHERE NOT e.id = ANY(t.path)  -- Cycle detection
  )
  SELECT * FROM org_tree
  ORDER BY path
`;

// CTE for modifying data
await sql`
  WITH deleted_orders AS (
    DELETE FROM orders
    WHERE status = 'cancelled' AND created_at < NOW() - INTERVAL '1 year'
    RETURNING *
  )
  INSERT INTO archived_orders
  SELECT * FROM deleted_orders
`;
```

### Window Functions

```typescript
// Ranking functions
const rankedProducts = await sql`
  SELECT
    category,
    name,
    price,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS row_num,
    RANK() OVER (PARTITION BY category ORDER BY price DESC) AS rank,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC) AS dense_rank,
    PERCENT_RANK() OVER (PARTITION BY category ORDER BY price DESC) AS pct_rank
  FROM products
  WHERE active = true
`;

// LAG/LEAD for time-series analysis
const salesTrend = await sql`
  SELECT
    date,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY date) AS prev_day,
    LEAD(revenue, 1) OVER (ORDER BY date) AS next_day,
    revenue - LAG(revenue, 1) OVER (ORDER BY date) AS daily_change,
    SUM(revenue) OVER (ORDER BY date) AS running_total,
    AVG(revenue) OVER (
      ORDER BY date
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7day
  FROM daily_sales
  WHERE date >= ${startDate}
`;

// FIRST_VALUE, LAST_VALUE, NTH_VALUE
const categoryStats = await sql`
  SELECT DISTINCT
    category,
    FIRST_VALUE(name) OVER w AS cheapest,
    LAST_VALUE(name) OVER w AS most_expensive,
    NTH_VALUE(name, 2) OVER w AS second_cheapest
  FROM products
  WINDOW w AS (
    PARTITION BY category
    ORDER BY price
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  )
`;
```

### GROUPING SETS, CUBE, ROLLUP

```typescript
// Multi-dimensional aggregation
const salesReport = await sql`
  SELECT
    COALESCE(region, 'All Regions') AS region,
    COALESCE(category, 'All Categories') AS category,
    COALESCE(TO_CHAR(sale_date, 'YYYY-MM'), 'All Months') AS month,
    SUM(amount) AS total_sales,
    COUNT(*) AS transaction_count,
    GROUPING(region, category, sale_date) AS grouping_level
  FROM sales
  WHERE sale_date >= ${startDate}
  GROUP BY CUBE (region, category, DATE_TRUNC('month', sale_date))
  ORDER BY
    GROUPING(region) DESC,
    GROUPING(category) DESC,
    region, category, month
`;

// ROLLUP for hierarchical totals
const hierarchicalReport = await sql`
  SELECT
    year,
    quarter,
    month,
    SUM(revenue) AS total_revenue
  FROM sales
  GROUP BY ROLLUP (year, quarter, month)
  ORDER BY year, quarter, month
`;
```

### Lateral Joins

```typescript
// Get top N items per category
const topPerCategory = await sql`
  SELECT c.name AS category, p.*
  FROM categories c
  CROSS JOIN LATERAL (
    SELECT id, name, price
    FROM products
    WHERE category_id = c.id
    ORDER BY sales_count DESC
    LIMIT 3
  ) p
`;

// Correlated subquery as lateral join
const userActivity = await sql`
  SELECT
    u.id,
    u.name,
    recent.order_count,
    recent.total_spent
  FROM users u
  LEFT JOIN LATERAL (
    SELECT
      COUNT(*) AS order_count,
      COALESCE(SUM(amount), 0) AS total_spent
    FROM orders o
    WHERE o.user_id = u.id
      AND o.created_at > NOW() - INTERVAL '30 days'
  ) recent ON true
  WHERE u.active = true
`;
```

---

## JSON/JSONB Operations

### Extraction and Querying

```typescript
// JSON extraction
const users = await sql`
  SELECT
    id,
    data->>'name' AS name,                    -- Text extraction
    data->'address'->>'city' AS city,         -- Nested text
    data->'address'->'coordinates' AS coords, -- JSON value
    data#>>'{contacts,0,email}' AS primary_email,  -- Path extraction
    data->'tags'->0 AS first_tag              -- Array index
  FROM users
  WHERE data->>'status' = ${status}
`;

// JSONB containment queries (uses GIN index)
const products = await sql`
  SELECT * FROM products
  WHERE metadata @> ${sql({ category: "electronics", inStock: true })}
`;

// Key existence
const withEmail = await sql`
  SELECT * FROM users WHERE data ? 'email'
`;

// Any/all keys exist
const withContact = await sql`
  SELECT * FROM users
  WHERE data ?| ARRAY['email', 'phone']  -- Any of these
`;

const complete = await sql`
  SELECT * FROM users
  WHERE data ?& ARRAY['email', 'phone', 'address']  -- All of these
`;
```

### JSON Path Queries

```typescript
// JSON path existence
const filtered = await sql`
  SELECT * FROM products
  WHERE data @? '$.tags[*] ? (@ == "sale")'
`;

// JSON path query functions
const extracted = await sql`
  SELECT
    id,
    jsonb_path_query_array(data, '$.items[*].price') AS all_prices,
    jsonb_path_query_first(data, '$.items[0].name') AS first_item
  FROM orders
  WHERE jsonb_path_exists(data, '$.items[*] ? (@.quantity > 10)')
`;

// JSON path with variables
const expensiveItems = await sql`
  SELECT jsonb_path_query(
    data,
    '$.items[*] ? (@.price > $min_price)',
    ${sql({ min_price: 100 })}
  ) AS expensive_items
  FROM orders
`;
```

### JSON Modification

```typescript
// Update nested value
await sql`
  UPDATE users
  SET data = jsonb_set(
    data,
    '{address,city}',
    ${sql(JSON.stringify(newCity))}::jsonb
  )
  WHERE id = ${userId}
`;

// Add to array
await sql`
  UPDATE products
  SET data = jsonb_insert(
    data,
    '{tags,0}',
    ${sql(JSON.stringify(newTag))}::jsonb
  )
  WHERE id = ${productId}
`;

// Concatenate/merge objects
await sql`
  UPDATE users
  SET data = data || ${sql({ lastLogin: new Date().toISOString() })}::jsonb
  WHERE id = ${userId}
`;

// Remove key
await sql`
  UPDATE users
  SET data = data - 'temporaryField'
  WHERE data ? 'temporaryField'
`;

// Remove at path
await sql`
  UPDATE users
  SET data = data #- '{address,apartment}'
  WHERE id = ${userId}
`;
```

### JSON Aggregation

```typescript
// Build JSON from query results
const orderWithItems = await sql`
  SELECT
    o.id,
    o.created_at,
    json_build_object(
      'id', c.id,
      'name', c.name,
      'email', c.email
    ) AS customer,
    json_agg(
      json_build_object(
        'product', p.name,
        'quantity', oi.quantity,
        'price', oi.price
      ) ORDER BY p.name
    ) AS items,
    json_object_agg(p.sku, oi.quantity) AS quantities_by_sku
  FROM orders o
  JOIN customers c ON c.id = o.customer_id
  JOIN order_items oi ON oi.order_id = o.id
  JOIN products p ON p.id = oi.product_id
  WHERE o.id = ${orderId}
  GROUP BY o.id, c.id
`;

// Expand JSON to rows
const expandedItems = await sql`
  SELECT
    o.id,
    item->>'name' AS item_name,
    (item->>'price')::numeric AS item_price
  FROM orders o,
  jsonb_array_elements(o.data->'items') AS item
  WHERE o.status = 'pending'
`;

// JSON to record
const structured = await sql`
  SELECT *
  FROM jsonb_to_record(${sql(jsonData)}::jsonb)
  AS x(name text, age int, email text)
`;
```

For complete JSON/JSONB reference, see [references/json-operations.md](references/json-operations.md).

---

## Full-Text Search

### Basic Full-Text Search

```typescript
// Simple search
const results = await sql`
  SELECT
    id,
    title,
    ts_headline('english', body, query, 'StartSel=<mark>, StopSel=</mark>') AS snippet,
    ts_rank(search_vector, query) AS rank
  FROM articles,
    to_tsquery('english', ${searchTerms}) AS query
  WHERE search_vector @@ query
  ORDER BY rank DESC
  LIMIT ${limit}
`;

// Phrase search
const phraseResults = await sql`
  SELECT * FROM articles
  WHERE search_vector @@ phraseto_tsquery('english', ${phrase})
`;

// Web search syntax (supports OR, quotes, -)
const webSearch = await sql`
  SELECT * FROM articles
  WHERE search_vector @@ websearch_to_tsquery('english', ${userQuery})
`;
```

### Weighted Search

```typescript
// Create weighted search vector
await sql`
  UPDATE articles SET search_vector =
    setweight(to_tsvector('english', COALESCE(title, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(subtitle, '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(abstract, '')), 'C') ||
    setweight(to_tsvector('english', COALESCE(body, '')), 'D')
`;

// Search with custom weights
const weighted = await sql`
  SELECT
    id, title,
    ts_rank(search_vector, query, 1) AS rank  -- 1 = normalize by document length
  FROM articles, to_tsquery('english', ${terms}) AS query
  WHERE search_vector @@ query
  ORDER BY rank DESC
`;
```

### Full-Text Search Indexes

```typescript
// GIN index for full-text search
await sql`
  CREATE INDEX articles_search_idx ON articles USING GIN (search_vector)
`;

// Expression-based index
await sql`
  CREATE INDEX articles_title_search_idx
  ON articles
  USING GIN (to_tsvector('english', title))
`;

// Combined with other columns
await sql`
  CREATE INDEX articles_search_idx
  ON articles
  USING GIN (search_vector)
  WHERE status = 'published'
`;
```

### Trigger for Auto-Updating Search Vector

```sql
-- Create trigger function
CREATE OR REPLACE FUNCTION articles_search_vector_update()
RETURNS trigger AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(NEW.subtitle, '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(NEW.body, '')), 'D');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER articles_search_vector_trigger
  BEFORE INSERT OR UPDATE OF title, subtitle, body ON articles
  FOR EACH ROW
  EXECUTE FUNCTION articles_search_vector_update();
```

For complete full-text search guide, see [references/full-text-search.md](references/full-text-search.md).

---

## Indexing Strategies

### Index Type Selection Guide

| Use Case | Index Type | Example |
|----------|------------|---------|
| Equality/range queries | B-tree (default) | `WHERE status = 'active'` |
| Equality only | Hash | `WHERE id = 123` |
| Array containment | GIN | `WHERE tags @> ARRAY['sql']` |
| JSONB queries | GIN | `WHERE data @> '{"key": "value"}'` |
| Full-text search | GIN | `WHERE search_vector @@ query` |
| Geometric/range types | GiST | `WHERE box @> point` |
| Nearest neighbor | GiST | `ORDER BY location <-> point` |
| Large sequential data | BRIN | `WHERE created_at > '2024-01-01'` |
| Fuzzy text matching | GIN + pg_trgm | `WHERE name % 'Jon'` |
| Vector similarity | HNSW/IVFFlat | `ORDER BY embedding <-> vector` |

### Creating Indexes

```typescript
// B-tree (default) - equality and range
await sql`CREATE INDEX orders_customer_id_idx ON orders (customer_id)`;
await sql`CREATE INDEX orders_date_idx ON orders (created_at DESC)`;

// Multi-column index
await sql`CREATE INDEX orders_customer_date_idx ON orders (customer_id, created_at DESC)`;

// Partial index (filtered)
await sql`CREATE INDEX orders_pending_idx ON orders (created_at) WHERE status = 'pending'`;

// Expression index
await sql`CREATE INDEX users_email_lower_idx ON users (LOWER(email))`;

// GIN for arrays
await sql`CREATE INDEX products_tags_idx ON products USING GIN (tags)`;

// GIN for JSONB
await sql`CREATE INDEX users_data_idx ON users USING GIN (data)`;
await sql`CREATE INDEX users_data_path_idx ON users USING GIN (data jsonb_path_ops)`;

// GiST for geometric/range
await sql`CREATE INDEX locations_point_idx ON locations USING GiST (coordinates)`;

// BRIN for large sequential tables
await sql`CREATE INDEX logs_created_idx ON logs USING BRIN (created_at) WITH (pages_per_range = 128)`;

// Covering index (include columns for index-only scans)
await sql`
  CREATE INDEX orders_customer_covering_idx
  ON orders (customer_id)
  INCLUDE (order_date, total_amount)
`;

// Concurrent index creation (no blocking)
await sql`CREATE INDEX CONCURRENTLY users_email_idx ON users (email)`;
```

### Fuzzy Text Matching (pg_trgm)

```typescript
// Enable extension
await sql`CREATE EXTENSION IF NOT EXISTS pg_trgm`;

// Create trigram index
await sql`CREATE INDEX users_name_trgm_idx ON users USING GIN (name gin_trgm_ops)`;

// Similarity search
const similar = await sql`
  SELECT name, similarity(name, ${searchTerm}) AS sim
  FROM users
  WHERE name % ${searchTerm}
  ORDER BY sim DESC
  LIMIT 10
`;

// ILIKE with index support
const matches = await sql`
  SELECT * FROM products
  WHERE name ILIKE ${`%${searchTerm}%`}
`;
```

For complete indexing guide, see [references/indexing-strategies.md](references/indexing-strategies.md).

---

## pgvector - Vector Similarity Search

### Setup

```typescript
await sql`CREATE EXTENSION IF NOT EXISTS vector`;

// Create table with vector column
await sql`
  CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI embedding dimension
    metadata JSONB DEFAULT '{}'
  )
`;
```

### Storing and Querying Vectors

```typescript
// Insert with embedding
await sql`
  INSERT INTO documents (content, embedding, metadata)
  VALUES (
    ${content},
    ${sql.array(embeddingArray)}::vector,
    ${sql({ source: "upload", category })}
  )
`;

// Similarity search (L2 distance)
const similar = await sql`
  SELECT
    id,
    content,
    embedding <-> ${sql.array(queryEmbedding)}::vector AS distance
  FROM documents
  ORDER BY embedding <-> ${sql.array(queryEmbedding)}::vector
  LIMIT ${k}
`;

// Cosine similarity
const cosineSimilar = await sql`
  SELECT
    id,
    content,
    1 - (embedding <=> ${sql.array(queryEmbedding)}::vector) AS similarity
  FROM documents
  ORDER BY embedding <=> ${sql.array(queryEmbedding)}::vector
  LIMIT ${k}
`;

// Inner product (for normalized vectors)
const innerProduct = await sql`
  SELECT id, content
  FROM documents
  ORDER BY embedding <#> ${sql.array(queryEmbedding)}::vector
  LIMIT ${k}
`;

// Filtered similarity search
const filtered = await sql`
  SELECT id, content
  FROM documents
  WHERE metadata @> ${sql({ category: "technical" })}
  ORDER BY embedding <-> ${sql.array(queryEmbedding)}::vector
  LIMIT ${k}
`;
```

### Vector Indexes

```typescript
// HNSW index (better query performance, can build before data)
await sql`
  CREATE INDEX documents_embedding_hnsw_idx
  ON documents
  USING hnsw (embedding vector_l2_ops)
  WITH (m = 16, ef_construction = 64)
`;

// IVFFlat index (build after data loaded)
await sql`
  CREATE INDEX documents_embedding_ivfflat_idx
  ON documents
  USING ivfflat (embedding vector_l2_ops)
  WITH (lists = 100)
`;

// Cosine distance index
await sql`
  CREATE INDEX documents_embedding_cosine_idx
  ON documents
  USING hnsw (embedding vector_cosine_ops)
`;

// Set search parameters for better recall
await sql`SET ivfflat.probes = 10`;
await sql`SET hnsw.ef_search = 100`;
```

For complete pgvector guide, see [references/pgvector-guide.md](references/pgvector-guide.md).

---

## PL/pgSQL Functions and Triggers

### Function Examples

```typescript
// Create function
await sql`
  CREATE OR REPLACE FUNCTION calculate_order_total(order_id INTEGER)
  RETURNS NUMERIC AS $$
  DECLARE
    total NUMERIC := 0;
  BEGIN
    SELECT COALESCE(SUM(quantity * unit_price), 0)
    INTO total
    FROM order_items
    WHERE order_id = calculate_order_total.order_id;

    RETURN total;
  END;
  $$ LANGUAGE plpgsql STABLE;
`;

// Table-returning function
await sql`
  CREATE OR REPLACE FUNCTION get_customer_orders(
    p_customer_id INTEGER,
    p_limit INTEGER DEFAULT 10
  )
  RETURNS TABLE(
    order_id INTEGER,
    order_date TIMESTAMP,
    total NUMERIC,
    item_count BIGINT
  ) AS $$
  BEGIN
    RETURN QUERY
    SELECT
      o.id,
      o.created_at,
      SUM(oi.quantity * oi.unit_price),
      COUNT(oi.id)
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.id
    WHERE o.customer_id = p_customer_id
    GROUP BY o.id
    ORDER BY o.created_at DESC
    LIMIT p_limit;
  END;
  $$ LANGUAGE plpgsql STABLE;
`;

// Call from Bun.sql
const orders = await sql`SELECT * FROM get_customer_orders(${customerId}, ${10})`;
```

### Trigger Examples

```typescript
// Audit trigger
await sql`
  CREATE OR REPLACE FUNCTION audit_trigger_func()
  RETURNS TRIGGER AS $$
  BEGIN
    IF TG_OP = 'DELETE' THEN
      INSERT INTO audit_log (table_name, operation, old_data, changed_by, changed_at)
      VALUES (TG_TABLE_NAME, 'D', row_to_json(OLD), current_user, NOW());
      RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
      INSERT INTO audit_log (table_name, operation, old_data, new_data, changed_by, changed_at)
      VALUES (TG_TABLE_NAME, 'U', row_to_json(OLD), row_to_json(NEW), current_user, NOW());
      RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
      INSERT INTO audit_log (table_name, operation, new_data, changed_by, changed_at)
      VALUES (TG_TABLE_NAME, 'I', row_to_json(NEW), current_user, NOW());
      RETURN NEW;
    END IF;
    RETURN NULL;
  END;
  $$ LANGUAGE plpgsql;
`;

// Auto-update timestamps trigger
await sql`
  CREATE OR REPLACE FUNCTION update_timestamps()
  RETURNS TRIGGER AS $$
  BEGIN
    NEW.updated_at := NOW();
    IF TG_OP = 'INSERT' THEN
      NEW.created_at := NOW();
    END IF;
    RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;

  CREATE TRIGGER set_timestamps
    BEFORE INSERT OR UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamps();
`;

// Validation trigger
await sql`
  CREATE OR REPLACE FUNCTION validate_order()
  RETURNS TRIGGER AS $$
  BEGIN
    IF NEW.quantity <= 0 THEN
      RAISE EXCEPTION 'Quantity must be positive';
    END IF;
    IF NEW.unit_price < 0 THEN
      RAISE EXCEPTION 'Price cannot be negative';
    END IF;
    RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;
`;
```

For complete PL/pgSQL reference, see [references/plpgsql-reference.md](references/plpgsql-reference.md).

---

## Performance Optimization

### EXPLAIN ANALYZE

```typescript
// Get execution plan with actual timing
const plan = await sql`
  EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
  SELECT * FROM orders o
  JOIN customers c ON c.id = o.customer_id
  WHERE o.created_at > NOW() - INTERVAL '30 days'
`;

// Interpretation guide in the result
console.log("Key metrics to analyze:");
console.log("- Seq Scan on large tables (consider indexes)");
console.log("- High actual rows vs estimated rows (run ANALYZE)");
console.log("- Buffers read >> hit (I/O bottleneck)");
console.log("- Nested Loop with high rows (consider Hash/Merge Join)");
```

### Query Optimization Patterns

```typescript
// Use EXISTS instead of IN for large subqueries
// Bad:
await sql`SELECT * FROM orders WHERE customer_id IN (SELECT id FROM customers WHERE active)`;
// Good:
await sql`SELECT * FROM orders o WHERE EXISTS (SELECT 1 FROM customers c WHERE c.id = o.customer_id AND c.active)`;

// Use LIMIT early in CTEs when possible
await sql`
  WITH recent_orders AS (
    SELECT * FROM orders
    WHERE created_at > NOW() - INTERVAL '1 day'
    LIMIT 1000  -- Early limit
  )
  SELECT * FROM recent_orders WHERE status = 'pending'
`;

// Batch operations for better performance
await sql.begin(async (tx) => {
  // Process in batches
  for (let i = 0; i < items.length; i += 1000) {
    const batch = items.slice(i, i + 1000);
    await tx`INSERT INTO products ${tx(batch)}`;
  }
});
```

### Statistics and Maintenance

```typescript
// Update statistics
await sql`ANALYZE orders`;
await sql`ANALYZE VERBOSE orders`;

// Vacuum table
await sql`VACUUM orders`;
await sql`VACUUM (ANALYZE, VERBOSE) orders`;

// Check table bloat
const bloatCheck = await sql`
  SELECT
    relname,
    n_live_tup,
    n_dead_tup,
    round(n_dead_tup::numeric / NULLIF(n_live_tup, 0) * 100, 2) AS dead_pct,
    last_vacuum,
    last_autovacuum
  FROM pg_stat_user_tables
  ORDER BY n_dead_tup DESC
  LIMIT 10
`;

// Check index usage
const indexUsage = await sql`
  SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
  FROM pg_stat_user_indexes
  ORDER BY idx_scan
  LIMIT 20
`;
```

For complete performance guide, see [references/performance-optimization.md](references/performance-optimization.md).

---

## Row-Level Security (RLS)

```typescript
// Enable RLS
await sql`ALTER TABLE documents ENABLE ROW LEVEL SECURITY`;

// Create policies
await sql`
  CREATE POLICY documents_owner_policy ON documents
    FOR ALL
    USING (owner_id = current_setting('app.current_user_id')::INTEGER)
    WITH CHECK (owner_id = current_setting('app.current_user_id')::INTEGER)
`;

// Set user context before queries
await sql`SET app.current_user_id = ${userId}`;
const userDocs = await sql`SELECT * FROM documents`; // Only sees owned docs

// Create tenant isolation policy
await sql`
  CREATE POLICY tenant_isolation ON data
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id')::UUID)
`;

// Admin bypass policy
await sql`
  CREATE POLICY admin_all_access ON documents
    FOR ALL
    TO admin_role
    USING (true)
`;
```

For complete security patterns, see [references/security-patterns.md](references/security-patterns.md).

---

## Migration Patterns

### Migration Template

```typescript
// migrations/001_initial_schema.ts
import { sql } from "bun";

export async function up() {
  await sql.begin(async (tx) => {
    await tx`
      CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
      )
    `;

    await tx`CREATE INDEX users_email_idx ON users (email)`;

    await tx`
      INSERT INTO schema_migrations (version, applied_at)
      VALUES ('001_initial_schema', NOW())
    `;
  });
}

export async function down() {
  await sql.begin(async (tx) => {
    await tx`DROP TABLE IF EXISTS users CASCADE`;
    await tx`DELETE FROM schema_migrations WHERE version = '001_initial_schema'`;
  });
}
```

### Migration Runner

```typescript
// migrate.ts
import { sql } from "bun";

async function migrate() {
  // Create migrations table if not exists
  await sql`
    CREATE TABLE IF NOT EXISTS schema_migrations (
      version VARCHAR(255) PRIMARY KEY,
      applied_at TIMESTAMPTZ DEFAULT NOW()
    )
  `;

  // Get applied migrations
  const applied = await sql`SELECT version FROM schema_migrations`;
  const appliedVersions = new Set(applied.map(r => r.version));

  // Get pending migrations
  const glob = new Bun.Glob("./migrations/*.ts");
  const files = Array.from(glob.scanSync(".")).sort();

  for (const file of files) {
    const version = file.match(/(\d+_[a-z_]+)/)?.[1];
    if (version && !appliedVersions.has(version)) {
      console.log(`Applying migration: ${version}`);
      const migration = await import(`./${file}`);
      await migration.up();
      console.log(`Applied: ${version}`);
    }
  }
}
```

---

## Testing Patterns

```typescript
// test/db.test.ts
import { describe, test, expect, beforeAll, afterAll, beforeEach } from "bun:test";
import { SQL } from "bun";

const testDb = new SQL({
  database: "myapp_test",
  // ... other config
});

describe("User Repository", () => {
  beforeAll(async () => {
    // Run migrations
    await testDb`CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      email VARCHAR(255) UNIQUE,
      name VARCHAR(255)
    )`;
  });

  beforeEach(async () => {
    // Clean up before each test
    await testDb`TRUNCATE users RESTART IDENTITY CASCADE`;
  });

  afterAll(async () => {
    await testDb.close();
  });

  test("creates a user", async () => {
    const [user] = await testDb`
      INSERT INTO users (email, name)
      VALUES ('test@example.com', 'Test User')
      RETURNING *
    `;

    expect(user.id).toBe(1);
    expect(user.email).toBe("test@example.com");
  });

  test("enforces unique email", async () => {
    await testDb`INSERT INTO users (email, name) VALUES ('test@example.com', 'User 1')`;

    expect(async () => {
      await testDb`INSERT INTO users (email, name) VALUES ('test@example.com', 'User 2')`;
    }).toThrow();
  });

  test("transactions rollback on error", async () => {
    try {
      await testDb.begin(async (tx) => {
        await tx`INSERT INTO users (email, name) VALUES ('a@example.com', 'A')`;
        throw new Error("Intentional rollback");
      });
    } catch {}

    const [{ count }] = await testDb`SELECT COUNT(*) FROM users`;
    expect(count).toBe("0");
  });
});
```

---

## Common Anti-Patterns to Avoid

1. **N+1 Queries**: Use JOINs or batch queries instead of loops
2. **SELECT ***: Only select needed columns, especially with JSONB
3. **Missing indexes on foreign keys**: Always index FK columns
4. **OFFSET pagination on large tables**: Use keyset/cursor pagination
5. **Not using prepared statements**: Bun.sql handles this automatically
6. **Ignoring EXPLAIN output**: Always analyze slow queries
7. **Large transactions**: Keep transactions short to avoid lock contention
8. **Not vacuuming**: Ensure autovacuum is enabled and tuned

---

## Quick Reference

### Essential PostgreSQL Error Codes

| Code | Name | Description |
|------|------|-------------|
| 23505 | unique_violation | Duplicate key value |
| 23503 | foreign_key_violation | FK constraint failed |
| 23502 | not_null_violation | NULL in non-null column |
| 23514 | check_violation | Check constraint failed |
| 42P01 | undefined_table | Table doesn't exist |
| 42703 | undefined_column | Column doesn't exist |
| 57014 | query_canceled | Query was cancelled |
| 40001 | serialization_failure | Transaction conflict |
| 40P01 | deadlock_detected | Deadlock occurred |

### Connection Environment Variables

| Variable | Description |
|----------|-------------|
| `POSTGRES_URL` | Primary connection URL |
| `DATABASE_URL` | Alternative URL |
| `PGHOST` | Database host |
| `PGPORT` | Database port (default: 5432) |
| `PGUSER` | Database user |
| `PGPASSWORD` | Database password |
| `PGDATABASE` | Database name |
| `PGSSLMODE` | SSL mode (disable/prefer/require/verify-full) |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [references/sql-patterns.md](references/sql-patterns.md) | Complete SQL syntax reference |
| [references/json-operations.md](references/json-operations.md) | JSONB operators and functions |
| [references/full-text-search.md](references/full-text-search.md) | FTS configuration guide |
| [references/indexing-strategies.md](references/indexing-strategies.md) | Index selection guide |
| [references/plpgsql-reference.md](references/plpgsql-reference.md) | PL/pgSQL complete reference |
| [references/pgvector-guide.md](references/pgvector-guide.md) | Vector search patterns |
| [references/performance-optimization.md](references/performance-optimization.md) | Query tuning guide |
| [references/security-patterns.md](references/security-patterns.md) | RLS and permissions |

---

## Sub-Agents

| Agent | Use When |
|-------|----------|
| **pg-query** | Writing complex SQL queries, CTEs, window functions, JSON operations |
| **pg-schema** | Designing schemas, creating tables, defining constraints, planning migrations |
| **pg-performance** | Optimizing slow queries, analyzing EXPLAIN output, tuning configuration |

---

## When This Skill Activates

This skill automatically activates when:
- Working with `Bun.sql` or PostgreSQL
- Writing SQL queries or designing schemas
- Implementing full-text search
- Working with JSON/JSONB data
- Using pgvector for similarity search
- Writing PL/pgSQL functions or triggers
- Optimizing database performance
- Implementing Row-Level Security

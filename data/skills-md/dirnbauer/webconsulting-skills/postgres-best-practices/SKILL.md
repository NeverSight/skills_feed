---
name: postgres-best-practices
description: Postgres performance optimization and best practices from Supabase. Query performance, connection pooling, Row Level Security, schema design, and diagnostics.
version: 1.0.0
triggers:
  - postgres
  - postgresql
  - sql
  - database
  - query
  - index
  - rls
  - row-level-security
  - supabase
  - connection-pooling
---

# Postgres Best Practices

> **Source:** This skill is based on [Supabase's Postgres Best Practices](https://github.com/supabase/agent-skills) 
> for AI agents. See the [announcement blog post](https://supabase.com/blog/postgres-best-practices-for-ai-agents).

Comprehensive Postgres performance optimization guide. Contains rules across 8 categories, 
prioritized by impact from critical (query performance, connection management) to incremental 
(advanced features).

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category | Impact | 
|----------|----------|--------|
| 1 | Query Performance | CRITICAL |
| 2 | Connection Management | CRITICAL |
| 3 | Security & RLS | CRITICAL |
| 4 | Schema Design | HIGH |
| 5 | Concurrency & Locking | MEDIUM-HIGH |
| 6 | Data Access Patterns | MEDIUM |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM |
| 8 | Advanced Features | LOW |

---

## 1. Query Performance (CRITICAL)

Slow queries, missing indexes, inefficient query plans. The most common source of Postgres performance issues.

### 1.1 Add Indexes on WHERE and JOIN Columns

**Impact: CRITICAL (100-1000x faster queries on large tables)**

Queries filtering or joining on unindexed columns cause full table scans.

**Incorrect (sequential scan on large table):**

```sql
-- No index on customer_id causes full table scan
select * from orders where customer_id = 123;

-- EXPLAIN shows: Seq Scan on orders (cost=0.00..25000.00 rows=100 width=85)
```

**Correct (index scan):**

```sql
-- Create index on frequently filtered column
create index orders_customer_id_idx on orders (customer_id);

select * from orders where customer_id = 123;

-- EXPLAIN shows: Index Scan using orders_customer_id_idx (cost=0.42..8.44 rows=100 width=85)
```

For JOIN columns, always index the foreign key side:

```sql
create index orders_customer_id_idx on orders (customer_id);

select c.name, o.total
from customers c
join orders o on o.customer_id = c.id;
```

### 1.2 Choose the Right Index Type

**Impact: HIGH (10-100x improvement with correct index type)**

| Index Type | Use Case | Operators |
|------------|----------|-----------|
| B-tree (default) | Equality, range queries | `=`, `<`, `>`, `BETWEEN`, `IN`, `IS NULL` |
| GIN | Arrays, JSONB, full-text | `@>`, `?`, `?&`, `?\|`, `@@` |
| BRIN | Large time-series tables | Range queries (10-100x smaller) |
| Hash | Equality-only | `=` (slightly faster than B-tree) |

**Incorrect (B-tree for JSONB containment):**

```sql
-- B-tree cannot optimize containment operators
create index products_attrs_idx on products (attributes);
select * from products where attributes @> '{"color": "red"}';
-- Full table scan - B-tree doesn't support @> operator
```

**Correct (GIN for JSONB):**

```sql
-- GIN supports @>, ?, ?&, ?| operators
create index products_attrs_idx on products using gin (attributes);
select * from products where attributes @> '{"color": "red"}';
```

### 1.3 Create Composite Indexes for Multi-Column Queries

**Impact: HIGH (5-10x faster multi-column queries)**

**Column order matters** - place equality columns first, range columns last:

```sql
-- Good: status (=) before created_at (>)
create index orders_status_created_idx on orders (status, created_at);

-- Works for: WHERE status = 'pending'
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
-- Does NOT work for: WHERE created_at > '2024-01-01' (leftmost prefix rule)
```

### 1.4 Use Covering Indexes to Avoid Table Lookups

**Impact: MEDIUM-HIGH (2-5x faster queries by eliminating heap fetches)**

```sql
-- Include non-searchable columns in the index
create index users_email_idx on users (email) include (name, created_at);

-- All columns served from index, no table access needed
select email, name, created_at from users where email = 'user@example.com';
```

### 1.5 Use Partial Indexes for Filtered Queries

**Impact: HIGH (5-20x smaller indexes, faster writes and queries)**

```sql
-- Index only includes active users
create index users_active_email_idx on users (email)
where deleted_at is null;

-- Only pending orders (status rarely changes once completed)
create index orders_pending_idx on orders (created_at)
where status = 'pending';
```

---

## 2. Connection Management (CRITICAL)

### 2.1 Use Connection Pooling

**Impact: CRITICAL (Handle 10-100x more concurrent users)**

Postgres connections are expensive (1-3MB RAM each). Use a pooler like PgBouncer.

```sql
-- Without pooling: 500 concurrent users = 500 connections = crashed database
-- With pooling: 500 concurrent users share 10 actual connections
```

Pool modes:
- **Transaction mode**: Connection returned after each transaction (best for most apps)
- **Session mode**: Connection held for entire session (needed for prepared statements, temp tables)

### 2.2 Configure Connection Limits

**Impact: CRITICAL (Prevent database crashes and memory exhaustion)**

```sql
-- Formula: max_connections = (RAM in MB / 5MB per connection) - reserved
-- For 4GB RAM: (4096 / 5) - 10 = ~800 theoretical max
-- Practically, 100-200 is better for query performance

alter system set max_connections = 100;

-- work_mem * max_connections should not exceed 25% of RAM
alter system set work_mem = '8MB';  -- 8MB * 100 = 800MB max
```

### 2.3 Configure Idle Connection Timeouts

```sql
-- Terminate connections idle in transaction after 30 seconds
alter system set idle_in_transaction_session_timeout = '30s';

-- Terminate completely idle connections after 10 minutes
alter system set idle_session_timeout = '10min';

select pg_reload_conf();
```

---

## 3. Security & RLS (CRITICAL)

### 3.1 Enable Row Level Security for Multi-Tenant Data

**Impact: CRITICAL (Database-enforced tenant isolation, prevent data leaks)**

**Incorrect (application-level filtering only):**

```sql
-- Relying only on application to filter
select * from orders where user_id = $current_user_id;

-- Bug or bypass means all data is exposed!
select * from orders;  -- Returns ALL orders
```

**Correct (database-enforced RLS):**

```sql
-- Enable RLS on the table
alter table orders enable row level security;

-- Create policy for users to see only their orders
create policy orders_user_policy on orders
  for all
  using (user_id = current_setting('app.current_user_id')::bigint);

-- Force RLS even for table owners
alter table orders force row level security;

-- Set user context and query
set app.current_user_id = '123';
select * from orders;  -- Only returns orders for user 123
```

**Supabase pattern with auth.uid():**

```sql
create policy orders_user_policy on orders
  for all
  to authenticated
  using (user_id = auth.uid());
```

### 3.2 Optimize RLS Policies for Performance

**Impact: HIGH (5-10x faster RLS queries with proper patterns)**

**Incorrect (function called for every row):**

```sql
create policy orders_policy on orders
  using (auth.uid() = user_id);  -- auth.uid() called per row!
```

**Correct (wrap functions in SELECT for caching):**

```sql
create policy orders_policy on orders
  using ((select auth.uid()) = user_id);  -- Called once, cached

-- 100x+ faster on large tables
```

Always add indexes on columns used in RLS policies:

```sql
create index orders_user_id_idx on orders (user_id);
```

### 3.3 Apply Principle of Least Privilege

```sql
-- Create role with no default privileges
create role app_readonly nologin;

-- Grant only SELECT on specific tables
grant usage on schema public to app_readonly;
grant select on public.products, public.categories to app_readonly;

-- Create role for writes with limited scope
create role app_writer nologin;
grant select, insert, update on public.orders to app_writer;
grant usage on sequence orders_id_seq to app_writer;
-- No DELETE permission
```

---

## 4. Schema Design (HIGH)

### 4.1 Choose Appropriate Data Types

| Use Case | Correct Type | Avoid |
|----------|--------------|-------|
| IDs | `bigint` | `int` (overflows at 2.1B) |
| Strings | `text` | `varchar(n)` unless constraint needed |
| Timestamps | `timestamptz` | `timestamp` (no timezone) |
| Money | `numeric(10,2)` | `float` (precision issues) |
| Boolean | `boolean` | `varchar(5)` |

```sql
create table users (
  id bigint generated always as identity primary key,
  email text,
  created_at timestamptz default now(),
  is_active boolean default true,
  price numeric(10,2)
);
```

### 4.2 Index Foreign Key Columns

**Impact: HIGH (10-100x faster JOINs and CASCADE operations)**

Postgres does NOT automatically index foreign key columns!

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- Always index the FK column
create index orders_customer_id_idx on orders (customer_id);
```

Find missing FK indexes:

```sql
select
  conrelid::regclass as table_name,
  a.attname as fk_column
from pg_constraint c
join pg_attribute a on a.attrelid = c.conrelid and a.attnum = any(c.conkey)
where c.contype = 'f'
  and not exists (
    select 1 from pg_index i
    where i.indrelid = c.conrelid and a.attnum = any(i.indkey)
  );
```

### 4.3 Partition Large Tables

**Impact: MEDIUM-HIGH (5-20x faster queries and maintenance on large tables)**

When to partition: Tables > 100M rows, time-series data, need to efficiently drop old data.

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz not null,
  data jsonb
) partition by range (created_at);

-- Create partitions for each month
create table events_2024_01 partition of events
  for values from ('2024-01-01') to ('2024-02-01');

-- Drop old data instantly
drop table events_2023_01;  -- Instant vs DELETE taking hours
```

### 4.4 Select Optimal Primary Key Strategy

```sql
-- Use IDENTITY for sequential IDs (SQL-standard, best for most cases)
create table users (
  id bigint generated always as identity primary key
);

-- For distributed systems needing UUIDs, use UUIDv7 (time-ordered)
-- Requires pg_uuidv7 extension
create table orders (
  id uuid default uuid_generate_v7() primary key
);
```

Guidelines:
- Single database: `bigint identity` (sequential, 8 bytes)
- Distributed/exposed IDs: UUIDv7 (time-ordered, no fragmentation)
- Avoid random UUIDs (v4) as primary keys on large tables (causes index fragmentation)

### 4.5 Use Lowercase Identifiers

```sql
-- Correct: unquoted lowercase identifiers are portable
create table users (
  user_id bigint primary key,
  first_name text,
  last_name text
);

-- Works without quotes, recognized by all tools
select first_name from users where user_id = 1;
```

---

## 5. Concurrency & Locking (MEDIUM-HIGH)

### 5.1 Keep Transactions Short

**Impact: MEDIUM-HIGH (3-5x throughput improvement, fewer deadlocks)**

**Incorrect:**

```sql
begin;
select * from orders where id = 1 for update;  -- Lock acquired
-- Application makes HTTP call to payment API (2-5 seconds)
-- Other queries on this row are blocked!
update orders set status = 'paid' where id = 1;
commit;
```

**Correct:**

```sql
-- Validate and call APIs outside transaction
-- Only hold lock for the actual update
begin;
update orders
set status = 'paid', payment_id = $1
where id = $2 and status = 'pending'
returning *;
commit;  -- Lock held for milliseconds
```

### 5.2 Prevent Deadlocks with Consistent Lock Ordering

```sql
-- Explicitly acquire locks in ID order before updating
begin;
select * from accounts where id in (1, 2) order by id for update;

-- Now perform updates in any order
update accounts set balance = balance - 100 where id = 1;
update accounts set balance = balance + 100 where id = 2;
commit;
```

### 5.3 Use SKIP LOCKED for Queue Processing

**Impact: MEDIUM-HIGH (10x throughput for worker queues)**

```sql
-- Each worker skips locked rows and gets the next available
begin;
select * from jobs
where status = 'pending'
order by created_at
limit 1
for update skip locked;

update jobs set status = 'processing' where id = $1;
commit;
```

Complete queue pattern (atomic claim-and-update):

```sql
update jobs
set status = 'processing', worker_id = $1, started_at = now()
where id = (
  select id from jobs
  where status = 'pending'
  order by created_at
  limit 1
  for update skip locked
)
returning *;
```

---

## 6. Data Access Patterns (MEDIUM)

### 6.1 Batch INSERT Statements

**Impact: MEDIUM (10-50x faster bulk inserts)**

```sql
-- Multiple rows in single statement
insert into events (user_id, action) values
  (1, 'click'),
  (1, 'view'),
  (2, 'click');

-- For large imports, use COPY
copy events (user_id, action, created_at)
from '/path/to/data.csv'
with (format csv, header true);
```

### 6.2 Eliminate N+1 Queries

**Impact: MEDIUM-HIGH (10-100x fewer database round trips)**

**Incorrect:**

```sql
-- 101 round trips
select id from users where active = true;  -- Returns 100 IDs
select * from orders where user_id = 1;
select * from orders where user_id = 2;
-- ... 98 more queries
```

**Correct:**

```sql
-- 1 round trip
select * from orders where user_id = any(array[1, 2, 3, ...]);

-- Or use JOIN
select u.id, u.name, o.*
from users u
left join orders o on o.user_id = u.id
where u.active = true;
```

### 6.3 Use Cursor-Based Pagination

**Impact: MEDIUM-HIGH (Consistent O(1) performance regardless of page depth)**

**Incorrect (OFFSET):**

```sql
-- Page 10000: scans 200,000 rows!
select * from products order by id limit 20 offset 199980;
```

**Correct (cursor/keyset):**

```sql
-- Page 10000: same speed as page 1
select * from products where id > 199980 order by id limit 20;
```

For multi-column sorting:

```sql
select * from products
where (created_at, id) > ('2024-01-15 10:00:00', 12345)
order by created_at, id
limit 20;
```

### 6.4 Use UPSERT for Insert-or-Update

```sql
-- Atomic operation, eliminates race conditions
insert into settings (user_id, key, value)
values (123, 'theme', 'dark')
on conflict (user_id, key)
do update set value = excluded.value, updated_at = now()
returning *;
```

---

## 7. Monitoring & Diagnostics (LOW-MEDIUM)

### 7.1 Enable pg_stat_statements

```sql
create extension if not exists pg_stat_statements;

-- Find slowest queries by total time
select
  calls,
  round(total_exec_time::numeric, 2) as total_time_ms,
  round(mean_exec_time::numeric, 2) as mean_time_ms,
  query
from pg_stat_statements
order by total_exec_time desc
limit 10;
```

### 7.2 Use EXPLAIN ANALYZE

```sql
explain (analyze, buffers, format text)
select * from orders where customer_id = 123 and status = 'pending';

-- Key things to look for:
-- Seq Scan on large tables = missing index
-- Rows Removed by Filter = poor selectivity or missing index
-- Buffers: read >> hit = data not cached
-- Nested Loop with high loops = consider different join strategy
```

### 7.3 Maintain Table Statistics

```sql
-- Manually analyze after large data changes
analyze orders;

-- Autovacuum tuning for busy tables
alter table orders set (
  autovacuum_vacuum_scale_factor = 0.05,
  autovacuum_analyze_scale_factor = 0.02
);
```

---

## 8. Advanced Features (LOW)

### 8.1 Index JSONB Columns

```sql
-- GIN for containment queries
create index products_attrs_gin on products using gin (attributes);

-- Expression index for specific key lookups
create index products_brand_idx on products ((attributes->>'brand'));
```

### 8.2 Use tsvector for Full-Text Search

**Impact: MEDIUM (100x faster than LIKE, with ranking support)**

```sql
-- Add tsvector column and index
alter table articles add column search_vector tsvector
  generated always as (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,''))) stored;

create index articles_search_idx on articles using gin (search_vector);

-- Fast full-text search with ranking
select *, ts_rank(search_vector, query) as rank
from articles, to_tsquery('english', 'postgresql') query
where search_vector @@ query
order by rank desc;
```

---

## Quick Reference: Common Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Slow queries on large tables | Missing index | Add B-tree index on WHERE/JOIN columns |
| JSONB queries slow | Wrong index type | Use GIN index |
| Connection errors under load | No pooling | Use PgBouncer in transaction mode |
| Memory exhaustion | Too many connections | Reduce max_connections, add pooler |
| Multi-tenant data leak | No RLS | Enable RLS with proper policies |
| RLS queries slow | Function per-row | Wrap in `(select ...)` for caching |
| Slow pagination on deep pages | Using OFFSET | Use cursor-based pagination |
| INSERT bottleneck | Single-row inserts | Batch INSERTs or use COPY |
| N+1 queries | Loop in application | Use ANY() or JOIN |
| Deadlocks | Inconsistent lock order | Lock in consistent order (by ID) |

---

## Credits & Attribution

This skill is adapted from the excellent Postgres best practices developed by
**[Supabase](https://supabase.com/)**.

Original repository: https://github.com/supabase/agent-skills

**Copyright (c) Supabase** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection

---
name: postgresql
description: "PostgreSQL best practices: multi-tenancy with RLS, schema design, Alembic migrations, async SQLAlchemy, and query optimization."
version: "18.1"
release_date: "2025-11-13"
---

# PostgreSQL

## When to use

- Designing or changing multi-tenant tables with Row-Level Security (RLS)
- Debugging tenant isolation issues
- Adding/changing Alembic migrations for schema, RLS policies, or indexes
- Writing tests that validate RLS isolation
- Configuring PostgreSQL authentication, replication, or tuning

## RLS Multi-tenancy Pattern

### Non-negotiables

- **RLS context is mandatory** for any tenant-scoped query
- **Context must be set inside the same transaction** as the queries
- **No fallbacks** for tenant ID (fail fast if missing)
- **Async-only** DB access when using async frameworks

### Setting RLS Context

RLS works only if the current transaction has the context set:

```sql
SET LOCAL app.current_tenant_id = '<tenant_uuid>';
```

Must run before the first tenant-scoped query in that transaction.

### Common Failure Modes

- Setting `SET LOCAL ...` after the first `select()`
- Setting the context in one session, then querying in another
- Running queries outside the expected transaction scope

### Typical RLS Policy

```sql
ALTER TABLE some_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY some_table_tenant_isolation
ON some_table
USING (tenant_id = current_setting('app.current_tenant_id', true)::uuid);
```

## Multi-tenant Table Checklist

- Tenant ID column is **UUID**
- FK to tenants table with `ON DELETE CASCADE`
- Indexes aligned with access patterns (usually tenant_id first)
  - PostgreSQL does **not** auto-index FK columns — add explicit indexes
  - UNIQUE allows multiple NULLs unless using `NULLS NOT DISTINCT` (PG15+)
- RLS is enabled and policies exist
- Application code sets RLS context at transaction start

## Alembic Migrations Checklist

1. Add/modify schema (columns, constraints, FKs)
2. Create/update indexes
3. Enable RLS and create/adjust policies
4. Add verification (tests) for isolation
5. Provide a real downgrade (no stubs)

## RLS Isolation Testing Recipe

Goal:

- Data for tenant A is visible to tenant A
- Data for tenant A is NOT visible to tenant B

Canonical flow:

1. Setup data through an **admin session** (RLS bypass) for tenant A and B
2. Assert via an **RLS session**:
   - set context to tenant A → sees only tenant A data
   - set context to tenant B → does not see tenant A data

## Destructive Operations Safety

Hard rules:

- Never run `DELETE` without a narrow `WHERE` targeting specific data
- Never run `TRUNCATE`/`DROP` without explicit confirmation

Pre-flight before destructive actions:

1. Confirm exact target (tables / IDs / date range)
2. Run a `SELECT`/row count first and show results
3. Ask for final confirmation, then execute

## References

### Schema & Design

- [table-design.md](references/table-design.md) — Data types, constraints, indexing, partitioning, JSONB, safe schema evolution
- [charset-encoding.md](references/charset-encoding.md) — Character sets, encoding, collation, ICU, locale settings

### Authentication

- [authentication.md](references/authentication.md) — pg_hba.conf, SCRAM-SHA-256, md5, peer, cert, LDAP, GSSAPI
- [authentication-oauth.md](references/authentication-oauth.md) — OAuth 2.0 (PostgreSQL 18+), SASL OAUTHBEARER, validators
- [user-management.md](references/user-management.md) — CREATE/ALTER/DROP ROLE, membership, GRANT/REVOKE, predefined roles

### Runtime Configuration

- [connection-settings.md](references/connection-settings.md) — listen_addresses, max_connections, SSL, TCP keepalives
- [query-tuning.md](references/query-tuning.md) — Planner settings, work_mem, parallel query, cost constants
- [replication.md](references/replication.md) — Streaming replication, WAL, synchronous commit, logical replication
- [vacuum.md](references/vacuum.md) — Autovacuum, vacuum cost model, freeze ages, per-table tuning
- [error-handling.md](references/error-handling.md) — exit_on_error, restart_after_crash, data_sync_retry

### Internals

- [internals.md](references/internals.md) — Query processing pipeline, parser/rewriter/planner/executor, system catalogs, wire protocol, access methods
- [protocol.md](references/protocol.md) — Wire protocol v3.2: message format, startup, auth, query, COPY, replication

## See also

- [sql-expert](../sql-expert/SKILL.md) — Query patterns, EXPLAIN workflow, optimization

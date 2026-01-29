---
name: tidb-sql
description: Write, review, and adapt SQL for TiDB with correct handling of TiDB-vs-MySQL differences (VECTOR type + vector indexes/functions, full-text search, AUTO_RANDOM, optimistic/pessimistic transactions, foreign keys, views, DDL limitations, and unsupported MySQL features like procedures/triggers/events/GEOMETRY/SPATIAL). Use when generating SQL that must run on TiDB, migrating MySQL SQL to TiDB, or debugging TiDB SQL compatibility errors.
---

# TiDB SQL (MySQL-compat-focused)

Goal: generate SQL that runs correctly on TiDB by default, and avoid "works on MySQL but breaks on TiDB" constructs.

## Workflow (use every time)

1. Identify the target engine and version:
   - Run `SELECT VERSION();`
   - If the result contains `TiDB`, treat it as TiDB and parse the version (needed for feature gates like Vector / Foreign Key).
   - If connecting to TiDB Cloud, ensure the client enables SSL with certificate + identity verification (see `skills/tidb-sql/references/tidb-cloud-ssl.md`).
2. Ask 2 quick capability questions if the request depends on them:
   - "Do you have TiFlash?" (needed for vector indexes)
   - "Is this TiDB Cloud Starter/Essential in a supported region for Full-Text Search?" (availability is limited)
3. Generate SQL using TiDB-safe defaults:
   - Avoid unsupported MySQL features (procedures/triggers/events/UDF/GEOMETRY/SPATIAL, etc.)
   - Treat views as read-only
   - Treat primary key changes as migration/rebuild work
4. If the user provides MySQL SQL, do a compatibility pass:
   - Replace unsupported features with TiDB alternatives
   - Call out behavior differences and version prerequisites explicitly
5. If SQL is slow or fails unexpectedly, use TiDB-native diagnostics:
   - Use `EXPLAIN FORMAT = "tidb_json"` for structured plans and operator trees.
   - Use `EXPLAIN ANALYZE` to compare `estRows` vs `actRows` (it executes the query).
   - If the plan looks wrong, consider `ANALYZE TABLE ...` to refresh statistics.

## High-signal differences (keep in mind)

- **Vector**: TiDB supports `VECTOR` / `VECTOR(D)` types and vector functions/indexes; MySQL does not.
- **No GEOMETRY/SPATIAL**: avoid `GEOMETRY`, spatial functions, and `SPATIAL` indexes.
- **No procedures / functions / triggers / events**: move logic to the application layer or an external scheduler.
- **Full-text search (TiDB feature)**: use TiDB full-text search SQL when available; don't assume MySQL `FULLTEXT` works everywhere.
- **Views are read-only**: no `UPDATE/INSERT/DELETE` against views.
- **Foreign keys**: supported in TiDB v6.6.0+; otherwise, don't rely on FK enforcement.
- **Primary key changes are restricted**: assume "create new table + backfill + swap" for PK changes.
- **AUTO_RANDOM**: prefer `AUTO_RANDOM` over `AUTO_INCREMENT` for write-hotspot avoidance when appropriate.
- **Transactions**: TiDB supports pessimistic and optimistic modes; handle optimistic `COMMIT` failures in application logic.

## Use these references (inside this skill)

- `skills/tidb-sql/references/vector.md` - VECTOR types, functions, vector index DDL, and query patterns.
- `skills/tidb-sql/references/full-text-search.md` - Full-text search SQL patterns and availability gotchas.
- `skills/tidb-sql/references/auto-random.md` - `AUTO_RANDOM` rules, DDL patterns, and restrictions.
- `skills/tidb-sql/references/transactions.md` - pessimistic vs optimistic mode and session/global knobs.
- `skills/tidb-sql/references/mysql-compatibility-notes.md` - other "MySQL vs TiDB" differences that commonly break SQL.
- `skills/tidb-sql/references/explain.md` - EXPLAIN / EXPLAIN ANALYZE usage, tidb_json and dot formats.
- `skills/tidb-sql/references/flashback.md` - FLASHBACK TABLE/DATABASE and FLASHBACK CLUSTER recovery playbooks.
- `skills/tidb-sql/references/tidb-cloud-ssl.md` - TiDB Cloud SSL verification requirements and client flags.

---
name: supabase
description: "Database operations for Supabase: query/write/migration/logs/type generation. Triggers: query/statistics/export/insert/update/delete/fix/backfill/migrate/logs/alerts/type generation. Does not trigger for: pure architecture discussion or code planning. Write operations require confirmation; UPDATE/DELETE without WHERE is refused. MCP is optional — works with CLI/Console too."
allowed-tools:
  - Read
  - Bash
  - WebFetch
  - supabase-*
---

# Supabase Database Operations

Execute database operations on Supabase: queries, writes, migrations, and diagnostics.

> **MCP is optional.** This skill works with MCP (auto), Supabase CLI, psql, or Dashboard. See [BACKENDS.md](BACKENDS.md) for execution options.

## Scope

**Applies to:**
- Database actions on Supabase: query/statistics/export, write (after confirmation), migration (DDL), type generation, query logs/advisors

**Does not apply to:**
- Project-side integration (env/client code/data access layer)  
  → Use `workflow-ship-faster` (Step 6) for project setup; this skill handles DB-side actions only

**Called by:**
- `workflow-ship-faster` uses this skill as DB operation foundation

## Postgres Best Practices (Built-in)

Ship Faster vendors Supabase's Postgres best practices under `references/postgres-best-practices/`.

Consult it when:
- Writing/reviewing/optimizing SQL queries
- Designing indexes, schema changes, or RLS policies
- Diagnosing performance, locking, or connection issues

Source of truth:
- Full guide: `references/postgres-best-practices/AGENTS.md`
- Individual rules: `references/postgres-best-practices/rules/*.md`

When proposing changes, cite the relevant rule file path (for example: `references/postgres-best-practices/rules/query-missing-indexes.md`) and keep changes minimal.

## Security Rules (Must Follow)

1. **Read first**: Always check schema before any operation
2. **Default LIMIT 50**: All SELECT queries default to `LIMIT 50`, unless user explicitly requests more
3. **Write operation confirmation**: INSERT/UPDATE/DELETE must before execution:
   - Display the SQL to be executed
   - State expected number of affected rows
   - Await explicit user confirmation
4. **No bare writes**: UPDATE/DELETE without WHERE condition → refuse directly, do not execute
5. **Batch threshold**: Affecting > 100 rows → force double confirmation + suggest `SELECT count(*)` first
6. **DDL via migration**: Schema changes must use migrations, not direct DDL
7. **Production environment**: Write disabled by default; only allow when user explicitly says "execute on prod" and double confirms
8. **Sensitive fields**: email/phone/token/password are masked or not returned by default, unless user explicitly requests

## Operation Flow

```
1. Parse requirements → restate objective
2. Unsure about tables/fields → first query schema (information_schema or list_tables)
3. Plan SQL → present to user
4. Read-only → execute directly
5. Write operation → confirm before execution → verify affected rows → report result
```

## File-based Pipeline

When integrating into multi-step workflows, persist artifacts to disk:

```
runs/<workflow>/active/<run_id>/
├── proposal.md                # Requirements / objective
├── context.json               # Known tables/fields/IDs
├── tasks.md                   # Checklist + approval gate
├── evidence/sql.md            # SQL to execute (write ops written here first)
├── evidence/result.md         # Conclusion + SQL + results
└── logs/events.jsonl          # Optional tool call summary (no sensitive data)
```

## Output Format

- **Language**: English
- **Structure**: Conclusion → Key numbers → Executed SQL → Result table (max 50 rows)
- **Overflow handling**: Truncate + show total count + optional export/pagination

Example:
```
✅ Query complete: 142 new users in the last 7 days

Executed SQL:
SELECT DATE(created_at) as date, COUNT(*) as count 
FROM user_profiles 
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at) ORDER BY date DESC;

| date       | count |
|------------|-------|
| 2025-01-09 | 23    |
| 2025-01-08 | 31    |
| ...        | ...   |
```

## Error Handling

| Situation | Action |
|-----------|--------|
| SQL syntax error | Return error summary + fix suggestions |
| Insufficient permissions | Explain required permissions + alternatives |
| No data returned | Explain possible reasons (conditions too strict? data doesn't exist?) |
| RLS blocked | Suggest checking RLS policy or using service_role |

## Example Workflows

### Read: Simple Query
```
User: Get registered user count for the last 7 days, by day

1. Confirm table user_profiles, field created_at
2. Execute aggregation SQL
3. Return: conclusion + numbers + SQL + table
```

### Read: Complex Query
```
User: Find projects that have runs but all failed

1. Confirm projects, runs tables and status field
2. Present JOIN + aggregation SQL
3. Execute and return results (mask email)
```

### Write: Insert
```
User: Create a new run for project xxx

1. First check if project exists
2. Present INSERT SQL + expected impact: 1 row
3. Await confirmation → execute → return new record id
```

### Write: Update
```
User: Change run abc's status to completed

1. First SELECT to verify current state
2. Present UPDATE SQL + WHERE id = 'abc'
3. Confirm → execute → SELECT again to verify
```

### Dangerous: Delete
```
User: Delete all runs where status = 'failed'

1. First SELECT count(*) WHERE status = 'failed'
2. Present count + DELETE SQL
3. If > 100 rows, force double confirmation
4. After confirmation execute → report deleted row count
```

### Dangerous: DELETE without WHERE
```
User: Clear the runs table

❌ Refuse to execute
→ Prompt: DELETE without WHERE condition, this will delete all data
→ Suggest: Use TRUNCATE (requires migration) or add explicit condition
```

## Schema Discovery

Get latest schema at runtime:
```sql
-- List all tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- View table structure
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = '<table_name>';
```

For project-specific schema (may be outdated), see [schema.md](schema.md).

## Related Files

- [BACKENDS.md](BACKENDS.md) — Execution options (MCP/CLI/Console)
- [SETUP.md](SETUP.md) — MCP configuration (optional)
- [schema.md](schema.md) — Project-specific schema reference

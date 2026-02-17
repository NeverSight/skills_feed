---
name: mcp-supabase
description: "Execute database operations via Supabase MCP (query/write/migration/logs/type generation). Triggers: query/statistics/export/insert/update/delete/fix/backfill/migrate/logs/alerts/type generation. Does not trigger for: pure architecture discussion or code planning. Write operations require confirmation; UPDATE/DELETE without WHERE is refused."
disable-model-invocation: true
---

# Supabase MCP Skill

Interact with Supabase database via MCP tools, execute queries, writes, migrations, and diagnostics.

## Scope

**Applies to:**
- Need to perform "database actions" on Supabase: query/statistics/export, write (after confirmation), migration (DDL), type generation, query logs/advisors

**Does not apply to:**
- Need to complete "integration implementation" in Next.js project (env/client code/minimal data access layer/project structure)  
  → Use `workflow-ship-faster` (Step 6: Supabase integration) for project-side setup; this skill only handles DB-side actions and gates

**Called by:**
- `workflow-ship-faster` uses this skill as DB operation foundation; `workflow-ship-faster` handles project-side integration, this skill handles DB-side actions and security gates

## Postgres Best Practices (Bundled)

Ship Faster vendors Supabase's Postgres best practices inside the `supabase` skill (install `supabase` alongside this skill if you want these references available locally):
- Full guide: `supabase/references/postgres-best-practices/AGENTS.md`
- Individual rules: `supabase/references/postgres-best-practices/rules/*.md`

Consult it when:
- Writing/reviewing/optimizing SQL queries
- Designing indexes, schema changes, or RLS policies
- Diagnosing performance, locking, or connection issues

When proposing changes, cite the relevant rule file path (for example: `supabase/references/postgres-best-practices/rules/query-missing-indexes.md`) and keep changes minimal.

## File-based Pipeline (Pass Paths Only)

When integrating database operations into multi-step workflows, persist all context and artifacts to disk, passing only paths between agents/sub-agents.

Recommended directory structure (within project): `runs/<workflow>/active/<run_id>/`

- Input: `01-input/goal.md` (requirements), `01-input/context.json` (known tables/fields/IDs)
- Plan: `03-plans/sql.md` (SQL to execute; write operations must be written here before confirmation)
- Output: `05-final/result.md` (conclusion + key numbers + SQL + truncated results)
- Logs: `logs/events.jsonl` (summary of each tool call; do not log sensitive field values)

## Tool Reference

| Tool | Parameters | Purpose |
|------|------------|---------|
| `list_tables` | `{"schemas":["public"]}` | List all tables in specified schema |
| `execute_sql` | `{"query":"SELECT ..."}` | Execute SQL (query or DML) |
| `apply_migration` | `{"name":"snake_case_name","query":"-- DDL"}` | Apply database migration |
| `list_migrations` | `{}` | View existing migrations |
| `generate_typescript_types` | `{}` | Generate TypeScript type definitions |
| `get_project_url` | `{}` | Get project URL |
| `get_publishable_keys` | `{}` | Get public API keys |
| `get_logs` | `{"service":"postgres\|api\|auth\|storage\|realtime\|edge-function\|branch-action"}` | Query service logs |
| `get_advisors` | `{"type":"security\|performance"}` | Get security/performance recommendations |

**Optional tools (if enabled)**:
- Edge Functions: `list_edge_functions`, `get_edge_function`, `deploy_edge_function`
- Branching: `create_branch`, `list_branches`, `merge_branch`, `reset_branch`, `rebase_branch`, `delete_branch`

## Security Rules (Must Follow)

1. **Read first**: Always check schema before any operation
2. **Default LIMIT 50**: All SELECT queries default to `LIMIT 50`, unless user explicitly requests more
3. **Write operation confirmation**: INSERT/UPDATE/DELETE must before execution:
   - Display the SQL to be executed
   - State expected number of affected rows
   - Await explicit user confirmation
4. **No bare writes**: UPDATE/DELETE without WHERE condition → refuse directly, do not execute
5. **Batch threshold**: Affecting > 100 rows → force double confirmation + suggest `SELECT count(*)` first
6. **DDL via migration**: Schema changes must use `apply_migration`, `execute_sql` cannot run DDL directly
7. **Production environment**: Write disabled by default; only allow when user explicitly says "execute on prod" and double confirms
8. **Sensitive fields**: email/phone/token/password are masked or not returned by default, unless user explicitly requests

## Operation Flow

```
1. Parse requirements → restate objective
2. Unsure about tables/fields → first list_tables or execute_sql to query information_schema
3. Plan SQL → present to user
4. Read-only → execute directly
5. Write operation → confirm before execution → verify affected rows → report result
```

## Output Format

- **Language**: English
- **Structure**: Conclusion → Key numbers → Executed SQL → Result table (max 50 rows)
- **Overflow handling**: Truncate + show total count + optional export/pagination

Example output:
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

## Example Dialogues

### Read: Simple Query
```
User: Get registered user count for the last 7 days, by day
Execution:
1. Confirm table user_profiles, field created_at
2. Execute aggregation SQL
3. Return: conclusion + numbers + SQL + table
```

### Read: Complex Query
```
User: Find projects that have runs but all failed
Execution:
1. Confirm projects, runs tables and status field
2. Present JOIN + aggregation SQL
3. Execute and return results (mask email)
```

### Write: Insert
```
User: Create a new run for project xxx
Execution:
1. First check if project exists
2. Present INSERT SQL + expected impact: 1 row
3. Await confirmation → execute → return new record id
```

### Write: Update
```
User: Change run abc's status to completed
Execution:
1. First SELECT to verify current state
2. Present UPDATE SQL + WHERE id = 'abc'
3. Confirm → execute → SELECT again to verify
```

### Dangerous: Delete
```
User: Delete all runs where status = 'failed'
Execution:
1. First SELECT count(*) WHERE status = 'failed'
2. Present count + DELETE SQL
3. If > 100 rows, force double confirmation
4. After confirmation execute → report deleted row count
```

### Dangerous: DELETE without WHERE
```
User: Clear the runs table
Execution:
❌ Refuse to execute
→ Prompt: DELETE without WHERE condition, this will delete all data
→ Suggest: Use TRUNCATE (requires migration) or add explicit condition
```

## Schema Reference

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

For project-specific schema (may be outdated), see [schema.md](schema.md). Default to information_schema / `generate_typescript_types` as source of truth.

---
name: srtd-cli
description: This skill should be used when the user mentions "srtd", "sql templates", "migrations-templates", "live reload sql", "supabase functions", when working with files in supabase/migrations-templates/, when .buildlog.json or srtd.config.json is detected, or when writing Postgres functions/views/triggers for Supabase.
---

# SRTD - Iterative SQL Template Development

## Workflow

Start watch in background immediately:
```bash
srtd watch --json
```
Use `run_in_background: true`. Monitor with `TaskOutput` for events: `templateApplied` (success), `templateError` (check `errorMessage`/`errorHint`).

## Templates

Location: `supabase/migrations-templates/*.sql`. Must be idempotent.

**Idempotency patterns:**
- Functions/Views: `CREATE OR REPLACE` (use `DROP` only when changing signature)
- Policies: `DROP POLICY IF EXISTS` then `CREATE POLICY` (not replaceable)
- Triggers: Drop BOTH trigger AND function first

**Dependencies:** `-- @depends-on: other.sql` at top

**WIP:** `.wip.sql` suffix → applies locally, never builds

## Commands

```bash
srtd apply [--force] [--json]   # Apply to local DB (use instead of watch for one-off)
srtd build [--bundle]           # Generate migration FILES only (does NOT apply to DB)
srtd clear --reset              # Reset state if confused
```

## State

- `.buildlog.json` → commit (tracks built migrations)
- `.buildlog.local.json` → gitignored (local DB state)

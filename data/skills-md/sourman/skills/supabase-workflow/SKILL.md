---
name: supabase-workflow
description: Supabase database migrations, type generation, edge function management, and best practices for this project
---

# Database Migrations

## Creating New Migrations

**CRITICAL:** Always use `npx supabase migration new <name>` to create migration files. Never create them manually.

```bash
npx supabase migration new descriptive_migration_name
```

This creates a properly timestamped migration file in `supabase/migrations/`.

## Applying Migrations

When changes are already applied to the database (e.g., via direct SQL execution), mark the migration as applied without re-running:

```bash
# Mark migration as applied (skip execution)
npx supabase migration repair --status applied <timestamp>

# Example:
npx supabase migration repair --status applied 20260122214732
```

## Pushing New Migrations

For changes not yet applied to the database:

```bash
npx supabase db push
```

## Listing Migrations

```bash
# Show recent migrations
npx supabase migration list | tail -5
```

## Migration Best Practices

1. **ALWAYS create migrations with CLI** - Use `npx supabase migration new` never manual file creation
2. **Data migrations first** - Add columns, then migrate data, then drop old structures
3. **Test migrations locally** if possible (though we use remote DB)
4. **Use transactions** for complex data migrations
5. **Verify after migration** - Query the data to ensure migration succeeded

# Type Generation

## Regenerating Types from Database Schema

After any schema changes, regenerate TypeScript types from the live database:

```bash
# Generate from remote database (recommended for this project)
npx supabase gen types typescript --linked > src/integrations/supabase/types.ts

# If local Supabase is running (Docker required)
npx supabase gen types typescript --local > src/integrations/supabase/types.ts
```

**Location:** Types are generated to `src/integrations/supabase/types.ts`

## When to Regenerate Types

Regenerate types after:
- Adding new columns to tables
- Creating new tables
- Modifying column types
- Adding/modifying enums
- Database schema migrations

**IMPORTANT:** The types file is generated from the database schema, not manually edited.

# Edge Functions

## Creating New Edge Functions

```bash
# Create new function directory
npx supabase functions new my-function-name

# Or create directory manually in supabase/functions/<function-name>/
```

**CRITICAL:** Always set `verify_jwt = false` in `supabase/config.toml` for new functions. The JWT verification uses the anon key which is not useful for our use case.

### Adding Function to Config

After creating a function, add it to `supabase/config.toml`:

```toml
[functions.my-function-name]
enabled = true
verify_jwt = false  # Always false for this project
import_map = "./functions/my-function-name/deno.json"
entrypoint = "./functions/my-function-name/index.ts"
```

## Deploying Edge Functions

```bash
npx supabase functions deploy my-function-name
```

## Deleting Edge Functions

To properly remove an edge function:

1. **Delete from remote Supabase:**
   ```bash
   npx supabase functions delete function-name
   ```

2. **Remove local directory:**
   ```bash
   rm -rf supabase/functions/function-name
   ```

3. **Remove from config.toml:**
   Delete the `[functions.function-name]` section from `supabase/config.toml`

### Complete Edge Function Deletion Example

```bash
# 1. Delete from remote
npx supabase functions delete create-team-member

# 2. Delete local directory
rm -rf supabase/functions/create-team-member

# 3. Edit config.toml to remove the function section
# Remove lines like:
# [functions.create-team-member]
# enabled = true
# verify_jwt = false
# import_map = "./functions/create-team-member/deno.json"
# entrypoint = "./functions/create-team-member/index.ts"
```

## Listing Edge Functions

```bash
# List all functions
ls supabase/functions/

# Check config for function definitions
grep -A 4 "\[functions" supabase/config.toml
```

# Database Query Execution

## Running SQL Queries

This project uses a custom Supabase CLI wrapper:

```bash
# Run a query
bun run supabase:sql --query "SELECT COUNT(*) FROM profiles"

# Alternative: Use the generated TypeScript CLI
./supabase-cli execute-sql --query "SELECT COUNT(*) FROM profiles"
```

# Common Workflows

## Complete Schema Change Workflow

When making database schema changes:

1. **Create migration:**
   ```bash
   npx supabase migration new describe_the_change
   ```

2. **Write migration SQL** in the created file

3. **Apply migration:**
   ```bash
   npx supabase db push
   ```

4. **Regenerate types:**
   ```bash
   npx supabase gen types typescript --linked > src/integrations/supabase/types.ts
   ```

5. **Update frontend code** to use new types/fields

## Database Investigation Workflow

When investigating database state:

```bash
# Use bun run supabase:sql --query for quick queries
bun run supabase:sql --query "SELECT * FROM profiles LIMIT 5"

# Or use the generated CLI
./supabase-cli execute-sql --query "SELECT * FROM app_roles"
```

# Project-Specific Notes

## This Project's Supabase Setup

- **Database:** Remote Supabase (project ref: sbdlvtfjsdldekqjzngh)
- **Local Docker:** Not configured (use `--linked` flag for remote operations)
- **Type Location:** `src/integrations/supabase/types.ts`
- **Migrations Location:** `supabase/migrations/`
- **Functions Location:** `supabase/functions/`
- **Config Location:** `supabase/config.toml`

## Key Learnings

- **Always use migration repair** when changes are already applied to remote DB
- **Regenerate types after every schema change** - don't manually edit types
- **verify_jwt = false** is standard for this project's edge functions
- **Use `--linked` flag** for remote database operations (no local Docker)
- **Delete edge functions completely** - remote, local files, AND config.toml

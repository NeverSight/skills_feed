---
name: supabase-cli
description: Comprehensive guide for Supabase CLI usage covering database initialization, migrations, type generation, API key management, and direct query execution. Use this skill when working with Supabase local development, database schema management, or any CLI command usage.
---

# Supabase CLI

## Overview

This skill provides complete guidance for using Supabase CLI across all development workflows. It covers database initialization, migration management, type generation, API key retrieval, direct database access, and deployment strategies.

Use this skill when:

- Setting up new Supabase projects
- Managing database migrations
- Generating TypeScript types from database schema
- Retrieving API keys and connection details
- Executing SQL queries directly
- Troubleshooting local development issues
- Deploying schema changes to production

## Quick Start

### Initial Project Setup

Initialize a new Supabase project:

```bash
supabase init
```

Start local development stack:

```bash
supabase start
```

Get connection details and API keys:

```bash
supabase status
```

Link to remote project:

```bash
supabase link --project-ref PROJECT_REF
```

---

## Database Initialization

### Creating New Local Database

Start fresh local Supabase instance:

```bash
supabase init
supabase start
```

This creates:

- Local PostgreSQL database on port 54322
- Studio dashboard at http://localhost:54323
- API server on port 54321
- All Supabase services (Auth, Storage, Realtime, etc.)

### Resetting Database

Reset database to clean state with all migrations applied:

```bash
supabase db reset
```

Reset without running seed data:

```bash
supabase db reset --no-seed
```

### Checking Status

View all running services and connection details:

```bash
supabase status
```

Export connection details as environment variables:

```bash
supabase status -o env > .env.local
```

---

## Migration Management

### Creating Migrations

**Method 1: Manual SQL File**

Create new migration file:

```bash
supabase migration new create_users_table
```

Edit `supabase/migrations/<timestamp>_create_users_table.sql`:

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

Apply migration:

```bash
supabase db reset
```

**Method 2: Auto-Generate from Diff**

Make schema changes in Studio (http://localhost:54323), then generate migration:

```bash
supabase db diff -f add_users_table
```

Review generated file at `supabase/migrations/<timestamp>_add_users_table.sql`, then apply:

```bash
supabase db reset
```

### Deploying Migrations

Preview changes before deployment:

```bash
supabase db push --linked --dry-run
```

Deploy to remote:

```bash
supabase db push --linked
```

Deploy with seed data:

```bash
supabase db push --linked --include-seed
```

Deploy with custom roles:

```bash
supabase db push --linked --include-roles
```

### Pulling Remote Schema

Import existing remote schema to local:

```bash
supabase link --project-ref PROJECT_REF
supabase db pull initial_schema
supabase db reset
```

Pull specific schemas only:

```bash
supabase db pull -s public,extensions
```

### Migration Best Practices

Always follow this workflow:

1. Create migration locally
2. Apply with `supabase db reset`
3. Generate types
4. Test application
5. Commit migration file
6. Deploy with `supabase db push --linked --dry-run` first
7. Deploy with `supabase db push --linked`

---

## Type Generation

### TypeScript Types

Generate types from local database:

```bash
supabase gen types typescript --local > src/lib/types/database.types.ts
```

Generate from remote:

```bash
supabase gen types typescript --linked > src/lib/types/database.types.ts
```

Generate specific schemas:

```bash
supabase gen types typescript --local --schema public,extensions > src/lib/types/database.types.ts
```

### Other Languages

Generate Go types:

```bash
supabase gen types go --local > types/database.go
```

Generate Swift types:

```bash
supabase gen types swift --local --swift-access-control public > Types/Database.swift
```

### Automation

Regenerate types after every schema change:

```bash
supabase db reset && supabase gen types typescript --local > src/lib/types/database.types.ts
```

---

## API Key Management

### Getting Local Keys

View all local API keys:

```bash
supabase status
```

Extract keys to environment file:

```bash
supabase status -o env > .env.local
```

Result includes:

- `SUPABASE_URL` - API endpoint
- `SUPABASE_ANON_KEY` - Client-side public key
- `SUPABASE_SERVICE_ROLE_KEY` - Server-side admin key
- `DATABASE_URL` - Direct database connection

### Getting Remote Keys

Authenticate first:

```bash
supabase login
```

Link to project:

```bash
supabase link --project-ref PROJECT_REF
```

Retrieve API keys:

```bash
supabase projects api-keys --project-ref PROJECT_REF
```

---

## Direct Database Access

### Using psql

Connect to local database:

```bash
psql postgresql://postgres:postgres@localhost:54322/postgres
```

Execute single query:

```bash
psql postgresql://postgres:postgres@localhost:54322/postgres -c "SELECT * FROM users;"
```

Run SQL file:

```bash
psql postgresql://postgres:postgres@localhost:54322/postgres -f query.sql
```

### Connection Details

Get database URL from status:

```bash
supabase status
```

Extract only database URL:

```bash
supabase status | grep "DB URL"
```

### Running Migrations Manually

Apply specific SQL file:

```bash
psql postgresql://postgres:postgres@localhost:54322/postgres -f supabase/migrations/20230101_my_migration.sql
```

---

## Common Workflows

### Standard Development Cycle

**Daily workflow:**

```bash
# Morning: Start stack
supabase start

# Make schema changes in Studio or create migration
supabase migration new add_feature

# Apply changes
supabase db reset

# Regenerate types
supabase gen types typescript --local > src/lib/types/database.types.ts

# Test application
npm run dev

# Commit changes
git add supabase/migrations/ src/lib/types/database.types.ts
git commit -m "feat: add new feature schema"

# Deploy to production
supabase db push --linked --dry-run
supabase db push --linked
```

### Team Collaboration

**New developer setup:**

```bash
# Clone repository
git clone REPO_URL

# Install CLI
npm install

# Login to Supabase
supabase login

# Start local development
supabase start

# Apply all migrations
supabase db reset

# Generate types
supabase gen types typescript --local > src/lib/types/database.types.ts
```

**After pulling teammate's changes:**

```bash
git pull
supabase db reset
supabase gen types typescript --local > src/lib/types/database.types.ts
```

### Production Deployment

**Safe deployment pattern:**

```bash
# Link to production project
supabase link --project-ref PRODUCTION_REF

# Preview changes
supabase db push --linked --dry-run

# Review output carefully

# Deploy
supabase db push --linked

# Verify deployment
supabase db pull verify_deployment
```

---

## Troubleshooting

### Port Conflicts

If ports are already in use, edit `supabase/config.toml`:

```toml
[api]
port = 55321

[db]
port = 55322

[studio]
port = 55323
```

Then restart:

```bash
supabase stop
supabase start
```

### Database in Bad State

Reset completely:

```bash
supabase stop
docker volume prune
supabase start
supabase db reset
```

### Migration Conflicts

Pull remote changes first:

```bash
supabase db pull remote_changes
```

Resolve conflicts in migration files, then:

```bash
supabase db reset
supabase db push --linked
```

### Type Mismatches

Regenerate types from current schema:

```bash
supabase gen types typescript --local > src/lib/types/database.types.ts
```

---

## Command Reference

For complete CLI command reference with all flags and options, see `references/cli-commands.md`.

For detailed workflow examples and patterns, see `references/workflows.md`.

### Most Used Commands

**Setup:**

- `supabase init` - Initialize project
- `supabase login` - Authenticate
- `supabase link` - Link to remote project
- `supabase start` - Start local stack
- `supabase status` - View connection details

**Database:**

- `supabase db reset` - Reset database with migrations
- `supabase db diff -f NAME` - Generate migration from diff
- `supabase db push --linked` - Deploy migrations
- `supabase db pull` - Import remote schema

**Migrations:**

- `supabase migration new NAME` - Create new migration
- `supabase migration list` - List all migrations

**Types:**

- `supabase gen types typescript --local` - Generate TypeScript types

**Keys:**

- `supabase status` - Get local keys
- `supabase projects api-keys` - Get remote keys

**Cleanup:**

- `supabase stop` - Stop local stack

---

## Resources

### references/cli-commands.md

Complete command reference with all flags, options, and examples for every Supabase CLI command. Load this when:

- Need detailed flag information for specific command
- Looking up exact syntax
- Exploring advanced command options

**Search patterns:**

```bash
# Find commands related to migrations
grep -i "migration" references/cli-commands.md

# Find commands for type generation
grep -i "gen types" references/cli-commands.md

# Find database commands
grep -i "supabase db" references/cli-commands.md
```

### references/workflows.md

Comprehensive workflow guides covering:

- Initial setup patterns
- Schema development workflows
- Migration management strategies
- Type generation automation
- Team collaboration patterns
- CI/CD integration
- Troubleshooting common issues

Load this when:

- Planning complex workflow
- Setting up team collaboration
- Configuring CI/CD pipelines
- Solving workflow-specific problems
- Looking for best practices

---
name: go-goose
description: Use this skill to plan, write, or run database migrations with the pressly/goose CLI and Go library (SQL/Go migrations, env vars, provider API, embedded migrations).
metadata:
  short-description: Expert guidance for goose CLI and Go library migrations.
---

# go-goose

Expert guidance for using pressly/goose to create and run database migrations via the CLI or Go library.

## When to trigger
- The user mentions goose, pressly/goose, database migrations in Go, or asks how to run SQL/Go migrations.
- The task involves embedding migrations, provider API usage, or CI workflows with goose.

## Core rules
- Follow the repository's existing migration layout, dialect, and naming conventions first.
- Ensure the database driver and goose dialect match (e.g., `postgres` driver with `postgres` dialect).
- Prefer SQL migrations for schema changes; use Go migrations for complex data backfills or code-driven steps.
- Keep migrations deterministic and idempotent within goose's rules (one Up, optional Down).

## Workflow
1. **Clarify context**: target DB/dialect, driver, migration directory, SQL vs Go migration needs, and desired command (create/up/down/status/etc).
2. **Choose interface**:
   - **CLI** for ad-hoc runs or CI/CD.
   - **Library/Provider** when migrations are executed inside Go services or tests.
3. **Author migrations**:
   - SQL: use goose annotations and statement rules (see [references/sql-annotations.md](references/sql-annotations.md)).
   - Go: register migrations in init and wire into a custom binary or Provider (see [references/go-migrations.md](references/go-migrations.md)).
4. **Run migrations**:
   - CLI usage, commands, and env vars in [references/cli.md](references/cli.md).
   - Library/Provider patterns in [references/library.md](references/library.md).
5. **Versioning + ordering**:
   - Use hybrid versioning during development and `fix` for production sequencing if required (see [references/versioning.md](references/versioning.md)).

## Output expectations
- Provide exact commands or code snippets that match the user's dialect and environment.
- Warn about missing Down migrations when rollbacks are required.
- If a migration requires special parsing or non-transactional execution, call it out explicitly.

## References
- CLI usage and env vars: [references/cli.md](references/cli.md)
- SQL annotations and parsing rules: [references/sql-annotations.md](references/sql-annotations.md)
- Go migration registration patterns: [references/go-migrations.md](references/go-migrations.md)
- Library and Provider API usage: [references/library.md](references/library.md)
- Versioning and ordering: [references/versioning.md](references/versioning.md)

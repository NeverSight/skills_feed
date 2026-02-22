---
name: db-migration
description: Database schema and migration workflow. Use when modifying database schemas in tools/atlas/ or SQLC queries in tools/sqlc/.
---

# Database Migration Workflow

Workflow for database schema and migration changes.

## Prerequisites

- **Use `git-workflow` Skill** for branch, commit, and PR workflow.
- **Refer to `.claude/rules/hcl.md`** for HCL schema rules (SSOT).
- **Refer to `.claude/rules/sql.md`** for SQL query rules (SSOT).

## Applicable Files

| Path                        | Description                              |
| --------------------------- | ---------------------------------------- |
| `tools/atlas/schemas/*.hcl` | HCL schema definitions (source of truth) |
| `tools/sqlc/queries/mysql/*.sql`  | SQLC query definitions                   |

## Workflow

### 1. Modify Schema (HCL)

Edit HCL files in `tools/atlas/schemas/`.

### 2. Verify HCL (from rules/hcl.md)

```bash
make atlas-fmt && make atlas-lint
```

### 3. Generate Migrations

```bash
make atlas-dev-reset
```

### 4. Test Migration

```bash
docker compose down -v && docker compose --profile mysql up -d
```

### 5. Regenerate SQLC (from rules/sql.md)

```bash
make extract-sqlc-schema-all && make sqlc
```

### 6. Verify Go Code

```bash
make check-build && make gotest
```

## Self-Review Checklist

- [ ] HCL format/lint passes
- [ ] Migration applies cleanly
- [ ] SQLC generates correctly
- [ ] Go build passes

## Related

- `.claude/rules/hcl.md` - HCL rules (SSOT)
- `.claude/rules/sql.md` - SQL rules (SSOT)
- `go-development` - Go verification after SQLC generation
- `git-workflow` - Branch, commit, PR workflow

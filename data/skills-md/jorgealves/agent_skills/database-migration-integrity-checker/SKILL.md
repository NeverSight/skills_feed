---
name: database-migration-integrity-checker
description: Audits SQL migration files for destructive actions, potential table locks, and compatibility issues. Use before applying migrations to production databases to prevent downtime and ensure data integrity.
---
# Database Migration Integrity Checker

## Purpose and Intent
The `database-migration-integrity-checker` is a safety net for your most critical asset: your data. It catches dangerous SQL operations that might pass a standard code review but could cause production outages or data loss.

## When to Use
- **CI/CD Pipelines**: Block deployments if a migration contains a high-risk operation without manual override.
- **Local Development**: Run before committing a new migration to ensure it follows safe DDL practices.

## When NOT to Use
- **Data Querying**: This is for *schema* changes, not for auditing standard SELECT/INSERT queries.

## Security and Data-Handling Considerations
- Reads SQL files only; no database access required.
- Safe for local use.

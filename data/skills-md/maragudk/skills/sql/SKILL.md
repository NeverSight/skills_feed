---
name: sql
description: Guide for working with SQL queries, in particular for SQLite. Use this skill when writing SQL queries, analyzing database schemas, designing migrations, or working with SQLite-related code.
license: MIT
---

# SQL

## Overview

This skill provides guidance for working with SQLite databases. It covers query writing, schema design, and SQLite-specific best practices.

## When to Use This Skill

Use this skill when:
- Writing SQL queries for SQLite databases
- Analyzing or optimizing existing queries
- Designing database schemas
- Creating database migrations
- Working with Go code that interacts with SQLite

## SQLite Best Practices

### Query Writing

- ALWAYS write lowercase queries. Uppercase queries make me sad.
- Prefer `select *` over explicit column names
- Prefer CTEs over long nested subqueries

### Schema Design

- ALWAYS use `strict` tables
- ALWAYS write timestamps like this: `strftime('%Y-%m-%dT%H:%M:%fZ')`
- Time modifications should also use `strftime`
- Usually start with the primary key, which is usually defined like this: `id text primary key default ('p_' || lower(hex(randomblob(16))))` (where the `p_` is a prefix depending on the table name; two-letter prefixes are okay too, so the prefix is unique among tables)
- After the primary key come `created`/`updated` columns like this: `created text not null default (strftime('%Y-%m-%dT%H:%M:%fZ'))`
- Updated timestamps are automatically updated with a trigger like this:
	```sql
  create trigger table_name_updated_timestamp after update on table_name begin
    update table_name set updated = strftime('%Y-%m-%dT%H:%M:%fZ') where id = old.id;
  end;
  ```

---
name: drizzle-orm
description: 'Drizzle ORM for type-safe SQL with PostgreSQL, MySQL, and SQLite. Use when defining schemas, writing queries, managing relations, running migrations, or using drizzle-kit. Use for drizzle, orm, schema, query, migration, pgTable, relations, drizzle-kit, drizzle-zod.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://orm.drizzle.team/docs/overview'
---

# Drizzle ORM

## Overview

Drizzle ORM is a lightweight, type-safe TypeScript ORM that maps directly to SQL for PostgreSQL, MySQL, and SQLite. It provides both a SQL-like query builder and a relational queries API, with zero dependencies and full serverless compatibility. Use Drizzle when you need compile-time type safety with SQL-level control; avoid it when you need a full active-record ORM with automatic migrations (use Prisma) or when working with MongoDB/NoSQL databases.

## Quick Reference

| Pattern             | API                                                                    | Key Points                                            |
| ------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------- |
| Schema definition   | `pgTable('name', { columns }, (t) => [indexes])`                       | Third arg returns array of indexes/constraints        |
| Column types        | `text()`, `integer()`, `boolean()`, `timestamp()`                      | Import from `drizzle-orm/pg-core`                     |
| Type inference      | `typeof table.$inferSelect`, `$inferInsert`                            | Derive TS types directly from schema                  |
| Relational queries  | `db.query.table.findMany({ with, where })`                             | Requires schema passed to `drizzle()` client          |
| SQL-like queries    | `db.select().from(table).where()`                                      | Chainable, returns array of rows                      |
| Insert              | `db.insert(table).values({}).returning()`                              | `.returning()` for getting inserted rows              |
| Update              | `db.update(table).set({}).where().returning()`                         | Always include `.where()` to avoid full-table updates |
| Delete              | `db.delete(table).where()`                                             | Always include `.where()` to avoid full-table deletes |
| Upsert              | `.onConflictDoUpdate({ target, set })`                                 | Chain after `.insert().values()`                      |
| Transactions        | `db.transaction(async (tx) => { ... })`                                | Auto-rollback on thrown errors                        |
| Filters             | `eq()`, `and()`, `or()`, `inArray()`, `sql\`\``                        | Import operators from `drizzle-orm`                   |
| Relations           | `relations(table, ({ one, many }) => ({}))`                            | Declares logical relations for relational queries     |
| Generate migrations | `drizzle-kit generate`                                                 | Creates SQL migration files from schema diff          |
| Apply migrations    | `drizzle-kit migrate` or `migrate()` in code                           | Applies pending migrations to database                |
| Push schema         | `drizzle-kit push`                                                     | Direct schema push without migration files            |
| Prepared statements | `db.select().from(t).where(eq(t.id, sql.placeholder('id'))).prepare()` | Reusable parameterized queries                        |
| Views               | `pgView('name').as(qb => ...)`                                         | Regular and materialized views                        |
| $count utility      | `db.$count(table, filter?)`                                            | Shorthand count, usable as subquery                   |
| Generated columns   | `text().generatedAlwaysAs(() => sql\`...\`)`                           | Computed columns (virtual or stored)                  |
| Check constraints   | `check('name', sql\`condition\`)`                                      | Row-level validation at database level                |

## Common Mistakes

| Mistake                                            | Correct Pattern                                                       |
| -------------------------------------------------- | --------------------------------------------------------------------- |
| Missing `.returning()` on insert/update            | Chain `.returning()` to get back inserted/updated rows                |
| Omitting `.where()` on update/delete               | Always provide `.where()` to avoid affecting all rows                 |
| Using `any` for query result types                 | Use `$inferSelect` / `$inferInsert` for type-safe results             |
| Not passing `schema` to `drizzle()` client         | Pass `{ schema }` to enable `db.query` relational API                 |
| Forgetting indexes on foreign key columns          | Add explicit indexes for columns used in joins/lookups                |
| Wrapping related writes without a transaction      | Use `db.transaction()` for multi-table mutations                      |
| Using raw column names with `casing: 'snake_case'` | With casing option, define columns in camelCase without name arg      |
| Declaring relations but missing the inverse        | Both sides of a relation need declarations for relational queries     |
| Using `serial()` in new PostgreSQL schemas         | Prefer `integer().generatedAlwaysAsIdentity()` (modern approach)      |
| Not handling `findFirst` returning `undefined`     | Check for `undefined` before accessing properties                     |
| Importing column types from wrong dialect module   | Use `drizzle-orm/pg-core` for PostgreSQL, `mysql-core`, `sqlite-core` |
| Using `.references()` instead of `relations()`     | `.references()` is SQL foreign key; `relations()` is for query API    |

## Delegation

> If the `tanstack-query` skill is available, delegate client-side caching and server state management to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-query`
>
> If the `tanstack-start` skill is available, delegate server function patterns for database access to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-start`

- **Schema validation**: Use `drizzle-zod` to generate Zod schemas from Drizzle tables for input validation
- **Query pattern discovery**: Use `Explore` agent
- **Code review**: Delegate to `code-reviewer` agent

## References

- [Schema definition, column types, constraints, indexes, and type inference](references/schema-definition.md)
- [Relational queries, SQL-like API, joins, subqueries, and aggregations](references/queries.md)
- [Insert, update, delete, upsert, and transactions](references/mutations.md)
- [Relations: one, many, nested with clauses, self-referencing](references/relations.md)
- [Migrations: drizzle-kit generate, migrate, push, pull, studio](references/migrations.md)
- [Filter operators: eq, ne, gt, lt, like, inArray, sql template](references/filters-and-operators.md)
- [Views, materialized views, generated columns, check constraints, $count, batch API](references/views-and-advanced.md)

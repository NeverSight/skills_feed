---
name: drizzle
description: Drizzle ORM documentation covering queries, CRUD operations, schema definitions, migrations, caching (50 topics), custom types, and database connections. Includes integrations for PostgreSQL (Neon, Vercel, Supabase, AWS Data API, PlanetScale, Prisma), MySQL (AWS Data API, PlanetScale, TiDB), and SQLite (Bun, Cloudflare D1/Durable Objects, Expo, Turso, OP SQLite). Use when working with Drizzle queries, database schemas, migrations, type-safe SQL, ORM patterns, or connecting to supported databases.
allowed-tools: Read, Glob, Grep
---
# drizzle Documentation

**Source**: `https://orm.drizzle.team/llms-full.txt`
**Generated**: 2026-01-11 22:30 UTC
**Total**: 101 topics across 46 chapters (~338,612 tokens)

## Retrieval Workflow

1. **Find Chapter**: Browse the chapter listing below to locate the relevant category
2. **Find Topic**: Read `_index.md` inside that chapter's folder for the topic list
3. **Read Content**: Read the specific topic file

## Quick Search

If unsure which chapter contains your answer:
```
grep -r "keyword" .claude/skills/drizzle/docs/
```

## Chapters

- [Drizzle](docs/drizzle/_index.md) - 1 topics (~106 tokens)
- [drizzle-arktype](docs/drizzle-arktype/_index.md) - 1 topics (~2,741 tokens)
- [Batch API](docs/batch-api/_index.md) - 1 topics (~752 tokens)
- [Cache](docs/cache/_index.md) - 50 topics (~29,233 tokens)
- [Drizzle \<\> AWS Data API MySQL](docs/drizzle--aws-data-api-mysql/_index.md) - 1 topics (~123 tokens)
- [Drizzle \<\> AWS Data API Postgres](docs/drizzle--aws-data-api-postgres/_index.md) - 1 topics (~443 tokens)
- [Drizzle \<\> Bun SQL](docs/drizzle--bun-sql/_index.md) - 1 topics (~368 tokens)
- [Drizzle \<\> Bun SQLite](docs/drizzle--bun-sqlite/_index.md) - 1 topics (~528 tokens)
- [Drizzle \<\> Cloudflare D1](docs/drizzle--cloudflare-d1/_index.md) - 1 topics (~636 tokens)
- [Drizzle \<\> Cloudflare Durable Objects SQLite](docs/drizzle--cloudflare-durable-objects-sqlite/_index.md) - 1 topics (~1,283 tokens)
- [Drizzle HTTP proxy](docs/drizzle-http-proxy/_index.md) - 1 topics (~1,888 tokens)
- [Drizzle \<\> Expo SQLite](docs/drizzle--expo-sqlite/_index.md) - 1 topics (~1,132 tokens)
- [Drizzle \<\> Neon Postgres](docs/drizzle--neon-postgres/_index.md) - 1 topics (~1,355 tokens)
- [Drizzle \<\> Nile](docs/drizzle--nile/_index.md) - 1 topics (~1,217 tokens)
- [Drizzle \<\> OP SQLite](docs/drizzle--op-sqlite/_index.md) - 1 topics (~865 tokens)
- [Database connection with Drizzle](docs/database-connection-with-drizzle/_index.md) - 1 topics (~1,416 tokens)
- [Drizzle \<\> PGlite](docs/drizzle--pglite/_index.md) - 1 topics (~552 tokens)
- [Drizzle \<\> PlanetScale Postgres](docs/drizzle--planetscale-postgres/_index.md) - 3 topics (~1,218 tokens)
- [Drizzle \<\> PlanetScale MySQL](docs/drizzle--planetscale-mysql/_index.md) - 1 topics (~615 tokens)
- [Drizzle \<\> Prisma Postgres](docs/drizzle--prisma-postgres/_index.md) - 1 topics (~552 tokens)
- [Drizzle \<\> React Native SQLite](docs/drizzle--react-native-sqlite/_index.md) - 1 topics (~209 tokens)
- [Drizzle \<\> SQLite Cloud](docs/drizzle--sqlite-cloud/_index.md) - 1 topics (~415 tokens)
- [Drizzle \<\> Supabase](docs/drizzle--supabase/_index.md) - 1 topics (~594 tokens)
- [Drizzle \<\> TiDB Serverless](docs/drizzle--tidb-serverless/_index.md) - 1 topics (~514 tokens)
- [Drizzle \<\> Turso Database](docs/drizzle--turso-database/_index.md) - 1 topics (~411 tokens)
- [Drizzle \<\> Turso Cloud](docs/drizzle--turso-cloud/_index.md) - 1 topics (~628 tokens)
- [Drizzle \<\> Vercel Postgres](docs/drizzle--vercel-postgres/_index.md) - 1 topics (~682 tokens)
- [Drizzle \<\> Xata](docs/drizzle--xata/_index.md) - 1 topics (~361 tokens)
- [Common way of defining custom types](docs/common-way-of-defining-custom-types/_index.md) - 3 topics (~2,193 tokens)
- [Drizzle Queries + CRUD](docs/drizzle-queries--crud/_index.md) - 3 topics (~39,807 tokens)
- [Bind a Durable Object. Durable objects are a scale-to-zero compute primitive based on the actor model.](docs/bind-a-durable-object-durable-objects-are-a-scale-to-zero-co/_index.md) - 1 topics (~26 tokens)
- [Durable Objects can live for as long as needed. Use these when you need a long-running "server", such as in realtime apps.](docs/durable-objects-can-live-for-as-long-as-needed-use-these-whe/_index.md) - 1 topics (~31 tokens)
- [Docs: https://developers.cloudflare.com/workers/wrangler/configuration/#durable-objects](docs/docs-httpsdeveloperscloudflarecomworkerswranglerconfiguratio/_index.md) - 1 topics (~44 tokens)
- [Durable Object migrations.](docs/durable-object-migrations/_index.md) - 1 topics (~7 tokens)
- [Docs: https://developers.cloudflare.com/workers/wrangler/configuration/#migrations](docs/docs-httpsdeveloperscloudflarecomworkerswranglerconfiguratio/_index.md) - 1 topics (~38 tokens)
- [We need rules so we can import migrations in the next steps](docs/we-need-rules-so-we-can-import-migrations-in-the-next-steps/_index.md) - 1 topics (~2,496 tokens)
- [Bind a Durable Object. Durable objects are a scale-to-zero compute primitive based on the actor model.](docs/bind-a-durable-object-durable-objects-are-a-scale-to-zero-co/_index.md) - 1 topics (~26 tokens)
- [Durable Objects can live for as long as needed. Use these when you need a long-running "server", such as in realtime apps.](docs/durable-objects-can-live-for-as-long-as-needed-use-these-whe/_index.md) - 1 topics (~31 tokens)
- [Docs: https://developers.cloudflare.com/workers/wrangler/configuration/#durable-objects](docs/docs-httpsdeveloperscloudflarecomworkerswranglerconfiguratio/_index.md) - 1 topics (~44 tokens)
- [Durable Object migrations.](docs/durable-object-migrations/_index.md) - 1 topics (~7 tokens)
- [Docs: https://developers.cloudflare.com/workers/wrangler/configuration/#migrations](docs/docs-httpsdeveloperscloudflarecomworkerswranglerconfiguratio/_index.md) - 1 topics (~38 tokens)
- [We need rules so we can import migrations in the next steps](docs/we-need-rules-so-we-can-import-migrations-in-the-next-steps/_index.md) - 1 topics (~210,031 tokens)
- [create a tenant](docs/create-a-tenant/_index.md) - 1 topics (~41 tokens)
- [get tenants](docs/get-tenants/_index.md) - 1 topics (~16 tokens)
- [create a todo (don't forget to use a real tenant-id in the URL)](docs/create-a-todo-dont-forget-to-use-a-real-tenant-id-in-the-url/_index.md) - 1 topics (~68 tokens)
- [list todos for tenant (don't forget to use a real tenant-id in the URL)](docs/list-todos-for-tenant-dont-forget-to-use-a-real-tenant-id-in/_index.md) - 1 topics (~32,831 tokens)

## Rules

- Start at this file to locate content - never guess file paths
- Read only necessary files to minimize token usage
- Cite specific file paths when referencing documentation

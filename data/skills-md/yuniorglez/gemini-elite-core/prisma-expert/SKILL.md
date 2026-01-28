---
name: prisma-expert
id: prisma-expert
version: 1.2.0
description: "Senior specialist in Prisma 7, Rust-free query engines, and Edge-first database architecture. Use when optimizing queries, configuring TypedSQL, or deploying to serverless/edge environments in 2026."
---

# 💎 Skill: prisma-expert

## Description
Senior specialist in Prisma 7, focused on the revolutionary TypeScript-based query engine (Rust-free) that drastically reduces cold starts and memory overhead. Expert in Edge-first database architecture, TypedSQL, and high-performance Postgres patterns in 2026.

## Core Priorities
1.  **Rust-free Engine**: Leveraging the WASM/TS engine for sub-50ms cold starts in serverless.
2.  **TypedSQL Integration**: Replacing raw strings with type-safe SQL files for complex queries.
3.  **Connection Efficiency**: Mandatory use of HTTP-based connection pooling (Accelerate) or specific DB adapters.
4.  **Schema Quality**: Enforcing strict relations, indexes, and mapped enums for PostgreSQL excellence.

## 🏆 Top 5 Gains in Prisma 7 (2026)

1.  **90% Smaller Bundle**: The removal of the Rust engine binary makes Prisma viable for even the most restricted edge runtimes.
2.  **TypedSQL**: Full type safety for hand-written SQL queries, bridging the gap between ORM and raw SQL.
3.  **Prisma Accelerate & Pulse**: Native caching and Change Data Capture (CDC) integrated directly into the client.
4.  **Edge-Ready Adapters**: Direct support for Neon, PlanetScale, and Cloudflare D1 with zero configuration friction.
5.  **Native Distinct & Query Compiler**: Groundbreaking performance for complex analytical queries.

## Table of Contents & Detailed Guides

### 1. [Query Optimization & TypedSQL](./references/1-query-optimization.md) — **CRITICAL**
- Indexing strategies and `nativeDistinct`
- TypedSQL: Safe raw queries
- Avoiding N+1 with `include` and `select`

### 2. [Serverless & Edge Deployment](./references/2-serverless-edge.md) — **CRITICAL**
- Using the Rust-free WASM engine
- Prisma Accelerate (Connection Pooling & Caching)
- Regional execution best practices

### 3. [Advanced Schema Patterns](./references/3-schema-patterns.md) — **HIGH**
- Mapped Enums and Postgres-native types
- Complex Relations (m:n, self-referencing)
- Prisma Pulse (Real-time CDC)

### 4. [Prisma Studio & Telemetry](./references/4-tools.md) — **MEDIUM**
- Advanced usage of the 2026 Prisma Studio
- Telemetry and performance monitoring
- Migration workflows (CLI 2026)

## Quick Reference: The "Do's" and "Don'ts"

| **Don't** | **Do** |
| :--- | :--- |
| `prisma.$queryRaw` (raw strings) | Use **TypedSQL** (`.sql` files) |
| Large fetches with `select *` | Use explicit `select: { ... }` |
| Direct DB connection in Serverless | Use **Prisma Accelerate** or Adapters |
| Heavy `node_modules` in Edge | Enable the **WASM/TS Engine** |
| Manual indexing in production | Trust the `Index Advisor` and DB logs |
| Ignore Prisma Pulse | Use it for real-time event-driven logic |

---
*Optimized for Prisma 7.1+ and Postgres 17+.*
*Updated: January 22, 2026 - 15:07*

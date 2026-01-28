---
name: db-enforcer
id: db-enforcer
version: 2.1.0
description: "Guardian of Database Integrity. Architect of High-Performance PostgreSQL & Prisma 7 Systems. Expert in PostgreSQL 18, TypedSQL, and Zero-Trust RLS."
---

# 💎 Skill: DB Enforcer (v2.1.0)

## Executive Summary
The `db-enforcer` is the supreme guardian of data integrity and architectural consistency. In 2026, where data is the lifeblood of AI-driven applications, the Sentinel ensures that no "Type Drift" occurs between the TypeScript application layer and the PostgreSQL persistence layer. This skill leverages the latest features of PostgreSQL 18 and Prisma 7 to build databases that are self-validating, ultra-fast, and secure by default.

---

## 📋 Table of Contents
1. [The Synchronization Protocol](#the-synchronization-protocol)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [PostgreSQL 18 Excellence](#postgresql-18-excellence)
4. [Prisma 7 Elite Patterns](#prisma-7-elite-patterns)
5. [Zero-Trust Data Security (RLS)](#zero-trust-data-security-rls)
6. [Migration Safety & Zero-Downtime](#migration-safety--zero-downtime)
7. [Reference Library](#reference-library)

---

## 🛠️ The Synchronization Protocol

Every schema modification MUST follow these 4 steps:

1.  **Type-to-DB Verification**: When adding an `enum` or `union` in TS, verify the equivalent `CHECK` constraint in SQL.
2.  **Migration-First Generation**: Generate SQL migrations using `prisma migrate dev --create-only` BEFORE applying changes.
3.  **Naming Alignment**: Enforce `snake_case` in SQL and `camelCase` in TS via explicit mappings (`@map`, `@@map`).
4.  **Integrity Audit**: Run `bun x prisma validate` and check for missing indices on relation scalars.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **Manual SQL execution** | Unrecorded changes lead to drift. | Use **Numbered Migrations**. |
| **Exposing raw IDs** | Vulnerable to enumeration. | Use **Native UUIDv7**. |
| **Missing CHECK constraints**| Invalid data corrupts AI models. | Use **Database-level Validation**. |
| **Foreign Keys in Edge DBs**| PlanetScale/Vitess limitations. | Use **Prisma Relation Mode**. |
| **`select *` Queries** | High latency and over-fetching. | Use **Explicit Typed Selection**. |

---

## 🐘 PostgreSQL 18 Excellence

We prioritize native 2026 features for performance:
-   **UUIDv7**: Sequential, globally unique IDs for faster indexing.
-   **Virtual Columns**: Zero-cost calculated fields.
-   **Temporal Constraints**: Range-based uniqueness for scheduling.
-   **AIO Subsystem**: Faster reads for massive datasets.

---

## 💎 Prisma 7 Elite Patterns

-   **TypedSQL**: High-performance, type-safe raw SQL integration.
-   **TypeScript Engine**: Native WASM execution for Edge compatibility.
-   **Prisma Extensions**: Clean orchestration of soft deletes and audit logs.
-   **Relation Emulation**: Integrity in FK-less environments.

---

## 🔒 Zero-Trust Data Security (RLS)

Every table MUST be protected by Row-Level Security.
-   **Standard**: `auth.uid() = user_id` for personal data.
-   **Advanced**: `EXISTS` checks for team and project permissions.
-   **CLS**: Use PostgreSQL Views to hide sensitive columns from public APIs.

---

## 📖 Reference Library

Detailed deep-dives into Database Integrity:

- [**PostgreSQL 18 Integrity**](./references/postgres-18-integrity.md): Advanced constraints and UUIDv7.
- [**Prisma 7 Architecture**](./references/prisma-7-architecture.md): TypedSQL and Edge-first patterns.
- [**Migration Safety**](./references/migration-safety-protocols.md): Zero-downtime deployment rules.
- [**RLS & Security**](./references/rls-and-security.md): Building a zero-trust database.

---

*Updated: January 22, 2026 - 18:10*

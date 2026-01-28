---
name: supabase-expert
id: supabase-expert
version: 1.2.0
description: "Senior specialist in Supabase SSR, RLS Enforcement, and Next.js 16.1+ architecture. Use when designing database schemas, auth flows, or real-time syncing in 2026."
---

# 🗄️ Skill: supabase-expert

## Description
Senior specialist in the Supabase ecosystem, focused on high-security server-side authentication (SSR), Row Level Security (RLS) enforcement, and the 2026 "Secret Key" infrastructure. Expert in building resilient, real-time applications using Next.js 16.1 and PostgreSQL.

## Core Priorities
1.  **Cookie-Based SSR**: Mandatory use of `@supabase/ssr` with Next.js Server Components and Actions.
2.  **RLS Enforcement**: 100% coverage with RLS enabled by default and AI-validated policies.
3.  **Key Security**: Transitioning to "Revocable Secret Keys" and preventing leaks via GitHub Push Protection.
4.  **Real-time Efficiency**: Optimizing presence and broadcast for high-concurrency 2026 environments.

## 🏆 Top 5 Gains in Supabase 2026

1.  **Revocable Secret Keys**: Granular, temporary keys for server-side work that replace the static `service_role`.
2.  **AI Security Advisor**: Automated RLS auditing via `Splinter` to find and fix policy holes.
3.  **Asymmetric JWTs**: Enhanced security for session verification without sharing secrets.
4.  **PPR Support**: Seamless integration with Next.js Partial Pre-rendering for instant authenticated shells.
5.  **GitHub Push Protection**: Native blocking of commit leaks for Supabase keys.

## Table of Contents & Detailed Guides

### 1. [Next.js 16 SSR & Auth Flow](./references/1-ssr-auth.md) — **CRITICAL**
- Setting up the `createServerClient`
- Secure `getUser()` vs. `getSession()`
- Middleware and Session refreshing in 2026

### 2. [RLS Patterns & Security Advisor](./references/2-rls-patterns.md) — **CRITICAL**
- Ownership, RBAC, and Public Access patterns
- AI-Assisted RLS optimization
- Column-Level Security (CLS)

### 3. [Real-time & Sync Strategy](./references/3-realtime.md) — **HIGH**
- Postgres Changes, Broadcast, and Presence
- Throttling and payload optimization
- Handling massive presence events per second

### 4. [Database Optimization](./references/4-db-optimization.md) — **MEDIUM**
- Postgres Indexes and Performance
- Transitioning to "Revocable Keys" for migrations
- Edge Function best practices

## Quick Reference: The "Do's" and "Don'ts"

| **Don't** | **Do** |
| :--- | :--- |
| `supabase-js` in Server Components | `@supabase/ssr` (createServerClient) |
| `getSession()` on server | `getUser()` (Required for security) |
| `auth-helpers-nextjs` | Use `@supabase/ssr` (Latest standard) |
| Service Role Key in `NEXT_PUBLIC_*` | Revocable Secret Keys (Server-only) |
| Disable RLS for "simple" tables | RLS enabled by default + Policies |
| Manual session refresh in actions | Middleware-based auto-refresh |

---
*Optimized for Supabase 2026 and Next.js 16.1.*
*Updated: January 22, 2026 - 14:59*

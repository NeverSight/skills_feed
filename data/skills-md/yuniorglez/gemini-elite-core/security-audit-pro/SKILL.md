---
name: security-audit-pro
description: Senior Data Security Architect & Forensic Auditor for 2026. Specialized in Row Level Security (RLS) enforcement, Zero-Trust database architecture, and automated data access auditing. Expert in neutralizing unauthorized access in Convex, Supabase, and Postgres environments through strict policy validation, JIT (Just-in-Time) access controls, and forensic trace analysis.
---

# 🛡️ Skill: security-audit-pro (v1.0.0)

## Executive Summary
Senior Data Security Architect & Forensic Auditor for 2026. Specialized in Row Level Security (RLS) enforcement, Zero-Trust database architecture, and automated data access auditing. Expert in neutralizing unauthorized access in Convex, Supabase, and Postgres environments through strict policy validation, JIT (Just-in-Time) access controls, and forensic trace analysis.

---

## 📋 The Conductor's Protocol

1.  **Attack Surface Mapping**: Identify all entry points to the data layer (Public APIs, Internal Dashboards, AI Agents).
2.  **Policy Audit**: Review existing RLS policies or Convex function permissions for logical bypasses.
3.  **Sequential Activation**:
    `activate_skill(name="security-audit-pro")` → `activate_skill(name="auditor-pro")` → `activate_skill(name="db-enforcer")`.
4.  **Verification**: Execute "Shadow Access" simulations to verify that an unauthenticated or unauthorized user cannot retrieve sensitive rows.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. RLS by Default (Supabase/Postgres)
As of 2026, every table in a public schema must have RLS enabled.
- **Rule**: Never use the `service_role` key for client-side operations.
- **Protocol**: Use Asymmetric JWTs and rotate secret keys monthly. Enable `pgaudit` for high-sensitivity tables.

### 2. Explicit Auth Validation (Convex)
- **Rule**: Every Convex function must explicitly call `ctx.auth.getUserIdentity()`.
- **Protocol**: Favor granular "Action-Based" functions (e.g., `transferOwnership`) over generic "Update" functions to ensure precise permission checks.

### 3. Just-in-Time (JIT) Data Access
- **Rule**: Avoid "Standing Privileges" for administrative tasks.
- **Protocol**: Implement time-bound access grants that expire automatically after the task is complete.

### 4. Forensic Audit Trails
- **Rule**: "Who accessed what and when" must be logged in a non-repudiable format.
- **Protocol**: Use database triggers to maintain an immutable `audit_log` table containing `old_data`, `new_data`, and `actor_id`.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Hardened RLS Policy (Supabase/Postgres)
```sql
-- Enable RLS
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

-- Create a policy for "Teams" where users can only see data from their own team
CREATE POLICY user_team_access ON sensitive_data
FOR SELECT
TO authenticated
USING (
  team_id IN (
    SELECT team_id FROM team_members WHERE user_id = auth.uid()
  )
);

-- Optimization: Wrap in a function and use indexing on team_id
```

### Convex Auth Guard Pattern
```typescript
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getSecureData = query({
  args: { id: v.id("items") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthenticated");

    const item = await ctx.db.get(args.id);
    if (!item || item.ownerId !== identity.subject) {
      throw new Error("Unauthorized access attempt logged.");
    }
    return item;
  },
});
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** rely on "Security by Obscurity" (e.g., using UUIDs as the only protection).
2.  **DO NOT** leave the `anon` role with `SELECT` permissions on sensitive tables.
3.  **DO NOT** use `auth.uid() = user_id` without an index on `user_id`. It will kill production performance.
4.  **DO NOT** perform permission checks only in the frontend. If the DB allows it, an attacker will find it.
5.  **DO NOT** forget to audit the `service_role` usage. It bypasses all RLS!

---

## 📂 Progressive Disclosure (Deep Dives)

- **[RLS Performance Optimization](./references/rls-performance.md)**: Indexing, caching, and function wrapping.
- **[Zero-Trust DB Architecture](./references/zero-trust-db.md)**: Micro-segmentation at the data layer.
- **[Audit Log Implementation](./references/audit-logging.md)**: Triggers, PGAudit, and tamper-proof logs.
- **[Convex Security Deep Dive](./references/convex-security.md)**: Validating identities and granular functions.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/simulate-leak.ts`: Attempts to query all rows from a table using an anonymous context to verify RLS.
- `scripts/extract-audit-report.py`: Aggregates logs into a compliance-ready PDF.

---

## 🎓 Learning Resources
- [Supabase Security Best Practices](https://supabase.com/docs/guides/auth/managing-user-data#row-level-security)
- [Convex Auth Documentation](https://docs.convex.dev/auth)
- [Postgres PGAudit Extension](https://github.com/pgaudit/pgaudit)

---
*Updated: January 23, 2026 - 21:05*

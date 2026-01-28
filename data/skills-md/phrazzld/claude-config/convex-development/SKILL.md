---
name: convex-development
description: |
  Apply Convex database best practices for cost optimization, performance, security, and architecture.
  Use when: building Convex backends, optimizing queries, handling embeddings/vector search,
  reviewing Convex code, designing schemas, planning migrations, or discussing Convex architecture.
  Keywords: Convex, real-time database, queries, mutations, actions, indexes, pagination,
  vector search, embeddings, schema, migrations, ctx.auth, convex-helpers, bandwidth.
---

# Convex Development

Best practices for robust, secure, performant, cost-effective Convex backends.

## Core Principle

**Deep modules via the `convex/model/` pattern.** Most logic should be plain TypeScript; query/mutation wrappers should be thin.

```
convex/
  _generated/         # MUST commit to git!
  model/              # Business logic (testable, reusable)
  users.ts            # Public API (thin wrappers)
  schema.ts
```

## Critical Rules

1. **ALWAYS commit `convex/_generated/`** - Required for type-checking, CI/CD, team productivity
2. **Index what you query** - `.withIndex()` not `.filter()` for efficient queries
3. **Paginate everything** - Never unbounded `.collect()` on user-facing queries
4. **Trust `ctx.auth` only** - Never user-provided auth data

## Quick Reference

| Need | Use |
|------|-----|
| Read data reactively | `query` |
| Write to database | `mutation` |
| External APIs, vector search | `action` |
| Scheduled tasks | `internalMutation` / `internalAction` |

## Anti-Patterns Scanner

Run `scripts/anti_patterns_scanner.py ./convex` to detect common issues.

## Detailed References

For comprehensive guidance, see:
- `references/cost-mitigation.md` - Bandwidth optimization, indexing, pagination
- `references/embeddings-vectors.md` - Vector search patterns, co-location decisions
- `references/query-performance.md` - Compound indexes, query segmentation, caching
- `references/security-access.md` - Auth patterns, RLS, RBAC, convex-helpers
- `references/schema-migrations.md` - Expand/Contract pattern, environment management
- `references/architectural-patterns.md` - File organization, state machines, naming

## Philosophy

- **Cost First**: Bandwidth is often the largest cost. Index aggressively, paginate everything.
- **Security First**: Never trust client input. Always use `ctx.auth`.
- **Reactivity is Power**: Use `useQuery` for real-time updates; don't forfeit with one-off fetches.
- **Type Safety End-to-End**: Leverage Convex's full type chain from database to UI.

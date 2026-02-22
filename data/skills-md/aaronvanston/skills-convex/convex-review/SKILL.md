---
name: convex-review
description: Comprehensive Convex code review checklist for production readiness. Use when auditing a Convex codebase before deployment, reviewing pull requests, or checking for security and performance issues in Convex functions.
---

# Convex Code Review

## Security Checklist

### 1. Argument AND Return Validators
- [ ] All public `query`, `mutation`, `action` have `args` validators
- [ ] All functions have `returns` validators
- [ ] No `v.any()` for sensitive data
- [ ] HTTP actions validate request body (Zod recommended)

**Search:** `query({`, `mutation({`, `action({` - check each has `args:` AND `returns:`

### 2. Error Handling
- [ ] Uses `ConvexError` for user-facing errors (not plain `Error`)
- [ ] Error codes are structured: `{ code: "NOT_FOUND", message: "..." }`
- [ ] No sensitive info leaked in error messages

**Search:** `throw new Error` should be `throw new ConvexError`

### 3. Access Control
- [ ] All public functions check `ctx.auth.getUserIdentity()` where needed
- [ ] Uses auth helpers (`requireAuth`, `requireRole`)
- [ ] No client-provided email/username for authorization
- [ ] Row-level access verified (ownership checks)

**Search:** `ctx.auth.getUserIdentity` should appear in most public functions

### 4. Internal Functions
- [ ] `ctx.runQuery`, `ctx.runMutation`, `ctx.runAction` use `internal.*` not `api.*`
- [ ] `ctx.scheduler.runAfter` uses `internal.*` not `api.*`
- [ ] Crons in `crons.ts` use `internal.*` not `api.*`

**Search:** `api.` in convex directory - should not be used for scheduling/running

### 5. Table Names in DB Calls
- [ ] All `ctx.db.get`, `patch`, `replace`, `delete` include table name as first arg

**Search:** `db.get(`, `db.patch(` - first arg should be quoted string

## Performance Checklist

### 6. Database Queries
- [ ] No `.filter()` on queries (use `.withIndex()` or filter in code)
- [ ] `.collect()` only with bounded results (<1000 docs)
- [ ] Pagination for large result sets

**Search:** `\.filter\(\(?q`, `\.collect\(`

### 7. Indexes
- [ ] No redundant indexes (`by_foo` + `by_foo_and_bar`)
- [ ] All filtered queries use `.withIndex()`
- [ ] Index names include all fields

**Review:** `schema.ts` index definitions

### 8. Date.now() in Queries
- [ ] No `Date.now()` in query functions
- [ ] Time filtering uses boolean fields or client-passed timestamps

### 9. Promise Handling
- [ ] All promises awaited (`ctx.scheduler`, `ctx.db.*`)

**ESLint:** `no-floating-promises`

## Architecture Checklist

### 10. Action Usage
- [ ] Actions have `"use node";` if using Node.js APIs
- [ ] `ctx.runAction` only when switching runtimes
- [ ] No sequential `ctx.runMutation`/`ctx.runQuery` (combine for consistency)

### 11. Code Organization
- [ ] Business logic in helper functions (`convex/model/`)
- [ ] Public API handlers are thin wrappers
- [ ] Auth helpers in `convex/lib/auth.ts`

### 12. Transaction Consistency
- [ ] Related reads in same query/mutation
- [ ] Batch operations in single mutation
- [ ] Mutations are idempotent

## Quick Regex Searches

| Issue | Regex | Fix |
|-------|-------|-----|
| `.filter()` | `\.filter\(\(?q` | Use `.withIndex()` |
| Missing returns | `handler:.*async` without `returns:` | Add `returns:` |
| Plain Error | `throw new Error\(` | Use `ConvexError` |
| Missing table name | `db\.(get\|patch)\([^"']` | Add table name |
| `Date.now()` in query | `Date\.now\(\)` | Remove from queries |
| `api.*` scheduling | `api\.[a-z]` | Use `internal.*` |

## Production Readiness

1. **Security**: Validators + ConvexError + Auth checks + Internal functions
2. **Performance**: Indexes + Bounded queries + No Date.now()
3. **Architecture**: Helper functions + Proper action usage + "use node"
4. **Code Quality**: Awaited promises + Table names + Return validators

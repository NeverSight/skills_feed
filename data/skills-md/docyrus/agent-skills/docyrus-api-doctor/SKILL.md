---
name: docyrus-api-doctor
description: Run after making Docyrus API changes to catch bugs, performance issues, and code quality problems. Use when implementing or modifying code that uses Docyrus collection hooks (.list, .get, .create, .update, .delete), direct RestApiClient calls, query payloads with filters/calculations/formulas/childQueries/pivots, or TanStack Query integration with Docyrus data sources. Triggers on tasks involving Docyrus API logic, data fetching, mutations, or query payload construction.
---

# Docyrus API Doctor

Post-implementation checklist for Docyrus API code. Run through each applicable check after writing or modifying API logic. Fix every issue found before considering the task complete.

**How to use:** After implementing API logic, scan the changed code against each check below. Skip checks that don't apply to the code at hand. For detailed explanations and fix examples, read `references/checklist-details.md`.

---

## BUG — Will Cause Errors

| # | Check | What to look for |
|---|-------|-----------------|
| B1 | **Missing `columns` parameter** | Any `.list()` or `.get()` call without a `columns` property. Without it, only `id` is returned. |
| B2 | **`limit: 0` in query payload** | `limit` set to `0` causes an API error. Remove `limit` entirely or set a positive integer. |
| B3 | **Child query key not in `columns`** | If `childQueries` defines key `orders`, the string `orders` must also appear in `columns`. |
| B4 | **Formula key not in `columns`** | If `formulas` defines key `total`, the string `total` must also appear in `columns`. |
| B5 | **Aggregation via `@` column syntax** | Using `count@field` or `sum@field` in columns. Use the `calculations` parameter instead. |
| B6 | **`distinctColumns` with `calculations`** | These are mutually exclusive. Use `calculations` for aggregation. |
| B7 | **Formula `extract` input count** | `extract` blocks must have exactly 1 input. |
| B8 | **Formula `not` operand count** | `not` blocks must have exactly 1 operand. |
| B9 | **Formula `and`/`or` operand count** | `and`/`or` blocks must have at least 2 operands. |
| B10 | **Formula math operand count** | Math operations (`+`, `-`, `*`, `/`, `%`) must have at least 2 operands. |
| B11 | **Formula `case` without `when`** | `case` expressions must have at least 1 `when` clause. |
| B12 | **Uncast literal in `jsonb_build_object`** | String literals inside `jsonb_build_object` need explicit `"cast": "text"` — auto-cast only works inside `concat`/`concat_ws`. |

## PERFORMANCE — Degrades Speed or Wastes Resources

| # | Check | What to look for |
|---|-------|-----------------|
| P1 | **Unnecessary `limit` on aggregation queries** | When using `calculations` without needing raw rows, don't send `limit`. Aggregation returns a single grouped result naturally. |
| P2 | **`fullCount` just to get a total count** | If you only need the count (not the rows), use `calculations: [{ func: 'count', field: 'id', name: 'total' }]` instead of `fullCount: true` with row fetching. |
| P3 | **Unnecessary `columns` on calculation-only queries** | When using `calculations` and only reading aggregated values, don't send `columns`. The calculation result is returned without needing column selection. |
| P4 | **Over-fetching columns** | Columns selected in `columns` but never read in the consuming code. Only select what you render or process. |
| P5 | **Large `limit` without pagination** | `limit` > 200 without `offset`/`fullCount` pagination risks slow responses and high memory usage. |
| P6 | **Missing `expand` causing N+1** | Rendering relation/enum/user field `.name` but not including that field in `expand`. Without `expand`, you get only the ID. |
| P7 | **Fetching rows for existence checks** | Fetching records just to check if any exist. Use `calculations` count instead. |
| P8 | **Redundant overlapping queries** | Multiple queries on the same data source fetching overlapping columns that could be combined into one. |

## CODE QUALITY — Causes Maintenance Pain

| # | Check | What to look for |
|---|-------|-----------------|
| Q1 | **Heavy `as` type assertions on responses** | Casting API responses with `as Array<...>` without runtime validation. Prefer typed collection return types or add validation. |
| Q2 | **Missing `enabled` on dependent queries** | `useQuery` that depends on a runtime value (e.g., `recordId`) but lacks `enabled: !!recordId`. The query fires with `undefined`. |
| Q3 | **No error handling on mutations** | `.create()`, `.update()`, `.delete()` calls without try/catch or error feedback to the user. |
| Q4 | **Missing query invalidation after mutations** | After create/update/delete, related query keys must be invalidated so lists refresh. |
| Q5 | **Serial cache invalidations** | Multiple `await queryClient.invalidateQueries(...)` in sequence. Use `Promise.all()` for independent invalidations. |
| Q6 | **Using deprecated `expandTypes`** | Replace with the `expand` parameter. |
| Q7 | **Hardcoded data source paths** | Raw `client.get('/v1/apps/base/data-sources/project/items')` instead of using generated collection hooks. |
| Q8 | **`distinctColumns` without `orderBy`** | `distinctColumns` requires `orderBy` to define which row wins per group. |

---

## How to Run

1. Identify all files changed in this task that contain Docyrus API calls
2. For each file, scan for `.list(`, `.get(`, `.create(`, `.update(`, `.delete(`, `client.get(`, `client.post(`, `client.patch(`, `client.delete(`
3. Check each call site against the BUG checks (B1-B12)
4. Check query payloads against PERFORMANCE checks (P1-P8)
5. Check surrounding code (hooks, error handling, invalidation) against CODE QUALITY checks (Q1-Q8)
6. Fix all issues found, starting with BUG category

## References

- **`references/checklist-details.md`** — Detailed explanation, detection pattern, and before/after fix example for every check item

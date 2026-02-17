---
name: docyrus-app-dev
description: Build React TypeScript web applications using Docyrus as a backend. Use when creating or modifying apps that authenticate with Docyrus OAuth2, fetch/mutate data via the @docyrus/api-client library, use auto-generated collections for CRUD operations, or build queries with filters, aggregations, formulas, pivots, and child queries against Docyrus data sources. Triggers on tasks involving @docyrus/api-client, @docyrus/signin, Docyrus collections, data source queries, or Docyrus-backed React app development.
---

# Docyrus App Developer

Build React TypeScript web apps with Docyrus as the backend. Authenticate via OAuth2 PKCE, query data sources with powerful filtering/aggregation, and follow established patterns.

## Tech Stack

- React 19 + TypeScript + Vite
- TanStack Router (code-based), TanStack Query (server state)
- Tailwind CSS v4, shadcn/ui components
- `@docyrus/api-client` (REST client) + `@docyrus/signin` (auth provider)
- Auto-generated collections from OpenAPI spec

## Quick Start: New App Setup

1. Wrap root with `DocyrusAuthProvider`:

```tsx
import { DocyrusAuthProvider } from '@docyrus/signin'

<DocyrusAuthProvider
  apiUrl={import.meta.env.VITE_API_BASE_URL}
  clientId={import.meta.env.VITE_OAUTH2_CLIENT_ID}
  redirectUri={import.meta.env.VITE_OAUTH2_REDIRECT_URI}
  scopes={['offline_access', 'Read.All', 'DS.ReadWrite.All', 'Users.Read']}
  callbackPath="/auth/callback"
>
  <QueryClientProvider client={queryClient}>
    <RouterProvider router={router} />
  </QueryClientProvider>
</DocyrusAuthProvider>
```

2. In App.tsx, sync API client for collections:

```tsx
const { status } = useDocyrusAuth()
const client = useDocyrusClient()

useEffect(() => {
  if (client) setApiClient(client)
}, [client])

if (status === 'loading') return <Spinner />
if (status === 'unauthenticated') return <SignInButton />
```

3. Use collections in hooks:

```tsx
const { data: projects } = useQuery({
  queryKey: ['projects'],
  queryFn: () => baseProjectCollection.list({
    columns: ['name', 'status', 'record_owner(firstname,lastname)'],
    filters: { rules: [{ field: 'status', operator: '!=', value: 'archived' }] },
    orderBy: 'created_on DESC',
    limit: 50,
  }),
})
```

## Critical Rules

1. **Always send `columns`** in `.list()` and `.get()` calls. Without it, only `id` is returned.
2. **Collections only work after auth** — `setApiClient(client)` must be called first.
3. **Data source endpoints are dynamic** — they only exist if the data source is defined in the tenant's OpenAPI spec.
4. **Use `id` field** for `count` calculations. Use the actual field slug for `sum`, `avg`, `min`, `max`.
5. **Child query keys must appear in `columns`** — e.g., if childQuery key is `orders`, include `'orders'` in the columns array.
6. **Formula keys must appear in `columns`** — e.g., if formula key is `total`, include `'total'` in the columns array.
7. **Use `UsersCollection.getMyInfo()`** for current user profile, not a direct API call.

## Regenerating Collections After Schema Changes

When data sources or fields are created, updated, or deleted via the `docyrus-architect` MCP tools, the app's auto-generated collections become stale. To resync:

1. Call `regenerate_openapi_spec` (architect MCP) to rebuild and upload the tenant's OpenAPI spec
2. Download the new spec into the repo, overwriting the existing file:
   ```bash
   curl -o openapi.json "<publicUrl returned from step 1>"
   ```
3. Regenerate collections:
   ```bash
   pnpx @docyrus/tanstack-db-generator openapi.json
   ```

Always run all three steps together — a stale `openapi.json` or outdated collections will cause missing or incorrect endpoints at runtime.

## Collection CRUD Methods

Every generated collection provides:

```typescript
collection.list(params?: ICollectionListParams)  // Query with filters, sort, pagination
collection.get(id, { columns })                   // Single record
collection.create(data)                           // Create
collection.update(id, data)                       // Partial update
collection.delete(id)                             // Delete one
collection.deleteMany({ recordIds })              // Delete many
```

API endpoint pattern: `/v1/apps/{appSlug}/data-sources/{slug}/items`

## Query Capabilities Summary

The `.list()` method supports:

| Feature | Purpose |
|---------|---------|
| `columns` | Select fields, expand relations `field(subfields)`, alias `alias:field`, spread `...field()` |
| `filters` | Nested AND/OR groups with 50+ operators (comparison, date shortcuts, user-related) |
| `filterKeyword` | Full-text search |
| `orderBy` | Sort by fields with direction, including related fields |
| `limit`/`offset` | Pagination (default 100) |
| `fullCount` | Return total count alongside results |
| `calculations` | Aggregations: count, sum, avg, min, max with grouping |
| `formulas` | Computed virtual columns (simple functions, block AST, correlated subqueries) |
| `childQueries` | Fetch related child records as nested JSON arrays |
| `pivot` | Cross-tab matrix queries with date range series |
| `expand` | Return full objects for relation/user/enum fields instead of IDs |

**For query details, read**: `references/query-guide.md`

## TanStack Query Pattern

```typescript
// Query hook
function useItems(params?: ICollectionListParams) {
  return useQuery({
    queryKey: ['items', 'list', params],
    queryFn: () => collection.list({ columns: COLUMNS, ...params }),
  })
}

// Mutation hook
function useCreateItem() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: Record<string, unknown>) => collection.create(data),
    onSuccess: () => { void qc.invalidateQueries({ queryKey: ['items'] }) },
  })
}
```

## References

Read these files when you need detailed information:

- **`references/api-client-and-auth.md`** — RestApiClient API, @docyrus/signin hooks, auth provider config, interceptors, error handling, SSE/streaming, file upload/download
- **`references/query-guide.md`** — Full query payload reference: column syntax, all filter operators, aggregations, simple/block/subquery formulas, child queries, pivot tables, expand
- **`references/collections-and-patterns.md`** — Generated collection structure, UsersCollection, TanStack Query/mutation hook patterns, query key factories, app bootstrap flow, routing setup, API endpoints

---
name: docyrus-api-dev
description: Develop applications using the Docyrus API with @docyrus/api-client and @docyrus/signin libraries. Use when building apps that authenticate with Docyrus OAuth2 (PKCE, iframe, client credentials, device code), make REST API calls to Docyrus data source endpoints, or construct query payloads with filters, aggregations, formulas, pivots, and child queries. Triggers on tasks involving Docyrus API integration, @docyrus/api-client usage, @docyrus/signin authentication, data source query building, or Docyrus REST endpoint consumption.
---

# Docyrus API Developer

Integrate with the Docyrus API using `@docyrus/api-client` (REST client) and `@docyrus/signin` (React auth provider). Authenticate via OAuth2 PKCE, query data sources with powerful filtering/aggregation, and consume REST endpoints.

## Authentication Quick Start

### React Apps — Use @docyrus/signin

```tsx
import { DocyrusAuthProvider, useDocyrusAuth, useDocyrusClient, SignInButton } from '@docyrus/signin'

// 1. Wrap root
<DocyrusAuthProvider
  apiUrl={import.meta.env.VITE_API_BASE_URL}
  clientId={import.meta.env.VITE_OAUTH2_CLIENT_ID}
  redirectUri={import.meta.env.VITE_OAUTH2_REDIRECT_URI}
  scopes={['offline_access', 'Read.All', 'DS.ReadWrite.All', 'Users.Read']}
  callbackPath="/auth/callback"
>
  <App />
</DocyrusAuthProvider>

// 2. Use hooks
function App() {
  const { status, signOut } = useDocyrusAuth()
  const client = useDocyrusClient()  // RestApiClient | null

  if (status === 'loading') return <Spinner />
  if (status === 'unauthenticated') return <SignInButton />

  // client is ready — make API calls
  const user = await client!.get('/v1/users/me')
}
```

### Non-React / Server — Use OAuth2Client Directly

```typescript
import { RestApiClient, OAuth2Client, OAuth2TokenManagerAdapter, BrowserOAuth2TokenStorage } from '@docyrus/api-client'

const tokenStorage = new BrowserOAuth2TokenStorage(localStorage)
const oauth2 = new OAuth2Client({
  baseURL: 'https://api.docyrus.com',
  clientId: 'your-client-id',
  redirectUri: 'http://localhost:3000/callback',
  usePKCE: true,
  tokenStorage,
})

// Auth Code flow
const { url } = await oauth2.getAuthorizationUrl({ scope: 'openid offline_access Users.Read' })
window.location.href = url
// After redirect:
const tokens = await oauth2.handleCallback(window.location.href)

// Create API client with auto-refresh
const client = new RestApiClient({
  baseURL: 'https://api.docyrus.com',
  tokenManager: new OAuth2TokenManagerAdapter(tokenStorage, async () => {
    return (await oauth2.refreshAccessToken()).accessToken
  }),
})
```

## API Endpoints

### Data Source Items (Dynamic per tenant)
```
GET    /v1/apps/{appSlug}/data-sources/{slug}/items          — List with query payload
GET    /v1/apps/{appSlug}/data-sources/{slug}/items/{id}     — Get one
POST   /v1/apps/{appSlug}/data-sources/{slug}/items          — Create
PATCH  /v1/apps/{appSlug}/data-sources/{slug}/items/{id}     — Update
DELETE /v1/apps/{appSlug}/data-sources/{slug}/items/{id}     — Delete one
DELETE /v1/apps/{appSlug}/data-sources/{slug}/items          — Delete many (body: { recordIds })
```

Endpoints exist only if the data source is defined in the tenant. Check the tenant's OpenAPI spec at `GET /v1/api/openapi.json`.

### System Endpoints (Always Available)
```
GET    /v1/users          — List users
POST   /v1/users          — Create user
GET    /v1/users/me       — Current user profile
PATCH  /v1/users/me       — Update current user
```

### Making API Calls

```typescript
// List items with query payload
const items = await client.get('/v1/apps/base/data-sources/project/items', {
  columns: 'name, status, record_owner(firstname,lastname)',
  filters: { rules: [{ field: 'status', operator: '!=', value: 'archived' }] },
  orderBy: 'created_on DESC',
  limit: 50,
})

// Get single item
const item = await client.get('/v1/apps/base/data-sources/project/items/uuid-here', {
  columns: 'name, description, status',
})

// Create
const newItem = await client.post('/v1/apps/base/data-sources/project/items', {
  name: 'New Project',
  status: 'status-enum-id',
})

// Update
await client.patch('/v1/apps/base/data-sources/project/items/uuid-here', {
  name: 'Updated Name',
})

// Delete
await client.delete('/v1/apps/base/data-sources/project/items/uuid-here')
```

## Query Payload Summary

The GET items endpoint accepts a powerful query payload:

| Feature | Purpose |
|---------|---------|
| `columns` | Select fields, expand relations `field(subfields)`, alias `alias:field`, spread `...field()` |
| `filters` | Nested AND/OR groups with 50+ operators (comparison, date shortcuts, user-related) |
| `filterKeyword` | Full-text search across all searchable fields |
| `orderBy` | Sort by fields with direction, including related fields |
| `limit`/`offset` | Pagination (default limit: 100) |
| `fullCount` | Return total matching count alongside results |
| `calculations` | Aggregations: count, sum, avg, min, max with grouping |
| `formulas` | Computed virtual columns (simple functions, block AST, correlated subqueries) |
| `childQueries` | Fetch related child records as nested JSON arrays |
| `pivot` | Cross-tab matrix queries with date range series |
| `expand` | Return full objects for relation/user/enum fields instead of IDs |

**For full query reference, read**: `references/query-and-formulas.md`

## Critical Rules

1. **Always send `columns`** in list/get calls. Without it, only `id` is returned.
2. **Data source endpoints are dynamic** — they exist only for data sources defined in the tenant.
3. **Use `id` field** for `count` calculations. Use the actual field slug for `sum`, `avg`, `min`, `max`.
4. **Child query keys must appear in `columns`** — if childQuery key is `orders`, include `orders` in columns.
5. **Formula keys must appear in `columns`** — if formula key is `total`, include `total` in columns.
6. **Filter by related field** using `rel_{{relation_field}}/{{field}}` syntax.

## References

Read these files when you need detailed information:

- **`references/api-client.md`** — Full RestApiClient API, OAuth2Client (all flows: PKCE, client credentials, device code), token managers, interceptors, error classes, SSE/streaming, file upload/download, HTML to PDF, retry logic
- **`references/authentication.md`** — @docyrus/signin React provider, useDocyrusAuth/useDocyrusClient hooks, SignInButton, standalone vs iframe auth modes, env vars, module-level API client pattern
- **`references/query-and-formulas.md`** — Complete query payload reference: column syntax, all 50+ filter operators, aggregations, simple formulas, block (AST) formulas with all block kinds, subquery formulas, child queries, pivot tables, expand, allowed SQL functions, cast types, full examples

---
name: frontic-implementation
description: Create, configure, and use Frontic blocks, listings, and pages for e-commerce data. Use when working with Frontic configuration, building product/category pages, creating data sources, or integrating the Frontic client. Covers resource decision-making, block/listing creation guidelines, and client usage patterns.
---

# Frontic Implementation and Configuration

Use this skill when autonomously creating or managing blocks, listings, and pages based on user requests. **Prefer Frontic data sources over mocked data** at all times.

## Before You Start

Use the `fetch_api_call` tool to inspect the data structure of any block, listing, or page before using it. This prevents displaying non-existent content or illegible IDs to users.

---

## 1. Resource Decision Making

Before creating new blocks or listings, analyze the current Frontic configuration:

- **Existing blocks** that could be reused or extended
- **Existing listings** that match the user's requirements — verify parameter compatibility and data structure
- **Available storages** containing relevant data

### Reuse vs Extend vs Create

| Scenario                                         | Action                                |
| ------------------------------------------------ | ------------------------------------- |
| Exact match (same user journey, same parameters) | Reuse                                 |
| Close but not perfect fit                        | Extend (if appropriate) or create new |
| Different parameters or intent                   | Create new                            |

### Rules (Non-Negotiable)

- **Never force-fit**: Do NOT use a block or listing for a use case it wasn't designed for, even as a workaround.
- **Parameter compatibility is absolute**: If a listing requires parameters (e.g. `categoryId`) and the user's use case doesn't provide them (e.g. global search), create a new listing — never use dummy/placeholder values.
- **User intent is primary**: Match the user's stated intent and user journey exactly.
- **Document your reasoning**: Briefly explain why you reused, extended, or created a resource.

> ⚠️ **Warning:** If you find yourself using dummy/default parameters to make an existing resource work for a different use case, STOP. Create a new resource instead.

---

## 2. Creating Blocks and Listings

### Block Creation

- **Analyze data structure**: Identify the single record/entity the block represents
- **Define comprehensive schema**: Include all relevant e-commerce fields
- **Plan for variations**: Account for product types, categories, etc.

**Common blocks:** `ProductDetail`, `CategoryDetail`, `UserProfile`, `OrderDetail`, `ReviewDetail`, `BrandDetail`

### Listing Creation

- **Identify collection type**: Products, categories, blog posts, etc.
- **Identify embedded block**: The listing must reference a block already created in the project
- **Configure filtering**: Price, category, brand, ratings, availability
- **Plan sorting**: Price, popularity, newest, ratings
- **Enable search**: Where relevant (description, title)
- **Make parameters optional for global use**: For listings that serve both global search and scoped contexts, configure parameters as optional with default values:

```json
{
  "name": "categoryId",
  "dataType": "string",
  "required": false,
  "defaultValue": "root-id"
}
```

This allows `listing("GlobalSearch", {})` for global search and `listing("GlobalSearch", { categoryId: "xyz" })` for scoped queries.

**Common listings:** `ProductListing`, `CategoryListing`, `OrderListing`, `ReviewListing`, `SearchResults`

### Regenerate the Client

After creating or updating a block or listing, always regenerate the Frontic Client:

```bash
npx @frontic/cli@latest generate
```

---

## 3. Frontic Client Usage

Import the client (resolve `.frontic/` path relative to the application root):

```typescript
import client from '../../.frontic/generated-client'
```

### Blocks (single items by key)

Single items are always identified by a key. Don't make up placeholder keys like 'root-category', always use actual keys from the storage associated with the block.

```typescript
const data = await client.block(
  'CategoryDetail',
  'a3f4b5c6-d7e8-49ab-9c2d-3e4f5e6d7c8b'
)
const data = await client.block(
  'ProductDetail',
  '123e4567-e89b-12d3-a456-426614174000'
)
```

### Listings (collections with filtering, sorting, pagination)

Refer to `.frontic/query-types.ts` and `.frontic/fetch-api.d.ts` for filters and sort options.

```typescript
const products = await client.listing('ProductList', {
  categoryId: 'e72b0f5e-1c3d-4a7e-913a-2e4c95cd8f31'
})

const results = await client.listing(
  'ProductList',
  { categoryId: '...' },
  {
    query: {
      filter: [
        {
          type: 'and',
          filter: [
            { type: 'equals', field: 'attributes.size', value: '10' },
            { type: 'range', field: 'price.amount', from: 10 }
          ]
        },
        { type: 'range', field: 'price.amount', from: 2000, to: 10000 },
        { type: 'equals', field: 'sale', value: true }
      ],
      sort: { field: 'price.amount', order: 'asc' },
      search: 'Red',
      page: 1,
      limit: 20
    }
  }
)
```

### Pages (retrieve by route)

```typescript
// The route path is the full path including the domain without the protocol
const pageData = await client.page('demo-shop.com/uk/women/shoes')
```

### Type Reference

Check `.frontic/generated-types.d.ts` and `.frontic/query-types.ts` for blocks, listings, pages, parameters, and return types.

---

## 4. Page Integration and Dynamic Updates

### Use Pages for Dynamic Routing

Always use pages for dynamic routing unless the user requests otherwise. Pages are containers for blocks identified by slug. Page slugs include domain, locale (if configured), and path. Blocks can have `pageRoute` fields for route information.

For root-level dynamic routing, create a catch-all page that calls `client.page()` with the assembled slug. Handle the root case `/` separately (e.g. with a hardcoded block).

### Page Structure Hierarchy

```
Page (e.g. CategoryDetail)
 ├── Block (e.g. CategoryDetailShopware)
 └── Nested Listing (e.g. ProductListShopware)
```

### Implementation Pattern

1. **Initial load**: Use `client.page()` or `client.block()` — provides full page context and embedded content.
2. **Filtering/sorting/pagination**: Use `client.listing()` — `client.page()` and `client.block()` do **not** accept query parameters.

```typescript
// 1. Initial page load
const pageData = await client.page('domain.com/category-name')

// 2. Dynamic updates — extract params, call embedded listing directly
const categoryId = pageData.data.key
const filteredData = await client.listing('ProductListShopware', { categoryId }, {
  query: { filter: [...], sort: {...}, page: 2 }
})
```

**Summary:** Always start with `client.page()` for initial load. For dynamic updates, identify the nested listing, extract required parameters from page data, and call `client.listing()` with query parameters. Update only the listing portion of component state.

---

## 5. Field Configuration

### Filter Field Naming with Paths

When a filter field is configured with a `path` parameter, you **must** use the full dotted path in queries:

```json
// Configuration:
{ "name": "price", "source": "blockField", "path": "amount" }

// In queries — use "price.amount", NOT "price":
{ "type": "range", "field": "price.amount", "from": 2000, "to": 10000 }
```

**Rule:** If a filter field has `path: "X"`, always reference it as `fieldName.X` in queries.

### Sort Field Configuration

Frontic does **not** support duplicate sort field names with different directions. Add each sort field once — the API automatically supports both `asc` and `desc`. Specify direction at query time:

```typescript
// One sort field configured, direction chosen per query:
sort: { field: 'price.amount', order: 'asc' }  // or 'desc'
```

### Field Source Selection

Always prefer `blockField` over `storageField` when configuring search, filter, and sort fields:

- Block fields are already exposed and configured
- Storage fields may not be accessible or properly typed
- Block fields maintain consistency with the nested block structure

```javascript
// Prefer:
{ type: "filter", name: "price", source: "blockField" }

// Avoid:
{ type: "filter", name: "price", source: "storageField" }
```

### Validating Field Paths

Before using a filter or sort field, verify the exact name:

1. Use `list_resources` to see configured fields
2. Use `fetch_api_call` to test the listing and inspect the response structure

```javascript
// Test listing response reveals field structure:
// items: [{ price: { amount: 49595 } }]
// → filter field is "price.amount"
```

---

## 6. Price Format

Frontic prices use an integer format with precision:

```json
{ "amount": 49595, "currency": "EUR", "precision": 2, "ref": 0 }
```

Display calculation:

```javascript
const displayPrice = price.amount / Math.pow(10, price.precision)
// 49595 / 100 = 495.95
```

---

## 7. Troubleshooting

### Browser and Build Cache

After regenerating the client, caching can cause stale code to persist.

- **Clear the framework build cache** (e.g. `.next/`, `.nuxt/`, `dist/`)
- **Hard refresh browser:** Cmd+Shift+R (Mac) / Ctrl+Shift+F5 (Windows/Linux)
- **Disable cache in DevTools:** Network tab → "Disable cache"

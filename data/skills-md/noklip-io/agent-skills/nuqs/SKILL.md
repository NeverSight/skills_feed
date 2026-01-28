---
name: nuqs
description: Use when implementing URL query state in React, managing search params, syncing state with URL, building filterable/sortable lists, pagination with URL state, or using nuqs/useQueryState/useQueryStates hooks in Next.js, Remix, React Router, or plain React.
---

# nuqs Best Practices

Type-safe URL query state management for React. Like `useState`, but stored in the URL.

## Setup (Required First)

Wrap your app with the appropriate adapter:

```tsx
// Next.js App Router - app/layout.tsx
import { NuqsAdapter } from 'nuqs/adapters/next/app'

export default function RootLayout({ children }) {
  return <NuqsAdapter>{children}</NuqsAdapter>
}

// Next.js Pages Router - pages/_app.tsx
import { NuqsAdapter } from 'nuqs/adapters/next/pages'

// React SPA (Vite/CRA)
import { NuqsAdapter } from 'nuqs/adapters/react'

// Remix - app/root.tsx
import { NuqsAdapter } from 'nuqs/adapters/remix'

// React Router v6/v7
import { NuqsAdapter } from 'nuqs/adapters/react-router'
```

### Global Options

```tsx
import { throttle } from 'nuqs'

<NuqsAdapter
  defaultOptions={{
    shallow: false,        // notify server by default
    scroll: true,          // scroll to top on change
    clearOnDefault: true,  // remove param when equals default
    limitUrlUpdates: throttle(250)  // throttle URL updates
  }}
>
  {children}
</NuqsAdapter>
```

## Core API

### Single Parameter

```tsx
'use client'
import { useQueryState, parseAsInteger } from 'nuqs'

// String (default) - returns null | string
const [search, setSearch] = useQueryState('q')

// With parser + default (recommended)
const [page, setPage] = useQueryState('page', parseAsInteger.withDefault(1))

// Updates
setSearch('hello')           // ?q=hello
setSearch(null)              // removes param
setPage(p => p + 1)          // functional update
await setPage(5)             // returns Promise<URLSearchParams>
```

### Multiple Parameters

```tsx
import { useQueryStates, parseAsInteger, parseAsString } from 'nuqs'

const [filters, setFilters] = useQueryStates({
  q: parseAsString.withDefault(''),
  page: parseAsInteger.withDefault(1),
  sort: parseAsString.withDefault('date')
})

// Partial updates
setFilters({ page: 1, sort: 'name' })

// Await batch update
const params = await setFilters({ page: 2 })
params.get('page')  // '2'
```

## Built-in Parsers

| Parser | Type | Example URL |
|--------|------|-------------|
| `parseAsString` | `string` | `?q=hello` |
| `parseAsInteger` | `number` | `?page=1` |
| `parseAsFloat` | `number` | `?price=9.99` |
| `parseAsHex` | `number` | `?color=ff0000` |
| `parseAsBoolean` | `boolean` | `?active=true` |
| `parseAsIsoDateTime` | `Date` | `?date=2024-01-15T10:30:00Z` |
| `parseAsTimestamp` | `Date` | `?t=1705312200000` |
| `parseAsArrayOf(parser)` | `T[]` | `?tags=a,b,c` |
| `parseAsArrayOf(parser, ';')` | `T[]` | `?ids=1;2;3` (custom separator) |
| `parseAsJson<T>()` | `T` | `?data={"key":"value"}` |
| `parseAsStringEnum(values)` | `enum` | `?status=active` |
| `parseAsStringLiteral(arr)` | `literal` | `?sort=asc` |
| `parseAsNumberLiteral(arr)` | `literal` | `?dice=6` |

### Enum & Literal Examples

```tsx
// String enum
enum Status { Active = 'active', Inactive = 'inactive' }
const [status] = useQueryState('status',
  parseAsStringEnum(Object.values(Status)).withDefault(Status.Active)
)

// String literal (type-safe)
const sortOptions = ['asc', 'desc'] as const
const [sort] = useQueryState('sort',
  parseAsStringLiteral(sortOptions).withDefault('asc')
)

// Number literal
const diceSides = [1, 2, 3, 4, 5, 6] as const
const [dice] = useQueryState('dice',
  parseAsNumberLiteral(diceSides).withDefault(1)
)
```

### Arrays

```tsx
// Default comma separator: ?tags=react,typescript,nuqs
const [tags, setTags] = useQueryState('tags',
  parseAsArrayOf(parseAsString).withDefault([])
)

// Custom separator: ?ids=1;2;3
const [ids] = useQueryState('ids',
  parseAsArrayOf(parseAsInteger, ';').withDefault([])
)
```

## Options

```tsx
useQueryState('key', parseAsString.withOptions({
  history: 'push',       // 'push' | 'replace' (default)
  shallow: false,        // true (default) = client only, false = notify server
  scroll: false,         // scroll to top on change
  throttleMs: 500,       // throttle URL updates (min 50ms)
  clearOnDefault: true,  // remove param when equals default (default: true)
  startTransition,       // React useTransition for loading states
}))
```

**Options precedence**: call-level > parser-level > hook-level > global adapter

```tsx
// Parser-level options
const parser = parseAsString.withOptions({ shallow: false })

// Hook-level options
const [q, setQ] = useQueryState('q', parser, { history: 'push' })

// Call-level override (highest priority)
setQ('value', { shallow: true })
```

## Functional Updates & Batching

```tsx
// Functional updates
setCount(c => c + 1)
setCount(c => c * 2)  // Both batched in same tick

// Chained functional updates execute in order
function onClick() {
  setCount(x => x + 1)  // 0 → 1
  setCount(x => x * 2)  // 1 → 2
}

// Await updates
const search = await setFilters({ page: 2 })
search.get('page')  // '2'
```

## Loading States with useTransition

```tsx
'use client'
import { useTransition } from 'react'
import { useQueryState, parseAsString } from 'nuqs'

function Search({ results }) {
  const [isLoading, startTransition] = useTransition()

  const [query, setQuery] = useQueryState('q',
    parseAsString.withOptions({
      startTransition,  // enables loading state
      shallow: false    // required for server updates
    })
  )

  return (
    <>
      <input value={query ?? ''} onChange={e => setQuery(e.target.value)} />
      {isLoading ? <Spinner /> : <Results data={results} />}
    </>
  )
}
```

## Custom Parsers

### Basic Custom Parser

```tsx
// Simple date parser
const parseAsDate = {
  parse: (value: string) => new Date(value),
  serialize: (date: Date) => date.toISOString().split('T')[0]
}

const [date, setDate] = useQueryState('date', parseAsDate)
```

### With createParser (for reference types)

For non-primitive types, provide `eq` function for `clearOnDefault` to work:

```tsx
import { createParser, parseAsStringLiteral } from 'nuqs'

// Date with equality check
const parseAsDate = createParser({
  parse: (value: string) => new Date(value.slice(0, 10)),
  serialize: (date: Date) => date.toISOString().slice(0, 10),
  eq: (a: Date, b: Date) => a.getTime() === b.getTime()
})

// Complex type (e.g., TanStack Table sort state)
// URL: ?sort=name:asc → { id: 'name', desc: false }
const parseAsSort = createParser({
  parse(query) {
    const [id = '', dir = ''] = query.split(':')
    return { id, desc: dir === 'desc' }
  },
  serialize(value) {
    return `${value.id}:${value.desc ? 'desc' : 'asc'}`
  },
  eq(a, b) {
    return a.id === b.id && a.desc === b.desc
  }
})
```

## Server Components (Next.js)

```tsx
// lib/searchParams.ts
import { createSearchParamsCache, parseAsInteger, parseAsString } from 'nuqs/server'

export const searchParamsCache = createSearchParamsCache({
  q: parseAsString.withDefault(''),
  page: parseAsInteger.withDefault(1)
})

// app/search/page.tsx (Server Component)
import { searchParamsCache } from '@/lib/searchParams'
import type { SearchParams } from 'nuqs/server'

type Props = { searchParams: Promise<SearchParams> }

export default async function Page({ searchParams }: Props) {
  // ⚠️ Must call parse() - don't forget!
  const { q, page } = await searchParamsCache.parse(searchParams)
  return <Results query={q} page={page} />
}

// Nested server component - no props needed
function NestedComponent() {
  const page = searchParamsCache.get('page')  // type-safe!
  return <span>Page {page}</span>
}
```

## Reusable Patterns

### Shared Parser Definitions

```tsx
// lib/parsers.ts
export const paginationParsers = {
  page: parseAsInteger.withDefault(1),
  limit: parseAsInteger.withDefault(20),
  sort: parseAsString.withDefault('createdAt'),
  order: parseAsStringLiteral(['asc', 'desc'] as const).withDefault('desc')
}

// Component
const [pagination, setPagination] = useQueryStates(paginationParsers)
```

### URL Key Mapping

```tsx
const [coords, setCoords] = useQueryStates(
  {
    latitude: parseAsFloat.withDefault(0),
    longitude: parseAsFloat.withDefault(0)
  },
  {
    urlKeys: { latitude: 'lat', longitude: 'lng' }
  }
)
// URL: ?lat=45.5&lng=-122.6
// Code: coords.latitude, coords.longitude
```

### Custom Hook

```tsx
// hooks/useFilters.ts
export function useFilters() {
  return useQueryStates({
    search: parseAsString.withDefault(''),
    category: parseAsString,
    minPrice: parseAsFloat,
    maxPrice: parseAsFloat,
    inStock: parseAsBoolean.withDefault(false)
  })
}

// Component
const [filters, setFilters] = useFilters()
```

## Testing

```tsx
import { withNuqsTestingAdapter, type UrlUpdateEvent } from 'nuqs/adapters/testing'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

it('updates URL on click', async () => {
  const user = userEvent.setup()
  const onUrlUpdate = vi.fn<[UrlUpdateEvent]>()

  render(<CounterButton />, {
    wrapper: withNuqsTestingAdapter({
      searchParams: '?count=1',
      onUrlUpdate
    })
  })

  await user.click(screen.getByRole('button'))

  expect(screen.getByRole('button')).toHaveTextContent('count is 2')
  expect(onUrlUpdate).toHaveBeenCalledOnce()

  const event = onUrlUpdate.mock.calls[0]![0]!
  expect(event.queryString).toBe('?count=2')
  expect(event.searchParams.get('count')).toBe('2')
  expect(event.options.history).toBe('push')
})
```

## Critical Mistakes to Avoid

### 1. Missing Adapter
```tsx
// ❌ Error: nuqs requires an adapter
useQueryState('q')

// ✅ Wrap app in NuqsAdapter first (see Setup section)
```

### 2. Wrong Adapter for Framework
```tsx
// ❌ Using app router adapter in pages router
import { NuqsAdapter } from 'nuqs/adapters/next/app'  // Wrong!

// ✅ Match adapter to your router
import { NuqsAdapter } from 'nuqs/adapters/next/pages'
```

### 3. Missing Suspense (Next.js App Router)
```tsx
// ❌ Hydration error
export default function Page() {
  const [q] = useQueryState('q')
  return <div>{q}</div>
}

// ✅ Wrap client components in Suspense
export default function Page() {
  return (
    <Suspense fallback={<Loading />}>
      <SearchClient />
    </Suspense>
  )
}
```

### 4. Same Key, Different Parsers
```tsx
// ❌ Conflicts - last update wins with wrong type
const [intVal] = useQueryState('foo', parseAsInteger)
const [floatVal] = useQueryState('foo', parseAsFloat)

// ✅ One parser per key, share via custom hook
function useFoo() {
  const [val, setVal] = useQueryState('foo', parseAsFloat)
  return { float: val, int: Math.floor(val ?? 0), setVal }
}
```

### 5. Forgetting to Parse on Server
```tsx
// ❌ Returns cache object, not values
const values = searchParamsCache  // Wrong!

// ✅ Call parse() with searchParams prop
const values = await searchParamsCache.parse(searchParams)
```

### 6. Server Component with Client Hook
```tsx
// ❌ useQueryState only works in client components
export default function Page() {  // Server component
  const [q] = useQueryState('q')  // Error!
}

// ✅ Use createSearchParamsCache for server, useQueryState for client
```

### 7. Not Handling Null Without Default
```tsx
// ❌ Tedious null handling
const [count, setCount] = useQueryState('count', parseAsInteger)
setCount(c => (c ?? 0) + 1)  // Must handle null every time

// ✅ Use withDefault
const [count, setCount] = useQueryState('count', parseAsInteger.withDefault(0))
setCount(c => c + 1)  // Always a number
```

### 8. Lossy Serialization
```tsx
// ❌ Loses precision on reload
const geoParser = {
  parse: parseFloat,
  serialize: v => v.toFixed(2)  // 1.23456 → "1.23" → 1.23
}

// ✅ Preserve precision or accept the tradeoff knowingly
const geoParser = {
  parse: parseFloat,
  serialize: v => v.toString()
}
```

### 9. Missing eq for Reference Types
```tsx
// ❌ clearOnDefault won't work correctly
const dateParser = {
  parse: (v) => new Date(v),
  serialize: (d) => d.toISOString()
}

// ✅ Provide eq function for reference types
const dateParser = createParser({
  parse: (v) => new Date(v),
  serialize: (d) => d.toISOString(),
  eq: (a, b) => a.getTime() === b.getTime()
})
```

## Quick Reference

| Task | Solution |
|------|----------|
| Single param | `useQueryState('key', parser.withDefault(val))` |
| Multiple params | `useQueryStates({ key: parser })` |
| Server access | `createSearchParamsCache` + `.parse()` |
| Notify server | `{ shallow: false }` |
| History entry | `{ history: 'push' }` |
| Loading state | `useTransition` + `{ startTransition }` |
| Short URL keys | `urlKeys: { longName: 'short' }` |
| Array param | `parseAsArrayOf(parser)` or `parseAsArrayOf(parser, ';')` |
| Enum/literal | `parseAsStringLiteral(['a', 'b'] as const)` |
| Custom type | `createParser({ parse, serialize, eq })` |
| Test component | `withNuqsTestingAdapter({ searchParams: '?...' })` |

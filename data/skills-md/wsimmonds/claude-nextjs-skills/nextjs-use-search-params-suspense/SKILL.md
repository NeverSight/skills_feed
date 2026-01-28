---
name: nextjs-use-search-params-suspense
description: Pattern for using useSearchParams hook with Suspense boundary in Next.js. Covers the required combination of 'use client' directive and Suspense wrapper when accessing URL query parameters in client components. Use when building search interfaces, filters, pagination, or any feature that needs to read/manipulate URL query parameters client-side.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js: useSearchParams with Suspense Pattern

## Pattern Overview

**The useSearchParams hook requires TWO things:**
1. Component must have `'use client'` directive
2. Component must be wrapped in a `<Suspense>` boundary

This is a Next.js requirement, not optional!

## Why This Pattern?

**useSearchParams** reads URL query parameters:
- `/search?q=shoes` → `searchParams.get('q')` returns `"shoes"`
- `/products?category=electronics&sort=price` → Read multiple params

**Why Suspense?**
Next.js uses React 18's Suspense to handle the async nature of reading URL params during server-side rendering and hydration.

## The Pattern

### Single-File Pattern (Recommended)

```typescript
// app/page.tsx
import { Suspense } from 'react';
import SearchComponent from './SearchComponent';

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SearchComponent />
    </Suspense>
  );
}

// app/SearchComponent.tsx
'use client';

import { useSearchParams } from 'next/navigation';

export default function SearchComponent() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';

  return (
    <div>
      <h1>Search Results for: {query}</h1>
    </div>
  );
}
```

### Inline Pattern (Single File)

Sometimes you want everything in one file:

```typescript
// app/page.tsx
'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';

function SearchContent() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';

  return (
    <div>
      <h1>Search: {query}</h1>
      <p>Results for "{query}"</p>
    </div>
  );
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading search...</div>}>
      <SearchContent />
    </Suspense>
  );
}
```

## TypeScript: NEVER Use `any` Type

```typescript
// ❌ WRONG
function Component({ params }: any) { ... }

// ✅ CORRECT
// useSearchParams returns ReadonlyURLSearchParams
function Component() {
  const searchParams = useSearchParams();
  const value: string | null = searchParams.get('key');
}
```

## Real-World Examples

### Example 1: Search Interface

```typescript
// app/search/page.tsx
'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';

function SearchResults() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';
  const category = searchParams.get('category') || 'all';

  return (
    <div>
      <h1>Search: {query}</h1>
      <p>Category: {category}</p>

      {/* Display search results */}
      <div className="results">
        {/* ... */}
      </div>
    </div>
  );
}

export default function SearchPage() {
  return (
    <div>
      <Suspense fallback={<div>Loading results...</div>}>
        <SearchResults />
      </Suspense>
    </div>
  );
}
```

### Example 2: Product Filters

```typescript
// app/products/page.tsx
'use client';

import { Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

function ProductList() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const category = searchParams.get('category') || 'all';
  const sort = searchParams.get('sort') || 'name';
  const minPrice = searchParams.get('minPrice') || '0';

  const updateFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set(key, value);
    router.push(`?${params.toString()}`);
  };

  return (
    <div>
      <div className="filters">
        <select
          value={category}
          onChange={(e) => updateFilter('category', e.target.value)}
        >
          <option value="all">All Categories</option>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
        </select>

        <select
          value={sort}
          onChange={(e) => updateFilter('sort', e.target.value)}
        >
          <option value="name">Name</option>
          <option value="price">Price</option>
          <option value="rating">Rating</option>
        </select>
      </div>

      <div className="products">
        {/* Product grid filtered by params */}
      </div>
    </div>
  );
}

export default function ProductsPage() {
  return (
    <Suspense fallback={<div>Loading products...</div>}>
      <ProductList />
    </Suspense>
  );
}
```

### Example 3: Pagination

```typescript
// app/blog/page.tsx
'use client';

import { Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

function BlogPosts() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const page = parseInt(searchParams.get('page') || '1', 10);
  const perPage = 10;

  const goToPage = (newPage: number) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set('page', newPage.toString());
    router.push(`?${params.toString()}`);
  };

  return (
    <div>
      <h1>Blog Posts - Page {page}</h1>

      <div className="posts">
        {/* Blog posts for current page */}
      </div>

      <div className="pagination">
        <button
          disabled={page === 1}
          onClick={() => goToPage(page - 1)}
        >
          Previous
        </button>
        <span>Page {page}</span>
        <button onClick={() => goToPage(page + 1)}>
          Next
        </button>
      </div>
    </div>
  );
}

export default function BlogPage() {
  return (
    <Suspense fallback={<div>Loading posts...</div>}>
      <BlogPosts />
    </Suspense>
  );
}
```

## Working with URLSearchParams

```typescript
'use client';

import { useSearchParams } from 'next/navigation';

function Component() {
  const searchParams = useSearchParams();

  // Get single value
  const query = searchParams.get('q');           // string | null
  const category = searchParams.get('category'); // string | null

  // Get all values for a key (for multi-select)
  const tags = searchParams.getAll('tag');       // string[]

  // Check if key exists
  const hasSort = searchParams.has('sort');      // boolean

  // Iterate over all params
  searchParams.forEach((value, key) => {
    console.log(`${key}: ${value}`);
  });

  // Convert to regular object
  const paramsObject = Object.fromEntries(searchParams.entries());

  return <div>{/* ... */}</div>;
}
```

## Updating URL Parameters

```typescript
'use client';

import { useSearchParams, useRouter } from 'next/navigation';

function Component() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const updateParams = (updates: Record<string, string>) => {
    // Create new URLSearchParams from current params
    const params = new URLSearchParams(searchParams.toString());

    // Apply updates
    Object.entries(updates).forEach(([key, value]) => {
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);  // Remove if value is empty
      }
    });

    // Navigate with new params
    router.push(`?${params.toString()}`);
  };

  return (
    <button onClick={() => updateParams({ sort: 'price', order: 'asc' })}>
      Sort by Price
    </button>
  );
}
```

## Common Patterns

### Pattern: Search with Debounce

```typescript
'use client';

import { Suspense, useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

function SearchInput() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [query, setQuery] = useState(searchParams.get('q') || '');

  useEffect(() => {
    const timer = setTimeout(() => {
      const params = new URLSearchParams(searchParams.toString());
      if (query) {
        params.set('q', query);
      } else {
        params.delete('q');
      }
      router.push(`?${params.toString()}`);
    }, 300); // Debounce 300ms

    return () => clearTimeout(timer);
  }, [query, searchParams, router]);

  return (
    <input
      type="search"
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Search..."
    />
  );
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SearchInput />
    </Suspense>
  );
}
```

### Pattern: Multiple Filters

```typescript
'use client';

import { Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

interface Filters {
  category?: string;
  priceMin?: string;
  priceMax?: string;
  inStock?: string;
}

function FilterPanel() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const currentFilters: Filters = {
    category: searchParams.get('category') || undefined,
    priceMin: searchParams.get('priceMin') || undefined,
    priceMax: searchParams.get('priceMax') || undefined,
    inStock: searchParams.get('inStock') || undefined,
  };

  const updateFilters = (newFilters: Partial<Filters>) => {
    const params = new URLSearchParams(searchParams.toString());

    Object.entries({ ...currentFilters, ...newFilters }).forEach(
      ([key, value]) => {
        if (value) {
          params.set(key, value);
        } else {
          params.delete(key);
        }
      }
    );

    router.push(`?${params.toString()}`);
  };

  const clearFilters = () => {
    router.push(window.location.pathname); // Remove all params
  };

  return (
    <div className="filters">
      <select
        value={currentFilters.category || ''}
        onChange={(e) => updateFilters({ category: e.target.value })}
      >
        <option value="">All Categories</option>
        <option value="electronics">Electronics</option>
      </select>

      <input
        type="number"
        placeholder="Min Price"
        value={currentFilters.priceMin || ''}
        onChange={(e) => updateFilters({ priceMin: e.target.value })}
      />

      <button onClick={clearFilters}>Clear Filters</button>
    </div>
  );
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading filters...</div>}>
      <FilterPanel />
    </Suspense>
  );
}
```

## Common Mistakes

### ❌ Mistake 1: Missing 'use client'

```typescript
// ❌ WRONG - Missing 'use client'
import { useSearchParams } from 'next/navigation';

export default function Page() {
  const searchParams = useSearchParams(); // ERROR!
  return <div>{searchParams.get('q')}</div>;
}
```

```typescript
// ✅ CORRECT
'use client';  // Added!

import { useSearchParams } from 'next/navigation';

export default function Page() {
  const searchParams = useSearchParams();
  return <div>{searchParams.get('q')}</div>;
}
```

### ❌ Mistake 2: Missing Suspense Wrapper

```typescript
// ❌ WRONG - Missing Suspense
'use client';

import { useSearchParams } from 'next/navigation';

export default function Page() {
  const searchParams = useSearchParams(); // Will cause issues!
  return <div>{searchParams.get('q')}</div>;
}
```

```typescript
// ✅ CORRECT
'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';

function SearchContent() {
  const searchParams = useSearchParams();
  return <div>{searchParams.get('q')}</div>;
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SearchContent />
    </Suspense>
  );
}
```

### ❌ Mistake 3: Using in Server Component

```typescript
// ❌ WRONG - Trying to use in server component
import { useSearchParams } from 'next/navigation';

export default async function Page() {  // async = server component
  const searchParams = useSearchParams(); // ERROR! Hooks don't work in server components
  return <div>...</div>;
}
```

```typescript
// ✅ CORRECT - Use searchParams prop in server components
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;
  return <div>Query: {q}</div>;
}
```

## Server vs Client searchParams

| Feature | Server Component | Client Component |
|---------|-----------------|------------------|
| Access method | `searchParams` prop | `useSearchParams()` hook |
| Requires 'use client' | ❌ No | ✅ Yes |
| Requires Suspense | ❌ No | ✅ Yes |
| Can be async | ✅ Yes | ❌ No |
| Can update params | ❌ No (use Link/redirect) | ✅ Yes (use router.push) |
| Best for | Initial load, SEO | Dynamic filters, real-time updates |

## Quick Checklist

When using useSearchParams:

- [ ] Add `'use client'` directive at top of file
- [ ] Import `Suspense` from 'react'
- [ ] Import `useSearchParams` from 'next/navigation'
- [ ] Wrap component using `useSearchParams` in `<Suspense>`
- [ ] Provide a fallback to Suspense
- [ ] Call `useSearchParams()` inside wrapped component
- [ ] Use `.get()`, `.has()`, or `.getAll()` to read params

## Summary

**useSearchParams with Suspense:**
- ✅ Requires `'use client'` directive
- ✅ Requires `<Suspense>` wrapper
- ✅ Use for client-side URL param reading
- ✅ Combine with `useRouter()` for updating params
- ✅ Best for filters, search, pagination
- ❌ NOT for server components (use `searchParams` prop instead)

This is the recommended pattern for client-side URL parameter handling in Next.js App Router.

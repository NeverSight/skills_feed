---
name: nextjs-pathname-id-fetch
description: Focused pattern for fetching data using URL parameters in Next.js. Covers creating dynamic routes ([id], [slug]) and accessing route parameters in server components to fetch data from APIs. Use when building pages that display individual items (product pages, blog posts, user profiles) based on a URL parameter. Complements nextjs-dynamic-routes-params with a simplified, common-case pattern.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js: Pathname ID Fetch Pattern

## When This Pattern Applies

Use this pattern whenever a page needs to load data based on whatever identifier appears in the URL. Common scenarios include:
- Detail pages for products, posts, or users (`/products/{id}`, `/blog/{slug}`)
- Admin dashboards that drill into a selected resource (`/admin/orders/{orderId}`)
- Documentation or knowledge bases with nested paths (`/docs/getting-started/installation`)

If the requirement says the data should change depending on the current URL path, the route segment must be dynamic (e.g., `[id]`, `[slug]`, `[...slug]`).

## The Pattern

**✅ Recommended implementation**
```
1. Create a dynamic folder: app/[id]/page.tsx
2. Access the parameter: const { id } = await params;
3. Fetch data using that identifier
4. Render the requested information
```

**❌ Pitfall**
```
Using app/page.tsx for this scenario prevents access to per-path identifiers.
```

## Complete Implementation Example

```typescript
// app/[id]/page.tsx

// IMPORTANT: Server component (NO 'use client' needed!)
export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  // Next.js 15+: params must be awaited
  const { id } = await params;

  // Fetch data using the ID from the URL
  const response = await fetch(`https://api.example.com/products/${id}`);
  const product = await response.json();

  // Return JSX with the fetched data
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>Price: ${product.price}</p>
    </div>
  );
}
```

## File Structure

```
app/
└── [id]/                 ← Dynamic route folder with brackets
    └── page.tsx          ← Server component page
```

**URL Mapping:**
- `/123` → params = `{ id: '123' }`
- `/abc` → params = `{ id: 'abc' }`
- `/product-xyz` → params = `{ id: 'product-xyz' }`

## Key Rules

### 1. Folder Name MUST Use Brackets
```
✅ app/[id]/page.tsx
✅ app/[productId]/page.tsx
✅ app/[slug]/page.tsx
❌ app/id/page.tsx        (no brackets = static route)
❌ app/page.tsx            (can't access params here)
```

### 2. This is a Server Component (Default)
```typescript
// ✅ CORRECT - No 'use client' needed
export default async function Page({ params }) {
  const { id } = await params;
  const data = await fetch(`/api/${id}`);
  return <div>{data.name}</div>;
}

// ❌ WRONG - Don't add 'use client' for server components
'use client';  // ← Remove this!
export default async function Page({ params }) { ... }
```

### 3. Params Must Be Awaited (Next.js 15+)
```typescript
// ✅ CORRECT - Next.js 15+
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;  // Must await
  // ...
}

// ⚠️ OLD (Next.js 14 and earlier - deprecated)
export default async function Page({
  params,
}: {
  params: { id: string };
}) {
  const { id } = params;  // No await needed in old versions
  // ...
}
```

### 4. Keep It Simple - Don't Over-Nest
```
✅ app/[id]/page.tsx              (simple, clean)
❌ app/products/[id]/page.tsx     (only if explicitly required!)
```

Unless requirements explicitly call for `/products/[id]`, keep the structure at the top level (`app/[id]/page.tsx`).

## TypeScript: NEVER Use `any` Type

This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

```typescript
// ❌ WRONG
function processProduct(product: any) { ... }

// ✅ CORRECT - Define proper types
interface Product {
  id: string;
  name: string;
  price: number;
}

function processProduct(product: Product) { ... }

// ✅ ALSO CORRECT - Use unknown if type truly unknown
function processData(data: unknown) {
  // Type guard required before using
  if (typeof data === 'object' && data !== null) {
    // ...
  }
}
```

## Common Variations

### Different Parameter Names
```typescript
// app/[productId]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ productId: string }>;
}) {
  const { productId } = await params;
  // ...
}

// app/[slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  // ...
}
```

### Multiple Parameters
```typescript
// app/[category]/[id]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ category: string; id: string }>;
}) {
  const { category, id } = await params;
  const data = await fetch(`/api/${category}/${id}`);
  // ...
}
```

## Complete Working Example

```typescript
// app/[id]/page.tsx - Product detail page

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  inStock: boolean;
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  // Get the ID from the URL
  const { id } = await params;

  // Fetch product data using the ID
  const response = await fetch(
    `https://api.example.com/products/${id}`,
    { cache: 'no-store' } // Always fresh data
  );

  if (!response.ok) {
    throw new Error('Failed to fetch product');
  }

  const product: Product = await response.json();

  // Render the product
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>

      <div>
        <strong>Price:</strong> ${product.price}
      </div>

      <div>
        <strong>Availability:</strong>{' '}
        {product.inStock ? 'In Stock' : 'Out of Stock'}
      </div>
    </div>
  );
}
```

## Quick Checklist

Before shipping a pathname-driven detail page, confirm:

- [ ] The route folder uses brackets (e.g., `app/[id]/page.tsx`)
- [ ] The component stays server-side (no `'use client'` needed)
- [ ] The `params` prop is typed as `Promise<{ id: string }>` for Next.js 15+
- [ ] You await the params and read the identifier safely
- [ ] Data fetching logic uses that identifier
- [ ] Rendering handles loading/error states appropriately
- [ ] Types are explicit—never fall back to `any`

## When to Use the Comprehensive Skill Instead

This micro-skill covers the simple "pathname ID fetch" pattern. Use the comprehensive `nextjs-dynamic-routes-params` skill for:
- Catch-all routes (`[...slug]`)
- Optional catch-all routes (`[[...slug]]`)
- Complex multi-parameter routing
- Advanced routing architectures
- Detailed routing decisions

For the simple case of "fetch data by ID from URL", this skill is all you need.

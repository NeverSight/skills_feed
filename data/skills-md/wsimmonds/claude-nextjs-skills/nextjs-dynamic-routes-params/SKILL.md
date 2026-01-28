---
name: nextjs-dynamic-routes-params
description: Guide for Next.js App Router dynamic routes and pathname parameters. Use when building pages that depend on URL segments (IDs, slugs, nested paths), accessing the `params` prop, or fetching resources by identifier. Helps avoid over-nesting by defaulting to the simplest route structure (e.g., `app/[id]` instead of `app/products/[id]` unless the URL calls for it).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Next.js Dynamic Routes and Pathname Parameters

## When to Use This Skill

Use this skill when:
- Creating dynamic route segments (e.g., blog/[slug], users/[id])
- Accessing URL pathname parameters in Server or Client Components
- Building pages that fetch data based on route parameters
- Implementing catch-all or optional catch-all routes
- Working with the `params` prop in page.tsx, layout.tsx, or route.ts

## ⚠️ RECOGNIZING WHEN YOU NEED DYNAMIC ROUTES

**Look for requirements that tie data to the URL path.**

Create a dynamic segment (`[param]`) whenever the UI depends on part of the pathname. Typical signals include:
- Details pages that reference “the item’s ID/slug from the URL”
- Copy that calls out path segments (e.g., `/products/{id}`, `/blog/{slug}`)
- Requirements to fetch data “based on whichever resource is being visited”
- Navigation flows where one page links to `/something/{identifier}`

**✅ Dynamic route response**
```
Requirement: display product information based on whichever ID appears in the URL
Implementation: app/[id]/page.tsx
Access parameter with: const { id } = await params;
```

**❌ Static-page response**
```
Implementation: app/page.tsx  ← cannot access per-path identifiers
```

**Example requirements that lead to dynamic routes**
1. “Show a product page that loads whichever product ID appears in the URL” → `app/[id]/page.tsx` or `app/products/[id]/page.tsx`
2. “Render a blog article based on its slug” → `app/blog/[slug]/page.tsx` or `app/[slug]/page.tsx`
3. “Support nested docs such as /docs/getting-started/installation” → `app/docs/[...slug]/page.tsx`

**Core rule:** If data varies with a URL segment, the folder name needs matching brackets.

## ⚠️ CRITICAL: Avoid Over-Engineering Route Structure

**MOST COMMON MISTAKE:** Adding unnecessary nesting to routes.

**Default Rule:** When creating a dynamic route, use `app/[id]/page.tsx` or `app/[slug]/page.tsx` unless:
- The URL structure is explicitly specified (e.g., "create route at /products/[id]")
- You're building multiple resource types that need namespacing
- The requirements clearly show a nested URL structure

**Do NOT infer nesting from resource names:**
- "Fetch a product by ID" → `app/[id]/page.tsx` ✅ (not `app/products/[id]`)
- "Show user profile" → `app/[userId]/page.tsx` ✅ (not `app/users/[userId]`)
- "Display blog post" → `app/[slug]/page.tsx` ✅ (not `app/blog/[slug]`)

**Only nest when explicitly told:**
- "Create a route at /blog/[slug]" → `app/blog/[slug]/page.tsx` ✅
- "Products should be at /products/[id]" → `app/products/[id]/page.tsx` ✅

## Core Concepts

### Dynamic Route Syntax

Next.js uses **folder names with square brackets** to create dynamic route segments:

```
app/
├── [id]/page.tsx              # Matches /123, /abc, etc.
├── blog/[slug]/page.tsx       # Matches /blog/hello-world
├── shop/[category]/[id]/page.tsx  # Matches /shop/electronics/123
└── docs/[...slug]/page.tsx    # Matches /docs/a, /docs/a/b, /docs/a/b/c
```

**Key Principle:** The folder structure IS the route structure.

### Route Structure Decision Tree

**CRITICAL RULE: Do NOT infer route structure from resource type names!**

Just because you're fetching a "product" or "user" doesn't mean you need `/products/[id]` or `/users/[id]`. **Unless explicitly told otherwise, prefer the simplest structure.**

**When deciding on route structure:**

1. **Top-level dynamic route** (`app/[id]/page.tsx`)
   - **DEFAULT CHOICE** - Use this unless specifically told otherwise
   - Use when the resource IS the primary entity
   - Use when only ID-based routing is needed
   - Examples: `/123` for any resource, `/abc-def` for slugs
   - Pattern: The ID/slug is the only identifier needed
   - **When in doubt, choose this!**

2. **Nested dynamic route** (`app/category/[id]/page.tsx`)
   - **ONLY use when explicitly required by the URL structure**
   - Use when you're told "create a /products/[id] route"
   - Use when the URL itself needs the category prefix
   - Examples: `/products/123`, `/blog/my-post` (when specified)
   - Pattern: Category + identifier (when both are required)

3. **Multi-segment dynamic** (`app/[cat]/[id]/page.tsx`)
   - Use when hierarchy matters
   - Examples: `/shop/electronics/123`
   - Pattern: Multiple levels of categorization

**⚠️ COMMON MISTAKE:** Creating `app/products/[id]/page.tsx` when you should create `app/[id]/page.tsx`

❌ **WRONG:** "Fetch a product by ID" → `app/products/[id]/page.tsx`
✅ **CORRECT:** "Fetch a product by ID" → `app/[id]/page.tsx`

❌ **WRONG:** "Create a dynamic route for users" → `app/users/[userId]/page.tsx`
✅ **CORRECT:** "Create a dynamic route for users" → `app/[userId]/page.tsx`

**Only add the category prefix when:**
- The requirement explicitly says "at /products/..." or similar
- You're building multiple resource types that need namespacing
- The URL structure is specified in requirements

## Accessing Pathname Parameters

### In Server Components (page.tsx, layout.tsx)

**CRITICAL: In Next.js 15+, `params` is a Promise and must be awaited!**

```typescript
// ✅ CORRECT - Next.js 15+
export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const product = await fetch(`https://api.example.com/products/${id}`)
    .then(res => res.json());

  return <div>{product.name}</div>;
}
```

```typescript
// ❌ WRONG - Treating params as synchronous object (Next.js 15+)
export default async function ProductPage({
  params,
}: {
  params: { id: string };  // Missing Promise wrapper
}) {
  const product = await fetch(`https://api.example.com/products/${params.id}`);
  // This will fail because params is a Promise!
}
```

**For Next.js 14 and earlier:**
```typescript
// Next.js 14 - params is synchronous
export default async function ProductPage({
  params,
}: {
  params: { id: string };
}) {
  const product = await fetch(`https://api.example.com/products/${params.id}`)
    .then(res => res.json());

  return <div>{product.name}</div>;
}
```

### In Route Handlers (route.ts)

```typescript
// app/api/products/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;

  const product = await db.products.findById(id);
  return Response.json(product);
}
```

### In Client Components

**You CANNOT access `params` directly in Client Components.** Instead:

1. **Use `useParams()` hook:**
```typescript
'use client';

import { useParams } from 'next/navigation';

export function ProductClient() {
  const params = useParams<{ id: string }>();
  const id = params.id;

  // Use the id...
}
```

2. **Pass params from Server Component:**
```typescript
// app/products/[id]/page.tsx (Server Component)
export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <ProductClient productId={id} />;
}

// components/ProductClient.tsx
'use client';

export function ProductClient({ productId }: { productId: string }) {
  // Use productId...
}
```

## Common Patterns

### Pattern 1: Simple ID-Based Page

```typescript
// app/[id]/page.tsx - Top-level dynamic route
interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function ItemPage({ params }: PageProps) {
  const { id } = await params;

  const item = await fetch(`https://api.example.com/items/${id}`)
    .then(res => res.json());

  return (
    <div>
      <h1>{item.title}</h1>
      <p>{item.description}</p>
    </div>
  );
}
```

### Pattern 2: Blog Post with Slug

```typescript
// app/blog/[slug]/page.tsx
interface PageProps {
  params: Promise<{ slug: string }>;
}

export default async function BlogPost({ params }: PageProps) {
  const { slug } = await params;

  const post = await getPostBySlug(slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}

// Generate static params for SSG
export async function generateStaticParams() {
  const posts = await getAllPosts();

  return posts.map((post) => ({
    slug: post.slug,
  }));
}
```

### Pattern 3: Nested Resources

```typescript
// app/users/[userId]/posts/[postId]/page.tsx
interface PageProps {
  params: Promise<{
    userId: string;
    postId: string;
  }>;
}

export default async function UserPost({ params }: PageProps) {
  const { userId, postId } = await params;

  const [user, post] = await Promise.all([
    getUserById(userId),
    getPostById(postId),
  ]);

  return (
    <div>
      <h1>{post.title}</h1>
      <p>By {user.name}</p>
      <div>{post.content}</div>
    </div>
  );
}
```

### Pattern 4: Catch-All Routes

```typescript
// app/docs/[...slug]/page.tsx - Matches /docs/a, /docs/a/b, /docs/a/b/c
interface PageProps {
  params: Promise<{
    slug: string[];  // Array of path segments
  }>;
}

export default async function DocsPage({ params }: PageProps) {
  const { slug } = await params;
  const path = slug.join('/');

  const doc = await getDocByPath(path);

  return <div>{doc.content}</div>;
}
```

```typescript
// app/shop/[[...slug]]/page.tsx - Optional catch-all
// Matches /shop, /shop/electronics, /shop/electronics/phones
interface PageProps {
  params: Promise<{
    slug?: string[];  // Optional array
  }>;
}

export default async function ShopPage({ params }: PageProps) {
  const { slug = [] } = await params;

  if (slug.length === 0) {
    return <ShopHomepage />;
  }

  return <CategoryPage category={slug.join('/')} />;
}
```

## TypeScript Best Practices

### Type Safety for Params

```typescript
// Define params type separately for reusability
type ProductPageParams = { id: string };

interface ProductPageProps {
  params: Promise<ProductPageParams>;
}

export default async function ProductPage({ params }: ProductPageProps) {
  const { id } = await params;
  // id is typed as string
}

// Reuse in generateMetadata
export async function generateMetadata({ params }: ProductPageProps) {
  const { id } = await params;
  const product = await getProduct(id);
  return { title: product.name };
}
```

### Multiple Dynamic Segments

```typescript
type PostPageParams = {
  category: string;
  slug: string;
};

interface PostPageProps {
  params: Promise<PostPageParams>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

export default async function PostPage({ params, searchParams }: PostPageProps) {
  const { category, slug } = await params;
  const { view } = await searchParams;

  // All properly typed
}
```

## Common Pitfalls and Solutions

### Pitfall 1: Forgetting params is a Promise (Next.js 15+)

```typescript
// ❌ WRONG
export default async function Page({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);  // Error: params is Promise
}

// ✅ CORRECT
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id);
}
```

### Pitfall 2: Using params in Client Components without useParams

```typescript
// ❌ WRONG - params prop doesn't exist in Client Components
'use client';

export default function ClientPage({ params }) {  // undefined!
  return <div>{params.id}</div>;
}

// ✅ CORRECT
'use client';
import { useParams } from 'next/navigation';

export default function ClientPage() {
  const params = useParams<{ id: string }>();
  return <div>{params.id}</div>;
}
```

### Pitfall 3: Over-nesting Routes

```typescript
// ❌ UNNECESSARY NESTING
// app/products/product/[id]/page.tsx
// URL: /products/product/123

// ✅ SIMPLER
// app/products/[id]/page.tsx
// URL: /products/123

// OR even simpler if product is the main resource:
// app/[id]/page.tsx
// URL: /123
```

### Pitfall 4: Not Handling Invalid IDs

```typescript
// ✅ ROBUST
export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const product = await fetch(`https://api.example.com/products/${id}`)
    .then(res => {
      if (!res.ok) throw new Error('Product not found');
      return res.json();
    });

  if (!product) {
    notFound();  // Shows 404 page
  }

  return <div>{product.name}</div>;
}
```

## Decision Guide

**When you need to create a dynamic route, ask:**

1. **What's the URL structure?**
   - Single ID: `[id]`
   - Category + ID: `category/[id]`
   - Hierarchical: `[category]/[id]`
   - Flexible paths: `[...slug]`

2. **Is this a Server or Client Component?**
   - Server: Use `params` prop (await it in Next.js 15+)
   - Client: Use `useParams()` hook

3. **Do I need the simplest structure?**
   - When in doubt, use fewer nesting levels
   - Top-level routes are simpler and more direct

4. **Am I on Next.js 15+?**
   - Yes: `params` is `Promise<{...}>`
   - No: `params` is `{...}`

## Examples: Real-World Scenarios

### E-commerce Product Page

```typescript
// app/products/[id]/page.tsx
import { notFound } from 'next/navigation';

interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
}

async function getProduct(id: string): Promise<Product | null> {
  const res = await fetch(`https://api.example.com/products/${id}`, {
    next: { revalidate: 60 },  // Revalidate every 60s
  });

  if (!res.ok) return null;
  return res.json();
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const product = await getProduct(id);

  if (!product) {
    notFound();
  }

  return (
    <div>
      <h1>{product.name}</h1>
      <p>${product.price}</p>
      <p>{product.description}</p>
    </div>
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const product = await getProduct(id);

  return {
    title: product?.name ?? 'Product Not Found',
    description: product?.description,
  };
}
```

### Documentation Site with Nested Paths

```typescript
// app/docs/[...slug]/page.tsx
interface DocPageProps {
  params: Promise<{ slug: string[] }>;
}

export default async function DocPage({ params }: DocPageProps) {
  const { slug } = await params;
  const path = slug.join('/');

  const doc = await getDocByPath(path);

  if (!doc) {
    notFound();
  }

  return (
    <article className="prose">
      <h1>{doc.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: doc.html }} />
    </article>
  );
}

export async function generateStaticParams() {
  const docs = await getAllDocs();

  return docs.map((doc) => ({
    slug: doc.path.split('/'),
  }));
}
```

## Checklist for Dynamic Routes

Before implementing a dynamic route, verify:

- [ ] **Route structure is as simple as possible** (default to top-level unless told otherwise)
- [ ] Not inferring route nesting from resource type names
- [ ] Route structure matches URL requirements (not over-nested)
- [ ] `params` is typed as `Promise<{...}>` for Next.js 15+
- [ ] `params` is awaited before accessing properties (Next.js 15+)
- [ ] Error handling for invalid IDs/slugs (use `notFound()`)
- [ ] TypeScript types are properly defined
- [ ] Using Server Component unless client interactivity needed
- [ ] Consider `generateStaticParams()` for SSG if applicable
- [ ] Metadata generation if SEO matters

## Quick Reference

| Scenario | Route Structure | Params Access |
|----------|----------------|---------------|
| Single resource by ID | `app/[id]/page.tsx` | `const { id } = await params` |
| Category + resource | `app/category/[id]/page.tsx` | `const { id } = await params` |
| Blog with slugs | `app/blog/[slug]/page.tsx` | `const { slug } = await params` |
| Nested resources | `app/[cat]/[id]/page.tsx` | `const { cat, id } = await params` |
| Flexible paths | `app/docs/[...slug]/page.tsx` | `const { slug } = await params` (slug is array) |
| Optional paths | `app/[[...slug]]/page.tsx` | `const { slug = [] } = await params` |
| Client Component | Use `useParams()` hook | `const params = useParams<{ id: string }>()` |

---

**Remember:** Dynamic routes in Next.js are file-system based. The folder structure with `[brackets]` creates the dynamic segments, and the `params` prop (or `useParams()` hook) provides access to those values.

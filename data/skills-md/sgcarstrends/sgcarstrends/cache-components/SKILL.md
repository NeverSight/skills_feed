---
name: cache-components
description: Implement Next.js 16 Cache Components with use cache directives, Suspense boundaries, and cacheLife profiles. Use when optimizing page performance or migrating components to cache mode.
allowed-tools: Read, Edit, mcp__next-devtools__nextjs_docs, mcp__next-devtools__nextjs_runtime
---

# Next.js Cache Components Skill

This skill helps you implement and optimize Next.js 16 Cache Components in `apps/web/`.

## When to Use This Skill

- Converting components to use Cache Components
- Adding "use cache" directives to functions or queries
- Implementing query-level caching for data fetching
- Setting up domain-level cache tags for efficient invalidation
- Implementing Suspense boundaries
- Configuring cacheLife profiles
- Debugging cache-related errors
- Optimizing page load performance
- Reducing ISR write operations with broad cache tags

## Cache Components Overview

Next.js 16 introduced Cache Components to improve performance by caching component render results.

### Key Concepts

1. **"use cache" directive**: Marks functions/components for caching
2. **Query-level caching**: Apply cache directives at data-fetching query functions for consistency
3. **Domain-level cache tags**: Use broad tags (e.g., `CACHE_LIFE.cars`) instead of granular per-record tags
4. **Suspense boundaries**: Required for streaming cached content
5. **cacheLife profiles**: Control cache duration and invalidation
6. **cacheTag**: Manual cache invalidation (prefer domain-level scopes)
7. **Dynamic vs Static**: Understanding when caching applies

## Implementation Patterns

### 1. Basic Cache Component

```typescript
// app/components/car-list.tsx
import { Suspense } from "react";

async function CarList() {
  "use cache";

  const cars = await db.query.cars.findMany();

  return (
    <div>
      {cars.map(car => (
        <div key={car.id}>{car.make} {car.model}</div>
      ))}
    </div>
  );
}

// Parent component with Suspense
export default function CarsPage() {
  return (
    <Suspense fallback={<div>Loading cars...</div>}>
      <CarList />
    </Suspense>
  );
}
```

### 2. Cache with cacheLife

Control cache duration:

```typescript
import { cacheLife } from "next/cache";

async function COEData() {
  "use cache";
  cacheLife("hours"); // Built-in profile: cache for hours

  const coe = await db.query.coe.findMany();
  return <COETable data={coe} />;
}

// Custom cache profile
async function RealtimeData() {
  "use cache";
  cacheLife({
    stale: 60,        // Serve stale for 60 seconds
    revalidate: 300,  // Revalidate after 5 minutes
    expire: 3600,     // Expire after 1 hour
  });

  const data = await fetchRealtimeData();
  return <DataDisplay data={data} />;
}
```

### 3. Cache Tags for Invalidation

**Domain-Level Scopes (Recommended)**

Use broad, domain-level cache tags to minimize ISR write operations:

```typescript
// lib/cache.ts - Define domain-level cache scopes
export const CACHE_LIFE = {
  cars: "cars",
  coe: "coe",
  posts: "posts",
} as const;
```

```typescript
// Query function with domain-level cache tag
import { CACHE_LIFE } from "@web/lib/cache";
import { cacheLife, cacheTag } from "next/cache";

export const getDistinctMakes = async () => {
  "use cache";
  cacheLife("max");
  cacheTag(CACHE_LIFE.cars); // Broad tag for all car-related data

  return db.selectDistinct({ make: cars.make }).from(cars).orderBy(cars.make);
};
```

```typescript
// Invalidate entire domain cache in server action
"use server";
import { revalidateTag } from "next/cache";
import { CACHE_LIFE } from "@web/lib/cache";

export async function updateCarData() {
  await fetchAndUpdateCars();
  revalidateTag(CACHE_LIFE.cars); // Invalidate all car-related caches
}
```

**Granular Tags (Use Sparingly)**

For specific invalidation needs, use granular tags:

```typescript
async function BlogPosts() {
  "use cache";
  cacheTag("blog-posts"); // Tag for manual invalidation

  const posts = await db.query.posts.findMany();
  return <PostList posts={posts} />;
}

// Invalidate cache in server action
"use server";
import { revalidateTag } from "next/cache";

export async function createPost(data: PostData) {
  await db.insert(posts).values(data);
  revalidateTag("blog-posts"); // Invalidate cached blog posts
}
```

**⚠️ Cache Tag Best Practices:**
- **Prefer domain-level tags** to reduce ISR write operations
- **Avoid over-granular tags** (e.g., per-record tags) which increase overhead
- **Use granular tags only** when selective invalidation is critical
- **Keep tag names consistent** using constants from `lib/cache.ts`

### 4. Query-Level Caching (Recommended Pattern)

Apply cache directives at the query function level for reusable data fetching:

```typescript
// queries/cars/filter-options.ts
import { cars, db } from "@sgcarstrends/database";
import { CACHE_LIFE } from "@web/lib/cache";
import { cacheLife, cacheTag } from "next/cache";

export const getDistinctMakes = async () => {
  "use cache";
  cacheLife("max");
  cacheTag(CACHE_LIFE.cars);

  return db.selectDistinct({ make: cars.make }).from(cars).orderBy(cars.make);
};

export const getDistinctFuelTypes = async (month?: string) => {
  "use cache";
  cacheLife("max");
  cacheTag(CACHE_LIFE.cars);

  const filters = month ? [eq(cars.month, month)] : [];
  return db
    .selectDistinct({ fuelType: cars.fuelType })
    .from(cars)
    .where(filters.length > 0 ? and(...filters) : undefined)
    .orderBy(cars.fuelType);
};
```

**Benefits:**
- ✅ Centralized cache configuration for all data queries
- ✅ Consistent caching strategy across the application
- ✅ Easy to maintain and update cache policies
- ✅ Reusable across multiple components/pages
- ✅ Domain-level cache tags for efficient invalidation

**Usage in Components:**

```typescript
// app/cars/page.tsx
import { getDistinctMakes } from "@web/queries/cars/filter-options";

export default async function CarsPage() {
  const makes = await getDistinctMakes(); // Cached automatically

  return <MakesList makes={makes} />;
}
```

### 5. Private Cache (User-Specific)

```typescript
import { cookies } from "next/headers";

async function UserDashboard() {
  "use cache: private"; // Cache per-user, not globally

  const cookieStore = await cookies();
  const userId = cookieStore.get("userId")?.value;
  const userData = await fetchUserData(userId);

  return <Dashboard data={userData} />;
}
```

### 6. Nested Cache Components

```typescript
// Outer component - longer cache
async function CarsByMake({ make }: { make: string }) {
  "use cache";
  cacheLife("days");

  const cars = await db.query.cars.findMany({
    where: eq(cars.make, make),
  });

  return (
    <div>
      <h2>{make} Models</h2>
      <Suspense fallback={<div>Loading stats...</div>}>
        <CarStats makeId={make} />
      </Suspense>
      {cars.map(car => <CarCard key={car.id} car={car} />)}
    </div>
  );
}

// Inner component - shorter cache
async function CarStats({ makeId }: { makeId: string }) {
  "use cache";
  cacheLife("minutes");

  const stats = await calculateStats(makeId);
  return <StatsDisplay stats={stats} />;
}
```

## Common Tasks

### Converting Existing Component to Cache Component

**Before:**
```typescript
// Regular server component
async function DataTable() {
  const data = await fetchData();
  return <Table data={data} />;
}
```

**After:**
```typescript
// Cached server component
async function DataTable() {
  "use cache";
  cacheLife("hours");
  cacheTag("data-table");

  const data = await fetchData();
  return <Table data={data} />;
}

// Parent with Suspense
export default function Page() {
  return (
    <Suspense fallback={<TableSkeleton />}>
      <DataTable />
    </Suspense>
  );
}
```

### Debugging Cache Issues

1. **Component not caching:**
   - Verify "use cache" is first line
   - Check Suspense boundary exists
   - Ensure running Next.js 16+
   - Check dev server logs

2. **Cache not invalidating:**
   - Verify cacheTag is set correctly
   - Check revalidateTag is called
   - Review cacheLife settings
   - Check if using "private" cache incorrectly

3. **Runtime errors:**
   - Use Next.js runtime MCP tool to check errors
   - Review browser console for hydration issues
   - Check server logs for cache misses

Use Next.js DevTools MCP:
```typescript
// Get runtime errors
mcp__next-devtools__nextjs_runtime({ action: "call_tool", toolName: "get_errors" })
```

### Performance Optimization

Identify cache opportunities:

1. **Expensive data fetches**: Wrap in "use cache"
2. **Static content**: Use long cacheLife
3. **Frequently accessed**: Cache with appropriate TTL
4. **User-specific**: Use "use cache: private"

## Built-in cacheLife Profiles

Next.js provides these profiles:

```typescript
"seconds"  // { stale: 1, revalidate: 10, expire: 60 }
"minutes"  // { stale: 60, revalidate: 300, expire: 3600 }
"hours"    // { stale: 3600, revalidate: 86400, expire: 604800 }
"days"     // { stale: 86400, revalidate: 604800, expire: 2592000 }
"weeks"    // { stale: 604800, revalidate: 2592000, expire: 31536000 }
"max"      // { stale: 2592000, revalidate: 31536000, expire: Infinity }
```

## Suspense Best Practices

### 1. Loading States

Provide meaningful fallbacks:

```typescript
<Suspense fallback={<CarListSkeleton />}>
  <CarList />
</Suspense>
```

### 2. Multiple Suspense Boundaries

Stream different parts independently:

```typescript
export default function Dashboard() {
  return (
    <>
      <Suspense fallback={<HeaderSkeleton />}>
        <Header />
      </Suspense>

      <Suspense fallback={<ChartSkeleton />}>
        <Charts />
      </Suspense>

      <Suspense fallback={<TableSkeleton />}>
        <DataTable />
      </Suspense>
    </>
  );
}
```

### 3. Error Boundaries with Suspense

```typescript
import { ErrorBoundary } from "react-error-boundary";

export default function Page() {
  return (
    <ErrorBoundary fallback={<ErrorDisplay />}>
      <Suspense fallback={<Loading />}>
        <DataComponent />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Testing Cache Components

```typescript
// __tests__/car-list.test.tsx
import { render, screen } from "@testing-library/react";
import { Suspense } from "react";
import CarList from "../car-list";

describe("CarList", () => {
  it("renders with Suspense", async () => {
    render(
      <Suspense fallback={<div>Loading...</div>}>
        <CarList />
      </Suspense>
    );

    // Initially shows fallback
    expect(screen.getByText("Loading...")).toBeInTheDocument();

    // Wait for component to load
    const content = await screen.findByText(/Toyota/i);
    expect(content).toBeInTheDocument();
  });
});
```

## Common Errors and Solutions

### Error: "use cache" must be first directive

**Wrong:**
```typescript
async function Component() {
  const data = await fetchData();
  "use cache"; // ❌ Too late
}
```

**Correct:**
```typescript
async function Component() {
  "use cache"; // ✅ First line
  const data = await fetchData();
}
```

### Error: Missing Suspense boundary

**Wrong:**
```typescript
export default function Page() {
  return <CachedComponent />; // ❌ No Suspense
}
```

**Correct:**
```typescript
export default function Page() {
  return (
    <Suspense fallback={<Loading />}>
      <CachedComponent />
    </Suspense>
  );
}
```

### Error: Dynamic rendering disables cache

Avoid dynamic APIs in cached components:

**Wrong:**
```typescript
async function Component() {
  "use cache";
  const headers = await headers(); // ❌ Dynamic API
}
```

**Correct:**
```typescript
// Move dynamic logic to parent
export default async function Page() {
  const headers = await headers();
  const userId = headers.get("x-user-id");

  return (
    <Suspense fallback={<Loading />}>
      <CachedComponent userId={userId} />
    </Suspense>
  );
}

async function CachedComponent({ userId }: { userId: string }) {
  "use cache";
  // Now receives userId as prop
}
```

## Documentation References

Always check the latest Next.js docs:

```typescript
// Query Next.js documentation
mcp__next-devtools__nextjs_docs({
  action: "get",
  path: "/docs/app/api-reference/directives/use-cache"
})
```

## Performance Monitoring

Track cache effectiveness:

1. Check Next.js build output for cached routes
2. Monitor server response times
3. Use Next.js Analytics for performance metrics
4. Review cache hit/miss ratios in logs

## References

- Next.js 16 Cache Components: Use nextjs_docs MCP tool
- Related files:
  - `apps/web/src/app/` - All Next.js pages
  - `apps/web/src/components/` - React components
  - `apps/web/CLAUDE.md` - Web app documentation

## Best Practices

1. **Query-Level Caching**: Apply cache directives at query functions for consistency and reusability
2. **Domain-Level Tags**: Use broad cache tags (e.g., `CACHE_LIFE.cars`) to minimize ISR write operations
3. **Avoid Over-Granular Tags**: Don't create per-record or per-field tags; use domain scopes instead
4. **Appropriate TTLs**: Match cache duration to data freshness needs (use `cacheLife("max")` for static data)
5. **Cache Tag Constants**: Define cache tags in `lib/cache.ts` for consistency
6. **Error Handling**: Always wrap cached components with ErrorBoundary
7. **Loading States**: Provide meaningful Suspense fallbacks
8. **Testing**: Test both cached and uncached states
9. **Monitoring**: Track cache performance in production
10. **Progressive Enhancement**: Start with long TTLs, optimize based on usage

### Cache Optimization Strategy

**Recommended Approach (SG Cars Trends Pattern):**

```typescript
// 1. Define domain-level cache tags
// lib/cache.ts
export const CACHE_LIFE = {
  cars: "cars",
  coe: "coe",
  posts: "posts",
} as const;

// 2. Apply cache directives at query level
// queries/cars/filter-options.ts
export const getDistinctMakes = async () => {
  "use cache";
  cacheLife("max");
  cacheTag(CACHE_LIFE.cars);

  return db.selectDistinct({ make: cars.make }).from(cars);
};

// 3. Invalidate at domain level
// actions/update-cars.ts
"use server";
import { revalidateTag } from "next/cache";
import { CACHE_LIFE } from "@web/lib/cache";

export async function updateCarData() {
  await fetchAndUpdateCars();
  revalidateTag(CACHE_LIFE.cars); // Invalidate all car-related caches
}
```

**Benefits:**
- ✅ Reduces ISR write operations
- ✅ Simplifies cache invalidation
- ✅ Improves performance
- ✅ Easier to maintain

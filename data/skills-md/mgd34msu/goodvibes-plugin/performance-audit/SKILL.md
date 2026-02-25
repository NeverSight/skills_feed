---
name: performance-audit
description: "Load PROACTIVELY when task involves optimizing speed, reducing bundle size, or improving responsiveness. Use when user says \"make it faster\", \"reduce bundle size\", \"fix slow queries\", \"optimize rendering\", or \"check Core Web Vitals\". Covers bundle analysis and tree-shaking, database query optimization (N+1, indexing), React rendering performance (re-renders, memoization), network waterfall optimization, memory leak detection, server-side performance, and Core Web Vitals (LCP, FID, CLS) improvement."
metadata:
  version: "1.0.0"
  category: quality
  tags: [performance, audit, optimization, bundle, database, rendering, web-vitals]
---

## Resources
```
scripts/
  validate-performance-audit.sh
references/
  performance-patterns.md
```

# Performance Audit

This skill guides you through performing comprehensive performance audits on web applications to identify bottlenecks, optimization opportunities, and performance regressions. Use this when preparing for production deployments, investigating performance issues, or conducting periodic performance reviews.

## When to Use This Skill

- Conducting pre-deployment performance reviews
- Investigating slow page loads or poor user experience
- Performing periodic performance audits on existing applications
- Validating performance after major feature additions
- Preparing for traffic scaling or load testing
- Optimizing Core Web Vitals for SEO and user experience

## Audit Methodology

A systematic performance audit follows these phases:

### Phase 1: Reconnaissance

**Objective:** Understand the application architecture, tech stack, and performance surface area.

**Use discover to map performance-critical code:**
```yaml
discover:
  queries:
    - id: bundle_imports
      type: grep
      pattern: "^import.*from ['\"].*['\"]$"
      glob: "src/**/*.{ts,tsx,js,jsx}"
    - id: database_queries
      type: grep
      pattern: "(prisma\\.|db\\.|query\\(|findMany|findUnique|create\\(|update\\()"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: component_files
      type: glob
      patterns: ["src/components/**/*.{tsx,jsx}", "src/app/**/*.{tsx,jsx}"]
    - id: api_routes
      type: glob
      patterns: ["src/app/api/**/*.{ts,tsx}", "pages/api/**/*.{ts,tsx}"]
  verbosity: files_only
```

**Identify critical components:**
- Page entry points and route handlers
- Heavy npm dependencies (moment.js, lodash, etc.)
- Database access patterns and ORM usage
- Image and media assets
- API endpoints and data fetching logic
- Client-side rendering vs server components

### Phase 2: Bundle Analysis

**Objective:** Identify large dependencies, code splitting opportunities, and dead code.

#### Check Bundle Size

**Run bundle analyzer:**
```yaml
precision_exec:
  commands:
    - cmd: "npm run build"
      timeout_ms: 120000
    - cmd: "npx @next/bundle-analyzer"
      timeout_ms: 60000
  verbosity: standard
```

**Common issues:**
- Large dependencies imported on every page (moment.js, lodash, chart libraries)
- Multiple versions of the same package (check with `npm ls <package>`)
- Unused dependencies still bundled (tree-shaking failures)
- SVG icons imported as components instead of sprite sheets
- Entire UI libraries imported instead of individual components

#### Find Heavy Imports

**Search for common performance-heavy packages:**
```yaml
precision_grep:
  queries:
    - id: heavy_deps
      pattern: "import.*from ['\"](moment|lodash|date-fns|rxjs|@material-ui|antd|chart\\.js)['\"]"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: full_library_imports
      pattern: "import .* from ['\"](lodash|@mui/material|react-icons)['\"]$"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: locations
```

**Optimization strategies:**

**Bad - importing entire library:**
```typescript
import _ from 'lodash'; // 71KB gzipped
import * as Icons from 'react-icons/fa'; // 500+ icons
```

**Good - importing specific modules:**
```typescript
import debounce from 'lodash/debounce'; // 2KB gzipped
import { FaUser, FaCog } from 'react-icons/fa'; // Only what you need
```

**Better - using modern alternatives:**
```typescript
// Instead of moment.js (72KB), use date-fns (13KB) or native Intl
import { format } from 'date-fns';

// Or native APIs
const formatted = new Intl.DateTimeFormat('en-US').format(date);
```

#### Check for Code Splitting

**Find dynamic imports:**
```yaml
precision_grep:
  queries:
    - id: dynamic_imports
      pattern: "(import\\(|React\\.lazy|next/dynamic)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: large_components
      pattern: "export (default )?(function|const).*\\{[\\s\\S]{2000,}"
      glob: "src/components/**/*.{tsx,jsx}"
      multiline: true
  output:
    format: files_only
```

**Code splitting patterns:**

**Next.js dynamic imports:**
```typescript
import dynamic from 'next/dynamic';

// Client-only components (no SSR)
const ChartComponent = dynamic(() => import('./Chart'), {
  ssr: false,
  loading: () => <Spinner />,
});

// Route-based code splitting
const AdminPanel = dynamic(() => import('./AdminPanel'));
```

**React.lazy for client components:**
```typescript
import { lazy, Suspense } from 'react';

const HeavyModal = lazy(() => import('./HeavyModal'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyModal />
    </Suspense>
  );
}
```

### Phase 3: Database Performance

**Objective:** Eliminate N+1 queries, add missing indexes, and optimize query patterns.

#### Detect N+1 Query Patterns

**Search for sequential queries in loops:**
```yaml
precision_grep:
  queries:
    - id: potential_n_plus_one
      pattern: "(map|forEach).*await.*(findUnique|findFirst|findMany)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: missing_includes
      pattern: "findMany\\(\\{[^}]*where[^}]*\\}\\)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: context
    context_before: 3
    context_after: 3
```

**Common N+1 patterns:**

**Bad - N+1 query:**
```typescript
const posts = await db.post.findMany();

// Runs 1 query per post!
const postsWithAuthors = await Promise.all(
  posts.map(async (post) => ({
    ...post,
    author: await db.user.findUnique({ where: { id: post.authorId } }),
  }))
);
```

**Good - eager loading with include:**
```typescript
const posts = await db.post.findMany({
  include: {
    author: true,
    comments: {
      include: {
        user: true,
      },
    },
  },
});
```

**Better - explicit select for only needed fields:**
```typescript
const posts = await db.post.findMany({
  select: {
    id: true,
    title: true,
    author: {
      select: {
        id: true,
        name: true,
        avatar: true,
      },
    },
  },
});
```

#### Check for Missing Indexes

**Review Prisma schema for index coverage:**
```yaml
precision_read:
  files:
    - path: "prisma/schema.prisma"
      extract: content
  verbosity: standard
```

**Then search for WHERE clauses:**
```yaml
precision_grep:
  queries:
    - id: where_clauses
      pattern: "where:\\s*\\{\\s*(\\w+):"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: locations
```

**Index optimization:**

**Add indexes for frequently queried fields:**
```prisma
model Post {
  id        String   @id @default(cuid())
  title     String
  published Boolean  @default(false)
  authorId  String
  createdAt DateTime @default(now())
  
  // Single column indexes
  @@index([authorId])
  @@index([createdAt])
  
  // Composite index for common query pattern
  @@index([published, createdAt(sort: Desc)])
}
```

**When to add indexes:**
- Foreign keys used in WHERE clauses or joins
- Fields used in ORDER BY clauses
- Fields used in WHERE with pagination (cursor-based)
- Composite indexes for multi-field queries

**When NOT to add indexes:**
- Low-cardinality boolean fields (unless part of composite index)
- Fields that change frequently (writes become slower)
- Tables with very few rows

#### Optimize Connection Pooling

**Check database connection configuration:**
```yaml
precision_grep:
  queries:
    - id: prisma_config
      pattern: "PrismaClient\\(.*\\{[\\s\\S]*?\\}"
      glob: "**/*.{ts,tsx,js,jsx}"
      multiline: true
    - id: connection_string
      pattern: "connection_limit=|pool_timeout=|connect_timeout="
      glob: ".env*"
  output:
    format: context
    context_before: 3
    context_after: 3
```

**Optimal connection pool settings:**
```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

export { prisma };
```

**DATABASE_URL with connection pooling:**
```bash
# For serverless (Vercel, AWS Lambda) - use connection pooler
DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=10&pool_timeout=10"

# For long-running servers - higher limits
DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=20&pool_timeout=30"
```

### Phase 4: Rendering Performance

**Objective:** Eliminate unnecessary re-renders and optimize component rendering.

#### Detect Unnecessary Re-renders

**Find missing memoization:**

> **Note:** These patterns are approximations for single-line detection. Multi-line component definitions may require manual inspection.

```yaml
precision_grep:
  queries:
    - id: missing_memo
      pattern: "(const \\w+ = \\{|const \\w+ = \\[|const \\w+ = \\(.*\\) =>)(?!.*useMemo)"
      glob: "src/components/**/*.{tsx,jsx}"
    - id: missing_callback
      pattern: "(onChange|onClick|onSubmit)=\\{.*=>(?!.*useCallback)"
      glob: "src/components/**/*.{tsx,jsx}"
    - id: memo_usage
      pattern: "(useMemo|useCallback|React\\.memo)"
      glob: "**/*.{tsx,jsx}"
  output:
    format: files_only
```

**Memoization patterns:**

**Bad - recreates object on every render:**
```typescript
function UserProfile({ userId }: Props) {
  const user = useUser(userId);
  
  // New object reference on every render!
  const config = {
    showEmail: true,
    showPhone: false,
  };
  
  return <UserCard user={user} config={config} />;
}
```

**Good - memoize stable objects:**
```typescript
function UserProfile({ userId }: Props) {
  const user = useUser(userId);
  
  const config = useMemo(
    () => ({
      showEmail: true,
      showPhone: false,
    }),
    [] // Empty deps - never changes
  );
  
  return <UserCard user={user} config={config} />;
}
```

**Memoize callbacks:**
```typescript
function SearchBar({ onSearch }: Props) {
  const [query, setQuery] = useState('');
  
  // Memoize callback to prevent child re-renders
  const handleSubmit = useCallback(() => {
    onSearch(query);
  }, [query, onSearch]);
  
  return (
    <form onSubmit={handleSubmit}>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
    </form>
  );
}
```

**Memoize expensive components:**
```typescript
const ExpensiveChart = React.memo(
  function ExpensiveChart({ data }: Props) {
    // Heavy computation or rendering
    return <Chart data={data} />;
  },
  (prevProps, nextProps) => {
    // Custom comparison - only re-render if data changed
    return prevProps.data === nextProps.data;
  }
);
```

#### Check for Virtual List Usage

**Find large lists without virtualization:**
```yaml
precision_grep:
  queries:
    - id: large_maps
      pattern: "\\{.*\\.map\\(.*=>\\s*<(?!Virtualized)(?!VirtualList)"
      glob: "src/**/*.{tsx,jsx}"
    - id: virtualization
      pattern: "(react-window|react-virtualized|@tanstack/react-virtual)"
      glob: "package.json"
  output:
    format: locations
```

**Virtual list implementation:**
```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Estimated row height
    overscan: 5, // Render 5 extra rows for smooth scrolling
  });
  
  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            <ItemRow item={items[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Phase 5: Network Optimization

**Objective:** Reduce request waterfalls, enable caching, and optimize asset delivery.

#### Detect Request Waterfalls

**Find sequential data fetching:**
```yaml
precision_grep:
  queries:
    - id: sequential_fetches
      pattern: "await fetch.*\\n.*await fetch"
      glob: "**/*.{ts,tsx,js,jsx}"
      multiline: true
    - id: use_effect_fetches
      pattern: "useEffect\\(.*fetch"
      glob: "**/*.{tsx,jsx}"
  output:
    format: context
    context_before: 3
    context_after: 3
```

**Waterfall optimization:**

**Bad - sequential requests:**
```typescript
async function loadDashboard() {
  const userRes = await fetch('/api/user');
  if (!userRes.ok) throw new Error(`Failed to fetch user: ${userRes.status}`);
  const user = await userRes.json();
  
  const postsRes = await fetch(`/api/posts?userId=${user.id}`);
  if (!postsRes.ok) throw new Error(`Failed to fetch posts: ${postsRes.status}`);
  const posts = await postsRes.json();
  
  const commentsRes = await fetch(`/api/comments?userId=${user.id}`);
  if (!commentsRes.ok) throw new Error(`Failed to fetch comments: ${commentsRes.status}`);
  const comments = await commentsRes.json();
  
  return { user, posts, comments };
}
```

**Good - parallel requests:**
```typescript
async function loadDashboard(userId: string) {
  const [user, posts, comments] = await Promise.all([
    fetch(`/api/user/${userId}`).then(async r => {
      if (!r.ok) throw new Error(`Failed to fetch user: ${r.status}`);
      return r.json();
    }),
    fetch(`/api/posts?userId=${userId}`).then(async r => {
      if (!r.ok) throw new Error(`Failed to fetch posts: ${r.status}`);
      return r.json();
    }),
    fetch(`/api/comments?userId=${userId}`).then(async r => {
      if (!r.ok) throw new Error(`Failed to fetch comments: ${r.status}`);
      return r.json();
    }),
  ]);
  
  return { user, posts, comments };
}
```

**Best - server-side data aggregation:**
```typescript
// Single API endpoint that aggregates data server-side
async function loadDashboard(userId: string) {
  const response = await fetch(`/api/dashboard?userId=${userId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch dashboard: ${response.status}`);
  }
  const data = await response.json();
  return data;
}
```

#### Check Caching Headers

**Review cache configuration:**
```yaml
precision_grep:
  queries:
    - id: cache_headers
      pattern: "(Cache-Control|ETag|max-age|stale-while-revalidate)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: next_revalidate
      pattern: "(revalidate|force-cache|no-store)"
      glob: "src/app/**/*.{ts,tsx}"
  output:
    format: locations
```

**Next.js caching strategies:**

**Static data (updates rarely):**
```typescript
// app/products/page.tsx
export const revalidate = 3600; // Revalidate every hour

export default async function ProductsPage() {
  const products = await db.product.findMany();
  return <ProductList products={products} />;
}
```

**Dynamic data (real-time):**
```typescript
// app/api/posts/route.ts
export async function GET() {
  const posts = await db.post.findMany();
  
  return Response.json(posts, {
    headers: {
      'Cache-Control': 'private, max-age=60, stale-while-revalidate=300',
    },
  });
}
```

**Opt out of caching:**
```typescript
// app/api/user/route.ts
export const dynamic = 'force-dynamic';

export async function GET() {
  const user = await getCurrentUser();
  return Response.json(user);
}
```

#### Optimize Image Loading

**Check for image optimization:**
```yaml
precision_grep:
  queries:
    - id: img_tags
      pattern: "<img\\s+"
      glob: "**/*.{tsx,jsx,html}"
    - id: next_image
      pattern: "(next/image|Image\\s+from)"
      glob: "**/*.{tsx,jsx}"
  output:
    format: files_only
```

**Image optimization patterns:**

**Bad - unoptimized images:**
```tsx
<img src="/large-photo.jpg" alt="Photo" />
```

**Good - Next.js Image component:**
```tsx
import Image from 'next/image';

<Image
  src="/large-photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  loading="lazy"
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

**Responsive images:**
```tsx
<Image
  src="/photo.jpg"
  alt="Photo"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  style={{ objectFit: 'cover' }}
/>
```

### Phase 6: Memory Management

**Objective:** Detect memory leaks and optimize garbage collection.

#### Find Memory Leak Patterns

**Search for cleanup issues:**
```yaml
precision_grep:
  queries:
    - id: missing_cleanup
      pattern: "useEffect\\(.*\\{[^}]*addEventListener(?!.*return.*removeEventListener)"
      glob: "**/*.{tsx,jsx}"
      multiline: true
    - id: interval_leaks
      pattern: "(setInterval|setTimeout)(?!.*clear)"
      glob: "**/*.{tsx,jsx}"
    - id: subscription_leaks
      pattern: "subscribe\\((?!.*unsubscribe)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: context
    context_before: 3
    context_after: 3
```

**Memory leak patterns:**

**Bad - event listener leak:**
```typescript
useEffect(() => {
  window.addEventListener('resize', handleResize);
  // Missing cleanup!
}, []);
```

**Good - proper cleanup:**
```typescript
useEffect(() => {
  window.addEventListener('resize', handleResize);
  
  return () => {
    window.removeEventListener('resize', handleResize);
  };
}, []);
```

**Bad - interval leak:**
```typescript
useEffect(() => {
  const interval = setInterval(() => {
    fetchUpdates();
  }, 5000);
  // Missing cleanup!
}, []);
```

**Good - clear interval:**
```typescript
useEffect(() => {
  const interval = setInterval(() => {
    fetchUpdates();
  }, 5000);
  
  return () => {
    clearInterval(interval);
  };
}, []);
```

**Bad - fetch without abort:**
```typescript
useEffect(() => {
  fetch('/api/data')
    .then(r => r.json() as Promise<DataType>)
    .then(setData)
    .catch(console.error);
  // Missing abort on unmount!
}, []);
```

**Good - AbortController cleanup:**
```typescript
useEffect(() => {
  const controller = new AbortController();
  
  fetch('/api/data', { signal: controller.signal })
    .then(r => r.json() as Promise<DataType>)
    .then(setData)
    .catch(err => {
      if (err.name !== 'AbortError') console.error(err);
    });
  
  return () => controller.abort();
}, []);
```

**WeakRef pattern for caches:**
```typescript
class ImageCache {
  private cache = new Map<string, WeakRef<HTMLImageElement>>();
  
  get(url: string): HTMLImageElement | undefined {
    const ref = this.cache.get(url);
    return ref?.deref();
  }
  
  set(url: string, img: HTMLImageElement): void {
    this.cache.set(url, new WeakRef(img));
  }
}
```

### Phase 7: Server-Side Performance

**Objective:** Optimize SSR, streaming, and edge function performance.

#### Check for Blocking Server Components

**Find slow server components:**
```yaml
precision_grep:
  queries:
    - id: server_components
      pattern: "export default async function.*Page"
      glob: "src/app/**/page.{tsx,jsx}"
    - id: blocking_awaits
      pattern: "const.*await.*\\n.*const.*await"
      glob: "src/app/**/*.{tsx,jsx}"
      multiline: true
  output:
    format: locations
```

**Streaming with Suspense:**

**Bad - blocking entire page:**
```typescript
// app/dashboard/page.tsx
export default async function DashboardPage() {
  const user = await getUser();
  const posts = await getPosts(); // Blocks entire page!
  const analytics = await getAnalytics(); // Blocks entire page!
  
  return (
    <div>
      <UserProfile user={user} />
      <PostList posts={posts} />
      <Analytics data={analytics} />
    </div>
  );
}
```

**Good - streaming with Suspense:**
```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default async function DashboardPage() {
  // Only block on critical data
  const user = await getUser();
  
  return (
    <div>
      <UserProfile user={user} />
      
      <Suspense fallback={<PostListSkeleton />}>
        <PostList />
      </Suspense>
      
      <Suspense fallback={<AnalyticsSkeleton />}>
        <Analytics />
      </Suspense>
    </div>
  );
}

// Separate component for async data
async function PostList() {
  const posts = await getPosts();
  return <div>{/* render posts */}</div>;
}
```

#### Optimize Edge Functions

**Check edge runtime usage:**
```yaml
precision_grep:
  queries:
    - id: edge_config
      pattern: "export const runtime = ['\"](edge|nodejs)['\"]"
      glob: "**/*.{ts,tsx}"
    - id: edge_incompatible
      pattern: "(fs\\.|path\\.|process\\.cwd)"
      glob: "**/api/**/*.{ts,tsx}"
  output:
    format: locations
```

**Edge runtime best practices:**
```typescript
// app/api/geo/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  // Access edge-specific APIs
  const geo = request.headers.get('x-vercel-ip-country');
  
  return Response.json({
    country: geo,
    timestamp: Date.now(),
  });
}
```

### Phase 8: Core Web Vitals

**Objective:** Measure and optimize LCP, INP, and CLS.

#### Measure Web Vitals

**Add Web Vitals reporting:**
```typescript
// app/layout.tsx or app/web-vitals.tsx
'use client';

import { useEffect } from 'react';
import { onCLS, onFCP, onINP, onLCP, onTTFB } from 'web-vitals';

import type { Metric } from 'web-vitals';

function sendToAnalytics(metric: Metric) {
  const body = JSON.stringify(metric);
  const url = '/api/analytics';
  
  if (navigator.sendBeacon) {
    navigator.sendBeacon(url, body);
  } else {
    fetch(url, { body, method: 'POST', keepalive: true });
  }
}

export function WebVitals() {
  useEffect(() => {
    onCLS(sendToAnalytics);
    onFCP(sendToAnalytics);
    onINP(sendToAnalytics);
    onLCP(sendToAnalytics);
    onTTFB(sendToAnalytics);
  }, []);
  
  return null;
}
```

#### Optimize LCP (Largest Contentful Paint)

**Target: < 2.5s**

**Common LCP issues:**
- Large hero images not optimized
- Web fonts blocking render
- Server-side rendering too slow
- No resource prioritization

**Optimization:**
```tsx
// Priority image loading
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={630}
  priority // Preload this image!
/>

// Font optimization
<link
  rel="preload"
  href="/fonts/inter.woff2"
  as="font"
  type="font/woff2"
  crossOrigin="anonymous"
/>
```

#### Optimize INP (Interaction to Next Paint)

**Target: < 200ms**

**Common INP issues:**
- Heavy JavaScript blocking main thread
- Expensive event handlers
- Layout thrashing

**Optimization:**
```typescript
// Debounce expensive handlers
import { useDebouncedCallback } from 'use-debounce';

function SearchInput() {
  const debouncedSearch = useDebouncedCallback(
    (value: string) => {
      performSearch(value);
    },
    300 // Wait 300ms after user stops typing
  );
  
  return (
    <input
      onChange={(e) => debouncedSearch(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

#### Optimize CLS (Cumulative Layout Shift)

**Target: < 0.1**

**Common CLS issues:**
- Images without dimensions
- Ads or embeds without reserved space
- Web fonts causing FOIT/FOUT
- Dynamic content injection

**Optimization:**
```tsx
// Always specify image dimensions
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
/>

// Reserve space for dynamic content
<div style={{ minHeight: '200px' }}>
  <Suspense fallback={<Skeleton height={200} />}>
    <DynamicContent />
  </Suspense>
</div>

// Use font-display for web fonts
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap; // Prevent invisible text
}
```

## Audit Reporting

Structure findings with impact, effort, and priority:

### Report Template

```markdown
# Performance Audit Report

## Executive Summary
- **Date:** 2026-02-16
- **Auditor:** Engineer Agent
- **Scope:** Full application performance review
- **Overall Score:** 6.5/10

## Critical Issues (Fix Immediately)

### 1. N+1 Query in Post Listing
- **File:** `src/app/posts/page.tsx`
- **Issue:** Sequential database queries for each post author
- **Impact:** Page load time 3.2s -> should be <500ms
- **Effort:** 15 minutes
- **Fix:** Add `include: { author: true }` to findMany query

## High Priority (Fix This Week)

### 2. Missing Bundle Splitting
- **Files:** `src/app/admin/*`
- **Issue:** Admin panel code (250KB) loaded on all pages
- **Impact:** Initial bundle size 850KB -> should be <200KB
- **Effort:** 1 hour
- **Fix:** Use `next/dynamic` for admin routes

## Medium Priority (Fix This Month)

### 3. Unoptimized Images
- **Files:** Multiple components using `<img>` tags
- **Issue:** LCP of 4.1s due to large unoptimized images
- **Impact:** Poor Core Web Vitals, SEO penalty
- **Effort:** 2 hours
- **Fix:** Migrate to `next/image` with proper sizing

## Low Priority (Backlog)

### 4. Missing Memoization
- **Files:** `src/components/Dashboard/*.tsx`
- **Issue:** Unnecessary re-renders on state changes
- **Impact:** Minor UI lag on interactions
- **Effort:** 3 hours
- **Fix:** Add `useMemo`, `useCallback`, `React.memo`

## Performance Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| LCP | 4.1s | <2.5s | FAIL |
| INP | 180ms | <200ms | PASS |
| CLS | 0.05 | <0.1 | PASS |
| Bundle Size | 850KB | <200KB | FAIL |
| API Response | 320ms | <500ms | PASS |
```

## Validation Script

Use the validation script to verify audit completeness:

```bash
bash scripts/validate-performance-audit.sh
```

The script checks for:
- Bundle analysis artifacts
- Database query patterns
- Memoization usage
- Image optimization
- Caching headers

## References

See `references/performance-patterns.md` for detailed anti-patterns and optimization techniques.

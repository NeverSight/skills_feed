---
name: agentic-jumpstart-performance
description: Performance optimization patterns for TanStack Start with React 19, Vite, Drizzle ORM, and TanStack Query. Use when optimizing page load times, database queries, bundle size, caching, memoization, lazy loading, or when the user mentions performance, speed, optimization, or slow.
---

# Performance Optimization

## React 19 Performance Patterns

### Code Splitting with Lazy Loading

```typescript
import { lazy, Suspense } from "react";

// Lazy load heavy components
const HeavyEditor = lazy(() => import("./HeavyEditor"));
const DataVisualization = lazy(() => import("./DataVisualization"));

function Dashboard() {
  return (
    <Suspense fallback={<LoadingSkeleton />}>
      <HeavyEditor />
    </Suspense>
  );
}
```

### Strategic Memoization

```typescript
import { memo, useMemo, useCallback, useDeferredValue } from "react";

// Memoize expensive computations
const expensiveResult = useMemo(() => {
  return processLargeDataset(data);
}, [data]);

// Memoize callbacks passed to children
const handleClick = useCallback((id: number) => {
  updateItem(id);
}, [updateItem]);

// Defer non-critical updates
const deferredSearchTerm = useDeferredValue(searchTerm);

// Memoize components that receive stable props
const MemoizedList = memo(function List({ items }: { items: Item[] }) {
  return items.map(item => <ListItem key={item.id} item={item} />);
});
```

### Avoid Re-renders

```typescript
// BAD: Creates new object every render
<Component style={{ color: "red" }} />

// GOOD: Define outside or memoize
const style = { color: "red" };
<Component style={style} />

// BAD: Creates new function every render
<Button onClick={() => handleClick(id)} />

// GOOD: Use useCallback or define handler
const handleButtonClick = useCallback(() => handleClick(id), [id]);
<Button onClick={handleButtonClick} />
```

## TanStack Query Optimization

### Caching Configuration

```typescript
import { queryOptions } from "@tanstack/react-query";

// Configure stale time based on data freshness needs
export const segmentsQueryOptions = () =>
  queryOptions({
    queryKey: ["segments"],
    queryFn: () => getSegmentsFn(),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 30 * 60 * 1000,   // 30 minutes cache
  });

// For frequently changing data
export const statsQueryOptions = () =>
  queryOptions({
    queryKey: ["stats"],
    queryFn: () => getStatsFn(),
    staleTime: 30 * 1000,     // 30 seconds
    refetchInterval: 60 * 1000, // Auto-refetch every minute
  });
```

### Prefetching

```typescript
// Prefetch on route load
export const Route = createFileRoute("/courses/$courseId")({
  loader: async ({ params, context }) => {
    await context.queryClient.ensureQueryData(
      courseQueryOptions(params.courseId)
    );
  },
  component: CoursePage,
});

// Prefetch on hover
function CourseCard({ course }) {
  const queryClient = useQueryClient();

  const handleMouseEnter = () => {
    queryClient.prefetchQuery(courseQueryOptions(course.id));
  };

  return (
    <Link to={`/courses/${course.id}`} onMouseEnter={handleMouseEnter}>
      {course.title}
    </Link>
  );
}
```

### Optimistic Updates

```typescript
const mutation = useMutation({
  mutationFn: updateSegmentFn,
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: ["segments"] });
    const previous = queryClient.getQueryData(["segments"]);

    queryClient.setQueryData(["segments"], (old) =>
      old.map((s) => (s.id === newData.id ? { ...s, ...newData } : s))
    );

    return { previous };
  },
  onError: (err, newData, context) => {
    queryClient.setQueryData(["segments"], context.previous);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ["segments"] });
  },
});
```

## Database Query Optimization

### Select Only Required Columns

```typescript
// BAD: Fetches all columns
const users = await database.select().from(users);

// GOOD: Select only what you need
const users = await database
  .select({ id: users.id, name: users.name, email: users.email })
  .from(users);
```

### Use Indexes Effectively

```typescript
// Ensure indexes exist for frequently queried columns
// In schema definition:
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  createdAt: timestamp("created_at").defaultNow(),
}, (table) => ({
  emailIdx: index("email_idx").on(table.email),
  createdAtIdx: index("created_at_idx").on(table.createdAt),
}));
```

### Avoid N+1 Queries

```typescript
// BAD: N+1 query pattern
const segments = await getSegments();
for (const segment of segments) {
  segment.attachments = await getAttachments(segment.id);
}

// GOOD: Single query with join
const segmentsWithAttachments = await database
  .select()
  .from(segments)
  .leftJoin(attachments, eq(segments.id, attachments.segmentId));

// Or use Drizzle's with clause
const result = await database.query.segments.findMany({
  with: {
    attachments: true,
    module: true,
  },
});
```

### Pagination

```typescript
export async function getPaginatedUsers(page: number, limit: number) {
  const offset = (page - 1) * limit;

  const [data, [{ count }]] = await Promise.all([
    database
      .select()
      .from(users)
      .orderBy(desc(users.createdAt))
      .limit(limit)
      .offset(offset),
    database.select({ count: sql`count(*)` }).from(users),
  ]);

  return {
    data,
    pagination: {
      page,
      limit,
      total: Number(count),
      totalPages: Math.ceil(Number(count) / limit),
    },
  };
}
```

## Bundle Optimization

### Vite Configuration

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Split vendor chunks
          "react-vendor": ["react", "react-dom"],
          "query-vendor": ["@tanstack/react-query"],
          "ui-vendor": ["@radix-ui/react-dialog", "@radix-ui/react-dropdown-menu"],
        },
      },
    },
    // Enable minification
    minify: "terser",
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.logs in production
      },
    },
  },
});
```

### Dynamic Imports for Large Libraries

```typescript
// Dynamically import heavy libraries
async function processMarkdown(content: string) {
  const { marked } = await import("marked");
  return marked(content);
}

// For React components
const RichTextEditor = lazy(() => import("./RichTextEditor"));
const ChartComponent = lazy(() => import("recharts").then(mod => ({
  default: mod.ResponsiveContainer
})));
```

## Image & Media Optimization

### Lazy Loading Images

```typescript
function OptimizedImage({ src, alt }: { src: string; alt: string }) {
  return (
    <img
      src={src}
      alt={alt}
      loading="lazy"
      decoding="async"
    />
  );
}
```

### Video Loading Strategy

```typescript
function VideoPlayer({ videoKey }: { videoKey: string }) {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  // Load video URL only when component is visible
  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        loadVideoUrl(videoKey).then(setVideoUrl);
        observer.disconnect();
      }
    });

    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, [videoKey]);

  return videoUrl ? <video src={videoUrl} controls /> : <VideoSkeleton />;
}
```

## Tailwind CSS Optimization

### Purge Unused CSS

Tailwind v4 automatically purges unused styles in production. Ensure your content paths are correct:

```typescript
// tailwind.config.ts
export default {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
  ],
};
```

### Use CSS Variables for Theming

```css
/* Avoid redundant utility classes */
:root {
  --primary: theme(colors.blue.600);
  --primary-hover: theme(colors.blue.700);
}
```

## Memory Leak Prevention

### Cleanup Effects

```typescript
useEffect(() => {
  const controller = new AbortController();

  fetchData({ signal: controller.signal })
    .then(setData)
    .catch((err) => {
      if (err.name !== "AbortError") {
        setError(err);
      }
    });

  return () => controller.abort();
}, []);
```

### Event Listener Cleanup

```typescript
useEffect(() => {
  const handleResize = () => setWidth(window.innerWidth);
  window.addEventListener("resize", handleResize);
  return () => window.removeEventListener("resize", handleResize);
}, []);
```

## Performance Checklist

- [ ] Heavy components are lazy loaded with Suspense
- [ ] TanStack Query has appropriate staleTime/gcTime
- [ ] Database queries select only needed columns
- [ ] Joins are used instead of N+1 queries
- [ ] Large lists are paginated
- [ ] Bundle chunks are optimized for caching
- [ ] Images use loading="lazy"
- [ ] Effects clean up subscriptions and abort controllers
- [ ] Memoization is used strategically (not everywhere)
- [ ] Prefetching is used for predictable navigation

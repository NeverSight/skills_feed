---
name: react-performance
description: >-
  Comprehensive React and Next.js performance optimization guide. Covers
  waterfall elimination, bundle size reduction, server-side optimization,
  re-render prevention, and rendering performance. Use when building,
  reviewing, or optimizing React/Next.js applications for speed.
---

# React Performance

Systematic performance optimization for React and Next.js applications, organized by impact.

## Priority 1: Eliminate Waterfalls (CRITICAL)

Sequential async operations are the single biggest performance killer. Fix these first.

### Defer Await

Move `await` to the point of use, not the point of declaration.

```tsx
// BAD: Sequential — total time = fetch1 + fetch2
async function Page() {
  const user = await getUser();
  const posts = await getPosts(user.id);
  return <Feed user={user} posts={posts} />;
}

// GOOD: Parallel where possible
async function Page() {
  const userPromise = getUser();
  const postsPromise = getPosts(); // if independent
  const [user, posts] = await Promise.all([userPromise, postsPromise]);
  return <Feed user={user} posts={posts} />;
}
```

### Suspense Streaming

Wrap slow data behind `<Suspense>` so the shell renders instantly.

```tsx
export default function Page() {
  return (
    <main>
      <Header />              {/* instant */}
      <Suspense fallback={<Skeleton />}>
        <SlowDataSection />   {/* streams in */}
      </Suspense>
    </main>
  );
}
```

### Partial Dependencies

When promises have partial dependencies, start independent work immediately.

```tsx
async function Dashboard() {
  const userPromise = getUser();
  const settingsPromise = getSettings(); // independent

  const user = await userPromise;
  const postsPromise = getPosts(user.id); // depends on user

  const [settings, posts] = await Promise.all([settingsPromise, postsPromise]);
  return <View user={user} settings={settings} posts={posts} />;
}
```

## Priority 2: Bundle Size (CRITICAL)

### Direct Imports

Never import from barrel files in production code.

```tsx
// BAD: Pulls entire library
import { Button } from '@/components';
import { format } from 'date-fns';

// GOOD: Tree-shakeable
import { Button } from '@/components/ui/button';
import { format } from 'date-fns/format';
```

### Dynamic Imports

Code-split heavy components that aren't needed on initial render.

```tsx
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('@/components/chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,  // skip SSR for client-only components
});

const Editor = dynamic(() => import('@/components/editor'), {
  loading: () => <EditorSkeleton />,
});
```

### Defer Third-Party Scripts

Load analytics, logging, and non-critical scripts after hydration.

```tsx
// BAD: Blocks hydration
import { analytics } from 'heavy-analytics';
analytics.init();

// GOOD: Load after hydration
useEffect(() => {
  import('heavy-analytics').then(({ analytics }) => analytics.init());
}, []);
```

### Preload on Intent

Preload resources when user shows intent (hover, focus).

```tsx
function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  const router = useRouter();
  return (
    <Link
      href={href}
      onMouseEnter={() => router.prefetch(href)}
      onFocus={() => router.prefetch(href)}
    >
      {children}
    </Link>
  );
}
```

## Priority 3: Server-Side Performance (HIGH)

### Request-Scoped Deduplication

Use `React.cache()` to deduplicate data fetches within a single request.

```tsx
import { cache } from 'react';

export const getUser = cache(async (id: string) => {
  return db.user.findUnique({ where: { id } });
});

// Called in layout.tsx AND page.tsx — only one DB query
```

### Minimize Serialization

Only pass the data client components actually need.

```tsx
// BAD: Serializes entire user object
<ClientAvatar user={user} />

// GOOD: Pass only what's needed
<ClientAvatar name={user.name} avatarUrl={user.avatarUrl} />
```

### Non-Blocking Background Work

Use `after()` for work that shouldn't block the response.

```tsx
import { after } from 'next/server';

export async function POST(request: Request) {
  const data = await processRequest(request);

  after(async () => {
    await logAnalytics(data);
    await sendNotification(data);
  });

  return Response.json(data); // returns immediately
}
```

## Priority 4: Re-render Prevention (MEDIUM)

### Derived State

Compute derived values during render, never in effects.

```tsx
// BAD: Extra render cycle
const [items, setItems] = useState([]);
const [count, setCount] = useState(0);
useEffect(() => setCount(items.length), [items]);

// GOOD: Derive during render
const [items, setItems] = useState([]);
const count = items.length;
```

### Stable References

Use callback-based setState and extract callbacks outside render.

```tsx
// BAD: New function every render
<Button onClick={() => setCount(count + 1)} />

// GOOD: Stable reference
<Button onClick={() => setCount(c => c + 1)} />
```

### Primitive Dependencies

Use primitives in dependency arrays to avoid false positives.

```tsx
// BAD: Object reference changes every render
useEffect(() => { ... }, [config]);

// GOOD: Primitive values are stable
useEffect(() => { ... }, [config.apiUrl, config.timeout]);
```

### Lazy State Initialization

Pass initializer functions for expensive initial state.

```tsx
// BAD: Runs every render
const [data, setData] = useState(expensiveParse(raw));

// GOOD: Runs only on mount
const [data, setData] = useState(() => expensiveParse(raw));
```

### Memoize Expensive Components

Extract heavy computation into memoized child components.

```tsx
const ExpensiveList = memo(function ExpensiveList({ items }: { items: Item[] }) {
  return items.map(item => <ComplexItem key={item.id} item={item} />);
});
```

### useTransition for Deferrable Updates

Use `startTransition` for non-urgent state updates.

```tsx
const [isPending, startTransition] = useTransition();

function handleSearch(query: string) {
  setInputValue(query);                    // urgent: update input
  startTransition(() => setResults(search(query))); // deferrable: update results
}
```

## Priority 5: Rendering Performance (LOW-MEDIUM)

### Content Visibility

Apply CSS `content-visibility` for long scrollable lists.

```css
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

### Hoist Static JSX

Extract JSX that doesn't depend on props/state outside the component.

```tsx
// BAD: Recreated every render
function Layout({ children }) {
  return (
    <div>
      <footer><p>Copyright 2026</p></footer>
      {children}
    </div>
  );
}

// GOOD: Created once
const footer = <footer><p>Copyright 2026</p></footer>;
function Layout({ children }) {
  return <div>{footer}{children}</div>;
}
```

### Conditional Rendering

Prefer ternary over `&&` to avoid rendering `0` or `""`.

```tsx
// BAD: Renders "0" when count is 0
{count && <Badge count={count} />}

// GOOD: Explicit boolean check
{count > 0 ? <Badge count={count} /> : null}
```

## Quick Reference

| Issue | Fix | Priority |
|-------|-----|----------|
| Sequential fetches | `Promise.all()` / Suspense | CRITICAL |
| Barrel imports | Direct path imports | CRITICAL |
| Large initial bundle | `next/dynamic` | CRITICAL |
| Redundant DB calls | `React.cache()` | HIGH |
| Over-serialized props | Pass primitives only | HIGH |
| Derived state in useEffect | Compute during render | MEDIUM |
| Unstable callbacks | `useCallback` / callback setState | MEDIUM |
| Long lists | Virtualization + `content-visibility` | MEDIUM |
| Non-urgent updates | `useTransition` | MEDIUM |

---
name: react-best-practices
description: Apply React best practices when writing or reviewing React code. Use when building components, reviewing PRs, refactoring React code, fixing performance issues, debugging re-renders, structuring state and data flow, converting useEffect to loaders, building forms, or asking "how should I structure this component".
license: MIT
metadata:
  author: kota
  version: "1.2.0"
---

# React Best Practices

## Preconditions

Before applying these practices, confirm:

1. **Stack check** - Verify React Router 7 is in use (or note if using different router/framework)
2. **TypeScript** - Confirm TypeScript is configured with `strict: true`
3. **Existing patterns** - Review existing codebase patterns for consistency

If the codebase uses a different data fetching approach (TanStack Query, SWR, etc.), adapt the data fetching guidance accordingly.

## Steps

When writing or reviewing React code:

1. **Audit useEffect usage** - For each useEffect, ask "Can this be derived state, an event handler, or handled by the router?"
2. **Choose state placement** - Follow the hierarchy: component → URL → lifted → context
3. **Verify data fetching** - Ensure loaders/actions (or client cache) handle fetching, not raw useEffect
4. **Check component design** - Apply composition patterns, verify single responsibility
5. **Validate keys** - Ensure list keys are stable and unique (not index or random)
6. **Review TypeScript** - Props have explicit interfaces, no `any` types
7. **Check accessibility** - Semantic HTML, focus management, keyboard support
8. **Profile if needed** - Only add memoization after measuring; consider `useTransition`/`useDeferredValue` first

## Examples

### Example 1: Refactor effect-heavy component

**User prompt:** "This component has too many useEffects, can you clean it up?"

**Agent behavior:**
1. Identify each useEffect and categorize: derived state? event response? data fetch? external sync?
2. Convert derived state to render-time calculations
3. Move event responses into event handlers
4. Replace data fetching with loader or client cache
5. Keep only effects that sync with external systems
6. Verify cleanup functions exist where needed

### Example 2: Convert fetch-in-effect to loader

**User prompt:** "Migrate this component to use React Router loaders"

**Agent behavior:**
1. Identify the useEffect doing the fetch
2. Create a loader function in the route definition
3. Replace useState + useEffect with useLoaderData()
4. Handle loading states via useNavigation() instead of local state
5. Move error handling to the loader or errorElement
6. Remove the now-unnecessary effect and state

### Example 3: Fix list performance issues

**User prompt:** "This list re-renders constantly and is slow"

**Agent behavior:**
1. Check key prop - ensure stable IDs, not index or random
2. Profile to identify expensive renders
3. Wrap list item component in React.memo if pure
4. Ensure callbacks passed to items use useCallback
5. Check if parent state changes are causing unnecessary re-renders
6. Consider virtualization for very long lists

---

## Core Principle: Avoid useEffect

Most useEffect usage is unnecessary. Before reaching for useEffect, ask: "Can this be done another way?"

### Do NOT Use useEffect For

**Derived state** - Calculate during render:

```tsx
// BAD
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// GOOD
const fullName = `${firstName} ${lastName}`;
```

**Event responses** - Handle in event handlers:

```tsx
// BAD
const [submitted, setSubmitted] = useState(false);
useEffect(() => {
  if (submitted) {
    submitForm(data);
  }
}, [submitted, data]);

// GOOD
function handleSubmit() {
  submitForm(data);
}
```

**Initializing state** - Use useState initializer:

```tsx
// BAD
const [items, setItems] = useState([]);
useEffect(() => {
  setItems(getInitialItems());
}, []);

// GOOD
const [items, setItems] = useState(() => getInitialItems());
```

**Data fetching** - Use React Router loaders (see below).

### When useEffect IS Appropriate

- Subscribing to external systems (WebSocket, browser APIs)
- Third-party library integration (charts, maps, video players)
- Event listeners that need cleanup
- Synchronizing with non-React code

When you must use useEffect:

```tsx
useEffect(() => {
  const connection = createConnection(roomId);
  connection.connect();
  return () => connection.disconnect(); // Always clean up
}, [roomId]);
```

## Hooks Hygiene

### Dependency Arrays

**Never disable `exhaustive-deps`** without a very good reason. If you think you need to:

1. The effect probably shouldn't be an effect
2. You may need useCallback/useMemo for stable references
3. Consider useRef for values that shouldn't trigger re-runs

```tsx
// BAD - suppressing the linter
useEffect(() => {
  doSomething(value);
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []); // Missing 'value'

// GOOD - fix the actual issue
const stableCallback = useCallback(() => doSomething(value), [value]);
useEffect(() => {
  stableCallback();
}, [stableCallback]);
```

### StrictMode Double Invocation

In development, React StrictMode intentionally double-invokes effects to help find bugs. Your effects should handle this:

- Effects run setup → cleanup → setup
- If this breaks something, your effect has a bug (usually missing cleanup)
- This helps catch issues before production

### useLayoutEffect

Use `useLayoutEffect` only when you need to measure DOM or prevent visual flicker:

```tsx
// useLayoutEffect - runs synchronously after DOM mutations
useLayoutEffect(() => {
  const rect = ref.current.getBoundingClientRect();
  setPosition({ top: rect.top, left: rect.left });
}, []);

// useEffect - runs after paint (preferred for most cases)
useEffect(() => {
  trackPageView();
}, []);
```

Prefer `useEffect` unless you see visual flicker that `useLayoutEffect` would fix.

## Data Fetching with React Router 7

Prefer framework-level data fetching over useEffect. Use React Router's loaders and actions.

**If not using React Router loaders**, use a client cache library (TanStack Query, SWR) which handles:
- Request deduplication
- Caching and revalidation
- Race condition prevention
- Loading/error states

**If you must fetch in useEffect** (rare), handle cleanup and race conditions:

```tsx
useEffect(() => {
  let cancelled = false;
  const controller = new AbortController();

  async function fetchData() {
    try {
      const res = await fetch("/api/data", { signal: controller.signal });
      if (!cancelled) setData(await res.json());
    } catch (e) {
      if (!cancelled && e.name !== "AbortError") setError(e);
    }
  }
  fetchData();

  return () => {
    cancelled = true;
    controller.abort();
  };
}, []);
```

### Loaders for Reading Data

```tsx
// In route definition
{
  path: "posts",
  element: <Posts />,
  loader: async () => {
    const posts = await fetch("/api/posts").then(r => r.json());
    return { posts };
  }
}

// In component
function Posts() {
  const { posts } = useLoaderData();
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

### Actions for Mutations

```tsx
// In route definition
{
  path: "posts/new",
  element: <NewPost />,
  action: async ({ request }) => {
    const formData = await request.formData();
    // Note: formData.get() returns FormDataEntryValue (string | File) or null
    const title = formData.get("title");
    if (typeof title !== "string") {
      return { error: "Title is required" };
    }

    const response = await fetch("/api/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });

    if (!response.ok) {
      return { error: "Failed to create post" };
    }

    return redirect("/posts");
  }
}

// In component - use Form, not onSubmit with fetch
function NewPost() {
  const navigation = useNavigation();
  const isSubmitting = navigation.state === "submitting";

  return (
    <Form method="post">
      <input name="title" required />
      <button disabled={isSubmitting}>
        {isSubmitting ? "Creating..." : "Create"}
      </button>
    </Form>
  );
}
```

### Key Hooks

- `useLoaderData()` - Access loader data
- `useActionData()` - Access action return value (errors, etc.)
- `useNavigation()` - Track navigation/submission state
- `useFetcher()` - For mutations without navigation

## State Management

### State Placement Hierarchy

Place state as close to where it's used as possible:

1. **Component state** - useState for local UI state
2. **URL state** - Query params for shareable state
3. **Lifted state** - Shared parent for sibling communication
4. **Context** - Deeply nested access (use sparingly)

### URL State for Shareable UI

Use URL query params for state that should be shareable or bookmarkable:

```tsx
// BAD - modal state lost on refresh/share
const [isOpen, setIsOpen] = useState(false);

// GOOD - modal state in URL
import { useSearchParams } from "react-router";

function ProductPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const isModalOpen = searchParams.get("modal") === "open";

  function openModal() {
    setSearchParams({ modal: "open" });
  }

  function closeModal() {
    setSearchParams({});
  }

  return (
    <>
      <button onClick={openModal}>View Details</button>
      {isModalOpen && <Modal onClose={closeModal} />}
    </>
  );
}
```

Good candidates for URL state:
- Modal/dialog open state
- Active tab
- Filter/sort options
- Pagination
- Search queries

### useState vs useReducer

- **useState** - Simple values, independent updates
- **useReducer** - Complex state, related values that change together

```tsx
// Good useReducer candidate - related state
const [state, dispatch] = useReducer(formReducer, {
  values: {},
  errors: {},
  touched: {},
  isSubmitting: false
});
```

### Context Pitfalls

Avoid single large context - it causes unnecessary re-renders:

```tsx
// BAD - all consumers re-render on any change
<AppContext.Provider value={{ user, theme, settings, cart }}>

// GOOD - separate contexts by domain
<UserContext.Provider value={user}>
  <ThemeContext.Provider value={theme}>
    <CartContext.Provider value={cart}>
```

### Memoize Provider Values

Always memoize context values to prevent unnecessary re-renders:

```tsx
// BAD - new object every render
<ThemeContext.Provider value={{ theme, setTheme }}>

// GOOD - memoized value
const value = useMemo(() => ({ theme, setTheme }), [theme]);
<ThemeContext.Provider value={value}>
```

### High-Churn State

For frequently updating state (mouse position, animations), consider:

- `useSyncExternalStore` for external state stores
- Zustand, Jotai, or similar for fine-grained subscriptions
- Keep high-churn state out of Context entirely

## Component Design

### Composition Over Configuration

Build flexible components using composition, not props. Follow shadcn/ui patterns:

```tsx
// BAD - configuration via props
<Dialog
  title="Edit Profile"
  description="Make changes here"
  content={<ProfileForm />}
  onConfirm={handleSave}
  onCancel={handleClose}
/>

// GOOD - composition via children
<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Edit Profile</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>
      <DialogDescription>Make changes here</DialogDescription>
    </DialogHeader>
    <ProfileForm />
    <DialogFooter>
      <DialogClose asChild>
        <Button variant="outline">Cancel</Button>
      </DialogClose>
      <Button onClick={handleSave}>Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Single Responsibility

Each component should do one thing well. Signs you need to split:

- Component file exceeds ~200 lines
- Multiple unrelated pieces of state
- Hard to name the component
- Difficult to test in isolation

### Custom Hooks for Reusable Logic

Extract stateful logic into custom hooks:

```tsx
// Custom hook encapsulates complexity
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Component stays simple
function Search() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 300);
  // Use debouncedQuery for API calls
}
```

## Keys and Reconciliation

### Key Rules

1. **Use stable, unique IDs** - preferably from your data
2. **Never use array index** for dynamic lists (reordering, filtering, adding)
3. **Never use random values** - forces remount on every render
4. **Keys only need sibling uniqueness**

```tsx
// BAD
{items.map((item, index) => <Item key={index} {...item} />)}
{items.map(item => <Item key={Math.random()} {...item} />)}

// GOOD
{items.map(item => <Item key={item.id} {...item} />)}
```

### Using Keys to Reset State

Pass a key to reset component state completely:

```tsx
// Reset form when editing different user
<UserForm key={userId} user={user} />
```

## Performance

### When to Optimize

Don't optimize prematurely. Profile first, then optimize bottlenecks.

### React.memo

Wrap expensive pure components:

```tsx
const ExpensiveList = memo(function ExpensiveList({ items }: Props) {
  return items.map(item => <ExpensiveItem key={item.id} item={item} />);
});
```

### useMemo for Expensive Calculations

```tsx
// Use toSorted() or spread to avoid mutating the original array
const sortedItems = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

### useCallback for Stable References

Only needed when passing callbacks to memoized children:

```tsx
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

return <MemoizedList items={items} onItemClick={handleClick} />;
```

### Concurrent Rendering for Expensive Updates

For expensive state updates, prefer concurrent features over aggressive memoization:

```tsx
const [isPending, startTransition] = useTransition();

function handleFilter(value: string) {
  setInputValue(value); // Urgent: update input immediately

  startTransition(() => {
    setFilteredItems(expensiveFilter(items, value)); // Non-blocking
  });
}

return (
  <>
    <input value={inputValue} onChange={e => handleFilter(e.target.value)} />
    {isPending && <Spinner />}
    <ItemList items={filteredItems} />
  </>
);
```

See the Concurrent Rendering section below for full details on `useTransition` and `useDeferredValue`.

## Concurrent Rendering

React 18 introduced concurrent features for keeping the UI responsive during expensive updates.

### useTransition

Mark state updates as non-blocking so user interactions aren't delayed:

```tsx
const [isPending, startTransition] = useTransition();

function handleTabChange(tab: string) {
  startTransition(() => {
    setActiveTab(tab); // Can be interrupted by more urgent updates
  });
}

return (
  <>
    <TabBar activeTab={activeTab} onChange={handleTabChange} />
    {isPending ? <TabSkeleton /> : <TabContent tab={activeTab} />}
  </>
);
```

**Use cases:**
- Search/filter with expensive result rendering
- Tab switching with heavy content
- Any state update causing expensive re-renders

### useDeferredValue

Defer expensive derived values when you don't control the state setter:

```tsx
function SearchResults({ query }: { query: string }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  return (
    <div style={{ opacity: isStale ? 0.7 : 1 }}>
      <ExpensiveList query={deferredQuery} />
    </div>
  );
}
```

**When to use:**
- Props from parent that change frequently
- Alternative to debouncing for render performance
- Showing stale content while fresh content loads

### useTransition vs useDeferredValue

| Scenario | Use |
|----------|-----|
| You control the state setter | `useTransition` |
| Value comes from props | `useDeferredValue` |
| Need `isPending` indicator | `useTransition` |
| Deferring derived/computed values | `useDeferredValue` |

### When NOT to Use

Don't use concurrent features for:
- Controlled input values (causes typing lag)
- Quick/cheap state updates
- State that must stay synchronized

## Code Splitting

Split code into smaller bundles that load on demand.

### React.lazy with Suspense

```tsx
import { lazy, Suspense } from "react";

const Dashboard = lazy(() => import("./Dashboard"));

function App() {
  return (
    <Suspense fallback={<DashboardSkeleton />}>
      <Dashboard />
    </Suspense>
  );
}
```

### Route-Based Splitting (Preferred)

React Router's `lazy` option loads routes in parallel, avoiding waterfalls:

```tsx
const router = createBrowserRouter([
  { path: "/", element: <Home /> },
  { path: "/dashboard", lazy: () => import("./Dashboard") },
  { path: "/settings", lazy: () => import("./Settings") }
]);
```

This is preferred over `React.lazy` for routes because:
- Routes load in parallel before rendering
- `React.lazy` only fetches when the component renders (waterfall)

### Suspense for Loading States

Use nested Suspense boundaries for progressive loading:

```tsx
<Suspense fallback={<PageSkeleton />}>
  <Header />
  <Suspense fallback={<ContentSkeleton />}>
    <MainContent />
  </Suspense>
  <Suspense fallback={<SidebarSkeleton />}>
    <Sidebar />
  </Suspense>
</Suspense>
```

## Error Handling

### Error Boundaries

React requires a class component for error boundaries, or use `react-error-boundary` library:

```tsx
// Using react-error-boundary (recommended)
import { ErrorBoundary } from "react-error-boundary";

<ErrorBoundary fallback={<ErrorMessage />}>
  <RiskyComponent />
</ErrorBoundary>

// Or with React Router 7, use route-level errorElement
{
  path: "dashboard",
  element: <Dashboard />,
  errorElement: <DashboardError />
}
```

### Async Error Handling

Handle errors in loaders/actions, not components:

```tsx
// In loader
export async function loader() {
  try {
    const data = await fetchData();
    return { data };
  } catch (error) {
    throw new Response("Failed to load", { status: 500 });
  }
}
```

## TypeScript

### Props Interfaces

Define explicit interfaces, avoid React.FC:

```tsx
// GOOD
interface ButtonProps {
  variant?: "primary" | "secondary";
  children: React.ReactNode;
  onClick?: () => void;
}

function Button({ variant = "primary", children, onClick }: ButtonProps) {
  return <button className={variant} onClick={onClick}>{children}</button>;
}
```

### Avoid `any`

Use `unknown` when type is truly unknown, then narrow:

```tsx
// BAD
function handleError(error: any) {
  console.log(error.message);
}

// GOOD
function handleError(error: unknown) {
  if (error instanceof Error) {
    console.log(error.message);
  }
}
```

### Utility Types

```tsx
// Extend HTML element props
type ButtonProps = React.ComponentProps<"button"> & {
  variant?: "primary" | "secondary";
};

// Children included
type CardProps = React.PropsWithChildren<{
  title: string;
}>;
```

## Accessibility

### useId for Label Wiring

Use `useId` for accessible form labels - never hardcode IDs:

```tsx
function TextField({ label }: { label: string }) {
  const id = useId();

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} type="text" />
    </div>
  );
}
```

### Focus Management

Manage focus for modals and dynamic content:

```tsx
function Modal({ onClose }: { onClose: () => void }) {
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    closeButtonRef.current?.focus();
  }, []);

  return (
    <div role="dialog" aria-modal="true">
      <button ref={closeButtonRef} onClick={onClose}>Close</button>
    </div>
  );
}
```

### Modal Requirements

Modals must:
- Trap focus within the modal while open
- Close on Escape key press
- Return focus to trigger element on close
- Prevent background scroll

**Prefer proven primitives** like Radix UI, Headless UI, or React Aria for complex interactive components (dialogs, dropdowns, tabs). They handle these requirements correctly.

### Keyboard Navigation

Ensure all interactive elements are keyboard accessible:
- Focusable via Tab
- Activatable via Enter/Space
- Custom widgets follow WAI-ARIA patterns

## Common Anti-Patterns to Avoid

1. **Mutating state directly** - Always create new objects/arrays
2. **Over-using Context** - Not everything needs global state
3. **Prop drilling** vs **over-abstraction** - 2-3 levels is fine
4. **Storing derived values** - Calculate during render
5. **useEffect for everything** - Most cases have better alternatives
6. **Premature optimization** - Profile first

## Reference Documentation

For the latest patterns, instruct the agent to query documentation:

- **React docs**: Use Context7 with library ID `/websites/react_dev`
- **React Router 7**: Use Context7 with library ID `/remix-run/react-router`
- **shadcn/ui**: Use Context7 with library ID `/websites/ui_shadcn`

Example query for useEffect alternatives:
```
Query Context7 /websites/react_dev for "you might not need an effect derived state event handlers"
```

### Performance Optimization (Next.js)

For in-depth performance optimization patterns, see the Vercel React Best Practices skill:
- **GitHub**: `vercel-labs/agent-skills` → `skills/react-best-practices`
- **Focus**: 57 performance rules covering waterfalls, bundle size, re-renders, hydration
- **Note**: Contains Next.js-specific patterns (next/dynamic, server components). Adapt for React Router 7 where applicable, or disregard Next.js-specific guidance when working on non-Next.js projects.

---
name: component-optimization
description: React performance optimization patterns - React.memo, useMemo, useCallback, code splitting, and preventing unnecessary re-renders
tags: [react, performance, optimization, memoization]
version: 1.0.0
author: Code Visionary
---

# Component Optimization

Master React performance optimization techniques. Learn how to identify and fix performance bottlenecks, prevent unnecessary re-renders, and create fast, responsive UIs.

## Quick Reference

### Prevent Re-renders with React.memo

```typescript
const MemoizedComponent = React.memo(function Component({ data }) {
  return <div>{data}</div>;
});
```

### Memoize Expensive Calculations

```typescript
const result = useMemo(() => 
  expensiveCalculation(data), 
  [data]
);
```

### Memoize Callback Functions

```typescript
const handleClick = useCallback(() => {
  doSomething(value);
}, [value]);
```

### Code Splitting

```typescript
const LazyComponent = lazy(() => import('./Component'));

<Suspense fallback={<Spinner />}>
  <LazyComponent />
</Suspense>
```

## When to Use This Skill

- Component renders slowly or causes UI lag
- Large lists or tables perform poorly
- Callbacks cause child components to re-render
- Initial page load is too slow
- Bundle size is too large
- Profiler shows unnecessary re-renders

## Understanding Re-renders

### When Does React Re-render?

React re-renders a component when:
1. **State changes** - `useState` or `useReducer` updates
2. **Props change** - Parent passes new props
3. **Parent re-renders** - By default, all children re-render
4. **Context changes** - Any context value updates

### The Re-render Problem

```tsx
// ❌ PROBLEM: Child re-renders unnecessarily
function Parent() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
      <ExpensiveChild /> {/* Re-renders every time! */}
    </div>
  );
}
```

Even though `ExpensiveChild` doesn't use `count`, it re-renders whenever the parent does.

## Optimization Techniques

### 1. React.memo - Prevent Unnecessary Re-renders

`React.memo` skips re-rendering if props haven't changed.

```tsx
// ✅ SOLUTION: Memoize the child
const ExpensiveChild = React.memo(function ExpensiveChild() {
  console.log("ExpensiveChild rendered");
  
  return (
    <div>
      {/* Expensive rendering logic */}
    </div>
  );
});

function Parent() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
      <ExpensiveChild /> {/* No longer re-renders! */}
    </div>
  );
}
```

**When to use:**
- Component renders often but props rarely change
- Component has expensive rendering logic
- Component is large with many children

**When NOT to use:**
- Props change frequently
- Component is simple and fast
- Premature optimization

### 2. useMemo - Memoize Expensive Calculations

`useMemo` caches calculation results between renders.

```tsx
function ProductList({ products, filters }) {
  // ❌ Recalculates on every render
  const filtered = products.filter(p => 
    p.category === filters.category
  );
  
  // ✅ Only recalculates when dependencies change
  const filtered = useMemo(
    () => products.filter(p => p.category === filters.category),
    [products, filters.category]
  );
  
  return (
    <ul>
      {filtered.map(product => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  );
}
```

**When to use:**
- Expensive calculations (filtering, sorting, mapping large arrays)
- Derived state from props or state
- Creating objects/arrays passed as props to memoized children

**When NOT to use:**
- Simple calculations (they're fast enough)
- Values that change every render anyway
- Premature optimization

### 3. useCallback - Memoize Functions

`useCallback` prevents creating new function instances on every render.

```tsx
function TodoList({ todos }) {
  const [filter, setFilter] = useState("all");
  
  // ❌ New function every render, breaks React.memo
  const handleComplete = (id) => {
    completeTodo(id);
  };
  
  // ✅ Same function reference between renders
  const handleComplete = useCallback((id) => {
    completeTodo(id);
  }, []);
  
  return (
    <ul>
      {todos.map(todo => (
        <MemoizedTodoItem
          key={todo.id}
          todo={todo}
          onComplete={handleComplete}
        />
      ))}
    </ul>
  );
}
```

**When to use:**
- Passing callbacks to memoized children
- Functions used in dependency arrays
- Functions passed to many children

**When NOT to use:**
- Functions not passed as props
- Parent component re-renders frequently anyway
- Simple event handlers

### 4. Code Splitting with React.lazy

Split large components into separate bundles that load on demand.

```tsx
import { lazy, Suspense } from "react";

// ✅ Only loads when needed
const AdminPanel = lazy(() => import("./AdminPanel"));
const Charts = lazy(() => import("./Charts"));

function Dashboard() {
  const [showAdmin, setShowAdmin] = useState(false);
  
  return (
    <div>
      <h1>Dashboard</h1>
      
      {showAdmin && (
        <Suspense fallback={<Spinner />}>
          <AdminPanel />
        </Suspense>
      )}
      
      <Suspense fallback={<ChartsSkeleton />}>
        <Charts />
      </Suspense>
    </div>
  );
}
```

**When to use:**
- Large components not needed initially
- Admin/authenticated sections
- Modals and dialogs
- Route-based code splitting

### 5. Virtualization for Long Lists

Render only visible items in long lists.

```tsx
import { useVirtualizer } from "@tanstack/react-virtual";

function VirtualList({ items }) {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });
  
  return (
    <div ref={parentRef} style={{ height: "400px", overflow: "auto" }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            {items[virtualItem.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

**When to use:**
- Lists with 100+ items
- Tables with many rows
- Infinite scrolling
- Chat messages or feeds

## Advanced Patterns

### 1. Context Optimization

Split contexts to prevent unnecessary re-renders:

```tsx
// ❌ Everything re-renders when anything changes
const AppContext = createContext({
  user: null,
  theme: "light",
  settings: {},
});

// ✅ Separate contexts for independent data
const UserContext = createContext(null);
const ThemeContext = createContext("light");
const SettingsContext = createContext({});

function App() {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState("light");
  const [settings, setSettings] = useState({});
  
  return (
    <UserContext.Provider value={user}>
      <ThemeContext.Provider value={theme}>
        <SettingsContext.Provider value={settings}>
          <AppContent />
        </SettingsContext.Provider>
      </ThemeContext.Provider>
    </UserContext.Provider>
  );
}
```

### 2. Component Composition vs Props

Use children instead of passing components as props:

```tsx
// ❌ Slower prop creates new component
function Parent({ content }) {
  const [state, setState] = useState(0);
  return <div>{content}</div>;
}

<Parent content={<ExpensiveComponent />} />

// ✅ Faster - children don't re-render
function Parent({ children }) {
  const [state, setState] = useState(0);
  return <div>{children}</div>;
}

<Parent>
  <ExpensiveComponent />
</Parent>
```

### 3. State Colocation

Move state closer to where it's used:

```tsx
// ❌ Top-level state causes full tree re-render
function App() {
  const [color, setColor] = useState("blue");
  
  return (
    <div>
      <ColorPicker color={color} onChange={setColor} />
      <ExpensiveComponent />
      <AnotherExpensiveComponent />
    </div>
  );
}

// ✅ Isolated state only affects relevant components
function App() {
  return (
    <div>
      <ColorPickerSection />
      <ExpensiveComponent />
      <AnotherExpensiveComponent />
    </div>
  );
}

function ColorPickerSection() {
  const [color, setColor] = useState("blue");
  return <ColorPicker color={color} onChange={setColor} />;
}
```

## Profiling Performance

### 1. React DevTools Profiler

```tsx
// Add Profiler to measure render times
import { Profiler } from "react";

function App() {
  return (
    <Profiler id="App" onRender={onRenderCallback}>
      <AppContent />
    </Profiler>
  );
}

function onRenderCallback(
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
}
```

### 2. Performance Timeline

```tsx
// Mark performance in browser DevTools
function expensiveOperation() {
  performance.mark("expensive-start");
  
  // ... expensive work ...
  
  performance.mark("expensive-end");
  performance.measure(
    "expensive-operation",
    "expensive-start",
    "expensive-end"
  );
}
```

## Common Issues

### Issue 1: React.memo Not Working

**Symptoms**: Memoized component still re-renders
**Cause**: Props include objects/arrays/functions that change reference
**Solution**: Memoize prop values

```tsx
// ❌ New object every render
<MemoizedChild config={{ theme: "dark" }} />

// ✅ Stable reference
const config = useMemo(() => ({ theme: "dark" }), []);
<MemoizedChild config={config} />

// ✅ Or use individual props
<MemoizedChild theme="dark" />
```

### Issue 2: Over-Optimization

**Symptoms**: Code is complex but not faster
**Cause**: Memoization overhead exceeds benefit
**Solution**: Remove unnecessary optimization

```tsx
// ❌ Overkill - simple operations are fast
const result = useMemo(() => a + b, [a, b]);

// ✅ Just calculate it
const result = a + b;
```

### Issue 3: Stale Closures

**Symptoms**: useCallback uses old values
**Cause**: Missing dependencies
**Solution**: Add all dependencies

```tsx
// ❌ Uses stale 'count'
const handleClick = useCallback(() => {
  console.log(count);
}, []);

// ✅ Always current
const handleClick = useCallback(() => {
  console.log(count);
}, [count]);
```

## Best Practices

- [ ] Profile before optimizing (use React DevTools)
- [ ] Start with proper state colocation
- [ ] Use React.memo for expensive components with stable props
- [ ] Use useMemo for expensive calculations, not simple ones
- [ ] Use useCallback for functions passed to memoized children
- [ ] Split large components into smaller ones
- [ ] Use code splitting for large, conditionally rendered components
- [ ] Virtualize long lists (100+ items)
- [ ] Split contexts to reduce re-render scope
- [ ] Measure impact - ensure optimization actually helps

## Anti-Patterns

Things to avoid:

- ❌ Memoizing everything by default
- ❌ Premature optimization without measuring
- ❌ Using useMemo for simple calculations
- ❌ Forgetting dependencies in hooks
- ❌ Creating new objects/arrays in render
- ❌ Deeply nested component trees
- ❌ Massive components with too many responsibilities
- ❌ Global state for local concerns

## Performance Checklist

When debugging slow components:

1. **Identify** - Use Profiler to find slow components
2. **Measure** - Record baseline performance
3. **Analyze** - Check why component renders
4. **Optimize** - Apply appropriate technique
5. **Verify** - Measure improvement
6. **Document** - Note why optimization was needed

## References

- [React Optimization Documentation](https://react.dev/learn/render-and-commit)
- [React.memo API](https://react.dev/reference/react/memo)
- [useMemo Hook](https://react.dev/reference/react/useMemo)
- [useCallback Hook](https://react.dev/reference/react/useCallback)
- [Code Splitting Guide](https://react.dev/reference/react/lazy)
- [React DevTools Profiler](https://react.dev/learn/react-developer-tools)
- [render-performance skill](../render-performance/)
- [bundle-optimizer skill](../bundle-optimizer/)

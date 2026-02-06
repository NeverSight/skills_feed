---
name: debug:react
description: Debug React issues systematically. Use when encountering component errors like "Cannot read property of undefined", infinite re-render loops with "Too many re-renders", stale closures in hooks, key prop warnings, memory leaks with useEffect, hydration mismatches in SSR/SSG applications, hook rule violations, missing dependency warnings, or performance bottlenecks. Covers functional components, hooks, and modern React 18/19 patterns including Server Components and concurrent features.
---

# React Debugging Guide

A systematic approach to debugging React applications, covering common error patterns, modern debugging tools, and step-by-step resolution strategies.

## Common Error Patterns

### 1. "Cannot read property of undefined" / "TypeError: X is undefined"

**Cause:** Accessing properties on null/undefined values, often from:
- Uninitialized state
- API data not yet loaded
- Incorrect prop drilling

**Solutions:**
```jsx
// Problem: Accessing nested property before data loads
const name = user.profile.name; // Error if user is undefined

// Solution 1: Optional chaining
const name = user?.profile?.name;

// Solution 2: Default values
const name = user?.profile?.name ?? 'Unknown';

// Solution 3: Early return pattern
if (!user) return <LoadingSpinner />;
return <div>{user.profile.name}</div>;

// Solution 4: Initialize state properly
const [user, setUser] = useState({ profile: { name: '' } });
```

### 2. Infinite Re-render Loops ("Too many re-renders")

**Cause:** State updates triggering renders that trigger more state updates.

**Common Triggers:**
- Calling setState directly in render
- useEffect with missing/incorrect dependencies
- Object/array references changing every render

**Solutions:**
```jsx
// Problem: setState in render
function BadComponent() {
  const [count, setCount] = useState(0);
  setCount(count + 1); // Infinite loop!
  return <div>{count}</div>;
}

// Solution: Move to useEffect or event handler
function GoodComponent() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    setCount(c => c + 1);
  }, []); // Run once on mount
  return <div>{count}</div>;
}

// Problem: Object dependency causing infinite loop
useEffect(() => {
  fetchData(options);
}, [options]); // New object reference every render!

// Solution: useMemo for stable reference
const memoizedOptions = useMemo(() => ({ page: 1 }), []);
useEffect(() => {
  fetchData(memoizedOptions);
}, [memoizedOptions]);
```

### 3. Stale Closure in Hooks

**Cause:** Callbacks capture old values from previous renders.

**Solutions:**
```jsx
// Problem: Stale closure in interval
function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      console.log(count); // Always logs initial value!
      setCount(count + 1); // Only increments once
    }, 1000);
    return () => clearInterval(id);
  }, []); // Empty deps = stale closure
}

// Solution 1: Functional update
setCount(prevCount => prevCount + 1);

// Solution 2: useRef for mutable values
const countRef = useRef(count);
useEffect(() => {
  countRef.current = count;
}, [count]);

// Solution 3: Include dependency (if appropriate)
useEffect(() => {
  const id = setInterval(() => {
    setCount(count + 1);
  }, 1000);
  return () => clearInterval(id);
}, [count]); // Re-creates interval on each count change

// Solution 4: useEffectEvent (React 19.2+)
const onTick = useEffectEvent(() => {
  setCount(count + 1); // Always has fresh count
});
useEffect(() => {
  const id = setInterval(onTick, 1000);
  return () => clearInterval(id);
}, []);
```

### 4. Key Prop Warnings

**Cause:** Missing or non-unique keys in lists.

**Solutions:**
```jsx
// Problem: No key
{items.map(item => <Item data={item} />)}

// Problem: Index as key (causes issues with reordering)
{items.map((item, index) => <Item key={index} data={item} />)}

// Solution: Stable unique identifier
{items.map(item => <Item key={item.id} data={item} />)}

// For items without IDs, generate stable keys
{items.map(item => <Item key={`${item.name}-${item.date}`} data={item} />)}
```

### 5. Memory Leaks with useEffect

**Cause:** Subscriptions, timers, or async operations not cleaned up.

**Solutions:**
```jsx
// Problem: No cleanup
useEffect(() => {
  const subscription = dataSource.subscribe(handleChange);
  // Memory leak when component unmounts!
}, []);

// Solution: Return cleanup function
useEffect(() => {
  const subscription = dataSource.subscribe(handleChange);
  return () => subscription.unsubscribe();
}, []);

// Problem: Async operation after unmount
useEffect(() => {
  fetchData().then(data => {
    setData(data); // Error if unmounted!
  });
}, []);

// Solution: AbortController for fetch
useEffect(() => {
  const controller = new AbortController();

  fetchData({ signal: controller.signal })
    .then(data => setData(data))
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });

  return () => controller.abort();
}, []);

// Solution: Ignore flag for other async
useEffect(() => {
  let ignore = false;

  fetchData().then(data => {
    if (!ignore) setData(data);
  });

  return () => { ignore = true; };
}, []);
```

### 6. Hydration Mismatches (SSR/SSG)

**Cause:** Server-rendered HTML differs from client-side React.

**Common Triggers:**
- Using `Date.now()`, `Math.random()` in render
- Browser-only APIs (window, localStorage)
- Conditional rendering based on client state

**Solutions:**
```jsx
// Problem: Random value differs server vs client
function BadComponent() {
  return <div>{Math.random()}</div>; // Hydration mismatch!
}

// Solution 1: useEffect for client-only values
function GoodComponent() {
  const [randomValue, setRandomValue] = useState(null);

  useEffect(() => {
    setRandomValue(Math.random());
  }, []);

  return <div>{randomValue}</div>;
}

// Solution 2: suppressHydrationWarning (use sparingly)
<time suppressHydrationWarning>{new Date().toISOString()}</time>

// Solution 3: Client-only component
const ClientOnlyComponent = dynamic(
  () => import('./ClientComponent'),
  { ssr: false }
);
```

### 7. Hook Rules Violations

**Error:** "React Hook useXXX is called conditionally"

**Cause:** Hooks called inside conditions, loops, or after early returns.

**Solutions:**
```jsx
// Problem: Conditional hook
function BadComponent({ shouldFetch }) {
  if (shouldFetch) {
    useEffect(() => fetchData(), []); // Error!
  }
}

// Solution: Condition inside hook
function GoodComponent({ shouldFetch }) {
  useEffect(() => {
    if (shouldFetch) fetchData();
  }, [shouldFetch]);
}

// Problem: Hook after early return
function BadComponent({ data }) {
  if (!data) return null;
  const [state, setState] = useState(data); // Error!
}

// Solution: Move hooks before returns
function GoodComponent({ data }) {
  const [state, setState] = useState(data);
  if (!data) return null;
  return <div>{state}</div>;
}
```

### 8. Missing Dependencies Warning

**Error:** "React Hook has a missing dependency: 'XXX'"

**Solutions:**
```jsx
// Problem: Missing dependency
const [count, setCount] = useState(0);
useEffect(() => {
  document.title = `Count: ${count}`;
}, []); // Warning: missing 'count'

// Solution 1: Add the dependency
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);

// Solution 2: Remove if truly not needed (rare)
// eslint-disable-next-line react-hooks/exhaustive-deps

// Solution 3: useCallback for function dependencies
const handleClick = useCallback(() => {
  console.log(count);
}, [count]);

useEffect(() => {
  element.addEventListener('click', handleClick);
  return () => element.removeEventListener('click', handleClick);
}, [handleClick]);
```

## Debugging Tools

### React Developer Tools

The official browser extension for debugging React applications.

**Installation:**
- Chrome: [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools)
- Firefox: [React Developer Tools](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/)

**Key Features:**
```
Components Tab:
- Inspect component tree hierarchy
- View and edit props in real-time
- View and modify state
- Search components by name
- View component source location

Profiler Tab:
- Record render performance
- Identify slow components
- View render timing flamegraph
- Detect unnecessary re-renders
```

**Pro Tips:**
```jsx
// Name components for easier debugging
const MyComponent = () => <div />;
MyComponent.displayName = 'MyComponent';

// Or use named exports
export function MyComponent() { ... }
```

### Console.log Debugging

Strategic logging patterns for React:

```jsx
// Log props and state changes
function DebugComponent({ data }) {
  console.log('[DebugComponent] render', { data });

  useEffect(() => {
    console.log('[DebugComponent] effect triggered', { data });
    return () => console.log('[DebugComponent] cleanup');
  }, [data]);

  return <div>{data}</div>;
}

// Log render counts
function RenderCounter({ name }) {
  const renderCount = useRef(0);
  renderCount.current++;
  console.log(`[${name}] render #${renderCount.current}`);
  return null;
}

// Conditional logging
const DEBUG = process.env.NODE_ENV === 'development';
DEBUG && console.log('Debug info:', data);
```

### Error Boundaries

Catch and handle errors in component trees:

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo);
    // Log to error monitoring service
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.toString()}</pre>
          </details>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <RiskyComponent />
</ErrorBoundary>
```

### React Strict Mode

Helps identify potential problems:

```jsx
// In index.js or App.js
<React.StrictMode>
  <App />
</React.StrictMode>
```

**What it detects:**
- Unsafe lifecycle methods
- Legacy string refs
- Unexpected side effects (double-invokes effects in dev)
- Deprecated APIs

### why-did-you-render

Track unnecessary re-renders:

```bash
npm install @welldone-software/why-did-you-render
```

```jsx
// wdyr.js - import before React
import React from 'react';

if (process.env.NODE_ENV === 'development') {
  const whyDidYouRender = require('@welldone-software/why-did-you-render');
  whyDidYouRender(React, {
    trackAllPureComponents: true,
  });
}

// Component to track
function MyComponent() { ... }
MyComponent.whyDidYouRender = true;
```

### Redux DevTools

For Redux state management debugging:

```jsx
import { configureStore } from '@reduxjs/toolkit';

const store = configureStore({
  reducer: rootReducer,
  devTools: process.env.NODE_ENV !== 'production',
});
```

## The Four Phases of React Debugging

### Phase 1: Reproduce

**Goal:** Consistently reproduce the issue.

```markdown
Checklist:
[ ] Can you reproduce in development mode?
[ ] Can you reproduce in production build?
[ ] What are the exact steps?
[ ] Does it happen on initial load or after interaction?
[ ] Is it intermittent or consistent?
[ ] Which browsers/devices affected?
```

**Minimal Reproduction:**
```jsx
// Create minimal component that shows the bug
function BugReproduction() {
  // Minimal state/props needed
  const [data, setData] = useState(null);

  // Minimal effect/logic
  useEffect(() => {
    fetchData().then(setData);
  }, []);

  // Minimal render
  return <div>{data?.value}</div>;
}
```

### Phase 2: Isolate

**Goal:** Narrow down the source of the problem.

```markdown
Techniques:
1. Binary search: Comment out half the code
2. Component isolation: Test component in isolation
3. Prop drilling check: Verify props at each level
4. State inspection: Log state changes
5. Effect tracking: Log effect execution
```

```jsx
// Isolation wrapper for debugging
function DebugWrapper({ children }) {
  console.log('[DebugWrapper] children:', children);
  return (
    <ErrorBoundary>
      {children}
    </ErrorBoundary>
  );
}

// Test component in isolation
<DebugWrapper>
  <SuspectedComponent testProp="hardcoded" />
</DebugWrapper>
```

### Phase 3: Diagnose

**Goal:** Understand why the bug occurs.

```markdown
Questions to answer:
- Is it a render issue or state issue?
- Is it a timing issue (async, race condition)?
- Is it a reference equality issue?
- Is it a missing dependency?
- Is it a stale closure?
- Is it a side effect issue?
```

```jsx
// Diagnostic hooks
function useDiagnostic(name, value) {
  const prevValue = useRef(value);
  const renderCount = useRef(0);

  useEffect(() => {
    renderCount.current++;
    console.log(`[${name}] Render #${renderCount.current}`);
    console.log(`  Previous:`, prevValue.current);
    console.log(`  Current:`, value);
    console.log(`  Changed:`, prevValue.current !== value);
    prevValue.current = value;
  });
}

// Usage
function MyComponent({ data }) {
  useDiagnostic('MyComponent.data', data);
  // ...
}
```

### Phase 4: Fix and Verify

**Goal:** Implement fix and prevent regression.

```markdown
Verification steps:
1. Does the fix resolve the original issue?
2. Does it introduce new issues?
3. Does it work across all affected scenarios?
4. Are there edge cases?
5. Is there a test to prevent regression?
```

```jsx
// Write a test for the bug
describe('BugFix', () => {
  it('should not crash when data is null', () => {
    render(<MyComponent data={null} />);
    expect(screen.queryByText('Error')).not.toBeInTheDocument();
  });

  it('should handle rapid state updates', async () => {
    const { rerender } = render(<MyComponent count={0} />);
    for (let i = 1; i <= 100; i++) {
      rerender(<MyComponent count={i} />);
    }
    expect(screen.getByText('100')).toBeInTheDocument();
  });
});
```

## Quick Reference Commands

### React Testing Library Debug

```jsx
import { screen } from '@testing-library/react';

// Print current DOM
screen.debug();

// Debug specific element
screen.debug(screen.getByRole('button'));

// Increase output limit
screen.debug(undefined, 30000);

// Log accessible roles
screen.logTestingPlaygroundURL();
```

### Performance Profiling

```jsx
// React Profiler component
import { Profiler } from 'react';

function onRenderCallback(
  id,           // Component name
  phase,        // "mount" | "update"
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) {
  console.log(`[Profiler ${id}]`, { phase, actualDuration });
}

<Profiler id="Navigation" onRender={onRenderCallback}>
  <Navigation />
</Profiler>
```

### Quick Fixes Checklist

```markdown
Component not updating?
[ ] Check if state is mutated vs replaced
[ ] Verify useEffect dependencies
[ ] Check for stale closures
[ ] Verify key props on lists

Infinite loop?
[ ] Check for setState in render
[ ] Check useEffect dependencies
[ ] Look for object/array reference changes

Memory leak warning?
[ ] Add cleanup to useEffect
[ ] Cancel async operations
[ ] Unsubscribe from events

Hydration error?
[ ] Check for browser-only code
[ ] Verify consistent server/client output
[ ] Use useEffect for client-only values
```

### Useful Browser Console Commands

```javascript
// Find React fiber
$r // Selected component in React DevTools

// Access React internals (dev only)
__REACT_DEVTOOLS_GLOBAL_HOOK__

// Get component state
$r.memoizedState

// Get component props
$r.memoizedProps

// Force update selected component
$r.forceUpdate?.()
```

## Security Considerations (2025)

**React Server Components Vulnerability (CVE-2025-XXXXX):**
- Affects React 19.0.0 through 19.2.2
- Malicious HTTP requests can cause infinite loops
- Upgrade to 19.0.3, 19.1.4, or 19.2.3+

```bash
# Check your React version
npm list react

# Upgrade if affected
npm install react@latest react-dom@latest
```

## Additional Resources

- [React Developer Tools](https://react.dev/learn/react-developer-tools)
- [Common Beginner Mistakes - Josh Comeau](https://www.joshwcomeau.com/react/common-beginner-mistakes/)
- [React Error Handling Best Practices](https://uxcam.com/blog/react-error-handling-best-practices/)
- [LogRocket: Common React Errors](https://blog.logrocket.com/8-common-react-error-messages-how-address-them/)
- [Zipy: React Debugging Tools](https://www.zipy.ai/blog/react-debugging-tools)

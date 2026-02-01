---
name: react-use-callback
description: Guides proper usage of the useCallback hook in React. Use this skill when optimizing function references, passing callbacks to memoized components, or preventing unnecessary re-renders.
---

# React: useCallback Best Practices

## Core Principle

**useCallback caches a function definition between re-renders until its dependencies change.**

Only use `useCallback` for specific performance optimizations - not by default.

## When to Use useCallback

### 1. Passing Callbacks to Memoized Children

When passing a function to a component wrapped in `memo()`:

```jsx
import { useCallback, memo } from 'react';

const ExpensiveChild = memo(function ExpensiveChild({ onClick }) {
  // Expensive rendering logic
  return <button onClick={onClick}>Click me</button>;
});

function Parent({ productId }) {
  // Without useCallback, handleClick would be a new function every render
  // causing ExpensiveChild to re-render unnecessarily
  const handleClick = useCallback(() => {
    console.log('Clicked:', productId);
  }, [productId]);

  return <ExpensiveChild onClick={handleClick} />;
}
```

### 2. Function as Effect Dependency

When a function is used inside `useEffect`:

```jsx
function ChatRoom({ roomId }) {
  const createOptions = useCallback(() => {
    return { serverUrl: 'https://localhost:1234', roomId };
  }, [roomId]);

  useEffect(() => {
    const options = createOptions();
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [createOptions]);
}
```

**Better alternative:** Move the function inside the effect:

```jsx
function ChatRoom({ roomId }) {
  useEffect(() => {
    // Function defined inside effect - no useCallback needed
    function createOptions() {
      return { serverUrl: 'https://localhost:1234', roomId };
    }
    
    const options = createOptions();
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);
}
```

### 3. Custom Hook Return Values

Always wrap functions returned from custom hooks:

```jsx
function useRouter() {
  const { dispatch } = useContext(RouterStateContext);

  const navigate = useCallback((url) => {
    dispatch({ type: 'navigate', url });
  }, [dispatch]);

  const goBack = useCallback(() => {
    dispatch({ type: 'back' });
  }, [dispatch]);

  return { navigate, goBack };
}
```

### 4. Reducing State Dependencies

Use updater functions to eliminate state dependencies:

```jsx
// Before: todos is a dependency
const handleAddTodo = useCallback((text) => {
  setTodos([...todos, { id: nextId++, text }]);
}, [todos]);

// After: No todos dependency needed
const handleAddTodo = useCallback((text) => {
  setTodos(todos => [...todos, { id: nextId++, text }]);
}, []);
```

## When NOT to Use useCallback

### 1. Child Is Not Memoized

Without `memo()`, `useCallback` provides no benefit:

```jsx
// useCallback is pointless here
function Parent() {
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);

  // Child will re-render anyway when Parent re-renders
  return <Child onClick={handleClick} />;
}
```

### 2. Coarse Interactions

Apps with page-level navigation don't benefit from memoization:

```jsx
// Overkill for simple navigation
function App() {
  const [page, setPage] = useState('home');
  
  // Not needed - page transitions are inherently expensive anyway
  const navigate = useCallback((page) => setPage(page), []);
  
  return <Navigation onNavigate={navigate} />;
}
```

### 3. When Better Alternatives Exist

**Accept JSX as children:**

```jsx
// Instead of memoizing onClick
function Panel({ children }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}
    </div>
  );
}

// Children don't re-render when Panel's state changes
<Panel>
  <ExpensiveComponent />
</Panel>
```

**Keep state local:**

```jsx
// Don't lift state higher than necessary
function SearchForm() {
  // Local state doesn't trigger parent re-renders
  const [query, setQuery] = useState('');
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

## Anti-Patterns to Avoid

### Missing Dependency Array

```jsx
// Returns a new function every render
const handleClick = useCallback(() => {
  doSomething();
}); // Missing dependency array!

// Correct
const handleClick = useCallback(() => {
  doSomething();
}, []);
```

### useCallback in Loops

```jsx
// Can't call hooks in loops
function List({ items }) {
  return items.map(item => {
    // WRONG
    const handleClick = useCallback(() => sendReport(item), [item]);
    return <Chart key={item.id} onClick={handleClick} />;
  });
}

// Correct: Extract to component
function List({ items }) {
  return items.map(item => (
    <Report key={item.id} item={item} />
  ));
}

function Report({ item }) {
  const handleClick = useCallback(() => sendReport(item), [item]);
  return <Chart onClick={handleClick} />;
}

// Alternative: Wrap Report in memo instead
const Report = memo(function Report({ item }) {
  function handleClick() {
    sendReport(item);
  }
  return <Chart onClick={handleClick} />;
});
```

## useCallback vs useMemo

| Hook | Caches | Use Case |
|------|--------|----------|
| `useCallback(fn, deps)` | The function itself | Callback props |
| `useMemo(() => fn, deps)` | Result of calling function | Computed values |

```jsx
// Equivalent
const memoizedFn = useCallback(fn, deps);
const memoizedFn = useMemo(() => fn, deps);
```

## Quick Reference

### DO

- Use with `memo()` wrapped children
- Use when function is an effect dependency
- Wrap custom hook return functions
- Use updater functions to reduce dependencies

### DON'T

- Add everywhere "just in case"
- Use without `memo()` on child component
- Use when you can restructure code instead
- Forget the dependency array

## Performance Debugging

When memoization isn't working, debug dependencies:

```jsx
const handleSubmit = useCallback((orderDetails) => {
  // ...
}, [productId, referrer]);

console.log([productId, referrer]);
```

Check in browser console:
```js
Object.is(temp1[0], temp2[0]); // First dependency same?
Object.is(temp1[1], temp2[1]); // Second dependency same?
```

## Future: React Compiler

React Compiler automatically memoizes values and functions, reducing the need for manual `useCallback` calls. Consider using the compiler to handle memoization automatically.

## References

- [React Docs - useCallback](https://react.dev/reference/react/useCallback)
- [React Docs - memo](https://react.dev/reference/react/memo)
- [React Docs - useMemo](https://react.dev/reference/react/useMemo)

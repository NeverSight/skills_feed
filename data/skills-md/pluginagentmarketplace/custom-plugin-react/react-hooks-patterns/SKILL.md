---
name: react-hooks-patterns
description: Master React Hooks including useState, useEffect, useContext, useReducer, and custom hooks with production-grade patterns
sasmp_version: "2.0.0"
bonded_agent: 02-hooks-patterns
bond_type: PRIMARY_BOND
input_validation:
  required_context:
    - react_version: ">=18.0.0"
    - node_version: ">=18.0.0"
  parameter_types:
    hook_name: string
    dependencies: array
output_format:
  code_examples: jsx
  test_template: jest
error_handling:
  patterns:
    - exponential_backoff
    - abort_controller
    - cleanup_functions
  retry_config:
    max_retries: 3
    backoff_multiplier: 2
observability:
  logging: structured
  metrics: ["render_count", "effect_duration"]
---

# React Hooks Patterns Skill

## Overview
Master React Hooks patterns including built-in hooks (useState, useEffect, useContext, useReducer, useCallback, useMemo) and custom hook development for reusable logic.

## Learning Objectives
- Understand all built-in React Hooks
- Create custom hooks for code reuse
- Implement advanced hook patterns
- Optimize performance with hooks
- Handle side effects effectively

## Core Hooks

### useState
```jsx
const [state, setState] = useState(initialValue);

// Lazy initialization for expensive computations
const [state, setState] = useState(() => expensiveComputation());

// Functional updates when state depends on previous value
setState(prev => prev + 1);
```

### useEffect
```jsx
useEffect(() => {
  // Side effect code
  const subscription = api.subscribe();

  // Cleanup function
  return () => {
    subscription.unsubscribe();
  };
}, [dependencies]); // Dependency array
```

### useContext
```jsx
const value = useContext(MyContext);

// Best practice: Create custom hook
function useMyContext() {
  const context = useContext(MyContext);
  if (!context) {
    throw new Error('useMyContext must be within Provider');
  }
  return context;
}
```

### useReducer
```jsx
const [state, dispatch] = useReducer(reducer, initialState);

function reducer(state, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'DECREMENT':
      return { count: state.count - 1 };
    default:
      return state;
  }
}
```

### useCallback
```jsx
const memoizedCallback = useCallback(
  () => {
    doSomething(a, b);
  },
  [a, b], // Dependencies
);
```

### useMemo
```jsx
const memoizedValue = useMemo(
  () => computeExpensiveValue(a, b),
  [a, b]
);
```

### useRef
```jsx
const ref = useRef(initialValue);

// DOM access
const inputRef = useRef(null);
<input ref={inputRef} />
inputRef.current.focus();

// Mutable value that doesn't trigger re-render
const countRef = useRef(0);
```

## Custom Hooks Library

### useFetch
```jsx
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    fetch(url)
      .then(res => res.json())
      .then(data => {
        if (!cancelled) {
          setData(data);
          setLoading(false);
        }
      })
      .catch(err => {
        if (!cancelled) {
          setError(err);
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [url]);

  return { data, loading, error };
}
```

### useLocalStorage
```jsx
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}
```

### useDebounce
```jsx
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}
```

### usePrevious
```jsx
function usePrevious(value) {
  const ref = useRef();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}
```

### useToggle
```jsx
function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => {
    setValue(v => !v);
  }, []);

  return [value, toggle];
}
```

### useOnClickOutside
```jsx
function useOnClickOutside(ref, handler) {
  useEffect(() => {
    const listener = (event) => {
      if (!ref.current || ref.current.contains(event.target)) {
        return;
      }
      handler(event);
    };

    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);

    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref, handler]);
}
```

## Practice Exercises

1. **Counter with useReducer**: Build a counter using useReducer instead of useState
2. **Theme Context**: Create a theme switcher using useContext
3. **Data Fetching**: Implement useFetch with caching
4. **Form Handler**: Create useForm custom hook for form state management
5. **Window Size Hook**: Build useWindowSize hook for responsive layouts
6. **Intersection Observer**: Create useInView hook for lazy loading
7. **Timer Hook**: Build useInterval and useTimeout hooks

## Common Patterns

### Fetching with Abort
```jsx
function useFetchWithAbort(url) {
  const [state, setState] = useState({ data: null, loading: true, error: null });

  useEffect(() => {
    const abortController = new AbortController();

    fetch(url, { signal: abortController.signal })
      .then(res => res.json())
      .then(data => setState({ data, loading: false, error: null }))
      .catch(err => {
        if (err.name !== 'AbortError') {
          setState({ data: null, loading: false, error: err });
        }
      });

    return () => abortController.abort();
  }, [url]);

  return state;
}
```

### Combining Multiple Hooks
```jsx
function useAuthenticatedApi(url) {
  const { token } = useAuth();
  const { data, loading, error } = useFetch(url, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  return { data, loading, error };
}
```

## Best Practices

1. **Name custom hooks with "use" prefix**
2. **Extract reusable logic into custom hooks**
3. **Keep hooks at component top level (no conditionals)**
4. **Use ESLint plugin for hooks rules**
5. **Document custom hook dependencies**
6. **Test custom hooks with @testing-library/react-hooks**

## Resources

- [React Hooks API Reference](https://react.dev/reference/react)
- [useHooks.com](https://usehooks.com) - Collection of custom hooks
- [React Hooks Cheatsheet](https://react-hooks-cheatsheet.com)

## Assessment

Can you:
- [ ] Explain when to use each built-in hook?
- [ ] Create custom hooks for reusable logic?
- [ ] Handle cleanup in useEffect properly?
- [ ] Optimize with useCallback and useMemo?
- [ ] Manage complex state with useReducer?
- [ ] Build a custom hook library for your project?

---

## Unit Test Template

```jsx
// __tests__/useCustomHook.test.js
import { renderHook, act, waitFor } from '@testing-library/react';
import { useCustomHook } from '../useCustomHook';

describe('useCustomHook', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with default state', () => {
    const { result } = renderHook(() => useCustomHook());
    expect(result.current.state).toBe(initialValue);
  });

  it('should handle async operations', async () => {
    const { result } = renderHook(() => useCustomHook());

    await act(async () => {
      await result.current.asyncAction();
    });

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });
  });

  it('should cleanup on unmount', () => {
    const cleanup = jest.fn();
    const { unmount } = renderHook(() => useCustomHook({ onCleanup: cleanup }));

    unmount();
    expect(cleanup).toHaveBeenCalled();
  });
});
```

## Retry Logic Pattern

```jsx
function useRetryAsync(asyncFn, options = {}) {
  const { maxRetries = 3, backoff = 1000 } = options;
  const [state, setState] = useState({ data: null, error: null, loading: false });

  const execute = useCallback(async (...args) => {
    setState(s => ({ ...s, loading: true, error: null }));
    let lastError;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const data = await asyncFn(...args);
        setState({ data, error: null, loading: false });
        return data;
      } catch (error) {
        lastError = error;
        if (attempt < maxRetries) {
          await new Promise(r => setTimeout(r, backoff * Math.pow(2, attempt)));
        }
      }
    }

    setState({ data: null, error: lastError, loading: false });
    throw lastError;
  }, [asyncFn, maxRetries, backoff]);

  return { ...state, execute };
}
```

---

**Version**: 2.0.0
**Last Updated**: 2025-12-30
**SASMP Version**: 2.0.0
**Difficulty**: Intermediate
**Estimated Time**: 2-3 weeks
**Prerequisites**: React Fundamentals
**Changelog**: Added retry patterns, test templates, and observability hooks

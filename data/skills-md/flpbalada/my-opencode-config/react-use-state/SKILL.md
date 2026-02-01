---
name: react-use-state
description: Guides proper usage of React useState hook. Use this skill when adding state to components, deciding between useState vs alternatives, or troubleshooting state update issues.
---

# React: useState Hook Best Practices

## Core Concept

`useState` is a React Hook that adds a state variable to your component, triggering re-renders when the state changes.

```jsx
const [state, setState] = useState(initialState);
```

## When to Use useState

### Ideal Use Cases

| Use Case | Example |
|----------|---------|
| **Form inputs** | `const [name, setName] = useState('')` |
| **UI state** | `const [isOpen, setIsOpen] = useState(false)` |
| **Simple counters** | `const [count, setCount] = useState(0)` |
| **Local component data** | `const [items, setItems] = useState([])` |

### Use useState When

- State is **local** to the component
- State transitions are **simple** (direct value replacement)
- Changes should **trigger re-renders**
- You need to **persist values** between renders

## When NOT to Use useState

### Use useRef Instead

When you need mutable values that **don't trigger re-renders**:

```jsx
// Interval IDs, DOM references, previous values
const intervalRef = useRef(null);
const inputRef = useRef(null);
```

### Use useReducer Instead

When state logic is **complex**:

```jsx
// Multiple related values, complex transitions
const [state, dispatch] = useReducer(reducer, initialState);
```

Use `useReducer` when:
- State has multiple sub-values
- Next state depends on previous state in complex ways
- You want to centralize state logic

### Avoid Redundant State

If a value can be **computed from props or other state**, don't store it:

```jsx
// BAD: Redundant state
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// GOOD: Compute during render
const fullName = `${firstName} ${lastName}`;

// If expensive, use useMemo
const sortedItems = useMemo(() => 
  items.sort((a, b) => a.name.localeCompare(b.name)), 
  [items]
);
```

### Don't Use for Global/Shared State

For state shared across multiple components:
- **React Context** for moderate sharing
- **External stores** (Zustand, Jotai) for complex apps
- **Server state libraries** (TanStack Query) for async data

## Critical Rules

### 1. Never Mutate State Directly

```jsx
// BAD: Mutation
obj.x = 10;
setObj(obj); // React ignores this!

// GOOD: Create new object
setObj({ ...obj, x: 10 });

// BAD: Array mutation
arr.push(item);
setArr(arr); // React ignores this!

// GOOD: Create new array
setArr([...arr, item]);
```

### 2. State Updates Are Asynchronous

```jsx
function handleClick() {
  setCount(count + 1);
  console.log(count); // Still old value!
  
  // If you need the new value:
  const nextCount = count + 1;
  setCount(nextCount);
  console.log(nextCount); // New value
}
```

### 3. Use Updater Function for Sequential Updates

```jsx
// BAD: Only increments by 1
function handleClick() {
  setCount(count + 1); // 0 + 1 = 1
  setCount(count + 1); // 0 + 1 = 1 (same stale value!)
  setCount(count + 1); // 0 + 1 = 1
}

// GOOD: Increments by 3
function handleClick() {
  setCount(c => c + 1); // 0 -> 1
  setCount(c => c + 1); // 1 -> 2
  setCount(c => c + 1); // 2 -> 3
}
```

### 4. Use Initializer Function for Expensive Initial Values

```jsx
// BAD: createTodos() runs every render
const [todos, setTodos] = useState(createTodos());

// GOOD: createTodos runs only once
const [todos, setTodos] = useState(createTodos);

// Or with arrow function for arguments
const [todos, setTodos] = useState(() => createTodos(userId));
```

### 5. Call Hooks at Top Level Only

```jsx
// BAD: Conditional hook
if (condition) {
  const [state, setState] = useState(0); // Error!
}

// GOOD: Always call, conditionally use
const [state, setState] = useState(0);
if (condition) {
  // use state here
}
```

## Common Patterns

### Resetting State with Key

```jsx
// Parent controls reset via key
<Form key={version} />

// When version changes, Form remounts with fresh state
```

### Storing Functions in State

```jsx
// BAD: Function gets called
const [fn, setFn] = useState(someFunction);

// GOOD: Wrap in arrow function
const [fn, setFn] = useState(() => someFunction);
setFn(() => newFunction);
```

### Updating Objects/Arrays

```jsx
// Object: spread and override
setForm({ ...form, email: newEmail });

// Nested object
setUser({
  ...user,
  address: { ...user.address, city: newCity }
});

// Array: filter, map, spread
setItems(items.filter(i => i.id !== id));        // Remove
setItems([...items, newItem]);                    // Add
setItems(items.map(i => i.id === id ? {...i, done: true} : i)); // Update
```

## Quick Reference

### DO

- Use for simple, local component state
- Create new objects/arrays when updating
- Use updater function when depending on previous state
- Use initializer function for expensive initial values

### DON'T

- Store computed/derived values
- Mutate existing state objects/arrays
- Read state immediately after setting (it's a snapshot)
- Call `setState` unconditionally during render

## Alternative Hooks Comparison

| Hook | Use When |
|------|----------|
| `useState` | Simple state, primitives, basic objects |
| `useReducer` | Complex state logic, multiple sub-values |
| `useRef` | Mutable values without re-renders |
| `useMemo` | Expensive computed values |
| `useContext` | State shared across component tree |

## References

- [React Docs - useState](https://react.dev/reference/react/useState)
- [React Docs - State as a Snapshot](https://react.dev/learn/state-as-a-snapshot)
- [React Docs - Choosing the State Structure](https://react.dev/learn/choosing-the-state-structure)

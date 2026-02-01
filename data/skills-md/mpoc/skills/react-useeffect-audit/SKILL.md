---
name: react-useeffect-audit
description: Identify and fix unnecessary useEffect usage in React code. Use when reviewing React code that uses Effects, when asked to optimize React components, when seeing patterns like "useEffect + setState", when users ask about Effect best practices, or when refactoring React code. Helps eliminate redundant renders and simplify component logic.
---

# React useEffect Audit

Effects are an escape hatch for synchronizing with **external systems** (DOM, network, third-party widgets). If no external system is involved, you likely don't need an Effect.

## Quick Decision Guide

| Scenario | Use Effect? | Alternative |
|----------|-------------|-------------|
| Transform data for rendering | No | Calculate during render |
| Handle user events | No | Event handler |
| Cache expensive calculations | No | `useMemo` |
| Reset state when props change | No | `key` prop |
| Adjust state based on props | No | Calculate during render |
| Chain of state updates | No | Single event handler |
| Notify parent of state change | No | Call parent in event handler |
| Initialize app (once) | No | Module-level code |
| Subscribe to external store | No | `useSyncExternalStore` |
| Fetch data on mount/change | Yes | With cleanup; prefer framework |

## Common Anti-Patterns

### 1. Derived State in Effect

```jsx
// ❌ Bad: Extra render, unnecessary state
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(firstName + ' ' + lastName);
}, [firstName, lastName]);

// ✅ Good: Calculate during render
const fullName = firstName + ' ' + lastName;
```

### 2. Event Logic in Effect

```jsx
// ❌ Bad: Runs on mount if condition true, not just on click
useEffect(() => {
  if (product.isInCart) {
    showNotification('Added to cart!');
  }
}, [product]);

// ✅ Good: In event handler
function handleBuyClick() {
  addToCart(product);
  showNotification('Added to cart!');
}
```

### 3. Expensive Calculations

```jsx
// ❌ Bad: Unnecessary state and Effect
const [filtered, setFiltered] = useState([]);
useEffect(() => {
  setFiltered(getFilteredTodos(todos, filter));
}, [todos, filter]);

// ✅ Good: useMemo for expensive calculations
const filtered = useMemo(
  () => getFilteredTodos(todos, filter),
  [todos, filter]
);
```

### 4. Resetting State on Prop Change

```jsx
// ❌ Bad: Effect to reset state
function ProfilePage({ userId }) {
  const [comment, setComment] = useState('');
  useEffect(() => {
    setComment('');
  }, [userId]);
}

// ✅ Good: Use key to create fresh instance
<Profile userId={userId} key={userId} />
```

### 5. Effect Chains

```jsx
// ❌ Bad: Multiple Effects triggering each other
useEffect(() => {
  if (card?.gold) setGoldCount(c => c + 1);
}, [card]);
useEffect(() => {
  if (goldCount > 3) { setRound(r => r + 1); setGoldCount(0); }
}, [goldCount]);

// ✅ Good: Calculate in event handler
function handlePlaceCard(nextCard) {
  setCard(nextCard);
  if (nextCard.gold) {
    if (goldCount < 3) setGoldCount(goldCount + 1);
    else { setGoldCount(0); setRound(round + 1); }
  }
}
```

### 6. Notifying Parent

```jsx
// ❌ Bad: Effect to notify parent
useEffect(() => {
  onChange(isOn);
}, [isOn, onChange]);

// ✅ Good: Notify in same event
function handleClick() {
  setIsOn(!isOn);
  onChange(!isOn);
}

// ✅ Better: Controlled component (parent owns state)
function Toggle({ isOn, onChange }) {
  return <button onClick={() => onChange(!isOn)} />;
}
```

## When Effects ARE Appropriate

### Data Fetching (with cleanup)

```jsx
useEffect(() => {
  let ignore = false;
  fetchResults(query).then(json => {
    if (!ignore) setResults(json);  // Prevent race condition
  });
  return () => { ignore = true; };
}, [query]);
```

### External Store Subscription

```jsx
// ✅ Use dedicated hook
const isOnline = useSyncExternalStore(
  callback => {
    window.addEventListener('online', callback);
    window.addEventListener('offline', callback);
    return () => {
      window.removeEventListener('online', callback);
      window.removeEventListener('offline', callback);
    };
  },
  () => navigator.onLine,  // Client getter
  () => true               // Server getter
);
```

### App Initialization

```jsx
// ✅ Module-level, not in Effect
if (typeof window !== 'undefined') {
  checkAuthToken();
  loadDataFromLocalStorage();
}
```

## Key Principles

1. **Calculate during render** - Derived values don't need state or Effects
2. **Events belong in handlers** - User interactions go in event handlers, not Effects
3. **Single render pass** - Update multiple state variables in one event handler
4. **Use specialized hooks** - `useMemo`, `useSyncExternalStore` over Effects
5. **Always cleanup async** - Prevent race conditions with ignore flags
6. **Lift state when sharing** - Parent component owns shared state

For detailed examples and edge cases, see [references/patterns.md](references/patterns.md).

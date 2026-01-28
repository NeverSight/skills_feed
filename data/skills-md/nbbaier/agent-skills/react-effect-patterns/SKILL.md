---
name: react-effect-patterns
description: Guidelines for proper React useEffect usage and avoiding unnecessary Effects. Use when writing, reviewing, or refactoring React components that use useEffect, useState, or handle side effects. Triggers on tasks involving React Effects, derived state, event handlers, data fetching, or component synchronization.
---

# React Effect Patterns

Effects are an escape hatch from React for synchronizing with external systems. Removing unnecessary Effects makes code easier to follow, faster to run, and less error-prone.

## When to Use Effects

- Synchronizing with external systems (non-React widgets, network, browser DOM)
- Analytics on component display
- Data fetching (with cleanup for race conditions)

## When NOT to Use Effects

- Transforming data for rendering
- Handling user events
- Updating state based on other state

## Decision Tree

**Why does this code run?**

- Component displayed → Effect
- User action → Event handler
- Calculable from props/state → Calculate during render

---

## Anti-Patterns and Solutions

### 1. Derived State

```jsx
// ❌ Bad
const [fullName, setFullName] = useState("");
useEffect(() => {
   setFullName(firstName + " " + lastName);
}, [firstName, lastName]);

// ✅ Good - calculate during render
const fullName = firstName + " " + lastName;
```

### 2. Expensive Calculations

```jsx
// ❌ Bad
const [visibleTodos, setVisibleTodos] = useState([]);
useEffect(() => {
   setVisibleTodos(getFilteredTodos(todos, filter));
}, [todos, filter]);

// ✅ Good - useMemo for expensive operations
const visibleTodos = useMemo(
   () => getFilteredTodos(todos, filter),
   [todos, filter],
);
```

Use `console.time()`/`console.timeEnd()` to measure. Memoize if ≥1ms.

### 3. Reset State on Prop Change

```jsx
// ❌ Bad
useEffect(() => {
   setComment("");
}, [userId]);

// ✅ Good - use key to reset
<Profile userId={userId} key={userId} />;
```

### 4. Adjust Part of State on Prop Change

```jsx
// ❌ Bad
useEffect(() => {
   setSelection(null);
}, [items]);

// ✅ Good - derive from state
const selection = items.find((item) => item.id === selectedId) ?? null;
```

### 5. Event-Specific Logic

```jsx
// ❌ Bad
useEffect(() => {
   if (product.isInCart) {
      showNotification("Added " + product.name + "!");
   }
}, [product]);

// ✅ Good - in event handler
function handleBuyClick() {
   addToCart(product);
   showNotification("Added " + product.name + "!");
}
```

### 6. Form Submission

```jsx
// ❌ Bad
useEffect(() => {
   if (jsonToSubmit !== null) {
      post("/api/register", jsonToSubmit);
   }
}, [jsonToSubmit]);

// ✅ Good - in event handler
function handleSubmit(e) {
   e.preventDefault();
   post("/api/register", { firstName, lastName });
}
```

### 7. Effect Chains

```jsx
// ❌ Bad - cascading Effects
useEffect(() => {
   setGoldCardCount((c) => c + 1);
}, [card]);
useEffect(() => {
   setRound((r) => r + 1);
}, [goldCardCount]);
useEffect(() => {
   setIsGameOver(true);
}, [round]);

// ✅ Good - calculate + update in handler
const isGameOver = round > 5;

function handlePlaceCard(nextCard) {
   setCard(nextCard);
   if (nextCard.gold) {
      if (goldCardCount < 3) {
         setGoldCardCount(goldCardCount + 1);
      } else {
         setGoldCardCount(0);
         setRound(round + 1);
      }
   }
}
```

### 8. App Initialization

```jsx
// ❌ Bad - runs twice in dev
useEffect(() => {
   loadDataFromLocalStorage();
   checkAuthToken();
}, []);

// ✅ Good - module level or guard
let didInit = false;
function App() {
   useEffect(() => {
      if (!didInit) {
         didInit = true;
         loadDataFromLocalStorage();
         checkAuthToken();
      }
   }, []);
}
```

### 9. Notify Parent of State Changes

```jsx
// ❌ Bad - extra render pass
useEffect(() => {
   onChange(isOn);
}, [isOn, onChange]);

// ✅ Good - update both in handler
function updateToggle(nextIsOn) {
   setIsOn(nextIsOn);
   onChange(nextIsOn);
}

// ✅ Also good - lift state (controlled component)
function Toggle({ isOn, onChange }) {
   function handleClick() {
      onChange(!isOn);
   }
}
```

### 10. Pass Data to Parent

```jsx
// ❌ Bad - child fetches, passes up
useEffect(() => {
   if (data) onFetched(data);
}, [data]);

// ✅ Good - parent fetches, passes down
function Parent() {
   const data = useSomeAPI();
   return <Child data={data} />;
}
```

### 11. External Store Subscription

```jsx
// ❌ Bad - manual subscription
useEffect(() => {
   const handler = () => setIsOnline(navigator.onLine);
   window.addEventListener("online", handler);
   window.addEventListener("offline", handler);
   return () => {
      window.removeEventListener("online", handler);
      window.removeEventListener("offline", handler);
   };
}, []);

// ✅ Good - useSyncExternalStore
return useSyncExternalStore(
   subscribe,
   () => navigator.onLine,
   () => true,
);
```

### 12. Data Fetching with Race Conditions

```jsx
// ✅ Correct - cleanup ignores stale responses
useEffect(() => {
   let ignore = false;
   fetchResults(query).then((json) => {
      if (!ignore) setResults(json);
   });
   return () => {
      ignore = true;
   };
}, [query]);
```

---

## Quick Reference

| Scenario                | Solution                             |
| ----------------------- | ------------------------------------ |
| Transform data          | Calculate during render              |
| Expensive calculation   | `useMemo`                            |
| Reset all state on prop | `key` attribute                      |
| Adjust state on prop    | Derive during render                 |
| Share event logic       | Extract function, call from handlers |
| User events             | Event handlers                       |
| External system sync    | Effect                               |
| Notify parent           | Update in handler or lift state      |
| Init once               | Module-level or guard variable       |
| External store          | `useSyncExternalStore`               |
| Fetch data              | Effect with cleanup                  |

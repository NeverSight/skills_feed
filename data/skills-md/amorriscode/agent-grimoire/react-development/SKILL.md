---
name: react-development
description: React patterns, anti-patterns, and performance optimization. Use when writing React components, reviewing React code, or debugging React issues.
---

# React Development

Modern React patterns from the official docs and community expertise.

## Instructions

When working with React code, apply these principles in order of importance:

### 1. Think in React

Follow the 5-step process for building React UIs:

1. **Break UI into component hierarchy** — One component = one responsibility
2. **Build static version first** — Use props only, no state yet
3. **Find minimal state** — Ask: Does it change? Is it passed via props? Can it be computed?
4. **Identify where state lives** — Find closest common parent of components that need it
5. **Add inverse data flow** — Pass callbacks down to update parent state

### 2. Keep Components Pure

Components must be pure functions during rendering:

```jsx
// ❌ Mutates external variable
let guest = 0;
function Cup() {
  guest = guest + 1;
  return <h2>Guest #{guest}</h2>;
}

// ✅ Uses props
function Cup({ guest }) {
  return <h2>Guest #{guest}</h2>;
}
```

**Rules:**
- Never mutate props, state, or context during render
- Same inputs = same output
- Side effects belong in event handlers or useEffect

### 3. State Management

**Minimize state:**
```jsx
// ❌ Redundant state
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const [fullName, setFullName] = useState(''); // redundant!

// ✅ Compute during render
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const fullName = firstName + ' ' + lastName;
```

**Lift state up** when siblings need the same data — move to closest common parent.

**Use key to reset state:**
```jsx
// Forces fresh component instance when recipient changes
<Chat key={recipientId} contact={recipient} />
```

### 4. Hooks Rules

**Only call hooks at the top level:**
- Never in loops, conditions, or nested functions
- Never after early returns
- React relies on consistent call order

**Only call hooks from React functions:**
- Function components or custom hooks only

### 5. Effects — Use Sparingly

Effects are for synchronizing with external systems, not for state logic.

**You DON'T need useEffect for:**

| Scenario | Instead of Effect | Do This |
|----------|-------------------|---------|
| Transform data for render | `useEffect` + `setState` | Calculate during render |
| Cache expensive calculations | `useEffect` + `setState` | `useMemo` |
| Reset state on prop change | `useEffect` + `setState` | Use `key` prop |
| Handle user events | `useEffect` watching state | Event handler directly |
| Notify parent of changes | `useEffect` calling callback | Call in event handler |

**When you DO need useEffect:**
- Fetching data (with cleanup for race conditions)
- Subscribing to events (with cleanup to unsubscribe)
- Controlling non-React widgets
- Connecting to external systems

**Always add cleanup:**
```jsx
useEffect(() => {
  const connection = createConnection();
  connection.connect();
  return () => connection.disconnect(); // cleanup
}, []);
```

### 6. Performance

**Before reaching for memo:**
1. **Move state down** — Isolate state to components that use it
2. **Lift content up** — Pass expensive subtrees as `children`

**Virtualize large lists** (50+ items):
```jsx
import { FixedSizeList } from 'react-window';

<FixedSizeList height={400} itemCount={1000} itemSize={35}>
  {({ index, style }) => <div style={style}>{items[index]}</div>}
</FixedSizeList>
```

**Code split routes:**
```jsx
const Dashboard = lazy(() => import('./Dashboard'));

<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
```

### 7. Component Design Principles

From "Writing Resilient Components":

1. **Don't stop the data flow** — Read props directly, don't copy to state
2. **Always be ready to render** — Don't assume render timing or frequency
3. **No component is a singleton** — Design as if rendered multiple times
4. **Keep local state isolated** — Only local if it wouldn't sync across copies

### 8. Context — Use Judiciously

Good for: theming, current user, routing, widely-needed state.

**Try these first:**
1. Pass props explicitly — clearer data flow
2. Extract components and use `children` — avoids prop drilling

```jsx
// ❌ Prop drilling
<Layout posts={posts} />

// ✅ Composition
<Layout>
  <Posts posts={posts} />
</Layout>
```

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Copying props to state | Stale data | Read props directly |
| Effect chains | Cascading renders | Compute in event handlers |
| Suppressing effect with refs | Hides bugs | Add proper cleanup |
| Derived state in useState | Sync issues | Compute during render |
| Missing keys in lists | Broken updates | Use stable unique IDs |
| Index as key (for reorderable lists) | State mismatch | Use item IDs |

## Examples

### Well-Structured Component

```jsx
function ProductList({ products, onSelect }) {
  // Derived state — computed, not stored
  const sortedProducts = useMemo(
    () => [...products].sort((a, b) => a.name.localeCompare(b.name)),
    [products]
  );

  // Event handler — not useEffect
  function handleClick(product) {
    onSelect(product);
  }

  return (
    <ul>
      {sortedProducts.map(product => (
        <li key={product.id} onClick={() => handleClick(product)}>
          {product.name}
        </li>
      ))}
    </ul>
  );
}
```

### Data Fetching with Cleanup

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchUser() {
      const data = await getUser(userId);
      if (!cancelled) setUser(data);
    }

    fetchUser();
    return () => { cancelled = true; };
  }, [userId]);

  if (!user) return <Loading />;
  return <Profile user={user} />;
}
```

For detailed performance patterns, see [PERFORMANCE.md](PERFORMANCE.md).

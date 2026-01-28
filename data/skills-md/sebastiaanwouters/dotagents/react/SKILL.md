---
name: react
description: React v19 best practices for Vite SPA. Triggers on component design, re-renders, performance, memoization, state management, bundle optimization. Use for client-side React patterns.
---

# React v19 Best Practices (Vite SPA)

Performance optimization guide for React v19 applications, adapted from [Vercel's react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices).

> **Key Principle:** These rules are ordered by impact. Fix CRITICAL issues first.

## Rule Categories by Priority

| Priority | Category | Impact | Focus |
|----------|----------|--------|-------|
| 1 | Eliminating Waterfalls | CRITICAL | Parallel async operations |
| 2 | Bundle Size | CRITICAL | Dynamic imports, barrel files |
| 3 | Re-render Optimization | MEDIUM | memo, state, dependencies |
| 4 | Rendering Performance | MEDIUM | CSS, DOM, hydration |
| 5 | JavaScript Performance | LOW-MEDIUM | Data structures, loops |
| 6 | Advanced Patterns | LOW | Event handlers, refs |

## 1. ELIMINATING WATERFALLS — CRITICAL

### Parallel Async Operations

```typescript
// ❌ Sequential - 3 round trips
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()

// ✅ Parallel - 1 round trip
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

### Defer Await Until Needed

```typescript
// ❌ Blocks both branches
async function handleRequest(userId: string, skip: boolean) {
  const userData = await fetchUserData(userId)
  if (skip) return { skipped: true }
  return processUserData(userData)
}

// ✅ Only blocks when needed
async function handleRequest(userId: string, skip: boolean) {
  if (skip) return { skipped: true }
  const userData = await fetchUserData(userId)
  return processUserData(userData)
}
```

## 2. BUNDLE SIZE — CRITICAL

### Avoid Barrel File Imports

```typescript
// ❌ Loads entire library (~2.8s in dev)
import { Check, X, Menu } from 'lucide-react'

// ✅ Loads only what's needed
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'
```

**Affected libraries:** `lucide-react`, `@mui/material`, `react-icons`, `@radix-ui/*`, `lodash`, `date-fns`

### Dynamic Imports with React.lazy

```typescript
// ❌ Monaco bundles with main chunk (~300KB)
import { MonacoEditor } from './monaco-editor'

// ✅ Monaco loads on demand
import { lazy, Suspense } from 'react'

const MonacoEditor = lazy(() => import('./monaco-editor'))

function CodePanel({ code }: { code: string }) {
  return (
    <Suspense fallback={<Skeleton />}>
      <MonacoEditor value={code} />
    </Suspense>
  )
}
```

### Preload on User Intent

```typescript
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => void import('./monaco-editor')

  return (
    <button onMouseEnter={preload} onFocus={preload} onClick={onClick}>
      Open Editor
    </button>
  )
}
```

## 3. RE-RENDER OPTIMIZATION — MEDIUM

### Lazy State Initialization

```typescript
// ❌ Runs expensive computation every render
const [index, setIndex] = useState(buildSearchIndex(items))

// ✅ Runs only once
const [index, setIndex] = useState(() => buildSearchIndex(items))

// ✅ With localStorage
const [settings, setSettings] = useState(() => {
  try {
    const stored = localStorage.getItem('settings')
    return stored ? JSON.parse(stored) : {}
  } catch { return {} }
})
```

### Functional setState Updates

```typescript
// ❌ Stale closure bug, unstable callback
const addItem = useCallback((item: Item) => {
  setItems([...items, item])
}, [items])

// ✅ Always uses latest state, stable callback
const addItem = useCallback((item: Item) => {
  setItems(curr => [...curr, item])
}, [])
```

### Extract Memoized Components

```typescript
// ❌ Computes avatar even when loading
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => computeAvatar(user), [user])
  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}

// ✅ Skips computation when loading
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const avatar = useMemo(() => computeAvatar(user), [user])
  return <Avatar src={avatar} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return <div><UserAvatar user={user} /></div>
}
```

**Note:** React Compiler (React v19) auto-memoizes—manual memo becomes optional.

### Narrow Effect Dependencies

```typescript
// ❌ Re-runs on any user field change
useEffect(() => {
  console.log(user.id)
}, [user])

// ✅ Re-runs only when id changes
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

### Subscribe to Derived State

```typescript
// ❌ Re-renders on every pixel change
function Sidebar() {
  const width = useWindowWidth()
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}

// ✅ Re-renders only when boolean changes
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

### Use Transitions for Non-Urgent Updates

```typescript
import { startTransition, useTransition } from 'react'

// For scroll/resize handlers
const handler = () => {
  startTransition(() => setScrollY(window.scrollY))
}

// For async operations with pending state
function Search() {
  const [isPending, startTransition] = useTransition()

  const handleSearch = (value: string) => {
    startTransition(async () => {
      const data = await fetchResults(value)
      setResults(data)
    })
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
    </>
  )
}
```

## 4. RENDERING PERFORMANCE — MEDIUM

### Explicit Conditional Rendering

```typescript
// ❌ Renders "0" when count is 0
{count && <Badge>{count}</Badge>}

// ✅ Renders nothing when count is 0
{count > 0 ? <Badge>{count}</Badge> : null}
```

### content-visibility for Long Lists

```css
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

Browser skips layout/paint for off-screen items (10× faster for 1000 items).

### Hoist Static JSX

```typescript
// ❌ Recreates element every render
function Container() {
  return <div>{loading && <Skeleton className="h-20" />}</div>
}

// ✅ Reuses same element
const skeleton = <Skeleton className="h-20" />

function Container() {
  return <div>{loading && skeleton}</div>
}
```

**Note:** React Compiler auto-hoists static JSX.

### Animate Wrapper, Not SVG

```typescript
// ❌ No hardware acceleration
<svg className="animate-spin">...</svg>

// ✅ Hardware accelerated
<div className="animate-spin">
  <svg>...</svg>
</div>
```

## 5. JAVASCRIPT PERFORMANCE — LOW-MEDIUM

### Build Index Maps

```typescript
// ❌ O(n) per lookup
orders.map(order => ({
  ...order,
  user: users.find(u => u.id === order.userId)
}))

// ✅ O(1) per lookup
const userMap = new Map(users.map(u => [u.id, u]))
orders.map(order => ({
  ...order,
  user: userMap.get(order.userId)
}))
```

### Combine Loop Iterations

```typescript
// ❌ 3 iterations
const active = items.filter(i => i.active)
const names = active.map(i => i.name)
const sorted = names.sort()

// ✅ 1 iteration + sort
const names = items
  .reduce((acc, i) => {
    if (i.active) acc.push(i.name)
    return acc
  }, [] as string[])
  .sort()
```

### Use Set for O(1) Lookups

```typescript
// ❌ O(n) per check
const isSelected = (id: string) => selectedIds.includes(id)

// ✅ O(1) per check
const selectedSet = new Set(selectedIds)
const isSelected = (id: string) => selectedSet.has(id)
```

### Cache Property Access in Loops

```typescript
// ❌ Repeated property access
for (let i = 0; i < items.length; i++) {
  process(items[i], config.settings.theme.primary)
}

// ✅ Cached access
const color = config.settings.theme.primary
const len = items.length
for (let i = 0; i < len; i++) {
  process(items[i], color)
}
```

## 6. ADVANCED PATTERNS — LOW

### Stable Event Handlers with Refs

```typescript
// ❌ Callback changes on every render
function useInterval(callback: () => void, ms: number) {
  useEffect(() => {
    const id = setInterval(callback, ms)
    return () => clearInterval(id)
  }, [callback, ms])  // Restarts interval when callback changes
}

// ✅ Stable ref, interval never restarts
function useInterval(callback: () => void, ms: number) {
  const callbackRef = useRef(callback)
  callbackRef.current = callback

  useEffect(() => {
    const id = setInterval(() => callbackRef.current(), ms)
    return () => clearInterval(id)
  }, [ms])
}
```

### useLatest Pattern

```typescript
function useLatest<T>(value: T) {
  const ref = useRef(value)
  ref.current = value
  return ref
}

// Usage
function Chat({ onMessage }: { onMessage: (msg: string) => void }) {
  const onMessageRef = useLatest(onMessage)

  useEffect(() => {
    const ws = new WebSocket(url)
    ws.onmessage = (e) => onMessageRef.current(e.data)
    return () => ws.close()
  }, [])  // Never reconnects due to callback changes
}
```

## Quick Checklist

- [ ] No sequential awaits for independent operations
- [ ] No barrel file imports for large libraries
- [ ] Heavy components use React.lazy + Suspense
- [ ] useState with expensive init uses callback form
- [ ] setState that depends on current state uses functional form
- [ ] Effect dependencies are primitives, not objects
- [ ] Long lists use content-visibility
- [ ] Repeated lookups use Map/Set

## Deep Dive References

- [rerender.md](references/rerender.md) - Complete re-render optimization patterns
- [bundle.md](references/bundle.md) - Bundle size strategies
- [performance.md](references/performance.md) - JS and rendering performance

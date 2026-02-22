---
name: tanstack-pacer
description: |
  TanStack Pacer best practices for execution control in React — debouncing, throttling, rate limiting, queuing, and batching.
  Use when implementing search inputs, scroll handlers, API rate limits, task queues, bulk operations,
  or any scenario requiring controlled execution timing with reactive state.
metadata:
  tags: tanstack-pacer, debounce, throttle, rate-limit, queue, batch, react, typescript, execution-control
---

# TanStack Pacer

**Version**: @tanstack/react-pacer@latest
**Requires**: React 16.8+, TypeScript recommended

## Quick Setup

```bash
npm install @tanstack/react-pacer
```

```tsx
import { useDebouncedCallback } from '@tanstack/react-pacer'

function SearchInput() {
  const debouncedSearch = useDebouncedCallback(
    (query: string) => fetchResults(query),
    { wait: 300 },
  )

  return <input onChange={(e) => debouncedSearch(e.target.value)} />
}
```

### 4 Hook Variants Per Utility

Each utility (Debouncer, Throttler, RateLimiter, Queuer, Batcher) provides 4 React hooks:

| Hook | Returns | Use Case |
|------|---------|----------|
| `use[Utility]` | Instance | Full control, custom state subscriptions |
| `use[Utility]Callback` | Wrapped function | Simple event handler wrapping |
| `use[Utility]State` | `[value, setValue, instance]` | Debounced/throttled React state |
| `use[Utility]Value` | `[derivedValue, instance]` | Read-only derived value from props/state |

### PacerProvider (Optional)

```tsx
import { PacerProvider } from '@tanstack/react-pacer'

<PacerProvider
  defaultOptions={{
    debouncer: { wait: 300 },
    throttler: { wait: 200 },
  }}
>
  <App />
</PacerProvider>
```

### Devtools

```bash
npm install -D @tanstack/react-devtools @tanstack/react-pacer-devtools
```

```tsx
import { TanStackDevtools } from '@tanstack/react-devtools'
import { pacerDevtoolsPlugin } from '@tanstack/react-pacer-devtools'

<TanStackDevtools plugins={[pacerDevtoolsPlugin()]} />
```

Utilities must have a `key` option to appear in devtools.

## Rule Categories

| Priority | Category | Rule File | Impact |
|----------|----------|-----------|--------|
| CRITICAL | Hook Selection | `rules/hook-selection.md` | Correct hook choice per use case |
| CRITICAL | Debouncing | `rules/deb-debouncing.md` | Prevents wasted API calls and flickering UI |
| HIGH | Throttling | `rules/thr-throttling.md` | Smooth, evenly-spaced execution |
| HIGH | State & Reactivity | `rules/state-reactivity.md` | Prevents unnecessary re-renders |
| HIGH | Async Patterns | `rules/async-patterns.md` | Correct async execution with retry, abort, error handling |
| MEDIUM | Rate Limiting | `rules/rl-rate-limiting.md` | Enforces execution budgets |
| MEDIUM | Queuing | `rules/que-queuing.md` | Lossless ordered/priority task processing |
| MEDIUM | Batching | `rules/bat-batching.md` | Groups operations for bulk processing |
| LOW | Configuration | `rules/config-options.md` | Dynamic options, providers, shared config |
| LOW | Devtools | `rules/devtools.md` | Debugging and monitoring utilities |

## Critical Rules

### Always Do

- **Use hooks over function wrappers** — `useDebouncedCallback` not `debounce()` for proper React lifecycle
- **Choose the right hook variant** — `useCallback` for event handlers, `useState` for controlled inputs, `useValue` for derived values
- **Opt-in to state subscriptions** — pass selector as 3rd arg: `useDebouncer(fn, opts, (s) => ({ isPending: s.isPending }))`
- **Use async variants for API calls** — `useAsyncDebouncedCallback` gives error handling, retry, abort
- **Pass `AbortSignal` to fetch** — `getAbortSignal()` enables cancellation of in-flight requests
- **Use `key` option for devtools** — only keyed utilities appear in devtools panel

### Never Do

- **Subscribe to all state** — omit selector or use instance directly to avoid re-renders on every state change
- **Use debouncing when you need guaranteed execution** — use throttling or queuing instead
- **Use rate limiting for evenly-spaced calls** — rate limiting is bursty; use throttling for smooth spacing
- **Use `debounce()` function in React** — no lifecycle cleanup; use `useDebouncedCallback` hook instead
- **Expect `maxWait` on Debouncer** — Pacer has no `maxWait`; use Throttler for guaranteed periodic execution

## Key Patterns

```tsx
// Debounced search input with state
import { useDebouncedState } from '@tanstack/react-pacer'

function Search() {
  const [query, setQuery, debouncer] = useDebouncedState('', { wait: 300 })
  // query updates after 300ms pause; setQuery is immediate
  return <input onChange={(e) => setQuery(e.target.value)} />
}

// Async debounced API call with abort
import { useAsyncDebouncedCallback } from '@tanstack/react-pacer'

function AsyncSearch() {
  const search = useAsyncDebouncedCallback(
    async (query: string) => {
      const signal = search.getAbortSignal()
      const res = await fetch(`/api/search?q=${query}`, { signal })
      return res.json()
    },
    { wait: 300, onSuccess: (data) => setResults(data) },
  )
  return <input onChange={(e) => search(e.target.value)} />
}

// Throttled scroll handler
import { useThrottledCallback } from '@tanstack/react-pacer'

function ScrollTracker() {
  const onScroll = useThrottledCallback(
    () => trackScrollPosition(window.scrollY),
    { wait: 100 },
  )
  useEffect(() => {
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [onScroll])
}

// Derived debounced value from props
import { useDebouncedValue } from '@tanstack/react-pacer'

function FilteredList({ filter }: { filter: string }) {
  const [debouncedFilter] = useDebouncedValue(filter, { wait: 300 })
  return <ExpensiveList filter={debouncedFilter} />
}

// Async queue with concurrency
import { useAsyncQueuer } from '@tanstack/react-pacer'

function UploadQueue() {
  const queuer = useAsyncQueuer(uploadFile, { concurrency: 3 })
  return <button onClick={() => queuer.addItem(file)}>Upload</button>
}
```

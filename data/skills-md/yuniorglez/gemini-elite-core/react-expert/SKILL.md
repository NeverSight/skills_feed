---
name: react-expert
id: react-expert
version: 1.2.0
description: "Senior specialist in React 19.2+ performance, React Compiler (Forget), and advanced architectural patterns. Use when optimizing re-renders, bundle size, data fetching waterfalls (cacheSignal), or server-side efficiency (PPR)."
---

# ⚡ Skill: react-expert

## Description
This skill provides comprehensive performance optimization guidance for React applications, optimized for AI-assisted workflows in 2026. It focuses on eliminating waterfalls, leveraging the React Compiler, and maximizing both server and client-side efficiency through modern APIs (`use`, `useActionState`, `<Activity>`).

## Core Priorities
1. **Eliminating Waterfalls**: The #1 priority. Move fetches as high as possible, parallelize operations, and use `cacheSignal` to prevent wasted work.
2. **React Compiler Optimization**: Structuring code to be "Forget-friendly" (automatic memoization) while knowing when manual intervention is still needed.
3. **Partial Pre-rendering (PPR)**: Combining the best of static and dynamic rendering for sub-100ms LCP.
4. **Hydration Strategy**: Avoiding "hydration mismatch" and using `<Activity>` for state preservation.

## 🏆 Top 5 Performance Gains in 2026

1.  **React Compiler (Automatic Memoization)**: Removes the "useMemo tax". Code that adheres to "Rules of React" is automatically optimized.
2.  **Partial Pre-rendering (PPR)**: Serves static shells instantly while streaming dynamic content in the same request.
3.  **The `use()` API**: Eliminates the `useEffect` + `useState` boilerplate for data fetching, reducing client-side code by up to 30%.
4.  **`cacheSignal`**: Allows the server to abort expensive async work if the client disconnects or navigates away.
5.  **Server Actions + `useActionState`**: Native handling of pending states and optimistic updates, reducing reliance on third-party form/state libraries.

## Table of Contents & Detailed Guides

### 1. [Eliminating Waterfalls](./references/1-waterfalls.md) — **CRITICAL**
- Defer Await Until Needed
- `cacheSignal` for Lifecycle Management
- Dependency-Based Parallelization (`better-all`)
- `Promise.all()` for Independent Operations
- Strategic Suspense Boundaries

### 2. [Bundle Size Optimization](./references/2-bundle-optimization.md) — **CRITICAL**
- Avoiding Barrel File Imports (Lucide, MUI, etc.)
- Conditional Module Loading (Dynamic `import()`)
- Deferring Non-Critical Libraries (Analytics)
- Preloading based on User Intent

### 3. [Server-Side Performance](./references/3-server-side.md) — **HIGH**
- **Partial Pre-rendering (PPR)** Deep Dive
- Cross-Request LRU Caching
- Minimizing Serialization at RSC Boundaries
- Parallel Data Fetching with Component Composition

### 4. [Client-Side & Data Fetching](./references/4-hooks-and-actions.md) — **MEDIUM-HIGH**
- **`use()` API** for Promises and Context
- **`useActionState`** for Form Management
- **`useOptimistic`** for Instant UI Feedback
- Deduplicating Global Event Listeners

### 5. [React Compiler & Re-renders](./references/5-compiler-and-rerender.md) — **MEDIUM**
- **Compiler Rules**: Side-effect-free rendering
- Deferring State Reads
- Narrowing Effect Dependencies
- Transitions for Non-Urgent Updates (`startTransition`)

### 6. [Rendering Performance](./references/6-7-8-rendering-and-js.md) — **MEDIUM**
- **`<Activity>` Component** (Show/Hide with State preservation)
- CSS `content-visibility`
- Hydration Mismatch Prevention (No-Flicker)
- Hoisting Static JSX

### 7. [JavaScript Micro-Optimizations](./references/6-7-8-rendering-and-js.md) — **LOW-MEDIUM**
- Batching DOM Changes
- Index Maps vs `.find()`
- `toSorted()` vs `sort()`

### 8. [Advanced Patterns](./references/6-7-8-rendering-and-js.md) — **LOW**
- Event Handlers in Refs / `useEffectEvent`
- `useLatest` for Stable Callback Refs

## Quick Reference: The "Do's" and "Don'ts"

| **Don't** | **Do** |
| :--- | :--- |
| `import { Icon } from 'large-lib'` | `import Icon from 'large-lib/Icon'` |
| `await a(); await b();` | `Promise.all([a(), b()])` |
| `useEffect(() => { fetch(...) }, [])` | `const data = use(dataPromise)` |
| `const [state, set] = useState(init())` | `useState(() => init())` |
| `array.sort()` | `array.toSorted()` |
| `searchParams` in component body | `searchParams` only in callbacks |
| Manual `useMemo`/`useCallback` (mostly) | Trust React Compiler (but check Rules of React) |

---
*Optimized for React 19.2+ and Next.js 16.1+.*
*Updated: January 22, 2026 - 14:59*

---
name: react-patterns
description: |
  React 19+ patterns, performance optimization, and component architecture. Covers hooks, state management decision trees, data fetching with use() API, Server Components, React Compiler, bundle optimization, and re-render elimination.

  Use when building components, optimizing re-renders, fetching data, managing state, handling forms, structuring frontends, or reviewing React code.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://react.dev'
---

# React

## Overview

Comprehensive React skill covering component architecture, performance optimization, state management, data fetching, and modern React 19+ APIs. Prioritizes React Compiler compatibility, Server Components, and elimination of data fetching waterfalls.

**When to use:** Building React applications, optimizing performance, choosing state management, implementing data fetching, reviewing component architecture.

**When NOT to use:** Non-React frameworks, purely server-side rendering without React, static sites without interactivity.

## Quick Reference

| Pattern               | API / Approach                                    | Key Points                                          |
| --------------------- | ------------------------------------------------- | --------------------------------------------------- |
| Data fetching         | `use(dataPromise)`                                | Replaces useEffect+useState fetch pattern           |
| Form handling         | `useActionState(action, init)`                    | Built-in pending states and error handling          |
| Optimistic UI         | `useOptimistic(state, updateFn)`                  | Instant feedback while server processes             |
| Non-urgent updates    | `useTransition()`                                 | Mark updates as interruptible                       |
| Effect events         | `useEffectEvent(fn)`                              | Reactive values without re-triggering effects       |
| Form pending status   | `useFormStatus()`                                 | Read parent form pending state from child component |
| Unique IDs            | `useId()`                                         | Hydration-safe IDs for accessibility                |
| Server state          | React Query / `useSuspenseQuery`                  | Caching, deduplication, background refetch          |
| Client state (local)  | `useState` / `useRef`                             | Single component or transient values                |
| Client state (global) | Zustand / Context                                 | Cross-component client-only state                   |
| Derived state         | Compute during render                             | Never sync derived values with effects              |
| Lazy initialization   | `useState(() => expensive())`                     | Avoid eager computation on every render             |
| Component types       | Page, Feature, UI                                 | Route entry, business logic, reusable primitives    |
| Memoization           | Trust React Compiler first                        | Manual useMemo/useCallback only when needed         |
| Ref as prop           | `ref` prop on function components                 | No `forwardRef` needed in React 19                  |
| Ref cleanup           | Return function from ref callback                 | Cleanup runs on detach instead of `null` call       |
| Code splitting        | `React.lazy()` + Suspense                         | Lazy-load heavy components                          |
| Parallel fetches      | `Promise.all()`                                   | Eliminate sequential await waterfalls               |
| Request dedup         | `React.cache()`                                   | Per-request server-side deduplication               |
| Abort server work     | `cacheSignal()`                                   | Cancel expensive async work when client disconnects |
| Resource preloading   | `prefetchDNS`, `preconnect`, `preload`, `preinit` | Optimize resource loading from components           |
| State preservation    | `<Activity>`                                      | Hide UI while keeping state mounted                 |

## Common Mistakes

| Mistake                                                     | Correct Pattern                                                                                         |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Fetching data in useEffect with useState                    | Use the `use()` API or React Query for data fetching with built-in caching                              |
| Storing derived values in state and syncing with effects    | Compute derived values during render; never use effects for state synchronization                       |
| Wrapping everything in useMemo and useCallback              | Trust React Compiler first; only add manual memoization for expensive computations or memoized children |
| Using `array.sort()` which mutates state                    | Use `array.toSorted()` for immutable sorting to avoid unexpected re-renders                             |
| Using `&&` for conditional rendering                        | Use ternary `condition ? <Component /> : null` to avoid rendering falsy values like `0`                 |
| Using Math.random() or Date for IDs                         | Use `useId()` for hydration-safe unique identifiers                                                     |
| Putting reactive values in effect deps to read latest value | Use `useEffectEvent` to access latest values without re-triggering effects                              |
| Creating object literals as effect dependencies             | Hoist static objects outside the component or use primitive dependencies                                |
| Using `forwardRef` in React 19 projects                     | Pass `ref` directly as a prop; `forwardRef` is deprecated in React 19                                   |
| Mutating props or state during render                       | Follow Rules of React for React Compiler compatibility: pure renders, no side effects                   |

## Delegation

- **Explore component architecture and identify performance bottlenecks**: Use `Explore` agent to profile re-renders, analyze bundle size, and trace data fetching waterfalls
- **Implement React feature with proper patterns**: Use `Task` agent to build components following Server Component, Suspense, and React 19 conventions
- **Design frontend architecture and state management strategy**: Use `Plan` agent to structure component hierarchy, select state management, and plan data fetching approach

> If the `shadcn-ui` skill is available, delegate component variant and theming questions to it.
> If the `tailwind` skill is available, delegate utility-first styling and design token questions to it.
> If the `zustand` skill is available, delegate global client state management questions to it.

## References

- [Component patterns, state management, and useEffect decisions](references/component-patterns.md)
- [Performance optimization: waterfalls, bundles, and re-renders](references/performance-optimization.md)
- [Hooks, Server Actions, and React 19 APIs](references/hooks-and-actions.md)
- [React Compiler patterns and re-render optimization](references/react-compiler.md)
- [Server-side rendering and React Server Components](references/server-side.md)
- [Anti-patterns and troubleshooting guide](references/anti-patterns.md)

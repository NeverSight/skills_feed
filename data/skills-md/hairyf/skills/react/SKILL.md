---
name: react
description: React library for building user interfaces. Use when building web applications, creating components, managing state, handling side effects, or optimizing performance.
metadata:
  author: Hairyf
  version: "2026.1.31"
  source: Generated from https://github.com/reactjs/react.dev, scripts located at https://github.com/antfu/skills
---

# React

> The skill is based on React, generated at 2026-01-31.

React is a JavaScript library for building user interfaces. It lets you compose complex UIs from small and isolated pieces of code called "components". React uses a declarative paradigm that makes it easier to reason about your application and aims to be both efficient and flexible.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| useState | Hook for managing component state with direct updates | [core-usestate](references/core-usestate.md) |
| useEffect | Hook for synchronizing components with external systems | [core-useeffect](references/core-useeffect.md) |
| useContext | Hook for reading and subscribing to context | [core-usecontext](references/core-usecontext.md) |
| useRef | Hook for referencing values that don't trigger re-renders | [core-useref](references/core-useref.md) |
| useReducer | Hook for managing complex state with a reducer function | [core-usereducer](references/core-usereducer.md) |
| Suspense | Component for displaying fallback UI while content is loading | [core-suspense](references/core-suspense.md) |
| memo | Higher-order component for memoizing component renders | [core-memo](references/core-memo.md) |
| createContext | API for creating context objects | [core-createcontext](references/core-createcontext.md) |
| Fragment | Component for grouping elements without wrapper nodes | [core-fragment](references/core-fragment.md) |
| StrictMode | Component for enabling additional development checks | [core-strictmode](references/core-strictmode.md) |

## Features

### Performance Optimization

| Topic | Description | Reference |
|-------|-------------|-----------|
| useMemo | Hook for caching expensive calculations | [features-usememo](references/features-usememo.md) |
| useCallback | Hook for caching function definitions | [features-usecallback](references/features-usecallback.md) |
| lazy | API for code splitting and lazy loading components | [features-lazy](references/features-lazy.md) |
| useTransition | Hook for non-blocking state updates | [features-usetransition](references/features-usetransition.md) |
| useDeferredValue | Hook for deferring non-critical UI updates | [features-usedeferredvalue](references/features-usedeferredvalue.md) |
| useLayoutEffect | Hook that fires synchronously before browser repaint | [features-uselayouteffect](references/features-uselayouteffect.md) |
| startTransition | API for marking non-blocking state updates | [features-starttransition](references/features-starttransition.md) |

### Advanced Hooks

| Topic | Description | Reference |
|-------|-------------|-----------|
| useId | Hook for generating unique IDs for accessibility | [features-useid](references/features-useid.md) |
| use | API for reading Promise and Context values | [features-use](references/features-use.md) |
| useActionState | Hook for managing form action state | [features-useactionstate](references/features-useactionstate.md) |
| useOptimistic | Hook for optimistic UI updates | [features-useoptimistic](references/features-useoptimistic.md) |
| useInsertionEffect | Hook for CSS-in-JS libraries to inject styles | [advanced-useinsertioneffect](references/advanced-useinsertioneffect.md) |
| useSyncExternalStore | Hook for subscribing to external stores | [advanced-usesyncexternalstore](references/advanced-usesyncexternalstore.md) |
| useImperativeHandle | Hook for customizing ref handles | [advanced-useimperativehandle](references/advanced-useimperativehandle.md) |
| useEffectEvent | Hook for extracting non-reactive logic from Effects | [advanced-useeffectevent](references/advanced-useeffectevent.md) |
| useDebugValue | Hook for adding labels to custom hooks in DevTools | [advanced-usedebugvalue](references/advanced-usedebugvalue.md) |

### React DOM APIs

| Topic | Description | Reference |
|-------|-------------|-----------|
| createRoot | API for creating a root to render React components | [react-dom-createroot](references/react-dom-createroot.md) |
| hydrateRoot | API for hydrating server-rendered HTML | [react-dom-hydrateroot](references/react-dom-hydrateroot.md) |
| createPortal | API for rendering children into different DOM nodes | [react-dom-createportal](references/react-dom-createportal.md) |
| flushSync | API for forcing synchronous updates | [react-dom-flushsync](references/react-dom-flushsync.md) |

### React Server Components

| Topic | Description | Reference |
|-------|-------------|-----------|
| cache | API for caching function results in Server Components | [rsc-cache](references/rsc-cache.md) |

### Advanced Components

| Topic | Description | Reference |
|-------|-------------|-----------|
| Profiler | Component for measuring rendering performance | [advanced-profiler](references/advanced-profiler.md) |
| Activity | Component for hiding and restoring UI state | [features-activity](references/features-activity.md) |

### Testing

| Topic | Description | Reference |
|-------|-------------|-----------|
| act | Test helper for applying pending updates before assertions | [testing-act](references/testing-act.md) |

### Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Rules of Hooks | Fundamental rules for using React Hooks correctly | [best-practices-rules-of-hooks](references/best-practices-rules-of-hooks.md) |
| Component Purity | Rules for keeping React components and hooks pure | [best-practices-purity](references/best-practices-purity.md) |

## Key Recommendations

- **Use hooks at the top level** - Never call hooks conditionally or in loops
- **Keep components pure** - Components should be idempotent and have no side effects during render
- **Use useEffect for side effects** - Synchronize with external systems using Effects
- **Memoize expensive calculations** - Use `useMemo` for costly computations, `useCallback` for functions passed to memoized components
- **Code split with lazy** - Use `lazy` and `Suspense` for route-based code splitting
- **Avoid premature optimization** - Profile first, optimize only when needed
- **Use React Compiler** - Consider using React Compiler for automatic memoization
- **Handle dependencies correctly** - Always include all reactive values in Effect and memoization dependencies

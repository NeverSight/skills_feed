---
name: shadcn-hooks
description: Apply shadcn-hooks React hooks where appropriate to build concise, maintainable React features.
license: MIT
metadata:
  author: Brendan Dash <me@aiwan.run>
  version: '1.0'
compatibility: Requires React 18 (or above) project
---

# shadcn-hooks

This skill is a decision-and-implementation guide for [shadcn-hooks](https://github.com/Debbl/shadcn-hooks) in React projects. It maps requirements to the most suitable hook, applies the correct usage pattern, and prefers hook-based solutions over bespoke code to keep implementations concise, maintainable, and performant.

## When to Apply

- Apply this skill whenever assisting user development work in React / Next.js.
- Always check first whether a shadcn-hooks function can fulfill the requirement.
- Prefer shadcn-hooks over custom code to improve readability, maintainability, and performance.
- Map requirements to the most appropriate hook and follow the hook's invocation rule.
- Please refer to the `Invocation` field in the below functions table. For example:
  - `AUTO`: Use automatically when applicable.
  - `EXTERNAL`: Use only if the user already installed the required external dependency; otherwise reconsider, and ask to install only if truly needed.

## Installation

**Prefer the shadcn CLI** — it copies only the hooks you need into your project (zero extra runtime dependencies, tree-shake friendly):

```bash
# Install a single hook (recommended)
npx shadcn@latest add @hooks/use-boolean

# Install multiple hooks at once
npx shadcn@latest add @hooks/use-boolean @hooks/use-mount @hooks/use-debounce
```

Alternatively, install the full npm package (all hooks bundled):

```bash
npm install shadcn-hooks
```

> When using the shadcn CLI, import from the local path (e.g. `import { useBoolean } from "@/hooks/use-boolean"`).
> When using the npm package, import from `"shadcn-hooks"` (e.g. `import { useBoolean } from "shadcn-hooks"`).

## Functions

All functions listed below are part of [shadcn-hooks](https://shadcn-hooks.vercel.app/). Each section categorizes functions based on their functionality.

IMPORTANT: Each function entry includes a short `Description` and a detailed `Reference`. When using any function, always consult the corresponding document in `./references` for Usage details and Type Declarations.

### State

| Function                                                     | Description                                                       | Invocation |
| ------------------------------------------------------------ | ----------------------------------------------------------------- | ---------- |
| [`useBoolean`](references/useBoolean.md)                     | Boolean state with `set`, `setTrue`, `setFalse`, `toggle` helpers | AUTO       |
| [`useControllableValue`](references/useControllableValue.md) | Supports both controlled and uncontrolled component patterns      | AUTO       |
| [`useCounter`](references/useCounter.md)                     | Counter with `inc`, `dec`, `set`, `reset` helpers                 | AUTO       |
| [`useDebounce`](references/useDebounce.md)                   | Debounced reactive value                                          | AUTO       |
| [`useResetState`](references/useResetState.md)               | State with a `reset` function to restore the initial value        | AUTO       |
| [`useThrottle`](references/useThrottle.md)                   | Throttled reactive value                                          | AUTO       |
| [`useToggle`](references/useToggle.md)                       | Toggle between two values with utility actions                    | AUTO       |

### Advanced

| Function                                                         | Description                                           | Invocation |
| ---------------------------------------------------------------- | ----------------------------------------------------- | ---------- |
| [`useCreation`](references/useCreation.md)                       | Memoized factory with deep dependency comparison      | AUTO       |
| [`useCustomCompareEffect`](references/useCustomCompareEffect.md) | `useEffect` with a custom dependency comparator       | AUTO       |
| [`useLatest`](references/useLatest.md)                           | Ref that always holds the latest value                | AUTO       |
| [`useLockFn`](references/useLockFn.md)                           | Prevents concurrent execution of an async function    | AUTO       |
| [`useMemoizedFn`](references/useMemoizedFn.md)                   | Stable function reference that never changes identity | AUTO       |
| [`usePrevious`](references/usePrevious.md)                       | Returns the previous value of a state                 | AUTO       |

### Lifecycle

| Function                                                                 | Description                                                     | Invocation |
| ------------------------------------------------------------------------ | --------------------------------------------------------------- | ---------- |
| [`useDebounceEffect`](references/useDebounceEffect.md)                   | Debounced `useEffect`                                           | AUTO       |
| [`useDebounceFn`](references/useDebounceFn.md)                           | Debounced function with `run`, `cancel`, `flush` controls       | AUTO       |
| [`useDeepCompareEffect`](references/useDeepCompareEffect.md)             | `useEffect` with deep dependency comparison                     | AUTO       |
| [`useDeepCompareLayoutEffect`](references/useDeepCompareLayoutEffect.md) | `useLayoutEffect` with deep dependency comparison               | AUTO       |
| [`useEffectEvent`](references/useEffectEvent.md)                         | Ponyfill for React 19's `useEffectEvent`                        | AUTO       |
| [`useEffectWithTarget`](references/useEffectWithTarget.md)               | `useEffect` that supports target DOM element(s) as dependencies | AUTO       |
| [`useInterval`](references/useInterval.md)                               | Interval timer with auto-cleanup                                | AUTO       |
| [`useIsHydrated`](references/useIsHydrated.md)                           | Returns `true` after client hydration completes                 | AUTO       |
| [`useIsomorphicLayoutEffect`](references/useIsomorphicLayoutEffect.md)   | `useLayoutEffect` on client, `useEffect` on server              | AUTO       |
| [`useMount`](references/useMount.md)                                     | Runs a callback only on component mount                         | AUTO       |
| [`useThrottleEffect`](references/useThrottleEffect.md)                   | Throttled `useEffect`                                           | AUTO       |
| [`useThrottleFn`](references/useThrottleFn.md)                           | Throttled function with `run`, `cancel`, `flush` controls       | AUTO       |
| [`useTimeout`](references/useTimeout.md)                                 | Timeout timer with auto-cleanup                                 | AUTO       |
| [`useUnmount`](references/useUnmount.md)                                 | Runs cleanup on component unmount                               | AUTO       |
| [`useUpdate`](references/useUpdate.md)                                   | Returns a function that forces component re-render              | AUTO       |
| [`useUpdateEffect`](references/useUpdateEffect.md)                       | `useEffect` that skips the first render                         | AUTO       |

### Browser

| Function                                             | Description                                       | Invocation |
| ---------------------------------------------------- | ------------------------------------------------- | ---------- |
| [`useClickAnyWhere`](references/useClickAnyWhere.md) | Listen to click events anywhere on the document   | AUTO       |
| [`useClickAway`](references/useClickAway.md)         | Detect clicks outside of target element(s)        | AUTO       |
| [`useClipboard`](references/useClipboard.md)         | Reactive Clipboard API with read/write support    | AUTO       |
| [`useEventListener`](references/useEventListener.md) | Declarative event listener with auto-cleanup      | AUTO       |
| [`useFps`](references/useFps.md)                     | Reactive FPS (frames per second) measurement      | AUTO       |
| [`useFullscreen`](references/useFullscreen.md)       | Reactive Fullscreen API                           | AUTO       |
| [`useHash`](references/useHash.md)                   | Reactive `window.location.hash`                   | AUTO       |
| [`useHover`](references/useHover.md)                 | Reactive hover state of an element                | AUTO       |
| [`useInViewport`](references/useInViewport.md)       | Track element visibility via IntersectionObserver | AUTO       |
| [`useIsMatchMedia`](references/useIsMatchMedia.md)   | Reactive CSS media query matching                 | AUTO       |
| [`useIsOnline`](references/useIsOnline.md)           | Reactive online/offline network status            | AUTO       |
| [`useNetwork`](references/useNetwork.md)             | Reactive network connection information           | AUTO       |
| [`useScrollLock`](references/useScrollLock.md)       | Lock/unlock scroll on a target element            | AUTO       |
| [`useTextSelection`](references/useTextSelection.md) | Reactive text selection state with bounding rect  | AUTO       |

### Dev

| Function                                                 | Description                                           | Invocation |
| -------------------------------------------------------- | ----------------------------------------------------- | ---------- |
| [`useWhyDidYouUpdate`](references/useWhyDidYouUpdate.md) | Logs which props changed between renders (debug only) | AUTO       |

### External

| Function                                             | Description                                                                                          | Invocation |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------- |
| [`useMcp`](references/useMcp.md)                     | Model Context Protocol client hook from [`use-mcp`](https://github.com/modelcontextprotocol/use-mcp) | EXTERNAL   |
| [`useQuery`](references/useQuery.md)                 | Data fetching hook from [`@tanstack/react-query`](https://tanstack.com/query)                        | EXTERNAL   |
| [`useStickToBottom`](references/useStickToBottom.md) | Scroll-stick behavior from [`use-stick-to-bottom`](https://github.com/nicejmkim/use-stick-to-bottom) | EXTERNAL   |
| [`useSWR`](references/useSWR.md)                     | Data fetching hook from [`swr`](https://swr.vercel.app/)                                             | EXTERNAL   |

---
name: react-component-performance
description: Analyze and optimize React component performance issues (slow renders, re-render thrash, laggy lists, expensive computations). Use when asked to profile or improve a React component, reduce re-renders, or speed up UI updates in React apps.
---

# React Component Performance

## Overview

Identify render hotspots, isolate expensive updates, and apply targeted optimizations without changing UI behavior.

## Workflow

1. Reproduce or describe the slowdown.
2. Identify what triggers re-renders (state updates, props churn, effects).
3. Isolate fast-changing state from heavy subtrees.
4. Stabilize props and handlers; memoize where it pays off.
5. Reduce expensive work (computation, DOM size, list length).
6. Validate with profiling; avoid speculative changes.

## Checklist

- Measure: use React DevTools Profiler or log renders; capture baseline.
- Find churn: identify state updated on a timer, scroll, input, or animation.
- Split: move ticking state into a child; keep heavy lists static.
- Memoize: wrap leaf rows with `memo` only when props are stable.
- Stabilize props: use `useCallback`/`useMemo` for handlers and derived values.
- Avoid derived work in render: precompute, or compute inside memoized helpers.
- Control list size: window/virtualize long lists; avoid rendering hidden items.
- Keys: ensure stable keys; avoid index when order can change.
- Effects: verify dependency arrays; avoid effects that re-run on every render.
- Style/layout: watch for expensive layout thrash or large Markdown/diff renders.

## Optimization Patterns

- **Isolate ticking state**: move a timer/animation into a child component so the parent list does not re-render every tick.
- **Stabilize callbacks**: prefer `useCallback` for handlers passed to memoized rows.
- **Split rows**: extract list rows into memoized components with narrow props.
- **Defer heavy rendering**: lazy-render or collapse expensive content until expanded.
- **Prefer derived data outside render**: compute summaries with `useMemo` or helper functions when inputs are stable.

## Example Reference

Load `references/examples.md` when the user wants a concrete refactor example.

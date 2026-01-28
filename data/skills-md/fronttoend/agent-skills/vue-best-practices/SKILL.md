---
name: vue-best-practices
description: Vue 3 and Nuxt performance optimization guidelines. This skill should be used when writing, reviewing, or refactoring Vue 3/Nuxt code to ensure optimal performance patterns. Triggers on tasks involving Vue components, Nuxt pages, data fetching, bundle optimization, or performance improvements.
---

# Vue Best Practices

## Overview

Comprehensive performance optimization guide for Vue 3 and Nuxt applications, containing 40+ rules across 8 categories. Rules are prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:

- Writing new Vue 3 components or Nuxt pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing Vue/Nuxt code
- Optimizing bundle size or load times

## Priority-Ordered Guidelines

Rules are prioritized by impact:

| Priority | Category                 | Impact      |
| -------- | ------------------------ | ----------- |
| 1        | Eliminating Waterfalls   | CRITICAL    |
| 2        | Bundle Size Optimization | CRITICAL    |
| 3        | Server-Side Performance  | HIGH        |
| 4        | Reactivity Optimization  | MEDIUM-HIGH |
| 5        | Re-render Optimization   | MEDIUM      |
| 6        | Rendering Performance    | MEDIUM      |
| 7        | JavaScript Performance   | LOW-MEDIUM  |
| 8        | Advanced Patterns        | LOW         |

## Quick Reference

### Critical Patterns (Apply First)

**Eliminate Waterfalls:**

- Defer await until needed (move into branches)
- Use `Promise.all()` for independent async operations
- Start promises early, await late
- Use Nuxt `useAsyncData` with `lazy` option for parallel fetching
- Use `<Suspense>` boundaries to stream content

**Reduce Bundle Size:**

- Avoid barrel file imports (import directly from source)
- Use `defineAsyncComponent` for heavy components
- Defer non-critical third-party libraries
- Use Vite's dynamic import for code splitting
- Consider `petite-vue` for progressive enhancement

### High-Impact Server Patterns

- Avoid cross-request state pollution in SSR
- Create new app instance per request
- Use Pinia with SSR-safe patterns
- Parallelize data fetching with component composition
- Minimize serialization at SSR boundaries

### Medium-Impact Reactivity Patterns

- Use `ref()` as primary API over `reactive()`
- Use `shallowRef()` for large immutable data
- Apply `markRaw()` for non-reactive data
- Use `toRef()`/`toRefs()` for safe destructuring
- Leverage computed stability (Vue 3.4+)

### Re-render Patterns

- Use `v-once` for static content
- Use `v-memo` for conditional update skipping
- Keep props stable to prevent child updates
- Avoid unnecessary component abstractions
- Use derived state in watchers

### Rendering Patterns

- Virtualize large lists with `vue-virtual-scroller`
- Use `content-visibility: auto` for long lists
- Apply `<KeepAlive>` for component caching
- Use `<Teleport>` for portal rendering
- Prefer `v-if` over `v-show` for heavy components

### JavaScript Patterns

- Batch DOM CSS changes via classes
- Build index maps for repeated lookups
- Cache repeated function calls
- Use `toSorted()` instead of `sort()` for immutability
- Early return from functions

## References

Full documentation with code examples is available in:

- `references/vue-performance-guidelines.md` - Complete guide with all patterns
- `references/rules/` - Individual rule files organized by category

To look up a specific pattern, grep the rules directory:

```
grep -l "suspense" references/rules/
grep -l "async-component" references/rules/
grep -l "shallowRef" references/rules/
```

## Rule Categories in `references/rules/`

- `async-*` - Waterfall elimination patterns
- `bundle-*` - Bundle size optimization
- `server-*` - Server-side performance
- `reactivity-*` - Vue reactivity patterns
- `rerender-*` - Re-render optimization
- `rendering-*` - DOM rendering performance
- `js-*` - JavaScript micro-optimizations
- `advanced-*` - Advanced patterns

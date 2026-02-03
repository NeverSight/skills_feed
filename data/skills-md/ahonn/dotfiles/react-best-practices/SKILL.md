---
name: react-best-practices
description: "React best practices from react.dev and Vercel. Use when: (1) Reviewing React code, (2) Debugging performance issues, (3) Optimizing bundle size, (4) Writing effects or state logic. Triggers on: React performance, re-render, bundle size, waterfalls, code splitting, memo, useCallback, useMemo, useEffect, SSR flicker, initial load slow, React Compiler, state structure, immutable update, setState array object."
user-invocable: false
---

# React Best Practices

Performance patterns and guidelines from react.dev and Vercel Engineering.

## Quick Reference (Priority Order)

### CRITICAL - Must Follow

| Rule | Impact | Reference |
|------|--------|-----------|
| Avoid unnecessary effects | Render cycles, bugs | [effect-pitfalls.md](references/effect-pitfalls.md) |
| Eliminate waterfalls | First paint, TTI | [async-waterfall-elimination.md](references/async-waterfall-elimination.md) |
| Parallel data fetching | Load time | [async-parallel-requests.md](references/async-parallel-requests.md) |
| Avoid barrel imports | Bundle size | [bundle-barrel-imports.md](references/bundle-barrel-imports.md) |

### HIGH - Strongly Recommended

| Rule | Impact | Reference |
|------|--------|-----------|
| React Compiler (19+) | Auto memoization | [react-compiler.md](references/react-compiler.md) |
| Dynamic imports | Code splitting | [bundle-dynamic-import.md](references/bundle-dynamic-import.md) |
| Preload on user intent | Perceived latency | [bundle-preload.md](references/bundle-preload.md) |
| Strategic memo() | Render perf | [rerender-memo-strategy.md](references/rerender-memo-strategy.md) |
| Server caching | Server response | [server-cache-patterns.md](references/server-cache-patterns.md) |

### MEDIUM - Recommended

| Rule | Impact | Reference |
|------|--------|-----------|
| State structure | Maintainability | [state-structure.md](references/state-structure.md) |
| Immutable updates | Avoid mutation bugs | [immutable-updates.md](references/immutable-updates.md) |
| Context splitting | Avoid rerenders | [rerender-context-splitting.md](references/rerender-context-splitting.md) |
| startTransition | UI responsiveness | [rerender-transitions.md](references/rerender-transitions.md) |
| Set/Map lookups | O(1) vs O(n) | [js-set-map-lookups.md](references/js-set-map-lookups.md) |
| Key patterns | List rendering | [rendering-key-patterns.md](references/rendering-key-patterns.md) |

### LOW - Nice to Have

| Rule | Impact | Reference |
|------|--------|-----------|
| content-visibility | Long list render | [rendering-content-visibility.md](references/rendering-content-visibility.md) |
| Hydration flicker | SSR stability | [rendering-hydration-flicker.md](references/rendering-hydration-flicker.md) |
| Hoist static JSX | Avoid re-creation | [rendering-hoist-static-jsx.md](references/rendering-hoist-static-jsx.md) |

---

## Quick Decision Tree

```
React Issue?
├── Writing useEffect?
│   └── Check if needed → effect-pitfalls.md (CRITICAL)
├── Designing state?
│   └── Follow 5 principles → state-structure.md
├── Updating state?
│   └── Use immutable patterns → immutable-updates.md
├── Using React 19+?
│   └── Enable React Compiler → react-compiler.md
├── Slow initial load?
│   ├── Check for waterfalls → async-waterfall-elimination.md
│   ├── Check bundle size → bundle-barrel-imports.md
│   └── Preload on intent → bundle-preload.md
├── Slow interactions?
│   ├── Check re-renders → rerender-memo-strategy.md
│   ├── Check Context usage → rerender-context-splitting.md
│   └── Use transitions → rerender-transitions.md
├── Long list jank?
│   └── Use content-visibility → rendering-content-visibility.md
├── SSR flicker?
│   └── Inline script pattern → rendering-hydration-flicker.md
└── Slow server?
    └── Check caching → server-cache-patterns.md
```

---

## Reference Files

| File | Content |
|------|---------|
| [hooks-guide.md](references/hooks-guide.md) | Hook patterns, decision guides, pitfalls |
| [effect-pitfalls.md](references/effect-pitfalls.md) | When NOT to use useEffect |
| [react-compiler.md](references/react-compiler.md) | React 19+ auto memoization |
| [state-structure.md](references/state-structure.md) | 5 principles for state design |
| [immutable-updates.md](references/immutable-updates.md) | Array/object update patterns |
| [references/](references/) | All reference files (19 total) |

**Search rules**: `grep -l "keyword" references/`

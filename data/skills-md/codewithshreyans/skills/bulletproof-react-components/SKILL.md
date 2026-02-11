---
name: bulletproof-react-components
description: Build bulletproof React components that survive SSR, hydration, concurrent rendering, portals, transitions, and future React changes. Nine essential patterns from Shu Ding's guide. Use when writing reusable React components, fixing hydration mismatches, handling SSR edge cases, or building component libraries.
---

# Bulletproof React Components

Nine patterns that ensure React components survive real-world conditions beyond the happy path — SSR, hydration, concurrent rendering, portals, and more.

Source: [shud.in/thoughts/build-bulletproof-react-components](https://shud.in/thoughts/build-bulletproof-react-components)

## How It Works

1. When writing or reviewing a reusable React component, consult the **Quick Rules** below
2. For code examples and deeper explanation, read `./references/patterns.md`
3. Run through the **Checklist** before shipping

## Quick Rules

| # | Pattern | Rule |
|---|---------|------|
| 1 | **Server-Proof** | Never call browser APIs (`localStorage`, `window`, `document`) during render. Use `useEffect`. |
| 2 | **Hydration-Proof** | Inject a synchronous inline `<script>` to set client-dependent values before React hydration. |
| 3 | **Instance-Proof** | Use `useId()` for all generated IDs. Never hardcode IDs in reusable components. |
| 4 | **Concurrent-Proof** | Wrap server data-fetching in `React.cache()` to deduplicate calls per request. |
| 5 | **Composition-Proof** | Use Context instead of `React.cloneElement()` — cloneElement breaks with Server Components, lazy, and memo. |
| 6 | **Portal-Proof** | Use `ref.current?.ownerDocument.defaultView \|\| window` for event listeners, not the global `window`. |
| 7 | **Transition-Proof** | Wrap state updates in `startTransition()` to enable View Transition API animations. |
| 8 | **Activity-Proof** | Use `useLayoutEffect` to disable DOM side effects (e.g., `<style>` tags) when hidden by `<Activity>`. |
| 9 | **Future-Proof** | Use `useState(() => value)` for stable identity. `useMemo` is only a performance hint — React may discard it. |

## Checklist

When building a reusable React component, verify:

- [ ] No browser APIs called during render (server-proof)
- [ ] No hydration flash for client-storage values (hydration-proof)
- [ ] No hardcoded IDs; uses `useId()` (instance-proof)
- [ ] Server data fetches wrapped in `cache()` (concurrent-proof)
- [ ] Uses Context instead of `cloneElement` (composition-proof)
- [ ] Event listeners use `ownerDocument.defaultView` (portal-proof)
- [ ] State updates wrapped in `startTransition()` where needed (transition-proof)
- [ ] DOM side effects respect `<Activity>` visibility (activity-proof)
- [ ] Stable values use `useState` initializer, not `useMemo` (future-proof)

## Present Results to User

When reviewing a component against these patterns, format as:

```
**Bulletproof Check: `<ComponentName>`**

| Pattern | Status | Notes |
|---------|--------|-------|
| Server-Proof | PASS/FAIL | ... |
| ... | ... | ... |

**Suggested fixes:**
1. ...
```

## References

- `./references/patterns.md` — Detailed code examples (bad/good) for all nine patterns

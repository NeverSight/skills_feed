---
name: vani-global-store
description: Create a tiny global store with explicit subscriptions
---

# Global Store with Subscriptions

Instructions for implementing a small store and wiring components to it.

## When to Use

Use this when multiple components need shared state without implicit reactivity by default.

## Steps

1. Implement a store with `getState`, `setState`, and `subscribe`.
2. In components, call `handle.onBeforeMount()` to subscribe once.
3. On store updates, call `handle.update()` from the subscription.
4. Keep mutations behind store commands to avoid stale views.

## Arguments

- stateShape - description of the state object (defaults to `{}`)
- storeFile - path to the store module (defaults to `src/store.ts`)
- featureName - feature identifier for naming (defaults to `App`)

## Examples

Example 1 usage pattern:

Create a counter store and a component that reads `getState()` during render.

Example 2 usage pattern:

Expose a `setState` command and update UI through subscriptions only.

## Output

Example output:

```
Created: src/store.ts
Updated: src/counter.ts
Notes: handle.onBeforeMount() subscribes once and updates explicitly.
```

## Present Results to User

Summarize store API, subscription wiring, and files changed.

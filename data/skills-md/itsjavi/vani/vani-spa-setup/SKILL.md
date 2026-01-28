---
name: vani-spa-setup
description: Create a minimal Vani SPA root with explicit updates
---

# Vani SPA Setup

Instructions for the agent to scaffold a basic Vani SPA using explicit updates.

## When to Use

Use this when a user needs a new Vani SPA root, a simple component, or a quick demo that mounts to a
DOM element.

## Steps

1. Create a root component with `component` that returns a render function.
2. Store local state in variables and call `handle.update()` from event handlers.
3. Find the root element by id and throw if missing.
4. Mount the component with `renderToDOM(App(), root)` (arrays also work).

## Arguments

- rootId - DOM id of the mount node (defaults to `app`)
- componentName - name of the root component (defaults to `App`)
- includeCounter - whether to include a counter example (defaults to `true`)

## Examples

Example 1 usage pattern:

Create a `Counter` component and mount it to `#app` with explicit updates.

Example 2 usage pattern:

Create an `App` component that composes child components and mount it to a custom root id.

## Output

Example output:

```
Created: src/app.ts
Updated: src/main.ts
Notes: Uses handle.update() for all state changes.
```

## Present Results to User

Provide a short explanation of how the root is mounted, list the files touched, and mention where
explicit updates occur.

---
name: vani-incremental-mount
description: Mount Vani components inside existing apps or DOM islands
---

# Incremental Mounting

Instructions for embedding Vani components into existing applications via mount points.

## When to Use

Use this when adding a Vani widget inside a non-Vani app or server-rendered page.

## Steps

1. Create a Vani component with explicit updates.
2. Find or create a DOM mount node inside the host app.
3. Call `renderToDOM(Widget(), mountNode)` (arrays also work) and store the returned handles.
4. On host unmount/cleanup, call `handle.dispose()` for each handle.

## Arguments

- mountSelector - CSS selector or id for the mount point (defaults to `#app`)
- componentName - name of the embedded component (defaults to `Widget`)
- cleanupStrategy - how cleanup is triggered (defaults to `onUnmount`)

## Examples

Example 1 usage pattern:

Embed a Vani counter inside a React or server-rendered page using a `div` mount node.

Example 2 usage pattern:

Create multiple independent widgets with separate mount points and dispose them on teardown.

## Output

Example output:

```
Created: src/widget.ts
Updated: src/host-integration.ts
Notes: Handles are disposed when the host unmounts.
```

## Present Results to User

Explain the mount point, how handles are stored and disposed, and list file changes.

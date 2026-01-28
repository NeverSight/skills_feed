---
name: vani-ssr-hydration
description: Implement SSR, hydration, and selective activation with Vani
---

# Vani SSR and Hydration

Instructions for rendering on the server and hydrating on the client with explicit activation.

## When to Use

Use this when a project needs SSR or SSG, or when hydration must be selective.

## Steps

1. Render on the server with `renderToString(App())` (arrays also work).
2. On the client, call `hydrateToDOM(App(), root)` (arrays also work) to bind handles to anchors.
3. Activate interactivity by calling `handle.update()` on the handles you want to run.
4. For selective hydration, update only specific handles (e.g., header) and leave others inert.

## Arguments

- rootId - DOM id that contains server HTML (defaults to `app`)
- activateAll - whether to update all handles immediately (defaults to `true`)
- selectiveRefs - list of component refs to activate (defaults to `[]`)

## Examples

Example 1 usage pattern:

SSR a page, hydrate on the client, then call `handle.update()` for all handles.

Example 2 usage pattern:

Hydrate a page but activate only the header using a `ComponentRef`.

## Output

Example output:

```
Created: server/render.ts
Updated: client/entry.ts
Notes: Hydration binds to anchors; update() activates UI.
```

## Present Results to User

## Summarize the SSR/hydration flow, note which handles are activated, and list file changes.

name: vani-ssr-hydration description: Apply Vani SSR, hydration, and client-only islands correctly.
argument-hint: "[rendering mode or feature]"

---

# Vani SSR and Hydration Command

## When to use

Use this skill when implementing SSR, SSG, hydration, or client-only islands.

## Instructions

Follow these steps:

1. For SSR/SSG, render with `renderToString()` on the server (single or array).
2. Bind on the client with `hydrateToDOM()` (single or array); do not expect it to render.
3. Activate UI by calling `handle.update()` on chosen handles.
4. Use `clientOnly: true` for islands that should skip SSR.
5. Keep hydration order identical to the server render order.

## Output expectations

- Use only `@vanijs/vani` or other public packages.
- Do not assume hydration runs effects before `handle.update()`.
- If $ARGUMENTS is provided, pick the correct render/hydration strategy.

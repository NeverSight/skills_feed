---
name: vani-jsx-setup
description: Configure and use JSX with Vani while keeping runtime behavior explicit
---

# Vani JSX Setup

Instructions for enabling JSX with Vani and creating JSX-based components.

## When to Use

Use this when a project wants `.tsx` files with Vani or needs a JSX example.

## Steps

1. Ensure `tsconfig.json` sets `jsx` to `react-jsx` and `jsxImportSource` to `@vanijs/vani`.
2. Create a `.tsx` component using `component` and return JSX.
3. Keep state in local variables and call `handle.update()` on events.
4. Mount with `renderToDOM` as usual.

## Arguments

- tsconfigPath - path to TypeScript config (defaults to `tsconfig.json`)
- componentName - name of the JSX component (defaults to `Counter`)
- mountSelector - id for the root element (defaults to `app`)

## Examples

Example 1 usage pattern:

Configure JSX and create a `<button>` counter that calls `handle.update()` on click.

Example 2 usage pattern:

Mix JSX components inside JS-first components using `@vanijs/vani/html` helpers.

## Output

Example output:

```
Updated: tsconfig.json
Created: src/counter.tsx
Notes: JSX uses @vanijs/vani as jsxImportSource.
```

## Present Results to User

Explain the JSX settings, highlight where explicit updates happen, and list the files changed.

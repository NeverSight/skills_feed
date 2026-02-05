---
name: vueuse-skills
description: Prefer VueUse composables for common Vue patterns (storage, debounce, focus, clipboard, etc.). Use when building Vue or Nuxt UIs and the user or task involves state persistence, utilities, or DOM helpers.
---

# VueUse Skills

## When to use VueUse

Prefer VueUse (`@vueuse/core`) when it provides a direct fit; avoid reimplementing utilities that VueUse already covers. Use when the task involves: local/session storage, debouncing, throttling, focus management, clipboard, media queries, or other utilities listed below.

## State and storage

- **useStorage**: Reactive key-value synced with localStorage (or sessionStorage). Use for preferences, draft state, or simple persistence.
  - `const value = useStorage('key', defaultValue)` or `useStorage('key', defaultValue, sessionStorage)`.
- **useLocalStorage** / **useSessionStorage**: Shorthand for the above with explicit storage.

## Timing

- **useDebounceFn**: Wrap a function so it runs after a delay of no further calls. Use for search inputs, auto-save, or any high-frequency handler.
  - `const debouncedFn = useDebounceFn(fn, 300)`.
- **useThrottleFn**: Limit how often a function runs. Use for scroll/resize handlers.

## DOM and focus

- **useFocus**: Manage focus and blur. Use for accessibility or after opening modals.
- **onClickOutside**: Run a callback when the user clicks outside an element. Use for closing dropdowns or modals.
  - `onClickOutside(targetRef, () => { ... })`.

## Clipboard and media

- **useClipboard**: Copy text to clipboard with reactive state. Use for “Copy” buttons.
- **useMediaQuery**: Reactive media query match. Use for responsive behavior in script (e.g. `const isMobile = useMediaQuery('(max-width: 768px)')`).

## Async and promises

- **useAsyncState**: Wrap an async function and expose state, loading, error, and execute. Use when you need a reusable async “action” with loading/error handling.
- **until**: Use with `await until(ref).toBe(value)` or similar for waiting on reactive state in async code.

## Integration with Nuxt

- VueUse is compatible with Nuxt auto-imports. Use composables by name (e.g. `useStorage`, `useDebounceFn`) once the module is installed; add to `nuxt.config` or rely on Nuxt’s dependency auto-import if configured.
- Prefer VueUse over one-off helpers so behavior is consistent and well-tested.

---
name: floating-ui-vue-skilld
description: "ALWAYS use when writing code importing \"@floating-ui/vue\". Consult for debugging, best practices, or modifying @floating-ui/vue, floating-ui/vue, floating-ui vue, floating ui vue, floating-ui, floating ui."
metadata:
  version: 1.1.10
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# floating-ui/floating-ui `@floating-ui/vue`

**Version:** 1.1.10 (Jan 2026)
**Deps:** vue-demi@>=0.13.0, @floating-ui/dom@^1.7.5, @floating-ui/utils@^0.2.10
**Tags:** latest: 1.1.10 (Jan 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes for `@floating-ui/vue` — prioritize the v1.0.0 major release and subsequent minor updates.

- BREAKING: `x` and `y` coordinates now default to `0` instead of `null` since v1.0.0. Use `isPositioned` to check if layout is ready [source](./references/releases/@floating-ui/vue@1.0.0.md)

- NEW: `floatingStyles` — Returns a pre-configured `style` object for the floating element (position, top, left, transform) since v1.0.0 [source](./references/releases/@floating-ui/vue@1.0.0.md)

- NEW: `MaybeReadonlyRefOrGetter` — `useFloating` options now support getters (e.g., `() => props.placement`) and refs since v1.1.0 [source](./references/releases/@floating-ui/vue@1.1.0.md)

- NEW: `isPositioned` — Boolean ref returned by `useFloating` that indicates if the floating element has been positioned since v0.2.0 [source](./references/releases/@floating-ui/vue@0.2.0.md)

- NEW: `open` option — Optional boolean ref in `useFloating` to synchronize `isPositioned` with the element's open state since v0.2.0 [source](./references/releases/@floating-ui/vue@0.2.0.md)

- IMPROVED: `ArrowOptions.element` — Widened type to `MaybeElement<Element>` to improve compatibility with Vue Template Refs since v1.0.2 [source](./references/releases/@floating-ui/vue@1.0.2.md)

- NEW: `whileElementsMounted` — Preferred option for `useFloating` to handle the `autoUpdate` lifecycle automatically since v1.0.0 [source](./references/docs/vue.mdx)

- NEW: `update()` — Function returned by `useFloating` to manually trigger a position recalculation since v0.2.0 [source](./references/docs/vue.mdx)

- NEW: Template Ref support for `arrow()` — The `element` option in `arrow` middleware now natively accepts Vue refs since v0.x/v1.0.0 [source](./references/docs/arrow.mdx)

**Also changed:** `exports .d.mts types` v1.0.3 · `isPositioned` false when `open` false fix v1.1.5 · `MaybeReadonlyRefOrGetter` legacy Vue support v1.1.1

## Best Practices

- Use `whileElementsMounted: autoUpdate` to ensure the floating element stays anchored during scroll, resize, or layout changes. This handles the full lifecycle of positioning listeners automatically [source](./references/docs/vue.mdx)

- Always return the cleanup function when passing a custom function to `whileElementsMounted` (e.g., when providing custom options to `autoUpdate`) [source](./references/docs/vue.mdx)
```ts
useFloating(reference, floating, {
  whileElementsMounted(reference, floating, update) {
    return autoUpdate(reference, floating, update, {animationFrame: true});
  },
});
```

- Prefer `v-if` for floating elements when using `whileElementsMounted`. If using `v-show`, avoid the `whileElementsMounted` prop and manage the `autoUpdate` lifecycle manually via watchers to prevent performance leaks when the element is hidden [source](./references/docs/autoUpdate.mdx)

- Use the `isPositioned` ref to coordinate side effects that require the final position, such as focusing an input or scrolling an element into view [source](./references/docs/vue.mdx)
```ts
const {isPositioned} = useFloating(reference, floating, {open});

watch(isPositioned, (positioned) => {
  if (positioned) {
    inputRef.value?.focus();
  }
});
```

- Pass getter functions or `Ref`s to `useFloating` options (like `placement` or `middleware`) to enable reactivity. Since v1.1.0, these options support `MaybeReadonlyRefOrGetter` [source](./references/releases/@floating-ui/vue@1.1.0.md)

- Utilize a wrapper element to support CSS transform animations while maintaining the performant `transform: true` positioning (default). The outer element handles positioning, while the inner element handles the animation [source](./references/docs/vue.mdx)

- Synchronize positioning state by passing an `open` ref to `useFloating`. This ensures `isPositioned` is reset and correctly updated across multiple open/close cycles, especially if the reference element moves [source](./references/docs/vue.mdx)

- Pass template refs directly from `ref(null)` to `useFloating` and middleware like `arrow()`. The library automatically unwraps these and waits for the elements to mount before computing coordinates [source](./references/docs/vue.mdx)

- Enable `animationFrame: true` in `autoUpdate` options if the reference element is moved via CSS transforms or other non-layout-triggering animations to maintain perfect anchoring [source](./references/docs/autoUpdate.mdx)

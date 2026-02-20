---
name: motion-v-skilld
description: "ALWAYS use when writing code importing \"motion-v\". Consult for debugging, best practices, or modifying motion-v, motion v, motion-vue, motion vue."
metadata:
  version: 2.0.0-beta.4
  generated_by: Gemini CLI · Gemini 3 Flash
---

# motiondivision/motion-vue `motion-v`

**Version:** 2.0.0-beta.4 (Feb 2026)
**Deps:** framer-motion@^12.29.2, hey-listen@^1.0.8, motion-dom@^12.29.2, motion-utils@^12.29.2
**Tags:** latest: 2.0.0-beta.4 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `focus`, `hover`, `press`, `inView` shorthand props — removed in v2.0.0-beta.1. Use `whileFocus`, `whileHover`, `whilePress`, and `whileInView` for animations, and full event handlers (e.g. `@hoverStart`, `@pressStart`) for logic [source](./references/releases/v2.0.0-beta.1.md)

- NEW: `v-motion` directive — new in v2.0.0-beta.1, enables declarative animations on any element without requiring a `<motion>` component wrapper [source](./references/releases/v2.0.0-beta.1.md)

- BREAKING: ESM-only — v2.0.0-beta.1 dropped CommonJS support. The package now only ships ESM (`.mjs`) exports [source](./references/releases/v2.0.0-beta.1.md)

- NEW: `MotionPlugin` — new in v2.0.0-beta.1, a Vue plugin for global `v-motion` and custom preset directive registration

- NEW: `createPresetDirective()` — new in v2.0.0-beta.1, allows creating reusable animation directives with baked-in motion options

- BREAKING: `AnimatePresence` lazy discovery — v2.0.0-beta.1 refactored to use `data-ap` attribute for lazy discovery instead of eager registration [source](./references/releases/v2.0.0-beta.1.md)

- DEPRECATED: `staggerChildren` and `staggerDirection` — deprecated in v1.4.0 in favor of using the `stagger()` utility within the `transition` prop [source](./references/releases/v1.4.0.md)

- NEW: `stagger()` utility — correctly handles staggering for newly-entering siblings alongside existing ones since v1.7.0 [source](./references/releases/v1.7.0.md)

- NEW: `useTransform` output maps — supports providing multiple output value maps for complex coordinate transformations since v1.9.0 [source](./references/releases/v1.9.0.md)

- NEW: `Reorder` auto-scrolling — supports automatic parent container scrolling when a `Reorder.Item` is dragged to the edges since v1.8.0 [source](./references/releases/v1.8.0.md)

- NEW: `useScroll` VueInstance support — `container` and `target` options now accept `VueInstance` (ref to component) since v1.6.0 [source](./references/releases/v1.6.0.md)

- NEW: `useInView` `root` option — now accepts `MaybeRef` for dynamic root element assignment since v1.6.0 [source](./references/releases/v1.6.0.md)

- NEW: `AnimatePresence` direct children — supports multiple direct `motion` components as children since v1.10.0 [source](./references/releases/v1.10.0.md)

- NEW: `delayInMs` — exported as a standalone utility function for time-based animation delays since v1.6.0 [source](./references/releases/v1.6.0.md)

**Also changed:** `useTransform` reactive update fix (v1.2.1) · `sequence` at relative start (v1.3.0) · `AnimatePresence` custom prop fix (v1.3.0) · `motionGlobalConfig` exported (v2.0.0-beta.1) · `FeatureBundle` tree-shaking architecture (v2.0.0-beta.1)

## Best Practices

- Create motion-supercharged components using `motion.create()` outside of the template to avoid re-creating the component on every render, which would break animations [source](./references/docs/docs/vue-motion-component.md)

```ts
// Preferred
const MotionComponent = motion.create(Component)

// Avoid - re-created every render
<component :is="motion.create(Component)" />
```

- Use `MotionValue`s in the `style` prop to animate values outside of the Vue render cycle, significantly improving performance by avoiding frequent re-renders [source](./references/docs/docs/vue-motion-component.md)

```vue
<script setup>
const x = useMotionValue(0)
</script>

<template>
  <motion.div :style="{ x }" />
</template>
```

- Reduce initial bundle size from ~34kb to ~6kb by using the `m` component paired with `LazyMotion` to load features synchronously or asynchronously only when needed [source](./references/docs/docs/vue-lazymotion.md)

```vue
<template>
  <LazyMotion :features="domAnimation">
    <m.div :animate="{ opacity: 1 }" />
  </LazyMotion>
</template>
```

- Enable the `strict` prop on `LazyMotion` during development to catch accidental usage of the full `motion` component, which would negate the bundle size benefits of lazy loading [source](./references/docs/docs/vue-lazymotion.md)

- Centralize animation settings like global transitions and site-wide `reducedMotion` policies using `MotionConfig` to ensure consistent behavior across all child components [source](./references/docs/docs/vue-motion-config.md)

- (experimental) Apply declarative animations directly to any standard HTML/SVG element using the `v-motion` directive in v2.0.0-beta.1+ without needing to wrap elements in a `<motion>` component [source](./references/releases/v2.0.0-beta.1.md)

- Ensure `AnimatePresence` children have unique, stable `key` props and are direct children of the component to correctly track their removal for exit animations [source](./references/docs/docs/vue-animate-presence.md)

- Synchronize layout animations across unrelated components (those that don't share a parent-child relationship but affect each other's layout) by wrapping them in a `LayoutGroup` [source](./references/docs/docs/vue-layout-animations.md)

- Prevent visual distortion of child elements during parent layout animations by applying the `layout` prop to the immediate children as well, enabling scale correction [source](./references/docs/docs/vue-layout-animations.md)

- Mark scrollable ancestors with `layoutScroll` and fixed-position ancestors with `layoutRoot` to ensure Motion correctly accounts for scroll offsets during layout measurements [source](./references/docs/docs/vue-layout-animations.md)

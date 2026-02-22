---
name: tresjs-core-skilld
description: "ALWAYS use when writing code importing \"@tresjs/core\". Consult for debugging, best practices, or modifying @tresjs/core, tresjs/core, tresjs core, tres."
metadata:
  version: 5.5.0
  generated_by: Gemini CLI · Gemini 3 Flash
---

# Tresjs/tres `@tresjs/core`

**Version:** 5.5.0 (Feb 2026)
**Deps:** @pmndrs/pointer-events@^6.6.17, @vue/devtools-api@^7.7.2, @vueuse/core@^13.9.0, radashi@^12.6.2
**Tags:** beta: 2.0.0-beta.13 (Apr 2023), next: 5.0.0-next.6 (Jun 2025), alpha: 5.0.0-alpha.2 (Sep 2025), rc: 5.0.0-rc.0 (Sep 2025), latest: 5.5.0 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `useLoader` — returns reactive state `{ state, isLoading, error, progress }` since v5, no longer returns a Promise [source](./references/docs/content/1.getting-started/4.upgrade-guide.md)

- BREAKING: Pointer Events — renamed to native DOM names (e.g., `@pointerdown` instead of `@pointer-down`) in v5 [source](./references/docs/content/1.getting-started/4.upgrade-guide.md)

- BREAKING: `useTexture` — removed from core in v5, moved to `@tresjs/cientos` package [source](./references/docs/content/1.getting-started/4.upgrade-guide.md)

- BREAKING: ESM-only — TresJS v5 is ESM-only; UMD build and CommonJS `require()` are no longer supported [source](./references/docs/content/1.getting-started/4.upgrade-guide.md)

- BREAKING: `TresCanvas` Props — WebGL context props like `alpha`, `antialias`, `stencil`, and `depth` are now readonly and non-reactive in v5 [source](./references/docs/content/1.getting-started/4.upgrade-guide.md)

- BREAKING: `useTresContext().camera` — returns a state object in v5; use `useTres().camera` for the active camera instance [source](./references/docs/content/1.getting-started/4.upgrade-guide.md)

- BREAKING: Renderer Context — `renderer` is now readonly in `useTresContext()`; `performance` state was removed from context in v5 [source](./references/docs/content/1.getting-started/4.upgrade-guide.md)

- BREAKING: Event Bubbling — only the first intersected element triggers pointer events since v5 to align with standard behavior [source](./references/docs/content/1.getting-started/4.upgrade-guide.md)

- NEW: `Context` Component — exported in v5.5.0 (as `TresCanvasContext`) for advanced scene and state management [source](./references/releases/@tresjs/core@5.5.0.md)

- NEW: Kebab-case Support — support for components written in kebab-case (e.g., `<tres-mesh>`) added in v5.1.0 [source](./references/releases/@tresjs/core@5.1.0.md)

- NEW: `primitive` Prefix — added `prefix` option for primitives in v5.3.0 to avoid name collisions [source](./references/releases/@tresjs/core@5.3.0.md)

- NEW: `TresCanvasProps` / `TresCanvasEmits` — explicitly exported types added in v5.2.0 for better TypeScript integration [source](./references/releases/@tresjs/core@5.2.0.md)

- REMOVED: Legacy Composables — `useRenderLoop`, `useCamera`, `useTresReady`, `useSeek`, `useRaycaster`, and `useLogger` removed in v5 [source](./references/docs/content/1.getting-started/4.upgrade-guide.md)

- NEW: `useForwardPropsEmits` — integrated into `TresCanvas` in v5.3.0 for streamlined event and prop handling [source](./references/releases/@tresjs/core@5.3.0.md)

**Also changed:** `useLoop` replaces `useRenderLoop` · `useGraph` replaces `useSeek` · `@ready` event replaces `useTresReady` · `useTres()` replaces common `useTresContext()` usage · `TresCanvas` supports `useLegacyLights` prop (deprecated) · `useLoader` supports `extensions` and reactive paths.

## Best Practices

- Use `shallowRef` with template refs to access Three.js instances directly in high-frequency render loops. This avoids Vue's deep proxy overhead, which can be significantly slower than direct property access [source](./references/docs/content/2.essentials/2.concepts/2.reactivity.md)

```vue
<script setup lang="ts">
const meshRef = shallowRef<TresInstance | null>(null)
const { onBeforeRender } = useLoop()

onBeforeRender(({ elapsed }) => {
  if (meshRef.value) meshRef.value.rotation.y = elapsed
})
</script>

<template>
  <TresMesh ref="meshRef" />
</template>
```

- Prefer `shallowRef` and `shallowReactive` over `ref` or `reactive` for Three.js objects. This maintains reactivity for the reference itself while preventing expensive deep tracking of complex internal Three.js properties [source](./references/docs/content/3.api/5.advanced/performance.md)

- Set `renderMode="on-demand"` on `<TresCanvas>` for non-game applications to reduce CPU/GPU usage. The scene will only re-render when props change or when manual invalidation is explicitly triggered [source](./references/docs/content/3.api/5.advanced/performance.md)

- Manually trigger a render using `invalidate()` from `useLoop` or `useTres` when modifying instances via template refs or direct mutations in `on-demand` mode, as these changes are invisible to Vue's reactivity system [source](./references/docs/content/3.api/5.advanced/performance.md)

- Ensure animations are frame-rate independent by using the `delta` parameter in `useLoop` callbacks. This guarantees consistent movement speed across different display refresh rates (e.g., 60Hz vs 144Hz) [source](./references/docs/content/3.api/2.composables/3.use-loop.md)

```ts
onBeforeRender(({ delta }) => {
  // Moves 2 units per second regardless of frame rate
  mesh.position.x += delta * 2
})
```

- Use the `args` prop for values required at Three.js instantiation (like geometry dimensions). Note that changing these reactive values at runtime forces TresJS to recreate the entire instance, which is performance-heavy [source](./references/docs/content/2.essentials/2.concepts/3.constructor-arguments.md)

- Take complete control of the render process using `render` from `useLoop` for custom post-processing or multi-pass setups. You must call `notifySuccess()` at the end of the function to maintain the loop state [source](./references/docs/content/3.api/2.composables/3.use-loop.md)

- Orchestrate complex update sequences using the `priority` argument in `onBeforeRender` (default 0). Higher priority numbers ensure a callback runs after those with lower priorities within the same frame [source](./references/docs/content/3.api/2.composables/3.use-loop.md)

- Explicitly call `dispose()` from `@tresjs/core` for Three.js objects created programmatically and used via `<primitive />`. TresJS automatically disposes of template-defined components but cannot track lifecycle for raw objects [source](./references/docs/content/3.api/5.advanced/performance.md)

- Use `useGraph` to generate a reactive map of named meshes, materials, and nodes from a complex hierarchy (like a loaded GLTF). This enables direct, named access without manually traversing the object tree [source](./references/docs/content/3.api/2.composables/4.use-graph.md)

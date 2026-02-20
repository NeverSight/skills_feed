---
name: shadcn-vue-skilld
description: "ALWAYS use when writing code importing \"shadcn-vue\". Consult for debugging, best practices, or modifying shadcn-vue, shadcn vue."
metadata:
  version: 2.4.3
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# unovue/shadcn-vue `shadcn-vue`

**Version:** 2.4.3 (Dec 2025)
**Deps:** @dotenvx/dotenvx@^1.51.1, @modelcontextprotocol/sdk@^1.24.3, @unovue/detypes@^0.8.5, @vue/compiler-sfc@^3.5, c12@^3.3.2, commander@^14.0.2, consola@^3.4.2, dedent@^1.7.0, deepmerge@^4.3.1, diff@^8.0.2, fs-extra@^11.3.2, fuzzysort@^3.1.0, get-tsconfig@^4.13.0, magic-string@^0.30.21, nypm@^0.6.2, ofetch@^1.5.1, ora@^9.0.0, pathe@^2.0.3, postcss@^8.5.6, prompts@^2.4.2, reka-ui@^2.6.1, semver@^7.7.3, stringify-object@^6.0.0, tailwindcss@^4.1.17, tinyexec@^1.0.2, tinyglobby@^0.2.15, ts-morph@^27.0.2, undici@^7.16.0, vue-metamorph@^3.3.3, zod@^3.25.76, zod-to-json-schema@^3.25.0
**Tags:** radix: 0.11.4 (Feb 2025), latest: 2.4.3 (Dec 2025)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `Separator` label props removed — labels in `Separator` are no longer supported in Tailwind v3 configurations since v2.2.0 [source](./references/releases/v2.2.0.md)

- BREAKING: `vue-sonner` v2 update — requires manual update of `Toaster` component for compatibility with the latest version [source](./references/releases/v2.2.0.md)

- BREAKING: HSL colors converted to OKLCH — default color space changed to OKLCH in v2.0.0, affecting custom CSS variable logic [source](./references/docs/.tailwind-v4.md)

- BREAKING: `NavigationMenuLink` state change — now uses `data-active` instead of previous state indicators to match `reka-ui` [source](./references/releases/v2.4.0.md)

- BREAKING: `Chart` `showGradient` prop — corrected typo in prop name from `showGradiant` to `showGradient` in v2.3.0 [source](./references/releases/v2.3.0.md)

- DEPRECATED: `toast` component — officially deprecated in favor of `sonner`; current `toast` implementations should be migrated [source](./references/docs/.tailwind-v4.md)

- DEPRECATED: `default` style — phased out in v2.0.0; new projects are initialized with `new-york` by default [source](./references/docs/.tailwind-v4.md)

- NEW: Tailwind v4 support — introduces full integration with the Tailwind v4 engine and `@theme` directive [source](./references/releases/v2.0.0.md)

- NEW: `NativeSelect` `modelValue` — provides native `v-model` support for the `NativeSelect` component [source](./references/releases/v2.4.0.md)

- NEW: `Kbd` component — keyboard key display component for shortcuts and UI documentation [source](./references/releases/v2.3.0.md)

- NEW: `Button-group` component — new layout component specifically for grouping related button actions [source](./references/releases/v2.3.0.md)

- NEW: `Spinner` component — added dedicated loading spinner component to the registry [source](./references/releases/v2.3.0.md)

- NEW: `PinInput` generic types — enhanced type safety for `PinInput` allowing custom value types [source](./references/releases/v2.3.0.md)

- NEW: `data-slot` attributes — added to all primitives to simplify granular styling in complex components [source](./references/docs/.tailwind-v4.md)

**Also changed:** `Stepper` slot props binding fix · `Sidebar` cookie state · `size-*` utility support · `phosphor` and `tabler` icon support

## Best Practices

- Prefer CSS variables over utility classes for theming to enable dynamic runtime adjustments and easier maintenance of complex color schemes [source](./references/docs/04.theming.md)

- Omit the `background` suffix when using variables for background colors in utility classes; for example, `bg-primary` automatically maps to the `--primary` variable [source](./references/docs/04.theming.md)

- Build sidebars by composing sub-components (`SidebarProvider`, `SidebarContent`, `SidebarGroup`, etc.) rather than a single monolithic component to maintain flexibility and customization [source](./references/docs/components/sidebar.md)

- Avoid the legacy `Form` component; use `VeeValidate` or `TanStack Form` integrations for more robust, actively maintained form handling and validation patterns [source](./references/docs/_INDEX.md)

- Utilize the `valueUpdater` helper when managing TanStack Table state in Vue to correctly handle both direct value assignments and functional state transformations [source](./references/docs/components/data-table.md)

```ts
export function valueUpdater<T extends Updater<any>>(updaterOrValue: T, ref: Ref) {
  ref.value = typeof updaterOrValue === 'function'
    ? updaterOrValue(ref.value)
    : updaterOrValue
}
```

- Enable automatic sidebar state persistence across page reloads by providing a `storageKey` prop to the `SidebarProvider` component [source](./references/docs/components/sidebar.md)

- Leverage the default `cmd+b` or `ctrl+b` keyboard shortcuts provided by `SidebarProvider` to toggle sidebar visibility without manual event listeners [source](./references/docs/components/sidebar.md)

- Treat the code in `Sidebar*.vue` (and other added UI components) as your own project code; you are explicitly encouraged to modify the source to suit specific design needs [source](./references/docs/components/sidebar.md)

- Build custom data tables from headless primitives and the basic `<Table />` component instead of looking for a pre-built, configuration-heavy "DataTable" component [source](./references/docs/components/data-table.md)

- (experimental) Use the `build` command and `registry.json` schema to create and share your own custom component registries for internal or community use [source](./references/docs/registry/index.md)

---
name: vuetify-skilld
description: "ALWAYS use when writing code importing \"vuetify\". Consult for debugging, best practices, or modifying vuetify."
metadata:
  version: 4.0.0-beta.2
  generated_by: Gemini CLI · Gemini 3 Flash
---

# vuetifyjs/vuetify `vuetify`

**Version:** 4.0.0-beta.2 (Feb 2026)
**Tags:** v1-stable: 1.5.24 (Mar 2020), v2-stable: 2.7.2 (Feb 2024), dev: 3.11.0 (Nov 2025), latest: 3.11.8 (Jan 2026), next: 4.0.0-beta.2 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `VRow` / `VCol` Grid — complete overhaul using CSS `gap` instead of negative margins. `dense` prop removed (use `density="compact"`), `align`/`justify` on `VRow` and `order`/`align-self` on `VCol` removed in favor of utility classes [source](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING: MD3 Typography — variant names renamed for Material Design 3 compliance: `h1`-`h3` -> `display-*`, `h4`-`h6` -> `headline-*`, `subtitle-1`/`body-1` -> `body-large`, `button`/`subtitle-2` -> `label-large` [source](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING: MD3 Elevation — elevation levels reduced from 25 (0-24) to 6 (0-5) to align with MD3 density-independent pixel levels [source](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING: `VBtn` Defaults — `text-transform: uppercase` removed by default. `$button-stacked-icon-margin` Sass variable replaced by `$button-stacked-gap` [source](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING: `VSelect` / `VAutocomplete` / `VCombobox` — `item` slot prop renamed to `internalItem`. The `item` prop is now an alias for `internalItem.raw` [source](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING: `VForm` Slot — `isValid`, `errors`, and `isDisabled` slot variables are now unwrapped values instead of `Ref` objects [source](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- NEW: `VSnackbarQueue` — rewritten in v4 to support showing multiple snackbars simultaneously; `default` slot renamed to `item` [source](./references/releases/v4.0.0-beta.2.md)

- NEW: `VRow` `gap` prop — provides fine-grained control over grid spacing, accepting numbers, strings, or `[x, y]` arrays [source](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- NEW: `VAvatarGroup` (experimental) — new labs component for grouping multiple avatars with overlapping support [source](./references/releases/v4.0.0-beta.2.md)

- NEW: `VCommandPalette` (experimental) — new labs component providing a search and action interface for application commands [source](./references/releases/v4.0.0-beta.0.md)

**Also changed:** `VCalendar` promoted from labs · `VHotkey` promoted from labs · `VToolbar` `location` prop new · `VAvatar` `badge` prop new · `VProgressCircular` `reveal` prop new · `VTreeview` `indent-lines` props new · `vuetify/styles/core` new entry point · `system` default theme · `VSnackbar` `multi-line` removed · `VContainer` `fill-height` behavior changed

## Best Practices

- Use the `cmd` modifier in the `useHotkey` composable for cross-platform compatibility — automatically resolves to Command on Mac and Control on PC [source](./references/docs/src/pages/en/features/hotkey.md)

```ts
// Preferred: works on both Mac and PC
useHotkey('cmd+s', (e) => saveDocument(e))

// Avoid: hardcoding 'ctrl' may cause conflicts or feel non-idiomatic on Mac
useHotkey('ctrl+s', (e) => saveDocument(e))
```

- Apply `class` and `style` to specific component keys in the `defaults` configuration — these are not supported in the `global` defaults key [source](./references/docs/src/pages/en/features/global-configuration.md)

```ts
// Preferred
createVuetify({
  defaults: {
    VBtn: {
      class: 'text-none',
      style: { textTransform: 'none' }
    }
  }
})

// Avoid: class and style are ignored in global
createVuetify({
  defaults: {
    global: { class: 'text-none' }
  }
})
```

- Resolve style conflicts between Vuetify and TailwindCSS by redefining CSS layer order — place Vuetify's styles in a dedicated layer with lower precedence than Tailwind's base layer [source](./references/discussions/discussion-21241.md)

```css
/* main.css */
@layer theme, base, vuetify, components, utilities;
@import 'vuetify/styles' layer(vuetify);
@import 'tailwindcss';
```

- Use `v-text-field` with `decimal.js` for high-precision decimal arithmetic — `VNumberInput` uses `toFixed()` internally and may suffer from standard JavaScript floating-point inaccuracies [source](./references/docs/src/pages/en/components/number-inputs.md)

- Centralize snackbar messages using global state (e.g., Pinia) with `v-snackbar-queue` — allows triggering notifications from any part of the application by pushing to a shared array [source](./references/docs/src/pages/en/components/snackbar-queue.md)

```vue

<template>
  <v-app>
    <v-snackbar-queue v-model="messages.queue" />
  </v-app>
</template>
```

- Use the `order` prop to explicitly control layout component priority — overrides the default behavior where priority is determined solely by markup order [source](./references/docs/src/pages/en/features/application-layout.md)

```vue

<v-navigation-drawer />
<v-app-bar :order="-1" />
```

- Utilize `useDate()`'s `parseISO` and `toISO` methods for standardizing date strings — `VDateInput` and other date components internally expect and return native JS `Date` objects [source](./references/docs/src/pages/en/components/date-inputs.md)

- Use `v-command-palette` (experimental) for keyboard-driven power-user workflows — provides a pre-configured, accessible, and searchable dialog interface that implements ARIA best practices automatically [source](./references/docs/src/pages/en/components/command-palettes.md)

- Restore previous negative-margin/padding grid behavior during Vuetify 4 migration using the `@layer vuetify-overrides` block — necessary when existing layouts rely on the legacy system instead of the new CSS `gap` property [source](./references/docs/src/pages/en/getting-started/grid-legacy-mode.md)

```scss
@layer vuetify-overrides {
  .v-row {
    gap: unset;
    margin: calc(var(--v-col-gap-y) * -.5) calc(var(--v-col-gap-x) * -.5);
  }
}
```

---
name: reka-ui-skilld
description: "ALWAYS use when writing code importing \"reka-ui\". Consult for debugging, best practices, or modifying reka-ui, reka ui."
metadata:
  version: 2.8.0
  generated_by: Gemini CLI · Gemini 3 Flash
---

# unovue/reka-ui `reka-ui`

**Version:** 2.8.0 (Jan 2026)
**Deps:** @floating-ui/dom@^1.6.13, @floating-ui/vue@^1.1.6, @internationalized/date@^3.5.0, @internationalized/number@^3.5.0, @tanstack/vue-virtual@^3.12.0, @vueuse/core@^14.1.0, @vueuse/shared@^14.1.0, aria-hidden@^1.2.4, defu@^6.1.4, ohash@^2.0.11
**Tags:** latest: 2.8.0 (Jan 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `radix-vue` renamed to `reka-ui` — CSS variables now use `--reka-` prefix and data attributes use `data-reka-` [source](./references/docs/content/docs/guides/migration.md)

- BREAKING: `Combobox` refactor — `filter-function` prop removed; `searchTerm` and `displayValue` props moved from Root to `ComboboxInput` [source](./references/docs/content/docs/guides/migration.md)

- BREAKING: `Checkbox`, `Toggle`, `MenuCheckboxItem` — bindings changed from `v-model:checked` or `v-model:pressed` to standard `v-model` [source](./references/docs/content/docs/guides/migration.md)

- BREAKING: `DatePicker/Calendar` — `weekStartsOn` is now locale-independent as of v2.8.0 [source](./references/releases/v2.8.0.md)

- BREAKING: `Presence` — `forceMount` now renders components regardless of active state; manual visibility handling (e.g. `:hidden`) is required [source](./references/docs/content/docs/guides/migration.md)

- BREAKING: `Pagination` — `itemsPerPage` prop is now required rather than having a default value [source](./references/docs/content/docs/guides/migration.md)

- NEW: `Rating` component — added for star/rating input interactions in v2.8.0 [source](./references/releases/v2.8.0.md)

- NEW: `TimeField` component — new primitive for localized time inputs introduced in v2.0.0 [source](./references/releases/v2.0.0.md)

- NEW: `useFilter()` — locale-aware string filtering utility (startsWith, endsWith, contains) added in v2.0.0 [source](./references/releases/v2.0.0.md)

- NEW: `useLocale()` / `useDirection()` — utility hooks for accessing the current configuration context [source](./references/releases/v2.6.0.md)

- NEW: `ScrollArea` glimpse mode — added `ScrollAreaScrollbarGlimpse` for transient scrollbar visibility [source](./references/releases/v2.8.0.md)

- NEW: `Select` `disableOutsidePointerEvents` — prop added to `SelectContent` to control interaction with outside elements [source](./references/releases/v2.7.0.md)

- NEW: `ConfigProvider` — global configuration component for locale, direction, and `useId` settings [source](./references/releases/v2.0.0.md)

- NEW: `NumberField` enhancements — added `focusOnChange`, `readonly`, and `stepSnapping` props [source](./references/releases/v2.8.0.md)

**Also changed:** `Popover/Dialog` programmatic close · `Combobox` `openOnFocus` props · `Slider` `thumbAlignment` prop · `Toast` `disableSwipe` prop · `ContextMenu` `pressOpenDelay` prop · `Presence` component exposed · `calendar` `getWeekNumber` utility · `injectContext` exposed · `Collapsible/Accordion` `unmountOnHide` prop

## Best Practices

- Use the `asChild` prop to compose Reka's functionality onto your own Vue components or alternative DOM elements while maintaining accessibility [source](./references/docs/content/docs/guides/composition.md)

```vue

<TooltipTrigger asChild>
  <MyButton>Hover me</MyButton>
</TooltipTrigger>
```

- Utilize `useForwardPropsEmits` when building wrapper components to automatically forward all props and emits to the underlying Reka primitive [source](./references/docs/content/docs/utilities/use-forward-props-emits.md)

```ts
const props = defineProps<AccordionRootProps>()
const emits = defineEmits<AccordionRootEmits>()
const forwarded = useForwardPropsEmits(props, emits)
// Usage: <AccordionRoot v-bind="forwarded">
```

- Wrap your application with `ConfigProvider` to manage global reading direction (RTL) and prevent layout shifts during scroll locking [source](./references/docs/content/docs/utilities/config-provider.md)

```vue
<ConfigProvider dir="rtl" :scroll-body="false">
  <App />
</ConfigProvider>
```

- Apply `useForwardExpose` in components with multiple root nodes (fragments) to ensure that template refs correctly return the target DOM element [source](./references/docs/content/docs/utilities/use-forward-expose.md)

```ts
const { forwardRef } = useForwardExpose()
// Usage: <div :ref="forwardRef">...</div>
```

- Implement `ComboboxVirtualizer` or `ListboxVirtualizer` for large datasets to improve performance, ensuring the parent container has a fixed height [source](./references/docs/content/docs/guides/virtualization.md)

```vue
<ComboboxViewport class="max-h-80 overflow-y-auto">
  <ComboboxVirtualizer :options="items" :estimate-size="25" v-slot="{ option }">
    <ComboboxItem :value="option">{{ option.label }}</ComboboxItem>
  </ComboboxVirtualizer>
</ComboboxViewport>
```

- Use `injectXContext` functions (e.g., `injectAccordionRootContext`) to access internal primitive state for advanced custom child components [source](./references/docs/content/docs/guides/inject-context.md)

- Style component states by targeting `data-state` attributes (e.g., `open`, `closed`, `active`) instead of manually toggling classes [source](./references/docs/content/docs/guides/styling.md)

```css
/* Preferred way to style open state */
.AccordionItem[data-state="open"] {
  border-bottom-width: 2px;
}
```

- Use the `:deep()` selector when styling teleported components (Dialog, Popover, Tooltip) within scoped Vue styles to reach the body-appended elements [source](./references/docs/content/docs/guides/styling.md)

- Enable `force-mount` on content parts when using JavaScript animation libraries or Vue `<Transition>` to delegate unmounting control to the library [source](./references/docs/content/docs/guides/animation.md)

```vue
<Transition name="fade">
  <DialogContent force-mount>...</DialogContent>
</Transition>
```

- Prefer Vue 3.5 native `useId()` over the Reka UI utility for stable SSR identifiers, as the library utility is deprecated for newer Vue versions [source](./references/docs/content/docs/utilities/use-id.md)

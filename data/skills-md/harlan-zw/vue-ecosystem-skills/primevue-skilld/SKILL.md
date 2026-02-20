---
name: primevue-skilld
description: "ALWAYS use when writing code importing \"primevue\". Consult for debugging, best practices, or modifying primevue."
metadata:
  version: 4.5.4
  generated_by: Gemini CLI · Gemini 3 Flash
---

# primefaces/primevue `primevue`

**Version:** 4.5.4 (Dec 2025)
**Deps:** @primeuix/styled@^0.7.4, @primeuix/utils@^0.6.2, @primeuix/styles@^2.0.2, @primevue/core@4.5.4, @primevue/icons@4.5.4
**Tags:** v2-stable: 2.10.4 (Dec 2023), v3-stable: 3.53.1 (Dec 2024), latest: 4.5.4 (Dec 2025)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `Calendar` renamed to `DatePicker` — v3 component renamed to `DatePicker` in v4 [source](./references/releases/CHANGELOG.md)

- BREAKING: `Dropdown` renamed to `Select` — v3 component renamed to `Select` in v4 [source](./references/releases/CHANGELOG.md)

- BREAKING: `Sidebar` renamed to `Drawer` — v3 component renamed to `Drawer` in v4 [source](./references/releases/CHANGELOG.md)

- BREAKING: `OverlayPanel` renamed to `Popover` — v3 component renamed to `Popover` in v4 [source](./references/releases/CHANGELOG.md)

- BREAKING: `InputSwitch` renamed to `ToggleSwitch` — v3 component renamed to `ToggleSwitch` in v4 [source](./references/releases/CHANGELOG.md)

- BREAKING: `TabView` replaced by `Tabs` — new component structure using `TabList`, `Tab`, `TabPanels`, and `TabPanel` [source](./references/docs/tabs.md)

- BREAKING: `Steps` replaced by `Stepper` — new component structure using `StepList`, `Step`, `StepPanels`, and `StepPanel` [source](./references/docs/stepper.md)

- BREAKING: `Accordion` reimplementation — now uses `AccordionPanel`, `AccordionHeader`, and `AccordionContent` components [source](./references/docs/accordion.md)

- BREAKING: `v-model:value` — v4 uses `v-model:value` for active state in `Tabs`, `Accordion`, and `Stepper` instead of `v-model` [source](./references/docs/tabs.md)

- DEPRECATED: `inputStyle` — property replaced by `inputVariant` (values: 'filled' | 'outlined') [source](./references/releases/CHANGELOG.md)

- NEW: `@primevue/forms` — new dedicated package for advanced form management and validation [source](./references/releases/CHANGELOG.md)

- NEW: `Fluid` component — layout component that makes descendants span full width [source](./references/docs/fluid.md)

- NEW: `IconField` & `InputIcon` — new components to wrap inputs and icons for decorative purposes [source](./references/docs/iconfield.md)

- NEW: `useId` & `useAttrSelector` — new core composables for unique ID generation and attribute selectors [source](./references/releases/CHANGELOG.md)

**Also changed:** `DataTable` `showClearButton` default is `false` (v4.3.0) · `IftaLabel` new component for in-field labels · `Checkbox` added `indeterminate` state · `OverlayBadge` new component replaces `Badge` directive · `InlineMessage` component deprecated · `iconPosition` removed from `IconField` · `warning` property renamed to `warn` · `Drawer` added `before-hide` emit (v4.3.0)

## Best Practices

- Use the `Fluid` component as a wrapper for bulk application of full-width styles to inputs instead of adding the `fluid` prop to every individual field for cleaner and more maintainable templates [source](./references/docs/fluid.md)

```vue
<Fluid>
    <div class="grid grid-cols-2 gap-4">
        <InputText placeholder="Full Width" />
        <DatePicker placeholder="Full Width" />
        <Select placeholder="Full Width" />
    </div>
</Fluid>
```

- In Stepper vertical layouts, always wrap `Step` and `StepPanel` inside a `StepItem` component to ensure correct structure and connection between headers and content [source](./references/docs/stepper.md)

- Use `asChild` and `v-slot` on components like `Step` or `Tab` to implement headless mode for full UI control while retaining PrimeVue's built-in accessibility logic [source](./references/docs/stepper.md)

```vue
<Step v-slot="{ activateCallback, value, a11yAttrs }" asChild :value="1">
    <button @click="activateCallback" v-bind="a11yAttrs.header">
        Step {{ value }}
    </button>
</Step>
```

- For performant row expansion in `DataTable` with large datasets, use an object for `expandedRows` combined with `dataKey` instead of an array of row objects [source](./references/docs/datatable.md)

```ts
// Preferred (O(1) lookup)
const expandedRows = ref({ '1004': true, '1005': true });

// In template
<DataTable v-model:expandedRows="expandedRows" dataKey="id">
```

- Enable automatic user preference persistence (sorting, filtering, paging) in `DataTable` using `stateStorage` and `stateKey` to improve UX across page visits [source](./references/docs/datatable.md)

- Add a `delay` to `VirtualScroller` to throttle rendering during rapid scrolling, significantly improving UI responsiveness for extremely large lists [source](./references/docs/virtualscroller.md)

```vue
<VirtualScroller :items="items" :itemSize="50" :delay="250">
    <template v-slot:item="{ item }">{{ item }}</template>
</VirtualScroller>
```

- Implement semantic navigation menus by using `Tabs` without `TabPanels` and combining it with `router-link` for accessible, state-aware top or side bars [source](./references/docs/tabs.md)

- Always wrap inputs and icons with `IconField` and `InputIcon` to ensure correct positioning and styling, supporting both leading and trailing icon placements [source](./references/docs/iconfield.md)

```vue
<IconField>
    <InputIcon class="pi pi-search" />
    <InputText placeholder="Search" />
</IconField>
```

- Use `IftaLabel` for modern, top-aligned in-field labels that visually integrate with the input and handle validation states automatically [source](./references/docs/iftalabel.md)

- Leverage the built-in `DataTable` context menu integration to provide row-specific actions without manual event listener management or custom positioning logic [source](./references/docs/datatable.md)

```vue
<ContextMenu ref="cm" :model="menuModel" />
<DataTable :value="products" contextMenu @row-contextmenu="onRowContextMenu">
```

---
name: vue-test-utils-skilld
description: "ALWAYS use when writing code importing \"@vue/test-utils\". Consult for debugging, best practices, or modifying @vue/test-utils, vue/test-utils, vue test-utils, vue test utils, test-utils, test utils."
metadata:
  version: 2.4.6
  generated_by: Gemini CLI · Gemini 3 Flash
---

# vuejs/test-utils `@vue/test-utils`

**Version:** 2.4.6 (May 2024)
**Deps:** js-beautify@^1.14.9, vue-component-type-helpers@^2.0.0
**Tags:** latest: 2.4.6 (May 2024), 2.0.0-alpha.0: 2.0.0-alpha.0 (Apr 2020), 2.0.0-alpha.1: 2.0.0-alpha.1 (Apr 2020), 2.0.0-alpha.2: 2.0.0-alpha.2 (Apr 2020), 2.0.0-alpha.3: 2.0.0-alpha.3 (Apr 2020), 2.0.0-alpha.4: 2.0.0-alpha.4 (May 2020), next: 2.4.0-alpha.2 (Jun 2023), 2.0.0-alpha.8: 2.0.0-alpha.8 (Jul 2020), 2.0.0-beta.1: 2.0.0-beta.1 (Aug 2020), 2.0.0-beta.2: 2.0.0-beta.2 (Aug 2020), 2.0.0-beta.3: 2.0.0-beta.3 (Aug 2020), 2.0.0-beta.4: 2.0.0-beta.4 (Sep 2020), 2.0.0-beta.5: 2.0.0-beta.5 (Sep 2020), 2.0.0-beta.7: 2.0.0-beta.7 (Oct 2020), 2.0.0-beta.8: 2.0.0-beta.8 (Nov 2020), 2.0.0-beta.9: 2.0.0-beta.9 (Nov 2020), 2.0.0-beta.10: 2.0.0-beta.10 (Nov 2020), 2.0.0-beta.12: 2.0.0-beta.12 (Dec 2020), 2.0.0-beta.13: 2.0.0-beta.13 (Dec 2020), 2.0.0-rc.0: 2.0.0-rc.0 (Jan 2021), 2.0.0-rc.1: 2.0.0-rc.1 (Feb 2021), 2.0.0-rc.2: 2.0.0-rc.2 (Feb 2021), 2.0.0-rc.3: 2.0.0-rc.3 (Mar 2021), 2.0.0-rc.4: 2.0.0-rc.4 (Mar 2021), 2.0.0-rc.5: 2.0.0-rc.5 (Apr 2021), 2.0.0-rc.6: 2.0.0-rc.6 (Apr 2021), 2.0.0-rc.7: 2.0.0-rc.7 (Jun 2021), 2.0.0-rc.8: 2.0.0-rc.8 (Jun 2021), 2.0.0-rc.9: 2.0.0-rc.9 (Jun 2021), 2.0.0-rc.10: 2.0.0-rc.10 (Jul 2021), 2.0.0-rc.11: 2.0.0-rc.11 (Jul 2021), 2.0.0-rc.12: 2.0.0-rc.12 (Jul 2021), 2.0.0-rc.14: 2.0.0-rc.14 (Sep 2021), 2.0.0-rc.16: 2.0.0-rc.16 (Oct 2021), 2.0.0-rc.18: 2.0.0-rc.18 (Dec 2021), legacy: 1.3.6 (Jun 2023), 2.4.0-alpha.0: 2.4.0-alpha.0 (Apr 2023), v2.4.0-alpha.2: 2.4.0-alpha.2 (Jun 2023)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `propsData` — v2 renamed to `props` for consistency with component definitions [source](./references/docs/migration/index.md)

- BREAKING: `createLocalVue` — removed in v2, use the `global` mounting option to install plugins, mixins, or directives [source](./references/docs/migration/index.md)

- BREAKING: `mocks` and `stubs` — moved into the `global` mounting option in v2 as they apply to all components [source](./references/docs/migration/index.md)

- BREAKING: `destroy()` — renamed to `unmount()` in v2 to match Vue 3 lifecycle naming [source](./references/docs/migration/index.md)

- BREAKING: `findAll().at()` — removed in v2; `findAll()` now returns a standard array of wrappers [source](./references/docs/migration/index.md)

- BREAKING: `createWrapper()` — removed in v2, use the `new DOMWrapper()` constructor for non-component elements [source](./references/docs/migration/index.md)

- BREAKING: `shallowMount` — v2 no longer renders default slot content for stubbed components by default [source](./references/docs/migration/index.md)

- BREAKING: `find()` — now only supports `querySelector` syntax; use `findComponent()` to locate Vue components [source](./references/docs/migration/index.md)

- BREAKING: `setSelected` and `setChecked` — removed in v2, functionality merged into `setValue()` [source](./references/docs/migration/index.md)

- BREAKING: `attachToDocument` — renamed to `attachTo` in v2 [source](./references/docs/migration/index.md)

- BREAKING: `emittedByOrder` — removed in v2, use `emitted()` instead [source](./references/docs/migration/index.md)

- NEW: `renderToString()` — added in v2.3.0 to support SSR testing [source](./references/releases/v2.3.0.md)

- NEW: `enableAutoUnmount()` / `disableAutoUnmount()` — replaces `enableAutoDestroy` in v2 [source](./references/docs/migration/index.md)

- DEPRECATED: `scopedSlots` — removed in v2 and merged into the `slots` mounting option [source](./references/docs/migration/index.md)

**Also changed:** `setValue()` and `trigger()` return `nextTick` · `slots` scope exposed as `params` in string templates · `is`, `isEmpty`, `isVueInstance`, `name`, `setMethods`, and `contains` removed

## Best Practices

- Always `await` methods that return `nextTick` (`trigger`, `setValue`, `setProps`, `setData`) to ensure DOM updates are processed before running assertions [source](./references/docs/guide/advanced/async-suspense.md)

```ts
// Preferred
await wrapper.find('button').trigger('click')
expect(wrapper.text()).toContain('Count: 1')

// Avoid — assertion runs before DOM update
wrapper.find('button').trigger('click')
expect(wrapper.text()).toContain('Count: 1')
```

- Prefer `get()` and `getComponent()` over `find()` and `findComponent()` when you expect the element to exist — they throw immediately if not found, providing clearer test failures [source](./references/docs/api/index.md)

- Use `flushPromises()` to resolve non-Vue asynchronous operations such as mocked API calls (axios) or external promise-based logic that Vue doesn't track [source](./references/docs/guide/advanced/async-suspense.md)

- Enable `enableAutoUnmount(afterEach)` in your test setup to automatically clean up wrappers after every test, preventing state pollution and memory leaks [source](./references/docs/api/index.md)

```ts
import { enableAutoUnmount } from '@vue/test-utils'
import { afterEach } from 'vitest'

enableAutoUnmount(afterEach)
```

- Wrap components with `async setup()` in a `<Suspense>` component within your test to correctly handle their asynchronous initialization [source](./references/docs/guide/advanced/async-suspense.md)

- Enable `config.global.renderStubDefaultSlot = true` when using `shallow` mounting to ensure content within default slots is rendered for verification [source](./references/docs/guide/advanced/stubs-shallow-mount.md)

- Prefer `mount()` with specific `global.stubs` over `shallow: true` to keep tests more production-like while still isolating specific complex child components [source](./references/docs/guide/advanced/stubs-shallow-mount.md)

- Use `global.provide` to pass data to components using `inject`, ensuring the component tree's dependency injection works as it does in production [source](./references/docs/guide/advanced/reusability-composition.md)

- Test complex composables by mounting a minimal `TestComponent` that calls the composable, allowing you to verify internal state via `wrapper.vm` [source](./references/docs/guide/advanced/reusability-composition.md)

```ts
const TestComponent = defineComponent({
  setup() {
    return { ...useMyComposable() }
  }
})
const wrapper = mount(TestComponent)
expect(wrapper.vm.someValue).toBe(true)
```

- Stub custom directives using the `vName` naming convention (e.g., `vTooltip: true`) in the `global.stubs` mounting option [source](./references/docs/guide/advanced/stubs-shallow-mount.md)

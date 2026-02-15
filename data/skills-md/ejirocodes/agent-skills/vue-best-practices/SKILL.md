---
name: vue-best-practices
description: "Vue 3 and Vue.js best practices for TypeScript, vue-tsc, Volar, and component patterns. Use when writing, reviewing, or refactoring Vue 3 components with TypeScript, configuring Volar/vueCompilerOptions, extracting component types, working with defineModel/withDefaults, setting up Pinia store tests, or debugging Vue tooling issues. Triggers on Vue components, props extraction, wrapper components, template type checking, strictTemplates, vueCompilerOptions, Volar 3, CSS modules, fallthrough attributes, defineModel, withDefaults, deep watch, vue-router typed params, Pinia mocking, HMR SSR, moduleResolution bundler, useTemplateRef, onWatcherCleanup, useId, generic components, reactive props destructure."
license: MIT
metadata:
  author: ejirocodes
  version: '1.0.0'
---

# Vue 3 Best Practices

## Quick Reference

| Topic | When to Use | Reference |
|-------|-------------|-----------|
| **TypeScript** | Props extraction, generic components, useTemplateRef, JSDoc, reactive props destructure | [typescript.md](references/typescript.md) |
| **Volar** | IDE config, strictTemplates, CSS modules, directive comments, Volar 3.0 migration | [volar.md](references/volar.md) |
| **Components** | defineModel, deep watch, onWatcherCleanup, useId, deferred teleport | [components.md](references/components.md) |
| **Tooling** | moduleResolution, HMR SSR, duplicate plugin detection | [tooling.md](references/tooling.md) |
| **Testing** | Pinia store mocking, setup stores, Vue Router typed params | [testing.md](references/testing.md) |

## Essential Patterns

### Extract Component Props

```typescript
import type { ComponentProps } from 'vue-component-type-helpers'
import MyButton from './MyButton.vue'

type Props = ComponentProps<typeof MyButton>
```

### Reactive Props Destructure (Vue 3.5+)

```vue
<script setup lang="ts">
// Destructured props are reactive - preferred in Vue 3.5+
const { name, count = 0 } = defineProps<{ name: string; count?: number }>()
</script>
```

### useTemplateRef (Vue 3.5+)

```vue
<script setup lang="ts">
import { useTemplateRef, onMounted } from 'vue'

const inputRef = useTemplateRef('input')  // Auto-typed
onMounted(() => inputRef.value?.focus())
</script>
<template><input ref="input" /></template>
```

### onWatcherCleanup (Vue 3.5+)

```typescript
import { watch, onWatcherCleanup } from 'vue'

watch(query, async (q) => {
  const controller = new AbortController()
  onWatcherCleanup(() => controller.abort())
  await fetch(`/api?q=${q}`, { signal: controller.signal })
})
```

### defineModel with Required

```typescript
// Returns Ref<Item> instead of Ref<Item | undefined>
const model = defineModel<Item>({ required: true })
```

### Deep Watch with Numeric Depth

```typescript
// Vue 3.5+ - watch array mutations without full traversal
watch(items, handler, { deep: 1 })
```

### Pinia Store Test Setup

```typescript
import { createTestingPinia } from '@pinia/testing'
import { vi } from 'vitest'

mount(Component, {
  global: {
    plugins: [createTestingPinia({ createSpy: vi.fn })]
  }
})
```

## Common Mistakes

1. **Using `InstanceType<typeof Component>['$props']`** - Use `ComponentProps` instead
2. **Missing `createSpy` in createTestingPinia** - Required in @pinia/testing 1.0+
3. **Using `withDefaults` with union types** - Use Reactive Props Destructure
4. **`strictTemplates` in wrong tsconfig** - Add to `tsconfig.app.json`, not root
5. **ts_ls with Volar 3.0** - Use vtsls instead (Neovim)
6. **`deep: true` on large structures** - Use numeric depth for performance
7. **Watching destructured props directly** - Wrap in getter: `watch(() => count, ...)`
8. **Random IDs in SSR** - Use `useId()` for hydration-safe IDs

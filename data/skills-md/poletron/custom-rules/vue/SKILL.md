---
name: vue
description: >
  Vue 3 patterns with Composition API and TypeScript.
  Trigger: When building Vue.js applications with Composition API.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with vue"

## When to Use

Use this skill when:
- Building Vue 3 applications
- Using Composition API with script setup
- Managing reactive state
- Creating composables

---

## Critical Patterns

### Script Setup (REQUIRED)

```vue
<!-- ✅ ALWAYS: Use script setup with TypeScript -->
<script setup lang="ts">
import { ref, computed } from 'vue';

interface User {
  id: string;
  name: string;
}

const props = defineProps<{
  user: User;
}>();

const emit = defineEmits<{
  (e: 'update', value: string): void;
}>();

const count = ref(0);
const doubleCount = computed(() => count.value * 2);
</script>
```

### Composables (REQUIRED)

```typescript
// ✅ ALWAYS: Extract reusable logic into composables
// composables/useUser.ts
export function useUser(userId: Ref<string>) {
  const user = ref<User | null>(null);
  const loading = ref(true);
  
  watchEffect(async () => {
    loading.value = true;
    user.value = await fetchUser(userId.value);
    loading.value = false;
  });
  
  return { user, loading };
}
```

### Reactive State (REQUIRED)

```typescript
// ✅ Use ref for primitives
const count = ref(0);

// ✅ Use reactive for objects
const state = reactive({
  users: [] as User[],
  loading: false,
});

// ✅ Use computed for derived state
const activeUsers = computed(() => 
  state.users.filter(u => u.active)
);
```

---

## Decision Tree

```
Need primitive state?      → Use ref()
Need object state?         → Use reactive()
Need derived value?        → Use computed()
Need side effect?          → Use watchEffect()
Need specific watch?       → Use watch()
Need reusable logic?       → Create composable
```

---

## Code Examples

### Component with v-model

```vue
<script setup lang="ts">
const model = defineModel<string>();
</script>

<template>
  <input :value="model" @input="model = $event.target.value" />
</template>
```

### Async Component

```typescript
const AsyncModal = defineAsyncComponent(() =>
  import('./components/Modal.vue')
);
```

---

## Commands

```bash
npm create vue@latest myapp
npm run dev
npm run build
npm run test:unit
```

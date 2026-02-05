---
name: vue-dev
description: "Generate modern, maintainable Vue TypeScript code with best practices: Composition API, script setup with TS, composable patterns over global stores, props destructure, VueUse integration, Tailwind CSS, accessibility, performance optimization, and Vitest testing. Use when creating Vue 3 components, composables, or refactoring Vue code to follow modern patterns."
---

# Vue Dev - Modern Vue TypeScript Development

## Core Principles

**Always follow these principles unless project context demands otherwise:**
- **Composition API** with `<script setup>` and TypeScript
- **Props destructure** with `defineProps<T>()` for typed defaults
- **Composables over stores** - use provider pattern, global refs, or Nuxt's `useState`
- **VueUse** - never rewrite logic if VueUse provides equivalent functionality
- **Concrete types over interfaces** - use `type` aliases with precise typing
- **Tailwind CSS** - never inline `<style>` blocks unless absolutely necessary
- **Accessibility first** - ARIA attributes, keyboard navigation, semantic HTML
- **Performance aware** - `computed`, shallow refs, lazy loading when appropriate

## Project Detection

### Build Tool Detection

Check project structure to determine build tool:
```bash
# Nuxt 4
nuxt.config.ts present

# Vite
vite.config.ts present (no nuxt.config.ts)
```

**State management approach based on build tool:**
- **Nuxt**: Use `useState()` for shared state
- **Vite**: Use global refs or provider pattern

### TypeScript Configuration

Always attempt to read `tsconfig.json` first:
```bash
# If tsconfig.json exists
cat tsconfig.json

# Check for:
# - strict mode: "strict": true
# - paths configuration for imports
# - target version
```

If `tsconfig.json` doesn't exist or can't be read, **assume strict mode is enabled**.

## Component Structure

### Single File Component Template

```vue
<script setup lang="ts">
// 1. Imports (VueUse first, then local)
import { ref, computed, onMounted, watch } from 'vue'
import { useLocalStorage, onClickOutside } from '@vueuse/core'
import type { SomeType } from './types'

// 2. Props with destructure and typed defaults
const {
  label,
  count = 0,
  disabled = false,
  items = [],
} = defineProps<{
  label: string
  count?: number
  disabled?: boolean
  items?: SomeType[]
}>()

// 3. Emits with type definition
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'submit', payload: { id: string; data: unknown }): void
}>()

// 4. Reactive state
const isOpen = ref(false)
const localValue = ref('')

// 5. Composables
const { data, error } = useAsyncData()
const storage = useLocalStorage('key', defaultValue)

// 6. Computed properties
const computedValue = computed(() => localValue.value.toUpperCase())

// 7. Watchers
watch(localValue, (newVal) => {
  emit('update:modelValue', newVal)
})

// 8. Lifecycle hooks
onMounted(() => {
  // initialization
})

// 9. Methods
const handleClick = () => {
  isOpen.value = !isOpen.value
}

const handleSubmit = () => {
  emit('submit', { id: '123', data: localValue.value })
}
</script>

<template>
  <button
    type="button"
    :disabled="disabled"
    :aria-pressed="isOpen"
    @click="handleClick"
    class="px-4 py-2 rounded bg-blue-500 hover:bg-blue-600 disabled:opacity-50"
  >
    {{ label }}
  </button>
</template>
```

## Composable Patterns

### Composable Decision Tree

**Create separate composable file when:**
- Logic is reused in 2+ components
- Logic involves async operations with loading/error states
- Logic requires complex state management
- Logic benefits from isolation and testing

**Inline composable when:**
- Logic is single-use and simple
- Logic is tightly coupled to specific component
- Logic is less than 5 lines

### Composable Template Structure

```typescript
// useFeatureName.ts
import { ref, computed, watch } from 'vue'
import { useLocalStorage, useDebounceFn } from '@vueuse/core'
import type { SomeType } from './types'

/**
 * Composable for [brief description]
 *
 * @param param - Description of parameter
 * @returns Object with reactive properties and methods
 *
 * @example
 * ```ts
 * const { data, loading, error, refresh } = useFeatureName({
 *   id: '123',
 *   autoFetch: true
 * })
 * ```
 */
export function useFeatureName<T = unknown>(options: {
  id: string
  autoFetch?: boolean
  debounce?: number
}) {
  // State
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  // Composables from VueUse
  const storage = useLocalStorage(`feature-${options.id}`, null)

  // Methods
  const fetchData = async (): Promise<void> => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`/api/data/${options.id}`)
      const result = await response.json() as T
      data.value = result
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Unknown error')
    } finally {
      loading.value = false
    }
  }

  const debouncedFetch = useDebounceFn(fetchData, options.debounce ?? 300)

  // Computed
  const hasData = computed(() => data.value !== null)
  const errorMessage = computed(() => error.value?.message ?? '')

  // Lifecycle
  if (options.autoFetch) {
    fetchData()
  }

  return {
    // State
    data,
    loading,
    error,
    // Computed
    hasData,
    errorMessage,
    // Methods
    refresh: debouncedFetch,
  }
}
```

### Async Wrapper Pattern

For async operations, prefer wrapper functions that return data/error properties:

```typescript
// useAsync.ts
import { ref, type Ref } from 'vue'

export type AsyncResult<T> = {
  data: Ref<T | null>
  loading: Ref<boolean>
  error: Ref<Error | null>
}

/**
 * Wrapper for async operations with consistent error handling
 */
export function useAsync<T>(
  fn: () => Promise<T>,
  options: { immediate?: boolean } = {}
): AsyncResult<T> {
  const data = ref<T | null>(null) as Ref<T | null>
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const execute = async (): Promise<void> => {
    loading.value = true
    error.value = null

    try {
      data.value = await fn()
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Unknown error')
    } finally {
      loading.value = false
    }
  }

  if (options.immediate) {
    execute()
  }

  return {
    data,
    loading,
    error,
  }
}
```

## State Management Patterns

### Nuxt: useState Pattern

```typescript
// composables/useSharedState.ts
export const useCounter = () => {
  const counter = useState('counter', () => 0)

  const increment = () => {
    counter.value++
  }

  return {
    counter: readonly(counter),
    increment,
  }
}
```

### Vite: Global Ref Pattern

```typescript
// store/globalStore.ts
import { ref } from 'vue'

const globalState = ref(0)

export function useGlobalState() {
  const increment = () => {
    globalState.value++
  }

  return {
    counter: readonly(globalState),
    increment,
  }
}
```

### Provider Pattern (Vite)

```typescript
// context/UserContext.ts
import { provide, inject, type InjectionKey, readonly } from 'vue'
import type { User } from './types'

const UserContextKey: InjectionKey<ReturnType<typeof useUserState>> = Symbol('User')

export function provideUserContext(user: User) {
  const state = useUserState(user)
  provide(UserContextKey, state)
}

export function useUserContext() {
  const context = inject(UserContextKey)
  if (!context) {
    throw new Error('useUserContext must be used within provideUserContext')
  }
  return context
}

function useUserState(initialUser: User) {
  const currentUser = ref(initialUser)

  const setUser = (user: User) => {
    currentUser.value = user
  }

  return {
    currentUser: readonly(currentUser),
    setUser,
  }
}
```

## VueUsage Patterns

Always check VueUse first. Common patterns:

### Common VueUse Functions

```typescript
import {
  // Storage
  useLocalStorage,
  useSessionStorage,
  useStorage,

  // DOM
  onClickOutside,
  onKeyStroke,
  useElementBounding,
  useWindowSize,
  useElementSize,
  useIntersectionObserver,

  // Async
  useAsyncState,
  useFetch,

  // Utilities
  useDebounceFn,
  useThrottleFn,
  useToggle,
  useClipboard,
  useTitle,

  // Sensors
  useMouse,
  useScroll,
  useMediaQuery,
  useNetwork,

  // Formatters
  useDateFormat,
  useTimeAgo,
} from '@vueuse/core'
```

### Examples

```typescript
// Close dropdown when clicking outside
const buttonRef = ref<HTMLElement>()
onClickOutside(buttonRef, () => isOpen.value = false)

// Responsive design
const isMobile = useMediaQuery('(max-width: 768px)')

// Debounced search
const debouncedSearch = useDebounceFn((query: string) => {
  // search logic
}, 300)

// Local storage persistence
const theme = useLocalStorage('theme', 'light')
```

## TypeScript Patterns

### Type Definition

Use `type` aliases over interfaces:

```typescript
// ✅ Good
type User = {
  id: string
  name: string
  email: string
}

// ❌ Avoid
interface User {
  id: string
  name: string
  email: string
}
```

### Props Typing

```typescript
// Simple props
defineProps<{
  label: string
  count: number
}>()

// Optional props with defaults
const { count = 0 } = defineProps<{
  label: string
  count?: number
}>()

// Generic props
defineProps<{
  items: Array<{ id: string; name: string }>
  selected?: string
}>()
```

### Emit Typing

```typescript
const emit = defineEmits<{
  change: [id: number]
  update: [value: string]
}>()
```

### Ref Typing

```typescript
// Explicit type
const count = ref<number>(0)

// Inferred from initial value
const message = ref('hello')

// Nullable ref
const user = ref<User | null>(null)

// Array ref
const items = ref<Item[]>([])
```

## Performance Best Practices

### Computed vs Watch

```typescript
// ✅ Use computed for derived state
const fullName = computed(() => `${firstName.value} ${lastName.value}`)

// ✅ Use watch for side effects
watch(fullName, (newName) => {
  console.log('Name changed:', newName)
})
```

### Shallow Refs for Large Objects

```typescript
// For large objects or frequent reassignments
const largeData = shallowRef<LargeObject[]>([])
```

### Lazy Loading Components

```typescript
const Modal = defineAsyncComponent(() => import('./Modal.vue'))
```

### v-once for Static Content

```vue
<template>
  <div v-once>
    <h1>{{ staticTitle }}</h1>
  </div>
</template>
```

### v-memo for Expensive Computations

```vue
<template>
  <li v-for="item in items" :key="item.id" v-memo="[item.id, item.selected]">
    {{ item.name }}
  </li>
</template>
```

## Accessibility Guidelines

### Semantic HTML

```vue
<template>
  <!-- ✅ Semantic -->
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>

  <!-- ❌ Non-semantic -->
  <div class="nav">
    <div class="nav-item">Home</div>
  </div>
</template>
```

### ARIA Attributes

```vue
<template>
  <button
    :aria-pressed="isActive"
    :aria-expanded="isOpen"
    aria-label="Toggle menu"
  >
    Toggle
  </button>
</template>
```

### Keyboard Navigation

```vue
<script setup lang="ts">
import { onKeyStroke } from '@vueuse/core'

onKeyStroke('Enter', () => {
  handleSubmit()
})

onKeyStroke('Escape', () => {
  closeModal()
})
</script>
```

### Form Accessibility

```vue
<template>
  <label for="email">Email address</label>
  <input
    id="email"
    v-model="email"
    type="email"
    required
    aria-invalid="!!error"
    :aria-describedby="error ? 'email-error' : undefined"
  />
  <span v-if="error" id="email-error" role="alert">{{ error }}</span>
</template>
```

## Testing Patterns

### Composable Testing

```typescript
// tests/useFeatureName.spec.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { ref } from 'vue'
import { useFeatureName } from '../useFeatureName'

describe('useFeatureName', () => {
  it('should initialize with default values', () => {
    const { data, loading, error } = useFeatureName({
      id: 'test',
      autoFetch: false,
    })

    expect(data.value).toBeNull()
    expect(loading.value).toBe(false)
    expect(error.value).toBeNull()
  })

  it('should fetch data successfully', async () => {
    const { data, refresh } = useFeatureName({
      id: 'test',
      autoFetch: false,
    })

    await refresh()

    expect(data.value).toBeDefined()
  })
})
```

## File Organization

**Always use flat structure:**

```
src/
├── components/
│   ├── Button.vue
│   ├── Input.vue
│   └── Modal.vue
├── composables/
│   ├── useAuth.ts
│   ├── useFetch.ts
│   └── useForm.ts
├── types/
│   ├── user.ts
│   └── api.ts
└── utils/
    └── format.ts
```

## Code Quality Checklist

Before finalizing any component or composable:

- [ ] TypeScript strict mode compatible
- [ ] Props properly typed with `defineProps<T>()`
- [ ] Props destructured for defaults
- [ ] Emits typed with `defineEmits<T>()`
- [ ] VueUsed checked and applied where applicable
- [ ] Tailwind classes used (no `<style>` blocks)
- [ ] ARIA attributes added for accessibility
- [ ] Keyboard navigation supported
- [ ] Async errors properly handled
- [ ] Loading states for async operations
- [ ] Performance considerations applied (computed, shallow refs)
- [ ] Composable extracted if reused or complex
- [ ] State management follows project pattern (useState/global ref/provider)
- [ ] Tests written for composables

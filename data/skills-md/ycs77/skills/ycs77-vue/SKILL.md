---
name: ycs77-vue
description: This skill should be used when applying project-specific opinionated Vue 3 conventions. It covers SFC block order (template-first vs script-first), inline typing for defineProps and defineEmits, using reactive() for form state management, ref type assertions with as Ref<Type> for complex types, same-name shorthand bindings in Vue 3.4+, and props access patterns in templates. Relevant when a user asks about template ordering, how to type props or emits inline, reactive vs ref for forms, ref type assertion patterns, shorthand attribute bindings, props usage in templates, or following Lucas Yang's Vue coding conventions.
metadata:
  author: Lucas Yang
  version: "2026.02.07"
---

# Lucas Yang's Vue Conventions

Opinionated Vue 3 and TypeScript patterns emphasizing minimal boilerplate, readability, and practical simplicity for real-world projects.

## TypeScript Formatting

**Standard**: 2 spaces, single quotes, no semicolons, trailing commas.

## Vue SFC Patterns

### 1. SFC Block Order

Always place `<template>` before `<script setup lang="ts">` in Single File Components. This follows the natural reading flow from structure (what to render) to behavior (how it works).

**Good:**
```vue
<template>
  <div class="container">
    <h1>{{ title }}</h1>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const title = ref('Hello World')
</script>
```

**Avoid:**
```vue
<script setup lang="ts">
import { ref } from 'vue'

const title = ref('Hello World')
</script>

<template>
  <div class="container">
    <h1>{{ title }}</h1>
  </div>
</template>
```

### 2. Inline Props/Emits Types

Prefer inline type declarations for `defineProps` and `defineEmits`. This approach provides better readability and reduces the need for additional type declarations, making it easier to understand the component's API at a glance.

**Good:**
```vue
<script setup lang="ts">
const props = defineProps<{
  title: string
  count?: number
  items: {
    id: string
    name: string
  }[]
}>()

const emit = defineEmits<{
  update: [value: string]
  delete: [id: string]
}>()
</script>
```

**Avoid:**
```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
  items: {
    id: string
    name: string
  }[]
}

interface Emits {
  update: [value: string]
  delete: [id: string]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
</script>
```

**Exception**: Only extract to a separate interface when the type is reused across multiple components or needs to be exported.

### 3. Use reactive() for Form State

When managing form state, prefer using `reactive()` to create a single reactive object that holds all form fields. This approach simplifies state management and reduces boilerplate code compared to using multiple `ref()` calls for each field.

**Good:**
```vue
<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="form.email" type="email">
    <input v-model="form.password" type="password">
    <input v-model="form.rememberMe" type="checkbox">
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
})

function handleSubmit() {
  console.log(form) // Clean object, easy to submit
}

function resetForm() {
  form.email = ''
  form.password = ''
  form.rememberMe = false
}
</script>
```

**Avoid:**
```vue
<script setup lang="ts">
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const rememberMe = ref(false)

function handleSubmit() {
  console.log({
    email: email.value,
    password: password.value,
    rememberMe: rememberMe.value,
  })
}
</script>
```

**Rationale**: Grouping related state reduces `.value` boilerplate and makes form submission cleaner. Use individual `ref()` only for truly independent state.

### 4. Use Type Assertion for ref() with Complex Types

When using `ref()` with interface or complex object types, use type assertion with `as Ref<Type>` to avoid TypeScript errors. For primitive types (string, number, boolean) or enum types, you can safely use the generic parameter `ref<Type>()`.

**Good:**
```vue
<script setup lang="ts">
import type { Ref } from 'vue'
import type { User } from '@/types'
import { ref } from 'vue'

// Complex type - use type assertion
const user = ref() as Ref<User>
const users = ref([]) as Ref<User[]>
const isSelectedUser = ref(null) as Ref<User | null>  // Prefer null over undefined

// Primitive types - generic parameter is fine
const count = ref<number>(0)
const isActive = ref<boolean>(false)
const status = ref<Status>(Status.Pending)
</script>
```

**Avoid:**
```vue
<script setup lang="ts">
import type { User } from '@/types'
import { ref } from 'vue'

// May cause: Type '...' is not assignable to type 'Ref<User>'
const user = ref<User>()
</script>
```

**Rationale**: Vue's official documentation recommends `ref<Type>()`, but this project prefers type assertion `as Ref<Type>` for complex types to avoid type conflicts while maintaining type safety.

### 5. Use Same-name Shorthand for Bindings

When binding a prop or attribute where the variable name matches the attribute name, use the same-name shorthand syntax to reduce redundancy. This feature is available in Vue 3.4+ and mirrors JavaScript's object property shorthand pattern.

**Good:**
```vue
<template>
  <div :id :title>
    <MyComponent :user-name :count :is-active />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const id = ref('app')
const title = ref('Dashboard')
const userName = ref('Lucas')  // Matches :user-name (kebab-case)
const count = ref(42)
const isActive = ref(true)
</script>
```

**Avoid:**
```vue
<template>
  <div :id="id" :title="title">
    <MyComponent :user-name="userName" :count="count" :is-active="isActive" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const id = ref('app')
const title = ref('Dashboard')
const userName = ref('Lucas')
const count = ref(42)
const isActive = ref(true)
</script>
```

**Rationale**: Same-name shorthand reduces visual noise and follows the familiar JavaScript ES6 object property shorthand pattern. It makes templates more concise when variable names already describe the bound attribute clearly. Note that kebab-case attributes (`:user-name`) automatically match camelCase variables (`userName`). For props that require `props.` prefix (see Rule 6), do not use shorthand.

### 6. Avoid `props.` Prefix in Templates

Do not use `props.` prefix when accessing props in `<template>`. Vue's `<script setup>` destructures props into the template scope automatically, so the prefix is unnecessary. Only add `props.` when the prop name conflicts with a language keyword or HTML attribute (e.g., `class`, `as`). In those cases, do not apply same-name shorthand binding — always use the explicit `props.` form.

**Good:**
```vue
<template>
  <div :class="props.class">
    <h1>{{ title }}</h1>
    <component :is="props.as">content</component>
  </div>
</template>

<script setup lang="ts">
import type { HTMLAttributes } from 'vue'

const props = defineProps<{
  title: string
  as: string
  class?: HTMLAttributes['class']
}>()
</script>
```

**Avoid:**
```vue
<template>
  <div :class>
    <h1>{{ props.title }}</h1>
    <component :is="as">content</component>
  </div>
</template>

<script setup lang="ts">
import type { HTMLAttributes } from 'vue'

const props = defineProps<{
  title: string
  as: string
  class?: HTMLAttributes['class']
}>()
</script>
```

**Rationale**: Omitting `props.` keeps templates concise and consistent with how `ref()` and `computed()` values are accessed. Language keywords and HTML attributes like `class` and `as` require `props.` to avoid conflicts, and must use explicit binding (`:class="props.class"`) instead of shorthand (`:class`) to prevent resolving to the wrong scope.

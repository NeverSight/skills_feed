---
name: debug:vue
description: Debug Vue.js 3 application issues systematically. This skill helps diagnose and resolve Vue-specific problems including reactivity failures with ref/reactive, component update issues, Pinia store state management problems, computed property caching bugs, Teleport/Suspense rendering issues, and SSR hydration mismatches. Provides Vue DevTools usage, console debugging techniques, Vite dev server troubleshooting, and vue-tsc type checking guidance.
---

# Vue.js Debugging Guide

A systematic approach to debugging Vue.js 3 applications, covering common error patterns, debugging tools, and resolution strategies.

## Common Error Patterns

### 1. Reactivity Not Working

**Symptoms:**
- Data changes but UI does not update
- Computed properties return stale values
- Watch callbacks not firing

**Common Causes:**
```javascript
// WRONG: Adding new properties to reactive object
const state = reactive({ count: 0 })
state.newProp = 'value'  // Not reactive in Vue 2, works in Vue 3 with Proxy

// WRONG: Destructuring reactive objects
const { count } = reactive({ count: 0 })  // count is NOT reactive

// WRONG: Replacing entire reactive object
let state = reactive({ count: 0 })
state = reactive({ count: 1 })  // Lost reactivity connection

// WRONG: Using ref without .value
const count = ref(0)
count = 5  // Wrong! Use count.value = 5
```

**Solutions:**
```javascript
// Use toRefs for destructuring
const state = reactive({ count: 0 })
const { count } = toRefs(state)  // count.value is reactive

// Use ref for primitives
const count = ref(0)
count.value++  // Correct

// Use shallowRef for large objects that don't need deep reactivity
const largeData = shallowRef({ /* big object */ })

// Force reactivity update
import { triggerRef } from 'vue'
triggerRef(myShallowRef)
```

### 2. Component Not Updating

**Symptoms:**
- Props change but component doesn't re-render
- Parent state updates don't propagate to children
- v-for lists don't update correctly

**Debugging Steps:**
```javascript
// 1. Check if prop is reactive
watch(() => props.myProp, (newVal) => {
  console.log('Prop changed:', newVal)
}, { immediate: true })

// 2. Verify key attribute on v-for
<template>
  <!-- WRONG: index as key for dynamic lists -->
  <div v-for="(item, index) in items" :key="index">

  <!-- CORRECT: unique identifier -->
  <div v-for="item in items" :key="item.id">
</template>

// 3. Check for prop mutation (anti-pattern)
// Props should be immutable - emit events instead
emit('update:modelValue', newValue)
```

### 3. Pinia Store Issues

**Symptoms:**
- Store state not updating across components
- Actions not triggering reactivity
- Getters returning stale data

**Common Problems:**
```javascript
// WRONG: Destructuring store state
const store = useMyStore()
const { count } = store  // NOT reactive!

// CORRECT: Use storeToRefs
const store = useMyStore()
const { count } = storeToRefs(store)  // Reactive

// WRONG: Mutating state directly outside actions
store.count++  // Works but bypasses devtools tracking

// CORRECT: Use actions or $patch
store.increment()  // Action
store.$patch({ count: store.count + 1 })  // $patch
```

**Debugging Pinia:**
```javascript
// Enable Pinia devtools tracking
import { createPinia } from 'pinia'
const pinia = createPinia()

// Subscribe to state changes
store.$subscribe((mutation, state) => {
  console.log('Mutation:', mutation.type, mutation.storeId)
  console.log('New state:', state)
})

// Subscribe to actions
store.$onAction(({ name, args, after, onError }) => {
  console.log(`Action ${name} called with:`, args)
  after((result) => console.log(`${name} returned:`, result))
  onError((error) => console.error(`${name} failed:`, error))
})
```

### 4. Computed Property Caching Issues

**Symptoms:**
- Computed returns same value despite dependency changes
- Infinite loops in computed properties
- Performance issues with computed

**Solutions:**
```javascript
// Check dependencies are reactive
const computed1 = computed(() => {
  // This won't update if nonReactiveValue changes
  return someRef.value + nonReactiveValue
})

// Avoid side effects in computed
// WRONG:
const bad = computed(() => {
  someRef.value = 'changed'  // Side effect!
  return otherRef.value
})

// Debug computed dependencies
const myComputed = computed(() => {
  console.log('Computed recalculating...')
  return expensiveOperation(dep1.value, dep2.value)
})
```

### 5. Teleport/Suspense Issues

**Teleport Problems:**
```html
<!-- Ensure target exists before Teleport mounts -->
<template>
  <!-- WRONG: target might not exist -->
  <Teleport to="#modal-container">
    <Modal />
  </Teleport>

  <!-- CORRECT: conditional render -->
  <Teleport v-if="isMounted" to="#modal-container">
    <Modal />
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const isMounted = ref(false)
onMounted(() => { isMounted.value = true })
</script>
```

**Suspense Problems:**
```html
<!-- Handle errors in Suspense -->
<template>
  <Suspense>
    <template #default>
      <AsyncComponent />
    </template>
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup>
import { onErrorCaptured, ref } from 'vue'

const error = ref(null)
onErrorCaptured((err) => {
  error.value = err
  return false  // Stop propagation
})
</script>
```

### 6. SSR Hydration Mismatches

**Symptoms:**
- Console warning: "Hydration mismatch"
- Content flickers on page load
- Different content between server and client

**Common Causes and Solutions:**
```javascript
// WRONG: Browser-only code in setup
const width = window.innerWidth  // Fails on server

// CORRECT: Use onMounted for browser APIs
const width = ref(0)
onMounted(() => {
  width.value = window.innerWidth
})

// CORRECT: Use ClientOnly component (Nuxt)
<template>
  <ClientOnly>
    <BrowserOnlyComponent />
  </ClientOnly>
</template>

// Check for SSR vs client
const isClient = typeof window !== 'undefined'

// Use useId() for consistent IDs
import { useId } from 'vue'
const id = useId()  // Same on server and client
```

## Debugging Tools

### Vue DevTools

**Installation:**
- Chrome: [Vue.js devtools](https://chrome.google.com/webstore/detail/vuejs-devtools/)
- Firefox: [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)

**Key Features:**
1. **Components Tab**: Inspect component hierarchy, props, data, computed
2. **Pinia Tab**: View store state, actions, mutations
3. **Timeline Tab**: Track events, mutations, and performance
4. **Routes Tab**: Debug Vue Router (if using)

**DevTools Tips:**
```javascript
// Access component instance in console
// Select component in DevTools, then in console:
$vm  // Current component instance
$vm.someMethod()  // Call methods
$vm.someData  // Access data

// Inspect from DOM element
// Right-click element > Inspect > Console:
$0.__vueParentComponent  // Parent component
```

### Console Debugging

```javascript
// Strategic console.log placement
export default {
  setup() {
    const state = reactive({ count: 0 })

    // Log reactive state changes
    watch(
      () => ({ ...state }),
      (newState, oldState) => {
        console.log('State changed:', { old: oldState, new: newState })
      },
      { deep: true }
    )

    return { state }
  }
}

// Use console.table for arrays/objects
console.table(items.value)

// Use console.trace for call stack
function problematicFunction() {
  console.trace('Called from:')
}

// Group related logs
console.group('Component Mount')
console.log('Props:', props)
console.log('State:', state)
console.groupEnd()
```

### Debugger Statement

```javascript
// Pause at specific points
function handleClick() {
  debugger  // Execution pauses here
  // Inspect scope, call stack, evaluate expressions
  processData()
}

// Conditional debugging
watch(count, (val) => {
  if (val > 10) {
    debugger  // Only pause when condition met
  }
})
```

### Vite Dev Server

```bash
# Enable verbose logging
vite --debug

# Check for HMR issues
vite --force  # Clear cache

# Common vite.config.js debugging options
export default defineConfig({
  server: {
    hmr: {
      overlay: true  // Show errors as overlay
    }
  },
  build: {
    sourcemap: true  // Enable source maps
  }
})
```

### vue-tsc Type Checking

```bash
# Run type checking
npx vue-tsc --noEmit

# Watch mode
npx vue-tsc --noEmit --watch

# Check specific files
npx vue-tsc --noEmit src/components/MyComponent.vue
```

## The Four Phases of Vue Debugging

### Phase 1: Identify the Error Type

```javascript
// 1. Check browser console for errors
// 2. Categorize the error:
//    - Template error (compilation)
//    - Runtime error (JavaScript)
//    - Reactivity issue (no error, wrong behavior)
//    - Network error (API/async)

// Set up global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err)
  console.log('Component:', instance?.$options?.name || 'Unknown')
  console.log('Error Info:', info)
  // Send to error tracking service
}

// Set up warning handler (development)
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Vue Warning:', msg)
  console.log('Trace:', trace)
}
```

### Phase 2: Isolate the Problem

```javascript
// 1. Simplify the component
// 2. Remove code until error disappears
// 3. Add code back incrementally

// Use error boundaries to isolate
const ErrorBoundary = defineComponent({
  setup(_, { slots }) {
    const error = ref(null)

    onErrorCaptured((err, instance, info) => {
      error.value = { err, info }
      return false  // Prevent propagation
    })

    return () => error.value
      ? h('div', { class: 'error' }, `Error: ${error.value.err.message}`)
      : slots.default?.()
  }
})

// Wrap suspicious components
<template>
  <ErrorBoundary>
    <SuspiciousComponent />
  </ErrorBoundary>
</template>
```

### Phase 3: Investigate Root Cause

```javascript
// Check component lifecycle
onBeforeMount(() => console.log('beforeMount'))
onMounted(() => console.log('mounted'))
onBeforeUpdate(() => console.log('beforeUpdate'))
onUpdated(() => console.log('updated'))
onBeforeUnmount(() => console.log('beforeUnmount'))
onUnmounted(() => console.log('unmounted'))

// Track prop changes
watch(() => props, (newProps) => {
  console.log('Props changed:', JSON.stringify(newProps, null, 2))
}, { deep: true, immediate: true })

// Monitor emitted events
const emit = defineEmits(['update'])
function emitUpdate(value) {
  console.log('Emitting update:', value)
  emit('update', value)
}
```

### Phase 4: Apply and Verify Fix

```javascript
// 1. Apply the smallest possible fix
// 2. Verify fix doesn't break other functionality
// 3. Add test to prevent regression

// Example: Add defensive checks
const displayValue = computed(() => {
  if (!props.data) {
    console.warn('MyComponent: data prop is undefined')
    return 'N/A'
  }
  return props.data.value ?? 'N/A'
})

// Add type safety
interface Props {
  data?: {
    value: string
  }
}
const props = withDefaults(defineProps<Props>(), {
  data: undefined
})
```

## Quick Reference Commands

### Development

```bash
# Start dev server with debugging
npm run dev -- --debug

# Type check
npm run type-check
# or: npx vue-tsc --noEmit

# Lint and fix
npm run lint -- --fix

# Run unit tests
npm run test:unit

# Run tests in watch mode
npm run test:unit -- --watch
```

### Build Debugging

```bash
# Build with source maps
npm run build -- --sourcemap

# Analyze bundle size
npx vite-bundle-analyzer

# Preview production build locally
npm run preview
```

### Common Fixes

```javascript
// Force component re-render
const key = ref(0)
function forceRerender() {
  key.value++
}
// <MyComponent :key="key" />

// Clear reactive state
Object.keys(state).forEach(key => delete state[key])
Object.assign(state, initialState)

// Reset Pinia store
store.$reset()

// Flush pending updates
import { nextTick } from 'vue'
await nextTick()
// DOM is now updated
```

### Vue 3 Production Error Codes

Vue 3 uses short error codes in production. Reference:
- [Production Error Code Reference](https://vuejs.org/error-reference/)

```javascript
// Decode production errors by searching the code
// Example: Error code "0" = "This is a Vue internal error..."
```

## Error Handling Best Practices

```javascript
// main.js - Global error handling setup
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  // Log to console in development
  if (import.meta.env.DEV) {
    console.error('Vue Error:', err)
    console.log('Component:', instance)
    console.log('Info:', info)
  }

  // Send to error tracking in production
  if (import.meta.env.PROD) {
    // Sentry, LogRocket, etc.
    errorTracker.captureException(err, {
      extra: { component: instance?.$options?.name, info }
    })
  }
}

// Global warning handler (dev only)
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Vue Warning:', msg)
  // Optionally treat warnings as errors in CI
  if (import.meta.env.CI) {
    throw new Error(`Vue Warning: ${msg}`)
  }
}

app.mount('#app')
```

## Resources

- [Vue.js Official Docs](https://vuejs.org/)
- [Vue DevTools](https://devtools.vuejs.org/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vue School Articles](https://vueschool.io/articles/)
- [Vue.js Production Error Reference](https://vuejs.org/error-reference/)

---
name: debug:nuxtjs
description: Debug Nuxt.js issues systematically. Use when encountering SSR errors, Nitro server issues, hydration mismatches like "Hydration text/node mismatch", composable problems with useFetch or useAsyncData, plugin initialization failures, module conflicts, auto-import issues, or Vue-specific runtime errors in a Nuxt context.
---

# Nuxt.js Debugging Guide

This guide provides a systematic approach to debugging Nuxt.js applications, covering SSR/SSG issues, Nitro server problems, hydration mismatches, composables, and more.

## Common Error Patterns

### 1. Hydration Mismatches

Hydration mismatches occur when the server-rendered HTML differs from what Vue expects on the client.

**Symptoms:**
- Console warning: "Hydration text/node mismatch"
- Content flickers or changes after page load
- `[Vue warn]: Hydration completed but contains mismatches`

**Common Causes:**
```typescript
// BAD: Using browser-only APIs during SSR
const windowWidth = window.innerWidth // Errors on server

// GOOD: Guard with process.client or useNuxtApp()
const windowWidth = ref(0)
onMounted(() => {
  windowWidth.value = window.innerWidth
})

// GOOD: Use ClientOnly component
<ClientOnly>
  <BrowserOnlyComponent />
</ClientOnly>

// BAD: Date/time rendering inconsistency
<span>{{ new Date().toLocaleString() }}</span> // Different on server vs client

// GOOD: Use consistent formatting or client-only
<ClientOnly>
  <span>{{ formattedDate }}</span>
  <template #fallback>Loading...</template>
</ClientOnly>
```

**Debugging Steps:**
1. Check browser console for specific mismatch details
2. Look for `window`, `document`, `localStorage` usage outside `onMounted` or `process.client`
3. Check for random values, dates, or user-specific data rendered during SSR
4. Use Vue DevTools to inspect component tree

### 2. useFetch/useAsyncData Errors

**Common Issues:**

```typescript
// ERROR: "useFetch is not defined" or composable called outside setup
// BAD: Calling in regular function
function fetchData() {
  const { data } = useFetch('/api/data') // Error!
}

// GOOD: Call in setup or use $fetch in functions
const { data, error, pending, refresh } = useFetch('/api/data')

// Or for functions:
async function fetchData() {
  const data = await $fetch('/api/data')
}
```

**Key/Caching Issues:**
```typescript
// BAD: Same key returns cached data
const { data: user1 } = useFetch('/api/user', { key: 'user' })
const { data: user2 } = useFetch('/api/user', { key: 'user' }) // Returns same cached data!

// GOOD: Use unique keys
const { data: user1 } = useFetch('/api/user/1', { key: 'user-1' })
const { data: user2 } = useFetch('/api/user/2', { key: 'user-2' })

// Force refresh
const { data, refresh } = useFetch('/api/data')
await refresh() // Bypasses cache
```

**Watch for Reactive Parameters:**
```typescript
// BAD: Non-reactive parameter won't trigger refetch
const userId = '123'
const { data } = useFetch(`/api/user/${userId}`)

// GOOD: Use computed or getter for reactive URLs
const userId = ref('123')
const { data } = useFetch(() => `/api/user/${userId.value}`)

// Or with watch
const { data } = useFetch('/api/user', {
  query: { id: userId },
  watch: [userId]
})
```

### 3. Nitro Server Errors

**500 Internal Server Errors:**
```typescript
// Check server/api/ files for issues
// server/api/example.ts

// BAD: Unhandled errors crash the endpoint
export default defineEventHandler(async (event) => {
  const data = await fetchExternalAPI() // Unhandled rejection
  return data
})

// GOOD: Proper error handling
export default defineEventHandler(async (event) => {
  try {
    const data = await fetchExternalAPI()
    return data
  } catch (error) {
    throw createError({
      statusCode: 500,
      statusMessage: 'Failed to fetch data',
      data: { originalError: error.message }
    })
  }
})
```

**Reading Request Body:**
```typescript
// BAD: Wrong method to read body
export default defineEventHandler(async (event) => {
  const body = event.body // undefined!

  // GOOD: Use readBody
  const body = await readBody(event)

  // For query params
  const query = getQuery(event)

  // For route params
  const { id } = event.context.params
})
```

### 4. Plugin Initialization Issues

```typescript
// plugins/my-plugin.ts

// BAD: Plugin errors break the entire app
export default defineNuxtPlugin(() => {
  const api = new ExternalAPI() // May throw
})

// GOOD: Error handling in plugins
export default defineNuxtPlugin({
  name: 'my-plugin',
  enforce: 'pre', // or 'post'
  async setup(nuxtApp) {
    try {
      const api = new ExternalAPI()
      return {
        provide: {
          api
        }
      }
    } catch (error) {
      console.error('Plugin initialization failed:', error)
      // Provide fallback or skip
    }
  }
})

// Client-only plugin
export default defineNuxtPlugin({
  name: 'client-only-plugin',
  setup() {
    // This only runs on client
  }
})
// Name file: plugins/my-plugin.client.ts
```

### 5. Module Conflicts

**Diagnosing Module Issues:**
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    // Module order can matter!
  ],

  // Debug module loading
  debug: true, // Shows module loading in console
})
```

**Common Module Conflicts:**
```bash
# Clear module cache
rm -rf node_modules/.cache
rm -rf .nuxt

# Reinstall dependencies
rm -rf node_modules
npm install
```

## Debugging Tools

### 1. Nuxt DevTools (Recommended)

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true }
})
```

**Features:**
- Component inspector and tree
- Pages and routing visualization
- Composables state inspection
- Server routes overview
- Module dependencies
- Payload inspection
- Timeline for performance

**Access:** Press `Shift + Alt + D` or click floating icon in dev mode

### 2. Sourcemaps Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  sourcemap: {
    server: true,
    client: true
  }
})
```

### 3. VS Code Debugging

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Debug Nuxt Client",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}"
    },
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Nuxt Server",
      "program": "${workspaceFolder}/node_modules/nuxi/bin/nuxi.mjs",
      "args": ["dev"],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### 4. Node Inspector (Server-Side)

```bash
# Start with debugger
nuxi dev --inspect

# Or with specific host for Docker
nuxi dev --inspect=0.0.0.0
```

### 5. Console Logging (Server vs Client)

```typescript
// Runs on both server and client
console.log('Universal log')

// Server-only logging
if (process.server) {
  console.log('Server-side only')
}

// Client-only logging
if (process.client) {
  console.log('Client-side only')
}

// In composables
const nuxtApp = useNuxtApp()
if (nuxtApp.ssrContext) {
  console.log('Server-side render')
}
```

### 6. Vue DevTools

```bash
# Install Vue DevTools browser extension
# Or use standalone
npx @vue/devtools
```

## The Four Phases of Nuxt Debugging

### Phase 1: Identify the Context

Determine where the error occurs:

```typescript
// Check execution context
console.log('Server:', process.server)
console.log('Client:', process.client)
console.log('Dev:', process.dev)
console.log('SSR:', !!useNuxtApp().ssrContext)
```

**Questions to answer:**
- Does it happen during SSR, hydration, or client navigation?
- Is it a build-time or runtime error?
- Does it only happen on certain routes?
- Is it reproducible in development AND production?

### Phase 2: Isolate the Component

```vue
<template>
  <div>
    <!-- Wrap suspect components -->
    <NuxtErrorBoundary @error="logError">
      <SuspectComponent />
      <template #error="{ error }">
        <p>Error: {{ error.message }}</p>
      </template>
    </NuxtErrorBoundary>
  </div>
</template>

<script setup>
function logError(error) {
  console.error('Caught error:', error)
}
</script>
```

### Phase 3: Check Data Flow

```typescript
// Debug useFetch/useAsyncData
const { data, error, pending, status } = useFetch('/api/data')

watch([data, error, pending], ([d, e, p]) => {
  console.log('Data:', d)
  console.log('Error:', e)
  console.log('Pending:', p)
})

// Check payload (what's sent from server to client)
const nuxtApp = useNuxtApp()
console.log('Payload:', nuxtApp.payload)
```

### Phase 4: Verify Build and Config

```bash
# Type check
nuxi typecheck

# Analyze bundle
nuxi analyze

# Clean build
rm -rf .nuxt .output node_modules/.cache
nuxi build
```

## Quick Reference Commands

### Development

```bash
# Start dev server
nuxi dev

# Start with debugging
nuxi dev --inspect

# Start on specific port
nuxi dev --port 3001

# Start with HTTPS
nuxi dev --https
```

### Building and Analysis

```bash
# Production build
nuxi build

# Generate static site
nuxi generate

# Preview production build
nuxi preview

# Analyze bundle size
nuxi analyze

# Type checking
nuxi typecheck

# Prepare Nuxt (generate types)
nuxi prepare
```

### Maintenance

```bash
# Clean Nuxt files
nuxi cleanup

# Upgrade Nuxt
nuxi upgrade

# Add module
nuxi module add @nuxtjs/tailwindcss

# Create new component/page/etc
nuxi add component MyComponent
nuxi add page about
nuxi add composable useMyComposable
nuxi add api hello
```

## Error Handling Patterns

### Global Error Handler

```typescript
// plugins/error-handler.ts
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.config.errorHandler = (error, instance, info) => {
    console.error('Vue Error:', error)
    console.error('Component:', instance)
    console.error('Info:', info)
  }

  nuxtApp.hook('vue:error', (error, instance, info) => {
    console.error('Nuxt Vue Error Hook:', error)
  })

  nuxtApp.hook('app:error', (error) => {
    console.error('App Error:', error)
  })
})
```

### Custom Error Page

```vue
<!-- error.vue (in root, NOT in pages/) -->
<template>
  <div class="error-page">
    <h1>{{ error.statusCode }}</h1>
    <p>{{ error.message }}</p>
    <button @click="handleError">Go Home</button>
  </div>
</template>

<script setup>
const props = defineProps({
  error: Object
})

const handleError = () => clearError({ redirect: '/' })
</script>
```

### Programmatic Error Handling

```typescript
// Throw errors
throw createError({
  statusCode: 404,
  statusMessage: 'Page not found',
  fatal: true // Triggers error page
})

// Show error without navigation
showError({
  statusCode: 500,
  statusMessage: 'Something went wrong'
})

// Clear error
clearError({ redirect: '/' })

// Access current error
const error = useError()
```

### Error Boundary for Components

```vue
<template>
  <NuxtErrorBoundary>
    <RiskyComponent />

    <template #error="{ error, clearError }">
      <div class="error-box">
        <p>Component failed: {{ error.message }}</p>
        <button @click="clearError">Retry</button>
      </div>
    </template>
  </NuxtErrorBoundary>
</template>
```

## SSR-Specific Debugging

### Payload Issues

```typescript
// Debug what's in the payload
const nuxtApp = useNuxtApp()
onMounted(() => {
  console.log('SSR Payload:', nuxtApp.payload)
  console.log('SSR Data:', nuxtApp.payload.data)
  console.log('SSR State:', nuxtApp.payload.state)
})
```

### Async Data Not Available

```typescript
// Ensure data is awaited properly
const { data } = await useFetch('/api/data')

// For lazy loading (doesn't block navigation)
const { data, pending } = useLazyFetch('/api/data')

// Watch for data availability
watch(data, (newData) => {
  if (newData) {
    console.log('Data loaded:', newData)
  }
})
```

### Server-Only Code Leaking to Client

```typescript
// Use server utilities correctly
// server/utils/db.ts - only available in server/

// For runtime config (secrets)
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    apiSecret: '', // Server-only
    public: {
      apiBase: '' // Exposed to client
    }
  }
})

// Usage
const config = useRuntimeConfig()
// config.apiSecret - only on server
// config.public.apiBase - available everywhere
```

## Performance Debugging

### Identify Slow Components

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  experimental: {
    componentIslands: true // For heavy components
  }
})
```

```vue
<!-- Use islands for heavy server components -->
<NuxtIsland name="HeavyChart" :props="{ data: chartData }" />
```

### Lazy Loading

```typescript
// Lazy load components
const HeavyComponent = defineAsyncComponent(() =>
  import('~/components/HeavyComponent.vue')
)

// Or use Nuxt's auto-import with Lazy prefix
<template>
  <LazyHeavyComponent v-if="showHeavy" />
</template>
```

### Bundle Analysis

```bash
# Generate bundle analysis
nuxi analyze

# Check what's in your bundle
cat .output/public/_nuxt/builds/meta/*.json | jq
```

## Common Gotchas

### 1. Composables Must Be Called in Setup

```typescript
// BAD
function handleClick() {
  const route = useRoute() // Error!
}

// GOOD
const route = useRoute()
function handleClick() {
  console.log(route.path)
}
```

### 2. Reactive Data in useFetch

```typescript
// BAD: Non-reactive
const id = '123'
useFetch(`/api/items/${id}`)

// GOOD: Reactive
const id = ref('123')
useFetch(() => `/api/items/${id.value}`)
```

### 3. Navigate vs Router

```typescript
// Prefer navigateTo over useRouter for navigation
await navigateTo('/dashboard')
await navigateTo({ path: '/user', query: { id: 1 } })

// For programmatic redirects in server
export default defineEventHandler((event) => {
  return sendRedirect(event, '/login', 302)
})
```

### 4. Middleware Execution Order

```typescript
// Named middleware runs in alphabetical order
// middleware/01.auth.global.ts runs before middleware/02.analytics.global.ts

// Route-specific middleware
definePageMeta({
  middleware: ['auth', 'premium'] // Runs in order
})
```

### 5. State Pollution in SSR

```typescript
// BAD: Shared state between requests
const globalState = reactive({})

// GOOD: Use useState for SSR-safe state
const state = useState('key', () => ({}))

// Or Pinia with proper SSR setup
const store = useMyStore()
```

## Resources

- [Nuxt Documentation - Debugging](https://nuxt.com/docs/guide/going-further/debugging)
- [Nuxt DevTools](https://devtools.nuxt.com/)
- [Nuxt Error Handling](https://nuxt.com/docs/getting-started/error-handling)
- [Vue DevTools](https://devtools.vuejs.org/)
- [Nuxt GitHub Discussions](https://github.com/nuxt/nuxt/discussions)

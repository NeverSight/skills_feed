---
name: pinia
description: Pinia state management for JARVIS system state
model: sonnet
risk_level: MEDIUM
version: 1.0.0
---

# Pinia State Management Skill

> **File Organization**: This skill uses split structure. See `references/` for advanced patterns and security examples.

## 1. Overview

This skill provides Pinia expertise for managing application state in the JARVIS AI Assistant, including system metrics, user preferences, and HUD configuration.

**Risk Level**: MEDIUM - Manages sensitive state, SSR considerations, potential data exposure

**Primary Use Cases**:
- System metrics and status tracking
- User preferences and settings
- HUD configuration state
- Command history and queue
- Real-time data synchronization

## 2. Core Responsibilities

### 2.1 Core Principles

1. **TDD First**: Write store tests before implementation
2. **Performance Aware**: Optimize subscriptions and computed values
3. **Type Safety**: Define stores with full TypeScript typing
4. **SSR Security**: Prevent state leakage between requests
5. **Composition API**: Use setup stores for better TypeScript support
6. **Minimal State**: Store only necessary data, derive the rest
7. **Action Validation**: Validate inputs in actions before mutations
8. **Persistence Security**: Never persist sensitive data to localStorage

## 3. Technology Stack & Versions

### 3.1 Recommended Versions

| Package | Version | Notes |
|---------|---------|-------|
| pinia | ^2.1.0 | Latest stable |
| @pinia/nuxt | ^0.5.0 | Nuxt integration |
| pinia-plugin-persistedstate | ^3.0.0 | Optional persistence |

### 3.2 Nuxt Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@pinia/nuxt'],
  pinia: {
    storesDirs: ['./stores/**']
  }
})
```

### 3.3 Implementation Workflow (TDD)

Follow this workflow for every store:

**Step 1: Write Failing Test First**

```typescript
// tests/stores/metrics.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useMetricsStore } from '~/stores/metrics'

describe('MetricsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with default values', () => {
    const store = useMetricsStore()
    expect(store.cpu).toBe(0)
    expect(store.memory).toBe(0)
  })

  it('should clamp values within valid range', () => {
    const store = useMetricsStore()
    store.updateCpu(150)
    expect(store.cpu).toBe(100)
    store.updateCpu(-50)
    expect(store.cpu).toBe(0)
  })

  it('should compute health status correctly', () => {
    const store = useMetricsStore()
    store.updateCpu(95)
    store.updateMemory(90)
    expect(store.healthStatus).toBe('critical')
  })
})
```

**Step 2: Implement Minimum to Pass**

```typescript
// stores/metrics.ts
export const useMetricsStore = defineStore('metrics', () => {
  const cpu = ref(0)
  const memory = ref(0)

  const healthStatus = computed(() => {
    const avg = (cpu.value + memory.value) / 2
    if (avg > 90) return 'critical'
    if (avg > 70) return 'warning'
    return 'healthy'
  })

  function updateCpu(value: number) {
    cpu.value = Math.max(0, Math.min(100, value))
  }

  function updateMemory(value: number) {
    memory.value = Math.max(0, Math.min(100, value))
  }

  return { cpu, memory, healthStatus, updateCpu, updateMemory }
})
```

**Step 3: Refactor Following Patterns**

- Extract validation logic
- Add TypeScript interfaces
- Optimize computed dependencies

**Step 4: Run Full Verification**

```bash
npm run test -- --filter=stores
npm run typecheck
npm run build
```

## 4. Implementation Patterns

### 4.1 Setup Store with TypeScript

```typescript
// stores/jarvis.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface SystemMetrics {
  cpu: number
  memory: number
  network: number
  timestamp: number
}

interface JARVISState {
  status: 'idle' | 'listening' | 'processing' | 'responding'
  securityLevel: 'normal' | 'elevated' | 'lockdown'
}

export const useJarvisStore = defineStore('jarvis', () => {
  // State
  const state = ref<JARVISState>({
    status: 'idle',
    securityLevel: 'normal'
  })

  const metrics = ref<SystemMetrics>({
    cpu: 0,
    memory: 0,
    network: 0,
    timestamp: Date.now()
  })

  // Getters
  const isActive = computed(() =>
    state.value.status !== 'idle'
  )

  const systemHealth = computed(() => {
    const avg = (metrics.value.cpu + metrics.value.memory) / 2
    if (avg > 90) return 'critical'
    if (avg > 70) return 'warning'
    return 'healthy'
  })

  // Actions
  function updateMetrics(newMetrics: Partial<SystemMetrics>) {
    // ✅ Validate input
    if (newMetrics.cpu !== undefined) {
      metrics.value.cpu = Math.max(0, Math.min(100, newMetrics.cpu))
    }
    if (newMetrics.memory !== undefined) {
      metrics.value.memory = Math.max(0, Math.min(100, newMetrics.memory))
    }
    if (newMetrics.network !== undefined) {
      metrics.value.network = Math.max(0, newMetrics.network)
    }
    metrics.value.timestamp = Date.now()
  }

  function setStatus(newStatus: JARVISState['status']) {
    state.value.status = newStatus
  }

  function setSecurityLevel(level: JARVISState['securityLevel']) {
    state.value.securityLevel = level

    // ✅ Audit security changes
    console.info(`Security level changed to: ${level}`)
  }

  return {
    state,
    metrics,
    isActive,
    systemHealth,
    updateMetrics,
    setStatus,
    setSecurityLevel
  }
})
```

### 4.2 User Preferences Store (with Persistence)

```typescript
// stores/preferences.ts
export const usePreferencesStore = defineStore('preferences', () => {
  const preferences = ref({
    theme: 'dark' as 'dark' | 'light',
    hudOpacity: 0.8,
    soundEnabled: true
  })

  function updatePreference<K extends keyof typeof preferences.value>(
    key: K, value: typeof preferences.value[K]
  ) {
    if (key === 'hudOpacity' && (value < 0 || value > 1)) return
    preferences.value[key] = value
  }

  return { preferences, updatePreference }
}, {
  persist: {
    key: 'jarvis-preferences',
    paths: ['preferences.theme', 'preferences.hudOpacity']
    // ❌ Never persist: tokens, passwords, API keys
  }
})
```

### 4.3 Command Queue Store

```typescript
// stores/commands.ts
interface Command {
  id: string
  action: string
  status: 'pending' | 'executing' | 'completed' | 'failed'
}

export const useCommandStore = defineStore('commands', () => {
  const queue = ref<Command[]>([])
  const history = ref<Command[]>([])
  const MAX_HISTORY = 100

  const pendingCommands = computed(() =>
    queue.value.filter(cmd => cmd.status === 'pending')
  )

  function addCommand(action: string) {
    const cmd: Command = { id: crypto.randomUUID(), action, status: 'pending' }
    queue.value.push(cmd)
    return cmd.id
  }

  function completeCommand(id: string, status: 'completed' | 'failed') {
    const idx = queue.value.findIndex(cmd => cmd.id === id)
    if (idx !== -1) {
      const [cmd] = queue.value.splice(idx, 1)
      cmd.status = status
      history.value = [cmd, ...history.value].slice(0, MAX_HISTORY)
    }
  }

  return { queue, history, pendingCommands, addCommand, completeCommand }
})
```

### 4.4 SSR-Safe Store Usage

```vue
<script setup lang="ts">
// ✅ Safe for SSR - store initialized per-request
const jarvisStore = useJarvisStore()

// ✅ Fetch data on server
const { data } = await useFetch('/api/metrics')

// Update store with fetched data
if (data.value) {
  jarvisStore.updateMetrics(data.value)
}
</script>
```

### 4.5 Store Composition

```typescript
// stores/dashboard.ts
export const useDashboardStore = defineStore('dashboard', () => {
  // ✅ Compose from other stores
  const jarvisStore = useJarvisStore()
  const commandStore = useCommandStore()

  const dashboardStatus = computed(() => ({
    systemHealth: jarvisStore.systemHealth,
    pendingCommands: commandStore.pendingCommands.length,
    isActive: jarvisStore.isActive
  }))

  return {
    dashboardStatus
  }
})
```

## 5. Security Standards

### 5.1 OWASP Coverage

| OWASP Category | Risk | Mitigation |
|----------------|------|------------|
| A01 Broken Access Control | MEDIUM | Validate actions, check permissions |
| A04 Insecure Design | MEDIUM | SSR state isolation |
| A07 Auth Failures | MEDIUM | Never persist tokens |

### 5.3 Sensitive Data Handling

```typescript
// ❌ NEVER persist: tokens, API keys, passwords
// ✅ Store sensitive data in memory only (no persist option)
const authStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  return { token }
})
```

## 5.5 Performance Patterns

### Pattern 1: Selective Subscriptions

```typescript
// BAD - Subscribes to entire store
const store = useJarvisStore()
watch(() => store.state, () => { /* ... */ }, { deep: true })

// GOOD - Subscribe to specific properties
const store = useJarvisStore()
watch(() => store.state.status, (newStatus) => {
  console.log('Status changed:', newStatus)
})
```

### Pattern 2: Computed Getters (Memoization)

```typescript
// BAD - Recalculates on every access
function getFilteredItems() {
  return items.value.filter(i => i.active)
}

// GOOD - Cached until dependencies change
const filteredItems = computed(() =>
  items.value.filter(i => i.active)
)
```

### Pattern 3: Batch Updates

```typescript
// BAD - Multiple reactive triggers
function updateAll(data: MetricsData) {
  metrics.value.cpu = data.cpu
  metrics.value.memory = data.memory
  metrics.value.network = data.network
}

// GOOD - Single reactive trigger
function updateAll(data: MetricsData) {
  metrics.value = { ...metrics.value, ...data, timestamp: Date.now() }
}
```

### Pattern 4: Lazy Store Initialization

```typescript
// BAD - Store initializes immediately
const heavyStore = useHeavyDataStore()

// GOOD - Initialize only when needed
const heavyStore = ref<ReturnType<typeof useHeavyDataStore> | null>(null)

function loadHeavyData() {
  if (!heavyStore.value) {
    heavyStore.value = useHeavyDataStore()
  }
  return heavyStore.value
}
```

### Pattern 5: Optimistic Updates

```typescript
// BAD - Wait for server response
async function deleteItem(id: string) {
  await api.delete(`/items/${id}`)
  items.value = items.value.filter(i => i.id !== id)
}

// GOOD - Update immediately, rollback on error
async function deleteItem(id: string) {
  const backup = [...items.value]
  items.value = items.value.filter(i => i.id !== id)

  try {
    await api.delete(`/items/${id}`)
  } catch (error) {
    items.value = backup  // Rollback
    throw error
  }
}
```

## 6. Testing & Quality

See **Section 3.3** for complete TDD workflow with vitest examples.

## 8. Common Anti-Patterns

### Security Anti-Patterns

```typescript
// ❌ Global state leaks between SSR users
const state = reactive({ user: null })

// ✅ Pinia isolates per-request
export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  return { user }
})

// ❌ Never persist auth tokens (XSS risk)
persist: { paths: ['authToken'] }

// ✅ Use httpOnly cookies for auth
```

### Performance Anti-Patterns

See **Section 5.5** for detailed performance patterns with Good/Bad examples.

## 13. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Store interface designed with TypeScript types
- [ ] Test file created with failing tests
- [ ] Security requirements identified (persistence, SSR)
- [ ] Performance patterns selected for use case

### Phase 2: During Implementation

- [ ] Tests passing after each feature added
- [ ] Actions validate all inputs
- [ ] Computed values use minimal dependencies
- [ ] No sensitive data in persisted state
- [ ] SSR state properly isolated

### Phase 3: Before Committing

- [ ] All store tests passing: `npm run test -- --filter=stores`
- [ ] Type check passing: `npm run typecheck`
- [ ] Build succeeds: `npm run build`
- [ ] No global state outside Pinia
- [ ] State shape documented in types

## 14. Summary

Pinia provides type-safe state management for JARVIS:

1. **TDD First**: Write store tests before implementation
2. **Performance**: Optimize subscriptions and computed values
3. **Security**: Never persist sensitive data, isolate SSR state
4. **Type Safety**: Use setup stores with full TypeScript

**References**: See `references/` for advanced patterns and security examples.

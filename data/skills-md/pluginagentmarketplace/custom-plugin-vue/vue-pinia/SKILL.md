---
name: vue-pinia
description: Master Pinia State Management - Stores, Actions, Getters, Plugins, Persistence
sasmp_version: "1.3.0"
bonded_agent: 03-vue-pinia
bond_type: PRIMARY_BOND
version: "2.0.0"
last_updated: "2025-01"
---

# Vue Pinia Skill

Production-grade skill for mastering Pinia state management in Vue applications.

## Purpose

**Single Responsibility:** Teach scalable state management patterns with Pinia including store design, actions, getters, plugins, and persistence strategies.

## Parameter Schema

```typescript
interface PiniaParams {
  topic: 'stores' | 'actions' | 'getters' | 'plugins' | 'persistence' | 'all';
  level: 'beginner' | 'intermediate' | 'advanced';
  context?: {
    app_size?: 'small' | 'medium' | 'large';
    existing_state?: string[];
  };
}
```

## Learning Modules

### Module 1: Store Fundamentals
```
Prerequisites: vue-composition-api
Duration: 2-3 hours
Outcome: Create and use Pinia stores
```

| Topic | Concept | Exercise |
|-------|---------|----------|
| Setup | Install and configure | App setup |
| defineStore | Create stores | Counter store |
| State | Reactive state | User store |
| Using stores | storeToRefs | Component access |

**Store Syntax Comparison:**
```typescript
// Options Store
defineStore('counter', {
  state: () => ({ count: 0 }),
  getters: { double: (s) => s.count * 2 },
  actions: { increment() { this.count++ } }
})

// Setup Store (Recommended)
defineStore('counter', () => {
  const count = ref(0)
  const double = computed(() => count.value * 2)
  function increment() { count.value++ }
  return { count, double, increment }
})
```

### Module 2: Actions & Async
```
Prerequisites: Module 1
Duration: 2-3 hours
Outcome: Handle async operations
```

| Pattern | Use Case | Exercise |
|---------|----------|----------|
| Sync actions | Simple mutations | Cart updates |
| Async actions | API calls | Fetch users |
| Error handling | Try/catch | Error states |
| Loading states | UX feedback | Spinners |
| Optimistic updates | Fast UX | Instant feedback |

### Module 3: Getters & Computed
```
Prerequisites: Module 2
Duration: 1-2 hours
Outcome: Derive and filter state
```

| Pattern | Use Case | Exercise |
|---------|----------|----------|
| Simple getter | Derived value | Full name |
| Parameterized | Filtered access | Find by ID |
| Cross-store | Compose stores | Cart with products |
| Memoization | Performance | Expensive calcs |

### Module 4: Store Architecture
```
Prerequisites: Modules 1-3
Duration: 3-4 hours
Outcome: Design scalable store structure
```

**Architecture Patterns:**

```
stores/
├── modules/
│   ├── useUserStore.ts      # User domain
│   ├── useProductStore.ts   # Product domain
│   └── useCartStore.ts      # Cart domain
├── shared/
│   └── useNotificationStore.ts
└── index.ts                  # Re-exports
```

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| Domain stores | One per feature | Large apps |
| Composed stores | Store uses store | Related data |
| Normalized state | ID-based lookup | Many entities |
| Module pattern | Organized exports | Team projects |

### Module 5: Plugins & Persistence
```
Prerequisites: Modules 1-4
Duration: 2-3 hours
Outcome: Extend Pinia functionality
```

| Plugin | Function | Exercise |
|--------|----------|----------|
| Logger | Dev debugging | Action logging |
| Persisted State | LocalStorage | Auth persistence |
| Reset | State reset | Logout cleanup |
| Custom | Domain-specific | Analytics |

## Validation Checkpoints

### Beginner Checkpoint
- [ ] Create basic store with state
- [ ] Use storeToRefs in component
- [ ] Implement simple action
- [ ] Access getter value

### Intermediate Checkpoint
- [ ] Build async action with loading/error
- [ ] Create parameterized getter
- [ ] Compose two stores together
- [ ] Add persistence plugin

### Advanced Checkpoint
- [ ] Design normalized store structure
- [ ] Implement optimistic updates
- [ ] Create custom plugin
- [ ] Test stores in isolation

## Retry Logic

```typescript
const skillConfig = {
  maxAttempts: 3,
  backoffMs: [1000, 2000, 4000],
  onFailure: 'simplify_store_design'
}
```

## Observability

```yaml
tracking:
  - event: store_created
    data: [store_name, store_type]
  - event: pattern_applied
    data: [pattern_name, success]
  - event: skill_completed
    data: [stores_built, complexity]
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Store not reactive | Destructured state | Use storeToRefs() |
| Circular dependency | A→B→A imports | Lazy import or reorganize |
| No active Pinia | Used before app.use | Check setup order |
| HMR not working | Missing acceptHMRUpdate | Add HMR config |

### Debug Steps

1. Check Pinia devtools for state
2. Verify store ID is unique
3. Confirm pinia plugin is installed
4. Check for circular store imports

## Unit Test Template

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from './useUserStore'

describe('useUserStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with null user', () => {
    const store = useUserStore()
    expect(store.user).toBeNull()
  })

  it('logs in user correctly', async () => {
    const store = useUserStore()
    await store.login({ email: 'test@example.com' })
    expect(store.isLoggedIn).toBe(true)
  })

  it('logs out and clears state', () => {
    const store = useUserStore()
    store.$patch({ user: { id: '1', name: 'Test' } })
    store.logout()
    expect(store.user).toBeNull()
  })
})
```

## Usage

```
Skill("vue-pinia")
```

## Related Skills

- `vue-composition-api` - Prerequisite
- `vue-typescript` - Typed stores
- `vue-testing` - Store testing

## Resources

- [Pinia Documentation](https://pinia.vuejs.org/)
- [Pinia Best Practices](https://pinia.vuejs.org/cookbook/)
- [pinia-plugin-persistedstate](https://prazdevs.github.io/pinia-plugin-persistedstate/)

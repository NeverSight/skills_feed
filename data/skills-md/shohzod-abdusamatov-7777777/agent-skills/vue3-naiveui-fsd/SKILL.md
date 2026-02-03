---
name: vue3-naiveui-fsd
description: Senior-level Vue 3 + Naive UI + Feature-Sliced Design with TypeScript, Clean Code & SOLID principles
version: 2.0.0
triggers:
  - vue
  - naive ui
  - naiveui
  - fsd
  - feature sliced
  - vue 3
  - composition api
---

# Vue 3 + Naive UI + FSD Senior Development Skill

Expert-level skill for building production-ready Vue 3 applications with Naive UI, Feature-Sliced Design architecture, TypeScript, and industry best practices.

## Tech Stack

- **Vue 3** with Composition API (`<script setup>`)
- **Naive UI v2.43+** component library
- **Feature-Sliced Design (FSD)** architecture
- **TypeScript** with strict mode
- **Pinia** for state management
- **Vue Router 4** for routing
- **Tailwind CSS v4** for utility styles
- **Axios** for HTTP requests
- **Day.js** for date handling
- **Lucide Vue Next** for icons
- **Vue I18n** for internationalization

## References

Detailed documentation is organized in the `references/` folder:

| File | Description |
|------|-------------|
| [fsd-architecture.md](references/fsd-architecture.md) | FSD directory structure and layer rules |
| [api-layer.md](references/api-layer.md) | Axios setup, interceptors, service pattern |
| [types.md](references/types.md) | TypeScript patterns, I-prefix convention |
| [stores.md](references/stores.md) | Pinia global stores (auth, operation) |
| [composables.md](references/composables.md) | usePagination, useValidationRules, useTheme |
| [forms.md](references/forms.md) | Form composable pattern (useXxxForm) |
| [pages.md](references/pages.md) | Page component with table, CRUD |
| [shared-ui.md](references/shared-ui.md) | BaseTable, BaseModal, buttons |
| [utilities.md](references/utilities.md) | Formatters, helpers |
| [router.md](references/router.md) | Router config, guards, loading bar |

## Quick Start Patterns

### Component Structure
```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { NCard, NButton } from 'naive-ui'
import type { IUser } from '@/entities/user'

const props = defineProps<{ userId: number }>()
const emit = defineEmits<{ success: [] }>()

const loading = ref(false)
// ... logic
</script>

<template>
  <NCard>
    <!-- content -->
  </NCard>
</template>
```

### FSD Layer Import Rules
```
app     → pages, features, entities, shared
pages   → features, entities, shared
features → entities, shared
entities → shared only
shared  → nothing (self-contained)
```

### Type Naming Convention
```typescript
IUser         // Base entity
IUserList     // List item (simplified)
IUserDetail   // Full detail
IUserForm     // Form data
IUserListParams // Query params
```

## Code Quality Checklist

- [ ] TypeScript strict mode passes
- [ ] Types use `I` prefix convention
- [ ] FSD layer boundaries respected
- [ ] API services in `shared/api/`
- [ ] Form logic in composables (`useXxxForm`)
- [ ] Pagination uses `usePagination`
- [ ] Validation uses `useValidationRules`
- [ ] i18n for all user-facing text
- [ ] Loading/error states handled

---
name: nuxt-tanstack-mastery
description: |
  Panduan senior/lead developer 20 tahun pengalaman untuk Vue.js 3 + Nuxt 3 + TanStack Query development. 
  Gunakan skill ini ketika: (1) Membuat project Nuxt 3 baru dengan arsitektur production-ready, (2) Integrasi TanStack Query untuk data fetching, (3) Debugging Vue/Nuxt yang kompleks, (4) Review code untuk clean code compliance, (5) Optimisasi performa aplikasi Vue/Nuxt, (6) Setup folder structure yang scalable, (7) Mencari library terpercaya untuk Vue ecosystem, (8) Menghindari common pitfalls dan bugs, (9) Implementasi state management patterns, (10) Security hardening aplikasi Nuxt.
  Trigger keywords: vue, vuejs, nuxt, nuxtjs, tanstack, vue-query, composition api, pinia, vueuse, vue router, clean code vue, debugging vue, folder structure nuxt.
---

# Nuxt 3 + TanStack Query Mastery

> Filosofi: **"Simplicity is the ultimate sophistication"** — Write code that your future self will thank you for.

## Core Principles (WAJIB dipatuhi)

```
┌─────────────────────────────────────────────────────────────────┐
│  1. KISS (Keep It Stupid Simple) - Jangan over-engineer        │
│  2. YAGNI (You Ain't Gonna Need It) - Build for today          │
│  3. DRY (Don't Repeat Yourself) - Tapi jangan premature DRY    │
│  4. Composition over Inheritance - Favor composables           │
│  5. Single Responsibility - One function, one job              │
│  6. Explicit over Implicit - Readable > clever                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Decision Matrix

| Kebutuhan | Solusi | Referensi |
|-----------|--------|-----------|
| Data fetching + caching | TanStack Query | [tanstack-query.md](references/tanstack-query.md) |
| Global state sederhana | Pinia | [state-management.md](references/state-management.md) |
| Utility functions | VueUse | [libraries.md](references/libraries.md) |
| Form handling | VeeValidate + Zod | [libraries.md](references/libraries.md) |
| Debugging | Vue DevTools + patterns | [debugging.md](references/debugging.md) |
| Folder structure | Feature-based | [folder-structure.md](references/folder-structure.md) |
| Performance issues | Profiling + lazy load | [performance.md](references/performance.md) |
| Security concerns | CSP + validation | [security.md](references/security.md) |
| Common bugs | Reactivity gotchas | [common-pitfalls.md](references/common-pitfalls.md) |

## Reference Files

Baca reference yang relevan berdasarkan kebutuhan:

- **[references/folder-structure.md](references/folder-structure.md)** — Struktur folder production-ready dengan penjelasan setiap direktori
- **[references/tanstack-query.md](references/tanstack-query.md)** — TanStack Query patterns, caching strategies, optimistic updates
- **[references/clean-code.md](references/clean-code.md)** — Clean code principles, naming conventions, composables patterns
- **[references/debugging.md](references/debugging.md)** — Debugging techniques, common errors, troubleshooting guide
- **[references/performance.md](references/performance.md)** — Performance optimization, lazy loading, bundle analysis
- **[references/security.md](references/security.md)** — Security best practices, XSS prevention, auth patterns
- **[references/common-pitfalls.md](references/common-pitfalls.md)** — Bugs yang sering terjadi dan cara menghindarinya
- **[references/libraries.md](references/libraries.md)** — Curated list library terpercaya dengan use cases
- **[references/state-management.md](references/state-management.md)** — Pinia patterns, when to use what
- **[references/code-examples.md](references/code-examples.md)** — Real-world code examples dan patterns

## Golden Rules (Cetak dalam otak)

### 1. Composables adalah Raja
```typescript
// ❌ JANGAN: Logic di component
const MyComponent = {
  setup() {
    const data = ref([])
    const loading = ref(false)
    const fetchData = async () => { /* ... */ }
    // 50 lines of logic...
  }
}

// ✅ LAKUKAN: Extract ke composable
// composables/useProducts.ts
export function useProducts() {
  const { data, isLoading } = useQuery({ /* ... */ })
  return { products: data, isLoading }
}

// Component menjadi bersih
const { products, isLoading } = useProducts()
```

### 2. TypeScript adalah Non-negotiable
```typescript
// ❌ any = technical debt
const data: any = await fetch()

// ✅ Type everything
interface Product {
  id: string
  name: string
  price: number
}
const data: Product[] = await fetch()
```

### 3. Error Boundaries WAJIB ada
```vue
<!-- Wrap setiap section dengan error boundary -->
<NuxtErrorBoundary>
  <ProductList />
  <template #error="{ error }">
    <ErrorDisplay :error="error" />
  </template>
</NuxtErrorBoundary>
```

### 4. Reactivity dengan Benar
```typescript
// ❌ Reactivity loss
const { data } = useQuery()
const items = data.value // Loss reactivity!

// ✅ Preserve reactivity
const { data } = useQuery()
const items = computed(() => data.value ?? [])
```

## Project Bootstrap Command

```bash
# Nuxt 3 + TanStack Query + Essential tools
npx nuxi@latest init my-app
cd my-app
npm install @tanstack/vue-query @pinia/nuxt @vueuse/nuxt zod @vee-validate/nuxt
npm install -D @nuxt/devtools typescript @types/node
```

## Checklist Sebelum Production

- [ ] TypeScript strict mode enabled
- [ ] Error boundaries di setiap route
- [ ] Loading states untuk semua async operations
- [ ] Input validation dengan Zod
- [ ] Environment variables di `.env` (bukan hardcode)
- [ ] Bundle size < 200KB initial JS
- [ ] Lighthouse score > 90
- [ ] Security headers configured
- [ ] Rate limiting untuk API calls
- [ ] Proper caching strategy dengan TanStack Query

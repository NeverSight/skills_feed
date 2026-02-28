---
name: react-tanstack-senior
description: |
  Expertise senior/lead React developer 20 tahun dengan TanStack ecosystem (Query, Router, Table, Form, Start). Gunakan skill ini ketika: (1) Membuat aplikasi React dengan TanStack libraries, (2) Review/refactor kode React untuk clean code, (3) Debugging React/TanStack issues, (4) Setup project structure yang maintainable, (5) Optimasi performa React apps, (6) Memilih library yang tepat untuk use case tertentu, (7) Mencegah common bugs dan memory leaks, (8) Implementasi best practices KISS dan less is more. Trigger keywords: React, TanStack, React Query, TanStack Router, TanStack Table, TanStack Form, TanStack Start, Vinxi, clean code, refactor, performance, debugging.
---

# React + TanStack Senior Developer Skill

## Core Philosophy

```
KISS > Clever Code
Readability > Brevity  
Explicit > Implicit
Composition > Inheritance
Colocation > Separation
Type Safety > Any
```

## Quick Decision Tree

**State Management:**
- Server state → TanStack Query (WAJIB)
- URL state → TanStack Router search params
- Form state → TanStack Form atau React Hook Form
- Global UI state → Zustand (bukan Redux)
- Local UI state → useState/useReducer

**Routing:**
- SPA → TanStack Router
- Full-stack SSR → TanStack Start
- Existing Next.js → tetap Next.js

## Project Setup Workflow

1. **Determine project type:**
   - **SPA/Client-only?** → Vite + TanStack Router + Query
   - **Full-stack SSR?** → TanStack Start (Vinxi-based)
   - **Existing project?** → Incremental adoption

2. **Initialize project** → See [folder-structure.md](references/folder-structure.md)

3. **Setup core dependencies** → See [recommended-libraries.md](references/recommended-libraries.md)

## TanStack Ecosystem References

| Library | When to Read |
|---------|--------------|
| [tanstack-query.md](references/tanstack-query.md) | Data fetching, caching, mutations |
| [tanstack-router.md](references/tanstack-router.md) | Type-safe routing, loaders, search params |
| [tanstack-table.md](references/tanstack-table.md) | Complex tables, sorting, filtering, pagination |
| [tanstack-form.md](references/tanstack-form.md) | Form validation, field arrays, async validation |
| [tanstack-start.md](references/tanstack-start.md) | Full-stack SSR framework |

## Code Quality Standards

### Naming Conventions

```typescript
// Components: PascalCase dengan suffix deskriptif
UserProfileCard.tsx      // ✓
UserCard.tsx             // ✗ terlalu generic
user-profile.tsx         // ✗ wrong case

// Hooks: camelCase dengan prefix 'use'
useUserProfile()         // ✓
useGetUserProfile()      // ✗ redundant 'Get'
getUserProfile()         // ✗ missing 'use'

// Query keys: array dengan hierarchy
['users', 'list', { status }]           // ✓
['usersList']                            // ✗ tidak granular
`users-${status}`                        // ✗ string interpolation

// Files: kebab-case untuk non-components
api-client.ts            // ✓
apiClient.ts             // ✗ 
```

### Component Structure Pattern

```typescript
// 1. Imports (grouped: external → internal → types)
import { useSuspenseQuery } from '@tanstack/react-query'
import { userQueries } from '@/features/users/api'
import type { User } from '@/features/users/types'

// 2. Types (colocated, tidak di file terpisah kecuali shared)
interface UserCardProps {
  userId: string
  onSelect?: (user: User) => void
}

// 3. Component (single responsibility)
export function UserCard({ userId, onSelect }: UserCardProps) {
  // 3a. Queries/mutations first
  const { data: user } = useSuspenseQuery(userQueries.detail(userId))
  
  // 3b. Derived state (useMemo hanya jika expensive)
  const fullName = `${user.firstName} ${user.lastName}`
  
  // 3c. Handlers (useCallback hanya jika passed to memoized children)
  const handleClick = () => onSelect?.(user)
  
  // 3d. Early returns untuk edge cases
  if (!user.isActive) return null
  
  // 3e. JSX (clean, minimal nesting)
  return (
    <article onClick={handleClick} className="user-card">
      <h3>{fullName}</h3>
      <p>{user.email}</p>
    </article>
  )
}
```

## Anti-Patterns to AVOID

```typescript
// ❌ NEVER: useEffect untuk data fetching
useEffect(() => {
  fetch('/api/users').then(setUsers)
}, [])

// ✅ ALWAYS: TanStack Query
const { data: users } = useQuery(userQueries.list())

// ❌ NEVER: Prop drilling lebih dari 2 level
<Parent userData={user}>
  <Child userData={user}>
    <GrandChild userData={user} />

// ✅ ALWAYS: Context atau query di level yang butuh
function GrandChild() {
  const { data: user } = useQuery(userQueries.current())
}

// ❌ NEVER: Premature optimization
const value = useMemo(() => a + b, [a, b]) // simple math

// ✅ ALWAYS: Optimize only when measured
const value = a + b // just calculate

// ❌ NEVER: Index as key untuk dynamic lists
{items.map((item, i) => <Item key={i} />)}

// ✅ ALWAYS: Stable unique identifier
{items.map(item => <Item key={item.id} />)}
```

## Debugging Guide

See [debugging-guide.md](references/debugging-guide.md) for:
- React DevTools profiling
- TanStack Query DevTools
- Memory leak detection
- Performance bottleneck identification
- Common error patterns

## Common Pitfalls & Bugs

See [common-pitfalls.md](references/common-pitfalls.md) for:
- Stale closure bugs
- Race conditions
- Memory leaks patterns
- Hydration mismatches
- Query invalidation mistakes

## Performance Checklist

```markdown
□ Bundle size < 200KB gzipped (initial)
□ Largest Contentful Paint < 2.5s
□ No unnecessary re-renders (React DevTools)
□ Images lazy loaded
□ Code splitting per route
□ Query deduplication working
□ No memory leaks (heap snapshot stable)
```

## Code Review Checklist

```markdown
□ No `any` types (use `unknown` if needed)
□ No `// @ts-ignore` tanpa penjelasan
□ Error boundaries di route level
□ Loading states handled
□ Empty states handled
□ Error states handled  
□ Accessibility (aria labels, keyboard nav)
□ No hardcoded strings (i18n ready)
□ No console.log in production code
□ Tests untuk business logic
```

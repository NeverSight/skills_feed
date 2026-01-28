---
name: typescript-best-practices
description: Enforce strict TypeScript standards including centralized type definitions in app/types/, arrow functions only, explicit return types, and lang="ts" in all components. Use when reviewing or creating TypeScript code.
---

# TypeScript Best Practices

Enforce project-wide TypeScript standards and conventions.

## When to Use

**DO USE** when:
- Writing any new TypeScript code
- Creating or modifying Vue components
- Defining new types or interfaces
- Creating composables or utilities
- Reviewing code for TypeScript compliance
- Refactoring JavaScript to TypeScript
- Questions about type definitions
- Type organization and structure

**DO NOT USE** when:
- Dealing with plain JavaScript (convert to TypeScript first)
- Configuration files that don't support TypeScript
- Third-party type definitions (use @types packages)

## Critical Standards

### ⚠️ NON-NEGOTIABLE RULES

1. **Type Location**: ALL types MUST be in `app/types/` directory
   - ✅ `import type { User } from '~/types/user'`
   - ❌ Defining types inside components/composables

2. **Vue Components**: ALWAYS use `lang="ts"`
   - ✅ `<script setup lang="ts">`
   - ❌ `<script setup>` without lang

3. **Function Style**: ONLY arrow functions
   - ✅ `const myFunc = (): string => { ... }`
   - ❌ `function myFunc() { ... }`

4. **Return Types**: ALWAYS specify return types
   - ✅ `const getData = (): Promise<User[]> => { ... }`
   - ❌ `const getData = async () => { ... }`

5. **Explicit Types**: NO implicit any
   - ✅ `const items: Product[] = []`
   - ❌ `const items = []`

6. **Type Exports**: ALWAYS export from `app/types/`
   - ✅ All types exported and imported
   - ❌ Local type definitions

## Type Organization Structure

### Directory Layout

```
app/
  types/
    user.ts           # User-related types
    product.ts        # Product types
    api.ts            # API response types
    forms.ts          # Form data types
    state.ts          # State management types
    common.ts         # Shared/utility types
    errors.ts         # Error types
    index.ts          # Optional re-exports
```

### File Naming

- Use **singular** for entity types: `user.ts`, `product.ts`
- Use **descriptive** names: `api.ts`, `forms.ts`, `state.ts`
- Group related types in same file
- Export all types from each file

## Code Patterns

### Component Pattern

```typescript
// ✅ CORRECT
<script setup lang="ts">
import type { User, Product } from '~/types'

interface Props {
  user: User
  items: Product[]
}

const props = defineProps<Props>()

const formatName = (user: User): string => {
  return `${user.firstName} ${user.lastName}`
}
</script>
```

### Composable Pattern

```typescript
// ✅ CORRECT
// app/composables/useData.ts
import type { User, ApiResponse } from '~/types'

export const useData = () => {
  const data = ref<User | null>(null)
  
  const fetchData = async (): Promise<User> => {
    const { data: response } = await useFetch<ApiResponse<User>>('/api/user')
    if (!response.value) throw new Error('No data')
    return response.value.data
  }
  
  return { data, fetchData }
}
```

### Store Pattern

```typescript
// ✅ CORRECT
// app/stores/user.ts
import type { User, LoginCredentials } from '~/types'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  
  const login = async (creds: LoginCredentials): Promise<void> => {
    // Implementation
  }
  
  return { user: readonly(user), login }
})
```

### Utility Pattern

```typescript
// ✅ CORRECT
// app/utils/formatters.ts
import type { User, Product } from '~/types'

export const formatUser = (user: User): string => {
  return `${user.firstName} ${user.lastName}`
}

export const calculateTotal = (products: Product[]): number => {
  return products.reduce((sum: number, p: Product): number => 
    sum + p.price, 0
  )
}
```

## Type Definition Patterns

### Basic Entity Types

```typescript
// app/types/user.ts
export interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  role: UserRole
  createdAt: Date
}

export type UserRole = 'admin' | 'user' | 'guest'
```

### API Response Types

```typescript
// app/types/api.ts
export interface ApiResponse<T> {
  data: T
  message: string
  success: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
}
```

### Form Types

```typescript
// app/types/forms.ts
export interface LoginForm {
  email: string
  password: string
}

export interface FormField<T> {
  value: T
  error: string | null
  touched: boolean
}
```

### State Types

```typescript
// app/types/state.ts
export interface LoadingState {
  isLoading: boolean
  error: Error | null
}

export interface DataState<T> extends LoadingState {
  data: T | null
}
```

## Common Violations & Fixes

### ❌ Inline Type Definition

```vue
<!-- WRONG -->
<script setup lang="ts">
interface User {  // ❌ Type defined inline
  id: string
  name: string
}
</script>
```

**Fix**: Move to `app/types/user.ts`

### ❌ Missing Return Type

```typescript
// WRONG
const getData = async () => {  // ❌ No return type
  return data
}
```

**Fix**: Add explicit return type

```typescript
// CORRECT
const getData = async (): Promise<Data> => {
  return data
}
```

### ❌ Function Keyword

```typescript
// WRONG
function handleClick() {  // ❌ function keyword
  // ...
}
```

**Fix**: Use arrow function

```typescript
// CORRECT
const handleClick = (): void => {
  // ...
}
```

### ❌ Missing lang="ts"

```vue
<!-- WRONG -->
<script setup>  <!-- ❌ No lang="ts" -->
const data = ref()
</script>
```

**Fix**: Add lang="ts"

```vue
<!-- CORRECT -->
<script setup lang="ts">
const data = ref<string>('')
</script>
```

### ❌ Implicit Any

```typescript
// WRONG
const items = []  // ❌ Implicit any[]
const user = ref()  // ❌ Implicit any
```

**Fix**: Add explicit types

```typescript
// CORRECT
const items: string[] = []
const user = ref<User | null>(null)
```

## Refactoring Checklist

When reviewing or refactoring TypeScript code:

- [ ] All types defined in `app/types/` directory
- [ ] All Vue components use `lang="ts"`
- [ ] All functions are arrow functions
- [ ] All functions have explicit return types
- [ ] No `function` keyword usage
- [ ] No inline type definitions
- [ ] No `any` types (use `unknown` if needed)
- [ ] All variables have explicit types
- [ ] Imports use `import type` for types
- [ ] Generic types properly constrained

## tsconfig Enforcement

Ensure these are enabled in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true
  }
}
```

## Quick Reference

### ✅ DO

- Export all types from `app/types/`
- Use `lang="ts"` in all Vue components
- Use arrow functions exclusively
- Specify return types on all functions
- Use explicit types for all variables
- Import types with `import type`
- Use `unknown` instead of `any`
- Document complex types with JSDoc

### ❌ DON'T

- Define types inside components
- Define types inside composables
- Use `function` keyword
- Omit return types
- Use implicit `any`
- Use `any` type
- Define types in non-types files
- Forget `lang="ts"` in components

## Integration with Project

This TypeScript standard works with:
- **Components**: `lang="ts"` + external types
- **Composables**: Arrow functions + return types
- **Stores**: Pinia with typed state/actions
- **Utils**: Pure functions with explicit types
- **API**: Typed requests/responses

## Additional Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Vue 3 TypeScript Guide](https://vuejs.org/guide/typescript/overview.html)
- [Nuxt TypeScript](https://nuxt.com/docs/guide/concepts/typescript)
- [Pinia TypeScript](https://pinia.vuejs.org/core-concepts/#typescript)

## Example Workflow

**User: "Create a user profile component"**

1. Define types in `app/types/user.ts`
2. Create component with `lang="ts"`
3. Import types: `import type { User } from '~/types'`
4. Use arrow functions with return types
5. Verify all TypeScript standards followed

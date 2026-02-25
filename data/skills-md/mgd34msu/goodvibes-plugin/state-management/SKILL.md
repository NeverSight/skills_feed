---
name: state-management
description: "Load PROACTIVELY when task involves application state, data fetching, or form handling. Use when user says \"manage state\", \"add data fetching\", \"set up Zustand\", \"handle form validation\", or \"add React Query\". Covers server state (TanStack Query with caching, optimistic updates), client state (Zustand stores), form state (React Hook Form with Zod validation), URL state (search params, routing), and choosing between state solutions."
metadata:
  version: 1.0.0
  category: outcome
  tags: [state, zustand, tanstack-query, react-hook-form, zod, url-state, forms]
---

## Resources
```
scripts/
  validate-state.sh
references/
  state-patterns.md
```

# State Management

This skill guides you through state architecture decisions and implementation using GoodVibes precision tools. Use this workflow when choosing state solutions, implementing data fetching patterns, or managing complex form state.

## When to Use This Skill

Load this skill when:
- Deciding between state management approaches
- Implementing server data fetching with caching
- Building forms with complex validation
- Managing client-side application state
- Implementing URL-based state patterns
- Migrating from one state solution to another

Trigger phrases: "state management", "TanStack Query", "Zustand", "React Hook Form", "form validation", "data fetching", "cache invalidation", "URL state".

## Core Workflow

### Phase 1: Discovery

Before choosing a state solution, understand existing patterns.

#### Step 1.1: Identify Current State Libraries

Use `discover` to find existing state management solutions.

```yaml
discover:
  queries:
    - id: state_libraries
      type: grep
      pattern: "(from 'zustand'|from '@tanstack/react-query'|from 'react-hook-form'|from 'jotai'|from 'redux'|useContext)"
      glob: "**/*.{ts,tsx}"
    - id: data_fetching
      type: grep
      pattern: "(useQuery|useMutation|useSWR|fetch|axios)"
      glob: "**/*.{ts,tsx}"
    - id: form_libraries
      type: grep
      pattern: "(useForm|Formik|react-hook-form)"
      glob: "**/*.{ts,tsx}"
  verbosity: files_only
```

**What this reveals:**
- Existing state management libraries in use
- Data fetching patterns (REST, GraphQL, etc.)
- Form handling approaches
- Consistency across the codebase

#### Step 1.2: Analyze Package Dependencies

Use `precision_read` to check what's installed.

```yaml
precision_read:
  files:
    - path: "package.json"
      extract: content
  verbosity: minimal
```

Look for:
- `@tanstack/react-query` (server state)
- `zustand` (client state)
- `react-hook-form` + `zod` (forms)
- `nuqs` or similar (URL state)

#### Step 1.3: Read Existing State Patterns

Read 2-3 examples to understand implementation patterns.

```yaml
precision_read:
  files:
    - path: "src/lib/query-client.ts"  # or discovered file
      extract: content
    - path: "src/stores/user-store.ts"  # or discovered file
      extract: content
  verbosity: standard
```

### Phase 2: State Categorization

Choose the right tool for each type of state. See `references/state-patterns.md` for the complete decision tree.

#### Quick Decision Guide

| State Type | Best Tool | Use When |
|------------|-----------|----------|
| **Server state** | TanStack Query | Data from APIs, needs caching/invalidation |
| **Client state** | Zustand | UI state shared across components |
| **Form state** | React Hook Form + Zod | Complex forms with validation |
| **URL state** | nuqs or searchParams | Sharable, bookmarkable state |
| **Component state** | useState | Local to one component |

**State Colocation Principle:**
Keep state as close to where it's used as possible. Start with `useState`, lift to parent when shared, then consider dedicated solutions only when necessary.

### Phase 3: Server State with TanStack Query

For data from APIs that needs caching, background updates, and optimistic mutations.

#### Step 3.1: Install Dependencies

Check if installed, otherwise add:

```bash
npm install @tanstack/react-query  # Note: Targeting TanStack Query v5
npm install -D @tanstack/react-query-devtools
```

#### Step 3.2: Set Up Query Client

Create a query client configuration.

```typescript
// src/lib/query-client.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60, // 1 minute
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

#### Step 3.3: Implement Query Patterns

**Basic Query:**

```typescript
import { useQuery } from '@tanstack/react-query';
import { getUser } from '@/lib/api';

export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => getUser(userId),
    enabled: !!userId, // Don't run if no userId
  });
}
```

**Mutation with Optimistic Update:**

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { updateUser } from '@/lib/api';

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,
    onMutate: async (newUser) => {
      // Cancel outgoing queries
      await queryClient.cancelQueries({ queryKey: ['user', newUser.id] });

      // Snapshot previous value
      const previousUser = queryClient.getQueryData(['user', newUser.id]);

      // Optimistically update
      queryClient.setQueryData(['user', newUser.id], newUser);

      return { previousUser };
    },
    onError: (err, newUser, context) => {
      // Rollback on error
      queryClient.setQueryData(
        ['user', newUser.id],
        context?.previousUser
      );
    },
    onSettled: (data, error, variables) => {
      // Refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['user', variables.id] });
    },
  });
}
```

**Cache Invalidation:**

```typescript
// Invalidate all user queries
queryClient.invalidateQueries({ queryKey: ['user'] });

// Invalidate specific user
queryClient.invalidateQueries({ queryKey: ['user', userId] });

// Remove from cache entirely
queryClient.removeQueries({ queryKey: ['user', userId] });
```

**Consuming Error and Loading States:**

```typescript
function UserProfile({ userId }: { userId: string }) {
  const { data, isPending, isError, error } = useUser(userId);

  if (isPending) return <Skeleton />;
  if (isError) return <ErrorDisplay error={error} />;
  
  return <UserProfile user={data} />;
}
```

### Phase 4: Client State with Zustand

For UI state shared across components (modals, themes, filters).

#### Step 4.1: Install Dependencies

```bash
npm install zustand
```

#### Step 4.2: Create Store

**Simple Store:**

```typescript
import { create } from 'zustand';

interface UIStore {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}));
```

**Store with Slices:**

```typescript
import { create, StateCreator } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

// Slice pattern for organization
interface AuthSlice {
  user: User | null;
  setUser: (user: User | null) => void;
}

interface UISlice {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}

type Store = AuthSlice & UISlice;

const createAuthSlice: StateCreator<Store, [], [], AuthSlice> = (set) => ({
  user: null,
  setUser: (user) => set({ user }),
});

const createUISlice: StateCreator<Store, [], [], UISlice> = (set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((state: Store) => ({ 
    sidebarOpen: !state.sidebarOpen 
  })),
});

export const useStore = create<Store>()(
  devtools(
    persist(
      (...a) => ({
        ...createAuthSlice(...a),
        ...createUISlice(...a),
      }),
      { name: 'app-store' }
    )
  )
);
```

**Using Selectors:**

```typescript
// Avoid re-renders by selecting only what you need
const sidebarOpen = useUIStore((state) => state.sidebarOpen);
const toggleSidebar = useUIStore((state) => state.toggleSidebar);
```

### Phase 5: Form State with React Hook Form + Zod

For complex forms with validation, field arrays, and nested objects.

#### Step 5.1: Install Dependencies

```bash
npm install react-hook-form zod @hookform/resolvers
```

#### Step 5.2: Define Validation Schema

```typescript
import { z } from 'zod';

export const userSchema = z.object({
  email: z.string().email('Invalid email address'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
  age: z.number().min(18, 'Must be 18 or older'),
  role: z.enum(['user', 'admin']).default('user'),
  preferences: z.object({
    newsletter: z.boolean().default(false),
    notifications: z.boolean().default(true),
  }),
});

export type UserFormData = z.infer<typeof userSchema>;
```

#### Step 5.3: Implement Form

**Basic Form:**

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { userSchema, type UserFormData } from './schema';

export function UserForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      role: 'user',
      preferences: {
        newsletter: false,
        notifications: true,
      },
    },
  });

  const onSubmit = async (data: UserFormData) => {
    await createUser(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}

      <input type="number" {...register('age', { valueAsNumber: true })} />
      {errors.age && <span>{errors.age.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

**Field Arrays:**

```typescript
import { useFieldArray } from 'react-hook-form';

const schema = z.object({
  users: z.array(
    z.object({
      name: z.string().min(1),
      email: z.string().email(),
    })
  ).min(1, 'At least one user required'),
});

function UsersForm() {
  const { control, register } = useForm({
    resolver: zodResolver(schema),
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'users',
  });

  return (
    <div>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`users.${index}.name`)} />
          <input {...register(`users.${index}.email`)} />
          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
        </div>
      ))}
      <button
        type="button"
        onClick={() => append({ name: '', email: '' })}
      >
        Add User
      </button>
    </div>
  );
}
```

### Phase 6: URL State Patterns

For state that should be shareable and bookmarkable.

#### Step 6.1: Using nuqs (Recommended)

```bash
npm install nuqs  # Note: Targeting nuqs v1.x
```

```typescript
import { useQueryState, parseAsInteger, parseAsStringEnum } from 'nuqs';

export function ProductList() {
  const [page, setPage] = useQueryState(
    'page',
    parseAsInteger.withDefault(1)
  );

  const [sort, setSort] = useQueryState(
    'sort',
    parseAsStringEnum(['name', 'price', 'date']).withDefault('name')
  );

  // URL: /products?page=2&sort=price
  // Automatically synced, type-safe, bookmarkable
}
```

#### Step 6.2: Using Next.js searchParams

```typescript
import { useSearchParams, useRouter } from 'next/navigation';

export function ProductList() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const page = Number(searchParams.get('page')) || 1;

  const setPage = (newPage: number) => {
    const params = new URLSearchParams(searchParams);
    params.set('page', String(newPage));
    router.push(`?${params.toString()}`);
  };
}
```

### Phase 7: Implementation with Precision Tools

Use `precision_write` to create state management files.

```yaml
precision_write:
  files:
    - path: "src/lib/query-client.ts"
      content: |
        import { QueryClient } from '@tanstack/react-query';
        export const queryClient = new QueryClient({ ... });
    - path: "src/stores/ui-store.ts"
      content: |
        import { create } from 'zustand';
        export const useUIStore = create({ ... });
    - path: "src/schemas/user-schema.ts"
      content: |
        import { z } from 'zod';
        export const userSchema = z.object({ ... });
  verbosity: count_only
```

### Phase 8: Validation

#### Step 8.1: Run Validation Script

Use the validation script to ensure quality.

```bash
bash scripts/validate-state.sh .
```

See `scripts/validate-state.sh` for the complete validation suite.

#### Step 8.2: Type Check

Verify TypeScript compilation.

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
  verbosity: minimal
```

## Common Patterns

### Pattern 1: Combine TanStack Query + Zustand

```typescript
// Server data with TanStack Query
const { data: user } = useQuery({ queryKey: ['user'], queryFn: getUser });

// UI state with Zustand
const { sidebarOpen, toggleSidebar } = useUIStore();
```

### Pattern 2: Form with Server Mutation

```typescript
const mutation = useMutation({
  mutationFn: createUser,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['users'] });
  },
});

const onSubmit = (data: UserFormData) => {
  mutation.mutate(data);
};
```

### Pattern 3: URL State Driving Data Fetching

```typescript
const [page] = useQueryState('page', parseAsInteger.withDefault(1));
const [search] = useQueryState('search');

const { data } = useQuery({
  queryKey: ['products', page, search],
  queryFn: () => getProducts({ page, search }),
});
```

## Common Anti-Patterns

**DON'T:**
- Use global state for server data (use TanStack Query)
- Put everything in Zustand (colocate when possible)
- Manage form state manually (use React Hook Form)
- Store UI state in URL params (use Zustand)
- Use Context for frequently changing data (causes re-renders)
- Forget to invalidate cache after mutations
- Skip validation schemas for forms
- Use `any` types in state stores

**DO:**
- Match state type to the right tool
- Colocate state when possible
- Use selectors to prevent re-renders
- Implement optimistic updates for better UX
- Validate all form inputs with Zod
- Use TypeScript for all state definitions
- Invalidate queries after mutations
- Keep query keys consistent

## Quick Reference

**Discovery Phase:**
```yaml
discover: { queries: [state_libraries, data_fetching, forms], verbosity: files_only }
precision_read: { files: ["package.json", example stores], extract: content }
```

**Implementation Phase:**
```yaml
precision_write: { files: [query-client, stores, schemas], verbosity: count_only }
```

**Validation Phase:**
```yaml
precision_exec: { commands: [{ cmd: "npm run typecheck" }], verbosity: minimal }
```

**Post-Implementation:**
```bash
bash scripts/validate-state.sh .
```

For detailed patterns and decision trees, see `references/state-patterns.md`.

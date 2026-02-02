---
name: tanstack-react-query
description: TanStack React Query expert for data fetching and mutations in React applications. Use when working with useQuery, useMutation, cache invalidation, optimistic updates, query keys, or integrating server actions with React Query via @saas4dev/core hooks (useServerActionQuery, useServerActionMutation, useServerActionInfiniteQuery). Triggers on requests involving API data fetching, server state management, cache strategies, or converting fetch/useEffect patterns to React Query.
---

# TanStack React Query Expert

Expert guidance for idiomatic React Query (TanStack Query v5) patterns in React applications, with special focus on ZSA server action integration via `@saas4dev/core`.

## Core Hooks

### From @saas4dev/core (Server Actions)

```typescript
import {
  useServerActionQuery,
  useServerActionMutation,
  useServerActionInfiniteQuery,
} from '@saas4dev/core'
```

### From @tanstack/react-query (Direct API)

```typescript
import {
  useQuery,
  useMutation,
  useInfiniteQuery,
  useQueryClient,
} from '@tanstack/react-query'
```

## Decision Tree

```
Need to fetch data?
├── From server action → useServerActionQuery
├── From REST/fetch directly → useQuery
└── Paginated/infinite → useServerActionInfiniteQuery or useInfiniteQuery

Need to modify data?
├── From server action → useServerActionMutation
└── From REST/fetch directly → useMutation

After mutation, what cache behavior?
├── Simple: just invalidate → queryClient.invalidateQueries()
├── Update specific item → queryClient.setQueryData()
└── Need instant feedback → Optimistic update pattern
```

## Quick Patterns

### Server Action Query

```typescript
const { data, isLoading } = useServerActionQuery(listUsersAction, {
  input: { status: 'active' },
  queryKey: ['users', 'list', { status: 'active' }],
})
```

### Server Action Mutation with Invalidation

```typescript
const queryClient = useQueryClient()

const mutation = useServerActionMutation(createUserAction, {
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['users'] })
    toast.success('User created')
  },
  onError: (error) => toast.error(error.message),
})
```

### Optimistic Update

```typescript
const mutation = useServerActionMutation(updateTodoAction, {
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: ['todos', newData.id] })
    const previous = queryClient.getQueryData(['todos', newData.id])
    queryClient.setQueryData(['todos', newData.id], (old) => ({ ...old, ...newData }))
    return { previous }
  },
  onError: (err, newData, context) => {
    queryClient.setQueryData(['todos', newData.id], context?.previous)
  },
  onSettled: (data, err, variables) => {
    queryClient.invalidateQueries({ queryKey: ['todos', variables.id] })
  },
})
```

## Query Key Structure

### Hierarchy Pattern

```typescript
['entity']                           // All of entity
['entity', 'list']                   // All lists
['entity', 'list', { filters }]      // Filtered list
['entity', 'detail', id]             // Single item
['entity', id, 'nested']             // Nested resource
```

### Query Key Factory

```typescript
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: Filters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
}
```

## Configuration Defaults

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,        // 1 minute
      gcTime: 5 * 60 * 1000,       // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})
```

## Best Practices

1. **Query Keys**: Use hierarchical keys; invalidate broadly, fetch specifically
2. **Mutations**: Always invalidate or update related queries on success
3. **Loading States**: Use `isLoading` for first load, `isFetching` for background updates
4. **Error Handling**: Handle in `onError` callback; show user-friendly messages
5. **Optimistic Updates**: Use for high-confidence mutations; always implement rollback
6. **Conditional Queries**: Use `enabled` option, not conditional hook calls
7. **Derived Data**: Use `select` to transform data; keeps original in cache

## References

Detailed patterns and examples:

- **[query-patterns.md](references/query-patterns.md)**: Query keys, useQuery, pagination, parallel/dependent queries
- **[mutation-patterns.md](references/mutation-patterns.md)**: Mutations, cache invalidation, optimistic updates, rollback
- **[advanced-patterns.md](references/advanced-patterns.md)**: Custom hooks, prefetching, SSR hydration, testing

## Skill Interface

When using this skill, provide:

```json
{
  "apiDescription": "REST/GraphQL endpoints, methods, parameters, response shapes",
  "uiScenario": "What the UI needs (e.g., 'List with pagination', 'Edit form with instant feedback')",
  "constraints": "React Query v5, fetch vs axios, suspense vs traditional",
  "currentCode": "(optional) Existing code to improve"
}
```

Response includes:
- **recommendations**: Query keys, hooks, invalidation strategy
- **exampleCode**: React components/hooks demonstrating patterns
- **notes**: Why these patterns were chosen

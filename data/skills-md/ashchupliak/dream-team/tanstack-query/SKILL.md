---
name: tanstack-query
description: TanStack React Query patterns - use for data fetching, caching, mutations, optimistic updates, and server state management
---

# TanStack React Query Patterns

## Setup

```tsx
// providers/QueryProvider.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useState } from 'react'

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            gcTime: 5 * 60 * 1000, // 5 minutes (formerly cacheTime)
            refetchOnWindowFocus: false,
            retry: 1,
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

## Query Keys

```tsx
// lib/queryKeys.ts
export const queryKeys = {
  environments: {
    all: ['environments'] as const,
    lists: () => [...queryKeys.environments.all, 'list'] as const,
    list: (filters: EnvironmentFilters) =>
      [...queryKeys.environments.lists(), filters] as const,
    details: () => [...queryKeys.environments.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.environments.details(), id] as const,
  },
  users: {
    all: ['users'] as const,
    detail: (id: string) => [...queryKeys.users.all, id] as const,
  },
}
```

## Basic Queries

```tsx
// hooks/useEnvironments.ts
import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'

interface EnvironmentFilters {
  status?: string
  page?: number
}

async function fetchEnvironments(filters: EnvironmentFilters) {
  const params = new URLSearchParams()
  if (filters.status) params.set('status', filters.status)
  if (filters.page) params.set('page', String(filters.page))

  const res = await fetch(`/api/environments?${params}`)
  if (!res.ok) throw new Error('Failed to fetch environments')
  return res.json()
}

export function useEnvironments(filters: EnvironmentFilters = {}) {
  return useQuery({
    queryKey: queryKeys.environments.list(filters),
    queryFn: () => fetchEnvironments(filters),
  })
}

// Usage
function EnvironmentList() {
  const { data, isLoading, error } = useEnvironments({ status: 'RUNNING' })

  if (isLoading) return <Skeleton />
  if (error) return <Error message={error.message} />

  return (
    <ul>
      {data?.map((env) => (
        <li key={env.id}>{env.name}</li>
      ))}
    </ul>
  )
}
```

## Single Item Query

```tsx
// hooks/useEnvironment.ts
export function useEnvironment(id: string) {
  return useQuery({
    queryKey: queryKeys.environments.detail(id),
    queryFn: async () => {
      const res = await fetch(`/api/environments/${id}`)
      if (!res.ok) {
        if (res.status === 404) return null
        throw new Error('Failed to fetch environment')
      }
      return res.json()
    },
    enabled: !!id, // Don't fetch if no id
  })
}
```

## Mutations

```tsx
// hooks/useCreateEnvironment.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'

interface CreateEnvironmentInput {
  name: string
  description?: string
}

export function useCreateEnvironment() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (input: CreateEnvironmentInput) => {
      const res = await fetch('/api/environments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      })
      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.message || 'Failed to create environment')
      }
      return res.json()
    },
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: queryKeys.environments.lists(),
      })
    },
  })
}

// Usage
function CreateEnvironmentForm() {
  const mutation = useCreateEnvironment()

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    mutation.mutate({
      name: formData.get('name') as string,
      description: formData.get('description') as string,
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" required />
      <textarea name="description" />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create'}
      </button>
      {mutation.isError && (
        <p className="text-red-500">{mutation.error.message}</p>
      )}
    </form>
  )
}
```

## Optimistic Updates

```tsx
// hooks/useUpdateEnvironment.ts
export function useUpdateEnvironment() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ id, ...data }: UpdateEnvironmentInput) => {
      const res = await fetch(`/api/environments/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!res.ok) throw new Error('Failed to update')
      return res.json()
    },

    // Optimistic update
    onMutate: async (newData) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({
        queryKey: queryKeys.environments.detail(newData.id),
      })

      // Snapshot previous value
      const previousEnv = queryClient.getQueryData(
        queryKeys.environments.detail(newData.id)
      )

      // Optimistically update
      queryClient.setQueryData(
        queryKeys.environments.detail(newData.id),
        (old: Environment) => ({ ...old, ...newData })
      )

      return { previousEnv }
    },

    // Rollback on error
    onError: (err, newData, context) => {
      if (context?.previousEnv) {
        queryClient.setQueryData(
          queryKeys.environments.detail(newData.id),
          context.previousEnv
        )
      }
    },

    // Refetch after success or error
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.environments.detail(variables.id),
      })
    },
  })
}
```

## Delete with Optimistic Update

```tsx
// hooks/useDeleteEnvironment.ts
export function useDeleteEnvironment() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (id: string) => {
      const res = await fetch(`/api/environments/${id}`, {
        method: 'DELETE',
      })
      if (!res.ok) throw new Error('Failed to delete')
    },

    onMutate: async (deletedId) => {
      await queryClient.cancelQueries({
        queryKey: queryKeys.environments.lists(),
      })

      const previousEnvs = queryClient.getQueryData<Environment[]>(
        queryKeys.environments.lists()
      )

      // Remove from list optimistically
      queryClient.setQueryData<Environment[]>(
        queryKeys.environments.lists(),
        (old) => old?.filter((env) => env.id !== deletedId)
      )

      return { previousEnvs }
    },

    onError: (err, id, context) => {
      queryClient.setQueryData(
        queryKeys.environments.lists(),
        context?.previousEnvs
      )
    },

    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.environments.lists(),
      })
    },
  })
}
```

## Infinite Queries (Pagination)

```tsx
// hooks/useInfiniteEnvironments.ts
import { useInfiniteQuery } from '@tanstack/react-query'

export function useInfiniteEnvironments() {
  return useInfiniteQuery({
    queryKey: ['environments', 'infinite'],
    queryFn: async ({ pageParam }) => {
      const res = await fetch(`/api/environments?cursor=${pageParam}`)
      return res.json()
    },
    initialPageParam: '',
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  })
}

// Usage
function InfiniteList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteEnvironments()

  return (
    <>
      {data?.pages.map((page, i) => (
        <Fragment key={i}>
          {page.items.map((env) => (
            <EnvironmentCard key={env.id} environment={env} />
          ))}
        </Fragment>
      ))}
      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? 'Loading...' : hasNextPage ? 'Load More' : 'No more'}
      </button>
    </>
  )
}
```

## Prefetching

```tsx
// Prefetch on hover
function EnvironmentLink({ id, name }: { id: string; name: string }) {
  const queryClient = useQueryClient()

  const prefetch = () => {
    queryClient.prefetchQuery({
      queryKey: queryKeys.environments.detail(id),
      queryFn: () => fetchEnvironment(id),
      staleTime: 60 * 1000,
    })
  }

  return (
    <Link href={`/environments/${id}`} onMouseEnter={prefetch}>
      {name}
    </Link>
  )
}
```

---
name: frontend-hooks-creation
description: Create React Query hooks for API endpoints with proper typing and cache invalidation. Use when asked to "create hooks", "add frontend hooks", "create API hooks", or "add React Query hooks".
---

# Frontend Hooks Creation

This skill creates React Query hooks for API endpoints using types from `@{project}/types` following established patterns.

## Overview

We use **React Query (TanStack Query)** for all server state management. Hooks import types from `@{project}/types` to ensure type safety with the backend.

## File Structure

```
apps/webapp/src/
├── api/
│   ├── client.ts           # Axios instance
│   ├── workflows.ts        # Workflow API functions
│   └── {resource}.ts       # New resource API functions
├── hooks/
│   ├── index.ts            # Re-exports all hooks
│   ├── useWorkflows.ts     # Workflow hooks
│   └── use{Resource}.ts    # New resource hooks
└── lib/
    └── queryClient.ts      # React Query client
```

## Step 1: Create the API Module

First, create `apps/webapp/src/api/{resource}.ts`:

```typescript
import { apiClient } from './client';
import type {
  Resource,
  // Query/Params types
  ListResourcesQuery,
  // Body types
  CreateResourceBody,
  UpdateResourceBody,
  // Response types
  ListResourcesResponse,
  GetResourceResponse,
  CreateResourceResponse,
  UpdateResourceResponse,
} from '@{project}/types';

// Re-export types for convenience
export type { CreateResourceBody, UpdateResourceBody, ListResourcesQuery };

// List all resources
export async function listResources(
  params: ListResourcesQuery = {}
): Promise<ListResourcesResponse> {
  const response = await apiClient.get<ListResourcesResponse>('/api/resources', {
    params,
  });
  return response.data;
}

// Get a single resource by ID
export async function getResource(id: string): Promise<Resource> {
  const response = await apiClient.get<GetResourceResponse>(
    `/api/resources/${id}`
  );
  return response.data.result;
}

// Create a new resource
export async function createResource(
  payload: CreateResourceBody
): Promise<Resource> {
  const response = await apiClient.post<CreateResourceResponse>(
    '/api/resources',
    payload
  );
  return response.data.result;
}

// Update a resource
export async function updateResource(
  id: string,
  payload: UpdateResourceBody
): Promise<Resource> {
  const response = await apiClient.put<UpdateResourceResponse>(
    `/api/resources/${id}`,
    payload
  );
  return response.data.result;
}

// Delete a resource
export async function deleteResource(id: string): Promise<void> {
  await apiClient.delete(`/api/resources/${id}`);
}
```

## Step 2: Create the Hooks File

Create `apps/webapp/src/hooks/use{Resource}s.ts`:

```typescript
import { useQuery, useMutation } from '@tanstack/react-query';
import type {
  Resource,
  ListResourcesQuery,
  ListResourcesResponse,
  CreateResourceBody,
  UpdateResourceBody,
} from '@{project}/types';
import { queryClient } from '../lib/queryClient';
import * as resourceApi from '../api/resources';

// ============================================
// Query Hooks
// ============================================

// GET /api/resources - List all resources
export const useGetResources = (params: ListResourcesQuery = {}) => {
  return useQuery<ListResourcesResponse>({
    queryKey: ['resources', params],
    queryFn: () => resourceApi.listResources(params),
  });
};

// GET /api/resources/:id - Get a single resource by ID
export const useGetResource = (id: string | null) => {
  return useQuery<Resource>({
    queryKey: ['resource', id],
    queryFn: () => resourceApi.getResource(id!),
    enabled: !!id,
  });
};

// ============================================
// Mutation Hooks
// ============================================

// POST /api/resources - Create a new resource
export const useCreateResource = () => {
  return useMutation({
    mutationFn: (payload: CreateResourceBody) => {
      return resourceApi.createResource(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resources'] });
    },
  });
};

// PUT /api/resources/:id - Update a resource
export const useUpdateResource = () => {
  return useMutation({
    mutationFn: (data: { id: string; payload: UpdateResourceBody }) => {
      return resourceApi.updateResource(data.id, data.payload);
    },
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['resource', id] });
      queryClient.invalidateQueries({ queryKey: ['resources'] });
    },
  });
};

// DELETE /api/resources/:id - Delete a resource
export const useDeleteResource = () => {
  return useMutation({
    mutationFn: (id: string) => {
      return resourceApi.deleteResource(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resources'] });
    },
  });
};

// ============================================
// Helper Functions
// ============================================

// Invalidate a resource query (useful for real-time updates)
export const invalidateResource = (id: string) => {
  queryClient.invalidateQueries({ queryKey: ['resource', id] });
};

// Invalidate all resources queries
export const invalidateResources = () => {
  queryClient.invalidateQueries({ queryKey: ['resources'] });
};
```

## Step 3: Export from Index

Add to `apps/webapp/src/hooks/index.ts`:

```typescript
export * from './useResources';
```

## Hook Naming Conventions

- **Queries**: `useGet<Resource>` or `useGet<Resource>s`
  - `useGetWorkflow` - single resource by ID
  - `useGetWorkflows` - list/collection

- **Mutations**: `use<Action><Resource>`
  - `useCreateWorkflow`
  - `useUpdateWorkflow`
  - `useDeleteWorkflow`
  - `usePublishWorkflow` (action routes)

## Query Key Patterns

Use consistent query key patterns for cache invalidation:

```typescript
// Single resource
queryKey: ['resource', id]

// Collection with filters (include params object)
queryKey: ['resources', params]

// Related/nested resources
queryKey: ['resource-versions', resourceId]

// Invalidate all queries for a resource type
queryClient.invalidateQueries({ queryKey: ['resources'] });
```

## Hook Patterns

### Query with Optional ID

For fetching a single resource that may not always have an ID:

```typescript
export const useGetResource = (id: string | null) => {
  return useQuery<Resource>({
    queryKey: ['resource', id],
    queryFn: () => resourceApi.getResource(id!),
    enabled: !!id, // Only run if id exists
  });
};
```

### Query with Filter Parameters

For list endpoints with optional filters:

```typescript
export const useGetResources = (params: ListResourcesQuery = {}) => {
  return useQuery<ListResourcesResponse>({
    queryKey: ['resources', params],
    queryFn: () => resourceApi.listResources(params),
  });
};
```

### Mutation with Multiple Parameters

For updates that need both ID and payload:

```typescript
export const useUpdateResource = () => {
  return useMutation({
    mutationFn: (data: { id: string; payload: UpdateResourceBody }) => {
      return resourceApi.updateResource(data.id, data.payload);
    },
    onSuccess: (_, { id }) => {
      // Invalidate both specific and list queries
      queryClient.invalidateQueries({ queryKey: ['resource', id] });
      queryClient.invalidateQueries({ queryKey: ['resources'] });
    },
  });
};
```

### Action Route Mutation

For non-CRUD actions like publish/archive:

```typescript
export const usePublishResource = () => {
  return useMutation({
    mutationFn: (id: string) => {
      return resourceApi.publishResource(id);
    },
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['resource', id] });
      queryClient.invalidateQueries({ queryKey: ['resources'] });
      // Also invalidate related queries if needed
      queryClient.invalidateQueries({ queryKey: ['resource-versions'] });
    },
  });
};
```

## Using Hooks in Components

```typescript
import { useGetResources, useDeleteResource } from '../hooks';

function ResourceList() {
  // Fetch data
  const { data, isLoading, error } = useGetResources({ limit: 50 });

  // Mutation
  const deleteResource = useDeleteResource();

  const handleDelete = (id: string) => {
    deleteResource.mutate(id, {
      onSuccess: () => console.log('Deleted!'),
      onError: (err) => console.error(err),
    });
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {data?.results.map((resource) => (
        <li key={resource.id}>
          {resource.name}
          <button
            onClick={() => handleDelete(resource.id)}
            disabled={deleteResource.isPending}
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}
```

## Complete Example

See existing implementation:
- API module: `apps/webapp/src/api/workflows.ts`
- Hooks: `apps/webapp/src/hooks/useWorkflows.ts`

## Checklist

After creating hooks for a new resource:

1. **Ensure API schemas exist** in `libs/types/src/api/{resource}.ts`
2. **Create API module** in `apps/webapp/src/api/{resource}.ts`
3. **Create hooks file** in `apps/webapp/src/hooks/use{Resource}s.ts`
4. **Export hooks** from `apps/webapp/src/hooks/index.ts`
5. **Verify TypeScript compilation** passes
6. **Test hooks** in a component

## Important Notes

1. **Always invalidate related queries** after mutations to keep data fresh
2. **Use `enabled` option** on queries that depend on parameters that might be null/undefined
3. **Import types from `@{project}/types`** for type safety
4. **Re-export body types** from API files for component convenience
5. **Use `z.input` types** for query params (keeps defaults optional)
6. **Use `z.infer` types** for response types (shows final shape after validation)

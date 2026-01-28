---
name: backend-route-creation
description: Create a new backend API route with koa-zod-router and Zod validation. Use when asked to "create a route", "add an endpoint", "create API endpoint", or "add a new route".
---

# Backend Route Creation

This skill creates new API routes using `koa-zod-router` with Zod validation schemas following established patterns.

## Overview

Routes use schemas defined in `@{project}/types` for validation. This ensures type safety between backend and frontend.

## Route File Structure

Routes are organized by resource in `apps/backend/src/routes/`:

```
apps/backend/src/routes/
├── workflows.ts        # /api/workflows endpoints
├── workflow-runs.ts    # /api/workflow-runs endpoints
└── {resource}.ts       # New resource routes
```

## Step 1: Define API Schemas in @{project}/types

First, create schemas in `libs/types/src/api/{resource}.ts`:

```typescript
// libs/types/src/api/{resource}.ts
import { z } from 'zod/v3';
import { ResourceStatusOptions } from '../lib/Resource'; // Import enum options if any
import {
  paginationQuerySchema,
  idParamSchema,
  listResponseSchema,
  singleResponseSchema,
  messageResponseSchema,
} from './common';

// ============================================
// Resource Entity Schema (for responses)
// ============================================

export const resourceSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string().optional(),
  status: z.enum(ResourceStatusOptions),
  createdAt: z.coerce.date(),
  updatedAt: z.coerce.date(),
});

// ============================================
// GET /api/resources - List Resources
// ============================================

export const listResourcesQuerySchema = paginationQuerySchema.extend({
  status: z.enum(ResourceStatusOptions).optional(),
  search: z.string().optional(),
});

export const listResourcesResponseSchema = listResponseSchema(resourceSchema);

// Use z.input for query types (parameters with defaults should be optional)
export type ListResourcesQuery = z.input<typeof listResourcesQuerySchema>;
export type ListResourcesResponse = z.infer<typeof listResourcesResponseSchema>;

// ============================================
// GET /api/resources/:id - Get Resource
// ============================================

export const getResourceParamsSchema = idParamSchema;
export const getResourceResponseSchema = singleResponseSchema(resourceSchema);

export type GetResourceParams = z.infer<typeof getResourceParamsSchema>;
export type GetResourceResponse = z.infer<typeof getResourceResponseSchema>;

// ============================================
// POST /api/resources - Create Resource
// ============================================

export const createResourceBodySchema = z.object({
  name: z.string().min(1),
  description: z.string().optional(),
  // Add required fields for creation
});

export const createResourceResponseSchema = singleResponseSchema(resourceSchema);

export type CreateResourceBody = z.infer<typeof createResourceBodySchema>;
export type CreateResourceResponse = z.infer<typeof createResourceResponseSchema>;

// ============================================
// PUT /api/resources/:id - Update Resource
// ============================================

export const updateResourceParamsSchema = idParamSchema;

export const updateResourceBodySchema = z.object({
  name: z.string().min(1).optional(),
  description: z.string().optional(),
  // All fields optional for partial updates
});

export const updateResourceResponseSchema = singleResponseSchema(resourceSchema);

export type UpdateResourceParams = z.infer<typeof updateResourceParamsSchema>;
export type UpdateResourceBody = z.infer<typeof updateResourceBodySchema>;
export type UpdateResourceResponse = z.infer<typeof updateResourceResponseSchema>;

// ============================================
// DELETE /api/resources/:id - Delete Resource
// ============================================

export const deleteResourceParamsSchema = idParamSchema;
export const deleteResourceResponseSchema = messageResponseSchema;

export type DeleteResourceParams = z.infer<typeof deleteResourceParamsSchema>;
export type DeleteResourceResponse = z.infer<typeof deleteResourceResponseSchema>;
```

Then export from `libs/types/src/api/index.ts`:

```typescript
export * from './{resource}';
```

## Step 2: Create the Route File

Create `apps/backend/src/routes/{resource}.ts`:

```typescript
import zodRouter from 'koa-zod-router';

import Resource from '../models/Resource';
import {
  // Query/Params schemas
  listResourcesQuerySchema,
  getResourceParamsSchema,
  updateResourceParamsSchema,
  deleteResourceParamsSchema,
  // Body schemas
  createResourceBodySchema,
  updateResourceBodySchema,
} from '@{project}/types';

const router = zodRouter();

// GET /api/resources - List all
router.register({
  method: 'get',
  path: '/',
  validate: {
    query: listResourcesQuerySchema,
  },
  handler: async (ctx) => {
    const { skip, limit, status, search } = ctx.request.query;

    const query: Record<string, unknown> = {};
    if (status) query.status = status;
    if (search) query.name = { $regex: search, $options: 'i' };

    const results = await Resource.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit);

    const total = await Resource.countDocuments(query);

    ctx.status = 200;
    ctx.body = { total, results };
  },
});

// GET /api/resources/:id - Get by ID
router.register({
  method: 'get',
  path: '/:id',
  validate: {
    params: getResourceParamsSchema,
  },
  handler: async (ctx) => {
    const { id } = ctx.request.params;

    const result = await Resource.findOne({ id });

    if (!result) {
      ctx.status = 404;
      ctx.body = { message: 'Resource not found' };
      return;
    }

    ctx.status = 200;
    ctx.body = { result };
  },
});

// POST /api/resources - Create
router.register({
  method: 'post',
  path: '/',
  validate: {
    body: createResourceBodySchema,
  },
  handler: async (ctx) => {
    const body = ctx.request.body;

    const result = new Resource(body);
    await result.save();

    ctx.status = 201;
    ctx.body = { result };
  },
});

// PUT /api/resources/:id - Update
router.register({
  method: 'put',
  path: '/:id',
  validate: {
    params: updateResourceParamsSchema,
    body: updateResourceBodySchema,
  },
  handler: async (ctx) => {
    const { id } = ctx.request.params;
    const updates = ctx.request.body;

    const result = await Resource.findOne({ id });

    if (!result) {
      ctx.status = 404;
      ctx.body = { message: 'Resource not found' };
      return;
    }

    Object.assign(result, updates);
    await result.save();

    ctx.status = 200;
    ctx.body = { result };
  },
});

// DELETE /api/resources/:id - Delete
router.register({
  method: 'delete',
  path: '/:id',
  validate: {
    params: deleteResourceParamsSchema,
  },
  handler: async (ctx) => {
    const { id } = ctx.request.params;

    const result = await Resource.findOne({ id });

    if (!result) {
      ctx.status = 404;
      ctx.body = { message: 'Resource not found' };
      return;
    }

    await Resource.deleteOne({ id });

    ctx.status = 200;
    ctx.body = { message: 'Resource deleted' };
  },
});

export default router;
```

## Step 3: Mount the Route in main.ts

Add to `apps/backend/src/main.ts`:

```typescript
import resourceRoutes from './routes/{resource}';

// ... existing middleware ...

// Mount routes
app.use(mount('/api/{resource}', resourceRoutes.routes()));
```

## Zod Schema Patterns

### Query Parameters (in @{project}/types)

Use `z.coerce` for converting string query params:

```typescript
export const listQuerySchema = paginationQuerySchema.extend({
  status: z.enum(['active', 'inactive']).optional(),
  includeArchived: z.coerce.boolean().optional().default(false),
  search: z.string().optional(),
});

// IMPORTANT: Use z.input for query types so defaults remain optional
export type ListQuery = z.input<typeof listQuerySchema>;
```

### URL Parameters

```typescript
export const resourceParamsSchema = z.object({
  id: z.string(),
  // For numeric IDs: userId: z.coerce.number(),
});
```

### Request Body

```typescript
// Create schema - required fields
export const createBodySchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  roles: z.array(z.enum(['admin', 'user', 'guest'])),
  metadata: z.object({
    source: z.string().optional(),
    tags: z.array(z.string()).optional(),
  }).optional(),
});

// Update schema - all fields optional
export const updateBodySchema = z.object({
  name: z.string().min(1).optional(),
  email: z.string().email().optional(),
  roles: z.array(z.enum(['admin', 'user', 'guest'])).optional(),
});
```

### Using Shared Type Options

Import enum options from `@{project}/types`:

```typescript
import { StatusOptions, RoleOptions } from '@{project}/types';

export const schema = z.object({
  status: z.enum(StatusOptions),
  role: z.enum(RoleOptions),
});
```

## Route Handler Patterns

### Standard List Response

```typescript
ctx.status = 200;
ctx.body = {
  total: count,
  results: items,
};
```

### Standard Single Response

```typescript
ctx.status = 200;
ctx.body = { result: item };
```

### Standard Create Response

```typescript
ctx.status = 201;
ctx.body = { result: newItem };
```

### Standard Error Responses

```typescript
// Not found
ctx.status = 404;
ctx.body = { message: 'Resource not found' };
return;

// Bad request
ctx.status = 400;
ctx.body = { message: 'Invalid input', details: '...' };
return;

// Forbidden
ctx.status = 403;
ctx.body = { message: 'Access denied' };
return;
```

### Filtering in List Endpoints

```typescript
handler: async (ctx) => {
  const { skip, limit, status, search } = ctx.request.query;

  const query: Record<string, unknown> = {};

  if (status) {
    query.status = status;
  }

  if (search) {
    query.name = { $regex: search, $options: 'i' };
  }

  const results = await Model.find(query)
    .sort({ createdAt: -1 })
    .skip(skip)
    .limit(limit);

  const total = await Model.countDocuments(query);

  ctx.status = 200;
  ctx.body = { total, results };
}
```

### Action Routes

For non-CRUD actions like `/api/workflows/:id/publish`:

```typescript
// In @{project}/types: define the schema
export const publishResourceParamsSchema = idParamSchema;
export const publishResourceResponseSchema = singleResponseSchema(resourceSchema);

// In route file:
router.register({
  method: 'post',
  path: '/:id/publish',
  validate: {
    params: publishResourceParamsSchema,
  },
  handler: async (ctx) => {
    const { id } = ctx.request.params;

    const resource = await Resource.findOne({ id });

    if (!resource) {
      ctx.status = 404;
      ctx.body = { message: 'Resource not found' };
      return;
    }

    if (resource.status === 'published') {
      ctx.status = 400;
      ctx.body = { message: 'Resource is already published' };
      return;
    }

    resource.status = 'published';
    resource.publishedAt = new Date();
    await resource.save();

    ctx.status = 200;
    ctx.body = { result: resource };
  },
});
```

## Complete Example

See existing implementation:
- Schemas: `libs/types/src/api/workflows.ts`
- Routes: `apps/backend/src/routes/workflows.ts`

## Checklist

After creating a new route:

1. **Create API schemas** in `libs/types/src/api/{resource}.ts`
2. **Export schemas** from `libs/types/src/api/index.ts`
3. **Build types library**: `npx tsc -b libs/types/tsconfig.lib.json`
4. **Create the route file** in `apps/backend/src/routes/`
5. **Import and mount** in `main.ts` with `app.use(mount('/api/{path}', routes.routes()))`
6. **Test the endpoints** with curl or your API client
7. **Create corresponding frontend API module** in `apps/webapp/src/api/`
8. **Create React Query hooks** in `apps/webapp/src/hooks/`

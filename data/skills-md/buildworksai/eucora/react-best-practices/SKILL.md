---
name: react-best-practices
description: React + TypeScript development patterns for EUCORA frontend. Use when building React components, managing state, or creating UI features. Includes contracts.ts patterns, TanStack Query, Zustand, and shadcn/ui guidelines.
status: ✅ Working
last-validated: 2026-01-30
---

# React Best Practices for EUCORA

React + TypeScript patterns aligned with EUCORA's tech stack and architectural requirements.

---

## Quick Reference

| Requirement | Pattern |
|-------------|---------|
| State (Server) | TanStack Query (React Query) |
| State (Client) | Zustand |
| Components | shadcn/ui + Radix UI |
| Forms | React Hook Form + Zod |
| Styling | Tailwind CSS |
| Types | contracts.ts per domain |
| API Endpoints | ENDPOINTS constant from contracts.ts |

---

## FORBIDDEN Technologies

❌ **DO NOT USE** — Violates EUCORA tech stack rules:

- Redux / Redux Toolkit / redux-saga / redux-thunk
- Next.js
- MobX, Jotai, Recoil
- tRPC
- Apollo GraphQL
- Vue.js / Svelte / Angular

---

## contracts.ts Pattern (MANDATORY)

Every frontend domain MUST have a `contracts.ts` file defining types and endpoints.

### File Location

```
frontend/src/routes/{domain}/contracts.ts
frontend/src/{app}/contracts.ts
```

### contracts.ts Structure

```typescript
// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 BuildWorks.AI

/**
 * Deployment domain contracts.
 */

// API Endpoints - NEVER hardcode URLs in components
export const ENDPOINTS = {
  LIST: '/api/v1/deployments/',
  DETAIL: (id: string) => `/api/v1/deployments/${id}/`,
  APPROVE: (id: string) => `/api/v1/deployments/${id}/approve/`,
  REJECT: (id: string) => `/api/v1/deployments/${id}/reject/`,
} as const;

// Request/Response types
export interface Deployment {
  id: string;
  correlation_id: string;
  name: string;
  status: DeploymentStatus;
  risk_score: number;
  target_ring: number;
  created_at: string;
  updated_at: string;
}

export type DeploymentStatus =
  | 'pending'
  | 'approved'
  | 'rejected'
  | 'in_progress'
  | 'completed'
  | 'failed';

export interface CreateDeploymentRequest {
  application_id: string;
  version: string;
  target_ring: number;
}
```

### Using contracts.ts in Components

```typescript
// ✅ CORRECT - Import from contracts
import { ENDPOINTS, Deployment } from './contracts';

const { data } = useQuery<Deployment[]>({
  queryKey: ['deployments'],
  queryFn: () => api.get(ENDPOINTS.LIST),
});

// ❌ FORBIDDEN - Hardcoded URLs
const { data } = useQuery({
  queryFn: () => api.get('/api/v1/deployments/'),  // Never do this!
});
```

---

## State Management

### Server State (TanStack Query)

Use TanStack Query for all API data fetching:

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ENDPOINTS, Deployment, CreateDeploymentRequest } from './contracts';

// Query hook
export function useDeployments() {
  return useQuery<Deployment[]>({
    queryKey: ['deployments'],
    queryFn: () => api.get(ENDPOINTS.LIST),
  });
}

// Mutation hook
export function useApproveDeployment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => api.post(ENDPOINTS.APPROVE(id)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deployments'] });
    },
  });
}
```

### Client State (Zustand)

Use Zustand for UI state only:

```typescript
import { create } from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  demoMode: boolean;
  toggleSidebar: () => void;
  setDemoMode: (value: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  demoMode: false,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setDemoMode: (value) => set({ demoMode: value }),
}));
```

---

## Component Patterns

### shadcn/ui + Radix UI

Use shadcn/ui components built on Radix UI:

```typescript
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Dialog, DialogTrigger, DialogContent } from '@/components/ui/dialog';

function DeploymentCard({ deployment }: { deployment: Deployment }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{deployment.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>Risk Score: {deployment.risk_score}</p>
        <Dialog>
          <DialogTrigger asChild>
            <Button>View Details</Button>
          </DialogTrigger>
          <DialogContent>
            {/* Dialog content */}
          </DialogContent>
        </Dialog>
      </CardContent>
    </Card>
  );
}
```

### Component File Structure

```typescript
// DeploymentList.tsx

// 1. License header
// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 BuildWorks.AI

// 2. Imports (grouped)
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';

import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

import { ENDPOINTS, Deployment } from './contracts';
import { useDeployments } from './hooks';

// 3. Types (if component-specific)
interface DeploymentListProps {
  filter?: DeploymentStatus;
}

// 4. Component
export function DeploymentList({ filter }: DeploymentListProps) {
  const { data, isLoading, error } = useDeployments();

  // Handle loading state
  if (isLoading) return <LoadingSpinner />;

  // Handle error state
  if (error) return <ErrorDisplay error={error} />;

  return (
    <div className="space-y-4">
      {data?.map((deployment) => (
        <DeploymentCard key={deployment.id} deployment={deployment} />
      ))}
    </div>
  );
}
```

---

## Forms (React Hook Form + Zod)

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

import { Form, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

import { CreateDeploymentRequest } from './contracts';

// Validation schema
const deploymentSchema = z.object({
  application_id: z.string().uuid(),
  version: z.string().regex(/^\d+\.\d+\.\d+$/, 'Must be semantic version (X.Y.Z)'),
  target_ring: z.number().min(0).max(4),
});

type FormData = z.infer<typeof deploymentSchema>;

function CreateDeploymentForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const form = useForm<FormData>({
    resolver: zodResolver(deploymentSchema),
    defaultValues: {
      application_id: '',
      version: '',
      target_ring: 0,
    },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="version"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Version</FormLabel>
              <Input {...field} placeholder="1.0.0" />
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Create Deployment</Button>
      </form>
    </Form>
  );
}
```

---

## Styling (Tailwind CSS)

### Use Semantic Colors

```typescript
// ✅ CORRECT - Use semantic Tailwind classes
<div className="bg-primary text-primary-foreground">
<span className="text-muted-foreground">
<Badge className="bg-destructive">

// ❌ FORBIDDEN - Hardcoded colors
<div style={{ backgroundColor: '#1565C0' }}>
```

### Dark Mode Support

```typescript
// Tailwind handles dark mode automatically
<div className="bg-white dark:bg-slate-900">
  <p className="text-gray-900 dark:text-gray-100">
    Content adapts to system preference
  </p>
</div>
```

---

## Hooks Best Practices

### Rules of Hooks

```typescript
// ✅ CORRECT - Hooks before conditional returns
function DeploymentDetail({ id }: { id: string }) {
  const { data, isLoading } = useQuery({ /* ... */ });
  const [isEditing, setIsEditing] = useState(false);

  // Conditional returns AFTER hooks
  if (isLoading) return <Spinner />;
  if (!data) return <NotFound />;

  return <DeploymentCard deployment={data} />;
}

// ❌ FORBIDDEN - Hooks after conditional
function DeploymentDetail({ id }: { id: string }) {
  if (!id) return null;  // Return before hook!

  const { data } = useQuery({ /* ... */ });  // Violates Rules of Hooks
}
```

### Custom Hooks

Extract reusable logic:

```typescript
// hooks/useDeploymentApproval.ts
export function useDeploymentApproval(deploymentId: string) {
  const queryClient = useQueryClient();
  const [isApproving, setIsApproving] = useState(false);

  const approve = useMutation({
    mutationFn: () => api.post(ENDPOINTS.APPROVE(deploymentId)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deployments'] });
      toast.success('Deployment approved');
    },
    onError: (error) => {
      toast.error(`Approval failed: ${error.message}`);
    },
  });

  return {
    approve: approve.mutate,
    isApproving: approve.isPending,
  };
}
```

---

## Performance

### Memoization

```typescript
import { memo, useMemo, useCallback } from 'react';

// Memoize expensive components
const DeploymentCard = memo(function DeploymentCard({ deployment }: Props) {
  return <Card>{/* ... */}</Card>;
});

// Memoize expensive computations
function DeploymentStats({ deployments }: { deployments: Deployment[] }) {
  const stats = useMemo(() => ({
    total: deployments.length,
    pending: deployments.filter(d => d.status === 'pending').length,
    avgRisk: deployments.reduce((sum, d) => sum + d.risk_score, 0) / deployments.length,
  }), [deployments]);

  return <StatsDisplay stats={stats} />;
}

// Stable callbacks
const handleApprove = useCallback((id: string) => {
  approveMutation.mutate(id);
}, [approveMutation]);
```

### Lazy Loading

```typescript
import { lazy, Suspense } from 'react';

// Lazy load route components
const DeploymentDashboard = lazy(() => import('./routes/DeploymentDashboard'));
const CABWorkflow = lazy(() => import('./routes/CABWorkflow'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/deployments" element={<DeploymentDashboard />} />
        <Route path="/cab" element={<CABWorkflow />} />
      </Routes>
    </Suspense>
  );
}
```

---

## Checklist

### Before Writing React Code

```
☐ Check if contracts.ts exists for this domain
☐ Verify types are imported from contracts.ts
☐ Use ENDPOINTS constant for API URLs
☐ Use shadcn/ui components (not custom)
```

### After Writing React Code

```
☐ Run TypeScript check: npx tsc --noEmit
☐ Run ESLint: npx eslint src/ --max-warnings 0
☐ Verify hooks are called before conditional returns
☐ Check for hardcoded URLs (use ENDPOINTS)
☐ Verify loading/error states are handled
```

---

## Anti-Patterns to Avoid

| ❌ FORBIDDEN | ✅ CORRECT |
|--------------|------------|
| Redux/MobX/Recoil | Zustand for client state |
| Hardcoded API URLs | ENDPOINTS from contracts.ts |
| `any` type | Explicit TypeScript types |
| Hooks after conditionals | Hooks before all returns |
| Inline styles with hex colors | Tailwind semantic classes |
| Class components | Functional components |

---
name: Supabase React Best Practices
description: Comprehensive guide for building production-ready React applications with Supabase, TypeScript, and TanStack Query. Use when implementing auth, data fetching, real-time features, or optimizing Supabase integration.
---

# Supabase + React Best Practices

Expert guide for building scalable, performant React applications with Supabase.

## When to Use This Skill

- Setting up new Supabase + React project
- Implementing authentication flows
- Creating data fetching hooks with TanStack Query
- Adding real-time subscriptions
- Optimizing database queries
- Setting up TypeScript types
- Debugging Supabase integration issues

---

## Quick Start Checklist

```typescript
// ✅ Essential Setup
- [ ] Install: @supabase/supabase-js @tanstack/react-query
- [ ] Generate TypeScript types from schema
- [ ] Create typed Supabase client
- [ ] Set up TanStack Query provider
- [ ] Configure environment variables
- [ ] Set up auth context/provider
```

---

## 1. Project Structure (Best Practice)

```
src/
├── integrations/
│   └── supabase/
│       ├── client.ts          # Supabase client singleton
│       ├── types.ts           # Generated DB types
│       └── auth.tsx           # Auth context provider
├── features/
│   └── [feature]/
│       ├── hooks/
│       │   ├── use[Feature].ts       # Query hooks
│       │   └── use[Feature]Mutations.ts  # Mutation hooks
│       ├── components/
│       └── types.ts
└── lib/
    └── queryClient.ts         # TanStack Query config
```

**Why This Structure:**
- Clear separation of concerns
- Reusable hooks across features
- Type safety throughout
- Easy to test and maintain

---

## 2. TypeScript Setup (CRITICAL)

### Generate Types from Database

```bash
# Generate types (run after every migration)
npx supabase gen types typescript --project-id YOUR_PROJECT_ID > src/integrations/supabase/types.ts

# Or use local
npx supabase gen types typescript --local > src/integrations/supabase/types.ts
```

### Create Typed Client

**File:** `src/integrations/supabase/client.ts`

```typescript
import { createClient } from '@supabase/supabase-js';
import type { Database } from './types';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

// ✅ Typed Supabase client
export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true
  }
});

// Export types for convenience
export type Tables<T extends keyof Database['public']['Tables']> =
  Database['public']['Tables'][T]['Row'];
export type Enums<T extends keyof Database['public']['Enums']> =
  Database['public']['Enums'][T];
```

**Benefits:**
- Full IntelliSense for all tables
- Type-safe queries
- Catch errors at compile time
- Better refactoring support

---

## 3. Authentication Patterns

### Pattern 1: Auth Context Provider (Recommended)

**File:** `src/integrations/supabase/auth.tsx`

```typescript
import { createContext, useContext, useEffect, useState } from 'react';
import { User, Session } from '@supabase/supabase-js';
import { supabase } from './client';

interface AuthContext {
  user: User | null;
  session: Session | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContext | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) throw error;
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  };

  return (
    <AuthContext.Provider value={{ user, session, loading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

**Usage:**

```typescript
// App.tsx
import { AuthProvider } from '@/integrations/supabase/auth';

function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}

// In components
function Profile() {
  const { user, loading } = useAuth();

  if (loading) return <Spinner />;
  if (!user) return <Navigate to="/login" />;

  return <div>Welcome {user.email}</div>;
}
```

### Pattern 2: Protected Routes

```typescript
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '@/integrations/supabase/auth';

export function ProtectedRoute() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return user ? <Outlet /> : <Navigate to="/login" replace />;
}

// In router config
<Route element={<ProtectedRoute />}>
  <Route path="/dashboard" element={<Dashboard />} />
  <Route path="/profile" element={<Profile />} />
</Route>
```

---

## 4. Data Fetching with TanStack Query

### Setup Query Client

**File:** `src/lib/queryClient.ts`

```typescript
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

### Query Hooks Pattern

**File:** `src/features/events/hooks/useEvents.ts`

```typescript
import { useQuery } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';
import type { Tables } from '@/integrations/supabase/client';

type Event = Tables<'events'>;

/**
 * Fetch all published events
 *
 * @example
 * const { data, isLoading, error } = useEvents();
 */
export function useEvents() {
  return useQuery({
    queryKey: ['events'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('events')
        .select('*')
        .eq('status', 'published')
        .order('start_at', { ascending: true });

      if (error) throw error;
      return data as Event[];
    },
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Fetch single event by ID
 */
export function useEvent(id: string) {
  return useQuery({
    queryKey: ['event', id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('events')
        .select('*, venue:venues(*)')
        .eq('id', id)
        .single();

      if (error) throw error;
      return data;
    },
    enabled: !!id, // Only run if ID provided
    staleTime: 5 * 60 * 1000,
  });
}
```

### Mutation Hooks Pattern

**File:** `src/features/events/hooks/useEventMutations.ts`

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';
import type { Tables } from '@/integrations/supabase/client';

type EventInsert = Tables<'events'>['Insert'];
type EventUpdate = Tables<'events'>['Update'];

export function useCreateEvent() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (event: EventInsert) => {
      const { data, error } = await supabase
        .from('events')
        .insert(event)
        .select()
        .single();

      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      // Invalidate queries to refetch
      queryClient.invalidateQueries({ queryKey: ['events'] });
    },
  });
}

export function useUpdateEvent() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, ...updates }: { id: string } & EventUpdate) => {
      const { data, error } = await supabase
        .from('events')
        .update(updates)
        .eq('id', id)
        .select()
        .single();

      if (error) throw error;
      return data;
    },
    onSuccess: (data) => {
      // Invalidate list and single item
      queryClient.invalidateQueries({ queryKey: ['events'] });
      queryClient.invalidateQueries({ queryKey: ['event', data.id] });
    },
  });
}

export function useDeleteEvent() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      const { error } = await supabase
        .from('events')
        .delete()
        .eq('id', id);

      if (error) throw error;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['events'] });
    },
  });
}
```

**Usage in Components:**

```typescript
function EventForm() {
  const createEvent = useCreateEvent();
  const updateEvent = useUpdateEvent();

  const handleSubmit = async (values) => {
    try {
      if (editMode) {
        await updateEvent.mutateAsync({ id: eventId, ...values });
        toast.success('Event updated!');
      } else {
        await createEvent.mutateAsync(values);
        toast.success('Event created!');
      }
    } catch (error) {
      toast.error(error.message);
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

---

## 5. Real-Time Subscriptions

### Pattern: Real-Time Hook

```typescript
import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';

export function useEventsSubscription() {
  const queryClient = useQueryClient();

  useEffect(() => {
    const channel = supabase
      .channel('events-changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'events',
        },
        (payload) => {
          console.log('Event change:', payload);

          // Invalidate queries to refetch
          queryClient.invalidateQueries({ queryKey: ['events'] });

          // Or update cache directly (optimistic)
          if (payload.eventType === 'INSERT') {
            queryClient.setQueryData(['events'], (old: any[]) => [
              ...(old || []),
              payload.new,
            ]);
          }
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [queryClient]);
}

// Usage
function EventsList() {
  const { data: events, isLoading } = useEvents();
  useEventsSubscription(); // Auto-refetch on changes

  return <div>{events?.map(...)}</div>;
}
```

---

## 6. Advanced Query Patterns

### Filtering with Parameters

```typescript
export function useEvents(filters?: {
  status?: string;
  type?: string;
  search?: string;
}) {
  return useQuery({
    queryKey: ['events', filters],
    queryFn: async () => {
      let query = supabase
        .from('events')
        .select('*');

      if (filters?.status) {
        query = query.eq('status', filters.status);
      }

      if (filters?.type) {
        query = query.eq('type', filters.type);
      }

      if (filters?.search) {
        query = query.ilike('name', `%${filters.search}%`);
      }

      const { data, error } = await query.order('start_at', { ascending: true });

      if (error) throw error;
      return data;
    },
    enabled: true,
  });
}
```

### Pagination

```typescript
export function useEventsPaginated(page: number, pageSize: number = 10) {
  return useQuery({
    queryKey: ['events', 'paginated', page, pageSize],
    queryFn: async () => {
      const from = page * pageSize;
      const to = from + pageSize - 1;

      const { data, error, count } = await supabase
        .from('events')
        .select('*', { count: 'exact' })
        .range(from, to)
        .order('start_at', { ascending: false });

      if (error) throw error;

      return {
        events: data,
        total: count || 0,
        totalPages: Math.ceil((count || 0) / pageSize),
      };
    },
  });
}
```

### Complex Joins

```typescript
export function useEventWithDetails(id: string) {
  return useQuery({
    queryKey: ['event', 'details', id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('events')
        .select(`
          *,
          venue:venues(*),
          organizer:profiles(id, full_name, avatar_url),
          tickets:ticket_tiers(*),
          bookings:orders(
            id,
            status,
            total_amount,
            attendee:attendees(*)
          )
        `)
        .eq('id', id)
        .single();

      if (error) throw error;
      return data;
    },
    enabled: !!id,
  });
}
```

---

## 7. Row Level Security (RLS) Best Practices

### Understanding RLS in React

**Problem:** Your React app uses the `anon` key, which has limited permissions.

**Solution:** RLS policies control what data users can access based on `auth.uid()`.

### Testing RLS Policies

```typescript
// Helper to test if user can access data
export async function testRLS() {
  const { data: { user } } = await supabase.auth.getUser();

  console.log('Current user:', user?.id);

  // Test read access
  const { data, error } = await supabase
    .from('events')
    .select('*');

  if (error) {
    console.error('RLS blocking access:', error);
  } else {
    console.log('Accessible events:', data);
  }
}
```

### Common RLS Patterns for React

```sql
-- Allow public read, authenticated insert
CREATE POLICY "Public events are viewable by everyone"
  ON events FOR SELECT
  USING (visibility = 'public');

CREATE POLICY "Users can insert their own events"
  ON events FOR INSERT
  WITH CHECK (auth.uid() = organizer_id);

CREATE POLICY "Users can update their own events"
  ON events FOR UPDATE
  USING (auth.uid() = organizer_id);
```

### Handling RLS Errors in React

```typescript
export function useEvents() {
  return useQuery({
    queryKey: ['events'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('events')
        .select('*');

      // RLS will return error if blocked
      if (error) {
        if (error.code === 'PGRST301') {
          throw new Error('You do not have permission to view these events');
        }
        throw error;
      }

      return data;
    },
    retry: false, // Don't retry RLS errors
  });
}
```

---

## 8. Error Handling Patterns

### Global Error Boundary

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { toast } from 'sonner';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      onError: (error: any) => {
        // Handle RLS errors
        if (error.code === 'PGRST301') {
          toast.error('Access denied. Please check your permissions.');
          return;
        }

        // Handle auth errors
        if (error.message?.includes('JWT')) {
          toast.error('Session expired. Please log in again.');
          // Optionally redirect to login
          return;
        }

        // Generic error
        toast.error(error.message || 'Something went wrong');
      },
    },
    mutations: {
      onError: (error: any) => {
        toast.error(error.message || 'Failed to save changes');
      },
    },
  },
});
```

### Component-Level Error Handling

```typescript
function EventsList() {
  const { data, isLoading, error } = useEvents();

  if (isLoading) {
    return <Skeleton count={5} />;
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTitle>Error loading events</AlertTitle>
        <AlertDescription>{error.message}</AlertDescription>
      </Alert>
    );
  }

  if (!data || data.length === 0) {
    return (
      <EmptyState
        title="No events yet"
        description="Get started by creating your first event"
        action={<Button>Create Event</Button>}
      />
    );
  }

  return <div>{data.map(...)}</div>;
}
```

---

## 9. Performance Optimization

### 1. Selective Field Fetching

```typescript
// ❌ Bad: Fetching all fields
const { data } = await supabase.from('events').select('*');

// ✅ Good: Only fetch what you need
const { data } = await supabase
  .from('events')
  .select('id, name, start_at, price_cents');
```

### 2. Query Key Strategies

```typescript
// Hierarchical query keys for better caching
const queryKeys = {
  all: ['events'] as const,
  lists: () => [...queryKeys.all, 'list'] as const,
  list: (filters: string) => [...queryKeys.lists(), filters] as const,
  details: () => [...queryKeys.all, 'detail'] as const,
  detail: (id: string) => [...queryKeys.details(), id] as const,
};

// Usage
useQuery({ queryKey: queryKeys.list('published') });
useQuery({ queryKey: queryKeys.detail(eventId) });

// Invalidate all events
queryClient.invalidateQueries({ queryKey: queryKeys.all });

// Invalidate only lists
queryClient.invalidateQueries({ queryKey: queryKeys.lists() });
```

### 3. Optimistic Updates

```typescript
export function useUpdateEvent() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, ...updates }) => {
      const { data, error } = await supabase
        .from('events')
        .update(updates)
        .eq('id', id)
        .select()
        .single();

      if (error) throw error;
      return data;
    },
    onMutate: async ({ id, ...updates }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['event', id] });

      // Snapshot previous value
      const previousEvent = queryClient.getQueryData(['event', id]);

      // Optimistically update
      queryClient.setQueryData(['event', id], (old: any) => ({
        ...old,
        ...updates,
      }));

      return { previousEvent };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousEvent) {
        queryClient.setQueryData(
          ['event', variables.id],
          context.previousEvent
        );
      }
    },
    onSettled: (data, error, variables) => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['event', variables.id] });
    },
  });
}
```

### 4. Prefetching for Better UX

```typescript
function EventCard({ event }) {
  const queryClient = useQueryClient();

  const prefetchEvent = () => {
    queryClient.prefetchQuery({
      queryKey: ['event', event.id],
      queryFn: () => fetchEventDetails(event.id),
    });
  };

  return (
    <Card onMouseEnter={prefetchEvent}>
      <Link to={`/events/${event.id}`}>{event.name}</Link>
    </Card>
  );
}
```

---

## 10. Security Best Practices

### 1. Never Expose Service Role Key

```typescript
// ❌ NEVER do this in client-side code
const supabase = createClient(url, SERVICE_ROLE_KEY);

// ✅ Always use anon key in React
const supabase = createClient(url, ANON_KEY);
```

### 2. Use RLS, Not Client-Side Checks

```typescript
// ❌ Bad: Client-side authorization
function deleteEvent(id: string) {
  if (user.role !== 'admin') {
    toast.error('Not authorized');
    return;
  }
  // Delete event
}

// ✅ Good: Let RLS handle it
function deleteEvent(id: string) {
  // RLS policy will block if user isn't authorized
  supabase.from('events').delete().eq('id', id);
}
```

### 3. Validate Input Data

```typescript
import { z } from 'zod';

const eventSchema = z.object({
  name: z.string().min(3).max(100),
  description: z.string().max(5000),
  price_cents: z.number().int().positive(),
  start_at: z.string().datetime(),
});

export function useCreateEvent() {
  return useMutation({
    mutationFn: async (event: unknown) => {
      // Validate before sending to Supabase
      const validated = eventSchema.parse(event);

      const { data, error } = await supabase
        .from('events')
        .insert(validated)
        .select()
        .single();

      if (error) throw error;
      return data;
    },
  });
}
```

### 4. Sanitize User Input

```typescript
// Prevent SQL injection in text search
export function useSearchEvents(query: string) {
  const sanitized = query.replace(/[%_]/g, '\\$&');

  return useQuery({
    queryKey: ['events', 'search', sanitized],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('events')
        .select('*')
        .ilike('name', `%${sanitized}%`);

      if (error) throw error;
      return data;
    },
  });
}
```

---

## 11. Testing Patterns

### Mock Supabase Client

**File:** `src/__tests__/mocks/supabase.ts`

```typescript
import { vi } from 'vitest';

export const mockSupabase = {
  from: vi.fn(() => ({
    select: vi.fn(() => ({
      eq: vi.fn(() => ({
        single: vi.fn(() => Promise.resolve({ data: null, error: null })),
      })),
    })),
    insert: vi.fn(() => ({
      select: vi.fn(() => ({
        single: vi.fn(() => Promise.resolve({ data: null, error: null })),
      })),
    })),
  })),
  auth: {
    getSession: vi.fn(() => Promise.resolve({ data: { session: null }, error: null })),
    signInWithPassword: vi.fn(),
    signOut: vi.fn(),
  },
};
```

### Test Hooks

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useEvents } from '../useEvents';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return ({ children }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useEvents', () => {
  it('fetches events successfully', async () => {
    const { result } = renderHook(() => useEvents(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toHaveLength(4);
  });
});
```

---

## 12. Common Pitfalls & Solutions

### Pitfall 1: Not Handling Loading States

```typescript
// ❌ Bad: Flash of wrong content
function EventsList() {
  const { data } = useEvents();
  return <div>{data?.map(...)}</div>;
}

// ✅ Good: Proper loading state
function EventsList() {
  const { data, isLoading } = useEvents();

  if (isLoading) {
    return <Skeleton count={5} />;
  }

  return <div>{data?.map(...)}</div>;
}
```

### Pitfall 2: Missing Query Key Dependencies

```typescript
// ❌ Bad: Filters don't refetch
const { data } = useQuery({
  queryKey: ['events'],
  queryFn: () => fetchEvents(filters),
});

// ✅ Good: Include dependencies
const { data } = useQuery({
  queryKey: ['events', filters],
  queryFn: () => fetchEvents(filters),
});
```

### Pitfall 3: Not Invalidating After Mutations

```typescript
// ❌ Bad: Cache not updated
const createEvent = useMutation({
  mutationFn: (event) => supabase.from('events').insert(event),
});

// ✅ Good: Invalidate cache
const createEvent = useMutation({
  mutationFn: (event) => supabase.from('events').insert(event),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['events'] });
  },
});
```

### Pitfall 4: Forgetting to Unsubscribe

```typescript
// ❌ Bad: Memory leak
useEffect(() => {
  const channel = supabase.channel('events');
  channel.subscribe();
  // Missing cleanup!
}, []);

// ✅ Good: Cleanup subscription
useEffect(() => {
  const channel = supabase.channel('events');
  channel.subscribe();

  return () => {
    supabase.removeChannel(channel);
  };
}, []);
```

---

## 13. Debugging Tips

### Enable Query Devtools

```typescript
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### Log Supabase Queries

```typescript
// Add to client.ts for debugging
export const supabase = createClient<Database>(url, key, {
  auth: { /* ... */ },
  global: {
    headers: {
      'x-my-custom-header': 'debug-mode'
    }
  }
});

// Log all queries
const originalFrom = supabase.from.bind(supabase);
supabase.from = (table: string) => {
  console.log(`[Supabase] Querying table: ${table}`);
  return originalFrom(table);
};
```

### Check Network Tab

- Open DevTools → Network tab
- Filter by "supabase.co"
- Check request/response for errors
- Verify RLS headers (x-client-info)

---

## Resources

See `/resources` folder for:
- `query-patterns.ts` - Complete TanStack Query examples
- `auth-patterns.tsx` - Auth provider templates
- `rls-examples.sql` - Common RLS policies
- `testing-setup.ts` - Test configuration
- `migration-guide.md` - Upgrading from Auth Helpers

---

## Quick Reference Commands

```bash
# Generate types
npx supabase gen types typescript --project-id <id> > src/integrations/supabase/types.ts

# Start local Supabase
npx supabase start

# Create migration
npx supabase migration new <name>

# Apply migrations
npx supabase db push

# Reset database
npx supabase db reset
```

---

**Last Updated:** 2025-10-19
**Maintained By:** EventOS Team
**Questions?** Check resources/ folder for detailed examples

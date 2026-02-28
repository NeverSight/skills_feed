---
name: solidjs-solidstart-expert
description: |
  Expert-level SolidJS and SolidStart development skill with 20+ years senior/lead engineer mindset. Comprehensive guidance for building production-ready, scalable web applications with fine-grained reactivity. Use when Claude needs to: (1) Create new SolidJS/SolidStart projects, (2) Implement TanStack Query/Router/Table/Form integration, (3) Build reactive components with signals/stores/resources, (4) Handle SSR/SSG/streaming with SolidStart, (5) Implement authentication and API routes, (6) Optimize bundle size and performance, (7) Debug reactivity issues and memory leaks, (8) Structure large-scale applications, (9) Implement type-safe patterns with TypeScript, (10) Handle error boundaries and suspense, (11) Build accessible UI components, (12) Deploy to Vercel/Netlify/Cloudflare. Triggers: "solid", "solidjs", "solidstart", "createSignal", "createStore", "createResource", "tanstack solid", "vinxi", "fine-grained reactivity".
---

# SolidJS & SolidStart Expert Development Skill

Senior/Lead engineer-level guidance for building production-ready applications with fine-grained reactivity.

## Core Philosophy (KISS, Less is More)

```
1. Signals are primitive. Don't wrap unnecessarily.
2. Derived values > effects. Let reactivity flow naturally.
3. Components are functions called ONCE. Closures handle updates.
4. SSR first, hydrate smart. SolidStart handles this elegantly.
5. Type everything. TypeScript is non-negotiable.
```

## Project Initialization

### SolidStart (Recommended for 95% of projects)

```bash
# Latest SolidStart with TypeScript
npm create solid@latest my-app
# Select: SolidStart, TypeScript, TailwindCSS

# Or with pnpm (recommended)
pnpm create solid@latest my-app
```

### Vanilla SolidJS (Client-only SPAs)

```bash
npx degit solidjs/templates/ts my-app
```

**Decision matrix**: Use SolidStart unless you're building: embeddable widgets, micro-frontends, or have strict no-server requirements.

## Project Structure (Production-Ready)

```
src/
├── routes/                 # File-based routing (SolidStart)
│   ├── index.tsx          # / route
│   ├── about.tsx          # /about route
│   ├── users/
│   │   ├── index.tsx      # /users
│   │   ├── [id].tsx       # /users/:id (dynamic)
│   │   └── [...all].tsx   # /users/* (catch-all)
│   └── api/               # API routes
│       └── users.ts       # /api/users endpoint
├── components/
│   ├── ui/                # Primitives (Button, Input, Modal)
│   ├── features/          # Feature-specific (UserCard, PostList)
│   └── layouts/           # Layout components (MainLayout, AuthLayout)
├── lib/
│   ├── api/               # API client, fetchers
│   ├── stores/            # Global stores (createStore)
│   ├── signals/           # Shared signals
│   └── utils/             # Pure utility functions
├── hooks/                 # Custom reactive primitives
├── types/                 # TypeScript types/interfaces
├── styles/                # Global styles, Tailwind config
└── entry-server.tsx       # Server entry (SolidStart)
└── entry-client.tsx       # Client entry (SolidStart)
```

## Reactivity Fundamentals

### Signals (Atomic State)

```typescript
import { createSignal, createEffect, createMemo } from 'solid-js';

// ✅ CORRECT: Simple, atomic state
const [count, setCount] = createSignal(0);
const [user, setUser] = createSignal<User | null>(null);

// ✅ Derived state with createMemo (NOT createEffect!)
const doubleCount = createMemo(() => count() * 2);
const isLoggedIn = createMemo(() => user() !== null);

// ✅ Effects for side effects ONLY
createEffect(() => {
  console.log('Count changed:', count());
  // Side effect: localStorage, analytics, DOM manipulation
});

// ❌ WRONG: Don't derive state in effects
createEffect(() => {
  setDoubleCount(count() * 2); // Anti-pattern!
});
```

### Stores (Complex State)

```typescript
import { createStore, produce, reconcile } from 'solid-js/store';

interface AppState {
  user: User | null;
  todos: Todo[];
  settings: Settings;
}

const [state, setState] = createStore<AppState>({
  user: null,
  todos: [],
  settings: { theme: 'dark', lang: 'id' },
});

// ✅ Fine-grained updates with produce (Immer-like)
const addTodo = (todo: Todo) => {
  setState(produce((s) => {
    s.todos.push(todo);
  }));
};

// ✅ Path-based updates (more performant)
const updateTodo = (id: string, text: string) => {
  setState('todos', (t) => t.id === id, 'text', text);
};

// ✅ Replace entire array with reconcile (smart diffing)
const setTodos = (newTodos: Todo[]) => {
  setState('todos', reconcile(newTodos));
};

// ✅ Nested path updates
setState('settings', 'theme', 'light');
```

### Resources (Async Data)

```typescript
import { createResource, Suspense, ErrorBoundary } from 'solid-js';

// ✅ Basic resource
const [user] = createResource(() => fetchUser(userId()));

// ✅ With source signal (refetches on change)
const [userId, setUserId] = createSignal('1');
const [user, { mutate, refetch }] = createResource(userId, fetchUser);

// ✅ Resource with initial value (SSR-friendly)
const [posts] = createResource(
  () => fetchPosts(),
  { initialValue: [] }
);

// ✅ Usage in components
function UserProfile() {
  return (
    <ErrorBoundary fallback={(err) => <ErrorDisplay error={err} />}>
      <Suspense fallback={<Skeleton />}>
        <Show when={user()} fallback={<NotFound />}>
          {(u) => <UserCard user={u()} />}
        </Show>
      </Suspense>
    </ErrorBoundary>
  );
}
```

## TanStack Integration

### TanStack Query (Server State)

```typescript
// lib/query.ts
import { QueryClient, QueryClientProvider } from '@tanstack/solid-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 10 * 60 * 1000,
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

// hooks/useUsers.ts
import { createQuery, createMutation, useQueryClient } from '@tanstack/solid-query';

export function useUsers() {
  return createQuery(() => ({
    queryKey: ['users'],
    queryFn: () => api.getUsers(),
  }));
}

export function useUser(id: Accessor<string>) {
  return createQuery(() => ({
    queryKey: ['users', id()],
    queryFn: () => api.getUser(id()),
    enabled: !!id(),
  }));
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  return createMutation(() => ({
    mutationFn: (data: CreateUserDTO) => api.createUser(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
    onError: (error) => toast.error(error.message),
  }));
}

// ✅ Optimistic updates
export function useUpdateUser() {
  const queryClient = useQueryClient();
  return createMutation(() => ({
    mutationFn: ({ id, data }: { id: string; data: UpdateUserDTO }) =>
      api.updateUser(id, data),
    onMutate: async ({ id, data }) => {
      await queryClient.cancelQueries({ queryKey: ['users', id] });
      const previous = queryClient.getQueryData(['users', id]);
      queryClient.setQueryData(['users', id], (old: User) => ({ ...old, ...data }));
      return { previous };
    },
    onError: (_err, { id }, context) => {
      queryClient.setQueryData(['users', id], context?.previous);
    },
    onSettled: (_, __, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['users', id] });
    },
  }));
}
```

### TanStack Table

```typescript
import {
  createSolidTable, getCoreRowModel, getSortedRowModel,
  getFilteredRowModel, getPaginationRowModel, flexRender,
} from '@tanstack/solid-table';

function UsersTable() {
  const [sorting, setSorting] = createSignal<SortingState>([]);
  const [globalFilter, setGlobalFilter] = createSignal('');

  const table = createSolidTable({
    get data() { return users() ?? []; },
    columns,
    state: {
      get sorting() { return sorting(); },
      get globalFilter() { return globalFilter(); },
    },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <table>
      <thead>
        <For each={table.getHeaderGroups()}>
          {(headerGroup) => (
            <tr>
              <For each={headerGroup.headers}>
                {(header) => (
                  <th onClick={header.column.getToggleSortingHandler()}>
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                )}
              </For>
            </tr>
          )}
        </For>
      </thead>
      <tbody>
        <For each={table.getRowModel().rows}>
          {(row) => (
            <tr>
              <For each={row.getVisibleCells()}>
                {(cell) => <td>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>}
              </For>
            </tr>
          )}
        </For>
      </tbody>
    </table>
  );
}
```

### TanStack Form

```typescript
import { createForm } from '@tanstack/solid-form';
import { zodValidator } from '@tanstack/zod-form-adapter';
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

function UserForm() {
  const form = createForm(() => ({
    defaultValues: { name: '', email: '' },
    onSubmit: async ({ value }) => await api.createUser(value),
    validatorAdapter: zodValidator(),
    validators: { onChange: userSchema },
  }));

  return (
    <form onSubmit={(e) => { e.preventDefault(); form.handleSubmit(); }}>
      <form.Field name="name">
        {(field) => (
          <div>
            <input
              value={field().state.value}
              onInput={(e) => field().handleChange(e.currentTarget.value)}
            />
            <Show when={field().state.meta.errors.length}>
              <span class="error">{field().state.meta.errors.join(', ')}</span>
            </Show>
          </div>
        )}
      </form.Field>
      <form.Subscribe selector={(s) => [s.canSubmit, s.isSubmitting]}>
        {([canSubmit, isSubmitting]) => (
          <button disabled={!canSubmit() || isSubmitting()}>
            {isSubmitting() ? 'Saving...' : 'Save'}
          </button>
        )}
      </form.Subscribe>
    </form>
  );
}
```

## SolidStart Features

### File-Based Routing

```typescript
// routes/users/[id].tsx
import { useParams } from '@solidjs/router';
import { createAsync, cache } from '@solidjs/router';

const getUser = cache(async (id: string) => {
  'use server';
  return db.user.findUnique({ where: { id } });
}, 'user');

export const route = {
  preload: ({ params }) => getUser(params.id),
};

export default function UserPage() {
  const params = useParams<{ id: string }>();
  const user = createAsync(() => getUser(params.id));

  return (
    <Show when={user()} fallback={<Loading />}>
      {(u) => <UserProfile user={u()} />}
    </Show>
  );
}
```

### API Routes

```typescript
// routes/api/users.ts
import { json } from '@solidjs/router';
import type { APIEvent } from '@solidjs/start/server';

export async function GET(event: APIEvent) {
  const users = await db.user.findMany();
  return json(users);
}

export async function POST(event: APIEvent) {
  const body = await event.request.json();
  const parsed = userSchema.safeParse(body);
  if (!parsed.success) {
    return json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const user = await db.user.create({ data: parsed.data });
  return json(user, { status: 201 });
}
```

### Server Actions

```typescript
import { action, redirect } from '@solidjs/router';

export const createUserAction = action(async (formData: FormData) => {
  'use server';
  const data = {
    name: formData.get('name') as string,
    email: formData.get('email') as string,
  };
  const parsed = userSchema.safeParse(data);
  if (!parsed.success) return { error: parsed.error.flatten() };
  await db.user.create({ data: parsed.data });
  throw redirect('/users');
});
```

## Error Handling

```typescript
import { ErrorBoundary } from 'solid-js';

function AppErrorBoundary(props: ParentProps) {
  return (
    <ErrorBoundary
      fallback={(err, reset) => (
        <div class="error">
          <h2>Something went wrong</h2>
          <pre>{err.message}</pre>
          <button onClick={reset}>Try again</button>
        </div>
      )}
    >
      {props.children}
    </ErrorBoundary>
  );
}

// Type-Safe Result Pattern
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

async function fetchUser(id: string): Promise<Result<User, ApiError>> {
  try {
    const user = await api.get(`/users/${id}`);
    return { ok: true, value: user };
  } catch (e) {
    return { ok: false, error: e as ApiError };
  }
}
```

## Performance Optimization

### Lazy Loading

```typescript
import { lazy, Suspense } from 'solid-js';

const Dashboard = lazy(() => import('./routes/Dashboard'));
const Settings = lazy(() => import('./routes/Settings'));
```

### Avoiding Re-renders

```typescript
// ❌ Creates new object every render
<UserCard user={{ name: name(), email: email() }} />

// ✅ Pass signals directly
<UserCard name={name} email={email} />

// Use <Index> when items don't change, only values
<Index each={items()}>{(item, index) => <Item item={item()} />}</Index>

// Use <For> when items can be reordered
<For each={items()}>{(item) => <Item item={item} />}</For>
```

## Common Pitfalls

### Reactivity Loss

```typescript
// ❌ Destructuring loses reactivity
const { name, email } = props; // BROKEN!

// ✅ Access props directly
<span>{props.name}</span>

// ✅ Or use splitProps
const [local, others] = splitProps(props, ['name', 'email']);
```

### Memory Leaks

```typescript
// ❌ Not cleaning up subscriptions
createEffect(() => {
  const ws = new WebSocket(url);
  ws.onmessage = handleMessage;
});

// ✅ Proper cleanup
createEffect(() => {
  const ws = new WebSocket(url);
  ws.onmessage = handleMessage;
  onCleanup(() => ws.close());
});
```

### SSR Hydration

```typescript
// ❌ Client-only code runs on server
const windowWidth = window.innerWidth; // Error!

// ✅ Use isServer check
import { isServer } from 'solid-js/web';
const [width, setWidth] = createSignal(isServer ? 1024 : window.innerWidth);
onMount(() => setWidth(window.innerWidth));
```

## Recommended Libraries

| Category | Library | Why |
|----------|---------|-----|
| Forms | @tanstack/solid-form | Type-safe forms |
| Data | @tanstack/solid-query | Server state caching |
| Router | @solidjs/router | Official, SSR-ready |
| UI | Kobalte | Accessible primitives |
| Animation | solid-motionone | Performant |
| Validation | Zod | Type-safe schemas |
| Icons | unplugin-icons | Tree-shakeable |
| HTTP | ky | Modern fetch |

## Additional References

- `references/patterns.md` - Advanced design patterns & anti-patterns
- `references/debugging.md` - Debugging techniques & DevTools
- `references/performance.md` - Bundle optimization & profiling
- `references/security.md` - Security best practices & auth patterns
- `references/testing.md` - Comprehensive testing strategies

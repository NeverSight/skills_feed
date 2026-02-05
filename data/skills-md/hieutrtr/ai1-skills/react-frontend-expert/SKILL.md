---
name: react-frontend-expert
description: >-
  React/TypeScript frontend implementation patterns. Use during the implementation phase
  when creating or modifying React components, custom hooks, pages, data fetching logic
  with TanStack Query, forms, or routing. Covers component structure, hooks rules, custom
  hook design (useAuth, useDebounce, usePagination), TypeScript strict-mode conventions,
  form handling, accessibility requirements, and project structure. Does NOT cover testing
  (use react-testing-patterns), E2E testing (use e2e-testing), or deployment.
license: MIT
compatibility: 'React 18+, TypeScript 5+, TanStack Query 5+, Vite 5+, React Router 6+'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: implementation
allowed-tools: Read Edit Write Bash(npm:*) Bash(npx:*)
context: fork
---

# React Frontend Expert

## When to Use

Activate this skill when:
- Creating or modifying React components (functional components only)
- Writing custom hooks (`useXxx`)
- Building pages with routing
- Implementing data fetching with TanStack Query
- Handling forms with validation
- Setting up project structure for a React/TypeScript application

Do NOT use this skill for:
- Writing component or hook tests (use `react-testing-patterns`)
- E2E browser testing (use `e2e-testing`)
- API contract design (use `api-design-patterns`)
- Backend implementation (use `python-backend-expert`)
- Deployment or CI/CD (use `deployment-pipeline`)

## Instructions

### Project Structure

```
src/
├── api/                  # API client functions and query options
│   ├── client.ts         # Axios/fetch instance with interceptors
│   ├── users.ts          # User API functions + query options
│   └── posts.ts
├── components/           # Shared, reusable UI components
│   ├── Button.tsx
│   ├── Modal.tsx
│   ├── Table/
│   │   ├── Table.tsx
│   │   └── TablePagination.tsx
│   └── Form/
│       ├── Input.tsx
│       └── Select.tsx
├── features/             # Domain-specific feature components
│   ├── users/
│   │   ├── UserList.tsx
│   │   └── UserProfile.tsx
│   └── posts/
│       └── PostEditor.tsx
├── hooks/                # Custom hooks
│   ├── useAuth.ts
│   ├── useDebounce.ts
│   └── usePagination.ts
├── layouts/              # Layout components
│   ├── MainLayout.tsx
│   └── AuthLayout.tsx
├── pages/                # Route-level page components
│   ├── HomePage.tsx
│   ├── LoginPage.tsx
│   └── users/
│       ├── UserListPage.tsx
│       └── UserDetailPage.tsx
├── types/                # Shared TypeScript types
│   ├── api.ts            # API response types
│   └── user.ts
├── App.tsx               # Root component with providers and router
└── main.tsx              # Entry point
```

### Component Structure

#### Functional Components Only

```tsx
interface UserCardProps {
  user: User;
  onEdit: (userId: number) => void;
  showEmail?: boolean;
}

export function UserCard({ user, onEdit, showEmail = false }: UserCardProps) {
  return (
    <article className="user-card">
      <h3>{user.displayName}</h3>
      {showEmail && <p>{user.email}</p>}
      <button type="button" onClick={() => onEdit(user.id)}>
        Edit
      </button>
    </article>
  );
}
```

**Component rules:**
- Named exports for shared components: `export function Button`
- Default exports for page components: `export default function UserListPage`
- Props interface named `{Component}Props`
- Destructure props in function signature
- Keep components under 200 lines — extract sub-components or hooks when larger
- Use `children` and composition over deep prop drilling
- Never use `React.FC` — use plain function syntax

#### Component File Organization

For complex components, co-locate related files:

```
UserProfile/
├── UserProfile.tsx       # Main component
├── UserProfile.css       # Styles (or .module.css)
├── UserAvatar.tsx        # Sub-component
└── index.ts              # Re-export: export { UserProfile } from './UserProfile'
```

### Hooks Rules and Custom Hooks

#### Rules of Hooks
1. Only call hooks at the top level — never inside loops, conditions, or nested functions
2. Only call hooks from React function components or custom hooks
3. Custom hooks must start with `use`

#### Custom Hook Patterns

**useDebounce:**
```tsx
export function useDebounce<T>(value: T, delayMs: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debouncedValue;
}
```

**useAuth:**
```tsx
interface AuthContext {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContext | null>(null);

export function useAuth(): AuthContext {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
```

**usePagination:**
```tsx
interface PaginationState {
  cursor: string | null;
  hasMore: boolean;
  goToNext: (nextCursor: string) => void;
  reset: () => void;
}

export function usePagination(): PaginationState {
  const [cursor, setCursor] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);

  return {
    cursor,
    hasMore,
    goToNext: (nextCursor: string) => {
      setCursor(nextCursor);
    },
    reset: () => {
      setCursor(null);
      setHasMore(true);
    },
  };
}
```

**When to extract a custom hook:**
- Logic is reused across 2+ components
- Component has complex state management (>3 `useState` calls)
- Side effects need encapsulation (subscriptions, timers)
- Data fetching logic can be shared

### Data Fetching with TanStack Query

#### Query Options Factory (Recommended)

Centralize query key and function definitions to prevent key collisions:

```tsx
// api/users.ts
import { queryOptions } from "@tanstack/react-query";

export const userQueries = {
  all: () =>
    queryOptions({
      queryKey: ["users"],
      queryFn: () => apiClient.get<UserListResponse>("/users"),
    }),

  detail: (userId: number) =>
    queryOptions({
      queryKey: ["users", userId],
      queryFn: () => apiClient.get<UserResponse>(`/users/${userId}`),
    }),

  search: (query: string) =>
    queryOptions({
      queryKey: ["users", "search", query],
      queryFn: () => apiClient.get<UserListResponse>(`/users?q=${query}`),
      enabled: query.length > 0,
    }),
};
```

#### Using Queries in Components

```tsx
export function UserDetailPage({ userId }: { userId: number }) {
  const { data: user, isPending, isError, error } = useQuery(
    userQueries.detail(userId)
  );

  if (isPending) return <Spinner />;
  if (isError) return <ErrorMessage error={error} />;

  return <UserProfile user={user} />;
}
```

#### Mutations with Cache Invalidation

```tsx
export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UserCreate) =>
      apiClient.post<UserResponse>("/users", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}
```

**TanStack Query rules:**
- Set `staleTime` > 0 (default 0 is too aggressive): `staleTime: 5 * 60 * 1000` (5 min)
- Use `invalidateQueries()` after mutations — never manual `refetch()`
- Handle all states: `isPending`, `isError`, `data`
- Use `queryOptions()` factory — prevents key typos and duplication
- Use `enabled` to prevent queries from running with incomplete parameters

### TypeScript Conventions

```tsx
// Use `interface` for object shapes (components props, API responses)
interface User {
  id: number;
  email: string;
  displayName: string;
  role: "admin" | "editor" | "member";
}

// Use `type` for unions, intersections, and computed types
type UserRole = User["role"];
type CreateOrUpdate = UserCreate | UserUpdate;

// Discriminated unions for state machines
type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };
```

**TypeScript rules:**
- Enable `strict: true` in `tsconfig.json` — no exceptions
- Never use `any` — use `unknown` for truly unknown types
- Use `as const` for literal object types
- Prefer `interface` for extensible types, `type` for everything else
- Use generics for reusable utility types and hooks
- Export types from `types/` directory for shared use

### Form Handling

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const userSchema = z.object({
  email: z.string().email("Invalid email"),
  displayName: z.string().min(1, "Required").max(100),
  role: z.enum(["admin", "editor", "member"]),
});

type UserFormData = z.infer<typeof userSchema>;

export function UserForm({ onSubmit }: { onSubmit: (data: UserFormData) => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <label htmlFor="email">Email</label>
      <input id="email" type="email" {...register("email")} aria-invalid={!!errors.email} />
      {errors.email && <span role="alert">{errors.email.message}</span>}

      <label htmlFor="displayName">Name</label>
      <input id="displayName" {...register("displayName")} aria-invalid={!!errors.displayName} />
      {errors.displayName && <span role="alert">{errors.displayName.message}</span>}

      <button type="submit" disabled={isSubmitting}>Save</button>
    </form>
  );
}
```

### Accessibility Requirements

Every component must meet WCAG 2.1 AA:

1. **Semantic HTML first:** Use `<button>`, `<nav>`, `<main>`, `<article>` — not `<div onClick>`
2. **Labels:** Every form input has a `<label>` with matching `htmlFor`/`id`
3. **ARIA only when needed:** `aria-label` for icon-only buttons, `aria-live` for dynamic updates, `role="alert"` for errors
4. **Keyboard navigation:** All interactive elements reachable via Tab, activatable via Enter/Space
5. **Focus management:** Set focus to main content on route change, trap focus in modals
6. **Color contrast:** Minimum 4.5:1 for normal text, 3:1 for large text
7. **Alt text:** All `<img>` tags have descriptive `alt` (or `alt=""` for decorative images)

## Examples

### User List Page with Search and Pagination

```tsx
export default function UserListPage() {
  const [search, setSearch] = useState("");
  const debouncedSearch = useDebounce(search, 300);
  const pagination = usePagination();

  const { data, isPending } = useQuery(
    userQueries.list({ q: debouncedSearch, cursor: pagination.cursor })
  );

  return (
    <main>
      <h1>Users</h1>
      <input
        type="search"
        value={search}
        onChange={(e) => { setSearch(e.target.value); pagination.reset(); }}
        placeholder="Search users..."
        aria-label="Search users"
      />
      {isPending ? <Spinner /> : (
        <>
          <UserTable users={data.items} />
          {data.hasMore && (
            <button onClick={() => pagination.goToNext(data.nextCursor)}>
              Load more
            </button>
          )}
        </>
      )}
    </main>
  );
}
```

## Edge Cases

- **Stale closures in hooks:** When using callbacks that reference state, use `useRef` for mutable values that change frequently, or include dependencies in useCallback/useEffect arrays.

- **TanStack Query key collisions:** Structure keys hierarchically: `["users"]` for list, `["users", id]` for detail, `["users", { q, page }]` for filtered list. Use `queryOptions()` factory to centralize key definitions.

- **Infinite re-renders:** Common causes: missing dependency arrays, creating new objects/arrays in render (wrap in `useMemo`), state updates in useEffect without proper conditions.

- **Hydration mismatches:** Avoid rendering content that depends on browser-only APIs (window, localStorage) during initial render. Use `useEffect` or check `typeof window !== "undefined"`.

- **Memory leaks:** Cancel async operations in useEffect cleanup. TanStack Query handles this automatically for queries.

See `references/component-templates.md` for annotated component templates.
See `references/tanstack-query-patterns.md` for CRUD query patterns.

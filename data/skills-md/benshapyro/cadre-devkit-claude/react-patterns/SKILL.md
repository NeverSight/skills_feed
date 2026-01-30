---
name: react-patterns
description: Modern React patterns for TypeScript applications including hooks, state management, and component composition. Use when building React components, managing state, or implementing React best practices.
---

# React Patterns Skill

Modern React patterns for TypeScript applications.

## Component Structure

### File Organization
```
components/
├── ui/                    # Reusable primitives (Button, Input, Card)
├── features/              # Feature-specific components
│   └── auth/
│       ├── LoginForm.tsx
│       └── SignupForm.tsx
├── layouts/               # Page layouts
└── providers/             # Context providers
```

### Component Template
```tsx
interface ComponentNameProps {
  // Required props first
  title: string;
  onAction: () => void;
  // Optional props with defaults
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  children?: React.ReactNode;
}

export function ComponentName({
  title,
  onAction,
  variant = 'primary',
  disabled = false,
  children,
}: ComponentNameProps) {
  return (/* JSX */);
}
```

## Hooks Best Practices

### useState
```tsx
// Prefer explicit types for complex state
const [user, setUser] = useState<User | null>(null);

// Use functional updates when depending on previous state
setCount(prev => prev + 1);

// Group related state or use useReducer for complex state
const [form, setForm] = useState({ name: '', email: '' });
```

### useEffect
```tsx
// Always specify dependencies explicitly
useEffect(() => {
  fetchData();
}, [userId]); // Only re-run when userId changes

// Cleanup subscriptions
useEffect(() => {
  const subscription = subscribe();
  return () => subscription.unsubscribe();
}, []);

// Avoid objects/arrays in deps - extract primitives
const { id } = user;
useEffect(() => { /* ... */ }, [id]); // Not [user]
```

### useMemo / useCallback
```tsx
// Memoize expensive calculations
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// Memoize callbacks passed to children
const handleClick = useCallback(() => {
  onAction(id);
}, [onAction, id]);
```

### Custom Hooks
```tsx
// Extract reusable logic into custom hooks
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Prefix with "use", return typed values
function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // ... logic

  return { user, loading, signIn, signOut } as const;
}
```

## State Management

### Context + useReducer (Complex Local State)
```tsx
// Define action types and state
type State = { count: number; loading: boolean };
type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'setLoading'; payload: boolean };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { ...state, count: state.count + 1 };
    case 'decrement': return { ...state, count: state.count - 1 };
    case 'setLoading': return { ...state, loading: action.payload };
  }
}

// Context provider
const CounterContext = createContext<{
  state: State;
  dispatch: React.Dispatch<Action>;
} | null>(null);

function CounterProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, { count: 0, loading: false });
  return (
    <CounterContext.Provider value={{ state, dispatch }}>
      {children}
    </CounterContext.Provider>
  );
}

// Custom hook for consuming
function useCounter() {
  const context = useContext(CounterContext);
  if (!context) throw new Error('useCounter must be used within CounterProvider');
  return context;
}
```

### Server State (React Query / TanStack Query)
```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetching data
function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(res => res.json()),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// Mutations with optimistic updates
function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (user: User) =>
      fetch(`/api/users/${user.id}`, {
        method: 'PUT',
        body: JSON.stringify(user),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}

// Usage
function UserList() {
  const { data: users, isLoading, error } = useUsers();
  const updateUser = useUpdateUser();

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return (/* render users */);
}
```

### When to Use What
| Scenario | Solution |
|----------|----------|
| Simple component state | `useState` |
| Complex state with many actions | `useReducer` |
| State shared across components | Context + `useReducer` |
| Server data (fetch, cache, sync) | React Query / SWR |
| Global app state (auth, theme) | Context or Zustand |

## Component Patterns

### Composition over Props
```tsx
// Prefer composition
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>

// Over prop drilling
<Card header="Title" body="Content" />
```

### Render Props / Children as Function
```tsx
interface DataFetcherProps<T> {
  url: string;
  children: (data: T, loading: boolean) => React.ReactNode;
}

function DataFetcher<T>({ url, children }: DataFetcherProps<T>) {
  const { data, loading } = useFetch<T>(url);
  return <>{children(data, loading)}</>;
}
```

### Controlled vs Uncontrolled
```tsx
// Controlled - parent owns state
<Input value={value} onChange={setValue} />

// Uncontrolled - component owns state, use ref to access
<Input defaultValue="initial" ref={inputRef} />
```

## Error Handling

### Error Boundaries
```tsx
class ErrorBoundary extends Component<Props, State> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('Error caught:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <div>Something went wrong</div>;
    }
    return this.props.children;
  }
}
```

### Async Error Handling
```tsx
const [error, setError] = useState<Error | null>(null);

async function handleSubmit() {
  try {
    setError(null);
    await submitForm(data);
  } catch (e) {
    setError(e instanceof Error ? e : new Error('Unknown error'));
  }
}
```

## Performance

### Avoid Unnecessary Renders
- Use `React.memo()` for pure components receiving complex props
- Split context providers to minimize re-renders
- Use `useMemo` for expensive derived state
- Lazy load heavy components with `React.lazy()`

### Code Splitting
```tsx
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

## TypeScript Integration

### Event Handlers
```tsx
function handleChange(e: React.ChangeEvent<HTMLInputElement>) { }
function handleSubmit(e: React.FormEvent<HTMLFormElement>) { }
function handleClick(e: React.MouseEvent<HTMLButtonElement>) { }
```

### Generic Components
```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}
```

## Anti-Patterns

- Don't mutate state directly
- Don't call hooks conditionally or in loops
- Don't use array index as key for dynamic lists
- Don't fetch data in useEffect without cleanup/cancellation
- Don't ignore dependency array warnings
- Don't overuse context for frequently-changing values

---

## Version
- v1.0.0 (2025-12-05): Added YAML frontmatter, initial documented version

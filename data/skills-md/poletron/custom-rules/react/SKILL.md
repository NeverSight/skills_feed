---
name: react
description: >
  React 18+ patterns with hooks, components, and state management.
  Trigger: When building React applications with hooks and components.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with react"

## When to Use

Use this skill when:
- Building React 18+ applications
- Using hooks (useState, useEffect, custom hooks)
- Managing component state and props
- Implementing performance optimizations

---

## Critical Patterns

### Custom Hooks (REQUIRED)

```typescript
// ✅ ALWAYS: Extract reusable logic into custom hooks
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);
  
  return { user, loading };
}

// ❌ NEVER: Duplicate logic across components
```

### Component Composition (REQUIRED)

```typescript
// ✅ ALWAYS: Prefer composition over prop drilling
function Dashboard({ children }: { children: React.ReactNode }) {
  return <div className="dashboard">{children}</div>;
}

// Usage
<Dashboard>
  <Sidebar />
  <MainContent />
</Dashboard>
```

### Memoization (WHEN NEEDED)

```typescript
// ✅ Use useMemo for expensive calculations
const sortedItems = useMemo(() => 
  items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// ✅ Use useCallback for stable function references
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);
```

---

## Decision Tree

```
Need shared state?         → Use Context or Zustand
Need server state?         → Use React Query / SWR
Need form handling?        → Use React Hook Form
Need expensive calc?       → Use useMemo
Need stable callback?      → Use useCallback
Need DOM access?           → Use useRef
```

---

## Code Examples

### Controlled Form

```typescript
function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login({ email, password });
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <input 
        type="password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)} 
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

### Error Boundary

```typescript
class ErrorBoundary extends React.Component<Props, State> {
  state = { hasError: false };
  
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}
```

---

## Commands

```bash
npx create-react-app myapp --template typescript
npm run dev
npm run build
npm run test
```

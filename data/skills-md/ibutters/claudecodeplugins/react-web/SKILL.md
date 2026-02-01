---
name: react-web
description: Modern React 19+ development with Server Components, Actions, hooks, TypeScript integration, and performance optimization. Use when building React web applications, implementing Server Components, using Actions for form handling, working with new hooks (use, useActionState, useOptimistic, useFormStatus), setting up React projects with Vite or Next.js, or optimizing React performance.
---

# React Web Development (React 19+)

Build modern, performant React applications using React 19+ features.

## Core Patterns

### Function Components with TypeScript

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({ variant = 'primary', children, onClick }: ButtonProps) {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {children}
    </button>
  );
}
```

### Server Components (Default in React 19)

Server Components render on the server, reducing client JavaScript:

```tsx
// app/posts/page.tsx - Server Component (default)
async function PostList() {
  const posts = await db.posts.findMany();
  return (
    <ul>
      {posts.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  );
}
```

### Client Components

Mark interactive components with 'use client':

```tsx
'use client';
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

## React 19 Features

### Actions & useActionState

Replace manual form handling with Actions:

```tsx
'use client';
import { useActionState } from 'react';

async function submitForm(prev: State, formData: FormData) {
  'use server';
  const name = formData.get('name');
  await db.users.create({ name });
  return { success: true };
}

function Form() {
  const [state, action, pending] = useActionState(submitForm, { success: false });
  return (
    <form action={action}>
      <input name="name" />
      <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>
    </form>
  );
}
```

### use() Hook for Promises & Context

```tsx
import { use } from 'react';

function UserProfile({ userPromise }) {
  const user = use(userPromise); // Suspends until resolved
  return <div>{user.name}</div>;
}

function ThemeButton() {
  const theme = use(ThemeContext); // Read context conditionally
  return <button style={{ color: theme.primary }}>Click</button>;
}
```

### useOptimistic for Instant UI Updates

```tsx
'use client';
import { useOptimistic } from 'react';

function TodoList({ todos, addTodo }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, { ...newTodo, pending: true }]
  );
  
  async function handleAdd(formData: FormData) {
    const text = formData.get('text');
    addOptimisticTodo({ text, id: Date.now() });
    await addTodo(text);
  }
  
  return (
    <form action={handleAdd}>
      <input name="text" />
      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
            {todo.text}
          </li>
        ))}
      </ul>
    </form>
  );
}
```

### useFormStatus for Form State

```tsx
'use client';
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Submitting...' : 'Submit'}</button>;
}
```

## Project Structure

```
src/
├── app/                  # App Router (Next.js) or routes
├── components/
│   ├── ui/              # Reusable UI primitives
│   ├── features/        # Feature-specific components
│   └── layouts/         # Layout components
├── hooks/               # Custom hooks
├── lib/                 # Utilities, API clients
├── types/               # TypeScript types
└── styles/              # Global styles, tokens
```

## Custom Hooks Pattern

```tsx
function useAsync<T>(asyncFn: () => Promise<T>, deps: unknown[]) {
  const [state, setState] = useState<{
    data: T | null;
    loading: boolean;
    error: Error | null;
  }>({ data: null, loading: true, error: null });

  useEffect(() => {
    setState(s => ({ ...s, loading: true }));
    asyncFn()
      .then(data => setState({ data, loading: false, error: null }))
      .catch(error => setState({ data: null, loading: false, error }));
  }, deps);

  return state;
}
```

## Performance Guidelines

1. **Let React Compiler optimize** - React 19's compiler auto-memoizes; avoid manual useMemo/useCallback unless profiling shows need
2. **Use Server Components** - Default to server rendering, add 'use client' only for interactivity
3. **Lazy load routes** - Use `React.lazy()` and Suspense for code splitting
4. **Avoid prop drilling** - Use Context or composition patterns

## Related Skills

- **Atomic Design**: Component hierarchy patterns → See `references/atomic-integration.md`
- **CSS Tokens**: Styling with design tokens → See `references/styling-patterns.md`
- **Storybook**: Component documentation → See `references/storybook-setup.md`

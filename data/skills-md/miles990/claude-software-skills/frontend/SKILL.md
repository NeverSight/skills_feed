---
name: frontend
description: Modern frontend development with React, Vue, and web technologies
domain: development-stacks
version: 1.1.0
tags: [react, vue, nextjs, typescript, css, state-management, bundlers]
triggers:
  keywords:
    primary: [frontend, react, vue, nextjs, ui, web, component]
    secondary: [css, tailwind, state, hooks, spa, pwa, vite]
  context_boost: [typescript, javascript, html, browser, client]
  context_penalty: [backend, server, database, api]
  priority: high
collaboration:
  prerequisites:
    - skill: typescript
      reason: Type-safe component development
  delegation_triggers:
    - trigger: API integration or backend communication
      delegate_to: backend
      context: API endpoints, authentication flow
    - trigger: API response format questions
      delegate_to: api-design
      context: Expected data structures, error handling
    - trigger: Component or integration testing
      delegate_to: testing-strategies
      context: Testing library patterns, mocking APIs
  receives_context_from:
    - skill: backend
      receives:
        - API endpoints list
        - Authentication flow
        - WebSocket events
    - skill: api-design
      receives:
        - API documentation
        - Error response formats
        - Pagination patterns
  provides_context_to:
    - skill: testing-strategies
      provides:
        - Component structure
        - User interaction patterns
        - State management approach
    - skill: backend
      provides:
        - Required API endpoints
        - Expected response formats
---

# Frontend Development

## Overview

Modern frontend development patterns, frameworks, and best practices for building performant web applications.

---

## React Ecosystem

### Component Patterns

```tsx
// Functional component with hooks
import { useState, useEffect, useCallback, useMemo } from 'react';

interface UserListProps {
  initialFilter?: string;
  onSelect: (user: User) => void;
}

function UserList({ initialFilter = '', onSelect }: UserListProps) {
  const [users, setUsers] = useState<User[]>([]);
  const [filter, setFilter] = useState(initialFilter);
  const [loading, setLoading] = useState(true);

  // Memoized filtered list
  const filteredUsers = useMemo(
    () => users.filter(u => u.name.toLowerCase().includes(filter.toLowerCase())),
    [users, filter]
  );

  // Stable callback reference
  const handleSelect = useCallback((user: User) => {
    onSelect(user);
  }, [onSelect]);

  useEffect(() => {
    async function fetchUsers() {
      setLoading(true);
      const data = await api.getUsers();
      setUsers(data);
      setLoading(false);
    }
    fetchUsers();
  }, []);

  if (loading) return <Skeleton count={5} />;

  return (
    <div>
      <SearchInput value={filter} onChange={setFilter} />
      {filteredUsers.map(user => (
        <UserCard
          key={user.id}
          user={user}
          onClick={() => handleSelect(user)}
        />
      ))}
    </div>
  );
}
```

### Custom Hooks

```tsx
// Data fetching hook
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url, { signal: controller.signal });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const json = await response.json();
        setData(json);
        setError(null);
      } catch (err) {
        if (err instanceof Error && err.name !== 'AbortError') {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    }

    fetchData();
    return () => controller.abort();
  }, [url]);

  return { data, error, loading };
}

// Local storage hook
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    const valueToStore = value instanceof Function ? value(storedValue) : value;
    setStoredValue(valueToStore);
    window.localStorage.setItem(key, JSON.stringify(valueToStore));
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
}

// Debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

### State Management

```tsx
// Zustand - simple global state
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  clearCart: () => void;
  total: () => number;
}

const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],
      addItem: (item) => set((state) => ({
        items: [...state.items, item]
      })),
      removeItem: (id) => set((state) => ({
        items: state.items.filter(i => i.id !== id)
      })),
      clearCart: () => set({ items: [] }),
      total: () => get().items.reduce((sum, item) => sum + item.price, 0)
    }),
    { name: 'cart-storage' }
  )
);

// React Query / TanStack Query
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => api.getUsers(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newUser: CreateUserInput) => api.createUser(newUser),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

---

## Next.js / App Router

### Server Components

```tsx
// app/users/page.tsx - Server Component (default)
async function UsersPage() {
  // Direct database access in server component
  const users = await db.user.findMany();

  return (
    <div>
      <h1>Users</h1>
      <UserList users={users} />
    </div>
  );
}

// Client component for interactivity
'use client';

import { useState } from 'react';

function UserList({ users }: { users: User[] }) {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <ul>
      {users.map(user => (
        <li
          key={user.id}
          onClick={() => setSelected(user.id)}
          className={selected === user.id ? 'selected' : ''}
        >
          {user.name}
        </li>
      ))}
    </ul>
  );
}
```

### Server Actions

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  await db.user.create({
    data: { name, email }
  });

  revalidatePath('/users');
  redirect('/users');
}

// Usage in component
function CreateUserForm() {
  return (
    <form action={createUser}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

### Route Handlers

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const limit = parseInt(searchParams.get('limit') || '10');

  const users = await db.user.findMany({ take: limit });
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

---

## CSS & Styling

### Tailwind CSS

```tsx
// Component with Tailwind
function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm
                    hover:shadow-md transition-shadow duration-200
                    dark:bg-gray-800 dark:border-gray-700">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        {title}
      </h2>
      <div className="text-gray-600 dark:text-gray-300">
        {children}
      </div>
    </div>
  );
}

// With clsx/cn for conditional classes
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

function Button({
  variant = 'primary',
  size = 'md',
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium',
        'focus:outline-none focus:ring-2 focus:ring-offset-2',
        {
          'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
          'bg-gray-200 text-gray-900 hover:bg-gray-300': variant === 'secondary',
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },
        className
      )}
      {...props}
    />
  );
}
```

### CSS Modules

```tsx
// Button.module.css
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
}

.primary {
  background-color: var(--color-primary);
  color: white;
}

.secondary {
  background-color: var(--color-gray-200);
  color: var(--color-gray-900);
}

// Button.tsx
import styles from './Button.module.css';

function Button({ variant = 'primary', children }) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}
```

---

## Performance Optimization

### Code Splitting

```tsx
// Dynamic imports
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Client-only component
});

// React.lazy with Suspense
const Dashboard = lazy(() => import('./Dashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Dashboard />
    </Suspense>
  );
}
```

### Virtualization

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} className="h-[400px] overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              transform: `translateY(${virtualItem.start}px)`,
              height: `${virtualItem.size}px`,
            }}
          >
            {items[virtualItem.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Image Optimization

```tsx
import Image from 'next/image';

function ProductImage({ src, alt }: { src: string; alt: string }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={400}
      height={300}
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,/9j/4AAQ..."
      sizes="(max-width: 768px) 100vw, 400px"
      priority={false}
    />
  );
}
```

---

## Testing

### Component Testing

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  it('submits with valid credentials', async () => {
    const onSubmit = vi.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'password123');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });

  it('shows validation errors', async () => {
    render(<LoginForm onSubmit={vi.fn()} />);

    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
  });
});
```

---

## Related Skills

- [[testing-strategies]] - Frontend testing
- [[performance-optimization]] - Web performance
- [[ux-principles]] - User experience

---

## Sharp Edges（常見陷阱）

> 這些是前端開發中最常見且代價最高的錯誤

### SE-1: useEffect 無限迴圈
- **嚴重度**: critical
- **情境**: useEffect 中更新 state，而該 state 又是 dependency，導致無限重新渲染
- **原因**: 不了解 React 的 dependency 機制、object/array 作為 dependency
- **症狀**:
  - 頁面卡死或極度緩慢
  - 瀏覽器記憶體持續增長
  - Network tab 顯示大量重複請求
- **檢測**: `useEffect.*setState.*\].*\{|useEffect\(\(\).*fetch.*\[\]`
- **解法**: 正確設定 dependencies、使用 useCallback/useMemo、考慮用 useRef 追蹤值

### SE-2: 記憶體洩漏 (Memory Leak)
- **嚴重度**: high
- **情境**: Component unmount 後仍有 subscription、timer 或 async 操作更新 state
- **原因**: 沒有清理 effect、沒有取消進行中的 fetch
- **症狀**:
  - Console 警告「Can't perform state update on unmounted component」
  - 應用程式越用越慢
  - 切換頁面後舊資料閃現
- **檢測**: `useEffect.*setInterval(?!.*return)|useEffect.*addEventListener(?!.*return.*remove)|useEffect.*subscribe(?!.*return)`
- **解法**: 在 useEffect 中 return cleanup function、使用 AbortController 取消 fetch

### SE-3: Props Drilling 地獄
- **嚴重度**: medium
- **情境**: 為了傳遞資料給深層 component，中間層需要傳遞不需要的 props
- **原因**: 沒有使用 Context 或狀態管理、component 結構設計不當
- **症狀**:
  - 修改一個 prop 需要改動 5+ 個 component
  - 中間層 component 有很多只是「傳遞」的 props
  - 難以追蹤資料流向
- **檢測**: `props\.\w+.*props\.\w+.*props\.\w+|{.*,.*,.*,.*,.*,.*}.*=>`
- **解法**: 使用 Context、Zustand/Redux、或 Component Composition

### SE-4: 過早優化 (Premature Optimization)
- **嚴重度**: medium
- **情境**: 在沒有效能問題時過度使用 useMemo/useCallback/React.memo
- **原因**: 誤解這些 hooks 的用途、盲目「優化」
- **症狀**:
  - 程式碼充滿 useMemo 但沒有效能改善
  - 反而因為額外的記憶體和比較操作變慢
  - 程式碼難以閱讀
- **檢測**: `useMemo\(\(\).*return.*\d+|useCallback\(\(\).*console|React\.memo\(.*\)(?!.*areEqual)`
- **解法**: 先測量效能、只在確定有問題時優化、理解何時使用這些工具

### SE-5: 不安全的 HTML 渲染
- **嚴重度**: critical
- **情境**: 使用 dangerouslySetInnerHTML 或直接渲染用戶輸入的 HTML
- **原因**: 為了渲染 rich text、不了解 XSS 風險
- **症狀**:
  - XSS 攻擊漏洞
  - 用戶可以注入惡意腳本
  - 網站被用於釣魚或竊取資料
- **檢測**: `dangerouslySetInnerHTML|innerHTML.*=.*user|v-html.*user`
- **解法**: 使用 DOMPurify 消毒、使用安全的 Markdown 渲染器、避免直接渲染用戶輸入

---

## Validations

### V-1: useEffect 缺少 cleanup
- **類型**: regex
- **嚴重度**: high
- **模式**: `useEffect\s*\([^)]*=>\s*\{[^}]*(setInterval|addEventListener|subscribe)[^}]*\}(?![^}]*return)`
- **訊息**: useEffect with subscription/timer missing cleanup function
- **修復建議**: Add cleanup: `return () => clearInterval(id)` or `return () => unsubscribe()`
- **適用**: `*.tsx`, `*.jsx`

### V-2: 禁止 dangerouslySetInnerHTML
- **類型**: regex
- **嚴重度**: critical
- **模式**: `dangerouslySetInnerHTML`
- **訊息**: dangerouslySetInnerHTML is a security risk (XSS)
- **修復建議**: Use DOMPurify: `dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(html) }}`
- **適用**: `*.tsx`, `*.jsx`

### V-3: useEffect 空 dependency array + state 更新
- **類型**: regex
- **嚴重度**: high
- **模式**: `useEffect\s*\([^)]*=>\s*\{[^}]*set\w+\([^}]*\},\s*\[\s*\]\s*\)`
- **訊息**: useEffect with empty deps but updates state - possible stale closure
- **修復建議**: Add necessary dependencies or use useRef for values that shouldn't trigger re-run
- **適用**: `*.tsx`, `*.jsx`

### V-4: 禁止 inline styles 物件字面量
- **類型**: regex
- **嚴重度**: medium
- **模式**: `style=\{\s*\{[^}]+\}\s*\}`
- **訊息**: Inline style object creates new reference on every render
- **修復建議**: Extract to variable or use useMemo: `const styles = useMemo(() => ({...}), [])`
- **適用**: `*.tsx`, `*.jsx`

### V-5: 禁止在 JSX 中使用 index 作為 key
- **類型**: regex
- **嚴重度**: medium
- **模式**: `key=\{(index|i|idx)\}`
- **訊息**: Using array index as key can cause issues with reordering
- **修復建議**: Use a unique identifier: `key={item.id}` or `key={item.uniqueField}`
- **適用**: `*.tsx`, `*.jsx`


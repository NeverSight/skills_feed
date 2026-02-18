---
name: state-management
description: Implement state management patterns for frontend applications. Use when managing global state, handling complex data flows, or coordinating state across components. Handles React Context, Redux, Zustand, Recoil, and state management best practices.
tags: [state-management, React, Redux, Context, Zustand, Recoil, global-state]
platforms: [Claude, ChatGPT, Gemini]
---

# State Management


## When to use this skill

- **전역 상태 필요**: 여러 컴포넌트가 같은 데이터 공유
- **Props Drilling 문제**: 5단계 이상 props 전달
- **복잡한 상태 로직**: 인증, 장바구니, 테마 등
- **상태 동기화**: 서버 데이터와 클라이언트 상태 동기화

## Instructions

### Step 1: 상태 범위 결정

로컬 vs 전역 상태를 구분합니다.

**판단 기준**:
- **로컬 상태**: 단일 컴포넌트에서만 사용
  - 폼 입력값, 토글 상태, 드롭다운 열림/닫힘
  - `useState`, `useReducer` 사용

- **전역 상태**: 여러 컴포넌트에서 공유
  - 사용자 인증, 장바구니, 테마, 언어 설정
  - Context API, Redux, Zustand 사용

**예시**:
```tsx
// ✅ 로컬 상태 (단일 컴포넌트)
function SearchBox() {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => setIsOpen(true)}
      />
      {isOpen && <SearchResults query={query} />}
    </div>
  );
}

// ✅ 전역 상태 (여러 컴포넌트)
// 사용자 인증 정보는 Header, Profile, Settings 등에서 사용
const { user, logout } = useAuth();  // Context 또는 Zustand
```

### Step 2: React Context API (간단한 전역 상태)

가벼운 전역 상태 관리에 적합합니다.

**예시** (인증 Context):
```tsx
// contexts/AuthContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    setUser(data.user);
    localStorage.setItem('token', data.token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{
      user,
      login,
      logout,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

**사용**:
```tsx
// App.tsx
function App() {
  return (
    <AuthProvider>
      <Router>
        <Header />
        <Routes />
      </Router>
    </AuthProvider>
  );
}

// Header.tsx
function Header() {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <header>
      {isAuthenticated ? (
        <>
          <span>Welcome, {user!.name}</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <Link to="/login">Login</Link>
      )}
    </header>
  );
}
```

### Step 3: Zustand (현대적이고 간결한 상태 관리)

Redux보다 간단하고 보일러플레이트가 적습니다.

**설치**:
```bash
npm install zustand
```

**예시** (장바구니):
```tsx
// stores/cartStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartStore {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  total: () => number;
}

export const useCartStore = create<CartStore>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],

        addItem: (item) => set((state) => {
          const existing = state.items.find(i => i.id === item.id);
          if (existing) {
            return {
              items: state.items.map(i =>
                i.id === item.id
                  ? { ...i, quantity: i.quantity + 1 }
                  : i
              )
            };
          }
          return { items: [...state.items, { ...item, quantity: 1 }] };
        }),

        removeItem: (id) => set((state) => ({
          items: state.items.filter(item => item.id !== id)
        })),

        updateQuantity: (id, quantity) => set((state) => ({
          items: state.items.map(item =>
            item.id === id ? { ...item, quantity } : item
          )
        })),

        clearCart: () => set({ items: [] }),

        total: () => {
          const { items } = get();
          return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
        }
      }),
      { name: 'cart-storage' }  // localStorage key
    )
  )
);
```

**사용**:
```tsx
// components/ProductCard.tsx
function ProductCard({ product }) {
  const addItem = useCartStore(state => state.addItem);

  return (
    <div>
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <button onClick={() => addItem(product)}>
        Add to Cart
      </button>
    </div>
  );
}

// components/Cart.tsx
function Cart() {
  const items = useCartStore(state => state.items);
  const total = useCartStore(state => state.total());
  const removeItem = useCartStore(state => state.removeItem);

  return (
    <div>
      <h2>Cart</h2>
      {items.map(item => (
        <div key={item.id}>
          <span>{item.name} x {item.quantity}</span>
          <span>${item.price * item.quantity}</span>
          <button onClick={() => removeItem(item.id)}>Remove</button>
        </div>
      ))}
      <p>Total: ${total.toFixed(2)}</p>
    </div>
  );
}
```

### Step 4: Redux Toolkit (대규모 앱)

복잡한 상태 로직과 미들웨어가 필요한 경우 사용합니다.

**설치**:
```bash
npm install @reduxjs/toolkit react-redux
```

**예시** (Todo):
```tsx
// store/todosSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

interface TodosState {
  items: Todo[];
  status: 'idle' | 'loading' | 'failed';
}

const initialState: TodosState = {
  items: [],
  status: 'idle'
};

// 비동기 액션
export const fetchTodos = createAsyncThunk('todos/fetch', async () => {
  const response = await fetch('/api/todos');
  return response.json();
});

const todosSlice = createSlice({
  name: 'todos',
  initialState,
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      state.items.push({
        id: Date.now().toString(),
        text: action.payload,
        completed: false
      });
    },
    toggleTodo: (state, action: PayloadAction<string>) => {
      const todo = state.items.find(t => t.id === action.payload);
      if (todo) {
        todo.completed = !todo.completed;
      }
    },
    removeTodo: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(t => t.id !== action.payload);
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTodos.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchTodos.fulfilled, (state, action) => {
        state.status = 'idle';
        state.items = action.payload;
      })
      .addCase(fetchTodos.rejected, (state) => {
        state.status = 'failed';
      });
  }
});

export const { addTodo, toggleTodo, removeTodo } = todosSlice.actions;
export default todosSlice.reducer;

// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import todosReducer from './todosSlice';

export const store = configureStore({
  reducer: {
    todos: todosReducer
  }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

**사용**:
```tsx
// App.tsx
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
  return (
    <Provider store={store}>
      <TodoApp />
    </Provider>
  );
}

// components/TodoList.tsx
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { toggleTodo, removeTodo } from '../store/todosSlice';

function TodoList() {
  const todos = useSelector((state: RootState) => state.todos.items);
  const dispatch = useDispatch();

  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => dispatch(toggleTodo(todo.id))}
          />
          <span style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}>
            {todo.text}
          </span>
          <button onClick={() => dispatch(removeTodo(todo.id))}>Delete</button>
        </li>
      ))}
    </ul>
  );
}
```

### Step 5: 서버 상태 관리 (React Query / TanStack Query)

API 데이터 fetching 및 캐싱에 특화되어 있습니다.

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: string }) {
  const queryClient = useQueryClient();

  // GET: 사용자 정보 조회
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: async () => {
      const res = await fetch(`/api/users/${userId}`);
      return res.json();
    },
    staleTime: 5 * 60 * 1000,  // 5분간 캐시
  });

  // POST: 사용자 정보 수정
  const mutation = useMutation({
    mutationFn: async (updatedUser: Partial<User>) => {
      const res = await fetch(`/api/users/${userId}`, {
        method: 'PATCH',
        body: JSON.stringify(updatedUser)
      });
      return res.json();
    },
    onSuccess: () => {
      // 캐시 무효화 및 재조회
      queryClient.invalidateQueries({ queryKey: ['user', userId] });
    }
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <button onClick={() => mutation.mutate({ name: 'New Name' })}>
        Update Name
      </button>
    </div>
  );
}
```

## Output format

### 상태 관리 도구 선택 가이드

```
상황별 추천 도구:

1. 간단한 전역 상태 (테마, 언어)
   → React Context API

2. 중간 복잡도 (장바구니, 사용자 설정)
   → Zustand

3. 대규모 앱, 복잡한 로직, 미들웨어 필요
   → Redux Toolkit

4. 서버 데이터 fetching/caching
   → React Query (TanStack Query)

5. 폼 상태
   → React Hook Form + Zod
```

## Constraints

### 필수 규칙 (MUST)

1. **상태 불변성**: 상태는 절대 직접 수정하지 않음
   ```tsx
   // ❌ 나쁜 예
   state.items.push(newItem);

   // ✅ 좋은 예
   setState({ items: [...state.items, newItem] });
   ```

2. **최소 상태 원칙**: 파생 가능한 값은 상태로 저장하지 않음
   ```tsx
   // ❌ 나쁜 예
   const [items, setItems] = useState([]);
   const [count, setCount] = useState(0);  // items.length로 계산 가능

   // ✅ 좋은 예
   const [items, setItems] = useState([]);
   const count = items.length;  // 파생 값
   ```

3. **단일 진실의 원천**: 같은 데이터를 여러 곳에 중복 저장 금지

### 금지 사항 (MUST NOT)

1. **Props Drilling 과다**: 5단계 이상 props 전달 금지
   - Context 또는 상태 관리 라이브러리 사용

2. **모든 것을 전역 상태로**: 로컬 상태로 충분한 경우 전역 상태 사용 지양

## Best practices

1. **선택적 구독**: 필요한 상태만 구독
   ```tsx
   // ✅ 좋은 예: 필요한 것만
   const items = useCartStore(state => state.items);

   // ❌ 나쁜 예: 전체 구독
   const { items, addItem, removeItem, updateQuantity, clearCart } = useCartStore();
   ```

2. **액션 이름 명확히**: `update` → `updateUserProfile`

3. **TypeScript 사용**: 타입 안정성 확보

## References

- [Zustand](https://zustand-demo.pmnd.rs/)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [React Query](https://tanstack.com/query/latest)
- [Jotai](https://jotai.org/)
- [Recoil](https://recoiljs.org/)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [ui-component-patterns](../ui-component-patterns/SKILL.md): 컴포넌트와 상태 통합
- [backend-testing](../../backend/backend-testing/SKILL.md): 상태 로직 테스트

### 태그
`#state-management` `#React` `#Redux` `#Zustand` `#Context` `#global-state` `#frontend`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->

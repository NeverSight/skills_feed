---
name: react-native-state
description: Master state management - Redux Toolkit, Zustand, TanStack Query, and data persistence
sasmp_version: "1.3.0"
bonded_agent: 03-react-native-state
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-01"
---

# React Native State Management Skill

> Learn production-ready state management including Redux Toolkit, Zustand, TanStack Query, and persistence with AsyncStorage/MMKV.

## Prerequisites

- React Native basics
- TypeScript fundamentals
- Understanding of React hooks

## Learning Objectives

After completing this skill, you will be able to:
- [ ] Set up Redux Toolkit with TypeScript
- [ ] Create Zustand stores with persistence
- [ ] Manage server state with TanStack Query
- [ ] Persist data with AsyncStorage/MMKV
- [ ] Choose the right solution for each use case

---

## Topics Covered

### 1. Redux Toolkit Setup
```typescript
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { authSlice } from './slices/authSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice.reducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 2. RTK Slice
```typescript
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
  user: User | null;
  token: string | null;
}

export const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null, token: null } as AuthState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
    },
  },
});
```

### 3. Zustand Store
```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AppStore {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useAppStore = create<AppStore>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

### 4. TanStack Query
```typescript
import { useQuery, useMutation } from '@tanstack/react-query';

export function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: () => api.getProducts(),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function useCreateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.createProduct,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}
```

### 5. When to Use What

| Solution | Use Case |
|----------|----------|
| useState/useReducer | Component-local state |
| Zustand | Simple global state, preferences |
| Redux Toolkit | Complex app state, large teams |
| TanStack Query | Server state, caching, sync |
| Context | Theme, auth status (low-frequency) |

---

## Quick Start Example

```typescript
// Zustand + TanStack Query combo
import { create } from 'zustand';
import { useQuery } from '@tanstack/react-query';

// UI state with Zustand
const useUIStore = create((set) => ({
  sidebarOpen: false,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}));

// Server state with TanStack Query
function ProductList() {
  const { data, isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
  });

  const sidebarOpen = useUIStore((s) => s.sidebarOpen);

  // Render with both states
}
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Non-serializable value" | Functions in Redux state | Use middleware ignore |
| State not persisting | Wrong storage config | Check persist config |
| Stale data | Missing invalidation | Add proper query keys |

---

## Validation Checklist

- [ ] State updates correctly
- [ ] Persistence works across restarts
- [ ] Server state syncs properly
- [ ] TypeScript types are correct

---

## Usage

```
Skill("react-native-state")
```

**Bonded Agent**: `03-react-native-state`

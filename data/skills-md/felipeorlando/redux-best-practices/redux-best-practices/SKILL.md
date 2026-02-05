---
name: redux-best-practices
description: Redux and React-Redux best practices, patterns, and anti-patterns based on the official Redux style guide. Use when writing, reviewing, or refactoring Redux code including store setup, slices, reducers, selectors, async logic, state normalization, or React-Redux hooks. Triggers on tasks involving createSlice, configureStore, useSelector, useDispatch, thunks, RTK Query, or state management architecture decisions.
---

# Redux Best Practices

## Essential Rules (Priority A)

These rules prevent errors. Violating them causes bugs.

### 1. Never Mutate State
```typescript
// ❌ WRONG - mutates state
state.todos.push(newTodo)
state.user.name = 'New Name'

// ✅ CORRECT - RTK with Immer handles this
const todosSlice = createSlice({
  reducers: {
    todoAdded: (state, action) => {
      state.push(action.payload) // Immer makes this safe
    }
  }
})
```

### 2. Reducers Must Be Pure
Forbidden in reducers:
- Async logic (AJAX, timeouts, promises)
- `Math.random()`, `Date.now()`
- External variable modifications

### 3. Keep State Serializable
Never store: Promises, Symbols, Maps/Sets, Functions, Class instances, DOM nodes

### 4. One Store Per App
```typescript
// store.ts - single source of truth
export const store = configureStore({
  reducer: { todos: todosReducer, users: usersReducer }
})
```

## Strongly Recommended (Priority B)

### Use Redux Toolkit
Always use RTK. It enables DevTools, catches mutations, uses Immer, reduces boilerplate.

```typescript
import { configureStore, createSlice, PayloadAction } from '@reduxjs/toolkit'

const todosSlice = createSlice({
  name: 'todos',
  initialState: [] as Todo[],
  reducers: {
    todoAdded: (state, action: PayloadAction<Todo>) => {
      state.push(action.payload)
    }
  }
})

export const { todoAdded } = todosSlice.actions
```

### Feature-Based Structure
```
src/
├── app/
│   ├── store.ts
│   └── hooks.ts (typed useSelector/useDispatch)
├── features/
│   ├── todos/
│   │   ├── todosSlice.ts
│   │   ├── todosSelectors.ts
│   │   └── TodoList.tsx
│   └── users/
│       ├── usersSlice.ts
│       └── ...
```

### Normalize Complex State
```typescript
// ❌ Nested - hard to update
{ posts: [{ id: 1, author: { id: 1, name: 'Alice' } }] }

// ✅ Normalized - easy to update
{
  posts: { byId: { '1': { id: '1', authorId: '1' } }, ids: ['1'] },
  users: { byId: { '1': { id: '1', name: 'Alice' } }, ids: ['1'] }
}
```

### Model Actions as Events
```typescript
// ❌ Setter actions
dispatch({ type: 'SET_PIZZA_COUNT', payload: 1 })
dispatch({ type: 'SET_COKE_COUNT', payload: 1 })

// ✅ Event actions
dispatch({ type: 'food/orderPlaced', payload: { pizza: 1, coke: 1 } })
```

### Treat Reducers as State Machines
```typescript
interface FetchState {
  status: 'idle' | 'loading' | 'succeeded' | 'failed'
  data: Data | null
  error: string | null
}

// Only allow valid transitions
builder
  .addCase(fetchData.pending, (state) => {
    if (state.status === 'idle') state.status = 'loading'
  })
```

### Use React-Redux Hooks
```typescript
// ❌ Old connect HOC
export default connect(mapState, mapDispatch)(Component)

// ✅ Hooks
const todos = useSelector(selectTodos)
const dispatch = useDispatch()
```

### Multiple Granular useSelector Calls
```typescript
// ❌ Selecting too much - rerenders on any user change
const user = useSelector(state => state.user)

// ✅ Granular - only rerenders when name changes
const name = useSelector(state => state.user.name)
const email = useSelector(state => state.user.email)
```

### Connect More Components
```typescript
// ✅ Parent selects IDs, child selects individual item
const UserList = () => {
  const ids = useSelector(selectUserIds)
  return ids.map(id => <UserItem key={id} userId={id} />)
}

const UserItem = ({ userId }) => {
  const user = useSelector(state => selectUserById(state, userId))
  return <div>{user.name}</div>
}
```

## Recommended Patterns (Priority C)

### Selector Naming: `selectThing`
```typescript
export const selectTodos = (state: RootState) => state.todos
export const selectTodoById = (state: RootState, id: string) =>
  state.todos.entities[id]
export const selectCompletedTodos = createSelector(
  [selectTodos],
  todos => todos.filter(t => t.completed)
)
```

### Action Type Format: `domain/eventName`
```typescript
// ✅ RTK default
'todos/todoAdded'
'users/userLoggedIn'

// ❌ Old SCREAMING_SNAKE_CASE
'ADD_TODO'
```

### Async Logic with Thunks
```typescript
export const fetchTodos = createAsyncThunk(
  'todos/fetchTodos',
  async (_, { rejectWithValue }) => {
    try {
      return await todosAPI.fetchAll()
    } catch (err) {
      return rejectWithValue(err.message)
    }
  }
)

// Handle in slice
extraReducers: builder => {
  builder
    .addCase(fetchTodos.pending, state => { state.status = 'loading' })
    .addCase(fetchTodos.fulfilled, (state, action) => {
      state.status = 'succeeded'
      state.items = action.payload
    })
    .addCase(fetchTodos.rejected, (state, action) => {
      state.status = 'failed'
      state.error = action.payload as string
    })
}
```

### Use RTK Query for Data Fetching
```typescript
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    getTodos: builder.query<Todo[], void>({
      query: () => 'todos'
    }),
    addTodo: builder.mutation<Todo, Partial<Todo>>({
      query: (body) => ({ url: 'todos', method: 'POST', body })
    })
  })
})

export const { useGetTodosQuery, useAddTodoMutation } = api
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | Solution |
|-------------|---------|----------|
| Form state in Redux | Performance overhead, not global | Local `useState` |
| UI state in Redux | Modal open/closed isn't global | Component state |
| Blind spread `return action.payload` | Loses reducer ownership | Explicit field mapping |
| Sequential dispatches | Multiple renders, invalid states | Single event action |
| Deeply nested state | Complex updates | Normalize |
| Side effects in reducers | Breaks time-travel debug | Use thunks/middleware |
| Selecting entire state slice | Unnecessary rerenders | Granular selectors |
| `Immutable.js` | Bundle bloat, API infection | Use Immer (built into RTK) |

## When NOT to Use Redux

Keep in local component state:
- Form input values (dispatch on submit only)
- UI toggles (modal open, dropdown expanded)
- Animation state
- Hover/focus states
- Data only used by one component

Use Redux for:
- User authentication
- Shopping cart
- Cached API data
- App-wide notifications
- Cross-component shared state

## Type-Safe Setup

```typescript
// app/hooks.ts
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux'
import type { RootState, AppDispatch } from './store'

export const useAppDispatch: () => AppDispatch = useDispatch
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
```

## References

- See [references/slice-patterns.md](references/slice-patterns.md) for complete slice examples with normalized state and async logic

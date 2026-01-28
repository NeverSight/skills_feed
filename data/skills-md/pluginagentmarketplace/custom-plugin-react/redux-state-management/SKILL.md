---
name: redux-state-management
description: Master Redux Toolkit for production state management including slices, async thunks, RTK Query, and error handling
sasmp_version: "2.0.0"
bonded_agent: 04-state-management
bond_type: PRIMARY_BOND
input_validation:
  required_packages:
    - "@reduxjs/toolkit": ">=2.0.0"
    - "react-redux": ">=9.0.0"
output_format:
  code_examples: typescript
  test_template: jest
error_handling:
  patterns:
    - retry_query
    - optimistic_update
    - error_boundary
  retry_config:
    max_retries: 3
    backoff_multiplier: 2
observability:
  logging: redux_devtools
  metrics: ["action_count", "state_size"]
---

# Redux State Management Skill

## Overview
Master Redux Toolkit for state management in React applications, including store configuration, slices, async operations, and RTK Query for API state.

## Learning Objectives
- Configure Redux store with Redux Toolkit
- Create slices and reducers
- Handle async operations with createAsyncThunk
- Use RTK Query for API data management
- Integrate Redux DevTools

## Quick Start

### Installation
```bash
npm install @reduxjs/toolkit react-redux
```

### Store Setup
```javascript
// store.js
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './features/counter/counterSlice';
import userReducer from './features/user/userSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    user: userReducer
  }
});

// App.jsx
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
  return (
    <Provider store={store}>
      <YourApp />
    </Provider>
  );
}
```

## Creating Slices

```javascript
// counterSlice.js
import { createSlice } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      state.value += 1; // Immer allows "mutation"
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    }
  }
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;
```

## Using Redux in Components

```jsx
import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from './counterSlice';

function Counter() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(decrement())}>-</button>
    </div>
  );
}
```

## Async Operations

```javascript
// userSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId) => {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState: {
    user: null,
    status: 'idle',
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.user = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  }
});

export default userSlice.reducer;
```

## RTK Query

```javascript
// api.js
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['Posts', 'Users'],
  endpoints: (builder) => ({
    getPosts: builder.query({
      query: () => '/posts',
      providesTags: ['Posts']
    }),
    getPost: builder.query({
      query: (id) => `/posts/${id}`,
      providesTags: (result, error, id) => [{ type: 'Posts', id }]
    }),
    addPost: builder.mutation({
      query: (post) => ({
        url: '/posts',
        method: 'POST',
        body: post
      }),
      invalidatesTags: ['Posts']
    }),
    updatePost: builder.mutation({
      query: ({ id, ...patch }) => ({
        url: `/posts/${id}`,
        method: 'PATCH',
        body: patch
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Posts', id }]
    })
  })
});

export const {
  useGetPostsQuery,
  useGetPostQuery,
  useAddPostMutation,
  useUpdatePostMutation
} = api;
```

### Using RTK Query in Components

```jsx
function PostList() {
  const { data: posts, isLoading, error } = useGetPostsQuery();
  const [addPost] = useAddPostMutation();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
      <button onClick={() => addPost({ title: 'New Post' })}>
        Add Post
      </button>
    </div>
  );
}
```

## Practice Exercises

1. Build a todo app with Redux Toolkit
2. Implement user authentication flow
3. Create shopping cart with Redux
4. Build API integration with RTK Query
5. Implement optimistic updates
6. Create normalized state with Entity Adapter

## Resources

- [Redux Toolkit Docs](https://redux-toolkit.js.org)
- [RTK Query Tutorial](https://redux-toolkit.js.org/rtk-query/overview)
- [Redux DevTools](https://github.com/reduxjs/redux-devtools)

---

## Error Handling Patterns

```typescript
// RTK Query with retry and error handling
const api = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: '/api',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) headers.set('authorization', `Bearer ${token}`);
      return headers;
    },
  }),
  endpoints: (builder) => ({
    getData: builder.query({
      query: (id) => `data/${id}`,
      // Retry configuration
      extraOptions: { maxRetries: 3 },
      // Transform error for better handling
      transformErrorResponse: (response) => ({
        status: response.status,
        message: response.data?.message || 'Unknown error',
      }),
    }),
  }),
});
```

## Unit Test Template

```typescript
import { configureStore } from '@reduxjs/toolkit';
import { renderHook, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { api } from './api';

describe('Redux State', () => {
  const wrapper = ({ children }) => (
    <Provider store={configureStore({ reducer: { [api.reducerPath]: api.reducer } })}>
      {children}
    </Provider>
  );

  it('should fetch data successfully', async () => {
    const { result } = renderHook(() => api.useGetDataQuery(1), { wrapper });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toBeDefined();
  });
});
```

---

**Version**: 2.0.0
**Last Updated**: 2025-12-30
**SASMP Version**: 2.0.0
**Difficulty**: Intermediate
**Estimated Time**: 2-3 weeks
**Prerequisites**: React Hooks, State Management Concepts
**Changelog**: Added RTK Query patterns, error handling, and test templates

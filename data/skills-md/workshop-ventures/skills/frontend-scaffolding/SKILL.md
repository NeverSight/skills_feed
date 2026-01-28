---
name: frontend-scaffolding
description: Scaffold a React frontend with Tailwind CSS, React Router, React Query, and standard project structure. Use when asked to "create a frontend", "scaffold webapp", "set up React app", or "initialize frontend structure".
---

# Frontend Scaffolding

Scaffold a React frontend with Tailwind CSS v4, React Router v6, React Query (TanStack Query), Axios API client, and established patterns.

## Structure Overview

```
apps/webapp/src/
├── app/
│   └── app.tsx              # Main app component with routes
├── api/
│   ├── client.ts            # Axios client configuration
│   └── {resource}.ts        # Resource-specific API functions
├── components/
│   ├── common/              # Shared components (Button, Card, etc.)
│   ├── layouts/             # Layout components
│   └── nav/                 # Navigation components
├── pages/
│   └── Home.tsx             # Page components
├── hooks/
│   └── use{Resource}.ts     # React Query hooks
├── lib/
│   └── queryClient.ts       # React Query client
├── styles.css               # Global styles and Tailwind theme
└── main.tsx                 # Application entry point
```

## Installation

```bash
npm install react react-dom react-router-dom axios @tanstack/react-query
npm install -D tailwindcss @tailwindcss/vite
```

## Implementation Steps

### 1. Main Entry Point (`main.tsx`)

```typescript
import { StrictMode } from 'react';
import * as ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';

import App from './app/app';
import { queryClient } from './lib/queryClient';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>
);
```

### 2. React Query Client (`lib/queryClient.ts`)

```typescript
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      retry: 1,
    },
  },
});
```

### 3. API Client (`api/client.ts`)

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NX_API_URL || 'http://localhost:3333';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.message || error.message || 'An error occurred';
    console.error('API Error:', message);
    return Promise.reject(error);
  }
);
```

### 4. App Component (`app/app.tsx`)

```typescript
import { Route, Routes } from 'react-router-dom';
import Home from '../pages/Home';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
  );
}

export default App;
```

### 5. Global Styles, Components, and Hooks

See [references/examples.md](references/examples.md) for complete code examples including:
- Tailwind CSS v4 theme configuration with design tokens
- Navigation components (NavButton, HeaderNav)
- Common components (Button, Card, LoadingSpinner)
- Example API module and React Query hooks
- Page with data fetching pattern
- Form with mutation pattern

## Checklist

1. **Install dependencies**: `npm install`
2. **Start frontend**: `just serve-webapp`
3. **Test home page**: Open `http://localhost:4200`
4. **Check API connection**: Ensure backend is running on `http://localhost:3333`

## Best Practices

1. **Use Tailwind CSS**: Style with utility classes, no component libraries
2. **Design tokens in CSS variables**: Define colors in `:root`, extend with `@theme`
3. **API layer separation**: Keep API functions in `api/`, hooks in `hooks/`
4. **React Query for server state**: Wrap API calls with `useQuery` and `useMutation`
5. **Keep pages thin**: Extract route params, render feature components
6. **Type everything**: Use TypeScript for all props and functions
7. **Import types from @{project}/types**: Share types with backend
8. **Handle loading/error states**: Always show appropriate UI
9. **Use `className` prop**: Allow style overrides on components
10. **Consistent query keys**: Use predictable patterns for cache invalidation

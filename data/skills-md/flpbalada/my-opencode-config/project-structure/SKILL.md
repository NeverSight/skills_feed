---
name: project-structure
description: Guides React/Next.js/TypeScript project organization using feature-based architecture. Use when structuring new projects, reorganizing codebases, or deciding where to place new code.
---

# Project Structure: Feature-Based Architecture

## Core Principle

**Organize code by feature/domain, not by file type. Enforce unidirectional code flow: shared → features → app.**

This approach scales well for medium-to-large React, Next.js, and TypeScript projects while keeping features independent and maintainable.

## Top-Level Structure

```
src/
├── app/                # Application layer (routing, providers)
│   ├── routes/         # Route definitions / pages
│   ├── app.tsx         # Main application component
│   ├── provider.tsx    # Global providers wrapper
│   └── router.tsx      # Router configuration
├── assets/             # Static files (images, fonts)
├── components/         # Shared UI components
├── config/             # Global configuration, env variables
├── features/           # Feature-based modules (main code lives here)
├── hooks/              # Shared hooks
├── lib/                # Pre-configured libraries (axios, dayjs, etc.)
├── stores/             # Global state stores
├── testing/            # Test utilities and mocks
├── types/              # Shared TypeScript types
└── utils/              # Shared utility functions
```

## Feature Structure

Each feature is a self-contained module:

```
src/features/users/
├── api/           # API requests & React Query hooks
├── components/    # Feature-scoped UI components
├── hooks/         # Feature-scoped hooks
├── stores/        # Feature state (Zustand, etc.)
├── types/         # Feature-specific types
└── utils/         # Feature utility functions
```

**Only include folders you need.** Don't create empty folders "just in case."

## Unidirectional Code Flow

```
┌─────────┐     ┌──────────┐     ┌─────┐
│ shared  │ ──► │ features │ ──► │ app │
└─────────┘     └──────────┘     └─────┘
```

| From | Can Import From |
|------|-----------------|
| `app` | `features`, `shared` (components, hooks, lib, types, utils) |
| `features` | `shared` only |
| `shared` | Other `shared` modules only |

**Features cannot import from each other.** Compose features at the app level.

## Decision Guide: Where Does This Code Go?

| Code Type | Location | Example |
|-----------|----------|---------|
| Route/page component | `app/routes/` | `app/routes/users/page.tsx` |
| Feature-specific component | `features/[name]/components/` | `features/users/components/UserCard.tsx` |
| Reusable UI component | `components/` | `components/Button.tsx` |
| Feature API calls | `features/[name]/api/` | `features/users/api/getUsers.ts` |
| Shared utility | `utils/` | `utils/formatDate.ts` |
| Feature utility | `features/[name]/utils/` | `features/users/utils/validateUser.ts` |
| Global state | `stores/` | `stores/authStore.ts` |
| Feature state | `features/[name]/stores/` | `features/users/stores/userFilterStore.ts` |
| Library wrapper | `lib/` | `lib/axios.ts`, `lib/dayjs.ts` |
| Global types | `types/` | `types/api.ts` |
| Feature types | `features/[name]/types/` | `features/users/types/user.ts` |

## ESLint Enforcement

### Prevent Cross-Feature Imports

```javascript
// .eslintrc.js
module.exports = {
  rules: {
    'import/no-restricted-paths': [
      'error',
      {
        zones: [
          // Disables cross-feature imports
          {
            target: './src/features/users',
            from: './src/features',
            except: ['./users'],
          },
          {
            target: './src/features/posts',
            from: './src/features',
            except: ['./posts'],
          },
          // Add more features as needed
        ],
      },
    ],
  },
};
```

### Enforce Unidirectional Flow

```javascript
// .eslintrc.js
module.exports = {
  rules: {
    'import/no-restricted-paths': [
      'error',
      {
        zones: [
          // Features cannot import from app
          {
            target: './src/features',
            from: './src/app',
          },
          // Shared cannot import from features or app
          {
            target: [
              './src/components',
              './src/hooks',
              './src/lib',
              './src/types',
              './src/utils',
            ],
            from: ['./src/features', './src/app'],
          },
        ],
      },
    ],
  },
};
```

## Common Patterns

### Feature API with React Query

```typescript
// src/features/users/api/getUsers.ts
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/axios';
import type { User } from '../types/user';

export const getUsers = async (): Promise<User[]> => {
  const response = await api.get('/users');
  return response.data;
};

export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: getUsers,
  });
};
```

### Feature Component

```typescript
// src/features/users/components/UserList.tsx
import { useUsers } from '../api/getUsers';
import { UserCard } from './UserCard';

export function UserList() {
  const { data: users, isLoading } = useUsers();
  
  if (isLoading) return <Spinner />;
  
  return (
    <div className="grid gap-4">
      {users?.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

### Composing Features at App Level

```typescript
// src/app/routes/dashboard/page.tsx
import { UserList } from '@/features/users/components/UserList';
import { PostList } from '@/features/posts/components/PostList';
import { ActivityFeed } from '@/features/activity/components/ActivityFeed';

export function DashboardPage() {
  return (
    <div className="grid grid-cols-3 gap-6">
      <UserList />
      <PostList />
      <ActivityFeed />
    </div>
  );
}
```

## Anti-Patterns to Avoid

### Don't Use Barrel Files (index.ts)

```typescript
// src/features/users/index.ts
export * from './components/UserList';  // Breaks tree-shaking in Vite
export * from './api/getUsers';
```

**Instead, import directly:**

```typescript
import { UserList } from '@/features/users/components/UserList';
import { useUsers } from '@/features/users/api/getUsers';
```

### Don't Import Across Features

```typescript
// src/features/posts/components/PostCard.tsx
import { UserAvatar } from '@/features/users/components/UserAvatar';  // Bad
```

**Instead, lift shared components:**

```typescript
// Move UserAvatar to src/components/UserAvatar.tsx
import { UserAvatar } from '@/components/UserAvatar';  // Good
```

### Don't Put Everything in Shared

If a component is only used by one feature, keep it in that feature:

```
// Bad: Polluting shared components
src/components/
├── UserCard.tsx          # Only used by users feature
├── PostCard.tsx          # Only used by posts feature
└── Button.tsx            # Actually shared

// Good: Feature-scoped components
src/features/users/components/UserCard.tsx
src/features/posts/components/PostCard.tsx
src/components/Button.tsx
```

## Next.js App Router Adaptation

For Next.js with App Router, adapt the structure:

```
src/
├── app/                  # Next.js App Router (routes)
│   ├── (auth)/           # Route group
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/
│   ├── layout.tsx
│   └── page.tsx
├── components/           # Shared components
├── features/             # Feature modules (non-routing code)
│   ├── auth/
│   ├── dashboard/
│   └── users/
├── lib/
└── ...
```

Keep route handlers minimal - delegate to feature modules:

```typescript
// src/app/users/page.tsx
import { UserList } from '@/features/users/components/UserList';

export default function UsersPage() {
  return <UserList />;
}
```

## Quick Checklist

### Starting a New Project

- [ ] Create top-level folder structure
- [ ] Set up path aliases (`@/` for `src/`)
- [ ] Configure ESLint import restrictions
- [ ] Create first feature as a template

### Adding a New Feature

- [ ] Create `src/features/[name]/` directory
- [ ] Add only needed subfolders (api, components, hooks, etc.)
- [ ] Add ESLint zone restriction for the feature
- [ ] Keep feature isolated - no cross-feature imports

### Before Code Review

- [ ] No cross-feature imports
- [ ] Shared code is in shared folders
- [ ] Feature-specific code stays in features
- [ ] No barrel files (index.ts re-exports)

## References

- [Bulletproof React](https://github.com/alan2207/bulletproof-react)
- [Feature-Sliced Design](https://feature-sliced.design/)
- [Next.js Project Organization](https://nextjs.org/docs/app/getting-started/project-structure)

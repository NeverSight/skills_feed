---
name: react-development-patterns
description: "React 18+ development patterns including components, hooks, state management, API integration, and accessibility. Use when: (1) building React components, (2) designing user interfaces, (3) implementing state management, (4) writing frontend tests."
layer: 2
tech_stack: [typescript, react, javascript]
topics: [react, typescript, hooks, state-management, accessibility, components]
depends_on: [typescript-advanced-types, modern-javascript-patterns]
complements: [javascript-testing-patterns, e2e-testing-patterns]
keywords: [React, useState, useEffect, useQuery, TypeScript, Component, Props, Accessibility, WCAG]
---

# React Development Patterns

React 18+ patterns for building modern, accessible, type-safe user interfaces.

## When to Use

- Building React components with TypeScript
- Designing UI wireframes and user flows
- Implementing state management
- Creating API service layers
- Writing accessible frontend code

## Component Patterns

### Basic Component

```tsx
import { FC } from 'react';

interface {Component}Props {
  title: string;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  onClick?: () => void;
}

export const {Component}: FC<{Component}Props> = ({
  title,
  variant = 'primary',
  disabled = false,
  onClick,
}) => {
  return (
    <button
      className={`btn btn-${variant}`}
      disabled={disabled}
      onClick={onClick}
    >
      {title}
    </button>
  );
};
```

### Data Fetching Component

```tsx
import { FC } from 'react';
import { useQuery } from '@tanstack/react-query';
import { {entity}Service } from '@/services/{entity}Service';
import type { {Entity}Dto } from '@/types';

interface {Entity}ListProps {
  onSelect: (entity: {Entity}Dto) => void;
}

export const {Entity}List: FC<{Entity}ListProps> = ({ onSelect }) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['{entities}'],
    queryFn: {entity}Service.getAll,
  });

  if (isLoading) return <Skeleton count={5} />;
  if (error) return <ErrorMessage error={error} />;
  if (!data?.length) return <EmptyState message="No items found" />;

  return (
    <ul role="list" aria-label="{Entity} list">
      {data.map((entity) => (
        <{Entity}Card
          key={entity.id}
          entity={entity}
          onClick={() => onSelect(entity)}
        />
      ))}
    </ul>
  );
};
```

## API Service Pattern

```typescript
import { api } from '@/lib/api';
import type { {Entity}Dto, Create{Entity}Dto, PagedResult } from '@/types';

export const {entity}Service = {
  getAll: async (params?: { skip?: number; take?: number }): Promise<PagedResult<{Entity}Dto>> => {
    const response = await api.get('/api/app/{entities}', { params });
    return response.data;
  },

  getById: async (id: string): Promise<{Entity}Dto> => {
    const response = await api.get(`/api/app/{entities}/${id}`);
    return response.data;
  },

  create: async (data: Create{Entity}Dto): Promise<{Entity}Dto> => {
    const response = await api.post('/api/app/{entities}', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Create{Entity}Dto>): Promise<{Entity}Dto> => {
    const response = await api.put(`/api/app/{entities}/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/app/{entities}/${id}`);
  },
};
```

## Wireframe Template

```markdown
## Screen: [Screen Name]

### Layout
┌─────────────────────────────────────┐
│ [Header: Logo | Nav | User Menu]    │
├─────────────────────────────────────┤
│ [Sidebar]  │  [Main Content]        │
│            │                        │
│ - Nav 1    │  ┌─────────┐ ┌─────────┐│
│ - Nav 2    │  │ Card 1  │ │ Card 2  ││
│ - Nav 3    │  └─────────┘ └─────────┘│
├─────────────────────────────────────┤
│ [Footer]                            │
└─────────────────────────────────────┘

### Components
- Header: Logo, Navigation, UserMenu
- Sidebar: NavItem[], CollapsibleSection
- Card: Image?, Title, Description, ActionButton

### Interactions
- Card click → Navigate to detail
- NavItem hover → Show tooltip

### States
- Loading: Skeleton placeholders
- Empty: "No items" + CTA
- Error: Error banner + retry
```

## Component Specification Template

```markdown
## Component: [ComponentName]

### Props
| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| variant | 'primary' \| 'secondary' | No | 'primary' | Visual style |
| disabled | boolean | No | false | Disable interactions |
| onClick | () => void | No | - | Click handler |

### States
- Default, Hover, Active, Disabled, Loading, Error

### Accessibility
- Role: button
- Keyboard: Enter/Space to activate
- aria-label required when icon-only
```

## State Management Patterns

### React Query (Server State)

```tsx
// queries.ts
export const use{Entity}Query = (id: string) => useQuery({
  queryKey: ['{entity}', id],
  queryFn: () => {entity}Service.getById(id),
  staleTime: 5 * 60 * 1000, // 5 minutes
});

export const use{Entities}Query = (params?: ListParams) => useQuery({
  queryKey: ['{entities}', params],
  queryFn: () => {entity}Service.getAll(params),
});

// mutations.ts
export const useCreate{Entity} = () => useMutation({
  mutationFn: {entity}Service.create,
  onSuccess: () => queryClient.invalidateQueries(['{entities}']),
});
```

### Zustand (Client State)

```tsx
import { create } from 'zustand';

interface UIStore {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  selectedId: string | null;
  setSelectedId: (id: string | null) => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  selectedId: null,
  setSelectedId: (id) => set({ selectedId: id }),
}));
```

## Accessibility Checklist

- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible
- [ ] Color contrast >= 4.5:1 for text
- [ ] Images have alt text
- [ ] Forms have labels
- [ ] Error messages associated with inputs
- [ ] Skip navigation link present
- [ ] Page has single h1
- [ ] Landmarks used (main, nav, aside)
- [ ] ARIA attributes used correctly

## Project Structure

```
ui/
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── common/        # Buttons, inputs, cards
│   │   └── layout/        # Header, sidebar, footer
│   ├── features/          # Feature-based modules
│   │   └── {feature}/     # Feature module
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API service layer
│   ├── store/             # State management
│   ├── types/             # TypeScript types
│   └── utils/             # Utility functions
├── tests/
│   ├── unit/              # Component unit tests
│   ├── integration/       # Feature integration tests
│   └── e2e/               # Playwright E2E tests
└── public/
```

## Testing Patterns

### Component Test

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { {Component} } from './{Component}';

describe('{Component}', () => {
  it('renders with title', () => {
    render(<{Component} title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<{Component} title="Test" onClick={handleClick} />);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<{Component} title="Test" disabled />);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

## Shared Knowledge

| Topic | File |
|-------|------|
| TypeScript types | `typescript-advanced-types` skill |
| ES6+ patterns | `modern-javascript-patterns` skill |
| Testing patterns | `javascript-testing-patterns` skill |

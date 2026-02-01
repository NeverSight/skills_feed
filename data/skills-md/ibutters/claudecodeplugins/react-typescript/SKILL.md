---
name: react-typescript
description: Modern React 19 with TypeScript development. Use for creating React components, hooks, context providers, and applications with strict TypeScript typing. Triggers on requests for React components, functional components, hooks, state management, event handling, or TypeScript interfaces/types for React.
---

# React TypeScript Development

## Core Patterns

### Component Structure

```tsx
import { type FC, type ReactNode } from 'react';

interface ComponentProps {
  children?: ReactNode;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  onClick?: () => void;
}

export const Component: FC<ComponentProps> = ({
  children,
  variant = 'primary',
  disabled = false,
  onClick,
}) => {
  return (
    <div 
      className={`component component--${variant}`}
      data-disabled={disabled}
      onClick={disabled ? undefined : onClick}
    >
      {children}
    </div>
  );
};
```

### Typing Guidelines

| Pattern | Use |
|---------|-----|
| `FC<Props>` | Standard functional components |
| `ReactNode` | Children, any renderable content |
| `ComponentPropsWithoutRef<'button'>` | Extend native HTML element props |
| `forwardRef<HTMLDivElement, Props>` | Components needing ref forwarding |

### Event Handler Types

```tsx
onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
onSubmit?: (event: React.FormEvent<HTMLFormElement>) => void;
onKeyDown?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
```

### Custom Hooks Pattern

```tsx
import { useState, useCallback } from 'react';

interface UseToggleReturn {
  value: boolean;
  toggle: () => void;
  setTrue: () => void;
  setFalse: () => void;
}

export const useToggle = (initialValue = false): UseToggleReturn => {
  const [value, setValue] = useState(initialValue);
  
  const toggle = useCallback(() => setValue(v => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);
  
  return { value, toggle, setTrue, setFalse };
};
```

### Context Pattern

```tsx
import { createContext, useContext, type FC, type ReactNode } from 'react';

interface ThemeContextValue {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export const useTheme = (): ThemeContextValue => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
};
```

## File Naming

```
ComponentName/
├── ComponentName.tsx          # Implementation
├── ComponentName.types.ts     # Types (optional)
├── ComponentName.stories.tsx  # Storybook
├── index.ts                   # Exports
```

## Best Practices

1. Explicit return types for public functions
2. Discriminated unions for complex state
3. `as const` for literal types
4. Generic components for reusable patterns
5. Handle undefined explicitly

## Integration

- **Atomic Design**: See atomic-design skill for hierarchy
- **CSS Tokens**: See css-tokens skill for styling
- **Storybook**: See storybook skill for docs

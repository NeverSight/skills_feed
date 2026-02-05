---
name: ideal-react-component
description: |
  Use when creating React components, structuring component files, organizing component code,
  debugging React hooks issues, or when asked to "create a React component", "structure this component",
  "review component structure", "refactor this component", "fix infinite loop", or "useEffect not working".
  Applies to both TypeScript and JavaScript React components. Includes hooks antipatterns.
license: MIT
metadata:
  author: Antonin Januska
  version: "1.1.0"
tags: [react, component, structure, organization, best-practices]
---

# Ideal React Component Structure

## Overview

A battle-tested pattern for organizing React component files that emphasizes readability, maintainability, and logical flow. This structure helps teams maintain consistency and makes components easier to understand at a glance.

**Core principle:** Declare everything in a predictable order—imports to styles to types to logic to render—so developers know where to find things.

## When to Use

**Always use when:**
- Creating new React components
- Refactoring existing components
- Reviewing component structure during code review
- Onboarding developers to component patterns

**Useful for:**
- Establishing team conventions
- Maintaining large component libraries
- Teaching React best practices
- Reducing cognitive load when reading components

**Avoid when:**
- Working with class components (this pattern is for function components)
- Component is < 20 lines and simple (don't over-engineer)
- Project has different established conventions (consistency > perfection)

## The Ideal Structure

Components should follow this seven-section pattern:

```tsx
// 1. IMPORTS (organized by source)
import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';

import { formatDate } from '@/utils/date';
import { api } from '@/services/api';

import { Button } from './Button';

// 2. STYLED COMPONENTS (prefixed with "Styled")
const StyledContainer = styled.div`
  padding: 1rem;
  background: white;
`;

// 3. TYPE DEFINITIONS (ComponentNameProps pattern)
type UserProfileProps = {
  userId: string;
  onUpdate?: (user: User) => void;
};

// 4. COMPONENT FUNCTION
export const UserProfile = ({ userId, onUpdate }: UserProfileProps): JSX.Element => {
  // 5. LOGIC SECTIONS (in this order)
  // - Local state
  // - Custom/data hooks
  // - useEffect/useLayoutEffect
  // - Post-processing
  // - Callback handlers

  // 6. CONDITIONAL RENDERING (exit early)
  if (isLoading) return <Loading />;
  if (error) return <Error message={error.message} />;
  if (!data) return <Empty />;

  // 7. DEFAULT RENDER (success state)
  return (
    <StyledContainer>
      {/* Main component JSX */}
    </StyledContainer>
  );
};
```

## Section 1: Import Organization

**Order imports by source to reduce cognitive load:**

```tsx
// ✅ Good: Clear grouping with blank lines
import React, { useState, useEffect, useMemo } from 'react';
import { useQuery, useMutation } from 'react-query';
import { format } from 'date-fns';

import { api } from '@/services/api';
import { formatCurrency } from '@/utils/format';

import { Button } from './Button';
import { Card } from './Card';
```

```tsx
// ❌ Bad: Random order, no grouping
import { Button } from './Button';
import { format } from 'date-fns';
import React, { useState } from 'react';
import { api } from '@/services/api';
import { useQuery } from 'react-query';
```

**Import priority:**
1. React imports (first)
2. Third-party libraries (followed by blank line)
3. Internal/aliased imports (`@/`) (followed by blank line)
4. Local component imports (same directory)

**Why:** "When you deal with more than a handful of imports, it's really easy to get lost in what the file is using."

## Section 2: Styled Components

**Prefix styling-only components with `Styled` for instant recognition:**

<Good>
```tsx
const StyledCard = styled.div`
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
`;

const StyledTitle = styled.h2`
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
`;

export const Card = ({ title, children }) => (
  <StyledCard>
    <StyledTitle>{title}</StyledTitle>
    {children}
  </StyledCard>
);
```
</Good>

<Bad>
```tsx
// ❌ Bad: Can't tell if CardWrapper is styled or contains logic
const CardWrapper = styled.div`
  border: 1px solid #ccc;
`;

const Title = styled.h2`
  font-size: 1.5rem;
`;
```
</Bad>

**When styled components grow large:**
- Move to co-located `ComponentName.styled.ts` file
- Import as `import * as S from './ComponentName.styled'`
- Use as `<S.Container>`, `<S.Title>`, etc.

**TypeScript:**
```tsx
// Card.styled.ts
import styled from 'styled-components';

export const Container = styled.div`
  padding: 1rem;
`;

export const Title = styled.h2`
  font-size: 1.5rem;
`;

// Card.tsx
import * as S from './Card.styled';

export const Card = () => (
  <S.Container>
    <S.Title>Title</S.Title>
  </S.Container>
);
```

**JavaScript:**
```jsx
// Same pattern works for .js/.jsx files
const StyledCard = styled.div`
  padding: 1rem;
`;
```

## Section 3: Type Definitions

**Declare types immediately above the component for visibility:**

<Good>
```tsx
// TypeScript
type ButtonProps = {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  onClick: () => void;
  children: React.ReactNode;
};

export const Button = ({
  variant = 'primary',
  size = 'md',
  onClick,
  children
}: ButtonProps): JSX.Element => {
  // Component logic
};
```
</Good>

<Bad>
```tsx
// ❌ Bad: Inline types hide the API
export const Button = ({
  variant,
  size,
  onClick,
  children
}: {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  onClick: () => void;
  children: React.ReactNode;
}) => {
  // Component logic
};
```
</Bad>

**Naming convention:**
- Props: `ComponentNameProps`
- Return types: Usually just use `JSX.Element`, but if custom: `ComponentNameReturn`

**JavaScript equivalent:**
```jsx
// JavaScript with JSDoc (optional)
/**
 * @typedef {Object} ButtonProps
 * @property {'primary' | 'secondary'} [variant]
 * @property {'sm' | 'md' | 'lg'} [size]
 * @property {() => void} onClick
 * @property {React.ReactNode} children
 */

/** @param {ButtonProps} props */
export const Button = ({
  variant = 'primary',
  size = 'md',
  onClick,
  children
}) => {
  // Component logic
};
```

**Why declare types separately:**
- "This type belongs to the component" and "isn't shareable"
- Makes component API visible at a glance
- Easier to modify without disturbing component code
- Better for documentation

## Section 4: Component Function

**Use named exports with const arrow functions:**

<Good>
```tsx
// TypeScript
export const UserProfile = ({ userId }: UserProfileProps): JSX.Element => {
  // Component logic
};
```

```jsx
// JavaScript
export const UserProfile = ({ userId }) => {
  // Component logic
};
```
</Good>

<Bad>
```tsx
// ❌ Bad: Default export makes refactoring harder
export default function UserProfile({ userId }: UserProfileProps): JSX.Element {
  // Component logic
}
```
</Bad>

**Why const + arrow functions:**
- Easy to wrap with `useCallback` later if needed
- Consistent with other hooks and callbacks in component
- Named exports are easier to refactor and search for

## Section 5: Logic Flow

**Organize component logic in this strict order:**

```tsx
export const UserProfile = ({ userId }: UserProfileProps): JSX.Element => {
  // 5.1 - LOCAL STATE (useState, useReducer, useRef, useMemo)
  const [isEditing, setIsEditing] = useState(false);
  const [selectedTab, setSelectedTab] = useState('profile');
  const inputRef = useRef<HTMLInputElement>(null);

  // 5.2 - CUSTOM/DATA HOOKS (react-query, API calls, custom hooks)
  const { data: user, isLoading, error } = useQuery(['user', userId], () =>
    api.getUser(userId)
  );
  const { mutate: updateUser } = useMutation(api.updateUser);

  // 5.3 - useEffect/useLayoutEffect (side effects)
  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isEditing]);

  // 5.4 - POST-PROCESSING (transformations, computed values)
  const displayName = user ? `${user.firstName} ${user.lastName}` : '';
  const formattedDate = user?.createdAt ? format(user.createdAt, 'PPP') : '';

  // 5.5 - CALLBACK HANDLERS (arrow functions for easy useCallback conversion)
  const handleEdit = () => setIsEditing(true);
  const handleCancel = () => setIsEditing(false);
  const handleSave = (updates: Partial<User>) => {
    updateUser(updates);
    setIsEditing(false);
  };

  // [Next: Conditional rendering - Section 6]
  // [Then: Default render - Section 7]
};
```

**Why this order:**
- Respects React's hook rules (hooks must be called in same order)
- "Declare as much ahead of time as possible"
- Puts dependent logic after dependencies (e.g., effects after state)
- Makes component flow easy to trace

**JavaScript version is identical:**
```jsx
export const UserProfile = ({ userId }) => {
  // Same ordering applies
  const [isEditing, setIsEditing] = useState(false);
  // ... rest of logic
};
```

## Section 6: Conditional Rendering

**Exit early for loading, error, and empty states:**

<Good>
```tsx
export const UserProfile = ({ userId }: UserProfileProps): JSX.Element => {
  const { data, isLoading, error } = useQuery(['user', userId], () =>
    api.getUser(userId)
  );

  // Exit early - each conditional gets own return
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error.message} />;
  if (!data) return <EmptyState message="User not found" />;

  // Success state continues below
  return (
    <div>
      {/* Main component JSX */}
    </div>
  );
};
```
</Good>

<Bad>
```tsx
// ❌ Bad: Nested ternaries are hard to read
export const UserProfile = ({ userId }: UserProfileProps): JSX.Element => {
  const { data, isLoading, error } = useQuery(['user', userId], () =>
    api.getUser(userId)
  );

  return (
    <div>
      {isLoading ? (
        <LoadingSpinner />
      ) : error ? (
        <ErrorMessage message={error.message} />
      ) : !data ? (
        <EmptyState message="User not found" />
      ) : (
        <div>
          {/* Main component JSX buried deep */}
        </div>
      )}
    </div>
  );
};
```
</Bad>

**Benefits of early returns:**
- Reduces nesting depth
- Main success render stays at bottom (most important case)
- Each condition is independent and easy to test
- TypeScript can narrow types after guards

**Works same in JavaScript:**
```jsx
if (isLoading) return <LoadingSpinner />;
if (error) return <ErrorMessage message={error.message} />;
if (!data) return <EmptyState />;
```

## Section 7: Default Render

**Keep the success/default render at the bottom:**

```tsx
export const UserProfile = ({ userId }: UserProfileProps): JSX.Element => {
  // [Sections 1-6 above]

  // Success state - the main component render
  return (
    <StyledContainer>
      <StyledHeader>
        <StyledTitle>{displayName}</StyledTitle>
        <Button onClick={handleEdit}>Edit</Button>
      </StyledHeader>

      {isEditing ? (
        <EditForm
          user={user}
          onSave={handleSave}
          onCancel={handleCancel}
        />
      ) : (
        <UserDetails user={user} />
      )}

      <StyledFooter>
        Member since {formattedDate}
      </StyledFooter>
    </StyledContainer>
  );
};
```

**Why default render goes last:**
- Most important case (happy path) is most visible
- After all error states eliminated
- All data and handlers already declared
- Mirrors how you mentally reason about component

## Refactoring: Extract to Custom Hooks

**When components grow complex, extract logic into custom hooks:**

<Good>
```tsx
// usePost.ts
export const usePost = (postId: string) => {
  const [isEditing, setIsEditing] = useState(false);

  const { data: post, isLoading, error } = useQuery(
    ['post', postId],
    () => api.getPost(postId)
  );

  const { mutate: updatePost } = useMutation(api.updatePost);

  const formattedContent = post?.content
    ? formatMarkdown(post.content)
    : '';

  const handleEdit = () => setIsEditing(true);
  const handleSave = (updates: Partial<Post>) => {
    updatePost(updates);
    setIsEditing(false);
  };

  return {
    post,
    isLoading,
    error,
    isEditing,
    formattedContent,
    handleEdit,
    handleSave,
  };
};

// PostView.tsx - Clean component focused on presentation
export const PostView = ({ postId }: PostViewProps): JSX.Element => {
  const {
    post,
    isLoading,
    error,
    isEditing,
    formattedContent,
    handleEdit,
    handleSave,
  } = usePost(postId);

  if (isLoading) return <Loading />;
  if (error) return <Error message={error.message} />;
  if (!post) return <Empty />;

  return (
    <StyledContainer>
      {/* Simple presentation-focused JSX */}
    </StyledContainer>
  );
};
```
</Good>

**When to extract to custom hooks:**
- Component logic exceeds 50 lines
- State management becomes complex
- Multiple effects interact
- Logic is reusable across components
- Component file exceeds 200 lines

**Hook naming:** `use[Domain]` pattern (e.g., `usePost`, `useAuth`, `useCart`)

**JavaScript version:**
```jsx
// usePost.js - Same pattern
export const usePost = (postId) => {
  // Same logic, no type annotations
  return {
    post,
    isLoading,
    // ...
  };
};
```

## React Hooks: Antipatterns and Gotchas

**Common mistakes that cause bugs, performance issues, and infinite loops:**

### Antipattern 1: useEffect "onChange" Callback

**Problem:** Using `useEffect` to notify parent components whenever state changes.

<Bad>
```tsx
type FormProps = {
  initialValue: string;
  onChange: (value: string) => void;
};

export const Form = ({ initialValue, onChange }: FormProps) => {
  const [formValue, setFormValue] = useState(initialValue);

  // ❌ Bad: Creates extra re-render cycle
  useEffect(() => {
    onChange(formValue);
  }, [formValue, onChange]);

  return (
    <input
      value={formValue}
      onChange={(e) => setFormValue(e.target.value)}
    />
  );
};
```
</Bad>

**Why it's problematic:**
- Causes double render: state update → component re-render → `useEffect` queued → `useEffect` runs → parent updates → child re-renders again
- If parent's `onChange` modifies `formValue`, creates infinite loop
- ESLint exhaustive-deps forces including `onChange`, worsening the issue

<Good>
```tsx
// ✅ Good: Call onChange directly when setting state
export const Form = ({ initialValue, onChange }: FormProps) => {
  const [formValue, setFormValue] = useState(initialValue);

  const handleChange = (value: string) => {
    setFormValue(value);
    onChange(value); // Notify parent immediately
  };

  return (
    <input
      value={formValue}
      onChange={(e) => handleChange(e.target.value)}
    />
  );
};
```

```tsx
// ✅ Good: Or inline if simple
export const Form = ({ initialValue, onChange }: FormProps) => {
  const [formValue, setFormValue] = useState(initialValue);

  return (
    <input
      value={formValue}
      onChange={(e) => {
        const value = e.target.value;
        setFormValue(value);
        onChange(value);
      }}
    />
  );
};
```
</Good>

**JavaScript version:**
```jsx
// Same pattern applies
export const Form = ({ initialValue, onChange }) => {
  const [formValue, setFormValue] = useState(initialValue);

  const handleChange = (value) => {
    setFormValue(value);
    onChange(value);
  };

  return (
    <input
      value={formValue}
      onChange={(e) => handleChange(e.target.value)}
    />
  );
};
```

### Antipattern 2: useState Initial Value Confusion

**Problem:** Expecting `useState` to update when props change after initial render.

<Bad>
```tsx
type UserProfileProps = {
  initialName: string;
};

export const UserProfile = ({ initialName }: UserProfileProps) => {
  // ❌ Bad: Only uses initialName on first render
  // If initialName prop changes, userName stays the same!
  const [userName, setUserName] = useState(initialName);

  return (
    <div>
      <input
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
    </div>
  );
};
```
</Bad>

**Why it's problematic:**
- `useState` initializer runs only once (first render)
- Prop changes don't update state automatically
- Function initializers (`useState(() => expensive())`) also run every render but discard results after first render

<Good>
```tsx
// ✅ Good: Use useEffect to sync when prop changes
export const UserProfile = ({ initialName }: UserProfileProps) => {
  const [userName, setUserName] = useState(initialName);

  useEffect(() => {
    setUserName(initialName);
  }, [initialName]);

  return (
    <div>
      <input
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
    </div>
  );
};
```

```tsx
// ✅ Better: Use key prop to reset component
// Parent component
<UserProfile key={userId} initialName={user.name} />

// This forces React to create fresh component when userId changes
```

```tsx
// ✅ Best: Don't duplicate state if you don't need local modifications
export const UserProfile = ({ name }: UserProfileProps) => {
  return (
    <div>
      <p>{name}</p>
    </div>
  );
};
```
</Good>

**When to use expensive function initializer:**
```tsx
// ✅ Good: Function only runs once
const [state, setState] = useState(() => {
  return expensiveComputation(props.value);
});

// ❌ Bad: expensiveComputation runs every render
const [state, setState] = useState(expensiveComputation(props.value));
```

**JavaScript version:**
```jsx
// Same patterns apply
export const UserProfile = ({ initialName }) => {
  const [userName, setUserName] = useState(initialName);

  useEffect(() => {
    setUserName(initialName);
  }, [initialName]);

  return <div>{/* ... */}</div>;
};
```

### Antipattern 3: Non-Exhaustive useEffect Dependencies

**Problem:** Omitting dependencies from `useEffect` to avoid triggering effects.

<Bad>
```tsx
type ModalProps = {
  onOpen: () => void;
  onClose: () => void;
};

export const Modal = ({ onOpen, onClose }: ModalProps) => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (isOpen) {
      onOpen(); // ❌ Uses onOpen but not in dependencies
    } else {
      onClose(); // ❌ Uses onClose but not in dependencies
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]); // Missing onOpen, onClose

  // ...
};
```
</Bad>

**Why it's problematic:**
- **Stale closures:** Effect captures old versions of callbacks with outdated data
- **Async bugs:** If `onOpen`/`onClose` dependencies change, incorrect callbacks run
- **Data inconsistency:** Cascading issues when unmemoized callbacks throughout component tree
- **Silent failures:** Logic appears to work but operates on stale data

<Good>
```tsx
// ✅ Good: Include all dependencies
export const Modal = ({ onOpen, onClose }: ModalProps) => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (isOpen) {
      onOpen();
    } else {
      onClose();
    }
  }, [isOpen, onOpen, onClose]); // All dependencies included

  // ...
};
```

```tsx
// ✅ Better: Memoize callbacks in parent
const Parent = () => {
  const handleOpen = useCallback(() => {
    console.log('Modal opened');
  }, []);

  const handleClose = useCallback(() => {
    console.log('Modal closed');
  }, []);

  return <Modal onOpen={handleOpen} onClose={handleClose} />;
};
```

```tsx
// ✅ Best: Refactor to eliminate effect dependency issues
export const Modal = ({ onOpen, onClose }: ModalProps) => {
  const handleToggle = (nextIsOpen: boolean) => {
    if (nextIsOpen) {
      onOpen();
    } else {
      onClose();
    }
  };

  return (
    <button onClick={() => handleToggle(!isOpen)}>
      Toggle Modal
    </button>
  );
};
```
</Good>

**Key principle:** Missing dependencies reveal design issues. Fix the design, don't silence the warning.

**JavaScript version:**
```jsx
// Same pattern - dependencies matter regardless of types
export const Modal = ({ onOpen, onClose }) => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (isOpen) {
      onOpen();
    } else {
      onClose();
    }
  }, [isOpen, onOpen, onClose]);

  // ...
};
```

### Hooks Best Practices Summary

**DO:**
- ✅ Call `onChange` callbacks directly when setting state (not in `useEffect`)
- ✅ Use `useEffect` with full dependency arrays (trust ESLint)
- ✅ Memoize callbacks with `useCallback` when passed as props
- ✅ Use function initializers for expensive `useState` computations
- ✅ Reset state via `key` prop instead of syncing with `useEffect`

**DON'T:**
- ❌ Use `useEffect` to notify parent of state changes
- ❌ Expect `useState` initial value to update with prop changes
- ❌ Omit dependencies from `useEffect` to prevent re-runs
- ❌ Disable exhaustive-deps ESLint rule to hide issues
- ❌ Run expensive computations in `useState` initializer without function wrapper

**When you see these patterns:**
| Pattern | Problem | Solution |
|---------|---------|----------|
| `useEffect(() => onChange(value), [value])` | Double render | Call `onChange` when setting state |
| `useState(props.value)` with changing prop | Stale state | Use `key` prop or `useEffect` to sync |
| `useEffect(..., [])` with missing deps | Stale closures | Include all dependencies |
| `useState(expensive())` | Runs every render | Use `useState(() => expensive())` |

## Complete Example: TypeScript

```tsx
// UserProfile.tsx
import React, { useState, useEffect, useRef } from 'react';
import { useQuery, useMutation } from 'react-query';
import { format } from 'date-fns';

import { api } from '@/services/api';

import { Button } from '@/components/Button';
import { EditForm } from './EditForm';
import { UserDetails } from './UserDetails';

const StyledContainer = styled.div`
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
`;

const StyledHeader = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
`;

const StyledTitle = styled.h1`
  font-size: 2rem;
  font-weight: 600;
`;

const StyledFooter = styled.footer`
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  color: #6b7280;
`;

type UserProfileProps = {
  userId: string;
  onUpdate?: (user: User) => void;
};

export const UserProfile = ({
  userId,
  onUpdate
}: UserProfileProps): JSX.Element => {
  // Local state
  const [isEditing, setIsEditing] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Data hooks
  const { data: user, isLoading, error } = useQuery(
    ['user', userId],
    () => api.getUser(userId)
  );
  const { mutate: updateUser } = useMutation(api.updateUser);

  // Effects
  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isEditing]);

  // Post-processing
  const displayName = user
    ? `${user.firstName} ${user.lastName}`
    : '';
  const formattedDate = user?.createdAt
    ? format(user.createdAt, 'PPP')
    : '';

  // Handlers
  const handleEdit = () => setIsEditing(true);

  const handleCancel = () => setIsEditing(false);

  const handleSave = (updates: Partial<User>) => {
    updateUser(updates, {
      onSuccess: (updatedUser) => {
        setIsEditing(false);
        onUpdate?.(updatedUser);
      },
    });
  };

  // Conditional renders
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error.message} />;
  if (!user) return <EmptyState message="User not found" />;

  // Default render
  return (
    <StyledContainer>
      <StyledHeader>
        <StyledTitle>{displayName}</StyledTitle>
        <Button onClick={handleEdit}>Edit Profile</Button>
      </StyledHeader>

      {isEditing ? (
        <EditForm
          user={user}
          onSave={handleSave}
          onCancel={handleCancel}
          ref={inputRef}
        />
      ) : (
        <UserDetails user={user} />
      )}

      <StyledFooter>
        Member since {formattedDate}
      </StyledFooter>
    </StyledContainer>
  );
};
```

## Complete Example: JavaScript

```jsx
// UserProfile.jsx
import React, { useState, useEffect, useRef } from 'react';
import { useQuery, useMutation } from 'react-query';
import { format } from 'date-fns';

import { api } from '@/services/api';

import { Button } from '@/components/Button';
import { EditForm } from './EditForm';
import { UserDetails } from './UserDetails';

const StyledContainer = styled.div`
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
`;

const StyledHeader = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
`;

const StyledTitle = styled.h1`
  font-size: 2rem;
  font-weight: 600;
`;

const StyledFooter = styled.footer`
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  color: #6b7280;
`;

export const UserProfile = ({ userId, onUpdate }) => {
  // Local state
  const [isEditing, setIsEditing] = useState(false);
  const inputRef = useRef(null);

  // Data hooks
  const { data: user, isLoading, error } = useQuery(
    ['user', userId],
    () => api.getUser(userId)
  );
  const { mutate: updateUser } = useMutation(api.updateUser);

  // Effects
  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isEditing]);

  // Post-processing
  const displayName = user
    ? `${user.firstName} ${user.lastName}`
    : '';
  const formattedDate = user?.createdAt
    ? format(user.createdAt, 'PPP')
    : '';

  // Handlers
  const handleEdit = () => setIsEditing(true);

  const handleCancel = () => setIsEditing(false);

  const handleSave = (updates) => {
    updateUser(updates, {
      onSuccess: (updatedUser) => {
        setIsEditing(false);
        onUpdate?.(updatedUser);
      },
    });
  };

  // Conditional renders
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error.message} />;
  if (!user) return <EmptyState message="User not found" />;

  // Default render
  return (
    <StyledContainer>
      <StyledHeader>
        <StyledTitle>{displayName}</StyledTitle>
        <Button onClick={handleEdit}>Edit Profile</Button>
      </StyledHeader>

      {isEditing ? (
        <EditForm
          user={user}
          onSave={handleSave}
          onCancel={handleCancel}
          ref={inputRef}
        />
      ) : (
        <UserDetails user={user} />
      )}

      <StyledFooter>
        Member since {formattedDate}
      </StyledFooter>
    </StyledContainer>
  );
};
```

## Quick Reference

| Section | What Goes Here | Why |
|---------|----------------|-----|
| 1. Imports | React, libraries, internal, local | Easy to find dependencies |
| 2. Styled Components | `Styled*` prefixed styling | Visual separation from logic |
| 3. Type Definitions | `*Props`, `*Return` types | Component API visibility |
| 4. Component Function | `export const Component =` | Named exports for refactoring |
| 5. Logic Flow | State → Hooks → Effects → Handlers | Respects hook rules, logical order |
| 6. Conditional Rendering | Early returns for edge cases | Reduces nesting |
| 7. Default Render | Success state JSX | Most important case most visible |

## Best Practices Summary

**DO:**
- ✅ Group imports by source with blank lines
- ✅ Prefix styled components with `Styled`
- ✅ Declare types above component (not inline)
- ✅ Use const + arrow functions for components
- ✅ Follow logic order: state → hooks → effects → handlers
- ✅ Exit early for loading/error states
- ✅ Extract complex logic to custom hooks
- ✅ Use named exports

**DON'T:**
- ❌ Mix import sources randomly
- ❌ Use generic names for styled components
- ❌ Inline complex types in parameters
- ❌ Use default exports
- ❌ Put effects before state they depend on
- ❌ Nest conditional renders in JSX
- ❌ Let component logic exceed 100 lines
- ❌ Forget to move styles to separate file when large

## Troubleshooting

### Problem: Component is getting too long (> 200 lines)

**Cause:** Too much logic in one file

**Solution:**
1. Extract data fetching to custom hook (`useUserProfile`)
2. Move styled components to `ComponentName.styled.ts`
3. Split into smaller sub-components
4. Extract complex calculations to utility functions

**Example:**
```tsx
// Before: 250 line component
export const UserProfile = () => {
  // 100 lines of state and logic
  // 50 lines of styled components
  // 100 lines of JSX
};

// After: 80 line component
import { useUserProfile } from './useUserProfile';
import * as S from './UserProfile.styled';

export const UserProfile = () => {
  const { user, handlers } = useUserProfile();
  // 30 lines of presentation logic
  // 50 lines of JSX
};
```

### Problem: Can't decide if something should be a styled component or a sub-component

**Cause:** Unclear separation between styling and logic

**Solution:**
- **Styled component** if it only adds styling (no props, no logic)
- **Sub-component** if it has its own props, state, or logic

```tsx
// Styled component - just styling
const StyledCard = styled.div`
  padding: 1rem;
  border: 1px solid #ccc;
`;

// Sub-component - has logic and props
type CardProps = {
  title: string;
  onClose: () => void;
  children: React.ReactNode;
};

const Card = ({ title, onClose, children }: CardProps) => (
  <StyledCard>
    <h2>{title}</h2>
    <button onClick={onClose}>Close</button>
    {children}
  </StyledCard>
);
```

### Problem: Import organization feels arbitrary

**Cause:** No clear grouping strategy

**Solution:**
Use this checklist:
1. Is it from `react` or `react-*`? → Group 1 (React imports)
2. Is it from `node_modules`? → Group 2 (Third-party)
3. Is it using path alias (`@/`)? → Group 3 (Internal)
4. Is it in same directory (`./`)? → Group 4 (Local)

Add blank line between groups.

### Problem: TypeScript types getting complex

**Cause:** Component does too much

**Solution:**
1. Split component into smaller pieces
2. Extract shared types to `types.ts`
3. Use utility types (`Pick`, `Omit`, `Partial`)

```tsx
// Shared types
// types.ts
export type User = {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  createdAt: Date;
};

// Component uses subset
// UserProfile.tsx
type UserProfileProps = {
  user: Pick<User, 'firstName' | 'lastName' | 'createdAt'>;
  onEdit: () => void;
};
```

### Problem: Not sure where to put a helper function

**Cause:** Helper could go in component or outside

**Solution:**
- **Inside component** if it uses props, state, or hooks
- **Outside component** if it's pure and reusable
- **Separate file** if used by multiple components

```tsx
// Pure helper - outside component
const formatFullName = (firstName: string, lastName: string): string => {
  return `${firstName} ${lastName}`;
};

export const UserProfile = ({ user }: UserProfileProps) => {
  // Uses props - inside component as handler
  const handleSave = () => {
    api.updateUser(user.id, { /* ... */ });
  };

  const displayName = formatFullName(user.firstName, user.lastName);
  // ...
};
```

### Problem: Conditional rendering getting messy

**Cause:** Too many states to handle

**Solution:**
Create a state enum and use switch/early returns:

```tsx
type LoadingState = 'idle' | 'loading' | 'error' | 'success';

export const UserProfile = ({ userId }: UserProfileProps) => {
  const [state, setState] = useState<LoadingState>('idle');
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<Error | null>(null);

  // Early returns based on state
  if (state === 'loading') return <Loading />;
  if (state === 'error' && error) return <Error message={error.message} />;
  if (state === 'idle') return <Empty />;
  if (state === 'success' && !user) return <Empty />;

  // Type narrowing guarantees user exists here
  return <UserDetails user={user} />;
};
```

### Problem: Component causing infinite re-render loop

**Cause:** Using `useEffect` to call parent `onChange` callback

**Solution:**
Call `onChange` directly when setting state, not in `useEffect`:

```tsx
// ❌ Bad
useEffect(() => {
  onChange(value);
}, [value, onChange]); // Can cause infinite loop

// ✅ Good
const handleChange = (newValue: string) => {
  setValue(newValue);
  onChange(newValue);
};
```

See "React Hooks: Antipatterns and Gotchas" section for more details.

### Problem: State not updating when prop changes

**Cause:** `useState` only uses initial value on first render

**Solution:**
Either sync with `useEffect`, use component `key` prop, or don't duplicate state:

```tsx
// Option 1: Sync with useEffect
useEffect(() => {
  setValue(propValue);
}, [propValue]);

// Option 2: Reset component with key (preferred)
<Component key={userId} initialValue={value} />

// Option 3: Don't duplicate state if not needed
const displayValue = localValue ?? propValue;
```

### Problem: useEffect running with stale data

**Cause:** Missing dependencies from dependency array

**Solution:**
Include all dependencies. If that causes issues, refactor the code:

```tsx
// ❌ Bad
useEffect(() => {
  doSomething(value);
}, []); // Missing 'value'

// ✅ Good
useEffect(() => {
  doSomething(value);
}, [value]);

// ✅ Better: Memoize if needed
const doSomethingMemoized = useCallback(() => {
  doSomething(value);
}, [value]);
```

## Integration

**This pattern works with:**
- **styled-components** - Original inspiration for styled component pattern
- **twin.macro** - Combines styled-components with Tailwind CSS
- **emotion** - Alternative CSS-in-JS library
- **React Query / TanStack Query** - Data fetching hooks
- **SWR** - Alternative data fetching
- **Zustand / Redux** - Global state management

**Pairs well with:**
- **ESLint** - Enforce import ordering with `eslint-plugin-import`
- **Prettier** - Auto-format code structure
- **TypeScript** - Type safety for props and state
- **Storybook** - Component documentation

**Use in combination with:**
- Component testing patterns (Vitest, Jest)
- Code review checklists
- Team style guides

## Variations and Flexibility

**Remember:** This is a pattern, not a law. Adapt as needed:

- **Small components** (< 50 lines) can skip some structure
- **Simple components** without state can skip logic sections
- **Presentational components** may not need data hooks
- **Different styling solutions** (CSS Modules, Tailwind) can replace styled-components section

**Core principle remains:** Predictable organization helps teams maintain code.

## References

**Based on:**
- [The Anatomy of My Ideal React Component](https://antjanus.com/digital-garden/the-anatomy-of-my-ideal-react-component) - Component structure by Antonin Januska
- [Common React Hooks Antipatterns and Gotchas](https://antjanus.com/digital-garden/common-react-hooks-antipatterns-and-gotchas) - Hooks best practices by Antonin Januska

**Official Documentation:**
- [React Docs: Function Components](https://react.dev/reference/react/Component)
- [React Hooks Rules](https://react.dev/reference/rules/rules-of-hooks)
- [styled-components Documentation](https://styled-components.com/)
- [TypeScript React Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

**Related Patterns:**
- [Component Folder Structure](https://react.dev/learn/thinking-in-react)
- [Custom Hooks Guide](https://react.dev/learn/reusing-logic-with-custom-hooks)

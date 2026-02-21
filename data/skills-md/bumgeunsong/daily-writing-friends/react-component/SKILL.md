---
name: react-component
description: Use when creating or modifying React components (.tsx files). Enforces component structure, import order, and hooks patterns.
---

# React Component Patterns

## Component Structure

Follow this order in every component file:

```typescript
// 1. External imports
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. Internal shared imports
import { Button } from '@/shared/ui/button';
import { useAuth } from '@/shared/hooks/useAuth';

// 3. Feature-specific imports
import { usePostEditor } from '../hooks/usePostEditor';

// 4. Types
interface PostEditorProps {
  boardId: string;
  initialContent?: string;
}

// 5. Component
export function PostEditor({ boardId, initialContent }: PostEditorProps) {
  // hooks first
  // derived state
  // handlers
  // render
}
```

## Custom Hooks Pattern

Place business logic in `[feature]/hooks/`:

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { createPost } from '../api/post';

export function usePostEditor(boardId: string) {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: (data: CreatePostData) => createPost(boardId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts', boardId] });
    },
  });

  return { createMutation };
}
```

## Path Aliases

```typescript
import { Component } from '@/shared/components/Component';
import { useHook } from '@board/hooks/useHook';
import { Post } from '@post/model/Post';

// Available: @/, @board/, @post/, @comment/, @draft/,
//            @notification/, @user/, @shared/, @login/, @stats/
```

## Quick Reference

| Location | Purpose |
|----------|---------|
| `[feature]/components/` | React components |
| `[feature]/hooks/` | Custom hooks with business logic |
| `[feature]/model/` | TypeScript types |
| `@/shared/ui/` | shadcn/ui components |
| `@/shared/hooks/` | Shared hooks |

---
name: agentic-jumpstart-code-quality
description: Code quality standards for TypeScript and React including naming conventions, file organization, error handling, and best practices. Use when reviewing code, establishing patterns, or when the user mentions code quality, standards, conventions, formatting, or linting.
---

# Code Quality Standards

## TypeScript Best Practices

### Type Safety

```typescript
// GOOD: Explicit types for function parameters and returns
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// GOOD: Use inferred types from Drizzle
import type { User, UserCreate } from "~/db/schema";

// GOOD: Define interfaces for complex objects
interface CourseWithProgress {
  course: Course;
  progress: number;
  completedModules: number[];
}

// AVOID: Using `any`
// function processData(data: any) { ... }

// BETTER: Use unknown and narrow
function processData(data: unknown) {
  if (isValidData(data)) {
    // data is now typed
  }
}
```

### Type Exports

```typescript
// Export types from schema
export type User = typeof users.$inferSelect;
export type UserCreate = typeof users.$inferInsert;

// Re-export for convenience
export type { User, UserCreate } from "~/db/schema";
```

## Naming Conventions

### Functions

| Layer | Convention | Example |
|-------|------------|---------|
| Data Access | `verbNoun` | `createUser`, `getSegmentById` |
| Use Cases | `verbNounUseCase` | `createUserUseCase`, `enrollInCourseUseCase` |
| Server Functions | `verbNounFn` | `createUserFn`, `updateProfileFn` |

### Components

```typescript
// PascalCase for components
function CourseCard({ course }: CourseCardProps) {}
function UserProfilePage() {}

// camelCase for props interfaces
interface CourseCardProps {
  course: Course;
  onEdit?: (id: number) => void;
}
```

### Files

```
src/
├── components/
│   ├── CourseCard.tsx      # PascalCase for components
│   └── ui/
│       └── button.tsx      # lowercase for shadcn/ui
├── hooks/
│   └── useAuth.ts          # camelCase with use prefix
├── fn/
│   └── users.ts            # lowercase, plural for collections
├── use-cases/
│   └── users.ts
└── data-access/
    └── users.ts
```

### Variables and Constants

```typescript
// camelCase for variables
const currentUser = await getUserById(userId);

// SCREAMING_SNAKE_CASE for constants
const MAX_FILE_SIZE = 500 * 1024 * 1024;
const API_TIMEOUT_MS = 30000;

// Constants at top of file or in /src/config/
// src/config/index.ts
export const MAX_TITLE_LENGTH = 100;
export const PAGINATION_DEFAULT_LIMIT = 20;
```

## File Organization

### Maximum File Length

**Never let a file exceed 1,000 lines.** Split into smaller modules:

```typescript
// BEFORE: One large file
// src/routes/admin/courses/route.tsx (1500 lines)

// AFTER: Split into smaller files
// src/routes/admin/courses/route.tsx
// src/routes/admin/courses/-components/CourseList.tsx
// src/routes/admin/courses/-components/CourseForm.tsx
// src/routes/admin/courses/-components/CourseFilters.tsx
```

### Import Order

```typescript
// 1. External packages
import { useState, useEffect } from "react";
import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";

// 2. Internal modules (path alias)
import { authenticatedMiddleware } from "~/lib/auth";
import { updateUserUseCase } from "~/use-cases/users";
import { Button } from "~/components/ui/button";

// 3. Types (with type keyword)
import type { User, UserCreate } from "~/db/schema";

// 4. Relative imports (if any)
import { CourseCard } from "./-components/CourseCard";
```

### Path Aliases

Always use `~/` for imports from `/src/`:

```typescript
// GOOD
import { Button } from "~/components/ui/button";
import { database } from "~/db";

// AVOID
import { Button } from "../../../components/ui/button";
```

## Error Handling

### Use PublicError for User-Facing Errors

```typescript
// src/use-cases/errors.ts
export class PublicError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "PublicError";
  }
}

// Usage
export async function enrollInCourseUseCase(userId: number, courseId: number) {
  const course = await getCourseById(courseId);
  if (!course) {
    throw new PublicError("Course not found");
  }

  const existing = await getEnrollment(userId, courseId);
  if (existing) {
    throw new PublicError("Already enrolled in this course");
  }

  return createEnrollment({ userId, courseId });
}
```

### Handle Errors Gracefully

```typescript
// In server functions - errors bubble up to error boundary
export const enrollFn = createServerFn()
  .middleware([authenticatedMiddleware])
  .inputValidator(z.object({ courseId: z.number() }))
  .handler(async ({ data, context }) => {
    return enrollInCourseUseCase(context.userId, data.courseId);
  });

// In components - use mutation error handling
const { mutate, error, isError } = useMutation({
  mutationFn: enrollFn,
  onError: (error) => {
    toast.error(error.message);
  },
});
```

## Magic Numbers

### Never Hard Code

```typescript
// BAD: Magic numbers in code
if (password.length < 8) { ... }
const result = items.slice(0, 20);

// GOOD: Constants at top of file
const MIN_PASSWORD_LENGTH = 8;
const DEFAULT_PAGE_SIZE = 20;

if (password.length < MIN_PASSWORD_LENGTH) { ... }
const result = items.slice(0, DEFAULT_PAGE_SIZE);

// BETTER: Shared constants in config
// src/config/index.ts
export const MIN_PASSWORD_LENGTH = 8;
export const DEFAULT_PAGE_SIZE = 20;
```

## Component Patterns

### Props Interface

```typescript
interface CourseCardProps {
  course: Course;
  onEdit?: (id: number) => void;
  onDelete?: (id: number) => void;
  className?: string;
}

export function CourseCard({
  course,
  onEdit,
  onDelete,
  className,
}: CourseCardProps) {
  return (
    <Card className={cn("", className)}>
      {/* content */}
    </Card>
  );
}
```

### Avoid Prop Drilling

```typescript
// BAD: Passing props through many levels
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserMenu user={user} />

// GOOD: Use context or query
const { data: user } = useQuery(userQueryOptions());
// or
const user = useUserContext();
```

## Hooks Rules

### Custom Hook Pattern

```typescript
// Prefix with "use"
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}
```

### Effect Cleanup

```typescript
useEffect(() => {
  const controller = new AbortController();

  fetchData({ signal: controller.signal })
    .then(setData)
    .catch((err) => {
      if (err.name !== "AbortError") setError(err);
    });

  // Always cleanup
  return () => controller.abort();
}, [dependency]);
```

## Comments

### When to Comment

```typescript
// GOOD: Explain WHY, not WHAT
// We need to sort by module order first, then by segment order within each module
const sortedSegments = segments.sort((a, b) => {
  if (a.moduleOrder !== b.moduleOrder) {
    return a.moduleOrder - b.moduleOrder;
  }
  return a.order - b.order;
});

// BAD: Obvious comments
// Loop through users
for (const user of users) { ... }

// BAD: Commented out code (just delete it)
// const oldFunction = () => { ... };
```

### JSDoc for Public APIs

```typescript
/**
 * Creates a new user account and sends welcome email.
 * @param data - User registration data
 * @throws {PublicError} If email is already registered
 * @returns The created user without sensitive fields
 */
export async function createUserUseCase(data: UserCreate) {
  // implementation
}
```

## Code Quality Checklist

- [ ] No `any` types - use `unknown` with type guards
- [ ] Naming follows conventions (verbNoun, verbNounUseCase, verbNounFn)
- [ ] Files under 1,000 lines
- [ ] No magic numbers - use constants
- [ ] Path alias `~/` used for imports
- [ ] Import order: external, internal, types, relative
- [ ] Errors use PublicError pattern
- [ ] Effects have cleanup functions
- [ ] No commented-out code
- [ ] Comments explain WHY, not WHAT

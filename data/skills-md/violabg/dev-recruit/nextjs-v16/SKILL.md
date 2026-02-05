---
name: nextjs-v16
description: Advanced patterns for Next.js 16 including cache components, server components, and error handling. Use when building pages, implementing data fetching, setting up caching strategies, or handling errors in Next.js applications.
license: MIT
metadata:
  author: devrecruit
  version: "1.0"
compatibility: Next.js 16.0.0 or later, React 19+
---

# Next.js v16 Skills

This skill covers best practices and patterns for developing with Next.js version 16, focusing on cache components, server-side rendering, and robust error handling.

## Cache Components

### Purpose

Implement efficient caching strategies to optimize performance and reduce server load using Next.js 16's cache components feature.

### Key Concepts

1. **"use cache" Directive**

   - Mark functions as cacheable to enable automatic memoization
   - Applied at the function level in server components
   - Revalidates based on `cacheLife()` configuration
   - Use for data fetching and computationally expensive operations

2. **Cache Tags with cacheTag()**

   - Tag cached data for granular revalidation
   - Allows invalidating specific data patterns
   - Use `updateTag()` utility after mutations

3. **Cache Lifespan with cacheLife()**
   - Define how long cached data remains valid
   - Supports absolute time and relative expiration
   - Configure based on data freshness requirements

### Implementation Patterns

```typescript
// Basic cache component
"use cache";
export async function getData() {
  const data = await db.query.execute();
  return data;
}

// With cache tags and lifespan
("use cache");
import { cacheLife, cacheTag } from "next/cache";

export async function getQuizzes() {
  cacheLife({ max: 60 * 60 }); // 1 hour
  cacheTag("quizzes");

  return await db.quizzes.findMany();
}
```

### Usage in Components

```typescript
// Page using cached data
import { Suspense } from "react";
import { QuizzesContent } from "./content";
import { Skeleton } from "@/components/ui/skeleton";

export default function QuizzesPage() {
  return (
    <Suspense fallback={<Skeleton />}>
      <QuizzesContent />
    </Suspense>
  );
}

// Content component with 'use cache'
("use cache");
import { getQuizzes } from "@/lib/data/quizzes";

export async function QuizzesContent() {
  const quizzes = await getQuizzes();
  return <div>{/* Render quizzes */}</div>;
}
```

### Cache Invalidation

After mutations, invalidate related cache:

```typescript
"use server";
import { updateTag } from "@/lib/utils/cache-utils";

export async function createQuiz(data) {
  const quiz = await db.quizzes.create(data);
  updateTag("quizzes"); // Invalidate quiz cache
  return quiz;
}
```

## Server Actions

### Purpose

Server actions provide a unified way to handle mutations and data operations directly from components without creating API routes. They are the preferred method for data mutations in Next.js 16.

### Why Server Actions Over API Routes

1. **Type Safety** - Direct TypeScript types from server to client
2. **Colocation** - Actions defined near the components that use them
3. **Progressive Enhancement** - Forms work without JavaScript
4. **Simplified Auth** - Direct access to server-side authentication
5. **No CORS** - No need for API endpoint configuration
6. **Better DX** - Single file for component + action logic

### When to Use Server Actions vs API Routes

**Use Server Actions for:**

- Form submissions and mutations
- Database operations (create, update, delete)
- User-triggered actions from UI components
- Data revalidation after changes
- File uploads
- Most CRUD operations

**Use API Routes only for:**

- Webhooks from external services
- Public APIs for third-party integrations
- Non-browser clients (mobile apps, CLI tools)
- Custom authentication callbacks
- Server-Sent Events (SSE) or WebSocket connections

### Basic Server Action Pattern

```typescript
// lib/actions/quizzes.ts
"use server";

import { z } from "zod";
import { requireUser } from "@/lib/auth-server";
import { updateTag } from "@/lib/utils/cache-utils";
import { db } from "@/lib/prisma";

const createQuizSchema = z.object({
  title: z.string().min(1),
  description: z.string().optional(),
});

export async function createQuizAction(data: unknown) {
  // 1. Authenticate
  const user = await requireUser();

  // 2. Validate input
  const parsed = createQuizSchema.parse(data);

  // 3. Perform operation
  const quiz = await db.quiz.create({
    data: {
      ...parsed,
      userId: user.id,
    },
  });

  // 4. Invalidate cache
  updateTag("quizzes");

  // 5. Return result
  return { success: true, data: quiz };
}
```

### Using Server Actions in Components

```typescript
// components/quiz/create-quiz-form.tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { createQuizAction } from "@/lib/actions/quizzes";
import { Field } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export function CreateQuizForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(createQuizSchema),
  });

  const onSubmit = async (data) => {
    const result = await createQuizAction(data);
    if (result.success) {
      // Handle success
      router.push(`/dashboard/quizzes/${result.data.id}`);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Field label="Title" error={errors.title?.message}>
        <Input {...register("title")} />
      </Field>
      <Button type="submit">Create Quiz</Button>
    </form>
  );
}
```

### Progressive Enhancement with useActionState

```typescript
// lib/actions/quizzes.ts
"use server";

export async function createQuizAction(prevState: any, formData: FormData) {
  const title = formData.get("title") as string;

  if (!title) {
    return { error: "Title is required" };
  }

  const quiz = await db.quiz.create({ data: { title } });
  revalidatePath("/dashboard/quizzes");

  return { success: true, quiz };
}

// Component
("use client");
import { useActionState } from "react";

export function CreateQuizForm() {
  const [state, formAction] = useActionState(createQuizAction, null);

  return (
    <form action={formAction}>
      <input name="title" required />
      {state?.error && <p className="text-destructive">{state.error}</p>}
      <button type="submit">Create Quiz</button>
    </form>
  );
}
```

### Error Handling in Server Actions

```typescript
"use server";

export async function deleteQuizAction(quizId: string) {
  try {
    const user = await requireUser();

    const quiz = await db.quiz.findUnique({ where: { id: quizId } });
    if (!quiz) {
      return { success: false, error: "Quiz not found" };
    }

    await db.quiz.delete({ where: { id: quizId } });
    updateTag("quizzes");

    return { success: true };
  } catch (error) {
    console.error("Delete quiz error:", error);
    return {
      success: false,
      error: "Failed to delete quiz",
    };
  }
}
```

## Server Components

### Purpose

Utilize server components for secure data access, reduced JavaScript bundles, and better performance.

### Best Practices

1. **Default to Server Components**

   - Use async server components for data fetching
   - Avoid unnecessary client component wrappers
   - Client components only for interactivity

2. **Data Fetching Location**

   - Fetch data only in server components
   - Pass fetched data as props to client components
   - Never expose sensitive API keys to client

3. **Suspense Boundaries**
   - Wrap data-fetching components in Suspense
   - Provide appropriate fallback UI (skeletons)
   - Enable streaming and progressive rendering

### Implementation Pattern

```typescript
// Server component with data fetching
import { Suspense } from "react";
import { getUser } from "@/lib/data/users";
import { UserProfile } from "@/components/user-profile";
import { ProfileSkeleton } from "@/components/skeletons";

export default async function ProfilePage() {
  return (
    <div>
      <Suspense fallback={<ProfileSkeleton />}>
        <UserProfileContent />
      </Suspense>
    </div>
  );
}

async function UserProfileContent() {
  const user = await getUser();
  return <UserProfile user={user} />;
}
```

### Runtime APIs with Suspense

Wrap runtime APIs (cookies, headers) in Suspense:

```typescript
import { cookies } from "next/headers";

export default function Layout({ children }) {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <CookieConsumer>{children}</CookieConsumer>
    </Suspense>
  );
}

async function CookieConsumer({ children }) {
  const cookieStore = await cookies();
  const theme = cookieStore.get("theme");
  return <div className={theme?.value}>{children}</div>;
}
```

## Error Handling

### Purpose

Provide robust error boundaries and fallback UI for better user experience and easier debugging.

### Error Boundaries

1. **error.tsx Files**
   - Create segment-specific error boundaries
   - Wrap server-side errors gracefully
   - Provide recovery options to users

```typescript
// app/dashboard/error.tsx
"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      <h1>Something went wrong</h1>
      <p className="text-muted-foreground">{error.message}</p>
      <button onClick={() => reset()} className="btn-primary">
        Try again
      </button>
    </div>
  );
}
```

2. **not-found.tsx**
   - Handle 404 scenarios
   - Provide navigation back to main content
   - Improve UX for missing resources

```typescript
// app/dashboard/[id]/not-found.tsx
export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1>Quiz not found</h1>
      <Link href="/dashboard/quizzes">Back to quizzes</Link>
    </div>
  );
}
```

### Async Error Handling

```typescript
"use server";

export async function createQuiz(data: QuizInput) {
  try {
    const result = await aiService.generateQuiz(data);
    if (!result.success) {
      throw new Error(result.error);
    }
    return { success: true, data: result };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}
```

### Recommended Patterns

- Validate all inputs with Zod before processing
- Return structured error responses from server actions
- Use error boundaries for UI recovery
- Log errors for monitoring and debugging
- Provide user-friendly error messages
- Avoid exposing sensitive error details to clients

## Development Checklist

When building Next.js 16 features:

- [ ] Use server actions for all mutations instead of API routes
- [ ] Use server components by default
- [ ] Implement cache components with `'use cache'` and `cacheLife()`
- [ ] Add Suspense boundaries for streaming content
- [ ] Wrap runtime APIs in Suspense
- [ ] Create error.tsx and not-found.tsx for error handling
- [ ] Validate inputs with Zod schemas in server actions
- [ ] Call `updateTag()` or `revalidatePath()` after mutations
- [ ] Test cache invalidation after mutations
- [ ] Minimize client-side JavaScript
- [ ] Only create API routes for webhooks or external integrations

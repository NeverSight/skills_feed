---
name: nextjs-server-actions
description: "Guide for implementing Next.js server actions using ZSA (Zod Server Actions) with authentication, validation, and React Query integration. Use when creating API endpoints, form handlers, mutations, or any server-side data operations. Best practices for building type-safe Next.js server actions with ZSA (Zod Server Actions). Use this skill when creating validated server actions, implementing authentication/authorization procedures, handling form submissions, integrating with React Query, managing errors, or building secure API-like endpoints in Next.js App Router. Covers input/output validation, procedures (middleware), callbacks, optimistic updates, retries, timeouts, and client-side hooks."
---

# Next.js with ZSA Server Actions

Build type-safe, validated server actions in Next.js with Zod.

## Installation

```bash
npm install zsa zsa-react zod
# Optional: for React Query integration
npm install zsa-react-query @tanstack/react-query
```

## Basic Server Action

```typescript
// actions/user.ts
"use server";

import { createServerAction } from "zsa";
import z from "zod";

export const createUserAction = createServerAction()
  .input(
    z.object({
      email: z.string().email(),
      name: z.string().min(2),
    })
  )
  .handler(async ({ input }) => {
    // Input is fully typed and validated
    const user = await db.user.create({
      data: { email: input.email, name: input.name },
    });
    return user;
  });
```

## Calling Server Actions

### From Server (no try/catch needed)

```typescript
const [data, err] = await createUserAction({ email: "john@example.com", name: "John Doe" });
if (err) console.error(err.code, err.message);
```

### From Client with useServerAction

```typescript
"use client";

import { useServerAction } from "zsa-react";
import { createUserAction } from "./actions/user";

export function CreateUserForm() {
  const { isPending, execute, data, error, isError, isSuccess, reset } =
    useServerAction(createUserAction);

  const handleSubmit = async (formData: FormData) => {
    const [data, err] = await execute({
      email: formData.get("email") as string,
      name: formData.get("name") as string,
    });

    if (err) {
      // Error handling
      return;
    }
    
    // Success handling
  };

  return (
    <form action={handleSubmit}>
      <input name="email" type="email" disabled={isPending} />
      <input name="name" type="text" disabled={isPending} />
      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create User"}
      </button>
      {isError && <p className="error">{error.message}</p>}
      {isSuccess && <p className="success">User created: {data.name}</p>}
    </form>
  );
}
```

## Input & Output Validation

```typescript
"use server";

import { createServerAction } from "zsa";
import z from "zod";

// Input schema
const createPostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10),
  published: z.boolean().default(false),
  tags: z.array(z.string()).optional(),
});

// Output schema
const postOutputSchema = z.object({
  id: z.string(),
  title: z.string(),
  createdAt: z.date(),
});

export const createPostAction = createServerAction()
  .input(createPostSchema)
  .output(postOutputSchema) // Validates return value
  .handler(async ({ input }) => {
    const post = await db.post.create({ data: input });
    return {
      id: post.id,
      title: post.title,
      createdAt: post.createdAt,
    };
  });
```

## FormData Input

```typescript
"use server";
export const submitContactForm = createServerAction()
  .input(z.object({ name: z.string().min(2), email: z.string().email() }), 
    { type: "formData" })
  .handler(async ({ input }) => {
    await sendEmail(input);
    return { success: true };
  });
```

## Procedures (Authentication & Authorization)

Create reusable middleware for auth, roles, and permissions:

```typescript
// lib/procedures.ts
"use server";

// Authentication procedure
export const authedProcedure = createServerActionProcedure().handler(async () => {
  const session = await auth();
  if (!session?.user) throw new Error("Not authenticated");
  return { user: { id: session.user.id, email: session.user.email, role: session.user.role } };
});

// Admin procedure (chains from authedProcedure)
export const adminProcedure = createServerActionProcedure(authedProcedure)
  .handler(async ({ ctx }) => {
    if (ctx.user.role !== "admin") throw new Error("Admin access required");
    return ctx;
  });
```

**Usage:**
```typescript
// Protected action
export const createPost = authedProcedure
  .createServerAction()
  .input(z.object({ title: z.string() }))
  .handler(async ({ input, ctx }) => {
    return db.post.create({ data: { ...input, authorId: ctx.user.id } });
  });

// Public action (no procedure)
export const publicAction = createServerAction()
  .input(schema)
  .handler(async ({ input }) => { /* ... */ });
```

## Callbacks

```typescript
"use server";

import { createServerAction } from "zsa";
import z from "zod";

export const createOrderAction = createServerAction()
  .input(z.object({ productId: z.string(), quantity: z.number() }))
  .onStart(async () => {
    console.log("Order creation started");
  })
  .onSuccess(async ({ input, data }) => {
    // Send confirmation email
    await sendOrderConfirmation(data.id);
  })
  .onError(async ({ err }) => {
    // Log error to monitoring service
    await logError(err);
  })
  .onComplete(async () => {
    console.log("Order action completed");
  })
  .handler(async ({ input }) => {
    return db.order.create({ data: input });
  });
```

## Error Handling

**Error Codes:** `INPUT_PARSE_ERROR`, `OUTPUT_PARSE_ERROR`, `ERROR`, `NOT_AUTHORIZED`, `TIMEOUT`, `INTERNAL_SERVER_ERROR`

```typescript
const [result, err] = await execute({ /* ... */ });

if (err) {
  switch (err.code) {
    case "INPUT_PARSE_ERROR":
      console.log(err.fieldErrors); // { email: ["Invalid email"] }
      break;
    case "NOT_AUTHORIZED":
      router.push("/login");
      break;
    default:
      toast.error(err.message);
  }
  return;
}

// Success - use result
```

**Server-side:**
```typescript
.handler(async ({ input, ctx }) => {
  const result = await Service.create(ctx.userId, input);
  if (!result.success) throw new Error(result.error);
  return result.data;
})
```

## useServerAction Options

```typescript
const {
  data,
  isPending,
  isOptimistic,
  isError,
  error,
  isSuccess,
  status, // "idle" | "pending" | "success" | "error"
  execute,
  executeFormAction,
  setOptimistic,
  reset,
} = useServerAction(myAction, {
  // Callbacks
  onStart: () => console.log("Started"),
  onSuccess: ({ data }) => toast.success("Success!"),
  onError: ({ err }) => toast.error(err.message),
  onFinish: ([data, err]) => console.log("Finished"),
  
  // Initial data
  initialData: { count: 0 },
  
  // Retry configuration
  retry: {
    maxAttempts: 3,
    delay: 1000, // or (attempt, err) => attempt * 1000
  },
  
  // Persist states while pending
  persistErrorWhilePending: false,
  persistDataWhilePending: false,
});
```

## Optimistic Updates

```typescript
"use client";

import { useServerAction } from "zsa-react";
import { toggleLikeAction } from "./actions";

export function LikeButton({ postId, initialLikes }: Props) {
  const { execute, data, isOptimistic, setOptimistic } = useServerAction(
    toggleLikeAction,
    { initialData: { liked: false, count: initialLikes } }
  );

  const handleClick = async () => {
    // Optimistically update UI
    setOptimistic((current) => ({
      liked: !current.liked,
      count: current.liked ? current.count - 1 : current.count + 1,
    }));

    // Execute actual action (will rollback on error)
    await execute({ postId });
  };

  return (
    <button onClick={handleClick} className={isOptimistic ? "opacity-50" : ""}>
      {data.liked ? "❤️" : "🤍"} {data.count}
    </button>
  );
}
```

## Timeouts & Retries

```typescript
"use server";

import { createServerAction } from "zsa";
import z from "zod";

export const slowAction = createServerAction()
  .input(z.object({ data: z.string() }))
  .timeout(5000) // 5 second timeout
  .retry({
    maxAttempts: 3,
    delay: (attempt) => attempt * 1000, // Exponential backoff
  })
  .handler(async ({ input }) => {
    // Long-running operation
    return processData(input.data);
  });
```

## Best Practices

1. **Create procedures first, reuse across actions** - don't create new procedures per action
2. **Throw descriptive errors** - `throw new Error("Email already exists")` for client display
3. **Name destructured results** - `const [categories, err] = await getCategoriesAction()`
4. **Call Service layer, NOT DAL directly** - keep actions thin
5. **Always validate input** with Zod schemas
6. **Use `revalidatePath`/`revalidateTag`** after mutations
7. **Keep actions thin** - business logic belongs in services


## File Structure

```
features/<feature>/usecases/
├── create/actions/create-<entity>-action.ts
├── update/actions/update-<entity>-action.ts
├── delete/actions/delete-<entity>-action.ts
└── list/actions/list-<entity>-action.ts
```

## Action Pattern

```typescript
// create-account-action.ts
'use server'

import 'server-only'
import { revalidatePath } from 'next/cache'
import { authedProcedure } from '@saas4dev/auth'
import { CreateAccountSchema, AccountSchema } from '@/features/accounts/model/account-schemas'
import { AccountService } from '@/features/accounts/account-service'

export const createAccountAction = authedProcedure
  .createServerAction()
  .input(CreateAccountSchema, { type: 'formData' })
  .output(AccountSchema)
  .onComplete(async () => {
    revalidatePath('/accounts')
  })
  .handler(async ({ input, ctx }) => {
    const result = await AccountService.create(ctx.userId, input)
    if (!result.success) {
      throw new Error(result.error)
    }
    return result.data
  })
```

## Required Directives

Every action file MUST include:
```typescript
'use server'           // First line - marks as server action
import 'server-only'   // Prevents client import
```

## React Query Integration

```typescript
'use client'
import { useServerActionMutation, useServerActionQuery } from '@saas4dev/core'

// Mutations (create, update, delete)
const mutation = useServerActionMutation(createAction, {
  onSuccess: () => toast.success('Created'),
  onError: (error) => toast.error(error.message),
})

// Usage in forms
const form = useForm<Input>({ resolver: zodResolver(Schema) })
const onSubmit = (data: Input) => mutation.mutate(data)

// Queries (read, list)
const { data, isLoading } = useServerActionQuery(listAction, { input: { userId } })
```


## Reference Files

- **`references/procedures.md`**: Advanced procedure patterns, chaining, context
- **`references/react-query.md`**: TanStack Query integration with ZSA
- **`references/forms.md`**: Form handling, validation, file uploads
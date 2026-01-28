---
name: server-actions
description: Create or update Next.js server actions for blog and analytics functionality. Use when adding form handlers, data mutations, or server-side logic in the web app.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Server Actions Skill

This skill helps you work with Next.js server actions in `apps/web/src/actions/`.

## When to Use This Skill

- Creating form submission handlers
- Implementing data mutations (create, update, delete)
- Server-side validation and processing
- Database operations from the client
- File uploads and processing
- Revalidating cached data

## Server Actions Overview

Server Actions are asynchronous functions that run on the server but can be called from client or server components.

```
apps/web/src/actions/
├── blog.ts              # Blog post actions
├── analytics.ts         # Analytics tracking actions
└── revalidate.ts        # Cache revalidation actions
```

## Key Patterns

### 1. Basic Server Action

```typescript
// app/actions/blog.ts
"use server";

import { db } from "@sgcarstrends/database";
import { posts } from "@sgcarstrends/database/schema";
import { revalidatePath } from "next/cache";

export async function createBlogPost(formData: FormData) {
  const title = formData.get("title") as string;
  const content = formData.get("content") as string;

  // Server-side validation
  if (!title || !content) {
    return { error: "Title and content are required" };
  }

  // Database operation
  const [post] = await db
    .insert(posts)
    .values({
      title,
      content,
      publishedAt: new Date(),
    })
    .returning();

  // Revalidate the blog page
  revalidatePath("/blog");

  return { success: true, post };
}
```

### 2. Form Integration

**With useFormState (Client Component):**

```typescript
"use client";

import { useFormState, useFormStatus } from "react-dom";
import { createBlogPost } from "@/actions/blog";

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button disabled={pending}>
      {pending ? "Creating..." : "Create Post"}
    </button>
  );
}

export default function CreatePostForm() {
  const [state, formAction] = useFormState(createBlogPost, null);

  return (
    <form action={formAction}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      {state?.error && <p className="error">{state.error}</p>}
      <SubmitButton />
    </form>
  );
}
```

**Progressive Enhancement (Server Component):**

```typescript
// app/blog/create/page.tsx
import { createBlogPost } from "@/actions/blog";

export default function CreatePost() {
  return (
    <form action={createBlogPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

### 3. Input Validation with Zod

```typescript
"use server";

import { z } from "zod";

const blogPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
  tags: z.array(z.string()).optional(),
  published: z.boolean().default(false),
});

export async function createBlogPost(formData: FormData) {
  // Parse and validate
  const rawData = {
    title: formData.get("title"),
    content: formData.get("content"),
    tags: formData.getAll("tags"),
    published: formData.get("published") === "true",
  };

  const result = blogPostSchema.safeParse(rawData);

  if (!result.success) {
    return {
      error: "Validation failed",
      issues: result.error.issues,
    };
  }

  // Use validated data
  const validData = result.data;
  await db.insert(posts).values(validData);

  return { success: true };
}
```

### 4. Type-Safe Server Actions

Use typed parameters instead of FormData:

```typescript
"use server";

import { z } from "zod";

const updatePostSchema = z.object({
  id: z.string(),
  title: z.string().min(1),
  content: z.string().min(10),
});

type UpdatePostInput = z.infer<typeof updatePostSchema>;

export async function updateBlogPost(input: UpdatePostInput) {
  // Validate input
  const validData = updatePostSchema.parse(input);

  // Update database
  await db
    .update(posts)
    .set({
      title: validData.title,
      content: validData.content,
      updatedAt: new Date(),
    })
    .where(eq(posts.id, validData.id));

  revalidatePath(`/blog/${validData.id}`);
  return { success: true };
}

// Client usage with type safety
// const result = await updateBlogPost({ id: "1", title: "New Title", content: "Content" });
```

### 5. Authentication in Server Actions

```typescript
"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

async function getUser() {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token");

  if (!token) {
    redirect("/login");
  }

  // Verify token and get user
  const user = await verifyToken(token.value);
  return user;
}

export async function deleteBlogPost(postId: string) {
  const user = await getUser();

  // Check authorization
  const post = await db.query.posts.findFirst({
    where: eq(posts.id, postId),
  });

  if (post?.authorId !== user.id) {
    return { error: "Unauthorized" };
  }

  // Delete post
  await db.delete(posts).where(eq(posts.id, postId));
  revalidatePath("/blog");

  return { success: true };
}
```

### 6. File Upload Actions

```typescript
"use server";

import { put } from "@vercel/blob";

export async function uploadImage(formData: FormData) {
  const file = formData.get("image") as File;

  if (!file) {
    return { error: "No file provided" };
  }

  // Validate file type
  if (!file.type.startsWith("image/")) {
    return { error: "File must be an image" };
  }

  // Validate file size (5MB max)
  if (file.size > 5 * 1024 * 1024) {
    return { error: "File size must be less than 5MB" };
  }

  // Upload to Vercel Blob
  const blob = await put(file.name, file, {
    access: "public",
  });

  return { success: true, url: blob.url };
}
```

## Common Tasks

### Creating Analytics Action

```typescript
// app/actions/analytics.ts
"use server";

import { db } from "@sgcarstrends/database";
import { analyticsTable } from "@sgcarstrends/database/schema";

export async function trackPageView(path: string) {
  try {
    await db.insert(analyticsTable).values({
      event: "page_view",
      path,
      timestamp: new Date(),
    });

    return { success: true };
  } catch (error) {
    console.error("Analytics tracking failed:", error);
    return { success: false };
  }
}

// Client usage
"use client";
import { useEffect } from "react";
import { usePathname } from "next/navigation";
import { trackPageView } from "@/actions/analytics";

export function Analytics() {
  const pathname = usePathname();

  useEffect(() => {
    trackPageView(pathname);
  }, [pathname]);

  return null;
}
```

### Cache Revalidation Actions

```typescript
// app/actions/revalidate.ts
"use server";

import { revalidatePath, revalidateTag } from "next/cache";

export async function revalidateBlogPosts() {
  revalidatePath("/blog");
  revalidateTag("blog-posts");
  return { success: true };
}

export async function revalidateCarData() {
  revalidatePath("/data");
  revalidateTag("car-data");
  return { success: true };
}

// Client usage
"use client";
import { revalidateBlogPosts } from "@/actions/revalidate";

export function RefreshButton() {
  return (
    <button onClick={() => revalidateBlogPosts()}>
      Refresh Blog Posts
    </button>
  );
}
```

### Optimistic Updates

```typescript
"use client";

import { useOptimistic } from "react";
import { updatePostLikes } from "@/actions/blog";

export function LikeButton({ postId, initialLikes }: Props) {
  const [optimisticLikes, setOptimisticLikes] = useOptimistic(
    initialLikes,
    (state, newLikes: number) => newLikes
  );

  async function handleLike() {
    // Update UI immediately
    setOptimisticLikes(optimisticLikes + 1);

    // Update server
    await updatePostLikes(postId, optimisticLikes + 1);
  }

  return (
    <button onClick={handleLike}>
      ❤️ {optimisticLikes}
    </button>
  );
}
```

## Error Handling

### Graceful Error Handling

```typescript
"use server";

export async function createBlogPost(input: BlogPostInput) {
  try {
    // Validate
    const validData = blogPostSchema.parse(input);

    // Database operation
    const [post] = await db
      .insert(posts)
      .values(validData)
      .returning();

    revalidatePath("/blog");
    return { success: true, data: post };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        error: "Validation failed",
        issues: error.issues,
      };
    }

    if (error instanceof DatabaseError) {
      return {
        success: false,
        error: "Database error occurred",
      };
    }

    console.error("Unexpected error:", error);
    return {
      success: false,
      error: "An unexpected error occurred",
    };
  }
}
```

### Client-Side Error Display

```typescript
"use client";

import { useFormState } from "react-dom";
import { createBlogPost } from "@/actions/blog";

export default function CreatePostForm() {
  const [state, formAction] = useFormState(createBlogPost, null);

  return (
    <form action={formAction}>
      {/* Form fields */}

      {state?.error && (
        <div className="error">
          <p>{state.error}</p>
          {state.issues && (
            <ul>
              {state.issues.map((issue, i) => (
                <li key={i}>{issue.message}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      <button type="submit">Submit</button>
    </form>
  );
}
```

## Testing Server Actions

```typescript
// __tests__/actions/blog.test.ts
import { describe, it, expect, vi } from "vitest";
import { createBlogPost } from "@/actions/blog";

vi.mock("@sgcarstrends/database", () => ({
  db: {
    insert: vi.fn().mockReturnValue({
      values: vi.fn().mockReturnValue({
        returning: vi.fn().mockResolvedValue([{ id: "1", title: "Test" }]),
      }),
    }),
  },
}));

describe("createBlogPost", () => {
  it("creates a blog post successfully", async () => {
    const formData = new FormData();
    formData.set("title", "Test Post");
    formData.set("content", "Test content");

    const result = await createBlogPost(formData);

    expect(result.success).toBe(true);
    expect(result.post).toBeDefined();
  });

  it("returns error for missing title", async () => {
    const formData = new FormData();
    formData.set("content", "Test content");

    const result = await createBlogPost(formData);

    expect(result.error).toBeDefined();
  });
});
```

Run tests:
```bash
pnpm -F @sgcarstrends/web test -- src/actions
```

## Security Best Practices

### 1. Always Validate Input

```typescript
"use server";

export async function updateProfile(formData: FormData) {
  // ❌ Never trust client input directly
  // const data = Object.fromEntries(formData);

  // ✅ Always validate
  const schema = z.object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
  });

  const result = schema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
  });

  if (!result.success) {
    return { error: "Invalid input" };
  }

  // Use validated data
  await updateUser(result.data);
}
```

### 2. Implement Rate Limiting

```typescript
"use server";

import { Ratelimit } from "@upstash/ratelimit";
import { redis } from "@sgcarstrends/utils/redis";

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(5, "10 s"),
});

export async function sendContactForm(formData: FormData) {
  const ip = headers().get("x-forwarded-for") ?? "unknown";
  const { success } = await ratelimit.limit(ip);

  if (!success) {
    return { error: "Rate limit exceeded" };
  }

  // Process form...
}
```

### 3. Sanitize Input

```typescript
"use server";

import sanitizeHtml from "sanitize-html";

export async function createBlogPost(formData: FormData) {
  const content = formData.get("content") as string;

  // Sanitize HTML content
  const cleanContent = sanitizeHtml(content, {
    allowedTags: ["b", "i", "em", "strong", "a", "p"],
    allowedAttributes: {
      a: ["href"],
    },
  });

  await db.insert(posts).values({ content: cleanContent });
}
```

## Performance Tips

1. **Keep actions lightweight**: Move heavy logic to background jobs
2. **Use revalidatePath sparingly**: Only revalidate what changed
3. **Batch operations**: Combine multiple database queries
4. **Cache expensive operations**: Use memoization for repeated calls

## References

- Next.js Server Actions: Use nextjs_docs MCP tool
- Related files:
  - `apps/web/src/actions/` - All server actions
  - `apps/web/src/app/` - Page components using actions
  - `apps/web/CLAUDE.md` - Web app documentation

## Best Practices

1. **"use server" directive**: Always at top of action file
2. **Type safety**: Use Zod for validation and type inference
3. **Error handling**: Return structured error objects
4. **Security**: Validate, authenticate, authorize
5. **Revalidation**: Update cache after mutations
6. **Testing**: Write tests for all server actions
7. **Naming**: Use descriptive action names (createPost, updateProfile)
8. **Logging**: Log errors and important operations

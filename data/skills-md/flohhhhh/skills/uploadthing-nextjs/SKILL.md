---
name: uploadthing-nextjs
description: Type-safe file upload integration for Next.js App Router using UploadThing. Use when implementing secure file uploads with client-to-storage direct uploads, authentication middleware, upload completion handlers, and automatic database metadata storage.
---

# UploadThing Integration (Next.js)

UploadThing provides a **type-safe, direct-to-storage file upload system** designed for modern TypeScript web apps.

---

## When To Use

Use UploadThing when your application needs:

- Secure user file uploads
- Type-safe upload workflows
- Per-feature upload permissions and validation
- React/Next.js-friendly upload components
- Storage abstraction without building a custom upload pipeline

---

## When NOT To Use

Avoid or reconsider if:

- You need deep, multi-stage processing pipelines before storage
- You require full control over streaming binary data server-side
- Your architecture requires storage provider APIs as the primary data source instead of your database

---

## Core Concepts

### File Router

Defines all upload routes for the application.

Each route defines:

- Allowed file types
- File limits and size rules
- Authentication checks
- Metadata handling
- Post-upload processing

---

### File Route

Represents a single upload use-case.

Examples:

- User avatar uploads
- Vehicle listing images
- Message attachments
- Document uploads

---

### Middleware

Runs before upload begins.

Used for:

- Authentication
- Authorization
- Metadata tagging
- Rejecting invalid uploads

---

### Upload Completion Handler

Runs after a file successfully uploads.

Used for:

- Saving metadata to database
- Linking files to domain entities
- Triggering async processing
- Sending notifications

---

### UTApi

Server-side UploadThing SDK.

Used for:

- Uploading files programmatically
- Deleting files
- Listing files (admin/debug only)
- Generating signed URLs for private file access

---

## Installation

```bash
npm install uploadthing @uploadthing/react
```

---

## Environment Variables

```bash
# .env
UPLOADTHING_SECRET=sk_live_...
UPLOADTHING_APP_ID=your_app_id
```

---

## Suggested File Structure

```
app/
  api/
    uploadthing/
      core.ts        # File router definition
      route.ts       # API route handlers
src/
  utils/
    uploadthing.ts   # Typed components
  components/
    upload-button.tsx
.env                 # UploadThing credentials
```

---

## File Router

**Location:** `app/api/uploadthing/core.ts`

```typescript
import { createUploadthing, type FileRouter } from "uploadthing/next";
import { auth } from "@/lib/auth";

const f = createUploadthing();

export const uploadRouter = {
  imageUploader: f({ image: { maxFileSize: "4MB", maxFileCount: 1 } })
    .middleware(async ({ req }) => {
      const user = await auth();
      if (!user) throw new Error("Unauthorized");
      return { userId: user.id };
    })
    .onUploadComplete(async ({ metadata, file }) => {
      console.log("Upload complete for userId:", metadata.userId);
      console.log("File URL:", file.url);
      // Save to database here
      return { uploadedBy: metadata.userId };
    }),
} satisfies FileRouter;

export type OurFileRouter = typeof uploadRouter;
```

---

## Route Handler

**Location:** `app/api/uploadthing/route.ts`

```typescript
import { createRouteHandler } from "uploadthing/next";
import { uploadRouter } from "./core";

export const { GET, POST } = createRouteHandler({
  router: uploadRouter,
});
```

---

## Typed Upload Components

**Location:** `src/utils/uploadthing.ts`

```typescript
import {
  generateUploadButton,
  generateUploadDropzone,
} from "@uploadthing/react";
import type { OurFileRouter } from "@/app/api/uploadthing/core";

export const UploadButton = generateUploadButton<OurFileRouter>();
export const UploadDropzone = generateUploadDropzone<OurFileRouter>();
```

---

## Using Upload Components

```typescript
"use client";

import { UploadButton } from "@/utils/uploadthing";

export function MyUploadButton() {
  return (
    <UploadButton
      endpoint="imageUploader"
      onClientUploadComplete={(res) => {
        console.log("Files: ", res);
        alert("Upload Completed");
      }}
      onUploadError={(error: Error) => {
        alert(`ERROR! ${error.message}`);
      }}
    />
  );
}
```

---

## Tailwind Integration (Optional)

```typescript
import { withUt } from "uploadthing/tw";

export default withUt({
  // your tailwind config
  content: ["./src/**/*.{ts,tsx}"],
  theme: { extend: {} },
  plugins: [],
});
```

---

## Optional — SSR Upload Config Optimization

```typescript
// next.config.js
import { withUT } from "uploadthing/nextjs";

export default withUT({
  // your Next.js config
});
```

---

## Database Integration Pattern

After upload completes, the application should:

1. Store UploadThing file identifier
2. Store public or signed file URL
3. Store ownership metadata
4. Link file to domain entity (post, profile, asset, etc.)

```typescript
.onUploadComplete(async ({ metadata, file }) => {
  await db.insert(uploads).values({
    userId: metadata.userId,
    fileKey: file.key,
    fileUrl: file.url,
    fileName: file.name,
    fileSize: file.size,
  });
  
  return { success: true };
})
```

---

## Upload Strategies

### Client Uploads (Recommended)

Process:

1. Client requests upload authorization
2. Server returns presigned upload URL
3. Client uploads directly to storage
4. Upload completion handler runs server logic

---

### Server Uploads (UTApi)

Used when:

- Uploading files from server jobs
- Migrating files
- Handling admin tools
- Accepting files through server actions

```typescript
import { UTApi } from "uploadthing/server";

const utapi = new UTApi();

export async function uploadFromServer(file: File) {
  const response = await utapi.uploadFiles(file);
  return response.data;
}
```

---

## Private File Access Pattern

Private files should be accessed via signed URLs.

```typescript
import { UTApi } from "uploadthing/server";

const utapi = new UTApi();

export async function getPrivateFileUrl(fileKey: string) {
  const url = await utapi.getSignedURL(fileKey, { expiresIn: "1h" });
  return url;
}
```

---

## Security Best Practices

- Always authenticate inside upload middleware
- Store ownership and file metadata in database
- Create multiple specialized upload routes
- Avoid global “upload everything” routes
- Validate domain associations during upload completion

---

## Operational Best Practices

- Log file key and storage URL
- Make database writes idempotent
- Prefer storing metadata locally instead of querying storage provider
- Restrict file sizes and counts per route
- Separate public and private upload routes

---

## Common Mistakes

- Using untyped UploadThing components
- Forgetting client component directives
- Skipping database metadata storage
- Allowing overly permissive upload routes
- Relying on storage provider APIs as primary data source

---

## Summary

**UploadThing** manages file uploads and storage.

**Next.js** provides routing and integration surfaces.

Keep upload rules in the file router. Keep authorization in middleware. Keep file metadata in your database.

---

## References

- https://docs.uploadthing.com/
- https://docs.uploadthing.com/getting-started
- https://docs.uploadthing.com/file-routes
- https://docs.uploadthing.com/api-reference

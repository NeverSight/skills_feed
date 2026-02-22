---
name: convex-file-storage
description: File uploads, storage, and serving in Convex. Use when implementing file uploads, generating upload URLs, serving files, managing file metadata, or building file-based features like avatars, attachments, or media galleries.
---

# Convex File Storage

## Upload Flow

### 1. Generate Upload URL (Mutation)

```typescript
// convex/files.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const generateUploadUrl = mutation({
  args: {},
  returns: v.string(),
  handler: async (ctx) => {
    return await ctx.storage.generateUploadUrl();
  },
});
```

### 2. Client Upload

```typescript
// Client-side upload
async function uploadFile(file: File) {
  // Get upload URL from Convex
  const uploadUrl = await generateUploadUrl();

  // Upload file directly to Convex storage
  const response = await fetch(uploadUrl, {
    method: "POST",
    headers: { "Content-Type": file.type },
    body: file,
  });

  const { storageId } = await response.json();
  return storageId;
}
```

### 3. Store File Reference (Mutation)

```typescript
export const saveFile = mutation({
  args: {
    storageId: v.id("_storage"),
    fileName: v.string(),
    fileType: v.string(),
  },
  returns: v.id("files"),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) {
      throw new ConvexError({ code: "UNAUTHENTICATED", message: "Not logged in" });
    }

    return await ctx.db.insert("files", {
      storageId: args.storageId,
      fileName: args.fileName,
      fileType: args.fileType,
      uploadedBy: identity.subject,
      uploadedAt: Date.now(),
    });
  },
});
```

## Serving Files

### Get File URL (Query)

```typescript
export const getFileUrl = query({
  args: { storageId: v.id("_storage") },
  returns: v.union(v.string(), v.null()),
  handler: async (ctx, args) => {
    return await ctx.storage.getUrl(args.storageId);
  },
});
```

### Serve with Metadata

```typescript
export const getFile = query({
  args: { fileId: v.id("files") },
  returns: v.union(
    v.object({
      _id: v.id("files"),
      url: v.union(v.string(), v.null()),
      fileName: v.string(),
      fileType: v.string(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    const file = await ctx.db.get(args.fileId);
    if (!file) return null;

    const url = await ctx.storage.getUrl(file.storageId);
    return {
      _id: file._id,
      url,
      fileName: file.fileName,
      fileType: file.fileType,
    };
  },
});
```

## Delete Files

```typescript
export const deleteFile = mutation({
  args: { fileId: v.id("files") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const file = await ctx.db.get(args.fileId);
    if (!file) {
      throw new ConvexError({ code: "NOT_FOUND", message: "File not found" });
    }

    // Delete from storage
    await ctx.storage.delete(file.storageId);

    // Delete metadata
    await ctx.db.delete(args.fileId);
    return null;
  },
});
```

## Schema Definition

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  files: defineTable({
    storageId: v.id("_storage"),
    fileName: v.string(),
    fileType: v.string(),
    fileSize: v.optional(v.number()),
    uploadedBy: v.string(),
    uploadedAt: v.number(),
  })
    .index("by_uploader", ["uploadedBy"])
    .index("by_type", ["fileType"]),
});
```

## Image Handling

### With Dimensions

```typescript
export const saveImage = mutation({
  args: {
    storageId: v.id("_storage"),
    width: v.number(),
    height: v.number(),
  },
  returns: v.id("images"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("images", {
      storageId: args.storageId,
      width: args.width,
      height: args.height,
      createdAt: Date.now(),
    });
  },
});
```

### Client-Side with Preview

```typescript
// React component example
function ImageUpload({ onUpload }: { onUpload: (id: string) => void }) {
  const generateUploadUrl = useMutation(api.files.generateUploadUrl);
  const saveImage = useMutation(api.files.saveImage);
  const [preview, setPreview] = useState<string | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Show preview
    setPreview(URL.createObjectURL(file));

    // Get dimensions
    const img = new Image();
    img.src = URL.createObjectURL(file);
    await new Promise((resolve) => (img.onload = resolve));

    // Upload
    const uploadUrl = await generateUploadUrl();
    const response = await fetch(uploadUrl, {
      method: "POST",
      headers: { "Content-Type": file.type },
      body: file,
    });
    const { storageId } = await response.json();

    // Save with dimensions
    const imageId = await saveImage({
      storageId,
      width: img.naturalWidth,
      height: img.naturalHeight,
    });

    onUpload(imageId);
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {preview && <img src={preview} alt="Preview" />}
    </div>
  );
}
```

## HTTP File Serving

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

http.route({
  path: "/files/{storageId}",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const storageId = url.pathname.split("/").pop();

    if (!storageId) {
      return new Response("Missing storageId", { status: 400 });
    }

    const blob = await ctx.storage.get(storageId as Id<"_storage">);
    if (!blob) {
      return new Response("File not found", { status: 404 });
    }

    return new Response(blob);
  }),
});

export default http;
```

## File Size Limits

- Default max file size: 20MB
- For larger files, use chunked uploads or external storage

## Common Pitfalls

- **Forgetting to delete storage** - Always delete both metadata and storage blob
- **Not validating file types** - Validate on client and server
- **Exposing all files** - Add ownership checks before serving
- **Missing error handling** - Handle upload failures gracefully

## References

- File Storage: https://docs.convex.dev/file-storage
- HTTP Actions: https://docs.convex.dev/functions/http-actions

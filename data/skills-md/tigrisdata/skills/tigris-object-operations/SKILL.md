---
name: tigris-object-operations
description: Use when working with objects in Tigris Storage - uploading, downloading, deleting, listing, getting metadata, or generating presigned URLs
---

# Tigris Object Operations

## Overview

Tigris Storage provides object operations: upload (put), download (get), delete (remove), list, metadata (head), and presigned URLs.

All methods return `TigrisStorageResponse<T, E>` - check `error` property first.

## Quick Reference

| Operation     | Function                         | Key Parameters                    |
| ------------- | -------------------------------- | --------------------------------- |
| Upload        | `put(path, body, options)`       | path, body, access, contentType   |
| Download      | `get(path, format, options)`     | path, format (string/file/stream) |
| Delete        | `remove(path, options)`          | path                              |
| List          | `list(options)`                  | prefix, limit, paginationToken    |
| Metadata      | `head(path, options)`            | path                              |
| Presigned URL | `getPresignedUrl(path, options)` | path, operation (get/put)         |

## Upload (put)

```typescript
import { put } from "@tigrisdata/storage";

// Simple upload
const result = await put("simple.txt", "Hello, World!");
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Uploaded:", result.data?.url);
}

// Large file with progress
const result = await put("large.mp4", fileStream, {
  multipart: true,
  onUploadProgress: ({ loaded, total, percentage }) => {
    console.log(`${loaded}/${total} bytes (${percentage}%)`);
  },
});

// Prevent overwrite
const result = await put("config.json", config, {
  allowOverwrite: false,
});
```

## Put Options

| Option             | Values            | Default  | Purpose                  |
| ------------------ | ----------------- | -------- | ------------------------ |
| access             | public/private    | -        | Object visibility        |
| addRandomSuffix    | boolean           | false    | Avoid naming collisions  |
| allowOverwrite     | boolean           | true     | Allow replacing existing |
| contentType        | string            | inferred | MIME type                |
| contentDisposition | inline/attachment | inline   | Download behavior        |
| multipart          | boolean           | false    | Enable for large files   |
| onUploadProgress   | callback          | -        | Track upload progress    |

## Download (get)

```typescript
import { get } from "@tigrisdata/storage";

// Get as string
const result = await get("object.txt", "string");
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Content:", result.data);
}

// Get as file (triggers download in browser)
const result = await get("object.pdf", "file", {
  contentDisposition: "attachment",
});

// Get as stream
const result = await get("video.mp4", "stream");
const reader = result.data?.getReader();
// Process stream...
```

## Get Options

| Option             | Values            | Default     | Purpose            |
| ------------------ | ----------------- | ----------- | ------------------ |
| contentDisposition | inline/attachment | inline      | Download behavior  |
| contentType        | string            | from upload | MIME type          |
| encoding           | string            | utf-8       | Text encoding      |
| snapshotVersion    | string            | -           | Read from snapshot |

## Delete (remove)

```typescript
import { remove } from "@tigrisdata/storage";

const result = await remove("object.txt");
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Deleted successfully");
}
```

## List Objects

```typescript
import { list } from "@tigrisdata/storage";

// List all objects
const result = await list();
console.log("Objects:", result.data?.items);

// List with prefix (folders)
const result = await list({ prefix: "images/" });

// List with pagination
const allFiles = [];
let currentPage = await list({ limit: 10 });
allFiles.push(...currentPage.data?.items);

while (currentPage.data?.hasMore) {
  currentPage = await list({
    limit: 10,
    paginationToken: currentPage.data?.paginationToken,
  });
  allFiles.push(...currentPage.data?.items);
}
```

## List Options

| Option          | Purpose                              |
| --------------- | ------------------------------------ |
| prefix          | Filter keys starting with prefix     |
| delimiter       | Group keys (e.g., '/' for folders)   |
| limit           | Max objects to return (default: 100) |
| paginationToken | Continue from previous list          |
| snapshotVersion | List from snapshot                   |

## Object Metadata (head)

```typescript
import { head } from "@tigrisdata/storage";

const result = await head("object.txt");
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Metadata:", result.data);
  // { path, size, contentType, modified, url, contentDisposition }
}
```

## Presigned URLs

```typescript
import { getPresignedUrl } from "@tigrisdata/storage";

// Presigned URL for GET (temporary access)
const result = await getPresignedUrl("object.txt", {
  operation: "get",
  expiresIn: 3600, // 1 hour
});
console.log("URL:", result.data?.url);

// Presigned URL for PUT (allow client upload)
const result = await getPresignedUrl("upload.txt", {
  operation: "put",
  expiresIn: 600, // 10 minutes
});
```

## Presigned URL Options

| Option      | Values  | Default | Purpose         |
| ----------- | ------- | ------- | --------------- |
| operation   | get/put | -       | URL purpose     |
| expiresIn   | seconds | 3600    | URL expiration  |
| contentType | string  | -       | Require for PUT |

## Common Mistakes

| Mistake                      | Fix                                                  |
| ---------------------------- | ---------------------------------------------------- |
| Not checking `error` first   | Always check `if (result.error)` before `result.data`|
| Wrong format in `get()`      | Use 'string', 'file', or 'stream'                    |
| Forgetting `multipart: true` | Enable for files >100MB                              |
| Ignoring pagination          | Use `hasMore` and `paginationToken`                  |

## Client-Side Uploads

For browser uploads, use the client package to upload directly to Tigris:

```typescript
import { upload } from "@tigrisdata/storage/client";

const result = await upload(file.name, file, {
  url: "/api/upload", // Your backend endpoint
  onUploadProgress: ({ percentage }) => {
    console.log(`${percentage}%`);
  },
});
```

For initial setup, see **installing-tigris-storage**.

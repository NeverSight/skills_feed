---
name: supabase-storage
description: Expert guide for Supabase Storage including bucket management, file operations, URL generation, and RLS policies. Use when working with file uploads/downloads, creating public or private buckets, generating signed URLs, implementing storage RLS policies, handling resumable uploads, image transformations, or any Supabase Storage-related tasks.
---

# Supabase Storage Expert

You are an expert in Supabase Storage, specializing in file management, bucket configuration, access control, and Row Level Security (RLS) policies for storage objects.

## 1. Storage Architecture Overview

Supabase Storage provides S3-compatible object storage with built-in CDN, image transformations, and Row Level Security integration.

**Key Components:**
- **Buckets**: Containers for organizing files (public or private)
- **Objects**: Files stored within buckets
- **RLS Policies**: Security rules controlling access to buckets and objects
- **Helper Functions**: SQL functions for path manipulation and access control

---

## 2. Bucket Management

### Creating Buckets

#### JavaScript
```javascript
const { data, error } = await supabase.storage.createBucket('avatars', {
  public: true,
  allowedMimeTypes: ['image/*'],
  fileSizeLimit: '1MB',
})
```

#### SQL
```sql
insert into storage.buckets (id, name, public)
values ('avatars', 'avatars', true);
```

#### Config.toml (Local Development)
```toml
[storage.buckets.images]
public = false
file_size_limit = "50MiB"
allowed_mime_types = ["image/png", "image/jpeg"]
objects_path = "./images"
```

### Bucket Operations

**Get Bucket:**
```javascript
const { data, error } = await supabase.storage.getBucket('avatars')
```

**List Buckets:**
```javascript
const { data, error } = await supabase.storage.listBuckets()
```

**Update Bucket:**
```javascript
const { data, error } = await supabase.storage.updateBucket('avatars', {
  public: false,
  allowedMimeTypes: ['image/png', 'image/jpeg'],
  fileSizeLimit: '5MB'
})
```

**Delete Bucket:**
```javascript
const { data, error } = await supabase.storage.deleteBucket('avatars')
```

**Empty Bucket:**
```javascript
const { data, error } = await supabase.storage.emptyBucket('avatars')
```

---

## 3. File Operations

### Upload Files

#### Standard Upload
```javascript
const avatarFile = event.target.files[0]
const { data, error } = await supabase
  .storage
  .from('avatars')
  .upload('public/avatar1.png', avatarFile, {
    cacheControl: '3600',
    upsert: false
  })
```

#### Upload from Base64 (React Native)
```javascript
import { decode } from 'base64-arraybuffer'

const { data, error } = await supabase
  .storage
  .from('avatars')
  .upload('public/avatar1.png', decode('base64FileData'), {
    contentType: 'image/png'
  })
```

#### TypeScript Upload Function
```typescript
async function uploadAvatar(file: File, userId: string) {
  const fileExt = file.name.split('.').pop()
  const fileName = `${userId}-${Math.random()}.${fileExt}`
  const filePath = `avatars/${fileName}`

  const { data, error } = await supabase.storage
    .from('avatars')
    .upload(filePath, file, {
      cacheControl: '3600',
      upsert: false,
    })

  if (error) {
    throw new Error(`Upload failed: ${error.message}`)
  }

  // Get public URL
  const { data: urlData } = supabase.storage
    .from('avatars')
    .getPublicUrl(filePath)

  console.log('File uploaded to:', urlData.publicUrl)
  return { path: data.path, url: urlData.publicUrl }
}
```

### Resumable Uploads

#### Using tus-js-client
```javascript
const tus = require('tus-js-client')

async function uploadFile(bucketName, fileName, file) {
  const { data: { session } } = await supabase.auth.getSession()

  return new Promise((resolve, reject) => {
    var upload = new tus.Upload(file, {
      endpoint: `https://${projectId}.storage.supabase.co/storage/v1/upload/resumable`,
      retryDelays: [0, 3000, 5000, 10000, 20000],
      headers: {
        authorization: `Bearer ${session.access_token}`,
        'x-upsert': 'true'
      },
      uploadDataDuringCreation: true,
      removeFingerprintOnSuccess: true,
      metadata: {
        bucketName: bucketName,
        objectName: fileName,
        contentType: 'image/png',
        cacheControl: 3600
      },
      chunkSize: 6 * 1024 * 1024, // Must be 6MB
      onError: function (error) {
        reject(error)
      },
      onProgress: function (bytesUploaded, bytesTotal) {
        var percentage = ((bytesUploaded / bytesTotal) * 100).toFixed(2)
        console.log(percentage + '%')
      },
      onSuccess: function () {
        resolve()
      }
    })

    return upload.findPreviousUploads().then(function (previousUploads) {
      if (previousUploads.length) {
        upload.resumeFromPreviousUpload(previousUploads[0])
      }
      upload.start()
    })
  })
}
```

#### Using Uppy.js
```javascript
import { Uppy, Dashboard, Tus } from 'https://releases.transloadit.com/uppy/v3.6.1/uppy.min.mjs'

const token = 'anon-key'
const projectId = 'your-project-ref'
const bucketName = 'avatars'
const supabaseUploadURL = `https://${projectId}.supabase.co/storage/v1/upload/resumable`

var uppy = new Uppy()
  .use(Dashboard, {
    inline: true,
    target: '#drag-drop-area',
    showProgressDetails: true,
  })
  .use(Tus, {
    endpoint: supabaseUploadURL,
    headers: {
      authorization: `Bearer ${token}`,
    },
    chunkSize: 6 * 1024 * 1024,
    allowedMetaFields: ['bucketName', 'objectName', 'contentType', 'cacheControl'],
  })

uppy.on('file-added', (file) => {
  file.meta = {
    ...file.meta,
    bucketName: bucketName,
    objectName: `folder/${file.name}`,
    contentType: file.type,
  }
})

uppy.on('complete', (result) => {
  console.log('Upload complete!', result.successful)
})
```

### Download Files

```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .download('folder/avatar1.png')
```

**With Transformations:**
```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .download('folder/avatar1.png', {
    transform: {
      width: 100,
      height: 100,
      quality: 80
    }
  })
```

### List Files

```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .list('folder', {
    limit: 100,
    offset: 0,
    sortBy: { column: 'name', order: 'asc' }
  })
```

### Update/Replace File

```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .update('folder/avatar1.png', newFile, {
    cacheControl: '3600',
    upsert: true
  })
```

### Move File

```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .move('folder/avatar1.png', 'folder/avatar2.png')
```

### Copy File

```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .copy('folder/avatar1.png', 'folder/avatar1-copy.png')
```

### Remove Files

```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .remove(['folder/avatar1.png', 'folder/avatar2.png'])
```

---

## 4. URL Generation

### Public URLs

**For Public Buckets:**
```javascript
const { data } = supabase
  .storage
  .from('public-bucket')
  .getPublicUrl('folder/avatar1.png')

console.log(data.publicUrl)
```

**Direct URL Format:**
```
https://[project_id].supabase.co/storage/v1/object/public/[bucket]/[asset-name]
```

**Force Download:**
```
https://[project_id].supabase.co/storage/v1/object/public/[bucket]/[asset-name]?download
https://[project_id].supabase.co/storage/v1/object/public/[bucket]/[asset-name]?download=customname.jpg
```

**With Transformations:**
```javascript
const { data } = supabase
  .storage
  .from('public-bucket')
  .getPublicUrl('folder/avatar1.png', {
    transform: {
      width: 100,
      height: 100,
    }
  })
```

### Signed URLs (Private Buckets)

**Create Single Signed URL:**
```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .createSignedUrl('folder/avatar1.png', 60) // 60 seconds
```

**TypeScript Function:**
```typescript
async function createSignedUrl(filePath: string, expiresIn: number = 3600) {
  const { data, error } = await supabase.storage
    .from('private-files')
    .createSignedUrl(filePath, expiresIn)

  if (error) {
    throw new Error(`Signed URL creation failed: ${error.message}`)
  }

  console.log('Signed URL:', data.signedUrl)
  return data.signedUrl
}
```

**With Transformations:**
```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .createSignedUrl('folder/avatar1.png', 60, {
    transform: {
      width: 100,
      height: 100,
    }
  })
```

**Force Download:**
```javascript
const { data } = await supabase
  .storage
  .from('avatars')
  .createSignedUrl('folder/avatar1.png', 60, {
    download: true,
  })
```

**Create Multiple Signed URLs:**
```javascript
const { data, error } = await supabase
  .storage
  .from('avatars')
  .createSignedUrls(['folder/avatar1.png', 'folder/avatar2.png'], 60)
```

### Signed Upload URLs

```javascript
// Create a signed upload url
const filePath = 'users.txt'
const { token } = await supabase
  .storage
  .from(bucketName)
  .createSignedUploadUrl(filePath)

// Upload to the signed URL
await supabase
  .storage
  .from(bucketName)
  .uploadToSignedUrl(filePath, token, file)
```

---

## 5. Row Level Security (RLS) Policies

### Basic Policy Structure

RLS policies control access to storage objects through the `storage.objects` table.

**Required Permissions:**
- `buckets` table permissions: Varies by operation
- `objects` table permissions: Varies by operation (select, insert, update, delete)

### Public Bucket Policies

**Allow Public Viewing:**
```sql
create policy "Avatar images are publicly accessible"
  on storage.objects for select
  using (bucket_id = 'avatars');
```

**Allow Authenticated Uploads:**
```sql
create policy "Anyone can upload an avatar"
  on storage.objects for insert
  with check (
    bucket_id = 'avatars'
    AND auth.role() = 'authenticated'
  );
```

**User-Specific Updates:**
```sql
create policy "Users can update own avatar"
  on storage.objects for update
  using (
    auth.uid()::text = (storage.foldername(name))[1]
    AND bucket_id = 'avatars'
  );
```

**User-Specific Deletes:**
```sql
create policy "Users can delete own avatar"
  on storage.objects for delete
  using (
    auth.uid()::text = (storage.foldername(name))[1]
    AND bucket_id = 'avatars'
  );
```

### Private Bucket Policies

**User-Only Access:**
```sql
-- Private bucket
insert into storage.buckets (id, name, public)
values ('private-files', 'private-files', false);

-- Users can only access their own private files
create policy "Users can access own private files"
  on storage.objects for select
  using (
    bucket_id = 'private-files'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

create policy "Users can upload own private files"
  on storage.objects for insert
  with check (
    bucket_id = 'private-files'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );
```

**Owner-Based Access:**
```sql
create policy "Individual user Access"
on storage.objects for select
to authenticated
using ( (select auth.uid()) = owner_id::uuid );
```

### Advanced Policy Patterns

**Restrict by File Extension:**
```sql
create policy "Only allow PNG uploads"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'cats' and storage.extension(name) = 'png'
);
```

**Restrict to Specific Folder:**
```sql
create policy "Allow authenticated uploads"
on storage.objects
for insert
to authenticated
with check (
  (storage.foldername(name))[1] = 'private'
);
```

**User Folder with Bucket Restriction:**
```sql
create policy "Allow authenticated uploads"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'my_bucket_id' and
  (storage.foldername(name))[1] = (select auth.uid()::text)
);
```

**Restrict by Bucket:**
```sql
create policy "policy_name"
on storage.objects for insert to authenticated with check (
  bucket_id = 'my_bucket_id'
);
```

**Role-Based Access:**
```sql
create policy "Manager can view all files in the bucket 'teams'"
on storage.objects
for select
to manager
using (
  bucket_id = 'teams'
);
```

### Complete Setup Example

```sql
-- Set up Storage bucket
insert into storage.buckets (id, name, public)
values ('avatars', 'avatars', true);

-- Policy: Anyone can view avatar images
create policy "Avatar images are publicly accessible"
  on storage.objects for select
  using (bucket_id = 'avatars');

-- Policy: Authenticated users can upload avatars
create policy "Anyone can upload an avatar"
  on storage.objects for insert
  with check (
    bucket_id = 'avatars'
    AND auth.role() = 'authenticated'
  );

-- Policy: Users can update their own avatars
create policy "Users can update own avatar"
  on storage.objects for update
  using (
    auth.uid()::text = (storage.foldername(name))[1]
    AND bucket_id = 'avatars'
  );

-- Policy: Users can delete their own avatars
create policy "Users can delete own avatar"
  on storage.objects for delete
  using (
    auth.uid()::text = (storage.foldername(name))[1]
    AND bucket_id = 'avatars'
  );
```

---

## 6. Storage Helper Functions

### `storage.foldername(name)`

Extracts folder path components from object name.

```sql
-- Returns array of folder names
(storage.foldername('folder1/folder2/file.png'))[1] -- 'folder1'
(storage.foldername('folder1/folder2/file.png'))[2] -- 'folder2'
```

### `storage.extension(name)`

Extracts file extension from object name.

```sql
storage.extension('file.png') -- 'png'
storage.extension('document.pdf') -- 'pdf'
```

---

## 7. Access Control via Edge Functions

For complex access control scenarios, use Edge Functions to proxy private storage:

```typescript
const ALLOWED_ORIGINS = ['http://localhost:8000']
const corsHeaders = {
  'Access-Control-Allow-Origin': ALLOWED_ORIGINS.join(','),
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, range, if-match',
  'Access-Control-Expose-Headers': 'range, accept-ranges, etag',
  'Access-Control-Max-Age': '300',
}

Deno.serve((req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  // Check origin
  const origin = req.headers.get('Origin')
  if (!origin || !ALLOWED_ORIGINS.includes(origin)) {
    return new Response('Not Allowed', { status: 405 })
  }

  const reqUrl = new URL(req.url)
  const url = `${Deno.env.get('SUPABASE_URL')}/storage/v1/object/authenticated${reqUrl.pathname}`

  const { method, headers } = req
  const modHeaders = new Headers(headers)
  modHeaders.append('authorization', `Bearer ${Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!}`)

  return fetch(url, { method, headers: modHeaders })
})
```

---

## 8. Best Practices

### Security
1. **Always enable RLS** on storage.objects when using storage
2. **Use separate buckets** for public and private content
3. **Organize files by user ID** in folder structure for easy access control
4. **Validate file types** and sizes at both client and policy level
5. **Use signed URLs** for temporary access to private files
6. **Never expose service role key** to client-side code

### Performance
1. **Use public buckets** for static assets with high CDN cache hit ratio
2. **Set appropriate cache control** headers for uploaded files
3. **Use image transformations** instead of uploading multiple sizes
4. **Implement resumable uploads** for large files (>6MB)
5. **Batch operations** when possible (e.g., createSignedUrls for multiple files)

### Organization
1. **Name buckets** descriptively (e.g., 'user-avatars', 'product-images')
2. **Use folder structure** for logical organization (e.g., `userId/avatars/filename.png`)
3. **Include metadata** in upload options for better file management
4. **Set file size limits** on buckets to prevent abuse
5. **Use allowed MIME types** to restrict upload types

### Error Handling
1. **Always check for errors** after storage operations
2. **Handle network failures** gracefully with retry logic
3. **Provide user feedback** during uploads and downloads
4. **Validate files** on client before uploading
5. **Log errors** for debugging and monitoring

---

## 9. Image Transformations

Supabase Storage includes built-in image transformation capabilities:

**Available Transformations:**
- `width`: Resize width
- `height`: Resize height
- `quality`: Compression quality (1-100)
- `format`: Convert format (webp, jpeg, png)

**Example:**
```javascript
const { data } = supabase
  .storage
  .from('avatars')
  .getPublicUrl('avatar.jpg', {
    transform: {
      width: 400,
      height: 400,
      quality: 80,
      format: 'webp'
    }
  })
```

---

## Summary

This comprehensive Supabase Storage skill covers:
1. **Bucket Management** - Create, configure, and manage storage buckets
2. **File Operations** - Upload, download, list, move, copy, and delete files
3. **URL Generation** - Public URLs, signed URLs, and signed upload URLs
4. **RLS Policies** - Comprehensive access control patterns
5. **Helper Functions** - SQL utilities for path and extension manipulation
6. **Edge Function Integration** - Advanced access control scenarios
7. **Best Practices** - Security, performance, and organization guidelines
8. **Image Transformations** - Built-in image processing

Use this skill whenever working with Supabase Storage to ensure best practices, security, and optimal performance.

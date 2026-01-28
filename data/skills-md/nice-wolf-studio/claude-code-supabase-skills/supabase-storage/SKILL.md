---
name: supabase-storage
description: Manage file storage operations in Supabase Storage. Use for uploading, downloading, listing, and deleting files in buckets.
---

# Supabase Storage Operations

## Overview

This skill provides file storage operations through the Supabase Storage API. Supports bucket management, file uploads/downloads, listing files, generating URLs, and managing access control.

## Prerequisites

**Required environment variables:**
```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-or-service-role-key"
```

**Helper script:**
This skill uses the shared Supabase API helper. Make sure to source it:
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"
```

## Bucket Operations

### List Buckets

**Get all storage buckets:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

supabase_get "/storage/v1/bucket"
```

### Create Bucket

**Create a new storage bucket:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

# Public bucket
supabase_post "/storage/v1/bucket" '{
  "name": "avatars",
  "public": true
}'

# Private bucket
supabase_post "/storage/v1/bucket" '{
  "name": "private-documents",
  "public": false,
  "file_size_limit": 52428800,
  "allowed_mime_types": ["image/png", "image/jpeg", "application/pdf"]
}'
```

### Get Bucket Details

**Retrieve bucket information:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

supabase_get "/storage/v1/bucket/avatars"
```

### Update Bucket

**Update bucket settings:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

curl -s -X PUT \
    "${SUPABASE_URL}/storage/v1/bucket/avatars" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -H "Content-Type: application/json" \
    -d '{
      "public": false,
      "file_size_limit": 10485760
    }'
```

### Delete Bucket

**Delete a bucket (must be empty):**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

supabase_delete "/storage/v1/bucket/old-bucket"
```

### Empty Bucket

**Delete all files in a bucket:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

supabase_post "/storage/v1/bucket/avatars/empty" '{}'
```

## File Operations

### Upload File

**Upload a file to storage:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="avatars"
FILE_PATH="/path/to/local/image.jpg"
STORAGE_PATH="user-123/profile.jpg"

curl -s -X POST \
    "${SUPABASE_URL}/storage/v1/object/${BUCKET_NAME}/${STORAGE_PATH}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -F "file=@${FILE_PATH}"
```

**Upload with upsert (overwrite if exists):**
```bash
curl -s -X POST \
    "${SUPABASE_URL}/storage/v1/object/${BUCKET_NAME}/${STORAGE_PATH}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -H "x-upsert: true" \
    -F "file=@${FILE_PATH}"
```

**Upload with content type:**
```bash
curl -s -X POST \
    "${SUPABASE_URL}/storage/v1/object/${BUCKET_NAME}/${STORAGE_PATH}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -H "Content-Type: image/jpeg" \
    -F "file=@${FILE_PATH}"
```

### Download File

**Download a file from storage:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="avatars"
STORAGE_PATH="user-123/profile.jpg"
OUTPUT_FILE="/path/to/save/downloaded.jpg"

curl -s -X GET \
    "${SUPABASE_URL}/storage/v1/object/${BUCKET_NAME}/${STORAGE_PATH}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -o "${OUTPUT_FILE}"
```

**Download to stdout (pipe to other commands):**
```bash
curl -s -X GET \
    "${SUPABASE_URL}/storage/v1/object/${BUCKET_NAME}/${STORAGE_PATH}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}"
```

### List Files

**List files in a bucket:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="avatars"

supabase_post "/storage/v1/object/list/${BUCKET_NAME}" '{
  "limit": 100,
  "offset": 0,
  "sortBy": {
    "column": "name",
    "order": "asc"
  }
}'
```

**List files in a specific folder:**
```bash
supabase_post "/storage/v1/object/list/${BUCKET_NAME}" '{
  "prefix": "user-123/",
  "limit": 100
}'
```

**Search files:**
```bash
supabase_post "/storage/v1/object/list/${BUCKET_NAME}" '{
  "search": "profile",
  "limit": 50
}'
```

### Delete File

**Delete a single file:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="avatars"
STORAGE_PATH="user-123/old-profile.jpg"

supabase_delete "/storage/v1/object/${BUCKET_NAME}/${STORAGE_PATH}"
```

**Delete multiple files:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="avatars"

supabase_delete "/storage/v1/object/${BUCKET_NAME}" -d '{
  "prefixes": ["user-123/temp/", "user-456/draft/"]
}'
```

### Move/Rename File

**Move or rename a file:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="avatars"
FROM_PATH="user-123/temp.jpg"
TO_PATH="user-123/final.jpg"

supabase_post "/storage/v1/object/move" '{
  "bucketId": "'"${BUCKET_NAME}"'",
  "sourceKey": "'"${FROM_PATH}"'",
  "destinationKey": "'"${TO_PATH}"'"
}'
```

### Copy File

**Copy a file to another location:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="avatars"
SOURCE_PATH="user-123/profile.jpg"
DEST_PATH="user-123/profile-backup.jpg"

supabase_post "/storage/v1/object/copy" '{
  "bucketId": "'"${BUCKET_NAME}"'",
  "sourceKey": "'"${SOURCE_PATH}"'",
  "destinationKey": "'"${DEST_PATH}"'"
}'
```

## URL Generation

### Get Public URL

**Get public URL for a file (public buckets only):**
```bash
BUCKET_NAME="avatars"
STORAGE_PATH="user-123/profile.jpg"

PUBLIC_URL="${SUPABASE_URL}/storage/v1/object/public/${BUCKET_NAME}/${STORAGE_PATH}"
echo "Public URL: $PUBLIC_URL"
```

### Create Signed URL

**Generate a signed URL for temporary access:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="private-documents"
STORAGE_PATH="user-123/secret.pdf"
EXPIRES_IN=3600  # 1 hour in seconds

supabase_post "/storage/v1/object/sign/${BUCKET_NAME}/${STORAGE_PATH}" '{
  "expiresIn": '"${EXPIRES_IN}"'
}'
```

Response will include:
```json
{
  "signedURL": "/storage/v1/object/sign/private-documents/user-123/secret.pdf?token=..."
}
```

Full URL:
```bash
signed_path=$(supabase_post "/storage/v1/object/sign/${BUCKET_NAME}/${STORAGE_PATH}" '{"expiresIn": 3600}' | jq -r '.signedURL')
full_url="${SUPABASE_URL}${signed_path}"
echo "Signed URL: $full_url"
```

### Create Multiple Signed URLs

**Generate signed URLs for multiple files:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="private-documents"

supabase_post "/storage/v1/object/sign/${BUCKET_NAME}" '{
  "paths": ["doc1.pdf", "doc2.pdf", "folder/doc3.pdf"],
  "expiresIn": 3600
}'
```

## Common Patterns

### Upload with Progress
```bash
#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="uploads"
FILE_PATH="/path/to/large-file.zip"
STORAGE_PATH="user-123/backup.zip"

echo "Uploading ${FILE_PATH}..."

curl -X POST \
    "${SUPABASE_URL}/storage/v1/object/${BUCKET_NAME}/${STORAGE_PATH}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -F "file=@${FILE_PATH}" \
    --progress-bar -o /dev/null

if [[ $? -eq 0 ]]; then
    echo "Upload successful!"
else
    echo "Upload failed!"
    exit 1
fi
```

### Check if File Exists
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="avatars"
STORAGE_PATH="user-123/profile.jpg"

# Try to get file info
response=$(curl -s -X GET \
    "${SUPABASE_URL}/storage/v1/object/info/${BUCKET_NAME}/${STORAGE_PATH}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -w "\n%{http_code}")

http_code=$(echo "$response" | tail -n1)

if [[ $http_code -eq 200 ]]; then
    echo "File exists"
else
    echo "File does not exist"
fi
```

### Batch Upload Files
```bash
#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="uploads"
LOCAL_DIR="/path/to/files"

for file in "$LOCAL_DIR"/*; do
    filename=$(basename "$file")
    echo "Uploading $filename..."

    curl -s -X POST \
        "${SUPABASE_URL}/storage/v1/object/${BUCKET_NAME}/batch/${filename}" \
        -H "apikey: ${SUPABASE_KEY}" \
        -H "Authorization: Bearer ${SUPABASE_KEY}" \
        -F "file=@${file}"

    echo "✓ Uploaded $filename"
done
```

### Download All Files from Bucket
```bash
#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

BUCKET_NAME="avatars"
OUTPUT_DIR="/path/to/download"

mkdir -p "$OUTPUT_DIR"

# Get file list
files=$(supabase_post "/storage/v1/object/list/${BUCKET_NAME}" '{"limit": 1000}')

# Download each file
echo "$files" | jq -r '.[].name' | while read -r filename; do
    echo "Downloading $filename..."

    curl -s -X GET \
        "${SUPABASE_URL}/storage/v1/object/${BUCKET_NAME}/${filename}" \
        -H "apikey: ${SUPABASE_KEY}" \
        -H "Authorization: Bearer ${SUPABASE_KEY}" \
        -o "${OUTPUT_DIR}/${filename}"

    echo "✓ Downloaded $filename"
done
```

## Image Transformations

**Transform images on-the-fly (public buckets):**
```bash
BUCKET_NAME="avatars"
STORAGE_PATH="user-123/profile.jpg"

# Resize to width 200px
TRANSFORMED_URL="${SUPABASE_URL}/storage/v1/render/image/public/${BUCKET_NAME}/${STORAGE_PATH}?width=200"

# Resize with quality
TRANSFORMED_URL="${SUPABASE_URL}/storage/v1/render/image/public/${BUCKET_NAME}/${STORAGE_PATH}?width=200&quality=80"

# Multiple transformations
TRANSFORMED_URL="${SUPABASE_URL}/storage/v1/render/image/public/${BUCKET_NAME}/${STORAGE_PATH}?width=300&height=300&resize=contain"
```

## Access Control

**Storage access is controlled by Storage Policies (RLS) in your Supabase dashboard.**

Common policy examples:

**Public read, authenticated write:**
```sql
-- Set in Supabase Dashboard > Storage > Policies
-- Allow public to read
SELECT: true for all users

-- Allow authenticated users to upload their own files
INSERT: auth.uid() = (storage.foldername(name))[1]
```

**User-specific folders:**
```sql
-- Users can only access files in their own folder
SELECT: auth.uid() = (storage.foldername(name))[1]
UPDATE: auth.uid() = (storage.foldername(name))[1]
DELETE: auth.uid() = (storage.foldername(name))[1]
```

## Error Handling

Common errors:

| Status | Error | Meaning |
|--------|-------|---------|
| 400 | Invalid bucket name | Bucket name contains invalid characters |
| 404 | Object not found | File doesn't exist |
| 409 | Bucket already exists | Bucket with that name exists |
| 413 | Payload too large | File exceeds size limit |
| 422 | Invalid MIME type | File type not allowed in bucket |

## Security Best Practices

1. **Use private buckets** for sensitive data
2. **Implement Storage Policies** (RLS) for access control
3. **Set file size limits** to prevent abuse
4. **Restrict MIME types** to expected file types
5. **Use signed URLs** for temporary access to private files
6. **Organize files** in user-specific folders (e.g., `user-{uuid}/`)
7. **Never expose service role key** to client applications

## File Size Limits

- Default max file size: 50MB
- Can be configured per bucket up to 5GB (contact Supabase for larger)
- Check bucket settings for current limit

## API Documentation

Full Supabase Storage API documentation: https://supabase.com/docs/guides/storage

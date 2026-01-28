---
name: minio
description: MinIO S3-compatible object storage API. Use this skill for file upload, download, bucket management, and pre-signed URL generation.
vm0_secrets:
  - MINIO_ACCESS_KEY
  - MINIO_SECRET_KEY
vm0_vars:
  - MINIO_ENDPOINT
---

# MinIO Object Storage

Use the MinIO API via `mc` (MinIO Client) or `curl` to manage **S3-compatible object storage** for file uploads, downloads, and bucket operations.

> Official docs: `https://min.io/docs/minio/linux/reference/minio-mc.html`

---

## When to Use

Use this skill when you need to:

- **Upload/download files** to S3-compatible storage
- **Manage buckets** (create, list, delete)
- **Generate pre-signed URLs** for temporary file access
- **List and search objects** in storage
- **Mirror/sync directories** between local and remote

---

## Prerequisites

1. Deploy MinIO server or use MinIO Play (public test server)
2. Get access credentials (Access Key and Secret Key)
3. Install MinIO Client (`mc`)

### Install MinIO Client

```bash
# macOS
brew install minio/stable/mc

# Linux (amd64)
curl -O https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc && sudo mv mc /usr/local/bin/

# Verify installation
mc --version
```

### Set Environment Variables

```bash
export MINIO_ENDPOINT="play.min.io"
export MINIO_ACCESS_KEY="your-access-key"
export MINIO_SECRET_KEY="your-secret-key"
```

For testing, use MinIO Play (public sandbox):

```bash
export MINIO_ENDPOINT="play.min.io"
export MINIO_ACCESS_KEY="Q3AM3UQ867SPQQA43P2F"
export MINIO_SECRET_KEY="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
```

### Configure mc Alias

```bash
mc alias set myminio https://${MINIO_ENDPOINT} ${MINIO_ACCESS_KEY} ${MINIO_SECRET_KEY}
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

### 1. List Buckets

```bash
mc ls myminio
```

### 2. Create a Bucket

```bash
mc mb myminio/my-bucket
```

### 3. Upload a File

```bash
# Upload single file
mc cp /path/to/file.txt myminio/my-bucket/

# Upload with custom name
mc cp /path/to/file.txt myminio/my-bucket/custom-name.txt

# Upload directory recursively
mc cp --recursive /path/to/folder/ myminio/my-bucket/folder/
```

### 4. Download a File

```bash
# Download single file
mc cp myminio/my-bucket/file.txt /local/path/

# Download entire bucket
mc cp --recursive myminio/my-bucket/ /local/path/
```

### 5. List Objects in Bucket

```bash
# List all objects
mc ls myminio/my-bucket

# List recursively with details
mc ls --recursive --summarize myminio/my-bucket
```

### 6. Delete Objects

```bash
# Delete single file
mc rm myminio/my-bucket/file.txt

# Delete all objects in bucket
mc rm --recursive --force myminio/my-bucket/

# Delete bucket (must be empty)
mc rb myminio/my-bucket
```

### 7. Generate Pre-signed URL

Create temporary shareable links:

```bash
# Download URL (expires in 7 days by default)
mc share download myminio/my-bucket/file.txt

# Download URL with custom expiry (max 7 days)
mc share download --expire 2h myminio/my-bucket/file.txt

# Upload URL (for external uploads)
mc share upload myminio/my-bucket/uploads/
```

### 8. Mirror/Sync Directories

```bash
# One-way sync local to remote
mc mirror /local/folder/ myminio/my-bucket/folder/

# One-way sync remote to local
mc mirror myminio/my-bucket/folder/ /local/folder/

# Watch and sync changes continuously
mc mirror --watch /local/folder/ myminio/my-bucket/folder/
```

### 9. Get Object Info

```bash
# Get file metadata
mc stat myminio/my-bucket/file.txt

# Get bucket info
mc stat myminio/my-bucket
```

### 10. Search Objects

```bash
# Find by name pattern
mc find myminio/my-bucket --name "*.txt"

# Find files larger than 10MB
mc find myminio/my-bucket --larger 10MB

# Find files modified in last 7 days
mc find myminio/my-bucket --newer-than 7d
```

---

## Using curl with Pre-signed URLs

For environments without `mc`, use pre-signed URLs with curl:

### Upload with Pre-signed URL

```bash
# First, generate upload URL with mc
UPLOAD_URL=$(bash -c 'mc share upload --json myminio/my-bucket/file.txt' | jq -r '.share')

# Then upload with curl
curl -X PUT --upload-file /path/to/file.txt "$UPLOAD_URL"
```

### Download with Pre-signed URL

```bash
# Generate download URL
DOWNLOAD_URL=$(bash -c 'mc share download --json myminio/my-bucket/file.txt' | jq -r '.share')

# Download with curl
curl -o /local/path/file.txt "$DOWNLOAD_URL"
```

---

## Using curl with AWS Signature V2

For direct API access without mc (simple authentication):

```bash
#!/bin/bash
# minio-upload.sh - Upload file to MinIO

bucket="$1"
file="$2"
host="${MINIO_ENDPOINT}"
s3_key="${MINIO_ACCESS_KEY}"
s3_secret="${MINIO_SECRET_KEY}"

resource="/${bucket}/${file}"
content_type="application/octet-stream"
date=$(date -R)
signature_string="PUT\n\n${content_type}\n${date}\n${resource}"
signature=$(echo -en "${signature_string}" | openssl sha1 -hmac "${s3_secret}" -binary | base64)

curl -X PUT -T "${file}" --header "Host: ${host}" --header "Date: ${date}" --header "Content-Type: ${content_type}" --header "Authorization: AWS ${s3_key}:${signature}" "https://${host}${resource}"
```

Usage:

```bash
chmod +x minio-upload.sh
./minio-upload.sh my-bucket myfile.txt
```

---

## Using AWS CLI

MinIO is fully compatible with AWS CLI:

```bash
# Configure AWS CLI for MinIO
aws configure set aws_access_key_id "${MINIO_ACCESS_KEY}"
aws configure set aws_secret_access_key "${MINIO_SECRET_KEY}"
aws configure set default.s3.signature_version s3v4

# List buckets
aws --endpoint-url "https://${MINIO_ENDPOINT}" s3 ls

# Upload file
aws --endpoint-url "https://${MINIO_ENDPOINT}" s3 cp file.txt s3://my-bucket/

# Download file
aws --endpoint-url "https://${MINIO_ENDPOINT}" s3 cp s3://my-bucket/file.txt ./

# List objects
aws --endpoint-url "https://${MINIO_ENDPOINT}" s3 ls s3://my-bucket/
```

---

## Bucket Policies

### Set Bucket to Public Read

```bash
mc anonymous set download myminio/my-bucket
```

### Set Bucket to Private

```bash
mc anonymous set none myminio/my-bucket
```

### Apply Custom Policy

```bash
# Create policy.json
cat > /tmp/policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
  {
  "Effect": "Allow",
  "Principal": {"AWS": ["*"]},
  "Action": ["s3:GetObject"],
  "Resource": ["arn:aws:s3:::my-bucket/public/*"]
  }
  ]
}
EOF

mc anonymous set-json /tmp/policy.json myminio/my-bucket
```

---

## Guidelines

1. **Use mc for most operations** - It handles authentication and signing automatically
2. **Pre-signed URLs for external access** - Share files without exposing credentials
3. **Use port 9000 for API** - Port 9001 is typically the web console
4. **Set appropriate expiry** - Pre-signed URLs should expire as soon as practical (max 7 days)
5. **Use mirror for backups** - `mc mirror --watch` for continuous sync
6. **Bucket naming rules** - Lowercase, 3-63 characters, no underscores or consecutive dots

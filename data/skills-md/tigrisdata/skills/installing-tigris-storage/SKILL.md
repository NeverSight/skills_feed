---
name: installing-tigris-storage
description: Use when setting up @tigrisdata/storage in a new project or configuring authentication and bucket access
---

# Installing Tigris Storage

## Overview

Tigris Storage is a high-performance object storage system for multi-cloud environments. This skill covers installation and configuration.

## Quick Setup

### 1. Install the Package

```bash
npm install @tigrisdata/storage
# or
yarn add @tigrisdata/storage
```

### 2. Create Account Resources

1. Create Tigris account: https://storage.new
2. Create bucket: https://console.tigris.dev/createbucket
3. Create access key: https://console.tigris.dev/createaccesskey

### 3. Configure the Environment

Create `.env` in project root:

```bash
TIGRIS_STORAGE_ACCESS_KEY_ID=tid_access_key_id
TIGRIS_STORAGE_SECRET_ACCESS_KEY=tsec_secret_access_key
TIGRIS_STORAGE_BUCKET=bucket_name
```

## Quick Reference

| Variable                           | Purpose               | Required           |
| ---------------------------------- | --------------------- | ------------------ |
| `TIGRIS_STORAGE_ACCESS_KEY_ID`     | Authentication key ID | Yes                |
| `TIGRIS_STORAGE_SECRET_ACCESS_KEY` | Authentication secret | Yes                |
| `TIGRIS_STORAGE_BUCKET`            | Default bucket name   | Yes (can override) |

## Per-Request Configuration

All methods accept optional config to override environment variables:

```typescript
import { list } from "@tigrisdata/storage";

// Use environment defaults
const result = await list();

// Override bucket
const result = await list({
  config: { bucket: "different-bucket" },
});

// Override all config
const result = await list({
  config: {
    bucket: "my-bucket",
    accessKeyId: "key",
    secretAccessKey: "secret",
  },
});
```

## Common Mistakes

| Mistake                | Fix                                             |
| ---------------------- | ----------------------------------------------- |
| Missing `.env` file    | Create it in project root                       |
| Wrong bucket name      | Verify at console.tigris.dev                    |
| Access key not working | Regenerate at console.tigris.dev/createaccesskey |

## Next Steps

After installation:

- Use **tigris-object-operations** to get, put, delete, and list objects
- Use **tigris-bucket-management** for bucket CRUD operations
- Use **tigris-snapshots-forking** for version control and forking

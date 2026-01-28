---
name: tigris-bucket-management
description: Use when creating, listing, inspecting, or deleting Tigris Storage buckets
---

# Tigris Bucket Management

## Overview

Buckets are containers for objects. This skill covers bucket lifecycle: create, list, inspect, and delete.

## Quick Reference

| Operation | Function                      | Key Parameters                       |
| --------- | ----------------------------- | ------------------------------------ |
| Create    | `createBucket(name, options)` | name, access, region, enableSnapshot |
| List      | `listBuckets(options)`        | limit, paginationToken               |
| Inspect   | `getBucketInfo(name)`         | bucketName                           |
| Delete    | `removeBucket(name, options)` | bucketName, force                    |

## Create Bucket

```typescript
import { createBucket } from "@tigrisdata/storage";

// Simple private bucket
const result = await createBucket("my-new-bucket");
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Created:", result.data);
}

// Public bucket (objects readable by anyone)
const result = await createBucket("public-assets", {
  access: "public",
});

// Snapshot-enabled bucket (for version control)
const result = await createBucket("my-snapshot-bucket", {
  enableSnapshot: true,
});

// Regional bucket
const result = await createBucket("eu-data", {
  region: "eu",
});

// Fork from existing bucket snapshot
const result = await createBucket("my-forked-bucket", {
  sourceBucketName: "parent-bucket",
  sourceBucketSnapshot: "1751631910169675092",
});
```

## Create Bucket Options

| Option               | Values                                  | Default  | Purpose                  |
| -------------------- | --------------------------------------- | -------- | ------------------------ |
| access               | public/private                          | private  | Object readability       |
| consistency          | default/strict                          | default  | Read consistency level   |
| defaultTier          | STANDARD/STANDARD_IA/GLACIER/GLACIER_IR | STANDARD | Default storage tier     |
| enableSnapshot       | boolean                                 | false    | Enable snapshots/forking |
| region               | string                                  | global   | Bucket region            |
| sourceBucketName     | string                                  | -        | Fork from this bucket    |
| sourceBucketSnapshot | string                                  | -        | Fork from this snapshot  |

**Note:** Snapshot-enabled buckets must use STANDARD tier.

## List Buckets

```typescript
import { listBuckets } from "@tigrisdata/storage";

// List all buckets
const result = await listBuckets();
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Buckets:", result.data?.buckets);
  console.log("Owner:", result.data?.owner);
}

// Paginated list
const allBuckets = [];
let currentPage = await listBuckets({ limit: 10 });
allBuckets.push(...currentPage.data?.buckets);

while (currentPage.data?.paginationToken) {
  currentPage = await listBuckets({
    limit: 10,
    paginationToken: currentPage.data?.paginationToken,
  });
  allBuckets.push(...currentPage.data?.buckets);
}
```

## Get Bucket Info

```typescript
import { getBucketInfo } from "@tigrisdata/storage";

const result = await getBucketInfo("my-bucket");
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Info:", result.data);
  // {
  //   isSnapshotEnabled: true,
  //   hasForks: false,
  //   sourceBucketName: undefined,
  //   sourceBucketSnapshot: undefined
  // }
}
```

## Delete Bucket

```typescript
import { removeBucket } from "@tigrisdata/storage";

// Delete empty bucket
const result = await removeBucket("my-bucket");
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Deleted successfully");
}

// Force delete (even if not empty)
const result = await removeBucket("my-bucket", {
  force: true,
});
```

**Warning:** Force delete is irreversible. All objects will be lost.

## Bucket Access Levels

| Level   | Behavior                  | Use Case                      |
| ------- | ------------------------- | ----------------------------- |
| private | Objects require auth      | Default, sensitive data       |
| public  | Objects publicly readable | Static assets, public content |

## Consistency Levels

| Level   | Behavior                           | Trade-off      |
| ------- | ---------------------------------- | -------------- |
| default | Low latency, eventual consistency  | Most workloads |
| strict  | Strong consistency, higher latency | Critical data  |

## Storage Tiers

| Tier        | Use Case                    | Cost                           |
| ----------- | --------------------------- | ------------------------------ |
| STANDARD    | General purpose             | Standard                       |
| STANDARD_IA | Infrequently accessed       | Lower cost                     |
| GLACIER     | Long-term archive           | Lowest cost                    |
| GLACIER_IR  | Rare access, fast retrieval | Archive with occasional access |

## Regions

Specify region for data locality or compliance:

```typescript
await createBucket("data-eu", { region: "eu" });
await createBucket("data-asia", { region: "asia-south-1" });
```

Leave empty for global bucket (recommended for most use cases).

## Common Mistakes

| Mistake                                         | Fix                                    |
| ----------------------------------------------- | -------------------------------------- |
| Enable snapshot with non-STANDARD tier          | Snapshot requires STANDARD tier        |
| Not checking bucket exists before delete        | Use `getBucketInfo` first              |
| Trying to delete non-empty bucket without force | Use `force: true` or empty bucket first |
| Name conflicts                                  | Bucket names must be globally unique   |

## Forking and Snapshots

For version control (snapshots/forking), see the **tigris-snapshots-forking** skill.

## Prerequisites

Before managing buckets, ensure @tigrisdata/storage is installed. See **installing-tigris-storage**.

---
name: tigris-snapshots-forking
description: Use when needing point-in-time recovery, version control for object storage, or creating isolated bucket copies for testing/experimentation
---

# Tigris Snapshots and Forking

## Overview

**Snapshots** capture your entire bucket at a point in time. **Forking** creates instant, isolated copies from snapshots using copy-on-write.

**Core principle:** Snapshots and forks protect your data from deletion. Even if you delete everything in a fork, the source bucket data remains intact.

## Why Snapshots Matter

Object storage serves as the primary data store for many systems. It needs safety features:

- **Point-in-time recovery** - Restore after accidental deletion or corruption
- **Version control** - Tag meaningful states like releases
- **Reproducibility** - Recreate exact environments for debugging or testing
- **Deletion protection** - Forks can be destroyed without affecting source

Traditional object versioning only works per-object. To restore a bucket to a point in time, you must check and restore each object individually. Tigris snapshots capture the entire bucket state instantly.

## Why Forking Matters

Forking creates isolated bucket copies instantly - even for terabytes of data:

- **Developer sandboxes** - Test with real production data safely
- **AI agent environments** - Spin up agents with pre-loaded dependencies
- **Load testing** - Use production data without risk
- **Feature branch testing** - Parallel environments for experiments
- **Training experiments** - Fork datasets to test without affecting source

**How it works:** Tigris uses immutable objects with backwards-ordered timestamps. Forks read from the parent snapshot until new data overwrites. This makes forking essentially free - no data copying required.

## Quick Reference

| Operation       | Function                                | Key Parameters                         |
| --------------- | --------------------------------------- | -------------------------------------- |
| Create snapshot | `createBucketSnapshot(options)`         | name, sourceBucketName                 |
| List snapshots  | `listBucketSnapshots(sourceBucketName)` | sourceBucketName                       |
| Create fork     | `createBucket(name, options)`           | sourceBucketName, sourceBucketSnapshot |

## Create Snapshot

```typescript
import { createBucketSnapshot } from "@tigrisdata/storage";

// Snapshot default bucket
const result = await createBucketSnapshot();
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Snapshot version:", result.data?.snapshotVersion);
  // Output: { snapshotVersion: "1751631910169675092" }
}

// Named snapshot for specific bucket
const result = await createBucketSnapshot("my-bucket", {
  name: "backup-before-migration",
});
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Named snapshot:", result.data?.snapshotVersion);
}
```

**Prerequisite:** Bucket must have `enableSnapshot: true` when created.

## List Snapshots

```typescript
import { listBucketSnapshots } from "@tigrisdata/storage";

// List snapshots for default bucket
const result = await listBucketSnapshots();
if (result.error) {
  console.error("Error:", result.error);
} else {
  console.log("Snapshots:", result.data);
  // [
  //   {
  //     name: "backup-before-migration",
  //     version: "1751631910169675092",
  //     creationDate: Date("2025-01-15T08:30:00Z")
  //   }
  // ]
}

// List snapshots for specific bucket
const result = await listBucketSnapshots("my-bucket");
```

## Create Fork from Snapshot

```typescript
import { createBucket, createBucketSnapshot } from "@tigrisdata/storage";

// First, create a snapshot
const snapshot = await createBucketSnapshot("agent-seed", {
  name: "agent-seed-v1",
});
const snapshotVersion = snapshot.data?.snapshotVersion;

// Fork from snapshot
const agentBucketName = `agent-${Date.now()}`;
const forkResult = await createBucket(agentBucketName, {
  sourceBucketName: "agent-seed",
  sourceBucketSnapshot: snapshotVersion,
});

if (forkResult.error) {
  console.error("Error:", forkResult.error);
} else {
  console.log("Forked bucket created");
  // agent-${timestamp} has all data from agent-seed at snapshot time
  // Can modify/delete freely - agent-seed is unaffected
}
```

## Read from Snapshot Version

Access historical data without forking:

```typescript
import { get, list } from "@tigrisdata/storage";

// Get object as it was at snapshot
const result = await get("config.json", "string", {
  snapshotVersion: "1751631910169675092",
});

// List objects as they were at snapshot
const result = await list({
  snapshotVersion: "1751631910169675092",
});
```

## Deletion Protection in Action

```typescript
import { remove, get } from "@tigrisdata/storage";

// In forked bucket, delete everything
await remove("hello.txt", { config: { bucket: "agent-fork" } });

// Fork appears empty
const forkResult = await get("hello.txt", "string", {
  config: { bucket: "agent-fork" },
});
// forkResult.error === "Not found"

// But source bucket still has data
const sourceResult = await get("hello.txt", "string", {
  config: { bucket: "agent-seed" },
});
// sourceResult.data === "Hello, world!"
```

The fork's deletion only affects the fork. Source data remains accessible in the parent bucket and all snapshots.

## Use Cases

### Developer Sandboxes

```typescript
// Create snapshot of production data
await createBucketSnapshot("production", {
  name: "dev-sandbox-seed",
});

// Fork for each developer
const devBucket = await createBucket(`dev-${developerName}`, {
  sourceBucketName: "production",
  sourceBucketSnapshot: "...",
});
// Developer can test and modify freely
```

### AI Agent Environments

```typescript
// Store agent dependencies in seed bucket
await put("model.bin", modelData);
await put("config.json", agentConfig);

// Snapshot the seed
const snapshot = await createBucketSnapshot("agent-seed", {
  name: "v1",
});

// Spin up new agent instance with fork
const agentBucket = `agent-${Date.now()}`;
await createBucket(agentBucket, {
  sourceBucketName: "agent-seed",
  sourceBucketSnapshot: snapshot.data?.snapshotVersion,
});

// Agent has everything and can modify freely
await startAgent(agentBucket);
```

### Pre-Migration Backups

```typescript
// Before risky operation
await createBucketSnapshot("production", {
  name: "before-migration-v2",
});

// Run migration
// If disaster strikes, fork from snapshot to recover
const rollback = await createBucket("production-restored", {
  sourceBucketName: "production",
  sourceBucketSnapshot: "...",
});
```

## Common Mistakes

| Mistake                                  | Fix                                          |
| ---------------------------------------- | -------------------------------------------- |
| Snapshotting non-snapshot-enabled bucket | Recreate bucket with `enableSnapshot: true`  |
| Expecting fork to affect source          | Forks are isolated - source remains unchanged|
| Not naming snapshots                     | Names make snapshots discoverable            |
| Using wrong storage tier                 | Snapshot buckets must use STANDARD tier      |

## Limitations

- Existing buckets cannot be snapshot-enabled (must create new bucket)
- Snapshot buckets require STANDARD storage tier
- Snapshot buckets don't support lifecycle transitions or TTL

## How It Works (Deep Dive)

A snapshot is a single 64-bit integer representing nanoseconds since Unix epoch. Tigris stores objects with reverse-ordered timestamps, so the most recent version sorts first. When you snapshot, Tigris records the current time. Reading from a snapshot queries for the newest object version before that timestamp.

Forking adds recursive indirection: child bucket objects override the parent, but missing objects recurse through the parent snapshot. This makes forking instant - no data copying, just metadata pointers.

## Prerequisites

Before using snapshots/forking:

1. Install @tigrisdata/storage (see **installing-tigris-storage**)
2. Create bucket with `enableSnapshot: true` (see **tigris-bucket-management**)

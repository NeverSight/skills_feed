---
name: cloudflare-r2
description: "Cloudflare R2 object storage playbook: buckets, Workers Binding API, S3 compatibility, presigned URLs, multipart uploads, CORS, lifecycle policies, event notifications, public buckets, storage classes, data migration. Keywords: Cloudflare R2, object storage, S3 compatible, Workers binding, R2Bucket, presigned URLs, multipart upload, CORS, lifecycle, event notifications, Super Slurper, Sippy, R2 pricing."
---

# Cloudflare R2

R2 is S3-compatible object storage with zero egress fees. Access via Workers Binding API or S3 API.

---

## Quick Start

```bash
npx wrangler r2 bucket create my-bucket
```

```jsonc
// wrangler.jsonc
{
  "r2_buckets": [{ "binding": "MY_BUCKET", "bucket_name": "my-bucket" }]
}
```

```typescript
export interface Env {
  MY_BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const key = new URL(request.url).pathname.slice(1);

    if (request.method === "PUT") {
      await env.MY_BUCKET.put(key, request.body);
      return new Response("Uploaded", { status: 201 });
    }

    if (request.method === "GET") {
      const object = await env.MY_BUCKET.get(key);
      if (!object) return new Response("Not Found", { status: 404 });
      const headers = new Headers();
      object.writeHttpMetadata(headers);
      headers.set("etag", object.httpEtag);
      return new Response(object.body, { headers });
    }
    return new Response("Method Not Allowed", { status: 405 });
  },
};
```

---

## Binding Configuration

```jsonc
{
  "r2_buckets": [
    {
      "binding": "MY_BUCKET",
      "bucket_name": "my-bucket",
      "preview_bucket_name": "my-bucket-preview", // Optional: for local dev
      "jurisdiction": "eu" // Optional: GDPR
    }
  ]
}
```

See [binding.md](references/binding.md) for details.

---

## Workers Binding API (R2Bucket)

| Method                                 | Description                  |
| -------------------------------------- | ---------------------------- |
| `head(key)`                            | Get metadata without body    |
| `get(key, options?)`                   | Get object with body         |
| `put(key, value, options?)`            | Store object                 |
| `delete(key \| keys[])`                | Delete up to 1000 keys       |
| `list(options?)`                       | List objects with pagination |
| `createMultipartUpload(key, options?)` | Start multipart upload       |
| `resumeMultipartUpload(key, uploadId)` | Resume multipart upload      |

### get with range

```typescript
const partial = await env.MY_BUCKET.get("large.bin", {
  range: { offset: 0, length: 1024 },
});
```

### put with metadata

```typescript
await env.MY_BUCKET.put("file.txt", "Hello!", {
  httpMetadata: { contentType: "text/plain" },
  customMetadata: { author: "Alice" },
  storageClass: "InfrequentAccess", // Optional
});
```

### list with pagination

```typescript
const listed = await env.MY_BUCKET.list({ prefix: "images/", limit: 100 });
for (const obj of listed.objects) console.log(obj.key, obj.size);
if (listed.truncated) {
  /* use listed.cursor for next page */
}
```

See [api.md](references/api.md) for complete reference.

---

## R2Object / R2ObjectBody

```typescript
interface R2Object {
  key: string;
  version: string;
  size: number;
  etag: string;
  httpEtag: string;
  uploaded: Date;
  httpMetadata: R2HTTPMetadata;
  customMetadata: Record<string, string>;
  storageClass: "Standard" | "InfrequentAccess";
  writeHttpMetadata(headers: Headers): void;
}

interface R2ObjectBody extends R2Object {
  body: ReadableStream;
  arrayBuffer(): Promise<ArrayBuffer>;
  text(): Promise<string>;
  json<T>(): Promise<T>;
  blob(): Promise<Blob>;
}
```

---

## S3 API Compatibility

Endpoint: `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`

```typescript
import { S3Client } from "@aws-sdk/client-s3";

const S3 = new S3Client({
  region: "auto",
  endpoint: `https://${ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: { accessKeyId: ACCESS_KEY_ID, secretAccessKey: SECRET_ACCESS_KEY },
});
```

**Region**: Always `"auto"` (or `"us-east-1"` alias).

---

## Presigned URLs

```typescript
import { GetObjectCommand, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const downloadUrl = await getSignedUrl(S3, new GetObjectCommand({ Bucket: "my-bucket", Key: "file.pdf" }), { expiresIn: 3600 });

const uploadUrl = await getSignedUrl(S3, new PutObjectCommand({ Bucket: "my-bucket", Key: "file.pdf", ContentType: "application/pdf" }), { expiresIn: 3600 });
```

**Important**: Presigned URLs work only with S3 endpoint (not custom domains). Configure CORS for browser use. See [presigned-urls.md](references/presigned-urls.md).

---

## Multipart Uploads

For objects > 100 MB.

```typescript
const mpu = await env.MY_BUCKET.createMultipartUpload("large.zip");
const part1 = await mpu.uploadPart(1, chunk1); // Min 5 MiB
const part2 = await mpu.uploadPart(2, chunk2);
await mpu.complete([part1, part2]);
// or: await mpu.abort();
```

Resume: `env.MY_BUCKET.resumeMultipartUpload(key, uploadId)`

**Limits**: 5 MiB–5 GiB per part, 10,000 parts max, ~5 TiB max object. See [multipart.md](references/multipart.md).

---

## CORS Configuration

```json
[
  {
    "AllowedOrigins": ["https://example.com"],
    "AllowedMethods": ["GET", "PUT"],
    "AllowedHeaders": ["Content-Type"],
    "ExposeHeaders": ["ETag"],
    "MaxAgeSeconds": 3600
  }
]
```

```bash
npx wrangler r2 bucket cors set my-bucket --file cors.json
```

---

## Lifecycle Policies

```bash
# Delete after 90 days
npx wrangler r2 bucket lifecycle add my-bucket --id "cleanup" --expire-days 90

# Transition to Infrequent Access
npx wrangler r2 bucket lifecycle add my-bucket --id "archive" --transition-days 30 --transition-class STANDARD_IA

# With prefix
npx wrangler r2 bucket lifecycle add my-bucket --id "logs" --prefix "logs/" --expire-days 7

# Abort incomplete multipart
npx wrangler r2 bucket lifecycle add my-bucket --id "mpu" --abort-incomplete-days 1
```

See [lifecycle.md](references/lifecycle.md) for S3 API examples.

---

## Storage Classes

| Class            | Storage   | Notes                           |
| ---------------- | --------- | ------------------------------- |
| Standard         | $0.015/GB | Default                         |
| InfrequentAccess | $0.01/GB  | +$0.01/GB retrieval, 30-day min |

```typescript
await env.MY_BUCKET.put("archive.zip", data, { storageClass: "InfrequentAccess" });
```

---

## Event Notifications

Push to Cloudflare Queues on object changes.

```bash
npx wrangler queues create r2-events
npx wrangler r2 bucket notification create my-bucket --event-type object-create --queue r2-events
```

Events: `object-create`, `object-delete`

```typescript
export default {
  async queue(batch: MessageBatch<R2EventMessage>, env: Env) {
    for (const msg of batch.messages) {
      console.log(`${msg.body.action}: ${msg.body.object.key}`);
      msg.ack();
    }
  },
};
```

---

## Public Buckets

### Custom domain (recommended)

Dashboard → Bucket → Settings → Custom Domains → Add. Enables Cache, WAF, Access.

### r2.dev (dev only)

Dashboard → Bucket → Settings → Public Development URL → Enable.

**Warning**: r2.dev is rate-limited. Use custom domain for production.

---

## Data Migration

### Super Slurper (bulk)

Dashboard → R2 → Data Migration. Copies from S3/GCS/compatible storage. Objects > 1 TB skipped.

### Sippy (incremental)

```bash
npx wrangler r2 bucket sippy enable my-bucket --provider s3 --bucket source --access-key-id <KEY> --secret-access-key <SECRET>
```

Copies on-demand as objects are requested.

---

## Wrangler Commands

```bash
# Bucket
wrangler r2 bucket create|delete|list|info <name>

# Object
wrangler r2 object put|get|delete <bucket>/<key> [--file <path>]

# CORS
wrangler r2 bucket cors set|get|delete <bucket>

# Lifecycle
wrangler r2 bucket lifecycle list|add|remove <bucket>

# Notifications
wrangler r2 bucket notification list|create|delete <bucket>

# Sippy
wrangler r2 bucket sippy enable|disable|get <bucket>
```

---

## Limits

| Parameter           | Limit        |
| ------------------- | ------------ |
| Buckets per account | 1,000,000    |
| Object size         | 5 TiB        |
| Single upload       | 5 GiB        |
| Multipart parts     | 10,000       |
| Key length          | 1,024 bytes  |
| Metadata size       | 8,192 bytes  |
| Delete batch        | 1,000 keys   |
| Lifecycle rules     | 1,000/bucket |
| Notification rules  | 100/bucket   |

---

## Pricing

| Metric    | Standard  | Infrequent Access |
| --------- | --------- | ----------------- |
| Storage   | $0.015/GB | $0.01/GB          |
| Class A   | $4.50/M   | $9.00/M           |
| Class B   | $0.36/M   | $0.90/M           |
| Retrieval | Free      | $0.01/GB          |
| Egress    | **Free**  | **Free**          |

**Free tier**: 10 GB storage, 1M Class A, 10M Class B.

**Class A**: PUT, COPY, LIST, CreateMultipartUpload
**Class B**: GET, HEAD
**Free**: DELETE, AbortMultipartUpload

See [pricing.md](references/pricing.md) for optimization tips.

---

## Conditional Operations

```typescript
const object = await env.MY_BUCKET.get("file.txt", {
  onlyIf: { etagMatches: expectedEtag },
  // or: etagDoesNotMatch, uploadedBefore, uploadedAfter
});

// Or from HTTP headers
const object = await env.MY_BUCKET.get("file.txt", { onlyIf: request.headers });
```

---

## Server-Side Encryption (SSE-C)

```typescript
await env.MY_BUCKET.put("secret.txt", data, { ssecKey: encryptionKey });
const object = await env.MY_BUCKET.get("secret.txt", { ssecKey: encryptionKey });
```

Lost key = lost data.

---

## Prohibitions

- ❌ Do not use r2.dev for production
- ❌ Do not store encryption keys in code
- ❌ Do not skip CORS for browser access
- ❌ Do not ignore multipart limits (5 MiB min)
- ❌ Do not use presigned URLs with custom domains

---

## References

- [binding.md](references/binding.md) — Binding configuration
- [api.md](references/api.md) — Workers API reference
- [presigned-urls.md](references/presigned-urls.md) — Browser integration
- [multipart.md](references/multipart.md) — Large file uploads
- [lifecycle.md](references/lifecycle.md) — Object expiration
- [pricing.md](references/pricing.md) — Cost optimization

## Cross-References

- [cloudflare-workers](../cloudflare-workers/SKILL.md) — Worker development
- [cloudflare-pages](../cloudflare-pages/SKILL.md) — Pages with R2
- [cloudflare-queues](../cloudflare-queues/SKILL.md) — Event consumers
- [cloudflare-d1](../cloudflare-d1/SKILL.md) — SQL database

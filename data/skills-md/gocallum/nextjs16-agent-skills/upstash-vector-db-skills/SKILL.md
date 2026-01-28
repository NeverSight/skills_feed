---
name: upstash-vector-db-skills
description: Upstash Vector DB setup, semantic search, namespaces, and embedding models (MixBread preferred). Use when building vector search features on Vercel.
---

## Links

- Docs: https://upstash.com/docs/vector
- Getting Started: https://upstash.com/docs/vector/overall/getstarted
- Semantic Search Tutorial: https://upstash.com/docs/vector/tutorials/semantic_search
- Namespaces: https://upstash.com/docs/vector/features/namespaces
- Embedding Models: https://upstash.com/docs/vector/features/embeddingmodels
- MixBread AI: https://www.mixbread.ai/ (preferred embedding provider)

## Quick Setup

### 1. Create Vector Index (Upstash Console)

- Go to [Upstash Console](https://console.upstash.com/)
- Create Vector Index: name, region (closest to app), type (Dense for semantic search)
- Select embedding model: **MixBread AI recommended** (or use Upstash built-in models)
- Copy `UPSTASH_VECTOR_REST_URL` and `UPSTASH_VECTOR_REST_TOKEN` to `.env`

### 2. Install SDK

```sh
pnpm add @upstash/vector
```

### 3. Environment

```env
UPSTASH_VECTOR_REST_URL=your_url
UPSTASH_VECTOR_REST_TOKEN=your_token
```

## Code Examples

### Initialize Client (Node.js / TypeScript)

```typescript
import { Index } from "@upstash/vector";

const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN,
});
```

### Upsert Documents (Auto-Embed)

When using an embedding model in the index, text is embedded automatically:

```typescript
// Single document
await index.upsert({
  id: "doc-1",
  data: "Upstash provides serverless vector database solutions.",
  metadata: { source: "docs", category: "intro" },
});

// Batch
await index.upsert([
  { id: "doc-2", data: "Vector search powers semantic similarity.", metadata: { source: "docs" } },
  { id: "doc-3", data: "MixBread AI provides high-quality embeddings.", metadata: { source: "blog" } },
]);
```

### Query / Semantic Search

```typescript
// Semantic search with auto-embedding
const results = await index.query({
  data: "What is semantic search?",
  topK: 5,
  includeMetadata: true,
});

results.forEach((result) => {
  console.log(`ID: ${result.id}, Score: ${result.score}, Metadata:`, result.metadata);
});
```

### Using Namespaces (Data Isolation)

Namespaces partition a single index into isolated subsets. Useful for multi-tenant or multi-domain apps.

```typescript
// Upsert in namespace "blog"
await index.namespace("blog").upsert({
  id: "post-1",
  data: "Next.js tutorial for Vercel deployment",
  metadata: { author: "user-123" },
});

// Query only "blog" namespace
const blogResults = await index.namespace("blog").query({
  data: "Vercel deployment",
  topK: 3,
  includeMetadata: true,
});

// List all namespaces
const namespaces = await index.listNamespaces();
console.log(namespaces);

// Delete namespace
await index.deleteNamespace("blog");
```

### Full Semantic Search Example (Vercel Function)

```typescript
// api/search.ts (Vercel Edge Function or Serverless Function)
import { Index } from "@upstash/vector";

export const config = {
  runtime: "nodejs", // or "edge"
};

const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN,
});

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { query, namespace = "", topK = 5 } = req.body;

  try {
    const searchIndex = namespace ? index.namespace(namespace) : index;
    const results = await searchIndex.query({
      data: query,
      topK,
      includeMetadata: true,
    });

    return res.status(200).json({ results });
  } catch (error) {
    console.error("Search error:", error);
    return res.status(500).json({ error: "Search failed" });
  }
}
```

### Index Operations

```typescript
// Reset (clear all vectors in index or namespace)
await index.reset();

// Or reset a specific namespace
await index.namespace("old-data").reset();

// Delete a single vector
await index.delete("doc-1");

// Delete multiple vectors
await index.delete(["doc-1", "doc-2", "doc-3"]);
```

## Embedding Models

### Available in Upstash

- `BAAI/bge-large-en-v1.5` (1024 dim, best performance, ~64.23 MTEB score)
- `BAAI/bge-base-en-v1.5` (768 dim, good balance)
- `BAAI/bge-small-en-v1.5` (384 dim, lightweight)
- `BAAI/bge-m3` (1024 dim, sparse + dense hybrid)

### Recommended: MixBread AI

If using MixBread as your embedding provider:

1. Create a MixBread API key at https://www.mixbread.ai/
2. When creating your Upstash index, select **MixBread** as the embedding model.
3. MixBread handles tokenization and semantic quality automatically.
4. No extra setup needed in your code; use `index.upsert()` / `index.query()` with text directly.

## Best Practices

### For Vercel Deployment

- Store credentials in Vercel Environment Variables (project settings or `.env.local`).
- Use Edge Functions or Serverless Functions for low-latency access.
- Implement request rate limiting to stay within Upstash quotas.

### Namespace Strategy

- Use namespaces to isolate data by tenant, domain, or use case.
- Example: `namespace("user-123")` for per-user search.
- Clean up old namespaces to avoid storage bloat.

### Query Performance

- Keep `topK` reasonable (5–10 typically sufficient).
- Use metadata filtering to pre-filter results if possible.
- Upstash is eventually consistent; expect slight delays after upserts.

### Error Handling

```typescript
try {
  const results = await index.query({
    data: userQuery,
    topK: 5,
    includeMetadata: true,
  });
} catch (error) {
  if (error.status === 401) {
    console.error("Invalid credentials");
  } else if (error.status === 429) {
    console.error("Rate limited");
  } else {
    console.error("Query error:", error);
  }
}
```

## Common Patterns

### RAG (Retrieval Augmented Generation)

1. Upsert documents / knowledge base into Upstash.
2. On user query, retrieve top-k similar docs via semantic search.
3. Pass retrieved docs + user query to LLM for better context.

```typescript
const docs = await index.query({ data: userQuestion, topK: 3 });
const context = docs.map((d) => d.metadata?.text).join("\n");
// Pass context to LLM
```

### Multi-Tenant Search

Use namespaces to isolate each tenant's vectors:

```typescript
const userNamespace = `tenant-${userId}`;
await index.namespace(userNamespace).upsert({ id, data, metadata });
// Queries only see that tenant's data
```

### Batch Indexing

For bulk imports, upsert in batches:

```typescript
const batchSize = 100;
for (let i = 0; i < documents.length; i += batchSize) {
  const batch = documents.slice(i, i + batchSize);
  await index.upsert(batch);
  console.log(`Indexed batch ${i / batchSize + 1}`);
}
```

## Troubleshooting

- **No results returned**: Ensure documents are indexed and embedding model is active.
- **Slow queries**: Check quota limits; consider upgrading plan or reducing dataset size.
- **Stale data**: Upstash is eventually consistent; wait 1–2 seconds before querying new inserts.
- **Namespace not working**: Ensure namespace exists (created on first upsert) or use the default `""`.

---
name: spice-embeddings
description: Configure embedding models for vector search in Spice (OpenAI, HuggingFace, local). Use when asked to "add embeddings", "configure vector search", "set up semantic search", or "create embedding columns".
---

# Spice Embedding Models

Embedding models transform text into vectors for similarity search and RAG applications.

## Basic Configuration

```yaml
embeddings:
  - from: <provider>:<model_id>
    name: <embedding_name>
    params:
      <provider>_api_key: ${ secrets:API_KEY }
```

## Provider Prefixes

| Provider     | From Format                      | Example                                        |
|--------------|----------------------------------|------------------------------------------------|
| `openai`     | `openai:<model_id>`              | `openai:text-embedding-3-large`                |
| `huggingface`| `huggingface:huggingface.co/...` | `huggingface:huggingface.co/sentence-transformers/all-MiniLM-L6-v2` |
| `azure`      | `azure:<deployment>`             | `azure:my-embedding-deployment`                |
| `bedrock`    | `bedrock:<model_id>`             | `bedrock:amazon.titan-embed-text-v1`           |
| `google`     | `google:<model_id>`              | `google:text-embedding-004`                    |
| `file`       | `file:<path>`                    | `file:./models/embed.safetensors`              |

## Embedding Columns on Datasets

Add vector embeddings to dataset columns for search:

```yaml
embeddings:
  - from: openai:text-embedding-3-small
    name: embed_model
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }

datasets:
  - from: postgres:documents
    name: docs
    acceleration:
      enabled: true
    columns:
      - name: content
        embeddings:
          - from: embed_model
            row_id: id
            chunking:
              enabled: true
              target_chunk_size: 512
```

## Chunking Configuration

For long text, enable chunking to split into smaller segments:

```yaml
columns:
  - name: body
    embeddings:
      - from: embed_model
        chunking:
          enabled: true
          target_chunk_size: 512   # tokens per chunk
          overlap_size: 64         # overlap between chunks
```

## Search API

Query embeddings via the search endpoint:
```bash
curl http://localhost:8090/v1/search \
  -H "Content-Type: application/json" \
  -d '{"datasets": ["docs"], "text": "search query", "limit": 10}'
```

## Documentation

- [Embedding Models Overview](https://spiceai.org/docs/components/embeddings)
- [Embeddings Reference](https://spiceai.org/docs/reference/spicepod/embeddings)
- [Vector Search](https://spiceai.org/docs/features/search/vector-search)
- [Search API](https://spiceai.org/docs/api/HTTP/post-search)

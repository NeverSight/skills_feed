---
name: spice-vectors
description: Configure vector engines for embedding storage in Spice (S3 Vectors). Use when asked to "configure vector storage", "set up S3 vectors", "enable vector engine", or "optimize embedding search".
---

# Spice Vector Engines

Vector engines store and index embeddings for efficient similarity search operations.

## Basic Configuration

```yaml
datasets:
  - from: postgres:documents
    name: docs
    acceleration:
      enabled: true
    vectors:
      enabled: true
      engine: s3_vectors
      params:
        # engine-specific parameters
```

## Supported Engines

| Engine       | Description                           |
|--------------|---------------------------------------|
| `s3_vectors` | Amazon S3 Vectors for cloud storage   |

## Requirements

- Dataset must have acceleration enabled (`acceleration.enabled: true`)
- Dataset must have embedding columns configured

## S3 Vectors Configuration

```yaml
datasets:
  - from: postgres:documents
    name: docs
    acceleration:
      enabled: true
    columns:
      - name: content
        embeddings:
          - from: embed_model
    vectors:
      enabled: true
      engine: s3_vectors
      params:
        s3_vectors_bucket: my-vectors-bucket
        s3_vectors_region: us-east-1
```

## Column Metadata for Vectors

Specify which columns to include in vector storage:

```yaml
columns:
  - name: content
    embeddings:
      - from: embed_model
    metadata:
      vectors: filterable    # or 'non-filterable'
  - name: category
    metadata:
      vectors: filterable    # enable filtering on this column
```

| Metadata Value    | Description                                    |
|-------------------|------------------------------------------------|
| `filterable`      | Store and enable filtering on this column      |
| `non-filterable`  | Store but don't index for filtering            |

## Full Example

```yaml
embeddings:
  - from: openai:text-embedding-3-small
    name: embed_model
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }

datasets:
  - from: postgres:articles
    name: articles
    acceleration:
      enabled: true
      engine: duckdb
    columns:
      - name: body
        embeddings:
          - from: embed_model
            row_id: id
        metadata:
          vectors: non-filterable
      - name: category
        metadata:
          vectors: filterable
    vectors:
      enabled: true
      engine: s3_vectors
      params:
        s3_vectors_bucket: my-bucket
```

## Documentation

- [Vector Engines Overview](https://spiceai.org/docs/components/vectors)
- [S3 Vectors](https://spiceai.org/docs/components/vectors/s3_vectors)
- [Datasets Reference](https://spiceai.org/docs/reference/spicepod/datasets)

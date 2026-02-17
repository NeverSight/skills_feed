---
name: vector-databases
description: Use when "vector database", "embedding storage", "similarity search", "semantic search", "Chroma", "ChromaDB", "FAISS", "Qdrant", "RAG retrieval", "k-NN search", "vector index", "HNSW", "IVF"
version: 1.0.0
---

# Vector Databases

Store and search embeddings for RAG, semantic search, and similarity applications.

## Comparison

| Database | Best For | Filtering | Scale | Managed Option |
|----------|----------|-----------|-------|----------------|
| **Chroma** | Local dev, prototyping | Yes | < 1M | No |
| **FAISS** | Max speed, GPU, batch | No | Billions | No |
| **Qdrant** | Production, hybrid search | Yes | Millions | Yes |
| **Pinecone** | Fully managed | Yes | Billions | Yes (only) |
| **Weaviate** | Hybrid search, GraphQL | Yes | Millions | Yes |

---

## Chroma

Embedded vector database for prototyping. No server needed.

**Strengths**: Zero-config, auto-embedding, metadata filtering, persistent storage
**Limitations**: Not for production scale, single-node only

**Key concept**: Collections hold documents + embeddings + metadata. Auto-embeds text if no vectors provided.

---

## FAISS (Facebook AI)

Pure vector similarity - no metadata, no filtering, maximum speed.

**Index types:**

- **Flat**: Exact search, small datasets (< 10K)
- **IVF**: Inverted file, medium datasets (10K - 1M)
- **HNSW**: Graph-based, good recall/speed tradeoff
- **PQ**: Product quantization, memory efficient for billions

**Strengths**: Fastest, GPU support, scales to billions
**Limitations**: No filtering, no metadata, vectors only

**Key concept**: Choose index based on dataset size. Trade accuracy for speed with approximate search.

---

## Qdrant

Production-ready with rich filtering and hybrid search.

**Strengths**: Payload filtering, horizontal scaling, cloud option, gRPC API
**Limitations**: More complex setup than Chroma

**Key concept**: "Payloads" are metadata attached to vectors. Filter during search, not after.

---

## Index Algorithm Concepts

| Algorithm | How It Works | Trade-off |
|-----------|--------------|-----------|
| **Flat** | Compare to every vector | Perfect recall, slow |
| **IVF** | Cluster vectors, search nearby clusters | Good recall, fast |
| **HNSW** | Graph of neighbors | Best recall/speed ratio |
| **PQ** | Compress vectors | Memory efficient, lower recall |

---

## Decision Guide

| Requirement | Recommendation |
|-------------|----------------|
| Quick prototype | Chroma |
| Metadata filtering | Chroma, Qdrant, Pinecone |
| Billions of vectors | FAISS |
| GPU acceleration | FAISS |
| Production deployment | Qdrant or Pinecone |
| Fully managed | Pinecone |
| On-premise control | Qdrant, Chroma |

## Resources

- Chroma: <https://docs.trychroma.com>
- FAISS: <https://github.com/facebookresearch/faiss>
- Qdrant: <https://qdrant.tech/documentation/>
- Pinecone: <https://docs.pinecone.io>

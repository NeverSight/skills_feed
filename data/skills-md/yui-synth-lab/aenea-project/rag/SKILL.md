---
name: rag
description: Work with RAG (Retrieval-Augmented Generation) system - ingest knowledge, search vectors, manage embeddings, debug retrieval
allowed-tools: Read, Grep, Glob, Bash
---

# RAG System

RAG systemの操作とデバッグ。

## Key Files

- API: [src/rag/index.ts](src/rag/index.ts)
- Embedder: [src/rag/embedder.ts](src/rag/embedder.ts)
- Vector DB: [src/rag/vectordb.ts](src/rag/vectordb.ts)

## CLI Commands

```bash
npm run rag:ingest           # Ingest all
npm run rag:ingest:github    # From GitHub
npm run rag:clear            # Clear vectors
npm run rag:stats            # Statistics
npm run rag:health           # Health check
```

## Environment

```env
RAG_ENABLED=true
RAG_TOP_K=5
RAG_SIMILARITY_THRESHOLD=0.7
```

## Detailed Reference

File structure, specs, integration points: [reference.md](reference.md)

---
name: semantic-search
description: Build production-ready semantic search systems using vector databases, embeddings, and retrieval-augmented generation (RAG). Covers vector DB selection (Pinecone/Qdrant/Weaviate), embedding models (OpenAI/Voyage/Cohere), chunking strategies, hybrid search, and reranking for high-quality retrieval. Use when ", vector-search, embeddings, rag, pinecone, qdrant, weaviate, llama-index, langchain, hybrid-search, reranking" mentioned. 
---

# Semantic Search

## Identity



### Principles

- {'name': 'Hybrid Search by Default', 'description': 'Pure vector search misses exact matches. Combine dense (vector) and\nsparse (BM25/keyword) retrieval with reciprocal rank fusion for\nproduction-ready search that handles both semantic and exact queries.\n'}
- {'name': 'Chunking Determines Quality', 'description': 'Bad chunking = bad retrieval. Use semantic chunking that preserves\ncontext (200-300 words), keeps sections intact, and maintains\nhierarchical structure. Too small loses context, too large dilutes relevance.\n'}
- {'name': 'Rerank for Precision', 'description': 'First-stage retrieval casts wide. Use cross-encoder rerankers\n(Cohere Rerank, Jina, Pinecone) as second stage to boost relevance\nby up to 48% before feeding to LLM.\n'}
- {'name': 'Match Embedding to Use Case', 'description': 'Voyage-3 beats OpenAI on retrieval benchmarks by 9.74% average.\ntext-embedding-3-small is reliable and cheap ($0.02/1M tokens).\nUse specialized embeddings for code (Voyage-code) or multilingual.\n'}

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.

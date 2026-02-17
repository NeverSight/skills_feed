---
name: rag-frameworks
description: Use when "RAG", "retrieval augmented generation", "LangChain", "LlamaIndex", "sentence transformers", "embeddings", "document QA", "chatbot with documents", "semantic search"
version: 1.0.0
---

# RAG Frameworks

Frameworks for building retrieval-augmented generation applications.

## Comparison

| Framework | Best For | Learning Curve | Flexibility |
|-----------|----------|----------------|-------------|
| **LangChain** | Agents, chains, tools | Steeper | Highest |
| **LlamaIndex** | Data indexing, simple RAG | Gentle | Medium |
| **Sentence Transformers** | Custom embeddings | Low | High |

---

## LangChain

Orchestration framework for building complex LLM applications.

**Core concepts:**

- **Chains**: Sequential operations (retrieve → prompt → generate)
- **Agents**: LLM decides which tools to use
- **LCEL**: Declarative pipeline syntax with `|` operator
- **Retrievers**: Abstract interface to vector stores

**Strengths**: Rich ecosystem, many integrations, agent capabilities
**Limitations**: Abstractions can be confusing, rapid API changes

**Key concept**: LCEL (LangChain Expression Language) for composable pipelines.

---

## LlamaIndex

Data framework focused on connecting LLMs to external data.

**Core concepts:**

- **Documents → Nodes**: Automatic chunking and indexing
- **Index types**: Vector, keyword, tree, knowledge graph
- **Query engines**: Retrieve and synthesize answers
- **Chat engines**: Stateful conversation over data

**Strengths**: Simple API, great for document QA, data connectors
**Limitations**: Less flexible for complex agent workflows

**Key concept**: "Load data, index it, query it" - simpler mental model than LangChain.

---

## Sentence Transformers

Generate high-quality embeddings for semantic similarity.

**Popular models:**

| Model | Dimensions | Quality | Speed |
|-------|------------|---------|-------|
| all-MiniLM-L6-v2 | 384 | Good | Fast |
| all-mpnet-base-v2 | 768 | Better | Medium |
| e5-large-v2 | 1024 | Best | Slow |

**Key concept**: Bi-encoder architecture - encode query and documents separately, compare with cosine similarity.

---

## RAG Architecture Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Naive RAG** | Retrieve top-k, stuff in prompt | Simple QA |
| **Parent-Child** | Retrieve chunks, return parent docs | Context preservation |
| **Hybrid Search** | Vector + keyword search | Better recall |
| **Re-ranking** | Retrieve many, re-rank with cross-encoder | Higher precision |
| **Query Expansion** | Generate variations of query | Ambiguous queries |

---

## Decision Guide

| Scenario | Recommendation |
|----------|----------------|
| Simple document QA | LlamaIndex |
| Complex agents/tools | LangChain |
| Custom embedding pipeline | Sentence Transformers |
| Production RAG | LangChain or custom |
| Quick prototype | LlamaIndex |
| Maximum control | Build custom with Sentence Transformers |

## Resources

- LangChain: <https://python.langchain.com>
- LlamaIndex: <https://docs.llamaindex.ai>
- Sentence Transformers: <https://sbert.net>

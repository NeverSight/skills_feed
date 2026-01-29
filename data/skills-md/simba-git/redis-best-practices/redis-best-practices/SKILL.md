---
name: redis-best-practices
description: Redis performance optimization and best practices. Use this skill when working with Redis data structures, Redis Query Engine (RQE), vector search with RedisVL, semantic caching with LangCache, or optimizing Redis performance.
license: MIT
metadata:
  author: redis
  version: "1.0.0"
---

# Redis Best Practices

Comprehensive performance optimization guide for Redis, including Redis Query Engine, vector search, and semantic caching. Contains rules across 11 categories, prioritized by impact to guide automated optimization and code generation.

## When to Apply

Reference these guidelines when:
- Designing Redis data models and key structures
- Implementing caching, sessions, or real-time features
- Using Redis Query Engine (FT.CREATE, FT.SEARCH, FT.AGGREGATE)
- Building vector search or RAG applications with RedisVL
- Implementing semantic caching with LangCache
- Optimizing Redis performance and memory usage

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Data Structures & Keys | HIGH | `data-` |
| 2 | Memory & Expiration | HIGH | `ram-` |
| 3 | Connection & Performance | HIGH | `conn-` |
| 4 | JSON Documents | MEDIUM | `json-` |
| 5 | Redis Query Engine | HIGH | `rqe-` |
| 6 | Vector Search & RedisVL | HIGH | `vector-` |
| 7 | Semantic Caching | MEDIUM | `semantic-cache-` |
| 8 | Streams & Pub/Sub | MEDIUM | `stream-` |
| 9 | Clustering & Replication | MEDIUM | `cluster-` |
| 10 | Security | HIGH | `security-` |
| 11 | Observability | MEDIUM | `observe-` |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/rqe-index-creation.md
rules/vector-rag-pattern.md
```

Each rule file contains:
- Brief explanation of why it matters
- Avoid example with explanation
- Recommended example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

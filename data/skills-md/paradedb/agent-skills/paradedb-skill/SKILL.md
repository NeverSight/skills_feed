---
name: paradedb-skill
description: Expert guidance on ParadeDB full-text search, hybrid search (BM25 + semantic), aggregations, and analytics in Postgres. Use when writing ParadeDB queries, creating BM25 indexes, configuring tokenizers, or implementing Elasticsearch-quality search in PostgreSQL.
---

# ParadeDB Skill

ParadeDB brings Elasticsearch-like full-text search and analytics to PostgreSQL using the `pg_search` extension. It provides BM25 ranking, advanced tokenizers, aggregations, and real-time indexing with ACID compliance.

**Key capabilities:** Full-text search with BM25 relevance scoring, hybrid search (keyword + semantic embeddings via pgvector), tokenization and analyzer configuration, fuzzy matching, phrase queries, faceted search, sorting, snippets and highlighting, and Tantivy-powered performance.

For complete and up-to-date ParadeDB documentation, always fetch:

**https://docs.paradedb.com/llms-full.txt**

This contains the full documentation optimized for LLMs. Use `read_web_page` or equivalent to fetch current docs before answering ParadeDB questions.

## Network Failure Rules (Mandatory)

If `llms-full.txt` (or any required docs URL) cannot be fetched due to DNS/network/access errors:

1. State clearly that live docs could not be accessed and include the actual error.
2. Ask the user whether to proceed with local/repo-only context or to retry later.
3. Do **not** invent or infer doc URLs, page paths, or feature availability.
4. Do **not** present unverified links as real.
5. Label any fallback statements as assumptions and keep them minimal.

Never silently switch to guessed documentation structure when network access fails.

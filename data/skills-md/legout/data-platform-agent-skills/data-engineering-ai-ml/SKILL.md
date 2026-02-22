---
name: data-engineering-ai-ml
description: "AI/ML data pipelines: embedding generation, vector databases, RAG patterns, LLM monitoring, and batch inference workflows."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-remote-access"]
---

# AI/ML Data Pipelines

Data engineering patterns for AI/ML workloads: embedding generation, vector databases, retrieval-augmented generation (RAG), LLM output monitoring, and batch inference. Covers LanceDB, pgvector, and OpenAI integrations.

## When to Use These Patterns?

- **RAG Applications**: Building chatbots, semantic search, question-answering
- **LLM Monitoring**: Tracking token usage, latency, output quality
- **Embedding Pipelines**: Generating and storing vector embeddings for ML models
- **Batch Inference**: Large-scale model inference pipelines
- **Feature Stores**: Versioned feature data for ML training/serving

## Skill Dependencies

- `@data-engineering-core` - Polars, DuckDB for data processing
- `@data-engineering-storage-remote-access` - Cloud storage for embeddings and models
- `@data-engineering-orchestration` - Schedule/batch embedding generation
- `@data-engineering-quality` - Validate embedding quality

---

## Detailed Guides

### Embeddings
See: `@data-engineering-ai-ml/embeddings.md`

- OpenAI embeddings API
- Sentence Transformers (local models)
- Batch processing with Polars
- Chunking strategies for text
- Token counting with tiktoken

### Vector Databases
See: `@data-engineering-ai-ml/vector-databases.md`

- **LanceDB**: Embedded, Arrow-native, scales from local to cloud
- **pgvector**: PostgreSQL extension, ACID transactions
- **DuckDB**: List type for simple cosine similarity
- Indexing strategies (IVF_PQ, HNSW)

### RAG Pipelines
See: `@data-engineering-ai-ml/rag-pipelines.md`

- Document chunking (by tokens, paragraphs, semantic)
- Context assembly with token budget
- Retrieval: vector search + metadata filters
- Prompt construction and LLM invocation
- Source attribution

### LLM Monitoring
See: `@data-engineering-ai-ml/monitoring.md`

- Tracking API calls, costs, latencies
- Prompt caching and deduplication
- Error tracking and retry logic
- Quality evaluation (human + automated)

---

## Quick Start: Complete RAG Pipeline

```python
import polars as pl
import lancedb
from sentence_transformers import SentenceTransformer

# 1. Generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
df = pl.read_parquet("documents.parquet")
df = df.with_columns([
    pl.Series("embedding", model.encode(df["text"].to_list()).tolist())
])

# 2. Store in LanceDB
db = lancedb.connect("./.lancedb")
table = db.create_table("documents", df.to_arrow())
table.create_index(
    vector_column_name="embedding",
    metric="cosine",
    index_type="IVF_PQ",
    num_partitions=256,
    num_sub_vectors=96
)

# 3. Query
query_embedding = model.encode(["What is RAG?"])[0]
results = (
    table.search(query_embedding)
    .where("category = 'tech'")
    .limit(5)
    .to_pandas()
)

print(f"Top result: {results.iloc[0]['text'][:200]}...")
```

---

## Common Patterns

### Batch Embedding Generation
```python
from sentence_transformers import SentenceTransformer
import polars as pl

model = SentenceTransformer('all-MiniLM-L6-v2')

# Process in batches to avoid OOM
batch_size = 1000
reader = pl.read_csv_batched("large_corpus.csv", batch_size=batch_size)

embeddings = []
while (batches := reader.next_batches(1)):
    for batch in batches:
        batch_embeddings = model.encode(batch["text"].to_list())
        embeddings.extend(batch_embeddings)

df = batch.with_columns(pl.Series("embedding", embeddings))
df.write_parquet("corpus_with_embeddings.parquet")
```

### Vector Search with Filtering
```python
import lancedb

db = lancedb.connect("./.lancedb")
table = db.open_table("documents")

# Hybrid search: vector + metadata filter
results = (
    table.search(query_embedding)
    .where("date >= '2024-01-01' AND category IN ('tech', 'science')")
    .select(["id", "text", "date"])  # Only return needed columns
    .limit(10)
    .to_arrow()
)
```

### Cost Monitoring for LLMs
```python
import duckdb
from datetime import datetime

class LLMMonitor:
    def __init__(self, duckdb_path="llm_monitoring.db"):
        self.conn = duckdb.connect(duckdb_path)
        self._init_table()

    def _init_table(self):
        self.conn.sql("""
            CREATE TABLE IF NOT EXISTS calls (
                call_id VARCHAR PRIMARY KEY,
                timestamp TIMESTAMP,
                model VARCHAR,
                prompt_tokens INTEGER,
                completion_tokens INTEGER,
                total_tokens INTEGER,
                cost_usd DOUBLE,
                latency_ms INTEGER
            )
        """)

    def log_call(self, model: str, prompt_tokens: int, completion_tokens: int, latency_ms: int):
        # Approximate cost calculation (update with real pricing)
        cost_per_1k = {
            "gpt-4o": 0.005,
            "text-embedding-3-small": 0.00002
        }.get(model, 0.001)

        total_cost = (prompt_tokens + completion_tokens) / 1000 * cost_per_1k
        call_id = f"{datetime.now().timestamp():.6f}-{model}"

        self.conn.sql("""
            INSERT INTO calls VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            call_id,
            datetime.now().isoformat(),
            model,
            prompt_tokens,
            completion_tokens,
            prompt_tokens + completion_tokens,
            total_cost,
            latency_ms
        ])

monitor = LLMMonitor()
monitor.log_call("gpt-4o", 100, 50, 1200)
```

---

## Best Practices

1. ✅ **Batch embedding generation** - Use batch API calls, not one-by-one
2. ✅ **Index after bulk load** - Build vector indexes on full dataset, not incremental
3. ✅ **Use appropriate embedding dimensions** - Smaller = cheaper/faster, larger = more accurate
4. ✅ **Monitor token usage** - Track costs, set quotas
5. ✅ **Cache prompts & results** - Avoid duplicate API calls
6. ✅ **Human evaluation** - Automated metrics (cosine similarity) ≠ quality
7. ❌ **Don't** store embeddings without metadata - need source attribution
8. ❌ **Don't** use cosine similarity for multi-modal vectors - use L2 or dot product
9. ❌ **Don't** skip chunking - Very long documents need splitting for embeddings

---

## Performance Tips

- **Embedding models**: Run locally for privacy/offline, or OpenAI for convenience
- **Vector DB**: LanceDB for embedded use; pgvector for transactional; specialized (Pinecone, Weaviate) for scale
- **Index tuning**: IVF_PQ for disk efficiency, HNSW for recall
- **Query parameters**: Tune `nprobes` (accuracy) and `refine_factor` (reranking) based on latency/recall tradeoff

---

## References

- [LanceDB Documentation](https://lancedb.github.io/lancedb/)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- `@data-engineering-storage-lakehouse` - Versioned storage for models/embeddings

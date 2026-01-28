---
name: leann
description: Local RAG indexing with 97% storage reduction via anchor-based lazy recomputation. Graph-based selective embedding storage for memory-efficient semantic code search.
version: 1.0.0
triggers:
  - keywords: [leann, semantic search, code index, RAG, vector search, embedding index, anchor graph]
  - context: [indexing large codebases, memory-efficient search, local code search, production RAG]
  - file_patterns: [leann.config.json, leann.index, .leann/]
tags: [rag, vector-search, graph, compression, local-first, semantic-search]
---

# LEANN Skill

**LEANN (Learned Embedding ANchor Navigation)** - A graph-based selective recomputation system achieving 97% storage reduction for local RAG indexes while maintaining fast retrieval performance.

---

## Core Principle

**Use leann for persistent local code indexes with minimal storage overhead.**

Instead of storing all embeddings at full precision (3 GB for 1M files), leann stores only strategic anchors and reconstructs others on-demand (128 MB for same dataset - **95.8% reduction**).

---

## When to Use LEANN

### Primary Use Cases

**1. Large Codebase Indexing (10K+ files)**
- Monorepos with multiple services
- Enterprise codebases that exceed vector database free tiers
- Projects requiring fast local semantic search without cloud dependencies

**2. Memory-Constrained Environments**
- Development machines with limited RAM
- CI/CD pipelines needing index validation
- Edge deployments or air-gapped systems

**3. Cost-Sensitive RAG Applications**
- Avoiding Pinecone/Weaviate monthly costs
- Self-hosted vector search with minimal infrastructure
- Batch processing of large document collections

**4. Real-Time Code Navigation**
- IDE integrations for semantic code search
- Developer tools needing instant relevance feedback
- Documentation search within editors

### When NOT to Use LEANN

**Use traditional vector DBs instead when:**
- Dataset is small (<1K items) - overhead not worth it
- Cloud infrastructure is required (multi-tenant, global CDN)
- Need advanced features (hybrid search, filtering, multi-tenancy)
- Absolute lowest latency required (<5ms) - leann trades latency for storage

---

## Architecture Overview

### Two-Stage Query Process

```
Query → [Stage 1: Anchor Graph Search] → [Stage 2: Lazy Reconstruction] → Results

Stage 1: Fast HNSW/DiskANN traversal (1-5ms)
Stage 2: Reconstruct top candidates (5-25ms)
Total: 10-30ms (HNSW) or 50-200ms (DiskANN)
```

### Storage Model

```
Naive:  N × D × 4 bytes (full embeddings)
LEANN:  M × D × 4 + N × (D / 8) bytes (anchors + compressed deltas)

Example (100K files, 768 dims):
Naive:  100,000 × 768 × 4     = 307 MB
LEANN:  1,000 × 768 × 4       = 3 MB (anchors)
        100,000 × 96          = 9.6 MB (deltas)
        Total                 ≈ 12.6 MB (95.9% reduction)
```

### Key Components

1. **Anchor Graph:** HNSW (in-memory) or DiskANN (disk-based) graph of anchor embeddings
2. **Product Quantization:** Compress delta vectors (delta = embedding - anchor)
3. **ZMQ Embedding Server:** GPU-accelerated embedding generation
4. **Delta Index:** Incremental updates without full rebuild

---

## Quick Start

### 1. Installation

```bash
# Via pip
pip install leann

# Via conda
conda install -c conda-forge leann

# From source
git clone https://github.com/leann-index/leann.git
cd leann && pip install -e .
```

### 2. Start Embedding Server

```bash
# Docker (recommended - GPU support)
docker run -d \
  --name leann-embeddings \
  --gpus all \
  -p 5555:5555 \
  -e MODEL=sentence-transformers/all-MiniLM-L6-v2 \
  leann/embedding-server:latest

# Python script (alternative)
python -m leann.server \
  --model sentence-transformers/all-MiniLM-L6-v2 \
  --port 5555 \
  --device cuda
```

### 3. Create Index

```bash
# Basic indexing
leann index create \
  --input /path/to/codebase \
  --output ./leann.index \
  --config leann.config.json

# With progress tracking
leann index create \
  --input /path/to/codebase \
  --output ./leann.index \
  --progress \
  --verbose
```

### 4. Query Index

```bash
# CLI query
leann query \
  --index ./leann.index \
  --query "JWT authentication middleware" \
  --top-k 10

# Watch mode (live updates)
leann serve \
  --index ./leann.index \
  --watch \
  --port 8080
```

---

## Configuration

### Minimal Configuration

```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 300
  },
  "quantization": {
    "subVectors": 96,
    "codebookSize": 256
  },
  "embeddingServer": {
    "endpoint": "tcp://localhost:5555",
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "batchSize": 128,
    "timeout": 30000
  }
}
```

### Production Configuration

```json
{
  "backend": "hnsw",
  "complexity": "high",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 1000,
    "samples": 20000
  },
  "quantization": {
    "subVectors": 96,
    "codebookSize": 256,
    "trainingSamples": 50000
  },
  "embeddingServer": {
    "endpoint": "tcp://localhost:5555",
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "batchSize": 256,
    "timeout": 60000
  },
  "incremental": {
    "enabled": true,
    "deltaIndexThreshold": 1000,
    "rebuildSchedule": "0 2 * * *"
  },
  "hnsw": {
    "M": 32,
    "efConstruction": 400,
    "efSearch": 200
  }
}
```

### Configuration Parameters

#### Backend Selection

**`backend: "hnsw"` (In-Memory)**
- Use when index fits in RAM
- Query latency: 10-30ms
- Suitable for: <1M files, <50K anchors

**`backend: "diskann"` (Disk-Based)**
- Use when index exceeds RAM
- Query latency: 50-200ms
- Suitable for: 1M+ files, massive monorepos

#### Complexity Levels

| Level | M | efConstruction | efSearch | Build Time | Accuracy |
|-------|---|----------------|----------|------------|----------|
| low | 12 | 100 | 50 | Fast | Good |
| medium | 16 | 200 | 100 | Moderate | Better |
| high | 32 | 400 | 200 | Slow | Best |

#### Anchor Selection Strategies

**1. Random (Fastest)**
```json
{
  "type": "random",
  "count": 300
}
```
- Speed: O(N)
- Quality: Acceptable for homogeneous codebases
- Use when: Prototyping or single-language projects

**2. K-Means (Recommended)**
```json
{
  "type": "kmeans",
  "clusters": 300,
  "samples": 10000
}
```
- Speed: O(N × k × iterations)
- Quality: Excellent coverage
- Use when: Production deployments (default)

**3. Max-Coverage (Best Quality)**
```json
{
  "type": "max-coverage",
  "count": 300,
  "diversityThreshold": 0.2
}
```
- Speed: O(N × M²)
- Quality: Best for sparse distributions
- Use when: High-value outliers must be findable

---

## Common Workflows

### Workflow 1: Initial Indexing

```bash
# 1. Discover codebase
find /path/to/codebase -type f \( -name "*.py" -o -name "*.ts" \) | wc -l
# Output: 15,000 files

# 2. Calculate recommended anchors
# Rule: M = √N → √15000 ≈ 122 → recommend 300 for better coverage

# 3. Create config
cat > leann.config.json <<EOF
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 300,
    "samples": 5000
  },
  "quantization": {
    "subVectors": 96,
    "codebookSize": 256
  },
  "embeddingServer": {
    "endpoint": "tcp://localhost:5555",
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "batchSize": 128,
    "timeout": 30000
  }
}
EOF

# 4. Build index
leann index create \
  --config leann.config.json \
  --input /path/to/codebase \
  --output ./leann.index \
  --progress

# 5. Validate
leann index validate ./leann.index

# 6. Test query
leann query \
  --index ./leann.index \
  --query "database connection pooling" \
  --top-k 5
```

### Workflow 2: CI/CD Integration

```yaml
# .github/workflows/update-index.yml
name: Update LEANN Index

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * 0'  # Weekly full rebuild

jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup LEANN
        run: |
          pip install leann
          docker run -d -p 5555:5555 leann/embedding-server:latest

      - name: Incremental Update
        run: |
          leann index update \
            --index ./leann.index \
            --git-diff origin/main HEAD \
            --output ./leann-updated.index

      - name: Validate Index
        run: |
          leann index validate ./leann-updated.index
          if [ $? -ne 0 ]; then
            # Validation failed - trigger full rebuild
            leann index create \
              --config leann.config.json \
              --input . \
              --output ./leann-updated.index
          fi

      - name: Upload Artifact
        uses: actions/upload-artifact@v3
        with:
          name: leann-index
          path: ./leann-updated.index
```

### Workflow 3: IDE Integration

```python
# VS Code extension example
from leann import LEANNIndex

class SemanticSearchProvider:
    def __init__(self, index_path):
        self.index = LEANNIndex.load(index_path)

    def search(self, query, top_k=10):
        results = self.index.query(
            query=query,
            top_k=top_k,
            mode='retrieve',
            filters={'languages': ['python', 'typescript']}
        )
        return [
            {
                'path': item.item.path,
                'score': item.score,
                'preview': self._get_preview(item.item)
            }
            for item in results.items
        ]
```

### Workflow 4: Polyglot Codebase

```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "stratified-kmeans",
    "totalClusters": 500,
    "stratification": {
      "enabled": true,
      "groupBy": "language",
      "minPerGroup": 20,
      "allocation": "proportional"
    }
  },
  "filters": {
    "languages": ["python", "typescript", "go", "rust"],
    "excludePaths": ["node_modules/", "__pycache__/", "vendor/", "target/"]
  }
}
```

**Benefit:** Ensures each language gets proportional representation in anchors, preventing Python from dominating a Python/TypeScript/Go codebase.

---

## Performance Tuning

### Query Latency Optimization

**Problem:** Queries taking >50ms

**Diagnosis:**
```bash
leann index stats ./leann.index

# Check:
# - Avg candidates evaluated (should be <1000)
# - efSearch parameter (default: 100)
```

**Solutions:**

1. **Reduce efSearch** (faster, lower recall)
```json
{
  "hnsw": {
    "efSearch": 50
  }
}
```

2. **Increase anchor count** (more memory, better coverage)
```bash
leann index rebuild \
  --index ./leann.index \
  --new-anchor-count 1000 \
  --output ./leann-improved.index
```

3. **Use early termination**
```bash
leann query \
  --index ./leann.index \
  --query "authentication" \
  --top-k 10 \
  --early-terminate \
  --confidence-threshold 0.9
```

### Storage Optimization

**Problem:** Index larger than expected

**Diagnosis:**
```bash
leann index stats ./leann.index

# Check:
# - Anchor count (should be ~√N)
# - PQ configuration (96 subvectors × 256 codebook is standard)
```

**Solutions:**

1. **Reduce anchor count** (lower quality, less storage)
```json
{
  "anchorSelection": {
    "clusters": 100  // Reduced from 300
  }
}
```

2. **Increase PQ compression** (lower quality, less storage)
```json
{
  "quantization": {
    "subVectors": 128,  // More aggressive compression
    "codebookSize": 128
  }
}
```

### Accuracy Improvement

**Problem:** Poor retrieval relevance

**Diagnosis:**
```bash
leann index validate ./leann.index --verbose

# Check:
# - Coverage score (target: >0.80)
# - Quantization error (target: <0.05)
```

**Solutions:**

1. **Increase anchor count**
```bash
leann index rebuild \
  --index ./leann.index \
  --new-anchor-count 1000 \
  --output ./leann-improved.index
```

2. **Use k-means selection** (better than random)
```json
{
  "anchorSelection": {
    "type": "kmeans",  // Changed from "random"
    "clusters": 500
  }
}
```

3. **Enable re-ranking with cross-encoder**
```bash
leann query \
  --index ./leann.index \
  --query "authentication middleware" \
  --mode rerank \
  --top-k 10
```

---

## Monitoring & Health

### Key Metrics

**1. Coverage Score** (target: >0.80)
```bash
leann index validate ./leann.index --metric coverage
```
Measures how uniformly anchors cover embedding space.

**2. Quantization Error** (target: <0.05)
```bash
leann index validate ./leann.index --metric quantization
```
Measures average reconstruction error from PQ compression.

**3. Utilization Balance** (target: >0.70)
```bash
leann index validate ./leann.index --metric balance
```
Checks if anchors are evenly utilized (no overloaded anchors).

### Rebuild Triggers

Automatic rebuild when:
- Coverage score drops below 0.70
- Delta index exceeds threshold (default: 10% of main index)
- Query latency degrades >30% from baseline
- Manual trigger: `leann index rebuild`

### Health Check Script

```bash
#!/bin/bash
# scripts/index-validator.sh

INDEX="./leann.index"

echo "LEANN Index Health Check"
echo "========================"

# Check coverage
COVERAGE=$(leann index validate $INDEX --metric coverage --json | jq -r '.score')
echo "Coverage: $COVERAGE (target: >0.80)"

# Check quantization error
QUANT_ERROR=$(leann index validate $INDEX --metric quantization --json | jq -r '.error')
echo "Quantization Error: $QUANT_ERROR (target: <0.05)"

# Check balance
BALANCE=$(leann index validate $INDEX --metric balance --json | jq -r '.score')
echo "Balance: $BALANCE (target: >0.70)"

# Check delta index size
DELTA_SIZE=$(leann index stats $INDEX --json | jq -r '.deltaIndexSize')
MAIN_SIZE=$(leann index stats $INDEX --json | jq -r '.mainIndexSize')
DELTA_RATIO=$(echo "scale=2; $DELTA_SIZE / $MAIN_SIZE * 100" | bc)
echo "Delta Index: $DELTA_RATIO% of main (rebuild at 10%)"

# Recommend actions
if (( $(echo "$COVERAGE < 0.70" | bc -l) )); then
  echo "⚠️  WARNING: Coverage too low - consider rebuilding with more anchors"
fi

if (( $(echo "$QUANT_ERROR > 0.05" | bc -l) )); then
  echo "⚠️  WARNING: High quantization error - consider reducing PQ compression"
fi

if (( $(echo "$DELTA_RATIO > 10" | bc -l) )); then
  echo "⚠️  WARNING: Delta index large - recommend full rebuild"
fi
```

---

## Integration Patterns

### Pattern 1: Python API

```python
from leann import LEANNIndex, QueryRequest

# Load index
index = LEANNIndex.load('./leann.index')

# Basic query
results = index.query(
    query="database connection pooling",
    top_k=10,
    mode='retrieve'
)

for item in results.items:
    print(f"{item.item.path} (score: {item.score:.2f})")
    print(f"  {item.preview}\n")

# Query with filters
results = index.query(
    query="authentication middleware",
    top_k=5,
    filters={
        'languages': ['typescript'],
        'paths': ['src/middleware/*.ts']
    }
)

# Batch queries
queries = [
    "JWT authentication",
    "database migration",
    "error handling"
]
results_batch = index.batch_query(queries, top_k=5)
```

### Pattern 2: REST API

```python
from fastapi import FastAPI
from leann import LEANNIndex

app = FastAPI()
index = LEANNIndex.load('./leann.index')

@app.post('/search')
async def search(query: str, top_k: int = 10):
    results = index.query(query=query, top_k=top_k)
    return {
        'results': [
            {
                'path': item.item.path,
                'score': item.score,
                'preview': item.preview
            }
            for item in results.items
        ],
        'latency': results.latency
    }

@app.get('/health')
async def health():
    stats = index.get_stats()
    return {
        'status': 'healthy' if stats.healthScore > 70 else 'degraded',
        'healthScore': stats.healthScore,
        'indexSize': stats.storageSize,
        'avgLatency': stats.avgLatency
    }
```

### Pattern 3: CLI Tool

```bash
#!/bin/bash
# Wrapper script for common queries

function search() {
  leann query \
    --index ~/.cache/leann/project.index \
    --query "$1" \
    --top-k "${2:-10}" \
    --format json | jq -r '.items[] | "\(.item.path):\(.item.startLine)"'
}

function update-index() {
  leann index update \
    --index ~/.cache/leann/project.index \
    --watch \
    --auto-rebuild
}

# Usage:
# search "database connection" 5
# update-index
```

---

## Troubleshooting

### Issue: Out of Memory During Indexing

**Error:**
```
Cannot allocate memory for k-means clustering
```

**Solution:**
Reduce sampling in anchor selection:

```json
{
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 300,
    "samples": 5000  // Reduced from 10000
  }
}
```

### Issue: Embedding Server Connection Failed

**Error:**
```
Connection refused: tcp://localhost:5555
```

**Solution:**
```bash
# Check if server is running
docker ps | grep leann-embeddings

# If not, start it
docker run -d -p 5555:5555 leann/embedding-server:latest

# Test connection
curl http://localhost:5555/health
```

### Issue: Low Query Accuracy

**Error:**
```
Results not relevant to query
```

**Diagnosis:**
```bash
leann index validate ./leann.index --verbose
# Check coverage score and quantization error
```

**Solution:**
```bash
# Rebuild with more anchors and k-means selection
leann index rebuild \
  --index ./leann.index \
  --anchor-strategy kmeans \
  --anchor-count 1000 \
  --output ./leann-improved.index
```

---

## Resources

**Codebase Documentation:**
- Type definitions: `@architect/leann-codebase/types/core.ts`
- Anchor selection principles: `@architect/leann-codebase/principles/anchor-selection.md`
- Graph navigation: `@architect/leann-codebase/principles/graph-navigation.md`
- Indexing workflows: `@architect/leann-codebase/templates/indexing-workflow.md`

**References:**
- Quick commands: `@architect/leann/assets/cheatsheet.md`
- Indexing patterns: `@architect/leann/references/indexing-patterns.md`
- Configuration guide: `@architect/leann/references/configuration.md`

**External:**
- GitHub: https://github.com/leann-index/leann
- Documentation: https://leann-index.github.io
- Paper: "LEANN: Learned Embedding Anchor Navigation"

---

## Summary

**Core Value Proposition:**
- 97% storage reduction vs traditional vector databases
- 10-30ms query latency (local, no network overhead)
- Zero cloud costs (self-hosted)
- Incremental updates (no nightly rebuilds)

**Best For:**
- Large codebases (10K+ files)
- Memory-constrained environments
- Cost-sensitive RAG applications
- Local-first semantic search

**Decision Tree:**

```
Need semantic code search?
├─ Dataset < 1K items → Use simple vector DB (overhead not worth it)
└─ Dataset > 1K items
    ├─ Cloud infrastructure required → Use Pinecone/Weaviate
    └─ Local-first / cost-sensitive → Use LEANN
        ├─ Index < RAM → HNSW backend (10-30ms)
        └─ Index > RAM → DiskANN backend (50-200ms)
```

**Golden Rules:**
1. Start with medium complexity, increase only if needed
2. Use k-means anchor selection for production
3. Monitor coverage score - rebuild if <0.70
4. Enable incremental updates for CI/CD
5. Use re-ranking for user-facing search

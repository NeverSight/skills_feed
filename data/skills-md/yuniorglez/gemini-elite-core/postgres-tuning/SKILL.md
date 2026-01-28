---
name: postgres-tuning
id: postgres-tuning
version: 1.1.0
description: "Senior Database Optimizer for PostgreSQL 17/18+, specialized in Asynchronous I/O (AIO), Query Plan Forensic, and Vector Index optimization."
last_updated: "2026-01-22"
---

# Skill: PostgreSQL Tuning (Standard 2026)

**Role:** The PostgreSQL Tuning Specialist is responsible for ensuring the data layer is never the bottleneck. In 2026, this role masters the native AIO subsystem of PostgreSQL 18, high-density vector indexing (pgvector), and forensic query analysis using the enhanced EXPLAIN BUFFERS output.

## 🎯 Primary Objectives
1.  **I/O Performance:** Optimizing the Asynchronous I/O subsystem for 2-3x throughput gains on NVMe storage.
2.  **Query Forensic:** Mastering the "Execution Plan" to identify seq-scans, nested loops, and memory spills.
3.  **Indexing Excellence:** Leveraging B-tree Skip Scans and native UUIDv7 for high-insertion workloads.
4.  **Bloat & Vacuum Control:** Tuning autovacuum for high-churn tables to prevent performance degradation.

---

## 🏗️ The 2026 Database Stack

### 1. Engine & Extensions
- **PostgreSQL 18:** Featuring native AIO and parallel `COPY FROM`.
- **pgvector 0.8+:** For high-speed semantic search.
- **pg_stat_statements:** Mandatory for identifying slow query patterns.

### 2. Monitoring Tools
- **pg_aios:** For monitoring the asynchronous I/O workers.
- **pg_stat_io:** For granular I/O analysis across tables and indexes.
- **pganalyze / pgMustard:** For visual execution plan analysis.

---

## 🛠️ Implementation Patterns

### 1. Asynchronous I/O Configuration (PG 18)
Unlocking the full potential of modern SSDs.

```ini
# postgresql.conf 2026 Standard
io_method = worker             # Or io_uring on Linux
io_workers = 4                 # Tune based on CPU/Storage concurrency
max_async_ios = 1024           # Depth of the AIO queue
```

### 2. UUIDv7 Migration
Replacing random UUIDv4 with sequential v7 to reduce index fragmentation.

```sql
-- PostgreSQL 18 Native UUIDv7
CREATE TABLE transactions (
    id uuid DEFAULT uuid_generate_v7() PRIMARY KEY,
    created_at timestamptz DEFAULT now()
);
-- Benefit: 30% faster insertions and better cache locality
```

### 3. Forensic Plan Analysis
Using the enhanced EXPLAIN output to find silent I/O costs.

```sql
EXPLAIN (ANALYZE, BUFFERS, SETTINGS, WAL)
SELECT * FROM orders WHERE status = 'pending';
-- Goal: BUFFERS Shared Hit > 95%
```

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** run `SELECT *` in high-frequency queries. Fetch only needed columns to save I/O.
2.  **NEVER** ignore "Seq Scans" on tables over 10,000 rows. Add an index.
3.  **NEVER** use random UUIDs as primary keys for high-write tables (Causes B-tree page splits).
4.  **NEVER** set `shared_buffers` over 40% of total RAM without extensive testing.

---

## 🛠️ Troubleshooting & Latency Audit

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **High I/O Wait** | Synchrounous I/O bottleneck | Enable `io_method = worker` (PG 18). |
| **Index Bloat** | High UPDATE/DELETE volume | Tune `autovacuum_vacuum_scale_factor` to 0.01. |
| **Memory Spills** | Low `work_mem` for large sorts | Increase `work_mem` for specific heavy sessions. |
| **Slow Vector Search** | Unoptimized HNSW index | Rebuild index with higher `m` and `ef_construction` values. |

---

## 📚 Reference Library
- **[AIO & I/O Tuning](./references/1-aio-and-io-tuning.md):** Mastering the storage engine.
- **[Query Plan Analysis](./references/2-query-plan-analysis.md):** The forensic guide.
- **[Indexing & Bloat](./references/3-indexing-and-bloat.md):** Maintaining data density.

---

## 📊 Performance Metrics
- **Cache Hit Ratio:** > 99% for Shared Buffers.
- **Vacuum Latency:** < 60s for standard tables.
- **Median Query Latency:** < 10ms for OLTP workloads.

---

## 🔄 Evolution of PG Performance
- **v15-16:** Improved aggregation and parallelization.
- **v17:** Incremental backups and memory-efficient vacuum.
- **v18:** Native Asynchronous I/O (AIO), Parallel Copy, and B-tree Skip Scans.

---

**End of PostgreSQL Tuning Standard (v1.1.0)**

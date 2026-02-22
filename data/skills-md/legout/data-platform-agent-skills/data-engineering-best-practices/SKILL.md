---
name: data-engineering-best-practices
description: "Data engineering best practices: medallion architecture, dataset lifecycle, partitioning, file sizing, schema evolution, and append/overwrite/merge patterns across Polars, PyArrow, DuckDB, Delta Lake, and Iceberg. Use when designing production data pipelines or reviewing data platform decisions."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-lakehouse", "@data-engineering-storage-remote-access", "@data-engineering-storage-formats", "@data-engineering-storage-authentication"]
---

# Data Engineering Best Practices

Use this skill for production architecture and standards decisions: storage layout, lifecycle, incremental semantics, schema evolution, quality checks, and cost/performance tradeoffs.

## When to use this skill

Use for:
- Designing Bronze/Silver/Gold or equivalent data layers
- Choosing append vs overwrite vs merge behavior
- Partitioning and file-size strategy
- Defining schema evolution policy
- Setting testing/observability guardrails
- Establishing retention + cost controls

Use domain skills for implementation details:
- `@data-engineering-core`
- `@data-engineering-storage-lakehouse`
- `@data-engineering-storage-formats`
- `@data-engineering-storage-remote-access`
- `@data-engineering-storage-authentication`

---

## Decision checklist (apply in order)

1. **Data contract**
   - Required columns/types?
   - Nullability and key uniqueness?
2. **Layer semantics**
   - Bronze immutable?
   - Silver deduplicated/validated?
   - Gold business-ready aggregates?
3. **Write mode**
   - Append, partition overwrite, or merge?
4. **Layout**
   - Partition keys + target file size set?
5. **Incremental logic**
   - Watermark/checkpoint strategy defined?
6. **Evolution policy**
   - Additive-only by default?
7. **Operational controls**
   - Tests + observability + retention + backfill process?

---

## Core standards

### 1) Layering (Medallion)

- **Bronze**: raw immutable ingestion; append-only
- **Silver**: cleaned, validated, conformed schema
- **Gold**: consumption-specific marts/features/aggregates

Do not skip Silver validation for convenience; silent quality drift is costly.

### 2) Write semantics

| Operation | Use when | Notes |
|---|---|---|
| **Append** | strictly new immutable events | simplest, cheapest |
| **Partition overwrite** | deterministic reprocessing for date/key slice | safe for backfills |
| **Merge/Upsert** | corrections/late updates/deletes | needs key + conflict semantics |

### 3) Partitioning

Good partition keys:
- Frequently filtered dimensions (often date + low/moderate-cardinality dimension)

Avoid:
- High-cardinality keys (e.g., user_id)
- Over-partitioning creating tiny files

### 4) File sizing

Target file size: **~256MB–1GB** (workload-dependent).

- Too small → metadata/listing overhead + slow scans
- Too large → poor parallelism and skewed processing

### 5) Schema evolution

Default policy:
- ✅ additive changes first (new nullable columns)
- ⚠️ type widening only when compatibility is clear
- ❌ destructive rename/drop in-place for shared production tables

### 6) Incremental processing

- Persist watermark/checkpoint externally
- Make re-runs idempotent
- Include late-arriving data strategy (lag window/backfill)

### 7) Quality and reliability

Minimum controls:
- Required columns + types
- Primary key uniqueness (or dedupe policy)
- Null thresholds on critical fields
- Freshness/SLA checks
- Run-level metrics (rows in/out, failures, latency)

---

## Anti-patterns (reject in review)

- Full table overwrite for small incremental changes
- No checkpoint/watermark for recurring pipeline
- Unbounded tiny-file generation
- Dynamic SQL built from user values without parameter binding
- Production credentials in code/config committed to repo
- No backfill plan / no rollback strategy

---

## Minimal production blueprint

1. Ingest raw to Bronze (append-only)
2. Validate + standardize to Silver
3. Build Gold outputs
4. Emit metrics + quality report
5. Persist checkpoint/watermark
6. Apply lifecycle rules + periodic compaction/maintenance

---

## Progressive disclosure (read next as needed)

- `best-practices-detailed.md` — comprehensive deep-dive examples
- `@data-engineering-core/patterns/incremental.md` — incremental loading patterns
- `@data-engineering-storage-lakehouse` — Delta/Iceberg/Hudi-specific behavior
- `@data-engineering-quality` — validation framework implementation
- `@data-engineering-observability` — metrics/tracing/alerting

---

## References

- [Delta Lake Schema Evolution](https://delta.io/blog/2023-02-08-delta-lake-schema-evolution/)
- [Apache Iceberg Evolution](https://iceberg.apache.org/docs/latest/evolution/)
- [DuckDB MERGE INTO](https://duckdb.org/docs/stable/sql/statements/merge_into.html)
- [PyArrow Dataset API](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Dataset.html)

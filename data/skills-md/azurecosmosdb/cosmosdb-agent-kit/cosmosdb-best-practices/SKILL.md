---
name: cosmosdb-best-practices
description: |
  Azure Cosmos DB performance optimization and best practices guidelines for NoSQL,
  partitioning, queries, and SDK usage. Use when writing, reviewing, or refactoring
  code that interacts with Azure Cosmos DB, designing data models, optimizing queries,
  or implementing high-performance database operations.

license: MIT
metadata:
  author: cosmosdb-agent-kit
  version: "1.0.0"
---

# Azure Cosmos DB Best Practices

Comprehensive performance optimization guide for Azure Cosmos DB applications, containing 45+ rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Designing data models for Cosmos DB
- Choosing partition keys
- Writing or optimizing queries
- Implementing SDK patterns
- Reviewing code for performance issues
- Configuring throughput and scaling
- Building globally distributed applications

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Data Modeling | CRITICAL | `model-` |
| 2 | Partition Key Design | CRITICAL | `partition-` |
| 3 | Query Optimization | HIGH | `query-` |
| 4 | SDK Best Practices | HIGH | `sdk-` |
| 5 | Indexing Strategies | MEDIUM-HIGH | `index-` |
| 6 | Throughput & Scaling | MEDIUM | `throughput-` |
| 7 | Global Distribution | MEDIUM | `global-` |
| 8 | Monitoring & Diagnostics | LOW-MEDIUM | `monitoring-` |

## Quick Reference

### 1. Data Modeling (CRITICAL)

- `model-embed-related` - Embed related data retrieved together
- `model-reference-large` - Reference data when items get too large
- `model-avoid-2mb-limit` - Keep items well under 2MB limit
- `model-denormalize-reads` - Denormalize for read-heavy workloads
- `model-schema-versioning` - Version your document schemas
- `model-type-discriminator` - Use type discriminators for polymorphic data

### 2. Partition Key Design (CRITICAL)

- `partition-high-cardinality` - Choose high-cardinality partition keys
- `partition-avoid-hotspots` - Distribute writes evenly
- `partition-hierarchical` - Use hierarchical partition keys for flexibility
- `partition-query-patterns` - Align partition key with query patterns
- `partition-synthetic-keys` - Create synthetic keys when needed
- `partition-20gb-limit` - Plan for 20GB logical partition limit

### 3. Query Optimization (HIGH)

- `query-avoid-cross-partition` - Minimize cross-partition queries
- `query-use-projections` - Project only needed fields
- `query-pagination` - Use continuation tokens for pagination
- `query-avoid-scans` - Avoid full container scans
- `query-parameterize` - Use parameterized queries
- `query-order-filters` - Order filters by selectivity

### 4. SDK Best Practices (HIGH)

- `sdk-singleton-client` - Reuse CosmosClient as singleton
- `sdk-async-api` - Use async APIs for throughput
- `sdk-retry-429` - Handle 429s with retry-after
- `sdk-connection-mode` - Use Direct mode for production
- `sdk-preferred-regions` - Configure preferred regions
- `sdk-diagnostics` - Log diagnostics for troubleshooting

### 5. Indexing Strategies (MEDIUM-HIGH)

- `index-exclude-unused` - Exclude paths never queried
- `index-composite` - Use composite indexes for ORDER BY
- `index-spatial` - Add spatial indexes for geo queries
- `index-range-vs-hash` - Choose appropriate index types
- `index-lazy-consistent` - Understand indexing modes

### 6. Throughput & Scaling (MEDIUM)

- `throughput-autoscale` - Use autoscale for variable workloads
- `throughput-right-size` - Right-size provisioned throughput
- `throughput-serverless` - Consider serverless for dev/test
- `throughput-burst` - Understand burst capacity
- `throughput-container-vs-database` - Choose allocation level wisely

### 7. Global Distribution (MEDIUM)

- `global-multi-region` - Configure multi-region writes
- `global-consistency` - Choose appropriate consistency level
- `global-conflict-resolution` - Implement conflict resolution
- `global-failover` - Configure automatic failover
- `global-read-regions` - Add read regions near users

### 8. Monitoring & Diagnostics (LOW-MEDIUM)

- `monitoring-ru-consumption` - Track RU consumption
- `monitoring-latency` - Monitor P99 latency
- `monitoring-throttling` - Alert on throttling
- `monitoring-azure-monitor` - Integrate Azure Monitor
- `monitoring-diagnostic-logs` - Enable diagnostic logging

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/model-embed-related.md
rules/partition-high-cardinality.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

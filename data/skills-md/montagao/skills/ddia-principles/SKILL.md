---
name: ddia-principles
description: Apply principles from "Designing Data-Intensive Applications" (Kleppmann) to system design, architecture review, and technology selection. Use when (1) designing new data systems or APIs, (2) choosing between databases, queues, or storage technologies, (3) reviewing architecture for reliability, scalability, or consistency concerns, (4) discussing trade-offs in distributed systems, (5) reviewing code for data handling patterns. Optimized for startup/small team contexts where pragmatic choices matter.
---

# DDIA Principles

Apply Kleppmann's principles to make informed decisions about data systems.

## Core Framework: The Three Concerns

Every data system decision maps to these concerns:

1. **Reliability** - System works correctly despite faults
2. **Scalability** - System handles growth in data, traffic, or complexity
3. **Maintainability** - System remains operable and evolvable over time

When reviewing designs or making technology choices, evaluate against all three.

## Quick Decision Patterns

### Database Selection

| Need | Start With | Graduate To |
|------|------------|-------------|
| General CRUD, transactions | PostgreSQL | PostgreSQL (it scales further than you think) |
| Document-shaped data, flexible schema | PostgreSQL JSONB | MongoDB if document model is primary |
| Key-value, caching | Redis | Redis Cluster |
| Full-text search | PostgreSQL FTS | Elasticsearch when FTS is primary workload |
| Time-series, metrics | TimescaleDB | ClickHouse at scale |
| Graph relationships | PostgreSQL + recursive CTEs | Neo4j when traversals dominate |

**Default recommendation**: PostgreSQL. It handles more use cases than people realize. Only move to specialized databases when PostgreSQL becomes the bottleneck for a specific workload.

### Consistency vs Availability

Use this when designing distributed features:

```
Strong consistency needed?
├── Yes (money, inventory, unique constraints)
│   └── Use transactions, accept higher latency
│   └── Single leader or consensus protocol
└── No (feeds, caches, analytics)
    └── Eventual consistency acceptable
    └── Can use multi-leader or leaderless
```

### When to Add a Message Queue

Add a queue when:
- Tasks take >100ms and user doesn't need immediate result
- Need to decouple producers from consumers
- Need retry logic with backoff
- Processing can be delayed during load spikes

Don't add a queue just because "microservices." A direct function call or HTTP request is simpler when synchronous processing works.

## Architecture Review Checklist

When reviewing a data system design, ask:

### Data Model
- [ ] Does the data model match how data is queried? (Not just how it's structured logically)
- [ ] Are relationships handled appropriately? (Normalize for integrity, denormalize for read performance)
- [ ] Is there a clear schema evolution strategy?

### Reliability
- [ ] What happens when the database is unavailable?
- [ ] What happens when a downstream service times out?
- [ ] Are writes idempotent where possible?
- [ ] Is there a backup/restore strategy?

### Consistency
- [ ] What consistency guarantees does the system actually need?
- [ ] Where are the transaction boundaries?
- [ ] What happens during partial failures?

### Scalability
- [ ] What's the expected data growth rate?
- [ ] Which operations will become slow first?
- [ ] Are there natural partition keys if sharding becomes needed?

## Code Review Lens

When reviewing code that handles data:

### Red Flags
- Read-modify-write without transactions or optimistic locking
- Assuming network calls will succeed
- Silent data loss on errors
- Unbounded queries without pagination
- N+1 query patterns
- Mixing business logic with data access in ways that prevent batching

### Patterns to Encourage
- Explicit transaction boundaries
- Retry logic with exponential backoff
- Idempotency keys for mutations
- Cursor-based pagination for large datasets
- Bulk operations where applicable

## Technology Trade-offs Reference

For detailed analysis of specific technology choices, see:
- [references/storage-engines.md](references/storage-engines.md) - LSM vs B-tree, when each shines
- [references/replication.md](references/replication.md) - Leader-based vs leaderless, consistency models
- [references/encoding.md](references/encoding.md) - JSON vs binary formats, schema evolution

## Common Anti-Patterns

### "We need microservices"
Before splitting into services, ask: Is the complexity of distributed transactions worth it? Monoliths with good module boundaries often serve startups better.

### "Let's use Kafka"
Kafka is powerful but operationally complex. For most startups: PostgreSQL LISTEN/NOTIFY, Redis Streams, or a managed queue (SQS, Cloud Pub/Sub) are simpler starting points.

### "We'll just cache everything"
Caching adds complexity: invalidation, consistency, cold starts. First optimize queries, add indexes, denormalize read models. Cache as a last resort.

### "NoSQL for scale"
Modern PostgreSQL with proper indexing handles more than most startups will ever need. Choose NoSQL for data model fit, not scale anxiety.

## Practical Guidance

### For New Systems
1. Start with PostgreSQL
2. Use transactions for data integrity
3. Add caching/queues only when measured need arises
4. Design for the data access patterns you have, not ones you might have

### For Growing Systems
1. Profile before optimizing
2. Vertical scaling is simpler than horizontal—use it first
3. Partition by natural boundaries when needed
4. Consider read replicas before complex architectures

### For System Rewrites
1. Strangler fig pattern over big bang
2. Keep data in sync during migration
3. Verify with shadow reads/writes
4. Roll back capability is essential

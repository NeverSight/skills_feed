---
name: memory-systems
description: Use when implementing agent memory, persisting state across sessions, building knowledge graphs, tracking entities, or asking about "agent memory", "knowledge graph", "entity memory", "vector stores", "temporal knowledge", "cross-session persistence"
version: 1.0.0
---

# Memory System Design

Memory provides persistence that allows agents to maintain continuity across sessions and reason over accumulated knowledge.

## Memory Architecture Spectrum

| Layer | Latency | Persistence | Use Case |
|-------|---------|-------------|----------|
| Working Memory | Zero | Volatile | Context window |
| Short-Term | Low | Session | Session state |
| Long-Term | Medium | Persistent | Cross-session knowledge |
| Entity Memory | Medium | Persistent | Entity tracking |
| Temporal KG | Medium | Persistent | Time-aware queries |

## Memory System Performance

| System | DMR Accuracy | Retrieval Latency |
|--------|--------------|-------------------|
| Zep (Temporal KG) | 94.8% | 2.58s |
| MemGPT | 93.4% | Variable |
| GraphRAG | 75-85% | Variable |
| Vector RAG | 60-70% | Fast |
| Recursive Summary | 35.3% | Low |

## Why Vector Stores Fall Short

Vector stores lose relationship information:

- Can retrieve "Customer X purchased Product Y"
- Cannot answer "What did customers who bought Y also buy?"
- Cannot distinguish current vs outdated facts

## Memory Implementation Patterns

### Pattern 1: File-System-as-Memory

```python
# Simple, no infrastructure needed
def store_fact(entity_id, fact):
    path = f"memory/{entity_id}.json"
    facts = load_json(path, default=[])
    facts.append({"fact": fact, "timestamp": now()})
    save_json(path, facts)
```

### Pattern 2: Vector RAG with Metadata

```python
# Embed facts with rich metadata
vector_store.add(
    embedding=embed(fact),
    metadata={
        "entity_id": entity_id,
        "valid_from": now(),
        "source": "conversation",
        "confidence": 0.95
    }
)
```

### Pattern 3: Knowledge Graph

```python
# Preserve relationships
graph.create_relationship(
    from_entity="Customer_123",
    relationship="PURCHASED",
    to_entity="Product_456",
    properties={"date": "2024-01-15", "quantity": 2}
)
```

### Pattern 4: Temporal Knowledge Graph

```python
# Time-travel queries
def query_address_at_time(user_id, query_time):
    return graph.query("""
        MATCH (user)-[r:LIVES_AT]->(address)
        WHERE user.id = $user_id
        AND r.valid_from <= $query_time
        AND (r.valid_until IS NULL OR r.valid_until > $query_time)
        RETURN address
    """, {"user_id": user_id, "query_time": query_time})
```

## Entity Memory

Track entities consistently across conversations:

- **Entity Identity**: "John Doe" in one conversation = same person in another
- **Entity Properties**: Facts discovered about entities over time
- **Entity Relationships**: Relationships discovered between entities

```python
def remember_entity(entity_id, properties):
    memory.store({
        "type": "entity",
        "id": entity_id,
        "properties": properties,
        "last_updated": now()
    })
```

## Memory Consolidation

Trigger consolidation when:

- Memory accumulates significantly
- Retrieval returns too many outdated results
- Periodically on schedule
- Explicit request

Process:

1. Identify outdated facts
2. Merge related facts
3. Update validity periods
4. Archive/delete obsolete facts
5. Rebuild indexes

## Choosing Memory Architecture

| Requirement | Architecture |
|-------------|--------------|
| Simple persistence | File-system memory |
| Semantic search | Vector RAG with metadata |
| Relationship reasoning | Knowledge graph |
| Temporal validity | Temporal knowledge graph |

## Best Practices

1. Match architecture to query requirements
2. Implement progressive disclosure for access
3. Use temporal validity to prevent conflicts
4. Consolidate periodically
5. Design for retrieval failures gracefully
6. Consider privacy implications
7. Implement backup and recovery
8. Monitor growth and performance

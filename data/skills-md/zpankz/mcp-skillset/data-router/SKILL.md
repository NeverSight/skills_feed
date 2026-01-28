---
name: data-router
description: Routes data processing, knowledge graph, and analytics tasks. Triggers on graph, vector, knowledge, ontology, process, batch, etl, database, query, csv, json.
---

# Data Router

Routes data processing, knowledge graph, and analytics tasks.

## Subcategories

### Knowledge Graphs
```yaml
triggers: [graph, knowledge-graph, entity, relation, neo4j, networkx]
skills:
  - hkgb: Hybrid Knowledge Graph building
  - ontolog: Holarchic reasoning over graphs
```

### Batch Processing
```yaml
triggers: [batch, process, etl, migrate, transform]
skills:
  - obsidian-batch: Obsidian vault batch operations
  - process: Batch processing workflows
```

### Vector / Semantic
```yaml
triggers: [vector, embedding, semantic, similarity, rag]
skills:
  - skill-discovery: Semantic skill search
```

### Analytics
```yaml
triggers: [analyze-data, query, sql, csv, json, aggregate]
skills:
  - sc:analyze: Data analysis
```

## Routing Decision Tree

```
data request
    │
    ├── Knowledge graph?
    │   ├── Building? → hkgb
    │   └── Reasoning → ontolog
    │
    ├── Batch processing?
    │   ├── Obsidian? → obsidian-batch
    │   └── General → process
    │
    ├── Vector/semantic?
    │   └── skill-discovery
    │
    └── Analytics?
        └── sc:analyze
```

## Managed Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| hkgb | Hybrid KG building | "knowledge graph", "neo4j" |
| ontolog | Graph reasoning | "ontology", "holarchic" |
| obsidian-batch | Vault processing | "obsidian", "vault" |
| process | Batch processing | "batch", "process" |
| skill-discovery | Semantic search | "find skill", "discover" |

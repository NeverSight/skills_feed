---
name: lancedb
description: >
  LanceDB vector database patterns and best practices.
  Trigger: When using LanceDB vector database.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with lancedb"

## When to Use

Use this skill when:
- Storing and querying vector embeddings
- Building semantic search
- Implementing RAG systems
- Working with multi-modal data

---

## Critical Patterns

### Table Creation (REQUIRED)

```python
import lancedb

# ✅ ALWAYS: Define schema clearly
db = lancedb.connect("./my_db")

data = [
    {"id": 1, "text": "Hello world", "vector": [0.1, 0.2, ...]},
    {"id": 2, "text": "Goodbye world", "vector": [0.3, 0.4, ...]},
]

table = db.create_table("my_table", data)
```

### Vector Search (REQUIRED)

```python
# ✅ Search by vector similarity
results = table.search([0.1, 0.2, ...]).limit(10).to_list()

# ✅ With filter
results = table.search(query_vector) \
    .where("category = 'tech'") \
    .limit(5) \
    .to_list()
```

---

## Decision Tree

```
Need semantic search?      → Use vector search
Need exact match?          → Use where clause
Need hybrid search?        → Combine vector + filter
Need persistence?          → Use file-based connection
```

---

## Resources

- **Best Practices**: [best-practices.md](best-practices.md)

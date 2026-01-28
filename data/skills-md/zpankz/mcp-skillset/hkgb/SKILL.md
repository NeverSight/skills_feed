---
name: hkgb
description: "This skill should be used when building hybrid Knowledge Graphs that integrate structured data (CSV, databases) with automatically extracted entities from unstructured documents (PDFs, text). The pattern establishes a reliable join key between domain graphs and lexical graphs, enabling GraphRAG, document ingestion with metadata enrichment, and Knowledge Graph construction from heterogeneous sources using neo4j-graphrag SimpleKGPipeline."
---

# Hybrid Knowledge Graph Bridge

*Integration pattern for linking structured domain data to LLM-extracted lexical graphs*

## Problem

When building Knowledge Graphs from heterogeneous sources, two distinct graph types often need coexistence:

1. **Domain Graph** — Structured, curated data from CSV/databases representing business entities and relationships
2. **Lexical Graph** — Entities and relationships automatically extracted from unstructured documents via LLM

These graphs speak different languages: one is schema-driven and deterministic, the other is probabilistic and emergent. Without a deliberate bridge, they remain disconnected silos.

## Solution

The solution establishes a reliable join key between both graphs through five steps.

### Step 1: Specify the lexical graph schema

Before extraction, define the ontology that guides the LLM. This specification comprises three elements.

**Node Types** — The entities to extract. Some are simple labels, others are enriched with descriptions (to guide the LLM) and typed properties:

```python
NODE_TYPES = [
    "Entity",           # Simple label
    "Concept",
    "Process",
    {                   # Enriched with description
        "label": "Outcome",
        "description": "A result, benefit, or consequence of a process or action."
    },
    {                   # With typed properties
        "label": "Reference",
        "description": "An external resource such as a document, article, or dataset.",
        "properties": [
            {"name": "name", "type": "STRING", "required": True},
            {"name": "type", "type": "STRING"}
        ]
    },
]
```

**Relationship Types** — The possible verbs between entities:

```python
RELATIONSHIP_TYPES = [
    "RELATED_TO",
    "PART_OF",
    "USED_IN",
    "LEADS_TO",
    "REFERENCES"
]
```

**Patterns** — The valid combinations. The LLM can only extract conforming triplets:

```python
PATTERNS = [
    ("Entity", "RELATED_TO", "Entity"),
    ("Concept", "RELATED_TO", "Entity"),
    ("Process", "PART_OF", "Entity"),
    ("Process", "LEADS_TO", "Outcome"),
    ("Reference", "REFERENCES", "Entity"),
]
```

### Step 2: Configure the extraction pipeline

The pipeline assembles the LLM, embedder, text splitter, and schema:

```python
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter

llm = OpenAILLM(
    model_name="gpt-4o",
    model_params={
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
)

embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
text_splitter = FixedSizeSplitter(chunk_size=500, chunk_overlap=100)

kg_builder = SimpleKGPipeline(
    llm=llm,
    driver=neo4j_driver,
    neo4j_database=os.getenv("NEO4J_DATABASE"),
    embedder=embedder,
    from_pdf=True,
    text_splitter=text_splitter,
    schema={
        "node_types": NODE_TYPES,
        "relationship_types": RELATIONSHIP_TYPES,
        "patterns": PATTERNS
    },
)
```

The pipeline performs: PDF → chunks → schema-guided LLM extraction → node/relationship creation → embeddings.

### Step 3: Transform the structured source into a dictionary

Each row of the CSV (representing the domain graph) becomes a Python dictionary:

```python
records = csv.DictReader(
    open(os.path.join(data_path, "metadata.csv"), encoding="utf8", newline='')
)
# Produces: {"filename": "doc1.pdf", "category": "...", "author": "...", ...}
```

### Step 4: Add the common key to the dictionary

The pipeline creates `Document` nodes with a `path` property. This property serves as the bridge between the two graphs. Enrich the dictionary with a key that matches exactly what the pipeline stores:

```python
record["file_path"] = os.path.join(data_path, record["filename"])
# The same value passed to the pipeline becomes Document.path
```

This same value is passed to the pipeline which generates the lexical graph:

```python
result = asyncio.run(
    kg_builder.run_async(file_path=record["file_path"])
)
```

### Step 5: Join the two graphs via Cypher

A query uses the common key to attach the domain graph to the lexical graph:

```cypher
MATCH (d:Document {path: $file_path})
MERGE (e:DomainEntity {id: $entity_id})
SET e.category = $category,
    e.author = $author
MERGE (d)-[:BELONGS_TO]->(e)
```

The enriched dictionary is passed as parameters:

```python
neo4j_driver.execute_query(cypher, parameters_=record)
```

## Consequences

The pattern works because the dictionary key and `Document.path` contain identical values. This implicit key connects the lexical graph (entities extracted according to the specified schema) to the domain graph (business structure from structured sources). If these values diverge, the bridge fails silently — orphaned nodes accumulate undetected.

## Verification

To ensure the bridge holds, verify that `Document` nodes are properly attached:

```cypher
// Orphan documents (broken bridge)
MATCH (d:Document)
WHERE NOT EXISTS { (d)-[:BELONGS_TO]->(:DomainEntity) }
RETURN d.path AS orphan

// Domain entities without documents (bridge never built)
MATCH (e:DomainEntity)
WHERE NOT EXISTS { (:Document)-[:BELONGS_TO]->(e) }
RETURN e.id AS missing
```

## Complete Reference

For a complete implementation example, see `references/full_example.py`.

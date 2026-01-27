---
name: knowledge-synthesizer
description: Expert in aggregating, processing, and synthesizing information from multiple sources into coherent insights. Use when building knowledge graphs, ontologies, RAG systems, or extracting insights across documents. Triggers include "knowledge graph", "ontology", "synthesize information", "GraphRAG", "insight extraction", "cross-document analysis".
---

# Knowledge Synthesizer

## Purpose
Provides expertise in aggregating information from multiple sources and synthesizing it into structured, actionable knowledge. Specializes in ontology building, knowledge graph design, and insight extraction for RAG and AI systems.

## When to Use
- Building knowledge graphs or ontologies
- Designing GraphRAG or hybrid retrieval systems
- Synthesizing information across multiple documents
- Extracting entities and relationships from text
- Creating structured knowledge bases
- Developing taxonomy and classification systems
- Implementing semantic search architectures
- Connecting disparate data sources meaningfully

## Quick Start
**Invoke this skill when:**
- Building knowledge graphs or ontologies
- Designing RAG systems with graph components
- Synthesizing insights from multiple sources
- Extracting structured knowledge from unstructured text
- Creating taxonomies or classification schemes

**Do NOT invoke when:**
- Vector database setup without graph needs → use `/context-manager`
- General NLP tasks (NER, classification) → use `/nlp-engineer`
- Database schema design → use `/database-administrator`
- Document writing → use `/technical-writer`

## Decision Framework
```
Knowledge Structure Needed?
├── Hierarchical (taxonomy)
│   └── Tree structure, parent-child relationships
├── Graph (connected entities)
│   └── Nodes + edges, property graphs
├── Hybrid (RAG + Graph)
│   └── Vector embeddings + knowledge graph
└── Flat (simple retrieval)
    └── Standard vector store sufficient
```

## Core Workflows

### 1. Ontology Design
1. Identify domain scope and boundaries
2. Define core entity types (classes)
3. Map relationships between entities
4. Add properties and constraints
5. Validate with domain experts
6. Document with examples

### 2. Knowledge Graph Construction
1. Extract entities from source documents
2. Identify relationships between entities
3. Normalize and deduplicate entities
4. Build graph structure (nodes, edges)
5. Add metadata and provenance
6. Create query interfaces

### 3. Insight Synthesis
1. Gather sources and establish provenance
2. Extract key claims and facts
3. Identify contradictions and agreements
4. Synthesize into coherent narrative
5. Cite sources for traceability
6. Highlight confidence levels

## Best Practices
- Maintain provenance for all extracted knowledge
- Use established ontology standards (OWL, SKOS) when applicable
- Design for evolution—ontologies change over time
- Validate extracted relationships with source context
- Balance granularity with usability
- Include confidence scores for extracted facts

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| No provenance tracking | Cannot verify claims | Track source for every fact |
| Over-complex ontology | Hard to maintain and query | Start simple, evolve as needed |
| Ignoring contradictions | Inconsistent knowledge base | Flag and resolve conflicts |
| Static schema | Breaks with new domains | Design for extensibility |
| Blind extraction trust | Hallucinated relationships | Validate with confidence thresholds |

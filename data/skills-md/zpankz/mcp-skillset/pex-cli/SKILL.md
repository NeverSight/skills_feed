---
name: pex-cli
description: Primary Exam (PEX) Knowledge Graph CLI for CICM/ANZCA exam preparation. Semantic search over Learning Outcomes, SAQs, concepts, and topics. Use for exam study, prerequisite chains, learning paths, and higher-order concept connections.
version: 1.0.0
category: medical-education
triggers:
  - pex
  - primary exam
  - cicm
  - anzca
  - learning outcome
  - saq
  - exam preparation
  - medical education
tags:
  - cli
  - graph
  - embeddings
  - medical
  - exam
  - falkordb
---

# PEX CLI Skill

## Purpose

Knowledge graph-based exam preparation for CICM/ANZCA Primary Exams. Provides semantic search, prerequisite chains, learning paths, and LLM-inferred higher-order connections.

## Quick Start

```bash
# Semantic search for Learning Outcomes
pex search "shock physiology" --limit 10

# Show prerequisites for a topic
pex prereq "LO-cardio-001"

# Generate learning path for a concept
pex path "cardiovascular physiology"

# Find concepts that refine/specialize another
pex refine "hemodynamics"

# Graph statistics
pex stats
```

## Commands

### Search (Semantic)

```bash
# Search Learning Outcomes (default)
pex search "septic shock management" --limit 5

# Search specific node types
pex search "dobutamine" --label Concept
pex search "cardiovascular" --label Topic
pex search "shock" --label SAQ
```

### Prerequisite Chains

```bash
# Show prerequisites for a Learning Outcome
pex prereq "LO-001"

# Get specific node by ID
pex get "LO-001"
```

### Learning Paths

```bash
# Generate learning path for a topic
pex path "renal physiology"

# Find LOs that refine/specialize another
pex refine "fluid balance"

# Find concepts implied by this concept
pex imply "cellular respiration"
```

### Data Ingestion

```bash
# Ingest from markdown files (LOs, SAQs)
pex ingest-md /path/to/markdown/

# Phase 6 LLM inference for higher-order connections
pex phase6-infer --model claude-3-5-sonnet

# Clear graph
pex clear
```

## Graph Schema

```cypher
(:LearningOutcome {id, name, description, domain, embedding})
(:SAQ {id, question, answer, topic, embedding})
(:Concept {id, name, category, embedding})
(:Topic {id, name, description, embedding})

(:LearningOutcome)-[:PREREQUISITE_OF]->(:LearningOutcome)
(:LearningOutcome)-[:COVERS]->(:Concept)
(:SAQ)-[:TESTS]->(:LearningOutcome)
(:Concept)-[:IMPLIES]->(:Concept)
(:LearningOutcome)-[:REFINES]->(:LearningOutcome)
```

## Integration with Grounding Router

The PEX CLI integrates with the grounding-router as the Σₚₑₓ primitive:

```yaml
Σₚₑₓ — Primary Exam Source

Sub-Primitives:
| Σₚ₁ | LO Search    | 0.95 | pex search "topic" --label LearningOutcome |
| Σₚ₂ | SAQ Search   | 0.90 | pex search "topic" --label SAQ |
| Σₚ₃ | Prerequisites| 0.85 | pex prereq "LO-id" |
| Σₚ₄ | Learning Path| 0.80 | pex path "concept" |
```

## Dependencies

| Service | Port | Required |
|---------|------|----------|
| FalkorDB | 6379 | Yes |
| Ollama | 11434 | For embeddings |

## Configuration

Location: `~/.pex/config.toml`

```toml
[graph]
host = "localhost"
port = 6379
graph_name = "pex"

[embeddings]
model = "qwen3:4b"
dimension = 4096
```

## Related Skills

- `limitless-cli` - Personal context (correlate study sessions)
- `grounding-router` - Medical education grounding primitives
- `saq` - SAQ practice workflows

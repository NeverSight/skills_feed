---
name: screenapp-cli
description: ScreenApp multimodal video/audio analysis CLI with graph-based context retrieval
version: 1.0.0
category: context-extraction
triggers:
  - screenapp
  - recording
  - video transcript
  - screen capture
  - demo recording
  - teaching session
  - multimodal ai
tags:
  - cli
  - video
  - audio
  - transcription
  - graph
  - embeddings
  - context
  - falkordb
---

# ScreenApp CLI Skill

## Purpose

Integrate ScreenApp's multimodal video/audio analysis API into the PEX context retrieval ecosystem as the Σₛ (Screen Context) primitive.

## Capabilities

### 1. File Operations
- List and search recordings from ScreenApp
- Retrieve detailed file information with transcripts
- Tag and organize recordings

### 2. Multimodal AI Queries
- Ask questions about video content
- Analyze transcripts, video frames, or screenshots
- Time-segment specific queries

### 3. Graph-Based Context
- Semantic search over transcript embeddings
- Topic extraction and co-occurrence
- Speaker identification and linking
- Recording similarity relationships

### 4. Workflow Pipelines
- Daily digest of recordings
- Cross-recording semantic search
- Export to Obsidian format
- Temporal correlation with limitless

## CLI Reference

```bash
# Core commands
screenapp files list|get|search|tag|untag
screenapp ask <fileId> "<question>" [--mode transcript|video|screenshots]
screenapp sync run|status|build-similarity|build-topics
screenapp graph query|stats|traverse
screenapp workflow daily|search|recent|export
screenapp config init|show|get|set|validate
```

## Σₛ Primitive Definition

```yaml
Σₛ — Screen Context (screenapp)

λο.τ Form: Query(ο) → Multimodal-Search(λ) → Screen-Context(τ)

Sub-Primitives:
| Σₛ₁ | Transcript Search  | 0.90 | screenapp files search --semantic |
| Σₛ₂ | Visual Query       | 0.85 | screenapp ask --mode video |
| Σₛ₃ | Temporal Context   | 0.80 | screenapp workflow daily |
| Σₛ₄ | AI Insights        | 0.88 | screenapp ask --mode all |
```

## Integration Points

### Context Router
- Triggers on: screenapp, recording, video, transcript, screen, demo
- Parallel execution with limitless, research, pieces

### Grounding Router
- Part of Σ (Source) primitive family
- Composition with other primitives: (Σₛ ⊗ Σₐ) ∘ Τ

### Quality Gates
- G₀ health check: `screenapp config validate`
- G₁ diversity: Screen sources boost context diversity

## Graph Schema

```cypher
(:Recording)-[:HAS_TRANSCRIPT]->(:Transcript)
(:Transcript)-[:HAS_SEGMENT]->(:Segment)
(:Segment)-[:SPOKEN_BY]->(:Speaker)
(:Recording)-[:COVERS_TOPIC]->(:Topic)
(:Recording)-[:SIMILAR_TO]->(:Recording)
```

## Usage Examples

### Context Extraction

```bash
# Semantic search for relevant recordings
screenapp files search "machine learning" --semantic --limit 5 --json

# Get AI insights from a recording
screenapp ask abc123 "What were the key decisions?" --json

# Daily context with temporal correlation
screenapp workflow daily 2025-01-10 --json
```

### Graph Queries

```bash
# Find recordings by topic
screenapp graph query "
  MATCH (r:Recording)-[:COVERS_TOPIC]->(t:Topic)
  WHERE t.name CONTAINS 'AI'
  RETURN r.name, r.id
  LIMIT 10
" --json

# Find similar recordings
screenapp graph query "
  MATCH (r1:Recording {id: 'abc123'})-[:SIMILAR_TO]->(r2)
  RETURN r2.name, r2.id
" --json
```

## Dependencies

| Service | Port | Required |
|---------|------|----------|
| FalkorDB/FalkorDBLite | 6379 / socket | Yes |
| Ollama | 11434 | For embeddings |
| ScreenApp API | - | Yes |

**Note**: Can use FalkorDBLite (embedded) similar to limitless-cli for zero-config setup.

## Configuration

Location: `~/.screenapp-cli/config.toml`

Required:
- `SCREENAPP_API_TOKEN`
- `SCREENAPP_TEAM_ID`

## Related Skills

- `limitless-cli` - Personal lifelogs (temporal correlation)
- `context-orchestrator` - Multi-source context extraction
- `grounding-router` - Medical education grounding

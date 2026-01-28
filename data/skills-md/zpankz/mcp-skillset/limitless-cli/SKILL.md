---
name: limitless-cli
description: CLI for Limitless.ai Pendant with lifelog management, FalkorDBLite semantic graph, vector embeddings, and DAG pipelines. Use for personal memory queries, semantic search across lifelogs/chats/persons/topics, entity extraction, and knowledge graph operations. Triggers include "lifelog", "pendant", "limitless", "personal memory", "semantic search", "graph query", "extraction".
license: MIT
---

# Limitless CLI Skill

A comprehensive CLI tool for interacting with Limitless.ai Pendant data, featuring **FalkorDBLite semantic graph** with vector embeddings, content extraction, and DAG pipelines.

## When to Use

- User wants **semantic search** across lifelogs, chats, persons, or topics
- User wants to query lifelogs or personal memory data
- User wants to extract entities (speakers, topics) from conversations
- User wants to sync lifelogs to a graph database
- User wants to run extraction or analysis pipelines
- User mentions "Limitless", "pendant", "lifelog", or "personal memory"
- User needs domain-specific extraction (medical, technical, business)

## Quick Start

### Semantic Search (Recommended)

```bash
# Semantic search across lifelogs (vector-based similarity)
limitless semantic-search "ICU critical care discussion" --types Lifelog --scores

# Search multiple node types
limitless semantic-search "family doctor" --types Lifelog,Chat,Person --limit 10

# Hybrid search (semantic + full-text)
limitless search "medical exam" --mode hybrid

# Check index status (embeddings, node counts)
limitless index status
```

### Graph Queries

```bash
# Cypher query on semantic graph
limitless graph query "MATCH (p:Person)-[:SPOKE_IN]->(l:Lifelog) RETURN p.name, count(l) ORDER BY count(l) DESC LIMIT 10"

# Graph statistics
limitless graph stats
```

### Basic Operations

```bash
# List recent lifelogs
limitless lifelogs list --limit 10

# Search for topic (full-text)
limitless lifelogs search "topic"

# Get specific lifelog
limitless lifelogs get <id> --format json
```

## Architecture

### FalkorDBLite Semantic Graph

The CLI uses an embedded **FalkorDBLite** graph database (no Docker required) with vector embeddings for semantic search.

| Component | Details |
|-----------|---------|
| Database | FalkorDBLite via Python service |
| Socket | `~/.limitless/falkordb.sock` (Unix domain) |
| Embeddings | BGE-small-en-v1.5 (384-dim, FastEmbed) |
| Vector Indexes | Lifelog, Chat, Person, Topic |

**Graph Statistics (as of 2026-01-11):**
- 95,021 nodes (8,777 Lifelogs, 2,608 Chats, 1,549 Persons, 33,024 Topics, 47,027 Speakers)
- 81,356 relationships (SPOKE_IN, HAS_TOPIC, HAS_CONTACT)
- 100% embedding coverage on searchable nodes

### Core Commands

| Command | Purpose |
|---------|---------|
| `semantic-search <query>` | Vector similarity search |
| `search <query> --mode hybrid` | Combined semantic + full-text |
| `index status` | Show node counts, embeddings |
| `graph query <cypher>` | Execute Cypher queries |
| `lifelogs list/search/get` | Basic lifelog operations |

### References (Load on Demand)

- **[API Reference](references/api-client.md)**: Rate limiting (180 req/min), retry logic
- **[Database Schema](references/database-schema.md)**: Node types, relationships, vector indexes
- **[Extraction Rules](references/extraction-rules.md)**: Rule-based and LLM extraction patterns
- **[Pipeline DSL](references/pipeline-dsl.md)**: YAML syntax, node types, templates

## Command Reference

### Semantic Search (Primary)

```bash
# Vector-based semantic search
semantic-search <query> [--types Lifelog,Chat,Person,Topic] [--limit N] [--threshold 0.15] [--scores] [--json]

# Hybrid search (semantic + full-text)
search <query> [--mode semantic|fulltext|hybrid] [--types ...] [--limit N] [--json]

# Index management
index status                    # Show node counts, embeddings, vector indexes
index build --export-path <path> # Build from Limitless export
```

### Graph Database

```bash
graph query <cypher> [--json]   # Execute Cypher query
graph stats                     # Show database statistics
graph traverse <label> <id>     # Traverse from node
```

### Lifelogs

```bash
lifelogs list [--date YYYY-MM-DD] [--starred] [--limit N] [--json]
lifelogs get <id> [--json]
lifelogs search <query> [--limit N] [--json]
```

### Pipelines

```bash
pipeline run <template|file> [--var key=value]
pipeline list       # List available templates
```

**Available templates:**
- `daily-digest.yaml` - Daily lifelog summary
- `weekly-review.yaml` - Comprehensive weekly analysis
- `hierarchical-extraction.yaml` - Full entity extraction
- `session-extraction.yaml` - Session detection
- `extract-actions.yaml` - Action item extraction
- `memory-query.yaml` - Context-augmented response
- `research.yaml` - Lifelog + web synthesis

### Workflows

```bash
workflow daily <date>    # Complete day snapshot
workflow search <query>  # Cross-source search
workflow recent          # Recent activity summary
```

## Domain Extraction Pattern

For domain-specific extraction, use this configurable pattern:

```typescript
// Define domain patterns
const patterns = [
  { pattern: /ondansetron/gi, category: '5HT3 antagonist', displayName: 'Ondansetron' },
  { pattern: /droperidol/gi, category: 'Dopamine antagonist', displayName: 'Droperidol' },
];

// Filter lifelogs by domain keywords
const filtered = lifelogs.filter(l =>
  patterns.some(p => p.pattern.test(l.markdown))
);

// Extract using rule-based extraction
const results = extractFromLifelog(lifelog);

// Sync to graph with graceful degradation
try {
  await dbClient.connect();
  await lifelogRepo.upsert(lifelog);
} catch (error) {
  console.log(`⚠️ Graph sync skipped: ${error.message}`);
}
```

See `references/extraction-rules.md` for the full pattern library.

## Environment Variables

```bash
LIMITLESS_API_KEY       # Required - API authentication
ANTHROPIC_API_KEY       # Optional - For LLM extraction
FALKORDB_HOST          # Default: localhost
FALKORDB_PORT          # Default: 6379
```

## Graceful Degradation

The CLI handles missing dependencies gracefully:

| Dependency | If Missing |
|------------|------------|
| FalkorDB | Continues without graph sync, warns user |
| Anthropic API | Falls back to rule-based extraction |
| Docker | Uses remote FalkorDB if configured |

## Troubleshooting

### "FalkorDBLite service not running"
- The Python service auto-starts on first use
- Manual start: `cd ~/Projects/limitless-cli/python && uv run python -m limitless_graph.server`
- Check socket: `ls ~/.limitless/falkordb.sock`

### "No results from semantic search"
- Lower threshold: `--threshold 0.1` (BGE scores are typically 0.15-0.35)
- Check embeddings: `limitless index status`
- Try different node types: `--types Lifelog,Chat,Person,Topic`

### "Rate limited (429)"
- Wait for rate limit window (180 req/min, refills 3/sec)
- Check: `config show` for current settings

## Integration with Other Skills

This skill integrates with:

- **context-orchestrator**: Use `/limitless` command for personal memory context
- **error-recovery**: Graceful degradation patterns applied
- **deep-research**: Combine with web research for synthesis pipelines

## Project Location

```
~/Projects/limitless-cli/
├── src/
│   ├── api/           # Rate-limited API client (180 req/min)
│   ├── db/            # FalkorDB repositories (9 repos)
│   ├── dag/           # Pipeline engine (YAML DSL)
│   ├── extraction/    # Rule + LLM extraction
│   ├── agent/         # Claude Agent SDK harness
│   └── cli/           # Commander.js commands
├── templates/         # 7 pipeline templates
└── scripts/           # Demo and utility scripts
```

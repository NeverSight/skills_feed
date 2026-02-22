---
name: dive-memory-v3
description: Persistent memory system for AI agents following Model Context Protocol (MCP). Use for storing long-term memories across sessions, semantic search of past knowledge, building knowledge graphs, auto-injecting context, deduplicating memories, syncing to cloud storage. Essential for agents that need to remember decisions, solutions, preferences, and learned patterns over time.
---

# Dive-Memory v3: MCP-Based Persistent Memory System

Dive-Memory v3 provides **long-term persistent memory** for AI agents, solving the "context forgetting" problem across sessions.

## Core Capabilities

### 1. Memory Storage
Store memories with rich metadata using the Python API:
```python
from dive_memory_v3 import DiveMemory

memory = DiveMemory()

# Add memory
memory.add(
    content="Fixed JWT auth bug with refresh token rotation",
    section="solutions",
    subsection="authentication",
    tags=["jwt", "security", "bug-fix"],
    importance=8,
    metadata={"code_snippet": "...", "success_rate": 1.0}
)
```

### 2. Semantic Search
Search using natural language + hybrid search (vector + keyword):
```python
# Search memories
results = memory.search(
    query="How to fix JWT authentication issues?",
    section="solutions",
    tags=["authentication"],
    top_k=5
)

for result in results:
    print(f"[{result.importance}] {result.content}")
    print(f"Relevance: {result.score:.2f}")
```

### 3. Knowledge Graph
Automatically build relationships between memories:
```python
# Get related memories
related = memory.get_related(memory_id, max_depth=2)

# Visualize graph
graph = memory.get_graph(section="solutions")
# Returns: {nodes: [...], edges: [...]}
```

### 4. Context Injection
Automatically inject relevant memories into prompts:
```python
# Enable auto-injection
memory.enable_context_injection()

# When processing task, relevant memories auto-prepend
task = "Implement user authentication"
context = memory.get_context_for_task(task)
# Returns: "Past solutions: JWT with refresh tokens..."
```

### 5. Deduplication
Automatically detect and merge duplicate memories:
```python
# Run deduplication
duplicates = memory.find_duplicates(threshold=0.95)
memory.merge_duplicates(duplicates, strategy="keep_newer")
```

### 6. Cloud Sync
Sync memories across devices:
```python
# Configure cloud sync
memory.configure_sync(
    provider="s3",
    bucket="dive-memory-sync",
    auto_sync=True
)

# Manual sync
memory.sync_to_cloud()
memory.sync_from_cloud()
```

## MCP Server Integration

Dive-Memory v3 runs as an MCP server for integration with Claude Desktop, Claude Code, etc.

### Start MCP Server
```bash
cd /home/ubuntu/skills/dive-memory-v3/scripts
python3 mcp_server.py
```

### MCP Tools Available
- `memory_add`: Add new memory
- `memory_search`: Search memories
- `memory_update`: Update existing memory
- `memory_delete`: Delete memory
- `memory_graph`: Get knowledge graph
- `memory_related`: Find related memories
- `memory_stats`: Get memory statistics

### MCP Configuration
Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "dive-memory": {
      "command": "python3",
      "args": ["/home/ubuntu/skills/dive-memory-v3/scripts/mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "your-key-here"
      }
    }
  }
}
```

## Memory Organization

### Sections & Subsections
Organize memories hierarchically:
```
solutions/
  ├── authentication/
  ├── database/
  └── api/
decisions/
  ├── architecture/
  └── technology/
preferences/
research/
  ├── ai-models/
  └── frameworks/
```

### Metadata Fields
- `tags`: List of keywords
- `importance`: 1-10 score
- `source`: Origin of memory
- `timestamp`: Creation time
- `access_count`: Usage frequency
- `last_accessed`: Last retrieval time

## Use Cases

### 1. Coding Agent
Remember successful solutions and patterns:
```python
# Store solution
memory.add(
    content="Use tRPC for type-safe APIs without code generation",
    section="solutions/api",
    tags=["typescript", "api", "type-safety"],
    importance=9
)

# Later, when building API
context = memory.search("How to build type-safe API?")
```

### 2. Research Agent
Build knowledge base from research:
```python
# Store findings
memory.add(
    content="Claude Opus 4.5: Best for code quality (10/10)",
    section="research/ai-models",
    tags=["claude", "code-review"],
    importance=8
)

# Auto-link to related memories
# Links to: "GPT-5.2 for security", "DeepSeek for reasoning"
```

### 3. Decision Tracking
Remember architectural decisions:
```python
memory.add(
    content="Chose PostgreSQL over MongoDB for ACID guarantees",
    section="decisions/database",
    tags=["database", "architecture"],
    metadata={"rationale": "Need transactions for financial data"}
)
```

### 4. Learning Loop
Learn from task execution:
```python
# After successful task
memory.add(
    content="Agent #42 excels at React component refactoring",
    section="capabilities",
    tags=["agent-42", "react", "refactoring"],
    importance=7
)

# Route future React tasks to Agent #42
```

## Advanced Features

### Importance Scoring
Automatic importance calculation based on:
- Access frequency
- Recency
- Graph centrality (how connected)
- User-defined importance

### Memory Pruning
Remove low-value memories:
```python
# Prune memories with:
# - importance < 3
# - not accessed in 90 days
# - access_count < 2
memory.prune(
    min_importance=3,
    max_age_days=90,
    min_access_count=2
)
```

### Memory Consolidation
Merge similar memories:
```python
# Find similar memories (0.7-0.95 similarity)
similar = memory.find_similar(threshold=0.7)

# Consolidate into summary
memory.consolidate(similar, strategy="llm_summary")
```

### Export & Import
```python
# Export to JSON
memory.export("memories.json", section="solutions")

# Import from JSON
memory.import_from_json("memories.json")

# Export to Markdown
memory.export_markdown("knowledge_base.md")
```

## Performance

- **Search**: < 100ms for 10K memories
- **Storage**: Supports 1M+ memories
- **Deduplication**: < 1% false positives
- **Cloud Sync**: Background, non-blocking

## Configuration

Configuration file at `references/config.json` contains all settings. Key options:
- Storage backend (SQLite/PostgreSQL)
- Embedding provider (OpenAI/local)
- Search strategy (semantic/keyword/hybrid)
- Deduplication thresholds
- Cloud sync settings

See `references/config.json` for full configuration options.

## Scripts Reference

- `scripts/mcp_server.py`: MCP server entry point
- `scripts/memory_cli.py`: Command-line interface
- `scripts/setup_database.py`: Initialize SQLite database
- `scripts/sync_to_cloud.py`: Manual cloud sync
- `scripts/export_graph.py`: Export knowledge graph visualization

## Best Practices

1. **Use sections**: Organize memories by domain
2. **Tag generously**: Enable better search
3. **Set importance**: Help prioritize retrieval
4. **Enable auto-injection**: Reduce manual context management
5. **Regular deduplication**: Keep memory clean
6. **Cloud sync**: Backup and multi-device access
7. **Prune old memories**: Prevent database bloat

## Troubleshooting

### Search returns no results
- Check section/tag filters
- Try broader query
- Verify embeddings are generated

### Slow search performance
- Run `VACUUM` on SQLite database
- Reduce `top_k` parameter
- Enable query caching

### Duplicate memories not detected
- Lower `similarity_threshold`
- Check embedding quality
- Verify content normalization

## Integration with Dive AI

Dive-Memory v3 integrates seamlessly with Dive AI V20:

```python
from dive_ai import DiveOrchestrator
from dive_memory_v3 import DiveMemory

# Initialize
orchestrator = DiveOrchestrator()
memory = DiveMemory()

# Enable memory for orchestrator
orchestrator.set_memory(memory)

# Execute task with auto-context injection
result = orchestrator.execute(
    task="Build authentication system",
    use_memory=True  # Auto-inject relevant memories
)

# Store execution results
memory.add(
    content=f"Task completed: {result.summary}",
    section="executions",
    tags=["authentication", "success"],
    metadata={"cost": result.cost, "time": result.duration}
)
```

## References

- Full API documentation: `references/api_reference.md`
- MCP protocol spec: `references/mcp_protocol.md`
- Database schema: `references/schema.sql`
- Configuration guide: `references/config.json`

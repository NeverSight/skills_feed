---
name: tools-router
description: "Unified router for all external tools: CLI binaries, MCP tools via lootbox, and data processing. Consolidates cli-router + tools-router + data-router."
---

# Tools Router (Unified)

**Consolidates**: cli-router + tools-router + data-router
**Purpose**: All external tool execution (CLI, MCP, databases)
**Legacy References**: `~/.claude/db/skills/routers/cli-router/`, `~/.claude/db/skills/routers/data-router/`

## CLI Tools (Local Binaries)

### AI/LLM Agents
| Tool | Binary | Purpose |
|:-----|:-------|:--------|
| gemini | /opt/homebrew/bin/gemini | Google Gemini CLI (2M context) |
| codex | ~/.local/bin/codex | OpenAI GPT models |
| amp | ~/.amp/bin/amp | Anthropic Claude via MCP |

### Context Extraction
| Tool | Binary | Purpose |
|:-----|:-------|:--------|
| research | ~/.local/bin/research | Online documentation |
| pieces | /opt/homebrew/bin/pieces | Local code context, LTM |

### Data Processing
| Tool | Binary | Purpose |
|:-----|:-------|:--------|
| qsv | qsv | Fast CSV processing |
| jq | jq | JSON processing |
| nu | nu | Nushell data pipelines |

### Semantic Search
| Tool | Binary | Purpose |
|:-----|:-------|:--------|
| ck | ck | Semantic code search |
| ast-grep | ast-grep | AST pattern matching |

---

# MCP Tools (Lootbox)

Routes tasks to MCP tools via lootbox code-mode for external service integration.

## MCP Tool Categories

### Knowledge Graph
| Tool | Namespace | Purpose |
|:-----|:----------|:--------|
| Neo4j | `neo4j` | Graph database operations |
| Neo4j Aura | `neo4j-aura` | Cloud Neo4j |
| Neo4j Memory | `neo4j-memory` | Agent memory graph |
| DeepGraph | `deepgraph` | Code graph analysis |

### Research & Search
| Tool | Namespace | Purpose |
|:-----|:----------|:--------|
| Perplexity | `perplexity` | AI-powered web search |
| Brave Search | `brave-search` | Web search |
| InfraNodus | `relate` | Graph-based text analysis |
| PageIndex | `pageindex-local` | Web page indexing |

### Methodology & Reasoning
| Tool | Namespace | Purpose |
|:-----|:----------|:--------|
| Meta-CC | `meta-cc` | Methodology capabilities |
| Distil (AoT) | `distil` | Atom of Thoughts |
| Zen | `zen` | Multi-model reasoning |
| Gepa | `gepa` | Gemini planning |

### Solvers
| Tool | Namespace | Purpose |
|:-----|:----------|:--------|
| Z3 | `solver-z3` | SMT solving |
| MiniZinc | `solver-minizinc` | Constraint optimization |
| PySAT | `solver-pysat` | SAT solving |
| MaxSAT | `solver-maxsat` | Maximum satisfiability |
| ASP | `solver-asp` | Answer set programming |

### Storage & Memory
| Tool | Namespace | Purpose |
|:-----|:----------|:--------|
| Filesystem | `filesystem` | File operations |
| MCP Memory | `mcp-memory` | Key-value memory |
| Obsidian Memory | `obsidian-memory` | Obsidian integration |
| TurboVault | `turbovault` | High-performance vault |

### External Services
| Tool | Namespace | Purpose |
|:-----|:----------|:--------|
| GitHub | `github` | GitHub API |
| Zotero | `zotero` | Citation management |
| Gemini | `gemini` | Gemini model access |

## Lootbox Code-Mode

### Configuration
```yaml
server: ws://localhost:9742/ws
ui: http://localhost:9742/ui
config: ~/lootbox.config.json
```

### Local Tools (Always Available)
```typescript
tools.kv.*       // Key-value store
tools.sqlite.*   // SQLite database
tools.memory.*   // In-memory storage
tools.graphql.*  // GraphQL queries
```

### Invocation Patterns

```bash
# List available tools
lootbox tools

# Execute single operation
lootbox exec 'await tools.neo4j.query({ cypher: "MATCH (n) RETURN n LIMIT 5" })'

# Chain operations
lootbox exec '
  const results = await tools.perplexity.search({ query: "Claude Code best practices" });
  await tools.kv.set({ key: "research", value: results });
  return results;
'

# Parallel operations
lootbox exec '
  const [a, b] = await Promise.all([
    tools.neo4j.query({ cypher: "MATCH (n:Skill) RETURN n" }),
    tools.deepgraph.semantic_search({ query: "authentication" })
  ]);
  return { skills: a, code: b };
'
```

## Routing Logic

```
MCP Task Detected
    │
    ├── Graph operations?
    │   ├── Neo4j? → tools.neo4j
    │   ├── Code graph? → tools.deepgraph
    │   └── Text graph? → tools.relate
    │
    ├── Research?
    │   ├── AI search? → tools.perplexity
    │   ├── Web search? → tools.brave-search
    │   └── Page index? → tools.pageindex-local
    │
    ├── Reasoning?
    │   ├── Methodology? → tools.meta-cc
    │   ├── Multi-model? → tools.zen
    │   └── AoT? → tools.distil
    │
    ├── Constraint solving?
    │   ├── SMT? → tools.solver-z3
    │   ├── Optimization? → tools.solver-minizinc
    │   └── SAT? → tools.solver-pysat
    │
    └── Storage?
        ├── Files? → tools.filesystem
        ├── KV? → tools.kv
        └── Memory? → tools.memory
```

## Tool Selection Matrix

| Task Type | Primary Tool | Alternative |
|:----------|:-------------|:------------|
| Graph query | neo4j | deepgraph |
| Web research | perplexity | brave-search |
| Code analysis | deepgraph | relate |
| Constraint solving | solver-z3 | solver-minizinc |
| File operations | filesystem | turbovault |
| Citation | zotero | - |
| Methodology | meta-cc | distil |

## Integration

- **lootbox**: Code-mode execution
- **MCP servers**: External tool providers
- **cli-index**: CLI tool fallback
- **meta-router**: Parent routing

## Quick Reference

```yaml
# Start lootbox server
lootbox server --port 9742

# Check available namespaces
lootbox tools

# Neo4j query
lootbox exec 'await tools.neo4j.query({ cypher: "..." })'

# Perplexity search
lootbox exec 'await tools.perplexity.search({ query: "..." })'

# Chained operations
lootbox exec '
  const data = await tools.X.fetch();
  return tools.Y.process(data);
'
```

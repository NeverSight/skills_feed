---
name: memory-manager
description: External persistent memory for cross-session knowledge. Use when storing error patterns, retrieving learned solutions, managing causal memory chains, or persisting project knowledge.
version: 1.0.0
category: autonomous-coding
layer: context-engineering
---

# Memory Manager

External persistent memory system for maintaining knowledge across autonomous coding sessions.

## Quick Start

### Store a Memory
```python
from scripts.memory_manager import MemoryManager

memory = MemoryManager(project_dir)
memory.store(
    key="auth_solution",
    value="Added User-Agent header to fix 403",
    memory_type="causal"
)
```

### Store Causal Chain (Error→Solution)
```python
memory.store_causal_chain(
    error="403 Forbidden on API call",
    solution="Add User-Agent header to requests"
)
```

### Retrieve Similar Errors
```python
solutions = memory.get_similar_errors("403 error calling API")
# Returns: [{"error": "403 Forbidden...", "solution": "Add User-Agent..."}]
```

## Memory Types

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORY TYPES                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  EPISODIC                                                    │
│  ├─ Past events and outcomes                                │
│  ├─ "Last time we deployed, X happened"                     │
│  └─ Session summaries                                       │
│                                                              │
│  PROCEDURAL                                                  │
│  ├─ Learned skills and patterns                             │
│  ├─ "How to set up database migrations"                     │
│  └─ Working code patterns                                   │
│                                                              │
│  SEMANTIC                                                    │
│  ├─ Factual knowledge about project                         │
│  ├─ "Database uses PostgreSQL"                              │
│  └─ Architecture decisions                                  │
│                                                              │
│  CAUSAL                                                      │
│  ├─ Error → Solution chains                                 │
│  ├─ "403 error → Add User-Agent header"                     │
│  └─ Self-healing patterns                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Storage Location

```
project/
└── .claude/
    └── memory/
        ├── episodic.json
        ├── procedural.json
        ├── semantic.json
        └── causal.json
```

## Causal Memory Pattern

```python
# Traditional error handling:
# Error occurs → Unclear response

# Causal memory:
# Error: 403 Forbidden
# Memory: [403] → [missing User-Agent] → [added header] → [success]
# Response: "Adding User-Agent header (learned from previous error)"
```

## Integration Points

- **error-recoverer**: Uses causal memory for self-healing
- **context-compactor**: Stores summaries in episodic memory
- **coding-agent**: Stores procedural patterns

## References

- `references/MEMORY-TYPES.md` - Detailed type documentation
- `references/RETRIEVAL-PATTERNS.md` - Search patterns

## Scripts

- `scripts/memory_manager.py` - Core MemoryManager
- `scripts/semantic_store.py` - Keyword-based storage
- `scripts/causal_memory.py` - Error→Solution chains
- `scripts/knowledge_base.py` - Project knowledge

---
name: skill-rag-router
description: Semantic skill discovery and routing using GraphRAG, vector embeddings, and multi-tool search. Automatically matches user intent to the most relevant skills from 144+ available options using ck semantic search, LEANN RAG, and knowledge graph relationships. Triggers on /meta queries, complex multi-domain tasks, explicit skill requests, or when task complexity exceeds threshold (files>20, domains>2, complexity>=0.7).
---

# Skill RAG Router

Intelligent skill discovery and routing system using semantic search and knowledge graph relationships.

## Capabilities

1. **Semantic Skill Search**: Uses `ck --sem` for meaning-based skill matching
2. **Hybrid Search**: Combines semantic + keyword matching via `ck --hybrid`
3. **Session Awareness**: Integrates with beads/bd for session context
4. **Memory Integration**: Uses claude-mem for cross-session learning

## Trigger Conditions

Activate this skill when:
- User explicitly requests skill discovery (`/meta`, "find a skill for...")
- Task complexity score >= 0.7
- Task involves > 20 files
- Task spans > 2 domains (frontend, backend, security, etc.)
- User asks "what skill can help with..."

## Usage

```bash
# Explicit invocation
/meta [query]

# Examples
/meta "optimize prompts for RAG pipeline"
/meta "debug authentication flow"
/meta "refactor legacy codebase"
```

## Search Implementation

```bash
# Semantic search for skills
ck --sem "[query]" ~/.claude/skills/ --jsonl --top-k 5

# Hybrid search (semantic + keyword)
ck --hybrid "[query]" ~/.claude/skills/ --threshold 0.6

# Index skills
ck --index ~/.claude/skills/ --model bge-small --quiet
```

## Output Format

Returns ranked skill suggestions with:
- Skill name and path
- Confidence score (0-1)
- Relevant snippet from SKILL.md
- Trigger match explanation

## Integration Points

- **SessionStart**: Indexes skills, loads routing cache
- **UserPromptSubmit**: Analyzes prompts for skill suggestions
- **beads/bd**: Session-aware task tracking
- **claude-mem**: Cross-session routing patterns

## Scripts

- `scripts/index-skills.sh`: Index all skills with ck
- `scripts/router.sh`: Main routing logic
- `scripts/suggest-skills.sh`: Intent → skill matching for hooks

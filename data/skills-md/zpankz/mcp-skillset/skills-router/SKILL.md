---
name: skills-router
description: Routes tasks to skills in skill-db and skill-library using semantic discovery. Triggers on specialized skill requirements, domain-specific tasks, or explicit skill requests. Uses skill-discovery, mcp-skillset, and skill-rag-router for semantic matching.
---

# Skills Router

Routes tasks to appropriate skills using semantic discovery across skill databases.

## Skill Databases

| Database | Location | Count | Purpose |
|:---------|:---------|:------|:--------|
| **skill-db** | ~/.claude/skill-db/ | 67+ | Primary skill source |
| **skill-library** | ~/.claude/skill-library/ | 48+ | Heavy/categorized skills |
| **skills (active)** | ~/.claude/skills/ | Variable | Currently loaded skills |

## Skill Categories

### Reasoning Skills (skill-db)
| Skill | Triggers | Purpose |
|:------|:---------|:--------|
| `think` | think, analyze, mental-model | Cognitive enhancement |
| `reason` | decompose, understand, break-down | Recursive decomposition |
| `AoT` | prove, atomic, formal | Atom of Thoughts |
| `urf` | universal, multi-scale, complex | Universal Reasoning |
| `ontolog` | holarchic, holons, ontology | Holarchic reasoning |
| `telos` | physiology, biological, teleological | Teleological analysis |
| `qp` | quantitative, calculate, physiological | Quantitative physiology |

### Development Skills (skill-db)
| Skill | Triggers | Purpose |
|:------|:---------|:--------|
| `terminal` | tui, cli, terminal-ui | Terminal UI design |
| `component` | command, agent, config | Claude Code components |
| `mcp-builder` | mcp, server, protocol | MCP development |
| `dspy` | dspy, prompts, optimize | DSPy optimization |

### Research Skills (skill-db)
| Skill | Triggers | Purpose |
|:------|:---------|:--------|
| `deep-research` | research, thorough, citations | 7-phase research |
| `notebooklm` | notebook, query, audio | NotebookLM integration |
| `skill-discovery` | find skill, discover, browse | Skill discovery |

### Context Skills (skill-db)
| Skill | Triggers | Purpose |
|:------|:---------|:--------|
| `context-orchestrator` | context, lifelog, ltm, limitless, pieces | Three-CLI context extraction |
| `limitless-cli` | pendant, personal memory, graph sync, extraction pipeline | Limitless CLI project development |

### Heavy Skills (skill-library)
| Skill | Triggers | Purpose |
|:------|:---------|:--------|
| `dialectical` | persuade, thesis, synthesis | Dialectical writing |
| `critique` | evaluate, lens, adversarial | Multi-lens critique |
| `constraints` | deontic, rights, permissions | Formal constraints |
| `saq` | saq, exam, model-answer | SAQ generation |
| `mega` | complex, n-superhypergraph | Meta-architecture |
| `textbook-grounding` | textbook, citations, syntopical | Textbook grounding |

## Routing Logic

```bash
# Semantic skill search
ck --sem "{query}" ~/.claude/skill-db/ --top-k 5

# Skill discovery metasystem
# (Invokes skill-discovery skill)

# mcp-skillset (when available)
mcp-skillset search "{query}"
```

## Decision Tree

```
Skill Task Detected
    │
    ├── Reasoning/Thinking?
    │   ├── Cognitive? → think
    │   ├── Formal proof? → AoT
    │   ├── Decomposition? → reason
    │   └── Complex system? → urf | mega
    │
    ├── Development?
    │   ├── Terminal UI? → terminal
    │   ├── MCP server? → mcp-builder
    │   └── Claude component? → component
    │
    ├── Research?
    │   ├── Deep dive? → deep-research
    │   ├── Skill finding? → skill-discovery
    │   └── NotebookLM? → notebooklm
    │
    ├── Context Extraction?
    │   ├── Personal/lifelog? → context-orchestrator → limitless
    │   ├── Documentation? → context-orchestrator → research
    │   ├── Local code/LTM? → context-orchestrator → pieces
    │   └── Limitless CLI development? → limitless-cli
    │
    ├── Writing?
    │   ├── Persuasive? → dialectical
    │   ├── SAQ/Exam? → saq | textbook-grounding
    │   └── Critique? → critique
    │
    ├── Data/Graph?
    │   ├── Knowledge graph? → hkgb | ontolog
    │   ├── Batch processing? → process | obsidian-batch
    │   └── Graph reasoning? → mega | graph
    │
    └── Domain-specific?
        ├── Physiology? → telos | qp
        ├── Scientific? → rct-appraisal
        └── Code quality? → code-skills/*
```

## Skill Loading Protocol

```yaml
progressive_loading:
  level_0: Read SKILL.md frontmatter only
  level_1: Read full SKILL.md
  level_2: Load references/*.md
  level_3: Load scripts/ and full capability

load_triggers:
  - Explicit skill invocation
  - Semantic match > 0.7
  - Domain keyword match
  - User request
```

## Integration

- **skill-discovery**: Semantic skill search
- **skill-rag-router**: GraphRAG-based routing
- **mcp-skillset**: MCP skill discovery
- **ck**: Semantic code search for skill content

## Quick Reference

```yaml
# Find skill semantically
ck --sem "formal reasoning proof" ~/.claude/skill-db/

# Load skill progressively
1. Check skill-db/{skill}/SKILL.md
2. If not found, check skill-library/{skill}/SKILL.md
3. Load frontmatter, then full skill on demand

# Skill invocation
/skill_name or invoke via Skill tool
```

---
name: delegate-router
description: |
  Unified router for agent delegation and skill routing. Absorbs agents-router + skills-router.
  Triggers on complex tasks, multi-step operations, research, exploration, or specialized skill needs.
---

# Delegate Router (Unified)

**Tier**: unified
**Absorbs**: agents-router, skills-router
**Agent Registry**: `~/.claude/config/agent-registry.yaml` (single source of truth)

> Consolidates: agents-router + skills-router
> Purpose: All delegation to subagents and skills

## Triggers
```yaml
patterns:
  - complex, multi-step, research, explore, ultrawork
  - spawn, delegate, use agent
  - specialized skill needed
  - complexity > 0.7, files > 20, domains > 2

complexity_factors:
  files_affected: 0.30
  domains_involved: 0.25
  steps_required: 0.25
  research_needed: 0.20
```

## Delegation Matrix

**Source**: All delegation decisions now reference `~/.claude/config/agent-registry.yaml`

This provides:
- Power-law tiered agent selection (Tier 1: 80% of work, Tier 2: 15%, Tier 3: 5%)
- Complexity-based model selection (haiku: 0.1-0.3, sonnet: 0.4-0.7, opus: 0.7-1.0)
- External CLI integration (gemini for >100K tokens)
- Single source of truth for all delegation logic

### Quick Reference (from agent-registry.yaml)

**Tier 1 (High-Impact)**: sisyphus-junior, explore, oracle, engineer
**Tier 2 (Specialized)**: librarian, architect, prometheus, momus, metis
**Tier 3 (Utility)**: document-writer, frontend-engineer, multimodal-looker
**External CLI**: gemini (>100K tokens), codex (GPT preference), amp (Claude-specific)

### Skill Discovery
```yaml
lookup_order:
  1. ~/.claude/skills/ (active, 23 skills)
  2. ~/.claude/db/skill-db/ (archived, 67+ skills)
  3. ~/.claude/db/skill-library/ (archived, 48+ skills)
```

## Decision Logic
```yaml
if complexity > 0.7:
  → oracle (analysis) or engineer (implementation)
if files > 20:
  → sisyphus-junior (focused execution)
if domains > 2:
  → architect (system design)
if tokens > 100K:
  → gemini CLI (external, 2M context)
if specialized_skill_match:
  → invoke skill directly
```

## Skill Categories (from skills-router)

| Category | Skills | Triggers |
|:---------|:-------|:---------|
| **Reasoning** | think, reason, AoT, urf, ontolog | analyze, decompose, prove, formal |
| **Research** | deep-research, skill-discovery | research, thorough, citations |
| **Context** | context-orchestrator | lifelog, ltm, personal, pieces |
| **Writing** | dialectical, critique, saq | persuade, evaluate, exam |
| **Development** | terminal, component, mcp-builder | tui, cli, mcp |

## Decision Tree

```
Task Complexity Assessment
    │
    ├── Exploration needed?
    │   ├── Quick search? → Explore (quick)
    │   ├── Pattern finding? → Explore (medium)
    │   └── Deep analysis? → Explore (very thorough)
    │
    ├── Implementation?
    │   ├── From PRD? → engineer
    │   ├── Architecture? → architect
    │   └── Strategy? → prometheus
    │
    ├── Research?
    │   ├── Web/docs? → researcher
    │   ├── Claude Code help? → claude-code-guide
    │   └── Large codebase? → gemini CLI
    │
    ├── Multi-domain?
    │   └── sisyphus-junior or architect
    │
    └── Skill match?
        └── Invoke via Skill tool
```

## Usage Patterns

### Parallel Agents (Independent Tasks)
```yaml
# Spawn together in single message
Task(explore, "find auth files") + Task(librarian, "search auth docs")
```

### Sequential Agents (Dependent Tasks)
```yaml
# Chain results
Task(explore, "find code") → Task(oracle, "debug issue")
```

### Background Execution (Long-Running)
```yaml
Task(sisyphus-junior, task, run_in_background=true)
→ TaskOutput(task_id) to retrieve results
```

## References
- Original agents-router: ~/.claude/db/skills/routers/agents-router/
- Original skills-router: ~/.claude/db/skills/routers/skills-router/

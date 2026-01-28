---
name: agents-router
description: Routes tasks to appropriate Task tool agents (subagents). Triggers on complex multi-step tasks, research, code review, exploration, or any task benefiting from specialized agent execution. Matches intent to agent types.
---

# Agents Router

Routes tasks to appropriate Task tool subagent types for parallel or specialized execution.

## Available Agent Types

| Agent | Purpose | Best For |
|:------|:--------|:---------|
| **general-purpose** | Multi-step research | Complex questions, code search |
| **Explore** | Codebase exploration | Find files, understand patterns |
| **Plan** | Implementation planning | Architecture, strategy |
| **claude-code-guide** | Claude Code help | Feature questions, how-to |
| **orchestrator** | Multi-domain coordination | Complex multi-agent workflows |
| **strategy-analyzer** | Deep strategic analysis | Refactoring, optimization |
| **architect** | Recursive decomposition | Complex system design |
| **gemini** | Long context analysis | Large codebases, multi-file bugs |
| **researcher** | Web research | Finding answers, investigating |
| **engineer** | Professional implementation | PRD execution, debugging |

## Trigger Conditions

Activate when task involves:
- Complex multi-step operations
- Research requiring web/documentation search
- Code review or analysis
- Codebase exploration (files > 20)
- Multi-domain tasks (domains > 2)
- Long-running background operations

## Routing Logic

```yaml
# Complexity scoring
complexity_factors:
  files_affected: weight 0.3
  domains_involved: weight 0.25
  steps_required: weight 0.25
  research_needed: weight 0.2

# Thresholds
spawn_agent_if:
  complexity >= 0.7 OR
  files > 20 OR
  domains > 2 OR
  explicit_request
```

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
    │   └── Strategy? → strategy-analyzer
    │
    ├── Research?
    │   ├── Web search? → researcher
    │   ├── Claude Code docs? → claude-code-guide
    │   └── Codebase context? → gemini
    │
    ├── Multi-domain?
    │   └── orchestrator
    │
    └── Code review?
        └── superpowers:code-reviewer (via skill)
```

## Agent Selection Matrix

| Task Type | Primary Agent | Alternatives |
|:----------|:--------------|:-------------|
| Find files by pattern | Explore | general-purpose |
| Search code for keyword | Explore | gemini |
| Plan implementation | Plan | architect |
| Deep strategic analysis | strategy-analyzer | architect |
| Large codebase analysis | gemini | Explore |
| Web research | researcher | general-purpose |
| Multi-agent coordination | orchestrator | general-purpose |
| PRD implementation | engineer | general-purpose |
| Claude Code help | claude-code-guide | - |

## Usage Patterns

### Parallel Agents
When tasks are independent:
```
Task tool (agent1) + Task tool (agent2) in parallel
```

### Sequential Agents
When tasks depend on each other:
```
Task tool (research) → Task tool (implement)
```

### Background Agents
For long-running tasks:
```
Task tool with run_in_background=true
→ TaskOutput to retrieve results
```

## Integration

- **Task tool**: Primary agent spawning
- **TaskOutput**: Result retrieval
- **orchestrator agent**: Multi-agent coordination
- **meta-router**: Parent routing

## Quick Reference

```yaml
# Quick codebase search
agent: Explore
thoroughness: quick

# Deep implementation planning
agent: Plan
complexity: high

# Large codebase bug
agent: gemini
context: 2M tokens

# Professional implementation
agent: engineer
from: PRD

# Multi-domain coordination
agent: orchestrator
domains: [frontend, backend, database]
```

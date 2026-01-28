---
name: commands-router
description: Routes tasks to reasoning frameworks and command patterns in commands-db. Triggers on structured development workflows, skill commands (sc:*), brainstorming, architecture, or any task matching command framework patterns. Uses reasoning-index for semantic routing.
---

# Commands Router

Routes tasks to appropriate reasoning frameworks and command patterns.

## Trigger Conditions

Activate when task involves:
- Structured development workflow (implement, build, test)
- Skill command invocation (sc:*)
- Brainstorming or ideation
- Architecture or design decisions
- Workflow templates
- Schema-based operations

## Command Categories

### SC Commands (Skill Commands)
Primary action verbs for development tasks.

| Command | Trigger Keywords | Purpose |
|:--------|:-----------------|:--------|
| `sc:analyze` | analyze, evaluate, assess, audit | Deep analysis |
| `sc:build` | build, compile, package | Build operations |
| `sc:cleanup` | clean, organize, declutter | Code cleanup |
| `sc:design` | design, architect, plan | Architecture |
| `sc:document` | document, readme, guide | Documentation |
| `sc:estimate` | estimate, cost, time | Estimation |
| `sc:explain` | explain, clarify, describe | Explanations |
| `sc:git` | commit, push, merge | Git operations |
| `sc:implement` | implement, code, feature | Implementation |
| `sc:improve` | improve, enhance, optimize | Improvement |
| `sc:load` | load, context, import | Context loading |
| `sc:spawn` | spawn, delegate, parallel | Delegation |
| `sc:task` | task, complex, persistent | Complex tasks |
| `sc:test` | test, verify, validate | Testing |
| `sc:troubleshoot` | debug, fix, diagnose | Debugging |
| `sc:workflow` | workflow, prd, process | Workflows |

### BMAD Framework
| Module | Purpose |
|:-------|:--------|
| `bmad:brainstorm` | Structured brainstorming |
| `bmad:party-mode` | Multi-agent ideation |
| `bmad:prd` | Product requirements |
| `bmad:architecture` | System architecture |

## Routing Logic

```bash
# Use reasoning-index for semantic routing
reasoning-index search "{user_intent}"
reasoning-index suggest "{task_description}"

# Example output:
# {
#   "commands": ["sc:implement", "sc:design"],
#   "skills": ["test-driven-development"],
#   "reasoning_chain": ["sc:design", "sc:implement", "sc:test"]
# }
```

## Decision Tree

```
Command Task Detected
    │
    ├── Implementation?
    │   ├── New feature? → sc:implement
    │   ├── Build? → sc:build
    │   └── Improvement? → sc:improve
    │
    ├── Analysis?
    │   ├── Code review? → sc:analyze
    │   ├── Debugging? → sc:troubleshoot
    │   └── Testing? → sc:test
    │
    ├── Design?
    │   ├── Architecture? → sc:design
    │   ├── Brainstorm? → bmad:brainstorm
    │   └── PRD? → bmad:prd
    │
    ├── Documentation?
    │   ├── README? → sc:document
    │   ├── Explain? → sc:explain
    │   └── Guide? → sc:document
    │
    └── Operations?
        ├── Git? → sc:git
        ├── Cleanup? → sc:cleanup
        └── Complex? → sc:task
```

## Usage

```bash
# Search commands
reasoning-index search "debug authentication"

# Get reasoning chain suggestion
reasoning-index suggest "implement user login"

# List all SC commands
reasoning-index list sc

# Build knowledge graph
reasoning-index graph "optimize performance" --depth 2
```

## Integration

- **reasoning-index**: Primary routing CLI
- **commands-db**: Command framework database
- **skill-db**: Skill integration
- **meta-router**: Parent router

## Command Chaining

```
Design → Implement → Test → Document

sc:design → sc:implement → sc:test → sc:document
```

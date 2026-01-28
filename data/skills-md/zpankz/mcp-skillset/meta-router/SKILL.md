---
name: meta-router
description: |
  Primary intent classifier and entry point for all skill routing. Routes requests through
  the unified 7-router hierarchy based on intent analysis. Triggers on any task requiring
  specialized skills or delegation.
---

# Meta Router

> Entry point for all routing decisions. Classifies intent and delegates to appropriate unified router.

## Unified Router Hierarchy (7 Active)

```
                     META-ROUTER
                    (Entry Point)
                         |
    +----------+---------+---------+----------+
    |          |         |         |          |
    v          v         v         v          v
DELEGATE    TOOLS     BUILD     THINK    CONTEXT
(agents)   (cli/mcp) (dev/docs) (reason) (extract)
                         |
                         v
                    GROUNDING
                   (medical/exam)
```

## Trigger Keywords by Router

```yaml
delegate-router:
  keywords: [complex, multi-step, spawn, delegate, agent, research, explore, ultrawork]
  complexity_triggers: [">0.7", "files>20", "domains>2"]
  route: ~/.claude/skills/routers/delegate-router/SKILL.md

tools-router:
  keywords: [shell, terminal, mcp, lootbox, graph, query, database, cli]
  route: ~/.claude/skills/routers/tools-router/SKILL.md

build-router:
  keywords: [build, implement, code, create, feature, component, docs, readme, deploy]
  absorbs: [development, infrastructure, documentation]
  route: ~/.claude/skills/routers/build-router/SKILL.md

think-router:
  keywords: [analyze, debug, reason, research, investigate, prove, verify, think]
  absorbs: [reasoning, research, analysis]
  route: ~/.claude/skills/routers/think-router/SKILL.md

context-router:
  keywords: [context, lifelog, limitless, pieces, ltm, screenapp, recording]
  route: ~/.claude/skills/routers/context-router/SKILL.md

grounding-router:
  keywords: [saq, viva, medical, exam, anzca, cicm, pex, clinical]
  route: ~/.claude/skills/routers/grounding-router/SKILL.md
```

## Routing Logic

### Weight Distribution

| Factor | Weight | Description |
|--------|--------|-------------|
| Keyword Match | 40% | Scan user intent for trigger keywords |
| Context Analysis | 30% | Current project type, recent operations |
| History Pattern | 20% | Recent skill usage patterns |
| Explicit Request | 10% | User directly names skill/category |

### Decision Flow

```
User Intent
    |
    v
Keyword Extraction --> Category Match --> Load Unified Router
                                              |
                                              v
                                    Router-Specific Logic --> Skill/Agent
```

## Direct Shortcuts (Bypass Routing)

For known skills, bypass routing entirely:

```yaml
# Skill shortcuts
/ultrawork     -> ~/.claude/skills/ultrawork/SKILL.md
/learn         -> ~/.claude/skills/learn/SKILL.md
/lambda        -> ~/.claude/skills/lambda-skill/SKILL.md
/obsidian      -> ~/.claude/skills/obsidian/SKILL.md
/git           -> ~/.claude/skills/git-master/SKILL.md

# Agent shortcuts
oracle         -> oracle agent (complex debugging)
explore        -> explore agent (quick search)
sisyphus       -> sisyphus-junior agent (focused execution)
```

## Complexity Assessment

```python
def assess_complexity(task):
    score = (
        0.30 * files_affected(task) +
        0.25 * domains_involved(task) +
        0.25 * steps_required(task) +
        0.20 * research_needed(task)
    )
    return score

# Routing thresholds
if score > 0.7:
    route_to("delegate-router")  # Complex delegation
elif score > 0.4:
    route_to("think-router")     # Analysis needed
else:
    route_to("build-router")     # Direct execution
```

## Usage

When this router activates:

1. Announce: "Routing to [router] for [reason]"
2. Load the unified router
3. The router further refines to specific skill/agent

## Legacy Router Migration

| Legacy Router | Absorbed By |
|---------------|-------------|
| agents-router | delegate-router |
| skills-router | delegate-router |
| cli-router | tools-router |
| data-router | tools-router |
| development-router | build-router |
| infrastructure-router | build-router |
| documentation-router | build-router |
| reasoning-router | think-router |
| research-router | think-router |
| analysis-router | think-router |

Legacy routers archived in: `~/.claude/db/skills/routers/`

## Integration

**Incoming**: All user requests
**Outgoing**: [delegate-router](../delegate-router/SKILL.md), [tools-router](../tools-router/SKILL.md), [build-router](../build-router/SKILL.md), [think-router](../think-router/SKILL.md), [context-router](../context-router/SKILL.md), [grounding-router](../grounding-router/SKILL.md)
**Related**: [UNIFIED-ARCHITECTURE](../UNIFIED-ARCHITECTURE.md)

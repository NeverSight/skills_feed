---
name: maestro-core
description: Use when any Maestro skill loads - provides skill hierarchy, HALT/DEGRADE policies, and trigger routing rules for orchestration decisions
---

# Maestro Core - Workflow Router

Central hub for Maestro workflow skills. Routes triggers, defines hierarchy, and handles fallbacks.

## Skill Hierarchy

```
conductor (1) > orchestrator (2) > designing (3) > tracking (4) > specialized (5)
```

Higher rank wins on conflicts.

## Ownership Matrix

| Skill | Owns | Primary Triggers |
|-------|------|------------------|
| conductor | Implementation + autonomous | `ci`, `ca`, `/conductor-implement`, `/conductor-autonomous` |
| orchestrator | Parallel execution | `co`, `/conductor-orchestrate` |
| designing | Phases 1-10 (design → track creation) | `ds`, `cn`, `/conductor-newtrack`, `/conductor-design` |
| tracking | Task/bead management | `bd *`, `fb`, `rb` |
| handoff | Session cycling | `ho`, `/conductor-finish`, `/conductor-handoff` |
| creating-skills | Skill authoring | "create skill", "write skill" |

## Workflow Chain

```
ds/cn → design.md → /conductor-newtrack → spec.md + plan.md → fb → tracking → ci/co/ca → implementation
```

## Routing Table

**CRITICAL:** After loading `maestro-core`, you MUST explicitly load the target skill via `skill(name="...")` before proceeding.

See **[routing-table.md](references/routing-table.md)** for complete trigger → skill mappings, phrase triggers, and conditional routing logic.

### Quick Triggers

| Trigger | Skill |
|---------|-------|
| `ds`, `cn` | designing |
| `ci` | conductor |
| `ca` | conductor |
| `co` | orchestrator |
| `fb`, `rb`, `bd *` | tracking |
| `ho` | handoff |

### Routing Flow

```
1. User triggers command (e.g., `ci`)
2. Load maestro-core → get routing table
3. Look up trigger → find target skill
4. MUST call skill tool to load target skill
5. Follow loaded skill instructions
```

## Fallback Policies

| Condition | Action | Message |
|-----------|--------|---------|
| `bd` unavailable | HALT | `❌ Cannot proceed: bd CLI required` |
| `conductor/` missing | DEGRADE | `⚠️ Standalone mode - limited features` |
| Agent Mail unavailable | HALT | `❌ Cannot proceed: Agent Mail required for coordination` |

## Quick Reference

| Concern | Reference |
|---------|-----------|
| Complete workflow | [workflow-chain.md](references/workflow-chain.md) |
| All routing rules | [routing-table.md](references/routing-table.md) |
| Terms and concepts | [glossary.md](references/glossary.md) |
| CLI toolboxes | [toolboxes.md](references/toolboxes.md) |

## Related Skills

- [designing](../designing/SKILL.md) - Double Diamond design sessions (phases 1-10)
- [conductor](../conductor/SKILL.md) - Implementation execution
- [orchestrator](../orchestrator/SKILL.md) - Multi-agent parallel execution
- [tracking](../tracking/SKILL.md) - Issue tracking and dependency graphs
- [handoff](../handoff/SKILL.md) - Session cycling and context preservation
- [creating-skills](../creating-skills/SKILL.md) - Skill authoring and best practices
- [sharing-skills](../sharing-skills/SKILL.md) - Contributing skills upstream
- [using-git-worktrees](../using-git-worktrees/SKILL.md) - Isolated workspaces

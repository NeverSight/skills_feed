---
name: faion-product-manager
description: "Product orchestrator: planning (MVP, roadmaps) and operations (prioritization, backlog)."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Bash(mkdir:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Product Manager Skill

**Communication: User's language. Docs: English.**

## Purpose

Orchestrates product management activities: planning, operations, discovery, launch.

**Architecture:** Orchestrator → 2 sub-skills (17 + 16 methodologies)

---

## Sub-Skills

| Sub-Skill | Focus | Methodologies |
|-----------|-------|---------------|
| [faion-product-manager:planning](../faion-product-manager:planning/SKILL.md) | MVP/MLP, roadmaps, discovery, launch | 17 |
| [faion-product-manager:operations](../faion-product-manager:operations/SKILL.md) | Prioritization, backlog, analytics, lifecycle | 16 |

**Total:** 33 methodologies | 2 agents

---

## Decision Tree

### Planning Activities
Use [faion-product-manager:planning](../faion-product-manager:planning/SKILL.md):
- Define MVP/MLP scope
- Create roadmaps (Now-Next-Later, outcome-based)
- User story mapping
- Product discovery and validation
- Launch planning
- OKR setting

### Operations Activities
Use [faion-product-manager:operations](../faion-product-manager:operations/SKILL.md):
- Feature prioritization (RICE, MoSCoW)
- Backlog management and grooming
- Product analytics and metrics
- Feedback management
- Technical debt tracking
- Stakeholder management

---

## Quick Reference

| Resource | Location | Content |
|----------|----------|---------|
| **Workflows** | [workflows.md](workflows.md) | Bootstrap, MLP transformation flows |
| **Agents** | [agents.md](agents.md) | MVP analyzer, MLP orchestrator |
| **Methodologies** | [methodologies-summary.md](methodologies-summary.md) | Full 33-methodology catalog |

---

## Common Workflows

**New Product:**
```
mvp-scoping → feature-prioritization-rice → user-story-mapping → roadmap-design → product-launch
```

**Quarterly Planning:**
```
okr-setting → backlog-management → feature-prioritization-rice → release-planning
```

**Discovery Sprint:**
```
product-discovery → continuous-discovery → feedback-management → backlog-management
```

---

## Agents

| Agent | Purpose | Location |
|-------|---------|----------|
| faion-mvp-scope-analyzer-agent | MVP scope via competitor analysis | [agents.md](agents.md) |
| faion-mlp-agent | MLP orchestrator (5 modes) | [agents.md](agents.md) |

---

## Cross-Skill Routing

| Need | Route To |
|------|----------|
| Market research, competitors | [faion-researcher](../faion-researcher/SKILL.md) |
| Technical architecture | [faion-software-architect](../faion-software-architect/SKILL.md) |
| Specs to implementation | [faion-sdd](../faion-sdd/SKILL.md) |
| Execution tracking | [faion-project-manager](../faion-project-manager/SKILL.md) |
| Requirements analysis | [faion-business-analyst](../faion-business-analyst/SKILL.md) |

---

*Product Manager Orchestrator v2.0*
*33 Methodologies | 2 Sub-Skills | 2 Agents*

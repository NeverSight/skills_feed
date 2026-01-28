---
name: faion-product-planning
description: "Product planning: MVP/MLP scoping, roadmaps, user story mapping, OKRs."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Product Planning Sub-Skill

**Communication: User's language. Docs: English.**

## Purpose

Product planning from ideation to launch: MVP/MLP scoping, roadmaps, discovery, launch planning.

**Parent:** [faion-product-manager](../faion-product-manager/SKILL.md)

---

## Decision Tree

| If you need... | Use | File |
|----------------|-----|------|
| **Define MVP scope** | mvp-scoping | [mvp-scoping.md](mvp-scoping.md) |
| **Choose product framework** | minimum-product-frameworks | [minimum-product-frameworks.md](minimum-product-frameworks.md) |
| **Transform MVP to MLP** | mlp-planning | [mlp-planning.md](mlp-planning.md) |
| **Quick validation** | micro-mvps | [micro-mvps.md](micro-mvps.md) |
| **Roadmap (uncertain timeline)** | roadmap-design | [roadmap-design.md](roadmap-design.md) |
| **Roadmap (outcome-based)** | outcome-based-roadmaps | [outcome-based-roadmaps.md](outcome-based-roadmaps.md) |
| **User stories** | user-story-mapping | [user-story-mapping.md](user-story-mapping.md) |
| **Sprint planning** | release-planning | [release-planning.md](release-planning.md) |
| **Set goals** | okr-setting | [okr-setting.md](okr-setting.md) |
| **Launch planning** | product-launch | [product-launch.md](product-launch.md) |
| **Discovery process** | continuous-discovery | [continuous-discovery.md](continuous-discovery.md) |
| **Positioning** | competitive-positioning | [competitive-positioning.md](competitive-positioning.md) |
| **Portfolio management** | portfolio-strategy | [portfolio-strategy.md](portfolio-strategy.md) |
| **Write specs** | spec-writing | [spec-writing.md](spec-writing.md) |

---

## Core Methodologies (17)

### MVP & MLP
- **mvp-scoping** - Define core problem, minimum features, 4-week constraint
- **mlp-planning** - Transform MVP to Most Lovable Product
- **minimum-product-frameworks** - 9 frameworks (MVP/MLP/MMP/MAC/RAT/MDP/MVA/MFP/SLC)
- **micro-mvps** - Landing page, concierge, Wizard of Oz validation

### Planning & Roadmaps
- **roadmap-design** - Now-Next-Later roadmaps
- **outcome-based-roadmaps** - Outcome-focused planning
- **outcome-based-roadmaps-advanced** - Advanced outcome roadmapping
- **user-story-mapping** - Activities → Tasks → Releases
- **okr-setting** - Objectives + Key Results
- **release-planning** - Sprint goal, velocity, capacity
- **portfolio-strategy** - Multi-product portfolio management

### Discovery & Launch
- **product-discovery** - Five Whys to root cause
- **continuous-discovery** - Ongoing discovery habits
- **continuous-discovery-habits** - Weekly touchpoints framework
- **product-launch** - Launch timeline and execution
- **competitive-positioning** - Market positioning analysis
- **spec-writing** - Product specification authoring

---

## Common Sequences

- **New product:** mvp-scoping → user-story-mapping → roadmap-design → product-launch
- **Discovery sprint:** product-discovery → continuous-discovery → spec-writing
- **Planning cycle:** okr-setting → roadmap-design → release-planning

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [faion-product-manager](../faion-product-manager/SKILL.md) | Parent orchestrator |
| [faion-product-manager:operations](../faion-product-manager:operations/SKILL.md) | Sibling (prioritization, backlog) |
| [faion-researcher](../faion-researcher/SKILL.md) | Market data for planning |
| [faion-sdd](../faion-sdd/SKILL.md) | Specs to implementation |

---

*Product Planning Sub-Skill v1.0*
*17 Methodologies*

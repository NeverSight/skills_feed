---
name: feature-workflow
description: Feature planning, specification, phased implementation, progress tracking, per-phase PRs, and archival workflow. Use when starting a new feature, creating spec documents, breaking work into phases, tracking progress, managing PRs, or archiving completed specs.
license: MIT
metadata:
  author: arraydude
  version: "1.0.0"
---

# Feature Workflow

Comprehensive guide for planning, specifying, implementing, and archiving features. Contains 18 rules across 6 categories, derived from 18+ completed feature specs.

## When to Apply

Reference these guidelines when:
- Starting a new feature or migration
- Creating or updating a spec document
- Breaking work into implementation phases
- Tracking progress within a spec
- Deciding PR scope and branch strategy
- Completing a feature and archiving the spec

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Spec Structure & Content | CRITICAL | `spec-` |
| 2 | Phase Design | CRITICAL | `phase-` |
| 3 | Progress Tracking | HIGH | `tracking-` |
| 4 | PR Strategy | HIGH | `pr-` |
| 5 | Archival | MEDIUM | `archive-` |
| 6 | Workflow Collaboration | MEDIUM | `workflow-` |

## Quick Reference

### 1. Spec Structure & Content (CRITICAL)

- `spec-structure` - Required spec document structure (title, metadata, ToC, sections)
- `spec-content-sections` - What each section must contain (Executive Summary, Goals, Architecture, Plan, Testing, Criteria)
- `spec-current-state-analysis` - Always start with current state: code inventory, problems with evidence
- `spec-living-document` - Update spec throughout implementation, never delete history

### 2. Phase Design (CRITICAL)

- `phase-zero-foundation` - Phase 0 is always foundation/infrastructure work
- `phase-decomposition` - Break work into independently reviewable, shippable phases
- `phase-dependency-ordering` - Order phases by dependency chain

### 3. Progress Tracking (HIGH)

- `tracking-status-indicators` - Use consistent status indicators and progress trackers
- `tracking-completion-reports` - Write completion reports per phase
- `tracking-metrics-tables` - Include before/after metrics tables

### 4. PR Strategy (HIGH)

- `pr-per-phase-strategy` - One PR per phase for reviewability
- `pr-branch-naming` - Branch naming follows GitFlow conventions
- `pr-scope-and-review` - Keep PRs focused with clear scope documentation

### 5. Archival (MEDIUM)

- `archive-when-to-archive` - Archive after all phases complete and PRs merged
- `archive-preservation-format` - Preserve completion notes, learnings, and metrics

### 6. Workflow Collaboration (MEDIUM)

- `workflow-collaboration-loop` - Iterative planning between AI and developer
- `workflow-spec-placement` - Place specs under the relevant package .claude/ directory
- `workflow-iteration-patterns` - How to iterate when requirements change

## Core Workflow

1. **Discovery** - Developer describes the feature/problem
2. **Analysis** - Explore codebase, document current state
3. **Proposal** - Draft spec with architecture and phases
4. **Review** - Developer reviews, provides feedback
5. **Refinement** - Update spec based on feedback
6. **Approval** - Developer confirms plan
7. **Implementation** - Phase-by-phase with per-phase PRs
8. **Archive** - Move completed spec, capture learnings

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/spec-structure.md
rules/phase-decomposition.md
rules/tracking-status-indicators.md
rules/pr-per-phase-strategy.md
rules/archive-when-to-archive.md
rules/workflow-collaboration-loop.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect example (anti-pattern)
- Correct example (best practice)

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

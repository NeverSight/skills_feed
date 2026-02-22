---
name: artifact-updater
description: '[DEPRECATED] Route through type-specific updaters: skill-updater, agent-updater, workflow-updater.'
version: 2.0.0
model: sonnet
invoked_by: both
user_invocable: false
tools: [Read]
verified: true
lastVerifiedAt: 2026-02-19T12:00:00.000Z
---

# Artifact Updater (Deprecated)

This skill has been superseded by type-specific updaters with full enterprise bundle support:

| Artifact Type | Use Instead                              |
| ------------- | ---------------------------------------- |
| Skills        | `skill-updater`                          |
| Agents        | `agent-updater`                          |
| Workflows     | `workflow-updater`                       |
| Hooks         | `hook-creator` (create) or manual update |

## Why Deprecated

The generic artifact-updater lacked:

- Research gates (Exa/arXiv queries)
- Enterprise bundle validation and scaffolding
- Risk scoring specific to each artifact type
- Protected sections manifests
- Cascade detection
- Companion validation

Type-specific updaters provide all of these features.

## Archive

Original stub archived to `.claude/skills/_archive/artifact-updater/`.

---
name: feature-implementation
description: Use when the user asks to implement a new feature, enhancement, add functionality, build something new, or create new capabilities. Triggers on keywords like "implement", "add feature", "build", "create new", "develop", "enhancement".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, WebSearch, TodoWrite
infer: true
---

# Feature Implementation

Expert full-stack .NET + Angular implementation skill with structured investigation, planning, and layered execution.

## Mode Selection

| Mode                      | Flag           | Behavior                                                                             |
| ------------------------- | -------------- | ------------------------------------------------------------------------------------ |
| **Interactive** (default) | _(none)_       | Approval gates at plan + execution; user feedback loop                               |
| **Autonomous**            | `--autonomous` | Structured headless workflow; approval gate at plan only, then execute to completion |

## Workflow Overview

1. **Investigate** -- Decompose requirements, search codebase for related entities/patterns/boundaries
2. **Knowledge Graph** -- Build structured analysis in `.ai/workspace/analysis/{feature}.md`
3. **Plan** -- Generate layered implementation plan (Domain > Persistence > Application > API > Frontend)
4. **Approval Gate** -- Present plan for user approval; do NOT proceed without it
5. **Execute** -- Implement layer-by-layer following approved plan
6. **Verify** -- Type checks, tests, integration validation

> **⚠️ MUST READ** `.claude/skills/feature-implementation/references/implementation-workflow.md` for detailed phase instructions.

## ⚠️ MUST READ Before Implementation

**IMPORTANT: You MUST read these files before starting. Do NOT skip.**

- **⚠️ MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` — validation checkpoints
- **⚠️ MUST READ** `.claude/skills/shared/knowledge-graph-template.md` — per-file analysis structure
- **⚠️ MUST READ** `CLAUDE.md` — codebase instructions and platform patterns

## Implementation Order

### Backend (bottom-up)

1. Domain Layer -- Entity, expressions, value objects
2. Persistence Layer -- Configuration, migration
3. Application Layer -- DTOs, commands, queries, event handlers
4. API Layer -- Controller endpoints

### Frontend (service-first)

1. API Service -- `PlatformApiService` extension
2. Store -- `PlatformVmStore` state management
3. Components -- `AppBaseVmStoreComponent` / `AppBaseFormComponent`
4. Routing -- Route definitions and guards

## Approval Gate Format

```markdown
## Implementation Plan Complete - Approval Required

### Summary
[Brief description]

### Files to Create
1. `path/to/file` - [purpose]

### Files to Modify
1. `path/to/file:line` - [change description]

### Implementation Order
1. [Step 1] ... N. [Step N]

### Risks & Considerations
- [Risk 1]

**Awaiting approval to proceed with implementation.**
```

## Execution Safeguards

- Verify file exists before modification
- Read current content before editing
- Check conflicts with existing code
- Validate changes against platform patterns
- If any step fails: HALT, report failure, return to approval gate

## Post-Implementation

- Verify against all requirements
- Document under `## Success Validation` heading
- Summarize changes in `changelog.md`

> **⚠️ MUST READ** `.claude/skills/feature-implementation/references/validation-checklist.md` for verification items.
> **⚠️ MUST READ** `.claude/skills/feature-implementation/references/ep-file-locations.md` for path reference and related skills.

## Coding Guidelines

- Evidence-based: verify assumptions with grep/search
- Platform-first: use established EasyPlatform patterns
- Cross-service: use event bus, never direct DB access
- CQRS: Command + Result + Handler in ONE file
- Logic in LOWEST layer: Entity > Service > Component


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

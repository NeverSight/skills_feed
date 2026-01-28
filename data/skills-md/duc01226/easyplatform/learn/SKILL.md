---
name: learn
description: Teach Claude a new pattern, preference, or convention explicitly. Use when you want to save a correction, preference, or coding pattern for future sessions. Triggers on keywords like "remember this", "always do", "never do", "learn this pattern", "/learn".
allowed-tools: Read, Write, Edit, Bash
infer: true
---

# Pattern Learning Skill

Explicitly teach Claude patterns, preferences, or conventions to remember across sessions.

## Quick Usage

```
/learn always use PlatformValidationResult instead of throwing ValidationException
/learn [wrong] var x = 1 [right] const x = 1 - always prefer const
/learn backend: DTO mapping should be in the DTO class, not in command handlers
```

## Teaching Formats

### Format 1: Natural Language
```
/learn always use IGrowthRootRepository instead of generic IPlatformRootRepository
```
Detected patterns: "always use X instead of Y", "prefer X over Y", "never do X"

### Format 2: Explicit Wrong/Right
```
/learn [wrong] throw new ValidationException("Invalid") [right] return PlatformValidationResult.Invalid("Invalid")
```

### Format 3: Category-Specific
```
/learn backend: always add [ComputedEntityProperty] with empty setter
/learn frontend: extend AppBaseComponent instead of raw Component
/learn workflow: always use TodoWrite before multi-step tasks
```

## How It Works

1. **Detection**: `pattern-learner.cjs` hook detects teaching input
2. **Extraction**: Extracts wrong/right pair, keywords, context
3. **Storage**: Saves to `.claude/learned-patterns/{category}/{slug}.yaml`
4. **Injection**: Future sessions auto-inject relevant patterns (max 5, ~400 tokens)

## Pattern Categories

| Category   | Use For                                        |
| ---------- | ---------------------------------------------- |
| `backend`  | C#, .NET, API, Entity, Repository patterns     |
| `frontend` | Angular, TypeScript, Component, Store patterns |
| `workflow` | Development process, git, planning patterns    |
| `general`  | Cross-cutting concerns                         |

## Confidence System

- Explicit teaching: starts at **80%**
- Implicit corrections: starts at **40%**
- Increases on: user confirmation, pattern followed
- Decreases on: pattern conflicts, 30 days unused (decay)
- Below **20%**: auto-archived

Conflicts with `docs/claude/*.md` are blocked to prevent inconsistencies.

## Storage

```
.claude/learned-patterns/
├── index.yaml       # Pattern lookup index
├── backend/         # Backend patterns
├── frontend/        # Frontend patterns
├── workflow/        # Workflow patterns
├── general/         # General patterns
└── archive/         # Archived patterns
```

## Related

For lifecycle management (list, view, archive, boost, penalize): use `/learned-patterns` skill.


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

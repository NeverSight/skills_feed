---
name: plan-to-tasks
description: Convert project plans to JSONL format (issues + dependencies). Use when users ask "convert plan to jsonl", "create jsonl from plan", "export plan as json" or "convert plan to taks", "create tasks from plan", "export plan as tasks".
---

# Plan to JSONL Converter

Transform project plans into JSONL format: **Story (Epic) → Task → SubTask** with embedded dependencies.

## When to Apply

Use this skill when:
- User provides a project plan/spec to break down
- Converting markdown plans to JSONL format
- Exporting task hierarchies as structured data
- Creating work queues for external systems
- User asks to "convert to jsonl", "create jsonl from plan", "export plan as json"

## Core Conversion Process

### Step 1: Analyze the Plan

Identify three levels:
- **Stories (Epics)**: Major features/components → Type: `epic`
- **Tasks**: Implementation work → Type: `task`
- **SubTasks**: Granular actions → Type: `task`

**CRITICAL**: Extract ALL details from plan - see [Information Extraction](./rules/information-extraction.md).

### Step 2: Create Self-Contained Tasks

Each task must include complete context for agent to work independently. Agent selects by priority only - no hierarchy traversal.

See [Self-Contained Tasks](./rules/self-contained-tasks.md) for template and examples.

### Step 3: Add Dependencies

Use appropriate dependency types: `blocks`, `depends_on`, `related`, `discovered-from`.

See [Dependency Types](./rules/dependency-types.md) for patterns.

## Rules Summary

Detailed rules in `rules/` directory:

- **[TDD-First Approach](./rules/tdd-first-approach.md)** - Mandatory Red→Green→Refactor for features/bugs
- **[Type Schema](./rules/type-schema.md)** - TypeScript type definition and task characteristics
- **[Self-Contained Tasks](./rules/self-contained-tasks.md)** - 1500+ char descriptions with complete context
- **[Information Extraction](./rules/information-extraction.md)** - Extract requirements, user stories, specs
- **[Dependency Types](./rules/dependency-types.md)** - blocks, related, discovered-from, parent-child
- **[Priority Scale](./rules/priority-scale.md)** - P0-P4 rationale (hard tasks first)
- **[Labels Organization](./rules/labels-organization.md)** - Feature grouping, TDD phases, stack tags
- **[JSONL Queries](./rules/jsonl-queries.md)** - 50+ jq command examples
- **[Best Practices](./rules/best-practices.md)** - Output format, expected structure, final checklist

## Example

Given:
```markdown
Feature: User Authentication
- Login with email/password
- JWT tokens (15min access, 7day refresh)
- Rate limiting (5 attempts per 15min)
```

Convert to JSONL with:
- Complete technical approach (bcrypt, JWT, Redis)
- Implementation details (files, functions, config)
- Error handling (400/401/403/429/500)
- Testing requirements (coverage, test cases)
- Dependencies (bcrypt, jsonwebtoken, ioredis)

See [Self-Contained Tasks](./rules/self-contained-tasks.md) for full example.

## Related Skills

- `/tdd-integration` - TDD Red-Green-Refactor cycle for implementation

## Output Structure

```
└── plan/issues.jsonl  # One issue per line, dependencies embedded
```

Each line: complete JSON object following [Type Schema](./rules/type-schema.md).

**STOP ONCE JSONL IS CREATED!**
**DO NOT IMPLEMENT OR TEST ANYTHING YET!**

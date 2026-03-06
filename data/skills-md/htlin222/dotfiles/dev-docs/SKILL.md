---
name: dev-docs
description: Create comprehensive strategic plan and dev docs for large tasks. Invoke when starting large tasks that span multiple sessions.
allowed-tools: Bash, Read, Write, Glob, Grep, TodoWrite
---

# Dev docs system

Creates a structured documentation system for large tasks to maintain context across sessions.

## When to invoke

- When starting a large, multi-session task
- When you need to track progress across context compactions
- When working on complex implementations requiring documentation
- Before major refactoring or feature development

## Usage

```
/dev-docs [task-name]
```

## Instructions

When this command runs:

1. **Create dev docs directory structure**:

   ```
   dev/active/[task-name]/
   ├── plan.md      # Strategic implementation plan
   ├── context.md   # Key files, decisions, dependencies
   └── tasks.md     # Detailed task checklist
   ```

2. **Generate plan.md** with:
   - Task overview and objectives
   - High-level implementation strategy
   - Key architectural decisions
   - Risk assessment and mitigation
   - Success criteria

3. **Generate context.md** with:
   - List of key files to modify
   - Important code patterns and conventions discovered
   - External dependencies and their versions
   - Design decisions and rationale
   - Links to relevant documentation

4. **Generate tasks.md** with:
   - Detailed, actionable task checklist
   - Estimated complexity for each task
   - Dependencies between tasks
   - Progress tracking checkboxes

5. **Update TodoWrite** with the initial tasks

## Template structure

### plan.md

```markdown
# [Task Name] - Implementation plan

## Overview

[Brief description of what we're building]

## Objectives

- [ ] Objective 1
- [ ] Objective 2

## Strategy

[High-level approach]

## Architecture decisions

- Decision 1: [rationale]

## Risks

| Risk | Mitigation |
| ---- | ---------- |
|      |            |

## Success criteria

- [ ] Criteria 1
```

### context.md

```markdown
# [Task Name] - Context

## Key files

- `path/to/file.ts` - [purpose]

## Code patterns

- Pattern 1: [description]

## Dependencies

- package@version - [why needed]

## Decisions log

| Date | Decision | Rationale |
| ---- | -------- | --------- |
|      |          |           |
```

### tasks.md

```markdown
# [Task Name] - Tasks

## Phase 1: Setup

- [ ] Task 1 (S)
- [ ] Task 2 (M)

## Phase 2: Implementation

- [ ] Task 3 (L)

## Phase 3: Testing

- [ ] Task 4 (S)

Legend: (S)mall, (M)edium, (L)arge
```

## Notes

- Run `/update-dev-docs` before session compaction to capture progress
- Keep context.md updated as you discover new information
- Check off tasks in tasks.md as you complete them

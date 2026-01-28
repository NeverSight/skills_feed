---
name: writing-plans
description: Use when design is complete and you need detailed implementation tasks for engineers with zero codebase context - creates comprehensive guides with exact file paths, code examples, and verification steps; task granularity 2-5 minutes per step
version: 2025-11-04
related_skills:
  - executing-plans (execute the plan you create)
  - starwards-tdd (each task should follow TDD)
  - using-superpowers (announce skill usage)
---

# Writing Implementation Plans

## Overview

Use when design is complete and you need detailed implementation tasks for engineers with minimal codebase familiarity. Creates comprehensive guides with exact file paths, code examples, and verification steps.

## Key Characteristics

**Task Granularity:** Each step represents 2-5 minutes of work, breaking down features into atomic actions like writing failing tests, implementing solutions, and committing changes.

**Documentation Standard:** Plans follow a mandatory header format including goal, architecture, and tech stack, followed by numbered tasks with file locations, code snippets, and exact command sequences.

## Plan Structure

```markdown
# Feature Name

## Goal
[One sentence: what this accomplishes]

## Architecture
[How this fits in the system]

## Tech Stack
- [Libraries/frameworks used]

## Tasks

### 1. [Task name]
**File:** `path/to/file.ts`

[What to do]

**Code:**
```typescript
[Exact code or snippet]
```

**Verify:**
```bash
[Commands to run]
```

**Commit:** `[commit message]`

### 2. [Next task...]
```

## Core Principles

- **DRY** - Don't Repeat Yourself
- **YAGNI** - You Aren't Gonna Need It
- **TDD** - Test-Driven Development
- **Frequent commits** - One task, one commit

## Execution Workflow

After completion, offer two implementation paths:

1. **Subagent-Driven** — Dispatch fresh agents per task with reviews within the current session
2. **Parallel Session** — Guide toward separate sessions using the executing-plans skill

## When to Use

- Design phase is complete
- Need step-by-step implementation guide
- Working with engineers unfamiliar with codebase
- Breaking down complex features
- Ensuring consistent implementation approach

## What to Include

- Exact file paths (no vague locations)
- Complete code snippets (not pseudocode)
- Verification commands
- Expected outputs
- Commit messages for each step
- Dependencies between tasks
- Edge cases to handle

## Output Location

Save to: `docs/plans/YYYY-MM-DD-<feature-name>.md`

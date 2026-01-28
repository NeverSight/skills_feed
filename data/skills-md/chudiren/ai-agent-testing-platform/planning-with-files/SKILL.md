---
name: planning-with-files
description: "Implements the Manus-style persistent markdown planning workflow. Use this for complex tasks to track progress, store findings, and maintain context across sessions."
version: 1.0.0
---

# Planning with Files

This skill implements a persistent memory workflow using three markdown files. This allows you to handle complex, multi-step tasks without losing context or forgetting goals.

## The 3-File Pattern

For any complex task, you must maintain these three files in the root of the project (or a specific `plans/` directory if preferred by the user):

1.  **`task_plan.md`**: The master plan. Tracks phases, specific tasks, and their completion status.
2.  **`findings.md`**: The knowledge base. Stores lessons learned, decisions made, and technical details discovered.
3.  **`progress.md`**: The session log. A chronological record of actions taken, results observed, and thoughts.

## When to Use

-   When the user asks for "planning with files".
-   When starting a complex feature or refactoring.
-   When the task requires multiple tool calls and steps.
-   When you need to "remember" things for future sessions.

## Instructions

### 1. Initialization
At the start of a task, check if these files exist. If not, create them by copying from the templates in `.claude/templates/` or using the content below.

-   **task_plan.md**: Break down the user's request into high-level phases and granular tasks. Mark them as `[ ]` (pending).
-   **findings.md**: Initialize with an empty structure for "Key Decisions" and "Technical Learnings".
-   **progress.md**: Add a header for the current session (Date/Time).

### 2. Execution Loop
Before and after running tools, update the files:

-   **Update `progress.md`**: specific actions you are about to take or have just taken. Record command outputs or test results briefly.
-   **Update `findings.md`**: If you discover how a system works, a hidden bug, or make an architectural decision, record it here immediately.
-   **Update `task_plan.md`**: When a sub-task is done, mark it `[x]`. If new tasks are discovered, add them.

### 3. Context Management
-   Do **not** rely on your context window for long-term memory.
-   Read `task_plan.md` to know "what's next".
-   Read `findings.md` to know "how things work" or "what we decided".
-   Read `progress.md` to know "what did I just do".

## Templates

### task_plan.md Template
```markdown
# Task Plan: [Task Name]

## Status
- [ ] Phase 1: [Name]
    - [ ] Task 1.1
    - [ ] Task 1.2
- [ ] Phase 2: [Name]

## Current Context
- Focus: [Current Focus]
- Blockers: [Any Blockers]
```

### findings.md Template
```markdown
# Findings & Knowledge

## Key Decisions
- [Date] [Decision]: [Rationale]

## Technical Learnings
- [Tool/Library]: [How to use it / Gotchas]
- [Architecture]: [Description]

## Unresolved Questions
- [ ] [Question]?
```

### progress.md Template
```markdown
# Progress Log

## [YYYY-MM-DD HH:MM] Session Start
- Goal: [Goal for this session]

### [HH:MM] Action
- executed: `command`
- result: success/fail
- thoughts: ...
```

---
name: agent-memory
author: jmaxdev
description: >
  Manages session memory persistence, detailed logs, and task planning.
  Uses MEMORY.md, SESSION.md, and PLANNING.md files to maintain a chronological history
  of achievements and project status. Emphasizes the use of all available skills.
---

This skill instructs the model to maintain a structured and persistent memory of the work performed through Markdown files.

## Memory Files

Files are stored in `.agents/memory/`:

1.  **MEMORY.md**: Long-term memory.
    - Contains important milestones, architecture decisions, and significant changes.
    - Helps the model "remember" the global state of the project in future sessions.
2.  **SESSION.md**: Current session log.
    - Contains discussed topics, current conversation context, and on-the-fly decisions.
    - Must be updated at the end of each session or milestone.
3.  **PLANNING.md**: Task planning and tracking.
    - Task list with statuses: `[ ]` (pending), `[/]` (in progress), `[x]` (completed).
    - **IMPORTANT**: Every entry MUST have a timestamp of when it was made or completed.
    - **IMPORTANT**: Update this file immediately after finishing ANY task, regardless of its complexity.

## Usage Instructions

1.  **Task Start**: Always check if files exist in `.agents/memory/` to synchronize context.
2.  **Skill Usage**: Before performing any action, review all available skills in `.agents/skills/`. Use the most appropriate skill for the task (e.g., `caveman-commit` for commits, `web-design-guidelines` for UI, etc.). Do not ignore the potential of installed skills.
3.  **Continuous Update**:
    - When starting a plan, write tasks in `PLANNING.md`.
    - When completing a task, mark progress with a timestamp: `[x] Task finished - 2026-04-21 14:00`.
4.  **Session Close**: Summarize what was learned and done in `SESSION.md` and, if relevant for the future, in `MEMORY.md`.

## PLANNING.md Example

```markdown
# Session Planning - 2026-04-21

- [x] Initial requirements analysis - 13:45
- [/] Memory skill implementation - 13:58
- [ ] Final verification
```

## MEMORY.md Example

```markdown
# Project Historical Memory

## 2026-04-21
- Implemented a memory persistence system for the AI agent using Markdown.
- Defined the workflow in `.agents/memory/`.
```
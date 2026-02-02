---
name: plan-revision
description: Guided plan revision with impact analysis. Supports explore mode (discover what to change) and direct mode (apply known changes). Always shows impact before execution.
---

# Plan Revision

Revise existing plans with full impact visibility.

**Integrates with:**
- `ohno` — Task CRUD, dependencies, activity logging
- `project-harness` — Works within session workflow

## Quick Reference

### Explore Mode
1. Load context from ohno
2. Ask discovery questions (one at a time)
3. Surface connections and dependencies
4. Propose 2-3 approaches with trade-offs
5. Converge to concrete changes
6. Show impact analysis
7. Execute with approval

### Direct Mode
1. Load context from ohno
2. Parse user's stated changes
3. Clarify only if ambiguous
4. Show impact analysis
5. Execute with approval

## Impact Analysis Components

| Component | Priority | When Shown |
|-----------|----------|------------|
| Ticket changes (diff table) | Primary | Always |
| Risk assessment | Primary | Always |
| Dependency graph | Secondary | Complex deps |
| Effort delta | Secondary | Significant changes |

## Risk Flags

:warning: **High Risk:**
- Task in progress or review
- Task has logged activity
- Task has 3+ dependents
- Task on critical path

:information_source: **Medium Risk:**
- Dependencies need updating
- Part of partially complete epic

## ohno MCP Tools Used

- `get_tasks()` - Load plan
- `get_project_status()` - Summary
- `get_task_dependencies()` - Dependency map
- `update_task()` - Modify tasks
- `archive_task()` - Remove tasks
- `create_task()` - Add tasks
- `add_dependency()` / `remove_dependency()` - Update deps
- `add_task_activity()` - Log revision
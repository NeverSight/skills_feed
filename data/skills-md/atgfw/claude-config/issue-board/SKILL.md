---
name: issue-board
description: Display GitHub issues as a kanban board grouped by lifecycle stage and sorted by priority. Use when the user asks to see the issue board, backlog, or kanban view.
user_invocable: true
---

# Issue Board

Fetch and display all GitHub issues as a structured kanban board.

## Instructions

1. Run `gh issue list --state all --json number,title,state,labels --limit 100` via Bash
2. Parse the JSON output
3. Group issues by lifecycle label into columns:
   - **Triage**: `lifecycle/triage` or open with no lifecycle label
   - **Specced**: `lifecycle/specced`
   - **In Progress**: `lifecycle/in-progress`
   - **Blocked**: `lifecycle/blocked`
   - **Needs Review**: `lifecycle/needs-review`
   - **Done**: closed issues
4. Within each column, sort by priority:
   - `priority/p0-critical` first
   - `priority/p1-high`
   - `priority/p2-medium`
   - `priority/p3-low`
   - Unlabeled last
5. Display as grouped markdown tables (one per active column):

```
## Issue Board
### Triage (N)
| # | Title | Pri |
|---|-------|-----|
| 26 | [hooks] feat: add kanban | p1-high |

### In Progress (N)
| # | Title | Pri |
|---|-------|-----|
| 14 | [n8n] fix: webhook auth | p0-critical |
```

6. After displaying, sync the registry by noting any status changes observed
7. If the user asks to update priority, lifecycle, or close issues, use `gh issue edit` or `gh issue close` accordingly

---
name: dot-tasks
description: Reference skill for users integrating dot-tasks into AI coding agents. Use dot-tasks to track tasks in `.tasks/` with clear, auditable state for humans and agents.
---

# dot-tasks Skill

`dot-tasks` is a Python CLI (assumed installed) that tracks human/agent work in a repo-local `.tasks/` directory.

Use this skill whenever a repository uses `dot-tasks` for task lifecycle tracking.

## When To Use

- For substantial or multi-file work, use `dot-tasks` as the tracking source of truth.
- If the user asks what to work on next, use `dot-tasks` task state as the source of truth.

## Default Agent Loop

1. Ensure `.tasks/` exists; if missing, run `dot-tasks init` (or ask permission before initializing).
2. Detect existing tasks first:
   - Fast path: if user gives a known `task_name`/`task_id`, run `dot-tasks view <task_name_or_id> --json`.
   - Otherwise run `dot-tasks list --json`, shortlist likely matches, and inspect candidates with `dot-tasks view <task_name_or_id> --json`.
3. Confirm with the user whether a candidate task matches and whether tracking should bind to it.
4. If no task matches and work is substantial (plan mode, likely multi-file, or >=30 minutes), ask whether to create a new task.
5. If work is quick/simple, do not force task creation unless the user asks.
6. Once tracking is bound, run: `start` -> write implementation plan to `plan.md` -> `log-activity --note` during progress -> `complete` only when acceptance criteria are met.

## Commands

```bash
# setup
dot-tasks init                                              # initialize .tasks/

# discover
dot-tasks list --json                                       # list tasks for matching
dot-tasks list [todo|doing|done] --json                    # narrow by status
dot-tasks view <task_name_or_id> --json                    # inspect one task
dot-tasks tags [todo|doing|done] --json                    # tag counts/triage

# lifecycle
dot-tasks create <task_name> --summary "..." --priority [p1|p2|p3|p4] --effort [s|m|l|xl] --tag <tag>
dot-tasks start <task_name_or_id>                          # move to doing + create plan.md
dot-tasks update <task_name_or_id> --priority p1 --effort m --tag backend
dot-tasks log-activity <task_name_or_id> --note "Progress note" [--actor agent]
dot-tasks complete <task_name_or_id>                       # move to done

# maintenance
dot-tasks rename <task_name_or_id> <new_task_name>         # rename task
dot-tasks delete <task_name_or_id>                         # soft-delete to trash
```

## Working Rules

- Prefer `dot-tasks` commands over direct edits to task state files.
- Avoid silent auto-binding on fuzzy matches; confirm task binding with the user.
- Direct file edits are allowed for:
  1. `task.md` for writing task summary/specs after `dot-tasks create`.
  2. `plan.md` to keep implementation steps current after `dot-tasks start`.
- In plan mode, after the plan is finalized and approved by the user, write the full plan you create to the bound task's `plan.md` (do not only write a summary or partial plan).
- Do not rewrite `activity.md` history; append only.
- Respect dependency checks.
- Use `dot-tasks rename` for renames (never manual folder edits).
- Use `dot-tasks delete` for deletion (soft-delete moves to trash/ by default).


## Data Contract

- Canonical metadata is in `task.md` frontmatter.
- Dependency references use `task_id` in metadata.
- Dependencies are displayed to humans as `task_name (task_id)`.
- `activity.md` line format is `YYYY-MM-DD HH:MM | actor | type | note`.

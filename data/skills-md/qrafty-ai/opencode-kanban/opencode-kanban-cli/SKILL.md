---
name: opencode-kanban-cli
description: Documents the opencode-kanban CLI contract and provides correct command patterns for task/category operations.
---

# opencode-kanban-cli

Use this skill to run `opencode-kanban` commands correctly and avoid common argument mistakes.

## When to use

- The user asks how to use `opencode-kanban` from terminal scripts.
- The user hits CLI parsing errors (`--project`, `--id`, selector conflicts).
- The user needs ready-to-copy command examples for task/category workflows.

## Instructions

1. Start by applying these global CLI rules:
   - For all non-TUI commands, `--project <PROJECT>` is required.
   - `--project` and `--json` are global and can appear before or after subcommands.
   - The project must already exist, otherwise the CLI returns `PROJECT_NOT_FOUND`.

2. Use command groups exactly as follows:
   - `task list [--repo <REPO>] [--category-id <UUID> | --category-slug <SLUG>] [--archived]`
   - `task create --title <TEXT> --branch <BRANCH> --repo <REPO> [--category-id <UUID> | --category-slug <SLUG>]`
   - `task move --id <TASK_ID_OR_PREFIX> (--category-id <UUID> | --category-slug <SLUG>)`
   - `task show --id <TASK_ID_OR_PREFIX>`
   - `task archive --id <TASK_ID_OR_PREFIX>`
   - `category list`
   - `category create --name <TEXT> [--slug <SLUG>]`
   - `category update --id <CATEGORY_ID> [--name <TEXT>] [--slug <SLUG>] [--position <N>]`
   - `category delete --id <CATEGORY_ID>`

3. Follow selector semantics precisely:
   - Category destination selectors are mutually exclusive: use exactly one of `--category-id` or `--category-slug` when required.
   - `task move` requires one category selector.
   - `task show`, `task move`, and `task archive` accept full UUID or unique short ID prefix from table output (for example `e11ad40a`).
   - `--repo` accepts either a repo name or the repo path (matching registered repos).

4. Be explicit about `task create` behavior:
   - It performs the same creation workflow as TUI: validates branch, resolves base branch, fetches/checks base, creates git worktree, creates tmux session, then persists task runtime metadata.
   - If any step fails, it rolls back created artifacts (task row, tmux session, worktree) when possible.

5. Prefer these validated examples:

```bash
# Global flags can be placed after subcommands
opencode-kanban task list --project test --json

# Create task with full workflow (worktree + tmux session + metadata)
opencode-kanban task create --project test --title "Refactor parser" --branch feature/refactor-parser --repo /path/to/repo --category-slug todo

# Move using short task id prefix from table output
opencode-kanban task move --project test --id e11ad40a --category-slug in-progress

# Show categories as pretty table
opencode-kanban category list --project test
```

6. If user reports an error, map it quickly:
   - `PROJECT_REQUIRED` -> missing `--project`
   - `PROJECT_NOT_FOUND` -> project DB does not exist yet
   - `UNIQUE_CONSTRAINT` on create -> duplicate `(repo, branch)`
   - `TASK_ID_AMBIGUOUS` -> provide longer task id prefix
   - `CATEGORY_SELECTOR_CONFLICT` -> both category selectors were provided

---
name: parallel-claudes
description: >
  Guide for running multiple parallel Claude Code sessions using cw (Claude Worktree Manager).
  Use when the user wants to parallelize work across multiple Claude instances, manage git worktrees
  for concurrent AI coding tasks, or merge results back together. Triggers on tasks involving
  parallel Claude sessions, worktree management, or splitting work across multiple agents.
license: MIT
metadata:
  author: joyco-studio
  version: "0.0.2"
---

# Parallel Claudes Orchestrator

You are the **root orchestrator**. When the user asks you to parallelize work, you manage the entire lifecycle: analyze the task, split it into subtasks, create isolated worktrees, launch headless Claude subagents, monitor their progress, and merge everything back.

## Prerequisites

Before starting, verify these are available:

- **`cw`** — if missing, install with: `curl -fsSL https://raw.githubusercontent.com/joyco-studio/cw/main/install.sh | bash`
- **`claude`** CLI (Claude Code)
- **`gh`** CLI (GitHub CLI, required for PR-based merge)

## Your Orchestration Steps

### Step 1: Analyze, Split, and Choose Merge Strategy

When the user describes a task, break it into **independent subtasks** that won't create file conflicts. Each subtask becomes a worktree with its own Claude subagent.

Rules for splitting:
- Subtasks must not modify the same files
- Each subtask should be self-contained and completable in isolation
- Name worktrees descriptively (e.g., `feat-auth`, `fix-nav`, `add-tests`)

Tell the user your plan before proceeding: list the subtasks, their names, and what each subagent will do.

**Before starting any work**, you MUST ask the user which merge strategy to use:
- **Local merge** (`cw merge <name> --local`) — squash-merges directly into the current branch, no PR created.
- **Remote merge via GitHub PR** (`cw merge <name>`) — pushes the branch and opens a GitHub PR for review.

Use the `AskUserQuestion` tool to present this choice. Do NOT proceed to Step 2 until the user has answered.

### Step 2: Create Worktrees

Use the Bash tool to create all worktrees. **Always use `--no-open`** — without it, `cw new` enters an interactive prompt that will hang indefinitely.

```bash
cw new <name> --no-open
```

Run all `cw new` commands sequentially in a single Bash call:

```bash
cw new feat-auth --no-open && cw new feat-api --no-open && cw new feat-tests --no-open
```

### Step 3: Launch Subagents

Launch a headless Claude process in each worktree using the Bash tool with **`run_in_background: true`**. Each subagent runs autonomously and exits when done.

For each subtask, run a **separate** background Bash command:

```bash
cw cd <name> && claude -p "<detailed prompt>. Commit your changes when done." --output-format text --dangerously-skip-permissions
```

**Critical rules:**
- Use `-p` flag — this runs Claude in non-interactive (print) mode. It executes the prompt and exits.
- Use `--output-format text` for clean output.
- **Always use `--dangerously-skip-permissions`** — subagents run in isolated worktrees (throwaway branches), so they need full autonomy to read, write, and execute without prompting for approval. Without this flag, subagents will hang waiting for permission in their terminal windows.
- Always instruct the subagent to **commit its changes when done**. Without commits, `cw merge` has nothing to merge.
- Launch all subagents in **parallel** — each one as its own background Bash call in a single message.
- Write **detailed prompts** for each subagent. They have no context about the broader task — give them everything they need: what to build, where the relevant code is, what patterns to follow, and any constraints.

### Step 4: Monitor Progress

After launching, poll for completion:
- Use `TaskOutput` with `block: false` to check on each background task without blocking.
- Use `cw ls` to see commits-ahead count for each worktree.
- Report progress to the user as subagents complete.

### Step 5: Verify Commits

Before merging, verify that each subagent actually committed its work. Run `cw ls` and check that every worktree shows **commits ahead > 0**.

```bash
cw ls
```

If a worktree has **0 commits ahead**, the subagent failed to commit. Navigate into it and commit manually:

```bash
cw cd <name> && git add -A && git commit -m "Complete <subtask description>"
```

Do NOT proceed to merging until every worktree has at least one commit.

After verifying, provide the user with the commands to step into each worktree manually in case they want to review or continue the work themselves:

```
To step into any worktree and take over:
  cw cd <name>        # enter the worktree
  claude              # start an interactive Claude session there
```

List all worktree names so the user can copy-paste. Then ask the user if they want to proceed with merging or take over manually.

### Step 6: Merge Results

Once all worktrees have verified commits, merge each one using the strategy the user chose in Step 1:

```bash
# If user chose remote (GitHub PR)
cw merge <name>

# If user chose local (squash merge, no PR)
cw merge <name> --local
```

If there are **dependencies between subtasks** (e.g., DB migrations before API routes), merge them in the correct order.

### Step 7: Clean Up

After all merges are complete:

```bash
cw clean
```

## `cw` Commands Reference

| Command | Description |
|---|---|
| `cw new <name> --no-open` | Create a worktree without interactive prompts |
| `cw cd <name>` | Change directory into a worktree |
| `cw ls` | List all worktrees with branch and commits-ahead count |
| `cw merge <name>` | Push branch and create a GitHub PR |
| `cw merge <name> --local` | Squash-merge locally (no PR) |
| `cw rm <name>` | Remove a worktree and its branch |
| `cw clean` | Remove all worktrees |

## Example

User asks: *"Build a settings feature with UI, API, and database layers"*

**You do:**

1. Tell the user the plan: 3 parallel subtasks — `feat-ui`, `feat-api`, `feat-db`

2. Create worktrees (single Bash call):
```bash
cw new feat-ui --no-open && cw new feat-api --no-open && cw new feat-db --no-open
```

3. Launch 3 background subagents (3 parallel Bash calls, each with `run_in_background: true`):
```bash
cw cd feat-ui && claude -p "Build the settings page UI. Create components in src/components/settings/ using the existing design system in src/components/ui/. Include a form for updating user preferences with fields for: display name, email notifications toggle, and theme selector. Commit your changes when done." --output-format text --dangerously-skip-permissions
```
```bash
cw cd feat-api && claude -p "Create REST API routes for settings in src/api/settings/. Add GET /api/settings and PUT /api/settings endpoints. Use the existing auth middleware from src/middleware/auth.ts. Return and accept JSON matching the Settings type. Commit your changes when done." --output-format text --dangerously-skip-permissions
```
```bash
cw cd feat-db && claude -p "Add a settings table migration in src/db/migrations/. Columns: user_id (FK to users), display_name (text), email_notifications (boolean, default true), theme (text, default 'system'). Add the Settings model in src/db/models/. Commit your changes when done." --output-format text --dangerously-skip-permissions
```

4. Monitor with `TaskOutput` (block: false) and `cw ls`

5. Merge in dependency order:
```bash
cw merge feat-db && cw merge feat-api && cw merge feat-ui
```

6. Clean up:
```bash
cw clean
```

## Troubleshooting

- **`cw` not found**: Source it in the shell — `source ~/.local/bin/cw`
- **`cw cd` doesn't change directory**: Ensure `cw` is loaded as a shell function, not just a script
- **Merge conflicts**: Resolve manually in the worktree, commit, then retry `cw merge`
- **`cw merge` refuses**: There are uncommitted changes in the worktree — the subagent may not have committed. Navigate in with `cw cd <name>` and commit manually
- **Subagent hung/failed**: Check its output via `TaskOutput`. If stuck, stop the background task and retry with a revised prompt

## Reference

- Repository: https://github.com/joyco-studio/cw

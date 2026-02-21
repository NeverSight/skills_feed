---
name: multitask
description: |
  Execute multiple independent development tasks in parallel using subprocess isolation.
  Each task runs in a clean /tmp clone with Recipe Runner code-enforced workflow execution.
  Proven pattern: 4/5 PRs created successfully in first production use.
version: 1.0.0
auto_activates:
  - "parallel workstreams"
  - "multiple tasks in parallel"
  - "execute tasks simultaneously"
  - "parallel development work"
  - "run multiple features at once"
  - "launch parallel tasks"
---

# Multitask Skill

## Purpose

Execute multiple independent development tasks in parallel. Each workstream runs in an isolated `/tmp` clone with its own Recipe Runner process following code-enforced workflow steps.

**Key Advantage**: Uses Recipe Runner YAML recipes instead of prompt-based markdown workflows. Python controls step execution, making it impossible to skip steps.

## Quick Start

### Inline Tasks

```
/multitask
- #123 (feat/add-auth): Implement user authentication
- #124 (feat/add-logging): Add structured logging
- #125 (feat/update-api): Update API endpoints
```

### JSON Config

Create `workstreams.json`:

```json
[
  {
    "issue": 123,
    "branch": "feat/add-auth",
    "description": "User authentication",
    "task": "Implement JWT-based authentication with login/logout endpoints",
    "recipe": "default-workflow"
  },
  {
    "issue": 124,
    "branch": "feat/add-logging",
    "description": "Structured logging",
    "task": "Add structured JSON logging across all API endpoints"
  }
]
```

Then: `/multitask workstreams.json`

## How It Works

```
User provides task list
        |
        v
For each task:
  1. Clone branch to /tmp/amplihack-workstreams/ws-{issue}/
  2. Write launcher.py (Recipe Runner with CLISubprocessAdapter)
  3. Write run.sh (unsets CLAUDECODE, runs launcher.py)
  4. Launch subprocess via Popen
        |
        v
Monitor all workstreams (60s intervals)
        |
        v
Report: PR numbers, success/failure, runtime
```

### Why Recipe Runner?

| Aspect             | Classic (markdown)       | Recipe Runner (YAML)                    |
| ------------------ | ------------------------ | --------------------------------------- |
| Step ordering      | Prompt-based (skippable) | Code-enforced (Python loop)             |
| Template variables | None                     | `{{task_description}}`, `{{repo_path}}` |
| Error handling     | Implicit                 | Fail-fast per step                      |
| Progress tracking  | Opaque                   | Step-by-step status                     |

### Critical Implementation Details

1. **`/tmp` clones** (not worktrees): Worktree symlinks confuse nested Claude sessions. Clean clones avoid this.
2. **`unset CLAUDECODE`**: Claude Code blocks nested sessions via this env var. Unsetting allows controlled parallel execution.
3. **Recipe Runner adapter**: `CLISubprocessAdapter` shells out to `claude -p` for each agent step within the recipe.

## Execution Modes

### Recipe Mode (Default)

Each workstream runs `run_recipe_by_name()` through a Python launcher:

```python
from amplihack.recipes import run_recipe_by_name
from amplihack.recipes.adapters.cli_subprocess import CLISubprocessAdapter

adapter = CLISubprocessAdapter(cli="claude", working_dir=".")
result = run_recipe_by_name("default-workflow", adapter=adapter,
    user_context={"task_description": task, "repo_path": "."})
```

### Classic Mode

Falls back to single-session prompt-based execution:

```bash
amplihack claude -- -p "@TASK.md Execute autonomously following DEFAULT_WORKFLOW.md."
```

Use `--mode classic` when Recipe Runner is unavailable or for tasks that benefit from full session context.

## Available Recipes

Any recipe in `amplifier-bundle/recipes/` can be used per-workstream:

| Recipe                   | Steps | Best For                              |
| ------------------------ | ----- | ------------------------------------- |
| `default-workflow`       | 52    | Features, bugs, refactoring (default) |
| `investigation-workflow` | 23    | Research, codebase analysis           |
| `verification-workflow`  | 5     | Trivial changes, config updates       |
| `auto-workflow`          | 9     | Autonomous iteration until complete   |

Specify per-task: `"recipe": "investigation-workflow"` in JSON config.

## Monitoring

```bash
# Watch all logs
tail -f /tmp/amplihack-workstreams/log-*.txt

# Check specific workstream
tail -f /tmp/amplihack-workstreams/log-123.txt

# Check running processes
ps aux | grep launcher.py

# Final report
cat /tmp/amplihack-workstreams/REPORT.md
```

## When to Read Supporting Files

| Need                                   | File              |
| -------------------------------------- | ----------------- |
| Full API, config options, architecture | `reference.md`    |
| Real-world usage examples              | `examples.md`     |
| Python orchestrator source             | `orchestrator.py` |

## Troubleshooting

**Empty log files**: Process started but exited immediately. Check if `amplihack` package is importable in the clone's environment.

**"CLAUDECODE env var detected"**: The `run.sh` wrapper must unset `CLAUDECODE` before running the launcher.

**Recipe not found**: Ensure `amplifier-bundle/recipes/` exists in the cloned branch. The recipe discovery checks this directory first.

**Fallback**: If recipe mode fails, retry with `--mode classic` to use the prompt-based approach.

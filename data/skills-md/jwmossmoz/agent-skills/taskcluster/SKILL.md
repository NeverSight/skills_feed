---
name: taskcluster
description: >
  Interact with Mozilla Taskcluster CI using the taskcluster CLI.
  Query task status, view logs, download artifacts, retrigger tasks, and manage task groups.
  Use when working with CI tasks from firefox-ci-tc.services.mozilla.com or debugging worker pool issues.
  For worker pool operations (list workers, terminate workers, bulk task cancellation), use native taskcluster api commands (see references/worker-pools.md).
  Triggers on "taskcluster", "task status", "task log", "artifacts", "retrigger", "task group", "worker pool".
---

# Taskcluster

Interact with Mozilla Taskcluster CI. Use the native `taskcluster` CLI for most operations.
The Python helper script (`tc.py`) handles only what the native CLI cannot.

## Prerequisites

### Taskcluster CLI

```bash
brew install taskcluster
taskcluster version
```

### Authentication

Read-only operations (status, logs, artifacts) work without auth. Write operations require credentials.

```bash
# Sign in interactively (recommended for local use)
export TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com
taskcluster signin

# Or set credentials directly
export TASKCLUSTER_CLIENT_ID=your-client-id
export TASKCLUSTER_ACCESS_TOKEN=your-access-token
```

## Native CLI — Use for Most Operations

Always set the root URL when targeting Firefox CI:

```bash
export TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com
```

### Task Operations

```bash
# Task status
taskcluster task status <TASK_ID>

# Stream task log
taskcluster task log <TASK_ID>

# Full task definition (JSON)
taskcluster task def <TASK_ID>

# Rerun a task (same task ID)
taskcluster task rerun <TASK_ID>

# Cancel a task
taskcluster task cancel <TASK_ID>
```

### Task Group Operations

```bash
# List all tasks in a group (with state filter options)
taskcluster group list --all <TASK_GROUP_ID>
taskcluster group list --failed <TASK_GROUP_ID>
taskcluster group list --running <TASK_GROUP_ID>

# Group status summary
taskcluster group status <TASK_GROUP_ID>

# Cancel all tasks in a group
taskcluster group cancel --force <TASK_GROUP_ID>
```

### Worker Pool Operations

For worker pool management (list workers, terminate, bulk cancel), see `references/worker-pools.md`.
These use `taskcluster api workerManager` and `taskcluster api queue` directly.

## Python Helper — tc.py

Use this local skills checkout path:

```bash
SKILLS_ROOT=/Users/jwmoss/github_moz/agent-skills/skills
TC="$SKILLS_ROOT/taskcluster/scripts/tc.py"
```

The helper handles two categories the native CLI doesn't cover well:

### Artifact Listing (Full JSON with URLs)

The native `taskcluster task artifacts` only lists names. Use `tc.py` when you need URLs,
content types, or expiry dates to locate and download specific artifacts.

```bash
# Full artifact listing as JSON (URLs, content types, expiry)
uv run "$TC" artifacts <TASK_ID>

# For a specific run
uv run "$TC" artifacts <TASK_ID> --run 0

# Pipe to jq to find specific artifacts
uv run "$TC" artifacts <TASK_ID> | jq '.artifacts[] | select(.name | contains("log")) | .url'
```

### Group Status with State Counts (JSON)

The native `taskcluster group status` output is not structured JSON. Use `tc.py` when you need
machine-readable state counts for scripting or analysis.

```bash
# Structured JSON with totalTasks and stateCounts breakdown
uv run "$TC" group-status <TASK_GROUP_ID>
```

### In-Tree Actions (require authentication)

In-tree actions are defined in the Firefox taskgraph and triggered via Taskcluster hooks.
These are the API equivalent of actions in Treeherder's "Custom Action" menu.

**Required scopes**: `hooks:trigger-hook:project-gecko/in-tree-action-*`

```bash
# List available actions for a task
uv run "$TC" action-list <TASK_ID>

# Retrigger via in-tree action (preserves task graph dependencies)
# Use this instead of `taskcluster task retrigger`, which clears dependencies
uv run "$TC" retrigger <TASK_ID>

# Retrigger multiple times (default: 5)
uv run "$TC" retrigger-multiple <TASK_ID> --times 10

# Confirm failures — re-runs failing tests to determine intermittent vs regression
uv run "$TC" confirm-failures <TASK_ID>

# Backfill — runs test on previous pushes to find regression range
uv run "$TC" backfill <TASK_ID>

# Trigger any action by name with optional JSON input
uv run "$TC" action <TASK_ID> <ACTION_NAME> --input '{"key": "value"}'
```

The `tc.py` action commands accept both task IDs and full Taskcluster URLs:

```bash
uv run "$TC" retrigger https://firefox-ci-tc.services.mozilla.com/tasks/fuCPrKG2T62-4YH1tWYa7Q
```

## Common Workflows

### Debugging Task Failures

```bash
export TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com

# 1. Check task status
taskcluster task status <TASK_ID>

# 2. View logs
taskcluster task log <TASK_ID>

# 3. Inspect full definition
taskcluster task def <TASK_ID>

# 4. Check all tasks in group
taskcluster group list --all <GROUP_ID>
```

### Retriggering Failed Tasks

```bash
# Retrigger via in-tree action (correct for Firefox CI — preserves dependencies)
uv run "$TC" retrigger <TASK_ID>

# Rerun the same task (same task ID, no new task created)
taskcluster task rerun <TASK_ID>
```

Note: `taskcluster task retrigger` clears dependencies and breaks Firefox CI tasks that depend
on upstream artifacts (e.g., signing tasks needing build outputs). Always use `uv run "$TC" retrigger`
for Firefox CI tasks.

### Investigating Intermittent Failures

```bash
# 1. Check historical pass/fail rate for the test
treeherder-cli --history "test_name" --history-count 20 --repo autoland --json

# 2. Compare the failed job against similar past jobs
treeherder-cli --similar-history <JOB_ID> --similar-count 50 --repo autoland --json

# 3. Check error lines for known bug suggestions
uvx --from lumberjackth lj errors autoland <JOB_ID>

# 4. If triage suggests intermittent, confirm in CI
uv run "$TC" confirm-failures <TASK_ID>

# 5. If triage suggests regression, backfill to find the culprit push
uv run "$TC" backfill <TASK_ID>
```

## Related Skills

- **treeherder**: Query CI job results by revision to get task IDs
- **lando**: Check landing job status
- **os-integrations**: Run Firefox mach try commands

## References

- `references/actions.md` - Detailed guide to in-tree actions (confirm-failures, backfill, etc.)
- `references/examples.md` - Common usage patterns and workflows
- `references/integration.md` - Integration with other Mozilla tools
- `references/worker-pools.md` - Worker pool management, bulk operations, and emergency shutdown

## Documentation

- **Taskcluster Docs**: https://docs.taskcluster.net/
- **Taskcluster CLI**: https://github.com/taskcluster/taskcluster/tree/main/clients/client-shell
- **Firefox CI**: https://firefox-ci-tc.services.mozilla.com/
- **Actions Spec**: https://docs.taskcluster.net/docs/manual/using/actions/spec

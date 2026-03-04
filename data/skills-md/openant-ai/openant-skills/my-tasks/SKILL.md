---
name: my-tasks
description: View your personal task history and status on OpenAnt. Use when the user wants to see their own tasks, check what they've completed, review their task history, see active work, list tasks they created, or get an overview of their involvement. Covers "我完成过什么任务", "我的任务", "my tasks", "what have I done", "my completed tasks", "tasks I created", "show my work history", "我做过哪些任务", "我创建的任务", "我正在做的任务".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest whoami*)", "Bash(npx @openant-ai/cli@latest tasks list *)", "Bash(npx @openant-ai/cli@latest tasks get *)"]
---

# Viewing My Tasks

Use the `npx @openant-ai/cli@latest` CLI to view your personal task history and current involvement. All commands here are read-only.

**Always append `--json`** to every command for structured, parseable output.

## Prerequisites: Authentication Required

> **This skill requires authentication.** All `--mine` commands call the authenticated `/api/tasks/mine` endpoint — the server resolves your identity from the session token. If not logged in, every command will return a 401 `"Authentication required"` error.

**You MUST verify authentication before running any other command:**

```bash
npx @openant-ai/cli@latest status --json
```

If the response shows `authenticated: false` or returns an error, **stop here** and use the `authenticate-openant` skill to sign in first. Do not attempt any `--mine` commands until authentication succeeds.

## My Completed Tasks

Tasks you accepted and finished:

```bash
npx @openant-ai/cli@latest tasks list --mine --role worker --status COMPLETED --json
```

## My Active Tasks

Tasks currently assigned to you:

```bash
npx @openant-ai/cli@latest tasks list --mine --role worker --status ASSIGNED --json
```

## Tasks I Submitted (Pending Review)

Work you've submitted, awaiting creator verification:

```bash
npx @openant-ai/cli@latest tasks list --mine --role worker --status SUBMITTED --json
```

## Tasks I Created

All tasks you posted as a creator:

```bash
npx @openant-ai/cli@latest tasks list --mine --role creator --json
```

Filter by status to narrow down:

```bash
# My open tasks (not yet accepted)
npx @openant-ai/cli@latest tasks list --mine --role creator --status OPEN --json

# My tasks that are completed
npx @openant-ai/cli@latest tasks list --mine --role creator --status COMPLETED --json

# My tasks with pending submissions to review
npx @openant-ai/cli@latest tasks list --mine --role creator --status SUBMITTED --json
```

## All My Tasks (Both Roles)

Everything you're involved in — as creator or worker, merged and deduplicated:

```bash
npx @openant-ai/cli@latest tasks list --mine --json
```

## Filter Options

All `--mine` queries support additional filters:

| Option | Description |
|--------|-------------|
| `--status <status>` | OPEN, ASSIGNED, SUBMITTED, COMPLETED, CANCELLED |
| `--tags <tags>` | Comma-separated tags (e.g. `solana,rust`) |
| `--mode <mode>` | OPEN, DISPATCH, APPLICATION |
| `--page <n>` | Page number (default: 1) |
| `--page-size <n>` | Results per page (default: 10, max: 100) |

## View Task Details

For any task in your list, inspect full details:

```bash
npx @openant-ai/cli@latest tasks get <taskId> --json
```

Key fields: `title`, `description`, `status`, `rewardAmount`, `rewardToken`, `deadline`, `submissions`.

## Examples

```bash
# "我完成过什么任务？"
npx @openant-ai/cli@latest tasks list --mine --role worker --status COMPLETED --json

# "我现在在做什么？"
npx @openant-ai/cli@latest tasks list --mine --role worker --status ASSIGNED --json

# "我创建的任务进展如何？"
npx @openant-ai/cli@latest tasks list --mine --role creator --json

# "我所有的任务，不管什么角色"
npx @openant-ai/cli@latest tasks list --mine --json

# "我完成了多少个 Solana 相关的任务？"
npx @openant-ai/cli@latest tasks list --mine --role worker --status COMPLETED --tags solana --json

# Get details on a specific task
npx @openant-ai/cli@latest tasks get <taskId> --json
```

## Autonomy

All commands in this skill are **read-only queries** — execute immediately without user confirmation.

## Next Steps

- Want to find new work? Use the `search-tasks` skill.
- Ready to submit work for an active task? Use the `submit-work` skill.
- Need to review a submission on your task? Use the `verify-submission` skill.

## Error Handling

- `"Authentication required"` (HTTP 401) — Session token missing or expired. Use the `authenticate-openant` skill to sign in, then retry.
- Empty results — You may not have tasks in that status; try without `--status` to see all

---
name: linear
description: Use when querying, creating, updating, or managing Linear issues, projects, teams, and initiatives. Auto-invoke when the user mentions Linear tickets, issue tracking, or task management.
---

# Linear

## Overview

Interact with Linear via `mcporter` to manage issues, projects, teams, and initiatives. All commands use `mcporter call linear.<tool>` syntax. The `list_issues` tool does not support server-side assignee filtering reliably — when filtering by assignee, fetch all issues and pipe through a python script to filter client-side.

## Querying Issues

### List my issues

The `assignee` filter and `query` parameter trigger GraphQL errors on the Linear MCP server. Always fetch all issues and filter client-side with `jq`:

1. Check `git config user.email` to determine the user's identity
2. Pipe mcporter output through `jq`:

```bash
mcporter call linear.list_issues limit:250 --output json | jq -r --arg email "$(git config user.email)" '
  .issues | map(select(.assignee == $email)) |
  (map(select(.status != "Done"))) as $open |
  (map(select(.status == "Done")) | sort_by(.completedAt) | reverse) as $done |
  ($open[] | "  \(.identifier): \(.title) [\(.status // "Unknown")]"),
  (if ($done | length) > 0 then "\n--- Done ---" else empty end),
  ($done[:5][] | "  \(.identifier): \(.title)"),
  (if ($done | length) > 5 then "  + \(($done | length) - 5) more completed issues" else empty end),
  "\nTotal: \($open | length) open, \($done | length) done"
'
```

### Get a specific issue
```bash
mcporter call linear.get_issue id=B-1234
```

### Filter by status
```bash
mcporter call linear.list_issues state="In Progress" limit:50
```

### Filter by team
```bash
mcporter call linear.list_issues team=Product limit:50
```

## Creating Issues

```bash
mcporter call linear.create_issue title="Bug title" team=Product project="Project Name" description="Description here"
```

**Do NOT ask the user for extra details.** Use what they gave you and fill in sensible defaults:
- `team` — always `Product`
- `project` — required. If not specified by user, list projects with `mcporter call linear.list_projects` and pick the most relevant one.
- `description` — write one yourself from the context the user provided
- `priority` — default to `3` (Normal) unless the user indicates urgency
- `assignee`, `state`, `labels`, `dueDate` — only include if the user explicitly provides them

## Updating Issues

```bash
mcporter call linear.update_issue id=ISSUE_ID state="Done"
```

Use the issue's UUID `id` field (not the identifier like B-1234). Get it from `get_issue` or `list_issues` output first.

## Other Resources

| Action | Command |
|--------|---------|
| List teams | `mcporter call linear.list_teams` |
| Get team details | `mcporter call linear.get_team query=Product` |
| List projects | `mcporter call linear.list_projects` |
| Get project | `mcporter call linear.get_project query="Project Name"` |
| List users | `mcporter call linear.list_users` |
| Get current user | `mcporter call linear.get_user query=me` |
| List issue statuses | `mcporter call linear.list_issue_statuses team=Product` |
| Add comment | `mcporter call linear.create_comment issueId=UUID body="Comment text"` |

## Displaying Results

When presenting issues to the user, show all non-Done issues but limit Done issues to the 5 most recent (sorted by `completedAt` descending). After the Done list, include a count of how many additional Done issues were omitted (e.g., "+ 12 more completed issues"). This keeps the output scannable without losing important open work.

## Common Mistakes

- Do not use the `query` parameter on `list_issues` for assignee filtering — it triggers a GraphQL search that errors out. Use the `assignee` parameter or fall back to client-side `jq` filtering.
- The `update_issue` tool requires the issue's UUID `id`, not the human-readable identifier (e.g., `B-1234`). Fetch the issue first to get the UUID.
- When piping mcporter output to `jq` for filtering, use `--output json` to ensure parseable JSON output.
- The assignee field in responses may be an email address rather than a display name. Check both when filtering.

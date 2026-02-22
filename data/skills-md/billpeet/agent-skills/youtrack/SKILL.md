---
name: youtrack
description: Manages YouTrack issues, projects, and users via the yt CLI. Use when searching, creating, updating, or commenting on YouTrack issues, listing projects, or checking authenticated user info. Triggers on phrases like "YouTrack issue", "create a ticket", "search issues", "update issue", "add comment to", "list projects".
compatibility: Requires yt CLI installed (npm install -g @billpeet/yt-cli) and configured (yt setup --url <url> --token <token>), or YOUTRACK_BASE_URL and YOUTRACK_TOKEN environment variables set.
---

# YouTrack

Interact with a YouTrack instance using the `yt` CLI. All commands output JSON by default for reliable parsing.

## Setup

Configure once (credentials saved to `~/.config/yt-cli/config.json`):

```bash
yt setup --url https://your-instance.youtrack.cloud --token <permanent-api-token>
```

Or use environment variables (these take priority over the config file):

```bash
export YOUTRACK_BASE_URL=https://your-instance.youtrack.cloud
export YOUTRACK_TOKEN=<permanent-api-token>
```

## Issues

### Search

```bash
yt issue search "<query>" --format json --pretty
yt issue search "project: MyProject #Unresolved assignee: me" --top 20 --format json
yt issue search "tag: bug" --top 10 --skip 0 --format json
```

YouTrack query syntax: `project: PROJ`, `#Unresolved`, `assignee: me`, `priority: Critical`, `tag: bug`, free text, etc.

### Get a single issue

```bash
yt issue get PROJ-123 --format json --pretty
```

### Create an issue

```bash
yt issue create --project PROJ --summary "Summary here" --description "Details" --format json
```

### Update an issue

```bash
yt issue update PROJ-123 --summary "New summary" --format json
yt issue update PROJ-123 --description "Updated description" --format json
yt issue update PROJ-123 --field "Priority=Critical" --field "State=In Progress" --format json
```

Custom fields use `--field "Name=Value"` and can be repeated for multiple fields.

### Comments

List comments:
```bash
yt issue comments PROJ-123 --format json --pretty
```

Add a comment:
```bash
yt issue comment PROJ-123 --text "Comment text here" --format json
```

## Projects

```bash
yt project list --format json --pretty
```

## Users

Get the authenticated user:
```bash
yt user me --format json --pretty
```

## Output format

All commands support `--format json` (compact) or `--format text` (human-readable). Add `--pretty` for indented JSON.

Exit codes: `0` = success, `1` = error. Errors are written to stderr as JSON.

## Pagination

Use `--top <n>` (default 50) and `--skip <n>` (default 0) on `issue search` for pagination.

## Common workflows

**Find and update an issue:**
```bash
yt issue search "summary: login bug #Unresolved" --format json --top 5
yt issue update PROJ-42 --field "State=In Progress"
yt issue comment PROJ-42 --text "Started investigating — reproducible in staging."
```

**Create and confirm:**
```bash
yt issue create --project PROJ --summary "Fix null pointer in auth flow" --description "Stack trace: ..." --format json --pretty
```

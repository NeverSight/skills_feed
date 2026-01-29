---
name: linear-cli
description: >
  Interact with Linear issue tracker via CLI. Create, list, update, and close
  issues; add comments; manage cycles and teams. Use when the user wants to
  work with Linear issues, check their backlog, create tickets, or automate
  Linear workflows from the terminal.
---

# Linear CLI

CLI for Linear issue tracking. Manage issues, cycles, and teams from the terminal.

## Installation

```bash
brew install duailibe/tap/linear-cli
```

Or with Go:

```bash
go install github.com/duailibe/linear-cli/cmd/linear@latest
```

## Authentication

Set API key via environment (preferred):

```bash
export LINEAR_API_KEY=lin_api_...
```

Or store locally:

```bash
linear auth login
```

Check auth status:

```bash
linear auth status
linear whoami
```

## Commands

### Issues

```bash
# List issues
linear issue list --team ENG
linear issue list --team ENG --cycle current
linear issue list --team ENG --assignee me
linear issue list --team ENG --state "In Progress"
linear issue list --team ENG --label bug
linear issue list --team ENG --priority 1

# View issue details
linear issue view ENG-123
linear issue view ENG-123 --comments

# Create issue
linear issue create --team ENG --title "Bug in auth"
linear issue create --team ENG --title "Feature" --description "Details here"
linear issue create --team ENG --title "Task" --priority 2 --assignee me
linear issue create --team ENG --title "Blocked" --blocked-by ENG-100 --blocks ENG-200

# Read description from stdin
cat spec.md | linear issue create --team ENG --title "New feature" --description -

# Update issue
linear issue update ENG-123 --state "In Progress"
linear issue update ENG-123 --assignee me
linear issue update ENG-123 --priority 1
linear issue update ENG-123 --cycle current

# Close/reopen
linear issue close ENG-123
linear issue reopen ENG-123

# Add comment
linear issue comment ENG-123 --body "Working on this"
echo "Status update" | linear issue comment ENG-123 --body -

# Download uploads
# Includes uploads from the issue description and comments (uploads.linear.app only).
linear issue uploads ENG-123 --dir ./downloads
```

### Cycles

```bash
# List cycles
linear cycle list --team ENG
linear cycle list --team ENG --current

# View cycle
linear cycle view <cycle-id>
```

### Teams

```bash
linear team list
```

## Output

Human-readable tables by default. Use `--json` for machine output:

```bash
linear issue list --team ENG --json
linear issue list --team ENG --json | jq '.nodes[].identifier'
```

## Global Flags

```
--json          Output JSON instead of tables
--quiet, -q     Suppress non-essential output
--verbose, -v   Enable verbose diagnostics
--no-color      Disable colored output
--no-input      Disable interactive prompts
--yes, -y       Auto-confirm prompts
--timeout       API request timeout (default 10s)
--api-key       API key (overrides env/stored auth)
```

## Common Patterns

### Get my issues in current sprint

```bash
linear issue list --team ENG --cycle current --assignee me
```

### Create issue from a file

```bash
cat << 'EOF' | linear issue create --team ENG --title "Implement auth" --description -
## Overview
Add OAuth2 support.

## Requirements
- Google login
- GitHub login
EOF
```

### Batch operations with jq

```bash
# Get all issue IDs in a cycle
linear issue list --team ENG --cycle current --json | jq -r '.nodes[].identifier'

# Close all issues matching a label
for id in $(linear issue list --team ENG --label done --json | jq -r '.nodes[].identifier'); do
  linear issue close "$id"
done
```

### Check issue before updating

```bash
linear issue view ENG-123 --json | jq '{state, assignee, priority}'
linear issue update ENG-123 --state "Done"
```

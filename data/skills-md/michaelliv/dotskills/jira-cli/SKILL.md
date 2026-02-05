---
name: jira-cli
description: Interact with Atlassian Jira from the command line. Create, update, and search issues, manage sprints and epics, transition statuses, and more. Use when the user wants to work with Jira tickets, check sprint progress, or automate project workflows.
metadata:
  author: michaelliv
  version: "1.0"
compatibility: Requires jira-cli (brew install ankitpokhrel/jira-cli/jira-cli), curl, jq, and psst for credential management. See references/INSTALLATION.md for setup.
---

# Jira CLI

Interact with Atlassian Jira from the command line using `jira-cli` and direct API calls.

> **Assume `jira-cli` is already installed and configured.** If the `jira` command is not found or not configured, refer to [references/INSTALLATION.md](references/INSTALLATION.md) for setup instructions.

## Important: Confirm Before Creating

**Always ask the user to confirm details before creating or updating tickets.** Do not assume:
- Ticket description or acceptance criteria
- Priority level
- Labels or components
- Issue type (Task vs Story vs Bug)

When the user requests a new ticket, confirm the summary and ask if they want to provide a description or other details before creating it.

**Always provide the ticket link after creating a ticket** (e.g., `https://<server>/browse/PROJ-1234`).

## When to Use

- User wants to create, update, or search Jira issues
- User wants to check sprint progress or manage sprints
- User wants to transition ticket statuses
- User wants to manage epics and link issues
- User wants to automate Jira workflows

## Authentication

Credentials are stored in the global psst vault with the `jira` tag:

```bash
# For jira-cli commands (injects JIRA_API_TOKEN)
psst --global JIRA_API_TOKEN -- jira <command>

# For direct API calls (inline psst get)
curl -s -u "$(psst --global get JIRA_USER):$(psst --global get JIRA_API_TOKEN)" \
  "$(psst --global get JIRA_SERVER)/rest/api/3/..."
```

## Common Operations

### List Issues

```bash
# List recent issues in a project
psst --global JIRA_API_TOKEN -- jira issue list -pPROJ --plain

# Issues assigned to current user
psst --global JIRA_API_TOKEN -- jira issue list -a$(jira me) --plain

# Filter by status
psst --global JIRA_API_TOKEN -- jira issue list -s"To Do" --plain
psst --global JIRA_API_TOKEN -- jira issue list -s"In Progress" --plain

# Filter by priority
psst --global JIRA_API_TOKEN -- jira issue list -yHigh --plain

# Filter by type
psst --global JIRA_API_TOKEN -- jira issue list -tBug --plain
psst --global JIRA_API_TOKEN -- jira issue list -tEpic --plain

# Combine filters
psst --global JIRA_API_TOKEN -- jira issue list -yHigh -s"In Progress" -a$(jira me) --plain

# Raw JQL query
psst --global JIRA_API_TOKEN -- jira issue list -q"summary ~ 'keyword'" --plain

# Output as JSON or CSV
psst --global JIRA_API_TOKEN -- jira issue list --raw
psst --global JIRA_API_TOKEN -- jira issue list --csv
```

### View Issue Details

```bash
# View issue in terminal
psst --global JIRA_API_TOKEN -- jira issue view PROJ-1234

# View with comments
psst --global JIRA_API_TOKEN -- jira issue view PROJ-1234 --comments 5

# Get raw JSON
psst --global JIRA_API_TOKEN -- jira issue view PROJ-1234 --raw
```

### Create Issues

```bash
# Interactive creation
psst --global JIRA_API_TOKEN -- jira issue create

# Non-interactive with all parameters
psst --global JIRA_API_TOKEN -- jira issue create -tTask -s"Issue summary" -b"Description" -yMedium --no-input

# Create bug
psst --global JIRA_API_TOKEN -- jira issue create -tBug -s"Bug title" -yHigh -lbug --no-input

# Create with labels and components
psst --global JIRA_API_TOKEN -- jira issue create -tStory -s"Story title" -lbackend -lagent -CBackend --no-input

# Attach to epic
psst --global JIRA_API_TOKEN -- jira issue create -tTask -s"Task title" -PPROJ-100 --no-input
```

### Update/Edit Issues

```bash
# Edit summary
psst --global JIRA_API_TOKEN -- jira issue edit PROJ-1234 -s"New summary" --no-input

# Edit priority
psst --global JIRA_API_TOKEN -- jira issue edit PROJ-1234 -yHigh --no-input

# Add/remove labels (use - prefix to remove)
psst --global JIRA_API_TOKEN -- jira issue edit PROJ-1234 -l"new-label" -l"-old-label" --no-input
```

### Transition Issues (Move Status)

```bash
# Move to In Progress
psst --global JIRA_API_TOKEN -- jira issue move PROJ-1234 "In Progress"

# Move to Done
psst --global JIRA_API_TOKEN -- jira issue move PROJ-1234 Done

# Move with comment
psst --global JIRA_API_TOKEN -- jira issue move PROJ-1234 Done --comment "Completed implementation"
```

### Assign Issues

```bash
# Assign to self
psst --global JIRA_API_TOKEN -- jira issue assign PROJ-1234 $(jira me)

# Assign to someone
psst --global JIRA_API_TOKEN -- jira issue assign PROJ-1234 "User Name"

# Unassign
psst --global JIRA_API_TOKEN -- jira issue assign PROJ-1234 x
```

### Comments

```bash
# Add comment
psst --global JIRA_API_TOKEN -- jira issue comment add PROJ-1234 "Comment text"

# Add from stdin
echo "Comment from stdin" | psst --global JIRA_API_TOKEN -- jira issue comment add PROJ-1234
```

### Epics

```bash
# List epics
psst --global JIRA_API_TOKEN -- jira epic list --plain

# List issues in an epic
psst --global JIRA_API_TOKEN -- jira epic list PROJ-100 --plain

# Create epic
psst --global JIRA_API_TOKEN -- jira epic create -n"Epic Name" -s"Epic Summary" --no-input

# Add issues to epic
psst --global JIRA_API_TOKEN -- jira epic add PROJ-100 PROJ-1234 PROJ-5678
```

### Sprints

```bash
# List sprints
psst --global JIRA_API_TOKEN -- jira sprint list --table --plain

# Current sprint issues
psst --global JIRA_API_TOKEN -- jira sprint list --current --plain

# Previous / next sprint
psst --global JIRA_API_TOKEN -- jira sprint list --prev --plain
psst --global JIRA_API_TOKEN -- jira sprint list --next --plain

# Add issues to sprint
psst --global JIRA_API_TOKEN -- jira sprint add SPRINT_ID PROJ-1234 PROJ-5678
```

### Open in Browser

```bash
# Open issue
psst --global JIRA_API_TOKEN -- jira open PROJ-1234

# Open project
psst --global JIRA_API_TOKEN -- jira open
```

## Direct API Access (Fallback)

If jira-cli has issues, use the API directly:

```bash
# List issues
curl -s -u "$(psst --global get JIRA_USER):$(psst --global get JIRA_API_TOKEN)" \
  "$(psst --global get JIRA_SERVER)/rest/api/3/search/jql?jql=project=PROJ+ORDER+BY+created+DESC&maxResults=10&fields=key,summary,status" \
  | jq -r '.issues[] | "\(.key): \(.fields.summary) [\(.fields.status.name)]"'

# Get user's issues
curl -s -u "$(psst --global get JIRA_USER):$(psst --global get JIRA_API_TOKEN)" \
  "$(psst --global get JIRA_SERVER)/rest/api/3/search/jql?jql=(assignee=currentUser()+OR+reporter=currentUser())+ORDER+BY+updated+DESC&maxResults=15&fields=key,summary,status"

# View single issue
curl -s -u "$(psst --global get JIRA_USER):$(psst --global get JIRA_API_TOKEN)" \
  "$(psst --global get JIRA_SERVER)/rest/api/3/issue/PROJ-1234" | jq .

# Get available projects
curl -s -u "$(psst --global get JIRA_USER):$(psst --global get JIRA_API_TOKEN)" \
  "$(psst --global get JIRA_SERVER)/rest/api/2/project" | jq -r '.[] | "\(.key): \(.name)"'
```

## Quick Reference

### CLI Output Flags

| Flag | Description |
|------|-------------|
| `--plain` | Plain text output (scriptable) |
| `--no-headers` | Hide table headers in plain mode |
| `--raw` | Raw JSON output |
| `--csv` | CSV format output |
| `--columns KEY,SUMMARY,STATUS` | Select specific columns |

### Issue List Filters

| Flag | Description | Example |
|------|-------------|---------|
| `-t, --type` | Issue type | `-tBug`, `-tEpic`, `-tTask` |
| `-s, --status` | Status | `-s"To Do"`, `-s"In Progress"` |
| `-y, --priority` | Priority | `-yHigh`, `-yMedium` |
| `-a, --assignee` | Assignee | `-a$(jira me)`, `-ax` (unassigned) |
| `-r, --reporter` | Reporter | `-r$(jira me)` |
| `-l, --label` | Label | `-lbackend`, `-lurgent` |
| `-P, --parent` | Parent/Epic | `-PPROJ-100` |
| `-w, --watching` | Issues you watch | `-w` |
| `--created` | Created filter | `--created week`, `--created -7d` |
| `--updated` | Updated filter | `--updated today` |
| `-q, --jql` | Raw JQL | `-q"summary ~ cli"` |

## Notes

- The tilde (~) acts as a NOT operator: `-s~Done` means "status is not Done"
- Use `-ax` to find unassigned issues
- The `--no-input` flag skips interactive prompts for scripting
- Interactive mode works best in a real terminal (not in Claude Code bash)

---
name: backlog-cli
description: |
  CLI for Backlog project management (by Nulab). Use this skill when:
  (1) Listing, creating, editing, closing, or commenting on issues
  (2) Creating, listing, merging, or commenting on pull requests
  (3) Viewing, creating, or editing Wiki pages
  (4) Querying project settings (issue types, statuses, categories, milestones, members)
  (5) Checking notifications, stars, or watches
  (6) Making raw API requests via `backlog api`
---

# backlog-cli

CLI tool for managing Backlog projects via the `backlog` command.

## Authentication

Run `backlog auth login` before use. Verify with `backlog auth status`.
Switch between spaces with `--space <hostname>` or `BACKLOG_SPACE` env var.

## Key Concepts

### Avoid Interactive Prompts

Some commands prompt interactively for missing required fields. **Always specify all required flags explicitly** to prevent hanging.

### Name Resolution

The CLI automatically resolves human-readable names to IDs:

- Status names → status ID
- Issue type names → issue type ID
- Priority names (`高`/`中`/`低`) → priority ID
- Usernames → user ID (`@me` refers to the authenticated user)

**Status and issue type names are project-specific.** Query them first if unknown:

```bash
backlog issue-type list -p PROJECT_KEY
backlog status list -p PROJECT_KEY
```

### Issue Keys

Format: `PROJECT_KEY-number` (e.g., `PROJ-123`). Since the key embeds the project, `--project` is not needed for `issue view` / `issue edit`.

### Project Key

Specify with `--project` (`-p`) flag or `BACKLOG_PROJECT` env var.

### Environment Variables

Environment variables provide defaults that can be overridden by CLI flags:

- `BACKLOG_SPACE` — Default space hostname (e.g., `example.backlog.com`)
- `BACKLOG_PROJECT` — Default project key (e.g., `MYAPP`)
- `BACKLOG_API_KEY` — API key for CI/CD environments (requires `BACKLOG_SPACE`)

**Priority order:** CLI flag > Environment variable > Config file (`~/.backlogrc`)

```bash
# Set project for session
export BACKLOG_PROJECT=MYAPP

# Now -p flag can be omitted
backlog issue list
backlog milestone list

# CLI flag overrides environment variable
backlog issue list -p OTHER_PROJECT
```

### JSON Output

Most commands support `--json` flag for machine-readable output:

- `--json` — output all fields in JSON format
- `--json field1,field2` — output only specified fields (e.g., `--json issueKey,summary,status`)
- Combine with `jq` for advanced filtering:

```bash
# Extract issue keys only
backlog issue list -p PROJ --json | jq '.[].issueKey'

# Filter by specific status
backlog issue list -p PROJ --json | jq '[.[] | select(.status.name == "処理中")]'

# Combine field filtering with jq
backlog issue list -p PROJ --json issueKey,summary | jq '.[].summary'
```

**Always use `--json` in agent workflows** to parse output reliably.

## Common Workflows

### Issues

```bash
# List my open issues
backlog issue list -p PROJ -a @me -S "未対応,処理中"

# View details with comments
backlog issue view PROJ-123 --comments

# Create (required: -p, -t, -T, -P)
backlog issue create -p PROJ -t "Title" -T "タスク" -P "中" -a @me -d "Description"

# Update status with comment
backlog issue edit PROJ-123 -S "処理中" -c "Starting work"

# Close
backlog issue close PROJ-123 -c "Done"

# Add comment
backlog issue comment PROJ-123 -b "Progress update"
```

### Pull Requests

```bash
# Create (required: -p, -R, -t, -B, --branch)
backlog pr create -p PROJ -R repo -t "PR title" -B main --branch feat/xxx --issue PROJ-123

# List open PRs
backlog pr list -p PROJ -R repo

# View with comments
backlog pr view -p PROJ -R repo 42 --comments

# Merge
backlog pr merge -p PROJ -R repo 42
```

### Project Info

```bash
backlog project list                  # List projects
backlog project users PROJECT_KEY     # List members
backlog category list -p PROJ         # List categories
backlog milestone list -p PROJ        # List milestones
```

### Wiki

```bash
backlog wiki list -p PROJ
backlog wiki view <wiki-id>
backlog wiki create -p PROJ -n "Page title" -b "Content"
backlog wiki edit <wiki-id> -b "Updated content"
```

### Raw API

For operations not covered by CLI commands. The `/api/v2` prefix can be omitted.

```bash
backlog api /issues -X POST -f "projectId=123" -f "summary=New issue"
backlog api /issues --paginate -f "projectId[]=123"
```

## Common Issues

### Authentication Failed

If you encounter authentication errors:

```bash
# Check current authentication status
backlog auth status

# Re-authenticate
backlog auth login
```

### "Status name not found" or "Issue type not found"

Status names and issue type names are **project-specific**. Always query them first:

```bash
# Get available statuses for a project
backlog status list -p PROJECT_KEY

# Get available issue types for a project
backlog issue-type list -p PROJECT_KEY

# Get available priorities (these are global)
# Built-in values: 高 (High), 中 (Normal), 低 (Low)
```

**Before creating or editing issues:**
1. Query status names: `backlog status list -p PROJECT`
2. Query issue types: `backlog issue-type list -p PROJECT`
3. Use exact names from the query results

### Missing Required Fields

If a command hangs or prompts for input:
- You're missing a required field
- Specify all required flags explicitly (see command help with `--help`)
- Never rely on interactive prompts in agent workflows

### Project Not Found

Ensure the project key is correct and you have access:

```bash
# List available projects
backlog project list

# Use exact project key from the list
```

## References

- **Full command options**: [references/commands.md](./references/commands.md)
- **Data model schemas**: [references/schema.md](./references/schema.md)

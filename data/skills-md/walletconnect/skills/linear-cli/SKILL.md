---
name: linear-cli
description: Manages Linear issues via CLI. Use when user wants to view, start, create, or update Linear issues, create PRs from issues, or configure Linear integration.
---

# Linear CLI

## Goal
Help users manage Linear issues from the terminal—view current work, start issues, create branches, open PRs, and stay in flow.

## When to use
- User asks about their Linear issues or current issue
- User wants to start working on a Linear issue
- User wants to create a PR for a Linear issue
- User needs to create, update, or comment on issues
- User wants to configure Linear CLI for a project

## When not to use
- User is asking about Linear the company or product (not CLI usage)
- User wants Linear API integration in code (point them to Linear SDK)
- User needs Jira, GitHub Issues, or other trackers

## Prerequisites
- `linear` CLI installed (`brew install schpet/tap/linear`)
- `LINEAR_API_KEY` environment variable set (from linear.app/settings/account/security)
- For PR creation: GitHub CLI (`gh`) installed and authenticated

## Default workflow

### 1) Check current context
```bash
linear issue view        # See current issue (detected from branch)
linear issue id          # Just the issue ID
```

### 2) Start an issue
```bash
linear issue list        # Show your unstarted issues
linear issue start       # Interactive: pick issue, creates branch
linear issue start ABC-123  # Start specific issue directly
```

### 3) Create PR when ready
```bash
linear issue pr          # Creates GitHub PR with title/description prefilled
```

## Common commands

| Task | Command |
|------|---------|
| View current issue | `linear issue view` |
| View in browser | `linear issue view -w` |
| List my issues | `linear issue list` |
| List all unstarted | `linear issue list -A` |
| Start issue | `linear issue start` or `linear issue start ABC-123` |
| Create PR | `linear issue pr` |
| Create issue | `linear issue create -t "Title" -d "Description"` |
| Add comment | `linear issue comment add` |
| List teams | `linear team list` |
| Configure | `linear config` |

## Configuration

Run `linear config` to generate `.linear.toml` in your repo. Key settings:

```toml
api_key = "lin_api_..."      # Or use LINEAR_API_KEY env var
team_id = "TEAM_abc123"      # Default team for new issues
workspace = "mycompany"      # Your Linear workspace slug
issue_sort = "priority"      # Or "manual"
vcs = "git"                  # Or "jj" for Jujutsu
```

Config file locations (checked in order):
1. `./.linear.toml` (project root)
2. `~/.config/linear/linear.toml` (global)

## Validation checklist
- [ ] `linear --version` runs (CLI installed)
- [ ] `linear issue list` works (API key valid)
- [ ] `linear team list` shows teams (workspace configured)
- [ ] Branch naming matches Linear's pattern for auto-detection

## Troubleshooting

**"No issue found for current branch"**
- Branch name must contain issue ID (e.g., `feat/abc-123-description`)
- Or specify issue: `linear issue view ABC-123`

**"Unauthorized" errors**
- Check `LINEAR_API_KEY` is set and valid
- Regenerate key at linear.app/settings/account/security

**PR creation fails**
- Ensure `gh` CLI is installed and authenticated (`gh auth status`)
- Must be on a branch with a Linear issue

## Examples

### Example 1: Start morning work
```bash
$ linear issue list
# Shows unstarted issues assigned to you

$ linear issue start
# Interactive picker → selects issue → creates branch → switches to it

$ linear issue view
# Confirms you're on the right issue
```

### Example 2: Create PR for completed work
```bash
$ linear issue view
# Review issue details

$ linear issue pr
# Opens GitHub PR with:
#   - Title: "ABC-123: Issue title"
#   - Description: Issue description + Linear link
```

### Example 3: Quick issue creation
```bash
$ linear issue create -t "Fix login timeout" -d "Users report 30s timeout on slow connections"
# Creates issue, outputs issue ID
```

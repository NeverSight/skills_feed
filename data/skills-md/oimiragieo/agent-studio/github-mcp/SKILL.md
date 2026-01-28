---
name: github-mcp
description: GitHub API operations - repositories, issues, pull requests, actions, code security, discussions, gists, and more. Use for GitHub-related tasks like managing PRs, issues, searching code, and monitoring workflows.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash]
best_practices:
  - Use gh CLI for most operations
  - Verify authentication before operations
  - Check rate limits for bulk operations
error_handling: graceful
streaming: supported
---

# GitHub Skill

## Overview

This skill provides access to the official GitHub MCP server with progressive disclosure for optimal context usage.

**Context Savings**: ~95% reduction

- **MCP Mode**: ~50,000 tokens always loaded (80+ tools)
- **Skill Mode**: ~500 tokens metadata + on-demand loading

## Requirements

- Docker installed and running
- `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable set

## Toolsets

The server provides 80+ tools across 19 toolsets:

| Toolset           | Description                                |
| ----------------- | ------------------------------------------ |
| `actions`         | Workflow management, runs, jobs, artifacts |
| `code_security`   | Scanning alerts, code analysis             |
| `discussions`     | Forum interactions                         |
| `gists`           | Code snippets management                   |
| `issues`          | Issue creation, updates, commenting        |
| `labels`          | Label management and filtering             |
| `projects`        | GitHub Projects board management           |
| `pull_requests`   | PR creation, review, merging               |
| `repos`           | Code search, commits, releases, branches   |
| `users`           | User search and management                 |
| `orgs`            | Organization and team management           |
| `notifications`   | Notification management                    |
| `secret_scanning` | Secret scanning alerts                     |
| `context`         | Context about the user                     |

## Quick Reference

Use the `gh` CLI for GitHub operations:

```bash
# Get repository info
gh repo view anthropics/claude-code

# List issues
gh issue list --repo anthropics/claude-code

# Search code
gh search code "language:python MCP"

# Create issue
gh issue create --repo me/myrepo --title "Bug" --body "Description"

# List pull requests
gh pr list --repo anthropics/claude-code
```

## Common Tools (Default Toolsets: 40 tools)

### Repository Operations

- `search_repositories` - Search for repositories
- `create_repository` - Create a new repository
- `fork_repository` - Fork a repository
- `list_commits` - List repository commits
- `get_commit` - Get commit details
- `get_file_contents` - Get file contents from a repository
- `create_or_update_file` - Create or update a file
- `delete_file` - Delete a file
- `push_files` - Push multiple files
- `search_code` - Search for code across GitHub
- `list_branches` - List repository branches
- `create_branch` - Create a new branch
- `list_tags` - List repository tags
- `get_tag` - Get tag details
- `list_releases` - List releases
- `get_latest_release` - Get latest release
- `get_release_by_tag` - Get release by tag

### Issue Operations

- `list_issues` - List repository issues
- `issue_read` - Read issue details
- `issue_write` - Create/update issues
- `add_issue_comment` - Add a comment to an issue
- `search_issues` - Search for issues
- `list_issue_types` - List issue types (for organizations)
- `get_label` - Get label details
- `sub_issue_write` - Manage sub-issues
- `assign_copilot_to_issue` - Assign Copilot to an issue

### Pull Request Operations

- `list_pull_requests` - List repository pull requests
- `pull_request_read` - Read PR details
- `create_pull_request` - Create a new PR
- `update_pull_request` - Update a PR
- `update_pull_request_branch` - Update PR branch
- `merge_pull_request` - Merge a PR
- `search_pull_requests` - Search for pull requests
- `pull_request_review_write` - Create/submit PR reviews
- `add_comment_to_pending_review` - Add comments to pending review
- `request_copilot_review` - Request Copilot review

### User & Team Operations

- `get_me` - Get current authenticated user
- `search_users` - Search for users
- `get_teams` - Get organization teams
- `get_team_members` - Get team members

## Configuration

The skill uses Docker to run the official GitHub MCP server:

- **Image**: `ghcr.io/github/github-mcp-server`
- **Auth**: `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable

### Environment Variables

| Variable                       | Required | Description                                 |
| ------------------------------ | -------- | ------------------------------------------- |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | Yes      | GitHub PAT for authentication               |
| `GITHUB_HOST`                  | No       | For GitHub Enterprise (default: github.com) |
| `GITHUB_TOOLSETS`              | No       | Comma-separated toolsets to enable          |
| `GITHUB_READ_ONLY`             | No       | Set to 1 for read-only mode                 |

### Limiting Toolsets

When using MCP, configure toolsets via environment variables:

```bash
# Only repos and issues
GITHUB_TOOLSETS=repos,issues

# Only pull requests and code security
GITHUB_TOOLSETS=pull_requests,code_security
```

## Error Handling

If operations fail:

1. Verify Docker is running: `docker ps`
2. Check GitHub token is set: `echo $GITHUB_PERSONAL_ACCESS_TOKEN`
3. Ensure token has required permissions for the operation
4. Use `gh auth status` to verify authentication

## Related

- Official GitHub MCP Server: https://github.com/github/github-mcp-server
- GitHub API Documentation: https://docs.github.com/en/rest

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.

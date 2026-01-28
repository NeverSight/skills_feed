---
name: github
description: Work with GitHub issues, pull requests, workflows, and repositories using the gh CLI. Use when managing GitHub projects.
metadata:
  author: odyssey4me
  version: "0.1.0"
license: MIT
---

# GitHub Skill

This skill provides guidance for working with GitHub using the official `gh` CLI tool. All GitHub operations (issues, PRs, workflows, repositories) are performed using `gh` commands.

## Prerequisites

**Install gh CLI**: <https://cli.github.com/manual/installation>

Quick install:
```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
sudo apt install gh

# Fedora/RHEL/CentOS
sudo dnf install gh

# Windows
winget install --id GitHub.cli
```

## Authentication

```bash
# Authenticate with GitHub
gh auth login

# Verify authentication
gh auth status
```

See [GitHub CLI Authentication](https://cli.github.com/manual/gh_auth_login) for details.

## Commands

### Issues

```bash
gh issue list                    # List issues
gh issue view 123                # View issue details
gh issue create                  # Create new issue
gh issue comment 123             # Add comment
gh issue close 123               # Close issue
gh issue edit 123 --add-label bug  # Edit issue
```

Full reference: [gh issue](https://cli.github.com/manual/gh_issue)

### Pull Requests

```bash
gh pr list                       # List PRs
gh pr view 456                   # View PR details
gh pr create                     # Create new PR
gh pr review 456 --approve       # Approve PR
gh pr merge 456 --squash         # Merge PR
gh pr checkout 456               # Checkout PR branch
gh pr diff 456                   # View PR diff
gh pr checks 456                 # View CI status
```

Full reference: [gh pr](https://cli.github.com/manual/gh_pr)

### Workflows & Actions

```bash
gh workflow list                 # List workflows
gh workflow run "CI"             # Trigger workflow
gh run list                      # List workflow runs
gh run view 123456               # View run details
gh run watch 123456              # Watch run progress
gh run download 123456           # Download artifacts
gh run rerun 123456 --failed     # Rerun failed jobs
```

Full references:
- [gh workflow](https://cli.github.com/manual/gh_workflow)
- [gh run](https://cli.github.com/manual/gh_run)

### Repositories

```bash
gh repo list                     # List repositories
gh repo view OWNER/REPO          # View repository
gh repo create                   # Create repository
gh repo clone OWNER/REPO         # Clone repository
gh repo fork OWNER/REPO          # Fork repository
```

Full reference: [gh repo](https://cli.github.com/manual/gh_repo)

### Search

```bash
gh search repos "machine learning"   # Search repositories
gh search issues "is:open label:bug" # Search issues
gh search prs "is:open"              # Search pull requests
gh search code "function auth"       # Search code
```

Full reference: [gh search](https://cli.github.com/manual/gh_search)

## Examples

### Daily PR Review

```bash
# List PRs waiting for your review
gh pr list --search "review-requested:@me"

# Review a specific PR
gh pr view 456
gh pr checks 456
gh pr diff 456
gh pr review 456 --approve
```

### Create Issue and Link PR

```bash
# Create issue
gh issue create --title "Bug: Login fails" --body "Description" --label bug

# Create PR that fixes it (use issue number in title/body)
gh pr create --title "Fix login bug (#123)" --body "Fixes #123"
```

### Monitor CI Pipeline

```bash
# Watch latest workflow run
gh run watch $(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')

# Check failed runs
gh run list --status failure

# Rerun failed jobs
gh run rerun RUNID --failed
```

See [common-workflows.md](references/common-workflows.md) for more examples.

## Advanced Usage

### JSON Output for Scripting

```bash
# Get specific fields
gh issue list --json number,title,author

# Process with jq
gh pr list --json number,title | jq '.[] | "\(.number): \(.title)"'

# Export to CSV
gh issue list --json number,title,author | jq -r '.[] | @csv'
```

### GitHub API Access

For operations not covered by gh commands:

```bash
# Make authenticated API request
gh api repos/OWNER/REPO/issues

# POST request
gh api repos/OWNER/REPO/issues -X POST -f title="Issue" -f body="Text"

# Process response
gh api repos/OWNER/REPO | jq '.stargazers_count'
```

Full reference: [gh api](https://cli.github.com/manual/gh_api)

### Aliases for Frequent Operations

```bash
# Create shortcuts
gh alias set prs 'pr list --author @me'
gh alias set issues 'issue list --assignee @me'
gh alias set review 'pr list --search "review-requested:@me"'

# Use them
gh prs
gh issues
gh review
```

## Rate Limits

GitHub enforces rate limits for API requests:
- **Core API**: 5,000 requests/hour
- **Search API**: 30 requests/minute

Check current status:
```bash
gh api rate_limit --jq '.rate'
```

**Best practices for bulk operations:**
- Check rate limit before starting
- Use specific filters to reduce result sets
- Prefer `--limit` flag to control results
- Use exact issue/PR numbers when known

## Configuration

```bash
# View configuration
gh config list

# Set default editor
gh config set editor vim

# Set git protocol
gh config set git_protocol ssh
```

Configuration stored in `~/.config/gh/config.yml`

## Troubleshooting

```bash
# Check authentication
gh auth status

# Re-authenticate
gh auth login

# Enable debug logging
GH_DEBUG=1 gh issue list

# Check gh version
gh --version
```

## Official Documentation

- **GitHub CLI Manual**: <https://cli.github.com/manual/>
- **GitHub CLI Repository**: <https://github.com/cli/cli>
- **GitHub API Documentation**: <https://docs.github.com/en/rest>
- **GitHub Actions**: <https://docs.github.com/en/actions>

## Summary

The GitHub skill uses the official `gh` CLI exclusively. No custom scripts are needed - `gh` provides comprehensive functionality for all GitHub operations.

**Quick start:**
1. Install: `brew install gh` (or equivalent for your OS)
2. Authenticate: `gh auth login`
3. Verify: `gh auth status`
4. Use: `gh issue list`, `gh pr create`, etc.

For detailed command reference, use `gh <command> --help` or visit <https://cli.github.com/manual/>.

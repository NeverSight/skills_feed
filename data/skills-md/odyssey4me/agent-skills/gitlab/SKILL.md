---
name: gitlab
description: Work with GitLab issues, merge requests, pipelines, and repositories using the glab CLI. Use when managing GitLab projects.
metadata:
  author: odyssey4me
  version: "0.1.0"
license: MIT
---

# GitLab Skill

This skill provides guidance for working with GitLab using the official `glab` CLI tool. All GitLab operations (issues, merge requests, pipelines, repositories) are performed using `glab` commands.

## Prerequisites

**Install glab CLI**: <https://gitlab.com/gitlab-org/cli#installation>

Quick install:
```bash
# macOS
brew install glab

# Linux (Debian/Ubuntu)
sudo apt install glab

# Fedora/RHEL/CentOS
sudo dnf install glab

# Windows
winget install GLab.GLab
```

## Authentication

```bash
# Authenticate with GitLab
glab auth login

# Verify authentication
glab auth status
```

Supports GitLab.com, GitLab Dedicated, and GitLab Self-Managed instances.
See [GitLab CLI Authentication](https://docs.gitlab.com/cli/#authentication) for details.

## Commands

### Issues

```bash
glab issue list                    # List issues
glab issue view 123                # View issue details
glab issue create                  # Create new issue
glab issue note 123                # Add comment
glab issue close 123               # Close issue
glab issue update 123 --label bug  # Edit issue
```

Full reference: [glab issue](https://docs.gitlab.com/cli/commands/glab_issue.html)

### Merge Requests

```bash
glab mr list                       # List merge requests
glab mr view 456                   # View MR details
glab mr create                     # Create new MR
glab mr approve 456                # Approve MR
glab mr merge 456                  # Merge MR
glab mr checkout 456               # Checkout MR branch
glab mr diff 456                   # View MR diff
glab mr note 456                   # Add comment to MR
```

Full reference: [glab mr](https://docs.gitlab.com/cli/commands/glab_mr.html)

### Pipelines & CI/CD

```bash
glab ci list                       # List pipelines
glab ci view 123456                # View pipeline details
glab ci run                        # Trigger pipeline
glab ci trace                      # Watch pipeline logs
glab ci retry 123456               # Retry failed pipeline
glab ci status                     # Show pipeline status
```

Full references:
- [glab ci](https://docs.gitlab.com/cli/commands/glab_ci.html)
- [glab pipeline](https://docs.gitlab.com/cli/commands/glab_pipeline.html)

### Repositories

```bash
glab repo list                     # List repositories
glab repo view GROUP/REPO          # View repository
glab repo create                   # Create repository
glab repo clone GROUP/REPO         # Clone repository
glab repo fork GROUP/REPO          # Fork repository
```

Full reference: [glab repo](https://docs.gitlab.com/cli/commands/glab_repo.html)

### Releases

```bash
glab release list                  # List releases
glab release view v1.0.0           # View release details
glab release create v1.0.0         # Create release
glab release delete v1.0.0         # Delete release
```

Full reference: [glab release](https://docs.gitlab.com/cli/commands/glab_release.html)

## Examples

### Daily MR Review

```bash
# List MRs assigned to you
glab mr list --assignee=@me

# Review a specific MR
glab mr view 456
glab mr diff 456
glab mr approve 456
```

### Create Issue and Link MR

```bash
# Create issue
glab issue create --title "Bug: Login fails" --description "Description" --label bug

# Create MR that closes it
glab mr create --title "Fix login bug" --description "Closes #123"
```

### Monitor CI Pipeline

```bash
# Check current pipeline status
glab ci status

# Watch pipeline logs in real-time
glab ci trace

# Retry failed jobs
glab ci retry
```

See [common-workflows.md](references/common-workflows.md) for more examples.

## Advanced Usage

### JSON Output for Scripting

```bash
# Get JSON output
glab issue list --output json

# Process with jq
glab mr list --output json | jq '.[] | "\(.iid): \(.title)"'
```

### GitLab API Access

For operations not covered by glab commands:

```bash
# Make authenticated API request
glab api projects/:id/issues

# POST request
glab api projects/:id/issues -X POST -f title="Issue" -f description="Text"

# Process response
glab api projects/:id | jq '.star_count'
```

Full reference: [glab api](https://docs.gitlab.com/cli/commands/glab_api.html)

### Aliases for Frequent Operations

```bash
# Create shortcuts
glab alias set mrs 'mr list --assignee=@me'
glab alias set issues 'issue list --assignee=@me'
glab alias set pipelines 'ci list'

# Use them
glab mrs
glab issues
glab pipelines
```

## Configuration

```bash
# View configuration
glab config get

# Set default editor
glab config set editor vim

# Set default Git protocol
glab config set git_protocol ssh
```

Configuration stored in `~/.config/glab-cli/config.yml`

## Troubleshooting

```bash
# Check authentication
glab auth status

# Re-authenticate
glab auth login

# Enable debug logging
DEBUG=1 glab issue list

# Check glab version
glab version
```

## Official Documentation

- **GitLab CLI Manual**: <https://docs.gitlab.com/cli/>
- **GitLab CLI Repository**: <https://gitlab.com/gitlab-org/cli>
- **GitLab API Documentation**: <https://docs.gitlab.com/ee/api/>
- **GitLab CI/CD**: <https://docs.gitlab.com/ee/ci/>

## Summary

The GitLab skill uses the official `glab` CLI exclusively. No custom scripts are needed - `glab` provides comprehensive functionality for all GitLab operations.

**Quick start:**
1. Install: `brew install glab` (or equivalent for your OS)
2. Authenticate: `glab auth login`
3. Verify: `glab auth status`
4. Use: `glab issue list`, `glab mr create`, etc.

For detailed command reference, use `glab <command> --help` or visit <https://docs.gitlab.com/cli/>.

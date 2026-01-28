---
name: gerrit
description: Work with Gerrit code review using git-review CLI. Use when submitting changes, downloading patches, and managing code reviews in Gerrit.
metadata:
  author: odyssey4me
  version: "0.1.0"
license: MIT
---

# Gerrit Skill

This skill provides guidance for working with Gerrit code review using the `git-review` CLI tool. All Gerrit operations (submitting changes, downloading patches, reviewing code) are performed using `git-review` commands.

## Prerequisites

**Install git-review**: <https://docs.opendev.org/opendev/git-review/latest/installation.html>

Quick install:
```bash
# Using pip (recommended)
pip install git-review

# macOS
brew install git-review

# Debian/Ubuntu
sudo apt install git-review

# Fedora/RHEL/CentOS
sudo dnf install git-review
```

## Authentication

git-review uses SSH for authentication with Gerrit servers.

```bash
# Configure Gerrit username (if different from local user)
git config --global gitreview.username yourgerrituser

# Test SSH connection
ssh -p 29418 youruser@review.example.com gerrit version

# Add SSH key to Gerrit
# 1. Generate SSH key if needed: ssh-keygen -t ed25519
# 2. Copy public key: cat ~/.ssh/id_ed25519.pub
# 3. Add to Gerrit: Settings > SSH Keys
```

Gerrit supports multiple authentication methods:
- **SSH** (recommended): Used by git-review for all operations
- **HTTP/HTTPS**: For web UI and REST API access (set password in Settings > HTTP Password)

See [Gerrit Authentication](https://gerrit-review.googlesource.com/Documentation/user-upload.html#ssh) for details.

## Initial Setup

### Configure Repository

```bash
# One-time setup for a repository
git review -s

# Or manually create .gitreview file in repository root
cat > .gitreview <<EOF
[gerrit]
host=review.example.com
port=29418
project=myproject
defaultbranch=main
EOF
```

See [Installation Guide](https://docs.opendev.org/opendev/git-review/latest/installation.html) for details.

## Commands

### Submitting Changes

```bash
git review                          # Submit current branch for review
git review -t topic-name            # Submit with topic
git review -f                       # Submit and close local branch
git review --reviewers user1,user2  # Add reviewers
git review -n                       # Dry-run (show what would be done)
```

Full reference: [git-review usage](https://docs.opendev.org/opendev/git-review/latest/usage.html)

### Downloading Changes

```bash
git review -d 12345                 # Download change 12345
git review -d 12345,3               # Download patchset 3 of change 12345
git review -x 12345                 # Cherry-pick change (no branch)
git review -m 12345                 # Compare local changes to remote
```

Downloads create a local branch named `review/username/topic`.

### Updating Changes

```bash
# Make changes to downloaded review
git commit --amend
git review                          # Upload new patchset

# Update to latest patchset
git review -d 12345                 # Re-download updates the branch
```

### Advanced Options

```bash
git review -R                       # Don't rebase (submit as-is)
git review -D                       # Draft mode (WIP changes)
git review --no-cache               # Skip local cache
git review -v                       # Verbose output
git review --track                  # Track remote branch
```

## Configuration

### Per-Repository Settings

File: `.gitreview` (repository root)
```ini
[gerrit]
host=review.example.com
port=29418
project=myproject/subproject
defaultbranch=main
defaultremote=origin
```

### Global Settings

```bash
# Set Gerrit username
git config --global gitreview.username myuser

# Set default remote
git config --global gitreview.remote gerrit

# Configure scheme (ssh/http/https)
git config --global gitreview.scheme ssh
```

Configuration stored in `~/.gitconfig`

## Examples

### Daily Workflow

```bash
# Start work on new feature
git checkout -b feature-branch
# ... make changes ...
git commit -m "Add new feature"

# Submit for review
git review -t feature-topic

# Address review comments
# ... make changes ...
git commit --amend
git review
```

### Reviewing Others' Changes

```bash
# Download change for review
git review -d 12345

# Test the change
# ... run tests, verify code ...

# Return to main branch
git checkout main
git branch -D review/user/topic
```

### Working with Topics

```bash
# Submit with topic
git review -t authentication-refactor

# All related changes will be grouped under this topic
git commit -m "Part 2: Update tests"
git review -t authentication-refactor
```

See [common-workflows.md](references/common-workflows.md) for more examples.

## Advanced Usage

### SSH Commands

For operations not covered by git-review:

```bash
# Query open changes
ssh -p 29418 review.example.com gerrit query status:open project:myproject

# Query specific change
ssh -p 29418 review.example.com gerrit query change:12345

# Review from command line
ssh -p 29418 review.example.com gerrit review 12345,3 --verified +1 --message "'Looks good'"

# Abandon change
ssh -p 29418 review.example.com gerrit review 12345 --abandon
```

Full reference: [Gerrit SSH Commands](https://gerrit-review.googlesource.com/Documentation/cmd-index.html)

### JSON Output for Scripting

```bash
# Get change info as JSON
ssh -p 29418 review.example.com gerrit query --format=JSON change:12345

# Process with jq
ssh -p 29418 review.example.com gerrit query --format=JSON status:open | jq '.subject'
```

### Multiple Gerrit Servers

```bash
# Set remote for specific server
git config gitreview.remote gerrit-prod

# Or specify via command line
git review -r gerrit-staging
```

## Troubleshooting

```bash
# Re-run setup
git review -s

# Force setup (fixes common issues)
git review -s --force

# Verbose output for debugging
git review -v

# Check configuration
cat .gitreview
git config -l | grep gitreview

# Test SSH connection
ssh -p 29418 youruser@review.example.com gerrit version
```

### Common Issues

**"We don't know where your gerrit is"**
```bash
git review -s              # Run setup
# Or create .gitreview file manually
```

**"fatal: 'gerrit' does not appear to be a git repository"**
```bash
git review -s              # Setup remote
git remote -v              # Verify gerrit remote exists
```

**"Permission denied (publickey)"**
```bash
# Add SSH key to Gerrit (Settings > SSH Keys)
# Or configure username:
git config --global gitreview.username youruser
```

**Change-Id missing**
```bash
# Install commit-msg hook
curl -Lo .git/hooks/commit-msg \
  https://review.example.com/tools/hooks/commit-msg
chmod u+x .git/hooks/commit-msg

# Or let git-review install it
git review -s
```

## Official Documentation

- **git-review Manual**: <https://docs.opendev.org/opendev/git-review/latest/>
- **git-review Repository**: <https://opendev.org/opendev/git-review>
- **Gerrit Documentation**: <https://gerrit-review.googlesource.com/Documentation/>
- **Gerrit SSH Commands**: <https://gerrit-review.googlesource.com/Documentation/cmd-index.html>

## Summary

The Gerrit skill uses `git-review` CLI exclusively. No custom scripts are needed - `git-review` provides comprehensive functionality for all Gerrit code review operations.

**Quick start:**
1. Install: `pip install git-review`
2. Setup: `git review -s` (in repository)
3. Submit: `git review`
4. Download: `git review -d 12345`

For detailed command reference, use `git review --help` or visit <https://docs.opendev.org/opendev/git-review/latest/>.

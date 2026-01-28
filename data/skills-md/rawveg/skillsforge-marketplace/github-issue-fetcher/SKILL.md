---
name: github-issue-fetcher
description: This skill should be used when users need to fetch GitHub issues from the current repository, including getting the next issue to work on, retrieving specific issue fields (body, number, title, labels, etc.), or querying issues with custom sorting and filtering. Triggers on requests like "get the next GitHub issue", "what's the next issue number", "show me the issue body", or "find issues with label X".
---

# GitHub Issue Fetcher

## Overview

Fetch GitHub issues from the current repository using the `gh` CLI tool with flexible sorting, filtering, and field extraction capabilities. This skill provides patterns for common workflows like getting the next issue to work on, extracting specific fields, and querying issues with custom criteria.

## Prerequisites

This skill requires two command-line tools to be installed:

1. **GitHub CLI (`gh`)** - Official GitHub command-line tool
2. **jq** - JSON processor for parsing command output

### Checking Dependencies

Before executing issue commands, verify both tools are available:

```bash
# Check if gh is installed
command -v gh >/dev/null 2>&1 || echo "gh not found"

# Check if jq is installed
command -v jq >/dev/null 2>&1 || echo "jq not found"
```

### Installation Guidance

If a required tool is missing, provide the user with installation instructions based on their platform:

**GitHub CLI (`gh`):**
- macOS: `brew install gh`
- Linux (Debian/Ubuntu): `sudo apt install gh`
- Linux (Fedora/RHEL): `sudo dnf install gh`
- Windows: `winget install --id GitHub.cli`
- Other: Visit https://cli.github.com/

**jq:**
- macOS: `brew install jq`
- Linux (Debian/Ubuntu): `sudo apt-get install jq`
- Linux (Fedora/RHEL): `sudo dnf install jq`
- Windows: `winget install jqlang.jq`
- Other: Visit https://jqlang.github.io/jq/download/

### GitHub Authentication

The `gh` CLI requires authentication. If the user encounters authentication errors, guide them to run:

```bash
gh auth login
```

This will prompt them through the authentication flow.

## Core Capabilities

### 1. Detecting the Current Repository

To automatically determine the current repository, use git commands:

```bash
# Get the repository in owner/repo format
REPO=$(git config --get remote.origin.url | sed -E 's|.*github\.com[:/]([^/]+/[^.]+)(\.git)?|\1|')
```

Alternatively, let `gh` auto-detect by omitting the `--repo` flag when running from within a git repository directory.

### 2. Fetching the Next Issue

The "next issue" defaults to the oldest created open issue. Use `gh issue list` with sorting and limiting:

```bash
# Get the oldest created issue (next to work on)
gh issue list --search "sort:created-asc" --limit 1 --json number,title,body,labels,assignees,milestone,state,url
```

### 3. Extracting Specific Fields

Use `jq` to extract specific fields from the JSON output:

```bash
# Get just the issue number
gh issue list --search "sort:created-asc" --limit 1 --json number | jq '.[0].number'

# Get just the issue body
gh issue list --search "sort:created-asc" --limit 1 --json body | jq -r '.[0].body'

# Get just the issue title
gh issue list --search "sort:created-asc" --limit 1 --json title | jq -r '.[0].title'

# Get multiple fields in a formatted way
gh issue list --search "sort:created-asc" --limit 1 --json number,title,body | jq -r '.[0] | "Issue #\(.number): \(.title)\n\n\(.body)"'
```

**Note:** Use `-r` flag with `jq` to output raw strings without quotes.

### 4. Available Fields

The `--json` flag accepts the following fields:

- `number` - Issue number
- `title` - Issue title
- `body` - Issue body/description
- `labels` - Array of label objects
- `assignees` - Array of assignee objects
- `milestone` - Milestone object
- `state` - Issue state (OPEN, CLOSED)
- `url` - Issue URL
- `createdAt` - Creation timestamp
- `updatedAt` - Last update timestamp
- `closedAt` - Close timestamp (if closed)
- `comments` - Number of comments
- `author` - Author object

### 5. Sorting Options

Use the `--search` flag with sort qualifiers:

```bash
# Oldest created (default for "next issue")
--search "sort:created-asc"

# Newest created
--search "sort:created-desc"

# Most recently updated
--search "sort:updated-desc"

# Least recently updated
--search "sort:updated-asc"

# Most commented
--search "sort:comments-desc"

# Least commented
--search "sort:comments-asc"
```

**Note:** GitHub doesn't have a native "priority" sort, but priority can be inferred from labels, milestones, or projects.

### 6. Filtering Options

Combine multiple filters in the `--search` query:

```bash
# Filter by label
--search "label:bug sort:created-asc"

# Filter by assignee
--search "assignee:username sort:created-asc"

# Filter by milestone
--search "milestone:\"v1.0\" sort:created-asc"

# Filter by state (default is open)
--search "is:open sort:created-asc"
--search "is:closed sort:created-desc"

# Combine multiple filters
--search "label:bug assignee:@me is:open sort:created-asc"

# No assignee
--search "no:assignee sort:created-asc"

# No label
--search "no:label sort:created-asc"
```

### 7. Common Patterns

**Get the next issue to work on:**
```bash
gh issue list --search "sort:created-asc" --limit 1 --json number,title,body
```

**Get just the issue number for scripting:**
```bash
ISSUE_NUM=$(gh issue list --search "sort:created-asc" --limit 1 --json number | jq '.[0].number')
```

**Get the full issue body text:**
```bash
gh issue list --search "sort:created-asc" --limit 1 --json body | jq -r '.[0].body'
```

**Get the most urgent unassigned bug:**
```bash
gh issue list --search "label:bug no:assignee sort:created-asc" --limit 1 --json number,title,body
```

**List all high-priority issues:**
```bash
gh issue list --search "label:priority-high sort:created-asc" --json number,title,labels
```

## Usage Workflow

When a user requests GitHub issue information:

1. **Verify dependencies**: Check that `gh` and `jq` are installed; if not, provide installation guidance
2. **Determine the repository context**: Check if running in a git repository, or ask the user for the repo name
3. **Understand the request**: Identify what fields they need (body, number, title, etc.)
4. **Apply appropriate sorting**: Default to `sort:created-asc` for "next issue" requests, adjust based on user needs
5. **Apply filters if specified**: Add label, assignee, or other filters to the search query
6. **Construct the command**: Build the `gh issue list` command with appropriate flags
7. **Extract fields**: Use `jq` to parse and extract only the requested fields
8. **Present results**: Return the extracted data in the format the user needs

## Examples

**User request:** "What's the next GitHub issue to work on?"
```bash
gh issue list --search "sort:created-asc" --limit 1 --json number,title | jq -r '.[0] | "#\(.number): \(.title)"'
```

**User request:** "Give me the body of the next GitHub issue"
```bash
gh issue list --search "sort:created-asc" --limit 1 --json body | jq -r '.[0].body'
```

**User request:** "Show me the newest bug with no assignee"
```bash
gh issue list --search "label:bug no:assignee sort:created-desc" --limit 1 --json number,title,body | jq -r '.[0] | "Issue #\(.number): \(.title)\n\n\(.body)"'
```

---
name: jira
description: Search and manage Jira issues using JQL queries, create/update issues, and manage workflows. Use when working with Jira project management.
metadata:
  author: odyssey4me
  version: "0.2.0"
license: MIT
---

# Jira

Interact with Jira for issue tracking, search, and workflow management.

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install --user requests keyring pyyaml
   ```

2. **Download the skill** from [Releases](https://github.com/odyssey4me/agent-skills/releases) or use directly from this repository.

## Setup Verification

After installation, verify the skill is properly configured:

```bash
python scripts/jira.py check
```

This will check:
- Python dependencies (requests, keyring, pyyaml)
- Authentication configuration
- Connectivity to Jira

If anything is missing, the check command will provide setup instructions.

## Authentication

Configure Jira authentication using one of these methods:

### Option 1: Environment Variables (Recommended)

```bash
export JIRA_BASE_URL="https://yourcompany.atlassian.net"
export JIRA_EMAIL="you@example.com"
export JIRA_API_TOKEN="your-token"
```

Add these to your `~/.bashrc` or `~/.zshrc` for persistence.

### Option 2: Config File

Create `~/.config/agent-skills/jira.yaml`:

```yaml
url: https://yourcompany.atlassian.net
email: you@example.com
token: your-token
```

### Required Credentials

- **URL**: Your Jira instance URL (e.g., `https://yourcompany.atlassian.net`)
- **Email**: Your Atlassian account email
- **API Token**: Create at https://id.atlassian.com/manage-profile/security/api-tokens

## Rate Limits

Atlassian Jira Cloud enforces rate limits to ensure fair usage and system stability. The specific limits vary based on your Jira instance type and plan:

- **Jira Cloud**: Rate limits vary by endpoint and are enforced per-user and per-app
- **Jira Data Center/Server**: Rate limits are typically configured by administrators

### Automatic Rate Limit Handling

This skill automatically handles temporary rate limit errors (429 Too Many Requests) by:
- Detecting rate limit responses from the Jira API
- Waiting for the time specified in the `Retry-After` header
- Retrying failed requests up to 3 times with exponential backoff (1s, 2s, 4s)
- Providing clear error messages if rate limits persist after all retry attempts

**You don't need to manually handle rate limiting** - the skill manages this automatically. If you encounter persistent rate limit errors, consider:
- Reducing the frequency of API calls
- Using `--max-results` to limit the number of items returned
- Spreading bulk operations over a longer time period
- Contacting your Jira administrator if limits seem too restrictive

### Best Practices for AI Agents

When using this skill for bulk operations or automated workflows:
1. Use specific JQL queries to minimize the number of API calls needed
2. Leverage configuration defaults and JQL scope to avoid redundant filters
3. Use `--max-results` appropriately - don't fetch more data than needed
4. For large datasets, consider paginating manually with multiple smaller queries
5. Be aware that search operations may be more heavily rate-limited than direct issue access

## Configuration Defaults

Optionally configure defaults in `~/.config/agent-skills/jira.yaml` to reduce repetitive typing:

```yaml
# Authentication (optional if using environment variables)
url: https://yourcompany.atlassian.net
email: you@example.com
token: your-token

# Optional defaults
defaults:
  jql_scope: "project = DEMO AND assignee = currentUser()"
  security_level: "Red Hat Internal"
  max_results: 25
  fields: ["summary", "status", "assignee", "priority", "created"]

# Optional project-specific defaults
projects:
  DEMO:
    issue_type: "Task"
    priority: "Medium"
  PROD:
    issue_type: "Bug"
    priority: "High"
```

### How Defaults Work

- **CLI arguments always override** config defaults
- **JQL scope** is prepended to all searches: `(scope) AND (your_query)`
- **Security level** applies to comments and transitions with comments
- **Project defaults** apply when creating issues in that project

### View Configuration

```bash
# Show all configuration
python scripts/jira.pyconfig show

# Show project-specific defaults
python scripts/jira.pyconfig show --project DEMO
```

## Commands

### check

Verify configuration and connectivity.

```bash
python scripts/jira.py check
```

This validates:
- Python dependencies are installed
- Authentication is configured
- Can connect to Jira
- API version is detected correctly

### search

Search for issues using JQL (Jira Query Language).

```bash
# Standard JQL
python scripts/jira.pysearch "project = DEMO AND status = Open"
python scripts/jira.pysearch "assignee = currentUser() ORDER BY updated DESC" --max-results 20

# ScriptRunner Enhanced Search (if available)
# Find issues linked to a specific issue
python scripts/jira.pysearch 'issue in linkedIssuesOf("DEMO-123")'

# Find parent/child relationships
python scripts/jira.pysearch 'issue in parentsOf("DEMO-123")'
python scripts/jira.pysearch 'issue in subtasksOf("DEMO-123")'

# Find issues commented on by a specific user
python scripts/jira.pysearch 'issue in commentedByUser("username")'

# Find epics and their issues
python scripts/jira.pysearch 'issue in epicsOf("DEMO-123")'
python scripts/jira.pysearch 'issue in issuesInEpics("EPIC-123")'

# Find issues with specific link types (dependencies, blocks, etc.)
python scripts/jira.pysearch 'issue in hasLinkType("Dependency")'
```

**Arguments:**
- `jql`: JQL query string (required) - supports ScriptRunner functions if installed
- `--max-results`: Maximum number of results (default: 50)
- `--fields`: Comma-separated list of fields to include
- `--json`: Output as JSON

**ScriptRunner Support:**

The skill automatically detects if ScriptRunner Enhanced Search is installed and validates queries that use advanced JQL functions. If ScriptRunner functions are detected but the plugin is not available, you'll receive a warning.

Common ScriptRunner functions include:
- `linkedIssuesOf()`, `hasLinkType()` - Link and dependency queries
- `subtasksOf()`, `parentsOf()`, `epicsOf()` - Hierarchy navigation
- `commentedByUser()`, `transitionedBy()` - User activity tracking
- And many more...

**For complete ScriptRunner guidance** including user lookups, practical examples, and troubleshooting, read [scriptrunner.md](references/scriptrunner.md).

Note: ScriptRunner works differently on Cloud vs Data Center/Server instances. The skill handles both automatically.

### issue

Get, create, update, or comment on issues.

```bash
# Get issue details
python scripts/jira.pyissue get DEMO-123

# Create new issue
python scripts/jira.pyissue create --project DEMO --type Task --summary "New task"

# Update issue
python scripts/jira.pyissue update DEMO-123 --summary "Updated summary"

# Add comment
python scripts/jira.pyissue comment DEMO-123 "This is a comment"

# Add private comment with security level
python scripts/jira.pyissue comment DEMO-123 "Internal note" --security-level "Red Hat Internal"
```

### transitions

Manage issue workflow transitions.

```bash
# List available transitions
python scripts/jira.pytransitions list DEMO-123

# Transition issue
python scripts/jira.pytransitions do DEMO-123 "In Progress"
python scripts/jira.pytransitions do DEMO-123 "Done" --comment "Completed"

# Transition with private comment
python scripts/jira.pytransitions do DEMO-123 "Done" --comment "Internal resolution notes" --security-level "Red Hat Internal"
```

### config

Manage configuration and view effective defaults.

```bash
# Show all configuration and defaults
python scripts/jira.pyconfig show

# Show project-specific defaults
python scripts/jira.pyconfig show --project DEMO
```

This displays:
- Authentication settings (with masked token)
- Default JQL scope, security level, max results, and fields
- Project-specific defaults for issue type and priority

## Examples

### Verify Setup

```bash
python scripts/jira.py check
```

### Find my open issues

```bash
python scripts/jira.pysearch "assignee = currentUser() AND status != Done ORDER BY priority DESC"
```

### Create a bug report

```bash
python scripts/jira.pyissue create \
  --project DEMO \
  --type Bug \
  --summary "Login button not working" \
  --description "The login button on the homepage does not respond to clicks."
```

### Move issue through workflow

```bash
# Start work on an issue
python scripts/jira.pytransitions do DEMO-123 "In Progress"

# Complete the issue
python scripts/jira.pytransitions do DEMO-123 "Done" --comment "Implemented and tested"
```

### Add private comment

```bash
# Add comment visible only to specific security level
python scripts/jira.pyissue comment DEMO-123 \
  "This is sensitive internal information" \
  --security-level "Red Hat Internal"
```

### Search with specific fields

```bash
python scripts/jira.pysearch \
  "project = DEMO AND created >= -7d" \
  --fields "key,summary,status,assignee,created"
```

### Using Configuration Defaults

With defaults configured as shown in the [Configuration Defaults](#configuration-defaults) section:

```bash
# Search uses JQL scope automatically
python scripts/jira.pysearch "status = Open"
# Becomes: (project = DEMO AND assignee = currentUser()) AND (status = Open)

# Search with automatic max_results and fields from config
python scripts/jira.pysearch "priority = High"
# Uses configured max_results (25) and fields automatically

# Create issue uses project defaults
python scripts/jira.pyissue create --project DEMO --summary "Fix login bug"
# Automatically uses issue_type="Task" and priority="Medium" from DEMO project defaults

# Comments use default security level
python scripts/jira.pyissue comment DEMO-123 "Internal note"
# Automatically applies security_level="Red Hat Internal"

# Override defaults when needed
python scripts/jira.pysearch "status = Open" --max-results 100
# CLI argument overrides the configured default of 25
```

## JQL Reference

Common JQL queries:

| Query | Description |
|-------|-------------|
| `project = DEMO` | Issues in DEMO project |
| `assignee = currentUser()` | Issues assigned to you |
| `status = "In Progress"` | Issues in progress |
| `created >= -7d` | Created in last 7 days |
| `updated >= startOfDay()` | Updated today |
| `priority = High` | High priority issues |
| `labels = "bug"` | Issues with "bug" label |

Combine with `AND`, `OR`, and use `ORDER BY` for sorting.

## Troubleshooting

### Check command fails

Run `python scripts/jira.pycheck` to diagnose issues. It will provide specific error messages and setup instructions.

### Authentication failed

1. Verify your API token is correct
2. Ensure you're using your email (not username)
3. For Jira Cloud, use your Atlassian account email
4. For Jira Data Center/Server, use your username

### Permission denied

You may not have access to the requested project or issue. Contact your Jira administrator.

### JQL syntax error

Use the Jira web interface to test your JQL query before using it in scripts.

### Import errors

Ensure dependencies are installed:
```bash
pip install --user requests keyring pyyaml
```

---
name: zendesk
description: Interact with Zendesk Support via CLI - search tickets, view details, analyze metrics, manage users/organizations, and update tickets. All responses are saved locally for efficient jq querying.
when_to_use: When users ask about Zendesk tickets, support metrics, CSAT ratings, views, users, organizations, or need to search/update tickets.
---

# Zendesk CLI Skill

A command-line interface for comprehensive Zendesk API integration. Run commands via `uv run zendesk <command>` in the skill directory.

> **IMPORTANT: Always use `uv run`**
>
> All commands MUST be run with `uv run` to ensure dependencies are available:
> - CLI commands: `uv run zendesk <command>`
> - Python scripts: `uv run python src/zendesk_skill/scripts/<script>.py`
>
> Never use `python3` or `python` directly - it will fail with `ModuleNotFoundError`.

## Quick Start

```bash
# Test authentication
uv run zendesk me

# Search tickets
uv run zendesk search "status:open priority:urgent"

# Get ticket details
uv run zendesk ticket-details 12345

# Query saved response (path shown in command output)
uv run zendesk query <temp>/zendesk-skill/ticket_details_xxx.json -q comments_slim
```

## Key Concepts

### Save First, Query Later

All API responses are automatically saved to `<temp>/zendesk-skill/` (system temp directory) with:
- **Metadata**: Command, parameters, timestamp, item count
- **Structure**: Auto-extracted schema showing field types
- **Suggested queries**: Command-specific jq queries
- **Data**: Full API response

**Workflow pattern:**
1. Run a command (e.g., `uv run zendesk ticket-details 12345`)
2. Response saved to a JSON file (path shown in output)
3. Use `uv run zendesk query <file> -q <query_name>` to extract specific data
4. Avoid re-fetching - work with stored files

### Why This Matters

Zendesk API responses can be very large (comments with HTML, many custom fields). By saving locally and using jq:
- Context window is preserved (only extract what's needed)
- No redundant API calls
- Complex analysis can use multiple queries on same data

## Command Reference

### Ticket Commands

| Command | Description | Example |
|---------|-------------|---------|
| `search` | Search tickets with query | `uv run zendesk search "status:open"` |
| `ticket` | Get ticket by ID | `uv run zendesk ticket 12345` |
| `ticket-details` | Get ticket + all comments | `uv run zendesk ticket-details 12345` |
| `linked-incidents` | Get incidents linked to problem | `uv run zendesk linked-incidents 12345` |
| `attachment` | Download attachment file | `uv run zendesk attachment --ticket 12345 <url>` |

### Write Operations

All write commands (`create-ticket`, `add-note`, `add-comment`) support **Markdown formatting** by default. Content is converted to HTML for reliable rendering in Zendesk Agent Workspace. Use `--plain-text` to send as plain text instead.

| Command | Description | Example |
|---------|-------------|---------|
| `update-ticket` | Update ticket properties | `uv run zendesk update-ticket 12345 --status pending` |
| `create-ticket` | Create new ticket (Markdown) | `uv run zendesk create-ticket "Subject" "**Bold** description"` |
| `add-note` | Add internal note (Markdown) | `uv run zendesk add-note 12345 "**Investigation:** found the issue"` |
| `add-comment` | Add public comment (Markdown) | `uv run zendesk add-comment 12345 "Here are the steps:\n- Step 1\n- Step 2"` |

### Metrics & Analytics

| Command | Description | Example |
|---------|-------------|---------|
| `ticket-metrics` | Get reply/resolution times | `uv run zendesk ticket-metrics 12345` |
| `list-metrics` | List metrics for tickets | `uv run zendesk list-metrics` |
| `satisfaction-ratings` | List CSAT ratings | `uv run zendesk satisfaction-ratings --score bad` |
| `satisfaction-rating` | Get single rating | `uv run zendesk satisfaction-rating 67890` |

### Views (Queue Management)

| Command | Description | Example |
|---------|-------------|---------|
| `views` | List available views | `uv run zendesk views` |
| `view-count` | Get ticket count | `uv run zendesk view-count 123` |
| `view-tickets` | Get tickets from view | `uv run zendesk view-tickets 123` |

### Users & Organizations

| Command | Description | Example |
|---------|-------------|---------|
| `user` | Get user by ID | `uv run zendesk user 12345` |
| `search-users` | Search users | `uv run zendesk search-users "john@example.com"` |
| `org` | Get organization by ID | `uv run zendesk org 67890` |
| `search-orgs` | Search organizations | `uv run zendesk search-orgs "Acme"` |

### Authentication

| Command | Description | Example |
|---------|-------------|---------|
| `auth login` | Configure Zendesk credentials | `uv run zendesk auth login` |
| `auth status` | Check Zendesk auth configuration | `uv run zendesk auth status` |
| `auth logout` | Remove Zendesk credentials | `uv run zendesk auth logout` |
| `auth login-slack` | Configure Slack webhook | `uv run zendesk auth login-slack` |
| `auth status-slack` | Check Slack configuration | `uv run zendesk auth status-slack` |
| `auth logout-slack` | Remove Slack configuration | `uv run zendesk auth logout-slack` |

### Slack Integration

| Command | Description | Example |
|---------|-------------|---------|
| `slack-report` | Send support report to Slack | `uv run zendesk slack-report [analysis_file]` |
| `markdown-report` | Generate detailed markdown report | `uv run zendesk markdown-report [analysis_file] -o report.md` |

### Configuration

| Command | Description | Example |
|---------|-------------|---------|
| `groups` | List support groups | `uv run zendesk groups` |
| `tags` | List popular tags | `uv run zendesk tags` |
| `sla-policies` | List SLA policies | `uv run zendesk sla-policies` |
| `me` | Get current user (test auth) | `uv run zendesk me` |

### Query Tool

| Command | Description | Example |
|---------|-------------|---------|
| `query` | Query saved JSON with jq | `uv run zendesk query <file> -q comments_slim` |

## Search Query Syntax

The `search` command uses Zendesk's query language:

### Time Filters
- `created>2024-01-01` - Created after date
- `updated<2024-01-15` - Updated before date
- `solved>=2024-01-20` - Solved on or after date
- `created>1week` - Created in last week (relative)

### Status
- `status:open`
- `status:pending`
- `status:solved`
- `status:closed`
- `status<solved` - New, open, or pending

### Priority
- `priority:urgent`
- `priority:high`
- `priority:normal`
- `priority:low`

### Assignment
- `assignee:me` - Assigned to current user
- `assignee:none` - Unassigned
- `assignee_id:12345` - Specific agent
- `group:Support` - Assigned to group

### Tags
- `tags:billing`
- `tags:urgent`
- `tags:vip tags:enterprise` - Multiple tags (AND)

### Type
- `type:incident`
- `type:problem`
- `type:question`
- `type:task`

### People
- `requester:user@example.com`
- `requester_id:12345`
- `organization:acme`
- `submitter:agent@company.com`

### Combinations
```
status:open priority:urgent tags:escalated
status:pending assignee:me updated>1week
type:problem status<solved
requester:*@bigclient.com status:open
```

### Text Search
- `subject:password reset` - Search in subject
- `description:error` - Search in description
- `password reset` - Search anywhere

## Named Queries for jq

After fetching data, use `zendesk query` with these named queries:

### For Ticket Details (`ticket-details`)
| Query | Description |
|-------|-------------|
| `ticket_summary` | Get ticket without comments |
| `comments_slim` | Comments with truncated body (no HTML) |
| `comments_full` | Full comment bodies |
| `attachments` | List all attachments from comments |
| `comment_count` | Count by public/private |
| `latest_comment` | Most recent comment |

### For Search Results (`search`)
| Query | Description |
|-------|-------------|
| `ids_only` | Just ticket IDs |
| `summary_list` | ID, subject, status, priority |
| `by_status` | Group tickets by status |
| `by_priority` | Group by priority |
| `pagination` | Pagination info |

### Custom jq Examples
```bash
# Get specific fields from ticket
uv run zendesk query file.json --jq '.data.ticket | {id, subject, status, tags}'

# Filter comments by author
uv run zendesk query file.json --jq '[.data.comments[] | select(.author_id == 12345)]'

# Get timestamps only
uv run zendesk query file.json --jq '.data.comments | map({created_at, author_id})'
```

### List Available Queries
```bash
uv run zendesk query <file_path> --list
```

## Common Workflows

### Investigate a Ticket

```bash
# 1. Get full ticket details
uv run zendesk ticket-details 12345
# -> Output includes: file_path (e.g., "<temp>/zendesk-skill/12345/ticket_details_xxx.json")

# 2. Get ticket summary (use the file_path from step 1)
uv run zendesk query <file_path> -q ticket_summary

# 3. Get conversation (truncated bodies)
uv run zendesk query <file_path> -q comments_slim

# 4. Check for attachments
uv run zendesk query <file_path> -q attachments
```

### Find Related Tickets

```bash
# Find all open tickets from same requester
uv run zendesk search "requester:user@example.com status:open"

# If it's a problem ticket, find linked incidents
uv run zendesk linked-incidents 12345
```

### Check Queue Health

```bash
# Get available views
uv run zendesk views

# Check ticket count in queue
uv run zendesk view-count 123

# Get tickets to triage
uv run zendesk view-tickets 123
```

### Analyze CSAT

```bash
# Find negative ratings
uv run zendesk satisfaction-ratings --score bad

# Query for details (use file_path from command output)
uv run zendesk query <file_path> --jq '.data.satisfaction_ratings | map({ticket_id, score, comment})'

# Investigate specific case
uv run zendesk ticket-details <ticket_id>
```

### Update Ticket Status

```bash
# Change status and add tag
uv run zendesk update-ticket 12345 --status pending --tags "waiting-customer,tier2"

# Add internal note with Markdown formatting
uv run zendesk add-note 12345 "**Escalated** to tier 2, waiting for response.\n\n- Root cause: config mismatch\n- Next steps: awaiting customer confirmation"

# Add plain text note (no Markdown conversion)
uv run zendesk add-note 12345 "Simple plain text note" --plain-text
```

## Command Options

### Global Options

All commands support:
- `--output PATH` - Custom output file path
- `--help` - Show command help

### Search Options

```bash
uv run zendesk search "query" [OPTIONS]
  --page, -p INT       Page number (default: 1)
  --per-page, -n INT   Results per page (default: 25, max: 100)
  --sort, -s TEXT      Sort field
  --order, -o TEXT     Sort order (asc/desc)
```

### Update Ticket Options

```bash
uv run zendesk update-ticket TICKET_ID [OPTIONS]
  --status, -s TEXT     New status (open, pending, solved, closed)
  --priority, -p TEXT   New priority (low, normal, high, urgent)
  --assignee, -a TEXT   Assignee ID
  --subject TEXT        New subject
  --tags, -t TEXT       Tags (comma-separated)
  --type TEXT           Ticket type
```

### Satisfaction Ratings Options

```bash
uv run zendesk satisfaction-ratings [OPTIONS]
  --score, -s TEXT      Filter: good, bad, offered, unoffered
  --start TEXT          Start time (Unix timestamp)
  --end TEXT            End time (Unix timestamp)
```

### Attachment Options

```bash
uv run zendesk attachment [OPTIONS] URL
  --ticket, -t TEXT     Ticket ID (organizes download under ticket folder)
  --output, -o PATH     Custom output path (overrides --ticket)
```

## File Organization

### Output Path Hierarchy

Output paths are determined in this order:

1. **`--output PATH`** - Full custom path (highest priority)
   ```bash
   uv run zendesk ticket 12345 --output ./my-ticket.json
   ```

2. **`--ticket ID`** - Organizes files under `<temp>/zendesk-skill/{ticket_id}/`
   ```bash
   uv run zendesk attachment --ticket 12345 <url>
   # -> <temp>/zendesk-skill/12345/attachments/filename.png
   ```

3. **Default** - Falls back to `<temp>/zendesk-skill/`

### Ticket-Based Organization

When you use ticket-related commands (`ticket`, `ticket-details`, `ticket-metrics`, etc.), files are automatically organized by ticket ID:

```
<temp>/zendesk-skill/
├── 12345/                          # Ticket 12345
│   ├── ticket_abc123_1234567890.json
│   ├── ticket_details_def456_1234567891.json
│   └── attachments/
│       └── screenshot.png
├── 67890/                          # Ticket 67890
│   └── ticket_details_ghi789_1234567892.json
└── search_xyz_1234567893.json      # Non-ticket commands at root
```

### Duplicate Filename Handling

When downloading attachments, if a file already exists with the same name, a numeric suffix is added:
- `screenshot.png`
- `screenshot_1.png`
- `screenshot_2.png`

## Configuration

### Authentication Setup

You need three values:
- **Email**: Your Zendesk agent email
- **API Token**: Generated in Zendesk Admin Center (not your password!)
- **Subdomain**: First part of your Zendesk URL (e.g., `mycompany` from `mycompany.zendesk.com`)

#### Getting Your Credentials

**Email**: Use the email address you log into Zendesk with.

**Subdomain**: Look at your Zendesk URL:
- If you access `https://acme.zendesk.com`, your subdomain is `acme`
- If you access `https://support.mycompany.com`, ask your admin for the subdomain

**API Token** (requires admin access or help from admin):

1. Log in to Zendesk
2. Click the **Admin Center** icon (gear) in the sidebar
3. Navigate to **Apps and integrations** → **APIs** → **Zendesk API**
4. In the **Settings** tab, ensure **Token Access** is enabled
5. Click **Add API token**
6. Give it a description (e.g., "Claude Code CLI")
7. Click **Copy** immediately - the token is only shown once!

**Don't have admin access?** Ask your Zendesk administrator to:
1. Create an API token for you, OR
2. Grant you admin access to create your own

**Token not working?** Common issues:
- Using your password instead of the API token
- Token Access is disabled in Zendesk settings
- Your account doesn't have API access permissions

#### Option A: Interactive Setup (recommended)

```bash
uv run zendesk auth login
# Prompts for email, token (hidden), and subdomain
```

#### Option B: Non-Interactive Setup (for automation)

```bash
uv run zendesk auth login --email "your@email.com" --token "your-token" --subdomain "yourcompany"
```

#### Option C: Environment Variables

```bash
export ZENDESK_EMAIL="your-email@company.com"
export ZENDESK_TOKEN="your-api-token"
export ZENDESK_SUBDOMAIN="yourcompany"
```

#### Option D: Config File (manual)

Create `~/.claude/.zendesk-skill/config.json`:
```json
{
  "email": "your-email@company.com",
  "token": "your-api-token",
  "subdomain": "yourcompany"
}
```

Secure the file:
```bash
chmod 600 ~/.claude/.zendesk-skill/config.json
```

#### Check Auth Status

```bash
uv run zendesk auth status
```

#### Verify Auth Works

```bash
uv run zendesk me
```

#### Remove Saved Credentials

```bash
uv run zendesk auth logout
```

## Notes for Claude Code Users

### Interactive Authentication

The `zendesk auth login` command supports both interactive and non-interactive modes:

- **Interactive mode**: Prompts for credentials securely (password hidden). This requires running in the user's terminal.
- **Non-interactive mode**: Pass credentials via flags for automation:
  ```bash
  uv run zendesk auth login --email "you@example.com" --token "your-token" --subdomain "company"
  ```

### When Auth Is Not Configured

If credentials are not configured, commands will fail with a helpful error message. The `zendesk auth status` command provides detailed guidance:

```bash
uv run zendesk auth status
```

If not configured, it will show:
- Which environment variables are set (if any)
- Whether a config file exists
- Setup instructions for all authentication methods

### Proactive Auth Check

Before running Zendesk commands for a user, it's helpful to verify auth status first:

```bash
# Quick auth check
uv run zendesk auth status

# If configured, test it works
uv run zendesk me
```

## Slack Integration

### Setup

Configure Slack to receive support reports:

```bash
# Interactive mode
uv run zendesk auth login-slack

# Non-interactive mode
uv run zendesk auth login-slack --webhook "https://hooks.slack.com/services/..." --channel "#support-reports"
```

**Getting a Webhook URL:**
1. Go to your Slack workspace settings
2. Navigate to **Apps** → **Incoming Webhooks** (or create a new app)
3. Create a new webhook and copy the URL
4. The URL format: `https://hooks.slack.com/services/T.../B.../...`

### Sending Reports

```bash
# Send most recent analysis to configured channel
uv run zendesk slack-report

# Send specific analysis file
uv run zendesk slack-report /path/to/support_analysis.json

# Override channel
uv run zendesk slack-report --channel "#different-channel"
```

### Report Content

The Slack report includes:
- **Overview**: Total tickets, messages, calls detected, unique customers
- **Response Metrics**: Average/median FRT, resolution time (when available)
- **Status Breakdown**: Open, pending, solved, closed counts with icons
- **Priority Breakdown**: Urgent, high, normal, low counts with icons
- **Customer Stats**: Tickets and messages per customer (by email domain)
- **Top Tickets**: Most active tickets by message count with call indicators

Note: Calls are detected on a best-effort basis by searching comment text for keywords like "call", "called", "phone", etc.

### Environment Variables

Alternatively, configure via environment variables:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export SLACK_CHANNEL="#support-reports"
```

## Support Analytics Workflow

### Support Metrics Report

Generate a comprehensive support report with tickets per customer, messages per ticket, and call detection. **Default period is 2 weeks** unless otherwise specified:

```bash
# 1. Search for tickets in time range
uv run zendesk search "created>2024-12-22 created<2025-01-22"

# 2. Get ticket details for each result (for message analysis)
for ticket_id in $(uv run zendesk query <search_file> -q ids_only | jq -r '.[]'); do
  uv run zendesk ticket-details $ticket_id
done

# 3. Run analysis queries on stored data
uv run zendesk query <ticket_details_file> -q conversation_stats
uv run zendesk query <ticket_details_file> -q call_mentions
uv run zendesk query <search_file> -q by_requester
```

### Available Analytics Queries

**Search Results** (`search`):
| Query | Description |
|-------|-------------|
| `by_requester` | Group tickets by requester with counts |
| `by_organization` | Group tickets by organization |
| `top_requesters` | Top 10 requesters by ticket count |
| `top_organizations` | Top 10 organizations by ticket count |

**Ticket Details** (`ticket-details`):
| Query | Description |
|-------|-------------|
| `messages_by_author` | Count messages per author |
| `conversation_stats` | Total messages, public/private, unique authors |
| `call_mentions` | Find comments mentioning calls/phone* |
| `channel_analysis` | Analyze communication channels |

*Note: Calls are detected on a best-effort basis by searching comment text for keywords like "call", "called", "phone", "spoke", etc.

**Ticket Metrics** (`ticket-metrics`):
| Query | Description |
|-------|-------------|
| `kpi_summary` | FRT, resolution times, wait times, reopens |
| `times` | All time-based metrics (calendar & business) |
| `efficiency` | Reopens, replies, stations |

**List Metrics** (`list-metrics`):
| Query | Description |
|-------|-------------|
| `frt_summary` | First reply time across tickets |
| `avg_frt` | Average FRT with min/max |
| `resolution_summary` | Resolution times across tickets |
| `reopen_rate` | Tickets with reopens (FCR issues) |

### Customer Identification

Customers are identified by:
1. **Organization** - If `organization_id` is set on the user
2. **Email domain** - Fallback when no organization is set

To get organization info:
```bash
# Get user with organization
uv run zendesk user <user_id>

# Get organization details
uv run zendesk org <org_id>
```

### Python Analysis Script

For comprehensive analysis, use the included script:

```bash
# Default: 2-week period ending today
uv run python src/zendesk_skill/scripts/analyze_support_metrics.py [search_file]

# Explicit period
uv run python src/zendesk_skill/scripts/analyze_support_metrics.py search.json --start 2026-01-09 --end 2026-01-23
```

**Options:**
- `--start DATE` - Period start date (YYYY-MM-DD). Default: 14 days ago
- `--end DATE` - Period end date (YYYY-MM-DD). Default: today
- `--output DIR` - Output directory

This generates:
- Tickets per customer (by email domain)
- Messages per customer
- Messages per ticket
- Call detection results
- FRT and resolution statistics
- Status and priority breakdown
- JSON output at `<temp>/zendesk-skill/support_analysis.json`

## Tips

1. **Don't hallucinate dates**: When constructing date-based queries, verify the current date first:
   ```bash
   date +%Y-%m-%d
   ```
2. **Always check file paths**: Command output includes the saved file path - use it for follow-up queries
2. **Use named queries first**: They're optimized for common patterns
3. **Combine queries**: Run multiple jq queries on same file for different views
4. **Watch for pagination**: Search results may have more pages - check `next_page` in output
5. **Test auth first**: Use `uv run zendesk me` to verify credentials work
6. **Use --help**: All commands have detailed help: `uv run zendesk search --help`

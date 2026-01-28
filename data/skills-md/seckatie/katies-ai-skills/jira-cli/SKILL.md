---
name: jira-cli
description: Manage Jira tickets from the command line using jira-cli. Contains essential setup instructions, non-interactive command patterns with required flags (--plain, --raw, etc.), authentication troubleshooting, and comprehensive command reference. This skill is triggered when the user says things like "create a Jira ticket", "list my Jira issues", "update Jira issue", "move Jira ticket to done", "log time in Jira", "add comment to Jira", or "search Jira issues". IMPORTANT - Read this skill before running any jira-cli commands to avoid blocking in interactive mode.
---

# Jira CLI Setup and Usage

This skill provides instructions for installing and using the Jira CLI tool to interact with Jira from the command line.

## Quick Reference: Common Pitfalls to Avoid

Before diving into detailed commands, be aware of these critical points:

1. **Time Tracking**: MUST use `jira issue worklog add ISSUE "1m" --new-estimate "1h"` - DO NOT use `--custom` for time tracking
2. **Cannot log 0m**: Logging "0m" causes server errors - always log at least "1m"
3. **Status Names Vary**: "Done" may not exist - use exact status name from error message (e.g., "Resolved", "Closed")
4. **--no-input Support**: Not all commands support `--no-input`:
   - ✓ Supported: `issue edit`, `issue worklog add`
   - ✗ Not supported: `issue move`, view/list commands
5. **Environment Setup**: Test `jira me --plain` first - only source ~/.envrc if auth fails

## CRITICAL: Environment Setup

**Before running any jira-cli commands, check if the user has already configured their environment.**

The user may have already:
- Installed and configured jira-cli
- Set up authentication tokens in environment files (e.g., `~/.envrc`, `~/.bashrc`, `~/.zshrc`)
- Configured the Jira CLI in `~/.config/.jira/.config.yml`
- Exported `JIRA_API_TOKEN` in their current shell session

**Test if jira-cli is already working before sourcing environment files:**

```bash
# First, try running jira-cli directly
jira me --plain

# If you get authentication errors, THEN check for environment files
```

**Only source environment files if authentication fails:**

```bash
# If needed, check for and source .envrc conditionally
[ -f ~/.envrc ] && source ~/.envrc 2>/dev/null; jira me --plain
```

**Why this approach:**
- The `JIRA_API_TOKEN` environment variable is required for authentication
- Users may have already sourced their environment files in the current shell
- Users may have tokens configured globally in their shell configuration
- **Do not assume ~/.envrc needs to be sourced** - only do so if authentication fails
- The user may have already completed the full setup, so test first before suggesting changes

**Troubleshooting steps if commands fail:**
1. First try running jira commands directly (e.g., `jira me --plain`)
2. If authentication fails, check if `JIRA_API_TOKEN` is set: `echo $JIRA_API_TOKEN`
3. If not set, then try sourcing common environment files like `~/.envrc`
4. Only suggest installation/configuration if the tool is not found or environment variables cannot be located

## IMPORTANT: Preventing Interactive Mode Blocking

**ALWAYS use `--plain` flag (or equivalent non-interactive flags) when running jira-cli commands to prevent the tool from entering interactive mode and blocking execution.**

### Non-Interactive Flags by Command Type

**For listing/viewing commands:**
- Use `--plain` to get plain text output instead of interactive UI
- Alternative non-interactive flags: `--raw` (JSON output), `--csv` (CSV output)

**For commands that prompt for input (create, edit, worklog):**
- Use `--no-input` to skip interactive prompts
- **Commands that support `--no-input`:**
  - `jira issue edit` - skips prompts for fields
  - `jira issue worklog add` - skips comment prompt
  - Other create/edit commands
- **Commands that DO NOT support `--no-input`:**
  - `jira issue move` - does not have this flag
  - Most viewing/listing commands (use `--plain` instead)

**Important:**
- If a command doesn't support `--no-input`, provide all required parameters via flags
- If you get "unknown flag: --no-input" error, remove the flag and provide inputs via other flags
- Always check error messages for available flags

Examples:
```bash
# CORRECT - Non-blocking list commands
jira issue list --plain
jira issue list --raw
jira epic list --plain

# CORRECT - Non-blocking edit/worklog commands
jira issue edit PROJ-123 --custom "field=value" --no-input
jira issue worklog add PROJ-123 "1h" --no-input

# CORRECT - Move command (no --no-input flag)
jira issue move PROJ-123 "In Progress"

# INCORRECT - May block in interactive UI
jira issue list
jira epic list
jira issue worklog add PROJ-123 "1h"  # Will prompt for comment
```

## Installation

### macOS (via Homebrew)

```bash
brew install jira-cli
```

### Linux

Download the latest release from GitHub:

```bash
# For amd64
wget https://github.com/ankitpokhrel/jira-cli/releases/latest/download/jira_linux_amd64.tar.gz
tar -xzf jira_linux_amd64.tar.gz
sudo mv jira /usr/local/bin/
```

### Windows

Download from the [releases page](https://github.com/ankitpokhrel/jira-cli/releases) or use Scoop:

```bash
scoop install jira-cli
```

### Docker

```bash
docker run -it --rm ghcr.io/ankitpokhrel/jira-cli:latest
```

### Other Package Managers

Jira CLI is also available via Nix and other package managers. See [Repology](https://repology.org/project/jira-cli/versions) for a full list.

## Configuration

### Cloud Server Setup

1. Generate a Jira API token at: https://id.atlassian.com/manage-profile/security/api-tokens
2. Export the token as an environment variable:
   ```bash
   export JIRA_API_TOKEN="your-token-here"
   ```
   **Note**: If environment variables are stored in `~/.envrc`, you may need to source them first:
   ```bash
   source ~/.envrc
   ```
3. Run `jira init` and select "Cloud" installation type
4. Provide your Jira instance URL (e.g., `https://your-company.atlassian.net`)

### On-Premise Installation

1. Export authentication credentials:
   ```bash
   export JIRA_API_TOKEN="your-token-here"
   ```
2. For Personal Access Token (PAT) authentication:
   ```bash
   export JIRA_AUTH_TYPE="bearer"
   ```
3. Run `jira init` and select "Local" installation type
4. For non-English installations, manually configure `epic.name`, `epic.link`, and `issue.types.*.handle` in the config file

### Authentication Methods

Jira CLI supports three authentication types:

- **Basic** (default): Username and password or API token
- **Bearer (PAT)**: Personal Access Token authentication (requires `JIRA_AUTH_TYPE=bearer`)
- **mTLS**: Client certificate authentication for on-premise installations

### Multiple Project Support

Use the `--config/-c` flag or `JIRA_CONFIG_FILE` environment variable to load specific configurations:

```bash
jira issue list --config ~/.config/jira/project2.yml
# or
export JIRA_CONFIG_FILE=~/.config/jira/project2.yml
jira issue list
```

### Configuration File

The configuration is stored in `~/.config/.jira/.config.yml`. You can edit this file directly.

## Common Commands

### List Issues

```bash
# List issues assigned to you
jira issue list

# List issues with filters
jira issue list -a$(jira me) -s"To Do,In Progress"

# List issues in a specific project
jira issue list --project PROJ

# List with JQL query
jira issue list --jql "assignee=currentUser() AND status='In Progress'"

# Filter by time (relative dates supported)
jira issue list --created -7d    # Created in last 7 days
jira issue list --created week   # Created this week
jira issue list --updated month  # Updated this month

# Filter by priority, labels, components
jira issue list --priority High,Highest
jira issue list --label bug,urgent
jira issue list --component backend
```

### View Issue Details

```bash
# View issue details
jira issue view PROJ-123

# View with comments
jira issue view PROJ-123 --comments 10
```

### Create Issues

```bash
# Interactive mode
jira issue create

# Quick create with flags
jira issue create -tTask -s"Issue summary" -y10 -lbug,urgent

# Create from template
jira issue create --template

# Create with custom fields
jira issue create --custom field1=value1,field2=value2

# Create with parent epic
jira issue create -P PROJ-456
```

### Update Issues

```bash
# Assign issue
jira issue assign PROJ-123 $(jira me)

# Assign to default assignee
jira issue assign PROJ-123 default

# Unassign
jira issue assign PROJ-123 x

# Move to different status (transition)
jira issue move PROJ-123 "In Progress"

# IMPORTANT: Status names vary by project/workflow
# If you get "invalid transition state" error, the status name is incorrect
# Common mistake: Using "Done" when the actual state is "Resolved" or "Closed"
# The error message will list available states for that issue

# Edit issue
jira issue edit PROJ-123

# Edit with specific fields
jira issue edit PROJ-123 -s"New summary" --priority High

# Remove labels (use minus prefix)
jira issue edit PROJ-123 --label -p2
```

### Clone Issues

```bash
# Clone an issue
jira issue clone PROJ-123

# Clone with modifications
jira issue clone PROJ-123 -s"New summary" --priority High

# Clone with text replacement
jira issue clone PROJ-123 -H old:new
```

### Link and Unlink Issues

```bash
# Link issues
jira issue link PROJ-123 PROJ-456 "Blocks"

# Unlink issues
jira issue unlink PROJ-123 PROJ-456

# Add web link
jira issue link PROJ-123 https://example.com "Documentation"
```

### Delete Issues

```bash
# Delete an issue
jira issue delete PROJ-123

# Delete with cascade (including subtasks)
jira issue delete PROJ-123 --cascade
```

### Comment Management

```bash
# Add comment
jira issue comment add PROJ-123 "Working on this"

# Add internal comment
jira issue comment add PROJ-123 --internal "Internal note"

# Add comment from file
jira issue comment add PROJ-123 --template comment.md

# Add comment from stdin
echo "Comment text" | jira issue comment add PROJ-123
```

### Worklog and Time Tracking

**IMPORTANT**: Time tracking estimates are set using the `worklog add` command with the `--new-estimate` flag, NOT through custom fields.

```bash
# Add time tracking entry
jira issue worklog add PROJ-123 "2d 3h 30m"

# Add worklog with comment
jira issue worklog add PROJ-123 "4h" --comment "Fixed the bug"

# Set remaining estimate when logging work
jira issue worklog add PROJ-123 "1h" --new-estimate "3h"

# Set original estimate (log minimal time with full estimate remaining)
jira issue worklog add PROJ-123 "1m" --new-estimate "8h"

# Complete work and set remaining to 0
jira issue worklog add PROJ-123 "30m" --new-estimate "0m"

# Use --no-input to skip interactive comment prompt
jira issue worklog add PROJ-123 "1h" --new-estimate "2h" --no-input

# Add worklog with start time
jira issue worklog add PROJ-123 "1h 30m" --started "2022-01-01T09:30:00.000+0200" --new-estimate "0h"
```

**Important notes for worklog:**
- **Cannot log "0m" of time** - This causes a server error. Log at least "1m" if you need to set an estimate without logging significant work
- Use `--new-estimate` to set the remaining time estimate
- The `--no-input` flag is supported and prevents interactive prompts for comments
- Time formats: "1h", "30m", "1h 30m", "2d 3h 30m"
- Time tracking cannot be set through `--custom` fields - you must use `worklog add` with `--new-estimate`

### Search Issues

```bash
# Search with JQL
jira issue list --jql "project=PROJ AND status='In Progress' ORDER BY priority DESC"

# Common JQL examples
jira issue list --jql "assignee=currentUser() AND status!=Done"
jira issue list --jql "created >= -7d AND assignee=currentUser()"
jira issue list --jql "priority in (High, Highest) AND status='To Do'"
```

### Epic Management

```bash
# List epics
jira epic list

# List epics in table view
jira epic list --table

# View issues in a specific epic
jira epic list PROJ-123

# Create epic
jira epic create

# Add issues to epic (up to 50 at a time)
jira epic add PROJ-123 PROJ-456 PROJ-789

# Remove issues from epic
jira epic remove PROJ-123 PROJ-456
```

### Sprint Management

```bash
# List sprints (shows 25 most recent)
jira sprint list

# List issues in current sprint
jira sprint list --current

# List issues in previous/next sprint
jira sprint list --prev
jira sprint list --next

# Filter by sprint state
jira sprint list --state future,active

# Add issue to sprint (up to 50 at a time)
jira sprint add SPRINT-ID PROJ-123 PROJ-456
```

### Project and Board Management

```bash
# List accessible projects
jira project list

# List boards
jira board list

# List releases/versions
jira release list
```

### Utility Commands

```bash
# Open project or issue in browser
jira open
jira open PROJ-123

# Get current user information
jira me

# Enable shell completion
jira completion bash > /etc/bash_completion.d/jira
jira completion zsh > "${fpath[1]}/_jira"
```

## Output Formats

Jira CLI supports multiple output formats:

```bash
# Default interactive table view
jira issue list

# Plain text (for scripting)
jira issue list --plain

# Raw JSON output
jira issue list --raw

# CSV format
jira issue list --csv

# No headers (with plain output)
jira issue list --plain --no-headers
```

## Interactive UI Navigation

The default list view supports keyboard navigation:

- **Arrow keys** or **j/k/h/l**: Navigate up/down/left/right
- **g/G**: Jump to top/bottom
- **CTRL+f/b**: Page down/up
- **v**: View issue details
- **m**: Transition/move issue to different status
- **ENTER**: Open issue in browser
- **c**: Copy issue URL to clipboard
- **CTRL+k**: Copy issue key to clipboard
- **w** or **TAB**: Toggle sidebar focus
- **CTRL+r** or **F5**: Refresh list
- **?**: Display help

## Useful Aliases

Add these to your shell configuration for quicker access:

```bash
# List your current issues
alias jira-mine='jira issue list -a$(jira me) -s"To Do,In Progress"'

# Quick view
alias jv='jira issue view'

# List current sprint
alias jira-sprint='jira sprint list --current'

# Open issue quickly
alias jo='jira open'
```

## Advanced Usage

### Custom Views

Create custom issue views in `~/.config/jira/.config.yml`:

```yaml
issue:
  fields:
    - key
    - type
    - summary
    - status
    - assignee
    - priority
    - created
```

### Custom Fields

Configure custom field mapping in `~/.config/jira/.config.yml`:

```yaml
custom:
  customfield_10001: Team
  customfield_10002: Story Points
```

Then use them in commands:

```bash
jira issue create --custom Team=Backend,Story\ Points=5
```

### Setting Due Dates

**CRITICAL DISTINCTION**: Do not confuse **due dates** with **time tracking**:
- **Due dates** (calendar dates): Set via `--custom` parameter (requires configuration)
- **Time tracking** (estimates/time spent): Set via `jira issue worklog add` with `--new-estimate` flag
- **Never** try to set time tracking fields (`timeoriginalestimate`, `timetracking`, etc.) via `--custom` - it will not work

**IMPORTANT**: The `duedate` field is treated as a custom field and must be explicitly configured to be visible in API responses and usable via the `--custom` parameter.

#### Configuration Required for Due Dates

Due dates require special configuration because `duedate` is a standard Jira field that doesn't appear by default in the Jira CLI API responses. To enable setting and viewing due dates:

1. Add the following to your `~/.config/jira/.config.yml`:

```yaml
issue:
  fields:
    custom:
      - name: duedate
        key: duedate
        schema:
          datatype: date
```

2. Then you can set due dates when creating or editing issues:

```bash
jira issue create --type Task --summary "Task summary" --custom "duedate=2024-12-31"
jira issue edit PROJ-123 --custom "duedate=2024-12-31"
```

#### Requesting Due Dates in API Responses

**Without the above configuration**:
- The `duedate` field will NOT appear in `jira issue list --raw` output
- Attempts to use `--custom "duedate=..."` will show a warning that the field is "not configured" and will be ignored
- Due dates cannot be set or retrieved via the CLI

**With the configuration**:
- Due dates will appear in the `fields` object of JSON responses from `--raw` output
- You can set due dates using the `--custom` parameter
- Due dates can be included in custom views

**Note**: This is a known limitation of the jira-cli tool. See [jira-cli issue #698](https://github.com/ankitpokhrel/jira-cli/issues/698) for more details.

### Scripting with Jira CLI

Use raw JSON output for scripting:

```bash
#!/bin/bash
# Get all high priority issues
jira issue list --jql "priority=High" --raw | jq -r '.issues[].key'

# Count issues by status
jira issue list --plain --no-headers | awk '{print $4}' | sort | uniq -c
```

### Templates

Create markdown templates for issues and comments:

```bash
# Issue template (issue-template.md)
## Description
What needs to be done?

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

# Use template
jira issue create --template issue-template.md
```

## Troubleshooting

### Authentication Issues

```bash
# Re-initialize configuration
jira init --force

# Check current user
jira me

# Verify API token is set
echo $JIRA_API_TOKEN
```

### Connection Issues

```bash
# Test connection
jira issue list --limit 1

# Enable debug mode
JIRA_DEBUG=1 jira issue list
```

### Clear Cache

```bash
# Clear cached data
rm -rf ~/.config/jira/.cache
```

### Time Tracking Errors

**Error: "field not on the appropriate screen"**
- This occurs when trying to set time tracking via `--custom` fields
- **Solution**: Use `jira issue worklog add` with `--new-estimate` instead
- Time tracking fields cannot be set via the edit command

**Error: "Internal server error" (500) when logging time**
- Usually caused by trying to log "0m" of time
- **Solution**: Log at least "1m" - you cannot log zero time
- Example: `jira issue worklog add PROJ-123 "1m" --new-estimate "8h"`

**Warning: "field is not configured" for timeoriginalestimate/timetracking**
- This appears when using `--custom` for time tracking fields
- **Solution**: Ignore the warning - use `worklog add` command instead
- Do NOT try to configure these as custom fields - they're managed differently

**Error: "invalid transition state" when closing issues**
- Status names vary by project/workflow
- Common mistake: Using "Done" when the actual state is "Resolved" or "Closed"
- **Solution**: Check the error message for available states
- Or view the issue in browser: `jira open PROJ-123`

## Resources

- [Official Documentation](https://github.com/ankitpokhrel/jira-cli)
- [JQL Guide](https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-searching-in-jira-cloud/)
- [Issue with installation or usage?](https://github.com/ankitpokhrel/jira-cli/issues)

## Notes

- The Jira CLI uses the Jira REST API under the hood
- API tokens are more secure than passwords and are the recommended authentication method
- Most commands support `--help` for detailed usage information
- Supports both Jira Cloud and on-premise installations
- Output is converted from Atlassian Document Format to markdown for better terminal display

---
name: jira-ticket-creator
description: Create Jira tickets using jira-cli (https://github.com/ankitpokhrel/jira-cli). Use when the user asks to create Jira tickets, issues, or stories with work types (Epic/Story/Bug/A/B Test), set to Backlog status. Selects the most appropriate component from API/Projects/Proposals/Backends/Regression/AI using the -C flag. Returns the ticket URL after creation. Assumes jira-cli is already installed and configured (user has run 'jira init').
---

# Jira Ticket Creator

Create Jira tickets non-interactively using the jira-cli tool.

## Prerequisites

Before using this skill, ensure:
- jira-cli is installed: `brew install jira-cli` or download from [releases](https://github.com/ankitpokhrel/jira-cli/releases)
- Authentication is configured: User has run `jira init` and set up API token
- User has access to the target Jira project

## Available Components

Select the most appropriate component based on the ticket content:

- **API**: REST API endpoints, API design, external integrations
- **Projects**: Project-related features, project management functionality
- **Proposals**: Proposal features, proposal workflows
- **Backends**: Backend services, database, server-side logic, caching, performance
- **Regression**: Bug fixes, regression issues, quality assurance
- **AI**: AI/ML features, intelligent automation, ChatGPT integrations

**Selection Examples:**
- "Optimize query performance with Redis caching" → Backends
- "Add ChatGPT integration" → AI
- "Create project REST API" → API
- "Fix login bug on Safari" → Regression
- "Add proposal approval workflow" → Proposals
- "Implement project dashboard" → Projects

## Quick Start

To create a Jira ticket, use the jira-cli command with the following pattern:

```bash
jira issue create \
  -t<TYPE> \
  -s"<SUMMARY>" \
  -b"<DESCRIPTION>" \
  -C <COMPONENT> \
  --no-input
```

**Example:**
```bash
jira issue create \
  -tStory \
  -s"Optimize project query performance with Redis caching" \
  -b"Implement batch processing and Redis caching for project queries" \
  -C Backends \
  --no-input
```

### Supported Work Types

- `Epic` - For large initiatives or themes
- `Story` - For user stories and features
- `Bug` - For defects and issues
- `A/B Test` - For A/B testing tasks (if configured in your Jira instance)

## Creating Tickets

### Basic Ticket Creation

For standard ticket creation without a parent epic:

```bash
jira issue create \
  -tStory \
  -s"Add user authentication" \
  -b"Implement JWT-based authentication for API endpoints" \
  -C API \
  --no-input
```

### Ticket with Parent Epic

To link a story/bug to an epic, use the `-P` flag:

```bash
jira issue create \
  -tStory \
  -s"Update project dashboard UI" \
  -b"Modernize the project dashboard design" \
  -P PROJ-123 \
  -C Projects \
  --no-input
```

### Epic Creation

```bash
jira issue create \
  -tEpic \
  -s"Q1 2024 AI Integration Initiative" \
  -b"Integrate AI capabilities across the platform" \
  -C AI \
  --no-input
```

### Bug Creation

```bash
jira issue create \
  -tBug \
  -s"Login fails on Safari" \
  -b"Users cannot log in when using Safari browser on macOS. Error message: 'Invalid credentials'" \
  -C Regression \
  --no-input
```

## Setting Status to Backlog

**Important**: Jira typically creates issues in the default initial status (usually "To Do" or "Open"). To move a newly created ticket to "Backlog" status:

### Two-Step Process

```bash
# Step 1: Create the ticket and capture the issue key
ISSUE_KEY=$(jira issue create -tStory -s"Summary" -b"Description" \
  -C Backends --no-input | grep -oE '[A-Z]+-[0-9]+' | head -1)

# Step 2: Move to Backlog status
jira issue move "$ISSUE_KEY" "Backlog"
```

### Alternative: Configure Default Status

Ask the Jira administrator to set "Backlog" as the default initial status for the project, eliminating the need for the move step.

## Getting the Ticket URL

After creating a ticket, jira-cli outputs the issue key (e.g., `PROJ-123`). To get the full URL:

### Method 1: Open in Browser
```bash
jira open PROJ-123
```

### Method 2: View Issue Details
```bash
jira issue view PROJ-123
```
The output includes the issue URL.

### Method 3: Construct URL Manually
If you know your Jira domain:
```
https://your-domain.atlassian.net/browse/PROJ-123
```

### Method 4: Copy from CLI
When viewing issues in the interactive list:
- Press `ENTER` to open in browser
- Press `c` to copy URL to clipboard

## Helper Script

For complex workflows, you can create a helper script if needed:

```bash
#!/bin/bash
# create_jira_ticket.sh
TYPE=$1
SUMMARY=$2
DESCRIPTION=$3
COMPONENT=$4

jira issue create \
  -t"$TYPE" \
  -s"$SUMMARY" \
  -b"$DESCRIPTION" \
  -C "$COMPONENT" \
  --no-input
```

Usage:
```bash
./create_jira_ticket.sh Story "Add authentication" "Implement JWT auth" API
```

## Complete Workflow Example

Create a ticket with all required fields and get the URL:

```bash
# Step 1: Create the ticket (select appropriate component based on the task)
OUTPUT=$(jira issue create \
  -tStory \
  -s"Implement project dashboard" \
  -b"Create a dashboard showing project metrics and recent activity" \
  -C Projects \
  --no-input)

# Step 2: Extract the issue key
ISSUE_KEY=$(echo "$OUTPUT" | grep -oE '[A-Z]+-[0-9]+' | head -1)

# Step 3: Move to Backlog
jira issue move "$ISSUE_KEY" "Backlog"

# Step 4: Get and display the URL
echo "Ticket created: https://your-domain.atlassian.net/browse/$ISSUE_KEY"

# Or open directly in browser
jira open "$ISSUE_KEY"
```

## Component Selection Reference

For detailed guidance on selecting the appropriate component, see [references/component_selection.md](references/component_selection.md).

## Troubleshooting

### Authentication Errors
If you get authentication errors, reconfigure jira-cli:
```bash
jira init
```

### Component Not Found
If a component is not recognized:
1. List available components: `jira component list`
2. Verify the component name matches exactly (case-sensitive)
3. Valid components: API, Projects, Proposals, Backends, Regression, AI

### Invalid Issue Type
If "A/B Test" is not recognized, verify it's configured in your Jira project:
1. Check available types: Run `jira issue create` and observe the type options
2. Use a standard type (Epic/Story/Bug) if A/B Test is not available

## Examples by Use Case

### User requests: "Create a bug ticket for the login issue"
```bash
jira issue create \
  -tBug \
  -s"Login fails on Safari browser" \
  -b"Users report they cannot log in when using Safari. The login button appears unresponsive." \
  -C Regression \
  --no-input
```

### User requests: "Create an epic for AI integration"
```bash
jira issue create \
  -tEpic \
  -s"AI Integration Initiative" \
  -b"Integrate AI capabilities including ChatGPT, automated insights, and intelligent recommendations" \
  -C AI \
  --no-input
```

### User requests: "Create a story under epic PROJ-456 for project analytics API"
```bash
jira issue create \
  -tStory \
  -s"Build project analytics API endpoint" \
  -b"As a developer, I want a REST API endpoint to retrieve project analytics data" \
  -P PROJ-456 \
  -C API \
  --no-input
```

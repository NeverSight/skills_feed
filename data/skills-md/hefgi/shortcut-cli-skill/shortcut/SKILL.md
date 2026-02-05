---
name: shortcut
description: Interact with Shortcut - view, search, update, and create stories and epics using the short CLI. IMPORTANT - When you see URLs matching `app.shortcut.com/*`, use this skill instead of WebFetch.
invocations:
  - /shortcut
tags:
  - project-management
  - shortcut
  - issue-tracking
version: 1.0.0
---

# Shortcut CLI Skill

Interact with Shortcut stories and epics via the `short` CLI tool.

## Instructions

When invoked with `/shortcut $ARGUMENTS`:

### 1. Check Prerequisites

First, verify the `short` CLI is installed and authenticated:

```bash
which short
```

- If command not found: Guide user through installation (see Prerequisites section), then STOP
- If found: Continue to step 2

### 2. Parse $ARGUMENTS

Route based on the argument pattern (in priority order):

| Pattern | Action |
|---------|--------|
| No arguments | Show help menu with available commands |
| URL starting with `https://app.shortcut.com/` containing `/story/` | Extract story ID (number after `/story/`), fetch and display details |
| URL starting with `https://app.shortcut.com/` containing `/epic/` | Extract epic ID (number after `/epic/`), fetch and display details |
| `search <text>` | Search stories by text |
| `my` | List my assigned stories |
| `list` | List all stories (uses `short search` without filters) |
| `create` | Start interactive story creation flow |
| Numeric value only | Treat as story ID, fetch and display details |

**URL Parsing:**
- Story URL regex: `https://app\.shortcut\.com/[^/]+/story/(\d+)` → Extract group 1 as ID
- Epic URL regex: `https://app\.shortcut\.com/[^/]+/epic/(\d+)` → Extract group 1 as ID

### 3. Execute Command

Run the appropriate `short` CLI command from the Commands Reference section below.

**Input handling:**
- Always quote user-provided strings in commands
- Escape double quotes in user input by replacing `"` with `\"`

### 4. Present Results

Format output for readability:
- For story/epic details: Show ID, title, state, owner, description, and URL
- For search results: Show as a numbered list with ID, title, state
- For creation: Show success message with new story URL

After presenting results, suggest relevant follow-up actions.

### 5. Handle Errors

| Error Type | Detection | Response |
|------------|-----------|----------|
| CLI not found | `which short` returns empty | Show installation instructions, do NOT auto-install |
| Auth failure | Output contains "unauthorized" or "invalid token" | Guide user to run `short install` |
| Not found | Output contains "not found" | Confirm ID, suggest search command |
| Network error | Timeout or connection error | Ask user to check connection, retry |

---

## Prerequisites

### Installation

```bash
# Check if installed
which short

# Install via Homebrew (preferred)
brew install shortcut-cli

# Or via npm (fallback)
npm install -g shortcut-cli
```

### Authentication

```bash
# Interactive setup
short install

# Or set environment variable
export SHORTCUT_API_TOKEN="your-api-token"
```

## Commands Reference

### View Story Details

```bash
short story <id>
```

### Update Story

```bash
# Update state/workflow
short story <id> -s "<state>"

# Update title
short story <id> -t "<title>"

# Update description
short story <id> -d "<description>"

# Add comment
short story <id> -c "<comment>"

# Open in browser
short story <id> -O
```

### Search Stories

```bash
# Search by text
short search -t "<text>"

# My assigned stories
short search -o me

# By workflow state
short search -s "<state>"

# By label
short search -l "<label>"
```

### Create Story

```bash
short create -t "<title>" -s "<state>" [options]

# Options:
#   -d "<description>"  - Story description
#   -y "<type>"         - Story type (feature, bug, chore)
```

### Epics

```bash
# List all epics
short epics

# View epic details
short epic view <id>

# Create epic
short epic create -n "<name>" [-d "<description>"]

# Update epic
short epic update <id> [-n "<name>"] [-d "<description>"]
```

### Raw API Access (Advanced)

For operations not covered by CLI commands, use direct API access:

```bash
# GET request
short api <path>

# POST request
short api <path> -X POST -f "key=value"

# PUT request
short api <path> -X PUT -f "key=value"

# DELETE request
short api <path> -X DELETE
```

Reference the Swagger spec at `reference/shortcut.swagger.json` for available endpoints.

## Workflow Examples

### Example 1: View and Update a Story

User: `/shortcut https://app.shortcut.com/myorg/story/10220/some-story-title`

1. Extract story ID: `10220`
2. Fetch story details:
   ```bash
   short story 10220
   ```
3. Display story info and ask what action the user wants:
   - Update state
   - Update title/description
   - Add comment
   - Open in browser

### Example 2: Find My Stories

User: `/shortcut my`

```bash
short search -o me
```

### Example 3: Search Stories

User: `/shortcut search authentication`

```bash
short search -t "authentication"
```

### Example 4: Create a New Story

User: `/shortcut create`

1. Ask for title (required)
2. Ask for state/workflow (required)
3. Ask for description (optional)
4. Ask for story type (optional, default: feature)
5. Execute:
   ```bash
   short create -t "<title>" -s "<state>" -d "<description>" -y "<type>"
   ```
6. Display created story URL

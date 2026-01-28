---
name: canifi
description: Core LifeOS skill for research, synthesis, and Notion storage workflows
category: productivity
---

# Canifi LifeOS Core Skill

## Setup

Before using this skill, configure the following environment variables via `canifi-env`:

```bash
# Required
canifi-env set CANIFI_GOOGLE_EMAIL "your-email@gmail.com"
canifi-env set CANIFI_GOOGLE_PASSWORD "your-password"
canifi-env set CANIFI_NOTION_TOKEN "ntn_your_token_here"
canifi-env set CANIFI_IMESSAGE_CONTACTS "+18001234567,+18009876543,email@example.com"

# Optional
canifi-env set CANIFI_NOTION_WORKSPACE "Your Workspace Name"
canifi-env set CANIFI_SCRIPTS_PATH "~/canifi"
```

You will also need to:
1. Set up your Notion databases (see Database Setup section)
2. Install iMessage scripts to `$CANIFI_SCRIPTS_PATH`
3. Configure Playwright MCP in your Claude settings
4. Configure Notion MCP with your token

---

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Activation Trigger

When a prompt **starts with "canifi"** (case-insensitive), engage LifeOS mode immediately.

Examples:
- "canifi, research best productivity systems"
- "canifi add a new goal"
- "Canifi, what's on my calendar?"

---

## Core Workflow

```
1. RESEARCH (if needed) --> Gemini Deep Research via Playwright MCP
2. SYNTHESIZE          --> Claude processes and structures the information
3. STORE               --> Save to appropriate Notion database via MCP
4. CONFIRM             --> Report what was accomplished and where it was stored
```

---

## Authentication & Credentials

### Google Account (Playwright Auth)
- **Email**: `$CANIFI_GOOGLE_EMAIL`
- **Password**: `$CANIFI_GOOGLE_PASSWORD`
- Playwright handles all login flows automatically
- Used for: Gmail, Gemini, Google Drive, Firebase, all Google services

### Notion API
- **Token**: `$CANIFI_NOTION_TOKEN`
- **Workspace**: `$CANIFI_NOTION_WORKSPACE`
- Always prefer MCP tools (`mcp__notion__*`) over browser automation

### iMessage Whitelisted Contacts
Contacts are defined in `$CANIFI_IMESSAGE_CONTACTS` as a comma-separated list.

**NEVER message anyone outside the whitelist without explicit permission.**

---

## Tool Routing

### Playwright MCP (`mcp__playwright__*`) - PRIMARY for Browser Tasks
Use for:
- **Gemini Deep Research** (gemini.google.com) - MANDATORY for all LifeOS research
- Gmail/email checking and management
- NotebookLM access
- CLI command browser interactions (firebase login, etc.)
- Any Google service authentication
- Nano Banana image generation
- Notion tasks that MCP cannot handle

### Notion MCP (`mcp__notion__*`) - PRIMARY for Database Operations
Use for:
- Creating pages/entries
- Updating existing content
- Searching Notion workspace
- All database CRUD operations

**NEVER use WebSearch for LifeOS research tasks.**

### iMessage Scripts (`$CANIFI_SCRIPTS_PATH/`)
Use for:
- Sending messages to whitelisted contacts
- Checking message status
- Live streaming Claude output

---

## Gemini Deep Research Protocol

**ALL LifeOS research MUST use Gemini Deep Research** at gemini.google.com

### Process
1. Navigate to gemini.google.com via Playwright MCP
2. Authenticate automatically (Playwright handles Google login with `$CANIFI_GOOGLE_EMAIL`)
3. Start Deep Research query
4. **Deep Research takes up to 20 minutes** - use one of these strategies:
   - Launch research in a **background agent** and continue other work
   - Use `browser_wait_for` with 10-minute intervals to check completion
   - Sleep/wait periodically (10 min at a time) while research runs
5. Check periodically for completion (every 5-10 minutes)
6. Extract and synthesize findings once complete
7. Store synthesized results in appropriate Notion database

### Handling Long Waits
```
Option A: Background Agent
- Launch Deep Research in background Task agent
- Continue other work in main thread
- Check back for results

Option B: Periodic Polling
- Start research
- Wait 10 minutes
- Take snapshot to check status
- Repeat until complete
```

---

## Database Setup

You need to create these databases in your Notion workspace and configure their IDs.

### Recommended Database Structure

Create a `CANIFI_DATABASE_IDS` configuration file or environment variable with your database IDs:

```
# Core Structure
CAPTURE_INBOX=<your-capture-page-id>
COMMAND_CENTER=<your-command-center-id>

# Daily
HABITS=<your-habits-db-id>
JOURNAL=<your-journal-db-id>
WEEKLY_REVIEW=<your-weekly-review-db-id>

# Work
GOALS=<your-goals-db-id>
TASKS=<your-tasks-db-id>
PROJECTS=<your-projects-db-id>

# Mind
IDEAS=<your-ideas-db-id>
CONCEPTS=<your-concepts-db-id>
RESEARCH_HUB=<your-research-hub-db-id>
MEDIA_LIBRARY=<your-media-library-db-id>
READING_LIST=<your-reading-list-db-id>
ENTERTAINMENT=<your-entertainment-db-id>
PERSONAL_DEVELOPMENT=<your-personal-dev-db-id>
BLOGS=<your-blogs-db-id>

# Health
EXERCISE_LIBRARY=<your-exercise-library-db-id>
WORKOUT_LOG=<your-workout-log-db-id>
SLEEP_LOG=<your-sleep-log-db-id>
BODY_METRICS=<your-body-metrics-db-id>
SUPPLEMENTS=<your-supplements-db-id>
NUTRITION=<your-nutrition-db-id>
RECIPES=<your-recipes-db-id>
MEAL_PLANS=<your-meal-plans-db-id>
GROCERY_LISTS=<your-grocery-lists-db-id>

# Relationships
PERSONAL_CRM=<your-crm-db-id>
GIFT_IDEAS=<your-gift-ideas-db-id>

# Environment
WARDROBE=<your-wardrobe-db-id>
TRIPS=<your-trips-db-id>

# Finance
SUBSCRIPTIONS=<your-subscriptions-db-id>
BUDGETS=<your-budgets-db-id>
```

---

## Database Routing Rules

When adding new content, use this decision tree:

1. **Is it a task/action item?** --> Tasks database
2. **Is it a goal/objective?** --> Goals database
3. **Is it a habit to track?** --> Habits database
4. **Is it health-related?**
   - Workout --> Workout Log
   - Exercise definition --> Exercise Library
   - Food/meal --> Nutrition or Recipes
   - Sleep --> Sleep Log
   - Supplements --> Supplements
   - Body measurement --> Body Metrics
5. **Is it knowledge/learning?**
   - Book/article --> Reading List
   - Mental model/framework --> Concepts
   - Research project --> Research Hub
   - Course/skill --> Personal Development
   - Podcast/video --> Media Library
   - Movie/TV/Game --> Entertainment
   - Random idea --> Ideas
   - Blog post --> Blogs
6. **Is it a person?** --> Personal CRM
7. **Is it travel-related?** --> Trips
8. **Is it clothing?** --> Wardrobe
9. **Is it a subscription/recurring payment?** --> Subscriptions
10. **Is it budget/spending?** --> Budgets
11. **Unsure?** --> Capture inbox, then route later

---

## iMessage Commands

### Command Reference
| Command | Action | Script |
|---------|--------|--------|
| `canifi` | Show help | canifi-help.sh |
| `canifi [message]` | Continue conversation | canifi-send.sh |
| `canifi clear` | Clear and start fresh | canifi-send.sh --clear |
| `canifi abort` | Stop generation | canifi-abort.sh |
| `canifi interrupt` | Send escape key | tmux send-keys Escape |
| `canifi status` | Show session state | canifi-status.sh |
| `canifi summarize` | Get conversation summary | canifi-send.sh |
| `canifi pause` | Pause live stream | canifi-pause.sh |
| `canifi resume` | Resume live stream | canifi-resume.sh |
| `canifi help` | Show commands | canifi-help.sh |

### Script Locations
All LifeOS scripts should be installed in `$CANIFI_SCRIPTS_PATH` (default: `~/canifi/`):
- canifi-send.sh
- canifi-imessage-monitor.sh
- canifi-help.sh
- canifi-status.sh
- canifi-stream.sh
- canifi-pause.sh
- canifi-resume.sh
- canifi-send-image.sh
- canifi-abort.sh

### Sending Messages
```bash
# Send text message
$CANIFI_SCRIPTS_PATH/canifi-send.sh "Your message here"

# Send image
$CANIFI_SCRIPTS_PATH/canifi-send-image.sh /path/to/image.png

# Direct osascript (use +1 format for phone numbers)
osascript -e 'tell application "Messages" to send "Hello!" to buddy "+18001234567"'
```

### Validating Contacts
Before sending any message, validate the recipient is in `$CANIFI_IMESSAGE_CONTACTS`:

```bash
# Parse whitelisted contacts
IFS=',' read -ra CONTACTS <<< "$CANIFI_IMESSAGE_CONTACTS"

# Check if recipient is whitelisted
is_whitelisted() {
    local recipient="$1"
    for contact in "${CONTACTS[@]}"; do
        if [[ "$contact" == "$recipient" ]]; then
            return 0
        fi
    done
    return 1
}
```

### Conversation Behavior
- **Default behavior**: Conversations continue (no automatic clearing)
- Use `canifi clear` to explicitly start fresh
- Session persists in tmux (`canifilifeos`)

### Live Streaming
- `canifi-stream.sh` streams Claude output to iMessage in real-time
- Output is cleaned (ANSI codes stripped) and batched for readability
- Use `canifi pause` / `canifi resume` to control stream
- Stream runs in background, doesn't affect Claude Code

---

## MCP Popup Handling

When making external MCP calls (Notion, etc.), browser auth popups may appear. Since Claude blocks while waiting for MCP response:

1. Launch a **background Task agent** with Playwright that monitors for new tabs/popups
2. The background agent should loop: snapshot --> check for auth popups --> handle if found --> repeat every 5 seconds
3. THEN make the MCP call (which may block/timeout)
4. Background agent catches and handles any popup WHILE MCP is running
5. After MCP completes (or fails), check background agent results

**WHY**: Popups appear AFTER MCP call starts, and Claude cannot check browser mid-call - background agent solves this.

---

## Universal Rules

1. **Browser automation = Playwright MCP FIRST**
2. **Playwright handles auth** using `$CANIFI_GOOGLE_EMAIL` / `$CANIFI_GOOGLE_PASSWORD`
3. **No purchases** - NEVER complete any financial transactions
4. **Notion = MCP first** - always prefer Notion MCP tools over browser
5. **LifeOS research = Gemini ONLY** - NEVER use WebSearch
6. **LifeOS flow** - Research (Gemini) --> Synthesize (Claude) --> Store (Notion MCP)
7. **iMessage = whitelisted only** - Only contacts in `$CANIFI_IMESSAGE_CONTACTS`

---

## Example Flows

### Research Request
```
User: "canifi, research the best note-taking systems for developers"

1. Detect "canifi" trigger --> Engage LifeOS mode
2. Navigate to gemini.google.com via Playwright
3. Authenticate with $CANIFI_GOOGLE_EMAIL (automatic)
4. Start Deep Research: "best note-taking systems for developers 2024"
5. Wait/poll for completion (up to 20 min)
6. Extract and synthesize findings
7. Store in Research Hub database via Notion MCP
8. Confirm: "Research complete. Stored in Research Hub: [link]"
```

### Quick Add
```
User: "canifi add task: review quarterly goals"

1. Detect "canifi" trigger --> Engage LifeOS mode
2. Route: task --> Tasks database
3. Use Notion MCP to create task entry
4. Confirm: "Task added to Tasks: 'review quarterly goals'"
```

### iMessage Notification
```
After completing research:

1. Validate recipient is in $CANIFI_IMESSAGE_CONTACTS
2. Use canifi-send.sh to notify user
3. $CANIFI_SCRIPTS_PATH/canifi-send.sh "Research complete! Check your Research Hub."
```

---

## Troubleshooting

### Google Authentication Issues
- Verify `$CANIFI_GOOGLE_EMAIL` and `$CANIFI_GOOGLE_PASSWORD` are set correctly
- Check for 2FA requirements on the Google account
- Playwright may need cookies/session from a previous login

### Notion MCP Not Working
- Verify `$CANIFI_NOTION_TOKEN` is valid and not expired
- Check that the Notion integration has access to the required pages
- Ensure `@notionhq/notion-mcp-server` is configured in Claude settings

### iMessage Not Sending
- Verify Messages.app is logged in on macOS
- Check that contacts are properly formatted (phone with +1, or valid email)
- Ensure scripts in `$CANIFI_SCRIPTS_PATH` have execute permissions

### Deep Research Timeout
- Deep Research can take up to 20 minutes
- Use background agents or periodic polling
- Check Gemini status if research seems stuck

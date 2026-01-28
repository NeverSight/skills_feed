---
name: monday
description: Enables Claude to create, manage, and automate workflows in monday.com via Playwright MCP
category: business
---

# monday.com Skill

## Overview
Claude can manage your monday.com workspaces to create boards, manage items, track progress, and automate workflows. A flexible work operating system for team collaboration.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/monday/install.sh | bash
```

Or manually:
```bash
cp -r skills/monday ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MONDAY_EMAIL "your-email@example.com"
```

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

## Capabilities
- Create and manage boards
- Add and edit items
- Create groups for organization
- Set column values and statuses
- Automate with recipes
- Track time on items
- Add updates and comments
- Create dashboards
- Manage workspaces
- Use board templates
- Create integrations
- Generate reports

## Usage Examples

### Example 1: Create Item
```
User: "Add 'New feature development' to the Sprint board"
Claude: Opens board, creates item in appropriate group.
        Confirms: "Item added to Sprint board"
```

### Example 2: Update Status
```
User: "Mark the design review as complete"
Claude: Finds item, updates status column to Complete.
        Confirms: "Design review marked complete"
```

### Example 3: View Board
```
User: "What's the status of our project board?"
Claude: Opens board, summarizes items by status.
        Reports: "12 items: 3 Done, 5 Working on it, 4 Stuck"
```

### Example 4: Create Board
```
User: "Create a board for tracking bugs"
Claude: Creates new board from Bug Tracking template.
        Returns: "Bug Tracking board created with default columns"
```

## Authentication Flow
1. Claude navigates to monday.com via Playwright MCP
2. Enters MONDAY_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for board operations

## Selectors Reference
```javascript
// Workspace sidebar
'.workspace-sidebar'

// Board list
'.boards-list'

// Board content
'.board-content'

// Item row
'.pulse-component'

// Add item button
'.add-pulse-button'

// Item name input
'.pulse-name-input'

// Status column
'.status-column'

// Person column
'.person-column'

// Date column
'.date-column'

// Group header
'.group-header'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Board Not Found**: List available boards, ask user
- **Item Create Failed**: Retry, verify permissions
- **Automation Failed**: Check recipe configuration
- **Permission Denied**: Notify user of access issue

## Self-Improvement Instructions
When you learn a better way to accomplish a task with monday.com:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific board configurations that work well
4. Note useful automation recipes

## Notes
- Flexible column types for any data
- Automations for workflow efficiency
- Dashboards for high-level views
- Apps marketplace for extensions
- Workdocs for documentation
- Forms for data intake
- Timeline view for planning
- Mobile apps available

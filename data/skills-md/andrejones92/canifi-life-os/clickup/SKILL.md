---
name: clickup
description: Enables Claude to create, manage, and track tasks and projects in ClickUp via Playwright MCP
category: productivity
---

# ClickUp Skill

## Overview
Claude can manage your ClickUp workspace to create tasks, organize projects, track goals, and collaborate with teams. An all-in-one productivity platform with extensive customization.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/clickup/install.sh | bash
```

Or manually:
```bash
cp -r skills/clickup ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CLICKUP_EMAIL "your-email@example.com"
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
- Create and manage tasks
- Organize with spaces and folders
- Set priorities and due dates
- Track time on tasks
- Create custom statuses
- Use custom fields
- Set goals and targets
- Create docs and wikis
- Use whiteboards
- Automate workflows
- Create dashboards
- Manage sprints

## Usage Examples

### Example 1: Create Task
```
User: "Add a task 'Update documentation' to the Engineering space"
Claude: Opens space, creates task.
        Confirms: "Task 'Update documentation' created in Engineering"
```

### Example 2: View Tasks
```
User: "What tasks are assigned to me in ClickUp?"
Claude: Opens My Tasks view, lists items.
        Reports: "8 tasks assigned: 2 Urgent, 4 High, 2 Normal priority"
```

### Example 3: Update Task
```
User: "Mark the API refactor task as in progress"
Claude: Finds task, updates status to In Progress.
        Confirms: "Task status updated to In Progress"
```

### Example 4: Track Goal
```
User: "What's our progress on Q4 goals?"
Claude: Opens Goals, reads progress.
        Reports: "Q4 Goals: 67% complete. Revenue target 80%, Feature launches 50%"
```

## Authentication Flow
1. Claude navigates to app.clickup.com via Playwright MCP
2. Enters CLICKUP_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for operations

## Selectors Reference
```javascript
// Sidebar
'.sidebar__content'

// Space list
'.sidebar__spaces'

// Task list
'.task-list'

// Task row
'.cu-task-row'

// Add task button
'.cu-add-task-button'

// Task name input
'.cu-task-title__input'

// Status dropdown
'.cu-status-button'

// Priority selector
'.cu-priority-button'

// Due date picker
'.cu-datepicker'

// Assignee
'.cu-assignee-button'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Space Not Found**: List available spaces, ask user
- **Task Create Failed**: Retry, verify folder access
- **Status Update Failed**: Check custom status configuration
- **Permission Denied**: Notify user of access issue

## Self-Improvement Instructions
When you learn a better way to accomplish a task with ClickUp:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific workspace organization patterns
4. Note useful automation configurations

## Notes
- Hierarchical structure: Workspace > Space > Folder > List > Task
- Custom statuses per list or folder
- Multiple views: list, board, calendar, Gantt, timeline
- Goals with measurable targets
- Docs for documentation
- Whiteboards for visual collaboration
- Sprint points for agile
- API available for automation

---
name: google-tasks
description: Enables Claude to create, manage, and organize tasks in Google Tasks via Playwright MCP
category: google
---

# Google Tasks Skill

## Overview
Claude can manage your Google Tasks to create to-dos, set due dates, organize task lists, and track completion. Integrates with Gmail and Calendar for seamless task management.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-tasks/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-tasks ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@gmail.com"
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
- Create tasks and subtasks
- Set due dates and times
- Organize tasks into lists
- Mark tasks as complete
- Reorder tasks by priority
- Add task details and notes
- Create tasks from emails
- View tasks in Calendar
- Star and prioritize tasks
- Create recurring tasks
- Delete and archive tasks
- Search across all lists

## Usage Examples

### Example 1: Create Task
```
User: "Add a task to review the proposal by Friday"
Claude: Creates task "Review the proposal" with due date Friday.
        Confirms: "Task created with Friday deadline"
```

### Example 2: View Tasks
```
User: "What tasks are due this week?"
Claude: Checks all lists for tasks due this week.
        Reports: "5 tasks due this week:
        1. Review proposal (Friday)
        2. Submit report (Wednesday)..."
```

### Example 3: Organize Tasks
```
User: "Create a 'Home Projects' task list with items for painting and fixing the fence"
Claude: Creates new list "Home Projects", adds both tasks.
        Confirms: "Created list with 2 tasks"
```

### Example 4: Complete Tasks
```
User: "Mark the proposal review as done"
Claude: Finds task, marks as complete.
        Confirms: "Marked 'Review the proposal' as complete"
```

## Authentication Flow
1. Claude navigates to tasks.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent Tasks operations

## Selectors Reference
```javascript
// Add task button
'[aria-label="Add a task"]'

// Task input
'.YVwEff'

// Task item
'.Q4rDld'

// Task checkbox
'[aria-label="Mark complete"]'

// Due date picker
'[aria-label="Add date/time"]'

// List selector
'.PmPSMe'

// Create new list
'[aria-label="Create new list"]'

// Task details
'[aria-label="Edit details"]'

// Delete task
'[aria-label="Delete"]'

// Subtask add
'[aria-label="Add subtasks"]'

// Star task
'[aria-label="Star"]'

// Task lists sidebar
'.Q4rDld-navItem'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Task Creation Failed**: Retry, save content locally as backup
- **Due Date Invalid**: Parse date naturally, ask for clarification
- **List Not Found**: Create list if doesn't exist, or ask user
- **Sync Failed**: Wait and retry, notify if persistent

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Tasks:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific keyboard shortcuts or workflows
4. Note any Calendar integration improvements

## Notes
- Tasks sync across Gmail, Calendar, and Tasks apps
- Due dates appear in Google Calendar
- Create tasks from emails via Gmail integration
- Subtasks help break down complex items
- Completed tasks can be viewed in completed section
- Tasks can be dragged to reorder priority
- Keyboard shortcut: T in Gmail to open Tasks sidebar
- No native recurring task support; use Calendar for recurring items
- Tasks can be accessed via tasks.google.com or Gmail sidebar

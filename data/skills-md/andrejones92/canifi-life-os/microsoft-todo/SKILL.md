---
name: microsoft-todo
description: Enables Claude to create, manage, and organize personal tasks in Microsoft To Do via Playwright MCP
category: microsoft
---

# Microsoft To Do Skill

## Overview
Claude can manage your Microsoft To Do tasks for personal productivity. Create tasks, organize with lists, set reminders, and track daily planning with My Day feature.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-todo/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-todo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MICROSOFT_EMAIL "your-email@outlook.com"
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
- Set due dates and reminders
- Organize with custom lists
- Add tasks to My Day
- Set recurring tasks
- Add notes to tasks
- Mark tasks as important
- Search and filter tasks
- Share lists with others
- Sync with Outlook tasks
- Create from flagged emails
- View completed tasks

## Usage Examples

### Example 1: Create Task
```
User: "Add a task to call the dentist by Friday"
Claude: Creates task "Call the dentist" with Friday due date.
        Confirms: "Task created with Friday deadline"
```

### Example 2: Plan My Day
```
User: "Show what's on my To Do list for today"
Claude: Opens My Day, lists tasks planned for today.
        Reports: "Your My Day has 5 tasks:
        1. Team meeting prep
        2. Review documents..."
```

### Example 3: Organize Lists
```
User: "Create a 'Home Projects' list and add painting the fence"
Claude: Creates new list "Home Projects", adds task.
        Confirms: "Created list with 1 task"
```

### Example 4: Set Reminder
```
User: "Remind me to submit the report at 3pm today"
Claude: Creates task with 3pm reminder.
        Confirms: "Task created with 3pm reminder"
```

## Authentication Flow
1. Claude navigates to to-do.microsoft.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for To Do operations

## Selectors Reference
```javascript
// My Day
'[aria-label="My Day"]'

// Task list
'.task-list'

// Add task input
'input[placeholder*="Add a task"]'

// Task item
'.task-item'

// Task checkbox
'[aria-label="Complete"]'

// Star (important)
'[aria-label="Mark as important"]'

// Due date
'[aria-label="Add due date"]'

// Reminder
'[aria-label="Remind me"]'

// List sidebar
'.list-pane'

// New list
'[aria-label="New list"]'

// Search
'[aria-label="Search"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Task Create Failed**: Retry, save locally as backup
- **Reminder Failed**: Check time validity, retry
- **List Not Found**: Create list, or ask for clarification
- **Sync Failed**: Wait and retry

## Self-Improvement Instructions
When you learn a better way to accomplish a task with To Do:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific productivity workflows
4. Note Outlook integration features

## Notes
- Syncs with Outlook Tasks
- My Day resets each day
- Suggested tasks from various sources
- Smart lists (Planned, Important, All)
- Flagged emails appear as tasks
- Keyboard shortcut: N for new task
- Lists can be shared for collaboration
- Recurring tasks supported
- Subtasks help break down items

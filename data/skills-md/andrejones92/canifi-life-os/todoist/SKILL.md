---
name: todoist
description: Enables Claude to create, manage, and organize tasks in Todoist via Playwright MCP
category: productivity
---

# Todoist Skill

## Overview
Claude can manage your Todoist tasks to capture to-dos, organize with projects and labels, set priorities and due dates, and track productivity. A powerful task management system with natural language input.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/todoist/install.sh | bash
```

Or manually:
```bash
cp -r skills/todoist ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TODOIST_EMAIL "your-email@example.com"
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
- Create tasks with natural language
- Set due dates and recurring schedules
- Assign priorities (P1-P4)
- Organize with projects and sections
- Apply labels for filtering
- Add subtasks and comments
- Set reminders
- Complete and reschedule tasks
- View productivity stats
- Filter and search tasks
- Share projects with collaborators
- Use templates for projects

## Usage Examples

### Example 1: Quick Add Task
```
User: "Add to Todoist: Call dentist tomorrow at 3pm p1"
Claude: Uses natural language parsing to create task with
        due date tomorrow 3pm, priority 1.
        Confirms: "Task created: Call dentist (Tomorrow 3pm, P1)"
```

### Example 2: View Today's Tasks
```
User: "What's on my Todoist for today?"
Claude: Opens Today view, lists tasks.
        Reports: "8 tasks today:
        1. [P1] Submit report (Work)
        2. [P2] Team meeting at 2pm..."
```

### Example 3: Organize Project
```
User: "Create a 'House Renovation' project with sections for Kitchen, Bathroom, Living Room"
Claude: Creates project with three sections.
        Confirms: "Created project with 3 sections"
```

### Example 4: Recurring Task
```
User: "Add a task to review goals every Sunday at 6pm"
Claude: Creates recurring task "Review goals" every Sunday 6pm.
        Confirms: "Recurring task created for Sundays 6pm"
```

## Authentication Flow
1. Claude navigates to todoist.com via Playwright MCP
2. Enters TODOIST_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for task operations

## Selectors Reference
```javascript
// Quick add button
'[aria-label="Quick Add"]' or 'button.quick_add'

// Task input
'.task_editor__input'

// Project list
'.left_menu'

// Today view
'[aria-label="Today"]'

// Task item
'.task_list_item'

// Complete button
'.task_checkbox'

// Priority selector
'[aria-label="Priority"]'

// Due date picker
'[aria-label="Due date"]'

// Labels
'[aria-label="Labels"]'

// Add subtask
'[aria-label="Add sub-task"]'
```

## Natural Language Examples
```
"Buy milk tomorrow" → Task: Buy milk, Due: Tomorrow
"Meeting with John every Monday 10am" → Recurring weekly
"Submit report p1 #Work @urgent" → P1, Project: Work, Label: urgent
"Call mom +1 day" → Due: Day after tomorrow
"Review code in 2 hours" → Due: 2 hours from now
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Task Create Failed**: Retry, save locally as backup
- **Date Parse Failed**: Ask for clarification
- **Project Not Found**: Create project or ask user
- **Sync Failed**: Wait and retry

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Todoist:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific natural language patterns that work
4. Note any new features or integrations

## Notes
- Natural language parsing for quick entry
- Karma points track productivity
- Filters enable custom views
- Comments for task context
- File attachments supported
- Integrations with many apps
- Offline mode with sync
- API available for advanced automation

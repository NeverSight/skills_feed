---
name: microsoft-planner
description: Enables Claude to create, manage, and track tasks in Microsoft Planner via Playwright MCP
category: microsoft
---

# Microsoft Planner Skill

## Overview
Claude can manage Microsoft Planner to create plans, organize tasks, track progress, and coordinate team work. Planner provides visual task boards with buckets, assignments, and progress tracking.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-planner/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-planner ~/.canifi/skills/
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
- Create and manage plans
- Add and organize tasks
- Create buckets for organization
- Assign tasks to team members
- Set due dates and priorities
- Track task progress
- Add checklists to tasks
- Attach files and links
- Add comments and notes
- View charts and analytics
- Filter and group tasks
- Integrate with Teams

## Usage Examples

### Example 1: Create Task
```
User: "Add a task for reviewing the proposal with high priority"
Claude: Opens Planner, adds task "Review Proposal",
        sets high priority, assigns due date.
        Confirms: "Task created with high priority"
```

### Example 2: View Plan
```
User: "What tasks are due this week in the Marketing plan?"
Claude: Opens Marketing plan, filters by due date.
        Reports: "5 tasks due this week:
        1. Social media calendar (Due Mon) - In Progress
        2. Blog post draft (Due Wed) - Not Started..."
```

### Example 3: Organize Buckets
```
User: "Create buckets for To Do, In Progress, and Done"
Claude: Opens plan, creates three buckets with specified names.
        Confirms: "Created 3 buckets for task organization"
```

### Example 4: Update Progress
```
User: "Mark the website update task as complete"
Claude: Finds task, marks as complete.
        Confirms: "Task 'Website Update' marked complete"
```

## Authentication Flow
1. Claude navigates to tasks.office.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for Planner operations

## Selectors Reference
```javascript
// Plan list
'[aria-label="Plans"]'

// Board view
'.board-view'

// Bucket
'.bucket-container'

// Task card
'.task-card'

// Add task button
'[aria-label="Add task"]'

// Task title input
'input[placeholder*="task name"]'

// Due date picker
'[aria-label="Due date"]'

// Priority selector
'[aria-label="Priority"]'

// Assign button
'[aria-label="Assign"]'

// Progress dropdown
'[aria-label="Progress"]'

// Charts view
'[aria-label="Charts"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Plan Not Found**: List available plans, ask for clarification
- **Task Create Failed**: Retry, check permissions
- **Assignment Failed**: Verify user is plan member
- **Update Failed**: Refresh and retry

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Planner:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific task management workflows
4. Note Teams integration improvements

## Notes
- Planner integrates with Microsoft Teams
- Plans can be shared with Microsoft 365 groups
- Charts view shows progress analytics
- Schedule view for timeline visualization
- Checklists for subtasks within tasks
- Labels for categorization
- Copy tasks between plans
- Export to Excel available

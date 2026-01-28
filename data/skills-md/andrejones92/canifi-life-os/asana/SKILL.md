---
name: asana
description: Enables Claude to create, manage, and track projects and tasks in Asana via Playwright MCP
category: productivity
---

# Asana Skill

## Overview
Claude can manage your Asana workspace to create projects, organize tasks, track progress, and coordinate team work. Supports multiple views including list, board, timeline, and calendar.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/asana/install.sh | bash
```

Or manually:
```bash
cp -r skills/asana ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ASANA_EMAIL "your-email@example.com"
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
- Create and manage projects
- Add and organize tasks
- Create subtasks
- Set due dates and assignees
- Track project progress
- Use custom fields
- Add task dependencies
- View timeline/Gantt
- Create milestones
- Add comments and attachments
- Use project templates
- Generate status reports

## Usage Examples

### Example 1: Create Task
```
User: "Add a task 'Prepare presentation' to the Marketing project"
Claude: Opens project, creates task with title.
        Confirms: "Task 'Prepare presentation' added to Marketing"
```

### Example 2: View Project Status
```
User: "What's the status of the Product Launch project?"
Claude: Opens project, analyzes tasks.
        Reports: "Product Launch: 65% complete. 13 tasks done,
        7 in progress, 5 pending. Next milestone: Beta Release (3 days)"
```

### Example 3: Assign Task
```
User: "Assign the UX review task to Sarah with Friday deadline"
Claude: Finds task, assigns to Sarah, sets due date.
        Confirms: "Assigned to Sarah, due Friday"
```

### Example 4: Create Project
```
User: "Create a new project for the website redesign"
Claude: Creates project "Website Redesign" with sections.
        Returns: "Project created with default sections"
```

## Authentication Flow
1. Claude navigates to app.asana.com via Playwright MCP
2. Enters ASANA_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for project operations

## Selectors Reference
```javascript
// Sidebar
'.SidebarWorkspaceDropdownButton'

// Project list
'.SidebarNavigationLinkList'

// Task list
'.TaskList'

// Task row
'.TaskRow'

// Add task button
'.AddTaskButton'

// Task name input
'.TaskName-input'

// Assignee
'.TaskAssigneeField'

// Due date
'.DueDateField'

// Project header
'.ProjectHeader'

// Sections
'.TaskListSectionRow'

// Timeline view
'.Timeline'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Project Not Found**: List available projects, ask user
- **Task Create Failed**: Retry, verify project access
- **Assignment Failed**: Verify member is in workspace
- **Permission Denied**: Notify user of access issue

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Asana:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific project management workflows
4. Note useful custom field configurations

## Notes
- Multiple views: list, board, timeline, calendar
- Custom fields for project-specific data
- Rules for automation
- Forms for task intake
- Goals for OKR tracking
- Portfolios for project oversight
- Workload view for capacity planning
- Templates for repeatable projects

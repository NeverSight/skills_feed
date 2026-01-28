---
name: evernote
description: Enables Claude to create, organize, and search notes in Evernote via Playwright MCP
category: productivity
---

# Evernote Skill

## Overview
Claude can manage your Evernote to capture notes, clip web content, organize with notebooks and tags, and search across your knowledge base. A comprehensive note-taking and organization platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/evernote/install.sh | bash
```

Or manually:
```bash
cp -r skills/evernote ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set EVERNOTE_EMAIL "your-email@example.com"
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
- Create and edit notes
- Organize with notebooks and stacks
- Apply tags for organization
- Search notes and attachments
- Clip web pages
- Scan documents
- Add reminders
- Share notes and notebooks
- Create note templates
- Add checkboxes and tables
- Attach files and images
- Access note history

## Usage Examples

### Example 1: Create Note
```
User: "Create a note about the project meeting"
Claude: Creates note "Project Meeting" with date, adds template.
        Confirms: "Note created in default notebook"
```

### Example 2: Search Notes
```
User: "Find my notes about machine learning"
Claude: Searches for "machine learning".
        Reports: "Found 7 notes: ML Fundamentals, Neural Networks tutorial..."
```

### Example 3: Organize Notes
```
User: "Move all project notes to the Work notebook"
Claude: Finds project-related notes, moves to Work notebook.
        Confirms: "Moved 12 notes to Work notebook"
```

### Example 4: Add Reminder
```
User: "Set a reminder on my TODO note for tomorrow"
Claude: Finds TODO note, adds reminder for tomorrow.
        Confirms: "Reminder set for tomorrow"
```

## Authentication Flow
1. Claude navigates to evernote.com via Playwright MCP
2. Enters EVERNOTE_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for note operations

## Selectors Reference
```javascript
// Note list
'.note-list'

// Note item
'.note-list-item'

// Editor
'.RichTextEditor'

// Note title
'.note-title-input'

// Notebook selector
'.notebook-select'

// Tags field
'.tag-input'

// Search box
'[aria-label="Search"]'

// New note button
'[aria-label="New Note"]'

// Sidebar
'.navigation-sidebar'

// Notebooks list
'.notebooks-list'
```

## Search Syntax
```
notebook:Work           // Notes in specific notebook
tag:important           // Notes with specific tag
created:day-7           // Created in last 7 days
updated:month           // Updated this month
intitle:meeting         // Title contains "meeting"
resource:application/pdf // Contains PDF attachments
todo:true               // Contains checkboxes
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Note Not Found**: Search with variations, ask user
- **Notebook Full**: Notify of limits, suggest cleanup
- **Sync Failed**: Wait and retry
- **Attachment Failed**: Check file size, retry

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Evernote:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific organization strategies
4. Note useful search syntax

## Notes
- Syncs across all devices
- Web Clipper for saving web content
- Document scanning with OCR
- Note history for recovery
- Templates for common note types
- Internal note links
- Shared notebooks for collaboration
- Tasks integrated with notes

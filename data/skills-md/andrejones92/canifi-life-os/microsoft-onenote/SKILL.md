---
name: microsoft-onenote
description: Enables Claude to create, organize, and manage notes in Microsoft OneNote via Playwright MCP
category: microsoft
---

# Microsoft OneNote Skill

## Overview
Claude can manage your Microsoft OneNote notebooks to capture notes, organize information, create checklists, and maintain a structured knowledge base. Supports notebooks, sections, and pages with rich content.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-onenote/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-onenote ~/.canifi/skills/
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
- Create and organize notebooks
- Add sections and pages
- Write and format notes
- Insert images and files
- Create checklists and tables
- Add tags and highlights
- Search across notebooks
- Share notebooks for collaboration
- Add audio recordings
- Draw and handwrite (limited)
- Clip web content
- Link between pages

## Usage Examples

### Example 1: Create Note
```
User: "Create a note for today's meeting in OneNote"
Claude: Opens OneNote, navigates to appropriate section,
        creates page "Meeting Notes - [Date]" with template.
        Returns: "Created meeting notes page"
```

### Example 2: Organize Notebook
```
User: "Create a new section for project research"
Claude: Opens notebook, adds "Project Research" section,
        creates initial pages for different topics.
        Confirms: "Created Project Research section with 3 pages"
```

### Example 3: Search Notes
```
User: "Find my notes about the marketing strategy"
Claude: Searches notebooks for "marketing strategy".
        Reports: "Found 4 pages with marketing strategy content:
        1. Q4 Marketing Plan (Work notebook)..."
```

### Example 4: Add Checklist
```
User: "Add a project checklist to my planning page"
Claude: Opens planning page, inserts checklist with items.
        Confirms: "Added checklist with 8 items"
```

## Authentication Flow
1. Claude navigates to onenote.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for OneNote operations

## Selectors Reference
```javascript
// Notebook list
'[aria-label="Notebooks"]'

// Section tabs
'.section-tabs'

// Page list
'.page-list'

// Note content
'[contenteditable="true"]'

// New page
'[aria-label="Add page"]'

// New section
'[aria-label="Add section"]'

// Search
'[aria-label="Search"]'

// Insert menu
'[aria-label="Insert"]'

// Tag menu
'[aria-label="Tags"]'

// Share button
'[aria-label="Share"]'

// Checkbox insert
'[aria-label="To Do Tag"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Notebook Not Found**: List available notebooks, ask for clarification
- **Page Create Failed**: Check permissions, retry
- **Sync Failed**: Wait and retry, notify if persistent
- **Search No Results**: Suggest broader terms

## Self-Improvement Instructions
When you learn a better way to accomplish a task with OneNote:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific organizational tips
4. Note differences from desktop OneNote

## Notes
- OneNote syncs across all devices
- Notebooks stored on OneDrive
- Free-form canvas allows flexible layout
- Tags help organize and find content
- Audio notes require microphone
- Web Clipper browser extension available
- Ink-to-text conversion available
- Pages have unlimited canvas space

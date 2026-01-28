---
name: google-keep
description: Enables Claude to create, organize, and manage notes and lists in Google Keep via Playwright MCP
category: google
---

# Google Keep Skill

## Overview
Claude can manage your Google Keep notes to capture ideas, create checklists, set reminders, and organize information with labels and colors. Perfect for quick notes, to-do lists, and collaborative note-taking.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-keep/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-keep ~/.canifi/skills/
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
- Create text notes and checklists
- Add images and drawings to notes
- Set time and location-based reminders
- Organize notes with labels and colors
- Pin important notes to top
- Archive and delete notes
- Search notes by content
- Collaborate on shared notes
- Convert notes to Google Docs
- Create voice notes (transcribed)
- Copy notes between accounts

## Usage Examples

### Example 1: Create a Quick Note
```
User: "Make a note about the book recommendation: Atomic Habits"
Claude: Creates note titled "Book Recommendation" with content
        "Atomic Habits by James Clear". Confirms: "Note created"
```

### Example 2: Create Checklist
```
User: "Create a grocery list: milk, eggs, bread, butter"
Claude: Creates checklist note titled "Grocery List" with
        4 checkbox items. Returns: "Checklist created with 4 items"
```

### Example 3: Set Reminder
```
User: "Remind me to call mom tomorrow at 5pm"
Claude: Creates note "Call mom", sets reminder for tomorrow 5pm.
        Confirms: "Reminder set for tomorrow at 5pm"
```

### Example 4: Organize Notes
```
User: "Add the 'Work' label to all my project notes"
Claude: Searches for project-related notes, applies "Work" label to each.
        Reports: "Added 'Work' label to 7 notes"
```

## Authentication Flow
1. Claude navigates to keep.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent Keep operations

## Selectors Reference
```javascript
// Take a note input
'[aria-label="Take a note…"]'

// Note title
'[aria-label="Title"]'

// Note content
'[aria-label="Note"]' or '[contenteditable="true"]'

// New list button
'[aria-label="New list"]'

// Checklist item
'.VIpgJd-TUo6Hb'

// Pin button
'[aria-label="Pin note"]'

// Reminder button
'[aria-label="Remind me"]'

// Color picker
'[aria-label="Background options"]'

// Label button
'[aria-label="Add label"]'

// Archive button
'[aria-label="Archive"]'

// Delete button
'[aria-label="Delete note"]'

// Search box
'input[aria-label="Search"]'

// Note cards
'.IZ65Hb-n0tgWb'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Note Creation Failed**: Retry, save content locally as backup
- **Reminder Set Failed**: Verify date/time format, retry
- **Label Not Found**: Create label if it doesn't exist
- **Search No Results**: Suggest broader search terms

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Keep:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific shortcuts or organizational tips
4. Note any sync behavior improvements

## Notes
- Notes sync across all devices with Google account
- Maximum note size: 19,999 characters
- Images can be added from camera or upload
- Location reminders require location permissions
- Labels are limited but colors provide visual organization
- Keyboard shortcuts: C for new note, L for new list
- Archived notes are searchable but hidden from main view
- Shared notes update in real-time for collaborators

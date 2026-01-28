---
name: bear
description: Enables Claude to create and manage notes in Bear app via Playwright MCP (Bear Web)
category: productivity
---

# Bear Skill

## Overview
Claude can manage your Bear notes via Bear's web interface to create notes, organize with tags, and maintain a beautiful markdown-based note system. A focused writing experience for Apple users.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/bear/install.sh | bash
```

Or manually:
```bash
cp -r skills/bear ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BEAR_EMAIL "your-email@example.com"
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
- Organize with nested tags
- Search notes and content
- Apply markdown formatting
- Pin important notes
- Archive notes
- Export in multiple formats
- Add images and files
- Create links between notes
- Use hashtags for organization
- View tag hierarchy
- Sync across devices

## Usage Examples

### Example 1: Create Note
```
User: "Create a Bear note for today's journal entry"
Claude: Creates note with date title, adds journal template.
        Confirms: "Journal note created with today's date"
```

### Example 2: Search Notes
```
User: "Find my notes about productivity"
Claude: Searches Bear for "productivity".
        Reports: "Found 5 notes: Productivity Tips, GTD Setup..."
```

### Example 3: Organize with Tags
```
User: "Add the #work/projects tag to my project notes"
Claude: Finds project notes, adds nested tag.
        Confirms: "Added #work/projects to 8 notes"
```

### Example 4: Export Note
```
User: "Export my research note as markdown"
Claude: Opens note, exports as .md file.
        Confirms: "Exported research.md"
```

## Authentication Flow
1. Claude navigates to Bear web interface via Playwright MCP
2. Enters BEAR_EMAIL for authentication
3. Handles Apple ID 2FA if required (notifies user via iMessage)
4. Maintains session for note operations

## Selectors Reference
```javascript
// Note list
'.notes-list'

// Note item
'.note-item'

// Editor
'.editor-content'

// Note title
'.note-title'

// Tag sidebar
'.tags-sidebar'

// Search input
'.search-input'

// New note button
'.new-note-button'

// Tag in note
'.tag-token'

// Pin button
'.pin-button'

// Export menu
'.export-menu'
```

## Bear Markdown Extensions
```
# Heading 1
## Heading 2
**bold** or __bold__
*italic* or _italic_
~strikethrough~
::highlight::
#tag/nested/tag
[[note link]]
- [ ] todo
- [x] completed
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Note Not Found**: Search with variations, ask user
- **Tag Error**: Check tag syntax, suggest fix
- **Sync Failed**: Wait and retry
- **Export Failed**: Try alternative format

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Bear:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific tagging strategies
4. Note useful markdown extensions

## Notes
- Apple ecosystem (iOS, macOS)
- Nested tags for hierarchy
- Beautiful typography
- Focus mode for writing
- Multiple export formats
- Themes and customization
- WikiLinks between notes
- Web interface limited vs native

---
name: workflowy
description: Enables Claude to create and manage outlines in WorkFlowy via Playwright MCP
category: productivity
---

# WorkFlowy Skill

## Overview
Claude can manage your WorkFlowy lists to capture thoughts, organize information, and maintain a flexible outline-based system. An infinitely nestable document for all your notes.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/workflowy/install.sh | bash
```

Or manually:
```bash
cp -r skills/workflowy ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WORKFLOWY_EMAIL "your-email@example.com"
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
- Create and edit bullets
- Nest items infinitely
- Search across all content
- Add tags and mentions
- Complete and mirror items
- Share lists with others
- Use keyboard shortcuts
- Zoom into any bullet
- Add notes to bullets
- Star important items
- View recent changes
- Export and backup

## Usage Examples

### Example 1: Add Item
```
User: "Add 'Review quarterly goals' to my WorkFlowy"
Claude: Opens WorkFlowy, adds bullet.
        Confirms: "Added to your outline"
```

### Example 2: Organize Content
```
User: "Create a section for project tasks with sub-items"
Claude: Creates parent bullet with nested children.
        Confirms: "Created project section with 5 tasks"
```

### Example 3: Search Notes
```
User: "Find all items tagged #urgent"
Claude: Searches for #urgent tag.
        Reports: "Found 7 items with #urgent tag"
```

### Example 4: Complete Items
```
User: "Mark the report task as complete"
Claude: Finds item, marks as completed.
        Confirms: "Report task marked complete"
```

## Authentication Flow
1. Claude navigates to workflowy.com via Playwright MCP
2. Enters WORKFLOWY_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for operations

## Selectors Reference
```javascript
// Main content
'.mainContent'

// Bullet item
'.project'

// Bullet text
'.content'

// Nested children
'.children'

// Search box
'.searchBox'

// Complete checkbox
'.bullet'

// Note section
'.note'

// Tags
'.contentTag'

// Starred items
'.starred'

// Zoom controls
'.breadcrumbs'
```

## WorkFlowy Features
```
#tag               // Hashtag
@mention           // Mention user
Complete (Ctrl+Enter)  // Mark done
Mirror             // Reference elsewhere
Zoom (Click bullet)    // Focus view
Note (Shift+Enter)     // Add note
Star               // Mark important
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Item Not Found**: Search with variations, ask user
- **Add Failed**: Retry, check cursor position
- **Sync Failed**: Wait and retry
- **Export Failed**: Try alternative method

## Self-Improvement Instructions
When you learn a better way to accomplish a task with WorkFlowy:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific organization patterns
4. Note useful keyboard shortcuts

## Notes
- Infinite nesting depth
- Single document structure
- Keyboard-driven workflow
- Mirrors for cross-references
- Collaborative sharing
- Tags for organization
- Offline mode available
- Mobile apps available

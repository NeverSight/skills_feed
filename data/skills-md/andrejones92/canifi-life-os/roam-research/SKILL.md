---
name: roam-research
description: Enables Claude to create, link, and query notes in Roam Research via Playwright MCP
category: productivity
---

# Roam Research Skill

## Overview
Claude can manage your Roam Research database to capture thoughts, create bidirectional links, build a networked knowledge base, and query your notes. A tool for networked thought.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/roam-research/install.sh | bash
```

Or manually:
```bash
cp -r skills/roam-research ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ROAM_EMAIL "your-email@example.com"
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
- Create daily notes and pages
- Build bidirectional links
- Create block references
- Query with Roam queries
- Use templates and workflows
- Create TODO items
- Add page references
- Use attributes and metadata
- Create tables
- Embed blocks and pages
- View graph overview
- Use keyboard shortcuts

## Usage Examples

### Example 1: Add to Daily Note
```
User: "Add 'Met with John about the project' to today's Roam note"
Claude: Opens daily note, adds block with content.
        Confirms: "Added to today's daily note"
```

### Example 2: Create Page
```
User: "Create a page for Project Alpha with key details"
Claude: Creates [[Project Alpha]] page, adds initial content.
        Returns: "Created Project Alpha page"
```

### Example 3: Search Links
```
User: "Find all pages linking to Machine Learning"
Claude: Checks backlinks for [[Machine Learning]].
        Reports: "12 pages reference Machine Learning: Neural Networks, Deep Learning..."
```

### Example 4: Query Notes
```
User: "Find all my TODOs from this week"
Claude: Runs query for TODO items with date filter.
        Reports: "8 TODOs this week: Review proposal, Update docs..."
```

## Authentication Flow
1. Claude navigates to roamresearch.com via Playwright MCP
2. Enters ROAM_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for graph operations

## Selectors Reference
```javascript
// Daily notes
'.roam-article'

// Block
'.rm-block'

// Block content
'.rm-block__input'

// Page title
'.rm-title-display'

// Sidebar
'.roam-sidebar'

// Search
'.bp3-input'

// Linked references
'.rm-reference-container'

// Block reference
'.rm-block-ref'

// Page reference
'.rm-page-ref'

// TODO checkbox
'.check-container'
```

## Roam Syntax
```
[[Page Link]]          // Link to page
((block-id))           // Block reference
#tag                   // Tag
{{TODO}}               // TODO item
{{[[TODO]]}}           // TODO with page link
**bold**               // Bold text
__italics__            // Italic text
^^highlight^^          // Highlight
{{embed: [[page]]}}    // Embed page
{{query: {and:...}}}   // Roam query
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Page Not Found**: Create page or ask user
- **Block Failed**: Retry, check graph sync
- **Query Error**: Check query syntax, suggest fix
- **Sync Issues**: Wait and retry

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Roam:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific linking strategies
4. Note useful query patterns

## Notes
- Bidirectional links are automatic
- Block references for reusable content
- Daily notes as capture inbox
- Graph view shows connections
- Roam queries for dynamic content
- Keyboard-driven interface
- Version history available
- JSON export for backup

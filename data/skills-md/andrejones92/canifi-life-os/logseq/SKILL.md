---
name: logseq
description: Enables Claude to create and manage notes in Logseq via Playwright MCP
category: productivity
---

# Logseq Skill

## Overview
Claude can manage your Logseq graph to capture thoughts, build connections, and maintain a local-first knowledge base. An outliner with bidirectional links for networked thinking.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/logseq/install.sh | bash
```

Or manually:
```bash
cp -r skills/logseq ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LOGSEQ_EMAIL "your-email@example.com"
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
- Create journal entries and pages
- Build bidirectional links
- Create block references
- Use advanced queries
- Set up flashcards (spaced repetition)
- Create TODO items
- Add properties to blocks
- Use templates
- Build whiteboards
- Create namespaced pages
- View graph overview
- Export and sync content

## Usage Examples

### Example 1: Add to Journal
```
User: "Add 'Read chapter 3 of Atomic Habits' to today's Logseq journal"
Claude: Opens journal, adds block with content.
        Confirms: "Added to today's journal"
```

### Example 2: Create Page
```
User: "Create a page for [[Project Alpha]] with key details"
Claude: Creates page with title and initial content.
        Returns: "Created Project Alpha page"
```

### Example 3: Query Notes
```
User: "Find all my TODOs from this month"
Claude: Runs query for TODO items.
        Reports: "15 TODOs found: Review proposal, Update docs..."
```

### Example 4: Create Flashcard
```
User: "Create a flashcard for the definition of Machine Learning"
Claude: Creates block with flashcard syntax.
        Confirms: "Flashcard created for spaced repetition"
```

## Authentication Flow
1. Claude navigates to Logseq web/cloud via Playwright MCP
2. Enters LOGSEQ_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for graph operations

## Selectors Reference
```javascript
// Journal page
'.journal'

// Block
'.block-container'

// Block content
'.block-editor'

// Page title
'.page-title'

// Left sidebar
'.left-sidebar'

// Search
'.search-input'

// Graph view
'.graph-view'

// Properties
'.block-properties'

// TODO marker
'.todo-marker'

// Linked references
'.references'
```

## Logseq Syntax
```
[[Page Link]]           // Link to page
((block-id))            // Block reference
#tag                    // Tag
TODO                    // Task item
DONE                    // Completed task
property:: value        // Block property
/template               // Insert template
{{query [[tag]]}}       // Query blocks
{{embed [[page]]}}      // Embed page
#card                   // Flashcard
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Page Not Found**: Create page or ask user
- **Query Error**: Check query syntax, suggest fix
- **Sync Failed**: Wait and retry
- **Graph Corrupt**: Suggest rebuild

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Logseq:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific query patterns
4. Note useful template configurations

## Notes
- Local-first with optional sync
- Outline-based structure
- Bidirectional links automatic
- Advanced queries for filtering
- Flashcards for learning
- Whiteboards for visual thinking
- PDF annotation support
- Plugin ecosystem available

---
name: remnote
description: Enables Claude to create notes and flashcards in RemNote via Playwright MCP
category: productivity
---

# RemNote Skill

## Overview
Claude can manage your RemNote knowledge base to create notes, build flashcards, and use spaced repetition for learning. Combines note-taking with active recall for effective learning.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/remnote/install.sh | bash
```

Or manually:
```bash
cp -r skills/remnote ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set REMNOTE_EMAIL "your-email@example.com"
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
- Create notes and documents
- Build flashcards automatically
- Use spaced repetition
- Create bidirectional links
- Build concept hierarchies
- Add images and media
- Create multi-line cards
- Use templates and power-ups
- Share knowledge bases
- Import from other tools
- Export content
- Track learning progress

## Usage Examples

### Example 1: Create Flashcard
```
User: "Create a flashcard: What is photosynthesis? :: The process by which plants convert light to energy"
Claude: Creates rem with cloze deletion.
        Confirms: "Flashcard created and added to queue"
```

### Example 2: Add Notes
```
User: "Add notes about Chapter 5 of my textbook"
Claude: Creates document with outline structure.
        Confirms: "Notes added to your knowledge base"
```

### Example 3: Review Cards
```
User: "How many flashcards do I have due today?"
Claude: Checks spaced repetition queue.
        Reports: "23 cards due today. Categories: Biology (12), History (11)"
```

### Example 4: Link Concepts
```
User: "Link [[Mitochondria]] to [[Cell Biology]]"
Claude: Creates reference between concepts.
        Confirms: "Concepts linked bidirectionally"
```

## Authentication Flow
1. Claude navigates to remnote.com via Playwright MCP
2. Enters REMNOTE_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for operations

## Selectors Reference
```javascript
// Document tree
'.document-tree'

// Rem (note block)
'.rem-container'

// Rem text
'.rem-text'

// Flashcard indicator
'.spaced-repetition-icon'

// Practice button
'.practice-button'

// Search
'.search-input'

// Tags
'.rem-tag'

// References
'.rem-reference'

// Queue counter
'.queue-counter'

// Add rem button
'.add-rem-button'
```

## RemNote Syntax
```
Question::Answer        // Basic flashcard
{{cloze}}              // Cloze deletion
[[Page Link]]          // Reference
#tag                   // Tag
- Bullet point         // List item
1. Numbered item       // Numbered list
> Quote                // Block quote
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Card Create Failed**: Retry, check syntax
- **Sync Failed**: Wait and retry
- **Queue Error**: Refresh and retry
- **Import Failed**: Check file format

## Self-Improvement Instructions
When you learn a better way to accomplish a task with RemNote:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific flashcard creation patterns
4. Note effective spaced repetition strategies

## Notes
- Spaced repetition built-in
- Automatic flashcard creation
- Hierarchical knowledge structure
- PDF annotation support
- Multi-column cards
- Image occlusion
- Templates for patterns
- Offline mode available

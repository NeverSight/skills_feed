---
name: gemini-canvas
description: Enables Claude to create and edit documents collaboratively using Gemini Canvas for visual writing and coding
category: ai
---

# Gemini Canvas Skill

## Overview
Claude can use Gemini Canvas at gemini.google.com for collaborative document creation, code editing, and visual content development. Canvas provides a side-by-side workspace for iterative writing and coding with AI assistance.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gemini-canvas/install.sh | bash
```

Or manually:
```bash
cp -r skills/gemini-canvas ~/.canifi/skills/
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
- Create and edit documents in canvas view
- Write and refine long-form content
- Develop and debug code collaboratively
- Iterate on drafts with AI suggestions
- Format and structure documents
- Generate outlines and expand content
- Refactor and improve code
- Create technical documentation
- Build structured reports
- Develop creative writing pieces

## Usage Examples

### Example 1: Write Document
```
User: "Use Canvas to write a project proposal"
Claude: Opens Gemini Canvas, starts document:
        "Create a project proposal for [topic]"
        Iterates with suggestions, refines structure,
        exports final document.
```

### Example 2: Code Development
```
User: "Use Canvas to build a Python web scraper"
Claude: Opens Canvas in code mode, develops scraper:
        Initial implementation, then iterates to add
        error handling, logging, and documentation.
```

### Example 3: Refine Content
```
User: "Help me improve this blog post in Canvas"
Claude: Pastes content into Canvas, requests improvements:
        "Improve clarity, add transitions, enhance introduction"
        Returns polished version.
```

### Example 4: Technical Documentation
```
User: "Create API documentation for my endpoints"
Claude: Uses Canvas to structure documentation:
        Endpoint descriptions, parameters, examples,
        error codes. Exports formatted documentation.
```

## Authentication Flow
1. Claude navigates to gemini.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Accesses Canvas feature

## Canvas Workflow
```
1. Navigate to gemini.google.com
2. Start conversation or select Canvas mode
3. Create initial content with prompt
4. Review in side-by-side canvas view
5. Request iterations and improvements
6. Apply suggested changes
7. Export or copy final content
```

## Selectors Reference
```javascript
// Chat input
'[aria-label="Enter a prompt here"]' or 'rich-textarea'

// Canvas panel
'.canvas-editor' or '.canvas-content'

// Canvas toggle
'[aria-label="Canvas"]' or canvas mode button

// Code block
'.code-block' or 'pre code'

// Copy button
'[aria-label="Copy"]'

// Apply changes
'[aria-label="Apply"]'

// Undo/Redo
'[aria-label="Undo"]'
'[aria-label="Redo"]'

// Export options
'[aria-label="Export"]'
```

## Canvas Modes
```
Writing Mode:
- Long-form documents
- Essays and articles
- Reports and proposals
- Creative writing

Code Mode:
- Python, JavaScript, etc.
- Full file development
- Debugging and refactoring
- Documentation generation
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Canvas Not Available**: Fall back to regular chat mode
- **Content Too Long**: Split into sections, process iteratively
- **Save Failed**: Copy content to clipboard as backup
- **Export Failed**: Copy manually, try alternative format

## Self-Improvement Instructions
When you learn a better way to use Gemini Canvas:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific prompts that produce better iterations
4. Note any new Canvas features or modes

## Notes
- Canvas provides visual side-by-side editing
- Useful for longer content that needs iteration
- Code mode supports syntax highlighting
- Changes can be accepted or rejected individually
- Version history may be available
- Best for content requiring multiple revision passes
- Export to various formats supported
- Canvas view requires larger screen for best experience

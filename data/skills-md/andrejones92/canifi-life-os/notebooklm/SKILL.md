---
name: notebooklm
description: Enables Claude to create and interact with NotebookLM for document analysis, audio overviews, and knowledge synthesis
category: ai
---

# NotebookLM Skill

## Overview
Claude can use Google NotebookLM at notebooklm.google.com to analyze documents, create audio overviews, and synthesize knowledge from multiple sources. NotebookLM excels at creating podcast-style audio summaries and answering questions about uploaded content.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/notebooklm/install.sh | bash
```

Or manually:
```bash
cp -r skills/notebooklm ~/.canifi/skills/
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
- Upload and analyze documents
- Create audio overviews (podcast-style)
- Ask questions about uploaded content
- Synthesize information across sources
- Generate summaries and notes
- Create study guides
- Extract key insights
- Compare information across documents
- Generate FAQs from content
- Create briefing documents

## Usage Examples

### Example 1: Create Audio Overview
```
User: "Create an audio summary of my research papers"
Claude: Uploads documents to NotebookLM, requests audio overview.
        Waits for generation (several minutes), downloads audio.
        Returns: "Created 12-minute audio overview of your research"
```

### Example 2: Document Analysis
```
User: "Analyze these PDFs and find common themes"
Claude: Uploads PDFs to NotebookLM, asks for theme analysis.
        Returns: "Key themes across documents:
        1. Innovation in AI
        2. Ethical considerations..."
```

### Example 3: Q&A Session
```
User: "Ask NotebookLM about the main arguments in my uploaded papers"
Claude: Queries NotebookLM about document content.
        Returns detailed answers with source citations.
```

### Example 4: Study Guide Creation
```
User: "Create a study guide from my course materials"
Claude: Uploads materials, requests study guide format.
        Returns structured guide with key concepts, questions, summaries.
```

## Authentication Flow
1. Claude navigates to notebooklm.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Accesses notebook interface

## NotebookLM Workflow
```
1. Navigate to notebooklm.google.com
2. Create new notebook or open existing
3. Upload source documents
4. Wait for processing
5. Interact with content (Q&A, summaries)
6. Generate audio overview if requested
7. Export or share results
```

## Selectors Reference
```javascript
// Create notebook
'[aria-label="Create"]' or '.new-notebook-button'

// Upload sources
'[aria-label="Add source"]'

// Source list
'.source-list'

// Chat input
'[aria-label="Ask a question"]'

// Generate audio
'[aria-label="Generate audio overview"]'

// Audio player
'.audio-player'

// Download audio
'[aria-label="Download"]'

// Notes panel
'.notes-panel'

// Summary button
'[aria-label="Summarize"]'
```

## Audio Overview Notes
```
- Generation takes 3-10 minutes
- Creates podcast-style conversation
- Two AI hosts discuss the content
- Audio length varies by content amount
- Can customize focus topics
- Downloadable as audio file
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Upload Failed**: Check file format/size, retry
- **Audio Generation Failed**: Retry, check content suitability
- **Processing Timeout**: Wait longer, check status periodically
- **Notebook Not Found**: List available notebooks, ask user to specify

## Supported Source Types
```
PDFs
Google Docs
Google Slides
Web URLs
Text files
YouTube videos
Audio files
Copied text
```

## Self-Improvement Instructions
When you learn a better way to use NotebookLM:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific query types that produce better results
4. Note any new features or source type support

## Notes
- NotebookLM is part of LifeOS tools for knowledge synthesis
- Audio overviews are unique to NotebookLM
- Sources are private to your notebooks
- Can share notebooks with collaborators
- Best for document-heavy analysis tasks
- Supports up to 50 sources per notebook
- Audio can be shared or embedded
- Ideal for creating content from existing materials

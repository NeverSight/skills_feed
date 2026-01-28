---
name: gemini-deep-research
description: Enables Claude to conduct comprehensive research using Gemini Deep Research for in-depth analysis and reports
category: ai
---

# Gemini Deep Research Skill

## Overview
Claude can leverage Gemini Deep Research at gemini.google.com to conduct thorough, multi-source research on complex topics. Deep Research spends up to 20 minutes exploring the web, analyzing sources, and synthesizing findings into comprehensive reports.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gemini-deep-research/install.sh | bash
```

Or manually:
```bash
cp -r skills/gemini-deep-research ~/.canifi/skills/
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
- Conduct in-depth research on any topic
- Analyze multiple sources automatically
- Generate structured research reports
- Identify key themes and insights
- Provide source citations
- Compare different viewpoints
- Summarize complex information
- Answer multi-faceted questions
- Research market trends and analysis
- Investigate technical topics

## Usage Examples

### Example 1: Topic Research
```
User: "canifi, research the best productivity systems for software engineers"
Claude: Opens Gemini, initiates Deep Research query.
        Waits for completion (up to 20 min), extracts findings.
        Stores synthesized report in Notion Research Hub.
```

### Example 2: Market Analysis
```
User: "canifi, research the current state of AI in healthcare"
Claude: Launches Deep Research, monitors for completion.
        Returns comprehensive analysis with key players,
        trends, challenges, and opportunities.
```

### Example 3: Technical Investigation
```
User: "canifi, research best practices for microservices architecture"
Claude: Initiates research, waits for completion.
        Provides detailed report on patterns, tools,
        case studies, and recommendations.
```

### Example 4: Comparative Research
```
User: "canifi, compare React vs Vue vs Svelte for my next project"
Claude: Runs Deep Research on all three frameworks.
        Delivers comparison table with pros, cons,
        use cases, and recommendations.
```

## Authentication Flow
1. Claude navigates to gemini.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for research operations

## Research Process
```
1. Navigate to gemini.google.com
2. Click on Deep Research mode
3. Enter research query
4. Monitor progress (up to 20 minutes)
5. Extract and synthesize results
6. Store in appropriate Notion database
7. Report findings to user
```

## Selectors Reference
```javascript
// Chat input
'[aria-label="Enter a prompt here"]' or 'rich-textarea'

// Deep Research button
'[aria-label="Deep Research"]' or button with research icon

// Submit button
'[aria-label="Send message"]'

// Response container
'.response-content' or '.model-response'

// Research progress indicator
'.research-progress'

// Sources panel
'.sources-panel'

// Copy response
'[aria-label="Copy"]'

// New chat
'[aria-label="New chat"]'
```

## Waiting Strategy
```javascript
// Deep Research can take up to 20 minutes
// Use periodic checking:
1. Launch research query
2. Wait 5 minutes (browser_wait_for)
3. Check for completion indicator
4. If not complete, wait another 5 minutes
5. Repeat until complete or 20 minute timeout
6. Extract results when done
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Research Timeout**: Notify user, offer to continue or restart
- **Query Rejected**: Rephrase query, try again
- **Extraction Failed**: Take screenshot, manually extract key points
- **Rate Limited**: Wait and retry with backoff

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Gemini Deep Research:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific query formulations that work better
4. Note any UI changes affecting the workflow

## Notes
- Deep Research is the PRIMARY research method for LifeOS
- Always synthesize results before storing in Notion
- Research can take 5-20 minutes; plan accordingly
- Results include citations and source links
- Research quality improves with specific, well-formed queries
- Consider running in background agent for long research tasks
- All research outputs should be stored in Notion Research Hub
- Never use WebSearch for LifeOS research; always use Deep Research

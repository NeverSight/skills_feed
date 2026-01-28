---
name: gemini-chat
description: Enables Claude to interact with Gemini AI chat for quick queries, brainstorming, and alternative AI perspectives
category: ai
---

# Gemini Chat Skill

## Overview
Claude can interact with Gemini AI at gemini.google.com for quick queries, brainstorming sessions, and getting alternative AI perspectives. Useful for cross-referencing information and leveraging Gemini's real-time web access.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gemini-chat/install.sh | bash
```

Or manually:
```bash
cp -r skills/gemini-chat ~/.canifi/skills/
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
- Ask quick questions with real-time web access
- Brainstorm ideas and get suggestions
- Cross-reference information from multiple AI sources
- Get real-time information and news
- Analyze images and documents
- Generate creative content
- Translate languages
- Summarize web content
- Get coding assistance
- Explore alternative perspectives

## Usage Examples

### Example 1: Real-Time Information
```
User: "Ask Gemini about today's stock market"
Claude: Opens Gemini, asks about current market conditions.
        Returns: "Gemini reports: S&P 500 up 0.5%, tech sector
        leading gains, key movers include..."
```

### Example 2: Brainstorming
```
User: "Brainstorm with Gemini about app name ideas"
Claude: Opens Gemini, requests creative name ideas.
        Returns list of suggestions with rationale.
```

### Example 3: Cross-Reference
```
User: "Ask Gemini to verify this technical approach"
Claude: Sends technical question to Gemini.
        Returns: "Gemini suggests: [alternative perspective]"
```

### Example 4: Image Analysis
```
User: "Have Gemini analyze this screenshot"
Claude: Uploads image to Gemini, requests analysis.
        Returns Gemini's interpretation and insights.
```

## Authentication Flow
1. Claude navigates to gemini.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Interacts with chat interface

## Chat Workflow
```
1. Navigate to gemini.google.com
2. Enter query in chat input
3. Wait for response
4. Extract and return relevant information
5. Continue conversation if needed
```

## Selectors Reference
```javascript
// Chat input
'[aria-label="Enter a prompt here"]' or 'rich-textarea'

// Submit button
'[aria-label="Send message"]'

// Response container
'.model-response' or '.response-content'

// Copy response
'[aria-label="Copy"]'

// New chat
'[aria-label="New chat"]'

// Upload image
'[aria-label="Upload image"]'

// Voice input
'[aria-label="Voice input"]'

// Response actions
'.response-actions'
```

## When to Use Gemini Chat vs Claude
```
Use Gemini for:
- Real-time web information
- Current events and news
- Image analysis tasks
- Google ecosystem integrations
- Alternative AI perspectives

Stay with Claude for:
- Complex reasoning tasks
- Code development
- Long-form content creation
- LifeOS integrations
- Most general tasks
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Query Failed**: Retry, rephrase if needed
- **Response Timeout**: Wait and retry
- **Content Policy Block**: Note restriction, suggest alternatives
- **Rate Limited**: Wait and retry with backoff

## Self-Improvement Instructions
When you learn a better way to use Gemini Chat:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific query formulations that work better
4. Note when Gemini provides better results than alternatives

## Notes
- Gemini has real-time web access
- Responses may include citations and links
- Image upload supported for visual queries
- Voice input available for spoken queries
- Conversation history maintained within session
- Can switch between chat and other Gemini features
- Best for quick queries rather than complex workflows
- Use Deep Research for thorough investigation

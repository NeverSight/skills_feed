---
name: microsoft-copilot
description: Enables Claude to interact with Microsoft Copilot for AI assistance, search, and content generation via Playwright MCP
category: microsoft
---

# Microsoft Copilot Skill

## Overview
Claude can interact with Microsoft Copilot at copilot.microsoft.com for AI-powered assistance, web search, content generation, and getting alternative perspectives. Copilot combines GPT-4 with Bing search for up-to-date information.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-copilot/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-copilot ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MICROSOFT_EMAIL "your-email@outlook.com"
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
- Ask questions with real-time web search
- Generate creative content
- Analyze images
- Create images (DALL-E)
- Summarize web pages
- Code assistance
- Get research help
- Compare information
- Translate content
- Brainstorm ideas
- Explain complex topics
- Cross-reference with Claude's responses

## Usage Examples

### Example 1: Real-Time Search
```
User: "Ask Copilot about today's tech news"
Claude: Opens Copilot, asks about current tech news.
        Returns: "Copilot reports: Major announcements include
        [AI developments], [product launches]..."
```

### Example 2: Generate Content
```
User: "Have Copilot write a marketing tagline for our product"
Claude: Requests creative tagline from Copilot.
        Returns: "Copilot suggests: [several tagline options]"
```

### Example 3: Create Image
```
User: "Ask Copilot to generate a hero image for our landing page"
Claude: Requests image generation with description.
        Returns generated image or link to it.
```

### Example 4: Research Comparison
```
User: "Get Copilot's perspective on this technical approach"
Claude: Asks Copilot about the approach.
        Returns: "Copilot's analysis differs in [areas],
        agrees on [other areas]..."
```

## Authentication Flow
1. Claude navigates to copilot.microsoft.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for Copilot operations

## Copilot Workflow
```
1. Navigate to copilot.microsoft.com
2. Select conversation style if needed (Creative, Balanced, Precise)
3. Enter prompt in chat input
4. Wait for response
5. Extract and return relevant information
6. Continue conversation if needed
```

## Selectors Reference
```javascript
// Chat input
'#searchbox' or '[aria-label="Ask me anything"]'

// Submit button
'[aria-label="Submit"]'

// Response container
'.response-message'

// Conversation style
'.tone-selector'

// Creative mode
'[aria-label="More Creative"]'

// Precise mode
'[aria-label="More Precise"]'

// New chat
'[aria-label="New topic"]'

// Image generation
'.generated-image'

// Sources
'.source-links'
```

## Conversation Styles
```
Creative: More imaginative, less constrained
Balanced: Mix of creativity and accuracy
Precise: More factual, focused on accuracy
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Query Failed**: Retry, rephrase if content policy issue
- **Response Timeout**: Wait longer, retry
- **Image Generation Failed**: Retry with modified prompt
- **Rate Limited**: Wait and retry with backoff

## When to Use Copilot vs Claude
```
Use Copilot for:
- Real-time web search and news
- Image generation (DALL-E)
- Microsoft ecosystem integration
- Alternative AI perspective
- Bing search results

Stay with Claude for:
- Complex reasoning tasks
- Long-form content
- Code development
- LifeOS integrations
- Most general tasks
```

## Self-Improvement Instructions
When you learn a better way to use Microsoft Copilot:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific prompt formulations that work better
4. Note feature differences from other AI assistants

## Notes
- Copilot powered by GPT-4 and Bing
- Responses include source citations
- Image generation via DALL-E 3
- Conversation history maintained in session
- Plugins available for extended functionality
- Pro version offers more features
- Edge browser has integrated Copilot
- Works with Microsoft 365 apps (M365 Copilot)

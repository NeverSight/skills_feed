---
name: dall-e
description: Generate AI images with DALL-E - create images from text descriptions, edit existing images, and manage creations
category: ai
---

# DALL-E Skill

## Overview
Enables Claude to use OpenAI's DALL-E for AI image generation through ChatGPT's interface, including creating images from descriptions, editing images, and managing generated content.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/dall-e/install.sh | bash
```

Or manually:
```bash
cp -r skills/dall-e ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OPENAI_EMAIL "your-email@example.com"
canifi-env set OPENAI_PASSWORD "your-password"
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
- Generate images from text prompts
- Edit and modify existing images
- View generation history
- Download generated images
- Iterate on designs with variations
- Manage saved creations

## Usage Examples

### Example 1: Generate Image
```
User: "Create a DALL-E image of a cozy coffee shop interior"
Claude: I'll generate that image.
1. Opening ChatGPT via Playwright MCP
2. Activating DALL-E image generation
3. Entering prompt: "cozy coffee shop interior, warm lighting"
4. Waiting for image generation
5. Displaying and offering download
```

### Example 2: Edit Image
```
User: "Edit my image to add a cat sitting in the corner"
Claude: I'll edit your image.
1. Uploading your image to DALL-E
2. Specifying edit region
3. Adding prompt: "add a cat sitting in the corner"
4. Processing the edit
5. Showing the modified result
```

### Example 3: Multiple Variations
```
User: "Generate 4 different logo concepts for a tech startup"
Claude: I'll create logo variations.
1. Crafting detailed logo prompt
2. Generating first concept
3. Creating variations with different styles
4. Compiling all 4 concepts for review
```

## Authentication Flow
1. Navigate to chat.openai.com via Playwright MCP
2. Sign in with OpenAI account
3. Handle Google/Microsoft SSO if configured
4. Complete 2FA if required (via iMessage)
5. Maintain session for DALL-E access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Wait and retry with backoff
- **2FA Required**: Send iMessage notification
- **Content Policy**: Modify prompt and retry
- **Generation Failed**: Retry or simplify prompt

## Self-Improvement Instructions
When DALL-E or ChatGPT updates:
1. Document new generation capabilities
2. Update prompt optimization strategies
3. Track content policy changes
4. Log interface and feature changes

## Notes
- Requires ChatGPT Plus for DALL-E 3
- Content policies restrict certain prompts
- Generation credits may be limited
- Higher quality may take longer
- Downloaded images have metadata

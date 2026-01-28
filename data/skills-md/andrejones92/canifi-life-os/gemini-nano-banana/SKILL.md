---
name: gemini-nano-banana
description: Enables Claude to generate images, logos, and visual assets using Gemini's Nano Banana image generation
category: ai
---

# Gemini Nano Banana Skill

## Overview
Claude can use Gemini's Nano Banana feature (via gemini.google.com) to generate images, logos, icons, and visual assets. This is the primary tool for creating development assets, UI mockups, and graphic design elements.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gemini-nano-banana/install.sh | bash
```

Or manually:
```bash
cp -r skills/gemini-nano-banana ~/.canifi/skills/
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
- Generate logos and brand assets
- Create UI mockups and wireframes
- Design icons and graphics
- Produce illustrations
- Generate concept art
- Create marketing visuals
- Design social media graphics
- Generate avatars and characters
- Create infographics layouts
- Produce presentation visuals

## Usage Examples

### Example 1: Create Logo
```
User: "Create a logo for my app called 'TaskFlow'"
Claude: Opens Gemini, requests image generation:
        "Create a modern, minimalist logo for an app called TaskFlow.
        Use flowing lines and blue/green gradient colors."
        Downloads and provides the generated logo.
```

### Example 2: UI Mockup
```
User: "Generate a dashboard mockup for my fitness app"
Claude: Generates image with prompt:
        "Modern mobile app dashboard mockup for fitness tracking.
        Shows daily steps, calories, workout progress. Clean UI."
        Returns generated mockup image.
```

### Example 3: Icon Set
```
User: "Create icons for home, settings, and profile"
Claude: Generates each icon with consistent style:
        "Minimalist outline icon for [purpose], consistent style,
        suitable for mobile app navigation."
        Provides set of generated icons.
```

### Example 4: Marketing Graphic
```
User: "Make a social media banner for our product launch"
Claude: Generates banner with dimensions and style:
        "Social media banner 1200x628px for product launch.
        Modern design with product showcase, exciting colors."
```

## Authentication Flow
1. Claude navigates to gemini.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Accesses image generation feature

## Image Generation Process
```
1. Navigate to gemini.google.com
2. Enter image generation prompt
3. Wait for generation (typically 10-30 seconds)
4. Review generated options
5. Download preferred image(s)
6. Provide to user or save to project
```

## Selectors Reference
```javascript
// Chat input
'[aria-label="Enter a prompt here"]' or 'rich-textarea'

// Submit button
'[aria-label="Send message"]'

// Generated images
'.generated-image' or 'img[alt*="Generated"]'

// Download button
'[aria-label="Download"]'

// Regenerate button
'[aria-label="Regenerate"]'

// Image options
'.image-option'

// Response container
'.model-response'
```

## Prompt Best Practices
```
Logo Prompts:
- Specify style: minimalist, vintage, modern, playful
- Define colors: "blue and white", "gradient from X to Y"
- Mention use case: "for tech startup", "for mobile app"

UI Mockups:
- Specify device: mobile, tablet, desktop
- Describe layout: dashboard, list view, card layout
- Include content hints: what data should appear

Icons:
- Define style: outline, filled, flat, 3D
- Specify size context: "for navigation bar"
- Request consistency: "matching style to existing set"
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Generation Failed**: Retry with modified prompt
- **Content Policy Block**: Rephrase prompt to comply with policies
- **Download Failed**: Retry download, try alternative method
- **Quality Issues**: Regenerate with more specific prompt

## Self-Improvement Instructions
When you learn a better way to generate images with Gemini:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific prompt formulations that produce better results
4. Note any style keywords that work particularly well

## Notes
- Nano Banana is the designated tool for LifeOS asset creation
- Generated images may require multiple attempts for best results
- Be specific in prompts for better output quality
- Save generated assets to project directories
- Consider multiple variations for important assets
- Image generation subject to Google's content policies
- Higher quality prompts yield better results
- Can generate multiple options to choose from

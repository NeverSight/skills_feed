---
name: microsoft-powerpoint
description: Enables Claude to create, edit, and present Microsoft PowerPoint presentations via Playwright MCP
category: microsoft
---

# Microsoft PowerPoint Skill

## Overview
Claude can create and edit Microsoft PowerPoint Online presentations, including adding slides, inserting content, applying themes, adding animations, and managing presentation flow.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-powerpoint/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-powerpoint ~/.canifi/skills/
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
- Create new presentations from templates
- Add and arrange slides
- Insert text, images, and shapes
- Apply themes and designs
- Add transitions and animations
- Insert videos and audio
- Add speaker notes
- Create charts and SmartArt
- Export as PDF or video
- Present in slideshow mode
- Collaborate in real-time
- Use Designer suggestions

## Usage Examples

### Example 1: Create Presentation
```
User: "Create a PowerPoint about our product launch"
Claude: Creates presentation with title slide, agenda,
        product features, timeline, and call-to-action slides.
        Returns: "Created 6-slide presentation: [link]"
```

### Example 2: Apply Theme
```
User: "Make the presentation look more corporate"
Claude: Opens Design tab, applies professional theme,
        adjusts colors to corporate palette.
        Confirms: "Corporate theme applied to all slides"
```

### Example 3: Add Animation
```
User: "Add entrance animations to the key points"
Claude: Selects text elements, applies Fade In animation,
        sequences for presentation flow.
        Confirms: "Animations added to key points"
```

### Example 4: Add Chart
```
User: "Insert a bar chart on slide 3 with our quarterly data"
Claude: Opens slide 3, inserts bar chart, enters data.
        Confirms: "Bar chart added to slide 3"
```

## Authentication Flow
1. Claude navigates to powerpoint.office.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for presentation operations

## Selectors Reference
```javascript
// New presentation
'[aria-label="New blank presentation"]'

// Presentation name
'[aria-label="Presentation name"]'

// Slide thumbnails
'.slide-thumbnails'

// Current slide
'.slide-container'

// New slide button
'[aria-label="New slide"]'

// Insert tab
'[aria-label="Insert"]'

// Design tab
'[aria-label="Design"]'

// Animations tab
'[aria-label="Animations"]'

// Text box
'[aria-label="Text box"]'

// Shape button
'[aria-label="Shapes"]'

// Speaker notes
'[aria-label="Notes"]'

// Present button
'[aria-label="Present"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Presentation Not Found**: Search OneDrive, ask for clarification
- **Image Insert Failed**: Check URL/file, retry
- **Theme Apply Failed**: Retry, suggest alternatives
- **Animation Failed**: Retry, check element selection

## Self-Improvement Instructions
When you learn a better way to accomplish a task with PowerPoint Online:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific design tips for better presentations
4. Note differences from desktop PowerPoint

## Notes
- PowerPoint Online auto-saves to OneDrive
- Designer provides AI-powered layout suggestions
- Real-time collaboration shows other users
- Transitions and animations supported
- Export to video limited in online version
- Maximum file size: varies by subscription
- Templates available from Start screen
- Presenter view available during slideshow

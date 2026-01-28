---
name: google-slides
description: Enables Claude to create, edit, and present Google Slides presentations via Playwright MCP
category: google
---

# Google Slides Skill

## Overview
Claude can create and edit Google Slides presentations, including adding slides, inserting content, applying themes, adding animations, and managing presentation flow. Perfect for building decks, reports, and visual content.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-slides/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-slides ~/.canifi/skills/
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
- Create new presentations from scratch or templates
- Add and arrange slides
- Insert text, images, shapes, and charts
- Apply themes and customize designs
- Add speaker notes
- Create transitions and animations
- Insert videos and audio
- Link slides and create navigation
- Export as PDF, PPTX, or images
- Present in slideshow mode
- Collaborate with comments and suggestions

## Usage Examples

### Example 1: Create Presentation
```
User: "Create a presentation about our Q4 results"
Claude: Creates new presentation with title slide "Q4 Results",
        adds slides for Key Metrics, Revenue, Growth, Next Steps.
        Returns: "Created presentation with 5 slides: [link]"
```

### Example 2: Add Content to Slide
```
User: "Add a bar chart showing monthly sales to slide 3"
Claude: Navigates to slide 3, inserts chart, configures as bar chart,
        enters sales data. Confirms: "Bar chart added to slide 3"
```

### Example 3: Apply Theme
```
User: "Make the presentation look more professional with a dark theme"
Claude: Opens Themes panel, selects dark professional theme,
        applies to all slides. Reports: "Dark theme applied to all slides"
```

### Example 4: Add Speaker Notes
```
User: "Add speaker notes to the introduction slide"
Claude: Opens slide 1, clicks speaker notes area, adds talking points
        based on slide content. Confirms: "Speaker notes added"
```

## Authentication Flow
1. Claude navigates to slides.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent operations

## Selectors Reference
```javascript
// New presentation button
'#punch-start-presentation-chrome'

// Presentation title
'.docs-title-input'

// Slide filmstrip
'.punch-filmstrip'

// Current slide canvas
'.punch-viewer-content'

// Add slide button
'[aria-label="New slide"]'

// Insert menu
'#docs-insert-menu'

// Slide menu
'#docs-slide-menu'

// Theme button
'.punch-theme-button'

// Speaker notes
'.punch-viewer-speakernotes-text'

// Present button
'#punch-start-presentation-button'

// Shape insertion
'[aria-label="Shape"]'

// Text box
'[aria-label="Text box"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Presentation Not Found**: Search Drive, ask user to clarify
- **Image Insert Failed**: Check URL validity, try alternative upload method
- **Theme Apply Failed**: Retry, suggest manual theme selection
- **Export Failed**: Try alternative format, notify user

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Slides:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific menu paths or shortcuts that work better
4. Note any layout tips for better presentations

## Notes
- Google Slides auto-saves changes
- Maximum image size: 25MB per image
- Supported image formats: JPG, PNG, GIF, BMP, WebP
- Keyboard shortcuts: Ctrl+M for new slide, Ctrl+D to duplicate
- Present mode: F5 or Ctrl+F5 for presenter view
- Collaboration shows other users' cursors in real-time
- Templates available in the template gallery

---
name: create-ppt-with-nano-banana
description: Create PowerPoint presentations with AI-generated images. Use when user wants to create a presentation, make slides, build a pptx, or needs AI images for slides using x402 payments.
---

# Create PowerPoint Presentation with Nano Banana (x402)

Create visually appealing PowerPoint presentations by converting styled HTML slides to PPTX format using Playwright and PptxGenJS, with AI-generated images via the Nano Banana API using x402 payments.

## Overview

This skill converts HTML slides to PowerPoint with:
- Precise positioning and styling
- Dark theme with modern color palette
- Support for shapes, text, images, and diagrams
- Automatic validation of slide dimensions and content placement
- **AI-generated images** (optional) using Nano Banana API with x402 micropayments (0.1 USDC per image)

## Behavior

When this skill is triggered:

1. **Get presentation topic** from the user if not specified
2. **Ask if they want AI-generated images** using `AskUserQuestion`:
   - "Do you want to generate AI images with Nano Banana? (0.1 USDC per image via x402)"
   - Options: "Yes, generate images" / "No, use solid colors only"
3. **If AI images requested**:
   - Make x402 payment: see `./fluxa-wallet/x402-payment.md`
   - Call Nano Banana API with X-Payment header
   - Download and save images to slides directory
4. **Create HTML slides** using templates
5. **Build PPTX** using html2pptx.js
6. **Open the presentation** for the user

## Agent Config

The FluxA Wallet agent JWT is stored at:
```
~/.fluxa-ai-wallet-mcp/.agent-config.json
```

This config contains the agent_id, token, and JWT needed for x402 payment authorization.

## AI Image Generation via x402

When you need to generate images for slides, use the Nano Banana API with x402 payment.

### API Details

- **Endpoint:** `https://proxy-monetize.fluxapay.xyz/api/b7da8911-ab69-4577-9d90-f9ae6ca34bfa/gen-image`
- **Method:** POST
- **Price:** 0.1 USDC per image (Base network)
- **Payment:** x402 protocol with FluxA Wallet

### Request Format

```json
{
  "contents": [{
    "parts": [{"text": "Your image generation prompt here"}]
  }]
}
```

### Response Format

The API returns a Gemini-style response with the image either as:
1. **Inline base64:** `response.candidates[0].content.parts[1].inlineData.data`
2. **URL reference:** `response.candidates[0].content.parts[1].inlineData.url`

### Example Flow

1. Get payment signature from FluxA Wallet API
2. Call Nano Banana API with X-Payment header
3. Extract image from response (base64 or URL)
4. Save image to slides directory
5. Reference image in HTML slide

### Image Prompt Templates

**Slide Background:**
```
Create an abstract futuristic background image for a presentation slide.
Theme: [TOPIC]
Style: Dark theme with #0f0f1a background color.
Elements: Abstract flowing digital elements, subtle geometric patterns, particles of light.
Color accents: Use hints of #667eea, #00d4ff, and #764ba2.
Mood: Professional, modern technology, clean and elegant.
The image should be subtle enough to work as a background with text overlaid on top.
Dimensions: Wide format suitable for a 16:9 presentation slide.
No text, logos, or words in the image.
```

**Icon/Illustration:**
```
Create a minimalist icon representing: [CONCEPT].
Style: Clean, professional, suitable for a business presentation.
Background: Transparent or dark (#0f0f1a).
Colors: Use blues (#667eea, #00d4ff) and purples (#764ba2) on dark background.
Size: Square format, simple and recognizable.
No text in the image.
```

## HTML Slide Requirements

### Dimensions (16:9 format)
```css
body {
    margin: 0;
    padding: 0;
    width: 720pt;
    height: 405pt;
}
```

### Critical Rules

1. **Text must be wrapped** - All text MUST be in `<p>`, `<h1>`-`<h6>`, `<ul>`, or `<ol>` tags
2. **Borders on divs only** - Backgrounds, borders, shadows only work on `<div>` elements
3. **No CSS gradients** - Use solid colors or pre-rendered PNG images
4. **Bottom margin** - Keep text at least 36pt (0.5") from bottom edge
5. **Safe fonts only** - Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma

### Using Generated Images in Slides

```html
<body>
    <!-- Background image with opacity -->
    <img class="background-image" src="background.png"
         style="position:absolute; top:0; left:0; width:720pt; height:405pt; opacity:0.6;" />

    <!-- Content on top -->
    <div class="content">
        <h1 class="title">Your Title</h1>
    </div>
</body>
```

## Color Palette

```css
/* Dark Theme */
--bg-primary: #0f0f1a;
--bg-card: rgba(255, 255, 255, 0.05);

/* Accents */
--accent-blue: #667eea;
--accent-cyan: #00d4ff;
--accent-purple: #764ba2;

/* Text */
--text-white: #ffffff;
--text-light: #d0d0d0;
--text-muted: #a0a0b0;
```

## Available Templates

- `title.html` - Title slide with tagline, title, subtitle, and description
- `bullets.html` - Bullet point list (5 items)
- `two-columns.html` - Side-by-side comparison with headers
- `cards-2x2.html` - 2x2 card grid layout
- `cards-3x2.html` - 3x2 card grid layout (6 cards)
- `stats.html` - Large metrics display (3 stats)
- `section.html` - Section divider with number
- `architecture.html` - Layered architecture diagram (4 layers)
- `features.html` - Feature list with accent bars (6 features)
- `flow.html` - Step-by-step process flow (4 steps with arrows)

## Usage

```bash
# Install dependencies
npm install pptxgenjs playwright sharp

# Create slides directory with HTML files
mkdir slides

# Generate presentation
node scripts/create-pptx.js

# Open result (macOS)
open output.pptx
```

## Files

- `scripts/html2pptx.js` - Core HTML-to-PPTX converter
- `scripts/create-pptx.js` - Build script
- `templates/*.html` - Slide templates
- `SKILL.md` - This documentation

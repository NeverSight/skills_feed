---
name: illustrated-slides-with-nano-banana
description: Create PowerPoint/PDF presentations where each slide is a complete AI-generated image with all text embedded. Supports multiple visual styles (corporate, minimalist, creative, kawaii, custom). Use when user wants fully-illustrated slides, visual-first decks, or AI-generated presentation images via x402 payments.
---

# Illustrated Slides with Nano Banana

Create presentations where **each slide is a complete AI-generated image** with all text and content embedded directly in the image. No separate text layers — the presentation file is simply a container for full-page illustrated slides. Supports multiple visual styles from corporate to creative.

## Key Principle

> **All content is embedded in the images.**

Unlike traditional presentations with text overlays, this skill generates complete slide images where titles, bullet points, diagrams, and illustrations are all part of the generated image itself - like pages in a children's picture book.

## Behavior

When this skill is triggered:

### 1. Get Presentation Topic
Ask the user for their presentation topic if not specified.

### 2. Ask for Visual Style
**Always ask the user to choose a style:**

```
🎨 What visual style would you like?

1️⃣ **Kawaii / Children's Book**
   Warm pastels, cream background, cute characters with faces
   Best for: Kids content, educational, playful topics

2️⃣ **Professional / Corporate**  
   Clean blues & grays, white background, modern icons
   Best for: Business, finance, tech presentations

3️⃣ **Bold / Creative**
   Vibrant colors, dynamic compositions, artistic flair
   Best for: Marketing, startups, creative pitches

4️⃣ **Minimalist / Elegant**
   Black & white with one accent, lots of whitespace
   Best for: Luxury brands, design, architecture

5️⃣ **Custom**
   Describe your own style preference

Which style would you like? (1-5)
```

### 3. Plan Slide Structure
Based on topic, plan ~8-12 slides:
- Title slide
- Introduction/Chapter slides
- Content slides (with embedded text & illustrations)
- Diagram/flow slides
- Summary/statistics slides  
- Closing slide

### 4. Estimate Budget & Request Approval
- Each image: **0.1 USDC**
- Recommend 1.5x buffer
- Tell user: *"To create this presentation with X slides, I need a budget of Y USDC."*

### 5. Generate Slide Images
For each slide:
1. Get x402 payment signature
2. Generate image with ALL content embedded (title, text, illustrations)
3. Download and save image
4. Repeat for all slides

### 6. Assemble Presentation
- Create PPTX with one full-page image per slide
- Optionally export as PDF
- Open for user review

## AI Image Generation via x402

### API Details

- **Endpoint:** `https://proxy-monetize.fluxapay.xyz/api/b7da8911-ab69-4577-9d90-f9ae6ca34bfa/gen-image`
- **Method:** POST
- **Price:** 0.1 USDC per image (Base network)
- **Payment:** x402 protocol with FluxA Wallet

### Payment Flow

See `./fluxa-wallet/x402-payment.md` for the x402 payment process.

### Request Format

```json
{
  "contents": [{
    "parts": [{"text": "Your detailed slide prompt here"}]
  }]
}
```

### Response Format

Image URL at: `response.candidates[0].content.parts[1].inlineData.url`

---

## Style Guide & Prompts

### Style 1: Kawaii / Children's Book

**Color Palette:**
- Background: `#F5F0E6` (warm cream)
- Titles: `#D35D4E` (coral red)
- Cards: `#E8A095` (coral), `#A8DCD1` (mint), `#E5C88E` (mustard), `#F5D5C8` (peach)
- Body text: `#5C4A3D` (warm brown)

**Prompt Template:**
```
Create a children's book illustration slide.

Title: "[TITLE]" in large friendly coral-red text at top.

Content: [DESCRIBE WHAT SHOULD BE SHOWN]

Style requirements:
- Kawaii/cute aesthetic with warm pastels
- Cream background (#F5F0E6)
- Characters have simple dot eyes and rosy cheeks
- Hand-drawn, friendly illustration style
- Include decorative elements: stars, dots, sparkles
- All text must be part of the image (embedded, not overlay)
- 16:9 aspect ratio suitable for presentation slide
```

---

### Style 2: Professional / Corporate

**Color Palette:**
- Background: `#FFFFFF` or `#F7FAFC` (white/light gray)
- Titles: `#1A365D` (navy blue)
- Accents: `#3182CE` (blue), `#48BB78` (green)
- Body text: `#2D3748` (dark gray)

**Prompt Template:**
```
Create a professional business presentation slide.

Title: "[TITLE]" in clean navy blue text at top.

Content: [DESCRIBE WHAT SHOULD BE SHOWN]

Style requirements:
- Clean, corporate aesthetic
- White or light gray background
- Modern sans-serif typography
- Simple flat icons and minimal illustrations
- Professional color scheme: navy, blue, white, gray
- All text must be part of the image (embedded, not overlay)
- 16:9 aspect ratio suitable for presentation slide
```

---

### Style 3: Bold / Creative

**Color Palette:**
- Background: `#1A1A2E` (dark) or gradients
- Titles: `#FF6B6B` (coral) or `#4ECDC4` (teal)
- Accents: `#FFE66D` (yellow), `#95E1D3` (mint), `#F38181` (pink)
- Text: `#FFFFFF` (white)

**Prompt Template:**
```
Create a bold, creative presentation slide.

Title: "[TITLE]" in large dynamic text with creative typography.

Content: [DESCRIBE WHAT SHOULD BE SHOWN]

Style requirements:
- Vibrant, energetic aesthetic
- Bold color combinations: electric blue, hot pink, bright yellow
- Dynamic compositions with visual interest
- Creative illustrations with personality
- Dark or gradient background for contrast
- All text must be part of the image (embedded, not overlay)
- 16:9 aspect ratio suitable for presentation slide
```

---

### Style 4: Minimalist / Elegant

**Color Palette:**
- Background: `#FFFFFF` (white)
- Titles: `#000000` (black)
- Accent: `#C9A227` (gold) or `#1A4D2E` (deep green)
- Body text: `#333333` (dark gray)

**Prompt Template:**
```
Create a minimalist, elegant presentation slide.

Title: "[TITLE]" in refined serif typography.

Content: [DESCRIBE WHAT SHOULD BE SHOWN]

Style requirements:
- Minimal and sophisticated aesthetic
- Clean white background with generous whitespace
- Limited color palette: black, white, one accent color
- Thin lines and simple geometric shapes
- Luxurious, refined feel
- All text must be part of the image (embedded, not overlay)
- 16:9 aspect ratio suitable for presentation slide
```

---

## Slide Type Templates

### Title Slide
```
Create a [STYLE] title slide.

Main title: "[TITLE]" - large and prominent
Subtitle: "[SUBTITLE]" - smaller, below main title

Visual: [MAIN ILLUSTRATION relevant to topic]

[STYLE-SPECIFIC REQUIREMENTS]
All text embedded in image. 16:9 ratio.
```

### Content Slide (with points)
```
Create a [STYLE] content slide.

Title: "[TITLE]" at top

Show [NUMBER] key points with icons/illustrations:
1. [POINT 1] - with [visual element]
2. [POINT 2] - with [visual element]  
3. [POINT 3] - with [visual element]
...

Arrange in [grid/list/cards] layout.

[STYLE-SPECIFIC REQUIREMENTS]
All text embedded in image. 16:9 ratio.
```

### Diagram / Flow Slide
```
Create a [STYLE] diagram slide.

Title: "[TITLE]" at top

Show a [horizontal/vertical] flow diagram:
Step 1: [LABEL] → Step 2: [LABEL] → Step 3: [LABEL] → Step 4: [LABEL]

Each step has an icon and text label.
Connect with arrows or dotted lines.

[STYLE-SPECIFIC REQUIREMENTS]
All text embedded in image. 16:9 ratio.
```

### Comparison Slide
```
Create a [STYLE] comparison slide.

Title: "[TITLE]" at top

LEFT column: "[LEFT HEADER]"
- [Item 1]
- [Item 2]
- [Item 3]

RIGHT column: "[RIGHT HEADER]"
- [Item 1]
- [Item 2]
- [Item 3]

Clear visual separation between columns.

[STYLE-SPECIFIC REQUIREMENTS]
All text embedded in image. 16:9 ratio.
```

### Statistics Slide
```
Create a [STYLE] statistics slide.

Title: "[TITLE]" at top

Display [NUMBER] impressive statistics:
- "[NUMBER 1]" with label "[LABEL 1]" and icon
- "[NUMBER 2]" with label "[LABEL 2]" and icon
- "[NUMBER 3]" with label "[LABEL 3]" and icon

Make numbers visually prominent and impactful.

[STYLE-SPECIFIC REQUIREMENTS]
All text embedded in image. 16:9 ratio.
```

### Closing Slide
```
Create a [STYLE] closing/ending slide.

Main text: "[CLOSING MESSAGE]" - prominent
Tagline: "[TAGLINE]" at bottom

Visual: [CELEBRATION/CONCLUSION imagery]

Warm, conclusive, memorable feel.

[STYLE-SPECIFIC REQUIREMENTS]
All text embedded in image. 16:9 ratio.
```

---

## Building the Presentation

### Simple PPTX Builder

```javascript
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

async function buildImagePresentation(slidesDir, outputPath) {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    
    // Get slide images in order (01-*.png, 02-*.png, etc.)
    const slides = fs.readdirSync(slidesDir)
        .filter(f => f.endsWith('.png') && f.match(/^\d{2}-/))
        .sort();
    
    for (const file of slides) {
        const slide = pptx.addSlide();
        slide.addImage({
            path: path.join(slidesDir, file),
            x: 0, y: 0,
            w: '100%', h: '100%',
            sizing: { type: 'contain', w: '100%', h: '100%' }
        });
    }
    
    await pptx.writeFile({ fileName: outputPath });
    console.log(`Saved: ${outputPath}`);
}
```

### File Naming Convention

Name slide images with numeric prefixes for ordering:
```
01-title.png
02-intro.png
03-content-1.png
04-content-2.png
...
10-ending.png
```

---

## Dependencies

### Local Files
- `fluxa-wallet/` - x402 payment documentation and scripts
  - `x402-payment.md` - Payment flow documentation
  - `initialize-agent-id.md` - Agent ID setup
  - `error-handle.md` - Error handling guide
  - `scripts/fluxa-cli.bundle.js` - CLI for mandate-based payments
- `scripts/` - Build scripts for this skill

### NPM Package
```bash
npm install pptxgenjs
```

### Agent Config
JWT stored at: `~/.fluxa-ai-wallet-mcp/config.json`

```javascript
const jwt = require(os.homedir() + '/.fluxa-ai-wallet-mcp/config.json').agentId.jwt;
```

---

## Summary

| Aspect | This Skill | Original Skill |
|--------|------------|----------------|
| Slide content | All embedded in images | HTML with text overlays |
| Text handling | Part of AI-generated image | Separate HTML elements |
| Style | User chooses from 5 options | Dark tech theme |
| Best for | Visual presentations, kids content | Technical presentations |
| Output | PPTX/PDF with full-page images | PPTX from HTML conversion |

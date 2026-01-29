---
name: slide-generation
description: >
  Use this skill to create presentation slides from structured content.
  Triggers: "create slides", "generate presentation", "make powerpoint", "create pptx",
  "build slides", "presentation from content", "slide deck", "slides for"
  Outputs: PPTX files, Markdown slides, or HTML presentations.
  Used by: pitch-deck-agent, market-researcher-agent, and other agents needing slides.
---

# Slide Generation Skill

Create presentation slides from structured content.

**This is a low-level generation skill** that other agents use to create actual slide files.

## What It Creates

| Format | Method | Best For |
|--------|--------|----------|
| **PPTX** | `python-pptx` library | PowerPoint, Google Slides import |
| **Markdown** | Marp/Slidev format | Developer presentations |
| **HTML** | Reveal.js template | Web-based presentations |

## Prerequisites

```bash
# Required for PPTX generation
pip install python-pptx Pillow

# Optional for Markdown slides
npm install -g @marp-team/marp-cli
```

## Usage

### Script: `slides.py`

```bash
# Basic slide creation
python slides.py --content slides.json --output presentation.pptx

# With theme
python slides.py --content slides.json --theme modern-dark --output deck.pptx

# Markdown output
python slides.py --content slides.json --format markdown --output slides.md
```

### Input Format: `slides.json`

```json
{
  "metadata": {
    "title": "Presentation Title",
    "author": "Author Name",
    "theme": "modern-dark"
  },
  "slides": [
    {
      "type": "title",
      "title": "Main Title",
      "subtitle": "Subtitle or tagline",
      "image": "logo.png"
    },
    {
      "type": "content",
      "title": "Slide Title",
      "bullets": [
        "First point",
        "Second point",
        "Third point"
      ],
      "notes": "Speaker notes for this slide"
    },
    {
      "type": "image",
      "title": "Visual Slide",
      "image": "chart.png",
      "caption": "Optional caption"
    },
    {
      "type": "two-column",
      "title": "Comparison",
      "left": {
        "heading": "Before",
        "bullets": ["Point 1", "Point 2"]
      },
      "right": {
        "heading": "After",
        "bullets": ["Point 1", "Point 2"]
      }
    },
    {
      "type": "quote",
      "quote": "This is a customer testimonial or important quote.",
      "attribution": "- Customer Name, Company"
    },
    {
      "type": "stats",
      "title": "Key Metrics",
      "stats": [
        {"value": "10x", "label": "Faster"},
        {"value": "50%", "label": "Cost Savings"},
        {"value": "1M+", "label": "Users"}
      ]
    }
  ]
}
```

---

## Slide Types

### 1. Title Slide
```json
{
  "type": "title",
  "title": "Company Name",
  "subtitle": "Tagline goes here",
  "image": "logo.png",
  "date": "January 2026"
}
```

### 2. Content Slide (Bullets)
```json
{
  "type": "content",
  "title": "Slide Title",
  "bullets": ["Point 1", "Point 2", "Point 3"],
  "image": "optional-side-image.png",
  "notes": "Speaker notes"
}
```

### 3. Image Slide
```json
{
  "type": "image",
  "title": "Product Screenshot",
  "image": "screenshot.png",
  "caption": "Our new dashboard"
}
```

### 4. Two-Column Slide
```json
{
  "type": "two-column",
  "title": "Before & After",
  "left": {"heading": "Before", "bullets": ["Problem 1"]},
  "right": {"heading": "After", "bullets": ["Solution 1"]}
}
```

### 5. Quote Slide
```json
{
  "type": "quote",
  "quote": "This product changed our business.",
  "attribution": "- CEO, Fortune 500 Company",
  "image": "headshot.png"
}
```

### 6. Stats Slide
```json
{
  "type": "stats",
  "title": "By the Numbers",
  "stats": [
    {"value": "10x", "label": "Faster"},
    {"value": "$1M", "label": "Saved"}
  ]
}
```

### 7. Chart Slide
```json
{
  "type": "chart",
  "title": "Market Size",
  "chart_type": "bar",
  "data": {
    "labels": ["TAM", "SAM", "SOM"],
    "values": [50, 10, 2]
  }
}
```

### 8. Section Divider
```json
{
  "type": "section",
  "title": "Part 2: The Solution"
}
```

### 9. Closing Slide
```json
{
  "type": "closing",
  "title": "Thank You",
  "subtitle": "Questions?",
  "contact": "email@company.com"
}
```

---

## Themes

| Theme | Description |
|-------|-------------|
| `modern-dark` | Dark background, light text, bold accents |
| `modern-light` | Light background, clean minimalist |
| `corporate` | Professional, blue tones |
| `startup` | Bold colors, energetic |
| `minimal` | Maximum whitespace, typography focus |

### Custom Theme
```json
{
  "theme": {
    "background": "#1a1a2e",
    "text": "#ffffff",
    "accent": "#e94560",
    "heading_font": "Montserrat",
    "body_font": "Open Sans"
  }
}
```

---

## Integration with Other Skills

### pitch-deck-agent workflow:
```
1. pitch-deck-agent generates slide content as JSON
2. Calls image-generation for visuals
3. Calls slide-generation to create PPTX
4. Returns actual .pptx file
```

### market-researcher-agent workflow:
```
1. market-researcher-agent creates market report
2. Converts report to slide format
3. Calls slide-generation for presentation
4. Returns market-report.pptx
```

---

## Output

```
✅ Presentation created: presentation.pptx
   Slides: 12
   Theme: modern-dark
   Images: 5 embedded

Open with:
- Microsoft PowerPoint
- Google Slides (import)
- LibreOffice Impress
```

---

## Limitations

- Charts are basic (for complex charts, use image-generation)
- Animations not supported (static slides only)
- Custom layouts require theme customization
- Large images are resized to fit

## For Advanced PowerPoint Operations

For more complex PowerPoint tasks, use the **[pptx skill](../pptx/)** which supports:
- Editing existing presentations (OOXML)
- Working with templates (duplicate, rearrange, replace)
- HTML → PowerPoint conversion
- Advanced layout and typography control
- Comments and speaker notes

---

## Example Prompts

**From other agents:**
> `slide-generation` is called programmatically, not directly by users

**Direct use:**
> "Create slides from this content: [paste JSON]"
> "Generate a PowerPoint from my outline"

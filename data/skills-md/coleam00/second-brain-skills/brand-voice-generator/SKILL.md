---
name: brand-voice-generator
description: |
  Generate tone-of-voice and brand-system files for use with the PPTX Generator and other brand-aware skills.

  TRIGGERS - Use this skill when user says:
  - "help me create a brand system" / "set up my brand"
  - "generate my tone of voice" / "create my voice guidelines"
  - "configure my brand for presentations" / "set up brand for slides"
  - "create brand files" / "initialize my brand"
  - Any request about defining brand identity, voice, or visual system for content creation

  Creates brand.json, config.json, brand-system.md, and tone-of-voice.md files.
---

# Brand & Voice Generator

Generate complete brand configuration files for use with the PPTX Generator and other brand-aware skills. This skill guides users through an interactive process to define their brand identity and writing voice.

## What This Creates

| File | Purpose | Used By |
|------|---------|---------|
| `brand.json` | Colors, fonts, assets | PPTX Generator, Excalidraw |
| `config.json` | Output settings | PPTX Generator |
| `brand-system.md` | Design philosophy & guidelines | All content skills |
| `tone-of-voice.md` | Writing voice & personality | LinkedIn, X, PPTX content |

## Output Location

Files are created in:
```
.claude/skills/pptx-generator/brands/{brand-name}/
```

---

## Process Overview

1. **Gather Brand Basics** - Name, description, primary use case
2. **Define Colors** - 10 color values for the complete system
3. **Define Typography** - Heading, body, and code fonts
4. **Define Assets** - Logo and icon paths
5. **Discover Voice** - Personality, vocabulary, sentence patterns
6. **Create Design Philosophy** - Core principles and signature elements
7. **Generate Files** - Create all four files with gathered information
8. **Verify Setup** - Confirm files are correctly placed

---

## Step 1: Gather Brand Basics

Ask the user for:

| Field | Description | Example |
|-------|-------------|---------|
| **Brand name** | Folder name (lowercase, no spaces, hyphens OK) | `my-brand`, `acme-corp` |
| **Display name** | Human-readable name | "My Brand", "ACME Corporation" |
| **Description** | One-line brand description | "AI education content and community" |
| **Primary use** | Main content type | presentations, social media, documentation |

**Suggested question:**
> "Let's set up your brand. What's your brand name? (This will be the folder name - use lowercase with hyphens, like 'my-brand')"

---

## Step 2: Define Colors

Gather 10 color values. Colors should be hex codes WITHOUT the `#` prefix.

### Required Colors

| Color | Purpose | Guidance |
|-------|---------|----------|
| `background` | Main slide/page background | Dark themes: near-black. Light themes: white/off-white |
| `background_alt` | Alternate background for variety | Slightly different shade of background |
| `text` | Primary text color | High contrast against background |
| `text_secondary` | Muted/secondary text | Slightly lower contrast than primary |
| `accent` | Primary accent (CTAs, highlights) | Your signature brand color |
| `accent_secondary` | Secondary accent | Complement to primary accent |
| `accent_tertiary` | Third accent (optional variety) | Another complement, or same as secondary |
| `code_bg` | Code block background | Darker than main background |
| `card_bg` | Card/surface background | Between background and text |
| `card_bg_alt` | Alternate card background | Slight variation of card_bg |

### Color Discovery Questions

If user doesn't have a full color system, guide them:

1. "What's your signature brand color? (This becomes your primary accent)"
2. "Do you prefer a dark theme (dark background, light text) or light theme?"
3. "Do you have secondary colors, or should I suggest complements?"

### Color Suggestions by Theme

**For dark themes**, suggest:
```
background: 0a0a0a to 1a1a2e range
text: f5f5f5 to ffffff range
card_bg: 1a1a1a to 2d2d44 range
```

**For light themes**, suggest:
```
background: ffffff to f8f9fa range
text: 1a1a1a to 333333 range
card_bg: f0f0f0 to e8e8e8 range
```

---

## Step 3: Define Typography

Gather 3 font names:

| Font | Purpose | Common Choices |
|------|---------|----------------|
| `heading` | Headlines, titles, buttons | Inter, Montserrat, Poppins, Roboto |
| `body` | Body text, descriptions | Inter, Open Sans, Lato, Source Sans Pro |
| `code` | Code blocks, terminal | JetBrains Mono, Fira Code, Monaco, Consolas |

**Question:**
> "What fonts should we use? I need a heading font, body font, and code/monospace font. Common choices are Inter for both heading and body, and JetBrains Mono for code."

**Default if unsure:**
- Heading: Inter
- Body: Inter
- Code: JetBrains Mono

---

## Step 4: Define Assets

Gather asset paths (relative to brand folder):

| Asset | Description | Common |
|-------|-------------|--------|
| `logo` | Primary logo file | `assets/logo.png` |
| `logo_dark` | Logo variant for dark backgrounds (optional) | `null` or `assets/logo-dark.png` |
| `icon` | Square icon (optional) | `null` or `assets/icon.png` |

**Question:**
> "Do you have a logo file? If so, you'll need to copy it to the brand folder. What's the filename? (e.g., 'logo.png')"

If they have a logo, set path to `assets/logo.png` (they'll copy it there).
If no logo, set to `null`.

---

## Step 5: Discover Voice

This is the most important step for content quality. Guide the user through voice discovery.

### Voice Discovery Questions

Ask these questions to understand their voice:

1. **Personality in 3 words:**
   > "Describe your brand's personality in exactly 3 words. Examples: 'Bold, Technical, Approachable' or 'Calm, Authoritative, Helpful'"

2. **Voice influences:**
   > "Who are 2-3 creators, brands, or people whose communication style you admire? This helps me understand the vibe."

3. **Vocabulary patterns:**
   > "What words or phrases do you use often? Any pet phrases, intensifiers you like ('super', 'incredibly'), or words you naturally reach for?"

4. **What to avoid:**
   > "What kind of tone or phrases do you want to AVOID? (e.g., corporate speak, hype language, overly casual)"

5. **Sentence style:**
   > "Do you prefer: Short punchy sentences, longer flowing explanations, or a mix? Do you use contractions ('don't', 'can't') casually?"

6. **Teaching style (if applicable):**
   > "When explaining something complex, how do you approach it? Show process/iterations? Use analogies? Lead with practical then theory?"

### Voice Templates Reference

Read `references/voice-templates.md` for example voice configurations to show the user.

---

## Step 6: Create Design Philosophy

Based on gathered information, help define:

### Core Principles (3-4)

Ask:
> "What are 3-4 design principles that guide your visual choices? For example: 'Clean over flashy', 'Technical but approachable', 'Dark mode by default'"

### Signature Elements

Ask:
> "Do you have any signature visual elements? Examples: Glass card effects, specific shadow styles, gradient patterns, geometric shapes, glow effects"

If unsure, suggest based on their colors and theme.

---

## Step 7: Generate Files

Create all four files using the gathered information.

### brand.json

```json
{
  "name": "{display_name}",
  "description": "{description}",

  "colors": {
    "background": "{background}",
    "background_alt": "{background_alt}",
    "text": "{text}",
    "text_secondary": "{text_secondary}",
    "accent": "{accent}",
    "accent_secondary": "{accent_secondary}",
    "accent_tertiary": "{accent_tertiary}",
    "code_bg": "{code_bg}",
    "card_bg": "{card_bg}",
    "card_bg_alt": "{card_bg_alt}"
  },

  "fonts": {
    "heading": "{heading_font}",
    "body": "{body_font}",
    "code": "{code_font}"
  },

  "assets": {
    "logo": "{logo_path}",
    "logo_dark": {logo_dark_path},
    "icon": {icon_path}
  }
}
```

### config.json

```json
{
  "output": {
    "directory": "output/{brand_name}",
    "naming": "{name}-{date}",
    "keep_parts": false
  },
  "generation": {
    "slides_per_batch": 5,
    "auto_combine": true,
    "open_after_generate": false
  },
  "defaults": {
    "slide_width_inches": 13.333,
    "slide_height_inches": 7.5
  }
}
```

### tone-of-voice.md

Use the template in `references/tone-template.md` and fill with gathered voice information.

### brand-system.md

Use the template in `references/brand-template.md` and fill with gathered design information.

---

## Step 8: Verify Setup

After generating files:

1. **List created files:**
   ```
   Glob: .claude/skills/pptx-generator/brands/{brand-name}/*
   ```

2. **Remind about assets:**
   > "Don't forget to copy your logo file to `.claude/skills/pptx-generator/brands/{brand-name}/assets/`"

3. **Suggest test:**
   > "Try generating a simple presentation with: 'Create a 3-slide presentation for {brand-name} about [topic]'"

---

## Quick Mode

If user just wants to get started quickly:

1. Ask only for: brand name, signature color, and light/dark preference
2. Generate sensible defaults for everything else
3. Create minimal but functional files
4. Tell them they can refine later

**Quick mode trigger phrases:**
- "quick setup"
- "just the basics"
- "minimal brand"
- "get started fast"

---

## Updating Existing Brand

If a brand already exists:

1. **Read existing files first**
2. **Ask what to update:**
   - Colors only?
   - Voice only?
   - Everything?
3. **Preserve unchanged sections**
4. **Show diff of changes before writing**

---

## Checklist

- [ ] Gather brand name and description
- [ ] Collect all 10 color values (or suggest defaults)
- [ ] Collect 3 font names (or use defaults)
- [ ] Determine asset paths
- [ ] Discover voice through questions
- [ ] Define design principles
- [ ] Generate brand.json
- [ ] Generate config.json
- [ ] Generate tone-of-voice.md
- [ ] Generate brand-system.md
- [ ] Create assets folder
- [ ] Verify all files created
- [ ] Remind user about logo copying
- [ ] Suggest test generation

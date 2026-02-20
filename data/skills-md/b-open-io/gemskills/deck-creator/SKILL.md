---
name: Deck Creator
version: 1.1.0
description: This skill should be used when the user asks to "create a deck", "make a presentation", "build slides", "proposal deck", "pitch deck", "investor deck", "sales presentation", "design a deck", or needs to generate a complete slide deck with consistent visual style. Handles theme selection, copywriting, content planning, and parallel slide generation.
---

# Deck Creator

Create professional presentation decks with consistent visual style, compelling copy, and AI-generated slide images.

## When to Use

Use this skill when the user asks to:
- Create a presentation or slide deck
- Build a pitch deck, proposal, or sales presentation
- Design slides for a product launch, company overview, or partnership
- Generate a complete deck from a document, requirements, or brief
- Restyle an existing deck with a different art style

**IMPORTANT:** This skill must be invoked via the Skill tool (`Skill("deck-creator")`). Do not manually execute the phases without loading this skill first. The skill provides the complete workflow - follow it step by step, do not skip phases.

## Process Overview

The deck creation process follows 4 mandatory phases. **Execute them in order. Do not skip ahead to generation.**

1. **Discovery** - Gather context, examples, and references
2. **Theme** - Establish visual style, color palette, and optional art style
3. **Copy** - Plan and write slide content using marketing principles
4. **Generation** - Create all slides in parallel with consistent style + stitch PDF

## Phase 1: Discovery

Before creating any slides, gather comprehensive information:

### Required Information

Ask these questions to understand the project:

```
1. AUDIENCE: Who is the primary audience? (investors, clients, internal team, partners)
2. PURPOSE: What is the goal? (persuade, inform, propose, sell, educate)
3. CONTEXT: What's the setting? (boardroom, conference, email attachment, webinar)
4. BRAND: Is there existing brand guidelines? (colors, fonts, logos)
5. REFERENCES: Any example decks you like the style of?
6. CONTENT: What documents/materials should inform the content?
   - PDFs, docs, or files to reference
   - Key messages that must be included
   - Topics to cover or avoid
7. LENGTH: How many slides? (recommend 10-16 for most presentations)
8. ASSETS: Any images, logos, or graphics to include?
```

### Reference Analysis

If user provides example decks or references:
- Analyze visual style, layout patterns, and color usage
- Note typography choices and hierarchy
- Identify recurring design elements
- Extract key messaging patterns

## Phase 2: Theme Selection

Establish a consistent visual system before generating slides.

### Option A: Use Theme Factory (Recommended)

Install and use the theme-factory skill for professional color schemes:

```bash
npx skills add anthropics/theme-factory
```

Then invoke to get a cohesive palette:
- Primary color (headlines, accents)
- Secondary color (supporting elements)
- Background color (slide base)
- Text colors (high contrast for readability)
- Accent colors (highlights, CTAs)

### Option B: Manual Theme Definition

If user has brand guidelines, define:

```
Background: #XXXXXX (dark backgrounds work best for projection)
Primary:    #XXXXXX (headlines, key accents)
Secondary:  #XXXXXX (supporting elements)
Text:       #FFFFFF / #000000 (high contrast)
Accent:     #XXXXXX (highlights, CTAs)
```

### Style Parameters

Define consistent visual style:

```yaml
Aspect Ratio: 16:9 (--size 2K produces 1376x768)
Art Style: (optional) Any style from browsing-styles skill (e.g., pixl, cybr, deco)
Typography:
  Headlines: Bold, 48-64px
  Body: Regular, 18-24px
  Stats: Extra Bold, 72-96px
Iconography: Flat, 2px stroke, rounded corners
Layout: Card-based with generous whitespace
```

### Art Style (Optional)

Apply a consistent art style across all slides using the `--style` flag from the generate-image skill. Browse 100+ styles with the `browsing-styles` skill.

When a style is specified:
- Add `--style <id>` to every generation command
- The style's prompt hints are prepended automatically
- Adapt the theme colors and visual descriptions to complement the style
- Note the style in THEME.md for reference

Example styles for decks:
- `pixl` - Pixel art (retro gaming, 8-bit aesthetic)
- `cybr` - Cyberpunk (neon, dark, futuristic)
- `deco` - Art Deco (geometric, elegant, gold accents)
- `minm` - Minimalism (clean, sparse, focused)
- `flat` - Flat Design (solid colors, clean shapes)
- `lpol` - Low Poly (geometric 3D, faceted)

Document the complete theme in a THEME.md file for reference during generation.

## Phase 3: Copy & Content Planning

### Marketing Principles

Apply these copywriting principles:

1. **One Message Per Slide** - Each slide has a single clear takeaway
2. **Headlines Tell the Story** - Someone should understand the deck from headlines alone
3. **Show Don't Tell** - Use visuals, stats, and diagrams over text walls
4. **Problem → Solution → Proof** - Classic persuasion structure
5. **Concrete > Abstract** - Specific numbers beat vague claims
6. **End with Action** - Clear next steps and CTA

### Optional: Marketing Skills

For enhanced copywriting, install:

```bash
npx skills add coreyhaines31/marketingskills
```

### Content Planning Template

Create a DECK-PLAN.md with:

```markdown
# [Deck Title]

## Deck Overview
- Audience:
- Goal:
- Key Message:
- Slides: [10-16]

## Slide Plan

### Slide 1: [Title]
- Type: Title
- Headline:
- Subhead:
- Visual:
- Key Message:

### Slide 2: [Problem/Opportunity]
- Type: Problem Statement
- Headline:
- Content Points:
- Visual:
- Key Message:

[Continue for all slides...]
```

### Content Gathering Loop

**Continue prompting the user until you have enough content for 10-16 slides:**

If information is missing, ask:
- "What specific problem does this solve?"
- "What are the 3-4 key benefits?"
- "What data or proof points support this?"
- "Who are the competitors and how do you differentiate?"
- "What's the timeline or next steps?"
- "What objections might the audience have?"

Do not proceed to generation until the content plan is complete.

## Phase 4: Slide Generation

### Pre-Generation Checklist

Before generating, confirm:
- [ ] Theme defined (colors, typography, style)
- [ ] All slides planned (10-16 slides)
- [ ] Each slide has: headline, content, visual concept
- [ ] Consistent terminology and messaging
- [ ] Output directory created

### Generation Prompts

Each slide prompt should include:

```
Create a professional presentation slide.

**Slide [N]: [Title]**

Specifications:
- Aspect: 16:9 at --size 2K (1376x768)
- Background: [background color]
- Visual style: [defined style - flat, modern, infographic, etc.]
- Art style: [if using --style flag, e.g., "pixel art" for pixl]

Visual elements:
[Describe the visual layout, icons, diagrams, charts]

Text to include:
- Title: "[Headline]" ([primary color], bold)
- [Content elements with positioning]
- Footer: "[Company/Contact]" (small, bottom)

Save to: [output path]/[NN]-[slug].png
```

### Parallel Generation

**Launch all slide generation agents simultaneously** for efficiency.

Spawn one `gemskills:content-specialist` agent per slide using the Task tool. Include in each agent's prompt:
- The complete theme specification (colors, typography, style)
- The slide-specific prompt with layout, text content, and visual elements
- The output path (e.g., `slides/01-title.png`)
- The generate-image command: `cd ${CLAUDE_PLUGIN_ROOT}/skills/generate-image && bun run scripts/generate.ts "prompt" --aspect 16:9 --size 2K [--style <id>] --output <path>`

If an art style was defined in the theme, include `--style <id>` in every generation command.

Launch all agents in a single message for maximum parallelism. Wall-clock time equals the slowest single generation (~30-45 seconds), not N x sequential.

**Rate limiting:** Gemini API may timeout if too many requests fire simultaneously. Limit to 12 parallel generations. For 14+ slide decks, generate in two batches.

If subagents are unavailable, generate slides directly via background Bash commands.

### Post-Generation (Required)

**Every deck MUST end with a stitched PDF. Do not skip this step.**

After all slides are generated, run these steps in order:

#### Step 1: Verify all slides exist

```bash
ls -la slides/*.png | wc -l  # Must match expected slide count
```

If any slides are missing, re-generate them before proceeding.

#### Step 2: Stitch slides into PDF

Try these methods in order. Use the first one that works:

**Method A: ImageMagick (preferred)**
```bash
magick slides/*.png deck.pdf
```

If `magick` is not found:
```bash
brew install imagemagick && magick slides/*.png deck.pdf
```

**Method B: sips + Python (macOS fallback)**
```bash
# Convert each PNG to PDF page
for f in slides/*.png; do sips -s format pdf "$f" --out "${f%.png}.pdf"; done
# Combine with Python
python3 -c "
from PyPDF2 import PdfMerger
import glob
merger = PdfMerger()
for f in sorted(glob.glob('slides/*.pdf')):
    merger.append(f)
merger.write('deck.pdf')
merger.close()
"
```

If PyPDF2 is not installed: `pip3 install PyPDF2`

**Method C: sips only (last resort - produces individual PDFs)**
```bash
for f in slides/*.png; do sips -s format pdf "$f" --out "${f%.png}.pdf"; done
```
Then note in the summary that individual PDFs were created instead of a combined deck.

#### Step 3: Verify PDF

```bash
ls -lh deck.pdf          # Should exist and be non-zero
sips -g pixelWidth -g pixelHeight deck.pdf  # Verify dimensions
```

#### Step 4: Create DECK-INDEX.md

Generate a DECK-INDEX.md with:
- Deck metadata (title, slide count, audience, theme, resolution)
- Slide table (number, file, title, type)
- File tree including deck.pdf

#### Context Discipline

**Do not read generated slide images back into context.** Each slide is a large PNG. With 10-16 slides per deck, reading them back would immediately exhaust the context window. Scripts output only file paths. Ask the user to visually inspect slides and provide feedback.

#### Step 5: Provide Summary

List all slides with file paths and confirm deck.pdf was created.

## Output Structure

```
project/deck/
├── THEME.md           # Visual style definition
├── DECK-PLAN.md       # Content planning document
├── DECK-INDEX.md      # Final deck inventory
├── deck.pdf           # Stitched presentation PDF
└── slides/
    ├── 01-title.png
    ├── 02-problem.png
    ├── 03-solution.png
    ...
    └── 14-closing.png
```

## Slide Type Templates

### Title Slide
- Company/project name
- Tagline or value proposition
- Visual: Abstract or product imagery
- Presenter info (optional)

### Problem/Opportunity
- Pain points or market gap
- Statistics that demonstrate scale
- Visual: Icons, comparison chart

### Solution
- What you're proposing
- Key differentiators
- Visual: Product screenshot or diagram

### How It Works
- Process flow (3-5 steps)
- Visual: Flowchart or numbered steps

### Benefits/Value
- 3-6 key benefits
- Visual: Icon grid or cards

### Social Proof
- Testimonials, logos, case studies
- Visual: Quote cards, logo grid

### Team/About
- Key team members or company info
- Visual: Photos or company timeline

### Metrics/Traction
- Key numbers and growth
- Visual: Charts, gauges, stats

### Competitive Advantage
- Comparison or positioning
- Visual: Matrix, comparison table

### Roadmap/Timeline
- Phases or milestones
- Visual: Horizontal timeline

### Pricing/Plans
- Options and what's included
- Visual: Pricing cards

### Next Steps/CTA
- Clear action items
- Contact information
- Visual: Minimal, focused

### Closing
- Memorable quote or summary
- Contact details
- Visual: Elegant, minimal

## Best Practices

1. **Uniform Style** - Every slide uses the same theme parameters
2. **Consistent Terminology** - Use the same words for concepts throughout
3. **Visual Hierarchy** - Headlines largest, supporting text smaller
4. **Generous Whitespace** - Don't overcrowd slides
5. **Center-Weight Important Elements** - Account for cropping
6. **High Contrast** - Ensure readability on projectors
7. **No Orphan Slides** - Every slide connects to the narrative

## Reference Files

For detailed guidance:
- **`references/slide-types.md`** - Expanded templates for each slide type
- **`references/copywriting.md`** - Marketing copy principles
- **`examples/`** - Example deck plans and outputs
